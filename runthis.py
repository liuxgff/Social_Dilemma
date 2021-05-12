# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/12 13:19
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import os
from Agent import Agent
from AgentsBrain import DeepQNetwork
from GameMap import Cleanup
from Draw import draw_list


def createFolder(PATH):
    if os.path.exists(PATH):
        pass
    else:
        os.mkdir(PATH)


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


def run(gameRound, Steps):
    """
    :param Steps:
    :param gameRound:
    :return:
    """
    step = 0
    endAppleList = []  # 每轮采集苹果的数量
    # 进行N轮游戏
    for Game_round in range(gameRound):
        '测试开始'
        for R_step in range(Steps):
            cle.updateRate()  # 更新数据
            "Agents动作执行"
            for agentIndex, eachAgent in enumerate(agentsList):

                observation = cle.getAgent(agentIndex)  # 获得当前状态

                action = agentsBrainList[agentIndex].choose_action(observation)  # 由网络选择一个动作

                # 判断该动作是否出界
                if cle.is_state(agentIndex, action):  # 如果下一个动作出界
                    nreward = -20
                    observation_ = observation
                else:
                    nreward = cle.move(agentIndex, action)  # 执行动作，并获取下一个状态
                    observation_ = cle.getAgent(agentIndex)  # 获得agent执行动作后的状态

                agentsBrainList[agentIndex].store_transition(observation, action, nreward, observation_)  # 存储记忆

                if step > 200 and step % 5 == 0:  # 进行学习
                    agentsBrainList[agentIndex].learn(eachAgent.current_learning_rate)
                    eachAgent.update_learning_rate()

                cle.updateApple()  # 苹果增长
                if R_step % 5 == 0:  # 每5步增长一次垃圾
                    cle.updateGarbage()

                # cle.display()  # print地图内容
                # input()
            step += 1
        print("第%d轮：" % Game_round, "收获苹果个数 = %d" % cle.endAppleNum)
        endAppleList.append(cle.endAppleNum)  # 记录本轮采集的苹果总数
        cle.newMap()  # 初始化地图
        for eachAgent in agentsList:  # 初始化Agent
            eachAgent.intitAgentData()

    "存储模型"
    for _, eachBrain in enumerate(agentsBrainList):
        eachBrain.plot_cost()

    draw_endApple_Num([endAppleList])


if __name__ == "__main__":
    'agent信息'
    agentsNum = 6  # 玩家个数
    agentsList = []  # 玩家列表
    agentsBrainList = []  # agent训练网络
    MaxSatisfaction = [20, 20, 20, 200, 200, 200]  # 玩家满足度

    '模型信息'
    number = 1  # 模型编号
    Model_number = 'Model_' + str(number)
    createFolder(Model_number)

    'agent实例化'
    for i in range(agentsNum):
        Name = chr(i + ord('A'))
        agentsList.append(Agent(Name, MaxSatisfaction[i]))
        agentsBrainList.append(
            DeepQNetwork(
                         agentName=Name,
                         savePath=Model_number + '/' + Name))

    '地图信息'
    cle = Cleanup(agentsList=agentsList)  # 游戏地图实例

    run(500, 150)  # 运行游戏
