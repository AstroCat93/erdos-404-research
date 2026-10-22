#!/bin/bash
# queue_completion_val.sh -- added when track R3C was completed (2026-10-13, after the original
# instance was cut off).  Large-scale exact checks of program D (covfast) against miss counts that
# were established in round 2 by other programs (note.md 10.2):
#   (11,7,40) K''=37: exactly 2 residues missed, 18038488330 and 23022655245 (A, B, C, covmiss.c)
#   (11,7,39) K''=1 : 1389738 residues missed (cov_pos.c, rcover.c, A, B)
#   (11,7,41) K''=37: covered (A, B, C, covmiss.c)
#   (17,7,42) K'=6  : 2 missed (C); K'=5 covered (C)
#   (13,8,46) K''=1 : 26 missed (A, C)
#   (7,6,33)  K'=5  : 2 missed mod 7^10 (round-2 logic and novelty referees); (7,6,34) K'=5 covered
# One log per case; sequential; nice 10 (via run.sh).
cd /home/user/erdos-404-research
R=code/round3/R3C/run.sh; B=/tmp/r3_R3C/bin; O=data/round3/R3C/valD
mkdir -p $O
$R $O/VD_11_7_40_K37.log env COVFAST_DUMP=10 $B/covfast 11 7 40 2 pos 37
$R $O/VD_11_7_39_K1.log  $B/covfast 11 7 39 2 pos 1
$R $O/VD_11_7_41_K37.log $B/covfast 11 7 41 2 pos 37
$R $O/VD_17_7_42_K56.log $B/covfast 17 7 42 2 pos 5 6
$R $O/VD_7_6_33_K5.log   env COVFAST_DUMP=10 $B/covfast 7 6 33 2 pos 5
$R $O/VD_7_6_34_K5.log   $B/covfast 7 6 34 2 pos 5
$R $O/VD_13_8_46_K1.log  env COVFAST_DUMP=30 $B/covfast 13 8 46 2 pos 1
echo "validation queue done"
