#include<stdio.h>
#include<string.h>
#include<algorithm>
#include<vector>
#include<stack>
#include<time.h>
#include<set>
#include<queue>
#include<math.h>
#include<map>
#include<windows.h>
#include "my3dbpp.h"
using namespace std;
void BR_INPUT::read(){
    scanf("%d%d%d",&container.x,&container.y,&container.z);
    scanf("%d",&nType);
    if (nType>=MAXTYPE){printf("type=%d\n",nType);exit(-4);}
    for (int i=1;i<=nType;i++){
      int tmp;scanf("%d",&tmp);
      scanf("%d %d %d %d %d %d %d",&l[i],&il[i],&w[i],&iw[i],&h[i],&ih[i],&nNum[i]);
      //使用冒泡排序对货箱长宽高按照w>l>h的顺序排序
      if (w[i]<l[i]) swap(w[i],l[i]),swap(iw[i],il[i]);
      if (l[i]<h[i]) swap(l[i],h[i]),swap(il[i],ih[i]);
      if (w[i]<l[i]) swap(w[i],l[i]),swap(iw[i],il[i]);
    }
  }

short occupy[600][600][600];
double BR_INPUT::solution_verify(vector<CUBOID>& box,vector<POINT3>& pos){
     int totV=0;
     for (int i=0;i<container.x;i++)
       for (int j=0;j<container.y;j++)
         for (int k=0;k<container.z;k++)
           occupy[i][j][k]=0;
     for (int i=0;i<box.size();i++){
       CUBOID b=box[i];
       totV+=b.getVolumn();
       int len[3]={b.x,b.y,b.z};sort(len,len+3);
       //计算盒子的类型
       int boxType=-1;
       for (int t=1;t<=nType;t++){
          if (w[t]==len[2] && l[t]==len[1] && h[t]==len[0] && nNum[t]>0) {boxType=t;break;}
       }
       //减去盒子数
       if (boxType==-1) {
           printf("No Box For %d*%d*%d\n",b.x,b.y,b.z);
           exit(11);
        }
       nNum[boxType]--;
       //空间被占标记
       POINT3 boxPos=pos[i];
       if (boxPos.x+b.x>container.x || boxPos.y+b.y>container.y ||boxPos.z+b.z>container.z){
         printf("(%d,%d,%d)",boxPos.x+b.x,boxPos.y+b.y,boxPos.z+b.z);container.display();
         printf("x ,y,z?????");exit(12);
       }
       for (int px=boxPos.x;px<boxPos.x+b.x;px++)
         for (int py=boxPos.y;py<boxPos.y+b.y;py++)
           for (int pz=boxPos.z;pz<boxPos.z+b.z;pz++)
           if (occupy[px][py][pz]){
             printf("(%d,%d,%d) has been occupied! %d box\n",px,py,pz,i);
             exit(12);
           }else
           occupy[px][py][pz]=1;
     }
     return 1.0*totV/container.getVolumn();
}
void  HEAP::push(STATE* state,int volumn){
    //for (int i=0;i<v.size();i++) if (volumn==v[i])return;

    s.push_back(state);
    v.push_back(volumn);
    int k=s.size()-1;
    while (k>=1 && v[k]>v[k-1]) {
        swap(s[k],s[k-1]);
        swap(v[k],v[k-1]);
        k--;
    }
    while (s.size()>n) {
        delete s[s.size()-1];
        s.pop_back();
        v.pop_back();
    }
  }
int BLOCK::initHash(){
    #define MOD 1000000007
    hash=0;
    for (int i=1;i<MAXTYPE;i++) hash+=i*i*nBoxNum[i];
    if (C2_CONSTRAIN)
      hash=1ll*hash*(nUpperX*1000+nUpperY)%MOD+1;
    hash=1ll*hash*(cEnvelop.x*10000+cEnvelop.y*100+cEnvelop.z)%MOD+1;
    return 0;
}

