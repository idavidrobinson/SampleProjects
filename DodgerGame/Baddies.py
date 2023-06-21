# Badde and BaddieMgr classes

import pygame
import pygwidgets
import random
from Constants import *

# Baddie class
class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    # Load the image only once - class variable shared by all Baddies
    BADDIE_IMAGE = pygame.image.load(BADDIE_IMG)

    def __init__(self, window):
        self.window = window
        # Set oBaddie speed attribute 
        self.speed = random.randrange(Baddie.MIN_SPEED, Baddie.MAX_SPEED + 1)
        # Create the image object
        size = random.randrange(Baddie.MIN_SIZE, Baddie.MAX_SIZE + 1)
        self.x = random.randrange(0, WINDOW_WIDTH - size)
        self.y = 0 - size # start above the window
        self.image = pygwidgets.Image(window=self.window, loc=(self.x, self.y),
                                      pathOrLoadedImage=Baddie.BADDIE_IMAGE)

        # Scale the image to match oBaddie size dimensions
        percent = (size * 100) / Baddie.MAX_SIZE
        self.image.scale(percent=percent, scaleFromCenter=False)

    def update(self): # move the Baddie down the screen
        self.y = self.y + self.speed # moving down the window at self.speed pace
        self.image.setLoc((self.x, self.y))

        # Check to see if Baddie moved off screen
        if self.y > GAME_HEIGHT:
            return True # needs to be deleted
        else:
            return False # still moving in the window

    def draw(self):
        self.image.draw()

    # test to see if oBaddie collided with Player - will be called by BaddieMgr
    def collide(self, playerRect):
        collidedWithPlayer = self.image.overlaps(playerRect)
        return collidedWithPlayer

# BaddieMgr class
class BaddieMgr():
    ADD_NEW_BADDIE_RATE = 8 # how many frames until add a new Baddie

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self): # called when starting a new game
        self.baddiesList = []
        self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE

    def update(self):
        # Tell each Baddie to update itself - Will be called by BaddieMgr in each frame
        # Count how many Baddies have fallen off the bottom of the window
        nBaddiesRemoved = 0
        # Use copy of baddiesList to avoid bug with .remove() skipping next element in given list
        # maintains integrity of baddiesList through iterations
        baddiesListCopy = self.baddiesList.copy()
        for oBaddie in baddiesListCopy:
            deleteMe = oBaddie.update()
            # run check to see if Baddie is off screen - True if so and ready to be deleted
            # test written in Baddie class
            if deleteMe:
                # note that oBaddie is removed from baddiesList and not baddiesListCopy
                self.baddiesList.remove(oBaddie)
                # tally for scoring purposes
                nBaddiesRemoved = nBaddiesRemoved + 1
        
        # Check if it's time to add a new Baddie using frame-counting approach
        self.nFramesTilNextBaddie = self.nFramesTilNextBaddie - 1
        if self.nFramesTilNextBaddie == 0:
            oBaddie = Baddie(self.window)
            self.baddiesList.append(oBaddie)
            self.nFramesTilNextBaddie = BaddieMgr.ADD_NEW_BADDIE_RATE # same as reset() handling of variable

        # Return the count of Baddies that were removed
        return nBaddiesRemoved

    def draw(self):
        # call .draw() on each Baddie in baddiesList
        for oBaddie in self.baddiesList:
            oBaddie.draw()

    def hasPlayerHitBaddie(self, playerRect):
        # check through each Baddie, if Baddie collides with Player, send signal to end game
        for oBaddie in self.baddiesList:
            if oBaddie.collide(playerRect):
                return True
        return False