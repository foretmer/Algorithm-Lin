# 22AA_project

## 问题描述

物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满。

设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：

1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；

2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。

基础部分：

- [x] 所有的参数为整数；

- [x] 静态装箱

- [x] 所有的箱子全部平放，即箱子的最大面朝下摆放；

- [x] 算法时间不做严格要求，只要1天内得出结果都可。

高级部分：

- [x] 参数考虑小数点后两位；

- [x] 实现在线算法，也就是箱子是按照随机顺序到达，先到达先摆放；

- [ ] 需要考虑箱子的摆放顺序，即箱子是从内到外，从下向上的摆放顺序；

- [x] 因箱子共有3个不同的面，所有每个箱子有3种不同的摆放状态；

- [x] 算法需要实时得出结果，即算法时间小于等于2秒。

额外功能

- [x] 可视化装箱

## 

## Run

```python
python main.py --mode static --visualize
```

mode：static/online

可视化：需要可视化加上`--visualize`

具体数据在代码内调整

--- 

## Reference

[3D-Bin-Packing-Problem](https://github.com/Janet-19/3d-bin-packing-problem)

[3D-bin-packing](https://github.com/jerry800416/3D-bin-packing)

[1] Li X, Zhao Z, Zhang K. A genetic algorithm for the three-dimensional bin packing problem with heterogeneous bins[C]//IIE Annual Conference. Proceedings. Institute of Industrial and Systems Engineers (IISE), 2014: 2039.

[2] Dube E, Kanavathy L R, Woodview P. Optimizing three-dimensional bin packing through simulation[C]//Sixth IASTED International Conference Modelling, Simulation, and Optimization. 2006.
