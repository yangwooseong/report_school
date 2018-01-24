'''
Simulated Annealing法を用いて納期遅れ最小化問題を解いた。
Solved minimize problem of delays sum using Simulated Annealing algorithm.
'''
import numpy as np
import sys
import time
import matplotlib.pyplot as plt

start_time = time.time()

# process and due time for each task
process = np.array([8, 20, 18, 26, 29, 31, 24, 28, 27, 7, 5, \
              20, 39, 14, 12, 9, 31, 11, 21, 28, 36, 39])
due = np.array([423, 444, 272, 306, 290, 451, 233, 69, 283, 13, 89, \
          29, 73, 369, 263, 108, 157, 14, 176, 153, 337, 359])
N_tasks = len(process)
order = np.arange(N_tasks)

# hyper parameter
Nx =  N_tasks * (N_tasks - 1) / 2 # number of neighbor = 22 * 21 / 2
T_initial = 100 # initial temperature
beta = 0.96 # decreasing rate of temperature
alpha_loop = 0.5 # end loop if count > alpha_loop * Nx
alpha_freeze = 0.5 # end search if count > alpha_freeze * Nx

def neighbor(order, s):
    '''
    function to switch two elements of order
    =============== input ===============
    order : order of tasks. array of (N_tasks, )
    s : indices of task to change. tuple of two elements

    =============== return ==============
    order_swapped : neighbor of order. array of (N_tasks, )
    '''
    a, b = s
    order_swapped = np.copy(order)
    order_swapped[a], order_swapped[b] = order_swapped[b], order_swapped[a]

    return list(order_swapped)

def evaluate(order):
    '''
    function to evaluate sum of delays
    =============== input ===============
    process : process time of tasks. array of (N_tasks, )
    due : due time of tasks. array of (N_tasks, )

    =============== return ==============
    sum_delays : sum of delays. scalar
    '''
    sum_delays = 0
    current = 0
    for task in order:
        current += process[task]
        sum_delays += max(0, current - due[task])

    return sum_delays

def loop(order, T):
    '''
    implement simulated annealing
    =============== input ===============
    order : order of tasks. array of (N_tasks, )
    T : temperature. scalar

    =============== return ==============
    sol : order of solution. list of (number of sol)
    fx_history : history of fx corresponding to evaluation count
    eval_count : evaluation count
    '''
    move_count = 0 # increment 1 whenever order doesn't move to neighbor
    eval_count = 0 # number of evaluation
    sol = []
    fx = evaluate(order) # current promising solution
    fx_history = [fx]
    current_min = fx

    while(move_count <= alpha_freeze * Nx):
        for i in range(int(alpha_loop * Nx)):
            eval_count += 1
            order_tmp = np.copy(order)
            indices_swap = np.random.choice(N_tasks, 2, replace=False)
            order_tmp = neighbor(order_tmp, indices_swap)
            fy = evaluate(order_tmp)
            delta = fy - fx

            if delta <= 0:
                # renew promising solution
                order = order_tmp
                fx = fy
                move_count = 0
            else:
                if np.random.choice(2, 1, \
                    p=[np.exp(- delta / T), 1 - np.exp(- delta / T)]) == 0:
                    order = order_tmp
                    fx = fy
                    move_count = 0
                else:
                    move_count += 1
            # if current solution is smaller than current_min, renew the solution list
            if fx < current_min:
                sol = [order]
                current_min = fx
            # if current solution is equal to current_min, append the order to solution list
            elif fx == current_min:
                if order not in sol:
                    sol.append(order)
            fx_history.append(fx)
        T *= beta
        # print(move_count, fx)

    return sol, fx_history, eval_count


# set initial order and initial promising solution
fx_history = []
eval_count_history = []
solve_repeat = 10

for i in range(solve_repeat):
    order_initial = np.random.permutation(N_tasks)
    sol, fx, eval_count = loop(order_initial, T_initial)
    fx_history.append(min(fx))
    eval_count_history.append(eval_count)
    if (1 + i) % 5 == 0:
        print('%2d steps done' %(1 + i))

print(np.mean(fx_history), np.std(fx_history))
print(np.mean(eval_count_history))
print('spent %f time' %((time.time() - start_time) / solve_repeat))

plt.plot(fx)
plt.ylabel('f(x)')
plt.xlabel('evaluation')
plt.show()
