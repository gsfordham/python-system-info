#! /bin/env python3
#cpumonitor.py
'''
	Library for getting information
	on the system's CPU.
'''

#Imports
import psutil

#Get current CPU frequency
def cpu_current():
	return psutil.cpu_freq()[0]

#Get CPU min frequency
def cpu_min():
	return psutil.cpu_freq()[1]

#Get CPU max frequency
def cpu_max():
	return psutil.cpu_freq()[2]
