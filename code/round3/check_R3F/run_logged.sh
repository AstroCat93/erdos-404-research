#!/bin/sh
# usage: run_logged.sh LOGFILE command...   (runs under nice -n 10; header with command, footer with wall time)
log="$1"; shift
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
start=$(date +%s.%N)
{ echo "# command: $*"; echo "# start: $(date -u +%Y-%m-%dT%H:%M:%SZ)"; } > "$log"
nice -n 10 "$@" >> "$log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "# end: $(date -u +%Y-%m-%dT%H:%M:%SZ)  exit=$rc  wall_seconds=$(echo "$end - $start" | bc)" >> "$log"
