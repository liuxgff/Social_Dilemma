# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/6/8 16:47
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
from Draw import draw_heatmap
import pandas as pd

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
        draw_heatmap(data, os.path.join(each_file, 'heatMap.jpg'))
        # apple_data = list(pd.read_csv(data_path)['Apples'])
        # apple_data = pd.DataFrame(apple_data, index=['Agent1', 'Agent2', 'Agent3', 'Agent4', 'Agent5', 'Agent6'],
        #                           columns=['Apples'])
        #
        # garbage_data = list(pd.read_csv(data_path)['Garbage'])
        # garbage_data = pd.DataFrame(garbage_data, index=['Agent1', 'Agent2', 'Agent3', 'Agent4', 'Agent5', 'Agent6'],
        #                             columns=['Garbage'])
        #
        # draw_heatmap(apple_data, os.path.join(each_file, 'apple_heatMap.jpg'))
        # draw_heatmap(garbage_data, os.path.join(each_file, 'garbage_heatMap.jpg'))


draw_heatMap()