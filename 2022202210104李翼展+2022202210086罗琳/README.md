# 在线3D装箱问题求解

## 问题描述

物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。

设车厢为长方形，其长宽高分别为![1](https://latex.codecogs.com/svg.image?L)，![1](https://latex.codecogs.com/svg.image?W)，![1](https://latex.codecogs.com/svg.image?H)；共有![1](https://latex.codecogs.com/svg.image?n)个箱子，箱子也为长方形，第![1](https://latex.codecogs.com/svg.image?i)个箱子的长宽高为![1](https://latex.codecogs.com/svg.image?l_i)，![1](https://latex.codecogs.com/svg.image?w_i)，![1](https://latex.codecogs.com/svg.image?h_i)（![1](https://latex.codecogs.com/svg.image?n)个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：

1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；

2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。

高级部分要求：

1. 参数考虑小数点后两位；

2. 实现在线算法，也就是箱子是按照随机顺序到达，先到达先摆放；

3. 需要考虑箱子的摆放顺序，即箱子是从内到外，从下向上的摆放顺序；

4. 因箱子共有3个不同的面，所有每个箱子有3种不同的摆放状态；

5. 算法需要实时得出结果，即算法时间小于等于2秒。

## 算法流程

### 装箱配置树（Packing Configuration Tree，PCT）

- 当矩形箱子![1](https://latex.codecogs.com/svg.image?n_t)在时间![1](https://latex.codecogs.com/svg.image?t)被添加到装箱时，设置一系列新的候选位置，以便容纳后续的箱子。结合![1](https://latex.codecogs.com/svg.image?n_t)基于现有位置的轴向方向![1](https://latex.codecogs.com/svg.image?o\in&space;O)，得到候选位置（即位置和方向）。

- 打包过程可以看作是已打包的箱子节点替换放置节点，并且生成了新的候选放置节点作为子节点。

- 随着打包时间![1](https://latex.codecogs.com/svg.image?t)的进行，迭代更新这些节点，生成动态打包配置树，记为![1](https://latex.codecogs.com/svg.image?T)。

- 内部节点集![1](https://latex.codecogs.com/svg.image?B_t\in&space;T_t)表示装箱箱子的空间配置，叶子节点集![1](https://latex.codecogs.com/svg.image?L_t\in&space;T_t)表示可装箱的候选位置。

- 在装箱过程中，将不可用的叶子节点（如被装箱箱子覆盖的叶子节点）从![1](https://latex.codecogs.com/svg.image?L_t)中移除。当没有可装箱的叶子节点使![1](https://latex.codecogs.com/svg.image?n_t)满足放置约束时，装箱阶段结束。

### 树表示

- 给定装箱配置![1](https://latex.codecogs.com/svg.image?T_t)和当前箱子![1](https://latex.codecogs.com/svg.image?n_t)，装箱策略可以表示为![1](https://latex.codecogs.com/svg.image?\pi\left(L_t&space;\mid&space;T_t,&space;n_t\right))。元组![1](https://latex.codecogs.com/svg.image?\left(T_t,&space;n_t\right))可视为图结构，并由图神经网络编码。

- 由于![1](https://latex.codecogs.com/svg.image?PCT)随时间![1](https://latex.codecogs.com/svg.image?t)不断变化，所以采用对图结构没有先验要求的图注意力网络（***Graph Attention Network，GAT***）。

- 使用三个独立的多层感知器（***Multi-Layer Perceptron，MLP***）模块获取![1](https://latex.codecogs.com/svg.image?B_t)、![1](https://latex.codecogs.com/svg.image?L_t)、![1](https://latex.codecogs.com/svg.image?n_t)的同构节点特征。

### 叶子节点选择

- 给定节点特征![1](https://latex.codecogs.com/svg.image?h)，需要决定容纳当前箱子![1](https://latex.codecogs.com/svg.image?n_t)的叶子节点索引。

- 由于叶子随![1](https://latex.codecogs.com/svg.image?PCT)根据时间不断变化，这里使用指针机制，基于上下文注意力从从![1](https://latex.codecogs.com/svg.image?L_t)中选择叶子节点。

- 采用***Scaled Dot-Product Attention***来计算指针，对![1](https://latex.codecogs.com/svg.image?h)取平均聚合得到全局上下文特征。

### 马尔可夫决策过程

在时间![1](https://latex.codecogs.com/svg.image?t)的在线三维装箱决策只依赖于元组![1](https://latex.codecogs.com/svg.image?\left(T_t,&space;n_t\right))，可以表示为马尔科夫决策过程（***Markov Decision Process，MDP***），该过程由状态![1](https://latex.codecogs.com/svg.image?S)、动作![1](https://latex.codecogs.com/svg.image?A)、转移![1](https://latex.codecogs.com/svg.image?P)和奖励![1](https://latex.codecogs.com/svg.image?R)构成。这里使用端到端的深度强化学习（***Deep Reinforcement Learning，DRL***）![1](https://latex.codecogs.com/svg.image?Agent)来处理这一MDP问题。

- ***State：*** 时间![1](https://latex.codecogs.com/svg.image?t)时的状态![1](https://latex.codecogs.com/svg.image?s_t)表示为![1](https://latex.codecogs.com/svg.image?s_t=\left(T_t,&space;n_t\right))，其中![1](https://latex.codecogs.com/svg.image?T_t)由内部节点![1](https://latex.codecogs.com/svg.image?B_t)和叶子节点![1](https://latex.codecogs.com/svg.image?L_t)组成。每个内部节点![1](https://latex.codecogs.com/svg.image?b\in&space;B_t)是一个箱子对应的大小、坐标等属性。当前箱子![1](https://latex.codecogs.com/svg.image?n_t)是一个表示大小的元组。![1](https://latex.codecogs.com/svg.image?b)和![1](https://latex.codecogs.com/svg.image?n_t)可以添加其他额外属性，比如箱子种类、密度。

- ***Action：*** ![1](https://latex.codecogs.com/svg.image?a_t\in&space;A)处的动作为所选叶子节点![1](https://latex.codecogs.com/svg.image?l)的索引，记为![1](https://latex.codecogs.com/svg.image?a_t=\operatorname{index}(l))。动作空间![1](https://latex.codecogs.com/svg.image?A)与![1](https://latex.codecogs.com/svg.image?L_t)大小相同，仅依赖于叶子节点展开方式和装箱集合![1](https://latex.codecogs.com/svg.image?B_t)，可用于求解连续解空间的在线三维装箱问题。

- ***Transition：*** 转移概率![1](https://latex.codecogs.com/svg.image?P\left(s_{t&plus;1}&space;\mid&space;s_t\right))由当前策略![1](https://latex.codecogs.com/svg.image?\pi)和抽样箱子的概率分布共同决定。在线序列从均匀分布的箱子集合![1](https://latex.codecogs.com/svg.image?I)中动态生成。

- ***Reward：*** 当箱子![1](https://latex.codecogs.com/svg.image?n_t)作为内部节点成功插入![1](https://latex.codecogs.com/svg.image?PCT)，奖励函数![1](https://latex.codecogs.com/svg.image?R)定义为![1](https://latex.codecogs.com/svg.image?r_t=c_r&space;\cdot&space;w_t)。装箱结束时![1](https://latex.codecogs.com/svg.image?r_t=0)。![1](https://latex.codecogs.com/svg.image?c_r)是一个常数，![1](https://latex.codecogs.com/svg.image?w_t)是![1](https://latex.codecogs.com/svg.image?n_t)的权重因子，默认大小为![1](https://latex.codecogs.com/svg.image?n_t)的体积。

- ***Training Method：*** ![1](https://latex.codecogs.com/svg.image?DRL) ![1](https://latex.codecogs.com/svg.image?Agent)学习策略![1](https://latex.codecogs.com/svg.image?\pi\left(a_t&space;\mid&space;s_t\right))以最大化累积折扣奖励。这里使用***ACKTR***方法进行训练。其中，![1](https://latex.codecogs.com/svg.image?actor)对叶子节点![1](https://latex.codecogs.com/svg.image?L_t)加权，并输出策略分布![1](https://latex.codecogs.com/svg.image?\pi_\theta\left(L_t&space;\mid&space;T_t,&space;n_t\right))；![1](https://latex.codecogs.com/svg.image?critic)将全局上下文映射为状态值预测，来预测![1](https://latex.codecogs.com/svg.image?Agent)可以在时间![1](https://latex.codecogs.com/svg.image?t)内获得多少累计折扣奖励，并帮助actor的训练。动作![1](https://latex.codecogs.com/svg.image?a_t)从分布![1](https://latex.codecogs.com/svg.image?\pi_\theta\left(L_t&space;\mid&space;T_t,&space;n_t\right))中采样并进行训练，对策略取argmax以进行测试。

## 实验环境

硬件 | 型号
:--|:--:
GPU          |   NVIDIA TITAN Xp 12GB
CPU          |   7 vCPU Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz

根据文件创建环境：

```bash
conda env create -f BPP.yml
```

包 | 版本
:--|--:
Python          |   3.7
PyTorch         |   1.10
CUDA            |   10.2
Gym             |   0.21
tensorboardX    |   2.5

## 代码执行

### 训练

进行训练，内部节点数和叶子节点数可以修改：

```bash
python main.py --internal-node-holder 160 --leaf-node-holder 100
```

由于训练数据是从均匀分布![1](https://latex.codecogs.com/svg.image?U(a,b))中采样，在实验环境下预计训练时间超过24小时。其中![1](https://latex.codecogs.com/svg.image?a)和![1](https://latex.codecogs.com/svg.image?b)默认取车厢对应维度的![1](https://latex.codecogs.com/svg.image?10\%)和![1](https://latex.codecogs.com/svg.image?50\%)，如宽度取值范围为![1](https://latex.codecogs.com/svg.image?[0.1&space;\times&space;W,&space;0.5&space;\times&space;W])。

### 测试

进行测试：

```bash
python evaluation.py --evaluate --load-model --model-path path/to/model --load-dataset --dataset-path path/to/dataset
```
