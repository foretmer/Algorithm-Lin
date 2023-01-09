
# 可变策略的拟人式三维装箱算法实现

## 问题

给定一个长方体容器和较多不同形态的长方体货物，需确定装箱策略，使货物尽可能多地装填到容器中。

### 假设与约束
物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。
设车厢为长方形，其长宽高分别为L,W,H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为(l_i，w_i，h_i )（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：
1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；
2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。
问题分解为基础和高级部分，完成基础部分可得78分以上，完成高级部分可得85分以上。
	所有的参数为整数；
	静态装箱，即从n个箱子中选取m个箱子，并实现m个箱子在车厢中的摆放（无需考虑装箱的顺序，即不需要考虑箱子从内向外，从下向上这种在车厢中的装箱顺序）；
	所有的箱子全部平放，即箱子的最大面朝下摆放；
	算法时间不做严格要求，只要1天内得出结果都可。


### 输入输出

输入为**容器**的**长宽高**数据和**货物**的**数量**及其**各自的长宽高**数据。

输出为以下三项：

1. 容器最终的利用率；
2. 容器中各个货物的位置和形态数据；
3. 结果示意图。

### 算法伪代码

```fake
初始化 容器;初始化 货物列表;
容器.水平参考面 = 0;
容器.垂直参考面 = 0;
容器.可放置点表 = [(0,0,0)];
while i = 1 until 货物列表.货物数量{
    初始化 flag = 未放置未更新;
    初始化 货物 = 货物列表中第 i 个货物;
    for 可放置点 in 容器.可放置点表{
        if (
            货物可以放置在可放置点 并且
            不与两个参考面冲突
        ){
            flag = 已放置;
            退出 可放置点 循环;
        }
    }
    if (flag 标记有 未放置){
        if (
            容器.水平参考面 == 0 或者
            容器.水平参考面 == 容器.长
        ){
            if (货物可以放置在 容器.垂直参考面 的原点){
                将货物放置在(0,0容器.垂直参考面);
                容器.垂直参考面 += 货物.高;
                容器.水平参考面 += 货物.长;
                flag = 已放置已更新;
            }else if (容器.垂直参考面 < 容器.高){
                容器.垂直参考面 = 货物.高;
                容器.水平参考面 = 货物.长;
                flag = 未放置已更新;
            }
        }else{
            for 可放置点 in 容器.可放置点表{
                if (
                    货物可以放置在可放置点 并且
                    货物 满足 容器.垂直参考线 的限制
                ){
                    容器.水平参考线 += 货物.长;
                    flag = 已放置已更新;
                    退出 可放置点 循环;
                }
            }
            if (flag 标记有 未放置){
                容器.水平参考线 = 容器.长;
                flag = 未放置已更新;
            }
        }
    }
    if (flag 标记有 已放置){
        容器.可放置点表.删除(货物.位置);
        货物.挪动;
        容器.可放置点表.并入(
            [根据新的 货物.位置 计算出的 3 个可放置点]
        );
        i++;
    }else if(flag 标记为 未放置已更新){
        i--;
    }else if(flag 标记为 未放置未更新){
        i++;
    }
}
```

### 碰撞检测

上述算法中的“某货物能否放置到某点”将在此节说明。直接在三维空间中确定两个实体是否冲突是有些困难的。本文将在二维平面上考虑三维空间中的实体的投影，通过各个方向上的投影情况判断是否冲突。易得，任意平行于长方体容器放置的长方体货物，如果它们在任意方向上的投影没有重叠，则两者就没有冲突。

而对于平面上的长方体而言，相对在左边的长方体的右上角坐标如果小于相对右边的长方体的左下角坐标，则两个长方形没有重叠。

## Python 实现

### 代码结构

所有的算法实现将组织于一个名为`Encase3D`的包中。该包分为四个模块：`__init__`、`_cargo`、`_container`和`drawer`。

`_cargo`与`_container`分别用于组织货物和容器的相关类代码，`drawer`用于组织绘制 3D 效果图的相关函数代码。`__init__`部分用于初始化包并组织算法代码和可变策略类。

