#! /usr/env python3
#main.py

#Imports
import alsaaudio
#END imports

#Volume functions
#Reset volume
def reset_volume(mx, rv):
	#Mixer, Reset Volume
	cond1 = isinstance(rv, int) and rv != None
	cond2 = isinstance(mx, alsaaudio.Mixer) and mx != None
	if cond1 and cond2:
		#Configuration is too high
		if rv > 100:
			mx.setvolume(100)
		#Configuration is too low
		elif rv < 0:
			mx.setvolume(0)
		else: #Configuration is valid
			mx.setvolume(rv)
		return True
	else:
		return False
	
#Mute volume
def mute_volume(mx, muv, mav):
	#Mixer, Mute Volume, Max Volume
	cond1 = isinstance(muv, int) and muv != None
	cond2 = isinstance(mav, int) and mav != None
	cond3 = isinstance(mx, alsaaudio.Mixer) and mx != None
	if cond1 and cond2 and cond3:
		if mav > 0:
			muv = mav
			mx.setvolume(0)
		else:
			mx.setvolume(muv)
		return muv
	else:
		return muv

#Increase volume
def inc_volume(mx, mav, step):
	#Mixer, Mute Volume, Max Volume
	cond1 = isinstance(step, int) and step != None
	cond2 = isinstance(mav, int) and mav != None
	cond3 = isinstance(mx, alsaaudio.Mixer) and mx != None
	if cond1 and cond2 and cond3:
		#Highest channel + step exceeds max volume
		if mav > (100 - step):
			mx.setvolume(100)
		else:
			mx.setvolume(mav + step)
		return True
	else:
		return False

#Decrease volume
def dec_volume(mx, miv, step):
	#Mixer, Mute Volume, Max Volume
	cond1 = isinstance(step, int) and step != None
	cond2 = isinstance(miv, int) and miv != None
	cond3 = isinstance(mx, alsaaudio.Mixer) and mx != None
	if cond1 and cond2 and cond3:
		#Lowering by one step is less than muted
		if miv < step:
			mx.setvolume(0)
		else:
			mx.setvolume(miv - step)
		return True
	else:
		return False
#END volume functions
