# Slide Puzzle

import sys
import random
import copy
import pygame
from pygame.locals import *
from CommonRGB import *

# Create the constants
BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None
NUMBERSLIDES = 80

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTTYPE = 'MakingGames/freesansbold.ttf'
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE
BUTTONXMARGIN = -120
RESETYMARGIN = -90
NEWGAMEYMARGIN = -60
SOLVEYMARGIN = -30

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

RESETTEXT = 'Reset'
NEWGAMETEXT = 'New Game'
SOLVETEXT = 'Solve'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock() # create Clock object
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font(BASICFONTTYPE, BASICFONTSIZE) # create Font object

    # Store the option buttons and their rectangles in OPTIONS; makeText() returns (oSurface, oRect) tuple
    RESET_SURF, RESET_RECT = makeText(RESETTEXT, TEXTCOLOR, TILECOLOR, WINDOWWIDTH + BUTTONXMARGIN, WINDOWHEIGHT + RESETYMARGIN)
    NEW_SURF, NEW_RECT = makeText(NEWGAMETEXT, TEXTCOLOR, TILECOLOR, WINDOWWIDTH + BUTTONXMARGIN, WINDOWHEIGHT + NEWGAMEYMARGIN)
    SOLVE_SURF, SOLVE_RECT = makeText(SOLVETEXT, TEXTCOLOR, TILECOLOR, WINDOWWIDTH + BUTTONXMARGIN, WINDOWHEIGHT + SOLVEYMARGIN)

    # need two board data structures: current state, solved state
    mainBoard, solutionSeq = generateNewPuzzle(NUMBERSLIDES) # scramble tiles NUMBERSLIDES times over
    SOLVEDBOARD = getStartingBoard() # a solved board is the same as the board in a start state
    allMoves = [] # list of moves made since solved puzzle scrambled by NUMBERSLIDES

    while True: # main game loop
        slideTo = None # the direction, if any, a tile should slide as decided by user
        msg = '' # contains the message to show in the upper left corner
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved!'

        drawBoard(mainBoard, msg)

        checkForQuit() # see if any QUIT events created and terminate if so
        for event in pygame.event.get(): # event handling loop
            # check if the user clicked the mouse on a tile or blank spot
            if event.type == MOUSEBUTTONUP: # mouse button released by user somewhere over the window
                # Pass mouse coordinates to getSpotClicked() to return board coordinates of spot on board where mouse released
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1]) # event.pos[0] - x coord | event.pos[1] - y coord

                # getSpotClicked() returns (None, None) if not on slider; need another check for Reset, New, Solve buttons
                if (spotx, spoty) == (None, None):
                    # check if the user clicked on an option (Reset, New, Solve) button
                    if RESET_RECT.collidepoint(event.pos): # coords of Reset button in Rect object
                        resetAnimation(mainBoard, allMoves) # clicked on Reset button
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(NUMBERSLIDES) # clicked on New Game button
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
                        allMoves = []
                else:
                    # user clicked on tile on the board
                    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard) # using board coordinate data structure
                    if spotx == blankx + 1 and spoty == blanky: # spot clicked is right of blank
                        slideTo = LEFT # move block left, 'blank' moves right
                    elif spotx == blankx - 1 and spoty == blanky: # spot clicked is left of blank
                        slideTo = RIGHT # move block right, 'blank' moves left
                    elif spotx == blankx and spoty == blanky + 1: # spot clicked is below blank
                        slideTo = UP # move block up, 'blank' moves down
                    elif spotx == blankx and spoty == blanky - 1: # spot clicked is above blank
                        slideTo = DOWN # move block down, 'blank' moves up
                    # if user clicks on tiles not near blank then we need record no activity; None

            elif event.type == KEYUP:
                # check if the user pressed a key to slide a tile
                # Uses arrow and WASD keys
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT): # one of K_LEFT and/or K_a
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
                
        if slideTo:
            # actually performing tile slide here
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
            makeMove(mainBoard, slideTo) # update actual board data structure
            allMoves.append(slideTo) # record the slide, used in reverse to 'solve' puzzle (return to solved state)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate(): # sytactic sugar
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events - leave remaining events in event queue
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events from the event queue
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back in event queue
        # if KEYUP events not 'posted' no other KEYUP events will be handled (arrow and WASD keys)


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    # [1][2][3]
    # [4][5][6]
    # [7][8]BLANK
    # numbers on itles increase by 1 going across the row, not down the column
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT -1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = BLANK # set last position on board to BLANK
    return board


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space
    # Use function instead of tracking blank space
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK: # only one blank space will resolve to (True, True)
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid
    # Move validation handled in main game loop
    blankx, blanky = getBlankPosition(board)

    # Value for tile is swapped with value for blank space - passing Boolean right? T|F at [x][y]
    if move == UP: # blank 'moves' DOWN (y + 1)
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
        # since board parameter is passed a list reference we don't need a return statement
        # any changes made to board in this function will be made to the list value passed to makeMove()


def isValidMove(board, move):
    # Move being valid depends on location of blank space
    blankx, blanky = getBlankPosition(board)
    # single expression below vvv
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


# used to scramble the board at the beginning of the game, lastMove parameter key to functionality
def getRandomMove(board, lastMove=None):
    # start with a full list of all four moves
    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN): # pointless to move UP then DOWN
        validMoves.remove(DOWN) # check every validMove
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    # return a random move from the list of remaining moves
    return random.choice(validMoves)


# Converting Board(tile) Coordinates to Pixel Coordinates
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


# Converting Pixel Coordinates to Board Coordinates
def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)): # for each tile on board
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY) # fetch pixel coordinates
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE) # need to build rect to call .collidepoint()
            if tileRect.collidepoint(x, y): # check if pixel coordinates of tile collide with mouse
                return (tileX, tileY) # return the board coordinates
    return (None, None) # pixel coords not over any board space


def drawTile(tilex, tiley, number, adjx=0, adjy=0): #adjx,adjy helpful for drawing as tile slides
    # draw a numbered tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley) # convert board coordinates to pixel coordinates
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE)) # draw background square adjust as needed
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR) # draw surface with number text drawn on it
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)
    # doesn't call pygame.display.update() because will want multiple tiles to be drawn before updating screen


def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text - one function instead of multiple calls for each text
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR) # paint over everything
    if message: # skipped if message='', otherwise draws message at top of window
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    # draw all tiles to the display Surface
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    # Drawing the Border of the Board
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    # Drawing the Buttons
    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid
    # Checks handled in main game loop
    # Need to know where the blank space is and where the moving tile is

    # Find blank space
    blankx, blanky = getBlankPosition(board)
    # Find moving tile based on blank space and direction of the slide (slide direction already validated)
    if direction == UP:
        movex = blankx # board x coord of tile to be moved
        movey = blanky + 1 # board y coord of tile to be moved
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface
    # we will draw the sliding tile over different parts of the baseSurf Surface object when we draw each frame of animation
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        # Any events created by the user during animation are not being handled
        # Will be handled next time through main() function or code in the checkForQuit() function
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting config, make numSlides number of moves (and animate these moves)
    # Also create board data structure for game with call to getStartingBoard()
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500) # pause 500 milliseconds for effect
    lastMove = None # used in 'Solve' action to reverse all moves since board created
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', animationSpeed=int(TILESIZE / 3))
        makeMove(board, move) # animation does not actually update board structure so need makeMove() call here
        sequence.append(move)
        lastMove = move
    return (board, sequence)


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse
    revAllMoves = copy.copy(allMoves) # makes a copy of the list using list slicing rather than copying list references
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()