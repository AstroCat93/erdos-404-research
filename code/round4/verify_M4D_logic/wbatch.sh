#!/bin/bash
# wbatch.sh -- logged batch for the logic check of M4D section 3 (Lemmas W1-W3, Prop W4, Cor W5, Thm W6).
# One job at a time, nice -n 10 (inside runlog.sh), single-threaded numpy.
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
C=/home/user/erdos-404-research/code/round4/verify_M4D_logic
L=/home/user/erdos-404-research/data/round4/verify_M4D_logic
R=$C/runlog.sh
PY="python3"

# 1. linearised model, arbitrary multisets: W1-W5 algebra   (args: p seed nsys D D' H H' npar mode)
for args in "3 11 200 2 1 5 3 3 rand" "3 12 200 1 2 6 3 1 dense" "3 13 100 2 2 7 4 4 win" \
            "3 14 100 0 2 5 3 2 rand" "3 15 60 2 0 5 3 3 rand" "3 16 60 3 1 7 3 2 win" \
            "5 21 150 1 1 6 4 3 win" "5 22 60 1 2 7 4 2 dense" "5 23 80 2 1 6 3 4 rand" "5 24 60 1 1 8 4 1 dense" \
            "7 31 100 1 1 7 4 3 win" "7 32 60 1 1 8 4 1 dense" "7 33 30 2 1 7 3 3 win" "7 34 30 1 2 7 3 2 win"; do
  $R $L/w1_abstract.log $PY $C/w1_abstract.py $args
done

# 2. real windows, direct valuations   (args: p seed nsamp n H H2 MAXPAR KMAX FULLPTS)
for args in "3 41 30 20 5 4 12 6 3" "3 42 20 26 6 5 12 7 2" "3 43 20 32 6 6 10 7 0" \
            "5 51 20 20 5 5 10 5 2" "5 52 15 25 6 5 10 5 0" "5 53 10 30 7 6 8 5 0" \
            "7 71 12 28 7 7 6 3 0" "7 72 8 35 8 7 5 4 0" "7 73 8 21 7 7 6 3 0"; do
  $R $L/w2_concrete.log $PY $C/w2_concrete.py $args
done

# 3. Theorem W6 chains over three windows   (args: p seed nA n0 H0 H1 H2 sched MAXPAR KMAX)
for s in U R S P; do
  $R $L/w3_chain.log $PY $C/w3_chain.py 3 6$s 4 20 5 5 4 $s 30 8
done
for s in U R S P; do
  $R $L/w3_chain.log $PY $C/w3_chain.py 5 6$s 4 20 5 5 5 $s 10 7
done
$R $L/w3_chain.log $PY $C/w3_chain.py 7 701 4 28 7 7 5 S 4 4
$R $L/w3_chain.log $PY $C/w3_chain.py 7 702 3 28 7 7 5 P 4 4
$R $L/w3_chain.log $PY $C/w3_chain.py 7 703 2 28 7 7 5 R 4 4
$R $L/w3_chain.log $PY $C/w3_chain.py 7 704 2 28 7 7 5 U 4 4

# 4. Corollary W5: KKT certificate, descent attack, scope probe   (args: p seed nsys n H H2 src KMAX NSTART)
for args in "3 81 40 20 6 4 win 5 4" "3 82 40 0 6 4 rand 4 4" "5 83 40 20 6 5 win 5 4" "5 84 30 0 7 4 rand 4 3" \
            "7 85 40 21 7 7 win 4 4" "7 86 20 0 7 4 rand 3 3" "11 87 30 22 8 8 win 3 3" "13 88 20 26 8 8 win 3 3"; do
  $R $L/w4_cw5_adv.log $PY $C/w4_cw5_adv.py $args
done
