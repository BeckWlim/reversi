
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

    def setSurface(self, surface):
        self.screen = surface

    def convert(self, chess, chessList, convertList):
        convertPool = []
        convertPool += convertList
        flag = not chess[0]
        count = 0
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        self.chessList = chessList
        for index in range(8):
            i = 1
            while(chessList.count((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) and chess[1] + i * searchVector[index][0] < 7 and chess[2] + i * searchVector[index][1] < 7
            and chess[1] + i * searchVector[index][0] > 0 and chess[2] + i * searchVector[index][1] > 0):
                # print((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
                i += 1
            if i == 1:
                continue
            # print(i)
            if(chessList.count((chess[0], chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))):
                # print((chess[0], chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
                for j in range(1, i):
                    count += 1
                    if(self.chessList.count((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))):
                        self.chessList.remove((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))
                    convertChess = (chess[0], chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1])
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (convertChess[1] * 50 + self.chessboardBaseX, convertChess[2] * 50 + self.chessboardBaseY, 50, 50),
                                     2)
                    self.chessList.append(convertChess)
                    convertPool.append(convertChess)
                    print(convertPool)
                    # print(chessList)
                    # print(convertChess)
                    self.chessList, temp, tempPool = self.convert(convertChess, self.chessList, convertPool)
                    count += temp
                    convertPool = tempPool
        return self.chessList, count, convertPool



