#!/bin/bash
# run_smc.sh LANE "p N0 K P seed" ...  -- sequential lane of SMC runs (1 core), logged with timings
cd "$(dirname "$0")/.."
lane=$1; shift
for args in "$@"; do
  set -- $args
  out=data/smc/p$1_N$2_K$3_P$4_s$5.txt
  echo "[$lane] start $args $(date -u +%FT%TZ)" >> logs/smc_lane_$lane.log
  /usr/bin/time -p python3 code/smc_l2.py $1 $2 $3 $4 $5 > $out 2>> logs/smc_lane_$lane.log
  echo "[$lane] done  $args $(date -u +%FT%TZ) rc=$?" >> logs/smc_lane_$lane.log
done
echo "[$lane] ALL DONE $(date -u +%FT%TZ)" >> logs/smc_lane_$lane.log
