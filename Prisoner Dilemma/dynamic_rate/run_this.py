#!/usr/bin/env python
# -*- coding: utf-8
# author： LiuXG
# datetime： 2021/11/8 23:08 
# ide： PyCharm
import random

import pandas as pd

from RL_brain import QLearningTable
from env import PD


def dynamic():
    q1 = QLearningTable(actions=['C', 'D'], Maxtarget=3)
    q2 = QLearningTable(actions=['C', 'D'], Maxtarget=3)

    reward_len = 3

    env = PD()
    step = 1200

    epoch = 12
    result = []
    cc_count = []
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

            state_ = a1 + a2

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
            if i > reward_len:
                q1.learn(state, a1, r1, state_)
                q2.learn(state, a2, r2, state_)

            state = state_
            PD_state[state] += 1
        result.append(sum1 + sum2)
        cc_count.append(agent1_action['C'] + agent2_action['C'])
        print('epoch:', each_epoch)
        print(sum1, sum2, sum1+sum2)
        print(q1.q_table)
        print(q2.q_table)
        print(agent1_action)
        print(agent2_action)
        print(PD_state)
    pd.DataFrame(result, columns=['result']).to_csv('result.csv', index=False)
    pd.DataFrame(cc_count, columns=['count']).to_csv('cc_count.csv', index=False)

dynamic()