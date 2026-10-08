#!/bin/sh
# Build every C program into the locations the run scripts expect (clang or gcc, no external libraries).
# usage: sh build.sh            (from anywhere; uses $CC, default clang)
set -e
cd "$(dirname "$0")"
CC="${CC:-clang}"
mkdir -p B/bin C/bin
for p in 2 3 5 7 11 13; do $CC -O3 -DPP=$p -o B/bin/search$p B/src/search.c; done
for f in verify_bin cov cov_check2 exact_g cov_pos; do $CC -O3 -o B/bin/$f B/src/$f.c; done
for f in ecover_fast tau win2 win2_fast win2g; do $CC -O3 -o C/bin/$f C/$f.c; done
( cd A && for f in zdens dens2 gdens; do $CC -O3 -o $f $f.c; done )
( cd D && for f in gclass gdfs gdfsp gall halving_check sumform_big gsample128 gsample256 gsamplep gvalp randmodel shell_period shell_period_deep; do $CC -O3 -o $f $f.c -lm; done )
( cd E && $CC -O3 -pthread -o tree tree.c && $CC -O3 -o frozen frozen.c )
( cd F && for f in wincheck wincheck2 cover chain fourier; do $CC -O3 -o $f $f.c -lm; done )
echo "build OK"
