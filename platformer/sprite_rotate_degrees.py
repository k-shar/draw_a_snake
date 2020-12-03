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
pygame.display.set_caption("Platformer 2")


class Player(pygame.sprite.Sprite):
    ''' 
    This class represents the player 
    and their carrot shooting carrot launcher 
    '''

    def __init__(self, color, spawn_loc):
        ''' Constructor function '''
        super().__init__()

        self.image = pygame.Surface([20, 40])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.level = None

        # For float computation
        self.x = spawn_loc[0]
        self.y = spawn_loc[1]

        # Rect can only store integer values
        self.rect.x = self.x
        self.rect.y = self.y

        self.landed = False

        self.speed = 4
        self.jump_strength = -20
        self.bounce = -0.4
        self.drag = 0.8
        self.gravity = 1.5

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

    # Horizontal movement on keypress

    def move_left(self):
        self.dx -= self.speed

    def move_right(self):
        self.dx += self.speed

    # Vertical movement on keypress
    def move_down(self):
        self.dy += self.speed

    def jump(self):
        if self.landed:
            self.vy = self.jump_strength
            self.landed = False


class CarrotShooter(pygame.sprite.Sprite):
    '''
    Class for the carrot the player wields
    '''

    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("carrot.png")
        self.image = pygame.transform.scale(self.image, (80, 30))
        self.image.set_colorkey(WHITE)

        self.orig_img = self.image

        self.rect = self.image.get_rect()
        self.player = player

    def update(self):
        # Distances between mouse and carrot
        self.xdis = pygame.mouse.get_pos()[0] - self.rect.centerx
        self.ydis = pygame.mouse.get_pos()[1] - self.rect.centery

        # Calculate the angle between self and mouse pointer
        if self.xdis != 0:
            self.theta = math.atan(-1 * self.ydis / self.xdis)
            self.theta = math.degrees(self.theta)
            # scale down theta between 0 and 180
            # as arctan returns negative values
            self.theta = self.theta - (self.theta//180) * 180

        # Convert the angle to 0-360 opposed to 0-180
        if pygame.mouse.get_pos()[1] > self.rect.centery:
            self.theta += 180

        # to handle edge cases
        if self.theta == 0:
            if self.rect.centerx > pygame.mouse.get_pos()[0]:
                self.theta = -180
            if self.rect.centerx < pygame.mouse.get_pos()[0]:
                self.theta = 0

            if self.rect.centery > pygame.mouse.get_pos()[1]:
                self.theta = 90
            if self.rect.centery < pygame.mouse.get_pos()[1]:
                self.theta = -90

        # Redefine Sprite with new rotated rect and suface
        self.image = pygame.transform.rotate(self.orig_img, self.theta)
        self.rect = self.image.get_rect(center=((self.player.x + self.player.rect.w // 2, self.player.y + self.player.rect.h // 3)))



class Platform(pygame.sprite.Sprite):
    '''
    Class for platforms 
    '''

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()


class Level:
    '''
    Superclass for a base level
    '''

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()

    def draw(self, screen):
        self.platform_list.draw(screen)


class Level_01(Level):
    '''
    Child of Level to hold data about level 1
    such as location and size of platforms
    '''

    def __init__(self, player):
        Level.__init__(self, player)

        # x, y, width, height
        level = [
            [0, 0, 10, 300],
            [0, 290, 300, 10],
            [150, 200, 100, 10]
        ]

        for platform in level:
            block = Platform(platform[2], platform[3])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            self.platform_list.add(block)


# Define player components
player = Player(BLUE, [100, 150])
carrot_shooter = CarrotShooter(player)

# Create sprite group for player
player_sprite_group = pygame.sprite.Group()
player_sprite_group.add(player)
player_sprite_group.add(carrot_shooter)

# Create list of all levels
level_list = []
level_list.append(Level_01(player))

# Set current level to first list item
current_level_no = 0
current_level = level_list[current_level_no]
player.level = current_level

clock = pygame.time.Clock()
done = False
while not done:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Player movement if keydown
    if pygame.key.get_pressed()[pygame.K_a]:
        player.move_left()
    if pygame.key.get_pressed()[pygame.K_d]:
        player.move_right()
    if pygame.key.get_pressed()[pygame.K_s]:
        player.move_down()
    if pygame.key.get_pressed()[pygame.K_w]:
        player.jump()

    current_level.update()
    player_sprite_group.update()

    current_level.draw(screen)
    player_sprite_group.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
