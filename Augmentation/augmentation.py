'''
    Step 1: count how many triples for each relation, if there are less than 3 triples. we count them as sparse relation
    Step 2: generate all the triples from edgelist, which can form a triangle. write it to a json file.
    A has list of [B, C, D, E] as neighbor, output A -> [B, C, D, E] key and value in json. Only contain entity
    
    Step 3: find all the triangle which these relation holds, and output them with their relation to a relation-entity JSON file
    
    Step 4: embeded each required triangle with a dummy node. like following example:
    A - r1 - B, B - r2 - C, C - r3 - A. this is a valid triangle, if it satisfies our condition(in this case, sparse relation), embed a dummy node
    
    
    Step 5: augmentation. A - r1 - B, B - r2 - C, C - r3 - A, it will become A - r1 - B, B - r2 - dummy, dummy - r3 - A first triangle. B - r2 - C, B - r1 - dummy, C - r3 - dummy second triangle. C - r3 - A, C - r2 - dummy, A - r1 - dummy. One triangle become three triangle. we hope such form can improve our model.
    
    
    Step 6: append results to the datasets.
    
    
    
'''

import numpy as np
import time
import json
import sys
from itertools import combinations
import os
import psutil
import ast


process = psutil.Process(os.getpid())
start_time = time.time()
dict_entity = {}
dict_relation = {}
triplet_list = []
triplet_with_relation_list = []
embedding_list = []
entity_list = []
dict_pair = {}
entity_number = []
sparse_relation = []




def get_relation_counts(input_file):
    with open('train2id.txt') as f:
        content = f.readlines()
    relation_count = []
    for i in range(1345):
        relation_count.append(0)
    for i in range(len(content)):
        if(i != 0):
            arr = content[i].split()
            head, tail, rels = int(arr[0]), int(arr[1]), int(arr[2])
            relation_count[rels] = relation_count[rels] + 1
    print relation_count
    for i in range(1345):
        if relation_count[i] <= 2:
            sparse_relation.append(i)

def read_triplets(input_file,input_file2):
    with open(input_file) as f:
        content = f.readlines()
    with open(input_file2) as f:
        entities = f.readlines()
    entity_number = int(entities[0].split()[0])
    for i in range(entity_number):
        dict_entity.setdefault(i,[])
        dict_relation.setdefault(i,[])
    for i in range(len(content)):
        if(i == 0): continue
        arr = content[i].split()
        head = int(arr[0])
        tail = int(arr[1])
        relation = int(arr[2])
        if(head not in dict_entity[tail]):
            dict_entity[tail].append(head);
        if(tail not in dict_entity[head]):
            dict_entity[head].append(tail);
        if (head < tail):
            string = str(head) + " " + str(tail) + " "+ str(relation)
            if string not in dict_relation[head]:
                dict_relation[head].append(string)
        if (head > tail):
            string = str(tail) + " " + str(head) + " " + str(relation)
            if string not in dict_relation[tail]:
                dict_relation[tail].append(string)


def find_relations(index1, index2):
    res = []
    current_list = dict_relation[index1]
    for i in range(len(current_list)):
        arr = current_list[i].split()
        if(int(arr[1]) == index2):
            res.append(current_list[i])
    return res;

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def generate_triangle_triplets(input_file):
    with open(input_file) as f:
        content = f.readlines()
    for i in range(len(content)):
        if(i%10000 == 0):
            print str(i) + (":  --- %s seconds ---" % (time.time() - start_time))
            print("current Memory usage: " + str(process.memory_full_info()[0]))
        if(i == 0): continue
        arr = content[i].split()
        n1,n2,r1 = int(arr[0]), int(arr[1]),int(arr[2])
        if(n2 < n1):
            temp = n1
            n1 = n2
            n2 = temp
        if(len(dict_entity[n1]) == 1 or len(dict_entity[n2]) == 1):
            continue
        str1 = str(n1)+ '-' + str(n2)
        if(str1 in dict_pair):
            intersect_list = dict_pair[str1]
        else:
            intersect_list = intersection(dict_entity[n1], dict_entity[n2])
            dict_pair.setdefault(str1,intersect_list)
        if len(intersect_list) == 0:
            continue
        else:
            for i in range(len(intersect_list)):
                list = [n1,n2,intersect_list[i]]
                list.sort()
                string = str(list[0]) + ' ' + str(list[1]) + ' ' + str(list[2])
                if string not in triplet_list:
                    triplet_list.append(string)
    with open('triangle_list.json', 'w') as outfile:
        json.dump(triplet_list, outfile)


