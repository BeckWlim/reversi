# 记住上面这行是必须的，而且保存文件的编码要一致！
import pygame
import copy
from pygame import *
from module.controller import Button
from module.controller import Terminal
from module.controller import gameTimer
from module.engine import ChessEngine
from module.robot import miniAlphaGo
import os
import sys



class MainWindow(object):
    SIGNAL_START = 0
    SIGNAL_RESET = 1
    SIGNAL_PAUSE = 2
    def __init__(self):
        pygame.init()
        # 初始化pygame,为使用硬件做准备
        self.screenWidth = 768
        self.screenHeight = 512
        self.chessboardWidth = 400
        self.chessboardHeight = 400
        self.chessboardBaseX = 50
        self.chessboardBaseY = 50
        self.gameTimer = gameTimer()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
        # 创建了一个窗口
        pygame.display.set_caption("Reversi")
        # 设置窗口标题

        background = pygame.image.load(os.getcwd() + "/image/background.jpg").convert()
        self.background = pygame.transform.scale(background, (self.screenWidth, self.screenHeight))
        chessboard = pygame.image.load(os.getcwd() + "/image/chessboard.jpeg").convert()
        self.chessboard = pygame.transform.scale(chessboard, (450, 450))

        blackChess = pygame.image.load(os.getcwd() + "/image/blackChess.png").convert_alpha()
        self.blackChess = pygame.transform.scale(blackChess, (40, 40))

        whiteChess = pygame.image.load(os.getcwd() + "/image/whiteChess.png").convert_alpha()
        self.whiteChess = pygame.transform.scale(whiteChess, (40, 40))

        pygame.key.set_repeat(10, 15)
        self.chessEngine = ChessEngine()
        self.buttonList = {}
        self.gameFlag = False
        self.terminal = None
        self.alpha = miniAlphaGo()

    def render(self):
        gameFont = pygame.font.SysFont("simsunnsimsun", 40)
        textTitle = gameFont.render("Reversi", True, (0, 0, 0))
        self.buttonList['start'] = Button(0, "Start", self.SIGNAL_START, (480, 100, 80, 40), self.screen)
        self.buttonList['reset'] = Button(1, "Reset", self.SIGNAL_RESET, (580, 100, 80, 40), self.screen)
        self.buttonList['pause'] = Button(2, "Pause", self.SIGNAL_PAUSE, (680, 100, 80, 40), self.screen)
        self.terminal = Terminal(3, (480, 200, 250, 200), self.screen)

        self.chessEngine.setSurface(self.screen)
        fcclock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                for button in self.buttonList.values():
                    button.isClick(event)
                if event.type == QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    # 判断是否为本地操作
                    if self.chessEngine.player[self.chessEngine.chessFlag] == self.chessEngine.PLAYER_LOCAL:
                       self.localOption()

                if event.type == self.SIGNAL_START:
                    self.terminal.insert("game start")
                    self.chessEngine.start()
                    self.gameFlag = True
                    self.alpha.chessFlag = False
                    # print((self.chessEngine.simulation(32)))
                    self.chessEngine.nextStep()
                    self.gameTimer.startTimer()
                if event.type == self.SIGNAL_RESET:
                    self.terminal.insert("game reset")
                    self.chessEngine.reset()
                    self.gameFlag = False
                if event.type == self.chessEngine.GAME_NEXTSTEP:
                    self.gameTimer.startTimer()
                    if self.chessEngine.player[self.chessEngine.chessFlag] == self.chessEngine.PLAYER_AI:
                        # 下一回合为AI
                        self.terminal.messageList += self.chessEngine.dropChess(self.alpha.analyse(copy.deepcopy(self.chessEngine.chessList)))
                        self.terminal.insert("AI time:" + str(self.gameTimer.endTimer()))
            self.screen.blit(self.background, (0, 0))
            self.gameDrawer()
            self.screen.blit(textTitle, (550, 50))
            for button in self.buttonList.values():
                button.update(pygame.mouse.get_pos())
            self.terminal.update()
            # 刷新控制台
            pygame.display.update()
            fcclock.tick(60)

    def drawChessBoard(self):
        chessboardColor = (246, 203, 144)
        black = (0, 0, 0)
        pygame.draw.rect(self.screen, chessboardColor, (self.chessboardBaseX, self.chessboardBaseY, self.chessboardWidth, self.chessboardHeight), 0)
        for i in range(0, 9):
            pygame.draw.line(self.screen, black, (self.chessboardBaseX, self.chessboardBaseY + i*50), (self.chessboardBaseX + self.chessboardWidth, self.chessboardBaseY + i*50), 2)
            pygame.draw.line(self.screen, black, (self.chessboardBaseX + i*50, self.chessboardBaseY), (self.chessboardBaseX + i*50, self.chessboardBaseY+self.chessboardHeight), 2)

    def gameDrawer(self):
        if (self.chessEngine.chessFlag):
            # 选择预置棋子
            chess = self.blackChess
        else:
            chess = self.whiteChess
        x, y = pygame.mouse.get_pos()
        x -= self.blackChess.get_width() / 2
        y -= self.blackChess.get_height() / 2
        # self.screen.blit(self.chessboard, (self.chessboardBaseX, self.chessboardBaseY))
        self.drawChessBoard()
        for convert in self.chessEngine.convertList:
            pygame.draw.rect(self.screen, (0, 0, 255),
                             (convert[1] * 50 + self.chessboardBaseX, convert[2] * 50 + self.chessboardBaseY, 50, 50))
        for temp in self.chessEngine.dropPool:
            # 可用落子点
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (temp[0] * 50 + self.chessboardBaseX, temp[1] * 50 + self.chessboardBaseY, 50, 50), 2)
        for temp in self.chessEngine.chessList:
            # 打印棋盘上存在的棋子
            if (temp[0]):
                self.screen.blit(self.blackChess,
                                 (temp[1] * 50 + self.chessboardBaseX + 5, temp[2] * 50 + self.chessboardBaseY + 6))
            else:
                self.screen.blit(self.whiteChess,
                                 (temp[1] * 50 + self.chessboardBaseX + 5, temp[2] * 50 + self.chessboardBaseY + 5))
        if (self.chessboardBaseX <= x <= self.chessboardBaseX + self.chessboardWidth
                and self.chessboardBaseY <= y <= self.chessboardBaseY + self.chessboardHeight) \
                and self.chessEngine.player[self.chessEngine.chessFlag] == self.chessEngine.PLAYER_LOCAL:  # 当前为本地操作回合
            self.screen.blit(chess, (x, y))
            x = x - self.chessboardBaseX
            y = y - self.chessboardBaseY
            indexX = int(x / 50)
            indexY = int(y / 50)  # 绘制落子提示框
            pygame.draw.rect(self.screen, (255, 255, 0),
                             (indexX * 50 + self.chessboardBaseX, indexY * 50 + self.chessboardBaseY, 50, 50), 2)

    def localOption(self):
        x, y = pygame.mouse.get_pos()
        if (x >= self.chessboardBaseX and x <= self.chessboardBaseX + self.chessboardWidth
                and y >= self.chessboardBaseY and y <= self.chessboardBaseY + self.chessboardHeight):
            # 棋盘区域内点击事件
            x = x - self.chessboardBaseX
            y = y - self.chessboardBaseY
            indexX = int(x / 50)
            indexY = int(y / 50)
            if (self.gameFlag == True):
                self.terminal.messageList += self.chessEngine.dropChess((indexX, indexY))
                self.terminal.insert("local time:" + str(self.gameTimer.endTimer()))