### 类设计

#### 货物 Cargo 类及其相关类

需要描述三维状态，首先需要建立坐标系，首先设置三维点`Point`类：

```python
class Point(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"
    
    def __eq__(self, _o: object) -> bool:
        return self.x == _o.x and self.y == _o.y and self.z == _o.z
```

为了简化后续对三维点的操作，在类中设置合法性属性和序列化属性：

```python
class Point(object):
    @property
    def is_valid(self) -> bool:
        return self.x >= 0 and self.y >=0 and self.z>= 0
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y, self.z)
```

为了直观地描述货物的六种摆放方式，抛弃抽象的 0、1、2... 记号。由于放入货物时，货物的重心非常重要，以货物的高将摆放方式分为三类。在高确定的情况下，将货物根据从前面观察的宽窄分为两类。将六种情况根据上述分类命名后设计为枚举类：

```python
from enum import Enum

class CargoPose(Enum):
    tall_wide  = 0
    tall_thin  = 1
    mid_wide   = 2
    mid_thin   = 3
    short_wide = 4
    short_thin = 5
```

货物初始化时，需要提供货物的尺寸信息：

```python
class Cargo(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._point = Point(-1, -1, -1)
        self._shape = {length, width, height}
        self._pose = CargoPose.tall_thin

    def __repr__(self) -> str:
        return f"{self._point} {self.shape}"
```

货物的长宽高不仅由货物的尺寸决定，还根据货物的摆放方式决定，故分别设置长宽高属性，根据其摆放方式返回正确的值。为了避免大量的 if-else，使用 hash 字典重构：

```python
class Cargo(object):
    @property
    def pose(self) -> CargoPose:
        return self._pose

    @pose.setter
    def pose(self, new_pose: CargoPose):
        self._pose = new_pose

    @property
    def _shape_swiche(self) -> dict:
        edges = sorted(self._shape)
        return {
            CargoPose.tall_thin: (edges[1], edges[0], edges[-1]),
            CargoPose.tall_wide: (edges[0], edges[1], edges[-1]),
            CargoPose.mid_thin: (edges[-1], edges[0], edges[1]),
            CargoPose.mid_wide: (edges[0], edges[-1], edges[-1]),
            CargoPose.short_thin: (edges[-1], edges[1], edges[0]),
            CargoPose.short_wide: (edges[1], edges[-1], edges[0])
        }

    @property
    def shape(self) -> tuple:
        return self._shape_swiche[self._pose]

    @shape.setter
    def shape(self, length, width, height):
        self._shape = {length, width, height}

    @property
    def length(self) -> int:
        return self.shape[0] # 宽、高类似
```

货物的位置信息如果通过先访问其点来访问将会给后续的编码带来一定的麻烦，故在此分别设置 x、y、z 属性，以直接通过货物实例访问其位置：

```python
class Cargo(object):
    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, new_point:Point):
        self._point = new_point

    @property
    def x(self) -> int:
        return self._point.x

    @x.setter
    def x(self, new_x: int):
        self._point = Point(new_x, self.y, self.z)
# y、z 类似
```

后续的算法中排序、利用率等需要用到提及信息，设置只读的体积属性：

```python
class Cargo(object):
    @property
    def volume(self) -> int:
        reslut = 1
        for i in self._shape:
            reslut *= i
        return reslut
```

碰撞检测中还会用到投影信息，设置投影方法，需要传入目标投影面参数：

```python
class Cargo(object):
    def get_shadow_of(self, planar: str) -> tuple:
        if planar in ("xy", "yx"):
            x0, y0 = self.x, self.y
            x1, y1 = self.x + self.length, self.y + self.width
        elif planar in ("xz", "zx"):
            x0, y0 = self.x, self.z
            x1, y1 = self.x + self.length, self.z + self.height
        elif planar in ("yz", "zy"):
            x0, y0 = self.y, self.z
            x1, y1 = self.y + self.width, self.z + self.height
        return (x0, y0, x1, y1)
```

#### 容器 Container 类

容器初始化需要长宽高信息。关于算法所需的可放置点表、已放置货物表、参考面信息使用另外的方法初始化，以便使用同意箱子反复尝试装填：

