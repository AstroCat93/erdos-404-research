#!/bin/sh
cd "$(dirname "$0")/.."
until grep -q SUMMARY logs/U_p17_t7_H43_A.log; do sleep 15; done
nohup sh src/worker.sh w2 > /dev/null 2>&1 &
until [ -f logs/gap_done.txt ]; do sleep 15; done
nohup sh src/worker.sh w3 > /dev/null 2>&1 &
