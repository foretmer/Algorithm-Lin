# container_size: A vector of length 3 describing the size of the container in the x, y, z dimension.
# item_size_set:  A list records the size of each item. The size of each item is also described by a vector of length 3.

container_size = [587, 233, 220]

MIN_LENGTH = 30
MAX_LENGTH = 120

MIN_WIDTH = 25
MAX_WIDTH = 100

MIN_HEIGHT = 20
MAX_HEIGHT = 75

resolution = 1

item_size_set = []
for i in range(MIN_LENGTH, MAX_LENGTH + 1):
    for j in range(MIN_WIDTH, MAX_WIDTH + 1):
        for k in range(MIN_HEIGHT, MAX_HEIGHT + 1):
                item_size_set.append((i * resolution, j * resolution , k *  resolution))

# If you want to sample item sizes from a uniform distribution in continuous domain,
# type --sample-from-distribution in your command line.
