#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:36:49 2019

@author: sc2195
"""
from cml2mopac import mkMOPACinputs

with open('all.cml') as db:
    lineList = db.readlines()
    
    #read through lines, feed chunks to mkMOPACinputs
    start = 1
    for i in range(len(lineList)):
        if 'molecule>' in lineList[i]:
            data = [j.split(' ') for j in lineList[start:i]]
            name = data[0][2][13:-1]
            
            mkMOPACinputs(data, name)

            start = i+1
