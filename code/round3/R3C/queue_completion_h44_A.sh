#!/bin/bash
# queue_completion_h44_A.sh -- added when track R3C was completed (2026-10-13).  Program D found
# (29,7,44) not covered at K'' = 3 (2 missed residues; p29_t7_H44/P29_t7_H44_D_K1-8.log).  Program A
# recomputes that position with its missed residues listed, and program C then does the same (third
# program).  Sequential: each job needs about 4.3 GB.
cd /home/user/erdos-404-research
R=code/round3/R3C/run.sh; B=/tmp/r3_R3C/bin; O=data/round3/R3C/p29_t7_H44
$R $O/P29_t7_H44_A_K3.log env FIBCOV_DUMP=20 $B/fibcov 29 7 44 1 pos 3
$R $O/P29_t7_H44_C_K3.log $B/covchk 29 7 44 1 pos 3
echo "H44 A/C queue done"
