import pygame
import random
import sys

pygame.init()

# set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Granny Smith")

# load bg images
background_images = []
for i in range(4):
    image = pygame.image.load(f"background_{i}.png")
    image = pygame.transform.scale(image, (screen_width, screen_height))
    background_images.append(image)

# load sprites
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (80, 80))
player_size = player_image.get_width()

squirrel_image = pygame.image.load("squirrel.png")
squirrel_image = pygame.transform.scale(squirrel_image, (60, 60))

apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (40, 40))

tree_image = pygame.image.load("tree.png")
tree_image = pygame.transform.scale(tree_image, (130, 130))
tree_size = tree_image.get_width()

# player props
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 5
player_direction = "right"  # initial direction

# squirrel props
squirrel_x = random.randint(0, screen_width - player_size)
squirrel_y = random.randint(0, screen_height - player_size)
squirrel_speed = 1  
squirrel_direction = "right"  # initial direction

# tree and apple props
tree_positions = []
apple_positions = []
num_trees = 6

# map boundaries
world_width = background_images[0].get_width() * 2
world_height = background_images[0].get_height() * 2

# set tree positions
for i in range(num_trees):
    tree_placed = False
    attempts = 0
    while not tree_placed and attempts < 100:
        tree_x = random.randint(0, world_width - tree_size)
        tree_y = random.randint(0, world_height - tree_size)
        tile_x = tree_x // screen_width
        tile_y = tree_y // screen_height
        tile_type = (tile_x % 2 == 0 and tile_y % 2 == 0)  # make sure trees are only placed on tile 0

        if tile_type:
            tree_positions.append((tree_x, tree_y))
            tree_placed = True
        attempts += 1

# make sure the apples are on trees
for tree_pos in tree_positions:
    apple_x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
    apple_y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
    apple_positions.append((apple_x, apple_y))

# game loop
running = True
score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_direction = "left"
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_direction = "right"
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
                    tile_type = 2  # image 2 for odd rows and columns

            # Calc the position to blit the background image
            bg_x = column * background_images[tile_type].get_width() - view_x
            bg_y = row * background_images[tile_type].get_height() - view_y
            # Blit the bg image at the position
            screen.blit(background_images[tile_type], (bg_x, bg_y))

            if tile_type == 0:
                # Draw trees
                for tree_pos in tree_positions:
                    tree_screen_x = tree_pos[0] - view_x
                    tree_screen_y = tree_pos[1] - view_y
                    if bg_x <= tree_screen_x < bg_x + screen_width and bg_y <= tree_screen_y < bg_y + screen_height:
                        screen.blit(tree_image, (tree_screen_x, tree_screen_y))

    # Draw apples
    for apple_pos in apple_positions:
        screen.blit(apple_image, (apple_pos[0] - view_x, apple_pos[1] - view_y))


    # Draw player (and direction)
    if player_direction == "right":
        screen.blit(player_image, (player_x - view_x, player_y - view_y))
    else:
        flipped_player_image = pygame.transform.flip(player_image, True, False)
        screen.blit(flipped_player_image, (player_x - view_x, player_y - view_y))
    # Draw squirrel (and direction)
    if squirrel_direction == "left":
        screen.blit(squirrel_image, (squirrel_x - view_x, squirrel_y - view_y))
    else:
        flipped_squirrel_image = pygame.transform.flip(squirrel_image, True, False)
        screen.blit(flipped_squirrel_image, (squirrel_x - view_x, squirrel_y - view_y))

    pygame.display.flip()

pygame.quit()
sys.exit()
