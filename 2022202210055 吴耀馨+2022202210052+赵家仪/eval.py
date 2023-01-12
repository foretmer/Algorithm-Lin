import torch
from train import DQN, solution
import time
from draw import *

# create the object of DQN class
dqn = DQN()

bn_state_dict = torch.load('cnn.pth')
dqn.target_net.load_state_dict(bn_state_dict)

def random_generate():
    idx = np.random.randint(0,len(solution))
    box_list = solution[idx]
    gen_box_order = []
    while True:
        index = np.random.randint(0, len(box_list))
        box_list[index] = (box_list[index][0], box_list[index][1], box_list[index][2], box_list[index][3]-1)
        gen_box_order.append((box_list[index][0], box_list[index][1], box_list[index][2]))
        if box_list[index][3] == 0:
            box_list.pop(index)
        if len(box_list) == 0:
            break
    return gen_box_order, idx

def evaluate_draw(cargo_list):
    start = time.time()
    c_index = 0
    state = Container(L, W, H)
    while True:
        cargo = Cargo(cargo_list[c_index][0], cargo_list[c_index][1], cargo_list[c_index][2])
        action = dqn.choose_action(state, cargo)
        if(len(action)==3):
            c_index += 1
            if c_index >= len(cargo_list):
                break
            else:
                continue
        else:
            cargo.pose = action[1]
            cargo.point = action[0]
            state.update_state(cargo)

        if c_index == len(cargo_list)-1:
            break
        c_index += 1

    end = time.time()
    last_time = end - start
    print("time cost: %f s" % last_time)
    occupy = state.occupy_volume() / state.volume
    print('final occupy rate: %f'% occupy)
    draw_reslut(state)

cargo_list, idx = random_generate()
kind_num = 3
if idx == 1:
    kind_num = 5
elif idx == 2:
    kind_num = 8
elif idx == 3:
    kind_num = 10
elif idx == 4:
    kind_num = 15

print('%d kinds of cargos' % kind_num)
print('cargo list length: %d' % len(cargo_list))
print("cargo list:")
print(cargo_list)
evaluate_draw(cargo_list)

