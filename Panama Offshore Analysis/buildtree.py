"""
    
    this is a cluster of relations in the offshore dataset.
    shows relations for each realtionship, some of them have similar meanings (their matrix are very close)and they will be clustered under the same group.
    
    such clean-up can be very meaningful for data analysis, and future exploration on the large dataset.
    
"""

from anytree import Node, RenderTree
import json


class User(object):
    def __init__(self, name):
        self.name = name

with open("offshore_transE/relation2id.txt","r") as f:
    content = f.readlines()
index = 0
relation_names = []
relation_map = {}
for i in range(len(content)):
    if i == 0: continue
    arr = content[i].split()
    text = ""
    for j in range(len(arr) - 1):
        if j == 0:
            text = arr[0]
        else:
            text = text + ' ' + arr[j]
    relation_names.append(text)
    relation_map[text] = i -1


users = {}
map_names = {}
name = 'node'
root = Node("root")

level4_map = {}
with open('tree4.json') as f:
    tree4 = json.load(f)
for i in range(len(tree4)):
    currentName = name + str(index)
    users[currentName] = User(currentName)
    level4_map[currentName] = tree4[str(i)]
    users[currentName] = Node('cluster'+ str(index), parent= root)
    index = index + 1

root_map = {}
with open('tree2.json') as f:
    tree2 = json.load(f)
for i in range(len(tree2)):
    currentName = name + str(index)
    users[currentName] = User(currentName)
    current_set = set(tree2[str(i)])
    for key in level4_map.keys():
        pervious_set = set(level4_map[key])
        if current_set.issubset(pervious_set):
            parentName = key
            break
    root_map[currentName] = tree2[str(i)]
    users[currentName] = Node('cluster'+ str(index), parent= users[parentName])
    index = index + 1



with open('tree1.json') as f:
    tree1 = json.load(f)
for i in range(len(tree1)):
    currentName = name + str(index)
    users[currentName] = User(currentName)
    current_set = set(tree1[str(i)])
    for key in root_map.keys():
        pervious_set = set(root_map[key])
        if current_set.issubset(pervious_set):
            parentName = key
            break
    map_names[currentName] = tree1[str(i)]
    users[currentName] = Node('cluster'+ str(index), parent= users[parentName])
    index = index + 1



with open('tree0.json') as f:
    data = json.load(f)

newMap = {}
for i in range(len(data)):
    currentName = name + str(index)
    users[currentName] = User(currentName)
    current_set = set(data[str(i)])
    for key in map_names.keys():
        pervious_set = set(map_names[key])
        if current_set.issubset(pervious_set):
            parentName = key
            break
    newMap[currentName] = data[str(i)]
    users[currentName] = Node('cluster'+ str(index), parent= users[parentName])
    index = index + 1



for j in range(len(data)):
    parentName = name + str(j)
    for i in data[str(j)]:
        currentName = name + str(index)
        users[currentName] = User(currentName)
        current_set = set([i])
        for key in newMap.keys():
            pervious_set = set(newMap[key])
            if current_set.issubset(pervious_set):
                parentName = key
                break
        users[currentName] = Node(i, parent= users[parentName])

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name)).encode('utf-8')
