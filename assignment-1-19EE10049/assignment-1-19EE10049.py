import threading
import re
import os
import sys
import time

start = time.time()

# path = "20_newsgroups"
# numThreads = 4
# n = 4
# k = 10 
path = sys.argv[1]
numThreads = int(sys.argv[2])
n = int(sys.argv[3])
k = int(sys.argv[4])

directories = []
for directory in os.listdir(path):
    directories.append(os.path.join(path,directory))

count = [dict()]*len(directories)
threads = [None]*numThreads
result = dict()

def countNgrams(threadNumber):
    dirNumber = 0
    for directory in directories:
        print(directory, "________" , threadNumber)
        size,rem = divmod(len(os.listdir(directory)),numThreads)
        numFiles = int(len(os.listdir(directories[dirNumber])))
        start = size*threadNumber + min(rem,threadNumber)
        end = start + size + int(threadNumber<rem)
        for file in os.listdir(directory)[start:end]:      
            f = open(os.path.join(directory,file), "r")
            text = f.read()
            f.close()
            words = list(filter(bool,re.split('[^a-zA-Z0-9]', text)))
            words = [word.lower() for word in words]
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

print("MULTI THREADING DONE")
for dirNumber in range(len(directories)):
    numFiles = int(len(os.listdir(directories[dirNumber])))
    par_result = dict()
    print(dirNumber,"START")
    for key,value in count[dirNumber].items():
        if key in result:
            result[key] = max(result[key],value/numFiles)
        else:
            result[key] = value/numFiles 
    print(dirNumber,"END")
print("HERE")
result = dict(sorted(result.items(), key=lambda item: -item[1]))
for key,value in result.items():
    if k>0:
        print(key,value)
        k-=1
    else:
        break

end = time.time()
print("Time taken: ",end - start)
print(len(result))