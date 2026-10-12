#!/bin/sh
# job-queue worker for the lead's re-runs: pops lines of data/rerun_jobs.txt
cd "$(dirname "$0")/.."
while :; do
  until mkdir data/.rlock 2>/dev/null; do sleep 1; done
  job=$(head -n 1 data/rerun_jobs.txt)
  if [ -z "$job" ]; then rmdir data/.rlock; break; fi
  tail -n +2 data/rerun_jobs.txt > data/rerun_jobs.tmp && mv data/rerun_jobs.tmp data/rerun_jobs.txt
  rmdir data/.rlock
  echo "$(date '+%F %T') START $job" >> ../outputs/R3/worker_$1.log
  /usr/bin/time -p sh -c "$job" 2>> ../outputs/R3/worker_$1.log
  echo "$(date '+%F %T') END" >> ../outputs/R3/worker_$1.log
done
