import numpy as np

def get_state_value(states, pos):
    if states[pos - 1].find("rew=") == 0:
        return 0
    else:
        return float(states[pos - 1])

def set_state_value(states, pos, val):
    states[pos - 1] = val
    return states

def get_state_reward(states, pos):
    if states[pos - 1].find("rew=") == 0:
        value_split = states[pos - 1].split("=")
        return int(value_split[1])
    else:
        return 0

def td_learning(states, alpha, gamma, walk):
    states = states.flatten()
    for i, state in enumerate(walk):
        if i + 1  < len(walk):
            new_val = get_state_value(states, walk[i]) + alpha * (get_state_reward(states, walk[i + 1]) + gamma * get_state_value(states, walk[i + 1]) - get_state_value(states, walk[i]))
            set_state_value(states, walk[i], round(new_val, 3))
    states = states.reshape(4, 5)
    return states

if __name__ == "__main__":
    states = np.array([
        [-0.001, -0.007, -0.027, -0.100, -0.000],
        ["rew=1", 0.271, -0.051, "rew=-1", -0.103],
        [ 0.271, 0.032, -0.023, -0.136, -0.023],
        [ 0.009, 0.002, 0.000, -0.000, -0.004]
    ])

    alpha = 0.1
    gamma = 0.9
    walk = np.array([1, 2, 3, 8, 13, 18, 19, 20, 15, 10, 9])

    states = td_learning(states, alpha, gamma, walk)
    print(states)