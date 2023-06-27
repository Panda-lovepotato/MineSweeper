import numpy as np
import random

'''
(file):if file != None; load file first
RemakeVariable make a (xLength*yLength*mineNum) minefield
(ruleType):{True:winxp rule, False:win7 rule}
<mineField> have the information of mine distribution
<board> stores page layout information
<status>:{0:new minefield, 1:demining, 2:fail, 3:succeed, -1:fail to load file}
<remainingFlags> stores remain flags
'''
#RemakeVariable, ClickPoint, PlantFlag
#GetBoard, GetStatus, GetRemainingFlags, SaveMineSweeper
class MineSweeper:
    def __init__(self, xLength=30, yLength=16, mineNum=99, ruleType=True, file=None):
        if(file):
            try:
                f = np.load(file+'.npz')
                self.__mineField = f['arr_0']
                self.__board = f['arr_1']
                self.__status, self.__remainingFlags = f['arr_2'][0], f['arr_2'][1]
                self.xLength, self.yLength, self.mineNum = f['arr_2'][2], f['arr_2'][3], f['arr_2'][4]
                self.ruleType = f['arr_3'][0]
            except:
                self.__status = -1
        else:
            self.xLength, self.yLength, self.mineNum, self.ruleType = xLength, yLength, mineNum, ruleType
            self.RemakeVariable()

    #init all variable except (x*y*z*rule)
    def RemakeVariable(self):
        self.__mineField = np.zeros((self.xLength, self.yLength), dtype=bool)
        self.__board = np.zeros((self.xLength, self.yLength), dtype=np.int8)
        self.__board[:, :] = -1
        self.__status = 0
        self.__remainingFlags = self.mineNum

    def ClickPoint(self, x:int, y:int):
        if(self.__board[x, y] == -1 and self.__status == 0):
            self.__InitMineField(x, y)
        if(self.__board[x, y] == -1 and self.__status == 1):
            #check if the point is a mine
            if(self.__mineField[x][y]):
                for i in range(self.xLength):
                    for j in range(self.yLength):
                        if(self.__mineField[i][j]):
                            self.__board[i, j] = -2
                self.__board[x, y] = -3
                self.__status, self.__remainingFlags = 2, 0
            else:
                used = []
                self.__DFS(x, y, used)
                if(np.sum(self.__board == -1)+np.sum(self.__board == 9) == self.mineNum):
                    for i in range(self.xLength):
                        for j in range(self.yLength):
                            if(self.__mineField[i][j]):
                                self.__board[i, j] = 9
                    self.__status = 3
                self.__remainingFlags = self.mineNum - np.sum(self.__board == 9)

    #use it to convert (x, y) in -1 and 9
    def PlantFlag(self, x:int, y:int):
        if(self.__status in (0, 1)):
            if(self.__board[x, y] == -1 and self.__remainingFlags > 0):
                self.__remainingFlags -= 1
                self.__board[x, y] = 9
            elif(self.__board[x, y] == 9):
                self.__remainingFlags += 1
                self.__board[x, y] = -1

    #board:{-3:red mine, -2:black mine, -1:unknown cell, 0~8:mineNum around it, 9:red flag}
    def GetBoard(self) -> np.ndarray:
        return self.__board
    
    #status:{0:new minefield, 1:demining, 2:fail, 3:succeed, -1:fail to load file}
    def GetStatus(self) -> int:
        return self.__status
    
    #remainingflags in the minefield is used
    def GetRemainingFlags(self) -> int:
        return self.__remainingFlags
    
    #if fail, return false; if succeed, return true
    def SaveMineSweeper(self, fileName:str) -> bool:
        intVariable = np.array([self.__status, self.__remainingFlags, self.xLength, self.yLength, self.mineNum])
        boolVariable = np.array([self.ruleType])
        np.savez(fileName+'.npz', self.__mineField, self.__board, intVariable, boolVariable)
        return True

    #obtain the situation around the point. (number of points, points), include point
    def __GetPointInEdge(self, x, y) -> tuple:
        tempList = []
        for i in range(max(0, x-1), min(self.xLength, x+2)):
            for j in range(max(0, y-1), min(self.yLength, y+2)):
                tempList.append((i, j))
        return (len(tempList), tuple(tempList))

    def __InitMineField(self, x, y):
        xLength, yLength, mineNum, ruleType = self.xLength, self.yLength, self.mineNum, self.ruleType
        if(ruleType):
            tempArr = np.concatenate((np.zeros(xLength*yLength-mineNum-1, dtype=bool), np.ones(mineNum, dtype=bool)), 0)
            for i in range(xLength*yLength-mineNum-1, xLength*yLength-1):
                temprint = random.randint(0, i)
                tempArr[i], tempArr[temprint] = tempArr[temprint], tempArr[i]
            tempArr = np.insert(tempArr, (x*yLength+y), False)
        else:
            tempTuple = self.__GetPointInEdge(x, y)
            tempArr = np.concatenate((np.zeros(xLength*yLength-mineNum-tempTuple[0], dtype=bool), np.ones(mineNum, dtype=bool)), 0)
            for i in range(xLength*yLength-mineNum-tempTuple[0], xLength*yLength-tempTuple[0]):
                temprint = random.randint(0, i)
                tempArr[i], tempArr[temprint] = tempArr[temprint], tempArr[i]
            for i in tempTuple[1]:
                tempArr = np.insert(tempArr, (i[0]*yLength+i[1]), False)
        self.__mineField = tempArr.reshape(xLength, yLength)
        self.__status = 1

    def __DFS(self, x, y, used:list):
        if((x, y) in used):
            return
        used.append((x, y))
        sumMine = 0
        tempTuple = self.__GetPointInEdge(x, y)[1]
        for i in tempTuple:
            if(self.__mineField[i[0], i[1]]):
                sumMine += 1
        self.__board[x, y] = sumMine
        if(sumMine == 0):
            for i in tempTuple:
                self.__DFS(i[0], i[1], used)


if __name__ == '__main__':
    mineSweeper = MineSweeper(file='MSR')
    if(mineSweeper.GetStatus() == -1):
        mineSweeper = MineSweeper()
    #test
    # mineSweeper.ClickPoint(29, 0)
    # mineSweeper.PlantFlag(0, 0)
    # mineSweeper.SaveMineSweeper('MSR')
    print(mineSweeper.GetStatus(), mineSweeper.GetRemainingFlags())
    with open('board.log', 'w') as fp:
        for i in range(mineSweeper.yLength):
            for j in range(mineSweeper.xLength):
                print(int(mineSweeper.GetBoard()[j, i]), end=' ', file=fp)
            print(file=fp)
