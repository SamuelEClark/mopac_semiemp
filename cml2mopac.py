#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 10:12:59 2019

@author: sc2195
"""
import numpy as np

methods = ['MNDO', 'AM1', 'PM3', 'PM6', 'MNDOD', 'PM7']

def mkMOPACinputs(data, name):
    
    for n in range(len(methods)):
                
        atom_data = np.empty([0, 4])
        for i in range(len(data)):
            
            if '<atom' in data[i]:
                el, x, y, z = 0, 0, 0, 0
                
                for j in range(len(data[i])):
                    if 'element' in data[i][j]:
                        el = data[i][j][13:-1]
                    elif 'x3' in data[i][j]:
                        x = data[i][j][4:-1]
                    elif 'y3' in data[i][j]:
                        y = data[i][j][4:-1]
                    elif 'z3' in data[i][j]:
                        z = data[i][j][4:-4]
                        
                row = np.asarray([[el, x, y, z]])
                atom_data = np.concatenate((atom_data, row), axis=0)
                
        with open('results/{:}_{:}.mop'.format(name, methods[n]), 'w') as mop:
            mop.write('{:} SYMMETRY CHARGE=0 ESP NSURF=7 POTWRT\n'.format(methods[n]))
            mop.write('{:}\n\n'.format(name))
            for n in range(len(atom_data)):
                mop.write('   {:}       {:.8f}             1         {:.8f}             1        {:.8f}             1 \n'
                          .format(atom_data[n][0], float(atom_data[n][1]), float(atom_data[n][2]), float(atom_data[n][3])))
    return
