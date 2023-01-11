import sys
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time
from model import *
from tools import get_leaf_nodes_with_factor,registration_envs,get_args,load_policy
import gym
import os
import numpy as np
import torch


def evaluate(PCT_policy, eval_envs, timeStr, args, device, eval_freq = 100, factor = 1):
    PCT_policy.eval()
    obs = eval_envs.reset()
    obs = torch.FloatTensor(obs).to(device).unsqueeze(dim=0)
    all_nodes, leaf_nodes = get_leaf_nodes_with_factor(obs, args.num_processes,
                                                             args.internal_node_holder, args.leaf_node_holder)
    batchX = torch.arange(args.num_processes)
    step_counter = 0
    episode_ratio = []
    episode_length = []
    all_episodes = []

    t1 = time.time()

    while step_counter < eval_freq:
        with torch.no_grad():
            selectedlogProb, selectedIdx, policy_dist_entropy, value = PCT_policy(all_nodes, True, normFactor = factor)
        selected_leaf_node = leaf_nodes[batchX, selectedIdx.squeeze()]
        items = eval_envs.packed
        obs, reward, done, infos = eval_envs.step(selected_leaf_node.cpu().numpy()[0][0:6])

        if done:
            print('Episode {} ends.'.format(step_counter))
            if 'ratio' in infos.keys():
                episode_ratio.append(infos['ratio'])
            if 'counter' in infos.keys():
                episode_length.append(infos['counter'])

            print('Mean ratio: {}, length: {}'.format(np.mean(episode_ratio), np.mean(episode_length)))
            print('Episode ratio: {}, length: {}'.format(infos['ratio'], infos['counter']))
            all_episodes.append(items)
            step_counter += 1
            obs = eval_envs.reset()

        obs = torch.FloatTensor(obs).to(device).unsqueeze(dim=0)
        all_nodes, leaf_nodes = get_leaf_nodes_with_factor(obs, args.num_processes,
                                                                 args.internal_node_holder, args.leaf_node_holder)
        all_nodes, leaf_nodes = all_nodes.to(device), leaf_nodes.to(device)
    
    t2 = time.time()
    cost_time = t2-t1
    result = "Evaluation using {} episodes\n" \
             "Mean ratio: {:.5f}, mean length: {:.5f}\n"\
             "Cost time: {:.5f}".format(len(episode_ratio), np.mean(episode_ratio), np.mean(episode_length),cost_time)
    print(result)
    # Save the test trajectories.
    np.save(os.path.join('./logs/evaluation', timeStr, 'trajs.npy'), all_episodes)
    # Write the test results into local file.
    file = open(os.path.join('./logs/evaluation', timeStr, 'result.txt'), 'w')
    file.write(result)
    file.close()


def main(args):
    # The name of this evaluation, related file backups and experiment tensorboard logs will
    # be saved to '.\logs\evaluation' and '.\logs\runs'
    custom = input('Please input the evaluate name\n')
    timeStr = custom + '-' + time.strftime('%Y.%m.%d-%H-%M-%S', time.localtime(time.time()))

    if args.no_cuda:
        device = torch.device('cpu')
    else:
        device = torch.device('cuda', args.device)
        torch.cuda.set_device(args.device)

    torch.cuda.set_device(args.device)
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)

    # Create single packing environment and load existing dataset.
    envs = gym.make(args.id,
                    setting = args.setting,
                    container_size=args.container_size,
                    item_set=args.item_size_set,
                    data_name=args.dataset_path,
                    load_test_data = args.load_dataset,
                    internal_node_holder=args.internal_node_holder,
                    leaf_node_holder=args.leaf_node_holder,
                    LNES = args.lnes,
                    shuffle=args.shuffle)

    # Create the main actor & critic networks of PCT
    PCT_policy =  DRL_GAT(args)
    PCT_policy =  PCT_policy.to(device)

    # Load the trained model
    if args.load_model:
        PCT_policy = load_policy(args.model_path, PCT_policy)
        print('Pre-train model loaded!', args.model_path)

    # Backup all py file
    # backup(timeStr, args, None)
    
    # Perform all evaluation.
    evaluate(PCT_policy, envs, timeStr, args, device,
             eval_freq=args.evaluation_episodes, factor=args.normFactor)

if __name__ == '__main__':
    registration_envs()
    args = get_args()
    main(args)