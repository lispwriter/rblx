#!/usr/bin/env python
#
# bbgsim-gridRun.py
#
# 

import pynput.mouse as mm
import pynput.keyboard as kk

import time
import sys

from math import sqrt

##
## this script controlls the character and makes them run in a square
## pattern including going diagonal to make an X
##

## pseudo code

##
## while TRUE: 
##   click "auto" button (TODO: hard-code the mouse position)
##   wait 10ish minutes
##   press 'S' for 0.5 seconds? (Test this to see if it moves far enough)
##   click "inventory is full" x (may not be on screen) (TODO: hard-code mouse position)
##   click pet inventory button (TODO: hard-code mouse position)
##   click delete unlocked button (TODO: hard-code mouse position)
##   click close inventory button (TODO: hard-code mouse position)
##   press 'W' for 0.5 seconds (same time as before hopefully this puts the character back into the same position)
## 

mc = mm.Controller()
mb = mm.Button

kc = kk.Controller()
ke = kk.Key


mouse_autoButton = (0, 0)
mouse_invAlertClose = (-593, 1199)
mouse_invOpen = (-288, 1358)
mouse_invClear = (-1034, 1162)
mouse_confirm = (-830, 1444)
mouse_invClose = mouse_invOpen

mouse_autoButton = (0, 0)
mouse_invAlertClose = (786, 591)
mouse_invOpen = (1055, 775)
mouse_invClear = (227, 598)
mouse_confirm = (431, 863)
mouse_invClose = mouse_invOpen

countdown = 5
# time to wait for hatching
walk_time = 0.7
side_time = 2.3
short_time = 0.22
across_time = 2.6
diag_time = sqrt(side_time**2 + side_time**2)
standard_delay = 0.8
turn_delay = 0.05

print("Make sure to bring game to foreground and click in it to capture the mouse")
print("Starting in\n> 5...")
while countdown > 0:
	countdown = countdown - 1
	time.sleep(1)
	print("> {}...".format(countdown))
i = 0

#kc.press('a')
#time.sleep(2.5)
#kc.release('a')
#time.sleep(0.05)
#kc.press('w')
#time.sleep(2)
#kc.release('w')

#sys.exit(0)

while True:
	i = i + 1
	print("Starting loop {}".format(i))

	# set position
	#mc.position = mouse_autoButton
	# click button
	#mc.click(mb.left, 1)

	j = 0
	for j in range(2):

		# long side
		kc.press('w')
		time.sleep(side_time)
		kc.release('w')
		
		time.sleep(turn_delay)

		# short side
		kc.press('d')
		time.sleep(short_time)
		kc.release('d')

		time.sleep(turn_delay)

		# long side
		kc.press('s')
		time.sleep(side_time)
		kc.release('s')

		time.sleep(turn_delay)

		# short side
		kc.press('d')
		time.sleep(short_time)
		kc.release('d')

		time.sleep(turn_delay)

	time.sleep(3)

	j = 0
	for j in range(2):

		# long side
		kc.press('w')
		time.sleep(side_time)
		kc.release('w')
		
		time.sleep(turn_delay)

		# short side
		kc.press('a')
		time.sleep(short_time)
		kc.release('a')

		time.sleep(turn_delay)

		# long side
		kc.press('s')
		time.sleep(side_time)
		kc.release('s')

		time.sleep(turn_delay)

		# short side
		kc.press('a')
		time.sleep(short_time)
		kc.release('a')

		time.sleep(turn_delay)

	#time.sleep(3)
	# avatar should be back where it started now. assuming right-hand side of island so 
	# now we can walk to the other side. maybe 3 seconds?

	kc.press('a')
	time.sleep(across_time)
	kc.release('a')

	j = 0
	for j in range(2):

		# long side
		kc.press('w')
		time.sleep(side_time)
		kc.release('w')
		
		time.sleep(turn_delay)

		# short side
		kc.press('a')
		time.sleep(short_time)
		kc.release('a')

		time.sleep(turn_delay)

		# long side
		kc.press('s')
		time.sleep(side_time)
		kc.release('s')

		time.sleep(turn_delay)

		# short side
		kc.press('a')
		time.sleep(short_time)
		kc.release('a')

		time.sleep(turn_delay)

	time.sleep(3)


	j = 0
	for j in range(2):

		# long side
		kc.press('w')
		time.sleep(side_time)
		kc.release('w')
		
		time.sleep(turn_delay)

		# short side
		kc.press('d')
		time.sleep(short_time)
		kc.release('d')

		time.sleep(turn_delay)

		# long side
		kc.press('s')
		time.sleep(side_time)
		kc.release('s')

		time.sleep(turn_delay)

		# short side
		kc.press('d')
		time.sleep(short_time)
		kc.release('d')

		time.sleep(turn_delay)


	kc.press('d')
	time.sleep(across_time)
	kc.release('d')

	time.sleep(3)


#	if i > 10:
#		print("waiting for 10 seconds....")
#		time.sleep(10)
#		i = 0


