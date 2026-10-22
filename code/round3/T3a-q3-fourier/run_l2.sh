#!/bin/bash
# run_l2.sh LANE "p E N0" ...   -- sequential lane of l2dp runs, logged with timings (1 core each)
cd "$(dirname "$0")/.."
lane=$1; shift
for args in "$@"; do
  set -- $args; p=$1; E=$2; N=$3
  out=data/l2/p${p}_E${E}_N${N}.txt; log=logs/p${p}_E${E}_N${N}.log
  echo "[$lane] start p=$p E=$E N0=$N $(date -u +%FT%TZ)" >> logs/lane_$lane.log
  /usr/bin/time -l ./code/l2dp $p $E $N > $out 2> $log
  echo "[$lane] done  p=$p E=$E N0=$N $(date -u +%FT%TZ) rc=$?" >> logs/lane_$lane.log
done
echo "[$lane] ALL DONE $(date -u +%FT%TZ)" >> logs/lane_$lane.log
