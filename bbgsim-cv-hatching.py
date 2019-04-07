#!/usr/bin/env python
#
# bbgsim-hatching.py
#
# 

import pynput.mouse as mm
import pynput.keyboard as kk
from random import random as rn

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

def calc_delay(d0, s0, r1, r2):

	if r1 < 0.5:
		r2 = -r2

	return(d0 + s0*r2)


class Lags(object):
	def __init__(self):
		self.cmd_tab = 0.07
		self.between = 0.5

class RobloxControl(object):
	
	def __init__(self):
		self.keyboard = kk.Controller()
		self.keys = kk.Key
		self.mouse = mm.Controller()
		self.button = mm.Button

		self.lags = Lags()

	def after_lag(self):
		time.sleep(self.lags.between)
		return(0)

	def random_move_key(self):
		keys = ['w', 's', 'a', 'd']
		draw = rn()
		i = int(math.floor(rn()*10/len(keys)))
		return(keys[i])


	def move_avatar(self, k, n):
		self.keyboard.press(k)
		time.sleep(n)
		self.keyboard.release(k)
		return(0)

	def cmd_tab(self):
		self.keyboard.press(self.keys.cmd)
		time.sleep(self.lags.cmd_tab)
		self.keyboard.press(self.keys.tab)
		time.sleep(self.lags.cmd_tab)
		self.keyboard.release(self.keys.tab)
		time.sleep(self.lags.cmd_tab)
		self.keyboard.release(self.keys.cmd)
		time.sleep(self.lags.between)

	def move_mouse(self, p):
		# 'alt-tab' away from the game
		self.cmd_tab()
		# set position
		self.mouse.position = p
		# 'alt-tab' back to the game
		self.cmd_tab()
		time.sleep(self.lags.between)

	def set_mouse_pos(self, p):
		self.mouse.position = p

	def click_mouse(self, n):
		# loop with single clicks with a lag in between. without lags
		# the games dont respond fast enough
		for i in range(n):
			self.mouse.click(self.button.left, 1)
			time.sleep(0.05)

		time.sleep(self.lags.between)

	def press_mouse(self):
		self.mouse.press(self.button.left)


mouse_autoButton = (0, 0)
mouse_invAlertClose = (690, 604)
mouse_invOpen = (1055, 775)
mouse_invClear = (227, 598)
mouse_confirm = (431, 863)
mouse_invClose = mouse_invOpen
close_window_pos = (25, 359)

# 'computer vision' class with presets to watch for certain things 
# in games
class RobloxCV(object):
	def __init__(self):
		self.bbgsim

		self.colors = {}
		self.positions = {}

		self.colors["bbgsim"] = {}
		self.colors["bbgsim"]["inv_full"] = [(255, 64, 64), (39, 180, 255)]
		self.colors["bbgsim"]["no_money"] = [(246, 195, 88), (28, 102, 87)]
		self.colors["general"]["disco"] = [(57, 59, 61), (57, 59, 61)]

		self.positions["bbgsim"] = {}
		self.positions["bbgsim"]["inv_full"] = [(690*2, 604*2), (658*2, 604*2)]
		self.positions["bbgsim"]["no_money"] = [(454*2, 877*2), (692*2, 571*2)]
		self.positions["general"]["disco"] = [(696*2, 639*2), (420*2, 629*2)]

		self.img = None
		self.px = None
		self.screenname = "screen.png"

		self.close_window_pos = (25, 359)

		self.control = RobloxControl()

	# use this function to close the roblox game window
	def close_roblox(self):
		self.control.cmd_tab()
		self.control.set_mouse_pos(self.close_window_pos)
		self.control.click_mouse(1)

	# take a screenshot and load it up for downstream analysis
	def screenshot(self):
		os.system("screencapture {}".format(self.screenname))
		time.sleep(0.5)
		self.img = Image.open(self.screenname)
		# load the image's pixel data
		self.px = self.img.load()

	def check_status(self, rtype, rsubtype):

		if self.px is None:
			return(None)

		pos = self.positions[rtype][rsubtype]
		col = self.colors[rtype][rsubtype]
		flag = True

		for i in range(len(pos)):
			obs_col = self.px[pos[i]]
			for j in range(3):
				if obs_col[j] != col[i][j]:
					flag = False

		return flag


	def check_disco(self):
		return self.check_status("general", "disco")

	def check_bbgsim_inv_full(self):
		return self.check_status("bbgsim", "inv_full")

	def check_bbgsim_no_money(self):
		return self.check_status("bbgsim", "no_money")


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


