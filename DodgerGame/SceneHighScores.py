# High Scores class
# Display top 10 high scores and names of players in a table
# Optionally, users can add their scores and names to the table
import pygwidgets
import pyghelpers
from HighScoresData import * 
from Constants import *

# High Scores Constants
# Text
TO_RECORD_SCORE_TEXT = 'To record your score of '
ENTER_NAME_TEXT = 'please enter your name:'
RESET_HIGH_SCORE_TEXT = 'Are you sure you want to \nReset the high scores?'

def showCustomAnswerDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(window=theWindow, loc=(35,450), pathOrLoadedImage=DIALOG_IMG)

    oPromptDisplayText = pygwidgets.DisplayText(window=theWindow, loc=(0,480), value=theText, width=WINDOW_WIDTH, 
                                                justified='center', fontSize=36)

    oUserInputText = pygwidgets.InputText(window=theWindow, loc=(200,550), value='', fontSize=36, initialFocus=True)

    oNoButton = pygwidgets.CustomButton(window=theWindow, loc=(65,595), up=NO_BUTTON_UP_IMG, 
                                        down=NO_BUTTON_DOWN_IMG, over=NO_BUTTON_OVER_IMG, disabled=NO_BUTTON_DISABLED_IMG)

    oYesButton = pygwidgets.CustomButton(window=theWindow, loc=(330,595), up=ADD_HIGH_SCORE_UP_IMG, 
                                         down=ADD_HIGH_SCORE_DOWN_IMG, over=ADD_HIGH_SCORE_OVER_IMG, disabled=ADD_HIGH_SCORE_DISABLED_IMG)

    userAnswer = pyghelpers.customAnswerDialog(theWindow=theWindow, oDialogImage=oDialogBackground,
                                               oPromptText=oPromptDisplayText, oAnswerText=oUserInputText,
                                               oOKButton=oYesButton, oCancelButton=oNoButton)

    # What will use userAnswer?
    return userAnswer

def showCustomResetDialog(theWindow, theText):
    # same as showCustomAnswerDialog()
    oDialogBackground = pygwidgets.Image(window=theWindow, loc=(35,450), pathOrLoadedImage=DIALOG_IMG)

    # same as showCustomAnswerDialog()
    oPromptDisplayText = pygwidgets.DisplayText(window=theWindow, loc=(0,480), value=theText,
                                                width=WINDOW_WIDTH, justified='center', fontSize=36)
 
    # same as showCustomAnswerDialog()
    oNoButton = pygwidgets.CustomButton(window=theWindow, loc=(65,595), up=NO_BUTTON_UP_IMG, 
                                        down=NO_BUTTON_DOWN_IMG, over=NO_BUTTON_OVER_IMG, disabled=NO_BUTTON_DISABLED_IMG)

    # same as showCustomAnswerDialog()
    oYesButton = pygwidgets.CustomButton(window=theWindow, loc=(330,595), up=ADD_HIGH_SCORE_UP_IMG,
                                         down=ADD_HIGH_SCORE_DOWN_IMG, over=ADD_HIGH_SCORE_OVER_IMG, disabled=ADD_HIGH_SCORE_DISABLED_IMG)

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow=theWindow, oDialogImage=oDialogBackground,
                                                   oPromptText=oPromptDisplayText, oYesButton=oYesButton,
                                                   oNoButton=oNoButton)

    # What will use choiceAsBoolean?
    return choiceAsBoolean

