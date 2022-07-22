from graphics import *
import random
from math import *

# Do not change these following 4 variables
margin = 10  # height of the paddle from the ground
moveIncrement = 15  # paddle movement
ballRadius = 15
BOUNCE_WAIT = 1200

BALL_COUNT = 2  # If we change this, the number of ball changes!


class Timer:
    def __init__(self):
        self.value = 0


class Paddle:

    def __init__(self, color, width, height, coordx, win):
        self.color = color
        self.width = width
        self.height = height
        self.x = coordx
        self.shape = Rectangle(Point(self.x - int(self.width / 2), win.getHeight() - margin - self.height),
                               Point(self.x + int(self.width / 2), win.getHeight() - margin))
        self.shape.setFill(self.color)
        self.window = win
        self.shape.draw(self.window)

    def move_left(self):   # move paddle to the left by the amount of global variable moveIncrement
        # TODO: control that it does not exceed the window
        # Done
        if (self.x - int(self.width / 2)) >= 0:
            self.x -= moveIncrement
            self.shape.move(-moveIncrement, 0)
        else:
            self.x += 0
            self.shape.move(0, 0)

    def move_right(self):  # move paddle to the right by the amount of global variable moveIncrement
        # TODO: control that it does not exceed the window
        # Done
        if (self.x + int(self.width / 2)) <= 300:
            self.x += moveIncrement
            self.shape.move(moveIncrement, 0)
        else:
            self.x += 0
            self.shape.move(0, 0)


#   TODO


class Bubbles:

    def __init__(self, xcoor, ycoor, color, win):
        self.shape = Circle(Point(xcoor, ycoor), 30)
        self.color = color
        self.window = win
        self.xcoor = xcoor
        self.ycoor = ycoor
        self.shape.setFill(self.color)
        self.shape.draw(self.window)


class Ball:

    def __init__(self, coordx, coordy, color, radius, x_direction, speed, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.xMovement = 0  # Current x movement
        self.yMovement = 0  # Current y movement
        self.color = color
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)
        self.radius = radius
        self.timer = 0
        self.x_direction = x_direction   # Initial x direction. This variable will be 0 or 1. 1:right 0:left
        self.speed = speed
        self.life = True

    def is_moving(self):   
        # TODO: It returns true if ball is moving
        
        return False

    def bounce(self, gameTimer, minX, maxX, maxY):
        # Calculating x-axis ball movement and bouncing
        # minX: min x coord. of paddle
        # maxX: max x coord. of paddle
        # maxY: max y coord. at which the ball can be move. If it goes further, it falls to the ground.

        global BOUNCE_WAIT
        gameOver = False

        if gameTimer >= self.timer + BOUNCE_WAIT:
            self.timer = gameTimer
            # TODO:
            # You should control ball movements. 
            # If it hits left-right-up of the window, or paddle it will turn back. Else, it hits to ground, so set gameOver to True
            
            if self.yMovement == 1:
                self.y += self.speed
            elif self.yMovement == -1:
                self.y -= self.speed
            
            if self.xMovement == 1:
                self.x += self.speed
            elif self.xMovement == -1:
                self.x -= self.speed

            if self.y > 650:
                self.life = False
            else:
                self.life = True
                if 0 <= self.y:
                    if minX + 15 <= self.x <= maxX + 15 and maxY - 30 <= self.y < maxY - 15:
                        self.yMovement = -1
                        self.y -= self.speed
                        self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)
                    elif 0 <= self.x <= 300:
                        self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)
                    else:
                        if self.x >= 300:
                            self.xMovement = -1
                            self.x -= self.speed
                            self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)
                        elif self.x <= 0:
                            self.xMovement = 1
                            self.x += self.speed
                            self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)
                elif self.y <= 0:
                    self.yMovement = 1
                    self.y += self.speed
                    self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)

            return gameOver


