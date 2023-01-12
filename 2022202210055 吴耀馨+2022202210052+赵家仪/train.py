# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import random
import copy
import time

# import draw
from container import *
from data import *
# from draw import *

# 1. Define some Hyper Parameters
EPSILON = 0.9  # epsilon used for epsilon greedy approach
BATCH_SIZE = 16  # batch size of sampling process from buffer
LR = 0.0001  # learning rate
GAMMA = 0.9  # discount factor
TARGET_NETWORK_REPLACE_FREQ = 100  # How frequently target netowrk updates
MEMORY_CAPACITY = 2000  # The capacity of experience replay buffer
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 2. Random generate box data
solution = [[(91, 54, 45, 32), (105, 77, 72, 24), (79, 78, 48, 30)],
[(108, 76, 30, 24), (110, 43, 25, 7), (92, 81, 55, 22), (81, 33, 28, 13), (120, 99, 73, 15)],
[(88, 54, 39, 16), (94, 54, 36, 14), (87, 77, 43, 20), (100, 80, 72, 16), (83, 40, 36, 6),(91, 54, 22, 15), (109, 58, 54, 17), (94, 55, 30, 9)],
[(86, 84, 45, 18), (81, 45, 34, 19), (70, 54, 37, 13), (71, 61, 52, 16), (78, 73, 40, 10),(69, 63, 46, 13), (72, 67, 56, 10), (75, 75, 36, 8), (94, 88, 50, 12), (65, 51, 50, 13)],
[(108, 76, 30, 12), (110, 43, 25, 12), (92, 81, 55, 6), (81, 33, 28, 9), (120, 99, 73, 5), (111, 70, 48, 12), (98, 72, 46, 9), (95, 66, 31, 10), (85, 84, 30, 8), (71, 32, 25, 3), (36, 34, 25, 10), (97, 67, 62, 7), (33, 25, 23, 7), (95, 27, 26, 10), (94, 81, 44, 9)]]

def random_generate():
    idx = np.random.randint(0,len(solution))
    box_list = solution[idx]
    gen_box_order = []
    while True:
        index = np.random.randint(0, len(box_list))
        box_list[index] = (box_list[index][0], box_list[index][1], box_list[index][2], box_list[index][3]-1)
        gen_box_order.append((box_list[index][0], box_list[index][1], box_list[index][2]))
        if box_list[index][3] == 0:
            box_list.pop(index)
        if len(box_list) == 0:
            break
    return gen_box_order


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def standardization(data):
    mu = np.mean(data)
    sigma = np.std(data)
    return (data - mu) / sigma

