import numpy as np
import itertools
import sys
import time
import math

start_time = time.time()

process_ex_ = np.array([8, 20, 18, 26, 29, 31, 24, 28, 27, 7, 7, \
              20, 30, 14, 12, 9, 31, 11, 21, 28, 36, 39])
# possible_ex = np.array([0, 0, 0, 14, 25, 25, 50])
due_ex_ = np.array([423, 444, 272, 306, 290, 451, 233, 69, 283, 13, 89, \
          29, 73, 369, 263, 108, 157, 14, 176, 153, 337, 359])

# sort by descending order of due time
due_order = due_ex_.argsort()
due_ex = np.array([due_ex_[i] for i in due_order])
process_ex = np.array([process_ex_[i] for i in due_order])

assert len(process_ex) == len(due_ex)
current_min = 10000
jobs = len(process_ex)

def get_max_delay(process, due, start, task2order, step):
    global current_min
    global jobs
    updated = False
    delay = {}
    end = {}
    sum_max_d = 0
    for task in range(jobs):
        end[task] = start[task] + process[task]
        delay[task] = max(0, end[task] - due[task])
        sum_max_d += delay[task]
        if current_min <= sum_max_d:
            break
    else:
        current_min = min(current_min, sum_max_d)
        print('=========================')
        print('order : ', task2order)
        print('start : ', start)
        print('process : ', process)
        print('end : ', end)
        print('due : ', due)
        print('delay : ', delay)
        print('=========================')
        print("---- %.4f seconds     ---" %(time.time() - start_time))
        print("---- %.8f %%progress  ---" %( 100 * step / math.factorial(jobs)))
        print('Min max delay : ', current_min)

process = {}
# possible = {}
due = {}
start = {} # (key, value) = (task, start time of task)
task2order = {} # (key, value) = (task, order of task)
order2task = {} # (key, value) = (order of task, task)

step = 0
for order in itertools.permutations(range(jobs)):
    current_time = 0
    for task, order_ in zip(range(jobs), order):
        process[task] = process_ex[task]
        due[task] = due_ex[task]
        # possible[task] = possible_ex[task]
        task2order[task] = order[task]
        order2task[order_] = task
    # start time of each task
    for order_ in range(jobs):
        current_task = order2task[order_]
        start[current_task] = current_time
        current_time = start[current_task] + process[current_task]
    step += 1

    get_max_delay(process, due, start, task2order, step)
