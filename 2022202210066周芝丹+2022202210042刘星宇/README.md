<h2>问题介绍</h2>

给定一个长方体车厢Container，其长宽高分别是 $L,W,H$ ，体积为 $V$ ；共有 $n$ 个箱子集合cargos，箱子也为长方体，第 $i$ 个箱子的长宽高为
$l_i,w_i,h_i$ （ $n$ 个箱子的体积总和是远远大于车厢的体积），
每个箱子体积为 $v_i=l_iw_ih_i$，定义车厢内所有箱子的体积之和为：

$$V_s = \sum_{cargo_i\in S}v_i$$

问题的目标是选择集合cargos的一个子集 $S$，使得 $V_s$ 最大，且满足以下条件和假设：

- 从 $n$ 个箱子中选择 $m$ 个箱子，并实现 $m$ 个箱子在车厢中的摆放；
- 箱子必须完全包含在容器内；
- 任意两个货物内的任意一点不可在空间中的同一位置；
- 需要考虑装箱的顺序，达到尽量优解；
- 箱子各个面都可以朝下放置，没有上下左右前后的区别。

我们输入车厢的长宽高数据和货物的数量及各自的长宽高数据，输出示意图和利用率：

$$\eta=\frac{V_s}{V}$$

<h2>算法介绍</h2>
<h3>1. 初步</h3>

假设给定的箱子序列是 $(b_1,b_2,...,b_n)$，首先第一个箱子的可放置点是 $(0,0,0)$，
若第一个箱子可以放入点 $(0,0,0)$，则第2个箱子的可放置点有3个，分别为 $(l_1,0,0)$,$(0,w_1,0)$,$(0,0,h_1)$，假设第2个箱子选择了点 $(l_1,0,0)$，
则我们删除点 $(l_1,0,0)$，同时增加点 $(l_1+l_2,0,0)$,$(l_1,w_2,0)$,$(l_1,0,h_2)$，
即第3个箱子的可放置点有5个。考虑第 $i$ 个箱子，若其选择了点 $(x,y,z)$，则我们先从
可放置点中删除点 $(x,y,z)$，再增加 $(x+l_i,y,z),(z,y+w_i,z),(x,y,z+h_1)$，
如下图黑圆点所示，若所有可放置点都不能放入第 $i$ 个箱子，则可放置点不更新，直接考虑第 $i+1$ 个箱子。