# 3. Define the network used in both target net and the net for training
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()   # 继承__init__功能
        ## 第一层卷积
        self.conv1 = nn.Sequential(
            # 输入[2,587,233]
            nn.Conv2d(
                in_channels=2,    # 输入图片的高度
                out_channels=16,  # 输出图片的高度
                kernel_size=3,    # 5x5的卷积核，相当于过滤器
                stride=1,         # 卷积核在图上滑动，每隔一个扫一次
                padding=1,        # 给图外边补上0
            ),
            # 经过卷积层 输出[16,28,28] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)   # 经过池化 输出[16,14,14] 传入下一个卷积
        )
        ## 第二层卷积
        self.conv2 = nn.Sequential(
            nn.Conv2d(
                in_channels=16,    # 同上
                out_channels=32,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            # 经过卷积 输出[32, 14, 14] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)  # 经过池化 输出[32,7,7] 传入输出层
        )
        ## 第三层卷积
        self.conv3 = nn.Sequential(
            nn.Conv2d(
                in_channels=32,  # 同上
                out_channels=64,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            # 经过卷积 输出[32, 14, 14] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)  # 经过池化 输出[32,7,7] 传入输出层
        )
        ## 第四层卷积
        self.conv4 = nn.Sequential(
            nn.Conv2d(
                in_channels=64,  # 同上
                out_channels=128,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            # 经过卷积 输出[32, 14, 14] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)  # 经过池化 输出[32,7,7] 传入输出层
        )
        ## 第五层卷积
        self.conv5 = nn.Sequential(
            nn.Conv2d(
                in_channels=128,  # 同上
                out_channels=256,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            # 经过卷积 输出[32, 14, 14] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)  # 经过池化 输出[32,7,7] 传入输出层
        )
        ## 第六层卷积
        self.conv6 = nn.Sequential(
            nn.Conv2d(
                in_channels=256,  # 同上
                out_channels=512,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            # 经过卷积 输出[32, 14, 14] 传入池化层
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)  # 经过池化 输出[32,7,7] 传入输出层
        )
        ## 输出层
        self.output = nn.Linear(in_features=512*9*3, out_features=1)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)           # [batch, 32,7,7]
        x = self.conv3(x)  # [batch, 32,7,7]
        x = self.conv4(x)  # [batch, 32,7,7]
        x = self.conv5(x)  # [batch, 32,7,7]
        x = self.conv6(x)  # [batch, 32,7,7]
        x = x.view(x.size(0), -1)   # 保留batch, 将后面的乘到一起 [batch, 32*7*7]
        output = self.output(x)     # 输出[50,10]
        return output


class DQN(object):
    def __init__(self):
        # -----------Define 2 networks (target and training)------#
        self.eval_net, self.target_net = CNN(), CNN()
        # Define counter, memory size and loss function
        self.learn_step_counter = 0  # count the steps of learning process
        self.memory: List = [None] * MEMORY_CAPACITY
        self.memory_counter = 0  # counter used for experience replay buffer
        # ------- Define the optimizer------#
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)

        # ------Define the loss function-----#
        self.loss_func = nn.MSELoss()

    def choose_action(self, state:Container, cargo):
        # 可行点取最大的
        is_encase, inputs, points, poses = state.encase(cargo)

        # torch.set_printoptions(profile="full")
        # print(inputs)
        if is_encase == False:
            return is_encase, is_encase, is_encase

        if np.random.uniform() < EPSILON:  # greedy
            data = inputs.data.cpu().numpy()
            data = normalization(data)
            data = standardization(data)
            inputs = torch.tensor(data)
            with torch.no_grad():
                actions_value = self.target_net.forward(inputs)
            action = torch.max(actions_value, 0)[1].data.numpy()
            action = action[0]
            point = points[action]
            pose = poses[action]
        else:
            action = np.random.randint(0, high=len(points))
            point = points[action]
            pose = poses[action]
        return point, pose

    def store_transition(self, s:torch.Tensor, a:Cargo, r, s_:Container, a_:Cargo):

        transition = [s, a.matrix(), r, s_, a_]
        # if the capacity is full, then use index to replace the old memory with new one
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index] = transition
        self.memory_counter += 1

    def learn(self):

        # update the target network every fixed steps
        if self.learn_step_counter % TARGET_NETWORK_REPLACE_FREQ == 0:
            # Assign the parameters of eval_net to target_net
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter += 1

        # Determine the index of Sampled batch from buffer
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)  # randomly select some data from buffer

        b_s_a_list = torch.zeros(1, 2, L, W)
        q_next_max = []
        b_r = []
        for index in sample_index:
            b_memory = self.memory[index]
            b_s = b_memory[0]
            b_a = b_memory[1]
            b_r.append(b_memory[2])
            b_s_a = torch.stack((b_s, b_a), dim=0)
            b_s_a = b_s_a.unsqueeze(0)
            b_s_a_list = torch.cat((b_s_a_list, b_s_a), dim=0)
            state_next = b_memory[-2]
            cargo_next = b_memory[-1]

            # calculate the q value of next state
            is_encasable, inputs, points, poses = state_next.encase(cargo_next)
            if is_encasable:
                data = inputs.data.cpu().numpy()
                data = normalization(data)
                data = standardization(data)
                inputs = torch.tensor(data)
                actions_value = self.target_net.forward(inputs)
                q_next = torch.max(actions_value, 0)[0]
                q_next_max.append(q_next)
            else:
                q_next = torch.zeros(size=[1])
                q_next_max.append(q_next)

        b_s_a = b_s_a_list[1:]
        data = b_s_a.data.cpu().numpy()
        data = normalization(data)
        data = standardization(data)
        b_s_a = torch.tensor(data).to(device)


        self.eval_net.to(device)
        q_eval = self.eval_net(b_s_a)

        # q_next = torch.stack(q_next_max,0)
        # b_r = torch.stack(b_r, 0).unsqueeze(1)

        q_next = torch.tensor(q_next_max).unsqueeze(1)
        b_r = torch.tensor(b_r).unsqueeze(1)

        q_target = (b_r + q_next * GAMMA).to(device)
        q_target.detach()

        self.loss_func.to(device)

        loss = self.loss_func(q_eval, q_target)
        print('loss: %f iters:%d cargo_id: %d' %(loss.item(), i_episode, c_i))

        self.optimizer.zero_grad()  # reset the gradient to zero
        loss.backward()
        self.optimizer.step()  # execute back propagation for one step

        # for parameters in self.eval_net.parameters():
        #     print(parameters)

        q_eval_again = self.eval_net(b_s_a)
        loss_again = self.loss_func(q_eval_again, q_target)
        print('loss_again: %f iters:%d cargo_id: %d' % (loss_again.item(), i_episode, c_i))


