from structure import *
from drawer import *
import csv
container = Container(587, 233, 220)
file = open("test.csv", 'r', encoding='utf-8')
file.readline()
count = 56
for i in range(count):
    cargodata = file.readline()
    cargodata = cargodata.replace('\n', '')
    cargodata = cargodata.split(',')
    pos = Point(int(cargodata[1]), int(cargodata[2]), int(cargodata[3]))
    cargo = CargoType(int(cargodata[4]), int(cargodata[5]), int(cargodata[6]), 1, 1)
    newCargo = CargoPos(cargo, pos)
    container.set_cargo.append(newCargo)

file.close()
draw_reslut(container)
