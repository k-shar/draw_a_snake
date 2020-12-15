import pygame
import pygame.freetype
import window_sizing as ws
import constants as con

class Button(pygame.sprite.Sprite):

    def __init__(self, name, color, size, pos, font_col):
        super().__init__()

        self.color = color
        self.font_col = font_col
        self.size = size
        self.pos = pos
        self.name = name
        self.hover_color = (200, 100, 200)
        self.font = pygame.freetype.SysFont("bell", 12)

    def update(self, window, screen):

        # set dimentions of surface
        self.width = int(window.get_width() * self.size[0])
        self.height = int(window.get_height() * self.size[1])
        self.image = pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect()

        # set position of rect
        self.rect.centerx = window.get_width() * self.pos[0]
        self.rect.centery = window.get_height() * self.pos[1]

        self.image.fill(self.color)

        self.display_text()

    def display_text(self):
        # -- display text --
        text_box = self.font.get_rect(self.name, size=self.rect.height)
        text_box.center = self.image.get_rect().center
        self.font.render_to(self.image, text_box, self.name, self.font_col, size=self.rect.height)

    def click(self):
        return self.name

    def hover(self):
        self.image.fill(self.hover_color)        
        self.display_text()