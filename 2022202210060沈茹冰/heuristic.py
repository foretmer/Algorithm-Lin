from utils import *
from plot import *


# 选择平面
def select_plane(ps: PackingState):
    # 选最低的平面
    min_z = min([p.z for p in ps.plane_list])
    temp_planes = [p for p in ps.plane_list if p.z == min_z]
    if len(temp_planes) == 1:
        return temp_planes[0]
    
    # 相同高度的平面有多个的话，选择面积最小的平面
    min_area = min([p.lx * p.ly for p in temp_planes])
    temp_planes = [p for p in temp_planes if p.lx * p.ly == min_area]
    if len(temp_planes) == 1:
        return temp_planes[0]
    
    # 较狭窄的
    min_narrow = min([p.lx/p.ly if p.lx <= p.ly else p.ly/p.lx for p in temp_planes])
    new_temp_planes = []
    for p in temp_planes:
        narrow = p.lx/p.ly if p.lx <= p.ly else p.ly/p.lx
        if narrow == min_narrow:
            new_temp_planes.append(p)
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
   
   # x坐标较小
    min_x = min([p.x for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.x == min_x]
    if len(new_temp_planes) == 1:
        return new_temp_planes[0]
    
    # y坐标较小
    min_y = min([p.y for p in new_temp_planes])
    new_temp_planes = [p for p in new_temp_planes if p.y == min_y]
    return new_temp_planes[0]


# 将某平面从可用平面列表转移到备用平面列表
def disable_plane(ps: PackingState, plane: Plane):
    ps.plane_list.remove(plane)
    ps.spare_plane_list.append(plane)


# 生成块
def gen_block(init_plane: Plane, box_list, num_list, max_height, can_rotate=False):
    block_table = []
    for box in box_list:
        for nx in np.arange(num_list[box.type]) + 1:
            for ny in np.arange(num_list[box.type] / nx) + 1:
                for nz in np.arange(num_list[box.type] / nx / ny) + 1:
                    if box.lx * nx <= init_plane.lx and box.ly * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                        # 该简单块需要的立体箱子数量
                        requires = np.full_like(num_list, 0)
                        requires[box.type] = int(nx) * int(ny) * int(nz)
                        # 简单块
                        block = Block(lx=box.lx * nx, ly=box.ly * ny, lz=box.lz * nz, require_list=requires)
                        # 简单块填充体积
                        block.volume = box.lx * nx * box.ly * ny * box.lz * nz
                        block_table.append(block)
                    # if can_rotate:
                    if True:
                        # 物品朝向选择90度进行堆叠
                        if box.ly * nx <= init_plane.lx and box.lx * ny <= init_plane.ly and box.lz * nz <= max_height - init_plane.z:
                            requires = np.full_like(num_list, 0)
                            requires[box.type] = int(nx) * int(ny) * int(nz)
                            # 简单块
                            block = Block(lx=box.ly * nx, ly=box.lx * ny, lz=box.lz * nz, require_list=requires, box_rotate=True)
                            # 简单块填充体积
                            block.volume = box.ly * nx * box.lx * ny * box.lz * nz
                            block_table.append(block)
    return block_table


# 生成可行块列表
def gen_block_list(plane: Plane, avail, block_table, max_height):
    block_list = []
    for block in block_table:
        # 块中需要的箱子数量必须小于最初的待装箱的箱子数量
        # 块的尺寸必须小于放置空间尺寸
        # 块的重量必须小于可放置重量
        if (np.array(block.require_list) <= np.array(avail)).all() and block.lx <= plane.lx and block.ly <= plane.ly \
                and block.lz <= max_height - plane.z:
            block_list.append(block)
    return block_list


# 查找下一个可行块
def find_block(plane: Plane, block_list, ps: PackingState):
    # 平面的面积
    plane_area = plane.lx * plane.ly
    # 放入块后，剩余的最小面积
    min_residual_area = min([plane_area - b.lx * b.ly for b in block_list])
    # 剩余面积相同，保留最大体积的块
    candidate = [b for b in block_list if plane_area - b.lx * b.ly == min_residual_area]
    # 可用平面最大高度
    max_plane_height = min([p.z for p in ps.plane_list])
    _candidate = sorted(candidate, key=lambda x: x.volume, reverse=True)

    return _candidate[0]



# 裁切出新的剩余空间（有稳定性约束）
def gen_new_plane(plane: Plane, block: Block):
    # 块顶部的新平面
    rs_top = Plane(plane.x, plane.y, plane.z + block.lz, block.lx, block.ly)
    # 底部平面裁切
    if block.lx == plane.lx and block.ly == plane.ly:
        return rs_top, None, None
    if block.lx == plane.lx:
        return rs_top, Plane(plane.x, plane.y + block.ly, plane.z, plane.lx, plane.ly - block.ly), None
    if block.ly == plane.ly:
        return rs_top, Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, block.ly), None
    # 比较两种方式中面积较大的两个子平面，选择有最大面积子平面的生成方式
    rsa1 = Plane(plane.x, plane.y + block.ly, plane.z, plane.lx, plane.ly - block.ly)
    rsa2 = Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, block.ly)
    rsa_bigger = rsa1 if rsa1.lx * rsa1.ly >= rsa2.lx * rsa2.ly else rsa2
    rsb1 = Plane(plane.x, plane.y + block.ly, plane.z, block.lx, plane.ly - block.ly)
    rsb2 = Plane(plane.x + block.lx, plane.y, plane.z, plane.lx - block.lx, plane.ly)
    rsb_bigger = rsb1 if rsb1.lx * rsb1.ly >= rsb2.lx * rsb2.ly else rsb2
    if rsa_bigger.lx * rsa_bigger.ly >= rsb_bigger.lx * rsb_bigger.ly:
        return rs_top, rsa1, rsa2
    else:
        return rs_top, rsb1, rsb2


