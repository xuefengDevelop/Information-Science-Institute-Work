'''
    example command: python randomwalk.py 0 100 200 text.edgelist transE_fb15k_with_valid.edgelist
    first parameter: 0/1 -> directed/undirected
    second parameter: maximum number of times a node can be visited
    third parameter: depth of each walk
    fourth parameter: store result place
    fifth parameter: which dataset you want to walk
'''

import time
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import sys
import os
import random
import copy
import sets
random.seed(3000)
sys.setrecursionlimit(10000000)
start_time = time.time()
def start_random_walk(node_count, max_depth, current_depth, arr_visited_arr_count, graph, set, current_index, path, valid_set,f):
    # pick a random node which has some neiborgh and arr_visited is less than the maximum visited.
    # otherwise return,
    # go to set of neighbors and ramdomly visit node, recursively visited other nodes
    # if nothing in the flag, return. otherise find next good node.
    if(len(graph[current_index]) == 0 or current_depth >= max_depth):
        f.write(path + '\n')
        return False
    next_index = random.choice(graph[current_index])
    start_random_walk(node_count, max_depth, current_depth + 1, arr_visited_arr_count, graph, set, next_index, path + " " + str(set[next_index]), valid_set,f)

def randomwalk(flag_direct, node_visit_count, max_depth, file_name, input_file):
    with open(input_file) as f:
        content = f.readlines()
    edgelist_arr = []
    set = []
    for i in range(len(content)):
        head,tail = content[i].split()[0], content[i].split()[1]
        if(head not in set):
            set.append(head)
        if(tail not in set):
            set.append(tail)
        # find the index of head and tail
        head_index = set.index(head)
        tail_index = set.index(tail)
        edgelist_arr.append([head_index, tail_index])
    graph_arr = []
    visited_count_arr = []
    for i in range(len(set)):
        visited_count_arr.append(0)
    for i in range(len(set)):
        graph_arr.append([])
    for i in range(len(edgelist_arr)):
        if(int(flag_direct) == 0):
            if(edgelist_arr[i][1] not in graph_arr[edgelist_arr[i][0]]):
                graph_arr[edgelist_arr[i][0]].append(edgelist_arr[i][1])
            if(edgelist_arr[i][0] not in graph_arr[edgelist_arr[i][1]]):
                graph_arr[edgelist_arr[i][1]].append(edgelist_arr[i][0])
        else:
            if(edgelist_arr[i][1] not in graph_arr[edgelist_arr[i][0]]):
                graph_arr[edgelist_arr[i][0]].append(edgelist_arr[i][1])
    valid_set = []
    for i in range(len(set)):
        valid_set.append(i)
    for i in range(len(graph_arr)):
        if(len(graph_arr[i]) == 0):
            valid_set.remove(i)
            visited_count_arr[i] = node_visit_count
    f = open('data/' + file_name, 'w')
    while(len(valid_set) != 0):
        index = random.choice(valid_set)
        visited_count_arr[index] = visited_count_arr[index] + 1
        if(visited_count_arr[index] >= node_visit_count): valid_set.remove(index)
        start_random_walk(node_visit_count,int(max_depth),0,visited_count_arr,graph_arr, set, index, str(set[index]),valid_set, f)
    f.close()
# first argement is for direct, undirect. second argments is for how many times a node can be visited, thrid argement is for depth of each walk, last one is the place where file will store
# 0 is undirect graph
# 1 is direct graph
randomwalk(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) -1, sys.argv[4],sys.argv[5])
print("final --- %s seconds ---" % (time.time() - start_time))

