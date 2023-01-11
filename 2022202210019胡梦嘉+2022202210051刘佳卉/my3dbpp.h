#include<stdio.h>
#include<string.h>
#include<algorithm>
#include<vector>
#include<stack>
#include<time.h>
#include<set>
#include<queue>
#include<map>
#include<windows.h>
using namespace std;
//#define DEBUG
#define HASH
#define MAXTYPE 101                           //最多的box类型数。下标从1开始
#define GETBRANCH(d,e) (int(pow(1.0*e,1.0/d)))
/*****  参数 *********/
bool   C2_CONSTRAIN    =true;           //是否满足C2约束
bool   GenGeneralBlock =false;           //是否生成复合块
int    MaxLevel        =2;               //复合块迭代次数
double MinAreaRate     =0.96;             //复合块顶部面积最小百分比
double MinFillRate     =0.98;             //复合块最小的空间使用率
int    MaxBlocks       =10000;            //复合块最多个数。（实现中，可略微超过）
int    MaxHeap         =16;                //HEAP中最多元素
int    MaxLayer        =6;
int    LayerExt        =8;               //当前layer某个state最多扩展的节点
int    MaxDepth        =2;                //dfs搜索的深度
int    MaxSearchEffort =1<<8;            //

struct CUBOID{                               //长方体
  int  x,y,z;
  int getVolumn(){return x*y*z;};
  CUBOID(int x=0,int y=0,int z=0):x(x),y(y),z(z){}
  bool contain(CUBOID* p){ return x>=p->x && y>=p->y && z>=p->z; }
  bool contain(CUBOID  c){ return x>=c.x && y>=c.y && z>=c.z; }
  int  display(){ printf("%d * %d * %d =%d\n",x,y,z,x*y*z);}
};
struct POINT3{
  int x,y,z;
  POINT3(int x=0,int y=0,int z=0):x(x),y(y),z(z){}
  POINT3(POINT3 p,CUBOID l){ //
    x=p.x+l.x;
    y=p.y+l.y;
    z=p.z+l.z;
  }
  void display(){printf("(%d,%d,%d)\n",x,y,z);}
};
POINT3 operator + (POINT3 p,CUBOID c){return POINT3(p,c);}
struct BR_INPUT{                             //一组输入数据
  CUBOID container;
  int nType;                                 //下标从1开始
  int l[MAXTYPE];                            //每个盒子按照w>l>h排序
  int w[MAXTYPE];
  int h[MAXTYPE];
  int il[MAXTYPE];
  int iw[MAXTYPE];
  int ih[MAXTYPE];
  int nNum[MAXTYPE];
  void read();
  double solution_verify(vector<CUBOID>& box,vector<POINT3>& pos);
  void   output_strategy(vector<CUBOID>& box,vector<POINT3>& pos){  //
    printf("------------------货物放置策略------------------------\n",box.size());
    //输出box放置位置
    for (int i=0;i<box.size();i++){
      CUBOID t=box[i];
      POINT3 p=pos[i];
      printf("[BLOCK %d] 货物坐标(%3d,%3d,%3d) 货物大小 %d*%d*%d \n",i,p.x,p.y,p.z,t.x,t.y,t.z);
    }
  }

};
struct BLOCK{
  CUBOID cEnvelop;                           //BLOCK外接长方体
  int    nBoxVolumn;                         //BLOCK内部Box体积大小
  int    nBoxNum[MAXTYPE];                    //BLOCK内部Box某类型的个数
  int    nType;                              //0表示Simple Block。 1、2、3分别代表x,y,z结合
  int    isSimple;                           //是否为Simple Block，如果是，记录其box type
  BLOCK* bl1;
  BLOCK* bl2;                                //若为General Block，则由bl1和bl2通过nType方式组合
  //
  int    nUpperX;
  int    nUpperY;                            //当满足稳定放置约束时，记录Block上部的面积
  int    hash;                               //用于判断两个block是否相同
  int    initHash();
  //构造函数
  BLOCK(){}
  BLOCK(int x,int y,int z,int boxType,int boxNum);  //Simple Block
  BLOCK(BLOCK* b1,BLOCK* b2,int type);              //General Block。纯粹结合两个BLOCK，不进行其他约束操作(如盒子数超出，体积率太低)
  //其他
  bool isGeneralBlock();
  int  decompose(POINT3 blkPos,vector<CUBOID>& boxType,vector<POINT3>& boxPos,BR_INPUT& input); //分解当前block。将box存入boxType,boxPos
  int  display();
};


