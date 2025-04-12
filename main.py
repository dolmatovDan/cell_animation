import pygame
import math
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Automatic Cell Division")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
BACKGROUND = (240, 240, 245)

# Cell parameters
cell_radius = 25
initial_pos = (WIDTH // 2, HEIGHT // 2)
base_speed = 2.5  # Increased base speed
split_angle = 90  # Angle between cell movement directions
max_generations = 4  # Maximum division generations
division_delay = 1000  # Time between divisions (ms)
spread_distance = 80  # Distance between parent and child cells


class Cell:
    def __init__(self, x: float, y: float, radius: int, generation: int = 1):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.moving = False
        self.generation = generation
        self.color = [BLUE, RED, GREEN][generation % 3]  # Cycling colors
        self.created_time = pygame.time.get_ticks()
        self.has_divided = False
        self.distance_moved = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x),
                           int(self.y)), self.radius - 3)

        # Display generation number
        font = pygame.font.SysFont(None, 20)
        gen_text = font.render(str(self.generation), True, (0, 0, 0))
        surface.blit(gen_text, (int(self.x) - 5, int(self.y) - 7))

    def update(self):
        if self.moving:
            self.x += self.dx
            self.y += self.dy
            self.distance_moved += math.sqrt(self.dx**2 + self.dy**2)

            # Stop when reached spread distance
            if self.distance_moved >= spread_distance:
                self.moving = False

    def should_divide(self, current_time: int) -> bool:
        return (not self.has_divided and
                self.generation < max_generations and
                current_time - self.created_time > division_delay and
                not self.moving)

    def divide(self) -> list:
        if self.has_divided or self.generation >= max_generations:
            return []

        angle_rad = math.radians(split_angle / 2)
        new_generation = self.generation + 1
        # Slightly reduce speed each generation
        speed = base_speed * (0.8 ** self.generation)

        # Calculate direction vectors
        dx1 = speed * math.cos(angle_rad)
        dy1 = -speed * math.sin(angle_rad)
        dx2 = speed * math.cos(angle_rad)
        dy2 = speed * math.sin(angle_rad)

        # Create new cells
        cell1 = Cell(self.x, self.y, self.radius, new_generation)
        cell1.dx = dx1
        cell1.dy = dy1
        cell1.moving = True

        cell2 = Cell(self.x, self.y, self.radius, new_generation)
        cell2.dx = dx2
        cell2.dy = dy2
        cell2.moving = True

        self.has_divided = True
        return [cell1, cell2]


def main():
    clock = pygame.time.Clock()
    cells = [Cell(initial_pos[0], initial_pos[1], cell_radius)]

    # UI elements
    font = pygame.font.SysFont(None, 24)
    info_text = font.render(
        f"Automatic Division - Max Generations: {max_generations}", True, (0, 0, 0))

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        screen.fill(BACKGROUND)

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Automatic division logic
        new_cells = []
        for cell in cells:
            cell.update()
            if cell.should_divide(current_time):
                new_cells.extend(cell.divide())
        # cells.extend(new_cells)
        if len(new_cells):
            cells = new_cells

        # Draw all cells
        for cell in cells:
            cell.draw(screen)

        # Display info
        screen.blit(info_text, (20, 20))
        count_text = font.render(f"Cells: {len(cells)}", True, (0, 0, 0))
        screen.blit(count_text, (20, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