BLOCK::BLOCK(int x,int y,int z,int boxType,int boxNum){                  //Simple Block
    cEnvelop.x=x;
    cEnvelop.y=y;
    cEnvelop.z=z;
    nBoxVolumn=x*y*z;
    nType=0;

    bl1=bl2=NULL;
    if (C2_CONSTRAIN){
      nUpperX=x;
      nUpperY=y;
    }else{
      nUpperX=nUpperY=0;
    }
    memset(nBoxNum,0,sizeof(nBoxNum));
    nBoxNum[boxType]=boxNum;
    isSimple=boxType;
    initHash();
  }
BLOCK::BLOCK(BLOCK* b1,BLOCK* b2,int type){                //General Block。纯粹结合两个BLOCK，不进行其他约束操作(如盒子数超出，体积率太低)
    bl1=b1;
    bl2=b2;
    nType=type;
    isSimple=0;
    nBoxVolumn=bl1->nBoxVolumn+bl2->nBoxVolumn;
    for (int i=0;i<MAXTYPE;i++)
      nBoxNum[i]=bl1->nBoxNum[i] + bl2->nBoxNum[i];
    //先预处理，再根据具体类型调整
    cEnvelop.x=max(bl1->cEnvelop.x,bl2->cEnvelop.x);
    cEnvelop.y=max(bl1->cEnvelop.y,bl2->cEnvelop.y);
    cEnvelop.z=max(bl1->cEnvelop.z,bl2->cEnvelop.z);
    BLOCK* tmp;
    switch (nType){
      case 1:
        cEnvelop.x=bl1->cEnvelop.x+bl2->cEnvelop.x;
        nUpperX=bl1->nUpperX;
        nUpperY=bl1->nUpperY;
        break;
      case 2:
        cEnvelop.y=bl1->cEnvelop.y+bl2->cEnvelop.y;
        nUpperX=bl1->nUpperX;
        nUpperY=bl2->nUpperY;
        break;
      case 3:
        cEnvelop.z=bl1->cEnvelop.z+bl2->cEnvelop.z;
        nUpperX=bl2->nUpperX;
        nUpperY=bl2->nUpperY;
        break;
      default:
        exit(-1);
    }
    initHash();
  }

bool BLOCK::isGeneralBlock(){ return nType!=0;}
int BLOCK::display(){
    printf("[BLOCK] %d*%d*%d  [UPPER] %d*%d isSimple:%d nType:%d FillRate:%lf %d %lf\n",
           cEnvelop.x,cEnvelop.y,cEnvelop.z,nUpperX,nUpperY,isSimple,nType,1.0*nBoxVolumn/cEnvelop.getVolumn()*1.0,
           nUpperX * nUpperY , cEnvelop.x*cEnvelop.y * MinAreaRate
           );

    for (int i=1;i<MAXTYPE;i++){
      if (nBoxNum[i])printf("    [%d] numer:%d\n",i,nBoxNum[i]);
    }
}
#define MATCH(w,l,h,env) (env.x%w==0 && env.y%l==0 && env.z%h==0)
int BLOCK::decompose(POINT3 blkPos,vector<CUBOID>& boxType,vector<POINT3>& boxPos,BR_INPUT& input){
    int w,l,h,num,type;
    CUBOID c,box;
    switch(nType){
      case 0: //simple block
         type=isSimple;
        //盒子大小
         box;
         w=input.w[type];
         l=input.l[type];
         h=input.h[type];
         num=nBoxVolumn/(w*h*l);
        //num个盒子组成的大小 1,2,3  =>2,1,3 =>  3,1,2
        //（1）
         c=cEnvelop;
        if (MATCH(l,w,h,c) || MATCH(l,h,w,c)) swap(w,l);
        if (MATCH(h,w,l,c) || MATCH(h,l,w,c)) swap(w,h);
        if (MATCH(w,h,l,c)) swap(l,h);
        if (!MATCH(w,l,h,c)) exit(1);
        for (int i=0;i<cEnvelop.x/w;i++)
          for (int j=0;j<cEnvelop.y/l;j++)
            for (int k=0;k<cEnvelop.z/h;k++){
              POINT3 pos=blkPos+CUBOID(i*w,j*l,k*h);
              boxType.push_back(CUBOID(w,l,h));
              boxPos.push_back(pos);
            }
        break;
      case 1: //x结合
        bl1->decompose(blkPos,boxType,boxPos,input);
        bl2->decompose(blkPos+CUBOID(bl1->cEnvelop.x,0,0),boxType,boxPos,input);
        break;
      case 2: //y结合
        bl1->decompose(blkPos,boxType,boxPos,input);
        bl2->decompose(blkPos+CUBOID(0,bl1->cEnvelop.y,0),boxType,boxPos,input);
        break;
      case 3: //z结合
        bl1->decompose(blkPos,boxType,boxPos,input);
        bl2->decompose(blkPos+CUBOID(0,0,bl1->cEnvelop.z),boxType,boxPos,input);
        break;
    }
    return 0;
}
//STATE
STATE::STATE(int *nBoxNum,CUBOID* container){
    pbl.clear();
    vol=0;
    for (int i=0;i<MAXTYPE;i++)Bres[i]=nBoxNum[i];
    isComplete=0;
    Rs_stack.push(*container);
    Rs_stack_pos.push(POINT3(0,0,0));
  }

