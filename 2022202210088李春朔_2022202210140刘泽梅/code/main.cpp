//
//  main.cpp
//  algorithm
//
//  Created by Raymond on 2022/11/30.
//

#include <iostream>
#include <vector>
#include <list>
#define MAX_NUM 100
#define MAX_SPACE 1000
using namespace std;

typedef struct Space{
    int start[MAX_NUM];
    int h[MAX_NUM];
    int count;
}Space;

Space loaded[MAX_SPACE][MAX_SPACE] = {0};

class Box{
public:
    int length;  //cm
    int width;
    int height;
    Box(int l, int w, int h): length(l), width(w), height(h) {};
    Box():length(1), width(1),height(1) {};
};

class Point{
public:
    int l;
    int w;
    int h;
    Point(int l, int w, int h): l(l), w(w), h(h) {};
};

class BPoint{
public:
    Point o;
    int l;
    int w;
    int h;
    BPoint(Point o, int l, int w, int h): o(o), l(l), w(w), h(h) {};
};

bool verify(BPoint v1, BPoint v2) {
    // v1是待放入箱子，v2是已放入箱子
    if(((v1.o.l >= v2.o.l && v1.o.l < v2.o.l + v2.l) || (v2.o.l >= v1.o.l && v2.o.l < v1.o.l + v1.l)) &&
       ((v1.o.w >= v2.o.w && v1.o.w < v2.o.w + v2.w) || (v2.o.w >= v1.o.w && v2.o.w < v1.o.w + v1.w)) &&
       ((v1.o.h >= v2.o.h && v1.o.h < v2.o.h + v2.h) || (v2.o.h >= v1.o.h && v2.o.h < v1.o.h + v1.h))) {
        return 0;
    }
    return 1;
}

//按体积降序排序
bool comp(const Box a, const Box b) {
    return a.length * a.width *a.height > b.length * b.width * b.height;
}


void normalize(vector<Box> &stuff) {
    int temp;
    for(int i =  0; i < stuff.size(); i++) {
        if(stuff[i].length < stuff[i].height && stuff[i].length < stuff[i].width) {
            temp  = stuff[i].height;
            stuff[i].height = stuff[i].length;
            stuff[i].length = temp;
        }
        else if(stuff[i].width < stuff[i].height && stuff[i].width < stuff[i].length) {
            temp  = stuff[i].height;
            stuff[i].height = stuff[i].width;
            stuff[i].width = temp;
        }
    }
}

//打乱箱子到达的顺序
void randomlize(vector<Box> &stuff) {
    srand((unsigned)time(NULL));
    Box temp;
    for(int i = 0; i < stuff.size() - 1; i++) {
        int index = rand() % (stuff.size()-i-1) + i + 1;
        temp = stuff[i];
        stuff[i] = stuff[index];
        stuff[index] = temp;
    }
}

int queryOnePosition(const Box vehicle, const Box a, int pl, int pw, int ph) {
    if(ph + a.height >= vehicle.height || pl + a.length >= vehicle.length ||
       pw +a.width >= vehicle.width)
        return 0;
    int Flag = 0;
    for(int j = pl; j < pl + a.length; j++){
        for(int k = pw; k < pw + a.width; k++) {
            int flag = 0;
            if(loaded[j][k].count == 0) {
                if(ph == 0)
                    Flag = 1;
                continue;
            }
            for(int i = 0; i < loaded[j][k].count; i++) {
                if(loaded[j][k].start[i] >= ph + a.height) {
                    continue;
                }
                if(loaded[j][k].start[i] + loaded[j][k].h[i] == ph)
                    flag = 1;
                if((loaded[j][k].start[i] >= ph) ||
                   (loaded[j][k].start[i] + loaded[j][k].h[i] > ph &&
                   loaded[j][k].start[i] + loaded[j][k].h[i] <= ph + a.height)) {
                    return 0;
                }
            }
            if(flag == 1){
                Flag = 1;
            }
        }
    }
    return Flag;
}
//关键点垂直空间排除法
Point find3(const Box vehicle, Box a, list<Point> &lis_l, list<Point> &lis_w, list<Point> &lis_h) {
    list<Point>::iterator iter;
    for(iter = lis_w.begin(); iter != lis_w.end( ); iter++) {
        if(queryOnePosition(vehicle, a, iter->l, iter->w, iter->h) == 1){
            Point P = Point(iter->l, iter->w, iter->h);
            lis_w.erase(iter);
            return P;
        }
    }
    for(iter = lis_h.begin(); iter != lis_h.end( ); iter++) {
        if(queryOnePosition(vehicle, a, iter->l, iter->w, iter->h) == 1){
            Point P = Point(iter->l, iter->w, iter->h);
            lis_h.erase(iter);
            return P;
        }
    }
    for(iter = lis_l.begin(); iter != lis_l.end( ); iter++) {
        if(queryOnePosition(vehicle, a, iter->l, iter->w, iter->h) == 1){
            Point P = Point(iter->l, iter->w, iter->h);
            lis_l.erase(iter);
            return P;
        }
    }
    return Point(-1, -1, -1);
}

