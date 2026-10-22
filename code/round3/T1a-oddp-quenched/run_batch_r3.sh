#!/bin/bash
# Production batch, track T1a round 3 (2026-10-21). Sequential, 1 core. Logs in logs/r3/.
cd "$(dirname "$0")"
run(){ echo "CMD: ./winvar $*"; /usr/bin/time -p ./winvar "$@"; echo; }
{ run 1 101 3 4 79 24 4 1.25 14 8000000 256; run 1 202 3 6 79 24 3 1.25 6 8000000 256; } > logs/r3/traj_p3.log 2>&1
{ run 1 303 5 2 54 20 2 1.25 12 8000000 256; run 1 404 5 1 54 20 3 1.25 12 8000000 256; } > logs/r3/traj_p5.log 2>&1
{ run 1 505 7 1 44 16 1 1.25 12 8000000 256; run 1 606 7 0 44 16 3 1.25 10 8000000 256; } > logs/r3/traj_p7.log 2>&1
{ for s in 11 12 13; do run 2 $s 3 4 79 24 4 1.25 200 8000000; done; } > logs/r3/atom_p3.log 2>&1
{ for s in 21 22 23; do run 2 $s 5 2 54 20 2 1.25 200 8000000; done; } > logs/r3/atom_p5.log 2>&1
{ for s in 31 32 33; do run 2 $s 7 1 44 16 1 1.25 150 8000000; done; for s in 41 42; do run 2 $s 7 0 44 16 3 1.25 150 8000000; done; } > logs/r3/atom_p7.log 2>&1
echo DONE > logs/r3/batch.done
