import pygame
import constants as con
import window_sizing
import buttons as b


def menu(screen, window):
    done = False

    buttons = pygame.sprite.Group()
    buttons.add(b.Button("~Title~", con.BLUE, [3/4, 0.2], [1/2, 2/8], con.WHITE))
    buttons.add(b.Button("Enter",  con.RED, [3/4, 0.2], [1/2, 4/8], con.WHITE))
    buttons.add(b.Button("Quit",   con.BLACK, [3/4, 0.2], [1/2, 6/8], con.WHITE))

    while not done:

        # -- update things --
        screen.fill(con.RED)
        window.fill(con.GREEN)
        buttons.update(window, screen)

        # -- handle events --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                window = window_sizing.fit_aspect_ratio(window, con.ASPECT_RATIO, screen, 2)
                window_pos = window_sizing.center_surfaces(window, screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    mouse_relative_to_window = (pygame.mouse.get_pos()[0] - window_pos[0],
                                                pygame.mouse.get_pos()[1] - window_pos[1])

                    if button.rect.collidepoint(mouse_relative_to_window):
                        print(button.name)


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
    pygame.font.init()
    pygame.freetype.init()
    screen = pygame.display.set_mode(con.SCREEN_SIZE, pygame.RESIZABLE)
    display = pygame.Surface([screen.get_width(), screen.get_height()])

    pygame.display.set_caption("Screen Sizing")
    clock = pygame.time.Clock()

    menu(screen, display)
  #  main(screen, display)
    pygame.quit()
