# 3D_Packing
### 李孟泽2022202210048
### 袁泽澄2022202210062
### 问题描述：
物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。
设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：
1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；
2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。
### 启发式算法：
启发式方法是人们在解决问题时所采取的一种根据经验规则来处理问题的方法。其特点是在解决问题时，利用过去的经验，选择已经行之有效的方法，而不是系统地、按照确定的步骤去寻求答案。但由于这种方法具有试错的特点，所以也有失败的可能，对于NP完全类的组合优化问题，目前缺少一般的算法来求解，精确算法又太耗时，所以启发式算法被广泛应用到这些问题的求解中。对于装箱问题亦是如此，自从该问题被提出以来，已经有很多启发式算法应用其中。

因为三维装箱问题本身的复杂性和实际操作需要，我们选择启发式方法来生成放置方案。一个好的启发式算法不但需要迅速找到解，而且需要尽可能地接近最优解，同时还需要提供必要的灵活性，能够适应不同的参数环境和额外条件。我们实现的启发式算法，以一个基于“块”装载的启发式方法为基础，通过深度优先搜索算法选择每个阶段采用的块。“块”装载方法决定了算法的主体，搜索算法决定了算法逼近最优解的速度和效果。

本题中装箱问题求解算法，思想类似于二维装箱问题的递归启发式算法。在算法的开始，生成复合块列表。启发式算法维护一个剩余空间堆栈，自顶向下地装载剩余空间。在算法开始时，容器整体是剩余空间堆栈中唯一的剩余空间。在装载过程中，堆栈剩余空间被取出，在有可行块时使用一个当前最优的块与剩余空间结合生成一个放置，并将未填充的空间切割成新的剩余空间加入堆栈。当没有可行块时，则放弃该空间。重复上述过程直至堆栈为空。

