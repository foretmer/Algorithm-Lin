from src.utils import boxes_generator
from gym import make
from dqn import DQNAgent
import numpy as np
import tensorflow as tf

if __name__ == "__main__":
    c_size = [10, 10, 10]
    seed = 42
    b_num = 128
    env = make(
        "PackingEnv-v0",
        container_size=c_size,
        box_sizes=boxes_generator(c_size, b_num, seed),
        num_visible_boxes=1,
    )
    state_size = env.observation_space["height_map"].shape[0] * env.observation_space["height_map"].shape[1] + \
                 env.observation_space[
                     "visible_box_sizes"].shape[0] * env.observation_space["visible_box_sizes"].shape[1]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 4
    EPISODES = 1000
    scores = np.zeros(EPISODES)
    for e in range(EPISODES):
        state = env.reset()
        state = np.concatenate((state["height_map"].flatten(), state["visible_box_sizes"].flatten()))
        state = np.reshape(state, (1, state_size))
        rewards = 0
        while True:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            rewards += reward
            if len(next_state["visible_box_sizes"]) == 0:
                next_state = np.concatenate(
                    (next_state["height_map"].flatten(), [0,0,0]))
            else:
                next_state = np.concatenate((next_state["height_map"].flatten(), next_state["visible_box_sizes"].flatten()))
            next_state = np.reshape(next_state, (1, state_size))
            agent.memorize(state, action, reward, next_state, done)
            if done:
                agent.update_target_model()
                print("episode: {}/{}, score: {}, e: {:.2}"
                      .format(e, EPISODES, rewards / (c_size[0] * c_size[1] * c_size[2]), agent.epsilon))
                scores[e] = rewards / (c_size[0] * c_size[1] * c_size[2])
                break
            state = next_state
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    np.save("scores", scores)
    agent.save("./agent")
