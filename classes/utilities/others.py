import math
import pygame

def distance_from_points(p1, p2):
    return math.sqrt(round((p2[0]-p1[0]), 2)**2 + round((p2[1] - p1[1]), 2)**2)

class Label:
    ''' CLASS FOR TEXT LABELS ON THE WIN SCREEN SURFACE '''
    def __init__(self, screen, text, x, y, font, size=20, color="white"):
        if size != 20:
            self.font = font
        else:
            self.font = font
        self.image = self.font.render(text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.text = text
    def change_text(self, newtext, color="white"):
        self.image = self.font.render(newtext, 1, color)
    def change_font(self, font, color="white"):
        self.font = font
        self.change_text(self.text, color)
    def draw(self):
        self.screen.blit(self.image, (self.rect))