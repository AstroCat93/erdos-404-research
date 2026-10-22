#!/bin/bash
# run_smc2.sh "N0 K P seed" ...  -- sequential lane of smc2 (p=2, C) runs, 1 core, logged with timings
cd "$(dirname "$0")/.."
for args in "$@"; do
  set -- $args
  out=data/smc/c2_N$1_K$2_P$3_s$4.txt
  echo "[C2] start $args $(date -u +%FT%TZ)" >> logs/smc2_lane.log
  /usr/bin/time -l ./code/smc2 $1 $2 $3 $4 > $out 2>> logs/smc2_lane.log
  echo "[C2] done  $args $(date -u +%FT%TZ) rc=$?" >> logs/smc2_lane.log
done
echo "[C2] ALL DONE $(date -u +%FT%TZ)" >> logs/smc2_lane.log
