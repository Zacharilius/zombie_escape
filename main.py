import settings
import pygame

def main():
    pygame.init()

    size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('Zombie Escape')

    active_sprite_list = pygame.sprite.Group()

    background = Background(window)

    player = Player()
    player.rect.x = 340
    player.rect.y = settings.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    clock = pygame.time.Clock()

    pygame.mixer.music.load('assets/game_music.ogg')
    pygame.mixer.music.play(-1, 0.0)  # -1 Causes to loop indefinitely

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.go_north()
                elif event.key == pygame.K_RIGHT:
                    player.go_east()
                elif event.key == pygame.K_DOWN:
                    player.go_south()
                elif event.key == pygame.K_LEFT:
                    player.go_west()
            elif event.type == pygame.KEYUP:
                player.stop()

        window.fill(settings.WHITE)

        background.update()

        active_sprite_list.update()
        active_sprite_list.draw(window)

        clock.tick(65)

        pygame.display.flip()


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
        image.set_colorkey(settings.BLACK)
        return image


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0

    direction = 'N'

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet('assets/zombie_topdown.png')

        sprite_sheet_num_cols = 36
        self.sprite_width = sprite_sheet.get_width() // sprite_sheet_num_cols

        sprite_sheet_num_rows = 8
        self.sprite_height = sprite_sheet.get_height() // sprite_sheet_num_rows

        self.walking_frames_n = self.get_sprite_images(sprite_sheet, 512, 384, self.sprite_width, self.sprite_height, 7)
        self.walking_frames_e = self.get_sprite_images(sprite_sheet, 512, 640, self.sprite_width, self.sprite_height, 7)
        self.walking_frames_s = self.get_sprite_images(sprite_sheet, 512, 896, self.sprite_width, self.sprite_height, 7)
        self.walking_frames_w = self.get_sprite_images(sprite_sheet, 512, 128, self.sprite_width, self.sprite_height, 7)

        self.image = self.walking_frames_n[0]
        self.rect = self.image.get_rect()

    def get_sprite_images(self, sprite_sheet, x, y, width, height, sprite_cols):
        images = []
        end_x = x + sprite_cols * width
        for i in range(x, end_x, width):
            images.append(sprite_sheet.get_image(i, y, width, height))
        return images

    def update(self):
        if (self.rect.x + self.change_x < 0) or (self.rect.x + self.change_x + self.sprite_width > settings.SCREEN_WIDTH):
            pos_x = self.rect.x
        else:
            pos_x = self.rect.x - self.change_x
            self.rect.x += self.change_x

        if self.rect.y + self.change_y < 0 or self.rect.y + self.change_y  + self.sprite_height > settings.SCREEN_HEIGHT:
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


class Background():

    def __init__(self, window):
        self.window = window
        self.rects = []

        rect_width = settings.SCREEN_WIDTH // 3
        rect_height = 100

        # Left top
        self.rects.append(pygame.Rect(0, 1 * (settings.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Left bottom
        self.rects.append(pygame.Rect(0, 2 * (settings.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Right top
        self.rects.append(pygame.Rect(2 * (settings.SCREEN_WIDTH // 3), 1 * (settings.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))
        # Right bottom
        self.rects.append(pygame.Rect(2 * (settings.SCREEN_WIDTH // 3), 2 * (settings.SCREEN_HEIGHT // 3) - (rect_height / 2), rect_width, rect_height))

    def update(self):
        for rect in self.rects:
            pygame.draw.rect(self.window, settings.BLACK, rect)


if __name__ == '__main__':
    main()
