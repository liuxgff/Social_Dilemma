# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/6/28 9:27
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
from Draw import draw_boxplot
import random
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
# 结果路径
path = 'Result/'


"不同τ下的总收益"


rewardLen_2 = list(pd.read_csv(path + '累计收益长度2/ApplesCollection.csv', index_col=False)['result'])
Heterogeneous = list(pd.read_csv(path + '异质群体/ApplesCollection.csv', index_col=False)['result'])
rewardLen_8 = list(pd.read_csv(path + '累计收益长度8/ApplesCollection.csv', index_col=False)['result'])
rewardLen_11 = list(pd.read_csv(path + '累计收益长度11/ApplesCollection.csv', index_col=False)['result'])


compareList = [rewardLen_2, Heterogeneous, rewardLen_8, rewardLen_11]
labels = [r'$\tau $' + '=2', r'$\tau $' + '=5', r'$\tau $' + '=8', r'$\tau $' + '=11']
figPath = '不同阶段收益长度.pdf'  # 存储图像的地址
draw_boxplot(compareList, figPath, labels)