STATE::STATE(STATE *state){                       //用于MultiLayerSearchc
    *this=*state;
    for (int i=0;i<MAXTYPE;i++) Bres[i]=state->Bres[i];
  }
//implementation
int BLS::init(BR_INPUT& input){
  block_hash.clear();
  for (int i=0;i<blockTable.size();i++)delete blockTable[i];
  blockTable.clear();
  container=input.container;
  //以下初始化box table
  //盒子数
  nType=input.nType;
  if (nType<=5) MaxSearchEffort=1<<8;else MaxSearchEffort=1<<4;
  for (int i=1;i<=input.nType;i++){
     nBoxNum[i]=input.nNum[i];
  }
  //生成不同朝向的block。最多有6种：顶面3种情况×正面2种情况
  for (int i=1;i<=input.nType;i++){
    int w=input.w[i];
    int h=input.h[i];
    int l=input.l[i];

    if (input.ih[i]){                                      //h作为高
      insertBlock(new BLOCK(l,w,h,i,1));
      insertBlock(new BLOCK(w,l,h,i,1));
    }
    if (input.iw[i]){                                      //w作为高
      insertBlock(new BLOCK(l,h,w,i,1));
      insertBlock(new BLOCK(h,l,w,i,1));
    }
    if (input.il[i]){                                      //l作为高
      insertBlock(new BLOCK(w,h,l,i,1));
      insertBlock(new BLOCK(h,w,l,i,1));
    }
  }
  //
  if (state!=NULL)delete state;
  state=new STATE(nBoxNum,&container);
  sol_box.clear();
  sol_boxPos.clear();
}
bool BLS::isBlockValid(BLOCK* block){
  //(1)C2限制
  if (C2_CONSTRAIN){
     //当为z叠放时，检测bl1顶部面积是否足够叠放bl2
     if (block->nType==3)
     if (block->bl1->nUpperX < block->bl2->cEnvelop.x || block->bl1->nUpperY < block->bl2->cEnvelop.y)
       return false;
     //顶部面积百分比至少为MinAreaRate
     if (block->nUpperX * block->nUpperY < block->cEnvelop.x*block->cEnvelop.y * MinAreaRate)
      return false;
  }
  //(2)三维不超过container
  if (block->cEnvelop.x > container.x || block->cEnvelop.y > container.y || block->cEnvelop.z > container.z) return false;
  //(3)体积百分比至少为MinFillRate
  if (block->nBoxVolumn < block->cEnvelop.getVolumn()*MinFillRate)
    return false;
  //(4)盒子数足够
  for (int i=1;i<=nType;i++)
    if (nBoxNum[i]<block->nBoxNum[i])
    return false;
  //(5)面积限制
  switch (block->nType){
    case 1:
      if (block->bl1->cEnvelop.y * block->bl1->cEnvelop.z < block->bl2->cEnvelop.y * block->bl2->cEnvelop.z) return false;
      break;
    case 2:
      if (block->bl1->cEnvelop.x * block->bl1->cEnvelop.z < block->bl2->cEnvelop.x * block->bl2->cEnvelop.z) return false;
      break;
    case 3:
      if (block->bl1->cEnvelop.x * block->bl1->cEnvelop.y < block->bl2->cEnvelop.x * block->bl2->cEnvelop.y) return false;
      break;
    default:
      exit(-1);
  }
  //(6)测试是否有重复。（envelope一致，block一致，顶部面积一致）
  #ifdef HASH
  if (block_hash.count(block->hash)==0)
      return true;
  return false;
  #endif
}

