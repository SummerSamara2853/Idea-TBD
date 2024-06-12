import pygame
import random
import sys
from player import Player
from squirrel import Squirrel
from tree import Tree
from apple import Apple
from house import House
from grandma import Grandma

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Granny Smith")

background_images = []
for i in range(4):
    image = pygame.image.load(f"background_{i}.png")
    image = pygame.transform.scale(image, (screen_width, screen_height))
    background_images.append(image)

p1_image = pygame.image.load("p1.png")
p1_image = pygame.transform.scale(p1_image, (80, 80))

p2_image = pygame.image.load("p2.png")
p2_image = pygame.transform.scale(p2_image, (60, 80))

p3_image = pygame.image.load("p3.png")
p3_image = pygame.transform.scale(p3_image, (60, 80))

squirrel_image = pygame.image.load("squirrel.png")
squirrel_image = pygame.transform.scale(squirrel_image, (70, 70))

apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (40, 40))

tree_image = pygame.image.load("tree.png")
tree_image = pygame.transform.scale(tree_image, (130, 130))
tree_size = tree_image.get_width()

house_image = pygame.image.load("house.png")
house_image = pygame.transform.scale(house_image, (195, 195))

grandma_image = pygame.image.load("grandma.png")
grandma_image = pygame.transform.scale(grandma_image, (50, 50))

def character_selection():
    selected_character = None
    while not selected_character:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Select your character", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))

        screen.blit(p1_image, (screen_width // 2 - 200, 300))
        screen.blit(p2_image, (screen_width // 2 - 40, 300))
        screen.blit(p3_image, (screen_width // 2 + 120, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_width // 2 - 200 <= mouse_x <= screen_width // 2 - 120 and 300 <= mouse_y <= 380:
                    selected_character = p1_image
                elif screen_width // 2 - 40 <= mouse_x <= screen_width // 2 + 40 and 300 <= mouse_y <= 380:
                    selected_character = p2_image
                elif screen_width // 2 + 120 <= mouse_x <= screen_width // 2 + 200 and 300 <= mouse_y <= 380:
                    selected_character = p3_image

    return selected_character

player_image = character_selection()
player_size = player_image.get_width()

player = Player(player_image, screen_width // 2 - player_size // 2, screen_height // 2 - player_size // 2, 4)
squirrel = Squirrel(squirrel_image, random.randint(0, screen_width - player_size), random.randint(0, screen_height - player_size), 1)

world_width = background_images[0].get_width() * 2
world_height = background_images[0].get_height() * 2

tree_positions = Tree.generate_positions(6, 100, screen_width, screen_height, world_width, world_height, tree_size)
trees = [Tree(tree_image, x, y) for x, y in tree_positions]

apple_positions = Apple.generate_positions(tree_positions, tree_image, apple_image)
apples = [Apple(apple_image, x, y) for x, y in apple_positions]

house_positions = [(1430, 85), (1430, 225), (1430, 365)]
houses = [House(house_image, x, y) for x, y in house_positions]

grandmas = [Grandma(grandma_image, x - 30, y + 70, random.randint(1, 5)) for x, y in house_positions]

running = True
score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            to_remove = []
            for grandma in grandmas:
                if grandma.check_request_fulfilled(player.rect, score):
                    score -= grandma.request
                    to_remove.append(grandma)
            grandmas = [g for g in grandmas if g not in to_remove]

    keys = pygame.key.get_pressed()
    player.move(keys, world_width, world_height)
    squirrel.move_towards_apple(apple_positions)

    view_x = max(0, min(world_width - screen_width, player.x - screen_width // 2))
    view_y = max(0, min(world_height - screen_height, player.y - screen_height // 2))

    for row in range(0, 2):
        for column in range(0, 2):
            if row % 2 == 0:
                tile_type = 0 if column % 2 == 0 else 3
            else:
                tile_type = 1 if column % 2 == 0 else 2

            bg_x = column * background_images[tile_type].get_width() - view_x
            bg_y = row * background_images[tile_type].get_height() - view_y
            screen.blit(background_images[tile_type], (bg_x, bg_y))

    for tree in trees:
        tree.draw(screen, view_x, view_y)

    for apple in apples:
        apple.draw(screen, view_x, view_y)

    for house in houses:
        house.draw(screen, view_x, view_y)

    for grandma in grandmas:
        grandma.draw(screen, view_x, view_y)

    player.rect = pygame.Rect(player.x, player.y, player.size, player.size)
    new_apple_positions = []
    for apple in apples:
        apple_rect = pygame.Rect(apple.x, apple.y, apple.image.get_width(), apple.image.get_height())
        if player.rect.colliderect(apple_rect):
            score += 1
            tree_pos = random.choice(tree_positions)
            new_apple_x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
            new_apple_y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
            new_apple_positions.append((new_apple_x, new_apple_y))
        else:
            new_apple_positions.append((apple.x, apple.y))
    apple_positions = new_apple_positions
    apples = [Apple(apple_image, x, y) for x, y in apple_positions]

    squirrel.rect = pygame.Rect(squirrel.x, squirrel.y, squirrel.image.get_width(), squirrel.image.get_height())
    new_apple_positions = []
    for apple in apples:
        apple_rect = pygame.Rect(apple.x, apple.y, apple.image.get_width(), apple.image.get_height())
        if squirrel.rect.colliderect(apple_rect):
            tree_pos = random.choice(tree_positions)
            new_apple_x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
            new_apple_y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
            new_apple_positions.append((new_apple_x, new_apple_y))
        else:
            new_apple_positions.append((apple.x, apple.y))
    apple_positions = new_apple_positions
    apples = [Apple(apple_image, x, y) for x, y in apple_positions]

    player.draw(screen, view_x, view_y)
    squirrel.draw(screen, view_x, view_y)

    score_text = font.render(f"Apples: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    if not grandmas:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("You got enough apples!", True, (255, 255, 255))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(50000)
        running = False

pygame.quit()
sys.exit()
