# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 15:52
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""

import random
import numpy as np

from TestModelNumber import number

# 生成垃圾的概率
GARBAGE_R = 0.15
GARBAGES = 10

# 生成苹果的概率
APPLE_R = 0.1
APPLES = 5

# agent的视野窗口5*5
win_width = 5
view = 2

if number == 1 or number == 0:
    # Agent的初始位置
    APPEL_REGION = 0  # 区域1垃圾增长区域
    GARBAGE_REGION = 1  # 区域4垃圾增长区域
    # Agent最大满足度设置
    AMSAT = 20
    BMSAT = 200
    CMSAT = 200
    DMSAT = 20


class Cleanup:
    def __init__(self, ROW=14, COL=14, apple_init_Num=5, garbage_init_Num=10, AgentsList=None):
        self.Map_table = np.empty((ROW, COL), dtype=np.str)  # 创建地图
        self.Apple_N = apple_init_Num  # 苹果的初始个数
        self.Garbage_N = garbage_init_Num  # 垃圾的初始个数
        self.AgentsList = AgentsList  # 玩家列表

        self.Init_Map = self.Map_table  # 记录地图的初始位置

        self.action_space = ['up', 'down', 'left', 'right']  # 玩家移动的方向
        self.actions = len(self.action_space)
        self.n_features = win_width * win_width * 3  # 神经网络输入数据长度(Agent信息M)
        self.Grate = GARBAGE_R  # 垃圾的生长率系数
        self.Arate = APPLE_R  # 苹果的生长率系数
        self.reward = 0  # 采集苹果的数量
        self.RoundA = [0] * len(self.Agents)  # 每个玩家每轮采集苹果的数量
        self.RoundG = [0] * len(self.Agents)  # 每个玩家每轮采集垃圾的数量
        self.build()  # 创建地图
        self.updata()  # 更新数据

    # 建立地图
    def build(self):
        # 地图初始化
        for i in range(ROW):
            for j in range(COL):
                self.Map_table[i, j] = ' '
        '-------------------四块游戏地图-------------------'
        "地图总大小: 14 * 14 ; 每小块地图大小: 7 * 7"
        "新建地图时，垃圾和苹果的随机增长概率Rate = 0.2"
        Rate = 0.1
        for i in range(0, int(ROW / 2)):
            # 第一块地图, 垃圾增长区域
            for j in range(0, int(COL / 2)):
                if random.random() <= Rate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '-'
                    self.Garbage_N += 1
            # 第二块地图, 苹果增长区域
            for j in range(int(COL / 2), COL):
                if random.random() <= Rate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '+'
                    self.Apple_N += 1

        for i in range(int(ROW / 2), ROW):
            # 第三块地图, 苹果增长区域
            for j in range(0, int(COL / 2)):
                if random.random() <= Rate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '+'
                    self.Apple_N += 1
            # 第四块地图, 垃圾增长区域
            for j in range(int(COL / 2), COL):
                if random.random() <= Rate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '-'
                    self.Garbage_N += 1
        '-------------------------------------------------'

    # 生成Agent初始坐标
    def set_init_address(self, regionNum):
        # #######################################################
        # 第一块区域(垃圾增长区域)[row坐标(0, int(ROW / 2) - 1)]; [col坐标(0, int(COL / 2) - 1)]
        # 第二块区域(苹果增长区域)[row坐标(0, int(ROW / 2) - 1)]; [col坐标(int(COL / 2), COL - 1)]
        # 第三块区域(苹果增长区域)[row坐标(int(ROW / 2), ROW - 1)]; [col坐标(0, int(COL / 2) - 1)]
        # 第四块区域(垃圾增长区域)[row坐标(int(ROW / 2), ROW - 1)]; [col坐标(int(COL / 2), COL - 1)]
        # #######################################################
        if regionNum == 1:
            tempROW = random.randint(0, int(ROW / 2) - 1)
            tempCOL = random.randint(0, int(COL / 2) - 1)
        elif regionNum == 2:
            tempROW = random.randint(0, int(ROW / 2) - 1)
            tempCOL = random.randint(int(COL / 2), COL - 1)
        elif regionNum == 3:
            tempROW = random.randint(int(ROW / 2), ROW - 1)
            tempCOL = random.randint(0, int(COL / 2) - 1)
        elif regionNum == 4:
            tempROW = random.randint(int(ROW / 2), ROW - 1)
            tempCOL = random.randint(int(COL / 2), COL - 1)
        return tempROW, tempCOL

    # 生成玩家
    def create_agent(self):
        # 创建玩家的初始位置
        self.Agent_address = []  # 玩家的坐标
        '------------第一块垃圾增长区域生成一个agent-----------'
        A_row, A_col = self.set_init_address(AREGION)
        while self.Map_table[A_row, A_col] != ' ':
            A_row, A_col = self.set_init_address(AREGION)
        self.Map_table[A_row, A_col] = 'A'
        # 记录玩家坐标
        self.Agent_address.append((A_row, A_col))

        '------------第二块苹果增长区域生成一个agent-----------'
        B_row, B_col = self.set_init_address(BREGION)
        while self.Map_table[B_row, B_col] != ' ':
            B_row, B_col = self.set_init_address(BREGION)
        self.Map_table[B_row, B_col] = 'B'
        self.Agent_address.append((B_row, B_col))

        '------------第三块苹果增长区域生成一个agent-----------'
        C_row, C_col = self.set_init_address(CREGION)
        while self.Map_table[C_row, C_col] != ' ':
            C_row, C_col = self.set_init_address(CREGION)
        self.Map_table[C_row, C_col] = 'C'
        self.Agent_address.append((C_row, C_col))

        '------------第四块垃圾增长区域生成一个agent-----------'
        D_row, D_col = self.set_init_address(DREGION)
        while self.Map_table[D_row, D_col] != ' ':
            D_row, D_col = self.set_init_address(DREGION)
        self.Map_table[D_row, D_col] = 'D'
        self.Agent_address.append((D_row, D_col))

    # 地图初始化
    def newMap(self):
        self.reward = 0  # 采集苹果的总个数
        self.Agent_reward = [0] * len(self.Agents)  # 每个玩家的外部奖励积分值
        '------玩家满意度设置------'
        self.Agent_satisfaction = [0] * len(self.Agents)  # 每个玩家的满意度
        '------------------------'
        self.RoundA = [0] * len(self.Agents)  # 每个玩家每轮采集苹果的数量
        self.RoundG = [0] * len(self.Agents)  # 每个玩家每轮采集垃圾的数量
        self.Apple_N = APPLES  # 苹果的初始个数
        self.Garbage_N = GARBAGES  # 垃圾的初始个数
        self.build()  # 创建地图
        self.create_agent()
        self.updata()

    # 获取Agent的信息
    def getAgent(self, num):  # num为第几个Agent
        M = np.array([])
        M = M.astype('float')

        'agent的坐标'
        x = self.Agent_address[num][0]
        y = self.Agent_address[num][1]

        'agent视野的起始位置、终止位置'
        sx = x - view  # 视野起始x
        sy = y - view  # 视野起始y
        ex = x + view  # 视野终止x
        ey = y + view  # 视野终止y

        'Agent的满足度占比'
        sPercent = int((self.Agent_satisfaction[num] / self.Max_satisfaction[num]) * (win_width * win_width))
        for i in range(win_width * win_width):
            if sPercent:
                M = np.append(M, 1)
                sPercent -= 1
            else:
                M = np.append(M, 0)

        # 苹果的位置
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if 0 <= i < ROW and 0 <= j < COL:  # 防止出界
                    if self.Map_table[i, j] == '+':
                        M = np.append(M, 1)
                    else:
                        M = np.append(M, 0)
                else:
                    M = np.append(M, 0)

        # 垃圾的位置
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if 0 <= i < ROW and 0 <= j < COL:
                    if self.Map_table[i, j] == '-':
                        M = np.append(M, 1)
                    else:
                        M = np.append(M, 0)
                else:
                    M = np.append(M, 0)
        return M

    # 检测Agent是否出界
    def is_state(self, i, action):
        x = self.Agent_address[i][0]
        y = self.Agent_address[i][1]
        mark = 0
        # up
        if action == 0:
            if x == 0:
                mark = 1
        # down
        if action == 1:
            if x == ROW - 1:
                mark = 1
        # left
        if action == 2:
            if y == 0:
                mark = 1
        # right
        if action == 3:
            if y == COL - 1:
                mark = 1
        return mark

    # Agent移动
    def move(self, action, num):  # i为第几个Agent
        x = self.Agent_address[num][0]
        y = self.Agent_address[num][1]
        x_ = x
        y_ = y
        R = 0
        # up
        if action == 0:
            x_ = x - 1
        # down
        if action == 1:
            x_ = x + 1
        # left
        if action == 2:
            y_ = y - 1
        # right
        if action == 3:
            y_ = y + 1

        # 如果新的位置是苹果------------------------------------------star
        if self.Map_table[x_, y_] == '+':
            self.reward += 1  # 获取苹果数量加1
            self.Apple_N -= 1  # 苹果数量减一
            self.RoundA[num] += 1  # 每轮agent采集苹果的数量
            '--------------采集苹果获得奖励--------------star'
            ar = 0.1  # 奖励系数
            if self.Agent_satisfaction[num] < self.Max_satisfaction[num]:
                R = (self.Max_satisfaction[num] - self.Agent_satisfaction[num]) * ar
            else:
                R = 0.1
            self.Agent_satisfaction[num] += R / 10
            # print("玩家：", num, "满意度:", self.Agent_satisfaction[num], "采集苹果奖励：", R)
            '--------------采集苹果获得奖励--------------end'
        # 如果新的位置是苹果-------------------------------------------end

        # 如果新位置为空
        if self.Map_table[x_, y_] == ' ':
            R = -5

        # 如果agent移动到垃圾清理区域---------------------------------star
        if (0 <= x_ <= int(ROW / 2) and 0 <= y_ <= int(COL / 2)) or \
                (int(ROW / 2) <= x_ < ROW and int(COL / 2) <= y_ < COL):
            window = 2
            beginx = 0
            endx = 0
            beginy = 0
            endy = 0
            if action == 0:  # agent向上走
                # 先清除当前agent眼前的垃圾
                beginx = x - window
                endx = x
                beginy = y - 1
                endy = y + 1
            if action == 1:  # 如果agent向下走
                beginx = x
                endx = x + window
                beginy = y - 1
                endy = y + 1
            if action == 2:  # agent向左走
                beginx = x - 1
                endx = x + 1
                beginy = y - window
                endy = y
            if action == 3:  # agent向右走
                beginx = x - 1
                endx = x + 1
                beginy = y
                endy = y + window

            # 清除agent眼前的垃圾
            temp_num_g = 0  # 记录清除了多少个垃圾
            for cx in range(beginx, endx + 1):
                for cy in range(beginy, endy + 1):
                    if (0 <= cx <= int(ROW / 2) and 0 <= cy <= int(COL / 2)) or \
                            (int(ROW / 2) <= cx < ROW and int(COL / 2) <= cy < COL):
                        if self.Map_table[cx, cy] == '-':
                            self.Map_table[cx, cy] = ' '
                            self.Garbage_N -= 1
                            temp_num_g += 1

            '--------------清理垃圾获得奖励--------------star'
            self.RoundG[num] += temp_num_g / 6  # 每轮agent采集垃圾的数量
            dr = 0.6  # 奖励系数
            R = dr * temp_num_g
            self.Agent_satisfaction[num] += R
            # print("玩家：", num, "满意度:", self.Agent_satisfaction[num], "清理垃圾奖励：", R)
            '--------------清理垃圾获得奖励--------------end'
        # 如果agent移动到垃圾清理区域---------------------------------end

        # 移动agent到新位置，且如果新位置是另一个Agent
        if self.Map_table[x_, y_] != ' ' and self.Map_table[x_, y_] != '+' and self.Map_table[x_, y_] != '-':
            x_ = x
            y_ = y
        self.Agent_address[num] = (x_, y_)  # Agent位置更新
        self.Map_table[x, y] = ' '  # 清空Agent原来的位置
        self.Map_table[x_, y_] = self.Agents[num]  # agent放置新位置
        self.updata()  # 更新增长率
        return R

    # 更新垃圾和苹果的增长率
    def updata(self):
        # 苹果的增长率
        k = -APPLE_R / (win_width * win_width * 2)  # 苹果增长率与垃圾数量的线性斜率
        self.Arate = k * self.Garbage_N + APPLE_R

    # 垃圾再生长
    def upG(self):
        # 更新垃圾
        # 第一块地图, 垃圾增长区域
        for i in range(0, int(ROW / 2)):
            for j in range(0, int(COL / 2)):
                if random.random() <= self.Grate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '-'
                    self.Garbage_N += 1

        # 第四块地图, 垃圾增长区域
        for i in range(int(ROW / 2), ROW):
            for j in range(int(COL / 2), COL):
                if random.random() <= self.Grate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '-'
                    self.Garbage_N += 1
        # 更新增长率
        self.updata()

    # 苹果再生长
    def upA(self):
        # 更新苹果
        # 第二块地图, 苹果增长区域
        for i in range(0, int(ROW / 2)):
            for j in range(int(COL / 2), COL):
                if random.random() <= self.Arate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '+'
                    self.Apple_N += 1
        # 第三块地图, 苹果增长区域
        for i in range(int(ROW / 2), ROW):
            for j in range(0, int(COL / 2)):
                if random.random() <= self.Arate and self.Map_table[i, j] == ' ':
                    self.Map_table[i, j] = '+'
                    self.Apple_N += 1
        # 更新增长率
        self.updata()

    def getAgentArea(self, num):
        """
        获得当前Agent所在的区域
        :param num:
        :return:
        """
        # #######################################################
        # 第一块区域(垃圾增长区域)[row坐标(0, int(ROW / 2) - 1)]; [col坐标(0, int(COL / 2) - 1)]
        # 第二块区域(苹果增长区域)[row坐标(0, int(ROW / 2) - 1)]; [col坐标(int(COL / 2), COL - 1)]
        # 第三块区域(苹果增长区域)[row坐标(int(ROW / 2), ROW - 1)]; [col坐标(0, int(COL / 2) - 1)]
        # 第四块区域(垃圾增长区域)[row坐标(int(ROW / 2), ROW - 1)]; [col坐标(int(COL / 2), COL - 1)]
        # #######################################################
        Agent_x = self.Agent_address[num][0]
        Agent_y = self.Agent_address[num][1]
        if 0 <= Agent_x <= (int(ROW / 2) - 1) and 0 <= Agent_y <= (int(COL / 2) - 1):
            return 0
        elif 0 <= Agent_x <= (int(ROW / 2) - 1) and int(COL / 2) <= Agent_y <= (COL - 1):
            return 1
        elif int(ROW / 2) <= Agent_x <= (ROW - 1) and 0 <= Agent_y <= (int(COL / 2) - 1):
            return 2
        elif int(ROW / 2) <= Agent_x <= (ROW - 1) and int(COL / 2) <= Agent_y <= (COL - 1):
            return 3

    # 输出函数
    def display(self):
        # 输出地图
        for i in range(ROW):
            print('%-2d' % i, end='')
            for j in range(COL):
                print(self.Map_table[i][j], end=' ')
            print('\r')
