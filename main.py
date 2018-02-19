#! /bin/env python3
#spec.py
'''
	Main program for monitoring
	your system.
'''

#Imports
import alsaaudio
import curses
from curses import wrapper
import curses.ascii
import math
import psutil
import sys
import time
#END imports

#Custom Imports
from cpumonitor import *
from datetimemonitor import *
from memmonitor import *
from procmonitor import *
from soundmonitor import *
from strfmt import *
from sysinfomonitor import *
#END Custom Imports

#---FUNCTIONS BELOW---#
	
#Main application function
def main(screen=None):
	#Set the timeout
	screen.timeout(250)
	
	#Turn off input echoing
	curses.noecho()
	
	#Enable cbreaking
	curses.cbreak()
	
	#Respond to special keys
	screen.keypad(True)
	
	#Set cursor visibility
	curses.curs_set(0)
	
	#Use terminal colours
	curses.use_default_colors()
	
	#Initial clear
	screen.clear()
	
	#Create the colour list
	curses.init_pair(1, -1, -1) #Clear
	
	curses.init_pair(2, curses.COLOR_MAGENTA, -1) #Magenta
	curses.init_pair(3, curses.COLOR_RED, -1) #Red 
	curses.init_pair(4, 166, -1) #Orange
	curses.init_pair(5, curses.COLOR_YELLOW, -1) #Yellow
	curses.init_pair(6, curses.COLOR_GREEN, -1) #Green
	curses.init_pair(7, curses.COLOR_BLUE, -1) #Blue
	curses.init_pair(8, curses.COLOR_CYAN, -1) #Cyan
	
	curses.init_pair(9, curses.COLOR_WHITE, -1) #White
	curses.init_pair(10, curses.COLOR_BLACK, -1) #Black
	
	#Custom colours
	curses.init_pair(11, 42, -1) #Purplish
	curses.init_pair(12, 231, -1) #Stark white
	curses.init_pair(13, 161, -1) #
	#curses.init_pair(14, , -1) #
	#curses.init_pair(15, , -1) #
	#curses.init_pair(16, , -1) #
	#END colour list
	
	#Create a configuration
	cfg = {
		'GOOD': curses.color_pair(6) | curses.A_BOLD,
		'OKAY': curses.color_pair(5) | curses.A_BOLD,
		'LOW': curses.color_pair(4) | curses.A_BOLD,
		'BAD': curses.color_pair(3) | curses.A_BOLD,
		'CRIT': curses.color_pair(13) | curses.A_BOLD, 
		
		'H1': curses.color_pair(11) | curses.A_BOLD,
		'H2': curses.color_pair(12) | curses.A_BOLD,
		#Just kinda used the HTML tag names <h1> and <h2>
		# b/c I couldn't think of something better, atm.
		# Will probably change this later.
		
		#Generic colours
		'GREEN': curses.color_pair(6) | curses.A_BOLD,
		'YELLOW': curses.color_pair(5) | curses.A_BOLD,
		'RED': curses.color_pair(3) | curses.A_BOLD,
		
		'NONE': curses.color_pair(10) #Clear
	}
	
	#Volume variables
	reset_vol = 50 #Select a default volume to reset to
	mute_vol = 0 #Store muted volume (to reset)
	step = 2 #Set volume step
	vol_bar = "█" #Character to use in volume bar
	
	#Get OS info
	os_name = get_os()
	kernel = get_kernel()
	architecture = get_arch()
	hostname = get_host()
	
	#Get CPU info
	threads = psutil.cpu_count()
	cores = psutil.cpu_count(logical=False)
	max_freq = cpu_max()
	min_freq = cpu_min()
	
	#Get RAM info
	mem_denom = math.pow(2, 20) #Divide memory to achieve desired output
	mem_postfix = "MB"
	mem_tot = mem_total(mem_denom)
	
	#Start the loop
	while True:
		#Clear the screen each time
		screen.clear()
		
		#Get the current time
		##Using this so that the time remains consistent
		time_now = time.time()
		
		#Create a playback mixer
		'''
			Must be done IN loop, because it doesn't seem
			to recognise changes if made outside.
		'''
		pb = alsaaudio.Mixer(control='Master', device='default')
		vols = pb.getvolume()
		max_vol = max(vols)
		min_vol = min(vols)
		
		#Title
		screen.addstr("++SYSTEM INFO++\n", cfg['H1']) #Application header
		
		#Date and time
		screen.addstr(" DATE AND TIME\n", cfg['H1']) #Date/time header
		screen.addstr("  {} {}\n".format(fmt_date(time_now), fmt_localtime(time_now)), cfg['H2']) #Date and time
		
		#System uptime
		screen.addstr(" SYSTEM UPTIME\n", cfg['H1']) #Uptime header
		screen.addstr("  {}\n".format(get_uptime(time_now)), cfg['H2']) #Current uptime
		
		#System info
		screen.addstr(" SYSTEM INFO\n", cfg['H1']) #SysInfo header
		screen.addstr("  OS: {}\n".format(os_name), cfg['H2']) #OS
		screen.addstr("  Kernel: {}\n".format(kernel), cfg['H2']) #Kernel
		screen.addstr("  Arch: {}\n".format(architecture), cfg['H2']) #Architecture
		screen.addstr("  Hostname: {}\n".format(hostname), cfg['H2']) #Hostname
		
		#CPU info
		screen.addstr(" CPU STATUS" + '\n', cfg['H1']) #CPU header
		screen.addstr("  Cores: {}C/{}T @{:7.2f} Mhz\n".format(cores, threads, cpu_current()), cfg['H2'])
		screen.addstr("  Min/Max: {} / {} Mhz\n".format(min_freq, max_freq), cfg['H2'])
		
		cpu_used = psutil.cpu_percent(interval=0, percpu=False)
		screen.addstr("  Utilisation: {}%\n".format(str(cpu_used)), 
			cfg['CRIT'] if cpu_used > 95.0 else cfg['BAD'] if cpu_used > 85.0 else cfg['LOW'] if cpu_used > 70.0 else cfg['OKAY'] if cpu_used > 40.0 else cfg['GOOD'])
			#percpu=True returns each CPU's usage, but this takes up a lot of space
		
		#Memory info
		screen.addstr(" FREE MEMORY\n", cfg['H1']) #Memory header
		
		perc_used = mem_perc(mem_denom, mem_tot)
		screen.addstr("  {:.0f} {} / {:.0f} {} ({:.2f}%)\n".format(mem_used(mem_denom), mem_postfix, mem_tot, mem_postfix, perc_used), 
			cfg['CRIT'] if perc_used < 15.0 else cfg['BAD'] if perc_used < 25.0 else cfg['LOW'] if perc_used < 30.0 else cfg['OKAY'] if perc_used < 40.0 else cfg['GOOD'])
		
		#Process count
		screen.addstr(" PROCESSES\n", cfg['H1']) #Processes header
		screen.addstr("  Count: {}\n".format(str(get_pids(True))), cfg['H2']) #Count of processes
		
		#Volume management
		lv, _ = divmod(vols[0], 5)
		rv, _ = divmod(vols[1], 5)
		lbarg = vol_bar * (lv if lv < 8 else 8)
		rbarg = vol_bar * (rv if rv < 8 else 8)
		lbary = vol_bar * (lv - 8 if (lv < 16) else 8)
		rbary = vol_bar * (rv - 8 if (rv < 16) else 8)
		lbarr = vol_bar * (lv - 16 if (lv < 20) else 4)
		rbarr = vol_bar * (lv - 16 if (rv < 20) else 4)
		screen.addstr(" VOLUME\n", cfg['H1'])
		screen.addstr("  L ({:3}%):".format(vols[0]), cfg['H2'])
		screen.addstr(lbarg, cfg['GREEN'])
		screen.addstr("{}".format(lbary), cfg['YELLOW'])
		screen.addstr("{}".format(lbarr), cfg['RED'])
		screen.addstr("\n")
		screen.addstr("  R ({:3}%):".format(vols[1]), cfg['H2'])
		screen.addstr(rbarg, cfg['GREEN'])
		screen.addstr("{}".format(rbary), cfg['YELLOW'])
		screen.addstr("{}".format(rbarr), cfg['RED'])
		screen.addstr("\n")
		screen.addstr("  Stored mute volume: {}\n".format(str(mute_vol)), cfg['H2'])
		screen.addstr("  Configured reset volume: {}\n".format(str(reset_vol)), cfg['H2'])
		
		#Get the key
		key = screen.getch()
		#RAISE the volume
		if key in [ord("A"), ord("a")]: #Both up
			inc_volume(pb, max_vol, step)
		#LOWER the volume
		elif key in [ord("Z"), ord("z")]: #Both down
			dec_volume(pb, min_vol, step)
		#RESET the volume
		elif key in [ord("R"), ord("r")]:
			reset_volume(pb, reset_vol)
		#MUTE the volume
		elif key in [ord("M"), ord("m")]:
			mute_vol = mute_volume(pb, mute_vol, max_vol)
		elif key in [
				27, #Escape
				#10, #Enter
				ord("q"),
				ord("Q")
			]:
			break

#Run the program
curses.wrapper(main)
#main()
