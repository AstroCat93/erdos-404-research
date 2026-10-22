#!/bin/bash
# waits for the python window batch (1-core cap), then runs the l2mc production runs sequentially
cd "$(dirname "$0")"
while [ ! -f logs/window_batch1.done ]; do sleep 10; done
run(){ echo "CMD: ./l2mc $*"; /usr/bin/time -p ./l2mc "$@"; }
{ run 1 3 1 40 16 7 1.25 20000; run 2 3 1 40 16 7 1.25 20000; run 3 3 1 40 16 7 1.25 20000; run 1 3 0 40 16 7 1.25 20000; run 1 3 2 40 16 7 1.25 20000; } > logs/l2mc_p3.log 2>&1
{ run 1 5 1 27 16 6 1.2 3000; run 2 5 1 27 16 6 1.2 3000; run 1 5 0 27 16 6 1.2 3000; } > logs/l2mc_p5.log 2>&1
{ run 1 7 1 22 16 5 1.2 3000; run 2 7 1 22 16 5 1.2 3000; run 1 7 0 22 16 5 1.2 3000; } > logs/l2mc_p7.log 2>&1
echo DONE > logs/l2mc_batch.done
