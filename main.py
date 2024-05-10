import pygame
import sys


# Set up screen
size = (800, 600)
screen = pygame.display.set_mode((size[0], size[1]))
pygame.display.set_caption("GAMEEEEEE")

# Background
bg_img = pygame.image.load("background.png").convert()

# Player size/speed
player_size = 50
player_x = size[0] // 2 - player_size // 2
player_y = size[1] // 2 - player_size // 2
player_speed = 5

# World size
world_width, world_height = 1600, 1200

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Make player stay in world boundaries
    player_x = max(0, min(world_width - player_size, player_x))
    player_y = max(0, min(world_height - player_size, player_y))

    # Calculate the view pos.
    view_x = max(0, min(world_width - size[0], player_x - size[0] // 2))
    view_y = max(0, min(world_height - size[1], player_y - size[1] // 2))

    # Draw the bg
    screen.blit(bg_img, (0 - view_x, 0 - view_y))

    # Drtw the player
    pygame.draw.rect(screen, (255, 255, 255), (player_x - view_x, player_y - view_y, player_size, player_size))

    # Update display
    pygame.display.flip()


# Endddd
pygame.quit()
sys.exit()