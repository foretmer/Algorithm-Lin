from enum import Enum
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
class CargoPose(Enum):
    long_wide_height = 0 #x,y,z轴分别对应“物体初始”长宽高
    long_height_wide = 1
    wide_long_height = 2
    wide_height_long = 3
    height_long_wide = 4
    height_wide_long = 5

class Point:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def __eq__(self, __o: object):
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    @property
    def is_valid(self):
        return self.x >= 0 and self.y >= 0 and self.z >= 0

    @property
    def tuple(self):
        return (self.x, self.y, self.z)

class Cargo:
    def __init__(self,long,width,height):
        #原始长宽高
        self.long=long
        self.width=width
        self.height=height
        self.pose=0
        #改变摆放姿态后形成的新立方体长宽高
        self.load_long=long
        self.load_width=width
        self.load_height=height

    def change_pose(self,num):
        if(num==0):
            self.load_long =self.long
            self.load_width = self.width
            self.load_height = self.height
            self.pose = 0
        elif(num==1):
            self.load_long =self.long
            self.load_width = self.height
            self.load_height = self.width
            self.pose = 1
        elif(num==2):
            self.load_long =self.width
            self.load_width = self.long
            self.load_height = self.height
            self.pose = 2
        elif(num==3):
            self.load_long =self.width
            self.load_width = self.height
            self.load_height = self.long
            self.pose = 3
        elif(num == 4):
            self.load_long =self.height
            self.load_width = self.long
            self.load_height = self.width
            self.pose = 4
        elif(num==5):
            self.load_long =self.height
            self.load_width = self.width
            self.load_height = self.long
            self.pose = 5

    @property
    def volume(self):
        return self.long*self.width*self.height

    def __repr__(self) -> str:
        return f"起始点坐标为({self.x},{self.y},{self.z})"

    def set_locate_point(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return "该货物被放在("+str(self.x)+","+str(self.y)+","+str(self.z)+"),摆放长宽高为("+str(self.load_long)+","+str(self.load_width)+","+str(self.load_height)+")"

    @property
    def get_x(self):
        return self.x

    @property
    def get_y(self):
        return self.y

    @property
    def get_z(self):
        return self.z

    @property
    def tuple(self):
        return (self.load_long, self.load_width, self.load_height)

    @property
    def get_locate_bottom_area(self):#求底面积(等同于求俯视图的面积)
        return self.load_long*self.load_width

    @property
    def get_locate_front_area(self):#求主视图的面积
        return self.load_height*self.load_width

    @property
    def get_locate_left_area(self):#求左视图的面积
        return self.load_height*self.load_long

class Container:
    def __init__(self,long,width,height):
        self.long=long
        self.width=width
        self.height=height
        self.available=[Point(0,0,0)]
        self.settled_cargo=[]
        self.current_bottom_area=0#当前已占用的底面积
        self.current_max_height=0# 当前最高的高度
        self.alpha=0.2#调节因子

    def calculate_bottom_area(self):
        length=len(self.settled_cargo)
        area_tmp=0
        for i in range(length):
            if(self.settled_cargo[i].get_z==0):
                area_tmp=area_tmp+self.settled_cargo[i].get_locate_bottom_area
        return area_tmp

    def calculate_usage(self):
        volume=0
        length=len(self.settled_cargo)
        for i in range(length):
            volume=volume+self.settled_cargo[i].volume
        return volume/(self.long*self.width*self.height)




    def determine_top_view_overlaps(self,cargoA,cargoB):#从俯视图判断两个物体是否相撞（判断俯视图是否有重叠）
        tmpA_1=[cargoA.get_x,cargoA.get_y]
        tmpA_4=[cargoA.get_x+cargoA.load_long,cargoA.get_y+cargoA.load_width]
        tmpB_1=[cargoB.get_x,cargoB.get_y]
        tmpB_4=[cargoB.get_x+cargoB.load_long,cargoB.get_y+cargoB.load_width]
        if tmpA_1[0]>=tmpB_4[0] or tmpA_1[1]>=tmpB_4[1] or tmpB_1[0]>=tmpA_4[0] or tmpB_1[1]>=tmpA_4[1]:
            return 0
        else:
            return 1

    def  determine_main_view_overlaps(self,cargoA,cargoB):#从主视图判断两个物体是否相撞（判断主视图是否有重叠）
        tmpA_1=[cargoA.get_y,cargoA.get_z]
        tmpA_4=[cargoA.get_y+cargoA.load_width,cargoA.get_z+cargoA.load_height]
        tmpB_1=[cargoB.get_y,cargoB.get_z]
        tmpB_4=[cargoB.get_y+cargoB.load_width,cargoB.get_z+cargoB.load_height]
        if tmpA_1[0]>=tmpB_4[0] or tmpA_1[1]>=tmpB_4[1] or tmpB_1[0]>=tmpA_4[0] or tmpB_1[1]>=tmpA_4[1]:
            return 0
        else:
            return 1


    def determine_left_view_overlaps(self,cargoA,cargoB):
        tmpA_1 = [cargoA.get_x, cargoA.get_z]
        tmpA_4 = [cargoA.get_x + cargoA.load_long, cargoA.get_z + cargoA.load_height]
        tmpB_1 = [cargoB.get_x, cargoB.get_z]
        tmpB_4 = [cargoB.get_x + cargoB.load_long, cargoB.get_z + cargoB.load_height]
        if tmpA_1[0]>=tmpB_4[0] or tmpA_1[1]>=tmpB_4[1] or tmpB_1[0]>=tmpA_4[0] or tmpB_1[1]>=tmpA_4[1]:
            return 0
        else:
            return 1


    def check_crash_and_suspended(self,cargo:Cargo):
        length=len(self.settled_cargo)
        if(length==0):
            return False,0
        result4=True
        for i in range(length):
            result1=self.determine_top_view_overlaps(cargo,self.settled_cargo[i])
            result2=self.determine_main_view_overlaps(cargo,self.settled_cargo[i])
            result3=self.determine_left_view_overlaps(cargo,self.settled_cargo[i])
            tmp=self.judge_box_suspended(self.settled_cargo[i],cargo)
            #print(tmp)
            if(tmp==False):
                result4=False
                result5=self.settled_cargo[i].get_locate_bottom_area
            if(result1+result2+result3>1):
                return True,0
        if(result4==False):
            return False,result5
        else:
            return True,0

    def determine_overflow(self,cargo):
        x1,y1,z1=cargo.get_x,cargo.get_y,cargo.get_z
        x4,y4,z4=x1+cargo.load_long,y1+cargo.load_width,z1
        x8,y8,z8=x1+cargo.load_long,y1+cargo.load_width,z1+cargo.load_height
        if(z8>self.height or x4>self.long or y4>self.width):
            #print("溢出")
            return True
        else:
            return False



    def solve_old_point_add_new_point(self,cargo,tmp_point):
        #print("before_remove",self.available)
        self.available.remove(tmp_point)
        #print("after_remove",self.available)
        x,y,z=tmp_point.tuple
        load_long=cargo.load_long
        load_width=cargo.load_width
        load_height=cargo.load_height
        self.available.append(Point(x+load_long,y,z))
        self.available.append(Point(x,y+load_width,z))
        self.available.append(Point(x,y,z+load_height))


    def judge_box_suspended(self,cargoA,cargoB):#判断物体是否悬空放置，禁止物品出现任何悬空
        #物体A被摆放在物体B的下面时
        if(cargoB.get_z==0):
            return False
        tmpA_1 = [cargoA.get_x, cargoA.get_y]
        tmpA_2 = [cargoA.get_x + cargoA.load_long, cargoA.get_y]
        tmpA_3 = [cargoA.get_x, cargoA.get_y + cargoA.load_width]
        tmpA_4 = [cargoA.get_x + cargoA.load_long, cargoA.get_y + cargoA.load_width]
        tmpB_1 = [cargoB.get_x, cargoB.get_y]
        tmpB_2 = [cargoB.get_x + cargoB.load_long, cargoB.get_y]
        tmpB_3 = [cargoB.get_x, cargoB.get_y + cargoB.load_width]
        tmpB_4 = [cargoB.get_x + cargoB.load_long, cargoB.get_y + cargoB.load_width]
        if(cargoA.get_z+cargoA.load_height==cargoB.get_z):
                if(tmpB_1[0]>=tmpA_1[0] and tmpB_4[0]<=tmpA_4[0] and tmpB_1[1]>=tmpA_1[1] and tmpB_4[1]<=tmpA_4[1]):
                    return False
                else:
                    return True
        else:
            return True


    #当只有一个可用点时，直接选择该点，当有多个可用点时，选择
    def add_cargo_to_container(self,cargo:Cargo):
        length=len(self.available)
        storage_result=[0,0,0,0]
        max_score=-1
        for i in range(length):
            x,y,z=self.available[i].tuple
            cargo.set_locate_point(x,y,z)
            for j in range(6):
                cargo.change_pose(j)
                result1,bottom=self.check_crash_and_suspended(cargo)
                result2=self.determine_overflow(cargo)
                if(result1==False and result2==False):
                    if(cargo.get_z==0):#找到使得tmp_score最小的摆放方式
                        tmp_score=cargo.load_height
                        #tmp_score=self.alpha*(self.current_bottom_area+cargo.get_locate_bottom_area)+(1-self.alpha)*max(cargo.get_z+cargo.load_height,self.current_max_height)
                        if(tmp_score<max_score or max_score==-1):
                            storage_result[0]=x
                            storage_result[1]=y
                            storage_result[2]=z
                            storage_result[3]=j
                            max_score=tmp_score
                    else:
                        tmp_score=self.alpha*(self.current_bottom_area)*(1-self.alpha)*max(cargo.get_z+cargo.load_height,self.current_max_height)*(bottom-cargo.get_locate_bottom_area)
                        #print(bottom-cargo.get_locate_bottom_area)
                        if(tmp_score<max_score or max_score==-1):
                            storage_result[0]=x
                            storage_result[1]=y
                            storage_result[2]=z
                            storage_result[3]=j
                            max_score=tmp_score

        if(max_score==-1):
            return False
        else:
            cargo.set_locate_point(storage_result[0],storage_result[1],storage_result[2])
            cargo.change_pose(storage_result[3])
            if(storage_result[2]==0):
                self.current_bottom_area=self.current_bottom_area+cargo.get_locate_bottom_area
            self.current_max_height=max(cargo.get_z+cargo.load_height,self.current_max_height)
            self.settled_cargo.append(cargo)
            point=Point(storage_result[0],storage_result[1],storage_result[2])
            self.solve_old_point_add_new_point(cargo,point)
            print("大小为",cargo.tuple,"成功装入,放在",point)
            return True


plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
fig:Figure = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.view_init(elev=5, azim=60)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

def draw_reslut(setted_container:Container):
    plt.gca().set_box_aspect((
        setted_container.long,
        setted_container.width,
        setted_container.height
    ))
    _draw_container(setted_container)
    for cargo in setted_container.settled_cargo:
        _draw_cargo(cargo)
    plt.show()

def _draw_container(container:Container):
    _plot_linear_cube(
        0,0,0,
        container.long,
        container.width,
        container.height
    )

def _draw_cargo(cargo:Cargo):
    _plot_opaque_cube(
        cargo.x, cargo.y, cargo.z,
        cargo.load_long, cargo.load_width, cargo.load_height
    )

def _plot_opaque_cube(x=10, y=20, z=30, dx=40, dy=50, dz=60):
    xx = np.linspace(x, x+dx, 2)
    yy = np.linspace(y, y+dy, 2)
    zz = np.linspace(z, z+dz, 2)
    xx2, yy2 = np.meshgrid(xx, yy)
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z))
    ax.plot_surface(xx2, yy2, np.full_like(xx2, z+dz))
    yy2, zz2 = np.meshgrid(yy, zz)
    ax.plot_surface(np.full_like(yy2, x), yy2, zz2)
    ax.plot_surface(np.full_like(yy2, x+dx), yy2, zz2)
    xx2, zz2= np.meshgrid(xx, zz)
    ax.plot_surface(xx2, np.full_like(yy2, y), zz2)
    ax.plot_surface(xx2, np.full_like(yy2, y+dy), zz2)

