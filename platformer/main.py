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
class Player:
    def __init__(self, color, spawn_loc):
        self.Rect = pygame.Rect([spawn_loc, [20, 40]])
        self.color = color
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

    # To handle keypresses
    def playerInput(self):

        # Change in velocity this frame
        self.dx = 0
        self.dy = 0

        # Horizontal movement
        if pygame.key.get_pressed()[pygame.K_d]:
            self.dx += self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            self.dx -= self.speed

        # Vertical movement
        if pygame.key.get_pressed()[pygame.K_s]:
            self.dy += self.speed
        if pygame.key.get_pressed()[pygame.K_w] and self.landed:
            self.vy = self.jump_strength
            self.landed = False

        # Change velocity by drag constants
        self.dy += self.gravity
        self.vx *= self.drag

        # add change in velocity t0 total velocitiy
        self.vx += self.dx
        self.vy += self.dy

        # test if this movement is valid
        self.rectifyCollisions()

    # Testing for collisions with platforms
    def rectifyCollisions(self):

        # Testing for horizontal collisions
        self.x += self.vx
        self.Rect.x = round(self.x)

        for platform in self.platforms:
            if self.Rect.colliderect(platform.Rect):

                # if collided traveling right
                if self.vx > 0:
                    self.Rect.right = platform.Rect.left
                # if collided traveling left
                if self.vx < 0:
                    self.Rect.left = platform.Rect.right

                self.x = self.Rect.x
                self.vx *= self.bounce

        # Testing for vertical collisions
        self.y += self.vy
        self.Rect.y = round(self.y)

        for platform in self.platforms:
            if self.Rect.colliderect(platform.Rect):

                # if collided traveling down
                if self.vy > 0:
                    self.Rect.bottom = platform.Rect.top
                    self.landed = True
                # if collided traveling up
                if self.vy < 0:
                    self.Rect.top = platform.Rect.bottom

                self.y = self.Rect.y
                self.vy *= self.bounce

    # Drawing the player rect on screen
    def draw(self, screen, platfomrs):
        self.screen = screen
        self.platforms = platforms

        self.playerInput()
        pygame.draw.rect(screen, self.color, self.Rect)


# Carrot the player holds, used to shoot other carrots
class Carrot:
    def __init__(self, platforms):
        self.platforms = platforms

        self.img = pygame.image.load("carrot.png")
        self.img = pygame.transform.scale(self.img, (80, 30))
        self.img.set_colorkey(WHITE)

        self.Rect = self.img.get_rect()

        self.proj_list = []

    # draw the carrot onscreen
    def draw(self, player):
        self.drawCarrot(player)

    # Draw carrot the player holds
    def draw(self, player):

        # Distances between mouse and carrot
        self.xdis = pygame.mouse.get_pos()[0] - self.Rect.centerx
        self.ydis = pygame.mouse.get_pos()[1] - self.Rect.centery

        # Calculate the angle between self and mouse pointer
        if self.xdis != 0:
            self.theta = math.atan(-1 * self.ydis / self.xdis)
            self.theta = math.degrees(self.theta)

            # scale down theta between 0 and 180
            # as arctan returns negative values
            self.theta = self.theta - (self.theta//180) * 180

        # Convert the angle to 0-360 opposed to 0-180
        if pygame.mouse.get_pos()[1] > self.Rect.centery:
            self.theta += 180

        # To avoid division by 0
        if self.xdis == 0:
            self.theta = 90.0

        # Rotate img by theta
        self.rotated = pygame.transform.rotate(self.img, self.theta)
        self.Rect = self.rotated.get_rect(center=((player.x + player.Rect.w // 2, player.y + player.Rect.h // 3)))

        # Blit rotated img
        screen.blit(self.rotated, (self.Rect.x, self.Rect.y))
        print(self.theta)

    def fireCarrot(self, proj_list):
        dx = pygame.mouse.get_pos()[0] - self.Rect.centerx
        dy = pygame.mouse.get_pos()[1] - self.Rect.centery

        hypot = math.hypot(dx, dy)
        dx /= hypot
        dy /= hypot

        proj_list.append(CarrotProj(screen, self.rotated, dx, dy, self.Rect.centerx, self.Rect.centery))

# Drawing projectiles shot by main carrot


class CarrotProj:
    def __init__(self, screen, img, dx, dy, x, y):
        self.screen = screen
        self.img = img

        self.speed = 2
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.vx = 0
        self.vy = 0

        # for float accuracy
        self.x = x
        self.y = y
        self.pos = [self.x, self.y]

        # rect for collisions
        self.Rect = self.img.get_rect()

    def draw(self):

        self.vx += self.dx
        self.vy += self.dy

        self.x += self.vx
        self.y += self.vy
        self.pos = [self.x, self.y]

        self.Rect.centerx = self.x
        self.Rect.centery = self.y

        screen.blit(self.img, (self.Rect.x, self.Rect.y))


# Displaying platforms
class Platform:
    def __init__(self, color, rect):
        self.Rect = rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)


# Create platforms
platforms = []
platforms.append(Platform(RED, pygame.Rect(0, 0, 300, 10)))
platforms.append(Platform(RED, pygame.Rect(0, 0, 10, 300)))
platforms.append(Platform(RED, pygame.Rect(0, 290, 300, 10)))
platforms.append(Platform(RED, pygame.Rect(290, 0, 10, 300)))
platforms.append(Platform(RED, pygame.Rect(150, 200, 100, 10)))

# Create player
player = Player(BLUE, [100, 150])
carrot = Carrot(platforms)
carrot_proj_list = []


clock = pygame.time.Clock()
done = False
while not done:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # fire carrot on mousedown
        if event.type == pygame.MOUSEBUTTONDOWN:
            carrot.fireCarrot(carrot_proj_list)
    # Draw
    player.draw(screen, platforms)
    carrot.draw(player)

    for carrot_proj in carrot_proj_list:
        carrot_proj.draw()

        # delete carrot if not on screen
        if not carrot_proj.Rect.colliderect(screen.get_rect()):
            carrot_proj_list.remove(carrot_proj)

        # delete if carrots center collides with platform
        for platform in platforms:
            if platform.Rect.collidepoint(carrot_proj.pos):
                carrot_proj_list.remove(carrot_proj)

    for platform in platforms:
        platform.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
