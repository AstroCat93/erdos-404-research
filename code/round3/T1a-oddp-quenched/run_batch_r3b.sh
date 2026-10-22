#!/bin/bash
cd "$(dirname "$0")"
run(){ echo "CMD: ./winvar $*"; /usr/bin/time -p ./winvar "$@"; echo; }
{ for s in 11 12 13 14; do run 2 $s 3 4 79 33 3 1.25 200 8000000; done; } > logs/r3/atom2_p3.log 2>&1
{ for s in 21 22 23 24; do run 2 $s 5 1 54 25 2 1.25 200 8000000; done; for s in 25 26; do run 2 $s 5 2 54 30 1 1.25 200 8000000; done; } > logs/r3/atom2_p5.log 2>&1
{ for s in 43 44 45 46 47; do run 2 $s 7 0 44 16 3 1.25 150 8000000; done; for s in 34 35 36 37; do run 2 $s 7 1 44 20 1 1.25 150 8000000; done; } > logs/r3/atom2_p7.log 2>&1
echo DONE > logs/r3/batch2.done
