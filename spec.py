'''A script for Python OS monitoring'''

#imports
import io
import math
import os
import psutil
import re
import time

'''Class of colours:
	These are ANSI escape codes for the terminal.
	To make use of them, your terminal must support
	coloured text.
'''
class Colours:
	'''
		NOTE: The ACTUAL colours you see will
		depend on your system scheme. These
		are just the names I got off a site listing
		ANSI colours.
	'''
	COLOURS = {
		'CLEAR': '\033[0m',
		
		'WHITE': '\033[1;37m',
		'BLACK': '\033[0;30m',
		'GREY': '\033[0;30m',
		'LIGHT_GREY': '\033[0;37m',
		
		'RED': '\033[0;31m',
		'LIGHT_RED': '\033[1;31m',
		'ORANGE': '\033[0;33m',
		'BROWN': '\033[0;33m', #Same as orange
		'YELLOW': '\033[1;33m',
		'GREEN': '\033[0;32m',
		'LIGHT_GREEN': '\033[1;32m',
		'BLUE': '\033[0;34m',
		'LIGHT_BLUE': '\033[1;34m',
		'CYAN': '\033[0;36m',
		'LIGHT_CYAN': '\033[1;36m',
		'PURPLE': '\033[0;35m',
		'LIGHT_PURPLE': '\033[1;35m'
	}
	
	#Return the colour code for a specific colour
	def get_colour(self, col):
		#Colour is valid type
		if isinstance(col, str):
			#Uppercase each
			c_out = col.upper()
			
			#Colour configured is valid
			if c_out in self.COLOURS and not (self.COLOURS[c_out] is None):
				return self.COLOURS[c_out]
			else: #Colour is invalid
				print("WARNING: Colour selected '" + c_out +
					"' is invalid.\n" +
					"Returning CLEAR, instead.\n" +
					"Press ENTER to continue: "
				)
				input()
				return self.COLOURS['CLEAR']
		else: #Type of one or more args is invalid
			print(
				"WARNING: One or more of the arguments passed " +
				"is invalid. Want: str. " +
				"Got: (" + str(type(col)) + ")\n" +
				"For function: get_colour(). Please check " +
				"your configuration.\nReturning CLEAR, instead.\n" +
				"Press ENTER to continue: "
			)
			input()
			return self.COLOURS['CLEAR']
#END Colours Class

#---FUNCTIONS BELOW---#

#Format a string output and return a buffer
def sprintf(format, *args):
	buf = io.StringIO()
	buf.write(format % args)
	return(buf.getvalue())

def do_clear():
	os.system('cls' if os.name == 'nt' else 'clear')

#Main application function
def main():
	#Initial clear
	do_clear()
	
	#Create the colour list
	cols = Colours()
	
	#Create a configuration
	cfg = {
		'GOOD': cols.get_colour("green"),
		'OKAY': cols.get_colour("yellow"),
		'LOW': cols.get_colour("orange"),
		'BAD': cols.get_colour("light_red"),
		'CRIT': cols.get_colour("red"),
		
		'H1': cols.get_colour("light_purple"), #Primary header colour
		'H2': cols.get_colour("white"), #Secondary header colour
		#Just kinda used the HTML tag names <h1> and <h2>
		# b/c I couldn't think of something better, atm.
		# Will probably change this later.
		
		'NONE': cols.get_colour("clear")
	}
	
	#Start the loop
	while True:
		#Clear the screen each time
		do_clear()
		
		#Get the current time
		time_now = time.time()
		
		#Get time since boot
		boot_time = psutil.boot_time()
		#Convert uptime
		uptime_raw = time.strftime("%H:%M:%S", time.gmtime(time_now - boot_time))
		uptime_split = uptime_raw.split(':')
		uptime_days, uptime_hours = divmod(int(uptime_split[0]), 24)
		uptime_final = sprintf("%d d, %s:%s:%s", uptime_days, str(uptime_hours).zfill(2), uptime_split[1], uptime_split[2])
		
		#Get system info
		sysinfo = os.uname()
		
		#Get CPU info
		cpu_list = psutil.cpu_freq()
		
		#Get memory info
		memory = psutil.virtual_memory()
		mem_denom = math.pow(2, 20) #Divide memory to achieve desired output
		mem_postfix = "MB"
		mem_used = (memory[1] / mem_denom)
		mem_left = (memory[0] / mem_denom)
		
		#Get list of process IDs
		pids = psutil.pids()
		
		#Create list
		out_list = []
		
		#Title
		out_list.append(cfg['H1'] + "++SYSTEM INFO++")
		
		#Date and time
		out_list.append(cfg['H1'] + " DATE AND TIME" + cfg['H2'])
		out_list.append(sprintf("  Time: %s\n  Date: %s\n", time.strftime("%H:%M:%S", time.localtime(time_now)), time.strftime("%Y-%b-%d, %A", time.localtime(time_now))))
		
		#System uptime
		out_list.append(cfg['H1'] + " SYSTEM UPTIME" + cfg['H2'])
		out_list.append(sprintf("  %s\n  Total seconds: %d\n", str(uptime_final), (time_now - boot_time)))
		#out_list.append(sprintf("  (%d seconds)\n", (time_now - boot_time)))
		
		#System info
		out_list.append(cfg['H1'] + " SYSTEM INFO" + cfg['H2'])
		#print(sprintf("\t%s\n\t%s\n\t%s\n\t%s\n", sysinfo['sysname'], sysinfo['nodename'], sysinfo['release'], sysinfo['machine']))
		out_list.append(sprintf("  OS: %s\n  Kernel: %s\n  Arch: %s\n  Hostname: %s\n", sysinfo[0], re.sub(r"(\.?"+(sysinfo[4])+")", "", sysinfo[2], flags=re.IGNORECASE), sysinfo[4], sysinfo[1]))
		
		#CPU info
		out_list.append(cfg['H1'] + " CPU INFO" + cfg['H2'])
		out_list.append(sprintf("  Cores: %dC/%dT @%7.2f Mhz", psutil.cpu_count(logical=False), psutil.cpu_count(), cpu_list[0]))
		out_list.append(sprintf("  Min/Max: %d / %d Mhz", cpu_list[1], cpu_list[2]))
		out_list.append(sprintf("  Utilisation: %s%%\n", str(psutil.cpu_percent(interval=0, percpu=False))))
			#percpu=True returns each CPU's usage, but this takes up a lot of space
		
		#Memory info
		out_list.append(cfg['H1'] + " MEMORY INFO" + cfg['H2'])
		#svmem(total, available, percent, used, free, active, inactive, buffers, cached, shared)
		out_list.append((sprintf("  %d %s / %d %s (%.2f%%)\n", mem_used, mem_postfix, mem_left, mem_postfix, ((mem_used / mem_left) * 100))))
		
		#Process count
		out_list.append(cfg['H1'] + " PROCESSES" + cfg['H2'])#sprintf(" PROCESSES\n  Count: %d", len(pids)))
		out_list.append("  Count: " + str(len(pids)))
		
		#Print all output
		for i in out_list:
			print(i)
		
		#Clear the colours
		print(cfg['NONE'], end='', flush=True)
		time.sleep(1)

#Run the program
main()
