# 三维装箱问题算法研究

#### 问题背景

​	物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。

​	设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：

1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；

2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。

####  基础部分

1. 所有的参数为整数；
2. 静态装箱，即从n个箱子中选取m个箱子，并实现m个箱子在车厢中的摆放（无需考虑装箱的顺序，即不需要考虑箱子从内向外，从下向上这种在车厢中的装箱顺序）；
3. 所有的箱子全部平放，即箱子的最大面朝下摆放；
4.  算法时间不做严格要求，只要1天内得出结果都可。

#### 高级部分

1. 参数考虑小数点后两位；

2. 实现在线算法，也就是箱子是按照随机顺序到达，先到达先摆放；

3. 需要考虑箱子的摆放顺序，即箱子是从内到外，从下向上的摆放顺序；

4.  因箱子共有3个不同的面，所有每个箱子有3种不同的摆放状态；

5. 算法需要实时得出结果，即算法时间小于等于2秒。

   

## 算法设计

#### 数据生成

##### 整数数据：

​	目前少有现成的3D装箱数据集。在大多数论文中，3D装箱问题的实验数据为随机生成。对于整数数据，我们规定容器的尺寸统一为10x10x10，箱子每边长为区间[2,5]内的整数，生成数据的方法：

​	将整个容器看作一个大箱子，给定生成的箱子种类集合，将容器切割为若干箱子集合中的箱子，这一问题可看作一个cutting stock问题。用列生成算法生成箱子序列，算法过程参考论文^[1]^。 箱子序列的顺序又有两种确定方式。第一种是根据箱子左下角的z坐标从小到大排序，如果z坐标相同，则顺序随机决定。第二种是根据箱子装载的顺序，即底层的箱子在前，上层的箱子在后，这一序列可以通过将切割后的箱子依次放入堆栈，再弹出得到。

##### 小数数据：

高度在指定数据列表中随机采样，长宽则从N(0.1,0.5)里采样

```py
#  sample_left_bound = 0.1, sample_right_bound = 0.5
def gen_next_box(self):
    if self.sample_from_distribution and not self.test:
        if self.setting == 2:
            next_box = (round(np.random.uniform(self.sample_left_bound,self.sample_right_bound), 3),
                    round(np.random.uniform(self.sample_left_bound,self.sample_right_bound), 3),
                    round(np.random.uniform(self.sample_left_bound,self.sample_right_bound), 3))
        else:
            next_box = (round(np.random.uniform(self.sample_left_bound,self.sample_right_bound), 3),
                    round(np.random.uniform(self.sample_left_bound,self.sample_right_bound), 3),
                    np.random.choice([0.1,0.2,0.3,0.4,0.5]))
    else:
        next_box = self.box_creator.preview(1)[0]
    return next_box

```



### ==离线算法 Offline==

