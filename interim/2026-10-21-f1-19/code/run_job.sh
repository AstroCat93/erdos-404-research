#!/bin/zsh
# usage: run_job.sh NAME CMD...   -> logs/NAME.log with command, start/end, wall time, max RSS
W="${T3B_WORKDIR:?set T3B_WORKDIR to the working directory that holds src/ (these scripts), bin/, logs/ and locks/}"
NAME=$1; shift
LOG="$W/logs/$NAME.log"
{ echo "# CMD: $*"; echo "# START $(date '+%F %T %Z') unix=$(date +%s) host=$(hostname)"; } > "$LOG"
/usr/bin/time -l "$@" >> "$LOG" 2>&1
echo "# END $(date '+%F %T %Z') unix=$(date +%s) exit=$?" >> "$LOG"
