#pragma once
#include "stdafx.h"

class Box
{
private:
    int L;
    int W;
    int H;
    int rotateState;
public:
    Box(int l, int w, int h) : L(l), W(w), H(h), rotateState(0)
    {

    }
    int Volume() const
    {
        return H * W * L;
    }
    int Length() const
    {
        return this->L;
    }
    int Width() const
    {
        return this->W;
    }
    int Height() const
    {
        return this->H;
    }
    /// @brief 周期地对箱子进行旋转
    void Rotate()
    {
        //LWH->WLH->WHL->HWL->HLW->LHW->LWH，可见，奇数次旋转交换前两个元素，偶数次旋转交换后两个元素
        //第六次旋转就会恢复原样
        if (rotateState == 0)
        {
            std::swap(L, W);
            rotateState = 1;
        }
        else
        {
            std::swap(W, H);
            rotateState = 0;
        }
    }
};

struct Point
{
    int x;
    int y;
    int z;
    Point(int _x, int _y, int _z) : x(_x), y(_y), z(_z)
    {

    }
};

std::ostream& operator<<(std::ostream&, const Box&);
std::ostream& operator<<(std::ostream&, const Point&);