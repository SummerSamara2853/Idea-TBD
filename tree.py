import random

class Tree:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.size = image.get_width()

    def generate_positions(num_trees, min_distance, screen_width, screen_height, world_width, world_height, tree_size):
        positions = []
        for tree in range(num_trees):
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                x = random.randint(screen_width, world_width - tree_size)
                y = random.randint(screen_height, world_height - tree_size)
                too_close = any((abs(x - tx) < min_distance and abs(y - ty) < min_distance) for tx, ty in positions)
                if not too_close:
                    positions.append((x, y))
                    placed = True
                attempts += 1
        return positions

    def draw(self, screen, view_x, view_y):
        screen.blit(self.image, (self.x - view_x, self.y - view_y))
