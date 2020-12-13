import pygame
import window_sizing as ws
import constants as con

class Button(pygame.sprite.Sprite):

    def __init__(self, name, color, size, pos):
        super().__init__()

        self.image = pygame.Surface(size)
        self.color = color
        self.rect = self.image.get_rect()

        self.size = size
        self.pos = pos
        self.name = name

        self.font = pygame.font.SysFont("bell", 12)
        self.text_box = self.font.render(name, False, color, color)

        self.text_size = [self.text_box.get_width(), self.text_box.get_height()]


    def update(self, display):

        self.image.fill(self.color)

        # set dimentions as a scale of the display size
        width = int(display.get_width() * self.size[0])
        height = int(display.get_height() * self.size[1])

        # scale image to height and width
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        # set position
        self.rect.centerx = display.get_width() * self.pos[0]
        self.rect.centery = display.get_height() * self.pos[1]

        """
        try set size of box then
        scale box
        ccenter box
        blit text
        """

        # -- display text --
        # scale up the text box
        self.text_box = ws.fit_aspect_ratio(self.text_box, [16, 9], self.image, 1)

        # create the text
        self.text = self.font.render(self.name, True, con.RED, con.GREEN)        
        self.text = pygame.transform.scale(self.text, (self.text_box.get_size()))

        pos = (0, 0)
        pos = ws.center_surfaces(self.text, self.image)

        self.image.blit(self.text, (pos))