'''
    Anthor: Xuefeng
    
    clean up dataset, to form JSON to easier to read and write.
    
    convert officer.cvs, Intermediaries.csv, Entities.cvs, Addresses.cvs to one big look up JSON file. Key will
    be the node_id, values will always contains where source is coming from (which document, like officer.cvs, and so on).
    key-value pairs for officers will contains values:
        * name
        * country
        * source
    key-value pairs for entites will contains values:
        * name
        * original_name
        * former_name
        * juridiction
        * address
        * country
        * service privider
        * source: entities
    key-value pairs for Intermederaies will contains values:
        * Inter_name
        * country
        * source: Intermederaies
    key-value pairs for Address will contains values:
        * address
        * country
    If in the future program changed such function, please update this table for better vislazation.
'''

import json
import csv

map = {}
with open('Officers.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row["name"]
        country = row["countries"]
        id = row["node_id"]
        map[id] = {}
        map[id]["country"] = country
        map[id]["name"] = name
        map[id]["source"] = "Officers.csv"


with open('Intermediaries.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row["name"]
        country = row["countries"]
        address = row["address"]
        id = row["node_id"]
        map[id] = {}
        map[id]["country"] = country
        map[id]["name"] = name
        map[id]["address"] = address
        map[id]["source"] = "Intermediaries.csv"

with open('Addresses.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        country = row["countries"]
        address = row["address"]
        id = row["node_id"]
        map[id] = {}
        map[id]["country"] = country
        map[id]["address"] = address
        map[id]["source"] = "Addresses.csv"

with open('Entities.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        name = row["name"]
        original_name = row["original_name"]
        former_name = row["former_name"]
        country = row["countries"]
        address = row["address"]
        service_provider = row["service_provider"]
        jurisdiction = row["jurisdiction"]
        id = row["node_id"]
        print id
        map[id] = {}
        map[id]["service_provider"] = service_provider
        map[id]["jurisdiction"] = jurisdiction
        map[id]["original_name"] = original_name
        map[id]["former_name"] = former_name
        map[id]["name"] = name
        map[id]["country"] = country
        map[id]["address"] = address
        map[id]["source"] = "Entities.csv"

with open('data.json', 'w') as outfile:
    json.dump(map, outfile)




