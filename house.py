import pygame

class House:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self, screen, view_x, view_y):
        screen.blit(self.image, (self.x - view_x, self.y - view_y))
