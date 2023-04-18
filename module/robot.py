import random
import copy
from module.engine import ChessEngine
import math


class miniAlphaGo(object):
    cParam = 2

    def __init__(self):
        self.chessFlag = False
        self.simuEngine = ChessEngine()
        self.simuEngine.chessFlag = self.chessFlag
        self.chessList = []

    def setChessFlag(self, flag):
        self.chessFlag = flag
        self.simuEngine.chessFlag = flag

    def analyse(self, chessList):
        # 载入棋局
        self.chessList = copy.deepcopy(chessList)
        head = MCTSNode()
        head.chessFlag = self.chessFlag
        # self.simuEngine.setSandBoxParam(chessList, self.chessFlag)
        for i in range(64):
            self.simuEngine.setSandBoxParam(copy.deepcopy(chessList), self.chessFlag)
            self.MCTSSearch(head.num, head)
        nextNode = None
        if len(head.childList) == 0:
            print("!!!!!!!!!!!")
            return None
        for temp in head.childList:
            tempParam = temp.award/temp.num + self.cParam * math.sqrt(math.log(head.num)/temp.num)
            if nextNode == None:  # 尚未选取待选择节点
                compareParam = tempParam
                nextNode = temp
            else:
                if tempParam > compareParam:
                    compareParam  = tempParam
                    nextNode = temp
        return nextNode.chess

    def MCTSSearch(self, domainNum, node):
        flag = self.simuEngine.chessFlag
        compareParam = None
        nextNode = None
        if node.result is True:
            return node.award
        if node.award == None:  # 未扩展
            # 随机模拟
            if self.nodeExpand(node) == 0:
                # 到达终局
                result = self.simuEngine.result()
                if result[0] > result[1]:
                    simuAward = 30
                elif result[0] == result[1]:
                    simuAward = 0
                else:
                    simuAward = -30
                if self.chessFlag == True:
                    node.award = -simuAward
                else:
                    node.award = simuAward
                node.num += 1
                node.result = True
            # 沙盘模拟32步
            result = self.simuEngine.simulation(32)
            # 检索棋局中的关键点
            corner = self.searchCorner(self.simuEngine.chessList)
            if result[0] > result[1]:
                simuAward = 4 + corner
            elif result[0] == result[1]:
                simuAward = 0 + corner
            else:
                simuAward = -4 + corner

            if flag == True:
                node.award = -simuAward
            else:
                node.award = simuAward
            # 扩展待选空结点
            node.num += 1

            return simuAward
        for temp in node.childList:
            if temp.award == None:  # 存在未扩展子节点
                nextNode = temp
                break
            tempParam = temp.award/temp.num + self.cParam * math.sqrt(math.log(domainNum)/temp.num)
            if nextNode == None:  # 尚未选取待选择节点
                compareParam = tempParam
                nextNode = temp
            else:
                if tempParam > compareParam:
                    compareParam  = tempParam
                    nextNode = temp
        # 沙盘中插入节点
        self.simuEngine.dropChess(nextNode.chess)
        increment = self.MCTSSearch(domainNum, nextNode)
        # 更新当前节点
        if flag:
            node.award -= increment
        else:
            node.award += increment
        node.num += 1
        return increment

    def nodeExpand(self, node):
        chessPool = self.searchBlank(self.simuEngine.chessList, self.simuEngine.chessFlag)
        if len(chessPool) == 0:
            node.result = True

        for chess in chessPool:
            temp = MCTSNode()
            temp.chess = chess
            node.addChild(temp)
        return len(chessPool)

    def searchBlank(self, chessList, chessFlag):
        searchPool = []
        dropPool = []  # 可用的落子点
        searchVector = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for chess in chessList:
            # 检索可用棋子
            if chessFlag is chess[0]:
                searchPool.append(chess)
        # 遍历可用落点
        for chess in searchPool:
            flag = not chessFlag
            for index in range(8):
                i = 1
                while chessList.count(
                        (flag, chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1])) > 0 \
                        and chess[1] + i * searchVector[index][0] < 8 and chess[2] + i * searchVector[index][1] < 8 \
                        and chess[1] + i * searchVector[index][0] >= 0 and chess[2] + i * searchVector[index][1] >= 0:
                    i += 1
                if i == 1:
                    continue
                else:
                    if (chessList.count((self.chessFlag, chess[1] + i * searchVector[index][0],
                                              chess[2] + i * searchVector[index][1])) == 0):
                        x = chess[1] + i * searchVector[index][0]
                        y = chess[2] + i * searchVector[index][1]
                        if dropPool.count((x, y)) == 0 and 0 <= x < 8 and 0 <= y < 8:
                            dropPool.append((chess[1] + i * searchVector[index][0], chess[2] + i * searchVector[index][1]))
        return dropPool

    def searchCorner(self, chessList):
        count = 0
        for chess in chessList:
            if chess[0] == True:
                if chess[1] == 0 and chess[2] == 0:
                    count += 1
                if chess[1] == 7 and chess[2] == 7:
                    count += 1
                if chess[1] == 0 and chess[2] == 7:
                    count += 1
                if chess[1] == 7 and chess[2] == 0:
                    count += 1
            if chess[0] == False:
                if chess[1] == 0 and chess[2] == 0:
                    count -= 1
                if chess[1] == 7 and chess[2] == 7:
                    count -= 1
                if chess[1] == 0 and chess[2] == 7:
                    count -= 1
                if chess[1] == 7 and chess[2] == 0:
                    count -= 1
        return count


class MCTSNode(object):
    def __init__(self):
        self.childList = []
        self.award = None
        self.num = 0
        self.chess = None
        self.chessFlag = None
        self.result = False


    def setData(self, map):
        self.chess = map

    def addChild(self, child):
        self.childList.append(child)

    def setAward(self, award):
        self.award = award


if __name__ == "__main__":
    for i in range(10):
        print(random.randint(0, 1))

