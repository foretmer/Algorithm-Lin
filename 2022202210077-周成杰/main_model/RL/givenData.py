

container_size = [10,10,10]

lower = 1
higher = 5
resolution = 1
item_size_set = []
for i in range(lower, higher + 1):
    for j in range(lower, higher + 1):
        for k in range(lower, higher + 1):
                item_size_set.append((i * resolution, j * resolution , k *  resolution))

