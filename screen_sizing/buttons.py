import pygame

class Button(pygame.sprite.Sprite):

    def __init__(self, name, color, size, pos):
        super().__init__()

        self.image = pygame.Surface((0,0))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.size = size
        self.pos = pos

    def update(self, window):

        # set size
        self.rect.width = window.get_width() * self.size[0]
        self.rect.height = window.get_height() * self.size[1]

        # set position
        self.rect.centerx = window.get_width() * self.pos[0]
        self.rect.centery = window.get_height() * self.pos[1]
