#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： LiuXG
# datetime： 2021/11/8 22:27 
# ide： PyCharm

import numpy as np
import pandas as pd


class QLearningTable:
    def __init__(self, actions, Maxtarget, learning_rate=0.1, reward_decay=0.9, e_greedy=0.9):
        self.actions = actions  # a list
        self.maxlr = learning_rate
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.Maxtarget = Maxtarget
        self.q_table = pd.DataFrame(columns=self.actions, dtype=np.float64)

    def choose_action(self, observation):
        self.check_state_exist(observation)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        return action

    def set_learn_rate(self, current_reward):
        # self.lr = self.maxlr * max((self.Maxtarget - sum(current_reward)), 0) / self.Maxtarget
        # self.lr = self.maxlr * max((sum(current_reward) - self.Maxtarget), 0)
        self.lr = self.maxlr * (np.mean(current_reward) / self.Maxtarget) * (10**(-abs(self.Maxtarget - current_reward[-1])))

    def learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.loc[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, a] += self.lr * (q_target - q_predict)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )