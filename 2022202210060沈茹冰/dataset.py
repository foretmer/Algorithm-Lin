# read and save data from the file (offline and online)

# prepare offline test data
def read_data(path):
    box_list = []
    cnt = 0
    with open(path) as f:
        tls = [l.strip() for l in f ]
        for tl in tls:
            cnt = 0
            box_l = []
            tid, blist = tl.split('|')
            list = "".join(blist)[2:-1]
            list = list.split(', ')
            # print(list)
            for bid in list:
                index = bid.split('(')[1].split(')')[0].split(' ')
                # print(index)
                box = {}
                box['test_id'] = tid[:-1]
                box['lx'] = index[0]
                box['ly'] = index[1]
                box['lz'] = index[2]
                box['num'] = index[3]
                box['type'] = cnt
                cnt += 1
                box_l.append(box)
            box_list.append(box_l)
 
    return box_list


# box_list = read_data('data.txt')
# print('all box numbers:', len(box_list))
# print('the first box:', box_list[0])
# print('the last box:', box_list[24])


def online_data(path):
    box_list = []
    with open(path) as f:
        tls = [l.strip() for l in f ]
        cnt = 0
        tid, blist = tls[-1].split('|')
        list = "".join(blist)[2:-1]
        list = list.split(', ')
        # print(list)
        for bid in list:
            index = bid.split('(')[1].split(')')[0].split(' ')
            # print(index)
            box = {}
            box['test_id'] = tid[:-1]
            box['lx'] = index[0]
            box['ly'] = index[1]
            box['lz'] = index[2]
            box['num'] = index[3]
            box['type'] = cnt
            cnt += 1
            box_list.append(box)
    
    return box_list


# box_list = online_data('data.txt')
# print('all box numbers:', len(box_list))
# print(box_list)
