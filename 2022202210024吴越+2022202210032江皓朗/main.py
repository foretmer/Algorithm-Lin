from function import *

def main():
    # 容器
    container = Space(0, 0, 0, 10, 10, 10)
    # 箱体列表及数量
    # 深度优先遍历算法效率较低，可以采用如下测试数据
    #box_list = [Box(1, 2, 3, 0), Box(4, 5, 5, 1), Box(1, 1, 1, 2), Box(2, 2, 2, 3), Box(4, 5, 2, 4)]
    #num_list = [3, 4, 3, 2, 1]
    # 贪心算法效率较高，可以采用如下测试数据
    box_list = [Box(1, 2, 3, 0), Box(4, 5, 5, 1), Box(1, 1, 1, 2), Box(2, 2, 2, 3), Box(4, 5, 2, 4)]
    num_list = [11, 5, 5, 8, 6]
    # 问题
    problem = Problem(container, box_list, num_list)
    search_params = dict()
    # 具体计算
    basic_heuristic(True, search_params, problem)


if __name__ == "__main__":
    main()
