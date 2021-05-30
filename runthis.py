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


def createFolder(PATH):
    if os.path.exists(PATH):
        pass
    else:
        os.mkdir(PATH)


def draw_apple_garbage(apple_garbage):
    """
    :param apple_garbage:
    :return:
    """
    y_label = 'apples and garbage'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称
    label_list = ['Apple', 'Garbage']
    figPath = Model_number + '/Apple&Garbage.png'  # 存储图像的地址
    draw_list(apple_garbage, y_label, x_label, figPath, label_list)  # 绘图


def draw_endApple_Num(appleList):
    """
    绘制每轮采集苹果的图像
    :param appleList:
    :return:
    """
    y_label = 'The number of apples'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称
    figPath = Model_number + '/AppleNum.png'  # 存储图像的地址
    draw_list(appleList, y_label, x_label, figPath)  # 绘图


def draw_Agent_area(AgentArea, nameList):
    y_label = 'Position'  # y坐标轴名称
    x_label = 'Steps'  # x轴名称
    figPath = Model_number + '/Agent_Area.png'  # 存储图像的地址
    draw_list(plot_list=AgentArea, y_lable=y_label, x_lable=x_label, figPath=figPath, label_list=nameList)


def run(gameRound, Steps):
    """
    :param Steps:
    :param gameRound:
    :return:
    """
    step = 0
    endAppleList = []  # 每轮采集苹果的数量
    AppleSum = 0  # 统计10轮内的采集苹果的数量
    # 进行N轮游戏
    for Game_round in range(gameRound):
        apple_garbage = [[], []]  # 苹果和垃圾的变化
        AgentArea = [[] for _ in range(len(agentsList))]  # agent每轮的移动轨迹
        '测试开始'
        for R_step in range(Steps):
            cle.updateRate()  # 更新数据
            "Agents动作执行"
            for agentIndex, eachAgent in enumerate(agentsList):
                apple_garbage[0].append(cle.apple_N)  # 苹果数量
                apple_garbage[1].append(cle.garbage_N)  # 垃圾数量
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
                eachAgent.update_learning_rate()  # 更新agent学习率
                agentsBrainList[agentIndex].learn()

                "存储agent当前的位置"
                AgentArea[agentIndex].append(cle.getAddressIndex(agentIndex))

            cle.updateApple()  # 苹果增长
            if R_step % 2 == 0:  # 每5步增长一次垃圾
                cle.updateGarbage()
            step += 1
            # cle.display()  # print地图内容
            # input()

        print("第%d轮：" % Game_round, "收获苹果个数 = %d" % cle.endAppleNum)
        AppleSum += cle.endAppleNum
        if (Game_round+1) % 10 == 0:  # 记录10轮内的平均采集数量
            endAppleList.append(AppleSum // 10)  # 记录本轮采集的苹果总数
            AppleSum = 0
        for eachAgent in agentsList:  # 初始化Agent
            eachAgent.intitAgentData()
        cle.newMap()  # 初始化地图

    "存储模型"
    for _, eachBrain in enumerate(agentsBrainList):
        eachBrain.plot_cost()

    "存储苹果数量"
    pd.DataFrame(endAppleList, columns=['result']).to_csv(Model_number + '.csv', index=False)

    "绘图"
    draw_endApple_Num([endAppleList])  # 最后采集苹果总数
    draw_apple_garbage(apple_garbage)  # 一轮中苹果和垃圾数量的变化
    nameList = ['Agent ' + str(p+1) for p in range(len(agentsList))]
    draw_Agent_area(AgentArea, nameList)


if __name__ == "__main__":
    'agent信息'
    agentsNum = 6  # 玩家个数
    agentsList = []  # 玩家列表
    agentsBrainList = []  # agent训练网络
    MaxSatisfaction = [10, 10, 10, 80, 80, 80]  # 玩家满足度

    '模型信息'
    number = 1  # 模型编号
    Model_number = 'Model_' + str(number)
    createFolder(Model_number)
    agentInitArea = [0, 0, 0, 1, 1, 1]

    'agent实例化'
    for i in range(agentsNum):
        Name = chr(i + ord('A'))
        agentsList.append(Agent(Name, MaxSatisfaction[i], rewardLen=5, initAddress=agentInitArea[i]))
        # agentsList.append(Agent(Name, MaxSatisfaction[i], rewardLen=5))
        agentsBrainList.append(
            DeepQNetwork(
                         batch_size=1,
                         agentName=Name,
                         memory_size=500,
                         savePath=Model_number + '/' + Name))

    '地图信息'
    cle = Cleanup(agentsList=agentsList, InitRandAddress=True)  # 游戏地图实例
    # cle = Cleanup(agentsList=agentsList)  # 游戏地图实例

    run(300, 100)  # 运行游戏
