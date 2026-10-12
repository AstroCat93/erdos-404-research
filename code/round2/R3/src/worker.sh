#!/bin/sh
# simple job-queue worker: pops the first line of data/jobs.txt (lock via mkdir) and runs it
cd "$(dirname "$0")/.."
while :; do
  until mkdir data/.lock 2>/dev/null; do sleep 1; done
  job=$(head -n 1 data/jobs.txt)
  if [ -z "$job" ]; then rmdir data/.lock; break; fi
  tail -n +2 data/jobs.txt > data/jobs.tmp && mv data/jobs.tmp data/jobs.txt
  rmdir data/.lock
  echo "$(date '+%H:%M:%S') START $job" >> logs/worker_$1.log
  sh -c "$job"
  echo "$(date '+%H:%M:%S') END" >> logs/worker_$1.log
done
