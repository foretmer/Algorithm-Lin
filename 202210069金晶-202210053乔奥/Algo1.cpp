#include<bits/stdc++.h>
#define sz(x) (int)(x).size()
#define all(x) (x).begin(),(x).end()
using namespace std;
const int maxn = 110;
const int ethnic_num = 20;
const int pair_n = 10;
const int variation_n = 1;

struct Box{
    int l, w, h;
    Box() {}
    Box(int l, int w, int h) : l(l), w(w), h(h) {}
}; 

struct Cell{
    int l, w, h;
    Cell() {}
    Cell(int l, int w, int h) : l(l), w(w), h(h) {}
};

struct Point{
    int x, y, z;
    Point() {}
    Point(int x, int y, int z) : x(x), y(y), z(z) {}
};

vector<Box> boxs;
Cell cell;
vector<vector<Box>> list_boxs;
vector<Point> put_point;
bool space[590][240][230];
vector<double> values;
vector<vector<pair<Box, Point>>> st;
vector<double> integral;

void init_ethnic() {
    mt19937 rng(time(0));
    vector<Box> tmp = boxs;
    for(int i = 0; i < ethnic_num; i++) {
        shuffle(all(tmp), rng);
        list_boxs.push_back(tmp);
    }
}

bool check_cell(Point p, Box b) {
    if(p.x + b.l <= cell.l && p.y + b.w <= cell.w && p.z + b.h <= cell.h) return true;
    return false;
}

bool check_box(Point p, Box b) {
    int x = p.x, y = p.y, z = p.z;
    int l = b.l, w = b.w, h = b.h;
    if(space[x][y][z] || space[x + l - 1][y][z] || space[x][y + w - 1][z] || space[x][y][z + h - 1] || 
    space[x + l - 1][y + w - 1][z] || space[x + l - 1][y][z + h - 1] || space[x][y + w - 1][z + h - 1] || 
    space[x + l - 1][y + w - 1][z + h - 1]) return false;
    return true;
}

void put_box(Point p, Box b) {
    int x = p.x, y = p.y, z = p.z;
    int l = b.l, w = b.w, h = b.h;
    for(int i = x; i < x + l; i++) 
        for(int j = y; j < y + w; j++) 
            for(int k = z; k < z + h; k++) 
                space[i][j][k] = 1;
}

void pack_box_into_drawer(vector<Box> &list) {
    put_point.clear();
    put_point.push_back(Point(0, 0, 0));
    for(int i = 0; i < cell.l; i++) 
        for(int j = 0; j < cell.w; j++) 
            for(int k = 0; k < cell.h; k++)
                space[i][j][k] = 0;

    vector<pair<Box, Point>> path;
    for(int i = 0; i < sz(list); i++) {
        sort(all(put_point), [&] (Point a, Point b) {
            if(a.z != b.z) return a.z < b.z;
            if(a.y != b.y) return a.y < b.y;
            return a.x < b.x;
        }
        );

        if(list[i].h > cell.h || list[i].w > cell.w || list[i].l > cell.l) continue;

        for(int j = 0; j < sz(put_point); j++) {
            if(check_cell(put_point[j],list[i]) && check_box(put_point[j], list[i])) {
                put_box(put_point[j], list[i]);
                path.push_back(make_pair(list[i], put_point[j]));
                int x = put_point[j].x, y = put_point[j].y, z = put_point[j].z;
                put_point.erase(put_point.begin() + j);
                put_point.push_back(Point(x + list[i].l, y, z));
                put_point.push_back(Point(x, y + list[i].w, z));
                put_point.push_back(Point(x, y, z + list[i].h));
                break;
            }
        }
    }

    int sum = 0;
    for(int i = 0; i < cell.l; i++) 
        for(int j = 0; j < cell.w; j++) 
            for(int k = 0; k < cell.h; k++)
                sum += space[i][j][k];
    double ratio = 1. * sum / (cell.h * cell.l * cell.w);

    values.push_back(ratio);
    st.push_back(path);
}

void get_integral() {
    integral.clear();
    double sum = 0;
    for(int i = 0; i < sz(values); i++) {
        sum += values[i];
        integral.push_back(sum);
    }
}

int my_random() {
    mt19937 gen(time(0));
    uniform_real_distribution<double> dis(0, *max_element(all(integral)));
    double p = dis(gen);
    for(int i = 0; i < sz(integral); i++) {
        if(p < integral[i]) {
            return i;
        }
    }
    return 0;
}

vector<Box> cross(int s1, int s2) {
    vector<Box> res;
    mt19937 rng(time(0));
    if(rng() % 2 == 1) res = list_boxs[s1];
    else res = list_boxs[s2];
    shuffle(all(res), rng);
    return res;
}

void exchange_box(int i) {
    int len = sz(list_boxs[i]);
    mt19937 rng(time(0));
    int s1 = rng() % len, s2 = rng() % len;
    if(s1 < 0) s1 += len;
    if(s2 < 0) s2 += len;
    cout << s1 << ' ' << s2 <<endl;
    swap(list_boxs[i][s1], list_boxs[i][s2]);
}

void solve() {
    init_ethnic();
    cout << sz(list_boxs) <<endl;
    for(int i = 0; i < ethnic_num; i++) pack_box_into_drawer(list_boxs[i]);
    
    double mx = 0, idx = -1;
    for(int i = 0; i < ethnic_num; i++) {
        if(values[i] > mx) {
            mx = values[i];
            idx = i;
        }
    }
    int cnt = 0;
    while(mx < 0.8 && cnt <= 20 && sz(st[idx]) < sz(boxs)) {
        for(int i = 0; i < pair_n; i++) {
            get_integral();
            int s1 = my_random(), s2 = my_random(); 
            while(s1 == s2) s2 = my_random();
            vector<Box> box_new = cross(s1, s2);
            list_boxs.push_back(box_new);
            pack_box_into_drawer(box_new);
        }   

        for(int i = 0; i < sz(list_boxs); i++) {
            for(int j = 0; j < variation_n; j++) {
                mt19937 rng(time(0));
                uniform_real_distribution<double> dis(0, 1);
                double p = dis(rng);
                if(p > 0.5) {
                    vector<Box> tmp = list_boxs[i];
                    values.erase(values.begin() + i);
                    st.erase(st.begin() + i);
                    list_boxs.erase(list_boxs.begin() + i);
                    list_boxs.push_back(tmp);
                    pack_box_into_drawer(tmp);
                }
            }
        }

        for(int i = 0; i < sz(values) - ethnic_num; i++) {
            int idx = min_element(all(values)) - values.begin();
            values.erase(values.begin() + idx);
            st.erase(st.begin() + idx);
            list_boxs.erase(list_boxs.begin() + idx);
        }
        for(int i = 0; i < ethnic_num; i++) {
            if(values[i] > mx) {
                mx = values[i];
                idx = i;
            }
        }
        cnt++;
    }
    cout << mx << endl;
    for(auto p : st[idx]) {
        cout << p.first.h << ' ' << p.first.l << ' ' << p.first.w << ':';
        cout << p.second.x << ' ' << p.second.y << ' ' << p.second.z << endl;
    }
}

int main() {
    freopen("1.in", "r", stdin);
    cin >> cell.l >> cell.w >> cell.h;
    int a[3], cnt;
    while(cin >> a[0] >> a[1] >> a[2] >> cnt) {
        sort(a, a + 3);
        reverse(a, a + 3);
        for(int i = 0; i < cnt; i++)
            boxs.push_back(Box(a[0], a[1], a[2]));
    }
    
    solve();

    return 0;
}