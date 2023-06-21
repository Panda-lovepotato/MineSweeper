import win32api, win32gui, win32con
from PIL import ImageGrab
import time
import numpy
import os

class Mine_Sweeper:
    def __init__(self):
        self.MineHandle = win32gui.FindWindow(None, '扫雷')
        win32gui.SetForegroundWindow(self.MineHandle)
        self.MinePos = win32gui.GetWindowRect(self.MineHandle)
        if self.MinePos[0] < 0: raise Exception('打不开扫雷窗口，可能是你将窗口最小化了')
        LeftBouLen, UpBouLen = 23, 152
        self.SquareLen = 24
        self.YellowFaceDis = 40
        self.SquareNum_x, self.SquareNum_y, self.MineNum = 30, 16, 99
        self.MineBouLen = (LeftBouLen, UpBouLen,
            self.MinePos[2]-self.MinePos[0]-self.SquareLen*self.SquareNum_x-LeftBouLen,
            self.MinePos[3]-self.MinePos[1]-self.SquareLen*self.SquareNum_y-UpBouLen)
        self.MineDelBou = (
            self.MinePos[0]+self.MineBouLen[0],
            self.MinePos[1]+self.MineBouLen[1],
            self.MinePos[2]-self.MineBouLen[2],
            self.MinePos[3]-self.MineBouLen[3])
        self.Board = [[-3 for i in range(self.SquareNum_x)] for j in range(self.SquareNum_y)]

    def Get_Board(self):
        SquareMap = {50505:-2, 70000:-2, 90909:90, 80707:100,
                    70709:1, 60806:2, 100606:3, 60608:4, 80606:5, 60808:6, 70707:7, 80808:8}
        Img = ImageGrab.grab(bbox=self.MineDelBou)
        ImgArr = numpy.array(Img)
        succ = False
        for i in range(self.SquareNum_x):
            for j in range(self.SquareNum_y):
                cur = ImgArr[j*self.SquareLen:(j+1)*self.SquareLen, i*self.SquareLen:(i+1)*self.SquareLen, 0:3]
                cur_0 = cur[1:self.SquareLen-1, 1:self.SquareLen-1, 0:3]
                s = (numpy.sum(cur_0[:, :, 0:1]))//10000*10000 \
                    + (numpy.sum(cur_0[:, :, 1:2]))//10000*100 + (numpy.sum(cur_0[:, :, 2:3]))//10000
                if s not in SquareMap: raise Exception('发现未知非空白方块(%d, %d, %d)'%(i, j, s))
                elif s == 90909:
                    s = numpy.sum(cur)//1000
                    if s==318 or s==319: self.Board[j][i] = 0
                    elif s>320 and s<340: self.Board[j][i] = -1
                    else: raise Exception('发现未知空白方块(%d, %d, %d)'%(i, j, s))
                else: self.Board[j][i] = SquareMap[s]
                if self.Board[j][i] == -2: return 'fail'    #返回失败的消息
                if self.Board[j][i] == 100: succ = True
        if succ == True: return 'succ'  #返回成功的消息
        return None
    
    def Solve_Mine(self):
        StrToSolver = 'Solver.exe 30 16 99 '
        for i in range(self.SquareNum_x):
            for j in range(self.SquareNum_y):
                StrToSolver = StrToSolver + str(self.Board[j][i]) + ','
        StrToSolver = StrToSolver[:-1]
        #StrToSolver是popen函数的参数
        points = []
        with os.popen(StrToSolver) as fd:
            for i in fd.readlines():
                point = (i[:-1]).split(',')
                x, y = int(point[1]), int(point[0])
                if (x, y) not in points: points.append((x, y))
        # print(points)
        for i in points:
            self.Click_Square(i[0], i[1])

    def Click_Square(self, Square_x, Square_y):
        if Square_x>=0 and Square_x<self.SquareNum_x and Square_y>=0 and Square_y<self.SquareNum_y:
            point_x = self.MineDelBou[0]+self.SquareLen*Square_x+self.SquareLen/2
            point_y = self.MineDelBou[1]+self.SquareLen*Square_y+self.SquareLen/2
        else:
            point_x = (self.MineDelBou[0]+self.MineDelBou[2])/2
            point_y = self.MineDelBou[1]-self.YellowFaceDis
        if int(point_x) != point_x: raise Exception('不接受浮点型坐标')
        win32api.SetCursorPos((int(point_x), int(point_y)))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def Cal_Winning_Rate(self, times):
        succ, fail = 0, 0
        StartTime = time.time()
        for i in range(times):
            while True:
                ret = self.Get_Board()
                if ret == 'succ':
                    succ += 1
                    self.Click_Square(0, -1)
                    break
                elif ret == 'fail':
                    fail += 1
                    self.Click_Square(0, -1)
                    break
                else:
                    self.Solve_Mine()
            res = 'total:%d, succ:%d, fail:%d, succ_rate:%.2f%%, runtime:%ds  ' \
                %(i+1, succ, fail, succ/(i+1)*100, time.time()-StartTime)
            print(res, end='\r')
        print(res)

if __name__ == '__main__':

    MineSweeper = Mine_Sweeper()
    MineSweeper.Cal_Winning_Rate(50)
    # MineSweeper.Get_Board()
    # with open('board.log', 'w') as fp:
    #     for i in MineSweeper.Board:
    #         print(i, file=fp)
