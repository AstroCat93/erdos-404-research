#!/bin/sh
# ck_run.sh LOG CMD... : run CMD under nice, appending the command line, start time,
# full output and wall time to LOG (check_R3M logging wrapper; written independently).
LOG=$1; shift
{
  echo "=== command: $*"
  echo "=== start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
s=$(date +%s.%N)
nice -n 10 "$@" >> "$LOG" 2>&1
rc=$?
e=$(date +%s.%N)
echo "=== exit: $rc   wall: $(python3 -c "print(round($e-$s,2))") s" >> "$LOG"
