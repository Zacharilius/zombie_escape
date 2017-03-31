import constants
from player import Player
import pygame
import sprite_image

def main():
    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Zombie Escape')

    player = Player()

    active_sprite_list = pygame.sprite.Group()

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    clock = pygame.time.Clock()

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

        active_sprite_list.update()

        screen.fill(constants.WHITE)
        active_sprite_list.draw(screen)

        clock.tick(65)

        pygame.display.flip()

if __name__ == '__main__':
    main()
