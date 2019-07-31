#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:28:14 2019

@author: sc2195
"""
import matplotlib.pyplot as plt
import csv

expt_beta = []
MEP_min = []

method = 'PM7'

with open('results/results_{:}_exp.csv'.format(method), 'r') as readFile:
    reader = csv.reader(readFile)
    for line in reader:
        if line[2] != '' and line[4] != '' and float(line[2]) > -1:
            expt_beta.append(float(line[4]))
            MEP_min.append(float(line[2]))
readFile.close() 

fig = plt.figure(figsize=(12,8))
plt.scatter(expt_beta, MEP_min)
plt.title('Expt_B against MEP min using {:} ({:} compounds)'.format(method, len(expt_beta)))
plt.grid(which='both')
plt.xlabel("Beta (exp)")
plt.ylabel("MEP min")
plt.savefig('{:}.png'.format(method))
plt.show()