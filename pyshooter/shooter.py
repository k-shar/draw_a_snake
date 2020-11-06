import pygame
import random

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.init()

BG = pygame.image.load("bg.jpg")
screen = pygame.display.set_mode(BG.get_rect().size)
BG.convert()

class Proj:
    def __init__(self, obj, img):
        self.img = img
        self.centerX = obj[2]//2
        self.centerY = obj[3]//2
        self.loc = [pygame.mouse.get_pos()[0] + self.centerX + random.choice([-1*self.centerX, self.centerX]),
                    pygame.mouse.get_pos()[1] + self.centerY]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.Rect = pygame.Rect([self.loc, [self.width, self.height]])

    def draw(self):
        self.loc = [self.loc[0], self.loc[1] - 15]
        self.Rect = pygame.Rect([self.loc, [self.width, self.height]])
        screen.blit(self.img, self.loc)

class Player:
    def __init__(self, img, key, proj_img, proj_key):

        self.img = pygame.image.load(img).convert()
        self.img.set_colorkey(key)

        self.proj_img = pygame.image.load(proj_img).convert()
        self.proj_img.set_colorkey(proj_key)

        self.proj_list = []

    def draw(self, loc):
        self.loc = loc
        screen.blit(self.img, self.loc)

        for proj in self.proj_list:

            # If projectile is not on screen
            if not proj.Rect.colliderect(screen.get_rect()):
                self.proj_list.remove(proj)
            else:
                proj.draw()

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot(self):
        self.proj_list.append(Proj(self.img.get_rect(), self.proj_img))


player = Player("player.png", WHITE, "proj.png", WHITE)

clock = pygame.time.Clock()
done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(BG, [0, 0])

    loc = pygame.mouse.get_pos()
    player.draw(loc)
    pygame.draw.rect(screen, RED, [300, 200, 50, 50])

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