```python
from typing import List
from Encase3D._cargo import *

class Container(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._length = length
        self._width = width
        self._height = height
        self._refresh()

    def __repr__(self) -> str:
        return f"{self._length}, {self._width}, {self._height}"

    def _refresh(self):
        self._horizontal_planar = 0  # 水平放置参考面
        self._vertical_planar = 0  # 垂直放置参考面
        self._available_points = [Point(0, 0, 0)]  # 可放置点有序列表
        self._setted_cargos : List[Cargo] = []
```

同样的，长宽高、提及等信息单独设置为只读属性：

```python
class Container(object):
    @property
    def length(self) -> int:
        return self._length
    # 宽、高类似

    @property
    def volume(self) -> int:
        return self.height * self.length * self.width
```

容器类中有部分的装箱算法逻辑，在后续算法相关节中介绍。

### 拟人式三维装箱

将一个货物装入容器中的算法在容器类中实现。可变的策略和遍历货物集合的的算法在包初始化的中的方法实现，详见“可变策略”一节。

#### 可放置点表排序

可放置点表需要需要按照$y$、$x$、$z$的顺序排列，在容器类中使用以下方法实现：

```python
class Container(object):
        def _sort_available_points(self):
        self._available_points.sort(key=lambda x: x.z)
        self._available_points.sort(key=lambda x: x.x)
        self._available_points.sort(key=lambda x: x.y)
```

#### 是否可放置

判断一个货物是否在一个点上可放置，需要满足以下两个条件：

1. 不与容器内任一一个其他货物位置相冲突；
2. 完全在容器内。

对于第 1 个条件，在当前模块中以“碰撞检测”的思想实现：

```python
def _is_cargos_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
        _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
        _is_rectangles_overlap(cargo0.get_shadow_of(
            "xz"), cargo1.get_shadow_of("xz"))
    )
```

其中判断长方形是否冲突的方法也定义在当前模块中：

```python
def _is_rectangles_overlap(rec1:tuple, rec2:tuple) -> bool:
    return not (
        rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
        rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )
```

由于第 1 个条件的检测需要遍历容器中的其他货物，故先检测是否与容器冲突，再检测是否与其他货物冲突。这些逻辑在容器实例中实现。需要注意的是，为了避免检测过程中对原货物数据造成污染，根据 Python 语言的特性，需要深复制一个临时货物实例，在其基础上操作。

```python
from copy import deepcopy

class Container(object):
    def is_encasable(self, site: Point, cargo: Cargo) -> bool:
        encasable = True
        temp = deepcopy(cargo)
        temp.point = site
        if (
            temp.x + temp.length > self.length or
            temp.y + temp.width > self.width or
            temp.z + temp.height > self.height
        ):
            encasable = False
        for setted_cargo in self._setted_cargos:
            if _is_cargos_collide(temp, setted_cargo):
                encasable = False
        return encasable
```

#### 挪动货物

挪动货物由于和上面同样的原因需要深复制后在进行操作。由于每个方向上的坐标的挪动逻辑是一样的，故需要将坐标序列化后进行遍历操作，避免代码的冗余重复。挪动完成后，再将最终的放置点赋值回需要挪动的货物：

```python
class Container(object):
    def _adjust_setting_cargo(self, cargo: Cargo):
        site = cargo.point
        temp = deepcopy(cargo)
        if not self.is_encasable(site, cargo):
            return None
        xyz = [site.x, site.y, site.z] 
        # 序列化坐标以执行遍历递减操作, 减少冗余
        for i in range(3): # 012 分别表示 xyz
            is_continue = True
            while xyz[i] > 1 and is_continue:
                xyz[i] -= 1
                temp.point = Point(xyz[0], xyz[1], xyz[2])
                for setted_cargo in self._setted_cargos:
                    if not _is_cargos_collide(setted_cargo, temp):
                        continue
                    xyz[i] += 1
                    is_continue = False
                    break
        cargo.point = Point(xyz[0], xyz[1], xyz[2]) # 反序列化
```

