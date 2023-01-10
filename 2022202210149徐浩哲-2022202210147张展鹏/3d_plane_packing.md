# 3d_plane_packing

利用基于平面的启发式算法，对三维离线装箱问题进行解决

## 使用方法：

在主函数中存在*file_data_input()* 和 *single_data_input()*两个函数。

当使用*file_data_input()*函数时，算法根据同一目录下*input_data.txt*文件中的输入内容进行计算，同时将输入打印在同一目录下*output_data.txt*文件中。

而当使用*single_data_input()*函数时，在该函数的*box_list*和*num_list*中可以自己设置想要输入的参数，结果将会在在控制台中以及画图的形式展现。

## 算法设计思路

本算法是基于平面的启发式DFS算法，详见文件*高级算法大作业-第35小组.docx*。

## 算法流程：

对于两种数据的输入，其内部算法流程是一致的，即首先会根据输入的箱体数据利用 *gen_simple_block()* 函数生成简单块，之后将真个容器作为初始的平面列表*plane_list*开始填充，当平面列表不为空时，从中利用选择平面函数*select_plane()*进行填充，而可行块列表则由*gen_block_list()*函数确定。确定完平面和可行块后利用*fill_block()*函数进平面填充。而如果没有可行块则会利用*merge_plane()*函数进行平面合并，以此获得更大的平面。当*plane_list*为空时，返回。

