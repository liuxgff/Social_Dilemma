# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/12 13:19
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import os
import pandas as pd
from Agent import Agent
from AgentsBrain import DeepQNetwork
from GameMap import Cleanup
from Draw import draw_list, draw_heatmap
import numpy as np


def createFolder(PATH):
    if os.path.exists(PATH):
        pass
    else:
        os.mkdir(PATH)


AVG = 5


def draw_apple_garbage(apple_garbage):
    """
    :param apple_garbage:
    :return:
    """
    y_label = 'Apples and Garbage'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称
    label_list = ['Apple', 'Garbage']
    figPath = Model_number + '/Apple&Garbage.pdf'  # 存储图像的地址
    draw_list(apple_garbage, y_label, x_label, figPath, label_list)  # 绘图


def draw_endApple_Num(appleList):
    """
    绘制每轮采集苹果的图像
    :param appleList:
    :return:
    """
    y_label = 'The number of apples'  # y坐标轴名称
    x_label = 'Episode'  # x轴名称
    figPath = Model_number + '/AppleNum.pdf'  # 存储图像的地址
    draw_list(appleList, y_label, x_label, figPath)  # 绘图


def draw_Agent_area(AgentArea, nameList, colorIndex=None):
    y_label = 'Position'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称
    figPath = Model_number + '/Agent_Area.pdf'  # 存储图像的地址
    draw_list(plot_list=AgentArea, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=nameList, colorIndex=colorIndex)


