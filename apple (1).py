import random

class Apple:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    
    def generate_positions(tree_positions, tree_image, apple_image):
        positions = []
        for tree_pos in tree_positions:
            x = tree_pos[0] + random.randint(0, tree_image.get_width() - apple_image.get_width())
            y = tree_pos[1] + random.randint(0, tree_image.get_height() - apple_image.get_height())
            positions.append((x, y))
        return positions

    def draw(self, screen, view_x, view_y):
        screen.blit(self.image, (self.x - view_x, self.y - view_y))
