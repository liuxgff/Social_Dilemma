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


def getData(dataName):
    """
    获得图像数据
    :return:
    """
    path = 'Result/'
    return list(pd.read_csv(path + dataName + '/ApplesCollection.csv', index_col=False)['result'])


"动态学习率与固定学习率比较"
compareList = [getData('异质群体'), getData('固定学习率'), getData('随机动作')]
draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='动态学习率与固定学习率.pdf',
          label_list=['Heterogeneous', 'Fixed Learning Rate', 'Random Action'], colorIndex=[2, 5, 4])

"异质性群体与同质性群体比较"
compareList = [getData('同质低目标收益群体'), getData('同质高目标收益群体'), getData('异质群体'), getData('随机动作')]
draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='异质性群体与同质性群体.pdf',
          label_list=['Homogeneous Low', 'Homogeneous High', 'Heterogeneous', 'Random Action'], colorIndex=[0, 1, 2, 4])



