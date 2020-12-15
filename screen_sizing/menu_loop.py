import pygame
import main as m
import constants as con
import window_sizing
import buttons as b

def main(screen, window):
    done = False
    clock = pygame.time.Clock()


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
                # Check all buttons
                for button in buttons:
                    # see if they have been clicked
                    mouse_relative_to_window = (pygame.mouse.get_pos()[0] - window_pos[0], pygame.mouse.get_pos()[1] - window_pos[1])
                    if button.rect.collidepoint(mouse_relative_to_window):
                        button_action = button.click()

                        if button_action == "Quit":
                            done = True

        # -- button on hover --
        # Check all buttons
        for button in buttons:
            # see if mouse is above the button
            mouse_relative_to_window = (pygame.mouse.get_pos()[0] - window_pos[0], pygame.mouse.get_pos()[1] - window_pos[1])
            if button.rect.collidepoint(mouse_relative_to_window):
                button.hover()


        # draw buttons
        buttons.draw(window)
            
        screen.blit(window, window_pos)

        pygame.display.update()
        clock.tick(con.FPS)

if __name__ == '__main__':

    screen, window = m.init()
    pygame.display.set_caption("Menu test")

    main(screen, window)
    pygame.quit()