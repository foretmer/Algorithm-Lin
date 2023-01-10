# container_size: 容器尺寸[长，宽，高].
# item_size_set:  货物尺寸列表.

#container_size = [587, 233, 220]
container_size = [10,10,10]
lower = 1
higher = 5
resolution = 1
item_size_set = []
for i in range(lower, higher + 1):
    for j in range(lower, higher + 1): ## Changing from + 1 to + 4 for large flat boxes.
        for k in range(lower, higher + 1): ## Changing from + 1 to + 4 for large flat boxes.
                item_size_set.append((i * resolution, j * resolution , k *  resolution))
# for i in range(20):
#     item_size_set.append((2,2,2))
# for i in range(20):
#     item_size_set.append((3,3,3))



