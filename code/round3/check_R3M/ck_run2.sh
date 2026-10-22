#!/bin/sh
# ck_run2.sh LOG TIMEOUT_S CMD... : like ck_run.sh, with a wall-time limit (exit 124 = timed out).
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