![image-20230111160918977](https://p.ipic.vip/gbb1p4.png)

##### 实验结果：

| 箱子种数 | 样例数 | 装载率 | 计算时间（秒） |
| -------- | ------ | ------ | -------------- |
| 3        | 100    | 0.742  | 199            |
| 5        | 100    | 0.779  | 2267           |
| 10       | 10     | 0.764  | 533            |
| 15       | 5      | 0.773  | 944            |



<img src="https://p.ipic.vip/6qg9jr.png" alt="image-20230111161241322" style="zoom:75%;" /><img src="https://p.ipic.vip/pggpqs.png" alt="image-20230111161313890" style="zoom:75%;" />



### ==基于强化学习的在线装箱算法==

#### 环境依赖：

- python==3.7.0
- pytorch==1.10.1
- tensorboardx==2.5.1
- gym==0.13.0
- cudatoolkit==10.2.89

#### 程序运行：

程序预训练的模型为model_1.pt，随机生成的数据存储在dataset.pt中

运行测试结果时，仅需要输入下列命令：

```shell
python evaluation.py --evaluate --load-model --model-path model_1.pt --load-dataset --dataset-path dataset.pt
```

运行

```she
python heuristic.py --setting 1 --heuristic OnlineBPH  --load-dataset  --dataset-path dataset.pt
```



#### **问题描述和约束**

​	本算法解决的问题可总结为：给定容器（体积为V），和一系列待装载的箱子，容器和箱子的形状都是长方体，所有箱子的尺寸和数量预先已知，需要确定一个可行的装箱方案使得在满足一定约束的条件下，容器的填充率尽可能大。可行的方案需要满足以下约束

​	(1) 被装载的箱子必须完全被包含在容器中。

​	(2) 任何两个被装载的箱子不能互相重叠。

​	(3) 所有被装载的箱子以与容器平行的方式放置，即不能斜放。

​	(4)考虑箱子摆放的顺序，箱子是从内到外，从下往上的摆放顺序。

​	(5)稳定性约束，每个箱子的底部要得到其他箱子的支撑，不能悬空。

​	(6)摆放状态的约束，箱子共有六个面，故每个箱子均有六种不同的摆放状态。。

​	(7)实现在线算法，先到达的箱子先摆放。

#### **问题表示**

​	一个装箱问题可用元组（container_size,item_size_set）表示，其中container_size表示容器的总体积，默认为10x10x10，item_size_set表示箱子列表，高度从给定的集合中随机取样，长宽则从N(0.1,0.5)里采样，保留小数点后三位小数。一般装箱的设定为从左下角开始装箱（from-left-bottom），故使用箱子左下角的坐标表示其位置，即每个箱子可表示为(x,y,z,l~x~,l~y~,l~z~)。

![image-20230111162030141](https://p.ipic.vip/j4lsad.png)

​	给定一个初始容器尺寸container_size后，将箱子按顺序依次装入箱子中，如图中的箱子0、1、2所示。当箱子0进入容器后，会得到三个新的候选位置，如t=1所示（由于画的是截面图，故y向上的候选位置无法画出)，然后当箱子1进入容器后，EMS继续更新，同时动态更新相应的配置树，随着时间的推移，新放入的箱子被陆续放入容器中，候选节点被替换，新的候选放置节点作为子节点生成。随着打包时间的推移，这些节点会迭代更新，并形成一个动态装箱配置树。

​	使用节点将PCT填充到固定长度，在GAT的特征计算过程中，通过掩蔽的注意力机制将冗余节点消除，利用多头注意力以稳定学习过程。它应用 K 个独立的注意力机制来计算隐藏状态，然后将其特征连接起来（或计算平均值），从而得到以下两种输出表示形式：transformer 模型（self-attention自注意力）利用多头注意力以稳定学习过程。它应用 K 个独立的注意力机制来计算隐藏状态，然后将其特征连接起来（或计算平均值），从而得到以下两种输出表示形式：

<img src="https://p.ipic.vip/o046ll.jpg" alt="img" style="zoom:150%;" />

<img src="https://p.ipic.vip/utr9bd.jpg" alt="img" style="zoom:150%;" />

​	其中，$\alpha$是第k个注意力头归一化的注意力系数,||表示拼接操作，$\sigma$表示激活函数。同时为了保持节点空间关系，状态被GAT嵌入为图下图(b)所示的全连通图，没有任何内部掩码操作。

![image-20230111162848072](https://p.ipic.vip/p8ojvg.png)

代码如下所示：

```py

class DRL_GAT(nn.Module):
    def __init__(self, args):
        super(DRL_GAT, self).__init__()

        self.actor = AttentionModel(args.embedding_size,
                                    args.hidden_size,
                                    n_encode_layers = args.gat_layer_num,
                                    n_heads = 1,
                                    internal_node_holder = args.internal_node_holder,
                                    internal_node_length = args.internal_node_length,
                                    leaf_node_holder = args.leaf_node_holder,
                                    )
        init_ = lambda m: init(m, nn.init.orthogonal_, lambda x: nn.init.constant_(x, 0), sqrt(2))
        self.critic = init_(nn.Linear(args.embedding_size, 1))

    def forward(self, items, deterministic = False, normFactor = 1, evaluate = False):
        o, p, dist_entropy, hidden, _= self.actor(items, deterministic, normFactor = normFactor, evaluate = evaluate)
        values = self.critic(hidden)
        return o, p, dist_entropy,values

    def evaluate_actions(self, items, actions, normFactor = 1):
        _, p, dist_entropy, hidden, dist = self.actor(items, evaluate_action = True, normFactor = normFactor)
        action_log_probs = dist.log_probs(actions)
        values =  self.critic(hidden)
        return values, action_log_probs, dist_entropy.mean()
    

    #自注意力机制
class AttentionModel(nn.Module):

    def __init__(self,
                 embedding_dim,
                 hidden_dim,
                 n_encode_layers=2,
                 tanh_clipping=10.,
                 mask_inner=False,
                 mask_logits=False,
                 n_heads=1,
                 internal_node_holder = None,
                 internal_node_length = None,
                 leaf_node_holder = None,
                 ):
        super(AttentionModel, self).__init__()

        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.n_encode_layers = n_encode_layers
        self.decode_type = None
        self.temp = 1.0

        self.tanh_clipping = tanh_clipping
        self.mask_inner = mask_inner
        self.mask_logits = mask_logits

        self.n_heads = n_heads
        self.internal_node_holder = internal_node_holder
        self.internal_node_length = internal_node_length
        self.next_holder = 1
        self.leaf_node_holder = leaf_node_holder

        graph_size = internal_node_holder + leaf_node_holder + self.next_holder

        activate, ini = nn.LeakyReLU, 'leaky_relu'
        init_ = lambda m: init(m, nn.init.orthogonal_, lambda x: nn.init.constant_(x, 0), nn.init.calculate_gain(ini))

        self.init_internal_node_embed = nn.Sequential(
            init_(nn.Linear(self.internal_node_length, 32)),
            activate(),
            init_(nn.Linear(32, embedding_dim)))

        self.init_leaf_node_embed  = nn.Sequential(
            init_(nn.Linear(8, 32)),
            activate(),
            init_(nn.Linear(32, embedding_dim)))

        self.init_next_embed = nn.Sequential(
            init_(nn.Linear(6, 32)),
            activate(),
            init_(nn.Linear(32, embedding_dim)))

        # Graph attention model
        self.embedder = GraphAttentionEncoder(
            n_heads=n_heads,
            embed_dim=embedding_dim,
            n_layers=self.n_encode_layers,
            graph_size = graph_size,
        )

        self.project_node_embeddings = nn.Linear(embedding_dim, 3 * embedding_dim, bias=False)
        self.project_fixed_context = nn.Linear(embedding_dim, embedding_dim, bias=False)
        assert embedding_dim % n_heads == 0

    def forward(self, input, deterministic = False, evaluate_action = False, normFactor = 1, evaluate = False):

        internal_nodes, leaf_nodes, next_item, invalid_leaf_nodes, full_mask = observation_decode_leaf_node
        (input,self.internal_node_holder,self.internal_node_length,self.leaf_node_holder)
        leaf_node_mask = 1 - invalid_leaf_nodes
        valid_length = full_mask.sum(1)
        full_mask = 1 - full_mask

        batch_size = input.size(0)
        graph_size = input.size(1)
        internal_nodes_size = internal_nodes.size(1)
        leaf_node_size = leaf_nodes.size(1)
        next_size = next_item.size(1)

        internal_inputs = internal_nodes.contiguous().view(batch_size * internal_nodes_size, self.internal_node_length)*normFactor
        leaf_inputs = leaf_nodes.contiguous().view(batch_size * leaf_node_size, 8)*normFactor
        current_inputs = next_item.contiguous().view(batch_size * next_size, 6)*normFactor

        # We use three independent node-wise Multi-Layer Perceptron (MLP) blocks to project these raw space configuration nodes
        # presented by descriptors in different formats into the homogeneous node features.
        internal_embedded_inputs = self.init_internal_node_embed(internal_inputs).reshape((batch_size, -1, self.embedding_dim))
        leaf_embedded_inputs = self.init_leaf_node_embed(leaf_inputs).reshape((batch_size, -1, self.embedding_dim))
        next_embedded_inputs = self.init_next_embed(current_inputs.squeeze()).reshape(batch_size, -1, self.embedding_dim)
        init_embedding = torch.cat((internal_embedded_inputs, leaf_embedded_inputs, next_embedded_inputs), dim=1).view(batch_size * graph_size, self.embedding_dim)

        # transform init_embedding into high-level node features.
        embeddings, _ = self.embedder(init_embedding, mask = full_mask, evaluate = evaluate)
        embedding_shape = (batch_size, graph_size, embeddings.shape[-1])
        
        # Decide the leaf node indices for accommodating the current item
        log_p, action_log_prob, pointers, dist_entropy, dist, hidden = self._inner(embeddings,
                                                          deterministic=deterministic,
                                                          evaluate_action=evaluate_action,
                                                          shape = embedding_shape,
                                                          mask = leaf_node_mask,
                                                          full_mask = full_mask,
                                                          valid_length = valid_length)
        return action_log_prob, pointers, dist_entropy, hidden, dist

    def _inner(self, embeddings, mask = None, deterministic = False, evaluate_action = False, shape = None, full_mask = None, valid_length =None): # 元素齐了
        # The aggregation of global feature
        fixed = self._precompute(embeddings, shape = shape, full_mask = full_mask, valid_length = valid_length)
        # Calculate probabilities of selecting leaf nodes
        log_p, mask = self._get_log_p(fixed, mask)

        # The leaf node which is not feasible will be masked in a soft way.
        if deterministic:
            masked_outs = log_p * (1 - mask)
            if torch.sum(masked_outs) == 0:
                masked_outs += 1e-20
        else:
            masked_outs = log_p * (1 - mask) + 1e-20
        log_p = torch.div(masked_outs, torch.sum(masked_outs, dim=1).unsqueeze(1))

        dist = FixedCategorical(probs=log_p)
        dist_entropy = dist.entropy()

        # Get maximum probabilities and indices
        if deterministic:
            # We take the argmax of the policy for the test.
            selected = dist.mode()
        else:
            # The action at is sampled from the distribution for training
            selected = dist.sample()

        if not evaluate_action:
            action_log_probs = dist.log_probs(selected)
        else:
            action_log_probs = None

        # Collected lists, return Tensor
        return log_p, action_log_probs, selected, dist_entropy, dist, fixed.context_node_projected

    def _precompute(self, embeddings, num_steps=1, shape = None, full_mask = None, valid_length = None):
        # The aggregation of global feature, only happens on the eligible nodes.
        transEmbedding = embeddings.view(shape)
        full_mask = full_mask.view(shape[0], shape[1],1).expand(shape).bool()
        transEmbedding[full_mask]  = 0
        graph_embed = transEmbedding.view(shape).sum(1)
        transEmbedding = transEmbedding.view(embeddings.shape)

        graph_embed = graph_embed / valid_length.reshape((-1,1))
        fixed_context = self.project_fixed_context(graph_embed)

        glimpse_key_fixed, glimpse_val_fixed, logit_key_fixed = \
            self.project_node_embeddings(transEmbedding).view((shape[0], 1, shape[1],-1)).chunk(3, dim=-1)

        fixed_attention_node_data = (
            self._make_heads(glimpse_key_fixed, num_steps),
            self._make_heads(glimpse_val_fixed, num_steps),
            logit_key_fixed.contiguous()
        )
        return AttentionModelFixed(transEmbedding, fixed_context, *fixed_attention_node_data)

    def _get_log_p(self, fixed, mask = None, normalize=True):
        # Compute query = context node embedding
        query = fixed.context_node_projected[:, None, :]

        # Compute keys and values for the nodes
        glimpse_K, glimpse_V, logit_K = self._get_attention_node_data(fixed)

        # Compute logits (unnormalized log_p)
        log_p, glimpse = self._one_to_many_logits(query, glimpse_K, glimpse_V, logit_K, mask)
        if normalize:
            log_p = torch.log_softmax(log_p / self.temp, dim=-1)
        assert not torch.isnan(log_p).any()
        return log_p.exp(), mask

    def _one_to_many_logits(self, query, glimpse_K, glimpse_V, logit_K, mask):

        batch_size, num_steps, embed_dim = query.size()
        key_size = val_size = embed_dim // self.n_heads

        # Compute the glimpse, rearrange dimensions so the dimensions are (n_heads, batch_size, num_steps, 1, key_size)
        glimpse_Q = query.view(batch_size, num_steps, self.n_heads, 1, key_size).permute(2, 0, 1, 3, 4)

        # Batch matrix multiplication to compute compatibilities (n_heads, batch_size, num_steps, graph_size)
        compatibility = torch.matmul(glimpse_Q, glimpse_K.transpose(-2, -1)) / math.sqrt(glimpse_Q.size(-1))
        logits = compatibility.reshape([-1,1,compatibility.shape[-1]])

        # From the logits compute the probabilities by clipping, masking and softmax
        if self.tanh_clipping > 0:
            logits = torch.tanh(logits) * self.tanh_clipping

        logits = logits[:, 0, self.internal_node_holder: self.internal_node_holder + self.leaf_node_holder]
        if self.mask_logits:
            logits[mask.bool()] = -math.inf

        return logits, None

    def _get_attention_node_data(self, fixed):
        return fixed.glimpse_key, fixed.glimpse_val, fixed.logit_key

    def _make_heads(self, v, num_steps=None):
        assert num_steps is None or v.size(1) == 1 or v.size(1) == num_steps

        return (v.contiguous().view(v.size(0), v.size(1), v.size(2), self.n_heads, -1).expand(v.size(0), v.size(1) if num_steps is None else num_steps, v.size(2), self.n_heads, -1)
                .permute(3, 0, 1, 2, 4) )
```

#### 模型结果：

| 箱子种数 | 样例数 | 装载率 | 计算时间（秒） |
| -------- | ------ | ------ | -------------- |
| 10       | 150    | 0.829  | 10.143         |
| 20       | 150    | 0.843  | 13.320         |



参考文献：

[1]Zhao H, She Q, Zhu C, et al. Online 3D Bin Packing with Constrained Deep Reinforcement Learning,2020: arXiv:2006.14978.

[2]https://github.com/alexfrom0815/Online-3D-BPP-PCT

[3]https://github.com/alexfrom0815/Online-3D-BPP-DRL

