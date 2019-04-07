#!/usr/bin/env python
#
# just clicking
#


from pynput.mouse import Button, Controller
import time

mouse = Controller()

countdown = 5
delay = 0.25
i = 0

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1

i = 0
while True:
	time.sleep(1)
	print("clicking")
	mouse.click(Button.left, 1)
	time.sleep(0.05)
	mouse.click(Button.left, 1)



