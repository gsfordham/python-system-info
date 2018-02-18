#! /bin/env python3
#spec.py
'''
	Main program for monitoring
	your system.
'''

#Imports
import curses
from curses import wrapper
import curses.ascii
import math
import os
import psutil
import sys
import time
#END imports

#Custom Imports
from cpumonitor import *
from datetimemonitor import *
from memmonitor import *
from procmonitor import *
from strfmt import *
from sysinfomonitor import *
#END Custom Imports

#---FUNCTIONS BELOW---#

def do_clear():
	os.system('clear')
	'''
		os.system('cls' if os.name == 'nt' else 'clear')
		Remnant of possible cross-plat version.
		Unsure if I will use at a later point.
	'''
	
#Main application function
def main(screen=None):
	#Set the timeout
	screen.timeout(1000)
	
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
	#do_clear()
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
		
		'NONE': curses.color_pair(10) #Clear
	}
	
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
		#do_clear()
		screen.clear()
		
		#Get the current time
		##Using this so that the time remains consistent
		time_now = time.time()
		
		#Create list
		out_list = []
		
		#Title
		screen.addstr("++SYSTEM INFO++" + '\n', cfg['H1']) #Application header
		
		#Date and time
		screen.addstr(" DATE AND TIME" + '\n', cfg['H1']) #Date/time header
		#out_list.append(sprintf("  Time: %s\n  Date: %s\n", fmt_localtime(time_now), fmt_date(time_now)))
		screen.addstr("  " + fmt_date(time_now) + " " + fmt_localtime(time_now) + '\n', cfg['H2']) #Date and time
		
		#System uptime
		screen.addstr(" SYSTEM UPTIME" + '\n', cfg['H1']) #Uptime header
		screen.addstr("  " + get_uptime(time_now) + '\n', cfg['H2']) #Current uptime
		
		#System info
		screen.addstr(" SYSTEM INFO" + '\n', cfg['H1']) #SysInfo header
		screen.addstr("  OS: " + os_name + '\n', cfg['H2']) #OS
		screen.addstr("  Kernel: " + kernel + '\n', cfg['H2']) #Kernel
		screen.addstr("  Arch: " + architecture + '\n', cfg['H2']) #Architecture
		screen.addstr("  Hostname: " + hostname + '\n', cfg['H2']) #Hostname
		
		#CPU info
		screen.addstr(" CPU STATUS" + '\n', cfg['H1']) #CPU header
		screen.addstr(sprintf("  Cores: %dC/%dT @%7.2f Mhz\n", cores, threads, cpu_current()), cfg['H2'])
		screen.addstr(sprintf("  Min/Max: %d / %d Mhz\n", min_freq, max_freq), cfg['H2'])
		
		cpu_used = psutil.cpu_percent(interval=0, percpu=False)
		screen.addstr(sprintf("  Utilisation: %s%%\n", str(cpu_used)), 
			cfg['CRIT'] if cpu_used > 95.0 else cfg['BAD'] if cpu_used > 85.0 else cfg['LOW'] if cpu_used > 70.0 else cfg['OKAY'] if cpu_used > 40.0 else cfg['GOOD'])
			#percpu=True returns each CPU's usage, but this takes up a lot of space
		
		#Memory info
		screen.addstr(" FREE MEMORY" + '\n', cfg['H1']) #Memory header
		
		perc_used = mem_perc(mem_denom, mem_tot)
		screen.addstr(sprintf("  %d %s / %d %s (%.2f%%)\n", mem_used(mem_denom), mem_postfix, mem_tot, mem_postfix, perc_used), 
			cfg['CRIT'] if perc_used < 15.0 else cfg['BAD'] if perc_used < 25.0 else cfg['LOW'] if perc_used < 30.0 else cfg['OKAY'] if perc_used < 40.0 else cfg['GOOD'])
		
		#Process count
		screen.addstr(" PROCESSES" + '\n', cfg['H1']) #Processes header
		screen.addstr("  Count: " + str(get_pids(True)) + '\n', cfg['H2']) #Count of processes
		
		#Print all output
		'''for i in out_list:
			#print(i)
			screen.addstr(i + '\n')
		'''
		#Clear the colours
		print(cfg['NONE'], end='', flush=True)
		key = screen.getch()
		if key in [
				27, #Escape
				#10, #Enter
				ord("q"),
				ord("Q")
			]:
			break

#Run the program
curses.wrapper(main)
#main()
