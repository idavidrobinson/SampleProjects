# Card class
import pygame
import pygwidgets

class Card():

    BACK_OF_CARD_IMAGE = pygame.image.load('CardGames/images/BackofCard.png')

    def __init__(self, window, rank, suit, value):
        self.window = window
        self.rank = rank
        self.suit = suit
        self.cardName = rank + ' of ' + suit
        self.value = value
        fileName = 'CardGames/images/' + self.cardName + '.png'
        # Set some starting location; use setLoc below to change
        self.images = pygwidgets.ImageCollection(window=window, loc=(0,0), 
                                                 imagesDict={'front':fileName, 'back':Card.BACK_OF_CARD_IMAGE},
                                                 startImageKey='back')

    def conceal(self):
        self.images.replace('back')

    def reveal(self):
        self.images.replace('front')

    def getName(self):
        return self.cardName

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def setLoc(self, loc): # call the setLoc method of the ImageCollection
        self.images.setLoc(loc)

    def getLoc(self):
        loc = self.images.getLoc()
        return loc

    def draw(self):
        self.images.draw()
