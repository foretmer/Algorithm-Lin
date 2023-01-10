import level1_a_test3
data=[]

#检查第三个字符是否是E
def judgeNewSet(line):
    if(len(line)<3):
        return False
    if(line[2]=='E'):
        return True
    return False

data=[]
file = open ("3DLoad-test-dataSet.txt", "r", encoding = "UTF-8")
file = file.readlines()
for line in file:
    if(len(line)<2):
        continue
    data.append(line)
    #print (len(line),'  ',line)

print(data)
i=0
names=[]
box_sets=[]
Ls=[]
Ws=[]
Hs=[]
Ns=[]
while(i<len(data)):
    if(judgeNewSet(data[i])):
        #找到一组新数据
        name=data[i]
        names.append(name)
        #data[i+1]就是C
        #",".join(list(filter(str.isdigit, data[i+1])))
        array = data[i+1].strip('C').strip(' ').strip('\n').strip('(').strip(')').split(' ')
        Ls.append(int(array[0]))
        Ws.append(int(array[1]))
        Hs.append(int(array[2]))
        box_data=data[i+2].strip('B').replace(')，(','), (').strip(' ').strip('[').strip('').strip('\n').strip(' ').strip(']').replace('(','').replace(')','').split(',')
        print(box_data)
        a_box_set=[]
        for item in box_data:
            box_temp=item.strip(' ').split(' ')
            #print(box_temp)
            #print(box_temp)
            li=int(box_temp[0])
            wi = int(box_temp[1])
            hi = int(box_temp[2])
            #print(name)
            #print(box_temp)
            ni = int(box_temp[3])
            #生成ni个li wi hi
            for k in range(ni):
                a_box=[]
                a_box.append(li)
                a_box.append(wi)
                a_box.append(hi)
                a_box_set.append(a_box)
            #print(a_box_set[-1])
        box_sets.append(a_box_set)
        #print(a_box_set)
        #print(box_data)
        i=i+3

for i in range(0,int(len(names)/5)):
    for j in range(5):
        print('------------------------------------------')
        print('------------------------------------------')
        print(names[5*i+j])
        #L, W, H, n, boxes
        print(Ls[5*i+j],Ws[5*i+j],Hs[5*i+j],len(box_sets[5*i+j]),box_sets[5*i+j])
        level1_a_test3.main(Ls[5*i+j],Ws[5*i+j],Hs[5*i+j],len(box_sets[5*i+j]),box_sets[5*i+j],i,j,names[5*i+j].replace('//',''))



# with open('3DLoad-test-dataSet.txt', encoding='utf-8') as file:
#     for line in file:
#         content = file.readline()
#         #print(len(content))
#         data.append(content)
#         print(content)
#         #print(judgeNewSet(content))
#         #print()