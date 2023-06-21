# Simulate (a Simon clone)
# Copy the pattern of flashing lights for as long as possible

import sys
import time
import random
import pygame
from pygame.locals import *
from CommonRGB import *
from CommonGameSpecs import *

FLASHSPEED = 500 # milliseconds
FLASHDELAY = 200 # milliseconds
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed

# using muted colors to make NEONCOLOR more noticeable on highlight
SIMULATEBLUE    = (  0,   0, 155)
SIMULATEGREEN   = (  0, 155,   0)
SIMULATERED     = (155,   0,   0)
SIMULATEYELLOW  = (155, 155,   0)

bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

# Rect objects for each of the four buttons
# Need rect objects so we can call collidpoint() method on them
YELLOWRECT  = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT    = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT     = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4 # defined below

    # start game and store Clock, window, Font, and Sound objects as global variables for use by other functions
    # essentially setting constants specific to Pygame library
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Simulate')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    # note text for infoSurf will not update as game is played
    infoSurf = BASICFONT.render('Match the pattern by clicking on the button or using the Q, W, A, S keys.', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # load the sounds files
    # these sounds will play when user selects button or correct button sequence plays
    BEEP1 = pygame.mixer.Sound('MakingGames/beep1.ogg')
    BEEP2 = pygame.mixer.Sound('MakingGames/beep2.ogg')
    BEEP3 = pygame.mixer.Sound('MakingGames/beep3.ogg')
    BEEP4 = pygame.mixer.Sound('MakingGames/beep4.ogg')

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors values in a list [SIMULATERED, SIMULATEYELLOW, SIMULATERED]
    currentStep = 0 # the color the player must push next in the current pattern of colors
    ''' 
    if currentStep = 0 and pattern = [SIMULATEGREEN, SIMULATERED, SIMULATERED, SIMULATEYELLOW
    then the player would have to click the green Rect object (with value = SIMULATEGREEN) 
    '''
    lastClickTime = 0 # timestamp of the player's last button push
    '''
    used with TIMEOUT constant to make player click next button in sequence within a given
    number of seconds, otherwise the code causes a game ove
    '''
    score = 0

    waitingForInput = False
    '''
    two states to Simulate program: 1). playing sequence for user 2). waiting to receive user input
    when False, the sequence is playing;  when True, waiting for the player to click a colored button:   
    '''

    while True: # main game loop
        # button that was clicked (set to SIMULATEYELLOW, SIMULATERED, SIMULATEGREEN, or SIMULATEBLUE)
        clickedButton = None 
        DISPLAYSURF.fill(bgColor)
        drawButtons()

        scoreSurf = BASICFONT.render(f'Score: {score}', 1, WHITE) # change Score text as applicable
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos # XY coordinates of any mouse clicks
                clickedButton = getButtonClicked(mousex, mousey) # return Color object of button clicked (otherwise None returned)
            elif event.type == KEYDOWN: # created when user presses a key on the keyboard
                if event.key == K_q:
                    clickedButton = SIMULATEYELLOW # same functionality provided with keyboard as mouse
                elif event.key == K_w:
                    clickedButton = SIMULATEBLUE
                elif event.key == K_a:
                    clickedButton = SIMULATERED
                elif event.key == K_s:
                    clickedButton = SIMULATEGREEN


        if not waitingForInput: # if not waiting for user input, must be starting next sequence in pattern
            # play the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((SIMULATEYELLOW, SIMULATEBLUE, SIMULATERED, SIMULATEGREEN)))
            for button in pattern: # play sequence with flashing buttons (and sounds) for user
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True # then update game state
        else: #waitingForInput = True
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step
            
            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):
                # pushed the incorrect button, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                changeBackgroundAnimation()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
              

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back


def flashButtonAnimation(color, animationSpeed = 50):
    if color == SIMULATEYELLOW:
        sound = BEEP1
        flashColor = NEONYELLOW
        rectangle = YELLOWRECT
    elif color == SIMULATEBLUE:
        sound = BEEP2
        flashColor = NEONBLUE
        rectangle = BLUERECT
    elif color == SIMULATERED:
        sound = BEEP3
        flashColor = NEONRED
        rectangle = REDRECT
    elif color == SIMULATEGREEN:
        sound = BEEP4
        flashColor = NEONGREEN
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): # animation loop
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    DISPLAYSURF.blit(origSurf, (0, 0))


def drawButtons():
    pygame.draw.rect(DISPLAYSURF, SIMULATEYELLOW,   YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, SIMULATEBLUE,     BLUERECT)
    pygame.draw.rect(DISPLAYSURF, SIMULATERED,      REDRECT)
    pygame.draw.rect(DISPLAYSURF, SIMULATEGREEN,    GREENRECT)


def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()
        DISPLAYSURF. fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0,0))

        drawButtons() # redraw the buttons on top of the tint

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor


def gameOverAnimation(color=WHITE, animationSpeed=50):
    # play all beeps at once, then flash the background
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() # play all four beeps at the same time, roughly.
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): # do the flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            # The first iteration in this loop sets the following for loop to go from
            # 0 to 255, the second from 255 to 0
            for alpha in range(start, end, animationSpeed * step): # animation loop
                # alpha means transparency, 255 is opaque, 0 is invisible
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return SIMULATEYELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return SIMULATEBLUE
    elif REDRECT.collidepoint( (x, y) ):
        return SIMULATERED
    elif GREENRECT.collidepoint( (x, y) ):
        return SIMULATEGREEN
    return None


if __name__ == '__main__':
    main()