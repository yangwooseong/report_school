import numpy as np
import sys
import time
import math
import sys
from copy import copy

start_time = time.time()

# process = np.array([6, 18, 12, 10, 10, 17, 16])
# due = np.array([8, 42, 44, 24, 90, 85, 68])

process = np.array([8, 20, 18, 26, 29, 31, 24, 28, 27, 7, 5, \
              20, 39, 14, 12, 9, 31, 11, 21, 28, 36, 39])
due = np.array([423, 444, 272, 306, 290, 451, 233, 69, 283, 13, 89, \
          29, 73, 369, 263, 108, 157, 14, 176, 153, 337, 359])
TASK_N = due.shape[0]
tasks = np.arange(1, TASK_N + 1)
branch = np.zeros(process.shape[0]).astype(int)

# order by desending order of due
order = due.argsort()
due = due[order]
process = process[order]
tasks = tasks[order]

# concatenate three arrays for convenience
data = np.concatenate((tasks, process, due), axis=0).reshape(3, TASK_N)

# get the total process time
total = process.sum()

# the starting order is desending order of due
sol = np.copy(tasks).tolist()

# get the initial lower bound by
def initial_lower_bound(process, due):
    lower_bound = 0
    current_time = 0
    for i in range(TASK_N):
        lower_bound += max(current_time + process[i] - due[i], 0)
        current_time += process[i]
    print("initial_lower_bound : ", lower_bound)
    return lower_bound

# parameter
relax = 0
delay = 0
solve_count = 0
step = 1
provisional = initial_lower_bound(process, due)

# the recursive funtion for solution will return this dictionary
sol_dict = {'provisional' : provisional, 'sol' : sol}

def branch_bound(data, total, relax, solve_count, branch, sol, sol_dict, step):
    provisional = sol_dict['provisional']
    sol = sol_dict['sol']

    rest = data.shape[1]
    for i in range(rest):
        tmp_data = np.copy(data)
        tmp_total = total
        tmp_total2 = tmp_total - data[1][i]
        # relaxation problem
        tmp_relax = relax + max(tmp_total - data[2][i], 0)
        tmp_branch = np.copy(branch)
        tmp_branch[TASK_N - rest] = data[0][i]
        # delete i task
        tmp_data = np.delete(tmp_data, i, axis=1)
        step += 1
        # select i task and go deeper if provisional solution >= lower bound
        if solve_count == 0:
            # if provisional solution is bigger than lower bound, go deeper
            if(provisional >= tmp_relax):
                solve_count = 1
                branch_bound(tmp_data, tmp_total2, tmp_relax, solve_count, tmp_branch, sol, sol_dict, step)

        else:
            # if provisional solution is bigger than lower bound, go deeper
            if(provisional >= tmp_relax):
                if(tmp_data.shape[1] == 1):
                    tmp_relax_final = relax + max(tmp_total2 - data[2][i], 0)
                    tmp_branch[-1] = tmp_data[0][0]
                    if(provisional > tmp_relax_final):
                        sol_dict['provisional'] = tmp_relax_final
                        sol_dict['sol'] = list(tmp_branch.tolist())
                        print(sol_dict['provisional'])
                        print(sol_dict['sol'])
                    elif(provisional == tmp_relax_final):
                        sol_dict['sol'].append(tmp_branch.tolist())
                        print(sol_dict['provisional'])
                        print(sol_dict['sol'])
                else:
                    branch_bound(tmp_data, tmp_total2, tmp_relax, solve_count, tmp_branch, sol, sol_dict, step)
    solve_count = 0
    return step

print('searching the solution by branch and bound strategy...')
branch_bound(data, total, relax, solve_count, branch, sol, sol_dict, step)
print('searching finished!')
