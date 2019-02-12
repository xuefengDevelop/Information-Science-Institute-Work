'''
    some text information are not useful for machine learning, did some preprocessing to filter out these results which is not useful
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
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import time
import regex as re

tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                    if unicodedata.category(unichr(i)).startswith('P'))
dict = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen","twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety","hundred","hundreds", "thousand","thousands","million","millions", "billion", "trillion"]

def filter_string(text) :
    stop_words = set(stopwords.words('english'))
    text = re.sub(ur"\p{P}+", "",text)
    #word_tokens = word_tokenize(text.translate(tbl))
    word_tokens = text.split()
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            if(w.startswith("http")):
                w = "url"
            if(w.isdigit() or w.lower() in dict):
                w = "num"
            filtered_sentence.append(w)
    return ' '.join(filtered_sentence)

def read_json():
    start_time = time.time()
    res = ""
    res_file = ""
    path_to_json = 'll_nepal/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    res += "{ \"data\":["
    res_file += "{ \"data\":["
    for j in range(29946):
        with open(path_to_json + json_files[j]) as f:
            data = json.load(f)
            text = data['originalText']
            unicodedata.normalize('NFKD', text).encode('ascii','ignore')
            text = filter_string(text)
            if(j == 29945):
                res += "\""+ text + "\""
                res_file += "\""+ json_files[j]+ "\""
            else:
                res += "\""+ text + "\"" + ", "
                res_file += "\""+ json_files[j]+ "\"" + ","
    print("process data--- %s seconds ---" % (time.time() - start_time))
    res += "] }"
    res_file += "] }"
    file = open("data/nepal_datset_new_filter.json", "w")
    file.write(res.encode('utf8'))
    file.close()
    file = open("data/file_name_index_new_filter.json", "w")
    file.write(res_file)
    file.close()
def main():
    read_json()
if __name__ == "__main__":
    main()
