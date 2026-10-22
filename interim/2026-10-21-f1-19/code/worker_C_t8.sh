#!/bin/zsh
# W2: C' on (19,8,49) positions K=1..18, one job per position
W="${T3B_WORKDIR:?set T3B_WORKDIR to the working directory that holds src/ (these scripts), bin/, logs/ and locks/}"
cd "$W"
for K in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
  src/run_job.sh P19_t8_H49_K${K}_C bin/covchk_ip 19 8 49 2 pos $K
done
echo W2_DONE >> logs/workers.out
