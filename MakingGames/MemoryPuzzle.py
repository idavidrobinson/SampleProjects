# Memory Puzzle
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import sys
import random
import pygame
from pygame.locals import *
from CommonRGB import *

# Define constants
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDWIDTH) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
GAMEWONWAIT = 2000 # milliseconds before resetting game after player wins
REVEALBOARDWAIT = 1000
COVERBOXESWAIT = 1000
HIGHLIGHTOFFSET = -5
HIGHLIGHTBOXWIDTH = 10
HIGHLIGHTBOXHEIGHT = 10
HIGHLIGHTLINEWIDTH = 4
GROUPSIZE = 8
GAMEWONFILLFRAMES = 13
GAMEWONWAIT = 300

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

# easier to debug with CONSTANT than 'string'
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, 'Board is too big for the number of shapes/colors defined.'
# if False either need more colors and shapes or board width|height smaller


def main():
    # Use global for constants that need pygame.init() function called first
    global FPSCLOCK, DISPLAYSURF # any values assigned to these will persist outside main() - used in other functions in program
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(BGCOLOR) # paints over anything that used to be on the surface
    pygame.display.set_caption('Memory Game')

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    
    # create board
    mainBoard = getRandomizedBoard() # returns data (list of list) representing state of board
    # make sure all boxes are hidden
    revealedBoxes = generateRevealedBoxesData(False) # returns data (list of list) representing which boxes are covered

    # program has to know if each selection is first or second given game mechanism, so create variable
    firstSelection = None # stores the (x,y) of the first box clicked.

   

    # Give player sneak peek at icons under boxes randomly
    startGameAnimation(mainBoard)

    while True: # main game loop
        '''
        Game state stored in following variables each loop:
        * mainBoard - list of list (shape, color) tuples for each box - listed by column
        * revealedBoxes - list of list booleans for each box - listed by column
        * firstSelection - boolean
        * mouseClicked - boolean
        * mousex - x coord of mouse
        * mousey - y coord of mouse
        '''
        mouseClicked = False # only update if MOUSEBUTTONUP detected

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard, revealedBoxes) # draw current state of the board

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: # cursor has moved
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP: # mouse button released by user (clicked)
                mousex, mousey = event.pos
                mouseClicked = True

        # Checking Which Box the Mouse Cursor is Over
        boxx, boxy = getBoxAtPixel(mousex, mousey) # return tuple of (x,y) board coords of cursor location
        if boxx != None and boxy != None:  # cursor x coord on box and cursor y coord on box
            # The mouse is currently over a box.
            # check if box covered - access list of list of booleans
            if not revealedBoxes[boxx][boxy]: # highlight box if not already revealed
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked: # user selected box for reveal
                revealBoxesAnimation(mainBoard, [(boxx, boxy)]) # play box reveal animation for box at (x,y)
                revealedBoxes[boxx][boxy] = True # box 'revealed' so True in list of lists at column|row (x,y)

                # Handling the First Clicked Box
                if firstSelection == None: # the current box was the first box clicked, set to None before game loop
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    
                    # Handling a Mismatched Pair of Icons
                    if icon1shape != icon2shape or icon1color != icon2color:
                        # Icons don't match. Re-cover both selections.
                        pygame.time.wait(COVERBOXESWAIT) # 1000 milliseconds = 1 second
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)]) # play animation
                        # update revealedBoxes list of list of booleans for selected boxes from True to False
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False # first selection no longer revealed
                        revealedBoxes[boxx][boxy] = False # second selection no longer revealed
                        # if boxes match then can leave both boxes in revealed state - just need to update data for game state
                    
                    # Handling if the Player Won
                    elif hasWon(revealedBoxes): # check if all pairs found (True if so), checks each time pair revealed
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(GAMEWONWAIT)

                        # Reset the board
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(REVEALBOARDWAIT)

                        # Replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None # reset firstSelection variable

        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Creating the 'Revealed Boxes' Data Structure
