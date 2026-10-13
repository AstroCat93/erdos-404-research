#!/bin/bash
# queue_misc.sh -- small second-core jobs (round 3, track R3C): missed-residue dumps of the two
# 2-residue negative certificates, and per-unit timings for the cost table (p = 19 depth 7, Cov(5,5,39)).
cd /home/user/erdos-404-research
R=code/round3/R3C/run.sh; B=/tmp/r3_R3C/bin; O=data/round3/R3C
$R $O/N29_t6_H39_K2_dump_D.log env COVFAST_DUMP=10 $B/covfast 29 6 39 1 pos 2
$R $O/N31_t6_H40_K2_dump_D.log env COVFAST_DUMP=10 $B/covfast 31 6 40 1 pos 2
$R $O/N29_t6_H39_K2_dump_A.log env FIBCOV_DUMP=10 $B/fibcov 29 6 39 1 pos 2
$R $O/N31_t6_H40_K2_dump_A.log env FIBCOV_DUMP=10 $B/fibcov 31 6 40 1 pos 2
# timing only (cost table): one new p = 19 depth-7 position (K'' = 20) with A and D, H = 45, k = 2
$R $O/T19_t7_H45_K20_A.log $B/fibcov 19 7 45 2 pos 20
$R $O/T19_t7_H45_K20_D.log $B/covfast 19 7 45 2 pos 20
# timing only: 48 classes of Cov(5,5,39) with D (A and C were timed on the same 48 classes)
$R $O/T5_t5_H39_D_48cls.log $B/covfast 5 5 39 5 pos $(seq 1 59 | awk '$1%5')
echo misc done
