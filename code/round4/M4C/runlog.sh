#!/bin/bash
# runlog.sh LOGFILE cmd args...  -- appends the command line, start time, output and wall time to LOGFILE
LOG="$1"; shift
{ echo "### command: $*"; echo "### start: $(date -u +%FT%TZ)"; } >> "$LOG"
S=$(date +%s)
nice -n 10 "$@" >> "$LOG" 2>&1
echo "### wall: $(( $(date +%s) - S )) s" >> "$LOG"
