#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 01 16:28:26 2019

@author: sc2195
"""
import csv

methods = ['MNDO', 'AM1', 'PM3', 'PM6', 'MNDOD', 'PM7']

def fetchexptval(method):
    
    lines = []

    with open('results_{:}.csv'.format(method), 'r') as db:
        reader = csv.reader(db)
        for row in reader:
            
            with open('nicola/_{:}.metadata'.format(row[0]), 'r') as f:
                 alpha, beta = None, None
                 lineList = f.readlines()
                 dataList = [i.split('     ') for i in lineList]
                 for d in dataList:
                      if d[0] == 'ExpBeta':
                           beta = float(d[1].strip())
                      elif d[0] == 'ExpAlpha':
                           alpha = float(d[1].strip())
            
            row.extend([alpha, beta])
            lines.append(row)
    db.close()
    
    with open('results_{:}_exp.csv'.format(method), 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    writeFile.close()
    
    return

for m in methods:
    print('Adding values for {:}'.format(m))
    fetchexptval(m)
