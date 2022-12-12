#!/bin/bash

for d in day*; do
  cd $d; 
  if [[ -e "./$d.py" ]]; then
    echo "Running ${d}"
    PYTHONPATH=..:. ./$d.py;
    r=$?
    if [ $r -ne 0 ]; then
      echo "Error running ${d}"
      exit $r
    fi
    echo ""
  fi
  cd $OLDPWD; 
done
