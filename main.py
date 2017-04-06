import settings
import pygame
from pygame.mixer import Sound
from pygame.sprite import groupcollide, spritecollide
import random
import sys


def main():

    # ==== Setup ====

    pygame.init()

    size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]
    window = pygame.display.set_mode(size)
    pygame.display.set_caption('Zombie Escape')

    if 'skip_intro' in sys.argv:
        show_intro_screen = False
    else:
        show_intro_screen = True
    if 'mute_sound' in sys.argv:
        mute_sound = True
    else:
        mute_sound = False

    # ==== Intro Screen ====

    intro_title_font_size = 60
    intro_title_font = pygame.font.Font('assets/jonathan-s-harris_something-strange/something_strange.ttf', intro_title_font_size)
    intro_font_title_image = intro_title_font.render('Brains... it\'s what\'s for dinner', True, settings.RED)

    intro_screen_show_time = 5000 # 5 seconds

    # ==== Game ====

    # ---- Sprites ----

    background = Background()
    background_single_sprite_group = pygame.sprite.GroupSingle(background)

    wall_sprite_list = Wall.create_walls_sprite_group()

    player_sprite_list = pygame.sprite.Group()
    player = Player(wall_sprite_list)
    player_sprite_list.add(player)

    enemy_sprite_group = pygame.sprite.Group()
    enemy1 = Enemy(x=30, y=30, direction='horizontal', collision_sprite_group=wall_sprite_list)
    enemy_sprite_group.add(enemy1)
    enemy2 = Enemy(x=settings.SCREEN_WIDTH / 2, y=30, direction='vertical', collision_sprite_group=wall_sprite_list)
    enemy_sprite_group.add(enemy2)

    brain_sprite_list = pygame.sprite.Group()
    brains_eaten = 0

    # ---- Clock ----

    clock = pygame.time.Clock()
    time_since_last_brain_created = 0

    # ---- Font ----

    brains_left_font_size = 16
    brains_left_font = pygame.font.Font(None, brains_left_font_size)  # Default system font

    # ---- Sound ----

    brain_eating_sound = Sound('assets/zombie_brain_eating.ogg')

    pygame.mixer.music.load('assets/game_music.ogg')
    if not mute_sound:
        pygame.mixer.music.play(-1, 0.0)  # -1 Causes to loop indefinitely

    # ==== End Screen ====

    show_end_screen = False
    end_game_title_font_size = 60
    end_game_title_font = pygame.font.Font('assets/jonathan-s-harris_something-strange/something_strange.ttf', end_game_title_font_size)
    end_game_font_title_image = end_game_title_font.render('You died...', True, settings.RED)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.go_north()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_east()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.go_south()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_west()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.stop_north()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.stop_east()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.stop_south()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.stop_west()

        window.fill(settings.WHITE)

        if show_intro_screen:
            window.blit(intro_font_title_image, (settings.SCREEN_WIDTH / 2 - intro_font_title_image.get_width() / 2, settings.SCREEN_HEIGHT / 2))

            if pygame.time.get_ticks() > intro_screen_show_time:
                show_intro_screen = False
        elif show_end_screen:
            window.blit(end_game_font_title_image, (settings.SCREEN_WIDTH / 2 - end_game_font_title_image.get_width() / 2, settings.SCREEN_HEIGHT / 3))
        else:
            time_since_last_brain_created += clock.get_time()
            ten_seconds = 10000
            if time_since_last_brain_created > ten_seconds:
                edge_offset = 20
                x, y = random.randint(0 + edge_offset, settings.SCREEN_WIDTH - edge_offset), random.randint(0 + edge_offset, settings.SCREEN_HEIGHT - edge_offset)
                brain = Brain(x, y)  # TODO pass in x, y
                brain_sprite_list.add(brain)
                time_since_last_brain_created = 0

            for brain in groupcollide(brain_sprite_list, player_sprite_list, True, False, collided=None):
                brains_eaten += 1
                if not mute_sound:
                    brain_eating_sound.play()

            background_single_sprite_group.update()
            background_single_sprite_group.draw(window)

            wall_sprite_list.update()
            wall_sprite_list.draw(window)

            player_sprite_list.update()
            player_sprite_list.draw(window)

            enemy_sprite_group.update()
            enemy_sprite_group.draw(window)

            brain_sprite_list.update()
            brain_sprite_list.draw(window)

            brains_eaten_message_image = get_brains_eaten_message_image(brains_left_font, brains_eaten)
            window.blit(brains_eaten_message_image, (settings.SCREEN_WIDTH - brains_eaten_message_image.get_width() - 20, 20))

            if spritecollide(player, enemy_sprite_group, True, collided=None):
                show_end_screen = True

        clock.tick(65)

        pygame.display.flip()


