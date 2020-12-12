import pygame
import constants as con
import window_sizing
import buttons as b


def menu(screen, window):
    done = False

    buttons = pygame.sprite.Group()   
    buttons.add(b.Button("Enter", con.WHITE, [3/4, 1/3], [1/2, 1/3]))
    buttons.add(b.Button("Quit", con.BLACK, [3/4, 1/3], [1/2, 2/3]))

    while not done:

        # -- update things --
        screen.fill(con.RED)
        window.fill(con.GREEN)
        buttons.update(window)

        # -- handle events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # scale up window to fill screen
        window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen)
        window_pos = window_sizing.center_surfaces(window, screen)

        # draw buttons
        buttons.draw(window)
        screen.blit(window, window_pos)

        pygame.display.update()
        clock.tick(con.FPS)


def main(screen, display):

    done = False
    while not done:

        screen.fill(con.BLUE)
        display.fill(con.RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # scale up display to fill screen
        display = window_sizing.fit_aspect_ratio(display, con.ASPECT_RATIO, screen)
        window_pos = window_sizing.center_surfaces(display, screen)

        screen.blit(display, window_pos)
        pygame.display.update()
        clock.tick(con.FPS)


if __name__ == "__main__":
    pygame.display.init()
    screen = pygame.display.set_mode(con.SCREEN_SIZE, pygame.RESIZABLE)
    display = pygame.Surface([screen.get_width(), screen.get_height()])

    pygame.display.set_caption("Pygame boilerplate")
    clock = pygame.time.Clock()

    menu(screen, display)
  #  main(screen, display)
    pygame.quit()
