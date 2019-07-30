# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

'''
for i in range(len(dataList)):
    dataList[i] = dataList[i].strip().split('  ')
    for j in range(len(dataList[i])):
        dataList[i][j] = float(dataList[i][j])
    dataList[i] = np.asarray(dataList[i])
        
dataList = np.transpose(np.asarray(dataList))
print(dataList)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(dataList[3], dataList[2], dataList[1], c=dataList[0])
plt.show()
'''
file='AM1/ADKYXUTOBAGS-OIBJUYFYSA-N_AM1.esp'
with open(file) as esp:
        
    #take InChiKey from file name
    name = surfaces[i].split('_')[0]
    print(name)
    
    #read data from file
    lineList = esp.readlines()
    data = [np.asarray(j.split('  ')) for j in lineList[1:]]
    data = np.transpose(np.asarray(data))
    
    potentials = data[0]
    
    max_ptl = max(potentials)
    min_ptl = min(potentials)