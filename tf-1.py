# -*- coding: UTF-8 -*-
"""=================================================
@Author ：Liu XingGuang
@Date   ：2021/5/10 15:20
@Email  ：liuxgemail@163.com
@Description ：
=================================================="""
import numpy as np
import tensorflow as tf

np.random.seed(1)  # 生成随机数种子
tf.set_random_seed(1)


# Deep Q Network off-policy
class DeepQNetwork:
    def __init__(
            self,
            n_actions=4,  # Agent的上下左右动作
            n_features=75,  # 训练网络的输入大小，默认100
            learning_rate=0.001,  # 学习率
            reward_decay=0.9,  # 奖励衰减值
            e_greedy=0.9,  # 探索的概率
            replace_target_iter=300,  # 每300步交换网络权重
            memory_size=500,  # 训练网络的记忆库大小
            batch_size=32,  # 选取训练记忆大小
            e_greedy_increment=None,
            output_graph=False,
            agentName=None,
            savePath=None
    ):
        self.n_actions = n_actions
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon_max = e_greedy
        self.replace_target_iter = replace_target_iter
        self.memory_size = memory_size
        self.batch_size = batch_size
        self.epsilon_increment = e_greedy_increment
        self.epsilon = 0 if e_greedy_increment is not None else self.epsilon_max
        self.agentName = agentName
        self.savePath = savePath

        # total learning step
        self.learn_step_counter = 0

        # initialize zero memory [s, a, r, s_]
        self.memory = np.zeros((self.memory_size, n_features * 2 + 2))

        # consist of [target_net, evaluate_net]
        self._build_net()
        t_params = tf.get_collection(self.agentName + '_target_net_params')
        e_params = tf.get_collection(self.agentName + '_eval_net_params')
        self.replace_target_op = [tf.assign(t, e) for t, e in zip(t_params, e_params)]

        # 保存模型
        self.saver = tf.compat.v1.train.Saver()

        self.sess = tf.Session()

        if output_graph:
            tf.summary.FileWriter("logs/", self.sess.graph)

        self.inputsess()
        self.cost_his = []

    # 检测是否有训练好的模型
    def inputsess(self):
        self.sess.run(tf.compat.v1.global_variables_initializer())  # 初始化变量
        checkpoint = tf.train.get_checkpoint_state(self.savePath)
        if checkpoint and checkpoint.model_checkpoint_path:
            self.saver.restore(self.sess, checkpoint.model_checkpoint_path)
            print('Successfully loaded')
        else:
            print('Load failed')

    def _build_net(self):
        # ------------------ build evaluate_net ------------------
        self.s = tf.placeholder(tf.float32, [None, self.n_features], name='A_s')  # input
        self.q_target = tf.placeholder(tf.float32, [None, self.n_actions], name='A_Q_target')  # for calculating loss
        with tf.variable_scope(self.agentName + '_eval_net'):
            # c_names(collections_names) are the collections to store variables
            c_names, n_l1, w_initializer, b_initializer = \
                [self.agentName + '_eval_net_params', tf.GraphKeys.GLOBAL_VARIABLES], 32, \
                tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)  # config of layers
            # first layer. collections is used later when assign to target net
            with tf.variable_scope(self.agentName + '_l1'):
                w1 = tf.get_variable(self.agentName + '_w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable(self.agentName + '_b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s, w1) + b1)
            # second layer. collections is used later when assign to target net
            with tf.variable_scope(self.agentName + '_l2'):
                w2 = tf.get_variable(self.agentName + '_w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable(self.agentName + '_b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_eval = tf.matmul(l1, w2) + b2

        with tf.variable_scope(self.agentName + '_loss'):
            self.loss = tf.reduce_mean(tf.squared_difference(self.q_target, self.q_eval))
        with tf.variable_scope(self.agentName + '_train'):
            self._train_op = tf.train.RMSPropOptimizer(self.lr).minimize(self.loss)

        # ------------------ build target_net ------------------
        self.s_ = tf.placeholder(tf.float32, [None, self.n_features], name=self.agentName + '_s_')  # input
        with tf.variable_scope(self.agentName + '_target_net'):
            # c_names(collections_names) are the collections to store variables
            c_names = [self.agentName + '_target_net_params', tf.GraphKeys.GLOBAL_VARIABLES]
            # first layer. collections is used later when assign to target net
            with tf.variable_scope(self.agentName + '_l1'):
                w1 = tf.get_variable(self.agentName + '_w1', [self.n_features, n_l1], initializer=w_initializer, collections=c_names)
                b1 = tf.get_variable(self.agentName + '_b1', [1, n_l1], initializer=b_initializer, collections=c_names)
                l1 = tf.nn.relu(tf.matmul(self.s_, w1) + b1)
            # second layer. collections is used later when assign to target net
            with tf.variable_scope(self.agentName + '_l2'):
                w2 = tf.get_variable(self.agentName + '_w2', [n_l1, self.n_actions], initializer=w_initializer, collections=c_names)
                b2 = tf.get_variable(self.agentName + '_b2', [1, self.n_actions], initializer=b_initializer, collections=c_names)
                self.q_next = tf.matmul(l1, w2) + b2

    def store_transition(self, s, a, r, s_):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0

        transition = np.hstack((s, [a, r], s_))

        # replace the old memory with new memory
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = transition

        self.memory_counter += 1

    def choose_action(self, observation):
        # to have batch dimension when feed into tf placeholder
        observation = observation[np.newaxis, :]
        if np.random.uniform() < self.epsilon:
            # forward feed the observation and get q value for every actions
            actions_value = self.sess.run(self.q_eval, feed_dict={self.s: observation})
            action = np.argmax(actions_value)
        else:
            action = np.random.randint(0, self.n_actions)
        return action

    def learn(self):
        # check to replace target parameters
        if self.learn_step_counter % self.replace_target_iter == 0:
            self.sess.run(self.replace_target_op)

        # sample batch memory from all memory
        if self.memory_counter > self.memory_size:
            sample_index = np.random.choice(self.memory_size, size=self.batch_size)
        else:
            sample_index = np.random.choice(self.memory_counter, size=self.batch_size)
        batch_memory = self.memory[sample_index, :]

        q_next, q_eval = self.sess.run(
            [self.q_next, self.q_eval],
            feed_dict={
                self.s_: batch_memory[:, -self.n_features:],  # fixed params
                self.s: batch_memory[:, :self.n_features],  # newest params
            })

        # change q_target w.r.t q_eval's action
        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)
        eval_act_index = batch_memory[:, self.n_features].astype(int)
        reward = batch_memory[:, self.n_features + 1]

        q_target[batch_index, eval_act_index] = reward + self.gamma * np.max(q_next, axis=1)
        # train eval network
        _, self.cost = self.sess.run([self._train_op, self.loss],
                                     feed_dict={self.s: batch_memory[:, :self.n_features],
                                                self.q_target: q_target})
        self.cost_his.append(self.cost)

        self.epsilon = self.epsilon + self.epsilon_increment if self.epsilon < self.epsilon_max else self.epsilon_max
        self.learn_step_counter += 1

    # 保存训练模型
    def save_sess(self):
        self.saver.save(self.sess, self.savePath + '/' + 'MAS')

    def plot_cost(self):
        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(self.cost_his)), self.cost_his)
        plt.title(self.agentName)
        plt.ylabel('Cost')
        plt.xlabel('training steps')
        # plt.show()
        plt.imsave(self.savePath + '/loss.jpg')