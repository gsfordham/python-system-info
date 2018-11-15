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
	uptime = (time_now - boot_time)
	
	m, s = divmod(uptime, 60) #Mins, Secs
	h, m = divmod(m, 60) #Hours, Mins
	d, h = divmod(h, 24) #Days, Hours
	dt = d #Store total days
	w, d = divmod(d, 7) #Weeks, Days
	
	dp = ('' if d == 1 else 's') #Is days plural?
	dtp = ('' if dt == 1 else 's') #Total days plural?
	wp = ('' if w == 1 else 's') #Weeks plural?
	
	return("{:,.0f} ".format(dt) +
		("day%s, %02d:%02d:%02d\n  " % (dtp, h, m, s)) +
		("({:,.0f} seconds)".format(uptime)) +
		("\n  (") +
		("{:,.0f} week".format(w)) +
		("%s and %d day%s)" % (wp, d, dp)))

#Get the current time
def get_localtime(arg=None):
	return time.localtime(arg if (arg != None and isinstance(arg, int)) else time.time())
	

#Get string-formatted current time
def fmt_localtime(arg=None):
	return time.strftime("%H:%M:%S", (arg if arg != None and isinstance(arg, int) else get_localtime()))
	
#Get string-formatted current date
def fmt_date(arg=None):
	return time.strftime("%Y-%b-%d, %a", (arg if arg != None and isinstance(arg, int) else get_localtime()))
