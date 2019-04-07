#!/usr/bin/env python
#
# just clicking
#

from pynput.mouse import Button, Controller
from random import random as rn
import pynput.keyboard as kbd
import time
import sys

mouse = Controller()
keyboard = kbd.Controller()

argc = len(sys.argv)
if argc < 2: 
	print("usage: bbgsim-singleHatch.py <time in seconds to wait>")
	sys.exit(1)


countdown = 5
delay = 2
press_lag = 0.2
i = 0
total_time = 0
max_time = int(sys.argv[1])

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
while True:

	time.sleep(delay)

	keyboard.press('e')
	time.sleep(press_lag)
	keyboard.release('e')

	total_time += delay

	if total_time > max_time:
		print("running for {:04f} seconds, breaking out...".format(total_time))
		break

print("waiting...are you coming back???")
while True:
	keyboard.press('w')
	time.sleep(0.03)
	keyboard.release('w')
	time.sleep(120)

