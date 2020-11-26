import pygame

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
        self.Rect = pygame.Rect(150, 150, 20, 40)
        self.color = color

    def move(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)


class Platform:
    def __init__(self, color, rect):
        self.Rect = rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)


# Create objects
player = Player(BLUE)
platforms = []
platforms.append(Platform(RED, pygame.Rect(0, 0, 300, 10)))
platforms.append(Platform(RED, pygame.Rect(0, 0, 10, 300)))
platforms.append(Platform(RED, pygame.Rect(0, 290, 300, 10)))
platforms.append(Platform(RED, pygame.Rect(290, 0, 10, 300)))
platforms.append(Platform(RED, pygame.Rect(150, 200, 100, 10)))


clock = pygame.time.Clock()
done = False
while not done:

    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Draw objects
    player.move()
    player.draw(screen)

    for platform in platforms:
        platform.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
