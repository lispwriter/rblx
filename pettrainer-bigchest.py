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
			(3, 127, 171),
			(121, 0, 121), 
			(124, 0, 124)
		]

	def color_match(self, a, b):
		di = sum([(a[i] - b[i])**2 for i in range(3)])
		return(di < 50)

	def check_coin(self, b):
		for i in range(len(self.coin)):
			di = self.color_match(self.coin[i], b)
			if di:
				break

		return di


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
found = 0
collecting = 0
while True:
	#i += 1
	#if (i % 4) == 0 or i == 1:

	# take a new capture
	print("grabbing screen")
	os.system("screencapture pettrain.png")
	im = Image.open("pettrain.png")
	px = im.load()

	if (time.time() - t0) > 500:
		keyboard.type('w')

		if cv.check_disco():
			print(time.strftime("%c", time.localtime()))
			print("DISCONNECTED. Bailing out...")
			break			

		t0 = time.time()

	# scan screengrab for the chest
	i = 0
	j = 0
	found = 0
	print("looking for the chest")
	while i < dx:
		j = 0
		while j < dy:
			xpos = scan_ul[0] + i
			ypos = scan_ul[1] + j
			pos = (xpos, ypos)
			cval = px[pos]

			if cols.check_coin(cval):
				print("found the chest")
				# chest is here. load the pets on it
				if collecting==0:
					collecting = 1
					control.move_mouse(( int(math.floor(xpos/2)), int(math.floor(ypos/2)) ))
					for k in range(7):
						control.click_mouse(1)
				else:
					print("you must be collecting it still")

				found = 1

			if found==1:
				break

			j += 12

		if found==1:
			break

		i += 12


	if found == 0:
		print("cant find it. you must have collected it.")
		# this means it was collected and we are just waiting for it to come back
		collecting = 0

	print("waiting a minute")
	time.sleep(60)



