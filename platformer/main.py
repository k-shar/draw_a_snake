import pygame
import math
import random

FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.display.init()
screen = pygame.display.set_mode((600, 600))
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

    def fired_carrot(self, carrot):
        self.vx -= carrot.dx * self.recoil
        self.vy -= carrot.dy * self.recoil


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
        self.pos = [self.rect.centerx, self.rect.centery]
        self.theta = calculateAngle(pygame.mouse.get_pos(), self.pos)
        # Redefine Sprite with new rotated rect and suface
        self.image = pygame.transform.rotate(self.orig_img, self.theta)
        self.rect = self.image.get_rect(center=((self.player.x + self.player.rect.w // 2,
                                                 self.player.y + self.player.rect.h // 3)))


class CarrotProj(pygame.sprite.Sprite):
    '''
    Class for individulal carrots shot from player
    '''

    def __init__(self, main_carrot):
        super().__init__()
        self.image = pygame.image.load("carrot.png")
    #    self.image = pygame.transform.scale(self.image, (80, 30))
        self.image = pygame.transform.scale(self.image, (40, 15))
        self.image.set_colorkey(WHITE)
        # copy of img to prevent deep frying when rotating
        self.orig_img = self.image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        # -- CARROT STATS --
        # set how fast the carrot accelerates
        self.acc = 5
        self.life = 20
        self.deflection = 15

        # -- rotation --
        self.pos = [main_carrot.rect.centerx, main_carrot.rect.centery]
        self.theta = calculateAngle(pygame.mouse.get_pos(), self.pos)

        # Redefine Sprite with new rotated rect and suface
        self.image = pygame.transform.rotate(self.orig_img, self.theta)
        self.rect = self.image.get_rect(center=((main_carrot.rect.x + main_carrot.rect.w // 2,
                                                 main_carrot.rect.y + main_carrot.rect.h // 3)))

        # for float accuracy
        self.x = main_carrot.rect.centerx
        self.y = main_carrot.rect.centery

        # set dx, dy as distance from center to mouse pointer
        self.dx = (pygame.mouse.get_pos()[0] - self.x) + random.randint(-1 * self.deflection, self.deflection)
        self.dy = (pygame.mouse.get_pos()[1] - self.y) + random.randint(-1 * self.deflection, self.deflection)

        # scale down dx dy so all angles will fire at the same speed
        self.hypot = math.hypot(self.dx, self.dy)
        self.dx /= self.hypot
        self.dy /= self.hypot

        self.vx, self.vy = 0, 0

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)

        # compound dx, dy to accelerate the carrot
        self.vx += self.dx
        self.vy += self.dy

        self.x += self.vx * self.acc
        self.y += self.vy * self.acc

        # set calculated values to the sprites rect
        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.life -= 1
        if self.life <= 0:
            self.kill()


class Platform(pygame.sprite.Sprite):
    '''
    Class for platforms 
    '''

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height], pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect()


class Level:
    '''
    Superclass for a base level
    '''

    def __init__(self, player):
        # Create list of all platforms the player interacts with
        self.platform_list = pygame.sprite.Group()
        # Create list of objects that destroy carrots
        self.destroy_carrot = pygame.sprite.Group()
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
            #[0, 0, 10, 300, False], 
            [0, 290, 3000, 10, False],
            [150, 200, 100, 10, True],
            #[0, 0, 300, 10, False],
            #[290, 0, 10, 300, False]
        ]

        for platform in level:
            block = Platform(platform[2], platform[3])
            block.rect.x = platform[0]
            block.rect.y = platform[1]
            self.platform_list.add(block)

            # Add to list of spries that destroy carrot on impact
            if platform[4]:
                self.destroy_carrot.add(block)


def calculateAngle(p1, p2):
    '''
    return the angle between two points
    in degrees from 0-360
    0 being the positive x-axis
    '''
    # Distances between p1 and p2
    xdis = p1[0] - p2[0]
    ydis = p1[1] - p2[1]

    # Calculate the angle between p1 and mouse p2
    # Avoid division by 0
    if xdis != 0:
        theta = math.atan(-1 * ydis / xdis)
        theta = math.degrees(theta)
        # scale down theta between 0 and 180
        # as arctan returns negative values
        theta = theta - (theta//180) * 180

        # Convert the angle from 0-180 to 0-360
        if p1[1] > p2[1]:
            theta += 180

        # Edge case for when points are inline on y-axis
        if p1[1] == p2[1]:
            theta = 180

    # When xdis is 0
    else:
        # If p1 is above p2
        if p1[1] < p2[1]:
            theta = 90
        # If p1 is below p2
        if p1[1] > p2[1]:
            theta = 270

    return theta


# Define player components
player = Player(BLUE, [100, 150])
carrot_shooter = CarrotShooter(player)

# Create sprite group for player
player_sprite_group = pygame.sprite.Group()
player_sprite_group.add(player)
player_sprite_group.add(carrot_shooter)

# Define list of player-projectiles
carrot_proj_list = pygame.sprite.Group()

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            carrot = CarrotProj(carrot_shooter)
            player.fired_carrot(carrot)
            carrot_proj_list.add(carrot)

    # Player movement if keydowns
    if pygame.key.get_pressed()[pygame.K_a]:
        player.move_left()
    if pygame.key.get_pressed()[pygame.K_d]:
        player.move_right()
    if pygame.key.get_pressed()[pygame.K_s]:
        player.move_down()
    if pygame.key.get_pressed()[pygame.K_w]:
        player.jump()

    carrot_proj_list.update()
    player_sprite_group.update()
    current_level.update()

    # Remove collided carrots
    for platform in current_level.destroy_carrot:
        col = pygame.sprite.spritecollide(platform, carrot_proj_list, True, pygame.sprite.collide_mask)

    carrot_proj_list.draw(screen)
    player_sprite_group.draw(screen)
    current_level.draw(screen)

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
