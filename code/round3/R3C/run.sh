#!/bin/bash
# run.sh LOG cmd args...   -- run a command at nice 10, logging the command line, host info, start/end
# time and wall/user/sys time into LOG (round 3, track R3C).
LOG="$1"; shift
{
  echo "# command: $*"
  echo "# cwd: $(pwd)  host: $(uname -n)  cpu: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)"
  echo "# start: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
} > "$LOG"
TIMEFORMAT='# wall=%R s user=%U s sys=%S s'
{ time nice -n 10 "$@" ; } >> "$LOG" 2>&1
echo "# end: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$LOG"
