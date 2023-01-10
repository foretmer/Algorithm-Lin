#pragma once

bool rectangleCross(const Box& b1, const Point& p1, const Box& b2, const Point& p2);
bool canLoad(const Box& box, const Point& target, const std::vector<std::pair<Point, Box>>& Loaded, int carriageLength, int carriageWidth, int carriageHeight);
void firstFit(std::vector<Box>& boxes, int carriageLength, int carriageWidth, int carriageHeight, bool shuffle);