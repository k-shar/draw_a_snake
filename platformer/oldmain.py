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


class Player:
    def __init__(self, color):
        self.Rect = pygame.Rect([50, 50], [20, 40])
        self.x = self.Rect.x
        self.y = self.Rect.y
        self.color = color

        self.gravity = 1
        self.speed = 5

        # to slow player down
        self.drag = 0.6

        # Velocity of player
        self.vx = 0
        self.vy = 0

        self.landed = False


    def draw(self, screen, platforms):

        # Change in x and y
        dx = 0
        dy = self.gravity

        # Process user input
        # Horizontal movement
        if pygame.key.get_pressed()[pygame.K_a]:
            dx -= self.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            dx += self.speed

        # Vertical movement
        if pygame.key.get_pressed()[pygame.K_w] and self.landed:
            dy -= self.speed * 4
            self.landed = False
        if pygame.key.get_pressed()[pygame.K_s]:
            dy += self.speed

        # Scale back player y velocity
        # as self.drag is less than 1
        self.vx *= self.drag

        self.vx += dx
        self.vy += dy

        # Test if collision is valid with move()
        self.Rect = Player.move(self, self.vx, self.vy, platforms)
        # Draw rect on screen
        pygame.draw.rect(screen, self.color, self.Rect)


    def move(self, dx, dy, platforms):
        # Test for collisions with platforms

        # handle movement on the X axis
        self.x += dx
        self.Rect.x = round(self.x)
        for platform in platforms:
            if self.Rect.colliderect(platform.Rect):
                if not self.hit:
                    self.vx *= -1
                self.hit = True
                if dx > 0:
                    self.Rect.right = platform.Rect.left
                    self.x = self.Rect.x
                if dx < 0:
                    self.Rect.left = platform.Rect.right
                    self.x = self.Rect.x
            else:
                self.hit = False
        # handle movement on the Y axis
        self.y += dy
        self.Rect.y = round(self.y)
        for platform in platforms:
            if self.Rect.colliderect(platform.Rect):
                if dy > 0:
                    self.Rect.bottom = platform.Rect.top
                    self.landed = True
                    self.y = self.Rect.y
                if dy < 0:
                    self.Rect.top = platform.Rect.bottom
                    self.y = self.Rect.y
                # Reset velocity when collision with floor or roof
                self.vy = 0

        # return correctly collided rect to draw()
        return self.Rect


class Carrot:
    def __init__(self, player, img):
        self.player = player
        self.img = pygame.image.load(img)
        self.img.set_colorkey(WHITE)
        self.img = pygame.transform.scale(self.img, (80, 30))
        self.Rect = self.img.get_rect()
        self.theta = 0

        self.reflected = False

    def draw(self, screen, platforms):
        # distances between mouse and carrot
        self.xdistance = pygame.mouse.get_pos()[0] - self.Rect.centerx
        self.ydistance = pygame.mouse.get_pos()[1] - self.Rect.centery

        # angle between mouse and carrot
        if self.xdistance != 0:
            self.theta = math.atan(-1 * self.ydistance / self.xdistance)
            self.theta = math.degrees(self.theta)
            # scale down theta between 0 and 180
            self.theta = self.theta - (self.theta//180) * 180
        else:
            self.theta = 0

        # correct for when theta needs to be above 180
        # when mouse is below the carrot
        if pygame.mouse.get_pos()[1] > self.Rect.centery:
            self.theta += 180

        # rotate carrot by theta
        self.rotated = pygame.transform.rotate(self.img, self.theta)
        self.Rect = self.rotated.get_rect(center=((player.x + player.Rect.w // 2, player.y + player.Rect.h // 3)))

        screen.blit(self.rotated, (self.Rect.x, self.Rect.y))

        print(self.theta)
    def fireCarrot(self):            

        dx, dy = pygame.mouse.get_pos()[0] - self.Rect.centerx, pygame.mouse.get_pos()[1] - self.Rect.centery 
        _len = math.hypot(dx, dy) 
        dx, dy = dx/_len, dy/_len
        carrotProjList.append(CarrotProj(screen, self.rotated, dx, dy, self.Rect.centerx, self.Rect.centery))



class CarrotProj:
    def __init__(self, screen, img, dx, dy, x, y):
        self.screen = screen
        self.img = img

        self.dx = dx
        self.dy = dy

        # for float accuracy
        self.x = x
        self.y = y
        # rect for collisions
        self.Rect = self.img.get_rect()

    def draw(self):

        self.x += self.dx
        self.y += self.dy
        self.Rect.centerx = self.x
        self.Rect.centery = self.y

        screen.blit(self.img, (self.Rect.x, self.Rect.y))



class Platform:
    def __init__(self, Rect, color):
        self.Rect = Rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)


player = Player(BLUE)
carrot = Carrot(player, "carrot.png")
carrotProjList = []

platforms = []
platforms.append(Platform(pygame.Rect(0, 280, 300, 20), RED))  # floor
platforms.append(Platform(pygame.Rect(0, 0, 300, 20), RED))  # roof
platforms.append(Platform(pygame.Rect(0, 0, 20, 300), RED))
platforms.append(Platform(pygame.Rect(280, 0, 20, 300), RED))  # Walls

platform_rects = []
for platform in platforms:
    platform_rects.append(platform.Rect)


clock = pygame.time.Clock()
done = False
while not done:
    # Every frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            Carrot.fireCarrot(carrot)

    # Clear the screen
    screen.fill(BLACK)
    player.draw(screen, platforms)
    carrot.draw(screen, platforms)

    for carrotProj in carrotProjList:
        carrotProj.draw()
       # if carrotProj.Rect.collidelist(platform_rects) != -1:
          #  carrotProjList.remove(carrotProj)

    for platform in platforms:
        platform.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
