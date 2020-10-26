import numpy as np;

#
#   0 일때 아무것도 없음
#   1 일때 흑돌
#   2 일때 백돌
#

class Omok:
    def __init__(self, boardLength):
        self.boardWidth = boardLength
        self.boardHeight = boardLength
        self.boardSize = self.boardWidth * self.boardHeight
        self.boardNumpy = np.zeros((self.boardSize), dtype=np.float)

    def getStone(self, x, y):
        if (x >= 0 and x < self.boardWidth and y >= 0 and y < self.boardHeight):
            return self.boardNumpy[y*self.boardHeight+x]
        else:
            return 0

    def getReward(self, x, y): # 주변에 돌이 있는지 판독 (돌이 많을수록 0.05점씩 추가)
        reward = 0

        if self.getStone(x, y-1) != 0:
            reward += 1
        if self.getStone(x+1, y-1) != 0:
            reward += 1
        if self.getStone(x+1, y) != 0:
            reward += 1
        if self.getStone(x+1, y+1) != 0:
            reward += 1
        if self.getStone(x, y+1) != 0:
            reward += 1
        if self.getStone(x-1, y+1) != 0:
            reward += 1
        if self.getStone(x-1, y) != 0:
            reward += 1
        if self.getStone(x-1, y-1) != 0:
            reward += 1

        return reward

    def setStone(self, x, y, stone):
        get = self.getStone(x, y)

        if (get == 0):
            self.boardNumpy[x+y*self.boardWidth] = stone
            
            reward = 0

            endres, _ = self.checkIsEnd()

            if (endres):
                reward += 20

            reward += self.getReward(x, y)

            return True, reward
        else:
            return False, 0

    def checkIsEnd(self):
        empty = False

        for xx in range(0, self.boardWidth):
            for yy in range(0, self.boardHeight):
                for stoneRaw in range(2):
                    stone = stoneRaw + 1
                    if (empty == False):
                        if (self.getStone(xx, yy) == 0):
                            empty = True

                    #가로 확인
                    if ((self.getStone(xx, yy) == stone) and
                        (self.getStone(xx-1, yy) == stone) and
                        (self.getStone(xx-2, yy) == stone) and
                        (self.getStone(xx-3, yy) == stone) and
                        (self.getStone(xx-4, yy) == stone)):
                        return (True, stone)

                    #세로 확인
                    if ((self.getStone(xx, yy) == stone) and
                        (self.getStone(xx, yy-1) == stone) and
                        (self.getStone(xx, yy-2) == stone) and
                        (self.getStone(xx, yy-3) == stone) and
                        (self.getStone(xx, yy-4) == stone)):
                        return (True, stone)

                    #대각선 확인 1
                    if ((self.getStone(xx, yy) == stone) and
                        (self.getStone(xx-1, yy-1) == stone) and
                        (self.getStone(xx-2, yy-2) == stone) and
                        (self.getStone(xx-3, yy-3) == stone) and
                        (self.getStone(xx-4, yy-4) == stone)):
                        return (True, stone)

                    #대각선 확인 2
                    if ((self.getStone(xx, yy) == stone) and
                        (self.getStone(xx-1, yy+1) == stone) and
                        (self.getStone(xx-2, yy+2) == stone) and
                        (self.getStone(xx-3, yy+3) == stone) and
                        (self.getStone(xx-4, yy+4) == stone)):
                        return (True, stone)
        if (empty):
            return (False, 0)
        else:
            return (True, 3)

    def showBoard(self):
        scence = ""

        for yy in range(self.boardHeight):
            for xx in range(self.boardWidth):
                stone = self.getStone(xx, yy)

                if (stone == 0):
                    if (xx == 0):
                        if (yy == 0):
                            scence += "┌ "
                        elif (yy == self.boardHeight - 1):
                            scence += "└ "
                        else:
                            scence += "├ "
                    elif (xx == self.boardWidth - 1):
                        if (yy == 0):
                            scence += "┐ "
                        elif (yy == self.boardHeight - 1):
                            scence += "┘ "
                        else:
                            scence += "┤ "
                    else:
                        if (yy == 0):
                            scence += "┬ "
                        elif (yy == self.boardHeight - 1):
                            scence += "┴ "
                        else:
                            scence += "┼ "
                elif (stone == 1):
                    scence += "○"
                elif (stone == 2):
                    scence += "●"
            scence += "\n"
        
        print(scence)

    def getProhibit(self):
        prohibit = np.zeros((self.boardSize), dtype=np.float)

        for xx in range(self.boardWidth):
            for yy in range(self.boardHeight):
                prohibit[xx+yy*self.boardWidth] = (self.getStone(xx, yy) > 0) * 1

        return prohibit

    def getInverseBoard(self):
        board = np.zeros((self.boardSize), dtype=np.float)

        for xx in range(self.boardWidth):
            for yy in range(self.boardHeight):
                index = xx+yy*self.boardWidth
                if (self.boardNumpy[index] == 1):
                    board[index] = 2
                elif (self.boardNumpy[index] == 2):
                    board[index] =1 

        return board

    def getBoard(self):
        return self.boardNumpy

class Replay:
    def __init__(self, boardLength):
        self.boardWidth = boardLength
        self.boardHeight = boardLength
        self.boardSize = self.boardWidth * self.boardHeight
        self.boardNumpyHistory = np.zeros((0, self.boardSize))
        self.rewardData = np.zeros((0))

    def addBoard(self, board, reward):
        self.boardNumpyHistory = np.vstack([self.boardNumpyHistory, board])
        self.rewardData = np.append(self.rewardData, reward)

    def getBatch(self):
        return self.boardNumpyHistory

    def getRewardBatch(self):
        return self.rewardData

def Inverse(origin):
    originShape = origin.shape
    board = np.zeros(origin.shape, dtype=np.float)

    for index in range(board.shape[0]):
            if (origin[index] == 1):
                board[index] = 2
            elif (origin[index] == 2):
                board[index] =1 

    return board