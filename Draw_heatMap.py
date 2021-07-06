# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/6/8 16:47
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
from Draw import draw_heatmap
import pandas as pd
import numpy as np
import os


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
        data_path = os.path.join(each_file, 'endReward.csv')

        data = pd.read_csv(data_path)
        newData = np.array(data['Apples'] + data['Garbage'])

        # newData = newData / np.average(newData) / 2
        newData = newData / 305

        newData = pd.DataFrame(newData, columns=['data'])

        draw_heatmap(newData, os.path.join(each_file, 'heatMap.pdf'))

draw_heatMap()
