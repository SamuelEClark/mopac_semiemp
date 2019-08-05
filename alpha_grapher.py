#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:28:14 2019

@author: sc2195
"""
import matplotlib.pyplot as plt
import csv
from scipy import stats

expt_alpha = []
MEP_max = []

method = 'PM7'

with open('results/results_{:}_exp.csv'.format(method), 'r') as readFile:
    reader = csv.reader(readFile)
    for line in reader:
        if line[1] != '' and line[3] != '' and float(line[1]) > -1:
            expt_alpha.append(float(line[3]))
            MEP_max.append(float(line[1]))
readFile.close() 

slope, intercept, r_value, p_value, std_err = stats.linregress(expt_alpha, MEP_max)
predict_y = [intercept + slope * i for i in expt_alpha]

fig = plt.figure(figsize=(12,8))
plt.scatter(expt_alpha, MEP_max)
plt.plot(expt_alpha, predict_y, color='black')

#format plot
plt.title('Expt_A against MEP min using {:} ({:} compounds)'.format(method, len(expt_alpha)))
plt.legend(['Best fit, R^2 = {:.3f}'.format(r_value)])
plt.grid(which='both')
plt.xlabel("alpha (exp)")
plt.ylabel("MEP min")

#save fig and display
plt.savefig('graphs/{:}_alpha.png'.format(method))
plt.show()