# The Results scene
# The player is shown the results of the current round

import pygwidgets
import pyghelpers
import pygame
from RPS_Constants import *

class SceneResults(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.playerScore = 0
        self.computerScore = 0

        self.rpsCollectionPlayer = pygwidgets.ImageCollection(
                                window, (50, 62),
                                {ROCK: ROCK_IMG,
                                PAPER: PAPER_IMG,
                                SCISSORS: SCISSORS_IMG}, '')
        self.rpsCollectionComputer = pygwidgets.ImageCollection(
                                window, (350, 62),
                                {ROCK: ROCK_IMG,
                                PAPER: PAPER_IMG,
                                SCISSORS: SCISSORS_IMG}, '')

        self.youComputerField = pygwidgets.DisplayText(
                                window, (22, 25),
                                'You                     Computer',
                                fontSize=50, textColor=WHITE, width=610, justified='center')

        self.resultsField = pygwidgets.DisplayText(
                                self.window, (20, 275), '',
                                fontSize=50, textColor=WHITE,
                                width=610, justified='center')

        self.restartButton = pygwidgets.CustomButton(
                                self.window, (220, 310),
                                up=RESTART_UP_IMG,
                                down=RESTART_DOWN_IMG,
                                over=RESTART_HIGHLIGHT_IMG)

        self.playerScoreCounter = pygwidgets.DisplayText(
                                self.window, (86, 315), SCORE_TEXT,
                                fontSize=50, textColor=WHITE)

        self.computerScoreCounter = pygwidgets.DisplayText(
                                self.window, (384, 315), SCORE_TEXT,
                                fontSize=50, textColor=WHITE)
        # Sounds
        self.winnerSound = pygame.mixer.Sound(WINNER_SOUND)
        self.tieSound = pygame.mixer.Sound(TIE_SOUND)
        self.loserSound = pygame.mixer.Sound(LOSER_SOUND)

    def getSceneKey(self):
        return SCENE_RESULTS

    def enter(self, data):
        # data is a dictionary (comes from Play scene) that looks like:
        #      {'player':playerChoice, 'computer':computerChoice}
        playerChoice = data['player']
        computerChoice = data['computer']

        # Set the player and computer images
        self.rpsCollectionPlayer.replace(playerChoice)
        self.rpsCollectionComputer.replace(computerChoice)

        # Evaluate the game's win/lose/tie conditions
        if playerChoice == computerChoice:
            self.resultsField.setValue(TIE_TEXT)
            self.tieSound.play()

        elif playerChoice == ROCK and computerChoice == SCISSORS:
            self.resultsField.setValue(ROCK_SCISSORS_TEXT + WIN_TEXT)
            self.playerScore = self.playerScore + 1
            self.winnerSound.play()

        elif playerChoice == ROCK and computerChoice == PAPER:
            self.resultsField.setValue(ROCK_PAPER_TEXT + LOSE_TEXT)
            self.computerScore = self.computerScore + 1
            self.loserSound.play()

        elif playerChoice == SCISSORS and computerChoice == PAPER:
            self.resultsField.setValue(SCISSORS_PAPER_TEXT + WIN_TEXT)
            self.playerScore = self.playerScore + 1
            self.winnerSound.play()

        elif playerChoice == SCISSORS and computerChoice == ROCK:
            self.resultsField.setValue(SCISSORS_ROCK_TEXT + LOSE_TEXT)
            self.computerScore = self.computerScore + 1
            self.loserSound.play()

        elif playerChoice == PAPER and computerChoice == ROCK:
            self.resultsField.setValue(PAPER_ROCK_TEXT + WIN_TEXT)
            self.playerScore = self.playerScore + 1
            self.winnerSound.play()

        elif playerChoice == PAPER and computerChoice == SCISSORS:
            self.resultsField.setValue(PAPER_SCISSORS_TEXT + LOSE_TEXT)
            self.computerScore = self.computerScore + 1
            self.loserSound.play()

        # Show the player's and computer's scores.
        self.playerScoreCounter.setValue(
                               SCORE_TEXT + ' ' + str(self.playerScore))
        self.computerScoreCounter.setValue(
                               SCORE_TEXT + ' ' + str(self.computerScore))

    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:
            if self.restartButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

    # No need to include update method,
    # defaults to inherited one which does nothing.

    def draw(self):
        self.window.fill(OTHER_GRAY)
        self.youComputerField.draw()
        self.resultsField.draw()
        self.rpsCollectionPlayer.draw()
        self.rpsCollectionComputer.draw()
        self.playerScoreCounter.draw()
        self.computerScoreCounter.draw()
        self.restartButton.draw()