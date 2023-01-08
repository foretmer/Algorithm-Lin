from shortcuts import pack_products_into_restrictions
import time
conataner_max_sizes = {
  'depth': 587,
  'width': 233,
  'height': 220
}


with open("data.txt","r") as f:
    data = f.readlines()
experiment = 0
result = []
for experiment in range(int(len(data)/4)):
    input_boxs = []
    name = data[experiment*4].replace("\n","")[2:]
    # container = data[experiment*4+1].replace("\n","")
    boxs = data[experiment*4+2].replace("\n","")
    boxs = boxs.split("(")
    boxs.pop(0)
    for box in boxs:
        b = {}
        params = box.split(")")[0]
        params = params.split(" ")

        b['depth'] = int(params[0])
        b['width'] = int(params[1])
        b['height'] = int(params[2])
        b['quantity'] = int(params[3])
        input_boxs.append(b)

    print("Experiment: {}".format(name))
    print("Container: {}".format(conataner_max_sizes))
    print("Boxse: {}".format(input_boxs))


    start = time.perf_counter()
    fitness, scheme = pack_products_into_restrictions(
        input_boxs,
        conataner_max_sizes,
        500,
        1,
        2
    )
    end = time.perf_counter()
    result.append([name,"{:.4f}".format(fitness),"{:.2f}".format(end - start), str(scheme)])

for i in result:
    print(i[:3])

for i in result:
    print(i)
