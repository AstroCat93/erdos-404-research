#!/bin/bash
# wbatch3.sh -- re-run of the p=3 and p=5 Theorem W6 chain runs of wbatch.sh/wbatch2.sh.
# In wbatch2.sh those eight runs were given non-numeric seeds ("6U", ...) and exited at once with a
# ValueError (logged in w3_chain.log as exit 1, wall 0 s).  Same parameters, numeric seeds.
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
C=/home/user/erdos-404-research/code/round4/verify_M4D_logic
L=/home/user/erdos-404-research/data/round4/verify_M4D_logic
R=$C/runlog.sh
i=0
for s in U R S P; do
  i=$((i+1))
  $R $L/w3_chain.log python3 $C/w3_chain.py 3 60$i 4 20 5 5 4 $s 30 8
done
i=0
for s in U R S P; do
  i=$((i+1))
  $R $L/w3_chain.log python3 $C/w3_chain.py 5 65$i 4 20 5 5 5 $s 10 7
done
