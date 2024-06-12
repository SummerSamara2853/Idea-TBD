import pygame

class Player:
    def __init__(self, image, x, y, speed, direction="left"):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.size = image.get_width()

    def move(self, keys, world_width, world_height):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(world_width - self.size, self.x))
        self.y = max(0, min(world_height - self.size, self.y))

    def draw(self, screen, view_x, view_y):
        if self.direction == "left":
            screen.blit(self.image, (self.x - view_x, self.y - view_y))
        else:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, (self.x - view_x, self.y - view_y))