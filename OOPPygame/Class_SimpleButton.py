'''
SimpleButton class
Uses a "state machine" approach
'''
import pygame
from pygame.locals import *

class SimpleButton():
    # Used to track the state of the button
    STATE_IDLE = 'idle' # button is up, mouse not over button
    STATE_ARMED = 'armed' # button is down, mouse over button
    STATE_DISARMED = 'disarmed' # clicked down on button, rolled off

    def __init__(self, window, loc, up, down, callBack=None):
        self.window = window
        self.loc = loc
        self.surfaceUp = pygame.image.load(up) # used for drawing button image
        self.surfaceDown = pygame.image.load(down) # used for drawing button image
        self.callBack = callBack

        # Get the rect of the button (used to see if mouse is over the button)
        self.rect = self.surfaceUp.get_rect()
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]

        self.state = SimpleButton.STATE_IDLE # initiate in idle state

    def handleEvent(self, eventObj):
        # Whenever the main program detects an event, it calls the handleEvent() method
        # This method will return True if user clicks the button.
        # Normally returns False.

        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            # The button only cares about mouse-related events, anything else considered "non-event"
            return False

        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos) # Boolean check of event and button locations
                                                                      # True if mouse in button rect

        if self.state == SimpleButton.STATE_IDLE: # if idle, check to change state
            if (eventObj.type == MOUSEBUTTONDOWN) and eventPointInButtonRect: # mouse click in button rect
                self.state = SimpleButton.STATE_ARMED # arm button for action
        
        elif self.state == SimpleButton.STATE_ARMED: # if armed, check to change state
            if (eventObj.type == MOUSEBUTTONUP) and eventPointInButtonRect: # mouse released (clicked) in button rect
                self.state = SimpleButton.STATE_IDLE # return to idle state, but also return True
                # If a callback was specified, call it back
                if self.callBack != None:
                    self.callBack()
                return True # clicked!

            if (eventObj.type == MOUSEMOTION) and (not eventPointInButtonRect): # mouse down but moving off button rect
                self.state = SimpleButton.STATE_DISARMED # primed but won't take action

        elif self.state == SimpleButton.STATE_DISARMED: # if disarmed, check to change state
            if eventPointInButtonRect: # mouse returns to button rect location
                self.state = SimpleButton.STATE_ARMED # arm button for action
            elif eventObj.type == MOUSEBUTTONUP: # mouse released (clicked) outside button rect
                self.state = SimpleButton.STATE_IDLE # return to idle state, send nothing

        return False

    def draw(self):
        # Draw the button's current appearance to the window
        if self.state == SimpleButton.STATE_ARMED: # button is down, mouse over button
            self.window.blit(self.surfaceDown, self.loc) # draw surface down image at button location

        else: # IDLE or DISARMED
            self.window.blit(self.surfaceUp, self.loc) # draw surface up image at button location