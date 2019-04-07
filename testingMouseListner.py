#!/usr/bin/env python
#
# just clicking
#


from pynput.mouse import Button, Controller, Listener
from random import random as rn
import pynput.keyboard as kbd
import time
import sys

mouse = Controller()
keyboard = kbd.Controller()

countdown = 5
delay0 = 360
delay = delay0
delay_spread = delay0 * 0.1
r1 = 0
r2 = 0
i = 0


def on_click(x, y, button, pressed):
	#print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
	if pressed:
		if button == Button.right:
			print("right clicked")
			return False


if __name__=="__main__":

	while i < countdown:
		print("{}...".format(countdown - i))
		time.sleep(1)
		i = i + 1

	with Listener(on_click=on_click) as listener:
		i = 0
		while True:
			i += 1
			print('yeah bro {}'.format(i))
			time.sleep(2)

			if not listener.running:
				print("you killed it")
				break


#	mlist = Listener(on_click=on_click)
#	mlist.start()
#
#	try:
#		i = 0
#		while True:
#			#mouse.press(Button.left)
#			i += 1
#			print("yeah {}".format(i))
#			time.sleep(2)
#	except MyException as e:
#		print("exiting...")
#		Listener.stop

