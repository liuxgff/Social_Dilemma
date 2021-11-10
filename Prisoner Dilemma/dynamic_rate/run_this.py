#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： LiuXG
# datetime： 2021/11/8 23:08 
# ide： PyCharm
import random

from RL_brain import QLearningTable
from env import PD


def dynamic():
    q1 = QLearningTable(actions=['C', 'D'], Maxtarget=3)
    q2 = QLearningTable(actions=['C', 'D'], Maxtarget=8)

    reward_len = 2

    env = PD()
    step = 1000

    epoch = 12

    for each_epoch in range(epoch):
        current_reward1 = []
        current_reward2 = []

        agent1_action = {'C': 0, 'D': 0}
        agent2_action = {'C': 0, 'D': 0}

        PD_state = {'CC': 0, 'CD': 0, 'DC': 0, 'DD': 0}
        # state = random.sample(PD_state.keys(), 1)[0]
        state = 'CC'

        sum1 = 0
        sum2 = 0
        for i in range(step):
            a1 = q1.choose_action(state)
            a2 = q2.choose_action(state)
            r1, r2 = env.get_reward(a1, a2)

            agent1_action[a1] += 1
            agent2_action[a2] += 1

            state_1 = a1 + state[1]
            state_2 = state[0] + a2

            # 更新agent的学习率
            current_reward1.append(r1)
            current_reward2.append(r2)

            if len(current_reward1) > reward_len:
                current_reward1.pop(0)
                current_reward2.pop(0)

            q1.set_learn_rate(current_reward1)
            q2.set_learn_rate(current_reward2)

            sum1 += r1
            sum2 += r2
            if i > 2:
                q1.learn(state, a1, r1, state_1)
                q2.learn(state, a2, r2, state_2)

            state = a1 + a2
            PD_state[state] += 1

        print('epoch:', each_epoch)
        print(sum1, sum2, sum1+sum2)
        print(agent1_action)
        print(agent2_action)
        print(PD_state)


dynamic()