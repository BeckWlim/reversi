import random
import pygame


class ChessEngine(object):
    PLAYER_AI = 0
    PLAYER_LOCAL = 1
    PLAYER_NET = 2
    GAME_NEXTSTEP = 11

    def __init__(self):
        self.screen = None
        self.chessList = []
        self.convertList = []
        self.dropPool = []
        self.chessFlag = True
        self.player = {True: self.PLAYER_LOCAL, False: self.PLAYER_AI}

    def setSurface(self, surface):
        self.screen = surface

    def convert(self, chess):
        flag = not chess[0]
        count = 0
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for index in range(8):
            i = 1
            while(self.chessList.count((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) and chess[1] + i * searchVector[index][0] < 8 and chess[2] + i * searchVector[index][1] < 8
            and chess[1] + i * searchVector[index][0] >= 0 and chess[2] + i * searchVector[index][1] >= 0):
                i += 1
            if i == 1:
                continue
            if(self.chessList.count((chess[0], chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) > 0):
                #出现被围困的对手棋
                for j in range(1, i):
                    count += 1
                    if(self.chessList.count((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1])) > 0):
                        self.chessList.remove((flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))
                        self.chessList.append((not flag, chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1]))
                    convertChess = (chess[0], chess[1] + j * searchVector[index][0], chess[2] + j * searchVector[index][1])
                    if(self.convertList.count(convertChess)==0):
                        # 添加翻转标记
                        self.convertList.append(convertChess)
                    # 递归翻转
                    self.convert(convertChess)
        return len(self.convertList)

    def searchFiled(self, chessFlag):
        searchPool = []
        self.dropPool = [] # 可用的落子点
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for chess in self.chessList:
            # 检索可用棋子
            if chessFlag is chess[0]:
                searchPool.append(chess)
        # 遍历可用落点
        for chess in searchPool:
            flag = not chessFlag
            for index in range(8):
                i = 1
                while self.chessList.count((flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) > 0 \
                        and chess[1] + i * searchVector[index][0] < 8 and chess[2] + i * searchVector[index][1] < 8 \
                        and chess[1] + i * searchVector[index][0] >= 0 and chess[2] + i * searchVector[index][1] >= 0:
                    i += 1
                if i == 1:
                    continue
                else:
                    if(self.chessList.count((chessFlag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))==0):
                        x=chess[1] + i * searchVector[index][0]
                        y=chess[2] + i * searchVector[index][1]
                        if self.dropPool.count((x, y))==0 and 0 <= x < 8 and 0 <= y < 8:
                            self.dropPool.append((chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
        return len(self.dropPool)

    def dropChess(self, position):
        message = []
        if (self.chessList.count((True, position[0], position[1])) == 0 and self.chessList.count(
                (False, position[0], position[1])) == 0):
            self.chessList.append((self.chessFlag, position[0], position[1]))
            self.convertList = []
            count = self.convert((self.chessFlag, position[0], position[1]))
            # 无冲突 落子 执行翻转
            # print(chessList)

            if count > 0:
                # 成功翻转
                if self.chessFlag:
                    name = "Black"
                else:
                    name = "White"
                message.append(name + ": " + str(position))
                # 获取对手的可用落点
                count_blank = self.searchFiled(not self.chessFlag)
                # print(count, count_blank)
                if count_blank > 0:
                    # 对手有可用落点 交换
                    self.chessFlag = not self.chessFlag
                    self.nextStep()
                else:
                    if self.searchFiled(self.chessFlag) == 0:
                        # 两方都无可用路径 结束
                        blackCounter, whiteCounter = self.result()
                        message.append("game over" + str((blackCounter, whiteCounter)))
                        if blackCounter > whiteCounter:
                            message.append("black win")
                        elif blackCounter == whiteCounter:
                            message.append("play even")
                        else:
                            message.append("white win")
                    else:
                        self.nextStep()
            else:
                # 没有实现翻转 无效落子
                self.chessList.remove((self.chessFlag, position[0], position[1]))
        return message

    def nextStep(self):
        ev = pygame.event.Event(self.GAME_NEXTSTEP)
        pygame.event.post(ev)

    def result(self):
        blackCounter = 0
        whiteCounter = 0
        for chess in self.chessList:
            # 检索可用棋子
            if True is chess[0]:
                blackCounter += 1
            else:
                whiteCounter += 1
        return blackCounter, whiteCounter

    def start(self):
        self.reset()
        self.chessList.append((True, 3, 3))
        self.chessList.append((False, 3, 4))
        self.chessList.append((False, 4, 3))
        self.chessList.append((True, 4, 4))

    def reset(self):
        self.__init__()

    def simulation(self, num):
        for i in range(num):
            self.searchFiled(self.chessFlag)
            blank = len(self.dropPool)
            if blank == 0:
                break
            index = random.randint(0, blank-1)
            message = self.dropChess(self.dropPool[index])
        return (self.result())

    def setSandBoxParam(self, chessList, chessFlag):
        self.chessList = chessList
        self.chessFlag = chessFlag











