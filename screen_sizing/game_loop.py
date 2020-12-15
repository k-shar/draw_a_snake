import pygame
import main as m
import constants as con
import window_sizing
import buttons as b


def main(screen, window):

    window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen, 2)
    window_pos = window_sizing.center_surfaces(window, screen)

    clock = pygame.time.Clock()
    done = False

    while not done:

        # -- update things --
        screen.fill(con.RED)
        window.fill(con.GREEN)

        # -- handle events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen, 2)
                window_pos = window_sizing.center_surfaces(window, screen)

        screen.blit(window, window_pos)

        pygame.display.update()
        clock.tick(con.FPS)


if __name__ == '__main__':

    screen, window = m.init()
    main(screen, window)

    pygame.quit()
