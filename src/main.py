import pygame
import sys
from pygame.locals import *
from config import *
from cell import Cell
from renderer import draw_cell, draw_ui
from recorder import FrameRecorder
import numpy as np
from cell_data import CellData


def main():
    print("Введите 3 координаты a через запятую: ", end="")
    a = np.array(list(map(float, input().split(","))))
    print("Введите 3 координаты d через запятую: ", end="")
    d = np.array(list(map(float, input().split(","))))
    print("Введите тета1: ", end="")
    teta1 = float(input())
    print("Введите тета2: ", end="")
    teta2 = float(input())
    print("Введите гамма: ", end="")
    gamma = float(input())

    # a = np.array([0, 1, 0])
    # d = np.array([1.5, 1, 0])
    # teta1 = 1.
    # teta2 = 1.5
    # gamma = 1

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Automatic Cell Division")

    clock = pygame.time.Clock()
    cells = [Cell(INITIAL_POS[0], INITIAL_POS[1], CELL_RADIUS,
                  1, CellData(a, d, teta1, teta2, gamma))]
    recorder = FrameRecorder(enabled=RECORD_FRAMES,
                             output_dir=FRAME_OUTPUT_DIR)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Simulation logic
        new_cells = []
        for cell in cells:
            cell.update()
            if cell.should_divide(current_time):
                print()
                new_cells.extend(cell.divide())
        if new_cells:
            cells = new_cells

        # Drawing
        for cell in cells:
            draw_cell(screen, cell)
        draw_ui(screen, len(cells))

        # Recording
        recorder.capture_frame(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
