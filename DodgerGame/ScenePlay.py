# Play scene - the main game play scene
import pygame
from pygame.locals import *
import pygwidgets
import pyghelpers
from Constants import *
from Player import *
from Baddies import *
from Goodies import *

# Play Constants
BOTTOM_RECT = (0, GAME_HEIGHT + 1, WINDOW_WIDTH, WINDOW_HEIGHT - GAME_HEIGHT)

# States
STATE_WAITING = 'waiting'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game over'

# Text
SCORE_DISPLAY_TEXT = 'Score:                                 High Score:'
YOUR_SCORE_TEXT = 'Your score: '
HIGHEST_SCORE_TEXT = 'is a new high score, CONGRATULATIONS!'
HIGH_SCORE_TEXT = 'gets you on the high scores list!'

# Only appears when user score qualifies for high score table 
# Asks the user if they want to record their score to the high scores list
# (enhancement: replace with standard post game window regardless of user score that allows nav to High Scores scene)
def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(window=theWindow, loc=(40,250), pathOrLoadedImage=DIALOG_IMG)

    oPromptDisplayText = pygwidgets.DisplayText(window=theWindow, loc=(0,290), value=theText, width=WINDOW_WIDTH,
                                                justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(window=theWindow, loc=(320, 370),
                                         up=HIGH_SCORES_UP_IMG, over=HIGH_SCORES_OVER_IMG,
                                         down=HIGH_SCORES_DOWN_IMG, disabled=HIGH_SCORES_DISABLED_IMG)

    oNoButton = pygwidgets.CustomButton(window=theWindow, loc=(62, 370),
                                         up=NO_BUTTON_UP_IMG, over=NO_BUTTON_OVER_IMG,
                                         down=NO_BUTTON_DOWN_IMG, disabled=NO_BUTTON_DISABLED_IMG)

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow=theWindow, oDialogImage=oDialogBackground,
                                                   oPromptText=oPromptDisplayText, oYesButton=oYesButton,
                                                   oNoButton=oNoButton)

    return choiceAsBoolean

