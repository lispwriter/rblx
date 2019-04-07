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


def cmd_tab(kbd, kbk):
	press_delay = 0.07
	standard_delay = 0.25
	kbd.press(kbk.cmd)
	time.sleep(press_delay)
	kbd.press(kbk.tab)
	time.sleep(press_delay)
	kbd.release(kbk.tab)
	time.sleep(press_delay)
	kbd.release(kbk.cmd)
	time.sleep(standard_delay)

def one_click(mouse):
	mouse.click(Button.left, 1)
	time.sleep(0.2)


argc = len(sys.argv)-1
if argc < 1:
	print("useage: petranch-upgrade.py <num_clicks>")
	sys.exit(1)

countdown = 3
delay0 = 60
delay = delay0
delay_spread = delay0 * 0.1
r1 = 0
r2 = 0
i = 0

n_clicks = int(sys.argv[1])

while i < countdown:
	print("{}...".format(countdown - i))
	time.sleep(1)
	i = i + 1


button_pos = (959, 894)
cmd_tab(keyboard, kbd.Key)
mouse.position = button_pos
cmd_tab(keyboard, kbd.Key)

for i in range(n_clicks):
	one_click(mouse)

