import pygame
import random

FPS = 30
SIZE = (700, 500)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.init()
screen = pygame.display.set_mode(SIZE)

bg = pygame.image.load("bg.jpg").convert()
ship = pygame.image.load("player.png").convert()
ship.set_colorkey(BLACK)
bullet = pygame.image.load("proj.png").convert()
bullet.set_colorkey(WHITE)

class Proj:
    def __init__(self, obj, img):
        self.img = img
        self.centerX = obj[2]//2
        self.centerY = obj[3]//2
        self.loc = [pygame.mouse.get_pos()[0] + self.centerX + random.choice([-1*self.centerX, self.centerX]),
                    pygame.mouse.get_pos()[1] + self.centerY]


    def draw(self):
        self.loc = [self.loc[0], self.loc[1] - 15]
        screen.blit(self.img, self.loc)

proj_list = []

clock = pygame.time.Clock()
done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if pygame.mouse.get_pressed()[0]:
        proj_list.append(Proj(ship.get_rect(), bullet))

    loc = pygame.mouse.get_pos()

    screen.blit(bg, [0,0])
    screen.blit(ship, loc)

    for proj in proj_list:
        proj.draw()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
