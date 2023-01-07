# Algorithm-Lin
# 3D_Packing
## 武汉大学国家网络安全学院
### 问题描述：
物流公司在流通过程中，需要将打包完毕的箱子装入到一个货车的车厢中，为了提高物流效率，需要将车厢尽量填满，显然，车厢如果能被100%填满是最优的，但通常认为，车厢能够填满85%，可认为装箱是比较优化的。
设车厢为长方形，其长宽高分别为L，W，H；共有n个箱子，箱子也为长方形，第i个箱子的长宽高为li，wi，hi（n个箱子的体积总和是要远远大于车厢的体积），做以下假设和要求：
1. 长方形的车厢共有8个角，并设靠近驾驶室并位于下端的一个角的坐标为（0,0,0），车厢共6个面，其中长的4个面，以及靠近驾驶室的面是封闭的，只有一个面是开着的，用于工人搬运箱子；
2. 需要计算出每个箱子在车厢中的坐标，即每个箱子摆放后，其和车厢坐标为（0,0,0）的角相对应的角在车厢中的坐标，并计算车厢的填充率。
### 启发式算法：
启发式方法是人们在解决问题时所采取的一种根据经验规则来处理问题的方法。其特点是在解决问题时，利用过去的经验，选择已经行之有效的方法，而不是系统地、按照确定的步骤去寻求答案。但由于这种方法具有试错的特点，所以也有失败的可能。
启发式方法是一种非常高效的解决问题方法，对于NP完全类的组合优化问题，目前缺少一般的算法来求解，精确算法又太耗时，所以启发式算法被广泛应用到这些问题的求解中。对于装箱问题亦是如此，自从该问题被提出以来，已经有很多启发式算法应用其中。
### 算法流程
<img width="257" alt="image" src="https://user-images.githubusercontent.com/72080671/210927333-6317df6d-2419-40ed-9c4f-ecd794d65893.png">

具体代码如下：
#### 基础启发式算法
```cpp
vector<Block> GenSimpleBlock(Space container, vector<Box> box, vector<int> num) {
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
```
#### 生成可行块列表
```cpp
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
```
#### 空间切割算法
```cpp
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
```
#### 块选择算法
```cpp
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
```
### 运行结果
![IJ16EB}E679JNHPS7JOWH{9](https://user-images.githubusercontent.com/72080671/210928261-f1852476-e030-433e-a972-f88d9d261a04.png)

可以看到，总体的空间利用率保持在85-90%之间，运行速度在15种箱子的情况下也能保证在几分钟内得出结果