int  BLS::insertBlock(BLOCK *block){
  if (block_hash.count(block->hash)==0 && container.contain(block->cEnvelop)){
    block_hash.insert(block->hash);
    blockTable.push_back(block);
  }else
  delete block;
  return 0;
}
int  BLS::genSimpleBlock(){  //不需要进行isBlockValid验证
  int sz=blockTable.size();
  for (int boxId=0;boxId<sz;boxId++){
    BLOCK* cur = blockTable[boxId];

    int    type= cur->isSimple;
    //同一type同一方向叠放
    for (int nx=1;nx<=nBoxNum[type];nx++)
      for (int ny=1;ny<=nBoxNum[type]/nx;ny++)
        for (int nz=1;nz<=nBoxNum[type]/nx/ny;nz++){
          if (nx*ny*nz == 1)continue;
          if (cur->cEnvelop.x * nx <=container.x && cur->cEnvelop.y*ny<=container.y && cur->cEnvelop.z*nz<=container.z){
            BLOCK *newBlock=new BLOCK(cur->cEnvelop.x * nx,cur->cEnvelop.y*ny,cur->cEnvelop.z*nz,type,nx*ny*nz);

            insertBlock(newBlock);
          }
        }
  }
}
int BLS::genGeneralBlock(){
  //hash
  int totalBlock=blockTable.size();
  int curLevel_l=0;
  int curLevel_r=blockTable.size()-1;
  for (int level=1;level<=MaxLevel && blockTable.size()<MaxBlocks;level++){
     //两两枚举组合
     int ts=GetTickCount();
     for (int i=curLevel_l;i<=curLevel_r && blockTable.size()<MaxBlocks; i++)
       for (int j=curLevel_l;j<=curLevel_r && blockTable.size()<MaxBlocks; j++){
          if (level ==1 && i==j) continue;         //general block退化成simple block，跳过。
          BLOCK* b1=blockTable[i];
          BLOCK* b2=blockTable[j];
          //x结合
          if (b1->cEnvelop.y*b1->cEnvelop.z >= b2->cEnvelop.y*b2->cEnvelop.z && isBlockValid(&BLOCK(b1,b2,1))) {
              insertBlock(new BLOCK(b1,b2,1));
          }
          //y结合
          if (b1->cEnvelop.x*b1->cEnvelop.z >= b2->cEnvelop.x*b2->cEnvelop.z && isBlockValid(&BLOCK(b1,b2,2))) {
              insertBlock(new BLOCK(b1,b2,2));
          }
          //z结合
          if (b1->cEnvelop.x*b1->cEnvelop.y >= b2->cEnvelop.x*b2->cEnvelop.y && isBlockValid(&BLOCK(b1,b2,3))) {
              insertBlock(new BLOCK(b1,b2,3));
          }
       }
       curLevel_l=curLevel_r+1;
       curLevel_r=blockTable.size()-1;
  }
}
/********************************************/
bool BLS::hasEnoughBox(STATE* state,BLOCK* block){     //state中是否存在足够的box
    for (int i=1;i<=nType;i++)
      if (state->Bres[i] < block->nBoxNum[i])
      return false;
    return true;
}
int  BLS::generateRSBlockList(STATE* state,CUBOID rs,POINT3 rs_pos,int mxBlocks,vector<BLOCK*>* bll){
   //二分加速
   int rs_vol=rs.getVolumn();
   int idx_l=0,idx_r=blockTable.size()-1;
   while (idx_l < idx_r){
     int mid=(idx_l+idx_r)>>1;
     if (blockTable[mid]->cEnvelop.getVolumn() >rs_vol)
       idx_l=mid+1;
     else
       idx_r=mid;
   }
   //查找
   bll->clear();
   for (int i=idx_l;i<blockTable.size();i++){
       if (!rs.contain(&(blockTable[i]->cEnvelop))) continue;  //rs?过小
       if (!hasEnoughBox(state,blockTable[i]))continue;//剩余可装载块的box数量不够
       bll->push_back(blockTable[i]);
       if (bll->size() == mxBlocks+1) break;
   }
   while (bll->size()>mxBlocks){
     int idx=rand()%bll->size();
     swap((*bll)[idx],(*bll)[bll->size()-1]);
     bll->pop_back();
   }
   return 0;
}
int  BLS::completeState(STATE *s){
   STATE *state=new STATE(s);              //复制一份
   vector<BLOCK*>* bll=new vector<BLOCK*>;
   while (!state->Rs_stack.empty()){
      //取栈顶可装载空间space
      CUBOID curRs=state->Rs_stack.top();
      POINT3 curRs_pos=state->Rs_stack_pos.top();
      //生成block
      bll->clear();
      generateRSBlockList(state,curRs,curRs_pos,1,bll);
      if (bll->size()==0) {
          state->Rs_stack.pop();
          state->Rs_stack_pos.pop();
          continue;                  //不存在block满足curRs
      }else
          placeBlock(state,(*bll)[0]);
   }
   delete bll;
   state->isComplete=true;
   int vol=state->vol;
   delete state;
   return vol;
}
int  BLS::placeBlock(STATE *state,BLOCK* block){  //将block放入state的栈顶。
   #ifdef DEBUG
   if (state->Rs_stack.empty()) exit(-7);
   #endif
   CUBOID space=state->Rs_stack.top(); //取栈顶可装载空间space
   POINT3 space_pos=state->Rs_stack_pos.top(); //及对应坐标
   state->Rs_stack.pop();             //弹出栈顶空间
   state->Rs_stack_pos.pop();         //弹出对应坐标
   #ifdef DEBUG
   if (!space.contain(block->cEnvelop)) {
       printf("Place Block Error:");
       space.display();
       block->cEnvelop.display();
       //state->display();
       exit(-6);
   }
   #endif
   //遍历所有货物
   for (int i=1;i<=nType;i++){
       #ifdef DEBUG
       if (state->Bres[i]<block->nBoxNum[i]) exit(-2);
       #endif
       state->Bres[i]-= block->nBoxNum[i]; //将当前可装载块从装载状态中的剩余可装载块列表中删除
   }
   state->pbl.push_back(block);  //将当前可装载快加入装载状态中的已装载列表
   state->pbl_pos.push_back(space_pos); //加入相应坐标
   state->vol+=block->nBoxVolumn; //加入对应体积
   generateDaughterSpaces(state,space,space_pos,block,NULL); //生成当前将当前可装载块放置后的新的可装载空间
   return 0;
}
int  BLS::removeBlock(STATE *state,BLOCK* block,CUBOID rs,POINT3 rs_pos){//恢复放置操作 
   for (int i=1;i<=3;i++)  state->Rs_stack.pop(),state->Rs_stack_pos.pop();   //弹出放置生成的3个可装载空间
   state->pbl.pop_back();  //装载状态中的已装载列表栈顶弹出块
   state->pbl_pos.pop_back();  //弹出对应坐标  
   state->vol -=block->nBoxVolumn; //删除对应体积  
   for (int i=1;i<=nType;i++){
     state->Bres[i]+=block->nBoxNum[i]; //遍历货物，将block的重新加到剩余可装载列表中  
   }
   state->Rs_stack.push(rs);  //将原可装载空间加入到可装载状态中的可装载空间堆
   state->Rs_stack_pos.push(rs_pos); //加入相应坐标  
   return 0;
}


