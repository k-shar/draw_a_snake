import pygame

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.init()


class Screen:
    def __init__(self, size, title):
        self.surface = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

    def update(self):
        self.surface.fill(BLACK)


class Player:
    def __init__(self, color):
        self.Rect = pygame.Rect([50, 50], [30, 50])
        self.color = color

        self.gravity = 1
        self.speed = 4

        # to slow player down
        self.drag = 0.1

        # Velocity of player
        self.vx = 0
        self.vy = 0

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
        if pygame.key.get_pressed()[pygame.K_w]:
            dy -= self.speed
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
        self.Rect.x += dx
        for platform in platforms:
            if self.Rect.colliderect(platform.Rect):
                if dx > 0:
                    self.Rect.right = platform.Rect.left
                if dx < 0:
                    self.Rect.left = platform.Rect.right
                # Reset velocity when collision with wall
                self.vx = 0

        # handle movement on the Y axis
        self.Rect.y += dy
        for platform in platforms:
            if self.Rect.colliderect(platform.Rect):
                if dy > 0:
                    self.Rect.bottom = platform.Rect.top
                if dy < 0:
                    self.Rect.top = platform.Rect.bottom
                # Reset velocity when collision with floor or roof
                self.vy = 0

        # return correctly collided rect to draw()
        return self.Rect


class Platform:
    def __init__(self, Rect, color):
        self.Rect = Rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.Rect)


screen = Screen((300, 300), "Pygame test")
player = Player(BLUE)

platforms = []
floor = Platform(pygame.Rect(0, 280, 300, 20), RED)
wall = Platform(pygame.Rect(200, 100, 30, 340), RED)

platforms.append(floor)
platforms.append(wall)

clock = pygame.time.Clock()
done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.update()
    player.draw(screen.surface, platforms)

    for platform in platforms:
        platform.draw(screen.surface)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
