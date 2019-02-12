'''
    Generate vectors from TFIDF, culster doucment by their vectors which produced by TFIDF. Similar context document will show up after running this program.
    
    We can retireval critical information from different message but have similar content.(information has been filtered)
    
    
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
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"

def read_json(i):
    start_time = time.time()
    text_list = []
    top_ten_neighbor = []
    #with open("data/nepal_datset_new_filter.json") as f:
    with open("data/nepal_text_after_process.json") as f:
        #with open("data/nepal_remove_duplicate.json") as f:
        data = json.load(f)
        message = data['data']
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer(use_idf= False, sublinear_tf = True)
    X = vectorizer.fit_transform([message[i]])
    text_list.append(message[i])
    #print message[i]
    #print "----------------------------------------"
    #print("before any caluculations --- %s seconds ---" % (time.time() - start_time))
    Y = vectorizer.transform(message).toarray() #this is most costly opeartion in the program
    #print("before fit_transform--- %s seconds ---" % (time.time() - start_time))
    tfidfTrain = transformer.fit_transform(Y)
    tfidfTest = transformer.fit_transform(X.toarray())
    #print("before simlarity--- %s seconds ---" % (time.time() - start_time))
    res = cosine_similarity(tfidfTest.toarray(), tfidfTrain.toarray())
    print len(res[0])
    #print("before sort--- %s seconds ---" % (time.time() - start_time))
    arr = kLargest(res[0], 1000)
    i = 10
    k = 0
    scores = []
    #print("before find 10--- %s seconds ---" % (time.time() - start_time))
    while i > 0:
        itemindex = np.where(res[0] == arr[k])
        for j in range(len(itemindex[0])):
            index = itemindex[0][j]
            if message[index] not in text_list:
                text_list.append(message[index])
                top_ten_neighbor.append(index)
                scores.append(arr[k])
                #print message[index]
                #print "----------------------------------------"
                i -= 1;
            if i == 0: break
        k += 1;
        if(k >= 1000):
            break;
    time_consume = time.time() - start_time
    print top_ten_neighbor
    return top_ten_neighbor,scores,time_consume
def main():
    path_to_json = 'll_nepal/'
    if sys.argv[1].isdigit():
        #with open("data/nepal_datset_new_filter.json") as f:
        with open("data/nepal_text_after_process.json") as f:
            #with open("data/nepal_remove_duplicate.json") as f:
            data = json.load(f)
            message = data['data']
        for i in range(len(sys.argv) - 1):
            arr, array, time_consume = read_json(int(sys.argv[i + 1]))
            json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
            with open(path_to_json + json_files[int(sys.argv[i + 1])]) as f:
                print "------------------------------------------------------------------"
                print
                print "Document ID: " + json_files[int(sys.argv[i + 1])]
                data = json.load(f)
                text = data['originalText']
                print text
                print
                print "text after filter: "
                print message[int(sys.argv[i + 1])]
                print "------------------------------------------------------------------"
            for j in range(len(array)):
                with open(path_to_json + json_files[int(arr[j])]) as f:
                    print "# " + str(j + 1) + " match"
                    print "Document ID: " + json_files[int(arr[j])]
                    print "Current Score: " + str(array[j])
                    data = json.load(f)
                    text = data['originalText']
                    print text
                    print
                    print "text after filter: "
                    print message[int(arr[j])]
                    print "------------------------------------------------------------------"
            print
            print("--- %s seconds ---" % time_consume)
            print "------------------------------------------------------------------"
    else:
        json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
        # with open("data/nepal_datset_new_filter.json") as f:
        with open("data/nepal_text_after_process.json") as f:
            data = json.load(f)
            message = data['data']
        for j in range(len(sys.argv) - 1):
            index = [i for i, s in enumerate(json_files) if sys.argv[j + 1] in s]
            arr, array, time_consume = read_json(index[0])
            with open(path_to_json + json_files[index[0]]) as f:
                print "------------------------------------------------------------------"
                print
                print "Document ID: " + json_files[index[0]]
                data = json.load(f)
                text = data['originalText']
                print text
                print
                print "text after filter: "
                print message[index[0]]
                print "------------------------------------------------------------------"
            for k in range(len(array)):
                with open(path_to_json + json_files[int(arr[k])]) as f:
                    print "# " + str(k + 1) + " match"
                    print "Document ID: " + json_files[int(arr[k])]
                    print "Current Score: " + str(array[k])
                    data = json.load(f)
                    text = data['originalText']
                    print text
                    print
                    print "text after filter: "
                    print message[int(arr[k])]
                    print "------------------------------------------------------------------"
            print
            print("--- %s seconds ---" % time_consume)
            print "------------------------------------------------------------------"
if __name__ == "__main__":
    main()

