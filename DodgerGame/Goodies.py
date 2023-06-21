# Goodie and GoodieMgr classes
from telnetlib import GA
from tkinter.tix import WINDOW
import pygame
import pygwidgets
import random
from Constants import *

class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image once
    GOODIE_IMAGE = pygame.image.load(GOODIE_IMG)
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE + 1) # to include MAX_SIZE in randrange() calculation
        self.y = random.randrange(0, GAME_HEIGHT - size)

        # Useful bit of code for defining if Goodie appears from left or right
        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT: # start on right side of the window
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1) # to include MAX_SPEED in randrange() calc
            self.minLeft = - size
        else: # start on the left side of the window
            self.x = 0 - size
            self.speed = random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)

        # Create image and scale to proper size
        self.image = pygwidgets.Image(window=window, loc=(self.x, self.y), pathOrLoadedImage=Goodie.GOODIE_IMAGE)
        percent = int((size * 100) / Goodie.MAX_SIZE)
        self.image.scale(percent=percent, scaleFromCenter=False)

    def update(self): # Move the Goodie either left or right on the screen
        self.x = self.x + self.speed 
        self.image.setLoc((self.x, self.y))

        # Check to see if Goodie has moved off screen
        # Will be dependent on which way each Goodie is moving (left|right)
        # Left moving Goodie check
        if self.direction == Goodie.LEFT:
            if self.x < self.minLeft: # has the Goodie moved off screen?
                return True # needs to be deleted
            else:
                return False # continues to move within window

    def draw(self):
        self.image.draw()

    # test to see if oGoodie collided with Player - will be called by GoodieMgr
    def collide(self, playerRect):
        collidedWithPlayer = self.image.overlaps(playerRect)
        return collidedWithPlayer

class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 110

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self): # Called when starting a new game
        self.goodiesList = []
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI

    def update(self, thePlayerRect):
        # Tell each Goodie to update itself
        # If a Goodie goes off an edge, remove it
        # Count up all Goodies that contact the Player in each frame and remove them
        nGoodiesHit = 0
        # Use copy of goodiesList to avoid bug with .remove() skipping next element in given list
        # maintains integrity of goodiesList through iterations
        goodiesListCopy = self.goodiesList.copy()
        for oGoodie in goodiesListCopy:
            deleteMe = oGoodie.update()
            # run check to see if Goodie is off screen - True if so and ready to be deleted
            # test written in Goodie class
            if deleteMe:
                # note that oGoodie is removed from goodiesList and not goodiesListCopy
                self.goodiesList.remove(oGoodie) # remove this Goodie

            # run check to see if Goodie collided with Player
            # test written in Goodie class
            elif oGoodie.collide(thePlayerRect):
                self.goodiesList.remove(oGoodie) # remove this Goodie
                
                # tally additional Goodies hit by Player object to be used for scoring
                nGoodiesHit = nGoodiesHit + 1

        # Test to see if Goodie needs to be added
        self.nFramesTilNextGoodie = self.nFramesTilNextGoodie - 1
        if self.nFramesTilNextGoodie == 0:
            oGoodie = Goodie(self.window)
            self.goodiesList.append(oGoodie)
            # reset frames until new Goodie to appear
            self.nFramesTilNextGoodie = random.randrange(GoodieMgr.GOODIE_RATE_LO, GoodieMgr.GOODIE_RATE_HI + 1)

        return nGoodiesHit # return number of Goodies that contacted player

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()