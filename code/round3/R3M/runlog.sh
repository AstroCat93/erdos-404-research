#!/bin/sh
# runlog.sh LOGFILE CMD... : append "### command: CMD", the filtered output and the wall time to LOGFILE.
# Output lines kept: those matching RESULT|MISMATCH|FAIL|SUMMARY|TABLE|^  (set FILTER to override).
LOG=$1; shift
FILTER=${FILTER:-'RESULT|MISMATCH|FAIL|SUMMARY|TABLE|^ '}
echo "### command: $*" >> "$LOG"
echo "### start: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG"
t0=$(date +%s.%N)
"$@" 2>&1 | grep -E "$FILTER" >> "$LOG"
t1=$(date +%s.%N)
echo "### wall: $(echo "$t1 - $t0" | bc) s" >> "$LOG"
