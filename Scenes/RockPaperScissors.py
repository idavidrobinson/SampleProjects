# Rock, Paper, Scissors in pygame
# Demonstration of a state machine

# 1 - Import packages
import pygame
from pygame.locals import *
import pygwidgets
import random
import sys
from RPS_Constants import *

# 2 Define constants
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
 
# 4 - Load assets: image(s), sound(s), etc.

# For Splash screen
messageField = pygwidgets.DisplayText(window=window, loc=(15,25), value=SPLASH_WELCOME_TEXT, 
                                    fontSize=50, textColor = WHITE, width = 610, justified = 'center')

rockImage = pygwidgets.Image(window=window, loc=(25,120), pathOrLoadedImage=ROCK_IMG)
paperImage = pygwidgets.Image(window=window, loc=(225,120), pathOrLoadedImage=PAPER_IMG)
scissorsImage = pygwidgets.Image(window=window, loc=(425,120), pathOrLoadedImage=SCISSORS_IMG)

startButton = pygwidgets.CustomButton(window=window, loc=(210,300), up=START_UP_IMG, down=START_DOWN_IMG, over=START_HIGHLIGHT_IMG)

# For Player Choice
rockButton = pygwidgets.CustomButton(window=window, loc=(25,120), up = ROCK_IMG, down = ROCK_DOWN_IMG, over = ROCK_HIGHLIGHT_IMG)
paperButton =  pygwidgets.CustomButton(window=window, loc=(225,120), up = PAPER_IMG, down = PAPER_DOWN_IMG, over = PAPER_HIGHLIGHT_IMG)
scissorButton =  pygwidgets.CustomButton(window=window, loc=(425,120), up = SCISSORS_IMG, down = SCISSORS_DOWN_IMG, over = SCISSORS_HIGHLIGHT_IMG)

chooseText = pygwidgets.DisplayText(window=window, loc=(15,395), value=CHOOSE_TEXT, 
                                    fontSize=50, textColor = WHITE, width = 610, justified = 'center')

resultsField = pygwidgets.DisplayText(window=window, loc=(20,275), value='',
                                    fontSize=50, textColor=WHITE, width=610, justified='center')

# For results
rpsCollectionPlayer = pygwidgets.ImageCollection(window=window, loc=(50,62), 
                    imagesDict={ROCK:ROCK_IMG, PAPER:PAPER_IMG, SCISSORS:SCISSORS_IMG}, startImageKey='')

rpsCollectionComputer = pygwidgets.ImageCollection(window=window, loc=(350,62), 
                    imagesDict={ROCK:ROCK_IMG, PAPER:PAPER_IMG, SCISSORS:SCISSORS_IMG}, startImageKey='')

restartButton = pygwidgets.CustomButton(window=window, loc=(220,310), 
                                    up=RESTART_UP_IMG, down=RESTART_DOWN_IMG, over=RESTART_HIGHLIGHT_IMG)

playerScoreCounter = pygwidgets.DisplayText(window=window, loc=(15,315), value=PLAYER_SCORE_TEXT, 
                                    fontSize=50, textColor = WHITE)

computerScoreCounter = pygwidgets.DisplayText(window=window, loc=(300,315), value=COMPUTER_SCORE_TEXT, 
                                    fontSize=50, textColor = WHITE)

# Sounds
winnerSound = pygame.mixer.Sound('Scenes/sounds/ding.wav')
tieSound = pygame.mixer.Sound('Scenes/sounds/push.wav')
loserSound = pygame.mixer.Sound('Scenes/sounds/buzz.wav')

# 5 - Initialize variables
playerScore = 0
computerScore = 0
state = STATE_SPLASH    # the starting state

# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()        
        
        if state == STATE_SPLASH:
            if startButton.handleEvent(event):
                state = STATE_PLAYER_CHOICE

        elif state == STATE_PLAYER_CHOICE:  # let the user choose
            playerChoice = ''  # indicates no choice yet
            if rockButton.handleEvent(event):
                playerChoice = ROCK
                rpsCollectionPlayer.replace(ROCK)
                
            elif paperButton.handleEvent(event):
                playerChoice = PAPER
                rpsCollectionPlayer.replace(PAPER)
                
            elif scissorButton.handleEvent(event):
                playerChoice = SCISSORS
                rpsCollectionPlayer.replace(SCISSORS)

            if playerChoice != '':  # player has made a choice, make computer choice
                # Computer chooses from tuple of moves
                rps = (ROCK, PAPER, SCISSORS)
                computerChoice = random.choice(rps) # computer chooses
                rpsCollectionComputer.replace(computerChoice)

                # Evaluate the game
                if playerChoice == computerChoice:  # tie
                    resultsField.setValue(TIE_TEXT)
                    tieSound.play()
                    
                elif playerChoice == ROCK and computerChoice == SCISSORS:
                    resultsField.setValue('Rock breaks Scissors.' + WIN_TEXT)
                    playerScore = playerScore + 1
                    winnerSound.play()

                elif playerChoice == ROCK and computerChoice == PAPER:
                    resultsField.setValue('Rock is covered by Paper.' + LOSE_TEXT)
                    computerScore = computerScore + 1
                    loserSound.play()
                   
                elif playerChoice == SCISSORS and computerChoice == PAPER:
                    resultsField.setValue('Scissors cuts Paper.' + WIN_TEXT)
                    playerScore = playerScore + 1
                    winnerSound.play()

                elif playerChoice == SCISSORS and computerChoice == ROCK:
                    resultsField.setValue('Scissors crushed by Rock.' + LOSE_TEXT)
                    computerScore = computerScore + 1
                    loserSound.play()

                elif playerChoice == PAPER and computerChoice == ROCK:
                    resultsField.setValue('Paper covers Rock.' + WIN_TEXT)
                    playerScore = playerScore + 1
                    winnerSound.play()

                elif playerChoice == PAPER and computerChoice == SCISSORS:
                    resultsField.setValue('Paper is cut by Scissors.' + LOSE_TEXT)
                    computerScore = computerScore + 1
                    loserSound.play()

                # Show the player's score
                playerScoreCounter.setValue(PLAYER_SCORE_TEXT + ' ' + str(playerScore))
                # Show the computer's score
                computerScoreCounter.setValue(COMPUTER_SCORE_TEXT + ' ' + str(computerScore))

                state = STATE_SHOW_RESULTS  # change state

        elif state == STATE_SHOW_RESULTS:
            if restartButton.handleEvent(event):
                state = STATE_PLAYER_CHOICE  # change state

        else:
            raise ValueError('Unknown value for state:', state)

    # 8 - Do any "per frame" actions
    if state == STATE_PLAYER_CHOICE:
        messageField.setValue('       Rock             Paper         Scissors')
    elif state == STATE_SHOW_RESULTS:
        messageField.setValue('You                     Computer')

    # 9 - Clear the window
    window.fill(GRAY)

    # 10 - Draw all window elements
    messageField.draw()

    if state == STATE_SPLASH:
        rockImage.draw()
        paperImage.draw()
        scissorsImage.draw()
        startButton.draw()

    # Draw player choices
    elif state == STATE_PLAYER_CHOICE:
        rockButton.draw()
        paperButton.draw()
        scissorButton.draw()
        chooseText.draw()       

    # Draw the results
    elif state == STATE_SHOW_RESULTS:
        resultsField.draw()
        rpsCollectionPlayer.draw()
        rpsCollectionComputer.draw()
        playerScoreCounter.draw()
        computerScoreCounter.draw()
        restartButton.draw()
        
    else:
        raise ValueError('Unknown value for state:', state)

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait 