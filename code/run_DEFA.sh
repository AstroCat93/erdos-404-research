#!/bin/sh
# Re-run (job 4): tracks D, E, F, A (single core; sequential).
cd "$(dirname "$0")"; OUT="$(pwd)/outputs"; mkdir -p data
# --- F: tail-coverage frontiers for p = 11, 13 (exact window checks)
( cd F && clang -O3 -o wincheck wincheck.c && clang -O3 -o wincheck2 wincheck2.c && clang -O3 -o cover cover.c )
rm -f "$OUT/F_frontier_p11.log" "$OUT/F_frontier_p13.log"
( time python3 F/frontier.py 11 11 150000 22 7 200 "$OUT/F_frontier_p11.log" ) > "$OUT"/F_frontier_p11.stdout 2>&1
( time python3 F/frontier.py 13 13 150000 26 7 220 "$OUT/F_frontier_p13.log" ) > "$OUT"/F_frontier_p13.stdout 2>&1
# --- E: residue-class trees (exact densities delta_G), frozen classes, shadows
( cd E && clang -O3 -pthread -o tree tree.c && clang -O3 -o frozen frozen.c )
mkdir -p "$OUT/E_trees"
( time E/tree 2 24 1 "$OUT/E_trees/p2" ) > "$OUT"/E_tree_p2.out 2>&1
( time E/tree 3 12 1 "$OUT/E_trees/p3" ) > "$OUT"/E_tree_p3.out 2>&1
( time E/tree 5 7 1 "$OUT/E_trees/p5" ) > "$OUT"/E_tree_p5.out 2>&1
( time E/tree 7 6 1 "$OUT/E_trees/p7" ) > "$OUT"/E_tree_p7.out 2>&1
( time E/frozen 3000 ) > "$OUT"/E_frozen_3000.out 2>&1
E/frozen 30000 > data/frozen_upto30000.txt 2>/dev/null
( cd E && time python3 shadow.py 16 ) > "$OUT"/E_shadow.out 2>&1
( cd E && time python3 checks_misc.py ) > "$OUT"/E_checks_misc.out 2>&1
# --- D: independent BFS census (gclass), halving numerics, exact deep values (multi-limb sum form)
( cd D && clang -O3 -o gclass gclass.c && clang -O3 -o halving_check halving_check.c && clang -O3 -o sumform_big sumform_big.c )
( time D/gclass 22 40 ) > "$OUT"/D_gclass22.out 2>&1
( time D/halving_check 16 ) > "$OUT"/D_halving_check16.out 2>&1
( for spec in "2 254" "2 255" "14 1533" "14 1534" "38 828" "38 829" "34 18444" "34 18445"; do set -- $spec; D/sumform_big $1 $2; done ) > "$OUT"/D_sumform_big.out 2>&1
( cd D && time python3 sumdp_check.py ) > "$OUT"/D_sumdp_check.out 2>&1
( cd D && time python3 gneg.py ) > "$OUT"/D_gneg.out 2>&1
# --- A: cross-checks of the class-density programs against the dynamics oracle; near -1 formula
( cd A && clang -O3 -o zdens zdens.c && clang -O3 -o dens2 dens2.c && clang -O3 -o gdens gdens.c )
( cd A && time python3 s8_near_minus1.py ) > "$OUT"/A_s8_near_minus1.out 2>&1
( cd A && time python3 s7_crosscheck.py ) > "$OUT"/A_s7_crosscheck.out 2>&1
echo DONE > "$OUT"/DEFA_done.txt
