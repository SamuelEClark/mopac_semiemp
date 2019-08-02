#!/bin/bash

for file in nicola_mops/*.mgf; do
  echo "Reading {$file}"
  "load {$file}; isosurface molecular map MEP; show isosurface"  > tmp.spt
  jmol -ion tmp.spt > $file.jvxl
  echo "Job complete"
done
