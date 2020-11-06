import pygame

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Initialise Pygame
pygame.init()
pygame.display.set_caption("Epic Py Game")

# Load background image
# BG = pygame.image.load("bg.jpg")
# screen = pygame.display.set_mode(BG.get_rect().size)
# BG.convert()
# BG_blit = BG

screen = pygame.display.set_mode([300, 400])

clock = pygame.time.Clock()

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        pressed = False
        loc = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            print(f"Left Mouse Click at {loc}")
            pressed = True

        if pygame.key.get_pressed()[pygame.K_a]:
            print("A pressed")

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # BG_blit = pygame.transform.scale(BG, screen.get_size())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

        # Crosshair settings
        if pressed:
            line = RED
            stroke = 2
        else:
            line = BLUE
            stroke = 1

        # For BG image
        # screen.blit(BG_blit, [0, 0])
        screen.fill(WHITE)

        pygame.draw.line(screen, line, (0, 0), (loc), stroke)
        pygame.draw.line(screen, line, (screen.get_rect()[2], 0), (loc), stroke)
        pygame.draw.line(screen, line, (0, screen.get_rect()[3]), (loc), stroke)
        pygame.draw.line(screen, line, (screen.get_rect()[2], screen.get_rect()[3]), (loc), stroke)

        clock.tick(FPS)
        pygame.display.update()
pygame.quit()
