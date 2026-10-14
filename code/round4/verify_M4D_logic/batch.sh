#!/bin/bash
# batch.sh -- the logged runs of the verify_M4D_logic track (one at a time, nice -n 10, 30-min cap per run).
cd /home/user/erdos-404-research/code/round4/verify_M4D_logic || exit 1
OUT=/home/user/erdos-404-research/data/round4/verify_M4D_logic
R=./runlog.sh

# t2: validation of the checker's two target routes (brute force, DFS, carry recursion python/numpy)
for args in "3 1 20 14" "5 2 20 14" "7 3 20 14" "3 4 10 14 6 4" "5 5 10 14 7 3" "7 6 10 14 9 3" "7 7 10 14 2 2"; do
  $R $OUT/t2_recursion.log python3 t2_recursion.py $args
done

# t1: Lemma L and (F2), brute force over all digit strings; edge cases D=0 / D2=0; forced gates; NEG control
for args in "3 11 30 9 8 6" "3 12 30 12 10 6" "5 13 30 10 9 8" "5 14 20 15 10 8" "7 15 30 14 10 8" "7 16 15 21 12 10" \
            "7 17 40 14 8 3" "13 18 40 13 6 4" "11 19 20 11 10 9" \
            "7 20 20 14 10 8 200 0 16 3" "7 21 20 14 10 8 200 0 26 4" "5 22 20 10 9 8 200 0 12 4" "3 23 20 9 8 6 200 0 12 5" \
            "5 24 20 10 9 8 200 1" "7 25 20 14 10 8 200 1"; do
  $R $OUT/t1_lemmaL.log python3 t1_lemmaL.py $args
done

# t3: Theorem F, strong quantitative form, many theta schedules; union identity; NEG1/NEG2 controls
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 3 31 150 14 3 8 14 22 32 44
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 5 32 120 10 5 12 20 30 42
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 7 33 300 8 8 18 30 44 60
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 7 34 25 8 10 34 60 88
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 7 35 30 8 8 18 30 44 60 --gate 19 3
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 11 36 40 6 11 33 58 86
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 13 37 40 6 13 39 65 91
$R $OUT/t3_thmF_chain.log python3 t3_thmF_chain.py 13 38 15 6 13 39 65 91 --gate 41 3
# ^ killed by hand after ~600 s at 0.9 GB (exit 143 in the log): the forced gate raises V_91 by 3, and the exact
#   target sets near n~37 grow towards 10^7-10^8 residues; no result taken.  The gated case is covered at p=7.

# t4: Corollary F1 (finite horizon), exhaustive over cylinders, exact Fractions; local-constancy spot checks
$R $OUT/t4_corF1.log python3 t4_corF1_exhaustive.py 7 0 0 8 tao 7 13 20 28
$R $OUT/t4_corF1.log python3 t4_corF1_exhaustive.py 7 3 1 9 1/2 7 13 20 28
$R $OUT/t4_corF1.log python3 t4_corF1_exhaustive.py 5 0 0 9 tao 5 10 16 23
$R $OUT/t4_corF1.log python3 t4_corF1_exhaustive.py 5 0 0 9 1/2 5 10 16 23
$R $OUT/t4_corF1.log python3 t4_corF1_exhaustive.py 3 0 0 13 tao 3 7 12 18

# replacement for the run "t1_lemmaL.py 3 23 20 9 8 6 200 0 12 5", killed by hand after 591 s (exit 143 in the log):
# x = -12 mod 3^5 fixes x mod p^{V_9}, and that class has no path alive at n=9, so the sampling loop never ended.
# t1 now has a draw guard; the replacement forces a depth-3 gate at i=14, which leaves aliveness at n=9 random.
$R $OUT/t1_lemmaL.log python3 t1_lemmaL.py 3 23 20 9 8 6 200 0 14 3
