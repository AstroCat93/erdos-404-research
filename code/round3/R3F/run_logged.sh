#!/bin/bash
# run_logged.sh LOGFILE CMD ARGS... -- run CMD under nice -n 10, writing the command line, UTC start/end
# times and the wall-clock seconds into LOGFILE (stdout+stderr of CMD go to LOGFILE too).
log="$1"; shift
{
  echo "# command: $*"
  echo "# host: $(uname -n)  start: $(date -u +%FT%TZ)"
  t0=$(date +%s.%N)
  nice -n 10 "$@" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  echo "# end: $(date -u +%FT%TZ)  exit=$rc  wall_seconds=$(echo "$t1 - $t0" | bc)"
} > "$log" 2>&1