//不用关键点垂直空间排除法
Point find(const Box vehicle, Box a) {
    int cur_h = 0;
    for(int i = 0; i < vehicle.length; i++) {
        for(int j = 0; j < vehicle.width; j++) {
            cur_h = 0;
            if(queryOnePosition(vehicle, a, i, j, cur_h) == 1)
                return Point(i, j ,cur_h);
            for(int k = 0; k < loaded[i][j].count; k++){
                cur_h = loaded[i][j].start[k] + loaded[i][j].h[k];
                if(queryOnePosition(vehicle, a, i, j, cur_h) == 1)
                    return Point(i, j ,cur_h);
            }
        }
    }
    return Point(-1, -1, -1);
}

Point find1(const Box vehicle, Box& a) {
    int cur_h = 0;
    int best_i=-1,best_j=-1,best_h=-1;
    int min_area=((unsigned)(-1)>>1);
    int area=0;
    for(int i = 0; i < vehicle.length; i++) {
        for(int j = 0; j < vehicle.width; j++) {
            cur_h = 0;
            if(loaded[i][j].count == 0 && queryOnePosition(vehicle, a, i, j, cur_h) == 1){
                area=i+j;
                if(area < min_area){
                    best_i = i;
                    best_j = j;
                    best_h = cur_h;
                    min_area = area;
                }
            }
            //return Point(i, j ,cur_h);
            for(int k = 0; k < loaded[i][j].count; k++){
                cur_h = loaded[i][j].start[k] + loaded[i][j].h[k];
                if(queryOnePosition(vehicle, a, i, j, cur_h) == 1) {
                    //area=loaded[i][j].l[k]*loaded[i][j].w[k]-a.length*a.width;
                    area = i+j;
                    if(area<min_area){
                        best_i=i;
                        best_j=j;
                        best_h=cur_h;
                        min_area=area;
                    }
                }
            }
        }
    }
    return Point(best_i, best_j ,best_h);
}


vector<int> defineH(int l, int w, vector<BPoint> BPox) {
    vector<int> h;
    h.push_back(0);
    for(int i = 0; i < BPox.size(); i++) {
        if(l >= BPox[i].o.l && l < BPox[i].o.l + BPox[i].l && w >= BPox[i].o.w && w < BPox[i].o.w + BPox[i].w) {
            h.push_back(BPox[i].o.h + BPox[i].h);
        }
    }
    sort(h.begin(), h.end());
    return h;
}

//关键点查已装入箱子判断重复法
Point find4(const Box vehicle, vector<BPoint> BPox, Box a, list<Point> &lis_l, list<Point> &lis_w, list<Point> &lis_h) {
    list<Point>::iterator iter;
    for(iter = lis_w.begin(); iter != lis_w.end( ); iter++) {
        if(iter->l + a.length >= vehicle.length || iter->w + a.width >= vehicle.width ||
           iter->h + a.height >= vehicle.height){
            continue;
        }
        int flag = 0;
        for(int t = 0; t < BPox.size(); t++) {
            //如果查到有重合则推出循环
            BPoint bp = BPoint(Point(iter->l, iter->w, iter->h), a.length, a.width, a.height);
            if(verify(bp, BPox[t]) == 0) {
                flag = 1;
                break;
            }
        }
        if(flag == 1)
            continue;
        Point P = Point(iter->l, iter->w, iter->h);
        lis_w.erase(iter);
        return P;
    }
    for(iter = lis_h.begin(); iter != lis_h.end( ); iter++) {
        if(iter->l + a.length >= vehicle.length || iter->w + a.width >= vehicle.width ||
           iter->h + a.height >= vehicle.height){
            continue;
        }
        int flag = 0;
        for(int t = 0; t < BPox.size(); t++) {
            //如果查到有重合则推出循环
            BPoint bp = BPoint(Point(iter->l, iter->w, iter->h), a.length, a.width, a.height);
            if(verify(bp, BPox[t]) == 0) {
                flag = 1;
                break;
            }
        }
        if(flag == 1)
            continue;
        Point P = Point(iter->l, iter->w, iter->h);
        lis_h.erase(iter);
        return P;
    }
    for(iter = lis_l.begin(); iter != lis_l.end( ); iter++) {
        if(iter->l + a.length >= vehicle.length || iter->w + a.width >= vehicle.width ||
           iter->h + a.height >= vehicle.height){
            continue;
        }
        int flag = 0;
        for(int t = 0; t < BPox.size(); t++) {
            //如果查到有重合则推出循环
            BPoint bp = BPoint(Point(iter->l, iter->w, iter->h), a.length, a.width, a.height);
            if(verify(bp, BPox[t]) == 0) {
                flag = 1;
                break;
            }
        }
        if(flag == 1)
            continue;
        Point P = Point(iter->l, iter->w, iter->h);
        lis_l.erase(iter);
        return P;
    }
    return Point(-1, -1, -1);
}

