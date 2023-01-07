import numpy as np
import pandas as pd

class Box():
    '''记录箱子信息的类
    name：种类名称
    length：长
    width：宽
    height：高
    num：数量
    '''
    def __init__(self, name, length, width, height, num):
        super(Box, self).__init__()
        self.name = name
        self.l = length
        self.w = width
        self.h =height
        self.num = num
        self.left = num  #剩余数量
        self.volume = length * width * height #体积
    
    #打印箱子信息
    def print_box(self):
        print("L:",self.l,"W:",self.w,"H:",self.h)
    
    #获取箱子信息，长宽高和剩余数目
    def get_message(self):
        message = {"L":self.l,"W":self.w,"H":self.h, "left_num":self.left}
        return message

#判断是否在卡车内
#输入:
# put_state 已经放入后的最大长宽高
# truck_size 卡车长宽高
def in_truck(put_state, truck_size):
    if put_state[0] > truck_size[0] or put_state[1] > truck_size[1] or put_state[2] > truck_size[2]:
        return False
    else:
        return True

#判断最上方的点是否与已经放入的箱子重叠
#输入
# point 待判断点坐标
# 一个箱子的四个坐标：origin原点坐标，top上方点坐标，front前方点坐标，right右方点坐标
def in_box_h(point, origin, top, front, right):
    if point[2]>origin[2] and point[2]<=top[2]:
        if point[0]>=origin[0] and point[0]<right[0]:
            if point[1]>=origin[1] and point[1]<front[1]:
                return True
    return False

#判断最右边的点是否与已经放入的箱子重叠
#输入
# point 待判断点坐标
# 一个箱子的四个坐标：origin原点坐标，top上方点坐标，front前方点坐标，right右方点坐标
def in_box_l(point, origin, top, front, right):
    if point[2]>=origin[2] and point[2]<top[2]:
        if point[0]>origin[0] and point[0]<=right[0]:
            if point[1]>=origin[1] and point[1]<front[1]:
                return True
    return False

#判断最前方的点是否与已经放入的箱子重叠
#输入
# point 待判断点坐标
# 一个箱子的四个坐标：origin原点坐标，top上方点坐标，front前方点坐标，right右方点坐标
def in_box_w(point, origin, top, front, right):
    if point[2]>=origin[2] and point[2]<top[2]:
        if point[0]>=origin[0] and point[0]<right[0]:
            if point[1]>origin[1] and point[1]<=front[1]:
                return True
    return False

#判断是否重叠
#输入
# put_loc 待放入的位置
# box 箱子类
# total_loc 所有已放入箱子的坐标
# state 箱子状态
# 0 l w h
# 1 w l h
# 2 l h w
# 3 h l w
# 4 w h l
# 5 h w l
def overlap(put_loc, box, total_loc, state):
    # 根据state调整l、w、h
    if state == 0:
        l, w, h = box.l, box.w, box.h
    elif state == 1:
        l, w, h = box.w, box.l, box.h
    elif state == 2:
        l, w, h = box.l, box.h, box.w
    elif state == 3:
        l, w, h = box.h, box.l, box.w
    elif state == 4:
        l, w, h = box.w, box.h, box.l
    elif state == 5:
        l, w, h = box.h, box.w, box.l
    
    #获取放入后的三个点坐标
    front = put_loc + np.array((0,w,0))
    top = put_loc + np.array((0,0,h))
    right = put_loc + np.array((l,0,0))

    #与所有loc判断是否重叠
    for loc in total_loc:
        loc_0 = loc["loc"]
        if loc["state"]==0:
            loc_l, loc_w, loc_h = loc["type"]["L"], loc["type"]["W"], loc["type"]["H"]
        elif loc["state"]==1:
            loc_l, loc_w, loc_h = loc["type"]["W"], loc["type"]["L"], loc["type"]["H"]
        elif loc["state"]==2:
            loc_l, loc_w, loc_h = loc["type"]["L"], loc["type"]["H"], loc["type"]["W"]
        elif loc["state"]==3:
            loc_l, loc_w, loc_h = loc["type"]["H"], loc["type"]["L"], loc["type"]["W"]
        elif loc["state"]==4:
            loc_l, loc_w, loc_h = loc["type"]["W"], loc["type"]["H"], loc["type"]["L"]
        elif loc["state"]==5:
            loc_l, loc_w, loc_h = loc["type"]["H"], loc["type"]["W"], loc["type"]["L"]

        loc_front = loc_0 + np.array((0,loc_w,0))
        loc_right = loc_0 + np.array((loc_l,0,0))
        loc_top = loc_0 + np.array((0,0,loc_h))
        
        if in_box_h(top, loc_0, loc_top, loc_front, loc_right) or in_box_w(front, loc_0, loc_top, loc_front, loc_right) \
            or in_box_l(right, loc_0, loc_top, loc_front, loc_right):
            return True
    return False

