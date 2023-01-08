#pragma once
#include "stdafx.h"
#include "Datastructure.h"

//using namespace std;     //在头文件里using namespace是要下地狱的

/// @brief 多个同一形状的物体
struct ItemSeries
{
	int l;
	int w;
	int h;
	int n;
	ItemSeries(int _l, int _w, int _h, int _n) : l(_l), w(_w), h(_h), n(_n)
	{

	}
};

using Group = std::vector<ItemSeries>;
using Dataset = std::pair<std::string, Group>;
using Datasets = std::vector<Dataset>;

Datasets datasets =
{
    //Dataset{"E0_0", Group{ItemSeries{587, 220, 233, 1}}}
    Dataset{"E1_1", Group{ItemSeries{108, 76, 30, 40}, ItemSeries(110, 43, 25, 33), ItemSeries(92, 81, 55, 39)}},
    Dataset{"E1_2", Group{ItemSeries{91, 54, 45, 32}, ItemSeries{105, 77, 72, 24}, ItemSeries{79, 78, 48, 30}}},
    Dataset{"E1_3", Group{ItemSeries{91, 54, 45, 32}, ItemSeries{105, 77, 72, 24}, ItemSeries{79, 78, 48, 30}}},
    Dataset{"E1_4", Group{ItemSeries{60, 40, 32, 64}, ItemSeries{98, 75, 55, 40}, ItemSeries{60, 59, 39, 64}}},
    Dataset{"E1_5", Group{ItemSeries{78, 37, 27, 63}, ItemSeries{89, 70, 25, 52}, ItemSeries{90, 84, 41, 55}}},
    Dataset{"E2_1", Group{ItemSeries{108, 76, 30, 24}, ItemSeries{110, 43, 25, 7}, ItemSeries{92, 81, 55, 22}, ItemSeries{81, 33, 28, 13}, ItemSeries{120, 99, 73, 15}}},
    Dataset{"E2_2", Group{ItemSeries{49, 25, 21, 22}, ItemSeries{60, 51, 41, 22}, ItemSeries{103, 76, 64, 28}, ItemSeries{95, 70, 62, 25}, ItemSeries{111, 49, 26, 17}}},
    Dataset{"E2_3", Group{ItemSeries{88, 54, 39, 25}, ItemSeries{94, 54, 36, 27}, ItemSeries{87, 77, 43, 21}, ItemSeries{100, 80, 72, 20}, ItemSeries{83, 40, 36, 24}}},
    Dataset{"E2_4", Group{ItemSeries{90, 70, 63, 16}, ItemSeries{84, 78, 28, 28}, ItemSeries{94, 85, 39, 20}, ItemSeries{80, 76, 54, 23}, ItemSeries{69, 50, 45, 31}}},
    Dataset{"E2_5", Group{ItemSeries{74, 63, 61, 22}, ItemSeries{71, 60, 25, 12}, ItemSeries{106, 80, 59, 25}, ItemSeries{109, 76, 42, 24}, ItemSeries{118, 56, 22, 11}}},
    Dataset{"E3_1", Group{ItemSeries{108, 76, 30, 24}, ItemSeries{110, 43, 25, 9}, ItemSeries{92, 81, 55, 8}, ItemSeries{81, 33, 28, 11}, ItemSeries{120, 99, 73, 11}, ItemSeries{111, 70, 48, 10}, ItemSeries{98, 72, 46, 12}, ItemSeries{95, 66, 31, 9}}},
    Dataset{"E3_2", Group{ItemSeries{97, 81, 27, 10}, ItemSeries{102, 78, 39, 20}, ItemSeries{113, 46, 36, 18}, ItemSeries{66, 50, 42, 21}, ItemSeries{101, 30, 26, 16}, ItemSeries{100, 56, 35, 17}, ItemSeries{91, 50, 40, 22}, ItemSeries{106, 61, 56, 19}}},
    Dataset{"E3_3", Group{ItemSeries{88, 54, 39, 16}, ItemSeries{94, 54, 36, 14}, ItemSeries{87, 77, 43, 20}, ItemSeries{100, 80, 72, 16}, ItemSeries{83, 40, 36, 6}, ItemSeries{91, 54, 22, 15}, ItemSeries{109, 58, 54, 17}, ItemSeries{94, 55, 30, 9}}},
    Dataset{"E3_4", Group{ItemSeries{49, 25, 21, 16}, ItemSeries{60, 51, 41, 8}, ItemSeries{103, 76, 64, 16}, ItemSeries{95, 70, 62, 18}, ItemSeries{111, 49, 26, 18}, ItemSeries{85, 84, 72, 16}, ItemSeries{48, 36, 31, 17}, ItemSeries{86, 76, 38, 6}}},
    Dataset{"E3_5", Group{ItemSeries{113, 92, 33, 23}, ItemSeries{52, 37, 28, 22}, ItemSeries{57, 33, 29, 26}, ItemSeries{99, 37, 30, 17}, ItemSeries{92, 64, 33, 23}, ItemSeries{119, 59, 39, 26}, ItemSeries{54, 52, 49, 18}, ItemSeries{75, 45, 35, 30}}},
    Dataset{"E4_1", Group{ItemSeries{49, 25, 21, 13}, ItemSeries{60, 51, 41, 9}, ItemSeries{103, 76, 64, 11}, ItemSeries{95, 70, 62, 14}, ItemSeries{111, 49, 26, 13}, ItemSeries{85, 84, 72, 16}, ItemSeries{48, 36, 31, 12}, ItemSeries{86, 76, 38, 11}, ItemSeries{71, 48, 47, 16}, ItemSeries{90, 43, 33, 8}}},
    Dataset{"E4_2", Group{ItemSeries{97, 81, 27, 8}, ItemSeries{102, 78, 39, 16}, ItemSeries{113, 46, 36, 12}, ItemSeries{66, 50, 42, 12}, ItemSeries{101, 30, 26, 18}, ItemSeries{100, 56, 35, 13}, ItemSeries{91, 50, 40, 14}, ItemSeries{106, 61, 56, 17}, ItemSeries{103, 63, 58, 12}, ItemSeries{75, 57, 41, 13}}},
    Dataset{"E4_3", Group{ItemSeries{86, 84, 45, 18}, ItemSeries{81, 45, 34, 19}, ItemSeries{70, 54, 37, 13}, ItemSeries{71, 61, 52, 16}, ItemSeries{78, 73, 40, 10}, ItemSeries{69, 63, 46, 13}, ItemSeries{72, 67, 56, 10}, ItemSeries{75, 75, 36, 8}, ItemSeries{94, 88, 50, 12}, ItemSeries{65, 51, 50, 13}}},
    Dataset{"E4_4", Group{ItemSeries{113, 92, 33, 15}, ItemSeries{52, 37, 28, 17}, ItemSeries{57, 33, 29, 17}, ItemSeries{99, 37, 30, 19}, ItemSeries{92, 64, 33, 13}, ItemSeries{119, 59, 39, 19}, ItemSeries{54, 52, 49, 13}, ItemSeries{75, 45, 35, 21}, ItemSeries{79, 68, 44, 13}, ItemSeries{116, 49, 47, 22}}},
    Dataset{"E4_5", Group{ItemSeries{118, 79, 51, 16}, ItemSeries{86, 32, 31, 8}, ItemSeries{64, 58, 52, 14}, ItemSeries{42, 42, 32, 14}, ItemSeries{64, 55, 43, 16}, ItemSeries{84, 70, 35, 10}, ItemSeries{76, 57, 36, 14}, ItemSeries{95, 60, 55, 14}, ItemSeries{80, 66, 52, 14}, ItemSeries{109, 73, 23, 18}}},
    Dataset{"E5_1", Group{ItemSeries{98, 73, 44, 6}, ItemSeries{60, 60, 38, 7}, ItemSeries{105, 73, 60, 10}, ItemSeries{90, 77, 52, 3}, ItemSeries{66, 58, 24, 5}, ItemSeries{106, 76, 55, 10}, ItemSeries{55, 44, 36, 12}, ItemSeries{82, 58, 23, 7}, ItemSeries{74, 61, 58, 6}, ItemSeries{81, 39, 24, 8}, ItemSeries{71, 65, 39, 11}, ItemSeries{105, 97, 47, 4}, ItemSeries{114, 97, 69, 5}, ItemSeries{103, 78, 55, 6}, ItemSeries{93, 66, 55, 6}}},
    Dataset{"E5_2", Group{ItemSeries{108, 76, 30, 12}, ItemSeries{110, 43, 25, 12}, ItemSeries{92, 81, 55, 6}, ItemSeries{81, 33, 28, 9}, ItemSeries{120, 99, 73, 5}, ItemSeries{111, 70, 48, 12}, ItemSeries{98, 72, 46, 9}, ItemSeries{95, 66, 31, 10}, ItemSeries{85, 84, 30, 8}, ItemSeries{71, 32, 25, 3}, ItemSeries{36, 34, 25, 10}, ItemSeries{97, 67, 62, 7}, ItemSeries{33, 25, 23, 7}, ItemSeries{95, 27, 26, 10}, ItemSeries{94, 81, 44, 9}}},
    Dataset{"E5_3", Group{ItemSeries{49, 25, 21, 13}, ItemSeries{60, 51, 41, 9}, ItemSeries{103, 76, 64, 8}, ItemSeries{95, 70, 62, 6}, ItemSeries{111, 49, 26, 10}, ItemSeries{74, 42, 40, 4}, ItemSeries{85, 84, 72, 10}, ItemSeries{48, 36, 31, 10}, ItemSeries{86, 76, 38, 12}, ItemSeries{71, 48, 47, 14}, ItemSeries{90, 43, 33, 9}, ItemSeries{98, 52, 44, 9}, ItemSeries{73, 37, 23, 10}, ItemSeries{61, 48, 39, 14}, ItemSeries{75, 75, 63, 11}}},
    Dataset{"E5_4", Group{ItemSeries{97, 81, 27, 6}, ItemSeries{102, 78, 39, 6}, ItemSeries{113, 46, 36, 15}, ItemSeries{66, 50, 42, 8}, ItemSeries{101, 30, 26, 6}, ItemSeries{100, 56, 35, 7}, ItemSeries{91, 50, 40, 12}, ItemSeries{106, 61, 56, 10}, ItemSeries{103, 63, 58, 8}, ItemSeries{75, 57, 41, 11}, ItemSeries{71, 68, 64, 6}, ItemSeries{85, 67, 39, 14}, ItemSeries{97, 63, 56, 9}, ItemSeries{61, 48, 30, 11}, ItemSeries{80, 54, 35, 9}}},
    Dataset{"E5_5", Group{ItemSeries{113, 92, 33, 8}, ItemSeries{52, 37, 28, 12}, ItemSeries{57, 33, 29, 5}, ItemSeries{99, 37, 30, 12}, ItemSeries{92, 64, 33, 9}, ItemSeries{119, 59, 39, 12}, ItemSeries{54, 52, 49, 8}, ItemSeries{75, 45, 35, 6}, ItemSeries{79, 68, 44, 12}, ItemSeries{116, 49, 47, 9}, ItemSeries{83, 44, 23, 11}, ItemSeries{98, 96, 56, 10}, ItemSeries{78, 72, 57, 8}, ItemSeries{98, 88, 47, 9}, ItemSeries{41, 33, 31, 13}}},
};

/// @brief 从一个group生成一个物品序列
/// @param g 
/// @return 物品序列
std::vector<Box> transform(const Group& g)
{
    std::vector<Box> r;
    for (auto& x : g)
    {
        for (int i = 0; i < x.n; ++i)
        {
            r.push_back(Box(x.l, x.w, x.h));
        }
    }
    return r;
}