import pygame
import random

class Grandma:
    def __init__(self, image, x, y, request):
        self.image = image
        self.x = x
        self.y = y
        self.request = request
        self.font = pygame.font.Font(None, 24)
        self.text_bubble = self.font.render(f"I need {self.request} apples!", True, (255, 255, 255))

    def draw(self, screen, view_x, view_y):
        screen.blit(self.image, (self.x - view_x, self.y - view_y))
        screen.blit(self.text_bubble, (self.x - view_x, self.y - view_y - 30))

    def check_request_fulfilled(self, player_rect, player_apples):
        grandma_rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        if player_rect.colliderect(grandma_rect) and player_apples >= self.request:
            return True
        return False