# 计算平面浪费面积
def plane_waste(ps: PackingState, plane: Plane, block_table, max_height):
    # 浪费面积
    waste = 0
    if plane:
        block_list = gen_block_list(plane, ps.avail_list, block_table, max_height)
        if len(block_list) > 0:
            block = find_block(plane, block_list, ps)
            waste = plane.lx * plane.ly - block.lx * block.ly
        else:
            waste = plane.lx * plane.ly
    return waste


# 判断平面是否可以放置物品
def can_place(ps: PackingState, plane: Plane, block_table, max_height):
    if plane is None:
        return False
    block_list = gen_block_list(plane, ps.avail_list, block_table, max_height)
    
    return True if len(block_list) > 0 else False


# 用块填充平面
def fill_block(ps: PackingState, plane: Plane, block: Block):
    # 更新可用箱体数目
    ps.avail_list = (np.array(ps.avail_list) - np.array(block.require_list)).tolist()
    # 更新放置计划
    place = Place(plane, block)
    ps.plan_list.append(place)
    # 更新体积利用率
    ps.volume = ps.volume + block.volume
    # 产生三个新的平面
    rs_top, rs1, rs2 = gen_new_plane(plane, block)
    # 移除裁切前的平面
    ps.plane_list.remove(plane)
    # 装入新的可用平面
    if rs_top:
        ps.plane_list.append(rs_top)
    if rs1:
        ps.plane_list.append(rs1)
    if rs2:
        ps.plane_list.append(rs2)


