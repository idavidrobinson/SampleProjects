# Player class
import pygwidgets
from Constants import *

class Player():
    def __init__(self, window):
        self.window = window
        self.image = pygwidgets.Image(window=window, loc=(-100,-100), pathOrLoadedImage=PLAYER_IMG)
        playerRect = self.image.getRect()
        self.maxX = WINDOW_WIDTH - playerRect.width
        self.maxY = GAME_HEIGHT - playerRect.height

    # Every frame, move the Player icon to the mouse position
    # Limits the x- and y-coordinates to the game area of the window
    def update(self, x, y):
        if x < 0:
            x = 0
        elif x > self.maxX:
            x = self.maxX
        if y < 0:
            y = 0
        elif y > self.maxY:
            y = self.maxY

        self.image.setLoc((x, y))
        
        # Return the updated rectangle of the Player icon so the ScenePlay.py code
        # can check if the Player's rectangle intersects with any Baddie or Goodie
        return self.image.getRect()

    def draw(self):
        self.image.draw()