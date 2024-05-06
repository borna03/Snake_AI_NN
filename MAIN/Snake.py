import pygame
from GUIButton import Button
from MAIN import TrainEnvironment
from SnakeAI import *
from TrainEnvironment import *
import neat
import os

bkColor = (21, 21, 21)

StartButton = Button(30, 50, 187, 85)
AIButton = Button(30, 175, 187, 85)
AIButton.text = ' AI '
PlayerButton = Button(30, 300, 187, 85)
PlayerButton.text = 'Player'

i = 0
move = True

TrainAI = False
Player = False
AI = False

if not TrainAI:
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('Snake game')
    screen.fill(bkColor)
    pygame.display.flip()


def draw(window, snake):
    window.fill((21, 21, 21))
    pygame.draw.rect(window, (255, 255, 255), (420, 45, 722, 684), 1)
    StartButton.draw(window)
    AIButton.draw(window)
    PlayerButton.draw(window)
    snake.drawSnake(window)
    drawScore(window, snake.score)  # Draw the score
    pygame.display.update()


def drawScore(window, score):
    font = pygame.font.SysFont('Arial', 24)  # Creates a Font object
    scoreSurface = font.render('Score: {}'.format(score), True, (255, 255, 255))
    window.blit(scoreSurface, (50, 10))  # Adjust position as needed

def drawShit(window):
    StartButton.draw(window)
    AIButton.draw(window)
    PlayerButton.draw(window)

    pygame.display.update()


def Screeen(winner):
    global screen, Player, AI

    WINNER = Snake(2, 2)
    gameRun = True
    AIScore = 0

    moveFrames = 0
    clock = pygame.time.Clock()
    PlayerSnake = Snake(15, 7)
    move = True

    AImove = False
    PMove = False
    a = 0

    while gameRun:
        mouse = pygame.mouse.get_pos()

        if not Player and not AI and not TrainAI:
            drawShit(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if StartButton.x <= mouse[0] <= StartButton.x + StartButton.width and StartButton.y <= mouse[1] <= StartButton.y + StartButton.height:
                    if a == 0:
                        StartButton.text = 'Move'
                        AImove = True
                        PMove = True
                        a = 1
                    else:
                        StartButton.text = 'Stop'
                        AImove = False
                        PMove = False
                        a = 0

                if AIButton.x <= mouse[0] <= AIButton.x + AIButton.width and AIButton.y <= mouse[1] <= AIButton.y + AIButton.height:
                    AI = True

                if PlayerButton.x <= mouse[0] <= PlayerButton.x + PlayerButton.width and PlayerButton.y <= mouse[1] <= PlayerButton.y + PlayerButton.height:
                    Player = True

            if Player:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        PlayerSnake.body[0].direction = 0
                    if event.key == pygame.K_d:
                        PlayerSnake.body[0].direction = 1
                    if event.key == pygame.K_s:
                        PlayerSnake.body[0].direction = 2
                    if event.key == pygame.K_a:
                        PlayerSnake.body[0].direction = 3
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if Player:
            if PMove:
                moveFrames += 0.5
                if moveFrames % 15 == 0:
                    if move:
                        PlayerSnake.move()
                if PlayerSnake.checkCollisionBody(PlayerSnake.headPos()[0], PlayerSnake.headPos()[1]) or PlayerSnake.checkCollisionWall(PlayerSnake.headPos()[0], PlayerSnake.headPos()[1]):
                    move = False

                PlayerSnake.VISION2()
                HeadPosition = PlayerSnake.headPos()
                PlayerSnake.EateApple(HeadPosition[0], HeadPosition[1])

            draw(screen, PlayerSnake)

        elif AI:
            if AImove:
                clock.tick(60)

                arr = WINNER.VISION2()
                output = winner.activate(arr)
                WINNER.interpretSnake(output)

                WINNER.move()
                a = WINNER.headPos()
                if WINNER.EateApple(a[0], a[1]):
                    AIScore += 1

                if WINNER.checkCollisionWall(a[0], a[1]) or WINNER.checkCollisionBody(a[0], a[1]):
                    del WINNER
                    AI = False

            draw(screen, WINNER)

        elif TrainAI:
            TrainEnvironment.run(config_path)


def test_best_network(config_file, genome_path="best.pickle"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    winner_net = neat.nn.FeedForwardNetwork.create(genome, config)
    return winner_net


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    winnerNet = test_best_network(config_path)
    if TrainAI:
        TrainEnvironment.run(config_path)
    Screeen(winnerNet)
