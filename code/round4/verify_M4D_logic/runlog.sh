#!/bin/bash
# runlog.sh LOG cmd... : appends "## <command line>" and start time, then the output, exit code and wall time, to LOG.
LOG="$1"; shift
{
  echo "## $*"
  echo "## start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
T0=$(date +%s)
timeout 1800 nice -n 10 "$@" >> "$LOG" 2>&1
RC=$?
T1=$(date +%s)
echo "## exit $RC, wall $((T1-T0)) s" >> "$LOG"
echo >> "$LOG"
exit $RC
