#!/bin/bash
# usage: run.sh LOGFILE cmd args...   (appends command line, start time, output, exit code, wall time)
LOG="$1"; shift
D=/home/user/erdos-404-research/data/round4/verify_D_P_recompute
mkdir -p "$D"
{
  echo "=== command: $*"
  echo "=== start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$D/$LOG"
S=$(date +%s.%N)
nice -n 10 "$@" >> "$D/$LOG" 2>&1
RC=$?
E=$(date +%s.%N)
echo "=== exit: $RC   wall: $(echo "$E - $S" | bc) s" >> "$D/$LOG"
exit $RC