# Create list of list of boolean values
def generateRevealedBoxesData(value):
    revealedBoxes = []
    # structure for loop to produce revealedBoxes[x][y]
    for i in range(BOARDWIDTH): # outer list represents horizontal rows revealedBoxes[x]
        revealedBoxes.append([value] * BOARDHEIGHT) # inner list represents vertical columns revealedBoxes[y]
    return revealedBoxes


# Create the Board Data Structure
# Step 1 - Get All Possible Icons
def getRandomizedBoard():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    # Step 2 - Shuffle and Truncate the List of All Icons
    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # calculate icons needed, have to have matching pairs
    icons = icons[:numIconsUsed] * 2 # make matching pairs of each icon using list slicing and overwrite icons list
    random.shuffle(icons)

    # Step 3 - Placing the Icons on the Board
    # Create the board data structure, with randomly placed icons
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT): 
            column.append(icons[0]) # Create list of randomly selected icons for each list
            del icons[0] # remove the icons as we assign them
        board.append(column) # add the column to the board and start a new column
    return board

# Splitting a List into a List of Lists
def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have
    # at most groupSize number of items
    result = []
    for i in range(0, len(theList), groupSize): # step is groupSize
        result.append(theList[i:i + groupSize]) # example theList[0:8], theList[8:16], theList[16:24]
    return result # returns list of lists with max size of groupSize


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    # easier to refer to box position, not pixel location
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN # return pixel coords for left
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN # return pixel coords for right
    return (left, top) # return two-integer tuple of top left corner of box


def getBoxAtPixel(x, y): # convert to box coordinates from pixel coordinates
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy) # get box coords for each box
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            # call collidepoint() on each box to see if mouse in a given box
            if boxRect.collidepoint(x, y):
                return (boxx,boxy) # return box coordinates
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    # many shape drawing functions call midpoint or quarterpoint of boxes
    # define variables to make it easier to read below in draw() statements hence 'syntactic sugar'
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half    = int(BOXSIZE * 0.5) # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape is DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape is SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape is DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, 
                            ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1),
                            (left, top + half)))
    elif shape is LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape is OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy): # more syntactic sugar
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage): # coverage range between 0 and BOXSIZE
    # Draws boxes being covered/revealed. 'boxes' is a list
    # of two item lists, which have the x & y spot of the box - box coords
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE)) # paint over anything existing
        shape, color = getShapeAndColor(board, box[0], box[1]) # get shape and color data
        drawIcon(shape, color, box[0], box[1]) # draw shape in color at box
        if coverage > 0: 
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update() # drawBoxCovers() called from separate loop than game loop
    FPSCLOCK.tick(FPS) # called from separate loop than game loop


def revealBoxesAnimation(board, boxesToReveal):
    # Do the 'box reveal' animation
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED): # changes coverage variable at intervals
        # white box decreases in size by REVEALSPEED pixels on each iteration
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    # Do the 'box cover' animation
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        # white box increases in size by REVEALSPEED pixels on each iteration
        drawBoxCovers(board, boxesToCover, coverage) # allows us to cover/reveal boxes as necessary

def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    # Helps player recognize that they can click on a covered box to reveal it
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left + HIGHLIGHTOFFSET, top + HIGHLIGHTOFFSET, 
                     BOXSIZE + HIGHLIGHTBOXWIDTH, BOXSIZE + HIGHLIGHTBOXHEIGHT), HIGHLIGHTLINEWIDTH)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes) # otherwise order of boxes being revealed would never change
    boxGroups = splitIntoGroupsOf(GROUPSIZE, boxes) # list of lists with groups to be revealed at same time

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    # Flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(GAMEWONFILLFRAMES):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(GAMEWONWAIT)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes: # revealedBoxes is list of lists
        if False in i: # set inner list as values of i
            return False # if any boxes still covered, game isn't over
    return True


# lets you import the program for testing individual functions
if __name__ == '__main__':
    main()