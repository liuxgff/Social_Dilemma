# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/26 10:54
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import numpy as np

from Draw import draw_list
import os
import pandas as pd
import matplotlib.pyplot as plt

LABELSIZE = 12  # 图像中所有label的大小
LEFT = 0.1  # 画布设置，距离左侧大小
BOTTOM = 0.14  # 距离底部大小
RIGHT = 0.77  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 7.5
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


def compare_de_fixed():
    "动态学习率与固定学习率比较"
    compareList = [getData('异质群体'), getData('固定学习率'), getData('随机动作')]
    draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='动态学习率与固定学习率.pdf',
              label_list=['Heterogeneous', 'Fixed Learning Rate', 'Random Action'], colorIndex=[2, 5, 4], allReward=True)


def compare_heterogeneous_homogeneous():
    "异质性群体与同质性群体比较"
    compareList = [getData('同质低目标收益群体'), getData('同质高目标收益群体'), getData('异质群体'), getData('随机动作')]
    draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='异质性群体与同质性群体.pdf',
              label_list=['Homogeneous Low', 'Homogeneous High', 'Heterogeneous', 'Random Action'], colorIndex=[0, 1, 2, 4], allReward=True)


def compare_No1_No6():
    """
    比较不同的苹果奖励
    :return:
    """
    compareList = [getData('No1_苹果奖励为1_累计长度为5'), getData('No2_苹果奖励为4_累计长度为5'), getData('No3_苹果奖励为8_累计长度为5'),
                   getData('No4_苹果奖励为10_累计长度为5'), getData('No5_苹果奖励为12_累计长度为5'), getData('No6_苹果奖励为14_累计长度为5')]
    draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='No1_No6_不同的奖励策略.pdf',
              label_list=['Apple_reward = 1', 'Apple_reward = 4', 'Apple_reward = 8', 'Apple_reward = 10', 'Apple_reward = 12', 'Apple_reward = 14'],
              colorIndex=[0, 1, 2, 3, 4, 5])


def compare_rewardLen():
    """
    比较不同累计收益对集体采集苹果的影响
    :return:
    """
    all_rewardLen = {}
    root = os.getcwd()
    root = os.path.join(root, 'Result/累计收益长度/苹果奖励=4')
    for each_rPath in os.listdir(root):
        data_path = os.path.join(root, each_rPath)
        lenNum = int(each_rPath.split('=')[1])
        data = sum(list(pd.read_csv(data_path + '/ApplesCollection.csv', index_col=False)['result']))
        all_rewardLen[lenNum] = data
        print(each_rPath, data, lenNum)
    x_y_data = sorted(all_rewardLen.items(), key=lambda item: item[0])
    x_list = []
    y_list = []
    for x, y in x_y_data:
        x_list.append(x)
        y_list.append(y)

    "绘制图像"
    plt.figure(1)  # 图像编号

    plt.rc('font', family='Calibri')  # 图像字体
    plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小
    # 建立画布
    fig, ax = plt.subplots()
    plt.grid()  # 生成网格
    fig.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    fig.set_size_inches(WIDTH, HEIGHT)  # 图像大小

    plt.plot(np.arange(len(y_list)), y_list, color='darkorange', linewidth=1.1, marker='^')
    plt.xticks(np.arange(len(x_list)), x_list)
    ax.set_ylabel('Insect collecting amount')  # y轴标签
    ax.set_xlabel('Cumulative profit length')  # x轴标签

    plt.savefig(os.path.join(root, '比较不同累计收益长度.pdf'), bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


compare_rewardLen()