# HighScoresData object will manage the actual data including read|write to file
# this allows High Scores Scene to update the table and to respond to requests
# from the Play scene for the current high and low scores in the table
class SceneHighScores(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        # Create instance of the HighScoresData class which maintains all the data for the High Scores class
        self.oHighScoresData = HighScoresData()

        # Create all the images, fields, and buttons for the High Scores scene
        self.backgroundImage = pygwidgets.Image(window=self.window, loc=(0,0), pathOrLoadedImage=HIGH_SCORES_BACKGROUND_IMG)

        self.namesField = pygwidgets.DisplayText(window=self.window, loc=(260,84), value='', fontSize=48, textColor=BLACK,
                                                 width=300, justified='left')

        self.scoresField = pygwidgets.DisplayText(window=self.window, loc=(25,84), value='', fontSize=48, textColor=BLACK,
                                                  width=175, justified='right')

        self.quitButton = pygwidgets.CustomButton(window=self.window, loc=(30,650), up=QUIT_BUTTON_UP_IMG,
                                                  down=QUIT_BUTTON_DOWN_IMG, over=QUIT_BUTTON_OVER_IMG, disabled=QUIT_BUTTON_DISABLED_IMG)

        self.backButton = pygwidgets.CustomButton(window=self.window, loc=(240,650), up=BACK_BUTTON_UP_IMG,
                                                  down=BACK_BUTTON_DOWN_IMG, over = BACK_BUTTON_OVER_IMG, disabled=BACK_BUTTON_DISABLED_IMG)

        self.resetScoresButton = pygwidgets.CustomButton(window=self.window, loc=(450,650), up=RESET_HIGH_SCORE_UP_IMG,
                                                         down=RESET_HIGH_SCORE_DOWN_IMG, over =RESET_HIGH_SCORE_OVER_IMG, 
                                                         disabled=RESET_HIGH_SCORE_DISABLED_IMG)
        
        # Call to populate the name and scores fields of the High Scores table
        self.showHighScores()
        
    def getSceneKey(self):
        return SCENE_HIGH_SCORES

    # Called by sceneMgr when navigating to High Scores scene from Play scene
    def enter(self, newHighScoreValue=None):
        # This can be called two different ways:
        # 1. If no new high score, newHighScoreValue will be None
        # 2. newHighScoreValue is score of the current game if it qualifies for top 10
        if newHighScoreValue is None:
            return # nothing to do, current list of high scores is already displayed

        self.draw() # draw before showing dialog offering user choice to add their score and name
        # We have a new high score sent in from the Play scene
        dialogQuestion = (TO_RECORD_SCORE_TEXT + str(newHighScoreValue) + ',\n' + ENTER_NAME_TEXT)

        # Custom Answer Dialog box for recording player name ('please enter your name')
        playerName = showCustomAnswerDialog(theWindow=self.window, theText=dialogQuestion)

        # User selects 'No Thanks' and None value returned
        if playerName is None:
            return # user pressed Cancel

        # Add user and score to high scores
        if playerName == '':
            playerName = 'CPU'
        
        # playerName check complete, send data to High Scores Data class
        # Name and score are added to the high scores table
        self.oHighScoresData.addHighScore(playerName, newHighScoreValue)
        # Enhancement: Update the High Scores table on the screen
        self.showHighScores()

    def showHighScores(self):
        # Get/update the scores and names, show them in two fields
        # Request data from High Scores Data class
        scoresList, namesList = self.oHighScoresData.getScoresAndNames()
        self.namesField.setValue(namesList) # oDisplayText.setValue() displayes each element on a separate line
        self.scoresField.setValue(scoresList) # two oDisplayTexts: namesField left justified, scoresField right justified

    # Only need to check for user clicking Quit, Back, and Reset Scores buttons
    def handleInputs(self, eventsList, keysDownList):
        for event in eventsList:
            if self.quitButton.handleEvent(event):
                self.quit()

            elif self.backButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)

            elif self.resetScoresButton.handleEvent(event):
                # Check with user to confirm they want to reset high scores data
                confirmed = showCustomResetDialog(theWindow=self.window, theText=RESET_HIGH_SCORE_TEXT)

                if confirmed:
                    self.oHighScoresData.resetScores()
                    self.showHighScores()

    def draw(self):
        self.backgroundImage.draw()
        self.scoresField.draw()
        self.namesField.draw()
        self.quitButton.draw()
        self.resetScoresButton.draw()
        self.backButton.draw()

    def respond(self, requestID):
        if requestID == HIGH_SCORES_DATA:
            # Request from Play scene for the highest and lowest scores
            # Build a dictionary and return it to the Play scene
            highestHighScore, lowestHighScore = self.oHighScoresData.getHighestAndLowest()
            return {'highest':highestHighScore, 'lowest':lowestHighScore}
