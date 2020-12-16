import pygame


class Player(pygame.sprite.Sprite):
    ''' 
    This class represents the player 
    and their carrot shooting carrot launcher 
    '''

    # (color, (x, y), (width, height))
    # as fractions of window width and height
    # window will stay fixed aspect ratio
    def __init__(self, color, spawn_loc, size, window):
        ''' Constructor function '''
        super().__init__()

        # size as fractions
        self.frac_size = size
        self.frac_pos = spawn_loc

        # dummy surface thats actually set in update
        self.image = pygame.Surface((0, 0))

        self.color = color
        self.level = None
        self.landed = False

        self.dx, self.dy = 0, 0
        self.vx, self.vy = 0, 0

        self.resize(window)

    def update(self, window):
        self.image.fill(self.color)

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

        # set fractional player pos incase of screen resize
        try:
            self.frac_pos[0] = self.x / window.get_width()
            self.frac_pos[1] = self.y / window.get_height()
        except:
            # division by 0
            pass

        self.dx = 0
        self.dy = 0

    def resize(self, window):

        # -- set stats --
        self.speed = 0.005 * window.get_width()
        self.jump_strength = -0.1 * window.get_height()
        self.gravity = 0.0075 * window.get_height()

        self.bounce = -0.4
        self.drag = 0.8
        self.recoil = 10

        # -- size the player --
        self.width = int(self.frac_size[0] * window.get_width())
        self.height = int(self.frac_size[1] * window.get_height())
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

        # -- pos of the player --
        self.x = self.frac_pos[0] * window.get_width()
        self.y = self.frac_pos[1] * window.get_height()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

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
