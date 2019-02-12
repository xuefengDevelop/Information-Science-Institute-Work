"""
    
    this is code for clsuter relations vectors, using sklearn
    It will gives groups of your cluester, and names of relation in each cluster
    
"""
#!/usr/bin/env python -W ignore::DeprecationWarning
import json
import time
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

with open("validate.json", "r") as f:
    data = json.load(f)
with open("offshore_transE/relation2id.txt","r") as f:
    content = f.readlines()
relation_names = []
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

np_arr = np.asarray(data)
clustering = MeanShift().fit(np_arr)

labels = clustering.labels_
cluster_centers = clustering.cluster_centers_
labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
map = {}
#print("number of estimated clusters : %d" % n_clusters_)
clusters = []
for i in range(len(data)):
    number = clustering.predict(data[i])[0]
    if number in map.keys():
        map[number].append(relation_names[i])
    else:
        map[number] = [relation_names[i]]
    clusters.append(clustering.predict(data[i])[0])
print map

