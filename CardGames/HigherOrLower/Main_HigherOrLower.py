# Higher or Lower - pygame version

# 1 - Import packages
from operator import eq
from tkinter import *
from pygame.locals import *
import pygwidgets
import sys
import pygame
from Class_HigherOrLowerGame import *

# 2 - Define constants
BLACK = (0,0,0)
GRAY = (200,200,200)
BACKGROUND_COLOR = (0,180,180)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
PANEL_HEIGHT = 60
USABLE_WINDOW_HEIGHT = WINDOW_HEIGHT - PANEL_HEIGHT
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sound(s), etc.
background = pygwidgets.Image(window=window, loc=(0,0), 
                              pathOrLoadedImage='CardGames/images/background.png')

newGameButton = pygwidgets.TextButton(window=window, loc=(20,530), text=('New Game'),
                                      width=100, height=45)

higherButton = pygwidgets.TextButton(window=window, loc=(280,520), text='Higher',
                                     width=120, height=55)

lowerButton = pygwidgets.TextButton(window=window, loc=(600,520), text = 'Lower',
                                    width=120, height=55)

equalButton = pygwidgets.TextButton(window=window, loc=(440,520), text='Equal',
                                    width=120, height=55)

quitButton = pygwidgets.TextButton(window=window, loc=(880,530), text='Quit',
                                   width=100, height=45)

# 5 - Initialize variables
oGame = Game(window)

# 6 - Loop forever
while True:
    # 7 - Check for and handle events
    for event in pygame.event.get():
        if ((event.type == QUIT) or
            ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or \
            (quitButton.handleEvent(event))):
            pygame.quit()
            sys.exit()

        if newGameButton.handleEvent(event):
            oGame.reset()
            lowerButton.enable()
            equalButton.enable()
            higherButton.enable()

        if higherButton.handleEvent(event):
            gameOver = oGame.hitHigherOrLower(HIGHER)
            if gameOver:
                higherButton.disable()
                equalButton.disable()
                lowerButton.disable()

        if equalButton.handleEvent(event):
            gameOver = oGame.hitHigherOrLower(EQUAL)
            if gameOver:
                higherButton.disable()
                equalButton.disable()
                lowerButton.disable()
        
        if lowerButton.handleEvent(event):
            gameOver = oGame.hitHigherOrLower(LOWER)
            if gameOver:
                higherButton.disable()
                equalButton.disable()
                lowerButton.disable()

    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    background.draw()

    # 10 - Draw all window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    newGameButton.draw()
    higherButton.draw()
    lowerButton.draw()
    equalButton.draw()
    quitButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND) # make pygame wait