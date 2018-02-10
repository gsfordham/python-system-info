'''A script for Python OS monitoring'''

#imports
import io
import math
import os
import psutil
import re
import time

#Format a string output and return a buffer
def sprintf(format, *args):
	buf = io.StringIO()
	buf.write(format % args)
	return(buf.getvalue())

def main():
	while True:
		#Clear the screen
		os.system('cls' if os.name == 'nt' else 'clear')
		
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
		out_list.append("++SYSTEM INFO++")
		
		#Date and time
		out_list.append(" DATE AND TIME")
		out_list.append(sprintf("  Time: %s\n  Date: %s\n", time.strftime("%H:%M:%S", time.localtime(time_now)), time.strftime("%Y-%b-%d, %A", time.localtime(time_now))))
		
		#System uptime
		out_list.append(" SYSTEM UPTIME")
		out_list.append(sprintf("  %s\n  Total seconds: %d\n", str(uptime_final), (time_now - boot_time)))
		#out_list.append(sprintf("  (%d seconds)\n", (time_now - boot_time)))
		
		#System info
		out_list.append(" SYSTEM INFO")
		#print(sprintf("\t%s\n\t%s\n\t%s\n\t%s\n", sysinfo['sysname'], sysinfo['nodename'], sysinfo['release'], sysinfo['machine']))
		out_list.append(sprintf("  OS: %s\n  Kernel: %s\n  Arch: %s\n  Hostname: %s\n", sysinfo[0], re.sub(r"(\.?"+(sysinfo[4])+")", "", sysinfo[2], flags=re.IGNORECASE), sysinfo[4], sysinfo[1]))
		
		#CPU info
		out_list.append(" CPU INFO")
		out_list.append(sprintf("  Cores: %dC/%dT @%7.2f Mhz", psutil.cpu_count(logical=False), psutil.cpu_count(), cpu_list[0]))
		out_list.append(sprintf("  Min/Max: %d / %d Mhz", cpu_list[1], cpu_list[2]))
		out_list.append(sprintf("  Utilisation: %s%%\n", str(psutil.cpu_percent(interval=0, percpu=False))))
			#percpu=True returns each CPU's usage, but this takes up a lot of space
		
		#Memory info
		out_list.append(" MEMORY INFO")
		#svmem(total, available, percent, used, free, active, inactive, buffers, cached, shared)
		out_list.append((sprintf("  %d %s / %d %s (%.2f%%)\n", mem_used, mem_postfix, mem_left, mem_postfix, ((mem_used / mem_left) * 100))))
		
		#Process count
		out_list.append(sprintf(" PROCESSES\n  Count: %d", len(pids)))
		
		#Print all output
		for i in out_list:
			print(i)
			
		#Print line at a delay
		'''for i in range(20):
			print("-", end='', flush=True)
			time.sleep(0.05)'''
		#print()
		
		#Pause before next iteration
		time.sleep(1)

#Run the program
main()
