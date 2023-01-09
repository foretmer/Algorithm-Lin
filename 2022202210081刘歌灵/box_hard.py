# 简单版的三维装箱问题
'''
题干(高级):
1. 参数考虑小数点后两位
2. 实现在线算法,也就是箱子是按照随机顺序到达,先到达先摆放
3. 需要考虑箱子的摆放顺序,即箱子是从内到外,从下向上的摆放顺序
4. 因箱子共有3个不同的面,所有每个箱子有3种不同的摆放状态
5. 算法需要实时得出结果,即算法时间小于等于2秒
'''
'''
算法说明:
和简单版的思路是一样的,不同的是,对于小数的处理,直接向上取整。然后不进行箱子体积的排序
'''
'''
算法效果:
平均能够达到73.45%
'''
from operator import itemgetter
import numpy as np
import random
import statistics
import math
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter 
from mpl_toolkits.mplot3d import Axes3D

#make_pic的内置函数,用来在图像里面不断添加立方体
def box(ax,x, y, z, dx, dy, dz, color='red'):
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 1, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)#下底
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)#上底
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)
    return ax
#显示图形的函数：Items = [[num[0],num[1],num[2],num[3],num[4],num[5],num[6]],]
#Items是N个列表的列表,里面的每个列表数据[放置点O三维坐标,长宽高,颜色]
def make_pic(Items):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.xaxis.set_major_locator(MultipleLocator(50)) 
    ax.yaxis.set_major_locator(MultipleLocator(50)) 
    ax.zaxis.set_major_locator(MultipleLocator(50)) 
    for num in Items:
        box(ax,num[0],num[1],num[2],num[3],num[4],num[5],num[6])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.title('Cube')
    plt.savefig('tmp.jpg')
    plt.show()
#根据图显需要的数据,把尺寸数据生成绘图数据的函数
def make(O,C,color):
    data = [O[0],O[1],O[2],C[0],C[1],C[2],color]
    return data

# 定义车厢类
class TRUCK():
    def __init__(self,L,W,H) -> None:
        self.L = L
        self.W = W
        self.H = H
        self.volumn = L*W*H
        self.space = np.zeros((self.L,self.W,self.H))
    
    def put(self,pos,size) -> bool:
        '''
        将一个选定的物品放进货车中
        '''
        for i in range(pos[0],pos[0]+size[0]):
            for j in range(pos[1],pos[1]+size[1]):
                for k in range(pos[2],pos[2]+size[2]):
                    # 判定当前物品是否剩余容积不够或者超出边界或者和其他物品重叠
                    if self.volumn<=size[0]*size[1]*size[2] or i>=self.L or j>=self.W or k >= self.H or self.space[i,j,k]:
                        # 发生以上情况认为物品放置失败
                        return False
        # 如果物品可以放置成功,就将它所占用的空间都标记
        for i in range(pos[0],pos[0]+size[0]):
            for j in range(pos[1],pos[1]+size[1]):
                for k in range(pos[2],pos[2]+size[2]):
                    self.space[i,j,k] = 1
        self.volumn -= size[0]*size[1]*size[2]
        return True

# 定义物品类
class BOX():
    def __init__(self,l,w,h) -> None:
        self.ol = l
        self.ow = w
        self.oh = h
        l = math.ceil(l)
        w = math.ceil(w)
        h = math.ceil(h)
        self.l = max(l,w,h)
        self.h = min(l,w,h)
        self.w = l+w+h-self.l-self.h
        self.pos = None
    def __getitem__(self):
        # 这里返回向上取整前的体积
        return self.ol*self.ow*self.oh


# 初始化物品列表
def init_boxlist(config)->list:
    box_list = []
    # # 随机指定箱子尺寸
    for n in range(500):
        l = round(random.uniform(40,100),2)
        w = round(random.uniform(20,80),2)
        h = round(random.uniform(20,80),2)
        box = BOX(l,w,h)
        box_list.append(box)
    # # 按照config指定箱子尺寸
    # for (l,w,h,n) in config:
    #     for i in range(n):
    #         box = BOX(l,w,h)
    #         box_list.append(box)
    # # 对物品列表按照体积由大到小排序
    # box_list.sort(key=lambda x:x.l*x.w*x.h,reverse=True)
    return box_list

