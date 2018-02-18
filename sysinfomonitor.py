#! /bin/env python3
#sysinfomonitor.py
'''
	Library with system Information
	monitoring functions.
'''

#Imports
import os
import re

'''
	os.uname() returns the following array:
	[OS name, Hostname, Kernel, Version, Architecture]
'''

#Gets the name of the OS
def get_os():
	return os.uname()[0]
	
#Gets the hostname
def get_host():
	return os.uname()[1]

#Gets the kernel
def get_kernel(noarch=False):
	return (os.uname()[2] if noarch == True else re.sub(r"(\.?"+(get_arch())+")", "", os.uname()[2], flags=re.IGNORECASE))

#Gets the version
def get_version():
	return os.uname()[3]

#Gets the architecture
def get_arch():
	return os.uname()[4]
