#!/bin/zsh
# W1: wait for the H=47 K=1 job, then A' on (19,8,49) positions K=1..18, one job per position (each <= 45 min)
W="${T3B_WORKDIR:?set T3B_WORKDIR to the working directory that holds src/ (these scripts), bin/, logs/ and locks/}"
cd "$W"
while pgrep -f "fibcov_ip 19 8 47" > /dev/null; do sleep 20; done
for K in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
  src/run_job.sh P19_t8_H49_K${K}_A bin/fibcov_ip 19 8 49 2 pos $K
done
echo W1_DONE >> logs/workers.out
