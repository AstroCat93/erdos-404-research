#!/bin/bash
# queue_completion_h44.sh -- added when track R3C was completed (2026-10-13).  Partial test of the
# registered prediction "p = 29, depth 7, H = 44 fails at >= 1 of the 28 positions" (nu = 1.149,
# PREDICTIONS_registered.txt), which the original instance had marked "run only if budget allows".
# Program D on K'' = 1..8 at H = 44, stopping at the first position that is not covered (one job,
# < 60 min); if one fails, program A is run on that position (queue_completion_h44_A.sh).
cd /home/user/erdos-404-research
R=code/round3/R3C/run.sh; B=/tmp/r3_R3C/bin; O=data/round3/R3C/p29_t7_H44
mkdir -p $O
$R $O/P29_t7_H44_D_K1-8.log env COVFAST_ZMAX=16777216 COVFAST_STOP=1 COVFAST_DUMP=20 $B/covfast 29 7 44 1 pos 1 2 3 4 5 6 7 8
echo "H44 D queue done"
