# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/12 18:51
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

LABELSIZE = 12  # 图像中所有label的大小
LEFT = 0.13  # 画布设置，距离左侧大小
BOTTOM = 0.14  # 距离底部大小
RIGHT = 0.98  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 5
HEIGHT = WIDTH / 1.5
# 图像像素
DPI = 400


# 折线图绘图设置(数据列表, y轴名称, x轴名称, 图像存储地址, 标签列表)
def draw_list(plot_list=None, y_lable='', x_lable='', figPath='', label_list=None, colorIndex=0):
    # plt.rc对全图字体进行统一修改
    plt.figure(1)  # 图像编号

    plt.rc('font', family='Calibri')  # 图像字体
    plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小
    # 建立画布
    fig, ax = plt.subplots()
    plt.grid()  # 生成网格
    fig.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    # ax.spines['right'].set_visible(False)  # 取消有边框
    # ax.spines['top'].set_visible(False)  # 取消左边框

    fig.set_size_inches(WIDTH, HEIGHT)  # 图像大小

    "绘图-----------------------------------------"
    linestylelist = ['-', '--', ':', '-.']
    colors1 = ['darkorange', 'royalblue']
    FillColor1 = ['wheat', 'cornflowerblue']
    colors2 = ['darkorange', 'r',  'b', 'darkgreen', 'darkslategray', 'purple']
    FillColor2 = ['tan', 'lightcoral', 'royalblue', 'forestgreen', 'darkcyan', 'violet']
    colors2 = colors2[colorIndex:]
    FillColor2 = FillColor2[colorIndex:]

    for i in range(len(plot_list)):
        updata = [j + 10 for j in plot_list[i]]
        downdata = [j - 10 for j in plot_list[i]]
        if len(plot_list) <= 2 and not colorIndex:
            plt.plot(np.arange(len(plot_list[i])), plot_list[i], color=colors1[i], linewidth=1.1)
            plt.fill_between(np.arange(len(plot_list[i])), downdata, updata, facecolor=FillColor1[i], alpha=0.3)
        else:
            plt.plot(np.arange(len(plot_list[i])), plot_list[i], color=colors2[i], linewidth=1.1)
            plt.fill_between(np.arange(len(plot_list[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    ax.set_ylabel(y_lable)  # x轴标签
    ax.set_xlabel(x_lable)  # y轴标签
    # 图例设置
    if label_list:
        ax.legend(label_list)
    plt.savefig(figPath, dpi=DPI)  # 图像存储, 设置分辨率
    plt.close()


def draw_heatmap(data_list,  nameList, figpath):
    """
    绘制agent停留区域热力图
    :return:
    """
    plt.rc('font', family='Arial')
    plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小

    x_tick = nameList
    y_tick = ['G_Area', 'A_Area']
    ALLdata = {}
    for i in range(len(data_list)):
        ALLdata[x_tick[i]] = data_list[i]
    ALLdata = pd.DataFrame(ALLdata, index=y_tick, columns=x_tick)
    sns.heatmap(ALLdata, cmap='GnBu')
    plt.xticks(fontproperties='Arial', size=10)
    plt.yticks(rotation=0, fontproperties='Arial', size=10)
    plt.savefig(figpath, dpi=DPI)
    plt.close()