#判断该位置是否合法
#输入
# put_loc 待放入的位置
# box 箱子类
# truck_size 卡车信息
# total_loc 所有已放入箱子的坐标
# 返回box状态，-1该位置不能摆放
# 0 l w h
# 1 w l h
# 2 l h w
# 3 h l w
# 4 w h l
# 5 h w l
def legal_box(put_loc, box, truck_size, total_loc):
    # total_loc为空，还没放箱子，直接放入
    if not total_loc:
        return 0
    # 箱子数量为0，则不能放入
    if not box.left:
        return -1
    put_state_0 = put_loc + np.array((box.l,box.w,box.h))
    put_state_1 = put_loc + np.array((box.w,box.l,box.h))
    put_state_2 = put_loc + np.array((box.l,box.h,box.w))
    put_state_3 = put_loc + np.array((box.h,box.l,box.w))
    put_state_4 = put_loc + np.array((box.w,box.h,box.l))
    put_state_5 = put_loc + np.array((box.h,box.w,box.l))
    #两个状态，必须在卡车内+不重叠，则放入
    if in_truck(put_state_0, truck_size) and not overlap(put_loc, box, total_loc, 0):
        return 0
    if in_truck(put_state_1, truck_size) and not overlap(put_loc, box, total_loc, 1):
        return 1
    if in_truck(put_state_2, truck_size) and not overlap(put_loc, box, total_loc, 2):
        return 2
    if in_truck(put_state_3, truck_size) and not overlap(put_loc, box, total_loc, 3):
        return 3
    if in_truck(put_state_4, truck_size) and not overlap(put_loc, box, total_loc, 4):
        return 4
    if in_truck(put_state_5, truck_size) and not overlap(put_loc, box, total_loc, 5):
        return 5
    return -1

#放入盒子。更新三个列表状态。
#输入
# put_loc 待放入的位置
# box 箱子类
# total_loc 所有已放入箱子的坐标
# state 箱子状态 0表示不旋转，1表示箱子旋转（长宽互换）
def put_box(box, put_loc, state, total_loc):
    box.left = box.left - 1
    loc = {"loc":put_loc, "type":box.get_message(), "state": state}
    total_loc.append(loc)
    print("Put %s into "%box.name, loc)
    top_loc = put_loc + np.array((0,0,box.h))
    right_loc = put_loc + np.array((box.l,0,0))
    front_loc = put_loc + np.array((0,box.w,0))
    return top_loc,right_loc,front_loc

def generate_box_id(box_list):
    box_num = np.random.randint(0,len(box_list))
    while box_list[box_num].left==0:
        box_num = np.random.randint(0,len(box_list))
    return box_num

truck_size = np.array([587,233,220],dtype=np.int32)
box_list = []

#读取csv
folder_name = 'E5'
example_id = '1'
file_name = f'./data/{folder_name}/{folder_name}-{example_id}.csv'
df = pd.read_csv(file_name)
for i in range(len(df)):
    box_name = df.iloc[i]["name"]
    box_l = df.iloc[i]["L"]
    box_w = df.iloc[i]["W"]
    box_h = df.iloc[i]["H"]
    box_n = df.iloc[i]["N"]
    box = Box(box_name,box_l,box_w,box_h,box_n)
    box_list.append(box)

#box类型数量
box_type = len(df)

int_loc = np.array((0,0,0))
h_wait_loc = []
l_wait_loc = []
w_wait_loc = []
total_loc = []

first_box = np.random.randint(0,box_type)

#放入第一个盒子
top_loc,right_loc,front_loc = put_box(box_list[first_box], int_loc, 0, total_loc)
h_wait_loc.append(top_loc)
l_wait_loc.append(right_loc)
w_wait_loc.append(front_loc)
box_id=-1
# 循环放入
while l_wait_loc:
    while w_wait_loc:
        while h_wait_loc:
            put_loc = h_wait_loc.pop(0)
            if box_id==-1:
                box_id = generate_box_id(box_list)
            state=legal_box(put_loc, box_list[box_id], truck_size, total_loc)
            if state!=-1:
                top_loc,right_loc,front_loc = put_box(box_list[box_id], put_loc, state, total_loc)
                box_id=-1
                h_wait_loc.append(top_loc)
                if not any(np.array_equal(np.array((right_loc[0],right_loc[1],0)),i) for i in l_wait_loc):
                    l_wait_loc.append(right_loc)
                if not any(np.array_equal(np.array((front_loc[0],front_loc[1],0)),i) for i in w_wait_loc):
                    w_wait_loc.append(front_loc)
                # print("H:",h_wait_loc)
                # print("L:",l_wait_loc)
                # print("W:",w_wait_loc)
        
        put_loc = w_wait_loc.pop(0)
        if box_id==-1:
            box_id = generate_box_id(box_list)
        state=legal_box(put_loc, box_list[box_id], truck_size, total_loc)
        if state!=-1:
            top_loc,right_loc,front_loc = put_box(box_list[box_id], put_loc, state, total_loc)
            box_id=-1
            h_wait_loc.append(top_loc)
            l_wait_loc.append(right_loc)
            w_wait_loc.append(front_loc)
            # print("H:",h_wait_loc)
            # print("L:",l_wait_loc)
            # print("W:",w_wait_loc)

    put_loc = l_wait_loc.pop(0)
    if box_id==-1:
        box_id = generate_box_id(box_list)
    state=legal_box(put_loc, box_list[box_id], truck_size, total_loc)
    if state!=-1:
        top_loc,right_loc,front_loc = put_box(box_list[box_id], put_loc, state, total_loc)
        box_id=-1
        h_wait_loc.append(top_loc)
        l_wait_loc.append(right_loc)
        w_wait_loc.append(front_loc)
        # print("H:",h_wait_loc)
        # print("L:",l_wait_loc)
        # print("W:",w_wait_loc)
        
volume = 0
for loc in total_loc:
    volume += loc["type"]["L"]*loc["type"]["H"]*loc["type"]["W"]
print("填充率：", volume/(truck_size[0]*truck_size[1]*truck_size[2])*100., "%")