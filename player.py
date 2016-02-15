

import pygame

import constants

from sprite_image import SpriteSheet

class Player(pygame.sprite.Sprite):
	change_x = 0
	change_y = 0

	zombie_sprite_width = 65
	zombie_sprite_height = 100


	walking_frames_n = []
	walking_frames_e = []
	walking_frames_s = []
	walking_frames_w = []

	direction = "N"

	level = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		sprite_sheet = SpriteSheet('images/zombie_topdown.png')

		
		image = sprite_sheet.get_image(535,395,65,100)
		self.walking_frames_n.append(image)		
		image = sprite_sheet.get_image(661,395,65,100)
		self.walking_frames_n.append(image)		
		image = sprite_sheet.get_image(794,395,65,100)
		self.walking_frames_n.append(image)
		image = sprite_sheet.get_image(921,395,65,100)
		self.walking_frames_n.append(image)
		image = sprite_sheet.get_image(1047,395,65,100)
		self.walking_frames_n.append(image)
		image = sprite_sheet.get_image(1177,395,65,100)
		self.walking_frames_n.append(image)
		image = sprite_sheet.get_image(1305,395,65,100)
		self.walking_frames_n.append(image)


		image = sprite_sheet.get_image(535,676,100,65)
		self.walking_frames_e.append(image)		
		image = sprite_sheet.get_image(661,676,100,65)
		self.walking_frames_e.append(image)		
		image = sprite_sheet.get_image(794,676,100,65)
		self.walking_frames_e.append(image)
		image = sprite_sheet.get_image(921,676,100,65)
		self.walking_frames_e.append(image)
		image = sprite_sheet.get_image(1047,676,100,65)
		self.walking_frames_e.append(image)
		image = sprite_sheet.get_image(1177,676,100,65)
		self.walking_frames_e.append(image)
		image = sprite_sheet.get_image(1305,676,100,65)
		self.walking_frames_e.append(image)

		image = sprite_sheet.get_image(535,921,65,100)
		self.walking_frames_s.append(image)		
		image = sprite_sheet.get_image(661,921,65,100)
		self.walking_frames_s.append(image)		
		image = sprite_sheet.get_image(794,921,65,100)
		self.walking_frames_s.append(image)
		image = sprite_sheet.get_image(921,921,65,100)
		self.walking_frames_s.append(image)
		image = sprite_sheet.get_image(1047,921,65,100)
		self.walking_frames_s.append(image)
		image = sprite_sheet.get_image(1177,921,65,100)
		self.walking_frames_s.append(image)
		image = sprite_sheet.get_image(1305,921,65,100)
		self.walking_frames_s.append(image)

		image = sprite_sheet.get_image(525,168,100,65)
		self.walking_frames_w.append(image)		
		image = sprite_sheet.get_image(651,168,100,65)
		self.walking_frames_w.append(image)		
		image = sprite_sheet.get_image(784,168,100,65)
		self.walking_frames_w.append(image)
		image = sprite_sheet.get_image(911,168,100,65)
		self.walking_frames_w.append(image)
		image = sprite_sheet.get_image(1037,168,100,65)
		self.walking_frames_w.append(image)
		image = sprite_sheet.get_image(1167,168,100,65)
		self.walking_frames_w.append(image)
		image = sprite_sheet.get_image(1295,168,100,65)
		self.walking_frames_w.append(image)

		self.image = self.walking_frames_n[0]

		self.rect = self.image.get_rect()

	def update(self):
		if (self.rect.x + self.change_x < 0) or (self.rect.x + self.change_x + self.zombie_sprite_width > constants.SCREEN_WIDTH):
			pos_x = self.rect.x
		else:
			pos_x = self.rect.x - self.change_x
			self.rect.x += self.change_x

		if self.rect.y + self.change_y < 0 or self.rect.y + self.change_y  + self.zombie_sprite_height > constants.SCREEN_HEIGHT:
			pos_y = self.rect.y - self.change_y
		else:
			self.rect.y += self.change_y
			pos_y = self.rect.y
			
		if self.direction == "N":
			frame = (pos_y // 65) % len(self.walking_frames_n)
			self.image = self.walking_frames_n[frame]
		elif self.direction == "E":
			frame = (pos_x // 100) % len(self.walking_frames_e)
			self.image = self.walking_frames_e[frame]
		elif self.direction == "S":
			frame = (pos_y // 100) % len(self.walking_frames_s)
			self.image = self.walking_frames_s[frame]
		elif self.direction == "W":
			frame = (pos_x // 65) % len(self.walking_frames_w)
			self.image = self.walking_frames_w[frame]

	def go_north(self):
		self.change_y = -6
		self.direction = "N"

	def go_east(self):
		self.change_x = 6
		self.direction = "E"

	def go_south(self):
		self.change_y = 6
		self.direction = "S"

	def go_west(self):
		self.change_x = -6
		self.direction = "W"

	def stop(self):
		self.change_x = 0
		self.change_y = 0
