import pygame
pygame.init()

Button_Background = (1, 166, 111)
font = pygame.font.Font('freesansbold.ttf', 32)

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)




class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = 'Move'

    def draw(self, window):

        tekstdemo = pygame.font.Font('freesansbold.ttf', 40)
        text = tekstdemo.render(self.text, True, (0, 0, 0), Button_Background)
        textRect = text.get_rect()
        textRect.center = (self.x + 90, self.y + 42)


        pygame.draw.rect(window, Button_Background, pygame.Rect(self.x , self.y, self.width, self.height), 0 , 10)
        window.blit(text, textRect)









