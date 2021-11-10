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
              label_list=['Heterogeneous', 'Fixed learning rate', 'Random action'], colorIndex=[2, 5, 4], allReward=True)


def compare_heterogeneous_homogeneous():
    "异质性群体与同质性群体比较"
    compareList = [getData('同质低目标收益群体'), getData('同质高目标收益群体'), getData('异质群体'), getData('随机动作')]
    draw_list(plot_list=compareList, y_lable='Collective return', x_lable='Episode', figPath='异质性群体与同质性群体.svg',
              label_list=['Homogeneous low', 'Homogeneous high', 'Heterogeneous', 'Random action'], colorIndex=[0, 1, 2, 4], allReward=True)


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
    root = os.path.join(root, 'Result/累计收益长度/苹果奖励=16')
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

    plt.rc('font', family=FONT)  # 图像字体
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

    plt.savefig(os.path.join(root, '比较不同累计收益长度.svg'), bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.savefig(os.path.join(root, '比较不同累计收益长度.pdf'), bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


def compare_all_lenReward():
    """
    比较所有不同累计收益长度的比较
    :return:
    """
    root = os.getcwd()
    root = os.path.join(root, 'Result/累计收益长度/')
    alldata_path = {}
    for each_reward in os.listdir(root):
        temp = each_reward.split('=')
        alldata_path[int(temp[1])] = each_reward
    alldata_path = sorted(alldata_path.items(), key=lambda item: item[0])
    data_dict = {}
    len_path = ['长度=1', '长度=2', '长度=5', '长度=6', '长度=8', '长度=10', '长度=14', '长度=18', '长度=22']

    "设置画板"
    plt.figure(1)  # 图像编号
    y_lable = 'Number of apples collected'
    x_lable = 'cumulative reward'
    plt.rc('font', family=FONT)  # 图像字体
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
    label_list = ['apple_reward=1', 'apple_reward=4', 'apple_reward=8', 'apple_reward=10', 'apple_reward=14', 'apple_reward=16']  # 图例
    colors = ['darkorange', 'r', 'b', 'g', 'purple', 'y']
    markers = ['^', 's', 'o', 'd', 'X', '.']
    different_reward = []
    for _, path in alldata_path:
        reward_path = os.path.join(root, path)
        mean_list = []
        avg_list = []
        for each_len in len_path:
            dataPath = os.path.join(reward_path, each_len)
            data = list(pd.read_csv(dataPath + '/ApplesCollection.csv', index_col=False)['result'])
            mean_list.append(np.mean(data))
            avg_list.append(np.std(data))

        different_reward.append([mean_list, avg_list])
    xlen = [1, 2, 5, 6, 8, 10, 14, 18, 22]
    for index, eachPlot in enumerate(different_reward):
        plt.plot(np.arange(len(xlen)), eachPlot[0], color=colors[index], linewidth=1.5, marker=markers[index])
        # plt.errorbar(np.arange(len(xlen)), eachPlot[0], eachPlot[1], color=colors[index], ecolor=colors[index], linewidth=1.5, marker=markers[index])
    plt.xticks(np.arange(len(xlen)), xlen)

    ax.set_ylabel(y_lable)  # y轴标签
    ax.set_xlabel(x_lable)  # x轴标签
    # 图例设置
    font1 = {'family': FONT,
             'weight': 'normal',
             'size': 12,
             }
    ax.legend(label_list, bbox_to_anchor=(1.01, 0), loc=3, borderaxespad=0, prop=font1)

    plt.savefig('compare_diff.svg', bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.savefig('compare_diff.pdf', bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


def draw_activate():
    """
    活动区域图
    :return:
    """
    root = os.path.join(os.getcwd(), 'Result')

    plt.figure(1)  # 图像编号
    y_label = 'Position'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称

    colors2 = ['darkorange', 'r',  'b', 'darkgreen', 'darkslategray', 'purple']
    FillColor2 = ['tan', 'lightcoral', 'royalblue', 'forestgreen', 'darkcyan', 'violet']
    nameList = ['Agent ' + str(p+1) for p in range(6)]
    shadow = 18

    plt.rc('font', family=FONT)  # 图像字体
    # plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    # plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小

    "Heterogeneous"
    data = pd.read_csv(os.path.join(root, '异质群体/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(221)
    ax.grid()  # 生成网格

    # fig1.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    # fig1.set_size_inches(WIDTH, HEIGHT)  # 图像大小
    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    ax.set_ylabel(y_label)  # y轴标签
    # ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('Heterogeneous')

    "Homogeneous high"
    data = pd.read_csv(os.path.join(root, '同质高目标收益群体/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(222)
    ax.grid()  # 生成网格

    # fig1.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    # fig1.set_size_inches(WIDTH, HEIGHT)  # 图像大小
    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    # ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('Homogeneous high')

    "Homogeneous low"
    data = pd.read_csv(os.path.join(root, '同质低目标收益群体/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(223)
    ax.grid()  # 生成网格

    # fig1.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    # fig1.set_size_inches(WIDTH, HEIGHT)  # 图像大小
    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    ax.set_ylabel(y_label)  # y轴标签
    ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('Homogeneous low')

    "Random action"
    data = pd.read_csv(os.path.join(root, '随机动作/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(224)
    ax.grid()  # 生成网格

    # fig1.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP)  # 画布范围设置: 离左侧.14,距离下方.18,右侧.97,上方.97
    # fig1.set_size_inches(WIDTH, HEIGHT)  # 图像大小
    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('Random action')

    # 图例设置
    font1 = {'family': FONT,
             'weight': 'normal',
             'size': 10,
             }
    plt.legend(nameList, bbox_to_anchor=(1.04, 0), loc=3, borderaxespad=0, prop=font1)
    plt.tight_layout()
    plt.savefig("activate.svg", bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.savefig("activate.pdf", bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


def draw_random_position():
    """
    随机位置
    :return:
    """
    root = os.path.join(os.getcwd(), 'Result')

    plt.figure(1)  # 图像编号
    plt.figure(figsize=(WIDTH, HEIGHT))  # 自定义画布大小(width,height)
    plt.rc('font', family=FONT)  # 图像字体
    # plt.rc('xtick', labelsize=LABELSIZE)  # x轴刻度大小
    # plt.rc('ytick', labelsize=LABELSIZE)  # y轴刻度大小
    plt.rc('axes', labelsize=LABELSIZE)  # 坐标轴字体大小

    y_label = 'Position'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称

    colors2 = ['darkorange', 'r', 'b', 'darkgreen', 'darkslategray', 'purple']
    FillColor2 = ['tan', 'lightcoral', 'royalblue', 'forestgreen', 'darkcyan', 'violet']
    nameList = ['Agent ' + str(p + 1) for p in range(6)]
    shadow = 12

    # 图例设置
    font1 = {'family': FONT,
             'weight': 'normal',
             'size': 12,
             }

    "000111"
    data = pd.read_csv(os.path.join(root, '异质群体/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(231)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    ax.set_ylabel(y_label, font1)  # y轴标签
    # ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('position-1', fontsize=LABELSIZE)

    "111000"
    data = pd.read_csv(os.path.join(root, '随机初始位置/111000/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(232)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    # ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('position-2', fontsize=LABELSIZE)

    "000000"
    data = pd.read_csv(os.path.join(root, '随机初始位置/000000/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(233)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    # ax.set_xlabel(x_label)  # x轴标签
    ax.set_title('position-3', fontsize=LABELSIZE)

    "111111"
    data = pd.read_csv(os.path.join(root, '随机初始位置/111111/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(234)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    ax.set_ylabel(y_label, font1)  # y轴标签
    ax.set_xlabel(x_label, font1)  # x轴标签
    ax.set_title('position-4', fontsize=LABELSIZE)

    "010100"
    data = pd.read_csv(os.path.join(root, '随机初始位置/010100/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(235)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    ax.set_xlabel(x_label, font1)  # x轴标签
    ax.set_title('position-5', fontsize=LABELSIZE)

    "110110"
    data = pd.read_csv(os.path.join(root, '随机初始位置/110110/activate.csv'))
    data = [list(data[i]) for i in data]
    ax = plt.subplot(236)
    ax.grid()  # 生成网格

    for i in range(len(data)):
        updata = [j + shadow for j in data[i]]
        downdata = [j - shadow for j in data[i]]
        plt.plot(np.arange(len(data[i])), data[i], color=colors2[i], linewidth=1.1)
        plt.fill_between(np.arange(len(data[i])), downdata, updata, facecolor=FillColor2[i], alpha=0.3)
    # ax.set_ylabel(y_label)  # y轴标签
    ax.set_xlabel(x_label, font1)  # x轴标签
    ax.set_title('position-6', fontsize=LABELSIZE)


    plt.legend(nameList, bbox_to_anchor=(1.04, 0), loc=3, borderaxespad=0, prop=font1)
    plt.tight_layout()
    plt.savefig("random_position_activate.svg", bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.savefig("random_position_activate.pdf", bbox_inches='tight')  # 图像存储, 设置分辨率
    plt.close()


# compare_rewardLen()
compare_all_lenReward()
# compare_heterogeneous_homogeneous()  # 异质群体与同质群体比较
# draw_activate()  # 异质群体与同质群体的活动路线
# compare_de_fixed()  # 动态与固定学习率比较

# draw_random_position()  # 随机位置的活动状态


