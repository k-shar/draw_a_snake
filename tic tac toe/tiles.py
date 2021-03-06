import pygame
from constants import *
import random
from window_resizing import *


class MousePointer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 5, 5)

    def update(self, offset):
        self.offset = offset
        self.rect.x = pygame.mouse.get_pos()[0] - offset[0]
        self.rect.y = pygame.mouse.get_pos()[1] - offset[1]

        self.image = pygame.Surface((5, 5))


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, window, key, side):
        super().__init__()

        self.pos = pos
        self.key = key
        self.image = pygame.Surface((window.get_width() // 3, window.get_height() // 3))
        if side == "main":
            self.color = (random.randint(240, 250), random.randint(110, 120), random.randint(40, 50))
        if side == "analysis":
            self.color = (random.randint(40, 50), random.randint(150, 160), random.randint(120, 130))

        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.state = "."

    def update(self, window):
        self.image = pygame.transform.scale(self.image, (window.get_width() // 3, window.get_height() // 3))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = int((window.get_width() / 3) * self.pos[0])
        self.rect.y = int((window.get_height() / 3) * self.pos[1])

        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.o = self.image.get_width() * 0.1  # offset or padding
        if self.state == "X":
            # drawing of a cross
            pygame.draw.polygon(self.image, BLACK, [(self.o, self.o), (self.w//2 - self.o, self.h//2),
                                                    (self.o, self.h - self.o), (2 * self.o, self.h - self.o),
                                                    (self.w//2, self.h//2), (self.w - 2*self.o, self.h - self.o),
                                                    (self.w - self.o, self.h - self.o), (self.w//2 + self.o, self.h//2),
                                                    (self.w - self.o, self.o), (self.w - 2*self.o, self.o), (self.w//2, self.h//2),
                                                    (self.o * 2, self.o)
                                                    ])
        if self.state == "O":
            # drawing of a naught
            pygame.draw.circle(self.image, BLACK, (self.w//2, self.h//2), int(self.w // 2 - self.o), int(self.o))

    def player_click(self): self.state = "X"


class TextSurface(pygame.sprite.Sprite):

    def __init__(self, text, color):
        super().__init__()
        self.image = pygame.Surface((1, 1))
        self.image.fill(YELLOW)

        self.color = color
        self.font_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.text = text

    def resize(self, scale, outer_surf, ratio, x, y, offset):
        self.image, self.rect, _ = resize_surfaces(scale, self.image, outer_surf, ratio, x, y, offset)

    def display_text(self):
        # might throw error if screen is tooo small...
        # font size is too small to render?
        try:
            self.font = pygame.freetype.SysFont("bell", self.image.get_height() * 0.6)
            self.image.fill(self.color)
            text, text_rect = self.font.render(self.text, fgcolor=(255, 255, 255))
            self.image.blit(text, text.get_rect(center=self.image.get_rect().center))
        except:
            print("oh no, you squished the screen too much? :/")


class Button(TextSurface):
    def __init__(self, text, color):
        super().__init__(text, color)
        self.rect = self.image.get_rect()

    def on_click(self):
        pass
