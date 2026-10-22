#!/bin/zsh
W="${T3B_WORKDIR:?set T3B_WORKDIR to the working directory that holds src/ (these scripts), bin/, logs/ and locks/}"
cd "$W"
src/run_job.sh VAL_A_p11_t7_H40_K37 bin/fibcov_ip 11 7 40 3 pos 37
src/run_job.sh VAL_C_p11_t7_H40_K37 bin/covchk_ip 11 7 40 3 pos 37
src/run_job.sh VAL_A_p17_t7_H42_K6 bin/fibcov_ip 17 7 42 2 pos 6 7
src/run_job.sh VAL_C_p17_t7_H42_K6 bin/covchk_ip 17 7 42 2 pos 6 7
src/run_job.sh VAL_A_p19_t7_H44 bin/fibcov_ip 19 7 44 2 pos 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
src/run_job.sh VAL_C_p19_t7_H44 bin/covchk_ip 19 7 44 2 pos 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
echo VALBIG_DONE
