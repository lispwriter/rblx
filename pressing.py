#!/usr/bin/env python
#
# just clicking
#


from pynput.mouse import Button, Controller
from random import random as rn
import pynput.keyboard as kbd
import time

mouse = Controller()
keyboard = kbd.Controller()

countdown = 5
delay0 = 60
delay = delay0
delay_spread = delay0 * 0.1
r1 = 0
r2 = 0
i = 0

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
while True:
	mouse.press(Button.left)

	r1 = rn()
	r2 = rn()
	if r1 < 0.5:
		r2 = -r2
	delay = delay0 + r2 * delay_spread

	print("sleeping for {:04f} seconds".format(delay))
	time.sleep(delay)

	i = i + 1
	print("moving. round {}".format(i))

	keyboard.press("s")
	time.sleep(0.05)
	keyboard.release('s')

	time.sleep(0.5)

	keyboard.press("w")
	time.sleep(0.07)
	keyboard.release('w')

	mouse.release(Button.left)
	time.sleep(0.5)



