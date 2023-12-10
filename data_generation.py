import time
import random
import threading
from time import sleep
from threading import Thread, Lock
from queue import Queue
import numpy as np
from collections import defaultdict, deque
import pandas as pd

numberOfMachines = input('Number of Machines:\n')
numberOfJobs = input('Number of Jobs:\n')
machiningSequence = []
SequenceLength = []

for i in range (int(numberOfJobs)):
  buffer = deque()
  sequenceLength= input(f"Enter the length of machine sequence for job {i+1}:\n")
  SequenceLength.append(sequenceLength)

  for j in range(int(sequenceLength)):
    id = (int(input(f"Enter {j+1}th required machine:\n")) - 1)
    meanTime = float(input(f"Enter the mean time for job completion of Machine {id + 1} for job {i+1}:\n"))
    stdDev = float(input(f"Enter the Standard Deviation for Machine {id + 1} for job {i+1}:\n"))
    buffer.append((id,meanTime,stdDev))

  machiningSequence.append(buffer)

def completionTime(jobID, sequenceNumber):
  time = np.random.normal(loc=machiningSequence[jobID][sequenceNumber][1],scale=machiningSequence[jobID][sequenceNumber][2])
  return time

lockList = []
bufferList = []
consumerState = []

for i in range(int(numberOfMachines)):
  lock = Lock()
  lockList.append(lock)
  consumerState.append(0)

for i in range(int(numberOfJobs)):
  buffer = deque()
  for j in range(int(SequenceLength[i])):
    machineID = machiningSequence[i][j][0]
    cTime = completionTime(i,j)
    buffer.append((machineID, completionTime(i, j)))
  bufferList.append(buffer)

print(bufferList)
print(bufferList[0])
print(len(bufferList[0]))

print(bufferList)
cTime = []

entity_id = []
product_id = []
start_time = []
end_time = []
time_elapsed = []

def entity(jobID, buffer):
  while(len(buffer)):
    product_id.append(jobID + 1)
    item = buffer.popleft()
    entity_id.append(item[0] + 1)
    with lockList[item[0]]:
      print(f"Entity {item[0] + 1} started consuming item {jobID + 1}")
      iniTime = time.time()
      sleep(item[1])
      finTime = time.time()
      print(f"Entity {item[0] + 1} finished consuming item {jobID + 1}")
      end_time.append(finTime)
      start_time.append(iniTime)
      TimeElapsed = (finTime-iniTime)
      print(TimeElapsed)
      time_elapsed.append(TimeElapsed)


# Create and start consumer threads
entityThreads = []
for i in range(int(numberOfJobs)):
    t = threading.Thread(target = entity, args=(i,bufferList[i]))
    entityThreads.append(t)
    t.start()

# Wait for all threads to finish
for t in entityThreads:
    t.join()

list_data = list(zip(entity_id,product_id,start_time,end_time,time_elapsed))

list_data

data = pd.DataFrame(list_data, columns = ['Entity ID', 'Product ID', 'Start Time', 'End Time', 'Time Elapsed'])

data

dataToExcel = pd.ExcelWriter('Generated_Data.xlsx')
data.to_excel(dataToExcel)

dataToExcel.save()