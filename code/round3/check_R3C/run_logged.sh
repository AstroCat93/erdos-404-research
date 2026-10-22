#!/bin/bash
# run_logged.sh LOG VMEM_KB cmd args...  (check of track R3C, round 3, 2026-10-13)
# Runs cmd at nice 10 under a virtual-memory cap (ulimit -v VMEM_KB; 0 = no cap) and writes the
# command, binary sha256, start/end time and wall/user/sys time into LOG.
LOG="$1"; VM="$2"; shift 2
{
  echo "# command: $*"
  for a in "$@"; do case "$a" in /*) [ -x "$a" ] && echo "# binary sha256: $(sha256sum "$a" | cut -c1-16)  $a";; esac; done
  echo "# host: $(uname -n)  cpu: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)  vmem cap (KB): $VM"
  echo "# start: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
} > "$LOG"
TIMEFORMAT='# wall=%R s user=%U s sys=%S s'
if [ "$VM" != 0 ]; then
  { time ( ulimit -v "$VM"; exec nice -n 10 "$@" ) ; } >> "$LOG" 2>&1
else
  { time nice -n 10 "$@" ; } >> "$LOG" 2>&1
fi
echo "# exit status: $?" >> "$LOG"
echo "# end: $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> "$LOG"
