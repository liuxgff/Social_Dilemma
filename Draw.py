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
LEFT = 0.1  # 画布设置，距离左侧大小
BOTTOM = 0.14  # 距离底部大小
RIGHT = 0.77  # 距离右侧大小
TOP = 0.98  # 距离上端大小

# 设置图像大小(1英尺=2.54cm)
WIDTH = 7.5
HEIGHT = WIDTH / 1.5
# 图像像素
DPI = 400


# 折线图绘图设置(数据列表, y轴名称, x轴名称, 图像存储地址, 标签列表)
def draw_list(plot_list=None, y_lable='', x_lable='', figPath='', label_list=None, colorIndex=None):
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

    for i in range(len(plot_list)):
        updata = [j + 18 for j in plot_list[i]]
        downdata = [j - 18 for j in plot_list[i]]
        if not colorIndex:
            plt.plot(np.arange(len(plot_list[i])), plot_list[i], color=colors1[i], linewidth=1.1)
            plt.fill_between(np.arange(len(plot_list[i])), downdata, updata, facecolor=FillColor1[i], alpha=0.3)
        else:
            plt.plot(np.arange(len(plot_list[i])), plot_list[i], color=colors2[colorIndex[i]], linewidth=1.1)
            plt.fill_between(np.arange(len(plot_list[i])), downdata, updata, facecolor=FillColor2[colorIndex[i]], alpha=0.3)
    ax.set_ylabel(y_lable)  # y轴标签
    ax.set_xlabel(x_lable)  # x轴标签
    ax.set_xticklabels([-50, 0, 50, 100, 150, 200, 250, 300])
    # 图例设置
    if label_list:
        ax.legend(label_list, bbox_to_anchor=(1.01, 0), loc=3, borderaxespad=0)
    plt.savefig(figPath, dpi=DPI)  # 图像存储, 设置分辨率
    plt.close()


def draw_heatmap(data_list, figpath):
    """
    绘制agent停留区域热力图
    :return:
    """
    plt.rc('font', family='Arial')
    plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小

    apple_data = list(data_list['data'])
    apple_data = pd.DataFrame(apple_data, index=['Agent1', 'Agent2', 'Agent3', 'Agent4', 'Agent5', 'Agent6'],
                              columns=['Income'])
    sns.heatmap(apple_data, cmap='YlOrRd', square=True, vmin=0, vmax=1)
    plt.xticks(fontproperties='Arial', size=LABELSIZE)
    plt.yticks(rotation=0, fontproperties='Arial', size=LABELSIZE)
    plt.savefig(figpath, dpi=DPI)
    plt.close()
