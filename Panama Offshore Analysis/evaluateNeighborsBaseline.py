"""
    This is baseline method to measure how well is machine learning model is compare to this baseline method
    
    How: neighbors of a node is likely to be a top rank for any relation of such node. following are the example why we think that way:
    
    John works at USC, John is 26 years old. Entity: John, USC, 26 Relations: is year old, works at. if we wanna predict john works at, nearest neighbor will give a good result. However if we want to predict John will work at A company in the future. machine learning method will do better in such case.
    
    
    
"""
import json
import operator

with open('map.json') as f:
    map = json.load(f)
with open("sameNameAs_testTriple.txt","r") as f:
    contents = f.readlines()
index = 0
hit1right = 0
hit3right = 0
hit10right = 0
hit1left = 0
hit3left = 0
hit10left = 0

for i in contents:
    arr = i.split()
    left, right = arr[0], arr[1]
    left_neighbors = map[left].keys()
    left_map = {}
    for i in left_neighbors:
        for j in map[i].keys():
            if j == left: continue
            if j in left_map:
                left_map[j] = left_map[j] + 1
            else:
                left_map[j] = 1
    sorted_x = dict(sorted(left_map.items(), key=lambda x: x[1])[-10:]).keys()
    if right in sorted_x[-1:]:
        hit1right = hit1right + 1
    if right in sorted_x[-3:]:
        hit3right = hit3right + 1
    if right in sorted_x[-10:]:
        hit10right = hit10right + 1


    right_neighbors = map[right].keys()
    right_map = {}
    for i in right_neighbors:
        for j in map[i].keys():
            if j == right: continue
            if j in right_map:
                right_map[j] = right_map[j] + 1
            else:
                right_map[j] = 1
    sorted_x = dict(sorted(right_map.items(), key=lambda x: x[1])[-10:]).keys()
    if left in sorted_x[-1:]:
        hit1left = hit1left + 1
    if left in sorted_x[-3:]:
        hit3left = hit3left + 1
    if left in sorted_x[-10:]:
        hit10left = hit10left + 1

print float(hit1right)/float(len(contents) -1)
print float(hit3right)/float(len(contents) -1)
print float(hit10right)/ float(len(contents) -1)
print float(hit1left)/ float(len(contents) - 1)
print float(hit3left)/float(len(contents) -1)
print float(hit10left)/float(len(contents) -1)
