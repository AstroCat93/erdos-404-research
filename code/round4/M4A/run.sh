#!/bin/sh
# run.sh LOG TIMEOUT_S CMD... : append the command line, start time, full output, exit code and wall time to LOG.
# Runs under nice -n 10 with a wall-time limit (exit 124 = timed out). Adapted from code/round3/check_R3M/ck_run2.sh.
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
