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
delay0 = 360
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

	mouse.click(Button.left, 1)
	time.sleep(4)


