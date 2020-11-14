import pygame
import random

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

pygame.font.init()
font = pygame.font.SysFont("comicsansms", 26)
instru = font.render("Higher dropped hat = more points", True, BLUE)
qf = pygame.font.SysFont("comicsansms", 20)
q = qf.render("(resize the window)", True, BLACK)
points = 0
t = font.render(f"Points: {points}", True, RED)

class Bee:

    def __init__(self, img, loc, speed, key, happy, gen):
        self.gen = gen
        self.img = pygame.image.load(img)
        self.img.set_colorkey(key)
        self.happy_img = pygame.image.load(happy)
        self.happy_img.set_colorkey(key)

        self.Rect = pygame.Rect(self.img.get_rect())
        self.Rect.x = loc[0]
        self.Rect.y = loc[1]
        self.vy = 0
        self.vx = 0

        self.dx = random.randint(1,3) * (1 + self.gen * 0.1) 
        self.dy = random.randint(1,3) * (1 + self.gen * 0.1) 

        self.hitbox = pygame.Rect(10, 10, 10, 10)
        self.hit = False
        self.life = 60

    def run(self, screen):
        if not self.hit: self.draw(screen)
        if self.hit: self.happy(screen)

    def draw(self, screen):
        self.Rect.x += self.dx
        self.Rect.y += self.dy
        if self.Rect.bottom >= HEIGHT or self.Rect.top <= 0:
            self.dy *= -1

        if self.Rect.right >= WIDTH or self.Rect.left <= 0:
            self.dx *= -1
            self.img = pygame.transform.flip(self.img, True, False)

        self.hitbox.x = self.Rect.x + self.Rect.w - self.hitbox.w
        self.hitbox.y = self.Rect.y + self.Rect.h//2 - self.hitbox.h
        self.hitbox.w = self.Rect.w

        for hat in hats:
            if self.hitbox.colliderect(hat.Rect):
                self.hit = True
                hats.remove(hat)

        screen.blit(self.img, [self.Rect.x, self.Rect.y])

    def happy(self, screen):
            if self.life > 0:
                self.life -= 1
                self.Rect.y -= abs(self.dy // self.gen)
                screen.blit(self.happy_img, [self.Rect.x, self.Rect.y])

            if self.life <= 0:
                if len(bees) <= 5:
                    for i in range(random.randint(0,2)):
                        bees.append(Bee("bee.png", [0, 0], 3, WHITE, "happy.png", self.gen+1))
                
                hats.append(Hat("hat.png", [random.randint(0, WIDTH - 100), HEIGHT-10], WHITE))
                bees.remove(self)

class Hat:

    def __init__(self, img, loc, key):
        self.img = pygame.image.load(img)
        self.img.set_colorkey(key)
        self.Rect = pygame.Rect(self.img.get_rect())
        self.Rect.x = loc[0]
        self.Rect.y = loc[1]
        self.held = False
        self.vy = 0
        self.dy = 0.3


    def draw(self, mouse):
        global points
        if mouse_down and self.Rect.collidepoint(mouse):
            self.held = True
        elif not mouse_down:
            self.held = False

        if self.held:
            self.Rect.center = mouse
            self.vy = 0

        if not self.held:

            self.other_rects = []
            for hat in hats:
                if hat != self:
                    self.other_rects.append(hat.Rect)

            self.collist = []
            for hat in self.other_rects:
                if self.Rect.colliderect(hat) and self.Rect.x > hat.x:
                    self.Rect.bottom = hat.top
                    self.collist.append(hat)                    
                    self.vy = 0


            if len(self.collist) == 0: 
                if self.Rect.bottom >= HEIGHT:
                    self.Rect.bottom = HEIGHT
                    self.vy = 0
                self.vy += self.dy
                self.Rect.y += self.vy

            for bee in bees:
                if self.Rect.colliderect(bee.Rect):
                    if int(self.vy) > points:
                        points = int(self.vy)

        screen.blit(self.img, self.Rect)


bees = []
for i in range(3):
    bees.append(Bee("bee.png", [random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)], 3, WHITE, "happy.png", 1))

hats = []
for i in range(2):
    hats.append(Hat("hat.png", [random.randint(0, WIDTH - 100), random.randint(0, HEIGHT - 100)], WHITE))

mouse_down = False
done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            WIDTH = screen.get_width()
            HEIGHT = screen.get_height()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
    
    screen.fill(WHITE)

    if len(bees) <= 0:
        bees.append(Bee("bee.png", [0, 0], 3, WHITE, "happy.png", 1))

    screen.blit(instru, [10, 10])
    screen.blit(q, [10, 70])

    t = font.render(f"Highest Drop: {points}", True, RED)
    screen.blit(t, [10, 45])
    for bee in bees:
        bee.run(screen)

    for hat in hats:
        hat.draw(pygame.mouse.get_pos())


    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
