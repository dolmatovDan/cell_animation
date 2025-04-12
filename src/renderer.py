import pygame
from config import *


def draw_cell(surface, cell):
    pygame.draw.circle(surface, cell.color,
                       (int(cell.x), int(cell.y)), cell.radius)
    pygame.draw.circle(surface, WHITE, (int(cell.x),
                       int(cell.y)), cell.radius - 3)

    font = pygame.font.SysFont(None, 20)
    gen_text = font.render(str(cell.generation), True, (0, 0, 0))
    surface.blit(gen_text, (int(cell.x) - 5, int(cell.y) - 7))


def draw_ui(surface, cell_count):
    font = pygame.font.SysFont(None, 24)
    info_text = font.render(
        f"Automatic Division - Max Generations: {MAX_GENERATIONS}", True, (0, 0, 0))
    count_text = font.render(f"Cells: {cell_count}", True, (0, 0, 0))

    surface.blit(info_text, (20, 20))
    surface.blit(count_text, (20, 50))