int BLS::generateDaughterSpaces(STATE* state,CUBOID curRs,POINT3 curRs_pos,BLOCK *block,vector<BLOCK*>* blockList=NULL){
  #ifdef DEBUG
  int space_sz=state->Rs_stack.size();
  #endif
  CUBOID blRs=block->cEnvelop;
  int rmx=curRs.x - blRs.x;
  int rmy=curRs.y - blRs.y;
  int rmz=curRs.z - blRs.z;
  //判断rmx,rmy,rmz是否太短使得不存在block可以放置
  bool bx=false;
  bool by=false;
  bool bz=false;
  if (blockList == NULL) blockList=& blockTable;
  for (int i=blockList->size()-1;i>=0;i--){
    if ((*blockList)[i]->cEnvelop.x <=rmx) bx=true;
    if ((*blockList)[i]->cEnvelop.y <=rmy) by=true;
    if ((*blockList)[i]->cEnvelop.z <=rmz) bz=true;

  }
  POINT3 p_x=POINT3(curRs_pos.x+block->cEnvelop.x,curRs_pos.y,curRs_pos.z);
  POINT3 p_y=POINT3(curRs_pos.x,curRs_pos.y+block->cEnvelop.y,curRs_pos.z);
  POINT3 p_z=POINT3(curRs_pos.x,curRs_pos.y,curRs_pos.z+block->cEnvelop.z);
  
  state->Rs_stack_pos.push(p_x);
  state->Rs_stack_pos.push(p_y);
  state->Rs_stack_pos.push(p_z);
 //（一）考虑C2约束只有两种情况(1,2)
  if (C2_CONSTRAIN){
    if (rmx>=rmy ||!by){
        state->Rs_stack.push(CUBOID(rmx,curRs.y,curRs.z));
        state->Rs_stack.push(CUBOID(blRs.x,rmy,curRs.z));
    }else{
        state->Rs_stack.push(CUBOID(rmx,blRs.y,curRs.z));
        state->Rs_stack.push(CUBOID(curRs.x,rmy,curRs.z));
    }
    state->Rs_stack.push(CUBOID(blRs.x,blRs.y,rmz)); //上方的最小
  }

  else{
  //（二）不考虑C2约束
  //以下分类6种（不考虑C2约束）
  if ((rmx >=rmy || !by) && (rmx>=rmz || !bz)){ //rmx => max
     state->Rs_stack.push(CUBOID(rmx,curRs.y,curRs.z));
     if (by &&(rmy >= rmz ||!bz)){  //情况一
         state->Rs_stack.push(CUBOID(blRs.x,rmy,curRs.z));
         state->Rs_stack.push(CUBOID(blRs.x,blRs.y,rmz));
     }else{                     //情况三
         state->Rs_stack.push(CUBOID(blRs.x,rmy,blRs.z));
         state->Rs_stack.push(CUBOID(blRs.x,curRs.y,rmz));
     }
  }else
  if ((rmy >=rmx || !bx) && (rmy>=rmz || !bz)){//rmy=>max
     if (bx && (rmx>=rmz || !bz)){ //情况二

         state->Rs_stack.push(CUBOID(rmx,blRs.y,curRs.z));
         state->Rs_stack.push(CUBOID(curRs.x,rmy,curRs.z));
         state->Rs_stack.push(CUBOID(blRs.x,blRs.y,rmz));
     }else{                //情况五
         state->Rs_stack.push(CUBOID(rmx,blRs.y,blRs.z));
         state->Rs_stack.push(CUBOID(curRs.x,rmy,curRs.z));
         state->Rs_stack.push(CUBOID(curRs.x,blRs.y,rmz));

     }
  }
  else{
     
     if (bx && (rmx >= rmy || !by)){ //情况四
         state->Rs_stack.push(CUBOID(rmx,curRs.y,blRs.z));
         state->Rs_stack.push(CUBOID(blRs.x,rmy,blRs.z));
     }else{                         //情况六
         state->Rs_stack.push(CUBOID(rmx,blRs.y,blRs.z));
         state->Rs_stack.push(CUBOID(curRs.x,rmy,blRs.z));
     }
     state->Rs_stack.push(CUBOID(curRs.x,curRs.y,rmz));
     }//当bx,by,bz都太小就不要加了
  }
  #ifdef DEBUG
  if (state->Rs_stack.size()-space_sz!=3)exit(-8);
  CUBOID c1=state->Rs_stack.top();state->Rs_stack.pop();
  CUBOID c2=state->Rs_stack.top();state->Rs_stack.pop();
  CUBOID c3=state->Rs_stack.top();state->Rs_stack.pop();
  if (c1.getVolumn()+c2.getVolumn()+c3.getVolumn()+block->cEnvelop.getVolumn()!=curRs.getVolumn())exit(-9);
  state->Rs_stack.push(c3);
  state->Rs_stack.push(c2);
  state->Rs_stack.push(c1);
  #endif
  return 0;
}

