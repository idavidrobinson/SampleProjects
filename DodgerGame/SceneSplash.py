# Splash scene - first scene the user sees
import pygwidgets
import pyghelpers
from Constants import *

class SceneSplash(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.backgroundImage = pygwidgets.Image(window=self.window, loc=(0,0),
                                                pathOrLoadedImage=SPLASH_BACKGROUND_IMG)
        
        self.dodgerImage = pygwidgets.Image(window=self.window, loc=(150,30),
                                            pathOrLoadedImage=DODGER_IMG)
        
        self.startButton = pygwidgets.CustomButton(window=self.window, loc=(250,500), up=START_BUTTON_UP_IMG,
                                                   down=START_BUTTON_DOWN_IMG, over=START_BUTTON_OVER_IMG,
                                                   disabled=START_BUTTON_DISABLED_IMG, enterToActivate=True)
        
        self.quitButton = pygwidgets.CustomButton(window=self.window, loc=(30,650), up=QUIT_BUTTON_UP_IMG,
                                                   down=QUIT_BUTTON_DOWN_IMG, over=QUIT_BUTTON_OVER_IMG,
                                                   disabled=QUIT_BUTTON_DISABLED_IMG, enterToActivate=True)
        
        self.highScoresButton = pygwidgets.CustomButton(window=self.window, loc=(360,650), up=HIGH_SCORES_UP_IMG,
                                                   down=HIGH_SCORES_DOWN_IMG, over=HIGH_SCORES_OVER_IMG,
                                                   disabled=HIGH_SCORES_DISABLED_IMG, enterToActivate=True)

    def getSceneKey(self):
        return SCENE_SPLASH # unique key for the scene

    def handleInputs(self, eventsList, keysDownList):
        for event in eventsList:
            if self.startButton.handleEvent(event):
                self.goToScene(SCENE_PLAY)
            elif self.quitButton.handleEvent(event):
                self.quit()
            elif self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

    def draw(self):
        self.backgroundImage.draw()
        self.dodgerImage.draw()
        self.startButton.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()