#!/usr/bin/env python

from pynput import mouse as mm
from pynput import keyboard as kk
from PIL import Image
import os
import time
from random import random
import math

class Lags(object):
	def __init__(self):
		self.cmd_tab = 0.07
		self.between = 0.5
		self.short_between = 0.18

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
		draw = random()
		i = int(math.floor(random()*10/len(keys)))
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

	def click_mouse(self, n, short_lag=False):
		# loop with single clicks with a lag in between. without lags
		# the games dont respond fast enough
		for i in range(n):
			self.mouse.click(self.button.left, 1)
			time.sleep(0.05)

		if short_lag:
			time.sleep(self.lags.short_between)
		else:
			time.sleep(self.lags.between)

		return(0)

	def press_mouse(self):
		self.mouse.press(self.button.left)


# 'computer vision' class with presets to watch for certain things 
# in games
class RobloxCV(object):
	def __init__(self):

		self.colors = {}
		self.positions = {}

		self.colors["bbgsim"] = {}
		self.colors["general"] = {}
		self.colors["ptrainer"] = {}

		self.colors["bbgsim"]["inv_full"] = [(255, 64, 64), (39, 180, 255)]
		self.colors["bbgsim"]["no_money"] = [(246, 195, 88), (28, 102, 87)]
		self.colors["general"]["disco"] = [(57, 59, 61), (57, 59, 61)]
		self.colors["ptrainer"]["inv_full"] = [(255, 255, 255), (102, 102, 102), (216, 0, 39)]
		self.colors["ptrainer"]["no_money"] = [(255, 255, 255), (102, 102, 102), (216, 0, 39)]

		self.positions["bbgsim"] = {}
		self.positions["general"] = {}
		self.positions["ptrainer"] = {}

		self.positions["bbgsim"]["inv_full"] = [(690*2, 604*2), (658*2, 604*2)]
		self.positions["bbgsim"]["no_money"] = [(454*2, 877*2), (692*2, 571*2)]
		self.positions["general"]["disco"] = [(696*2, 639*2), (420*2, 629*2)]
		self.positions["ptrainer"]["inv_full"] = [(777*2, 573*2), (798*2, 758*2), (916*2, 552*2)]
		self.positions["ptrainer"]["no_money"] = [(777*2, 573*2), (590*2, 635*2), (916*2, 552*2)]

		self.img = None
		self.px = None
		self.screenname = "screen.png"

		self.close_window_pos = (25, 359)

		self.control = RobloxControl()

	# use this function to close the roblox game window
	def close_roblox(self):
		self.control.cmd_tab()
		print("setting mouse position")
		self.control.set_mouse_pos(self.close_window_pos)
		print("clicking")
		self.control.click_mouse(1)

	# take a screenshot and load it up for downstream analysis
	def screenshot(self):
		os.system("screencapture {}".format(self.screenname))
		#time.sleep(0.1)
		self.img = Image.open(self.screenname)
		# load the image's pixel data
		self.px = self.img.load()

	# check status. i select different positions and their color values from the
	# screenshot to detect certain events such as disconnections as well as 
	# inventory full alerts in bubblegum sim.
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
