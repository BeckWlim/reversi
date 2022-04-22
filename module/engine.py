
import pygame


class ChessEngine(object):
    def __init__(self):
        self.screen = None
        self.screenWidth = 768
        self.screenHeight = 512
        self.chessboardWidth = 400
        self.chessboardHeight = 400
        self.chessboardBaseX = 50
        self.chessboardBaseY = 50
        self.chessList = []

    def setSurface(self, surface):
        self.screen = surface

    def convert(self, chess, chessList, convertList):
        flag = not chess[0]
        count = 0
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for index in range(8):
            i = 1
            while(chessList.count((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) and chess[1] + i * searchVector[index][0] < 8 and chess[2] + i * searchVector[index][1] < 8
            and chess[1] + i * searchVector[index][0] >= 0 and chess[2] + i * searchVector[index][1] >= 0):
                # print((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
                i += 1
            if i == 1:
                continue
            # print(i)
            if(chessList.count((chess[0], chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))):
                # print((chess[0], chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
                for j in range(1, i):
                    count += 1
                    if(chessList.count((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))):
                        chessList.remove((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))
                    convertChess = (chess[0], chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1])
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (convertChess[1] * 50 + self.chessboardBaseX, convertChess[2] * 50 + self.chessboardBaseY, 50, 50),
                                     2)
                    chessList.append(convertChess)
                    convertList.append(convertChess)
                    # print(convertList)
                    # print(chessList)
                    # print(convertChess)
                    temp = self.convert(convertChess, chessList, convertList)
                    count += temp
        return count

    def searchFiled(self, chessFlag, chessList):
        searchPool = []
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        count = 0
        for chess in chessList:
            # 检索可用棋子
            if chessFlag is chess[0]:
                searchPool.append(chess)
        # 遍历可用落子点
        for chess in searchPool:
            flag = not chessFlag
            for index in range(8):
                i = 1
                while (chessList.count(
                        (flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) and chess[
                           1] + i * searchVector[index][0] < 8 and chess[2] + i * searchVector[index][1] < 8
                       and chess[1] + i * searchVector[index][0] > 0 and chess[2] + i * searchVector[index][1] > 0):
                    # print((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
                    i += 1
                if i == 1:
                    continue
                else:
                    if(chessList.count((chessFlag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))==0):
                        count += 1
        return count

    def result(self, chessList):
        blackCounter = 0
        whiteCounter = 0
        for chess in chessList:
            # 检索可用棋子
            if True is chess[0]:
                blackCounter += 1
            else:
                whiteCounter += 1
        return blackCounter, whiteCounter




