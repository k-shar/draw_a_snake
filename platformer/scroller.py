import pygame

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = [300, 200]


class Player(pygame.sprite.Sprite):
    def __init__(self, color, spawn_loc, size):
        super().__init__()

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # For float computation
        self.x = spawn_loc[0]
        self.y = spawn_loc[1]

        # Rect can only store integer values
        self.rect.x = self.x
        self.rect.y = self.y

        self.landed = False

        self.speed = 2
        self.jump_strength = -20
        self.bounce = -0.4
        self.drag = 0.8
        self.gravity = 1.5
        self.recoil = 10

        self.dx, self.dy = 0, 0
        self.vx, self.vy = 0, 0

    def update(self):

        # Change velocity by drag constants
        self.dy += self.gravity
        self.vx *= self.drag

        # Add change in velocity to total velocitiy
        self.vx += self.dx
        self.vy += self.dy

        # -- Testing for horizontal collisions --
        self.x += self.vx
        self.rect.x = round(self.x)

        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in hit_list:

            # If collided traveling right
            if self.vx > 0:
                self.rect.right = platform.rect.left
            # If collided traveling left
            if self.vx < 0:
                self.rect.left = platform.rect.right

            self.x = self.rect.x
            self.vx *= self.bounce

        # -- Testing for vertical collisions --
        self.y += self.vy
        self.rect.y = round(self.y)

        hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for platform in hit_list:

            # If collided traveling down
            if self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.landed = True
            # If collided traveling up
            if self.vy < 0:
                self.rect.top = platform.rect.bottom

            self.y = self.rect.y
            self.vy *= self.bounce
            self.landed = True

        self.dx = 0
        self.dy = 0


def main():
    pygame.display.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Pygame boilerplate")

    player = Player(RED, [100, 100], [20, 40])

    clock = pygame.time.Clock()
    done = False
    while not done:

        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
