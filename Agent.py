# -*- coding: UTF-8 -*-dd
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 20:32
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import math


class Agent:
    def __init__(self, name, MaxSatisfaction, rewardLen=8, initAddress=None):
        """
        :param name: agent的名字
        :param MaxSatisfaction: agent的最大满足度
        """
        self.name = name  # agent的名称
        self.MaxSatisfaction = MaxSatisfaction  # agent最高满足度
        self.currentSatisfaction = []  # agent当前的满足度
        self.rewardLen = rewardLen  # 存储奖励的长度
        self.ownAppleNum = 0  # agent持有苹果
        self.ownGarbageNum = 0  # agent持有垃圾
        self.address = [0, 0]  # agent的地址
        self.selectAddress = initAddress  # [0/1] 选择agent的初始位置，0代表垃圾区域，1代表苹果区域
        self.view = 2  # agent的视野窗口3*3
        """
        Agent的视野，1表示Agent，0表示其看到的范围
        [[0,0,0]
         [0,0,0]
         [0,1,0]]
        """

        'agent的学习率'
        # self.current_learning_rate = math.exp(-sum(self.currentSatisfaction) / (self.MaxSatisfaction / 2))
        self.current_learning_rate = max((self.MaxSatisfaction - sum(self.currentSatisfaction)), 0) / self.MaxSatisfaction
        # self.current_learning_rate = abs(self.MaxSatisfaction - sum(self.currentSatisfaction)) / self.MaxSatisfaction

    def intitAgentData(self):
        """
        初始化Agent的信息
        :return:
        """
        self.currentSatisfaction = []  # agent当前的满足度
        self.ownAppleNum = 0  # agent持有苹果
        self.ownGarbageNum = 0  # agent持有垃圾
        self.address = [0, 0]  # agent的地址
        self.update_learning_rate()  # 更新学习率

    def update_learning_rate(self):
        """
        更新该agent的学习率
        :return:
        """
        # self.current_learning_rate = math.exp(-sum(self.currentSatisfaction) / (self.MaxSatisfaction / 5))
        self.current_learning_rate = max((self.MaxSatisfaction - sum(self.currentSatisfaction)), 0) / self.MaxSatisfaction
        # self.current_learning_rate = abs(self.MaxSatisfaction - sum(self.currentSatisfaction)) / self.MaxSatisfaction
