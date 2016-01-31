

import pygame

import constants

from sprite_image import SpriteSheet

class Player(pygame.sprite.Sprite):
	change_x = 0
	change_y = 0

	walking_frames_l = []
	walking_frames_r = []

	direction = "R"

	level = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)


		sprite_sheet = SpriteSheet('images/zombie_topdown.png')

		image = sprite_sheet.get_image(48,48,30,45)
		self.walking_frames_r.append(image)

		self.image = self.walking_frames_r[0]

		self.rect = self.image.get_rect()


	def go_north(self):
		self.change_y = -6
		self.direction = "N"

	def go_east(self):
		self.change_x = 6
		self.direction = "E"

	def go_south(self):
		self.change_y == 6
		self.direction = "S"

	def go_west(self):
		self.change_x == -6
		self.direction = "W"

	def stop(self):
		self.change_x = 0
		self.change_y = 0
