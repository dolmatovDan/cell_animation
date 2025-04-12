import pygame
import math
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Division")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BACKGROUND = (240, 240, 245)

# Cell parameters
cell_radius = 30
initial_pos = (WIDTH // 2, HEIGHT // 2)
speed = 2
split_angle = 45  # Angle between cell movement directions


class Cell:
    def __init__(self, x, y, radius, dx=0, dy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx  # X velocity
        self.dy = dy  # Y velocity
        self.moving = False
        self.split_time = 0

    def draw(self, surface):
        pygame.draw.circle(
            surface, BLUE, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x),
                           int(self.y)), self.radius - 3)

    def update(self):
        if self.moving:
            self.x += self.dx
            self.y += self.dy


def main():
    clock = pygame.time.Clock()
    cells = [Cell(initial_pos[0], initial_pos[1], cell_radius)]
    splitting = False
    split_start_time = 0

    running = True
    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE and len(cells) == 1 and not splitting:
                    splitting = True
                    split_start_time = pygame.time.get_ticks()

        # When space is pressed and there's only one cell
        if splitting and len(cells) == 1:
            current_time = pygame.time.get_ticks()
            if current_time - split_start_time > 1000:  # Delay before division
                # Convert angle to radians
                angle_rad = math.radians(split_angle / 2)

                # First cell (moving right-up)
                dx1 = speed * math.cos(angle_rad)
                dy1 = -speed * math.sin(angle_rad)
                cell1 = Cell(cells[0].x, cells[0].y, cell_radius, dx1, dy1)
                cell1.moving = True

                # Second cell (moving right-down)
                dx2 = speed * math.cos(angle_rad)
                dy2 = speed * math.sin(angle_rad)
                cell2 = Cell(cells[0].x, cells[0].y, cell_radius, dx2, dy2)
                cell2.moving = True

                cells = [cell1, cell2]
                splitting = False
                split_start_time = pygame.time.get_ticks()

        # Stop cells after 1 second of movement
        if len(cells) == 2:
            current_time = pygame.time.get_ticks()
            if current_time - split_start_time > 1000:  # 1000 ms = 1 second
                for cell in cells:
                    cell.moving = False

        # Update and draw all cells
        for cell in cells:
            cell.update()
            cell.draw(screen)

        # Instruction text
        font = pygame.font.SysFont(None, 24)
        if len(cells) == 1:
            text = font.render(
                "Press SPACE to divide cell", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - 150, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
