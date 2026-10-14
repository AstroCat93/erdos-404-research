#!/bin/bash
# runlog.sh LOG cmd args... : append a run to LOG with command line, start time, output, exit status and wall time.
LOG="$1"; shift
{
  echo "=== command: $*"
  echo "=== start: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
T0=$(date +%s)
nice -n 10 "$@" >> "$LOG" 2>&1
RC=$?
T1=$(date +%s)
echo "=== exit: $RC   wall: $((T1-T0)) s" >> "$LOG"
exit $RC
