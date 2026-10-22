#!/bin/sh
# deep lifting of the five a <= 4096 with g_2(a) >= 4094 (4 processes, then 594); output: a g_capped maxpop steps cpu_seconds
cd "$(dirname "$0")"
L=../logs/deep.log; D=../data/deep_lift.txt
echo "# a g_capped(or CAP if survived) maxpop steps cpu_s   (p2add CAP a; -1 = population overflow)" > $D
run() { echo "start p2add $1 $2 $(date +%T)" >> $L; ./p2add $1 $2 22 >> $D 2>> $L; echo "done p2add $1 $2 $(date +%T)" >> $L; }
run 18500 34 &
run 11600 1102 &
run 4900 3456 &
run 16382 2210 &
wait
run 16382 594
echo DEEPDONE >> $L
