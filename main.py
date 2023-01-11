from binpack import Packer,Bin,Item
import time

packer = Packer()

packer.add_bin(Bin('Bin', 587.0, 233.0, 220.0))

# packer.add_item(Item('BoxA',3.0,3.0,1.0))
# packer.add_item(Item('BoxB',4.0,2.0,1.0))
# packer.add_item(Item('BoxC',4.0,4.0,0.1))


for i in range( 6):
    packer.add_item(Item('BoxA',  97.0, 81.0, 27.0))
i = 0
for i in range( 6):
    packer.add_item(Item('BoxB',102.0, 78.0, 39.0))
i = 0
for i in range(15):
    packer.add_item(Item('BoxC',113.0, 46.0, 36.0))
i = 0
for i in range( 8):
    packer.add_item(Item('BoxD', 66.0, 50.0, 42.0))
i = 0
for i in range( 6):
    packer.add_item(Item('BoxE',101.0, 30.0, 26.0))
i = 0
for i in range( 7):
    packer.add_item(Item('BoxF', 100.0, 56.0, 35.0))
i = 0
for i in range(12):
    packer.add_item(Item('BoxG', 91.0, 50.0, 40.0))
i = 0
for i in range(10):
    packer.add_item(Item('BoxH',106.0, 61.0, 56.0))
i = 0
for i in range( 8):
    packer.add_item(Item('BoxI',103.0, 63.0, 58.0))
i = 0
for i in range(11):
    packer.add_item(Item('BoxJ',  75.0, 57.0, 41.0))
i = 0
for i in range( 6):
    packer.add_item(Item('BoxK', 71.0, 68.0, 64.0))
i = 0
for i in range(14):
    packer.add_item(Item('BoxL', 85.0, 67.0, 39.0))
i = 0
for i in range( 9):
    packer.add_item(Item('BoxM', 97.0, 63.0, 56.0))
i = 0
for i in range(11):
    packer.add_item(Item('BoxN', 61.0, 48.0, 30.0))
i = 0
for i in range( 9):
    packer.add_item(Item('BoxO', 80.0, 54.0, 35.0))

start = time.time()
packer.pack()
end = time.time()


for b in packer.bins:
    print(b.string())
    sum = b.get_volume()

    items_vol = 0
    i = 1
    print("FITTED ITEMS:")
    for item in b.fitted_items:
        items_vol += item.get_volume()
        print("(",i,")",item.string())
        i += 1

    i = 1
    print("UNFITTED ITEMS:")
    for item in b.unfitted_items:
        print("(",i,")", item.string())
        i+=1
    # print(items_vol/sum)
    print("utility rate of space is {:.2f}%".format(items_vol/sum*100))
    print("used {:.2f}".format(end - start), "seconds")