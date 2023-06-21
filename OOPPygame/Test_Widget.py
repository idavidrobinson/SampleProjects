# test of pygwidgets

# 1 - Import packages
import pygame 
from pygame.locals import *
import pygwidgets
import sys

# 2 - Define constants
BLACK = (0,0,0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sound(s), etc.
'''
# Build a path to the file in the images folder
# pathToBall = BASE_PATH + 'images/ball.png'
'''

# 5 - Initialize variables
oImage = pygwidgets.Image(window, (100,200), 'OOPPygame/images/SomeImage.png')

# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Clicked the close button? Quit pygame and end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if oImage.handleEvent(event):
            # The user has done something to oImage that we should respond to
            # Add code here
            pass

    # 8 - Do any "per frame" actions

    # 9 - Clear the window
    window.fill(BLACK)

    # 10 - Draw all window elements
    oImage.draw() # draw method of Image class contains call to blit() to draw image
                  # to move image, call setLoc() method with new x- and y- coord tuple
                  # oImage.setLoc((newX, newY))

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)