# Scene A

import pygwidgets
import pyghelpers
import pygame
from pygame.locals import *
from Constants import *

class SceneA(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window

        self.messageField = pygwidgets.DisplayText(self.window,
                            (15, 25), SCENE_A_MSG, fontSize=50,
                            textColor=WHITE, width=610, justified='center')

        self.gotoAButton = pygwidgets.TextButton(self.window,
                                    (100, 100), GO_SCENE_A_MSG)
        self.gotoBButton = pygwidgets.TextButton(self.window,
                                    (250, 100), GO_SCENE_B_MSG)
        self.gotoCButton = pygwidgets.TextButton(self.window,
                                    (400, 100), GO_SCENE_C_MSG)
        self.gotoAButton.disable()

    def getSceneKey(self):
        return SCENE_A

    def handleInputs(self, eventsList, keysDownList):
        for event in eventsList:
            if self.gotoBButton.handleEvent(event):
                self.goToScene(SCENE_B)
            if self.gotoCButton.handleEvent(event):
                self.goToScene(SCENE_C)

            # Testing:  Press b or c to send message to those scenes
            #           Press or 2 or 3 to get data from B and C
            #           Press x to send message to all scenes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.send(SCENE_B, SEND_MESSAGE, SEND_SCENE_B_MSG)

                if event.key == pygame.K_c:
                    self.send(SCENE_C, SEND_MESSAGE, SEND_SCENE_C_MSG)

                if event.key == pygame.K_2:
                    answer = self.request(SCENE_B, GET_DATA)
                    print(RCV_SCENE_B_MSG)
                    print(ANSWER_TEXT, answer)

                if event.key == pygame.K_3:
                    answer = self.request(SCENE_C, GET_DATA)
                    print(RCV_SCENE_C_MSG)
                    print(ANSWER_TEXT, answer)

                if event.key == pygame.K_x:
                    self.sendAll(SEND_MESSAGE, SEND_ALL_SCENE_MSG)

    def draw(self):
        self.window.fill(GRAYA)
        self.messageField.draw()
        self.gotoAButton.draw()
        self.gotoBButton.draw()
        self.gotoCButton.draw()

    def receive(self, receiveID, data):
        print('In A')
        print(RCV_MSG_TYPE_TEXT, receiveID)
        print(DATA_RCV_TEXT, data)

    def respond(self, requestID):
        if requestID == GET_DATA:
            return 'Here is data from scene A'