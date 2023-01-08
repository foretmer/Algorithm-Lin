##  要求

&emsp;&emsp;物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。
设车厢为长方形，其长宽高分别为 $L，W，H$ ；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为 $l_i，w_i，h_i$ （n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：
1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为 $（0,0,0） $，车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；
2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为 $（0,0,0）$ 的角相对应的角在车厢中的坐标，并计算车厢的填充率。
问题分解为基础和高级部分。

基础部分：
1. 所有的参数为整数；
2. 静态装箱，即从 $n$ 个箱子中选取 $m$ 个箱子，并实现 $m$ 个箱子在车厢中的摆放（无需考虑装箱的顺序，即不需要考虑箱子从内向外，从下向上这种在车厢中的装箱顺序）；
3. 所有的箱子全部平放，即箱子的最大面朝下摆放；
4. 算法时间不做严格要求，只要1天内得出结果都可。

高级部分：
1. 参数考虑小数点后两位；
2. 实现在线算法，也就是箱子是按照随机顺序到达，先到达先摆放；
3. 需要考虑箱子的摆放顺序，即箱子是从内到外，从下向上的摆放顺序；
4. 因箱子共有3个不同的面，所有每个箱子有6种不同的摆放状态；
5. 算法需要实时得出结果，即算法时间小于等于2秒。

## 设计

&emsp;&emsp;此次实验对该问题的基础部分进行了实现和测试。本文实现的算法参考了博客https://blog.csdn.net/qq_29848559/article/details/113035681 。所有的代码和测试均由本组所有成员独立完成。

&emsp;&emsp;三维装箱问题是一个NPC问题，可以在多项式时间内验证答案是否正确，但无法在多项式时间内找到准确解。因此，本算法采用了类似于操作系统中空闲内存的申请方法以及日常生活中装货工人进行装货的启发式算法，即将已知货物从大到小进行排序，优先填装体积较大的货物，并将货物从按照车厢内从内到外、从下到上的顺序进行状态，并且装填的过程中尽量保证货物之间紧贴。

&emsp;&emsp;本算法中用到的数据结构：```Point```结构体，定义了一个坐标，包含```x```、```y```和```z```。```Box```类，定义了长```length```、宽```width```、高```height```和旋转方法```rotate()```。长宽高是根据其在空间中的放置姿态来定义的，例如，对于一个```Box```类，```length=1```，```width=2```，```height=3```，对其调用```rotate()```方法，会变为```length=2```，```width=1```，```height=3```。```rotate()```方法是周期性的，对每个box对象每调用6次```rotate()```方法，```Box```的长宽高顺序会恢复到原来的状态。

&emsp;&emsp;本实验采用了首次适应（First-Fit）的算法。思路如下：首先将所有物体按照体积大小进行排序，按序取货。设放置进货箱的货物组成的```Box```列表为```loadedBoxes```，每个元素都包含了货箱的放置坐标和尺寸```<Point, Box>```。对于第一件货物，将其尝试放入坐标为 $(0,0,0)$ 的位置，如果无法放下，则将其按照一定的顺序进行旋转（转置），容易得到，最多可以旋转五次，第六次会回到初始的状态，一旦发现可以放置则立即放置。如果六种状态均无法装入货箱，则丢弃并选取下一个货物。对于后来的货物，均按此处理。第一件货物被放置后，```loadedBoxes```不为空，按照顺序遍历其中的元素，对于每个元素，设其为```loadedBoxes[i]```，其坐标为```(loadedBoxes[i].point.x, loadedBoxes[i].point.y, loadedBoxes[i].point.z)```，长宽高分别为```loadedBoxes[i].length```、```loadedBox[i].width```和```loadedBox[i].height```。现有待放入箱子```box```，对于每个这样的```box```，都判断其是否能放到```loadedBox[i]```的前方、右方或者上方，更具体地说，依次判断```box```能否放置到```(loadedBoxes[i].point.x + loadedBoxes[i].box.length,loadedBoxes[i].point.y,loadedBoxes[i].point.z)```、```(loadedBoxes[i].point.x,loadedBoxes[i].point.y+loadedBox[i].box.width,loadedBoxes[i].point.z)```和```(loadedBoxes[i].point.x,loadedBoxes[i].point.y, loadedBoxes[i].point.z + loadedBoxes[i].box.height)```这三个点。且```box```的表面与```loadedBoxes[i]```的表面是紧贴的。在这个过程中，一旦发现可以放置则立即放置，再对下一个物体进行处理。对所有物体都如此处理，直到结束。

##  分析及结果

&emsp;&emsp;本实验采用C++实现了上述算法，首先对待放置物体进行排序，调用标准库排序函数```std::sort()```(在``algorithm``头文件中)，复杂度为 $O(nlogn)$ 。对每一个物体进行取出，这个过程共取 $n$ 次，对每个取到的第 $i$ 个物体，又要根据之前已经放置的 $i-1$ 个物体来确定本物体的放置位置，对于三个候选的点，又必须根据已经放置的 $i-2$ 个物体来判断该点是否会阻挡该物体放置在这几个点。显然，整个过程的时间复杂度为 $\Theta(n^3)$ 。

