
import pygame
import sys

pygame.init()

# Set up
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GAMEEEEEE")

# Load background images into a list
background_images = []
for i in range(4):
    image = pygame.image.load(f"background_{i}.png")
    image = pygame.transform.scale(image, (screen_width, screen_height))
    background_images.append(image)

# Player props
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 5

# Map boundaries
world_width = background_images[0].get_width() * 2
world_height = background_images[0].get_height() * 2


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    player_x = max(0, min(world_width - player_size, player_x))
    player_y = max(0, min(world_height - player_size, player_y))

    view_x = max(0, min(world_width - screen_width, player_x - screen_width // 2))
    view_y = max(0, min(world_height - screen_height, player_y - screen_height // 2))

    for row in range(0, 2):
        # Loop through each column of background tiles
        for column in range(0, 2):
            # Determine the type of tile based on its position
            if row % 2 == 0:
                if column % 2 == 0:
                    tile_type = 0  #  image 0 for even rows and columns
                else:
                    tile_type = 3  #  image 3 for odd columns in even rows
            else:
                if column % 2 == 0:
                    tile_type = 1  # image 1 for even columns in odd rows
                else:
                    tile_type = 2   # image 2 for odd rows and columns

            # Calc the position to blit the background image
            bg_x = column * background_images[0].get_width() - view_x
            bg_y = row * background_images[0].get_height() - view_y

            # Blit the bg image at the position
            screen.blit(background_images[tile_type], (bg_x, bg_y))

    pygame.draw.rect(screen, (255, 255, 255), (player_x - view_x, player_y - view_y, player_size, player_size))

    pygame.display.flip()

pygame.quit()
sys.exit()
