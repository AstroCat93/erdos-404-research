#!/bin/bash
# logged batch 2 (after the fix of the q* perturbation loop): W1-W5 per cylinder
# (w2), W3 all bands (w3), Cor W5 windows (w4), W1(a) slopes (w5)
cd "$(dirname "$0")"
L=../../../data/round4/verify_M4D_falsify
for a in "7 103 60 42 14 7 mix 60 2" "7 104 30 49 7 7 gateW2 60 3" "7 105 30 49 7 7 gateW 60 3" "7 106 10 49 14 14 rand 40 2" \
         "7 108 150 21 7 7 mix 150 2" "7 109 80 35 7 7 mix 100 2" \
         "5 201 100 20 5 5 mix 150 3" "5 202 40 30 10 10 mix 60 3" "5 203 40 40 5 5 gateW 80 4" \
         "3 301 100 18 3 3 mix 150 3" "3 302 60 30 6 6 mix 80 4" "3 303 40 40 6 6 gateW2 60 5" "3 304 40 40 6 6 gateW 60 5" \
         "7 107 1 35 7 7 near2 60 3" "5 204 1 20 5 5 near2 60 3" "3 305 1 30 6 6 near2 60 3"; do
  ./run.sh $L/w2_cyl.log python3 w2_cyl.py $a
done
for a in "7 401 20 42 7 mix 60 2" "7 402 20 35 7 mix 60 2" "7 403 10 49 14 gateW 40 3" "5 404 30 30 5 mix 60 3" "3 405 20 24 4 mix 60 3" "3 406 15 30 6 mix 60 4"; do
  ./run.sh $L/w3_bands.log python3 w3_bands.py $a
done
for a in "7 501 300 21 7 7 next" "7 502 150 35 7 7 next" "7 503 200 21 7 7 free" "7 504 60 28 14 14 next" "5 505 300 20 5 5 next" "5 506 200 20 5 5 free" \
         "3 507 300 18 4 3 next" "3 508 200 18 4 3 free" "11 509 60 22 11 11 next"; do
  ./run.sh $L/w4_cw5.log python3 w4_cw5.py $a
done
for a in "7 601 4 21 7 near2 3 3" "7 602 6 21 7 mix 3 3" "7 603 3 35 7 gateW 2 2" "5 604 10 20 5 mix 4 3" "5 605 4 20 5 near2 3 3" "3 606 20 18 4 mix 6 3" "3 607 10 24 4 near2 4 4"; do
  ./run.sh $L/w5_slopes.log python3 w5_slopes.py $a
done
