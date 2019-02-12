'''
    Author: Xuefeng
    
    Append top 10, not duplicate result from nepal dataset
    
'''

import numpy as np
import sys
import os
import json
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata
from sklearn.metrics.pairwise import cosine_similarity
import string
import time
from top_n_num import kLargest
import pandas as pd

start_time = time.time()
final_res = []
final_score = []
text_list = []
top_ten_neighbor = []
with open("data/nepal_text_after_process.json") as f:
    data = json.load(f)
    message = data['data']
index = 0
while index < 29946:
    current_list = []
    maxRange = 6000
    if(index + 6000 > 29946): maxRange = 29946 - index
    for i in range(maxRange):
        current_list.append(message[i + index])
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer(use_idf= False, sublinear_tf = True)
    X = vectorizer.fit_transform(current_list)
    Y = vectorizer.transform(message).toarray()
    tfidfTrain = transformer.fit_transform(Y)
    tfidfTest = transformer.fit_transform(X.toarray())
    res = np.dot(tfidfTest.toarray(), tfidfTrain.toarray().transpose())
    for h in range(maxRange):
        print h
        print("--- %s seconds ---" % (time.time() - start_time))
        text_list.append(message[h])
        arr = kLargest(res[h], 1000)
        i = 10
        k = 0
        scores = []
        set_score = []
        while i > 0:
            if arr[k] not in set_score:
                itemindex = np.where(res[h] == arr[k])
                set_score.append(arr[k])
                for j in range(len(itemindex[0])):
                    current_index = itemindex[0][j]
                    if message[current_index] not in text_list:
                        text_list.append(message[current_index])
                        top_ten_neighbor.append(current_index)
                        scores.append(arr[k])
                        i -= 1;
                if i == 0: break
            k += 1;
            if(k >= 1000):
                break;
        final_res.append(top_ten_neighbor)
        final_score.append(scores)
    index = index + maxRange
print len(final_res)
res = "{ \"data\":"
res += json.dumps(final_res)
res += "}"
file = open("data/top_10_from_matrix_tfidf.json", "w")
file.write(res)
file.close()
print("--- %s seconds ---" % (time.time() - start_time))
