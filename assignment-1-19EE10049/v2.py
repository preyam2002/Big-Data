import threading
import re
import os
import sys
import time
import heapq

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

count = []
for _ in range(numThreads):
    count1 = []
    for _ in range(len(directories)):
        count1.append(dict())
    count.append(count1)

threads = [None]*numThreads
par_result = dict()
def countNgrams(threadNumber):
    dirNumber = 0
    for directory in directories:
        print(directory, "________" , threadNumber)
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
                if nGram in count[threadNumber][dirNumber]:
                    count[threadNumber][dirNumber][nGram]+=1
                else:
                    count[threadNumber][dirNumber][nGram]=1
        
        dirNumber+=1

for i in range(len(threads)):
    threads[i] = threading.Thread(target=countNgrams ,args=(i,))
    threads[i].start() 

for i in range(len(threads)):
    threads[i].join() 

result = dict()
print("MULTI THREADING DONE")
for dirNumber in range(len(directories)):
    numFiles = int(len(os.listdir(directories[dirNumber])))
    par_result = dict()
    print(dirNumber,"START")
    for i in range(len(threads)):
        for key,value in count[i][dirNumber].items():
            if key in par_result:
                par_result[key]+=value               
            else:
                par_result[key]=value
    print(dirNumber,"END")
    for key,value in par_result.items():
        if key in result:
            result[key] = max(result[key],value/numFiles)
        else:
            result[key] = value/numFiles 
k_result = heapq.nlargest(k, result, key=result.__getitem__)
for x in k_result:
    print(x, result[x])

end = time.time()
print("Time taken: ",end - start)
print(len(result))