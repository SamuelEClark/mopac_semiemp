#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:46:26 2019

@author: sc2195
"""
import sys
sys.path.append('/home/sc2195/workspace/phasexmlparser')
sys.path.append('/home/sc2195/.conda/pkgs/lxml-4.3.4-py37hefd8a0e_0/lib/python3.7/site-packages')
import databaseextraction
import csv

def fetchexptval(method):
    with open('firstdatabase.xml') as f:
        tree = databaseextraction.read_and_validate_file(f)
    
    lines = []
    nfail=0
    with open('results/results_{:}.csv'.format(method), 'r') as db:
        reader = csv.reader(db)
        for row in reader:
            info = ['', ['', None, None]]
            try:
                info = databaseextraction.extract_mol_info_from_db(tree, row[0])
            except:
                #print('{:} not in database'.format(row[0]))
                nfail += 1
                pass
            
            alpha = None if info[1][1]==None else info[1][1][0]
            beta = None if info[1][2]==None else info[1][2][0]
                
            row.extend([alpha, beta])
            lines.append(row)
    db.close()
    
    with open('results/results_{:}_exp.csv'.format(method), 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    writeFile.close()
    
    return nfail
    