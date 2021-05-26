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


Model_1 = list(pd.read_csv('Model_1.csv', index_col=False)['result'])

Model_2 = list(pd.read_csv('Model_2.csv', index_col=False)['result'])

Model_3 = list(pd.read_csv('Model_3.csv', index_col=False)['result'])

compareList = [Model_1, Model_2, Model_3]
y_label = 'The number of apples'  # y坐标轴名称
x_label = 'Steps'  # x轴名称
label_list = ['Model_1', 'Model_2', 'Model_3']
figPath = 'Apples.png'  # 存储图像的地址


draw_list(plot_list=compareList, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=label_list)

