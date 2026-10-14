#!/bin/bash
# End-to-end tests of Theorem P (exact decisions of P(x,n) via census DFS), with controls.
R=/home/user/erdos-404-research/code/round4/verify_D_P_recompute/run.sh
X=/tmp/r4_verify_D_P_recompute/thmP_test
XB=/tmp/r4_verify_D_P_recompute/thmP_test_big   # same source, compiled with -DHBITS=27 (depth-7 gates at p=13)
#            p  T n0  N  L  samples seed tlo thi ilo ihi premise
# main tests (hypotheses of Theorem P met whenever dmax <= T)
$R thmP.log $X 7  6 34  70 21 600 11 1 6 35 70 34
$R thmP.log $X 7  6 34 100 21 300 12 0 0 0 0 34
$R thmP.log $X 11 6 33  70 17 400 13 1 6 34 70 33
$R thmP.log $X 13 7 39  60 16 300 14 1 6 40 60 39
$R thmP.log $XB 13 7 39 50 16 40 15 7 7 40 50 39   # first attempt: aborted on a full memo (exit 2, old build)
# rerun after making a full memo an "undecided" outcome (thmP_test.c now counts it), 16 samples:
$R thmP.log $XB 13 7 39 50 16 16 16 7 7 40 50 39
# controls (hypotheses deliberately violated): premise too early, or gate deeper than T
$R thmP.log $X 7  6 34  40 21 300 21 4 6 21 30 20
$R thmP.log $X 7  6 34  45 21 150 22 7 8 35 45 34
$R thmP.log $X 13 7 39  40 16 300 23 4 6 21 33 20
echo THMP_BATCH_DONE >> /home/user/erdos-404-research/data/round4/verify_D_P_recompute/thmP.log
# run afterwards (same session), 32 further depth-7 samples at p=13 with another seed:
$R thmP.log $XB 13 7 39 50 16 32 17 7 7 40 50 39
