#!/bin/bash
# logged batch 1: engine validation (w1) and per-cylinder W1-W5 tests (w2)
cd "$(dirname "$0")"
L=../../../data/round4/verify_M4D_falsify
for a in "3 11 12 18 3 3" "3 12 6 24 4 4" "5 13 10 15 5 5" "5 14 5 20 5 5" "7 15 6 14 3 7" "7 16 4 14 6 3"; do
  ./run.sh $L/w1_validate.log python3 w1_validate.py $a
done
./run.sh $L/w1_validate.log python3 w1_validate.py 5 13 10 15 5 5 60000 1
./run.sh $L/w1_validate.log python3 w1_validate.py 3 11 12 18 3 3 60000 1
for a in "7 101 40 21 7 7 rand 150" "7 102 30 35 7 7 mix 80 2" "7 103 15 42 14 7 mix 60 2" "7 104 10 49 7 7 gateW2 60 3" "7 105 10 49 7 7 gateW 60 3" "7 106 6 49 14 14 rand 40 2" \
         "5 201 40 20 5 5 mix 150 3" "5 202 20 30 10 10 mix 60 3" "5 203 15 40 5 5 gateW 80 4" \
         "3 301 40 18 3 3 mix 150 3" "3 302 30 30 6 6 mix 80 4" "3 303 20 40 6 6 gateW2 60 5" "3 304 20 40 6 6 gateW 60 5" \
         "7 107 1 35 7 7 near2 60 3" "5 204 1 20 5 5 near2 60 3" "3 305 1 30 6 6 near2 60 3"; do
  ./run.sh $L/w2_cyl.log python3 w2_cyl.py $a
done
