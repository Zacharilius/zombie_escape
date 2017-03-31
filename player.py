import constants
import pygame
from sprite_image import SpriteSheet

class Player(pygame.sprite.Sprite):
	change_x = 0
	change_y = 0

	direction = 'N'

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		sprite_sheet = SpriteSheet('images/zombie_topdown.png')

		sprite_sheet_num_cols = 36
		self.sprite_width = sprite_sheet.get_width() // sprite_sheet_num_cols

		sprite_sheet_num_rows = 8
		self.sprite_height = sprite_sheet.get_height() // sprite_sheet_num_rows

		self.walking_frames_n = get_sprite_images(sprite_sheet, 512, 384, self.sprite_width, self.sprite_height, 7)
		self.walking_frames_e = get_sprite_images(sprite_sheet, 512, 640, self.sprite_width, self.sprite_height, 7)
		self.walking_frames_s = get_sprite_images(sprite_sheet, 512, 896, self.sprite_width, self.sprite_height, 7)
		self.walking_frames_w = get_sprite_images(sprite_sheet, 512, 128, self.sprite_width, self.sprite_height, 7)

		self.image = self.walking_frames_n[0]

		self.rect = self.image.get_rect()

	def update(self):
		if (self.rect.x + self.change_x < 0) or (self.rect.x + self.change_x + self.sprite_width > constants.SCREEN_WIDTH):
			pos_x = self.rect.x
		else:
			pos_x = self.rect.x - self.change_x
			self.rect.x += self.change_x

		if self.rect.y + self.change_y < 0 or self.rect.y + self.change_y  + self.sprite_height > constants.SCREEN_HEIGHT:
			pos_y = self.rect.y - self.change_y
		else:
			self.rect.y += self.change_y
			pos_y = self.rect.y

		speed_multiplier = 6
		if self.direction == 'N':
			frame = (pos_y * speed_multiplier // self.sprite_width) % len(self.walking_frames_n)
			self.image = self.walking_frames_n[frame]
		elif self.direction == 'E':
			frame = (pos_x * speed_multiplier // self.sprite_height) % len(self.walking_frames_e)
			self.image = self.walking_frames_e[frame]
		elif self.direction == 'S':
			frame = (pos_y * speed_multiplier // self.sprite_height) % len(self.walking_frames_s)
			self.image = self.walking_frames_s[frame]
		elif self.direction == 'W':
			frame = (pos_x * speed_multiplier // self.sprite_width) % len(self.walking_frames_w)
			self.image = self.walking_frames_w[frame]

	def go_north(self):
		self.change_y = -6
		self.direction = 'N'

	def go_east(self):
		self.change_x = 6
		self.direction = 'E'

	def go_south(self):
		self.change_y = 6
		self.direction = 'S'

	def go_west(self):
		self.change_x = -6
		self.direction = 'W'

	def stop(self):
		self.change_x = 0
		self.change_y = 0


def get_sprite_images(sprite_sheet, x, y, width, height, sprite_cols):
	images = []
	end_x = x + sprite_cols * width
	for i in range(x, end_x, width):
		images.append(sprite_sheet.get_image(i, y, width, height))
	return images
