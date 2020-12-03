import pygame
import math

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()

screen = pygame.display.set_mode([300, 300])
clock = pygame.time.Clock()


class Particle(pygame.sprite.Sprite):
    def __init__(self, dx, dy, x, y):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.image = pygame.Surface((5, 5))
        self.rect = pygame.Rect(100, 150, 5, 5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.mask = pygame.mask.from_surface(self.image)


class Platform(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.image = pygame.Surface([rect[2], rect[3]])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = rect[0]
        self.rect.centery = rect[1]


player_rect = pygame.Rect(100, 150, 10, 10)
particles = []
particle_group = pygame.sprite.Group()

platform_group = pygame.sprite.Group()
platform_group.add(Platform([50, 50, 300, 10]))

done = False
while not done:

    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if pygame.mouse.get_pressed()[0]:
            mousex = pygame.mouse.get_pos()[0]
            mousey = pygame.mouse.get_pos()[1]

            dx, dy = mousex - player_rect.centerx, mousey - player_rect.centery
            _len = math.hypot(dx, dy)
            dx, dy = dx/_len, dy/_len

            particle_group.add(Particle(dx, dy, player_rect.centerx, player_rect.centery))

    particle_group.update()
    platform_group.update()

    for platform in platform_group:
        collided = pygame.sprite.spritecollide(platform, particle_group, True)
        print(collided)

    particle_group.draw(screen)
    platform_group.draw(screen)

    # draw player
    pygame.draw.rect(screen, RED, player_rect)

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
