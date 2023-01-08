#include "Datastructure.h"
#include "stdafx.h"
#include "Solution.h"
#include "Dataset.h"

int main(int argc, char** argv)
{
    for (auto& x : datasets)
    {
        std::cout << x.first << ":" << std::endl;
        auto boxes = transform(x.second);
        //第一个参数传的是引用，在函数内会被sort或者shuffle，所以boxes会被更改
        firstFit(boxes, 587, 233, 220, false);
    }
    return 0;
}