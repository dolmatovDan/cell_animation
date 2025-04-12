import pygame
import math
from config import *


class Cell:
    def __init__(self, x: float, y: float, radius: int, generation: int = 1):
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

        angle_rad = math.radians(SPLIT_ANGLE / 2)
        new_generation = self.generation + 1
        speed = BASE_SPEED * (0.8 ** self.generation)

        dx1 = speed * math.cos(angle_rad)
        dy1 = -speed * math.sin(angle_rad)
        dx2 = speed * math.cos(angle_rad)
        dy2 = speed * math.sin(angle_rad)

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