def _plot_linear_cube(x, y, z, dx, dy, dz, color='red'):
    # ax = Axes3D(fig)
    xx = [x, x, x+dx, x+dx, x]
    yy = [y, y+dy, y+dy, y, y]
    kwargs = {'alpha': 0, 'color': color}
    ax.plot3D(xx, yy, [z]*5, **kwargs)
    ax.plot3D(xx, yy, [z+dz]*5, **kwargs)
    ax.plot3D([x, x], [y, y], [z, z+dz], **kwargs)
    ax.plot3D([x, x], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y+dy, y+dy], [z, z+dz], **kwargs)
    ax.plot3D([x+dx, x+dx], [y, y], [z, z+dz], **kwargs)



'''用例4if(i<20):
            result = containerA.add_cargo_to_container(Cargo(97, 81, 27))
        elif(i>=20 and i<40):
            result = containerA.add_cargo_to_container(Cargo(102, 78, 39))
        elif(i >= 40 and i < 60):
            result = containerA.add_cargo_to_container(Cargo(113, 46, 36))
        elif (i >= 60 and i < 80):
            result = containerA.add_cargo_to_container(Cargo(101, 30, 26))
        elif (i >= 80 and i < 100):
            result = containerA.add_cargo_to_container(Cargo(66, 50, 42))
        elif (i >= 100 and i < 120):
            result = containerA.add_cargo_to_container(Cargo(100, 56, 35))
        elif (i >= 120 and i < 140):
            result = containerA.add_cargo_to_container(Cargo(91, 50, 40))
        elif (i >= 150 and i < 150):
            result = containerA.add_cargo_to_container(Cargo(106, 61, 56))'''





