#!/bin/bash
  (( i = 1 ))
for file in nicola_mops/*.mgf; do
  echo "Reading $file"
  echo "load $file; isosurface molecular map MEP; show isosurface"  > tmp.spt
  jmol -ion tmp.spt > nicola_jmol/"$file".jvxl
  echo "Job complete $i/4618"
  (( i++ ))
done
