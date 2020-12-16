import pygame
import constants


class Platform(pygame.sprite.Sprite):

    def __init__(self, width, height, pos):
        super().__init__()

        self.width_scale = width
        self.height_scale = height
        self.pos = pos

        # dummy surface and rect, changed in update
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

    def update(self, window):

        # scale width and height proportional to window size
        self.width = int(self.width_scale * window.get_width())
        self.height = int(self.height_scale * window.get_height())
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()

        # scale pos of rect
        self.rect.x = self.pos[0] * window.get_width()
        self.rect.y = self.pos[1] * window.get_height()


class Level:
    '''
    Superclass for a base level
    '''

    def __init__(self, player):
        # Create list of all platforms the player interacts with
        self.platform_list = pygame.sprite.Group()
        self.player = player

    def update(self, window):
        self.platform_list.update(window)

    def draw(self, surface):
        self.platform_list.draw(surface)


class Level_01(Level):

    def __init__(self, player):
        super().__init__(player)

        # width, height, x, y
        p_list = [
            [1, 1, -7/8, 0],
            [1, 1, 0, 7/8],
            [1/3, 1/8, 2/3, 1/3]
        ]

        for p in p_list:
            self.platform_list.add(Platform(p[0], p[1], (p[2], p[3])))
