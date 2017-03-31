import constants
import pygame

class SpriteSheet(object):
    sprite_sheet = None

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_width(self):
        return self.sprite_sheet.get_width()

    def get_height(self):
        return self.sprite_sheet.get_height()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.BLACK)
        return image
