#! /bin/env python3
#strfmt.py

#Imports
import io
import sys

#A standard C-style printf
#Format a string and print it directly
def printf(format, *args):
	sys.stdout.write(format % args)

#A standard C-style sprintf
#Format a string output and return a buffer
def sprintf(format, *args):
	buf = io.StringIO()
	buf.write(format % args)
	return(buf.getvalue())
