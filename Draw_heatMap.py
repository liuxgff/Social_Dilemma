# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/6/8 16:47
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
from matplotlib import pyplot as plt
from Draw import draw_heatmap
import pandas as pd
import numpy as np
import os

LABELSIZE = 12  # 图像中所有label的大小
LEFT = 0.1  # 画布设置，距离左侧大小
BOTTOM = 0.14  # 距离底部大小
RIGHT = 0.77  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 10
HEIGHT = WIDTH / 1.7
# 图像像素
DPI = 400



def get_all_file(path):
    files = os.listdir(path)
    files.sort()  # 排序
    list = []
    for file in files:
        if not os.path.isdir(path + file):  # 判断该文件是否是一个文件夹
            f_name = str(file)
            #             print(f_name)
            tr = '\\'  # 多增加一个斜杠
            filename = path + tr + f_name
            list.append(filename)
    return list


def draw_heatMap():
    file_list = get_all_file(os.path.join(os.getcwd(), 'Result'))
    for each_file in file_list:
        if each_file == 'D:\Pycharm\Projects\多智能体\Social_Dilemma\Result\累计收益长度' or\
                each_file == 'D:\Pycharm\Projects\多智能体\Social_Dilemma\Result\随机初始位置' or \
                each_file == 'D:\Pycharm\Projects\多智能体\Social_Dilemma\Result\不同的目标收益':
            continue
        data_path = os.path.join(each_file, 'endReward.csv')

        data = pd.read_csv(data_path)
        newData = np.array(data['Apples'] + data['Garbage'])
        newData = newData / np.sum(newData)
        # newData = newData / np.average(newData) / 2

        newData = pd.DataFrame(newData, columns=['data'])

        draw_heatmap(newData, os.path.join(each_file, 'heatMap.svg'))

draw_heatMap()