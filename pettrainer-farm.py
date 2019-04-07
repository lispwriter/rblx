#!/usr/bin/env python
#
# just clicking
#

from pynput.mouse import Button, Controller
from random import random as rn
import pynput.keyboard as kbd
import time
import sys
from RobloxSupport import *

mouse = Controller()
keyboard = kbd.Controller()

class Colors(object):
	def __init__(self):
		self.coin = [
			(255, 238, 165), 
			(255, 237, 160),
			(250, 214, 65),
			(191,160,38),
			(255, 241, 153),
			(191, 0, 191),
			(153, 77, 0),
			(117, 97, 73),
			(124, 62, 0),
			(6, 200, 255),
			(3, 121, 163),

		]

		self.bush = [
			(129, 127, 120),
			(151, 148, 140)
		]

	def color_match(self, a, b):
		di = sum([(a[i] - b[i])**2 for i in range(3)])
		return(di < 50)

	def check_coin(self, b):
		for i in range(len(self.coin)):
			di = self.color_match(self.coin[i], b)
			if di:
				return True

		return False

	def check_bush(self, b):
		for i in range(len(self.bush)):
			di = self.color_match(self.bush[i], b)
			if di:
				return True

		return False


scan_ul = [267*2, 462*2]
scan_lr = [1097*2, 1003*2]

dx = scan_lr[0] - scan_ul[0]
dy = scan_lr[1] - scan_ul[1]

countdown = 5
hatch_interval = 5
press_lag = 0.2
i = 0
total_time = 0
control = RobloxControl()
cv = RobloxCV()
cols = Colors()

max_find = 10

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
tog = 1
def toggle(n):
	return(n * -1 + 1)

#control.move_mouse((561, 963))


t0 = time.time()

while True:
	i += 1
	#if (i % 4) == 0 or i == 1:

	# take a new capture
	print("grabbing screen")
	os.system("screencapture pettrain.png")
	im = Image.open("pettrain.png")
	px = im.load()
	tog = toggle(tog)

	if time.time() - t0 > 200:

		if cv.check_disco():
			print(time.strftime("%c", time.localtime()))
			print("DISCONNECTED. Bailing out...")
			break			

		t0 = time.time()

	if True:
		j = 0
		found = 0
		#print("checking {} positions at random".format(dx*dy))
		while j < dx*dy:
			xpos = int(math.floor(rn()*dx)) + scan_ul[0]
			ypos = int(math.floor(rn()*dy)) + scan_ul[1]
			j += 1

			pos = (xpos, ypos)
			cval = px[pos]

			if cols.check_coin(cval):
				print("found something!")
				found += 1
				# click it
				pos = (int(math.floor(xpos/2)), int(math.floor(ypos/2)))
				print(pos)
				print(cval)
				control.move_mouse(pos)
				control.click_mouse(1)

			if found > max_find:
				#print("getting new screengrab")
				break

	if tog==1:
		# rotate a little
		keyboard.press(kbd.Key.left)
		time.sleep(1.5)
		keyboard.release(kbd.Key.left)