具体代码如下：
#### packing.h
```cpp
#ifndef _PACKING_H
#define _PACKING_H

#include<vector>
#include<stack>
using namespace std;

#define MinFillRate 0.9
#define MaxTimes 2
#define MaxBlocks 500
#define DEPTH 2
#define BRANCH 2

struct Box {
	int lx, ly, lz;
	int type;
	Box(int lx, int ly, int lz, int type) {
		this->lx = lx;
		this->ly = ly;
		this->lz = lz;
		this->type = type;
	}
};

struct Space {
	int x, y, z;
	int lx, ly, lz;
	Space() {}
	Space(int lx, int ly, int lz) {
		this->x = 0;
		this->y = 0;
		this->z = 0;
		this->lx = lx;
		this->ly = ly;
		this->lz = lz;
	}
};

struct Problem {
	Space container;
	vector<Box> box;
	vector<int> num;
	Problem() {}
	Problem(Space container, vector<Box> box, vector<int> num) {
		this->container = container;
		this->box = box;
		this->num = num;
	}
};

struct Block {
	int lx, ly, lz;
	vector<int> require;
	vector<Block> childs;
	int volumn;
	int times;
	int fitness;
};

struct Place {
	Space space;
	Block block;
};

struct PakingState {
	vector<Place> plan;
	stack<Space> spaceStack;
	vector<int> avail;
	int volumn;
	int volumnComplete;
};

extern vector<Block> BlockTable;
extern PakingState best;

vector<Block> GenBlocklist(Space space, vector<int> avail);
vector<Block> GenSimpleBlock(Space container, vector<Box> box, vector<int> num);
vector<Block> GenComplexBlock(Space container, vector<Box> box, vector<int> num);
vector<Space> GenResidualSpace(Space space, Block block);
Block FindNextBlock(PakingState ps, vector<Block> blockList);
int Estimate(PakingState ps);
void PlaceBlock(PakingState *ps, Block block);
void RemoveBlock(PakingState *ps, Space space, Block block);
void Complete(PakingState *ps);
void DepthFirstSearch(PakingState ps, int depth);
PakingState BasicHeuristic(Problem problem);

#endif
```
#### packing.cpp
```cpp
#include"packing.h"
#include<algorithm>

vector<Block> BlockTable;
PakingState best;

static bool BlockCmp(Block b1, Block b2) {
	if (b1.volumn != b2.volumn)
		return b1.volumn > b2.volumn;
	else if (b1.lx != b2.lx)
		return b1.lx > b2.lx;
	else if (b1.ly != b2.ly)
		return b1.ly > b2.ly;
	else if (b1.lz != b2.lz)
		return b1.lz > b2.lz;
	else 
		return false;
}

vector<Block> GenSimpleBlock(Space container, vector<Box> box, vector<int> num) {	// 生成简单块
	vector<Block> blockTable;
	for (Box b : box) {
		for (int nx = 1; nx <= num[b.type]; nx++) {
			for (int ny = 1; ny <= num[b.type] / nx; ny++) {
				for (int nz = 1; nz <= num[b.type] / (nx * ny); nz++) {
					if (b.lx * nx <= container.lx && b.ly * ny <= container.ly && b.lz * nz <= container.lz) {
						vector<int> require(num.size());
						require[b.type] = nx * ny * nz;

						Block block;
						block.lx = b.lx * nx;
						block.ly = b.ly * ny;
						block.lz = b.lz * nz;
						block.require = require;
						block.volumn = block.lx * block.ly * block.lz;
						block.times = 0;
						blockTable.push_back(block);
					}
				}
			}
		}
	}
	sort(blockTable.begin(), blockTable.end(), BlockCmp);
	return blockTable;
}

static bool BlockEqual(Block b1, Block b2) {
	if (b1.lx == b2.lx && b1.ly == b2.ly && b1.lz == b2.lz && b1.volumn == b2.volumn)
		return true;
	return false;
}

vector<Block> GenComplexBlock(Space container, vector<Box> box, vector<int> num) {	// 生成复杂块
	vector<Block> blockTable = GenSimpleBlock(container, box, num);
	for (int t = 0; t < MaxTimes; t++) {
		vector<Block> newBlockTable;
		int blocknum = (int)blockTable.size();
		for (int i = 0; i < blocknum; i++) {
			Block a = blockTable[i];
			for (int j = 0; j < blocknum; j++) {
				if (i == j) 
					continue;
				
				Block b = blockTable[i];
				int boxnum = (int)num.size();
				int flag = 1;
				for (int k = 0; k < boxnum; k++) {
					if (a.require[k] + b.require[k] > num[k]) {
						flag = 0;
						break;
					}
				}
				if (flag == 0)
					continue;

				if (a.times == t || b.times == t) {
					if (a.lx + b.lx <= container.lx) {	// x方向
						Block c;
						c.lx = a.lx + b.lx;
						c.ly = max(a.ly, b.ly);
						c.lz = max(a.lz, b.lz);
						c.volumn = a.volumn + b.volumn;
						if (c.volumn / (c.lx * c.ly * c.lz) >= MinFillRate) {
							c.childs.push_back(a);
							c.childs.push_back(b);
							c.times = max(a.times, b.times) + 1;
							for (int k = 0; k < boxnum; k++) {
								c.require.push_back(a.require[k] + b.require[k]);
							}
							newBlockTable.push_back(c);
						}
					}
					if (a.ly + b.ly <= container.ly) {	// y方向
						Block c;
						c.ly = a.ly + b.ly;
						c.lx = max(a.lx, b.lx);
						c.lz = max(a.lz, b.lz);
						c.volumn = a.volumn + b.volumn;
						if (c.volumn / (c.lx * c.ly * c.lz) >= MinFillRate) {
							c.childs.push_back(a);
							c.childs.push_back(b);
							c.times = max(a.times, b.times) + 1;
							for (int k = 0; k < boxnum; k++) {
								c.require.push_back(a.require[k] + b.require[k]);
							}
							newBlockTable.push_back(c);
						}
					}
					if (a.ly + b.ly <= container.ly) {	// z方向
						Block c;
						c.lz = a.lz + b.lz;
						c.lx = max(a.lx, b.lx);
						c.ly = max(a.ly, b.ly);
						c.volumn = a.volumn + b.volumn;
						if (c.volumn / (c.lx * c.ly * c.lz) >= MinFillRate) {
							c.childs.push_back(a);
							c.childs.push_back(b);
							c.times = max(a.times, b.times) + 1;
							for (int k = 0; k < boxnum; k++) {
								c.require.push_back(a.require[k] + b.require[k]);
							}
							newBlockTable.push_back(c);
						}
					}
				}
			}
		}
		blockTable.insert(blockTable.end(), newBlockTable.begin(), newBlockTable.end());
		sort(blockTable.begin(), blockTable.end(), BlockCmp);
		blockTable.erase(unique(blockTable.begin(), blockTable.end(), BlockEqual), blockTable.end());	// 去除重复块
		if (blockTable.size() >= MaxBlocks) 
			break;
	}
	return blockTable;
}

vector<Block> GenBlocklist(Space space, vector<int> avail) {
	vector<Block> blockList;
	for (Block block : BlockTable) {
		int boxnum = (int)avail.size();
		int flag = 1;
		for (int i = 0; i < boxnum; i++) {
			if (block.require[i] > avail[i]) {
				flag = 0;
				break;
			}
		}
		if (flag == 0)
			continue;

		if (block.lx <= space.lx && block.ly <= space.ly && block.lz <= space.lz)
			blockList.push_back(block);
		if (blockList.size() >= MaxBlocks)
			break;
	}
	return blockList;
}

static Space GenSpace(int x, int y, int z, int lx, int ly, int lz) {
	Space space;
	space.x = x;
	space.y = y;
	space.z = z;
	space.lx = lx;
	space.ly = ly;
	space.lz = lz;
	return space;
}

vector<Space> GenResidualSpace(Space space, Block block) {
	int mx = space.lx - block.lx;
	int my = space.ly - block.ly;
	int mz = space.lz - block.lz;
	vector<Space> ret;
	Space X, Y, Z;
	if (my >= mx && mx >= mz) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, block.ly, space.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, space.lx, my, space.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, block.lx, block.ly, mz);
		ret.push_back(Z);
		ret.push_back(X);
		ret.push_back(Y);
	} else if (mx >= my && my >= mz) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, space.ly, space.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, block.lx, my, space.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, block.lx, block.ly, mz);
		ret.push_back(Z);
		ret.push_back(Y);
		ret.push_back(X);	
	} else if (my >= mz && mz >= mx) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, block.ly, block.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, space.lx, my, space.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, space.lx, block.ly, mz);
		ret.push_back(X);
		ret.push_back(Z);
		ret.push_back(Y);		
	} else if (mz >= my && my >= mx) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, block.ly, block.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, space.lx, my, block.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, space.lx, space.ly, mz);
		ret.push_back(X);
		ret.push_back(Y);
		ret.push_back(Z);	
	} else if (mx >= mz && mz >= my) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, space.ly, space.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, block.lx, my, block.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, block.lx, space.ly, mz);
		ret.push_back(Y);
		ret.push_back(Z);
		ret.push_back(X);
	} else if (mz >= mx && mx >= my) {
		X = GenSpace(space.x + block.lx, space.y, space.z, mx, space.ly, block.lz);
		Y = GenSpace(space.x, space.y + block.ly, space.z, block.lx, my, block.lz);
		Z = GenSpace(space.x, space.y, space.z + block.lz, space.lx, space.ly, mz);
		ret.push_back(Y);
		ret.push_back(X);
		ret.push_back(Z);	
	}
	return ret;
}

Block FindNextBlock(PakingState ps, vector<Block> blockList) {
	int bestFitness = 0;
	Block bestBlock = blockList[0];
	for (Block block : blockList) {
		Space space = ps.spaceStack.top();
		PlaceBlock(&ps, block);
		block.fitness = Estimate(ps);
		RemoveBlock(&ps, space, block);
		if (block.fitness > bestFitness) {
			bestFitness = block.fitness;
			bestBlock = block;
		}
	}
	return bestBlock;
}

int Estimate(PakingState ps) {
	best.volumnComplete = 0;
	DepthFirstSearch(ps, 0);
	return best.volumnComplete;
}

void PlaceBlock(PakingState *ps, Block block) {
	Space space = ps->spaceStack.top();
	ps->spaceStack.pop();
	int boxnum = (int)ps->avail.size();
	for (int i = 0; i < boxnum; i++) {
		ps->avail[i] -= block.require[i];
	}
	Place place;
	place.block = block;
	place.space = space;
	ps->plan.push_back(place);
	ps->volumn += block.volumn;
	vector<Space> vs = GenResidualSpace(space, block);
	ps->spaceStack.push(vs[0]);
	ps->spaceStack.push(vs[1]);
	ps->spaceStack.push(vs[2]);
}

void RemoveBlock(PakingState *ps, Space space, Block block) {
	int boxnum = (int)ps->avail.size();
	for (int i = 0; i < boxnum; i++) {
		ps->avail[i] += block.require[i];
	}
	ps->plan.pop_back();
	ps->volumn -= block.volumn;
	ps->spaceStack.pop();
	ps->spaceStack.pop();
	ps->spaceStack.pop();
	ps->spaceStack.push(space);
}

void Complete(PakingState *ps) {
	PakingState tmp = *ps;
	while (!tmp.spaceStack.empty()) {
		Space space = tmp.spaceStack.top();
		vector<Block> blockList = GenBlocklist(space, tmp.avail);
		if (!blockList.empty()) {
			PlaceBlock(&tmp, blockList[0]);
		}
		else {
			tmp.spaceStack.pop();
		}
	}
	ps->volumnComplete = tmp.volumn;
}

void DepthFirstSearch(PakingState ps, int depth) {
	if (depth != DEPTH) {
		if (ps.spaceStack.empty())
			return;
		Space space = ps.spaceStack.top();
		vector<Block> blockList = GenBlocklist(space, ps.avail);
		if (!blockList.empty()) {
			for (int i = 0; i < min((int)blockList.size(), BRANCH); i++) {
				PlaceBlock(&ps, blockList[i]);
				DepthFirstSearch(ps, depth + 1);
				RemoveBlock(&ps, space, blockList[i]);
			}
		}
		else {
			ps.spaceStack.pop();
			DepthFirstSearch(ps, depth);
			ps.spaceStack.push(space);
		}
	}
	else {
		Complete(&ps);
		if (ps.volumnComplete > best.volumnComplete) {
			best = ps;
		}
	}
}

PakingState BasicHeuristic(Problem problem) {
	BlockTable = GenComplexBlock(problem.container, problem.box, problem.num);
	PakingState ps;
	ps.avail = problem.num;
	ps.volumn = 0;
	ps.spaceStack.push(problem.container);
	while(!ps.spaceStack.empty()) {
		Space space = ps.spaceStack.top();
		vector<Block> blockList = GenBlocklist(space, ps.avail);
		if (!blockList.empty()) {
			Block block = FindNextBlock(ps, blockList);
			PlaceBlock(&ps, block);
			// printf("%d\n", ps.volumn);
		}
		else {
			ps.spaceStack.pop();
		}
	}
	return ps;
}
```
#### main.cpp
```cpp
#include<iostream>
#include"packing.h"
#include<Windows.h>

using namespace std;

int main() {
	Space container = Space(587, 233, 220);
	vector<Box> box;
	vector<int> num;
	Problem problem;
	PakingState ps;
	LARGE_INTEGER freq;
	LARGE_INTEGER beginTime;
	LARGE_INTEGER endTime;

	QueryPerformanceFrequency(&freq);

	cout << "3种箱子:\n";
	box = { Box(108, 76, 30, 0), Box(110, 43, 25, 1), Box(92, 81, 55, 2) };
	num = { 40, 33, 39 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps =  BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E1-1   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(91, 54, 45, 0), Box(105, 77, 72, 1), Box(79, 78, 48, 2) };
	num = { 32, 24, 30 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E1-2   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(91, 54, 45, 0), Box(105, 77, 72, 1), Box(79, 78, 48, 2) };
	num = { 32, 24, 30 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E1-3   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(60, 40, 32, 0), Box(98, 75, 55, 1), Box(60, 59, 39, 2) };
	num = { 64, 40, 64 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E1-4   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(78, 37, 27, 0), Box(89, 70, 25, 1), Box(90, 84, 41, 2) };
	num = { 63, 52, 55 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E1-5   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	cout << "5种箱子:\n";
	box = { Box(108, 76, 30, 0), Box(110, 43, 25, 1), Box(92, 81, 55, 2), Box(81, 33, 28, 3), Box(120, 99, 73, 4) };
	num = { 24, 7, 22, 13, 15 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E2-1   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(49, 25, 21, 0), Box(60, 51, 41, 1), Box(103, 76, 64, 2), Box(95, 70, 62, 3), Box(111, 49, 26, 4) };
	num = { 22, 22, 28, 25, 17 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E2-2   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(88, 54, 39, 0), Box(94, 54, 36, 1), Box(87, 77, 43, 2), Box(100, 80, 72, 3), Box(83, 40, 36, 4) };
	num = { 25, 27, 21, 20, 24 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E2-3   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(90, 70, 63, 0), Box(84, 78, 28, 1), Box(94, 85, 39, 2), Box(80, 76, 54, 3), Box(69, 50, 45, 4) };
	num = { 16, 28, 20, 23, 31 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E2-4   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(74, 63, 61, 0), Box(71, 60, 25, 1), Box(106, 80, 59, 2), Box(109, 76, 42, 3), Box(118, 56, 22, 4) };
	num = { 22, 12, 25, 24, 11 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E2-5   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	cout << "8种箱子:\n";
	box = { Box(108, 76, 30, 0), Box(110, 43, 25, 1), Box(92, 81, 55, 2), Box(81, 33, 28, 3),
		Box(120, 99, 73, 4), Box(111, 70, 48, 5), Box(98, 72, 46, 6), Box(95, 66, 31, 7) };
	num = { 24, 9, 8, 11, 11, 10, 12, 9 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E3-1   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(97, 81, 27, 0), Box(102, 78, 39, 1), Box(113, 46, 36, 2), Box(66, 50, 42, 3),
		Box(101, 30, 26, 4), Box(100, 56, 35, 5), Box(91, 50, 40, 6), Box(106, 61, 56, 7) };
	num = { 10, 20, 18, 21, 16, 17, 22, 19 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E3-2   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(88, 54, 39, 0), Box(94, 54, 36, 1), Box(87, 77, 43, 2), Box(100, 80, 72, 3),
		Box(83, 40, 36, 4), Box(91, 54, 22, 5), Box(109, 58, 54, 6), Box(94, 55, 30, 7) };
	num = { 16, 14, 20, 16, 6, 15, 17, 9 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E3-3   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(49, 25, 21, 0), Box(60, 51, 41, 1), Box(103, 76, 64, 2), Box(95, 70, 62, 3),
		Box(111, 49, 26, 4), Box(85, 84, 72, 5), Box(48, 36, 31, 6), Box(86, 76, 38, 7) };
	num = { 16, 8, 16, 18, 18, 16, 17, 6 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E3-4   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(113, 92, 33, 0), Box(52, 37, 28, 1), Box(57, 33, 29, 2), Box(99, 37, 30, 3),
		Box(92, 64, 33, 4), Box(119, 59, 39, 5), Box(54, 52, 49, 6), Box(75, 45, 35, 7) };
	num = { 23, 22, 26, 17, 23, 26, 18, 30 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E3-5   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	cout << "10种箱子:\n";
	box = { Box(49, 25, 21, 0), Box(60, 51, 41, 1), Box(103, 76, 64, 2), Box(95, 70, 62, 3), Box(111, 49, 26, 4),
		Box(85, 84, 72, 5), Box(48, 36, 31, 6), Box(86, 76, 38, 7), Box(71, 48, 47, 8), Box(90, 43, 33, 9) };
	num = { 13, 9, 11, 14, 13, 16, 12, 11, 16, 8 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E4-1   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(97, 81, 27, 0), Box(102, 78, 39, 1), Box(113, 46, 36, 2), Box(66, 50, 42, 3), Box(101, 30, 26, 4),
		Box(100, 56, 35, 5), Box(91, 50, 40, 6), Box(106, 61, 56, 7), Box(103, 63, 58, 8), Box(75, 57, 41, 9) };
	num = { 8, 16, 12, 12, 18, 13, 14, 17, 12, 13 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E4-2   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(86, 84, 45, 0), Box(81, 45, 34, 1), Box(70, 54, 37, 2), Box(71, 61, 52, 3), Box(78, 73, 40, 4),
		Box(69, 63, 46, 5), Box(72, 67, 56, 6), Box(75, 75, 36, 7), Box(94, 88, 50, 8), Box(65, 51, 50, 9) };
	num = { 18, 19, 13, 16, 10, 13, 10, 8, 12, 13 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E4-3   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(113, 92, 33, 0), Box(52, 37, 28, 1), Box(57, 33, 29, 2), Box(99, 37, 30, 3), Box(92, 64, 33, 4),
		Box(119, 59, 39, 5), Box(54, 52, 49, 6), Box(75, 45, 35, 7), Box(79, 68, 44, 8), Box(116, 49, 47, 9) };
	num = { 15, 17, 17, 19, 13, 19, 13, 21, 13, 22 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E4-4   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(118, 79, 51, 0), Box(86, 32, 31, 1), Box(64, 58, 52, 2), Box(42, 42, 32, 3), Box(64, 55, 43, 4),
		Box(84, 70, 35, 5), Box(76, 57, 36, 6), Box(95, 60, 55, 7), Box(80, 66, 52, 8), Box(109, 73, 23, 9) };
	num = { 16, 8, 14, 14, 16, 10, 14, 14, 14, 18 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E4-5   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	cout << "15种箱子:\n";
	box = { Box(98, 73, 44, 0), Box(60, 60, 38, 1), Box(105, 73, 60, 2), Box(90, 77, 52, 3), Box(66, 58, 24, 4), Box(106, 76, 55, 5), Box(55, 44, 36, 6),
		Box(82, 58, 23, 7), Box(74, 61, 58, 8), Box(81, 39, 24, 9), Box(71, 65, 39, 10), Box(105, 97, 47, 11), Box(114, 97, 69, 12), Box(103, 78, 55, 13), Box(93, 66, 55, 14) };
	num = { 6, 7, 10, 3, 5, 10, 12, 7, 6, 8, 11, 4, 5, 6, 6 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E5-1   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(108, 76, 30, 0), Box(110, 43, 25, 1), Box(92, 81, 55, 2), Box(81, 33, 28, 3), Box(120, 99, 73, 4), Box(111, 70, 48, 5), Box(98, 72, 46, 6),
		Box(95, 66, 31, 7), Box(85, 84, 30, 8), Box(71, 32, 25, 9), Box(36, 34, 25, 10), Box(97, 67, 62, 11), Box(33, 25, 23, 12), Box(95, 27, 26, 13), Box(94, 81, 44, 14) };
	num = { 12, 12, 6, 9, 5, 12, 9, 10, 8, 3, 10, 7, 7, 10, 9 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E5-2   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(49, 25, 21, 0), Box(60, 51, 41, 1), Box(103, 76, 64, 2), Box(95, 70, 62, 3), Box(111, 49, 26, 4), Box(74, 42, 40, 5), Box(85, 84, 72, 6),
		Box(48, 36, 31, 7), Box(86, 76, 38, 8), Box(71, 48, 47, 9), Box(90, 43, 33, 10), Box(98, 52, 44, 11), Box(73, 37, 23, 12), Box(61, 48, 39, 13), Box(75, 75, 63, 14) };
	num = { 13, 9, 8, 6, 10, 4, 10, 10, 12, 14, 9, 9, 10, 14, 11 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E5-3   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(97, 81, 27, 0), Box(102, 78, 39, 1), Box(113, 46, 36, 2), Box(66, 50, 42, 3), Box(101, 30, 26, 4),Box(100, 56, 35, 5), Box(91, 50, 40, 6), 
		Box(106, 61, 56, 7), Box(103, 63, 58, 8), Box(75, 57, 41, 9), Box(71, 68, 64, 10), Box(85, 67, 39, 11), Box(97, 63, 56, 12), Box(61, 48, 30, 13), Box(80, 54, 35, 14) };
	num = { 6, 6, 15, 8, 6, 7, 12, 10, 8, 11, 6, 14, 9, 11, 9 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E5-4   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	box = { Box(113, 92, 33, 0), Box(52, 37, 28, 1), Box(57, 33, 29, 2), Box(99, 37, 30, 3), Box(92, 64, 33, 4),Box(119, 59, 39, 5), Box(54, 52, 49, 6),
		Box(75, 45, 35, 7), Box(79, 68, 44, 8), Box(116, 49, 47, 9), Box(83, 44, 23, 10), Box(98, 96, 56, 11), Box(78, 72, 57, 12), Box(98, 88, 47, 13), Box(41, 33, 31, 14) };
	num = { 8, 12, 5, 12, 9, 12, 8, 6, 12, 9, 11, 10, 8, 9, 13 };
	problem = Problem(container, box, num);
	QueryPerformanceCounter(&beginTime);
	ps = BasicHeuristic(problem);
	QueryPerformanceCounter(&endTime);
	cout << "E5-5   " << (ps.volumn * 100.0) / (1.0 * container.lx * container.ly * container.lz) << "%   " << (double)(endTime.QuadPart - beginTime.QuadPart) / (double)freq.QuadPart << "s\n";

	return 0;
}
```
