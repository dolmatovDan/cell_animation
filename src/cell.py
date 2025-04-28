import pygame
import math
from config import *
from cell_data import CellData


class Cell:
    def __init__(self, x: float, y: float, radius: int, generation: int, cell_data: CellData):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.moving = False
        self.generation = generation
        self.color = [BLUE, RED, GREEN][generation % 3]
        self.created_time = pygame.time.get_ticks()
        self.has_divided = False
        self.distance_moved = 0

        self.cell_data = cell_data

    def update(self):
        if self.moving:
            self.x += self.dx
            self.y += self.dy
            self.distance_moved += math.sqrt(self.dx**2 + self.dy**2)
            if self.distance_moved >= SPREAD_DISTANCE:
                self.moving = False

    def should_divide(self, current_time: int) -> bool:
        return (not self.has_divided and
                self.generation < MAX_GENERATIONS and
                current_time - self.created_time > DIVISION_DELAY and
                not self.moving)

    def divide(self) -> list:
        if self.has_divided or self.generation >= MAX_GENERATIONS:
            return []
        new_generation = self.generation + 1
        speed = BASE_SPEED * (0.8 ** self.generation)

        cd1, cd2 = self.cell_data.get_childs()

        cell1 = Cell(self.x, self.y, self.radius, new_generation, cd1)
        cell1.dx, cell1.dy = cell1.cell_data.calc_dxy()
        cell1.moving = True
        cell1.dx *= speed
        cell1.dy *= speed

        cell2 = Cell(self.x, self.y, self.radius, new_generation, cd2)
        cell2.dx, cell2.dy = cell2.cell_data.calc_dxy()
        cell2.moving = True
        cell2.dx *= speed
        cell2.dy *= speed

        self.has_divided = True
        return [cell1, cell2]
