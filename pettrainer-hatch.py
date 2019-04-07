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


countdown = 5
hatch_interval = 5
press_lag = 0.2
i = 0
total_time = 0
control = RobloxControl()
cv = RobloxCV()

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
tog = 0
def toggle(n):
	return(n * -1 + 1)

control.move_mouse((561, 963))

while True:
	i += 1
	#if (i % 4) == 0 or i == 1:

	if rn() < 0.1:
		control.move_mouse((561, 963))

	#control.after_lag()
	control.click_mouse(1)
	#control.after_lag()

	#tog = toggle(tog)
	if rn() < 0.3:
		# time.sleep(1)
		# check connection
		print("checking status...")
		cv.screenshot()
		if cv.check_status("ptrainer", "inv_full"):
			print(time.strftime("%c", time.localtime()))
			print("Inventory full. Bailing out...")
			break
		elif cv.check_status("ptrainer", "no_money"):
			print(time.strftime("%c", time.localtime()))
			print("YOU'RE OUT OF MONEY, NOOB. Bailing out...")
			break
		elif cv.check_disco():
			print(time.strftime("%c", time.localtime()))
			print("DISCONNECTED. Bailing out...")
			break			
		else:
			print("GOOD TO GO")

	# wait
	keyboard.type('e')
	time.sleep(hatch_interval)
