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