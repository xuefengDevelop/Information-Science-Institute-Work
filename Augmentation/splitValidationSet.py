'''
    example command: python splitValidationSet.py 0.5
    Code can change to couple parameters, as following: python splitValidationSet.py valid_neg.txt valid_neg_revised.txt test_neg_revised.txt 0.5
    set will split into X prect, to validation and test set
    
'''
import numpy as np
import sys


np.random.seed(0)
def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

def random_split_dataset(percetage):
    with open("valid_neg.txt") as f:
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
    cur_dict = {}
    for i in range(len(content)):
        arr = content[i].split()
        string = arr[0] + " " + arr[1] + " " + arr[2] + '\n'
        value = int(arr[3])
        cur_dict[string] = value
    file = open("valid_neg_revised.txt", "w")
    file2 = open("test_neg_revised.txt", "w")
    file3 = open("valid2id_revised.txt", "w")
    file4 = open("test2id_revised.txt", "w")
    valid_id = []
    test_id = []
    for i in range(len(validation_set)):
        file.write(validation_set[i])
        arr = validation_set[i].split()
        string = arr[0] + " " + arr[1] + " " + arr[2] + '\n'
        if(cur_dict[string] == 1):
            valid_id.append(string)
    for i in range(len(test_set)):
        file2.write(test_set[i])
        arr = test_set[i].split()
        string = arr[0] + " " + arr[1] + " " + arr[2] + '\n'
        if(cur_dict[string] == 1):
            test_id.append(string)
    for i in range(len(valid_id)):
        if(i == 0):
            file3.write(str(len(valid_id)))
        file3.write(valid_id[i])
    for i in range(len(test_id)):
        if(i == 0):
            file4.write(str(len(test_id)))
        file4.write(test_id[i])
    file.close()
    file2.close()
    file3.close()
    file4.close()
random_split_dataset(sys.argv[1])
