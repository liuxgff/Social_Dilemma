# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 15:52
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""

import random
import numpy as np


class Cleanup:
    def __init__(self, ROW=12, COL=20, appleRate=0.1, garbageRate=0.15, agentsList=None, InitRandAddress=True):
        self.ROW = ROW  # 地图的宽
        self.COL = COL   # 地图的长
        self.Map_table = None  # 创建地图
        self.apple_N = 0  # 苹果的个数
        self.garbage_N = 0  # 垃圾的个数
        self.appleMaxRate = appleRate
        self.appleRate = 0  # 垃圾的生长率系数
        self.garbageRate = garbageRate  # 苹果的生长率系数
        self.agentsList = agentsList  # 玩家列表
        self.initRandAddress = InitRandAddress  # 玩家初始位置
        self.doAction = [[-1, 1, 0, 0], [0, 0, -1, 1]]  # 动作矩阵，上下左右
        self.endAppleNum = 0  # 采集苹果的数量

        self.aStr = '+'  # 苹果表示
        self.gStr = '-'  # 垃圾表示

        self.build()  # 创建地图
        self.updateRate()  # 更新数据

    # 建立地图
    def build(self):
        """
        地图分为上下两部分，上部分区域为垃圾区域，下部分为苹果区域
        地图总大小: 12 * 20 ; 每小块地图大小: 6 * 10
        新建地图时，垃圾和苹果的随机增长概率Rate = 0.2
        """
        INIT_RATE = 0.05
        self.Map_table = np.empty((self.ROW, self.COL), dtype=np.str_)  # 初始化地图
        # 地图初始化
        for i in range(self.ROW):
            for j in range(self.COL):
                if 0 <= i < self.ROW // 2 and random.random() <= INIT_RATE:  # 如果在垃圾增长的区域, 随机增长垃圾
                    self.Map_table[i, j] = self.gStr
                    self.garbage_N += 1
                elif self.ROW // 2 <= i < self.ROW and random.random() <= INIT_RATE:  # 如果在苹果区域，随机生成苹果
                    self.Map_table[i, j] = self.aStr
                    self.apple_N += 1
                else:  # 否则为空
                    self.Map_table[i, j] = ' '
        self.set_init_agents()  # 放置agents
        self.updateRate()  # 更新数据

    # 生成Agent初始坐标
    def set_init_agents(self):
        """
        创建Agents的初始位置
        :return:
        """
        for agent in self.agentsList:
            if self.initRandAddress:  # 如果agent位置是随机
                while True:
                    x = random.randint(0, self.ROW - 1)
                    y = random.randint(0, self.COL - 1)
                    if self.Map_table[x, y] == ' ':  # 如果该位置为空可以安置agent
                        break
                agent.address = [x, y]
            else:
                if agent.selectAddress == 0:  # selectAddress == 0表示初始位置在垃圾区域
                    while True:
                        x = random.randint(0, self.ROW // 2 - 1)
                        y = random.randint(0, self.COL - 1)
                        if self.Map_table[x, y] == ' ':  # 如果该位置为空可以安置agent
                            break
                    agent.address = [x, y]
                elif agent.selectAddress == 1:  # selectAddress == 1表示初始位置在苹果区域
                    while True:
                        x = random.randint(self.ROW // 2, self.ROW - 1)
                        y = random.randint(0, self.COL - 1)
                        if self.Map_table[x, y] == ' ':  # 如果该位置为空可以安置agent
                            break
                    agent.address = [x, y]
            self.Map_table[x, y] = agent.name

    # 地图初始化
    def newMap(self):
        self.endAppleNum = 0  # 采集苹果的总个数
        self.apple_N = 0  # 苹果的个数
        self.garbage_N = 0  # 垃圾的个数
        self.build()  # 创建地图

    # 更新苹果的增长率
    def updateRate(self):
        k = -self.appleMaxRate / (self.ROW / 4 * self.COL)  # 苹果增长率与垃圾数量的线性斜率
        self.appleRate = k * self.garbage_N + self.appleMaxRate

    # 获取Agent的信息
    def getAgent(self, agentNum):  # num为第几个Agent
        M = np.array([])
        M = M.astype('float')

        'agent的坐标'
        x = self.agentsList[agentNum].address[0]
        y = self.agentsList[agentNum].address[1]

        'agent视野的起始位置、终止位置'
        sx = x - self.agentsList[agentNum].view  # 视野起始x
        sy = y - self.agentsList[agentNum].view  # 视野起始y
        ex = x + self.agentsList[agentNum].view  # 视野终止x
        ey = y + self.agentsList[agentNum].view  # 视野终止y

        '视野大小'
        viewSize = (self.agentsList[agentNum].view * 2 + 1) ** 2

        'Agent的满足度占比'
        sPercent = int((self.agentsList[agentNum].currentSatisfaction / self.agentsList[agentNum].MaxSatisfaction) * viewSize)
        for i in range(viewSize):
            if sPercent:
                M = np.append(M, 1)
                sPercent -= 1
            else:
                M = np.append(M, 0)

        # 苹果的位置
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if 0 <= i < self.ROW and 0 <= j < self.COL:  # 防止出界
                    if self.Map_table[i, j] == self.aStr:
                        M = np.append(M, 1)
                    else:
                        M = np.append(M, 0)
                else:
                    M = np.append(M, 0)

        # 垃圾的位置
        for i in range(sx, ex + 1):
            for j in range(sy, ey + 1):
                if 0 <= i < self.ROW and 0 <= j < self.COL:
                    if self.Map_table[i, j] == self.gStr:
                        M = np.append(M, 1)
                    else:
                        M = np.append(M, 0)
                else:
                    M = np.append(M, 0)
        return M

    # 检测Agent是否出界
    def is_state(self, agentNum, action):
        """
        :param agentNum: agent编号
        :param action: 动作
        :return:
        """
        x = self.agentsList[agentNum].address[0] + self.doAction[0][action]
        y = self.agentsList[agentNum].address[1] + self.doAction[1][action]
        if 0 <= x < self.ROW and 0 <= y < self.COL:  # 未出界
            return False
        else:  # 出界
            return True

    # Agent移动
    def move(self, agentNum, action):
        """
        :param agentNum: agent编号
        :param action: 动作
        :return:
        """
        # 移动前的坐标
        x = self.agentsList[agentNum].address[0]
        y = self.agentsList[agentNum].address[1]
        # 移动后的坐标
        x_ = x + self.doAction[0][action]
        y_ = y + self.doAction[1][action]

        Reward = 0

        "如果新的位置是苹果"
        if self.Map_table[x_, y_] == self.aStr:
            self.endAppleNum += 1  # 获取苹果数量加1
            self.apple_N -= 1  # 苹果数量减一
            self.agentsList[agentNum].ownAppleNum += 1  # 每轮agent采集苹果的数量
            # 采集苹果获得奖励
            realReward = 10  # 实际奖励
            self.agentsList[agentNum].currentSatisfaction += realReward
            Reward = realReward

        "如果新位置为空"
        if self.Map_table[x_, y_] == ' ':
            Reward = 0

        "如果agent移动到垃圾清理区域"
        if x_ < self.ROW//2:
            # agent的视野
            if action == 0:  # agent向上走
                begin_x = x_ - self.agentsList[agentNum].view
                end_x = x_
                begin_y = y_ - 1
                end_y = y_ + 1
            elif action == 1:  # 如果agent向下走
                begin_x = x_
                end_x = x_ + self.agentsList[agentNum].view
                begin_y = y_ - 1
                end_y = y_ + 1
            elif action == 2:  # agent向左走
                begin_x = x_ - 1
                end_x = x_ + 1
                begin_y = y_ - self.agentsList[agentNum].view
                end_y = y_
            else:  # agent向右走
                begin_x = x_ - 1
                end_x = x_ + 1
                begin_y = y_
                end_y = y_ + self.agentsList[agentNum].view

            # 清除agent眼前的垃圾
            temp_num_g = 0  # 记录清除了多少个垃圾
            for cx in range(begin_x, end_x + 1):
                for cy in range(begin_y, end_y + 1):
                    if 0 <= cx < self.ROW // 2 and 0 <= cy < self.COL:
                        if self.Map_table[cx, cy] == self.gStr:
                            self.Map_table[cx, cy] = ' '
                            self.garbage_N -= 1
                            temp_num_g += 1
            # 每轮agent采集垃圾的数量
            temp_num_g = temp_num_g / ((self.agentsList[agentNum].view + 1) ** 2)
            self.agentsList[agentNum].ownGarbageNum += temp_num_g
            # 清理垃圾获得奖励
            realReward = temp_num_g * 5
            self.agentsList[agentNum].currentSatisfaction += realReward
            Reward = realReward

        "移动agent到新位置"
        # 如果新位置是另一个Agent
        if self.Map_table[x_, y_] != ' ' and self.Map_table[x_, y_] != self.gStr and self.Map_table[x_, y_] != self.aStr:
            x_ = x
            y_ = y

        # Agent位置更新
        self.agentsList[agentNum].address = [x_, y_]
        self.Map_table[x, y] = ' '  # 清空Agent原来的位置
        self.Map_table[x_, y_] = self.agentsList[agentNum].name  # agent放置新位置
        self.updateRate()  # 更新增长率

        print(self.agentsList[agentNum].name, self.agentsList[agentNum].currentSatisfaction)
        return Reward

    # 垃圾再生长
    def updateGarbage(self):
        for i in range(self.ROW//2):
            for j in range(self.COL):
                if random.random() <= self.garbageRate and self.Map_table[i, j] == ' ':  # 如果在垃圾增长的区域, 更新垃圾
                    self.Map_table[i, j] = self.gStr
                    self.garbage_N += 1
        # 更新增长率
        self.updateRate()

    # 苹果再生长
    def updateApple(self):
        for i in range(self.ROW//2, self.ROW):
            for j in range(self.COL):
                if random.random() <= self.appleRate and self.Map_table[i, j] == ' ':  # 如果在苹果区域，更新苹果
                    self.Map_table[i, j] = self.aStr
                    self.apple_N += 1
        # 更新增长率
        self.updateRate()

    def getAgentArea(self, agentNum):
        """
        获得当前Agent所在的区域
        :param agentNum:
        :return:
        """
        Agent_x = self.agentsList[agentNum].address[0]
        if 0 <= Agent_x < self.ROW // 2:
            return 0
        else:
            return 1

    # 输出函数
    def display(self):
        # 输出地图
        for i in range(self.ROW):
            print('%-2d' % i, end='')
            for j in range(self.COL):
                print(self.Map_table[i][j], end=' ')
            print('\r')
