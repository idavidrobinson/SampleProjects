# Bin - Roll the Dice

import pygame
import pygwidgets
from Constants import *

# Constants
MAX_BAR_HEIGHT = 300
BAR_BOTTOM = 390
BAR_WIDTH = 30
BAR_COLOR = (128,128,128)

COLUMN_LEFT_START = 30
COLUMN_OFFSET = 55

LABEL_OFFSET_RIGHT = 3
LABEL_OFFSET_DOWN = 12
LABEL_FONT_SIZE = 24
LABEL_WIDTH = 25

COUNT_OFFSET_LEFT = -5
COUNT_OFFSET_DOWN = 50
COUNT_FONT_SIZE = 18
COUNT_WIDTH = 50

PERCENT_OFFSET_LEFT = -5
PERCENT_OFFSET_DOWN = 80
PERCENT_FONT_SIZE = 18
PERCENT_WIDTH = 50

# Bin Class
class Bin():
    def __init__(self, window, binNumber):
        self.window = window
        self.pixelsPerCount = MAX_BAR_HEIGHT
        self.left = COLUMN_LEFT_START + (binNumber * COLUMN_OFFSET)

        self.oBinLabel = pygwidgets.DisplayText(window=window, loc=(self.left + LABEL_OFFSET_RIGHT, BAR_BOTTOM + LABEL_OFFSET_DOWN), 
                                                value=binNumber, fontName=ARIAL_FONT, fontSize=LABEL_FONT_SIZE, width=LABEL_WIDTH, 
                                                justified=CENTER)

        self.oBinCount = pygwidgets.DisplayText(window=window, loc=(self.left + COUNT_OFFSET_LEFT, BAR_BOTTOM + COUNT_OFFSET_DOWN), 
                                                value='', fontName=ARIAL_FONT, fontSize=COUNT_FONT_SIZE, width=COUNT_WIDTH, 
                                                justified=CENTER)

        self.oBinPercent = pygwidgets.DisplayText(window=window, loc=(self.left + PERCENT_OFFSET_LEFT, BAR_BOTTOM + PERCENT_OFFSET_DOWN), 
                                                  value='', fontName=ARIAL_FONT, fontSize=PERCENT_FONT_SIZE, width=PERCENT_WIDTH, 
                                                  justified=RIGHT)

    def update(self, nRounds, count, percent):
        # set new BinCount
        self.oBinCount.setValue(count)
        # set new BinPercent
        percent = '{:.1%}'.format(percent)
        self.oBinPercent.setValue(percent)
        # set new rect
        # force float here, use int when drawing rects
        self.nPixelsPerTrial = float(MAX_BAR_HEIGHT) / nRounds
        barHeight = int(count * self.nPixelsPerTrial) * 2
        self.rect = pygame.Rect(self.left, BAR_BOTTOM - barHeight, BAR_WIDTH, barHeight)

    def draw(self):
        pygame.draw.rect(surface=self.window, color=BAR_COLOR, rect=self.rect, width=0)
        self.oBinLabel.draw()
        self.oBinCount.draw()
        self.oBinPercent.draw()