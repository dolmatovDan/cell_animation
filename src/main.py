import pygame
import sys
from pygame.locals import *
from config import *
from cell import Cell
from renderer import draw_cell, draw_ui
from recorder import FrameRecorder


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Automatic Cell Division")

    clock = pygame.time.Clock()
    cells = [Cell(INITIAL_POS[0], INITIAL_POS[1], CELL_RADIUS)]
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
