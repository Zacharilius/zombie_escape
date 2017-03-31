import constants
import pygame

class Background():

    def __init__(self, window):
        self.window = window
        self.rects = []

        rect_width = constants.SCREEN_WIDTH // 3
        rect_height = 100

        # Left top
        self.rects.append(pygame.Rect(0, 1 * (constants.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Left bottom
        self.rects.append(pygame.Rect(0, 2 * (constants.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Right top
        self.rects.append(pygame.Rect(2 * (constants.SCREEN_WIDTH // 3), 1 * (constants.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Right bottom
        self.rects.append(pygame.Rect(2 * (constants.SCREEN_WIDTH // 3), 2 * (constants.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))

    def update(self):
        for rect in self.rects:
            pygame.draw.rect(self.window, constants.BLACK, rect)
