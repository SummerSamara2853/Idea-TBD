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

# load character sprites
p1_image = pygame.image.load("p1.png")
p1_image = pygame.transform.scale(p1_image, (80, 80))

p2_image = pygame.image.load("p2.png")
p2_image = pygame.transform.scale(p2_image, (60, 80))

p3_image = pygame.image.load("p3.png")
p3_image = pygame.transform.scale(p3_image, (60, 80))

# load other sprites
squirrel_image = pygame.image.load("squirrel.png")
squirrel_image = pygame.transform.scale(squirrel_image, (70, 70))

apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (40, 40))

tree_image = pygame.image.load("tree.png")
tree_image = pygame.transform.scale(tree_image, (130, 130))
tree_size = tree_image.get_width()

# function to display character selection screen
def character_selection():
    selected_character = None
    while not selected_character:
        screen.fill((59, 40, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Select your character!!!!!", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))

        # display characters
        screen.blit(p1_image, (screen_width // 2 - 200, 300))
        screen.blit(p2_image, (screen_width // 2 - 40, 300))
        screen.blit(p3_image, (screen_width // 2 + 120, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
#testinggggg
character_selection()

# Character selection
player_image = pygame.image.load("p1.png") #note to myself: using p1 for now so player_image is defined while I change things
player_size = player_image.get_width()

# player props
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 4
player_direction = "right"  # Initial direction

# squirrel props
squirrel_x = random.randint(0, screen_width - player_size)
squirrel_y = random.randint(0, screen_height - player_size)
squirrel_speed = 1
squirrel_direction = "right"  # Initial direction

# tree and apple props
tree_positions = []
apple_positions = []
num_trees = 6
min_distance_between_trees = 100

# map boundaries
world_width = background_images[0].get_width() * 2
world_height = background_images[0].get_height() * 2

# set tree positions
for _ in range(num_trees):
    tree_placed = False
    attempts = 0
    while not tree_placed and attempts < 100:
        # make sure trees are placed in img 3
        tree_x = random.randint(screen_width, world_width - tree_size)
        tree_y = random.randint(screen_height, world_height - tree_size)
        too_close = any((abs(tree_x - tx) < min_distance_between_trees and abs(tree_y - ty) < min_distance_between_trees) for tx, ty in tree_positions)
        if not too_close:
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
                    tile_type = 0 #  image 0 for even rows and columns
                else:
                    tile_type = 3 #  image 3 for odd columns in even rows
            else:
                if column % 2 == 0:
                    tile_type = 1 # image 1 for even columns in odd rows
                else:
                    tile_type = 2 # image 2 for odd rows and columns

            # Calc the position to blit the background image
            bg_x = column * background_images[tile_type].get_width() - view_x
            bg_y = row * background_images[tile_type].get_height() - view_y
            screen.blit(background_images[tile_type], (bg_x, bg_y))

    # Draw trees
    for tree_pos in tree_positions:
        tree_screen_x = tree_pos[0] - view_x
        tree_screen_y = tree_pos[1] - view_y
        # Ensure trees are drawn within the visible screen area
        if 0 <= tree_screen_x < screen_width and 0 <= tree_screen_y < screen_height:
            screen.blit(tree_image, (tree_screen_x, tree_screen_y))


    # Move the squirrel towards the closest apple
    if apple_positions:
        # make closest apple the first apple in the list
        closest_apple = apple_positions[0]
        # calc the distance from the squirrel to the first apple
        closest_distance = abs(squirrel_x - closest_apple[0]) + abs(squirrel_y - closest_apple[1])
        # go through remaining apple positions
        for pos in apple_positions[1:]:
             # calc the distance from the squirrel to the current apple
            distance = abs(squirrel_x - pos[0]) + abs(squirrel_y - pos[1])
            # If this distance is less than the prev. closest distance --> update the closest distance and closest apple
            if distance < closest_distance:
                closest_distance = distance
                closest_apple = pos
        # Move the squirrel horizontally towards the closest apple (need to flip direction here)
        if squirrel_x < closest_apple[0]:
            squirrel_x += squirrel_speed
            squirrel_direction = "right"  # flip direction
        elif squirrel_x > closest_apple[0]:
            squirrel_x -= squirrel_speed
            squirrel_direction = "left"   # flip direction

        # Move the squirrel vertically towards the closest apple
        if squirrel_y < closest_apple[1]:
            squirrel_y += squirrel_speed
        elif squirrel_y > closest_apple[1]:
            squirrel_y -= squirrel_speed

    # Draw apples
    for apple_pos in apple_positions:
        apple_screen_x = apple_pos[0] - view_x
        apple_screen_y = apple_pos[1] - view_y
        if 0 <= apple_screen_x < screen_width and 0 <= apple_screen_y < screen_height:
            screen.blit(apple_image, (apple_screen_x, apple_screen_y))

    # Check for apple collection by player
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    new_apple_positions = []
    for apple_pos in apple_positions:
        apple_rect = pygame.Rect(apple_pos[0], apple_pos[1], apple_image.get_width(), apple_image.get_height())
        if player_rect.colliderect(apple_rect):
            score += 1
            tree_pos = random.choice(tree_positions)
            new_apple_x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
            new_apple_y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
            new_apple_positions.append((new_apple_x, new_apple_y))
        else:
            new_apple_positions.append(apple_pos)
    apple_positions = new_apple_positions

    # Check for apple collection by squirrel

    squirrel_rect = pygame.Rect(squirrel_x, squirrel_y, squirrel_image.get_width(), squirrel_image.get_height())
    new_apple_positions = []
    for apple_pos in apple_positions:
        apple_rect = pygame.Rect(apple_pos[0], apple_pos[1], apple_image.get_width(), apple_image.get_height())
        if squirrel_rect.colliderect(apple_rect):
            tree_pos = random.choice(tree_positions)
            new_apple_x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
            new_apple_y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
            new_apple_positions.append((new_apple_x, new_apple_y))
        else:
            new_apple_positions.append(apple_pos)
    apple_positions = new_apple_positions

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

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
