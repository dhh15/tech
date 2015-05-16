#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pandas
import json
import codecs
import rpy2.robjects.numpy2ri
import rpy2.robjects as ro
import pandas.rpy.common as com
rpy2.robjects.numpy2ri.activate()

#Here we open a list of interesting words. The list is taken to be in txt file, with one word per line
with codecs.open("content_words.txt", "r", "utf-8") as content_words:
    content_words = content_words.read()

content_words = re.split("\n", content_words)


#In case there happens to be duplicates by mistake, here we filter them out
content_words = set(content_words)
content_words = list(content_words)

#Here we open n-grams, which are stored locally in json format. The json is produced by the other py-script
data = open("res_json.txt", "r").read()

data = json.loads(data)

data_res = dict()
data_res_norm = dict()
yearlist = [str(x) for x in range(1880, 1911)]
empty_list = [ 0 for x in range(1880, 1911)]

#print(data_res)

#We combine the n-grams and interesting words -list to a year-by-word frequency matrix

for word in content_words:
    line = [ 0 for x in range(1880, 1911)]
    #print(line)
    maximum = 0
    for year in data:
        ind = yearlist.index(year)
           
        if word in data[year]:



            line[ind] = data[year][word]
            #print(str(ind) + " " + str(data[year][word]))

    line_norm = []
    if max(line) > 0:
 #       print(type(line))

        for n in line:
            r = n*10000000/max(line)
            r = float(float(r)/float(10000000))
            print("r:"+str(r)+" max-line:"+str(max(line))+" n:"+str(n))
            line_norm.append(r)
 #       print(line_norm)
        
    print(line_norm)
    data_res.update( { word : line } )
    data_res_norm.update( { word : line_norm } )
   
    
    
    
    #print(word+" "+str(line))
print(data_res_norm)

data_res_norm = { x : data_res_norm[x] for x in data_res_norm if len(data_res_norm[x]) > 0 }
data_res_norm_x = []

for i in range(0, 31):
    line = [0 for i in range(0, len(data_res_norm))]
    data_res_norm_x.append(line)

i = 0
for word in data_res_norm:
   for f in range(0, 31):
       #print(data_res_norm[word][f])
       #print(data_res_norm_x[0])
       data_res_norm_x[f][i] = data_res_norm[word][f]
   i += 1
   

#The matrix is transformed to a Pandas DataFrame object

dataframe = pandas.DataFrame.from_dict(data_res)
norm_dataframe = pandas.DataFrame.from_dict(data_res_norm_x)

print(norm_dataframe.head())

#The dataframe is again converted to an R dataframe

df = com.convert_to_r_dataframe(norm_dataframe)

#The LSA library used here is an R library, and R is operated within the Python script with 'robjects' package

ro.globalenv['myTM'] = df
ro.r('library(lsa)')
ro.r('labels = row.names(myTM)')
file_row = 'png("/home/kanner/dhh15/plot.png", width=800, height=800)'
ro.r(file_row)
ro.r('par(mar=c(0,0,0,0))')
lsa_com = 'myLSA = lsa(myTM, dims=3)'
ro.r(lsa_com)
ro.r('TM = as.textmatrix(myLSA)')
ro.r('plot(TM, col="white")')
ro.r('text(TM, labels)')
ro.r('dev.off()')

    

