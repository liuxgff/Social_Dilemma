#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： LiuXG
# datetime： 2021/11/8 23:08 
# ide： PyCharm
import random

from RL_brain import QLearningTable
from env import PD


def base():
    q1 = QLearningTable(actions=['C', 'D'])
    q2 = QLearningTable(actions=['C', 'D'])
    env = PD()
    step = 1000

    epoch = 12

    for each_epoch in range(epoch):
        sum1 = 0
        sum2 = 0
        PD_state = {'CC': 0, 'CD': 0, 'DC': 0, 'DD': 0}
        state = random.sample(PD_state.keys(), 1)[0]
        # state = 'DD'
        agent1_action = {'C': 0, 'D': 0}
        agent2_action = {'C': 0, 'D': 0}

        for i in range(step):
            a1 = q1.choose_action(state)
            a2 = q2.choose_action(state)
            r1, r2 = env.get_reward(a1, a2)

            agent1_action[a1] += 1
            agent2_action[a2] += 1

            sum1 += r1
            sum2 += r2
            # state_1 = a1 + state[1]
            # state_2 = state[0] + a2
            state_ = a1 + a2

            if i > 2:
                q1.learn(state, a1, r1, state_)
                q2.learn(state, a2, r2, state_)

            state = state_

            PD_state[state] += 1
        print('epoch:', each_epoch)
        print(sum1, sum2, sum1+sum2)
        print(agent1_action)
        print(agent2_action)
        print(PD_state)

base()