#!/bin/bash
  (( i = 1 ))
for file in nicola_mops/*.mop ; do
  echo "Initialising job... "
  ./MOPAC2016.exe "$file"
  echo "Job $i/4620 complete"
  (( ++i ))
done
