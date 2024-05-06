import pickle
import pygame
from SnakeAI import *
import neat
import os

gen = 0

bkColor = (21, 21, 21)

# screen = pygame.display.set_mode((1200, 800))
# pygame.display.set_caption('Snake game')

# screen.fill(bkColor)
# pygame.display.flip()

PlayerSnake = Snake(15, 7)
i = 0
move = True


# def draw_window(win, snakes):
#     win.fill((21, 21, 21))
#     pygame.draw.rect(win, (255, 255, 255), (420, 45, 722, 684), 1)  # Board
#
#     # drawBoard(window)
#     for snake in snakes:
#         snake.drawSnake(win)
#     # snake.drawApple(screen)
#
#     pygame.display.update()


def eval_genomes(genomes, config):
    # global gen, screen
    # win = screen
    # gen += 1

    nets = []
    snakes = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(Snake(17, 17))
        ge.append(genome)

    TrainingRun = True
    clock = pygame.time.Clock()

    while TrainingRun and len(snakes) > 0:

        for x, snake in enumerate(snakes):
            Sensors = snake.VISION2()
            DiagonalsSensors = snake.diagonal()
            combined = Sensors + DiagonalsSensors
            output = nets[snakes.index(snake)].activate((combined))
            snake.interpretSnake(output)

            snake.move()
            a = snake.headPos()
            ge[snakes.index(snake)].fitness += 0.01
            if ge[snakes.index(snake)].fitness % 100 != 99:
                ge[snakes.index(snake)].fitness += 1

            if snake.EateApple(a[0], a[1]):
                ge[snakes.index(snake)].fitness += 100 * ((snake.lifeLeft - 10 - snake.senceAte) / (snake.lifeLeft - 10))

            if snake.checkCollisionBody(a[0], a[1]):
                ge[snakes.index(snake)].fitness -= 15
                nets.pop(snakes.index(snake))
                ge.pop(snakes.index(snake))
                snakes.pop(snakes.index(snake))

            elif snake.checkCollisionWall(a[0], a[1]) or snake.senceAte > snake.lifeLeft:
                ge[snakes.index(snake)].fitness -= 10
                nets.pop(snakes.index(snake))
                ge.pop(snakes.index(snake))
                snakes.pop(snakes.index(snake))

        # draw_window(win, snakes)


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 2000)
    with open("bestLOL.pickle", "wb") as f:
        pickle.dump(winner, f)

    print('\nBest genome:\n{!s}'.format(winner))
