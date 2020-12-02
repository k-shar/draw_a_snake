import pygame
import math

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.display.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Platformer")


# the Player and their carrot shooting carrot gun
class Player(pygame.sprite.Sprite):
    def __init__(self, color, spawn_loc):
        super().__init__()

        self.img = pygame.Surface([20, 40])
        self.img.fill(color)
        self.Rect = self.img.get_rect()

        self.projectiles = []
        self.landed = False

        self.speed = 4
        self.jump_strength = -20

        self.bounce = -0.4
        self.drag = 0.8
        self.gravity = 1.5

        self.x = spawn_loc[0]
        self.y = spawn_loc[1]

        self.vx = 0
        self.vy = 0
        self.dx = 0
        self.dy = 0

    def move_left(self):
        self.dx -= self.speed

    def move_right(self):
        self.dx += self.speed

    def move_down(self):
        self.dy += self.speed

    def jump(self):
        if self.landed:
            self.vy = self.jump_strength
            self.landed = False

    def update(self):

        # Change velocity by drag constants
        self.dy += self.gravity
        self.vx *= self.drag

        # add change-in-velocity to total velocitiy
        self.vx += self.dx
        self.vy += self.dy

        # -- Testing for horizontal collisions --
        self.x += self.vx
        self.Rect.x = round(self.x)
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in platform_hit_list:
            # if collided traveling right
            if self.vx > 0:
                self.Rect.right = platform.Rect.left
            # if collided traveling left
            if self.vx < 0:
                self.Rect.left = platform.Rect.right

            self.x = self.Rect.x
            self.vx *= self.bounce

        # -- Testing for vertical collisions --
        self.y += self.vy
        self.Rect.y = round(self.y)
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in platform_hit_list:
            # if collided traveling down
            if self.vy > 0:
                self.Rect.bottom = platform.Rect.top
                self.landed = True
            # if collided traveling up
            if self.vy < 0:
                self.Rect.top = platform.Rect.bottom

            self.y = self.Rect.y
            self.vy *= self.bounce

class Level:
    pass
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()        
        self.player = player
        
class Level_01(Level):
    pass
# Platforms
platforms.append(Platform(RED, pygame.Rect(0, 0, 10, 300)))
platforms.append(Platform(RED, pygame.Rect(0, 290, 300, 10)))
platforms.append(Platform(RED, pygame.Rect(150, 200, 100, 10)))

# Create player
player = Player(BLUE, [100, 150])
player_sprite = pygame.sprite.Group()
player_sprite.add(player)
player.platforms = platform_list


clock = pygame.time.Clock()
done = False
while not done:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Player controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move_left()
            if event.key == pygame.K_d:
                player.move_right()
            if event.key == pygame.K_s:
                player.move_down()
            if event.key == pygame.K_w:
                player.jump()

    player_sprite.update()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
