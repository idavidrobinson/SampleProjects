import pygame
from pygame.locals import *
import random

# Ball class
class Ball():

    def __init__(self, window, windowWidth, windowHeight):
        self.window = window # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.image = pygame.image.load('OOPPygame/images/ball.png')
        self.bounceSound = pygame.mixer.Sound('OOPPygame/sounds/boing.wav')
        # A rect is made up of [x, y, width, height]
        ballRect = self.image.get_rect()
        self.width = ballRect.width
        self.height = ballRect.height
        self.maxWidth = windowWidth - self.width
        self.maxHeight = windowHeight - self.height

        # Pick a random starting position
        self.x = random.randrange(start=0, stop=self.maxWidth)
        self.y = random.randrange(0, self.maxHeight)

        # Choose a random speed between -4 and 4, but not zero, in both x and y directions
        speedsList = [-4, -3, -2, -1, 1, 2, 3, 4]
        self.xSpeed = random.choice(speedsList)
        self.ySpeed = random.choice(speedsList)

    def update(self):
        # Will call update() method in each frame of main loop, so place code here that checks ball boundaries
        # Check for hitting a wall. If so, change that direction.
        if (self.x < 0) or (self.x >= self.maxWidth):
            self.xSpeed = -self.xSpeed
            self.bounceSound.play()

        if (self.y < 0) or (self.y >= self.maxHeight):
            self.ySpeed = -self.ySpeed
            self.bounceSound.play()
            
        # Update the Ball's x and y, using the speed in two directions
        self.x = self.x + self.xSpeed
        self.y = self.y + self.ySpeed

    def draw(self):
        self.window.blit(self.image, (self.x, self.y)) # draw ball at x- y-coords