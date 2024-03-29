import threading
import re
import os
import sys
import time
import heapq

start = time.time()

path = sys.argv[1]
numThreads = int(sys.argv[2])
n = int(sys.argv[3])
k = int(sys.argv[4])

directories = []
for directory in os.listdir(path):
    directories.append(os.path.join(path,directory))  

count = []
for i in range(len(directories)):
    count.append(dict())
threads = [None]*numThreads
result = dict()

def countNgrams(threadNumber):
    dirNumber = 0
    for directory in directories:
        size,rem = divmod(len(os.listdir(directory)),numThreads)
        start = size*threadNumber + min(rem,threadNumber)
        end = start + size + int(threadNumber<rem)
        for file in os.listdir(directory)[start:end]:  
            f = open(os.path.join(directory,file), "rb")
            text = f.read()
            f.close()
            words = list(filter(bool,re.split(b'[^a-zA-Z0-9]', text)))
            words = [(word.decode("utf-8")).lower() for word in words]
            for i in range(len(words)-n+1):
                nGrams = []
                for j in range(n):
                    nGrams.append(words[i+j])
                nGram = " ".join(nGrams)
                if nGram in count[dirNumber]:
                    count[dirNumber][nGram]+=1
                else:
                    count[dirNumber][nGram]=1
        dirNumber+=1

for i in range(len(threads)):
    threads[i] = threading.Thread(target=countNgrams ,args=(i,))
    threads[i].start() 

for i in range(len(threads)):
    threads[i].join() 

for dirNumber in range(len(directories)):
    numFiles = int(len(os.listdir(directories[dirNumber])))
    par_result = dict()
    for key,value in count[dirNumber].items():
        if key in result:
            result[key] = max(result[key],value/numFiles)
        else:
            result[key] = value/numFiles

k_result = heapq.nlargest(k, result, key=result.__getitem__)
for x in k_result:
    print(x, result[x])

end = time.time()