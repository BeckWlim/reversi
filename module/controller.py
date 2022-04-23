from tkinter.ttk import Label
import time
import pygame
from pygame import MOUSEBUTTONDOWN


class Button(object):
    def __init__(self, id, text, event, rect, surface):
        self.surface = surface
        self.id = id
        self.event = event
        self.rect = rect
        self.buttonFont = pygame.font.SysFont("arial", 20)
        self.nohover = (255, 255, 255)
        self.hover = (135, 206, 250)
        self.background = self.nohover
        self.text = self.buttonFont.render(text, True, (0, 0, 0))

    def render(self, surface):
        self.surface = surface
        pygame.draw.rect(surface, self.background, self.rect,  0, 5)
        surface.blit(self.text, (self.rect[0] + self.rect[2]/2 - self.text.get_width()/2, self.rect[1] + self.rect[3]/2 - self.text.get_height()/2))

    def isOver(self, point):
        result = False
        if(point[0] >= self.rect[0] and point[0] <self.rect[0] + self.rect[2] and point[1] >= self.rect[1] and point[1] < self.rect[1] + self.rect[3]):
            self.background = self.hover
            result = True
        else:
            self.background = self.nohover
            result = False
        return result

    def isClick(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.isOver(event.pos):
                ev = pygame.event.Event(self.event)
                pygame.event.post(ev)

    def update(self, point):
        self.isOver(point)
        self.render(self.surface)


class Terminal(object):
    def __init__(self, id, rect, surface):
        self.id = id
        self.rect = rect
        self.surface = surface
        self.background = (255, 255, 255)
        self.font = pygame.font.SysFont("arial", 16)
        self.messageList = []

    def update(self):
        pygame.draw.rect(self.surface, self.background, self.rect, 0, 10)
        showText = self.messageList[int(-self.rect[3]/self.font.get_height()):]
        y = self.rect[3] - self.font.get_height()
        for text in reversed(showText):
            self.surface.blit(self.font.render(text, True, (0, 0, 0)), (self.rect[0], self.rect[1] + y))
            y-=self.font.get_height()

    def insert(self, msg):
        self.messageList.append(msg)

class gameTimer(object):
    def __init__(self):
        self.timeStart = 0
        self.timeEnd = 0
        self.time = 0

    def startTimer(self):
        self.timeStart = round(time.time(), 3)

    def endTimer(self):
        self.timeEnd = round(time.time(), 3)
        return round(self.timeEnd - self.timeStart, 3)

