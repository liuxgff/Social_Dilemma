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

Model_1_h = list(pd.read_csv(path + 'Model_1_h/ApplesCollection.csv', index_col=False)['result'])

Model_2_h = list(pd.read_csv(path + 'Model_2_h/ApplesCollection.csv', index_col=False)['result'])

Model_3_h = list(pd.read_csv(path + 'Model_3_h/ApplesCollection.csv', index_col=False)['result'])

Model_FixedLR = list(pd.read_csv(path + 'Model_FixedLR/ApplesCollection.csv', index_col=False)['result'])

Model_Random = list(pd.read_csv(path + 'Model_Random/ApplesCollection.csv', index_col=False)['result'])

Model_6 = list(pd.read_csv(path + 'Model_rewardLen_8/ApplesCollection.csv', index_col=False)['result'])

Model__randLocation = list(pd.read_csv(path + 'Model_randLocation/ApplesCollection.csv', index_col=False)['result'])

Model_randLocation_2 = list(pd.read_csv(path + 'Model_randLocation_2/ApplesCollection.csv', index_col=False)['result'])

Model_randLocation_3 = list(pd.read_csv(path + 'Model_randLocation_3/ApplesCollection.csv', index_col=False)['result'])

"同质性与异质性比较"
compareList = [Model_1_h, Model_2_h, Model_3_h, Model_Random]
# compareList = [Model_3, Model__randLocation, Model_randLocation_2, Model_randLocation_3]

y_label = 'Collective reward'  # y坐标轴名称
x_label = 'Episode'  # x轴名称
label_list = ['Homogeneous Low', 'Homogeneous High', 'Heterogeneous', 'Random Action']
# [2, 3, 4, 5]
# label_list = ['Homogeneous Low', 'Homogeneous High', 'Heterogeneous', 'Random Action']
# [0, 1, 2, 4]
figPath = 'Apple_h.png'  # 存储图像的地址

draw_list(plot_list=compareList, y_lable=y_label, x_lable=x_label, figPath=figPath,
          label_list=label_list, colorIndex=[0, 1, 2, 4])


# "改变学习率与固定学习率"
# compareList = [Model_3, Model_FixedLR, Model_Random]
# y_label = 'Collective reward'  # y坐标轴名称
# x_label = 'Episode'  # x轴名称
# label_list = ['Heterogeneous', 'Fixed LR', 'Random Action']
# figPath = 'Apples_lr.png'  # 存储图像的地址
#
# draw_list(plot_list=compareList, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=label_list, colorIndex=[2, 5, 4])
