#! /bin/env python3
#memmonitor.py
'''
	This library contains functions for
	monitoring memory.
'''

#Imports
import psutil

#Get total RAM
def mem_total(denom=None):
	return (psutil.virtual_memory()[0] / (denom if denom != None and denom != 0 and isinstance(denom, (int, float, complex)) else 1))

#Get used RAM
def mem_used(denom=None):
	return (psutil.virtual_memory()[1] / (denom if denom != None and denom != 0 and isinstance(denom, (int, float, complex)) else 1))

#Get percentage of memory used
def mem_perc(denom=None, mem_tot=None):
	if denom != None and denom != 0 and isinstance(denom, (int, float, complex)):
		return (mem_used(denom) / (mem_tot if mem_tot != None and mem_tot != 0 and isinstance(mem_tot, (int, float, complex)) else mem_total(denom)) * 100)
	else:
		return 0.00
