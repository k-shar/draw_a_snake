import pygame
import math

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

screen = pygame.display.set_mode([300, 300])

clock = pygame.time.Clock()

class Particle:
    def __init__(self, dx, dy, x, y):
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.Rect = pygame.Rect(100, 150, 5, 5)


    def draw(self, screen):
        self.x += self.dx
        self.y += self.dy
        self.Rect.centerx = self.x
        self.Rect.centery = self.y
        pygame.draw.rect(screen, BLUE, self.Rect)


particles = []

done = False
while not done:

    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


        if pygame.mouse.get_pressed()[0]:
            mousex = pygame.mouse.get_pos()[0]
            mousey = pygame.mouse.get_pos()[1]

            dx, dy = mousex - player_rect.x, mousey - player_rect.y 
            _len = math.hypot(dx, dy) 
            dx, dy = dx/_len, dy/_len

            particles.append(Particle(dx, dy, player_rect.x, player_rect.y))

    for particle in particles:
        particle.draw(screen)



    player_rect = pygame.Rect(100, 150, 10, 10)
    pygame.draw.rect(screen, RED, player_rect)
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()