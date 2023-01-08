#include "Datastructure.h"
#include "stdafx.h"

/// @brief 优雅地输出箱子的形状
/// @param o 输出流
/// @param box 要打印的Box对象
/// @return 还是o，为什么要把o给返回因为可以连用：像是这样cout << box1 << box2 << endl;
std::ostream& operator<<(std::ostream& o, const Box& box)
{
    o << "(" << box.Length() << ", " << box.Width() << ", " << box.Height() << ")";
    return o;
}

/// @brief 优雅地输出坐标
/// @param o 输出流
/// @param point 要打印的point对象
/// @return 还是o，为什么要把o给返回因为可以连用：像是这样cout << box1 << box2 << endl;
std::ostream& operator<<(std::ostream& o, const Point& point)
{
    o << "(" << point.x << ", " << point.y << ", " << point.z << ")";
    return o;
}