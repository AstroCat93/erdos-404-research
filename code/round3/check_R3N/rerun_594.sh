#!/bin/bash
# check_R3N: re-run the track's programs B and C (rebuilt from source in /tmp/r3_check_R3N) on a=594.
# Sequential, one core, nice -n 10.  Logs go to data/round3/check_R3N/.
B=/tmp/r3_check_R3N
L=/home/user/erdos-404-research/data/round3/check_R3N
for spec in "W 90395" "W 90394 $B/w594_90394_C.txt" "B 90395"; do
  set -- $spec
  prog=$1; K=$2; wf=$3
  log=$L/rerun_${prog}_594_K${K}.log
  extra=""; [ "$prog" = B ] && extra=" -lgmp"
  echo "# cmd: nice -n 10 $B/dfs$prog 594 $K $wf   (binary rebuilt by check_R3N: gcc 13.3.0 -O3 -march=native code/round3/R3N/dfs$prog.c$extra; started $(date -u +%FT%TZ))" > $log
  s=$(date +%s.%N)
  nice -n 10 $B/dfs$prog 594 $K $wf >> $log 2>&1
  e=$(date +%s.%N)
  echo "# wall time (driver): $(echo "$e - $s" | bc) s; finished $(date -u +%FT%TZ)" >> $log
done
echo done > /tmp/r3_check_R3N/rerun_594.done
