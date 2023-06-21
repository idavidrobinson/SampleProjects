# PieView

import pygwidgets
import pygame
import pygame.gfxdraw
import math
from Constants import *

# Constants
CENTER_X = 300
CENTER_Y = 300
RADIUS = 200
RADIUS_MINUS_1 = RADIUS - 1

# LEGEND
GRAY_GRADIANT = 20
LEGEND_LOC_X = 550
LEGEND_LOC_Y = 160
LEGEND_FONT_SIZE = 32
LEGEND_VERTICAL_SPACE = 25

class PieView():
    def __init__(self, window, oModel):
        self.window = window
        self.oModel = oModel
        self.legendFieldsDict = {}
        y = LEGEND_LOC_Y
        # Create the legend fields
        for index in range(MIN_TOTAL, MAX_TOTAL_PLUS_1):
            gray = (index * GRAY_GRADIANT, index * GRAY_GRADIANT, index * GRAY_GRADIANT)
            oLegendField = pygwidgets.DisplayText(window=window, loc=(LEGEND_LOC_X, y), value=str(index),
                                                  fontSize=LEGEND_FONT_SIZE, textColor=gray)
            self.legendFieldsDict[index] = oLegendField
            y = y + LEGEND_VERTICAL_SPACE # vertical spacing

    def update(self, ):
        nRounds, resultsDict, percentsDict = self.oModel.getRoundsRollsPercents()

        self.nRounds = nRounds
        self.resultsDict = resultsDict
        self.percentsDict = percentsDict
        for index in range(MIN_TOTAL, MAX_TOTAL_PLUS_1):
            # Could use the count if we want to display it later
            #rollCount = resultsDict[index]
            percent = percentsDict[index]
            oLegendFiled = self.legendFieldsDict[index]

    def drawFilledArc(self, centerX, centerY, radius, degrees1, degrees2, color):
        '''
        This method generates a list of points that are used to create a filled
        polygon representing an arc in the circle. We'll use the angles passed in
        and a little trig to figure out the points in the arc
        '''
        centerTuple = (centerX,centerY)
        nPointsToDraw = int(degrees2-degrees1)
        if nPointsToDraw is 0:
            return # nothing to draw
        # Both degrees parameters need to be converted to radians for calculating points
        radians1 = math.radians(degrees1)
        radians2 = math.radians(degrees2)
        radiansDiff = (radians2 - radians1) / nPointsToDraw

        # Start and end with the center point of the circle
        pointsList = [centerTuple]
        # Determine the points on the edge of the arc
        for pointNumber in range(nPointsToDraw + 1): # check range() error? swapped enum() instead of range(+1)
            offset = pointNumber * radiansDiff
            x = centerX + (radius * math.cos(radians1 + offset))
            y = centerY + (radius * math.sin(radians1 + offset))
            pointsList.append((x,y))
        pointsList.append(centerTuple)

        pygame.gfxdraw.filled_polygon(self.window, pointsList, color)
        # If you would like black lines around each arc, uncomment the next line
        #pygame.gfxdraw.polygon(surface=self.window, points=pointsList, color=BLACK)

    # Draw the slice of the pie (arc) for every roll total
    def draw(self):
        startAngle = 0.0
        for index in range(MIN_TOTAL, MAX_TOTAL_PLUS_1):
            percent = self.percentsDict[index]
            endAngle = startAngle + (percent * 360)
            gray = (index * GRAY_GRADIANT, index * GRAY_GRADIANT, index * GRAY_GRADIANT)
            self.drawFilledArc(centerX=CENTER_X, centerY=CENTER_Y, radius=RADIUS_MINUS_1,
                               degrees1=startAngle, degrees2=endAngle, color=gray)
            self.legendFieldsDict[index].draw()

            startAngle = endAngle # set up for next wedge

        pygame.draw.circle(surface=self.window, color=BLACK, center=(CENTER_X, CENTER_Y),
                           radius=RADIUS, width=2)