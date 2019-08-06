#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:28:14 2019

@author: sc2195
"""
import matplotlib.pyplot as plt
import csv
from scipy import stats

expt_beta = []
MEP_min = []
colors = []
types = {'CO2':1, '0':0, 'SO':2, 'Py':3, 'OH':4, 
         'CN':5, 'mdd':6, 'N1':7, 'CO3':8, 'N2':9, 'N3':10, 'XX':11, 'PO':12, 'NO2':13}

method = 'PM7'

with open('jmolresults_{:}_exp.csv'.format(method), 'r') as readFile:
    reader = csv.reader(readFile)
    for line in reader:
        if line[2] != '' and line[4] != '':
            expt_beta.append(float(line[4]))
            MEP_min.append(-1*float(line[2]))
            colors.append(types.get(line[5]))
readFile.close()

#calculate best fit
slope, intercept, r_value, p_value, std_err = stats.linregress(expt_beta, MEP_min)
predict_y = [intercept + slope * i for i in expt_beta]

fig = plt.figure(figsize=(12,8))
plt.scatter(expt_beta, MEP_min, c=colors)
plt.plot(expt_beta, predict_y, color='black')

#format plot
plt.title('Expt_B against MEP min using {:} ({:} compounds)'.format(method, len(expt_beta)))
plt.legend(['Best fit, R^2 = {:.3f}'.format(r_value)])
plt.grid(which='both')
plt.xlabel("Beta (exp)")
plt.ylabel("MEP min")

#save fig and display
plt.savefig('graphs/{:}.png'.format(method))
plt.show()
