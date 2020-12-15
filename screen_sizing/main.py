import pygame
import constants as con
import window_sizing
import buttons as b
import menu_loop
import game_loop

def init():
    pygame.display.init()
    pygame.font.init()
    pygame.freetype.init()

    screen = pygame.display.set_mode(con.SCREEN_SIZE, pygame.RESIZABLE)
    window = pygame.Surface([screen.get_width(), screen.get_height()])

    pygame.display.set_caption("Screen Sizing")
    return screen, window

if __name__ == "__main__":

    screen, window = init()
    menu_loop.main(screen, window)
    game_loop.main(screen, window)

    pygame.quit()
