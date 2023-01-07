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
