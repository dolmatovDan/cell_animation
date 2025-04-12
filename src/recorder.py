import pygame
import os


class FrameRecorder:
    def __init__(self, enabled=False, output_dir="frames"):
        self.enabled = enabled
        self.frame_count = 0
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def capture_frame(self, surface):
        if self.enabled:
            pygame.image.save(
                surface, f"{self.output_dir}/frame_{self.frame_count:04d}.png")
            self.frame_count += 1