//找到最优的下一块。执行后不改变state  
BLOCK* BLS::findNextBlock(STATE* s,int search_effort){ //不存在返回null
  //不存在rs，退出  
  if (s->Rs_stack.empty())return NULL;
  STATE *state=new STATE(s);
  //全局最优
  BLOCK *bestBlock=NULL;
  int    bestVolum=state->vol; //粗略查找后能找到的最好的
  //定义heap 
  HEAP *curHeap,*nextHeap;
  curHeap=new HEAP(MaxHeap);
  nextHeap=new HEAP(MaxHeap);
  //Layer 0
  int pbl_sz=state->pbl.size();
  curHeap->push(state,0);      //第0层只有1个，故值无所谓(另外，由于最后会清空heap,heap.clear会delete内部state，故无需再次delete)
  vector<BLOCK*>* bll=new vector<BLOCK*>;

  for (int layer=1;layer<=MaxLayer;layer++){
    for (int i=0;i<curHeap->size();i++){ //枚举当前layer
      STATE* curState=curHeap->get(i);
      //产生后代节点
      //栈顶空间
      bll->clear();
      CUBOID space;
      POINT3 space_pos;
      //找到一个可以产生后代节点的space
      bool find=false;
      while (!find){
         if (curState->Rs_stack.empty())break;
         space=curState->Rs_stack.top();
         space_pos=curState->Rs_stack_pos.top();
         generateRSBlockList(curState,space,space_pos,MaxHeap,bll);
         if (bll->size()!=0)find=true;
         else{
           if (layer==1) {s->Rs_stack.pop();s->Rs_stack_pos.pop();}
           curState->Rs_stack.pop();
           curState->Rs_stack_pos.pop();
         }
      }
      if (!find)continue;//当前state没有后续节点
      for (int i=0;i<bll->size();i++){
          BLOCK* nxtBlk=(*bll)[i];
          STATE* nxtState=new STATE(curState);
          placeBlock(nxtState,nxtBlk);
          //当前搜索：在curState放入nxtBlk，形成nxtState，针对nxtState进行不同深度的搜索
          //保存nxtState进行不同深度搜索后的最优值
          int nxtBestVol=nxtState->vol;//以下搜索不同深度，以获取当前策略(nxtBlk)可以达到的体积
          for (int d=1;d<=MaxDepth;d++){
              int branch=GETBRANCH(d,search_effort);
              if (branch==1) branch=2;
              int curVol=dfs(nxtState,d,branch);
              //更新global best
              if ( nxtBestVol <curVol)
                nxtBestVol=curVol;
          }
          //现在curState+nxtBlk=CurState，最好的体积为nxtBestVol。放入下一个layer
          nextHeap->push(nxtState,nxtBestVol);
          //由于生成state途中，可能有state complete，故每次生成都保存全局最优
          if (bestVolum<nxtBestVol){
            bestVolum=nxtBestVol;
            bestBlock=nxtState->pbl[pbl_sz];
          }
      }
    }

    if (nextHeap->size()==0) break;          //搜不到下个了  
    swap(curHeap,nextHeap);
    nextHeap->clear();
  }
  curHeap->clear();
  nextHeap->clear();
  delete curHeap;
  delete nextHeap;
  return bestBlock;
}

