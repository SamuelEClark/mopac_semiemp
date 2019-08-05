#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:18:09 2019

@author: sc2195
"""
from os import listdir
from os.path import isfile, join
import numpy as np
import csv
import time

methods = ['MNDO', 'AM1', 'PM3', 'PM6', 'MNDOD', 'PM7']

def tabulate(file):
     #create a list of all MOPAC output files in the directory
     onlyfiles = [f for f in listdir('nicola_mops') if isfile(join('nicola_mops', f))]
     surfaces = [i for i in onlyfiles if '{:}.esp'.format(file) in i]
     
     rows = []
     
     #iterate through output files
     for i in range(len(surfaces)):
          with open('nicola_mops/'+surfaces[i]) as esp:

               #take InChiKey from file name
               name = surfaces[i].split('_')[1]
               
               #read data from file
               lineList = esp.readlines()
               data = [np.asarray([float(k) for k in j.strip().split('  ')]) for j in lineList[1:]]
               data = np.transpose(np.asarray(data))
  
               potentials = data[0]
	
               max_ptl = max(potentials)
               min_ptl = min(potentials)

               rows.append([name, max_ptl, min_ptl])

     with open('results_{:}.csv'.format(file), 'w') as results:
          writer = csv.writer(results)
          writer.writerows(rows)

     results.close()
     return

for n in range(len(methods)):
     tabulate(methods[n])
     print('{:} results generated: {:}'.format(methods[n], time.ctime()))
     print('Saved to file: results_{:}.csv\n\n'.format(methods[n]))
