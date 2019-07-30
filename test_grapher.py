#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:52:18 2019

@author: sc2195
"""
import numpy as np

file='AM1/AAADKYXUTOBAGS-OIBJUYFYSA-N_AM1.esp'
with open(file) as esp:
        
    #take InChiKey from file name
    name = file.split('_')[0]
    
    #read data from file
    lineList = esp.readlines()
    data = [np.asarray([float(k) for k in j.strip().split('  ')]) for j in lineList[1:]]
    data = np.transpose(np.asarray(data))
    
    potentials = data[0]
    
    max_ptl = max(potentials)
    min_ptl = min(potentials)
