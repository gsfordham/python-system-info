#! /bin/env python3
#procmonitor.py
'''
	Library with process-monitoring
	functions.
'''

#Imports
import psutil

'''
	This function will return the process
	count for the system.
'''
def get_pids(count=False):
	pids = psutil.pids()
	return (pids if count == False else len(pids))
