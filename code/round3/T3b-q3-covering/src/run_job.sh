#!/bin/zsh
# usage: run_job.sh NAME CMD...   -> logs/NAME.log with command, start/end, wall time, max RSS
W="<WORKSPACE>/e404r3/T3b-q3-covering"
NAME=$1; shift
LOG="$W/logs/$NAME.log"
{ echo "# CMD: $*"; echo "# START $(date '+%F %T %Z') unix=$(date +%s) host=$(hostname)"; } > "$LOG"
/usr/bin/time -l "$@" >> "$LOG" 2>&1
echo "# END $(date '+%F %T %Z') unix=$(date +%s) exit=$?" >> "$LOG"
