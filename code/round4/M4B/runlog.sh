#!/bin/sh
# runlog.sh LOGFILE CMD... : run CMD under nice -n 10 with a 30-minute limit and append
# "### command: CMD", "### start:", the filtered output, the exit code and the wall time to LOGFILE.
# Output lines kept: those matching RESULT|MISMATCH|FAIL|SUMMARY|TABLE|ROW|^  (set FILTER to override).
LOG=$1; shift
FILTER=${FILTER:-'RESULT|MISMATCH|FAIL|SUMMARY|TABLE|ROW|^ '}
echo "### command: $*" >> "$LOG"
echo "### start: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
t0=$(date +%s.%N)
PYTHONDONTWRITEBYTECODE=1 timeout 1800 nice -n 10 "$@" > /tmp/r4_M4B/last_run.out 2>&1
rc=$?
grep -E "$FILTER" /tmp/r4_M4B/last_run.out >> "$LOG"
t1=$(date +%s.%N)
echo "### exit: $rc" >> "$LOG"
echo "### wall: $(echo "$t1 - $t0" | bc) s" >> "$LOG"
