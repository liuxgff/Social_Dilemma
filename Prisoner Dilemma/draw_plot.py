#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： LiuXG
# datetime： 2021/11/11 20:55 
# ide： PyCharm
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LABELSIZE = 16  # 图像中所有label的大小
LEFT = 0.1  # 画布设置，距离左侧大小
BOTTOM = 0.14  # 距离底部大小
RIGHT = 0.77  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 10
HEIGHT = WIDTH / 1.7
# 图像像素
DPI = 400

FONT = 'Arial'


def draw_sorce(path1, path2, data_name, shadow=100):
    """
    分数对比
    :return:
    """
    path1_result = pd.read_csv(os.path.join(path1, data_name[0]))
    result1 = [list(path1_result[i]) for i in path1_result][0]

    path2_result = pd.read_csv(os.path.join(path2, data_name[0]))
    result2 = [list(path2_result[i]) for i in path2_result][0]


    "绘制图像"
    plt.figure(1)  # 图像编号

    plt.rc('font', family=FONT)  # 图像字体
    plt.figure(figsize=(WIDTH, HEIGHT))  # 自定义画布大小(width,height)

    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小


    # 建立画布
    ax = plt.subplot(211)
    plt.grid()  # 生成网格

    plt.plot(np.arange(len(result1)), result1, color='darkorange', linewidth=1.1)
    updata = [j + shadow for j in result1]
    downdata = [j - shadow for j in result1]
    plt.fill_between(np.arange(len(result1)), downdata, updata, facecolor='tan', alpha=0.3)

    plt.plot(np.arange(len(result2)), result2, color='b', linewidth=1.1)
    updata = [j + shadow for j in result2]
    downdata = [j - shadow for j in result2]
    plt.fill_between(np.arange(len(result2)), downdata, updata, facecolor='royalblue', alpha=0.3)

    ax.set_ylabel('Collective score')  # y轴标签


    "=======CC占比========="
    path1_result = pd.read_csv(os.path.join(path1, data_name[1]))
    result1 = [list(path1_result[i]) for i in path1_result][0]

    path2_result = pd.read_csv(os.path.join(path2, data_name[1]))
    result2 = [list(path2_result[i]) for i in path2_result][0]

    ax = plt.subplot(212)
    plt.grid()  # 生成网格

    plt.plot(np.arange(len(result1)), result1, color='darkorange', linewidth=1.1)
    updata = [j + shadow for j in result1]
    downdata = [j - shadow for j in result1]
    plt.fill_between(np.arange(len(result1)), downdata, updata, facecolor='tan', alpha=0.3)

    plt.plot(np.arange(len(result2)), result2, color='b', linewidth=1.1)
    updata = [j + shadow for j in result2]
    downdata = [j - shadow for j in result2]
    plt.fill_between(np.arange(len(result2)), downdata, updata, facecolor='royalblue', alpha=0.3)

    ax.set_ylabel('Number of cooperation')  # y轴标签
    ax.set_xlabel('Episode')  # x轴标签

    # 图例设置
    font1 = {'family': FONT,
             'weight': 'normal',
             'size': 10,
             }
    plt.legend(['Baseline', 'Dynamic learning rate'], bbox_to_anchor=(1.01, 0), loc=3, borderaxespad=0, prop=font1)

    plt.savefig('比较得分.svg', bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.savefig('比较得分.pdf', bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


draw_sorce('baseline', 'dynamic_rate', ['result.csv', 'cc_count.csv'])