int  BLS::dfs(STATE* state,int depth,int branch){
//return value: state出发最多的体积大小。
  if (depth !=0){
     //residual space为空
     if (state->Rs_stack.size()==0){
       return state->vol;
     }
     //取栈顶空间
     CUBOID rs=state->Rs_stack.top();
     POINT3 rs_pos=state->Rs_stack_pos.top();

     vector<BLOCK*> *blockList=new vector<BLOCK*>;
     blockList->clear();
     generateRSBlockList(state,rs,rs_pos,LayerExt,blockList); //生成可装载块列表  

     //不存在满足rs的block
     if (blockList->size()==0){ 
        state->Rs_stack.pop();
        state->Rs_stack_pos.pop();
        int v=dfs(state,depth,branch); //弹出栈顶空间进行下一次dfs  
        state->Rs_stack.push(rs); //恢复
        state->Rs_stack_pos.push(rs_pos);
        delete blockList;
        return v;
     }else{
         int mxVol=state->vol;
         for (int i=0;i<min(branch,(int)blockList->size());i++){   //选择branch进行搜索  
             //放置block
             placeBlock(state,(*blockList)[i]);
             int k=dfs(state,depth-1,branch);
             //恢复
             removeBlock(state,(*blockList)[i],rs,rs_pos);
             mxVol=max(mxVol,k); //维护最优值
         }
         delete blockList;
         return mxVol;
     }
  }else{
     return completeState(state);
  }
}

