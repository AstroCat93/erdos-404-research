#!/bin/zsh
# sequential batch (1 core); each line: p w K
cd "${0:A:h}/.."
for a in "2 7 22" "2 9 20" "2 9 22" "3 1 8" "3 2 10" "3 4 12" "3 5 13" "5 1 7" "5 2 8" "5 3 8" "7 1 5" "7 2 6" "13 1 5" "13 2 4" "11 1 5" "17 1 4" "19 1 4" "23 1 4"; do
  echo "### $(date -u +%FT%TZ) wdim $a"
  /usr/bin/time -p ./code/wdim ${=a}
done
echo "### done $(date -u +%FT%TZ)"
