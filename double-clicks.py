#!/usr/bin/env python
#
# just clicking
#


from pynput.mouse import Button, Controller, Listener
import time
from RobloxSupport import *

control = RobloxControl()

def kill_click(x, y, button, pressed):
	if pressed and button == Button.right:
		print("KILL CLICK BRO")
		return(False)

countdown = 5
delay = 0.25
i = 0

if __name__ == "__main__":

	while i < countdown:
		print("{}...".format(countdown - i))
		time.sleep(1)
		i = i + 1

	with Listener(on_click=kill_click) as listener:

		i = 0
		while True:
			if not listener.running:
				break

			time.sleep(1)
			print("clicking")
			control.click_mouse(2)