我们考虑两条参考线形成的参考面， $z$ 轴上的参考线 $L_z$ 和 $x$ 轴上的 $L_x$。我们的放置策略是：
按顺序考虑箱子，在考虑箱子 $b_i$ 时，先把可放置点按 $y$ 坐标从小到大排序， $y$ 坐标相同的按 $x$ 
坐标从小到大排序， $x,y$ 坐标都相同的按 $z$ 坐标从小到大排序，按照排好序的可放位置去检测 $b_i$
能否放入该位置。在评判箱子 $b_i$ 能否放入位置 $(x,y,z)$ 中时，不仅要求其不能与车厢和其他箱子相交，
而且要求 $z+h_i\leq L_z, x+l_i\leq L_x$ 。在检测一个可放位置位置时，我们尝试所有可放置方向，
当找到第1个可放入点时，则把箱子 $b_i$ 放入该位置，并更新可放置点。若所有可放置点都不能放入
该箱子，则分一下两种情况考虑：（1）若 $L_x< L$，则提高 $x$ 轴上的参考线，即把该箱子作为水平
方向参考箱子；（2）否则，提高 $z$ 轴上的参考线。如果提高参考线后，该箱子还是不能放下，
这在此装填中，该箱子不能放入容器中，在以后的装填中将不再考虑该箱子。
![image](https://github.com/ZhouZhidan1212/3D_packing_homework/blob/main/images/image1.png)
- 与其他箱子的碰撞检测：直接在三维空间中确定两个实体是否冲突有些困难。于是，在这里，我们采用的
方法是在二维平面上考虑三维空间中的实体投影，在 $xy$ 面、 $xz$ 面和 $yz$ 面上的投影情况判断是否冲突。
任意平行于长方形车厢放置的长方体货物，如果它们在任意三个方向上的投影没有重叠，则两者就没有冲突。
而对于平面上的长方体而言，相对在左边的长方体的右上角坐标如果小于相对右边的长方体的左下角坐标，
则两个长方形没有重叠。碰撞思想的检测在模块`_is_cargos_collide()`中体现，判断长方形是否冲突在`_is_rectangles_overlap()`；
- 伪代码的内循环体现在 `_encase()`与`_extend_points()`里；外训练在文件`__init__.py`中掌控程序。


**伪代码**：

$I$代表可放置点列表.

```Python
初始化 容器;初始化 货物列表;
I = [(0,0,0)]，Lx = Lz = 0;
while i = 1 until n{
    flag = 未放置未更新;
    for (x,y,z) in I{
        if (bi可以放置在可放置点 并且x+li<=Lx,z+hi<=Lz){
            flag = 已放置;
            退出 可放置点 循环;}
    }
    if (flag 标记有 未放置){
        if (Lx == 0 或者 Lx == L){
            if (bi可以放入位置(0,0,Lz)){
                将bi放置在(0,0,Lz);
                x = 0, y = 0, Lz = Lz+hi, Lx = li
                flag = 已放置已更新;}
            else if (Lz < H){
                Lz = H, Lx = H;
                flag = 未放置已更新;}
        }else{
            for (x,y,z) in I{
                if (bi可以放置在(x,y,z) 并且z+hi<=Lz){
                    Lx=Lx+li;
                    flag = 已放置已更新;
                    退出 可放置点 循环;}
            }
            if (flag 标记有 未放置){
                Lx = H;
                flag = 未放置已更新;}
        }
    }
    if (flag 标记有 已放置){
        把bi放入位置(x,y,z), I=I/{(x,y,z)};
        I新增三个点可放置点;
        i++;
    }else if(flag 标记为 未放置已更新){
        i--;
    }else if(flag 标记为 未放置未更新){
        i++;
    }
}

```

### 2. 改进（退火算法）

之前的顺序是死板的按照箱子体积从大到小摆放的，但我们知道箱子的装填顺序对效果影响很大，因此我们考虑加入了模拟退火算法来改变箱子的摆放顺序。
这里我们将领域定为随机选取两类箱子的装填顺序。因为我们的目标是使装入车厢的箱子总体积最大，因此在生成初解时，考虑贪心策略，
先把箱子体积从大到小的顺序排列。根据模拟退火的特性，我们动态增加邻域的大小。记初始温度为 $S_t$ ，结束温度为 $E_t$ ，温度下降率为
$d_t$ ，邻域初始大小为 $L$ ，温度下降一次时增加邻域大小为 $d_L$ 。设初始输入箱子集合为 $B$ ，用 $f$ 来记录当前的填充率，用 $f_{best}$
记录当前最高的填充率， $B_{best}$ 记录最高填充率时对应的顺序，用 $t$ 表示当前温度， $L_t$ 表示当前邻域长度。在实验中，我们使用了二次退火来保证解的稳定性。

**伪代码**：

```Python
将箱子体积从大到小顺序排序
f = fbest = encase_cargos_into_container(cargo)
Bbest = B
for i = 1 to 2{
    t = St, Lt = L;
    while (t >= Et):
        for j in range(1, Lt){
             随机调换两个箱子顺序,得到B1；
             f1 = encase_cargos_into_container(cargo)；
             df = f' - f；}
             if (df > 0){
                  f = f1, B = B1；
                  if(f > fbest){
                       fbest = f, Bbest = B}
                  else{
                      随机生成一个(0,1)之间的数x；
                      if (x < exp(10*df/t)){
                           f = f1, B = B1}
         Lt += dL, t *= dt

```

但此算法有个问题是时间消耗巨大，在初步算法中，平均只需要花费20s时间，而加入退火算法后，时间长达几小时。

### 3. 失败案例（放置面）

因为不同箱子有六个不同的放置面，根据现实经验，放置一定数量的箱子后，每放入一个箱子，若这个箱子与已放置的箱子
重叠面面积越大（也就是此箱子与已放置箱子越紧贴），则装箱效果理应越好，如下图所示，图二a的摆放方式应比图二b的
摆放方式更合理。受此启发，我们在程序中引入了此算法。
![image](https://github.com/ZhouZhidan1212/3D_packing_homework/blob/main/images/image2.png)
假定此次放入第 $i$ 个箱子， $b_i$ ，计算它与已放置箱子的重叠面积，可以转化为它与相邻箱子在 $xy$ 平面、 $xz$ 平面和 $yz$
平面的投影重叠面积，投影重叠面积越大，说明它与已放置箱子贴的越紧密。而 $b_i$ 与相邻箱子的投影重叠面积又可以近似于
此箱子与紧贴三个坐标平面的箱子的重叠面积，于是，我们存储了所有紧贴三个坐标平面的箱子，创建`rectangles_overlap_area()`
来计算 $b_i$ 与那些箱子的重叠面积，在每放入一个箱子，计算其各个放置方向与那些箱子的重叠面积大小，再取最大的那个姿势放入。

但是结果却不尽人意，不管是装箱全程都使用此算法进行放置，还是先采用此算法放置后同方向放置（即采用同长宽高、同放置面），
抑或是先同方向放置再采用此方法放置，都使装箱率有所下降。对于一直采用此算法放置或者先采用此算法放置后随机放置，
由于一开始箱子放置少，这样刻意地放置，可能使得很多箱子的放置方向不一致，导致箱子间的间隙增多，不如一直采用一种放
置方式，整齐划一排列；而先同方向放置再采用此方法放置，由于算法比较粗糙，放置多个箱子后， $xy$ 平面、 $xz$ 平面和 $yz$
平面基本都已经被已放置箱子紧贴了，所以此时计算待放置箱子与这三个面的阴影面积重合时，各个放置方向的重合面积几乎一致
不变，这也是为什么这个方法与未加此算法跑出来的结果差不多。

## 实验与运行结果

### 1. 代码结构

所有算法的实现将组织在一个名为*算法设计*的包中。该包分为五个模块：`__init__`、`_cargo`、`_container`、`_Program`和`drawer`。

- `__init__`：用于初始化包并组织算法代码和可变策略类；
- `_cargo`：组织箱子的代码；
- `_container`：关于容器的相关类代码；
- `drawer`：组织绘制3D效果图的相关函数代码；
- `Program`：总的控制和运行文件，加入箱子和容器尺寸命令。

### 1.1 初步算法代码

#### 1. `__init__.py`

```Python
from typing import Iterable, List
from _cargo import *
from _container import *
import random

class Strategy(object):
    # 继承此类 重写两个静态函数 实现自定义两个装载策略: 装箱顺序 和 货物.
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return cargos

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)

def encase_cargos_into_container(
    cargos:Iterable, 
    container:Container, 
    strategy:type
) -> float:
    sorted_cargos:List[Cargo] = strategy.encasement_sequence(cargos)
    i = 0 # 记录发当前货物
    print(sorted_cargos,'ffff')
    # 随意调换四个摆放顺序
    for k in range(4):
        p1 = random.randint(int(len(sorted_cargos)/2), int(len(sorted_cargos)*3/4)-1)
        p2 = random.randint(int(len(sorted_cargos)*3/4), len(sorted_cargos)-1)
        sorted_cargos[p1], sorted_cargos[p2] = sorted_cargos[p2], sorted_cargos[p1]

    print(sorted_cargos,'ssss')

    while i < len(sorted_cargos):
        j = 0 # 记录当前摆放方式
        cargo = sorted_cargos[i]
        poses = strategy.choose_cargo_poses(cargo, container)

        # 没加任何东西：
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                break # 可以装入 不在考虑后续摆放方式
            j += 1  # 不可装入 查看下一个摆放方式
        container._extend_points(cargo, temp_flag[-1])

        # 一直都用最小面
        '''area = [0 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                print(area)
                area[j] = container.rectangles_overlap_area_sum(cargo) 
            j += 1
        b = area.index(max(area))
        cargo.pose = poses[b]
        container._extend_points(cargo, temp_flag[b])'''

        # 先随机放，再用最小面
        '''if i <= 0.3*len(sorted_cargos):
            temp_flag = []
            while j < len(poses):
                cargo.pose = poses[j]
                is_encased = container._encase(cargo)
                temp_flag.append(deepcopy(is_encased))
                if is_encased.is_valid:
                    break # 可以装入 不在考虑后续摆放方式
                j += 1  # 不可装入 查看下一个摆放方式
            container._extend_points(cargo, temp_flag[-1])

        elif i > 0.3*len(sorted_cargos):
            area = [0 for _ in range(len(poses))]
            temp_flag = []
            while j < len(poses):
                cargo.pose = poses[j]
                is_encased = container._encase(cargo)
                temp_flag.append(deepcopy(is_encased))
                if is_encased.is_valid:
                    print(area)
                    area[j] = container.rectangles_overlap_area_sum(cargo) 
                j += 1
            b = area.index(max(area))
            cargo.pose = poses[b]
            container._extend_points(cargo, temp_flag[b])#'''
        
        # 放底面最大面
        '''area = [99999999 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                area[j] = container.rectangles_overlap_area_bottom(cargo) 
                #print(area,'~~')
                #print(cargo,'!!')
            j += 1
        b = area.index(min(area))
        cargo.pose = poses[b]
        print(cargo,'!!!')
        container._extend_points(cargo, temp_flag[b])'''

        #放底面最小面
        '''area = [0 for _ in range(len(poses))]
        temp_flag = []
        while j < len(poses):
            cargo.pose = poses[j]
            is_encased = container._encase(cargo)
            temp_flag.append(deepcopy(is_encased))
            if is_encased.is_valid:
                print(area)
                area[j] = container.rectangles_overlap_area_bottom(cargo) 
            j += 1
        b = area.index(max(area))
        cargo.pose = poses[b]
        container._extend_points(cargo, temp_flag[b])'''

        
        if is_encased.is_valid:
            container._setted_cargos.append(cargo)
            i += 1 # 成功放入 继续装箱
        elif is_encased == Point(-1,-1,0):
            continue # 没放进去但是修改了参考面位置 重装
        else :
            i += 1 # 纯纯没放进去 跳过看下一个箱子
    return sum(list(map(
            lambda cargo:cargo.volume,container._setted_cargos
        ))) / container.volume



class VolumeGreedyStrategy(Strategy):
    @staticmethod
    def encasement_sequence(cargos:Iterable) -> Iterable:
        return sorted(cargos, key= lambda cargo:cargo.volume,reverse=1)

    @staticmethod
    def choose_cargo_poses(cargo:Cargo, container:Container) -> list:
        return list(CargoPose)
```

#### 2. `cargo.py`

```Python
from enum import Enum


class CargoPose(Enum):
    tall_wide = 0
    tall_thin = 1
    mid_wide = 2
    mid_thin = 3
    short_wide = 4
    short_thin = 5


class Point(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    @property
    def is_valid(self) -> bool:
        return self.x >= 0 and self.y >=0 and self.z>= 0
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y, self.z)


class Cargo(object):
    def __init__(self, length: int, width: int, height: int) -> None:
        self._point = Point(-1, -1, -1)
        self._shape = {length, width, height}
        self._pose = CargoPose.tall_thin

    def __repr__(self) -> str:
        return f"{self._point} {self.shape}"

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

    @property
    def y(self) -> int:
        return self._point.y

    @y.setter
    def y(self, new_y: int):
        self._point = Point(self.x, new_y, self.z)

    @property
    def z(self) -> int:
        return self._point.z

    @z.setter
    def z(self, new_z: int):
        self._point = Point(self.z, self.y, new_z)

    @property
    def length(self) -> int:
        return self.shape[0]

    @property
    def width(self) -> int:
        return self.shape[1]

    @property
    def height(self) -> int:
        return self.shape[-1]

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

    @property
    def shape(self) -> tuple:
        return self._shape_swiche[self._pose]

    @shape.setter
    def shape(self, length, width, height):
        self._shape = {length, width, height}

    @property
    def volume(self) -> int:
        reslut = 1
        for i in self._shape:
            reslut *= i
        return reslut
```

#### 3. `_container.py`

```Python
from time import time
from typing import List
from _cargo import *
from copy import deepcopy


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
        self._available_points = [Point(0, 0, 0)]  # 可放置点有序集合
        self._setted_cargos : List[Cargo] = []
        self.plane_shadow = [[],[],[]] # 创建紧贴坐标面的cargo列表

    def _sort_available_points(self):
        self._available_points.sort(key=lambda x: x.z)
        self._available_points.sort(key=lambda x: x.x)
        self._available_points.sort(key=lambda x: x.y)

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


        return flag

    def _extend_points(self,cargo,flag):
        if flag.is_valid:
            print(flag)
            print(cargo,'$$')
            cargo.point = flag
            print(cargo,'^^')
            if flag in self._available_points:
                self._available_points.remove(flag)
            self._adjust_setting_cargo(cargo)
       #     self._setted_cargos.append(cargo)
            self._available_points.extend([
                Point(cargo.x + cargo.length, cargo.y, cargo.z),
                Point(cargo.x, cargo.y + cargo.width, cargo.z),
                Point(cargo.x, cargo.y, cargo.z + cargo.height)
            ])
            #若cargo贴着坐标面，则加入到各自的分组中
            if cargo.x == 0:
                self.plane_shadow[0].append(cargo) #yz面货物集合
            if cargo.y == 0:
                self.plane_shadow[1].append(cargo) #xz面货物集合
            if cargo.z == 0:
                self.plane_shadow[2].append(cargo) #xy面货物集合
            self._sort_available_points()

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
    
    # 求出每一个cargo与三个平面投影面积重叠的和
    def rectangles_overlap_area_sum(self, cargo: Cargo):
        temp = deepcopy(cargo)
        area = 0
        for i in range(3):
            for j in range(len(self.plane_shadow[i])):
                plusarea = rectangles_overlap_area(self.plane_shadow[i][j], temp, i)
                area += plusarea
        return area

    # 求每一个cargo与底面投影面积重叠面积
    def rectangles_overlap_area_bottom(self, cargo: Cargo):
        temp = deepcopy(cargo)
        area = 0
        for j in range(len(self.plane_shadow[2])):
            plusarea = rectangles_overlap_area(self.plane_shadow[2][j], temp, 2)
            area += plusarea
        return area



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

    @property
    def length(self) -> int:
        return self._length

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def volume(self) -> int:
        return self.height * self.length * self.width


def _is_rectangles_overlap(rec1:tuple, rec2:tuple) -> bool:
    return not (
        rec1[0] >= rec2[2] or rec1[1] >= rec2[3] or
        rec2[0] >= rec1[2] or rec2[1] >= rec1[3]
    )


def rectangles_overlap_area(cargo0:Cargo, cargo1:Cargo, opt):
    area = 0
    if opt == 0:
        rec0 = cargo0.get_shadow_of("yz")
        rec1 = cargo1.get_shadow_of("yz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1]))
    if opt == 1:
        rec0 = cargo0.get_shadow_of("xz")
        rec1 = cargo1.get_shadow_of("xz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1])) 
    if opt == 2:
        rec0 = cargo0.get_shadow_of("yz")
        rec1 = cargo1.get_shadow_of("yz")
        if _is_rectangles_overlap(rec0, rec1):
            # 求重叠阴影面积
            area = area + min(abs(rec0[0]-rec1[2]),abs(rec0[2]-rec1[0])) * min(abs(rec0[1]-rec1[3]),abs(rec0[3]-rec1[1]))   
    return area

    


def _is_cargos_collide(cargo0: Cargo, cargo1: Cargo) -> bool:
    return (
        _is_rectangles_overlap(cargo0.get_shadow_of("xy"), cargo1.get_shadow_of("xy")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("yz"), cargo1.get_shadow_of("yz")) and
        _is_rectangles_overlap(cargo0.get_shadow_of("xz"), cargo1.get_shadow_of("xz"))
    )
```


#### 4. `drawer.py`

```Python
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from _cargo import *
from _container import *
import random

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig:Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=20, azim=40)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

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

cclor = ['tomato', 'indianred', 'salmon', 'rosybrown', 'sienna', 'maroon']
cclor = ['k', 'dimgrey', 'gray', 'darkgray', 'lightgray', 'whitesmoke']

def _plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
    xx = np.linspace(x, x+dx, 2)
    yy = np.linspace(y, y+dy, 2)
    zz = np.linspace(z, z+dz, 2)
    xx2, yy2 = np.meshgrid(xx, yy)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z), color=random.choice(cclor))
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z+dz), color=random.choice(cclor))
    yy2, zz2 = np.meshgrid(yy, zz)
    ax.plot_surface(np.full_like(yy2, x), yy2, zz2, color=random.choice(cclor))
    ax.plot_surface(np.full_like(yy2, x+dx), yy2, zz2, color=random.choice(cclor))
    xx2, zz2= np.meshgrid(xx, zz)
    ax.plot_surface(xx2, np.full_like(yy2, y), zz2, color=random.choice(cclor))
    ax.plot_surface(xx2, np.full_like(yy2, y+dy), zz2, color=random.choice(cclor))

def _plot_linear_cube(x, y, z, dx, dy, dz, color='grey'):
    # ax = Axes3D(fig)
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

#### 5. `Program.py`

```Python
from _container import *
import drawer
from _cargo import *
from __init__ import *
import time


if __name__ == "__main__":
    '''cargos = [Cargo(108,76,30) for _ in range(2)] #246240
    #cargos.extend([Cargo(110,43,25) for _ in range(25)]) #118250
    cargos.extend([Cargo(92,81,55) for _ in range(2)]) #409860
    cargos.extend([Cargo(210,120,100) for _ in range(1)])#'''

    '''cargos = [Cargo(108,76,30) for _ in range(40)] #246240
    cargos.extend([Cargo(110,43,25) for _ in range(33)]) #118250
    cargos.extend([Cargo(92,81,55) for _ in range(39)]) #409860'''
    '''cargos = [Cargo(91,54,45) for _ in range(32)] 
    cargos.extend([Cargo(105,77,72) for _ in range(24)]) 
    cargos.extend([Cargo(79,78,48) for _ in range(30)])# '''
    cargos = [Cargo(78,37,27) for _ in range(63)] 
    cargos.extend([Cargo(89,70,25) for _ in range(52)]) 
    cargos.extend([Cargo(90,84,41) for _ in range(55)])# '''


    '''cargos = [Cargo(49,25,21) for _ in range(22)] 
    cargos.extend([Cargo(60,51,41) for _ in range(22)]) 
    cargos.extend([Cargo(103,76,64) for _ in range(28)]) 
    cargos.extend([Cargo(95,70,62) for _ in range(25)]) 
    cargos.extend([Cargo(111,49,26) for _ in range(17)])#'''
    '''cargos = [Cargo(88,54,39) for _ in range(25)] 
    cargos.extend([Cargo(94,54,36) for _ in range(27)]) 
    cargos.extend([Cargo(87,77,43) for _ in range(21)]) 
    cargos.extend([Cargo(100,80,72) for _ in range(20)]) 
    cargos.extend([Cargo(83,40,36) for _ in range(24)])#'''
    '''cargos = [Cargo(90,70,63) for _ in range(16)] 
    cargos.extend([Cargo(84,78,28) for _ in range(28)]) 
    cargos.extend([Cargo(94,85,39) for _ in range(20)]) 
    cargos.extend([Cargo(80,76,54) for _ in range(23)]) 
    cargos.extend([Cargo(69,50,45) for _ in range(31)])#'''
    '''cargos = [Cargo(74,63,61) for _ in range(22)] 
    cargos.extend([Cargo(71,60,25) for _ in range(12)]) 
    cargos.extend([Cargo(106,80,59) for _ in range(25)]) 
    cargos.extend([Cargo(109,76,42) for _ in range(24)]) 
    cargos.extend([Cargo(118,56,22) for _ in range(11)])#'''


    '''cargos = [Cargo(98,73,44) for _ in range(6)] 
    cargos.extend([Cargo(60,60,38) for _ in range(7)]) 
    cargos.extend([Cargo(105,73,60) for _ in range(10)]) 
    cargos.extend([Cargo(90,77,52) for _ in range(3)]) 
    cargos.extend([Cargo(66,48,24) for _ in range(5)])
    cargos.extend([Cargo(106,76,55) for _ in range(10)]) 
    cargos.extend([Cargo(55,44,36) for _ in range(12)]) 
    cargos.extend([Cargo(82,58,23) for _ in range(7)]) 
    cargos.extend([Cargo(74,61,58) for _ in range(6)])
    cargos.extend([Cargo(81,39,24) for _ in range(8)]) 
    cargos.extend([Cargo(71,65,39) for _ in range(11)]) 
    cargos.extend([Cargo(105,97,47) for _ in range(4)]) 
    cargos.extend([Cargo(114,97,69) for _ in range(5)])
    cargos.extend([Cargo(103,78,55) for _ in range(6)]) 
    cargos.extend([Cargo(93,66,55) for _ in range(6)])#'''

    start = time.time()
    case = Container(587,233,220)
    print(
        encase_cargos_into_container(cargos,case,VolumeGreedyStrategy)
    )
    end = time.time()
    print("消耗时间为：", end - start)
    case.save_encasement_as_file()
    drawer.draw_reslut(case)
```

### 1.2 加入退火算法代码

其余的文件没有变动的，改动了Program文件。

#### 1. `Program.py`

```Python    
from _container import *
import drawer
from _cargo import *
from __init__ import *
from random import *
import numpy as np


if __name__ == "__main__":
    #模拟退火参数设置
    St = 1
    L = 0
    Et = 0.4
    dL = 3
    dt = 0.9
    ###################

    # E1-1
    cargos = [Cargo(108, 76, 30 ) for _ in range(40)]
    cargos.extend([Cargo(110, 43, 25) for _ in range(33)])
    cargos.extend([Cargo(92, 81, 55) for _ in range(39)])

    case = Container(587,233,220)
    sorted_list = sorted(cargos, key=lambda cargo: cargo.volume, reverse=1)
    print(sorted_list)
    start_list = deepcopy(sorted_list)
    fstart = encase_cargos_into_container(cargos,case,sorted_cargos=sorted_list) #初始摆放时的空间利用率
    print(start_list,'1111')
    f = fstart
    fbest = fstart
    #print(f)
    Bbest = case._setted_cargos     #初识摆放时的放置顺序
    for i in [1,2]: # 进行两次退火
        print("第%d次退火" %i)
        t = St
        Lt = L
        while(t >= Et):
            for j in range(Lt):
                #E1-1
                cargos = [Cargo(108, 76, 30 ) for _ in range(40)]
                cargos.extend([Cargo(110, 43, 25) for _ in range(33)])
                cargos.extend([Cargo(92, 81, 55) for _ in range(39)])
                case = Container(587,233,220)              

                # 交换路径中的这2个节点的顺序
                s1, s2 = randint(0, int(len(sorted_list)/2) - 1), randint(int(len(sorted_list)/2), len(sorted_list) - 1)
                start_list[s1], start_list[s2], = start_list[s2], start_list[s1]
                
                print(start_list,'!!')
                print(len(start_list))
                temp_list = deepcopy(start_list)
                temp_list2 = deepcopy(start_list)
                f1 = encase_cargos_into_container(cargos, case, sorted_cargos = temp_list)
                print("第%d次的利用率 = " %j, f1)
                #drawer.draw_reslut(case,'')  # 画出最终装箱的效果图
                B1 = case._setted_cargos
                df = f1 - f
                if(df > 0):
                    f = f1
                    B = B1
                    if (f > fbest):
                        fbest = f
                        Bbest = B
                        start_list = temp_list2
                else:
                    x = random()
                    if(x < np.exp(10*df/t)):
                        f = f1
                        B = B1
                        start_list = temp_list2
            Lt += dL
            t *= dt
    
    print("初始装箱率=", fstart)
    print("最高的装箱率=", fbest)
```

### 2. 结果评估

下图是装箱结果示意图：
![image](https://github.com/ZhouZhidan1212/3D_packing_homework/blob/main/images/image3.png)

下表是实验结果，由于退火算法耗时太长，每一次运算耗时三四个小时，因此我们就选择实验了几个case：
|||||
|-|-|-|-|
|||初步算法|退火算法|
|3种箱子|E1-1|0.862179|0.870249|
||E1-2|0.825345|0.846219|
||E1-3|0.810554|0.829913|
||E1-4|0.915273|\|
||E1-5|0.859043|\|
|5种箱子|E2-1|0.885719|0.892465|
||E2-2|0.850537|0.867355|
||E2-3|0.755692|0.794312|
||E2-4|0.816871|\|
||E2-5|0.856844|\|
|8种箱子|E3-1|0.880662|0.902684|
||E3-2|0.839484|0.860121|
||E3-3|0.867228|\|
||E3-4|0.859428|\|
||E3-5|0.838870|\|
|10种箱子|E4-1|0.831654|0.862310|
||E4-2|0.859887|0.880219|
||E4-3|0.854682|\|
||E4-4|0.856146|\|
||E4-5|0.818804|\|
|15种箱子|E5-1|0.862838|0.894377|
||E5-2|0.857390|0.883702|
||E5-3|0.855311|\|
||E5-4|0.819068|\|
||E5-5|0.847980|\|

