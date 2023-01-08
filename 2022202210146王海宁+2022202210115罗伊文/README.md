# 离线和在线三维装箱问题算法研究
装箱问题研究的是在满足一定约束情况下往容器中放置尽可能多的物品。更广泛的描述为将一定数量的物品放入有一定量的容器中，使得容器中的物品不超过容器容量并能取得最佳效益，一般用空间利用率来衡量。在进行装箱的过程中，是否知道所有物品的信息可以划分为离线和在线问题：若事先获得了待放置箱子的信息，则属于离线装箱问题，反之属于在线装箱问题。下面根据设定不同的情况，同时考虑这两种情况，分别探讨离线三维装箱问题和在线三维装箱问题。

![请添加图片描述](https://img-blog.csdnimg.cn/0c8981071fc14e4b892fd1f51da7c9cd.png)


先讨论了离线的三维装箱问题，选用了基于贪心块选择的启发式算法；再讨论了在线的三维装箱问题，在基于树结构来更新、维护EMS的基础上，我们使用了DBL、BPH和random三种策略。因此在这一部分，我们将通过具体实验数据分别对这四种算法进行评估和分析。在我们的实验中一共采用五种情况，每一种情况包含不同种类的箱子。其中实验数据的箱子顺序对于离线算法没有影响，而对于在线算法我们将其视为固定。
## 离线三维装箱问题
离线三维装箱问题，即事先已经获得所有待放置箱子的具体情况。这时候装箱问题需要两个步骤来解决：在待放置箱子列表中选择合适的箱子，再根据放置策略尝试放置到容器内。如何选择合适的放置策略是值得讨论的一点。具体的形式化定义如下：
给定一个容积为V的容器和待装载的物品的具体信息（长、宽、高）。具体问题是要在满足约束条件下使得放入容器内总体积S更大，即填充率S/V尽可能高。
### 代码结构
>main.py 主函数
> * gen_block():生成块算法
> * gen_list():生成列表算法
> * place_block():放置算法
> * remove_block():块移除算法
> * draw_result():绘制放置方案，引入draw_3d方法

> draw_3d.py  绘制三维放置方案
> * packing_simple(l, w, h, goods):输入为长、宽、商品集，输出为箱子个数
> * Addcube_3d(ren, coordinate, edge_max, x_re, y_re, z_re):添加箱子图形
> * show_3d(L_box, L_coordinates):三维展示，输入为容器集和商品箱子集
> * png_save(renWin, name):图像保存
### 运行方法
直接在**main.py**中的main函数输入相关数据，container为容器大小，**boxlist**存放箱子尺寸，
其中Box用于构造箱子种类【长，宽，高，种类序号】，**numlist**为各种箱子种类对应箱子个数列表
点击run即可得到计算出的占用率以及箱子坐标和放置方案绘图

## 在线三维装箱问题
在线3D-BPP必须要按照物品的到达顺序进行装箱，这给在线3D-BPP问题带来了额外的限制，因此不能用常见的基于搜索的方法来解决在线问题，通常用启发式方法或深度学习的方法来解决在线3D-BPP。
### 代码结构
>main.py 主函数
> * DBL：DBL算法
> * BPH: BPH算法
> * random：随机放置算法

>input.py：输入数据 箱子尺寸列表（列表中的位置代表箱子到来的次序） 容器尺寸

> draw_3d.py：绘制放置方案

> tools.py：调整实验具体参数和选择方案（DBL、BPH、random）

> binCreator.py：制造箱子

> space.py：维护EMS（计算、修改）
### 使用说明
举个例子：
```
在input.py中给出125种箱子，尺寸由【1，1，1】依次序递增到【5，5，5】（可随意更改）
在tools.py中选择DBL方法
运行程序，得到结果如下：
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2d29c25ea07b494a8d2cf92ac0028d70.png)
>会打印出最好结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/f2621ef9ab8a4389ab77a9a04c5f5131.png)

## 其他说明
![在这里插入图片描述](https://img-blog.csdnimg.cn/dc47fcb1e4584f1083ee2cab69a4824e.png)
具体实验数据和结果见作业内容

### 参考源

参考源：

https://github.com/Pseudomanifold/bin-packing-heuristics

https://github.com/alexfrom0815/Online-3D-BPP-PCT


参考文献如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/1d07ba5c5be845b49107973b195e6d0c.png)


### 实验配置
1. Python=3.7，
2. CPU: 12th Gen Intel(R) Core(TM) i7-12700H  2.50 GHz
3. Windows10 64位
4. Pycharm