#### 标记

伪代码中的标记非常的理想化，不仅可以记录是否放置的情况，还可以记录容器参考面是否改变的情况。然而在实现中，是否放置可以比较简单的实现，但是否改变参考面需要有前后对比，实现比较复杂。

标记本算法实现中设置为一个坐标点。如果成功放置，则该标记就记录成功放置的点，但没有成功放置时，使用 (-1, -1, 0) 表示放置失败并改变了参考面，(-1, -1, -1) 则表示单纯的放置失败。并在放置算法中专门设置一个子方法用于比较参考面是否发生改变：

```python
class Container(object):
    def _encase(self, cargo: Cargo) -> Point:
        # flag存储放置位置, (-1, -1, 0)放置失败并调整参考面, (-1, -1, -1)放置失败.
        flag = Point(-1, -1, -1)  
        # 用于记录执行前的参考面位置, 便于后续比较
        history = [self._horizontal_planar, self._vertical_planar]
        def __is_planar_changed() -> bool:
            return (
                not flag.is_valid and # 防止破坏已经确定可放置的点位, 即只能在(-1, -1, -1)基础上改
                self._horizontal_planar == history[0] and 
                self._vertical_planar == history[-1]
            ) 
```

#### 单装箱实现

根据伪代码的逻辑，最终的实现代码如下；

```python
class Container(object):
    def _encase(self, cargo: Cargo) -> Point:
        for point in self._available_points:
            if (
                self.is_encasable(point, cargo) and
                point.x + cargo.length < self._horizontal_planar and
                point.z + cargo.height < self._vertical_planar
            ):
                flag = point
                break
        if not flag.is_valid:
            if (
                self._horizontal_planar == 0 or
                self._horizontal_planar == self.length
            ):
                if self.is_encasable(Point(0, 0, self._vertical_planar), cargo):
                    flag = Point(0, 0, self._vertical_planar)
                    self._vertical_planar += cargo.height
                    self._horizontal_planar = cargo.length 
                    # 放置了货物 不检测参考面改变
                elif self._vertical_planar < self.height:
                    self._vertical_planar = self.height
                    self._horizontal_planar = self.length
                    if __is_planar_changed():
                        flag.z == 0 # 放置失败并调整参考面
            else:
                for point in self._available_points:
                    if (
                        point.x == self._horizontal_planar and
                        point.y == 0 and
                        self.is_encasable(point, cargo) and
                        point.z + cargo.height <= self._vertical_planar
                    ):
                        flag = point
                        self._horizontal_planar += cargo.length
                        break
                        # 放置了货物 不检测参考面改变
                if not flag.is_valid:
                    self._horizontal_planar = self.length
                    if __is_planar_changed():
                        flag.z == 0 # 放置失败并调整参考面
        if flag.is_valid:
            cargo.point = flag
            if flag in self._available_points:
                self._available_points.remove(flag)
            self._adjust_setting_cargo(cargo)
            self._setted_cargos.append(cargo)
            self._available_points.extend([
                Point(cargo.x + cargo.length, cargo.y, cargo.z),
                Point(cargo.x, cargo.y + cargo.width, cargo.z),
                Point(cargo.x, cargo.y, cargo.z + cargo.height)
            ])
            self._sort_available_points()
        return flag
```

### 可变策略

本来的想法是留有策略接口，用户实现策略类来实现自定义可变策略。但 Python 中没有接口，方法是第一类型可以直接作参数传递，可为了两个策略的完整性，故使用继承重写的方式来实现可变策略。

#### 策略 Strategy 类

用户通过继承此类，重写两个静态方法，实现自定义两个装载策略：装箱顺序和货物摆放方式。

```python
from typing import Iterable, List
from Encase3D._cargo import *
from Encase3D._container import *

class Strategy(object):
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return cargos

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)
```

#### 装箱实现

此部分实现的是伪代码中外层的循环以及伪代码中没有体现的摆放方式的选择。此外，这部分代码顺便完成了空间利用率的输出。

