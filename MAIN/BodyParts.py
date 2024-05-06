import pygame
dimX, dimY = 722, 68
Gap = dimX / 38


class bodyPart:

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = Gap
        self.height = Gap
        self.direction = direction

    def draw(self, window, color):
        pygame.draw.rect(window, color, (420 + self.x * Gap, 45 + self.y * Gap, self.width, self.height))
