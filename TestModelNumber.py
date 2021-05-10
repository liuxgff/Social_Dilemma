# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 15:53
@Email  ：liuxgemail@163.com
@Description ：实验模型
=================================================="""
import os


def createFolder(PATH):
    if os.path.exists(PATH):
        pass
    else:
        os.mkdir(PATH)


number = 1  # 模型编号
Model_number = 'Model_' + str(number)
createFolder(Model_number)

#  每个Agent的训练模型存储地址
MODEL_PATH_A = Model_number + '/Network' + '_A'
MODEL_PATH_B = Model_number + '/Network' + '_B'
MODEL_PATH_C = Model_number + '/Network' + '_C'
MODEL_PATH_D = Model_number + '/Network' + '_D'