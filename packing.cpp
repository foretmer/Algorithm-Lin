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