```python
def encase_cargos_into_container(
    cargos:Iterable, 
    container:Container, 
    strategy:type
) -> float:
    sorted_cargos:List[Cargo] = strategy.encasement_sequence(cargos)
    i = 0 # 记录发当前货物
    while i < len(sorted_cargos):
        j = 0 # 记录当前摆放方式
        cargo = sorted_cargos[i]
        poses = strategy.choose_cargo_poses(cargo, container)
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            if is_encased.is_valid:
                break # 可以装入 不在考虑后续摆放方式
            j += 1  # 不可装入 查看下一个摆放方式
        if is_encased.is_valid:
            i += 1 # 成功放入 继续装箱
        elif is_encased == Point(-1,-1,0):
            continue # 没放进去但是修改了参考面位置 重装
        else :
            i += 1 # 纯纯没放进去 跳过看下一个箱子
    return sum(list(map(
            lambda cargo:cargo.volume,container._setted_cargos
        ))) / container.volume
```

### 输出与可视化 [2]

空间利用率的输出已在“可变策略”中实现，这里具体讨论容器中各个货物的位置和形态数据和三维可视化示意图。

#### 详细数据输出

详细数据为一个 csv 文件，其中的表由七个字段组成：

| 字段名 | 含义 |
| ------ | --- |
| index | 序号 |
| x | 货物放置点的 x 坐标 |
| y | 货物放置点的 y 坐标 |
| z | 货物放置点的 z 坐标 |
| length | 货物当前摆放方式下的长 |
| width | 货物当前摆放方式下的宽 |
| height | 货物当前摆放方式下的高 |

具体在容器类中实现，一个容器实例完成装载后，可以调用该方法在主程序目录下输出 csv 文档，文档名为调用保存时的时间戳组成。文档的最后一行会输出当前容器的数据。

```python
from time import time

class Container(object):
    def save_encasement_as_file(self):
        file = open(f"{int(time())}_encasement.csv",'w',encoding='utf-8')
        file.write(f"index,x,y,z,length,width,height\n")
        i = 1
        for cargo in self._setted_cargos:
            file.write(f"{i},{cargo.x},{cargo.y},{cargo.z},")
            file.write(f"{cargo.length},{cargo.width},{cargo.height}\n")
            i += 1
        file.write(f"container,,,,{self}\n")
        file.close()
```

#### 三维可视化

可视化的初始参数如下所示，其中部分配置改编自[2]：

```python
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from Encase3D._cargo import *
from Encase3D._container import *

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig:Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=20, azim=40)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
```

绘制六面颜色不同的立方体代码[2]为：

```python
def _plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
    xx = np.linspace(x, x+dx, 2)
    yy = np.linspace(y, y+dy, 2)
    zz = np.linspace(z, z+dz, 2)
    xx2, yy2 = np.meshgrid(xx, yy)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z))
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z+dz))
    yy2, zz2 = np.meshgrid(yy, zz)
    ax.plot_surface(np.full_like(yy2, x), yy2, zz2)
    ax.plot_surface(np.full_like(yy2, x+dx), yy2, zz2)
    xx2, zz2= np.meshgrid(xx, zz)
    ax.plot_surface(xx2, np.full_like(yy2, y), zz2)
    ax.plot_surface(xx2, np.full_like(yy2, y+dy), zz2)
```

绘制线框立方体代码[2]为：

```python
def _plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
```

具体可视化时，首先初始化可视化配置，然后根据容器尺寸调整坐标轴显示比例。绘制出容器线框后，遍历容器中已放置的货物逐一绘制：

```python
def _draw_container(container:Container):
    _plot_linear_cube(
        0,0,0,
        container.length,
        container.width,
        container.height
    )

def _draw_cargo(cargo:Cargo):
    _plot_opaque_cube(
        cargo.x, cargo.y, cargo.z,
        cargo.length, cargo.width, cargo.height
    )

def draw_reslut(setted_container:Container):
    plt.gca().set_box_aspect((
        setted_container.length,
        setted_container.width,
        setted_container.height
    )) 
    _draw_container(setted_container)
    for cargo in setted_container._setted_cargos:
        _draw_cargo(cargo)
    plt.show()
```

