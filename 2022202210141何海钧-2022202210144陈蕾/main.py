import sys
import torch.cuda
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time
from model import *
from tools import *
from envs import make_vec_envs
import numpy as np
import random
from train_tools import train_tools
from tensorboardX import SummaryWriter
from tools import get_args, registration_envs

def main(args):
    
    # 输入实验名称，如1-1，实验结果数据以此名称保存到'.\logs\experiment' and '.\logs\runs'
    custom = input('Please input the experiment name\n')
    timeStr = custom + '-' + time.strftime('%Y.%m.%d-%H-%M-%S', time.localtime(time.time()))

    if args.no_cuda:
        device = torch.device('cpu')
    else:
        device = torch.device('cuda', args.device)
        torch.cuda.set_device(args.device)

    torch.set_num_threads(1)
    torch.backends.cudnn.deterministic = True
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    backup(timeStr, args, None)
    log_writer_path = './logs/runs/{}'.format('PCT-' + timeStr)
    if not os.path.exists(log_writer_path):
        os.makedirs(log_writer_path)
    writer = SummaryWriter(logdir=log_writer_path)

    # 创建并行环境
    envs = make_vec_envs(args, './logs/runinfo', True)

    # 创建PCT的 actor & critic 网络
    PCT_policy =  DRL_GAT(args)
    PCT_policy =  PCT_policy.to(device)

    # 如果需要加载已训练模型
    if args.load_model:
        PCT_policy = load_policy(args.model_path, PCT_policy)
        print('Loading pre-train model', args.model_path)

    # 训练模型
    trainTool = train_tools(writer, timeStr, PCT_policy, args, custom)
    trainTool.train_n_steps(envs, args, device)

if __name__ == '__main__':
    registration_envs()
    args = get_args()
    main(args)