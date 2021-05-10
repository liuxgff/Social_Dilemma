# -*- coding: UTF-8 -*-dd
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 20:32
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""


class Agent:
    def __init__(self, name, MaxSatisfaction):
        """
        :param name: agent的名字
        :param MaxSatisfaction: agent的最大满足度
        """
        self.name = name
        self.MaxSatisfaction = MaxSatisfaction
        self.currentSatisfaction = 0
        self.ownAppleNum = 0
        self.ownGarbageNum = 0
        self.address = [0, 0]  # agent的地址

