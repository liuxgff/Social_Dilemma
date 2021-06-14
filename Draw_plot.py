# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/26 10:54
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
from Draw import draw_list
import pandas as pd

LABELSIZE = 8  # 图像中所有label的大小
LEFT = 0.13  # 画布设置，距离左侧大小
BOTTOM = 0.13  # 距离底部大小
RIGHT = 0.98  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 5
HEIGHT = WIDTH / 1.5
# 图像像素
DPI = 400

path = 'Result/'

Model_1 = list(pd.read_csv(path + 'Model_1/ApplesCollection.csv', index_col=False)['result'])

Model_2 = list(pd.read_csv(path + 'Model_2/ApplesCollection.csv', index_col=False)['result'])

Model_3 = list(pd.read_csv(path + 'Model_3/ApplesCollection.csv', index_col=False)['result'])

Model_4 = list(pd.read_csv(path + 'Model_FixedLR/ApplesCollection.csv', index_col=False)['result'])

Model_5 = list(pd.read_csv(path + 'Model_Random/ApplesCollection.csv', index_col=False)['result'])

Model_6 = list(pd.read_csv(path + 'Model_rewardLen_8/ApplesCollection.csv', index_col=False)['result'])

Model_rl = list(pd.read_csv(path + 'Model_randLocation/ApplesCollection.csv', index_col=False)['result'])

Model_rl2 = list(pd.read_csv(path + 'Model_randLocation_2/ApplesCollection.csv', index_col=False)['result'])

Model_rl3 = list(pd.read_csv(path + 'Model_randLocation_3/ApplesCollection.csv', index_col=False)['result'])

"同质性与异质性比较"
compareList = [Model_3, Model_rl, Model_rl2, Model_rl3]
y_label = 'Collective benefit'  # y坐标轴名称
x_label = 'Episode'  # x轴名称
label_list = ['Heterogeneous', 'Random Location-1', 'Random Location-2', 'Random Location-3']
figPath = 'Apples_randLocation.png'  # 存储图像的地址

draw_list(plot_list=compareList, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=label_list, colorIndex=[2, 3, 4, 5])


# "改变学习率与固定学习率"
# compareList = [Model_3, Model_4, Model_5]
# y_label = 'Apple collection'  # y坐标轴名称
# x_label = 'Episode'  # x轴名称
# label_list = ['Heterogeneous', 'FixedLR', 'RandomAction']
# figPath = 'Apples_lr.png'  # 存储图像的地址
#
# draw_list(plot_list=compareList, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=label_list, colorIndex=[2, 3, 4])
