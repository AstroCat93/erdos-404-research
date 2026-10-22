#!/bin/zsh
# runs dimref on every case of the Corollary 11.19 table, 2 threads
for c in "2 1 2" "2 3 16" "2 5 16" "3 1 8" "3 2 10" "3 4 12" "3 5 13" "5 1 7" "5 2 8" "5 3 8" "7 1 5" "7 2 6" "11 1 5" "13 1 5" "17 1 4" "19 1 4" "23 1 4" "2 7 22" "2 9 22"; do
  /usr/bin/time -p <scratchpad>/r3-verify-computation/dimref ${=c} 2 2>&1
done
