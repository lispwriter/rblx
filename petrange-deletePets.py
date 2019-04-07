#!/usr/bin/env python
#
# petranch-deletePets.py
#
# 

import pynput.mouse as mm
import pynput.keyboard as kk
from random import random as rn

import time
import sys

##
## this script automates deleting pets in pet ranch sim
## row by row. you have to manually scroll the pet inventory and
## also run this for only up to 3 rows at a time.
##

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


mc = mm.Controller()
mb = mm.Button

kc = kk.Controller()
ke = kk.Key

argc = len(sys.argv)
if argc < 2:
	print("useage: <scriptname>.py <num_rows>")
	sys.exit(1)

countdown = 5
num_rows = int(sys.argv[1])
# time to wait for hatching
after_click_delay = 2
press_delay = 0.07
standard_delay = 0.25

# positions
start_position = (759, 811)
delta_x = 97
delta_y = 103
delete_button = (995, 857)
delete_confirm = (465, 604)


print("Make sure to bring game to foreground and click in it to capture the mouse")
print("Starting in\n> 5...")
while countdown > 0:
	countdown = countdown - 1
	time.sleep(1)
	print("> {}...".format(countdown))


i = 0
for i in range(num_rows):
	# calcualte y position for current row
	current_y = start_position[1] - i * delta_y
	for j in range(5):
		# calculate x position for curent pet
		current_x = start_position[0] - j * delta_x
		this_pos = (current_x, current_y)

		cmd_tab(kc, ke)
		# set mouse in position of pet
		mc.position = this_pos
		time.sleep(standard_delay)
		cmd_tab(kc, ke)
		# click the pet
		mc.click(mb.left, 1)
		time.sleep(standard_delay)

		cmd_tab(kc, ke)
		# move to the delete button
		mc.position = delete_button
		time.sleep(standard_delay)
		cmd_tab(kc, ke)
		# click in it
		mc.click(mb.left, 1)
		time.sleep(standard_delay)

		# move to delete confirm
		cmd_tab(kc, ke)
		mc.position = delete_confirm
		time.sleep(standard_delay)
		cmd_tab(kc, ke)
		mc.click(mb.left, 1)
		time.sleep(standard_delay)



