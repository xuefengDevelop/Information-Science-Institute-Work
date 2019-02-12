'''
   use filtered information to generate data visulazation for nepal earthquake.
   
   
'''


import numpy as np
import sys
import os
import json
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import unicodedata
from sklearn.metrics.pairwise import cosine_similarity
import h5py
import string
import datetime
import regex as re
from read_json import read_file
import pandas as pd
from datetime import datetime
from read_json import read_file

object = read_file('timeline_sorted_time_miss.json',0)
geo = object['geo']
res = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.0"><Document><Style id="z1"><IconStyle><Icon><href>http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png</href></Icon></IconStyle></Style>'
for i in range(len(geo)):
    if len(geo[i]) != 0:
        res += '<Placemark><Point><coordinates>'
        res += str(geo[i])
        res += '</coordinates></Point></Placemark>'
res += '</Document></kml>'
print res
