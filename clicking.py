#!/usr/bin/env python
#
# just clicking
#


from pynput.mouse import Button, Controller
import time

mouse = Controller()

countdown = 5
delay = 0.25
loops = 10000
i = 0

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
while i < loops:
	mouse.click(Button.left, 1)
	time.sleep(delay)
	i = i + 1