def evaluate():
    start = time.time()
    c_index = 0
    state = Container(L, W, H)
    while True:
        cargo = Cargo(cargo_list[c_index][0], cargo_list[c_index][1], cargo_list[c_index][2])
        action = dqn.choose_action(state, cargo)
        if(len(action)==3):
            c_index += 1
            if c_index >= len(cargo_list):
                break
            else:
                continue
        else:
            cargo.pose = action[1]
            cargo.point = action[0]
            state.update_state(cargo)

        if c_index == len(cargo_list)-1:
            break
        c_index += 1

    end = time.time()
    last_time = end - start
    print("time cost: %f s" % last_time)
    occupy = state.occupy_volume() / state.volume
    return occupy


if __name__ == '__main__':

    '''
    --------------Procedures of DQN Algorithm------------------
    '''
    # create the object of DQN class
    dqn = DQN()

    # Start training
    print("\nCollecting experience...")

    cargo_list = random_generate()
    print('cargo list length: %d' % len(cargo_list))

    for i_episode in range(500):
        # refresh

        state = Container(L, W, H)
        c_i = 0
        ep_r = 0
        done = False
        while True:
            # print('episode: %d box id: %d' % (i_episode, c_i))
            # take action based on the current state
            cargo = Cargo(cargo_list[c_i][0], cargo_list[c_i][1], cargo_list[c_i][2])

            # take action based on the current state
            action = dqn.choose_action(state, cargo)

            if len(action) == 3:
                done = True
            else:
                pose = action[1]
                point = action[0]

            if done:
                c_i += 1
                if c_i >= len(cargo_list):
                    break
                else:
                    continue

            pre_s = copy.deepcopy(state._H_matrix)
            # obtain the reward and next state and some other information
            cargo.pose = pose
            cargo.point = point
            state.update_state(cargo)
            # obtain the reward
            r = state.reward()

            # store the transitions of states
            cargo_next = Cargo(cargo_list[c_i+1][0], cargo_list[c_i+1][1], cargo_list[c_i+1][2])
            dqn.store_transition(pre_s, cargo, r, state, cargo_next)
            # memory = dqn.memory
            # print("store finished")

            ep_r += r
            # if the experience repaly buffer is filled, DQN begins to learn or update
            # its parameters.
            if dqn.memory_counter > MEMORY_CAPACITY:
                dqn.learn()
                if done:
                    print('Ep: ', i_episode, ' |', 'Ep_r: ', round(ep_r, 2))

            if c_i+1 == len(cargo_list)-1:
                break
            c_i += 1

        occupy_rate = evaluate()
        print('occupy_rate: %f' %occupy_rate)

    torch.save(dqn.target_net.state_dict(), 'cnn.pth')