int BLS::accelerate(){
  int mx_x=0,mx_y=0,mx_z=0,mx_v=0;
  //以下获取所有rs中，最大的体积，x轴大小，y轴大小，z轴大小
  vector<CUBOID>* rs=new vector<CUBOID>;
  while (!state->Rs_stack.empty()){
    CUBOID curRs=state->Rs_stack.top();
    state->Rs_stack.pop();
    mx_x=max(mx_x,curRs.x);
    mx_y=max(mx_y,curRs.y);
    mx_z=max(mx_z,curRs.z);
    mx_v=max(mx_v,curRs.getVolumn());
    rs->push_back(curRs);
  }
  //恢复rs stack
  //sort(rs->begin(),rs->end(),cmp_rs);//从大到小排序rs
  for (int i=rs->size()-1;i>=0;i--){
    state->Rs_stack.push((*rs)[i]);
  }
  delete rs;
  //blocktable缩小
  int curIdx=0;
  for (int i=0;i<blockTable.size();i++){
    CUBOID cb=blockTable[i]->cEnvelop;
    //太大的block删去
    if (cb.x>mx_x && cb.y>mx_y && cb.z>mx_z &&cb.getVolumn()>mx_v) continue;
    //box不足的删去
    bool notEnoughBox=false;
    for (int boxId=1;boxId<=nType;boxId++){
      if (state->Bres[boxId] < blockTable[i]->nBoxNum[boxId]) {notEnoughBox=true;break;}
    }
    if (notEnoughBox) continue;
    blockTable[curIdx++]=blockTable[i];
  
  }
  while (blockTable.size()>curIdx) blockTable.pop_back();
  return 0;
}
double BLS::Work(BR_INPUT &input,bool bGeneral=true){
  //初始化
  init(input);
  //产生blocks，并按体积排序
  genSimpleBlock();
  bGeneral && genGeneralBlock();
  sort(blockTable.begin(),blockTable.end(),cmp_block_table);
  int search_effort=1;
  while (!state->isComplete){
    BLOCK *nextBlock=findNextBlock(state,search_effort);
    if (nextBlock == NULL){state->isComplete=true;break;}
    placeBlock(state,nextBlock);
    nextBlock->decompose(state->pbl_pos[state->pbl_pos.size()-1] ,sol_box,sol_boxPos,input);
    //blockTable[0]->display();
    if (search_effort<MaxSearchEffort)search_effort<<=1;
    #ifdef DEBUG
    printf("Work NextBlock:");nextBlock->display();
    #endif
    accelerate();
  }

  return 1.0*state->vol/container.getVolumn() - 0.1;
}


vector<BR_INPUT> data;
void read(char *filename){
  if (!freopen(filename,"r",stdin)){
    exit(-1);
  }
  int ks=0;
  scanf("%d",&ks);
  data.resize(ks);
  for (int i=0;i<ks;i++){
    int t1,t2;
    scanf("%d%d",&t1,&t2);  //t1是每组数据中的index，t2无用
    data[i].read();
  }
}
BLS bls;
int main(int argc,char** argv){
  read(argv[1]);
  double avgUsage=0;
  for (int i=0;i<5;i++){
    int ts=time(NULL);
    double usageRate=bls.Work(data[i],GenGeneralBlock);
    double usageRate2=data[i].solution_verify(bls.sol_box,bls.sol_boxPos);

    printf("[样例-%d] 空间利用率:%.6lf\n",i+1,usageRate);
    //data[i].output_strategy(bls.sol_box,bls.sol_boxPos);//输出box放置策略
    avgUsage+=usageRate;
    int te=time(NULL);
    printf("         花费时间:%d s\n",te-ts);
  }
  return 0;
}