&emsp;&emsp;本实验核心算法实现在```Solution.cpp```的```firstFit()```函数中:
```cpp
void firstFit(std::vector<Box>& boxes, int carriageLength, int carriageWidth, int carriageHeight, bool shuffle = false)
{
    using Point_Box = std::pair<Point, Box>;
    auto t1 = clock();
    if (!shuffle) std::sort(boxes.begin(), boxes.end(), [](const Box& l, const Box& r)->bool {return l.Volume() > r.Volume(); });
    else std::shuffle(boxes.begin(), boxes.end(), std::mt19937(time(nullptr)));
    std::vector<Point_Box> loadedBoxes;
    int loadedVolume = 0;
    int loadedNum = 0;
    for (decltype(boxes.begin()) boxIter = boxes.begin(); boxIter != boxes.end(); ++boxIter)
    {
        //如果一个箱子都还没放进去
        if (loadedBoxes.empty())
        {
            //对这个箱子做最多5次旋转，第6次旋转就恢复原样了
            //旋转五次都放不进去，直接扔掉
            for (int j = 0; j <= 5; ++j)
            {
                //如果在某个状态能放进去，那就直接放进去
                if (boxIter->Length() <= carriageLength && boxIter->Width() <= carriageWidth && boxIter->Height() <= carriageHeight)
                {
                    loadedBoxes.push_back(Point_Box(Point(0, 0, 0), *boxIter));
                    loadedVolume += boxIter->Volume();
                    ++loadedNum;
                    break;
                }
                //否则对箱子进行旋转，最多5次
                else
                {
                    boxIter->Rotate();
                }
            }
        }
        //已有箱子被放置
        /*在首次适应算法中，对于每个已经放置的箱子（设为p），它的坐标为(p.x, p.y, p.z)，
        三个基准点的坐标分别为(p.x, p.y, p.z + height)，(x, y + width, z)，(x + length, y, z)
        只需要判断box能否放到这三个点即可
        即判断如果在这三个点放置箱子，都去判断之前每一个已装填的箱子会不会挡到这个箱子
        */
        else
        {
            for (const auto& loaded : loadedBoxes)
            {
                bool flag = false;
                Point pos1 = Point(loaded.first.x, loaded.first.y, loaded.first.z + loaded.second.Height());
                Point pos2 = Point(loaded.first.x, loaded.first.y + loaded.second.Width(), loaded.first.z);
                Point pos3 = Point(loaded.first.x + loaded.second.Length(), loaded.first.y, loaded.first.z);
                for (int j = 0; j <= 5; ++j)
                {
                    if (canLoad(*boxIter, pos1, loadedBoxes, carriageLength, carriageWidth, carriageHeight))
                    {
                        loadedBoxes.push_back(Point_Box(Point(pos1), *boxIter));
                        loadedVolume += boxIter->Volume();
                        ++loadedNum;
                        flag = true;
                        break;
                    }
                    if (canLoad(*boxIter, pos2, loadedBoxes, carriageLength, carriageWidth, carriageHeight))
                    {
                        loadedBoxes.push_back(Point_Box(Point(pos2), *boxIter));
                        loadedVolume += boxIter->Volume();
                        ++loadedNum;
                        flag = true;
                        break;
                    }
                    if (canLoad(*boxIter, pos3, loadedBoxes, carriageLength, carriageWidth, carriageHeight))
                    {
                        loadedBoxes.push_back(Point_Box(Point(pos3), *boxIter));
                        loadedVolume += boxIter->Volume();
                        ++loadedNum;
                        flag = true;
                        break;
                    }
                    //这个姿势装载不进去，那么就旋转一下
                    boxIter->Rotate();
                }
                //既然已经填进去了，就不用判断后面的块会不会挡住了
                if (flag) break;
            }
        }
    }
    auto t2 = clock();
    std::cout << "放进去" << loadedNum << "个。" <<  "填充率" << loadedVolume * 100.0 / (carriageHeight * carriageLength * carriageWidth) << "%。" << "耗时" << (double)(t2 - t1) / CLOCKS_PER_SEC << "s。" << std::endl;
    for (const auto& i : loadedBoxes)
    {
        std::cout << "位置：" << i.first << "，形状：" << i.second << std::endl;
    }
}
```
且分别在排序状态下和随机打乱的状态下进行了测试。测试项目包括每组装进的物体个数、填充率和所用时间。具体源代码和结果见附件。

&emsp;&emsp;从表中看出，排序+放置算法的最大填充率为87.95%，平均填充率为77.39%，平均耗时56ms；而打乱+放置算法的最大填充率为79.20%，平均填充率为71.66%，平均耗时75ms。从排序和打乱两组对照中可以发现，该算法对较大体积的物品友好，而较小的物品会在空间内形成较多难以利用的空间碎片。

## 编译
需要编译器支持C++11。
```bash
g++ -std=c++11 -o main *.cpp && ./main
```
