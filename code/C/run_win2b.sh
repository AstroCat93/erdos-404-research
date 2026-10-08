#!/bin/zsh
# usage: run_win2b.sh p jstart maxbits   (stops at the first t0 that is not FULL)
p=$1; j=$2; maxbits=$3
while true; do
  bits=$(python3 -c "print($p**($j+2))")
  if python3 -c "import sys; sys.exit(0 if $bits <= $maxbits else 1)"; then :; else echo "p=$p j=$j skipped (p^(j+2)=$bits > maxbits)"; break; fi
  allfull=1
  for t in $(seq 1 $((p-1))); do
    out=$(./win2 $p $j $t); echo "$out"
    case "$out" in *FULL*) ;; *) allfull=0; break;; esac
  done
  if [ $allfull = 1 ]; then echo "LEVEL p=$p j=$j : ALL t FULL (2-block window crosses every level-$j gate)"; else echo "LEVEL p=$p j=$j : NOT all full"; break; fi
  j=$((j+1))
done
