import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 480
HEIGHT = 360
FPS = 60

# Initialise Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Py Game")
clock = pygame.time.Clock()

done = False
while not done:
    clock.tick(FPS)

    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        loc = pygame.mouse.get_pos()
        
        pressed = False
        if pygame.mouse.get_pressed()[0]:
            print(f"Left Mouse Click at {loc}")
            pressed = True

        if pygame.key.get_pressed()[pygame.K_a]:
            print("A pressed")
    
        
        # Crosshair settings
        if pressed:
            line = RED
            stroke = 2
        else:
            line = BLUE
            stroke = 1

        pygame.draw.line(screen, line, (0,0), (loc), stroke)
        pygame.draw.line(screen, line, (WIDTH,0), (loc), stroke)
        pygame.draw.line(screen, line, (0, HEIGHT), (loc), stroke)
        pygame.draw.line(screen, line, (WIDTH, HEIGHT), (loc), stroke)
        
        pygame.display.update()
pygame.quit()

