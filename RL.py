import numpy as np
import math
import matplotlib.pyplot as plt

num_jobs = 5
num_actions = num_jobs
Q = np.zeros((num_jobs, num_actions))

jobs = [15, 10, 6, 20, 12]

learning_rate = 0.0001
discount_factor = 0.8
epsilon = 0.8
min_epsilon = 0
epsilon_decay = 0.9999

num_episodes = 100000



def calculate_average_sublist(list_of_lists):
    if not list_of_lists:
        return None

    num_sublists = len(list_of_lists)
    sublist_length = len(list_of_lists[0])

    averages = [0] * sublist_length

    for sublist in list_of_lists:
        for i in range(sublist_length):
            if len(sublist) > i:
                averages[i] += sublist[i]

    averages = [average / num_sublists for average in averages]

    return averages

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


fitness_curves = []

for execution in range(10):
    np.random.seed(execution)

    data_fitness_curve = []

    for episode in range(num_episodes):
        history_states = []
        history_actions = []
        return_ = 0
        history_actions_index = []

        for state in range(num_jobs):
            possible_actions = get_possible_actions(jobs, history_actions)
            if np.random.random() > epsilon:
                Q_state_temp = Q[state]
                action_index = argmax(Q_state_temp)
                action = jobs[action_index]
                if action not in possible_actions:
                    action = possible_actions[np.random.randint(0, len(possible_actions))]
                    action_index = jobs.index(action)
            else:
                action = possible_actions[np.random.randint(0, len(possible_actions))]
                action_index = jobs.index(action)
            history_actions.append(action)
            history_actions_index.append(action_index)
            history_states.append(state)

            reward = calculate_reward(history_actions)
            return_ += reward

        return_sum = 0
        for i in range(len(history_actions)):
            Q[history_states[i], history_actions_index[i]] += \
                learning_rate * (return_ - Q[history_states[i], history_actions_index[i]])

        #print("History: ", history_actions)
        epsilon = max(min_epsilon, epsilon * epsilon_decay)
        data_fitness_curve.append(return_)

    fitness_curves.append(data_fitness_curve)
    print(execution)


show_fitness_curve(calculate_average_sublist(fitness_curves), title="Average Fitness Curve",
                       subtitle=f"DQN average performance of {len(fitness_curves)} executions")

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