struct STATE{                                //装箱状态
  vector<BLOCK*> pbl;                        //已装载块
  vector<POINT3> pbl_pos;
  int            vol;                          //已装载块的Volumn
  int            Bres[MAXTYPE];              //剩余的Block
  stack<CUBOID>  Rs_stack;                   //剩余的可装载空间堆栈
  stack<POINT3>  Rs_stack_pos;
  bool           isComplete;                 //是否达到最终状态
  //存储最终的solution

  STATE(){}
  STATE(int *nBoxNum,CUBOID* container);
  STATE(STATE *state);                       //复制一份
  const bool operator < (STATE  s2)const{
    return vol> s2.vol;
  }
  void display(){
      printf("--STATE--\n");
    printf("  usage:%d\n",vol);
    printf("  BLOCK:\n");
    for (int i=0;i<pbl.size();i++) printf("  "),pbl[i]->cEnvelop.display();
  }
};

struct HEAP{
  vector<STATE*> s;  // 该heap中的state列表
  vector<int>    v; //s进行complete后的体积
  int n;            //最多保存n个最优STATE
  HEAP(){}
  HEAP(int n):n(n){}
  int size(){return s.size();}
  void   push(STATE* state,int volumn);
  void clear(){ for (int i=0;i<s.size();i++) delete s[i]; s.clear();v.clear();}
  STATE* get(int idx){return s[idx];}
};
//BLS类
//直接调用work函数，返回空间使用率。
//bls.sol_box和bls.solboxPos 记录box的放置位置。
//solution_verify函数验证sol_box和solbox_Pos是否正确。
class BLS{
private:
  /****** 算法数据结构 *********/
  CUBOID           container;                             //放置box的空间
  vector<BLOCK*>   blockTable;                            //生成的block
  int              nType;                                 //所有box种类
  int              nBoxNum[MAXTYPE];                      //各类Box数量
  set<int>         block_hash;                            //block判重。防止生成一样的block
  STATE*           state;                                 //主过程的状态
  /****** 函数  ************/
  bool             isBlockValid(BLOCK* block);           //判断General Block是否满足限制条件
  int              init(BR_INPUT& input);                //对于一组数据input，初始化context
  int              genSimpleBlock();                     //生成simple block。
  int              genGeneralBlock();
  static bool      cmp_block_table(BLOCK *x,BLOCK *y){return x->cEnvelop.getVolumn() > y->cEnvelop.getVolumn();} //用于排序blocks
  static bool      cmp_rs(CUBOID x,CUBOID y){return x.getVolumn() > y.getVolumn();}
  //以下函数用于装载block
  int              insertBlock(BLOCK *block);
  int              placeBlock(STATE *state,BLOCK* block); //将block放入state的栈顶。
  int              removeBlock(STATE *state,BLOCK* block,CUBOID rs,POINT3 rs_pos);//恢复上述操作

  //int              addBlock(STATE *state,BLOCK* block);  //将block加入当前state中。不处理residual space
  int              completeState(STATE *state);       //返回state可以达到的volumn。（贪心）
  BLOCK*           findNextBlock(STATE* state,int search_effort); //MyltiLayerSearch。找到较适合state的下一个block，不存在返回NULL
  int              generateRSBlockList(STATE*state,CUBOID rs,POINT3 rs_pos,int mxBlocks,vector<BLOCK*>* bll); //在state中，找出满足rs的block，存入bll
  //curRs 减去 block，产生3个块加入 state中。 blockList可以放入curRs，用于如何切割。
  int              generateDaughterSpaces(STATE* state,CUBOID curRs,POINT3 curRs_pos,BLOCK *block,vector<BLOCK*>* blockList);
  bool             hasEnoughBox(STATE* state,BLOCK* block);     //state中是否存在足够的box
  //从state出发，进行深度为d，广度为branch的搜索栈顶rs最优的block，搜索不到底用complete_state搞 ，返回最大的体积值。
  //（途中返回时应保证state不被修改）
  int              dfs(STATE* state,int depth,int branch);
  int              accelerate(); //优化
public:
  BLS(){state=NULL;}
  //solution
  vector<CUBOID>   sol_box;
  vector<POINT3>   sol_boxPos;
  double           Work(BR_INPUT &input,bool bGeneral); //返回使用率
};

