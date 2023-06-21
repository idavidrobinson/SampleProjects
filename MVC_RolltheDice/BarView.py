# BarView

from Bin import *
from Constants import *

# Constants
ROLL_TOTAL_LOC = (50,406)
ROLL_TOTAL_TEXT = 'Roll total:'
ROLL_TOTAL_FONT_SIZE = 16
ROLL_TOTAL_WIDTH = 80

COUNT_LOC = (50,441)
COUNT_TEXT = 'Count:'
COUNT_FONT_SIZE = 16
COUNT_WIDTH = 80

PERCENT_LOC = (50,471)
PERCENT_TEXT = 'Percent:'
PERCENT_FONT_SIZE = 16
PERCENT_WIDTH = 80

class BarView():
    def __init__(self, window, oModel):
        self.window = window
        self.oModel = oModel

        self.oRollTotal = pygwidgets.DisplayText(window=self.window, loc=ROLL_TOTAL_LOC, value=ROLL_TOTAL_TEXT, fontName=ARIAL_FONT, 
                                                 fontSize=ROLL_TOTAL_FONT_SIZE, justified=RIGHT, width=ROLL_TOTAL_WIDTH)

        self.oCount = pygwidgets.DisplayText(window=self.window, loc=COUNT_LOC, value=COUNT_TEXT, fontName=ARIAL_FONT,
                                             fontSize=COUNT_FONT_SIZE, justified=RIGHT, width=COUNT_WIDTH)

        self.oPercent = pygwidgets.DisplayText(window=self.window, loc=PERCENT_LOC, value=PERCENT_TEXT, fontName=ARIAL_FONT,
                                               fontSize=PERCENT_FONT_SIZE, justified=RIGHT, width=PERCENT_WIDTH)

        self.oBinsDict = {}
        # Possible rolls only go from 2 to 12 with 2 dice
        for rollTotal in range(MIN_TOTAL, MAX_TOTAL_PLUS_1): # using PLUS_1 to include MAX in range()
            oBin = Bin(window=self.window, binNumber=rollTotal) # oBins 2-12
            self.oBinsDict[rollTotal] = oBin

    def update(self):
        # ask Model to generate rolls and return results/data as attributes of oModel
        nRounds, resultsDict, percentsDict = self.oModel.getRoundsRollsPercents() # request data from oModel via getter .get...()
        for rollTotal in range(MIN_TOTAL, MAX_TOTAL_PLUS_1): # for 2 - 12 results in resultsDict and PercentsDict
            thisResult = resultsDict[rollTotal]
            thisPercent = percentsDict[rollTotal]
            oBin = self.oBinsDict[rollTotal]
            oBin.update(nRounds, thisResult, thisPercent)

    def draw(self):
        # draw __init__ attributes
        self.oRollTotal.draw()
        self.oCount.draw()
        self.oPercent.draw()
        # draw Bins in oBinsDict
        for oBin in self.oBinsDict.values():
            oBin.draw()