// 不用关键点查已装入箱子判断重复法
Point find2(const Box vehicle, vector<BPoint> BPox, Box a) {
    for(int i = 0; i < vehicle.length; i++) {
        if(i + a.length >= vehicle.length)
            break;
        for(int j = 0; j < vehicle.width; j++) {
            if(j + a.width >= vehicle.width)
                break;
            vector<int> h = defineH(i, j, BPox);
            for(int k = 0; k < h.size(); k++) {
                //cout << i << "--" << j << "--" << h[k] << endl;
                if(h[k] + a.height >= vehicle.height)
                    continue;
                BPoint bp = BPoint(Point(i,j,h[k]), a.length, a.width, a.height);
                int flag = 0;
                for(int t = 0; t < BPox.size(); t++) {
                    //如果查到有重合则推出循环
                    if(verify(bp, BPox[t]) == 0) {
                        flag = 1;
                        break;
                    }
                }
                if(flag == 1)
                    continue;
                return Point(i, j, h[k]);
            }
        }
    }
    return Point(-1, -1, -1);
}

int upload1(const Box vehicle, vector<Box> &stuff) {
    double sum = 0;
    vector<BPoint> BPox;
    list<Point> key_l, key_w, key_h;
    for(int i = 0; i < stuff.size(); i++) {
        if(BPox.size() == 0) {
            BPox.push_back(BPoint(Point(0, 0, 0), stuff[i].length, stuff[i].width, stuff[i].height));
            //初始三个关键点
            key_w.push_back(Point(0, stuff[i].width, 0));
            key_h.push_back(Point(0, 0, stuff[i].height));
            key_l.push_back(Point(stuff[i].length, 0, 0));
            cout << i << " the position:(0,0,0)  size:" <<  '('<< (double)stuff[i].length/100 << ',' << (double)stuff[i].width/100 << ',' << (double)stuff[i].height/100 << ')' << endl;
            sum += (double)stuff[i].length/100 * (double)stuff[i].width/100 * (double)stuff[i].height/100;
            continue;
        }
        Point pos = find4(vehicle, BPox, stuff[i], key_l, key_w, key_h);
        int cnt = 0;
        int temp;
        // 六种摆放方式
        while(pos.l < 0 && cnt < 6) {
            if(cnt % 2 == 0) {
                temp = stuff[i].length;
                stuff[i].length = stuff[i].width;
                stuff[i].width = temp;
            }
            else if( cnt % 2 == 1) {
                temp = stuff[i].width;
                stuff[i].width = stuff[i].height;
                stuff[i].height = temp;
            }
            pos = find4(vehicle, BPox, stuff[i], key_l, key_w, key_h);
            cnt++;
        }
        if(pos.l < 0) {
            cout << " can not find position for the " << i << "th  stuff" << endl;
            continue;
        }
        //如果可以装载
        BPox.push_back(BPoint(pos, stuff[i].length, stuff[i].width, stuff[i].height));
        
        key_w.push_back(Point(pos.l, pos.w + stuff[i].width, pos.h));
        key_h.push_back(Point(pos.l, pos.w, pos.h + stuff[i].height));
        key_l.push_back(Point(pos.l+stuff[i].length, pos.w, pos.h));
        cout << i << " the position:" << '(' << (double)pos.l/100 << ',' << (double)pos.w/100 << ',' << (double)pos.h/100 << ')' << "  size:" <<  '('
        << (double)stuff[i].length/100 << ',' << (double)stuff[i].width/100 << ',' << (double)stuff[i].height/100 << ')' << endl;
        sum += (double)stuff[i].length/100 * (double)stuff[i].width/100 * (double)stuff[i].height/100;
        //cout << "debug:" << (double)stuff[i].length/100 << endl;
        //cout << "debug:" << sum << endl;
    }
    sum = sum / ((double)(vehicle.length/100) * (double)vehicle.width/100 * (double)vehicle.height/100);
    cout << "共装载" << BPox.size() << "/" << stuff.size() << "个箱子" << endl;
    cout << "装载率" << sum << endl;
    return (int)BPox.size();
}
int upload(const Box vehicle, vector<Box> &stuff) {
    double sum = 0;
    int num = 0;
    int temp;
    list<Point> key_l, key_w, key_h;
    key_w.push_back(Point(0, 0, 0));
    Point pos = Point(-1, -1, -1);
    for(int i = 0; i < stuff.size(); i++) {
        pos = find3(vehicle, stuff[i], key_l, key_w, key_h);
        int cnt = 0;
        // 六种摆放方式
        while(pos.l < 0 && cnt < 6) {
            if(cnt % 2 == 0) {
                temp = stuff[i].length;
                stuff[i].length = stuff[i].width;
                stuff[i].width = temp;
            }
            else if( cnt % 2 == 1) {
                temp = stuff[i].width;
                stuff[i].width = stuff[i].height;
                stuff[i].height = temp;
            }
            pos = find3(vehicle, stuff[i], key_l, key_w, key_h);
            cnt++;
        }
        if(pos.l < 0) {
            cout << " can not find position for the " << i << "th  stuff" << endl;
            continue;
        }
        for(int k = pos.l; k < pos.l + stuff[i].length; k++) {
            for(int j = pos.w; j < pos.w + stuff[i].width; j++) {
                loaded[k][j].start[loaded[k][j].count] = pos.h;
                loaded[k][j].h[loaded[k][j].count] = stuff[i].height;
                loaded[k][j].count++;
            }
        }
        //key.remove(pos);
        key_w.push_back(Point(pos.l, pos.w + stuff[i].width, pos.h));
        key_h.push_back(Point(pos.l, pos.w, pos.h + stuff[i].height));
        key_l.push_back(Point(pos.l+stuff[i].length, pos.w, pos.h));
        cout << i << " the position:" << '(' << pos.l << ',' << pos.w << ',' << pos.h << ')' << "  size:" <<  '('
        << stuff[i].length << ',' << stuff[i].width << ',' << stuff[i].height << ')' << endl;
        sum += (double)stuff[i].length/100 * (double)stuff[i].width/100 * (double)stuff[i].height/100;
        num += 1;
    }
    sum = sum / ((double)(vehicle.length/100) * (double)vehicle.width/100 * (double)vehicle.height/100);
    cout << "共装载" << num << "/" << stuff.size() << "个箱子" << endl;
    cout << "装载率：" << sum << endl;
    return num;
}
int main(int argc, const char * argv[]) {
    Box vehicle(58700, 23300, 22000);
    vector<Box> stuff;
    int num;
    cout << "请输入货物的种类数量：" << endl;
    cin >> num;
    cout << "请逐行输入每个货物的长宽高：" << endl;
    //int l, w, h, index;
    double l, w, h;
    int index;
    for(int i = 0; i < num; i++) {
        cin >> l >> w >> h >> index;
        for(int j = 0; j < index; j++){
            stuff.push_back(Box((int)(l*100), (int)(w*100), (int)(h*100)));
        }
    }
    randomlize(stuff);
    //将物体放平，即高<长， 高<宽
    normalize(stuff);
    
    //离线情况下，将物体按体积降序排序
    //sort(stuff.begin(), stuff.end(), comp);
    for(int i = 0; i < stuff.size(); i++) {
        cout << '('<< (double)stuff[i].length/100 << ',' << (double)stuff[i].width/100 <<
        ',' << (double)stuff[i].height/100 << ')' << endl;
    }
    clock_t start=clock();
    upload1(vehicle, stuff);
    cout<<"time："<<(clock() - start) / CLOCKS_PER_SEC<<endl;
    return 0;
}







