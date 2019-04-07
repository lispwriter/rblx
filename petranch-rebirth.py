#!/usr/bin/env python
#
# petranch-deletePets.py
#
# 

from pynput.mouse import Button, Listener
#import pynput.mouse as mm
#import pynput.keyboard as kk
from random import random as rn
import math
import os
#from PIL import Image
from RobloxSupport import *

import time
import sys

##
## this script automates deleting pets in pet ranch sim
## row by row. you have to manually scroll the pet inventory and
## also run this for only up to 3 rows at a time.
##

def main():


#	mc = mm.Controller()
#	mb = mm.Button
#
#	kc = kk.Controller()
#	ke = kk.Key

	control = RobloxControl()
	cv = RobloxCV()

	countdown = 5
	# time to wait for hatching
	after_click_delay = 2
	press_delay = 0.07
	standard_delay = 0.25
	between_delay = 0.75

	per_row = 8
	equipped = 0

	pos = positions()

	upgrade0 = 0.4
	upgradeDelta = 0.5

	if False:
		# settings for single-rebirths. best time is like 49 seconds
		end_wait = 6
		max_equip = 10
		num_upgrades = int((max_equip - 4) / 2)
		equip_rows = int(math.ceil(max_equip * 1.0 / per_row))
		rb_button = pos.rebirth_1

	if False:
		# settings for triple-rebirths. 

		#end_wait = 24
		#max_equip = 24
		# these two lines are for when they have 2x coin events
		end_wait = 10
		max_equip = 20
		num_upgrades = int((max_equip - 4) / 2 )
		equip_rows = int(math.ceil(max_equip * 1.0 / per_row))
		rb_button = pos.rebirth_3

	if True:
		# settings for 5-rebirths during 2x event
		end_wait = 20
		max_equip = 32
		num_upgrades = int((max_equip - 4) / 2 )
		equip_rows = int(math.ceil(max_equip * 1.0 / per_row))
		rb_button = pos.rebirth_5

	if True:
		# settings for 10-rebirths during 2x event
		end_wait = 72
		max_equip = 40
		num_upgrades = int((max_equip - 4) / 2 )
		equip_rows = int(math.ceil(max_equip * 1.0 / per_row))
		rb_button = pos.rebirth_10

	count = 0

	print("Make sure to bring game to foreground and click in it to capture the mouse")
	print("Starting in\n> 5...")
	while countdown > 0:
		countdown = countdown - 1
		time.sleep(1)
		print("> {}...".format(countdown))

	with Listener(on_click=kill_click) as listener:

		# start by opening rebirths and rebirthing
		control.move_mouse(pos.rebirth_open)
		#control.after_lag()
		control.click_mouse(1)
		control.after_lag()
		
		# first time try from the highest rebirth option down to the lowest
		rbpos = [pos.rebirth_20, pos.rebirth_10, pos.rebirth_5, 
			pos.rebirth_3, pos.rebirth_1]
		for i in range(len(rbpos)):
			control.move_mouse(rbpos[i])
			control.click_mouse(1, short_lag=True)
			#control.after_lag()

		while True:

			if not listener.running:
				break

			t0 = time.time()

			# check connection
			print("checking status...")
			cv.screenshot()
			if cv.check_disco():
				print("YOU GOT DISCONNECTED, BRO!")
				# close roblox
				cv.close_roblox()
				break
			else:
				print("GOOD TO GO")

			# open the pet dialog
			control.move_mouse(pos.pets_open)
			control.click_mouse(1)
			control.after_lag()

			# equip pets
			equipped = 0
			
			print("equipping to {} pets".format(max_equip))

			for rowid in range(equip_rows):

				ypos = pos.first_pet[1] + pos.pet_dy*rowid
				for colid in range(per_row):

					xpos = pos.first_pet[0] + pos.pet_dx*colid

					control.move_mouse((xpos, ypos))
					control.click_mouse(2, short_lag=True)

					equipped += 1
					# initially we can only equip 4 pets so now we have to 
					# take a break and upgrade the range
					if equipped == 4:
						control.after_lag()

						# open the ranch control to upgrade it
						control.move_mouse(pos.ranch_open)
						control.click_mouse(1)
						#control.after_lag()

						# move to the upgrade button
						control.move_mouse(pos.ranch_upgrade)

						# upgrade the ranch a little
						for i in range(num_upgrades):

							if i < 10:
								time.sleep(upgrade0 + upgradeDelta*i/10)
							else:
								time.sleep(upgrade0 + upgradeDelta)

							control.click_mouse(1)

						control.after_lag()

						# go back to the pets dialog so the loop can finish equipping
						# pets
						control.move_mouse(pos.pets_open)
						control.click_mouse(1)


					if equipped >= max_equip:
						break


			control.after_lag()

			# close it and move a tiny bit
			control.move_mouse(pos.pets_open)
			control.click_mouse(1)

			ky = control.random_move_key()
			control.move_avatar(ky, 0.05)

			print("waiting to rebirth again...")
			time.sleep(end_wait)

			# rebirth time
			control.move_mouse(pos.rebirth_open)
			#control.after_lag()
			control.click_mouse(1)
			control.after_lag()
			
			# click the rebirth button
			control.move_mouse(rb_button)
			control.click_mouse(1)
			control.after_lag()		

			# close it
	#		control.move_mouse(pos.rebirth_open)
	#		control.click_mouse(1)
	#		control.after_lag()

			passtime = time.time() - t0
			count += 1
			print("rebirth {} time was {} seconds...".format(count, passtime))

	return(0)

def kill_click(x, y, button, pressed):
	if pressed and button == Button.right:
		print("KILL CLICK BRO")
		return(False)

class positions(object):
	def __init__(self):
		self.ranch_open = (1086, 671)
		self.ranch_upgrade = (564, 762)
		self.pets_open = (1021, 677)
		self.rebirth_open = (1088, 739)
		self.rebirth_1 = (372, 761)
		self.rebirth_3 = (471, 761)
		self.rebirth_5 = (564, 761)
		self.rebirth_10 = (656, 761)
		self.rebirth_20 = (751, 761)
		self.first_pet = (350, 589)
		self.pet_dx = 412 - 348
		self.pet_dy = 675 - 606


if __name__ == "__main__":
	main()

