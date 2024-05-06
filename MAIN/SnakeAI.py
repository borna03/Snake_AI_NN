import pygame
from BodyParts import bodyPart
from Food import Apple

dimX, dimY = 722, 684
SIZE = 38
Gap = dimX / SIZE
SIZEE = 19
NumRows = int(dimX / Gap)
NumCols = int(dimY / Gap)
StartingParts = 1

WIDTH = 722
HEIGHT = 684
SNAKESIZE = 19


def drawBoard(window):
    for i in range(NumRows):
        for j in range(NumCols):
            pygame.draw.rect(window, (100, 100, 100), (420 + (i * Gap), 45 + (j * Gap), Gap, Gap), 1)


def moveUp(part):
    part.y -= 1


def moveDown(part):
    part.y += 1


def moveLeft(part):
    part.x -= 1


def moveRight(part):
    part.x += 1


class Snake:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = [bodyPart(self.x - i, self.y, 1) for i in range(StartingParts)]

        self.lifeTime = 0
        self.lifeLeft = 300
        self.senceAte = 0

        self.apple = Apple()
        self.apple.createApple(self)

        self.score = 0  # Initialize score here

    def headPos(self):
        return (self.body[0].x, self.body[0].y)

    def drawSnake(self, window):
        self.apple.drawApple(window)
        for part in self.body:
            if self.body.index(part) == 0:
                color = (34, 139, 34)
            else:
                color = (44, 239, 16)
            part.draw(window, color)

    def move(self):
        for part in self.body:
            if part.direction == 0:
                moveUp(part)
            if part.direction == 1:
                moveRight(part)
            if part.direction == 2:
                moveDown(part)
            if part.direction == 3:
                moveLeft(part)

        self.changeDirections()
        self.lifeTime += 1

        self.senceAte += 1

    def changeDirections(self):
        for i in range(len(self.body)):
            if i != len(self.body) - 1:
                self.body[i * -1 - 1].direction = self.body[i * -1 - 2].direction

    def EateApple(self, x, y):
        if self.apple.x == x and self.apple.y == y:
            tempRow = self.body[-1].x
            tempCol = self.body[-1].y
            tempDirection = self.body[-1].direction

            if tempDirection == 0:
                tempCol += 1
            if tempDirection == 1:
                tempRow -= 1
            if tempDirection == 2:
                tempCol -= 1
            if tempDirection == 3:
                tempRow += 1

            self.body.append(bodyPart(tempRow, tempCol, tempDirection))

            self.apple.createApple(self)
            self.senceAte = 0

            self.score += 1  # Increase score by 10 for each apple eaten
            print(self.score)

            return True
        return False

    def sensors(self):
        a = self.headPos()
        wallColide = False
        temparr = [38 - a[0] - 1, a[0], 35 - a[1], a[1]]
        # 0 = Right , 1 = Left , 2 = Dole , 3 = Gore
        BodyRight = False
        BodyLeft = False
        BodyForward = False
        Bodybackwards = False
        i = 1
        while not wallColide:
            if BodyRight == True and BodyLeft == True and BodyForward == True and Bodybackwards == True:
                wallColide = True
            else:
                if a[0] + i >= 36:
                    BodyRight = True
                if self.checkCollisionBody(a[0] + i, a[1]) and not BodyRight:
                    temparr[0] = i - 1
                    BodyRight = True
                if a[0] - i <= -1:
                    BodyLeft = True
                if self.checkCollisionBody(a[0] - i, a[1]) and not BodyLeft:
                    temparr[1] = i - 1
                    BodyLeft = True

                if a[1] + i >= 36:
                    BodyForward = True
                if self.checkCollisionBody(a[0], a[1] + i) and not BodyForward:
                    temparr[2] = i - 1
                    BodyForward = True

                if a[1] - i <= -1:
                    Bodybackwards = True
                if self.checkCollisionBody(a[0], a[1] - i) and not Bodybackwards:
                    temparr[3] = i - 1
                    Bodybackwards = True
                i += 1

        return temparr

    def diagonal(self):
        DiagWall = False
        DiagApple = False
        DiagBody = False
        Wall = [99, 99, 99, 99]  # Wall 1 , Wall 4 , Wall 2 , Wall 3
        distance = 1
        x, y = self.body[0].x, self.body[0].y

        Body = [99, 99, 99, 99]  # Body 1 , Body 4 , Body 2 , Body 3

        first = SIZE - x - 1
        second = x

        if first > 0:
            for i in range(first + 1):
                if self.checkCollisionWall(x + i + 1, y - i - 1) and Wall[0] == 99:
                    Wall[0] = i

                if self.checkCollisionWall(x + i + 1, y + i + 1) and Wall[1] == 99:
                    Wall[1] = i

                if self.checkCollisionBody(x + i + 1, y - i - 1) and Body[0] == 99:
                    Body[0] = i

                if self.checkCollisionBody(x + i + 1, y + i + 1) and Body[1] == 99:
                    Body[1] = i

        if second > 0:
            for i in range(second + 1):
                if self.checkCollisionWall(x - i - 1, y - i - 1) and Wall[2] == 99:
                    Wall[2] = i

                if self.checkCollisionWall(x - i - 1, y + i + 1) and Wall[3] == 99:
                    Wall[3] = i

                if self.checkCollisionBody(x - i - 1, y - i - 1) and Body[2] == 99:
                    Body[2] = i

                if self.checkCollisionBody(x - i - 1, y + i + 1) and Body[3] == 99:
                    Body[3] = i

        a = [0 if item == 99 else item * Gap for item in Wall]
        b = [Body[i] * Gap if Body[i] != 99 else a[i] for i in range(4)]

        arr = a + b

        return arr

    def checkApple(self, x, y):
        if self.apple.x == x and self.apple.y == y:
            return True
        return False

    def checkCollisionBody(self, x, y):
        for part in self.body:
            if x == part.x and y == part.y and self.body.index(part) != 0:
                return True
        return False

    def checkCollisionWall(self, x, y):
        if x <= -1 or x > SIZE - 1:
            return True
        if y <= -1 or y > SIZE - 3:
            return True
        return False

    def VISION2(self):
        direction = self.body[0].direction
        x = self.body[0].x * Gap
        y = self.body[0].y * Gap

        a = self.sensors()  # 0 = Right , 1 = Left , 2 = Dole , 3 = Gore

        appleX = self.apple.x * 19
        appleY = self.apple.y * 19

        a = [item * Gap for item in a]

        if direction == 1:

            dist_straight_wall = WIDTH - x - SNAKESIZE
            dist_right_wall = HEIGHT - y - SNAKESIZE
            dist_left_wall = y

            dist_left_fruit = y - appleY - SNAKESIZE
            dist_right_fruit = appleY - y - SNAKESIZE
            dist_straight_fruit = appleX - x - SNAKESIZE
            info = [dist_straight_wall, dist_straight_fruit, dist_right_wall, dist_right_fruit, dist_left_wall, dist_left_fruit, a[0], a[2], a[3]]



        elif direction == 3:
            dist_straight_wall = x
            dist_right_wall = y
            dist_left_wall = HEIGHT - y - SNAKESIZE

            dist_left_fruit = appleY - y - SNAKESIZE
            dist_right_fruit = y - appleY - SNAKESIZE
            dist_straight_fruit = x - appleX - SNAKESIZE
            info = [dist_straight_wall, dist_straight_fruit, dist_right_wall, dist_right_fruit, dist_left_wall, dist_left_fruit, a[1], a[3], a[2]]



        elif direction == 0:

            dist_straight_wall = y
            dist_right_wall = WIDTH - x - SNAKESIZE
            dist_left_wall = x

            dist_left_fruit = x - appleX - SNAKESIZE
            dist_right_fruit = x - appleX - x - SNAKESIZE
            dist_straight_fruit = y - appleY - SNAKESIZE
            info = [dist_straight_wall, dist_straight_fruit, dist_right_wall, dist_right_fruit, dist_left_wall, dist_left_fruit, a[3], a[0], a[1]]


        elif direction == 2:
            dist_straight_wall = HEIGHT - y - SNAKESIZE
            dist_right_wall = x
            dist_left_wall = WIDTH - x - SNAKESIZE

            dist_left_fruit = appleX - x - SNAKESIZE
            dist_right_fruit = x - appleX - SNAKESIZE
            dist_straight_fruit = appleY - y - SNAKESIZE
            info = [dist_straight_wall, dist_straight_fruit, dist_right_wall, dist_right_fruit, dist_left_wall, dist_left_fruit, a[2], a[1], a[0]]

        return info

    def interpretSnake(self, output):

        index = output.index(max(output))
        direction = self.body[0].direction
        decidion = ''

        if index == 0:
            decidion = "straight"
        elif index == 1:
            decidion = "right"
        elif index == 2:
            decidion = "left"

        if direction == 2:
            if decidion == "right":
                self.body[0].direction = 3
            elif decidion == "left":
                self.body[0].direction = 1


        elif direction == 0:
            if decidion == "right":
                self.body[0].direction = 1
            elif decidion == "left":
                self.body[0].direction = 3

        elif direction == 3:
            if decidion == "right":
                self.body[0].direction = 0
            elif decidion == "left":
                self.body[0].direction = 2

        elif direction == 1:
            if decidion == "right":
                self.body[0].direction = 2
            elif decidion == "left":
                self.body[0].direction = 0
