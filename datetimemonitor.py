#! /bin/env python3
#datetimemonitor.py
'''
	Library of functions that handle
	various date and time purposes.
'''

#Imports
import psutil
import time

#Custom Imports
from strfmt import *
#END Custom Imports

'''
	Gets the uptime as a string, formatted as
	Days, Hours:Minutes:Seconds (Seconds)
'''
def get_uptime(arg=None):
	time_now = (arg if (arg is not None and isinstance(arg, int)) else time.time()) #Current time
	boot_time = psutil.boot_time() #Boot time
	uptime_raw = time.strftime("%H:%M:%S", time.gmtime(time_now - boot_time))
	uptime_split = uptime_raw.split(':') #Split the raw uptime
	
	#Divide hours (uptime_split[0]) by 24 to get days
	uptime_days, uptime_hours = divmod(int(uptime_split[0]), 24)
	
	#Return formatted string using a sprintf buffer
	return (
		sprintf("%d days, %s:%s:%s (%d s)",
			uptime_days, 
			str(uptime_hours).zfill(2), 
			uptime_split[1], 
			uptime_split[2],
			(time_now - boot_time)
		)
	)

#Get the current time
def get_localtime(arg=None):
	return time.localtime(arg if (arg != None and isinstance(arg, int)) else time.time())
	

#Get string-formatted current time
def fmt_localtime(arg=None):
	return time.strftime("%H:%M:%S", (arg if arg != None and isinstance(arg, int) else get_localtime()))
	
#Get string-formatted current date
def fmt_date(arg=None):
	return time.strftime("%Y-%b-%d, %a", (arg if arg != None and isinstance(arg, int) else get_localtime()))
