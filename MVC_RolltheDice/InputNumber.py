# InputNumber class - allows the user to enter only numbers

import pygame
from pygame.locals import *
import pygwidgets
from Constants import *

# Tuple of legal editing keys
LEGAL_KEYS_TUPLE = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END,
                   pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_KP_ENTER)

# Legal keys to be typed
LEGAL_UNICODE_CHARS = ('0123456789.-')

# InputNumber inherits from InputText
class InputNumber(pygwidgets.InputText):
    def __init__(self, window, loc, value='', fontName=None, fontSize=24, width=200,
                 textColor=BLACK, backgroundColor=WHITE, focusColor=BLACK,
                 initialFocus=False, nickName=None, callback=None, mask=None,
                 keepFocusOnSubmit=False, allowFloatingNumber=True,
                 allowNegativeNumber=True):
        self.allowFloatingNumber=allowFloatingNumber
        self.allowNegativeNumber=allowNegativeNumber

        # Call the __init__ method of our base class
        super().__init__(window, loc, value, fontName, fontSize, width, textColor,
                         backgroundColor, focusColor, initialFocus, nickName, callback,
                         mask, keepFocusOnSubmit)

    # Override handleEvent so we can filter for proper keys
    def handleEvent(self, event):
        if (event.type is pygame.KEYDOWN):
            # If it's not an editing or numeric key ignore it
            # Unicode value is only present on key down
            allowableKey = ((event.key in LEGAL_KEYS_TUPLE) or
                            (event.unicode in LEGAL_UNICODE_CHARS))
            if not allowableKey:
                return False

            # Unicode chars include '-' and '.' so need to add checks
            # and custom rules to handle these keys
            if event.unicode is '-': # user typed a minus sign
                # check to see if allowing negatives
                if not self.allowNegativeNumber:
                    # If no negatives, don't pass it through
                    return False
                if self.cursorPosition > 0:
                    return False # can't put minus sign after 1st char
                if '-' in self.text:
                    return False # can't enter a second minus sign

            if event.unicode is '.':
                if not self.allowFloatingNumber:
                    # If no floats, don't pass the period through
                    return False
                if '.' in self.text:
                    return False # can't enter a second period
                
            
        # Allow the key to go through to the base class
        result = super().handleEvent(event)
        return result

    def getValue(self):
        userString = super().getValue()
        try:
            if self.allowFloatingNumber:
                returnValue = float(userString)
            else:
                returnValue = int(userString)
        except ValueError:
            raise ValueError('Entry is not a number, needs to have at least one digit.')

        return returnValue