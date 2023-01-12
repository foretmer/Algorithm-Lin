# container_size: A vector of length 3 describing the size of the container in the x, y, z dimension.
# item_size_set:  A list records the size of each item. The size of each item is also described by a vector of length 3.
import numpy as np
from random import uniform

container_size = [10,10,10]

lower = 1
higher = 5
resolution = 1
item_size_set = []
for i in range(lower, higher + 1):
    for j in range(lower, higher + 1):
        for k in range(lower, higher + 1):
                item_size_set.append((i * resolution, j * resolution , k *  resolution))

                
# N = 3000
# for i in range(1,N):
#     x = uniform(0.1, 0.5)
#     y = uniform(0.1, 0.5)
#     z = uniform(0.1, 0.5)
#     item_size_set.append((round(x,3),round(y,3),round(z,3)))
        

# If you want to sample item sizes from a uniform distribution in continuous domain,
# type --sample-from-distribution in your command line.s