def main():
    win = GraphWin("20290122 Pong Game", 300, 600)   # Replace your student id
    lives = 2
    win.setBackground("Black")
    myPaddle = Paddle("White", 100, 15, 150, win)

    BallList = list()
    ColorsList = ["Cyan", "Red", "Green", "Yellow"]
    for i in range(BALL_COUNT):
        rand_speed = random.randint(5, 10)   # random speed for ball
        # Note that the speed of the balls may vary depending on the hardware. If it is too fast or too slow, you can change the speed range for yourself while testing.
        # However, if you change these range, do not forget to reset these values to the initial limits before sending us.
        
        rand_direction = random.randint(0, 1)  # This variable will be 0 or 1 randomly.
        ball = Ball(myPaddle.x - int(myPaddle.width/2) + i*30, win.getHeight() - margin - myPaddle.height - ballRadius, ColorsList[i%4], ballRadius, rand_direction, rand_speed, win)
        BallList.append(ball)


    color_list = ["Purple", "Pink", "Blue"]
    Bubble = list()
    BubbleList = list()
    Bubble_x = list()
    Bubble_y = list()
    for k in range(3):
        for t in range(5):
            bubble = Bubbles(t * 60 + 30, k * 60 + 30, color_list[k], win)
            Bubble.append(bubble)
            BubbleList.append(bubble.shape)
            Bubble_x.append(bubble.xcoor)
            Bubble_y.append(bubble.ycoor)
    
    # TODO:
    # You must add all necessary codes for the game to run.

    livesCounter = Text(Point(win.getWidth() - int(win.getWidth() / 5), 250), f'Lives -- {lives}')
    livesCounter.setTextColor("Cyan")
    livesCounter.setSize(15)
    livesCounter.draw(win)
    gameTimer = Timer()

    def returner():
        for g in BallList:
            g.shape.undraw()
        for h in BubbleList:
            h.undraw()
        myPaddle.shape.undraw()


    gameOver = False
    for y in range(1):
        try:
            while not gameOver:
                any_list = []
                while lives > 0:
                    keyPress = win.checkKey()
                    if keyPress == 'a':
                        myPaddle.move_left()

                    if keyPress == 'd':
                        myPaddle.move_right()

                    if keyPress == 'l':  # balls will move faster
                        for item in BallList:
                            item.speed += 1

                    if keyPress == 'k':  # Balls will move slower. Note that in our case min speed is 2.
                        for item in BallList:
                            if item.speed > 2:
                                item.speed -= 1

                    if keyPress == 's':  # Initial movement of balls
                        for item in BallList:
                            if not item.is_moving():
                                if item.x_direction == 1:   # it means ball moves to right in x direction
                                    item.xMovement = 1
                                else:                   # it means ball moves to left in x direction
                                    item.xMovement = -1
                                item.yMovement = -1  # at initial ball moves up in y direction
                    gameTimer.value += 1
                    for item in BallList:
                        gameOver = item.bounce(gameTimer.value, (myPaddle.x-int(myPaddle.width/2)), (myPaddle.x+int(myPaddle.width/2)), win.getHeight() - margin - myPaddle.height)
                        if gameOver == True:
                            break
                    for item in BallList:
                        if item.life == False:
                            lives -= 1
                            livesCounter.setText("Lives -- " + str(lives))
                            BallList.remove(item)
                            returner()
                            any_list = []
                            BallList = []
                            for c in BubbleList:
                                c.draw(win)
                            myPaddle = Paddle("White", 100, 15, 150, win)
                            ColorsList = ["Cyan", "Red", "Green", "Yellow"]
                            for i in range(BALL_COUNT):
                                rand_speed = random.randint(5, 10)   # random speed for ball
                                # Note that the speed of the balls may vary depending on the hardware. If it is too fast or too slow, you can change the speed range for yourself while testing.
                                # However, if you change these range, do not forget to reset these values to the initial limits before sending us.

                                rand_direction = random.randint(0, 1)  # This variable will be 0 or 1 randomly.
                                ball = Ball(myPaddle.x - int(myPaddle.width/2) + i*30, win.getHeight() - margin - myPaddle.height - ballRadius, ColorsList[i%4], ballRadius, rand_direction, rand_speed, win)
                                BallList.append(ball)


                    for it in BallList:
                        for ti in range(len(BubbleList)):
                            if sqrt((it.x - Bubble_x[ti])**2 + (it.y - Bubble_y[ti])**2) <= 45:
                                BubbleList[ti].undraw()
                                if BubbleList[ti] not in any_list:
                                    any_list.append(BubbleList[ti])
                            if len(any_list) == 15:
                                for v in BallList:
                                    v.shape.undraw()
                                myPaddle.shape.undraw()
                                gamewon = Text(Point(150, 350), "GAME OVER\n\nYOU WIN!\n\nPress Any Key to Quit")
                                gamewon.setTextColor("red")
                                gamewon.setSize(15)
                                gamewon.draw(win)
                                if any(keyPress):
                                    win.close()
                                    break

                else:
                    returner()
                    gameovertext = Text(Point(150, 350), "GAME OVER\n\nYOU LOST!\n\nPress Any Key to Quit")
                    gameovertext.setTextColor("red")
                    gameovertext.setSize(15)
                    gameovertext.draw(win)
                    gov = win.getKey()
                    if any(gov):
                        win.close()
                        break

        except:
            win.close()
            break


main()
