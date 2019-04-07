#!/usr/bin/env python
#
# bbgsim-hatching.py
#
# 

import pynput.mouse as mm
import pynput.keyboard as kk
from random import random as rn

import time
import sys

##
## this script automates hatching eggs in bubblegum simulator. 
## to allow it to run for long periods of time the script has 
## to click the "auto" hatch button and then every 10 minutes
## on average it needs to move the character away from the egg, 
## click on the pets button, click the delete all unlocked button, 
## close the pet dialog, and walk back to the egg
##

## pseudo code

##
## while TRUE: 
##   click "auto" button (TODO: hard-code the mouse position)
##   wait 10ish minutes
##   press 'S' for 0.5 seconds? (Test this to see if it moves far enough)
##   click "inventory is full" x (may not be on screen) (TODO: hard-code mouse position)
##   click pet inventory button (TODO: hard-code mouse position)
##   click delete unlocked button (TODO: hard-code mouse position)
##   click close inventory button (TODO: hard-code mouse position)
##   press 'W' for 0.5 seconds (same time as before hopefully this puts the character back into the same position)
## 

mc = mm.Controller()
mb = mm.Button

kc = kk.Controller()
ke = kk.Key

rand1 = 0
rand2 = 0

def calc_delay(d0, s0, r1, r2):

	if r1 < 0.5:
		r2 = -r2

	return(d0 + s0*r2)


mouse_autoButton = (0, 0)
mouse_invAlertClose = (-593, 1199)
mouse_invOpen = (-288, 1358)
mouse_invClear = (-1034, 1162)
mouse_confirm = (-830, 1444)
mouse_invClose = mouse_invOpen

mouse_autoButton = (0, 0)
mouse_invAlertClose = (786, 591)
mouse_invOpen = (1055, 775)
mouse_invClear = (227, 598)
mouse_confirm = (431, 863)
mouse_invClose = mouse_invOpen

countdown = 5
# time to wait for hatching
hatch_time = 600
hatch_spread = 30
walk_time = 0.7
after_click_delay = 2
press_delay = 0.07
standard_delay = 0.95

print("Make sure to bring game to foreground and click in it to capture the mouse")
print("Starting in\n> 5...")
while countdown > 0:
	countdown = countdown - 1
	time.sleep(1)
	print("> {}...".format(countdown))
i = 0

while True:
	i = i + 1
	print("Starting loop {}".format(i))

	# set position
	#mc.position = mouse_autoButton
	# click button
	#mc.click(mb.left, 1)

	# start hatching
	kc.press('t')
	time.sleep(press_delay)
	kc.release('t')

	# wait about 10 minutes
	#time.sleep(567)
	time.sleep(calc_delay(hatch_time, hatch_spread, rn(), rn()))
	
	# walk away from egg
	kc.press('s')
	time.sleep(walk_time)
	kc.release('s')
	#kc.press(ke.space)
	#time.sleep(8)
	#kc.release(ke.space)

	# wait a few seconds in case some hatching is still going on
	time.sleep(10)

	# possibly close the inventory full alert box

	if False:

		print("Closing inventory full alert (possibly)")
		
		# cmd-tab away to give the system back the mouse
		kc.press(ke.cmd)
		time.sleep(press_delay)
		kc.press(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.cmd)
		time.sleep(standard_delay)

		# set position
		mc.position = mouse_invAlertClose
		time.sleep(standard_delay)

		kc.press(ke.cmd)
		time.sleep(press_delay)
		kc.press(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.cmd)
		time.sleep(standard_delay)

		# click into game window
		mc.click(mb.left, 1)
		time.sleep(standard_delay)

	# open inventory
	print("Opening inventory")

	# cmd-tab away to give the system back the mouse
	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	# set position
	mc.position = mouse_invOpen
	time.sleep(standard_delay)

	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	# click into game window
	mc.click(mb.left, 1)
	time.sleep(standard_delay)

	# clear inventory
	print("Clearing inventory")

	# cmd-tab away to give the system back the mouse
	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	mc.position = mouse_invClear
	time.sleep(press_delay)

	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	# click into game window
	mc.click(mb.left, 1)
	time.sleep(standard_delay)

	print("Confirming clear")

	# cmd-tab away to give the system back the mouse
	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	mc.position = mouse_confirm
	time.sleep(standard_delay)

	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	# click into game window
	mc.click(mb.left, 1)
	time.sleep(standard_delay)

	print("Closing inventory")

	# cmd-tab away to give the system back the mouse
	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	mc.position = mouse_invClose
	time.sleep(standard_delay)

	kc.press(ke.cmd)
	time.sleep(press_delay)
	kc.press(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.tab)
	time.sleep(press_delay)
	kc.release(ke.cmd)
	time.sleep(standard_delay)

	# click into game window
	mc.click(mb.left, 1)
	time.sleep(standard_delay)

	# walk back
	kc.press('w')
	time.sleep(walk_time)
	kc.release('w')
	time.sleep(standard_delay)

