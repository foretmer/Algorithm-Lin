# 算法三维装箱

#### 介绍
物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。

#### 设计思路
传统的装箱问题（bin packing）是将一组物品包装在无限的固定尺寸的集装箱中，目的是最大程度地减少所使用的集装箱数量。我们进行相应的转化，将实验目标转化为装箱问题，装入到无限数量的箱子中，再选取填充率最高的箱子作为实验结果。
实验思路：构建基于层的列生成框架，将三维装箱问题作为二维装箱问题的扩展，并进一步考虑垂直支撑的问题。（其中，层是指具有近似高度的货物构成的集合，彼此之间不堆叠）
1）将问题分成对于每一层的子问题，若每个子问题都可以得到一个较优解，那么整体的实验结果就可以有一个不错的下界，并且可以启发式地快速启动。
2）按密度降序排列层，将这些层堆叠起来，使得集装箱具有足够的稳定性和垂直支撑。
我们采用两种解决方案：Maxrects和列生成（column generation）

#### Maxrects
因为每个集装箱都是一样的规格尺寸，所以这里先不考虑集装箱的高度。具体对于每一层来说，采用Maxrects启发式算法。先根据货物的高度对货物进行分组，然后将这些货物集合用作自定义maxrects过程的输入。

#### Column Generation
列生成解决方案是将每层的货物放置问题分解为主要问题和定价子问题。列生成通过迭代解决两个子问题（[RMP]和[SP]）来进行，并在此过程中包含越来越多的变量。通过这种方式，主要问题[RMP]选择迄今为止最好的层，并提供用于定价子问题[SP]的对偶变量（每个货物一个），它确定货物集合的最佳子集来组成一个新的层，当且仅当减少的成本非负时，在下一次迭代中结转（否则列生成过程终止）。并且，这些层通过Maxrects过程或通过为每个货物构建一个层（每个层只有一个货物）来计算生成。

#### 安装教程

在当前目录下

加载数据集（已预处理，可以跳过）：

`python src/getData.py`

创建虚拟环境、安装依赖：

```
python3 -m venv venv
source venv/bin/activate
pip install -r init/requirements.txt
```

或

```
conda env create --name 3d-bpp -f init/environment.yml
conda activate environment.yml
```


#### 使用说明


```
cd src
python -m streamlit run dashboard.py
```
