#!/bin/zsh
# round-3 continuation worker (2026-10-20): pulls jobs from queue_r3cont.txt, one at a time, mkdir-locked;
# skips a job whose log already has an '# END' line (finished earlier).  Start 3 copies (core cap 3).
W="<WORKSPACE>/e404r3/T3b-q3-covering"
cd "$W"
ID=$1
while read -r line; do
  NAME=${line%% *}; CMD=${line#* }
  grep -q '^# END' "logs/$NAME.log" 2>/dev/null && continue
  mkdir "locks/$NAME" 2>/dev/null || continue
  echo "$(date '+%F %T') worker$ID start $NAME" >> logs/workers_r3cont.out
  src/run_job.sh "$NAME" ${=CMD}
  echo "$(date '+%F %T') worker$ID done  $NAME" >> logs/workers_r3cont.out
done < queue_r3cont.txt
echo "$(date '+%F %T') worker$ID QUEUE_EXHAUSTED" >> logs/workers_r3cont.out
