#!/bin/zsh
for c in "13 13 6" "11 1 7" "7 1 9" "13 1 7" "5 1 11" "3 1 16" "2 1 27"; do
  echo "== $c"; /usr/bin/time -l <scratchpad>/r3-verify-computation/l2refw ${=c} 2>&1 | egrep -v "^ +[0-9]+ +(page|signals|voluntary|invol|messages|socket|block|swaps|instructions|cycles|peak|average)" 
done