def main():
    # 老师给的箱子数据,每个元组是(长,宽,高,个数),一行是装一次的箱子型号
    box_configs = [[(108,76,30,40), (110,43,25,33), (92,81,55,39)],
                [(91,54,45,32), (105,77,72,24), (79,78,48,30)],
                [(60,40,32,64), (98,75,55,40), (60,59,39,64)],
                [(78,37,27,63), (89,70,25,52), (90,84,41,55)],
                [(108,76,30,24), (110,43,25,7), (92,81,55,22), (81,33,28,13), (120,99,73,15)],
                [(49,25,21,22), (60,51,41,22), (103,76,64,28), (95,70,62,25), (111,49,26,17)],
                [(88,54,39,25), (94,54,36,27), (87,77,43,21), (100,80,72,20), (83,40,36,24)],
                [(90,70,63,16), (84,78,28,28), (94,85,39,20), (80,76,54,23), (69,50,45,31)],
                [(74,63,61,22), (71,60,25,12), (106,80,59,25), (109,76,42,24), (118,56,22,11)],
                [(108,76,30,24), (110,43,25,9), (92,81,55,8), (81,33,28,11), (120,99,73,11), (111,70,48,10), (98,72,46,12), (95,66,31,9)],
                [(97,81,27,10), (102,78,39,20), (113,46,36,18), (66,50,42,21), (101,30,26,16), (100,56,35,17), (91,50,40,22), (106,61,56,19)],
                [(88,54,39,16), (94,54,36,14), (87,77,43,20), (100,80,72,16), (83,40,36,6), (91,54,22,15), (109,58,54,17), (94,55,30,9)],
                [(49,25,21,16), (60,51,41,8), (103,76,64,16), (95,70,62,18), (111,49,26,18), (85,84,72,16), (48,36,31,17), (86,76,38,6)],
                [(113,92,33,23), (52,37,28,22), (57,33,29,26), (99,37,30,17), (92,64,33,23), (119,59,39,26), (54,52,49,18), (75,45,35,30)],
                [(49,25,21,13), (60,51,41,9), (103,76,64,11), (95,70,62,14), (111,49,26,13), (85,84,72,16), (48,36,31,12), (86,76,38,11), (71,48,47,16), (90,43,33,8)],
                [(97,81,27,8), (102,78,39,16), (113,46,36,12), (66,50,42,12), (101,30,26,18), (100,56,35,13), (91,50,40,14), (106,61,56,17), (103,63,58,12), (75,57,41,13)],
                [(86,84,45,18), (81,45,34,19), (70,54,37,13), (71,61,52,16), (78,73,40,10), (69,63,46,13), (72,67,56,10), (75,75,36,8), (94,88,50,12), (65,51,50,13)],
                [(113,92,33,15), (52,37,28,17), (57,33,29,17), (99,37,30,19), (92,64,33,13), (119,59,39,19), (54,52,49,13), (75,45,35,21), (79,68,44,13), (116,49,47,22)],
                [(118,79,51,16), (86,32,31,8), (64,58,52,14), (42,42,32,14), (64,55,43,16), (84,70,35,10), (76,57,36,14), (95,60,55,14), (80,66,52,14), (109,73,23,18)],
                [(98,73,44,6), (60,60,38,7), (105,73,60,10), (90,77,52,3), (66,58,24,5), (106,76,55,10), (55,44,36,12), (82,58,23,7), (74,61,58,6), (81,39,24,8), (71,65,39,11), (105,97,47,4), (114,97,69,5), (103,78,55,6), (93,66,55,6)],
                [(108,76,30,12), (110,43,25,12), (92,81,55,6), (81,33,28,9), (120,99,73,5), (111,70,48,12), (98,72,46,9), (95,66,31,10), (85,84,30,8), (71,32,25,3), (36,34,25,10), (97,67,62,7), (33,25,23,7), (95,27,26,10), (94,81,44,9)],
                [(49,25,21,13), (60,51,41,9), (103,76,64,8), (95,70,62,6), (111,49,26,10), (74,42,40,4), (85,84,72,10), (48,36,31,10), (86,76,38,12), (71,48,47,14), (90,43,33,9), (98,52,44,9), (73,37,23,10), (61,48,39,14), (75,75,63,11)],
                [(97,81,27,6), (102,78,39,6), (113,46,36,15), (66,50,42,8), (101,30,26,6), (100,56,35,7), (91,50,40,12), (106,61,56,10), (103,63,58,8), (75,57,41,11), (71,68,64,6), (85,67,39,14), (97,63,56,9), (61,48,30,11), (80,54,35,9)],
                [(113,92,33,8), (52,37,28,12), (57,33,29,5), (99,37,30,12), (92,64,33,9), (119,59,39,12), (54,52,49,8), (75,45,35,6), (79,68,44,12), (116,49,47,9), (83,44,23,11), (98,96,56,10), (78,72,57,8), (98,88,47,9), (41,33,31,13)]
                ]
    rate_all = []
    for c,config in enumerate(box_configs[:1]):
        truck_l = 587
        truck_w = 233
        truck_h = 220
        truck = TRUCK(truck_l,truck_w,truck_h)
        box_list = init_boxlist(config)
        #1.给定空间容器C      
        #内容积为:长4.2x宽1.9x高1.8米
        O = (0,0,0)           #原点坐标
        C = (truck_l,truck_w,truck_h)    #箱体长宽高
        color1 = 'black'         #箱体颜色
        color2 = 'hotpink'         #物品颜色
        fit_in_boxs = [make(O,C,color1)]
        # make_pic(fit_in_boxs) # 画出空车厢
        # 以下是算法的主体部分
        pos_list = [[0,0,0]]
        fit_in_num = 0
        fit_in_v = 0.
        for b,box in enumerate(box_list): # 遍历box列表中的每个box
            for i,pos in enumerate(pos_list): # 遍历pos列表中的每个pos,对第一个箱子来说,就放在原点
                if truck.put(pos,(box.l,box.w,box.h)): # 尝试一下按照当前的长宽高能不能放下
                    now_box = (box.l,box.w,box.h) # 记录放下箱子的型号
                    fit_in_num += 1 
                    fit_in_v += box.__getitem__() # 计算实际放入的箱子体积
                    pos_l = (pos[0]+box.l,pos[1],pos[2]) # 在长边处产生的新的可放点
                    pos_w = (pos[0],pos[1]+box.w,pos[2]) # 在宽边处产生的新的可放点
                    pos_h = (pos[0],pos[1],pos[2]+box.h) # 在高边处产生的新的可放点
                    pos_list.append(pos_l) # 把可放点加入列表中
                    pos_list.append(pos_w)
                    pos_list.append(pos_h)
                    now_pos = pos_list.pop(i)
                    # 相比于ver1在这里添加一个排序
                    pos_list = sorted(pos_list,key=itemgetter(0,1,2)) # 可放点列表按长、宽、高的优先级排序
                    fit_in_boxs.append(make(now_pos,now_box,color2)) # 在绘图里添加放进了的箱子
                    print("物品:{},位置:{}".format(now_box,now_pos))
                    # make_pic(fit_in_boxs) # 画出目前的车厢,不用看图的话可以注释
                    break
                # 换一个方向试试
                elif truck.put(pos,(box.w,box.l,box.h)): # 这里把w和l调转了
                    now_box = (box.w,box.l,box.h)
                    fit_in_num += 1
                    fit_in_v += box.__getitem__()
                    pos_l = (pos[0]+box.w,pos[1],pos[2]) # 注意在这里也是要把w和l调转的
                    pos_w = (pos[0],pos[1]+box.l,pos[2])
                    pos_h = (pos[0],pos[1],pos[2]+box.h)
                    pos_list.append(pos_l)
                    pos_list.append(pos_w)
                    pos_list.append(pos_h)
                    now_pos = pos_list.pop(i)
                    # 相比于ver1在这里添加一个排序
                    pos_list = sorted(pos_list,key=itemgetter(0,1,2))
                    fit_in_boxs.append(make(now_pos,now_box,color2))
                    print("物品:{},位置:{}".format(now_box,now_pos))
                    # make_pic(fit_in_boxs)
                    break
                # 还可以把物品立起来
                elif truck.put(pos,(box.h,box.l,box.w)):
                    now_box = (box.h,box.l,box.w)
                    fit_in_num += 1
                    pos_l = (pos[0]+box.h,pos[1],pos[2])
                    pos_w = (pos[0],pos[1]+box.l,pos[2])
                    pos_h = (pos[0],pos[1],pos[2]+box.w)
                    pos_list.append(pos_l)
                    pos_list.append(pos_w)
                    pos_list.append(pos_h)
                    now_pos = pos_list.pop(i)
                    # 相比于ver1在这里添加一个排序
                    pos_list = sorted(pos_list,key=itemgetter(0,1,2))
                    fit_in_boxs.append(make(now_pos,now_box,color2))
                    print("物品:{},位置:{}".format(now_box,now_pos))
                    # make_pic(fit_in_boxs)
                    break
                
        rate_all.append(fit_in_v/(truck_l*truck_w*truck_h))
        make_pic(fit_in_boxs) #画出最终车厢放置的示意图
        print("第{}个config,放入物品数:{}".format(c,fit_in_num))  
        print("车厢填充率{}".format(fit_in_v/(truck_l*truck_w*truck_h)))
        del truck,box_list,pos_list
    print("填充率均值:{}".format(statistics.mean(rate_all)))

main()