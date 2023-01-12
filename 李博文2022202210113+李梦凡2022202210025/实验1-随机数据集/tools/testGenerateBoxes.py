from box import Box
import random



def generateBoxes(n, is_integer=True):
    boxes = []
    if is_integer:
        for i in range(n):
            if random.random()<0.4:
                MIN_SIZE, MAX_SIZE = 1, 15
            elif random.random()<0.8:
                MIN_SIZE, MAX_SIZE = 15, 50
            else:
                MIN_SIZE, MAX_SIZE = 1, 50
            boxes.append(Box(random.randint(MIN_SIZE, MAX_SIZE), random.randint(MIN_SIZE, MAX_SIZE), random.randint(MIN_SIZE, MAX_SIZE)))
    else:
        for i in range(n):
            boxes.append(Box(random.random(random.random()*(MAX_SIZE - 1) + MIN_SIZE), random.random(random.random()*(MAX_SIZE - 1) + MIN_SIZE)))

    return boxes


if __name__ =='__main__':
    boxes = generateBoxes(400)
    for box in boxes:
        print(box)