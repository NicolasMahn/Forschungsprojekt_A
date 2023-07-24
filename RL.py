import numpy as np
import math
import matplotlib.pyplot as plt

num_jobs = 5
num_actions = num_jobs
Q = np.zeros((num_jobs, num_actions))

jobs = [15, 10, 6, 20, 12]

learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.5
min_epsilon = 0.1
epsilon_decay = 0.85

num_episodes = 500


def argmax(elements):
    # print(f"elements: {elements}")
    best_elements = argmax_multi(elements)
    return best_elements[np.random.randint(0, len(best_elements))]


def argmax_multi(elements):
    max_element = np.max(elements)
    # print(f"max_element: {max_element}")
    if math.isnan(max_element):
        raise ValueError("NaN in argmax_multi")
    best_elements = [i for i in range(len(elements)) if elements[i] == max_element]
    return best_elements


def calculate_reward(history):
    if len(history) == 1:
        if history[0] == min(jobs):
            return 1
        else:
            return -1
    else:
        if history[-1] > history[-2]:
            return 1
        else:
            return -1


def show_fitness_curve(data, title="Fitness Curve", subtitle="", x_label="episodes", y_label="return"):
    plt.suptitle(title, fontsize=18) # title
    plt.title(subtitle, fontsize=10) # subtitle
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot([data[i] for i in range(0, len(data))], color="#008855", linewidth=3)
    plt.show()


def get_possible_actions(job_list, history_list):
    return list(set(job_list) - set(history_list))


data_fitness_curve = []

for episode in range(num_episodes):
    history = []
    sum_rewards = 0
    for state in range(num_jobs):
        possible_actions = get_possible_actions(jobs, history)
        if np.random.random() > epsilon:
            Q_state_temp = list(Q[state])
            while True:
                action_index = argmax(Q_state_temp)
                action = jobs[action_index]
                if action in possible_actions:
                    break
                else:
                    Q_state_temp[action_index] = -1000
        else:
            action = possible_actions[np.random.randint(0, len(possible_actions))]
            action_index = jobs.index(action)
        history.append(action)

        reward = calculate_reward(history)
        sum_rewards += reward

        try:
            Q[state, action_index] += learning_rate * (reward + discount_factor * np.max(Q[state + 1]) - Q[state, action_index])
        except Exception:
            None


    print("History: ", history)
    epsilon = max(min_epsilon, epsilon * epsilon_decay)
    data_fitness_curve.append(sum_rewards)


show_fitness_curve(data_fitness_curve)

print("Optimales Ergebnis: ")
history_final = []
for state in range(num_jobs):
    possible_actions = get_possible_actions(jobs, history_final)
    Q_state_temp = Q[state]
    while True:
        temp = argmax(Q_state_temp)
        action = jobs[temp]
        if action in possible_actions:
            break
        else:
            Q_state_temp[temp] = -1000

    history_final.append(action)

print("History: ", history_final)
print("Q-Table: ", Q)