def get_brains_eaten_message_image(font, brains_eaten):
    image = font.render(str(brains_eaten) + ' brains eaten', True, settings.RED)
    return image

class SpriteSheet(object):
    sprite_sheet = None

    def __init__(self, file_name, num_columns, num_rows):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        self.num_columns = num_columns
        self.num_rows = num_rows

    def get_sprite_width(self):
        return self.get_width() // self.num_columns

    def get_sprite_height(self):
        return self.get_height() // self.num_rows

    def get_width(self):
        return self.sprite_sheet.get_width()

    def get_height(self):
        return self.sprite_sheet.get_height()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.fill(settings.BLACK)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(settings.BLACK)
        return image

    def get_frames(self, col_start_index, row_start_index, sprite_cols):
        images = []
        x = col_start_index * self.get_sprite_width()
        y = row_start_index * self.get_sprite_height()
        end_x = x + sprite_cols * self.get_sprite_width()
        for i in range(x, end_x, self.get_sprite_width()):
            images.append(self.get_image(i, y, self.get_sprite_width(), self.get_sprite_height()))
        assert len(images) == sprite_cols
        return images


class Background(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/stone_background.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    speed = 18

    moving_north = False
    moving_east = False
    moving_south = False
    moving_west = False

    def __init__(self, collision_sprite_group):
        super().__init__()

        self.collision_sprite_group = collision_sprite_group

        self.sprite_sheet = SpriteSheet('assets/zombie_topdown.png', num_columns=36, num_rows=8)

        self.walking_frames_n = self.sprite_sheet.get_frames(col_start_index=4, row_start_index=3, sprite_cols=7)
        self.walking_frames_e = self.sprite_sheet.get_frames(col_start_index=4, row_start_index=5, sprite_cols=7)
        self.walking_frames_s = self.sprite_sheet.get_frames(col_start_index=4, row_start_index=7, sprite_cols=7)
        self.walking_frames_w = self.sprite_sheet.get_frames(col_start_index=4, row_start_index=1, sprite_cols=7)

        self.image = self.walking_frames_n[0]
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = settings.SCREEN_HEIGHT - self.rect.height - self.speed

    def update(self):
        pos_x = self.rect.x - self.change_x
        pos_y = self.rect.y

        frame_multiplier = 6
        if self.moving_north:
            frame = (pos_y * frame_multiplier // self.sprite_sheet.get_sprite_width()) % len(self.walking_frames_n)
            self.image = self.walking_frames_n[frame]
        elif self.moving_east:
            frame = (pos_x * frame_multiplier // self.sprite_sheet.get_sprite_height()) % len(self.walking_frames_e)
            self.image = self.walking_frames_e[frame]
        elif self.moving_south:
            frame = (pos_y * frame_multiplier // self.sprite_sheet.get_sprite_height()) % len(self.walking_frames_s)
            self.image = self.walking_frames_s[frame]
        elif self.moving_west:
            frame = (pos_x * frame_multiplier // self.sprite_sheet.get_sprite_width()) % len(self.walking_frames_w)
            self.image = self.walking_frames_w[frame]

        if (self.is_speed_and_direction_are_invalid()):
            return

        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def can_move_in_directions(self, x, y):
        for sprite in self.collision_sprite_group.sprites():
            rect = self.rect.copy()
            rect.x += x
            rect.y += y
            if sprite.rect.colliderect(rect):
                return True
        return False

    def is_speed_and_direction_are_invalid(self):
        return (self.moving_north and not self.can_move_north() or
                self.moving_east and not self.can_move_east() or
                self.moving_south and not self.can_move_south() or
                self.moving_west and not self.can_move_west())

    def can_move_north(self):
        return not self.can_move_in_directions(0, -self.speed)

    def go_north(self):
        self.moving_north = True
        self.moving_south = False
        self.change_y = -self.speed

    def stop_north(self):
        self.moving_north = False
        self.change_y = 0

    def can_move_east(self):
        return not self.can_move_in_directions(self.speed, 0)

    def go_east(self):
        self.moving_east = True
        self.moving_west = False
        self.change_x = self.speed

    def stop_east(self):
        self.moving_east = False
        self.change_x = 0

    def can_move_south(self):
        return not self.can_move_in_directions(0, self.speed)

    def go_south(self):
        self.moving_south = True
        self.moving_north = False
        self.change_y = self.speed

    def stop_south(self):
        self.moving_south = False
        self.change_y = 0

    def can_move_west(self):
        return not self.can_move_in_directions(-self.speed, 0)

    def go_west(self):
        self.moving_west = True
        self.moving_east = False
        self.change_x = -self.speed

    def stop_west(self):
        self.moving_west = False
        self.change_x = 0


class Enemy(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    speed = 18

    moving_north = False
    moving_east = False
    moving_south = True
    moving_west = False

    def __init__(self, x, y, direction, collision_sprite_group):
        super().__init__()

        self.sprite_sheet = SpriteSheet('assets/doubleleggy_sprites/sprite_sheet.png', num_columns=12, num_rows=8)

        self.walking_frames_n = self.sprite_sheet.get_frames(col_start_index=9, row_start_index=3, sprite_cols=3)
        self.walking_frames_e = self.sprite_sheet.get_frames(col_start_index=9, row_start_index=2, sprite_cols=3)
        self.walking_frames_s = self.sprite_sheet.get_frames(col_start_index=9, row_start_index=0, sprite_cols=3)
        self.walking_frames_w = self.sprite_sheet.get_frames(col_start_index=9, row_start_index=1, sprite_cols=3)

        self.collision_sprite_group = collision_sprite_group

        if direction == 'horizontal':
            self.moving_east = True
            self.image = self.walking_frames_e[0]
            self.change_x = 20
        elif direction == 'vertical':
            self.moving_south = True
            self.image = self.walking_frames_s[0]
            self.change_y = 20
        else:
            raise 'Did not recognize: %s' % direction

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pos_x = self.rect.x - self.change_x
        pos_y = self.rect.y

        if spritecollide(self, self.collision_sprite_group, False, collided=None):
            self.reverse_direction()

        frame_multiplier = 6
        if self.moving_north:
            frame = (pos_y * frame_multiplier // self.sprite_sheet.get_sprite_width()) % len(self.walking_frames_n)
            self.image = self.walking_frames_n[frame]
        elif self.moving_east:
            frame = (pos_x * frame_multiplier // self.sprite_sheet.get_sprite_height()) % len(self.walking_frames_e)
            self.image = self.walking_frames_e[frame]
        elif self.moving_south:
            frame = (pos_y * frame_multiplier // self.sprite_sheet.get_sprite_height()) % len(self.walking_frames_s)
            self.image = self.walking_frames_s[frame]
        elif self.moving_west:
            frame = (pos_x * frame_multiplier // self.sprite_sheet.get_sprite_width()) % len(self.walking_frames_w)
            self.image = self.walking_frames_w[frame]

        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect.x += self.change_x
        self.rect.y += self.change_y

    def reverse_direction(self):
        # Switch east/west direction
        old_east = self.moving_east
        self.moving_east = self.moving_west
        self.moving_west = old_east
        self.change_x = -self.change_x

        # Rotate north/south direction
        old_south = self.moving_south
        self.moving_south = self.moving_north
        self.moving_north = old_south
        self.change_y = -self.change_y

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(settings.BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    @staticmethod
    def create_walls_sprite_group():
        wall_sprite_list = pygame.sprite.Group()

        # Inside Walls
        inside_wall_width = settings.SCREEN_WIDTH // 3
        inside_wall_height = 20

        x, y = 0, 1 * (settings.SCREEN_HEIGHT // 3) - (inside_wall_height / 2)
        wall_nw = Wall(x, y, inside_wall_width, inside_wall_height)
        wall_sprite_list.add(wall_nw)

        x, y = 2 * (settings.SCREEN_WIDTH // 3), 1 * (settings.SCREEN_HEIGHT // 3) - (inside_wall_height / 2)
        wall_ne = Wall(x, y, inside_wall_width, inside_wall_height)
        wall_sprite_list.add(wall_ne)

        x, y = 2 * (settings.SCREEN_WIDTH // 3), 2 * (settings.SCREEN_HEIGHT // 3) - (inside_wall_height / 2)
        wall_se = Wall(x, y, inside_wall_width, inside_wall_height)
        wall_sprite_list.add(wall_se)

        x, y = 0, 2 * (settings.SCREEN_HEIGHT // 3) - (inside_wall_height / 2)
        wall_sw = Wall(x, y, inside_wall_width, inside_wall_height)
        wall_sprite_list.add(wall_sw)

        # Outside Border Wals
        border_wall_thickness = 5

        border_wall_n = Wall(0, 0, settings.SCREEN_WIDTH, border_wall_thickness)
        wall_sprite_list.add(border_wall_n)

        border_wall_e = Wall(settings.SCREEN_WIDTH - border_wall_thickness, 0, border_wall_thickness, settings.SCREEN_HEIGHT)
        wall_sprite_list.add(border_wall_e)

        border_wall_s = Wall(0, settings.SCREEN_HEIGHT - border_wall_thickness, settings.SCREEN_WIDTH, border_wall_thickness)
        wall_sprite_list.add(border_wall_s)

        border_wall_w = Wall(0, 0, border_wall_thickness, settings.SCREEN_HEIGHT)
        wall_sprite_list.add(border_wall_w)

        return wall_sprite_list



class Brain(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("assets/brain.png"), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


if __name__ == '__main__':
    main()
