#!/bin/sh
# run.sh LOG CMD... : run CMD under nice -n 10 (30 min limit), write the command line at the top
# of LOG (overwriting it), then the full output, exit code and wall time.
LOG=$1; shift
{
  echo "### command: $*"
  echo "### start (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$LOG"
t0=$(date +%s)
PYTHONDONTWRITEBYTECODE=1 timeout 1800 nice -n 10 "$@" >> "$LOG" 2>&1
rc=$?
t1=$(date +%s)
echo "### exit: $rc" >> "$LOG"
echo "### wall: $((t1 - t0)) s" >> "$LOG"
exit $rc