class ScenePlay(pyghelpers.Scene):

    def __init__(self, window):
        self.window=window
        self.controlsBackground = pygwidgets.Image(window=self.window, loc=(0, GAME_HEIGHT),
                                                   pathOrLoadedImage=CONTROLS_BACKGROUND_IMG)
        
        self.quitButton = pygwidgets.CustomButton(window=self.window, loc=(30, GAME_HEIGHT + 90),
                                                  up=QUIT_BUTTON_UP_IMG, down=QUIT_BUTTON_DOWN_IMG,
                                                  over=QUIT_BUTTON_OVER_IMG, disabled=QUIT_BUTTON_DISABLED_IMG)

        self.highScoresButton = pygwidgets.CustomButton(window=self.window, loc=(190, GAME_HEIGHT + 90),
                                                        up=HIGH_SCORES_UP_IMG, down=HIGH_SCORES_DOWN_IMG,
                                                        over=HIGH_SCORES_OVER_IMG, disabled=HIGH_SCORES_DISABLED_IMG)

        self.newGameButton = pygwidgets.CustomButton(window=self.window, loc=(450, GAME_HEIGHT + 90),
                                                     up=NEW_GAME_UP_IMG, down=NEW_GAME_DOWN_IMG,
                                                     over=NEW_GAME_OVER_IMG, disabled=NEW_GAME_DISABLED_IMG,
                                                     enterToActivate=True)
                                    
        self.soundCheckBox = pygwidgets.TextCheckBox(window=self.window, loc=(430, GAME_HEIGHT + 17),
                                                     text=BACKGROUND_MUSIC_CHECK_TEXT, value=True, textColor=WHITE)

        self.gameOverImage = pygwidgets.Image(window=self.window, loc=(140,180), 
                                              pathOrLoadedImage=GAME_OVER_IMG)

        self.titleText = pygwidgets.DisplayText(window=self.window, loc=(70, GAME_HEIGHT + 17),
                                                value=SCORE_DISPLAY_TEXT, fontSize=24, textColor=WHITE)

        self.scoreText = pygwidgets.DisplayText(window=self.window, loc=(80, GAME_HEIGHT + 47), value='0',
                                                fontSize=36, textColor=WHITE, justified='right')

        self.highScoreText = pygwidgets.DisplayText(window=self.window, loc=(270, GAME_HEIGHT + 47), value='',
                                                    fontSize=36, textColor=WHITE, justified='right')

        pygame.mixer.music.load(BACKGROUND_MUSIC)
        self.dingSound = pygame.mixer.Sound(DING_SOUND)
        self.gameOverSound = pygame.mixer.Sound(GAME_OVER_SOUND)

        # Instantiate objects
        self.oPlayer = Player(self.window)
        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)

        self.highestHighScore = 0
        self.lowestHighScore = 0
        self.backgroundMusic = True
        self.score = 0
        self.playingState = STATE_WAITING

    def getSceneKey(self):
        return SCENE_PLAY

    def enter(self, data):
        self.getHighandLowScores()

    def getHighandLowScores(self):
        ''' 
        Ask the High Scores scene for a dict of scores from high score table:
            {'highest': highestScore, 'lowest': lowestScore} 
        '''
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)
        self.highestHighScore = infoDict['highest']
        self.lowestHighScore = infoDict['lowest']
        # update display text for high score in game window - don't show lowest HighScore (could be future enhancement)
        self.highScoreText.setValue(self.highestHighScore)

    def reset(self):    # start a new game
        self.score = 0
        # set display text for player score to zero
        self.scoreText.setValue(self.score)
        # get scores data and update display text for high score
        self.getHighandLowScores()

        # Tell the managers to reset themselves
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()

        # Check to see if user wants music
        if self.backgroundMusic:
            pygame.mixer.music.play(-1,0.0)
        
        # Disable buttons once new game is selected
        self.newGameButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()

        # hide the pointer cursor while game is in play mode
        pygame.mouse.set_visible(False) 

    def handleInputs(self, eventsList, keysDownList):
        if self.playingState == STATE_PLAYING:
            return # ignore button events while playing

        for event in eventsList:
            if self.newGameButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING # update from STATE_WAITING

            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue() # retrieve new setting (boolean); used by reset()

            if self.quitButton.handleEvent(event):
                self.quit()

    # Scene Manager will call update() every frame - handles all events during gameplay
    def update(self):
        if self.playingState != STATE_PLAYING:
            return # only update when playing

        # Move the Player to the mouse position, get back its rect
        # Need to move Player first, then check for Goodies and Baddies contacting Player after movement
        # Data sent from Player.py .update() method
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)

        # Tell the GoodieMgr to move all the Goodies
        # Returns the number of Goodies that contact the updated Player location
        nGoodiesHit = self.oGoodieMgr.update(playerRect)
        if nGoodiesHit > 0:
            self.dingSound.play()
            self.score = self.score + (nGoodiesHit * POINTS_FOR_GOODIE)

        # Tell the BaddieMgr to move all the Baddies
        # Returns the number of Baddies that fell off the bottom in that frame - avoiding contact with Player throughout
        nBaddiesEvaded = self.oBaddieMgr.update()
        self.score = self.score + (nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED)

        self.scoreText.setValue(self.score)

        # Check if the Player has hit any Baddie which ends the game
        # As soon as a Baddie makes contact with the Player, the game ends
        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            self.gameOverSound.play()

            self.playingState = STATE_GAME_OVER
            self.draw() # force drawing of game over message triggered by playingState = STATE_GAME_OVER
            # 'we may put up a dialog for the user, and the game's main loop will not draw the Game Over
            # graphic until the user clicks one of the buttons in the dialog'

            # check to see if score qualifies for high scores table
            # send special message in the dialog if highest score or on high scores table
            if self.score > self.lowestHighScore:
                scoreString = YOUR_SCORE_TEXT + str(self.score) + '\n'
                # check to see if score beats previous highest score
                if self.score > self.highestHighScore:
                    dialogText = (scoreString + HIGHEST_SCORE_TEXT)
                # score is in high score table but not highest score
                else:
                    dialogText = (scoreString + HIGH_SCORE_TEXT)

                # send score data and dialog text to High Scores scene
                # 'put up a dialog giving the user the option of recording their score in the high scores list.'
                result = showCustomYesNoDialog(self.window, dialogText)
                if result: # navigate to High Scores scene
                     self.goToScene(SCENE_HIGH_SCORES, self.score)

            # enable all buttons and boxes
            self.newGameButton.enable()
            self.highScoresButton.enable()
            self.soundCheckBox.enable()
            self.quitButton.enable()
    
    def draw(self):
        self.window.fill(BLACK)

        # Tell the managers to draw all Baddies and Goodies
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()

        # Tell the Player to draw itself
        self.oPlayer.draw()

        # Draw all the info at the bottom of the window
        self.controlsBackground.draw()
        self.titleText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.newGameButton.draw()

        # picks up playingState update from update() when Baddie contacts Player
        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    # When user navigates away from this scene, the scene manager calls the leave() method
    def leave(self):
        pygame.mixer.music.stop()