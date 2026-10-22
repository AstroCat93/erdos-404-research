#!/bin/sh
# run.sh LOG TIMEOUT_S CMD... : append the command line, start time, full output, exit code and wall time to LOG.
# nice -n 10, wall-time limit (exit 124 = timed out). Track verify_M4A_obstruction (round 4).
LOG=$1; shift
TO=$1; shift
{
  echo "=== command: $*"
  echo "=== start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
s=$(date +%s.%N)
PYTHONDONTWRITEBYTECODE=1 timeout "$TO" nice -n 10 "$@" >> "$LOG" 2>&1
rc=$?
e=$(date +%s.%N)
echo "=== exit: $rc   wall: $(python3 -c "print(round($e-$s,2))") s" >> "$LOG"
