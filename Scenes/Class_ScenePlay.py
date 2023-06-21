# The Play scene
# The player chooses among rock, paper, or scissors

import pygwidgets
import pyghelpers
import pygame
from RPS_Constants import *
import random

class ScenePlay(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.RPSTuple = RPS_TUPLE

        self.titleField = pygwidgets.DisplayText(self.window, (15, 40), '    Rock               Paper          Scissors', 
                                              fontSize=50, textColor=WHITE, width=610, justified='center')

        self.messageField = pygwidgets.DisplayText(self.window, (30, 395), CHOOSE_TEXT, 
                                              fontSize=50, textColor=WHITE, width=610, justified='center')

        self.rockButton = pygwidgets.CustomButton(self.window, (25, 120), 
                                             up=ROCK_IMG, 
                                             over=ROCK_HIGHLIGHT_IMG, 
                                             down=ROCK_DOWN_IMG)

        self.paperButton = pygwidgets.CustomButton(self.window, (225, 120), 
                                              up=PAPER_IMG, 
                                              over=PAPER_HIGHLIGHT_IMG, 
                                              down=PAPER_DOWN_IMG)

        self.scissorButton = pygwidgets.CustomButton(self.window, (425, 120), 
                                                up=SCISSORS_IMG, 
                                                over=SCISSORS_HIGHLIGHT_IMG, 
                                                down=SCISSORS_DOWN_IMG)

    def getSceneKey(self):
        return SCENE_PLAY

    def handleInputs(self, eventsList, keyPressedList):
        playerChoice = None

        for event in eventsList:
            if self.rockButton.handleEvent(event):
                playerChoice = ROCK

            if self.paperButton.handleEvent(event):
                playerChoice = PAPER

            if self.scissorButton.handleEvent(event):
                playerChoice = SCISSORS

            if playerChoice is not None:  # user has made a choice
                computerChoice = random.choice(self.RPSTuple)  # computer chooses
                dataDict = {'player': playerChoice, 'computer': computerChoice}
                self.goToScene(SCENE_RESULTS, dataDict)  # go to Results scene

    # No need to include update method, defaults to inherited one which does nothing

    def draw(self):
        self.window.fill(GRAY)
        self.titleField.draw()
        self.rockButton.draw()
        self.paperButton.draw()
        self.scissorButton.draw()
        self.messageField.draw()
