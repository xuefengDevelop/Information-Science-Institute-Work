'''
    classify infra for each triplets based on the matrix, which produced by machine learning algorithm.
    This classify is targeting on FB15k dataset, and very specific. However, this approach can be generalize to
    different experiment.
    
'''
import json
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
from string import punctuation
import time
import re
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.calibration import CalibratedClassifierCV
from sklearn.kernel_approximation import RBFSampler

final_average_acc = 0
final_test_size = 118142
def Classification(testSet, testLabel, trainSet, trainLabel, major, number):
    global final_average_acc
    count = 0
    list_f = []
    list_f_m = []
    if major == 1:
        for item in testLabel:
            list_f.append(1)
            list_f_m.append(0)
            if item == '1':
                count = count + 1
    else:
        for item in testLabel:
            list_f.append(0)
            list_f_m.append(1)
            if item == '0':
                count = count + 1
    LR = LogisticRegression()
    LR.fit(trainSet, trainLabel)
    pre_result = LR.predict_proba(testSet)

    threshold = [-0.9,-0.8,-0.7,-0.6,0.5,-0.4,-0.3,-0.2,-0.1,0,0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    Acc_max = 0
    maxth_Acc = 0
    maxth_0 = 0
    maxf1_0 = 0
    maxth_1 = 0
    maxf1_1 = 0
    # f_1 score on 1 --> has topic
    for index in range(0, len(threshold)):
        predict_final = []
        thre = threshold[index]
        for results in pre_result:
            if results[1] > thre:
                predict_final.append(1)
            else:
                predict_final.append(0)

        f_1 = f1_score(list(map(int, testLabel)), list(map(int, predict_final)), average=None)
        Acc = accuracy_score(list(map(int, testLabel)), list(map(int, predict_final)))
        Acc_max = max(Acc, Acc_max)
        if Acc_max == Acc:
            maxth_Acc = thre
        maxf1_0 = max(f_1[0], maxf1_0)
        if maxf1_0 == f_1[0]:
            maxth_0 = thre
        maxf1_1 = max(f_1[1], maxf1_1)
        if maxf1_1 == f_1[1]:
            maxth_1 = thre
    final_average_acc = final_average_acc + Acc_max * number
    print "---> Max Acc, ", Acc_max," threshold: ", maxth_Acc


res = []
path1 = 'data/'
path2 = 'benchmarks/FB15K/'
start_time = time.time()
with open(path1 + "directed_50_20_valid_sentence_vector.txt") as f:
    content_valid = f.readlines()
with open(path1 + "directed_50_20_test_sentence_vector.txt") as f:
    content_test = f.readlines()
with open(path2 + "valid_neg.txt") as f:
    content_valid_label = f.readlines()
with open(path2 + "test_neg.txt") as f:
    content_test_label = f.readlines()

test_label = []
train_label = []
dict_train_label = {}
dict_test_label = {}
for i in range(1345):
    dict_train_label.setdefault(i,[])
    dict_test_label.setdefault(i,[])
for i in range(len(content_valid_label)):
    arr = content_valid_label[i].split()
    if(int(arr[3]) == -1):
        train_label.append(0)
    else:
        train_label.append(1)
    dict_train_label[int(arr[2])].append(i)

for i in range(len(content_test_label)):
    arr = content_test_label[i].split()
    if(int(arr[3]) == -1):
        test_label.append(0)
    else:
        test_label.append(1)
    dict_test_label[int(arr[2])].append(i)

for index in range(1345):
    test_vectors = []
    train_vectors = []
    for i in range(len(dict_train_label[index])):
        arr = content_valid[dict_train_label[index][i]].split()
        train_vectors.append([])
        for j in range(100):
            train_vectors[i].append(float(arr[j + 3]))

    for i in range(len(dict_test_label[index])):
        arr = content_test[dict_test_label[index][i]].split()
        test_vectors.append([])
        for j in range(100):
            test_vectors[i].append(float(arr[j + 3]))
    test_label_2 = []
    train_label_2 = []
    for i in range(len(dict_train_label[index])):
        train_label_2.append(train_label[dict_train_label[index][i]])
    for i in range(len(dict_test_label[index])):
        test_label_2.append(test_label[dict_test_label[index][i]])
    print "relation " + str(index)
    if(len(dict_test_label[index]) == 0 or len(dict_train_label[index]) == 0):
        final_test_size = final_test_size - len(dict_test_label[index])
        continue
    Classification(test_vectors, test_label_2, train_vectors, train_label_2, 1, len(dict_test_label[index]))
print final_average_acc/float(final_test_size)
