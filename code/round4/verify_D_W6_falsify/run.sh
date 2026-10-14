#!/bin/bash
# usage: run.sh LOGFILE cmd args...
# Appends to LOGFILE: the command line and start time, the program output, then exit code and wall time.
# Every job runs under nice -n 10, a 30-minute timeout and a 3 GB address-space limit.
LOG="$1"; shift
{
  echo "================================================================"
  echo "\$ cd $(pwd) && nice -n 10 $*"
  echo "# start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$LOG"
START=$(date +%s)
( ulimit -v 3000000; nice -n 10 timeout 1800 "$@" ) >> "$LOG" 2>&1
RC=$?
END=$(date +%s)
echo "# exit $RC  wall $((END-START)) s" >> "$LOG"
exit $RC
