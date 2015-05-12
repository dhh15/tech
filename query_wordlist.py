import re
import json
import os

# Opening the pre-defined local wordlist
wordlist = open("wordlist.txt", "r").read()
wordlist = json.loads(wordlist)

BASE_URL = "/home/kanner/dhh15/data/nlf_techeng_journals/"
FOLDS = ["0371-6635/", "1458-6711/", "1458-8625/"]

CONTEXT_LENGTH = 10

global counter
counter = 0
contexts= dict()
# Acquiring the raw data as filelist
filelist = []
for i in FOLDS:
    f_list = os.listdir(BASE_URL+i)
    f_list = [BASE_URL+i+f for f in f_list]
    filelist.extend(f_list)

# res is the main ouput object, a Python dict()
res = dict()
for cat in wordlist:
    res.update( {cat : dict() })


    
#building empty context list, a dict-object of yearly keyword contexts
for i in range(1880, 1911):
    global contexts
    contexts.update( { str(i) : dict() } )
    for w in wordlist:
        for t in wordlist[w]:
            contexts[str(i)].update( { t : [] } )


# method for extracting year from a filename
def get_year_from_filename(filename):
    year = re.split("_", filename)[4]
    year = re.split("-", year)[0]
    return year  

# matching a word to predefined wordlist
def locate_word(word, filename):
    test = None
    year = get_year_from_filename(filename)
#   print(year)
    
    for w in wordlist:
        for t in wordlist[w]:
            
            if t in word and len(word) > 4:
                print(word+"="+t)
                test = t
            
    return test

# analyzing a word from the raw data

def query_file(file_as_string, filename):
    global counter
    global contexts
    as_list = re.split(" ", file_as_string)
    year = get_year_from_filename(filename)
    for word in as_list:
        test = locate_word(word, filename)
#        print(word)
        if test is not None:
            counter += 1
            index = as_list.index(word)
            start = index-CONTEXT_LENGTH
            if start < 0: start = 0
            end = index + CONTEXT_LENGTH
            if end > len(as_list)-1: end = len(as_list)-1
            context = as_list[start:end]
            contexts[year][test].append(context)    
        
               
            
                        
#actual script

for i in filelist:
    file = open(i, "r").read()    
    query_file(file, i)
        
freqs = dict()

#producing the output

for year in contexts:
    freq = 0
    freqs.update( { year : dict() } ) 
    for searchword in contexts[year]:
        for ccword in contexts[year][searchword]:
            for cword in ccword:
                print(cword)
                cword = re.sub("[\.,]", "", cword)
                if cword in freqs[year]:
                    freqs[year][cword] += 1
                else:
                    freqs[year].update( { cword : 1 } )


res = ""

for year in freqs:
    
    for cword in freqs[year]:
        if freqs[year][cword] > 3:
            res += str(year)+"\t"+cword+"\t"+str(freqs[year][cword])+"\n"


resfile = open("res.txt", "w")
resfile.write(res)



            
    
