import pygame
import random

SizeX = 38
SizeY = SizeX - 3

dimX, dimY = 722, 684
SIZE = 38
Gap = dimX / SIZE


class Apple:

    def __init__(self):
        self.x = 0
        self.y = 0

    def createApple(self, snake):
        self.genAxis()
        x = [(part.x, part.y) for part in snake.body]

        if (self.x, self.y) in x:
            self.createApple(snake)

    def genAxis(self):
        self.x = random.randrange(0, SizeX)
        self.y = random.randrange(0, SizeY + 1)

    def drawApple(self, window):
        pygame.draw.rect(window, (220, 20, 60), (420 + self.x * Gap, 45 + self.y * Gap, Gap, Gap))

    def get_apple_x(self):
        return self.x

    def get_apple_y(self):
        return self.y