def run(gameRound, Steps):
    """
    :param Steps:
    :param gameRound:
    :return:
    """
    step = 0
    incomeList = []  # 每轮的总得分
    appleNumList = []  # 每轮采集苹果的数量
    incomeSum = 0  # 统计10轮内的得分
    appleNum = 0  # 统计10轮内的采集苹果的数量
    AgentsReward = [[0, 0] for _ in range(len(agentsList))]  # Agent的得分情况
    AgentArea = [[] for _ in range(len(agentsList))]  # agent每轮的移动轨迹
    learn_rate = [[] for _ in range(len(agentsList))]  # 每轮agent的学习率变换

    # 进行N轮游戏
    for Game_round in range(gameRound):
        apple_garbage = [[], []]  # 苹果和垃圾的变化
        AgentArea = [[] for _ in range(len(agentsList))]  # agent每轮的移动轨迹

        '测试开始'
        for R_step in range(Steps):
            cle.updateRate()  # 更新数据
            apple_garbage[0].append(cle.apple_N)  # 苹果数量
            apple_garbage[1].append(cle.garbage_N)  # 垃圾数量
            "Agents动作执行"
            for agentIndex, eachAgent in enumerate(agentsList):
                "存储agent当前的位置"
                AgentArea[agentIndex].append(cle.getAddressIndex(agentIndex))
                learn_rate[agentIndex].append(agentsBrainList[agentIndex].get_lr())

                '学习过程'
                observation = cle.getAgent(agentIndex)  # 获得当前状态
                action = agentsBrainList[agentIndex].choose_action(observation)  # 由网络选择一个动作

                # 判断该动作是否出界
                if cle.is_state(agentIndex, action):  # 如果下一个动作出界
                    nreward = -5
                    observation_ = observation
                else:
                    nreward = cle.move(agentIndex, action)  # 执行动作，并获取下一个状态
                    observation_ = cle.getAgent(agentIndex)  # 获得agent执行动作后的状态
                agentsBrainList[agentIndex].store_transition(observation,
                                                             action,
                                                             nreward,
                                                             observation_,
                                                             eachAgent.current_learning_rate)  # 存储记忆
                "进行学习"
                agentsBrainList[agentIndex].learn()

                # "随机选择动作"
                # action = np.random.randint(0, 4)
                # if not cle.is_state(agentIndex, action):  # 如果下一个动作出界
                #     cle.move(agentIndex, action)  # 执行动作，并获取下一个状态

            cle.updateApple()  # 苹果增长
            if R_step % 2 == 0:  # 每5步增长一次垃圾
                cle.updateGarbage()
            step += 1
            # cle.display()  # print地图内容
            # input()

        print("第%d轮：" % Game_round, "集体收益 = %d" % cle.income)
        incomeSum += cle.income
        appleNum += cle.appleNum

        if (Game_round+1) % AVG == 0:  # 记录10轮内的平均采集数量
            incomeList.append(incomeSum // AVG)  # 记录本轮采集的苹果总数
            appleNumList.append(appleNum // AVG)
            incomeSum = 0
            appleNum = 0
        for agentIndex, eachAgent in enumerate(agentsList):  # 初始化Agent
            AgentsReward[agentIndex][0] += eachAgent.ownAppleNum
            AgentsReward[agentIndex][1] += eachAgent.ownGarbageNum
            eachAgent.intitAgentData()
        cle.newMap()  # 初始化地图

    # "存储模型"
    # for _, eachBrain in enumerate(agentsBrainList):
    #     eachBrain.plot_cost()
    "显示每轮收益的图像"
    draw_endApple_Num([incomeList])
    "显示每轮采集苹果的图像"
    draw_endApple_Num([appleNumList])
    "存储苹果数量"
    pd.DataFrame(appleNumList, columns=['result']).to_csv(Model_number + '/AppleNum.csv', index=False)
    "存储收益"
    pd.DataFrame(incomeList, columns=['result']).to_csv(Model_number + '/ApplesCollection.csv', index=False)

    "存储每个Agent的得分"
    pd.DataFrame(AgentsReward, columns=['Apples', 'Garbage']).to_csv(Model_number + '/endReward.csv', index=False)

    "绘图"
    nameList = ['Agent ' + str(p+1) for p in range(len(agentsList))]
    draw_Agent_area(AgentArea, nameList, colorIndex=[0, 1, 2, 3, 4, 5])

    "Agent的活动区域"
    AgentArea = [list(i) for i in zip(AgentArea[0], AgentArea[1], AgentArea[2], AgentArea[3], AgentArea[4], AgentArea[5])]
    pd.DataFrame(data=AgentArea, columns=nameList).to_csv(Model_number + '/activate.csv', index=False)

    "学习率"
    learn_rate = [list(i) for i in zip(learn_rate[0], learn_rate[1], learn_rate[2], learn_rate[3], learn_rate[4], learn_rate[5])]
    pd.DataFrame(data=learn_rate, columns=nameList).to_csv(Model_number + '/learn_rate.csv', index=False)


if __name__ == "__main__":

    # Model_1 = [[10, 10, 10, 10, 10, 10], [0, 0, 0, 1, 1, 1], '同质低目标收益群体', 5]
    # Model_2 = [[80, 80, 80, 80, 80, 80], [0, 0, 0, 1, 1, 1], '同质高目标收益群体', 5]
    # Model_3 = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], '异质群体', 5]
    # Model_Random = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], '随机动作', 5]
    #
    # Model_FixedLR = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], 'Model_FixedLR', 5]
    #
    # Model_rewardLen_2 = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度2', 2]
    # Model_rewardLen_8 = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度8', 8]
    # Model_rewardLen_11 = [[10, 10, 10, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度11', 11]

    # tast = [No1, No2, No3, No4, No5, No6, No7, No8, No9, No10, No11, No12, No13, No14]
    # tast = [Model_Random]

    # tast = []
    # "异质群体实验: 苹果奖励=10, 高目标收益者=50, 低目标收益者=12.5, 初始位置固定[0,0,0,1,1,1]"
    # tast.append([[12.5, 12.5, 12.5, 50, 50, 50], [0, 0, 0, 1, 1, 1], '异质群体', 5, 10])
    # "同质高目标收益群体实验: 苹果奖励=10, 目标收益者均=50, 初始位置固定[0,0,0,1,1,1]"
    # tast.append([[50, 50, 50, 50, 50, 50], [0, 0, 0, 1, 1, 1], '同质高目标收益群体', 5, 10])
    # "同质低目标收益群体实验: 苹果奖励=10, 目标收益者均=12.5, 初始位置固定[0,0,0,1,1,1]"
    # tast.append([[12.5, 12.5, 12.5, 12.5, 12.5, 12.5], [0, 0, 0, 1, 1, 1], '同质低目标收益群体', 5, 10])

    "随机初始位置实验: 控制苹果奖励=10, 高目标收益者=50, 低目标收益者=12.5, 初始位置高-垃圾区域, 低-苹果区域"
    root = '随机初始位置'
    # loc = [1, 1, 1, 0, 0, 0]
    # path = ""+''.join([str(i) for i in loc])
    # path = os.path.join(root, path)
    # tast.append([[12.5, 12.5, 12.5, 50, 50, 50], loc, path, 5, 10])
    # "均在苹果区域"
    # loc = [1, 1, 1, 1, 1, 1]
    # path = ""+''.join([str(i) for i in loc])
    # path = os.path.join(root, path)
    # tast.append([[12.5, 12.5, 12.5, 50, 50, 50], loc, path, 5, 10])
    # "均在垃圾区域"
    # loc = [0, 0, 0, 0, 0, 0]
    # path = "" + ''.join([str(i) for i in loc])
    # path = os.path.join(root, path)
    # tast.append([[12.5, 12.5, 12.5, 50, 50, 50], loc, path, 5, 10])
    "随机初始位置实验: 控制苹果奖励=10, 高目标收益者=50, 低目标收益者=12.5, 初始位置随机"
    # for _ in range(1):
    #     loc = np.random.randint(0, 2, (1, 6))[0]
    #     path = ""+''.join([str(i) for i in loc])
    #     path = os.path.join(root, path)
    #     tast.append([[12.5, 12.5, 12.5, 50, 50, 50], loc, path, 5, 10])

    "对不同累计收益长度的比较: 苹果奖励为10, 高目标收益者=50, 低目标收益者为12.5"
    # tast = []
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=10/长度=' + str(i)
    #     tast.append([[12.5, 12.5, 12.5, 50, 50, 50], [0, 0, 0, 1, 1, 1], path, i, 10])
    # tast.append([[12.5, 12.5, 12.5, 50, 50, 50], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=10/长度=10', 10, 10])

    "对不同累计收益长度的比较: 苹果奖励为1, 高目标收益者=5, 低目标收益者为1.25"
    # tast = []
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=1/长度=' + str(i)
    #     tast.append([[1.25, 1.25, 1.25, 5, 5, 5], [0, 0, 0, 1, 1, 1], path, i, 1])
    # tast.append([[1.25, 1.25, 1.25, 5, 5, 5], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=1/长度=8', 8, 1])

    "对不同累计收益长度的比较: 苹果奖励为4, 高目标收益者=20, 低目标收益者为5"
    # tast = []
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=4/长度=' + str(i)
    #     tast.append([[5, 5, 5, 20, 20, 20], [0, 0, 0, 1, 1, 1], path, i, 4])
    # tast.append([[5, 5, 5, 20, 20, 20], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=4/长度=1', 1, 4])
    # tast.append([[5, 5, 5, 20, 20, 20], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=4/长度=8', 8, 4])

    "对不同累计收益长度的比较: 苹果奖励为8, 高目标收益者=40, 低目标收益者为10"
    # tast = []
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=8/长度=' + str(i)
    #     tast.append([[10, 10, 10, 40, 40, 40], [0, 0, 0, 1, 1, 1], path, i, 8])
    # tast.append([[10, 10, 10, 40, 40, 40], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=8/长度=1', 1, 8])
    # tast.append([[10, 10, 10, 40, 40, 40], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=8/长度=8', 8, 8])

    "对不同累计收益长度的比较: 苹果奖励为14, 高目标收益者=70, 低目标收益者为17.5"
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=14/长度=' + str(i)
    #     tast.append([[17.5, 17.5, 17.5, 70, 70, 70], [0, 0, 0, 1, 1, 1], path, i, 14])
    # tast.append([[17.5, 17.5, 17.5, 70, 70, 70], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=14/长度=1', 1, 14])
    # tast.append([[17.5, 17.5, 17.5, 70, 70, 70], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=14/长度=8', 8, 14])

    "对不同累计收益长度的比较: 苹果奖励为16, 高目标收益者=80, 低目标收益者为20"
    # tast = []
    # for i in range(2, 25, 4):
    #     path = '累计收益长度/苹果奖励=16/长度=' + str(i)
    #     tast.append([[20, 20, 20, 80, 80, 80], [0, 0, 0, 1, 1, 1], path, i, 4])
    # tast.append([[20, 20, 20, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=16/长度=5', 5, 16])
    # tast.append([[20, 20, 20, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=16/长度=1', 1, 16])
    # tast.append([[20, 20, 20, 80, 80, 80], [0, 0, 0, 1, 1, 1], '累计收益长度/苹果奖励=16/长度=8', 8, 16])

    "固定苹果的奖励为10, 根据累计收益长度和agent目标收益之间的关系，测试不同的目标奖励策略"
    tast = []
    tast.append([[4, 4, 4, 16, 16, 16], [0, 0, 0, 1, 1, 1], '不同的目标收益/高目标收益=16', 2, 10])
    tast.append([[10, 10, 10, 40, 40, 40], [0, 0, 0, 1, 1, 1], '不同的目标收益/高目标收益=40', 5, 10])
    tast.append([[16, 16, 16, 64, 64, 64], [0, 0, 0, 1, 1, 1], '不同的目标收益/高目标收益=64', 8, 10])
    tast.append([[22, 22, 22, 88, 88, 88], [0, 0, 0, 1, 1, 1], '不同的目标收益/高目标收益=88', 11, 10])


    for each_tast in tast:
        'agent信息'
        agentsNum = 6  # 玩家个数
        agentsList = []  # 玩家列表
        agentsBrainList = []  # agent训练网络
        MaxSatisfaction = each_tast[0]

        '模型信息'
        Model_number = 'Result/' + each_tast[2]
        createFolder(Model_number)
        agentInitArea = each_tast[1]

        'agent实例化'
        for i in range(agentsNum):
            Name = chr(i + ord('A'))
            agentsList.append(Agent(Name, MaxSatisfaction[i], rewardLen=each_tast[3], initAddress=agentInitArea[i]))
            # agentsList.append(Agent(Name, MaxSatisfaction[i], rewardLen=5))
            agentsBrainList.append(
                DeepQNetwork(
                             batch_size=1,
                             agentName=Name,
                             memory_size=500,
                             savePath=Model_number + '/' + Name))

        '地图信息'
        cle = Cleanup(agentsList=agentsList, InitRandAddress=True, appleReward=each_tast[4])  # 游戏地图实例
        # cle = Cleanup(agentsList=agentsList)  # 游戏地图实例
        print('tast:', each_tast[2])
        '运行游戏'
        run(305, 100)
