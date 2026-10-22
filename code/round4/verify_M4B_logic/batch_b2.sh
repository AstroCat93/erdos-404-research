#!/bin/sh
# batch_b2.sh: runs of the logic check of M4B Lemma B2a / Corollary B2' (one job at a time, nice -n 10 via runlog.sh).
D=/home/user/erdos-404-research/data/round4/verify_M4B_logic
cd /home/user/erdos-404-research/code/round4/verify_M4B_logic
R=./runlog.sh
# t5: Lemma B2a, exhaustive (meet in the middle) for d <= 22; tail bound; negative controls
$R $D/t5_b2a.log 1200 python3 b2a_exhaustive.py 22
# t6: Corollary B2' end to end (exact).  args: p SEED NPER n H H2 KMAX PREC DLIST SEXTRA SUB
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 7 11 6 21 4 24 8 30 1,2,3,4 2 1
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 7 12 5 14 12 12 8 30 1,2,3,5,6,12 2 1
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 7 13 4 14 9 7 8 30 7,8,9 1 1
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 7 14 4 21 3 3 8 30 1,2,3 1 0
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 5 21 5 15 8 14 9 30 1,2,3,4,5,6,7,8 2 1
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 3 31 5 12 8 12 13 40 1,2,3,4,5,6,7,8 2 1
# t6 (added): p=3 with a short post window, to reach d = 7, 8 (v((d-1)!) = 2) under KMAX
$R $D/t6_b2p.log 1200 python3 b2p_identity.py 3 32 4 12 8 4 14 40 6,7,8 1 1
