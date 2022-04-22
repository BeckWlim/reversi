# 记住上面这行是必须的，而且保存文件的编码要一致！
import pygame
from pygame import *
from module.controller import Button
from module.controller import Terminal
from module.engine import ChessEngine


class MainWindow(object):
    def __init__(self):
        pygame.init()
        # 初始化pygame,为使用硬件做准备
        self.screenWidth = 768
        self.screenHeight = 512
        self.chessboardWidth = 400
        self.chessboardHeight = 400
        self.chessboardBaseX = 50
        self.chessboardBaseY = 50

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
        # 创建了一个窗口
        pygame.display.set_caption("Reversi")
        # 设置窗口标题

        background = pygame.image.load("image/background.jpg").convert()
        self.background = pygame.transform.scale(background, (self.screenWidth, self.screenHeight))
        chessboard = pygame.image.load("image/chessboard.jpeg").convert()
        self.chessboard = pygame.transform.scale(chessboard, (450, 450))

        blackChess = pygame.image.load("image/blackChess.png").convert_alpha()
        self.blackChess = pygame.transform.scale(blackChess, (40, 40))

        whiteChess = pygame.image.load("image/whiteChess.png").convert_alpha()
        self.whiteChess = pygame.transform.scale(whiteChess, (40, 40))

        mouse_cursor = pygame.image.load("image/fugu.png").convert_alpha()
        self.mouse_cursor = pygame.transform.scale(mouse_cursor, (40, 40))
        pygame.key.set_repeat(10, 15)
        self.convertList = []

    def render(self):
        chessFlag = True
        chessList = []
        gameFont = pygame.font.SysFont("simsunnsimsun", 40)
        textTitle = gameFont.render("Reversi", True, (0, 0, 0))
        buttonList = {}
        buttonList['start'] = Button(0, "Start", 0, (480, 100, 80, 40), self.screen)
        buttonList['reset'] = Button(1, "Reset", 1, (580, 100, 80, 40), self.screen)
        buttonList['pause'] = Button(2, "Pause", 2, (680, 100, 80, 40), self.screen)
        terminal = Terminal(3, (480, 200, 250, 200), self.screen)
        chessEngine = ChessEngine()
        chessEngine.setSurface(self.screen)
        fcclock = pygame.time.Clock()
        gameFlag = False
        while True:
            if(chessFlag): # 换手
                chess = self.blackChess
            else:
                chess = self.whiteChess
            for event in pygame.event.get():
                for button in buttonList.values():
                    button.isClick(event)
                if event.type == QUIT:
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if (x >= self.chessboardBaseX and x <= self.chessboardBaseX + self.chessboardWidth
                            and y >= self.chessboardBaseY and y <= self.chessboardBaseY + self.chessboardHeight):
                        # 棋盘区域内点击事件
                        x = x - self.chessboardBaseX
                        y = y - self.chessboardBaseY
                        indexX = int(x/50)
                        indexY = int(y/50)
                        if(chessList.count((True, indexX, indexY))==0 and chessList.count((False, indexX, indexY))==0 and gameFlag):
                            chessList.append((chessFlag, indexX, indexY))
                            chessList, count, self.convertList = chessEngine.convert((chessFlag, indexX, indexY), chessList, [])
                            # 无冲突 落子
                            # print(chessList)
                            if count > 0:
                                if chessFlag:
                                    name = "Black"
                                else:
                                    name = "White"
                                terminal.insert(name + ": " + str((indexX, indexY)))
                                chessFlag = not chessFlag
                            else:
                                # 没有实现翻转 无效落子
                                chessList.remove((chessFlag, indexX, indexY))
                if event.type == 0:
                    terminal.insert("game start")
                    chessList.append((True, 3, 3))
                    chessList.append((False, 3, 4))
                    chessList.append((False, 4, 3))
                    chessList.append((True, 4, 4))
                    gameFlag = True
                if event.type == 1:
                    terminal.insert("game reset")
                    chessList.clear()
                    gameFlag = False

            x, y = pygame.mouse.get_pos()
            x -= self.blackChess.get_width()/2
            y -= self.blackChess.get_height()/2
            self.screen.blit(self.background, (0, 0))
            # self.screen.blit(self.chessboard, (self.chessboardBaseX, self.chessboardBaseY))
            self.drawChessBoard()
            if(x >= self.chessboardBaseX and x <= self.chessboardBaseX + self.chessboardWidth
            and y >= self.chessboardBaseY and y <= self.chessboardBaseY + self.chessboardHeight):
                self.screen.blit(chess, (x, y))
                x = x - self.chessboardBaseX
                y = y - self.chessboardBaseY
                indexX = int(x / 50)
                indexY = int(y / 50) #绘制落子提示框
                pygame.draw.rect(self.screen, (255, 255, 0), (indexX * 50 + self.chessboardBaseX, indexY * 50 + self.chessboardBaseY, 50, 50), 2)
            for convert in self.convertList:
                pygame.draw.rect(self.screen, (0, 0, 255), (convert[1] * 50 + self.chessboardBaseX, convert[2] * 50 + self.chessboardBaseY, 50, 50))
            for temp in chessList:
                if(temp[0]):
                    self.screen.blit(self.blackChess, (temp[1]*50 + self.chessboardBaseX + 5, temp[2]*50 + self.chessboardBaseY + 6))
                else:
                    self.screen.blit(self.whiteChess, (temp[1]*50 + self.chessboardBaseX + 5, temp[2]*50 + self.chessboardBaseY + 5))
            self.screen.blit(textTitle, (550, 50))
            for button in buttonList.values():
                button.update(pygame.mouse.get_pos())
            terminal.update()
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

