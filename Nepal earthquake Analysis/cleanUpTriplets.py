'''
    
    Knowledge graph contains relations and entites. After spliting dataset, it is very possible to have some entities and relations which only occurs in the test set, not in the traning set.
    
    We have remove all of these invalid cases to get accurate result.

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

with open('train2id.txt') as f:
    train = f.readlines()
with open('valid2id.txt') as f:
    valid = f.readlines()
with open('test2id.txt') as f:
    test = f.readlines()

print "length of train:" + str(len(train))
print "length of valid:" + str(len(valid))
print "length of test:" + str(len(test))

train_set = []
for i in range(len(train)):
    if i == 0: continue
    arr = train[i].split()
    train_set.append(int(arr[0]))
    train_set.append(int(arr[1]))

valid_set = []
result_set = []
for i in range(len(valid)):
    if i == 0: continue
    arr = valid[i].split()
    if(int(arr[0]) in train_set and int(arr[1]) in train_set):
        valid_set.append(valid[i])
    else:
        if(int(arr[1]) not in result_set):
            result_set.append(int(arr[1]))

test_set = []
for i in range(len(test)):
    if i == 0: continue
    arr = test[i].split()
    if(int(arr[0]) in train_set and int(arr[1]) in train_set):
        test_set.append(test[i])
    else:
        if(int(arr[1]) not in result_set):
            result_set.append(int(arr[1]))


print "length of train_set:" + str(len(train_set))
print "length of valid_set:" + str(len(valid_set))
print "length of test_set:" + str(len(test_set))
print "length of result:" + str(len(result_set))


f = open('test2id.txt', 'w')
for i in range(len(test_set)):
    if i == 0:
        f.write(str(len(test_set)) + '\n')
    f.write(test_set[i])
f.close()

f = open('valid2id.txt', 'w')
for i in range(len(valid_set)):
    if i == 0:
        f.write(str(len(valid_set)) + '\n')
    f.write(valid_set[i])
f.close()
