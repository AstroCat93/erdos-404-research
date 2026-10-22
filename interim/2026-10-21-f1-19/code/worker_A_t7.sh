#!/bin/zsh
# W3: after validation finishes, A' uniform Cov(19,7,45) over the remaining classes K' mod 361 (19..360, 19 !| K'), in chunks of 36 classes (~40 min each)
W="${T3B_WORKDIR:?set T3B_WORKDIR to the working directory that holds src/ (these scripts), bin/, logs/ and locks/}"
cd "$W"
while ! grep -q VALBIG_DONE logs/val_big.out 2>/dev/null; do sleep 30; done
python3 -c "
Ks=[K for K in range(19,361) if K%19]
for j in range(0,len(Ks),36): print(' '.join(map(str,Ks[j:j+36])))
" > data_p19_t7_classes.txt
i=0
while read -r line; do
  i=$((i+1))
  src/run_job.sh U19_t7_H45_A_chunk$i bin/fibcov_ip 19 7 45 2 pos ${=line}
done < data_p19_t7_classes.txt
echo W3_DONE >> logs/workers.out
