#!/bin/sh
# run.sh LOG TIMEOUT CMD... : run CMD under nice -n 10 with a wall-time limit (seconds),
# write the command line at the top of LOG (overwriting), then output, exit code and wall time.
LOG=$1; shift
TO=$1; shift
{
  echo "=== command: $*"
  echo "=== start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$LOG"
S=$(date +%s.%N)
nice -n 10 timeout "$TO" "$@" >> "$LOG" 2>&1
RC=$?
E=$(date +%s.%N)
echo "=== exit: $RC   wall: $(python3 -c "print(round($E-$S,2))") s" >> "$LOG"
exit $RC
