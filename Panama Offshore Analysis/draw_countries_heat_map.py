"""
    
    this function is using 2D array to plot to interactive heatmap to help user to identify the behavior of data.
    
    Read data from countries dataset, which is handled by another python program. From dataset, this program will produce a heatmap. shows the pattern of serice provider and service taker's country relations(which country gives more such service and which country uses more such service.)
    
"""

import sys
import json
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import csv

reload(sys)
sys.setdefaultencoding('utf8')

def saveToCSV(unique_country, times):
    csv = open("countries.csv", "w")
    titles = "country_name"
    for i in range(len(unique_country)):
        if i != len(unique_country) -1:
            titles += "," + unique_country[i]
        else:
            titles += "," + unique_country[i] + "\n"
    csv.write(titles)
    index = 0
    for time in times:
        name = unique_country[index]
        for i in range(len(time)):
            if i != len(unique_country) -1:
                name += "," + str(time[i])
            else:
                name += "," + str(time[i]) + "\n"
        csv.write(name)
        index = index + 1



def plotHeatMap(countries, graph):
    values = np.array(graph, dtype=np.double)
    values[ values==0 ] = np.nan
    plt.imshow(values ,interpolation='nearest')
    plt.xticks(range(len(countries)), countries, rotation='vertical')
    plt.yticks(range(len(countries)), countries)
    plt.colorbar()
    plt.show()
    plt.savefig('country.png', bbox_inches='tight')
    '''
    ax = sns.heatmap(values, vmin = 0, vmax = 173148, cmap="YlGnBu", center = 1000, square=True, linewidth=0.5,interpolation = 'none')
    '''

def zero_to_nan(values):
    """Replace every 0 with 'nan' and return a copy."""
    return [float('nan') if x==0 else x for x in values]
'''
    find such triplets contains relation. output in the array form with only two egde node
'''
def find(relation):
    with open("offshore_transE/train.txt","r") as f:
        contents = f.readlines()
    list_triplets = []
    for content in contents:
        arr = content.split()
        if int(arr[2]) == relation:
            string = arr[0] + " " + arr[1]
            list_triplets.append(string)
    return list_triplets

'''
    find all the entities contries, and output list of non-duplicated country, and pair of nodes contains two
    side of countries
'''
def map_countries(list_IDs):
    with open("offshore_transE/entity2id.txt","r") as f:
        contents = f.readlines()
    with open("offshore_leaks_csvs-20170104/data.json") as f:
        data = json.load(f)
    map = {}
    for i in range(len(contents)):
        if i == 0: continue
        arr = contents[i].split()
        map[arr[1]] = arr[0]
    list_country = []
    result = []
    for entities in list_IDs:
        arr = entities.split()
        leftID = map[arr[0]]
        rightID = map[arr[1]]
        leftCountry = data[leftID]["country"]
        rightCountry = data[rightID]["country"]
        if leftCountry not in list_country:
            list_country.append(leftCountry)
        if rightCountry not in list_country:
            list_country.append(rightCountry)
        pair = (leftCountry, rightCountry)
        result.append(pair)
    return result, list_country



'''
    2d table contains occurence of the country on left countries and right countries.
    will use this 2d map to generate a head map
'''
def update(country_pair, dp, countries_list):
    totalcount = 0
    maxValue = 0
    for pair in country_pair:
        leftArr = pair[0].split(";")
        rightArr = pair[1].split(";")
        leftIndex = 0
        rightIndex = 0
        if(len(leftArr) >= 2):
            continue
        else:
            if (len(leftArr) == 0 or len(leftArr[0].encode("utf-8")) == 0):
                leftIndex = len(countries_list) -1
            else:
                leftIndex = countries_list.index(leftArr[0].encode("utf-8"))
        if(len(rightArr) >= 2):
            continue
        else:
            if (len(rightArr) == 0 or len(rightArr[0].encode("utf-8")) == 0):
                rightIndex = len(countries_list) -1
            else:
                rightIndex = countries_list.index(rightArr[0].encode("utf-8"))
        dp[leftIndex][rightIndex] = dp[leftIndex][rightIndex] + 1
        maxValue = max(maxValue, dp[leftIndex][rightIndex])
        totalcount = totalcount + 1
    print maxValue
    return dp



relation = sys.argv[1]
with open("offshore_transE/relation2id.txt","r") as f:
    content = f.readlines()
relation_id = -1
for i in range(len(content)):
    if i == 0: continue
    arr = content[i].split()
    text = ""
    for j in range(len(arr) - 1):
        if j == 0:
            text = arr[0]
        else:
            text = text + ' ' + arr[j]
    if(text == relation):
        relation_id = i -1
        break
list_IDs = find(relation_id)
country_pair, list_country = map_countries(list_IDs)
unique_country = []
for country in list_country:
    arr = country.split(";")
    for j in range(len(arr)):
        String = arr[j].encode("utf-8")
        if String not in unique_country and len(String) != 0:
            unique_country.append(String)
current_index = unique_country.index('Not identified')
temp = unique_country[len(unique_country) - 1]
unique_country[len(unique_country) - 1] = unique_country[current_index]
unique_country[current_index] = temp
times = []
for i in range(len(unique_country)):
    times.append([])
    for j in range(len(unique_country)):
        times[i].append(0)
times = update(country_pair, times,unique_country)
#print unique_country
plotHeatMap(unique_country, times)
saveToCSV(unique_country, times)