# 合并平面
def merge_plane(ps: PackingState, plane: Plane, block_table, max_height):
    for ns in ps.plane_list + ps.spare_plane_list:
        # 不和自己合并
        if plane == ns:
            continue
        # 找相邻平面
        is_adjacent, ms1, ms2 = plane.adjacent_with(ns)
        if is_adjacent:  # 有相邻平面 
            block_list = gen_block_list(ns, ps.avail_list, block_table, max_height)
            # 相邻平面本身能放入至少一个剩余物品
            if len(block_list) > 0:
                block = find_block(ns, block_list, ps)
                # 计算相邻平面和原平面浪费面积的总和
                ws1 = ns.lx * ns.ly - block.lx * block.ly + plane.lx * plane.ly
                # 计算合并后平面的总浪费面积
                ws2 = plane_waste(ps, ms1, block_table, max_height) + plane_waste(ps, ms2, block_table, max_height)
                # 合并后，浪费更小，则保留合并
                if ws1 > ws2:
                    # 保留平面合并
                    ps.plane_list.remove(plane)
                    if ns in ps.plane_list:
                        ps.plane_list.remove(ns)
                    else:
                        ps.spare_plane_list.remove(ns)
                    if ms1:
                        ps.plane_list.append(ms1)
                    if ms2:
                        ps.plane_list.append(ms2)
                    return
                else:
                    # 放弃平面合并，寻找其他相邻平面
                    continue
            # 相邻平面本身无法放入剩余物品
            else:
                # 合共后产生一个平面
                if ms2 is None:
                    # 能放物品，则保留平面合并
                    if can_place(ps, ms1, block_table, max_height):
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        ps.plane_list.append(ms1)
                        return
                    elif ms1.lx * ms1.ly > plane.lx * plane.ly and ms1.lx * ms1.ly > ns.lx * ns.ly:
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        # ps.spare_plane_list.append(ms1)
                        ps.plane_list.append(ms1)
                        return
                    else:
                        continue
                # 合并后产生两个平面
                else:
                    if (not can_place(ps, ms1, block_table, max_height)) and (not can_place(ps, ms2, block_table, max_height)):
                        if (ms1.lx * ms1.ly > plane.lx * plane.ly and ms1.lx * ms1.ly > ns.lx * ns.ly) or (ms2.lx * ms2.ly > plane.lx * plane.ly and ms2.lx * ms2.ly > ns.lx * ns.ly):
                            ps.plane_list.remove(plane)
                            if ns in ps.plane_list:
                                ps.plane_list.remove(ns)
                            else:
                                ps.spare_plane_list.remove(ns)
                            ps.spare_plane_list.append(ms1)
                            ps.spare_plane_list.append(ms2)
                            return
                        else:
                            continue
                    else:
                        ps.plane_list.remove(plane)
                        if ns in ps.plane_list:
                            ps.plane_list.remove(ns)
                        else:
                            ps.spare_plane_list.remove(ns)
                        if can_place(ps, ms1, block_table, max_height):
                            ps.plane_list.append(ms1)
                        else:
                            ps.spare_plane_list.append(ms1)

                        if can_place(ps, ms2, block_table, max_height):
                            ps.plane_list.append(ms2)
                        else:
                            ps.spare_plane_list.append(ms2)
                        return

    # 若对平面列表和备用平面列表搜索完毕后，最终仍没有找到可合并的平面，则将目标平面从平面列表移入备用平面列表
    disable_plane(ps, plane)



# 启发式算法
def heuristic(problem: Problem, test_id):
    # 生成块
    block_table = gen_block(problem.container, problem.box_list, problem.num_list, problem.height_limit, problem.rotate)
    # 初始化箱子状态
    ps = PackingState(avail_list=problem.num_list)
    # 开始时，剩余空间堆栈中只有车厢本身
    ps.plane_list.append(Plane(problem.container.x, problem.container.y, problem.container.z, problem.container.lx,problem.container.ly))
    max_used_high = 0
    # 循环直到所有平面使用完毕
    while ps.plane_list:
        # 选择平面
        plane = select_plane(ps)
        # 查找可用块
        block_list = gen_block_list(plane, ps.avail_list, block_table, problem.height_limit)
        if block_list:
            # 查找下一个近似最优块
            block = find_block(plane, block_list, ps)
            # 填充平面
            fill_block(ps, plane, block)
            # 更新最大使用高度
            if plane.z + block.lz > max_used_high:
                max_used_high = plane.z + block.lz
        else:
            # 合并相邻平面
            merge_plane(ps, plane, block_table, problem.height_limit)

    # 位置信息
    box_pos_info = [[] for _ in problem.num_list]
    for p in ps.plan_list:
        box_pos, box_idx = build_box_position(p.block, (p.plane.x, p.plane.y, p.plane.z), problem.box_list)
        for bp in box_pos:
            box_pos_info[box_idx].append((bp[0], bp[1], bp[2]))
    # 计算容器利用率
    used_volume = problem.container.lx * problem.container.ly * max_used_high
    used_ratio = round(float(ps.volume) * 100 / float(used_volume), 3) if used_volume > 0 else 0

    # 绘制结果图
    draw_packing_result(problem, ps, test_id)

    return ps.avail_list, used_ratio, max_used_high, box_pos_info, ps