#!/usr/bin/env python
#
# bbgsim-hatching.py
#
# 

import pynput.mouse as mm
import pynput.keyboard as kk
from random import random as rn
from math import floor

import os
from PIL import Image

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


def cmd_tab(kbd, kbk):
	press_delay = 0.07
	standard_delay = 0.25
	kbd.press(kbk.cmd)
	time.sleep(press_delay)
	kbd.press(kbk.tab)
	time.sleep(press_delay)
	kbd.release(kbk.tab)
	time.sleep(press_delay)
	kbd.release(kbk.cmd)
	time.sleep(standard_delay)

box_ul = (247, 428)
box_lr = (1044, 943)

box_ul_im = (box_ul[0]*2, box_ul[1]*2)
box_lr_im = (box_lr[0]*2, box_lr[1]*2)

box_width = box_lr_im[0] - box_ul_im[0]
box_height = box_lr_im[1] - box_ul_im[1]

# void coin colors
color_1 = (120, 12, 112)
color_2 = (250, 0, 250)
time.sleep(3)

os.system("screencapture foo.png")
im = Image.open("foo.png")
px = im.load()

for i in range(0, box_width, 3):
	for j in range(0, box_height, 3):
		pos = (box_ul_im[0] + i, box_ul_im[1] + j)
		cv = px[pos]
		print(cv)
		match = True
		for k in range(3):
			if cv[k] != color_1[k]:
				match = False
				

		if not match:
			match = True
			for k in range(3):
				if cv[k] != color_2[k]:
					match = False
		
		if match:
			# found a spot that is probably a coin i guess
			# calculate mouse position
			mpos = (floor(pos[0] / 2.0), floor(pos[1] / 2.0))
			cmd_tab(kc, ke)
			mouse.position = mpos
			time.sleep(0.05)
			cmd_tab(kc, ke)
			print("is this a coin????")
			sys.exit(0)



sys.exit(0)

mouse_autoButton = (0, 0)
mouse_invAlertClose = (690, 604)
mouse_invOpen = (1055, 775)
mouse_invClear = (227, 598)
mouse_confirm = (431, 863)
mouse_invClose = mouse_invOpen

# screencapture on my computer produces an image that's double the
# pixel resolution as reported by pynput.mouse so we have to double
# the position values for scanning the image for colors
chk_1_pos = (mouse_invAlertClose[0]*2, mouse_invAlertClose[1]*2)
# expected colors to find at the inventory full button location
# to trigger the inventory clearning process
chk_1_col = (255, 64, 64)

chk_2_pos = (658*2, 604*2)
chk_2_col = (39, 180, 255)

# this should help identify the dialog that comes up when we are out of currency
chk_3_pos = (454*2, 877*2)
chk_3_col = (246, 195, 88)

chk_4_pos = (692*2, 571*2)
chk_4_col = (28, 102, 87)

# these are used to detect disconnections
chk_5_pos = (696*2, 639*2)
chk_5_col = (57, 59, 61)

chk_6_pos = (420*2, 629*2)
chk_6_col = (57, 59, 61)

close_window_pos = (25, 359)

countdown = 5
# time to wait for hatching
hatch_time = 60
hatch_spread = 0
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

loop_count = 1
print("Starting loop {}".format(loop_count))

while True:
	
	kc.press('w')
	time.sleep(0.05)
	kc.release('w')

	kc.press('t')
	time.sleep(press_delay)
	kc.release('t')

	# wait for some hatching to happen
	time.sleep(hatch_time)

	# take a screenshot
	print("checking screen...")
	os.system("screencapture screen.png")

	# open it and figure if we're looking at a full inventory alert
	# based on the RGB values at two positions of the alert dialog

	im = Image.open("screen.png")
	# load the image's pixel data
	px = im.load()

	## 
	## first check for disconnection
	##

	disco = True

	obs_color = px[chk_5_pos]
	for i in range(3):
		if obs_color[i] != chk_5_col[i]:
			disco = False

	obs_color = px[chk_6_pos]
	for i in range(3):
		if obs_color[i] != chk_6_col[i]:
			disco = False

	if disco:
		print("disconnected")
		# close the window...

		kc.press(ke.cmd)
		time.sleep(press_delay)
		kc.press(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.cmd)
		time.sleep(standard_delay)

		# set position
		mc.position = close_window_pos
		mc.click(mb.left, 1)

		sys.exit(1)

	##
	## now chedk for being out of money
	##

	out_of_money = True

	obs_color = px[chk_3_pos]
	for i in range(3):
		if obs_color[i] != chk_3_col[i]:
			out_of_money = False

	obs_color = px[chk_4_pos]
	for i in range(3):
		if obs_color[i] != chk_4_col[i]:
			out_of_money = False

	if out_of_money:
		print("OUT OF MONEY BRO")
		print("waiting 5 minutes then disconnecting")
		time.sleep(300)

		kc.press(ke.cmd)
		time.sleep(press_delay)
		kc.press(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.tab)
		time.sleep(press_delay)
		kc.release(ke.cmd)
		time.sleep(standard_delay)

		# set position
		mc.position = close_window_pos
		mc.click(mb.left, 1)

		sys.exit(1)


		#sys.exit(1)
		continue

	# now check if we have a full inventory
	# assume match
	match = True

	obs_color = px[chk_1_pos]
	for i in range(3):
		if obs_color[i] != chk_1_col[i]:
			match = False

	obs_color = px[chk_2_pos]
	for i in range(3):
		if obs_color[i] != chk_2_col[i]:
			match = False

	if not match:
		print("STILL HATCHING")

	else:
		print("INVENTORY IS FULL BRO")


		# ok now we have to close the dialog

		print("Closing alert")

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

		# clear inventory

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

		# increment number of fills
		loop_count = loop_count + 1
		print("Starting loop {}".format(loop_count))


