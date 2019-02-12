"""
    split ont dataset randomly, current is split test2id.txt into two dataset. one for testing another one for validation.
    
    command: python split_set.py 0.5
    
    dataset will split by 50% percent. becasue seed is fixed, such experiment can replicate, and produce same machine learning result.
    
"""
import numpy as np
import sys

np.random.seed(0)
def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

def random_split_dataset(percetage):
    with open("offshore_transE/test2id.txt") as f:
        content = f.readlines()
    list = []
    print len(content)
    for i in range(len(content)):
        list.append(i)
    arr = np.asarray(list)
    perc = int(len(content)*float(percetage))
    validation = np.random.choice(arr,perc,replace=False, p= None)
    validation = validation.tolist()
    testing = Diff(arr.tolist(), validation)
    test_set = []
    validation_set = []
    for i in range(len(validation)):
        validation_set.append(content[validation[i]])
    for i in range(len(testing)):
        test_set.append(content[testing[i]])

    file = open("offshore_transE/newtest2id.txt", "w")
    file2 = open("offshore_transE/new2test2id.txt", "w")
    valid_id = []
    test_id = []
    for i in range(len(validation_set)):
        file.write(validation_set[i])
    for i in range(len(test_set)):
        file2.write(test_set[i])
    file.close()
    file2.close()
random_split_dataset(sys.argv[1])
