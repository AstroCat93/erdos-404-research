#!/bin/sh
# Usage: runlog.sh LOGFILE TIMEOUT_SECONDS cmd args...
# Runs cmd at nice -n 10 with a wall-time limit; logs the command line,
# start time, all output, exit code and wall time.
LOG="$1"; shift
TO="$1"; shift
{
  echo "=== command: $*"
  echo "=== start: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$LOG"
T0=$(date +%s)
nice -n 10 timeout "$TO" "$@" >> "$LOG" 2>&1
RC=$?
T1=$(date +%s)
{
  echo "=== exit: $RC"
  echo "=== wall: $((T1 - T0)) s"
} >> "$LOG"
exit $RC
