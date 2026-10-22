#!/bin/bash
# usage: runlog.sh LOGFILE TIMEOUT_SECONDS cmd args...
# Appends "=== command: ..." at the top of the run, the output, and "=== exit: CODE wall: S".
LOG="$1"; shift; TO="$1"; shift
{
  echo "=== command: $*"
  echo "=== start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
T0=$(date +%s.%N)
nice -n 10 timeout "$TO" "$@" >> "$LOG" 2>&1
RC=$?
T1=$(date +%s.%N)
echo "=== exit: $RC   wall: $(echo "$T1 - $T0" | bc) s" >> "$LOG"
exit $RC
