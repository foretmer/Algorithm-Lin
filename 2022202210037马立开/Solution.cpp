#include "Datastructure.h"
#include "Solution.h"
#include "stdafx.h"

/// @brief 给定两个长方体，判断两者空间上是否有重叠
/// @param b1 第一个长方体形状
/// @param p1 第一个长方体坐标
/// @param b2 第二个长方体形状
/// @param p2 第二个长方体坐标
/// @return 是（true）否（false）重叠
bool rectangleCross(const Box& b1, const Point& p1, const Box& b2, const Point& p2)
{
    return !(p2.x >= (p1.x + b1.Length()) || (p2.x + b2.Length()) <= p1.x ||
        p2.y >= (p1.y + b1.Width()) || (p2.y + b2.Width()) <= p1.y ||
        p2.z >= (p1.z + b1.Height()) || (p2.z + b2.Height()) <= p1.z
        );
}

/// @brief 哈哈哈哈哈哈哈
/// @param box 要放置的箱子
/// @param target 想要放置的坐标
/// @param Loaded 已经被装填的箱子
/// @return box能否放在target
bool canLoad(const Box& box, const Point& target, const std::vector<std::pair<Point, Box>>& Loaded, int carriageLength, int carriageWidth, int carriageHeight)
{
    //只要判断(target.x + box.Length(), target.y + box.Width(), target.z + box.Height()这个区域内有没有箱子就行了
    for (const auto& loaded : Loaded)
    {
        bool overLength = (target.x + box.Length()) > carriageLength;
        bool overWidth = (target.y + box.Width()) > carriageWidth;
        bool overHeight = (target.z + box.Height()) > carriageHeight;
        bool cross = rectangleCross(box, target, loaded.second, loaded.first);
        if (cross || overLength || overWidth || overHeight)
            return false;
    }
    return true;
}

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