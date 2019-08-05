#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:45:45 2019

@author: sc2195
"""
from os import listdir
from os.path import isfile, join

methods = ['MNDO', 'AM1', 'PM3', 'PM6', 'MNDOD', 'PM7']

def parse(lines):
    parsed_lines = []
    for line in lines:
        start = 0
        row = []
        for i in range(len(line)):
            if (line[i] == ' ' and line[i-1] != ' ') or i == len(line):
                row.append(line[start:i])
            elif line[i-1] == ' ' and line[i] != ' ':
                start = i
        parsed_lines.append(row)
    return parsed_lines

onlyfiles = [f for f in listdir('nicola_pdbs') if isfile(join('nicola_pdbs', f))]
MoleculeFiles = [i for i in onlyfiles if '.pdb' in i]

for file in MoleculeFiles:
    with open('nicola_pdbs/'+file) as f:
        name = file.split('.')[0]
        lineList = f.readlines()
        parsed = parse(lineList)
    
    atomLines = [i for i in parsed[:-1] if i[0] == 'HETATM']
    atomData = [[i[2], float(i[5]), float(i[6]), float(i[7])] for i in atomLines]
    
    for method in methods:
        with open('nicola_mops/{:}_{:}.mop'.format(name, method), 'w') as mop:
                mop.write('{:} SYMMETRY CHARGE=0 ESP NSURF=7 POTWRT\n'.format(method))
                mop.write('{:}\n\n'.format(name))
                for atom in atomData:
                    mop.write('   {:}       {:.8f}             1         {:.8f}             1        {:.8f}             1 \n'
                              .format(atom[0], atom[1], atom[2], atom[3]))
    
