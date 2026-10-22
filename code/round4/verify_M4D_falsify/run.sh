#!/bin/bash
# usage: run.sh LOGFILE cmd args...   (appends; command line first, exit code and wall time after)
LOG="$1"; shift
{
  echo "================================================================"
  echo "\$ cd $(pwd) && nice -n 10 $*"
  echo "# start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
START=$(date +%s)
nice -n 10 timeout 1800 "$@" >> "$LOG" 2>&1
RC=$?
END=$(date +%s)
echo "# exit $RC  wall $((END-START)) s" >> "$LOG"
exit $RC
