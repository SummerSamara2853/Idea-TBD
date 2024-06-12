import pygame
import random

class Squirrel:
    def __init__(self, image, x, y, speed, direction="right"):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction

    def move_towards_apple(self, apple_positions):
        if apple_positions:
            closest_apple = apple_positions[0]
            closest_distance = abs(self.x - closest_apple[0]) + abs(self.y - closest_apple[1])
            for pos in apple_positions[1:]:
                distance = abs(self.x - pos[0]) + abs(self.y - pos[1])
                if distance < closest_distance:
                    closest_distance = distance
                    closest_apple = pos

            if self.x < closest_apple[0]:
                self.x += self.speed
                self.direction = "right"
            elif self.x > closest_apple[0]:
                self.x -= self.speed
                self.direction = "left"
            if self.y < closest_apple[1]:
                self.y += self.speed
            elif self.y > closest_apple[1]:
                self.y -= self.speed

    def draw(self, screen, view_x, view_y):
        if self.direction == "left":
            screen.blit(self.image, (self.x - view_x, self.y - view_y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x - view_x, self.y - view_y))
