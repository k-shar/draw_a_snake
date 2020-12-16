import pygame
import main as m
import constants as con
import window_sizing
import buttons as b
import player as p
import levels as l
import window_sizing


def main(screen, window):

    # scale window on load
    window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen, 2)
    window_pos = window_sizing.center_surfaces(window, screen)

    # create a player
    player_group = pygame.sprite.Group()
    player = p.Player(con.BLUE, [1/2, 1/2], (1/16, 16/81), window)
    player_group.add(player)

    # current level
    current_level = l.Level_01(player)

    player.level = current_level

    clock = pygame.time.Clock()
    done = False
    while not done:
        window.fill(con.GREEN)
        screen.fill(con.BLUE)

        current_level.update(window)
        player_group.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen, 2)
                window_pos = window_sizing.center_surfaces(window, screen)
                player.resize(window)

        # Player movement if keydowns
        if pygame.key.get_pressed()[pygame.K_a]:
            player.move_left()
        if pygame.key.get_pressed()[pygame.K_d]:
            player.move_right()
        if pygame.key.get_pressed()[pygame.K_s]:
            player.move_down()
        if pygame.key.get_pressed()[pygame.K_w]:
            player.jump()

        current_level.draw(window)
        player_group.draw(window)
        # pygame.draw.rect(window, (0, 255, 255), r)
        # pygame.draw.rect(window, (255, 0, 255), r2)

        screen.blit(window, window_pos)

        pygame.display.update()
        clock.tick(con.FPS)


if __name__ == '__main__':

    screen, window = m.init()
    pygame.display.set_caption("game loop test")
    main(screen, window)

    pygame.quit()