def get_relation_triangle():
    for i in range(len(triplet_list)):
        print str(i),
        print("get Triplets:  --- %s seconds ---" % (time.time() - start_time))
        print("current Memory usage: " + str(process.memory_full_info()[0]))
        arr = triplet_list[i].split()
        list1 = find_relations(int(arr[0]), int(arr[1]))
        list2 = find_relations(int(arr[0]), int(arr[2]))
        list3 = find_relations(int(arr[1]), int(arr[2]))
        for i in range(len(list1)):
            for j in range(len(list2)):
                for k in range(len(list3)):
                    string = list1[i] + ' ' + list2[j] + ' ' + list3[k]
                    triplet_with_relation_list.append(string)
    with open('triangle_list_relation.json', 'w') as outfile:
        json.dump(triplet_with_relation_list, outfile)



def embedding_nodes(input):
    with open('triangle_list_relation.json', 'r') as f:
        triplet_with_relation_list = ast.literal_eval(f.read())
    print "total triangle: ", len(triplet_with_relation_list)
    with open(input) as f:
        entities = f.readlines()
    entity_number = int(entities[0].split()[0])
    relation_constraint = {}
    for i in range(1345):
        relation_constraint.setdefault(i,0)
    count = 0
    for i in range(len(triplet_with_relation_list)):
        arr = triplet_with_relation_list[i].split()
        n1,n2,r1,n3,n4,r2,n5,n6,r3 = int(arr[0]), int(arr[1]), int(arr[2]),int(arr[3]),int(arr[4]),int(arr[5]),int(arr[6]),int(arr[7]),int(arr[8])
        if(relation_constraint[r1] < 10 and relation_constraint[r2] < 10 and relation_constraint[r3] < 10):
            length_of_entity = entity_number
            dummy_node = length_of_entity + count
            entity_list.append("dummy" + str(dummy_node) + " " + str(dummy_node))
            string1 = str(n1) + ' ' + str(dummy_node) + ' ' + str(r2)
            string2 = str(n2) + ' ' + str(dummy_node) + ' ' + str(r3)
            string3 = str(n3) + ' ' + str(dummy_node) + ' ' + str(r1)
            string4 = str(n4) + ' ' + str(dummy_node) + ' ' + str(r3)
            string5 = str(n5) + ' ' + str(dummy_node) + ' ' + str(r1)
            string6 = str(n6) + ' ' + str(dummy_node) + ' ' + str(r2)
            if(string1 not in embedding_list):
                embedding_list.append(string1)
            if(string2 not in embedding_list):
                embedding_list.append(string2)
            if(string3 not in embedding_list):
                embedding_list.append(string3)
            if(string4 not in embedding_list):
                embedding_list.append(string4)
            if(string5 not in embedding_list):
                embedding_list.append(string5)
            if(string6 not in embedding_list):
                embedding_list.append(string6)
            count = count + 1
            relation_constraint[r1] = relation_constraint[r1] + 1
            relation_constraint[r2] = relation_constraint[r2] + 1
            relation_constraint[r3] = relation_constraint[r3] + 1

def write_to_file(file1,file2):
    print "embedding %s nodes:  "%(len(entity_list))
    print "embedding %s relations:  "%(len(embedding_list))
    print(" --- %s seconds ---" % (time.time() - start_time))
    print ("------------------------------------------")
    with open(file1) as f:
        content = f.readlines()
    with open(file2) as f:
        content2 = f.readlines()
    for i in range(len(entity_list)):
        content2.append(entity_list[i]+ '\n')
    content2[0] = str(len(content2) -1) + '\n'
    for i in range(len(embedding_list)):
        content.append(embedding_list[i] + '\n')
    content[0] = str(len(content) -1) + '\n'
    file1 = open(file1,"w")
    file2 = open(file2,"w")
    for i in range(len(content)):
        file1.write(content[i])
    for i in range(len(content2)):
        file2.write(content2[i])
    file1.close()
    file2.close()
'''
#get_relation_counts(sys.argv[1])
read_triplets(sys.argv[1],sys.argv[2])
print("finish reading--- %s seconds ---" % (time.time() - start_time))
print("current Memory usage: " + str(process.memory_full_info()[0]))
generate_triangle_triplets(sys.argv[1])
print("finish get triangle triplets--- %s seconds ---" % (time.time() - start_time))
get_relation_triangle()
print("finish get triplets--- %s seconds ---" % (time.time() - start_time))
#get_relation_counts(sys.argv[1])
'''
embedding_nodes(sys.argv[2])
print("current Memory usage: " + str(process.memory_full_info()[0]))
write_to_file(sys.argv[1],sys.argv[2])
print("final--- %s seconds ---" % (time.time() - start_time))

