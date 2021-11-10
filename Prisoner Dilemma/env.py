#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： LiuXG
# datetime： 2021/11/8 23:11 
# ide： PyCharm


class PD:
    def __init__(self):
        pass

    def get_reward(self, a1, a2):
        if a1 == 'C' and a2 == 'C':
            return 3, 3
        elif a1 == 'C' and a2 == 'D':
            return 0, 5
        elif a1 == 'D' and a2 == 'C':
            return 5, 0
        elif a1 == 'D' and a2 == 'D':
            return 1, 1
