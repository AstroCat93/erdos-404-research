#!/bin/sh
# Task (1): exact annealed moments.  4 threads.  Each run logged with timing.
W="<WORKSPACE>/e404r3/T4-computations"
cd "$W"
for pg in "2 4" "2 8" "2 12" "2 16" "2 18" "2 20" "2 22" "2 24" "2 26" "3 2" "3 4" "3 6" "3 8" "3 10" "3 12" "3 13" "3 14" "3 15" "3 16" "5 2" "5 3" "5 4" "5 5" "5 6" "5 7" "5 8" "5 9" "5 10" "7 1" "7 2" "7 3" "7 4" "7 5" "7 6" "7 7" "7 8" "2 27" "3 17" "5 11" "7 9" "2 28"; do
  set -- $pg
  echo "=== annealed p=$1 G=$2 start $(date +%T)" >> logs/annealed.log
  s=$(date +%s)
  ./src/annealed $1 $2 4 > data/annealed_p$1_G$2.txt 2>> logs/annealed.log
  echo "=== done p=$1 G=$2 in $(( $(date +%s) - s )) s" >> logs/annealed.log
done
echo ALLDONE >> logs/annealed.log
