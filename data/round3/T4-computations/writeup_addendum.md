# Track T4b-finish — addendum to the T4 report (round 3, Erdős #404), 2026-10-20

Work dir: `e404r3/T4-computations/` (this file, `code/t4b_final.py`, `data/results_final.json`, `logs/t4b_*.{log,out}` are the additions of this task; nothing was deleted). Everything below is [computer-assisted] unless marked otherwise; nothing is human-refereed. The mathematics is unchanged from `writeup.md`; this addendum (i) confirms that every queued run completed, (ii) re-runs the first-attempt post-processors and an independently written one on the complete data, (iii) delivers the tables the task asked for, and (iv) records the sanity checks against the exact census and Kitamura's table.

## A. Status of the queued runs [verified from logs and file contents]

All runs launched by T4 on 2026-10-12 completed (`logs/annealed.log` ends `ALLDONE`, `logs/queue.log` ends `QUEUEDONE`, `logs/deep.log` ends `DEEPDONE`). Completeness was checked on the files, not the logs: each `annealed_p*_G*.txt` has its `total classes=... maxN=...` line with the bucket rows summing to the totals (asserted in `code/t4b_final.py` for all 42 cases); each `mc_cap*.txt` has exactly `CAP+1` monotone `k=` rows, `surv(0)=ns`, `overflow_samples=0`; each `surv_cap*.txt` has 4096 rows and no `-1`.

| run | command | wall time | output |
|---|---|---|---|
| annealed p=7 G=9 | `src/annealed 7 9 4` | 3932 s (65.5 min; 4 threads, over the 45-min cap: launched by T4, not re-run) | `data/annealed_p7_G9.txt` |
| annealed p=5 G=11 | `src/annealed 5 11 4` | 490 s | `data/annealed_p5_G11.txt` |
| annealed p=2 G=28 | `src/annealed 2 28 4` | 127 s | `data/annealed_p2_G28.txt` |
| annealed p=3 G=17 | `src/annealed 3 17 4` | 111 s | `data/annealed_p3_G17.txt` |
| survivors cap 1022 / 2046 / 4094 | `src/gsample_nl{17,33,65} -1 0 CAP 4096 4` | 2 / 10 / 38 s | `data/surv_cap{1022,2046,4094}.txt` |
| MC cap 126 / 256 / 512 / 1024 / 2046 | `src/gsample_nl{2,5,9,17,33} ns seed CAP 4` | 155 / 375 / 141 / 353 / 324 s | `data/mc_cap*.txt` |
| gate sums p=11 / 13 | `src/gatesum 11 8 4 16`, `13 8 4 12` | 12 / 152 s | `data/gatesum_p{11,13}.txt` |
| deep lifts | `code/p2add CAP a 22` | 0.5–116 s | `data/deep_lift.txt` |

Nothing had to be re-run. One remark for the record: the $p=7$, $G=9$ annealed run took 65.5 min of wall time on 4 threads, exceeding the 45-min guideline; it was already finished before this task started and its output passed the internal consistency assertions, so it was kept.

## B. Post-processors re-run on the complete data [verified]

`python3 -I` on `src/annealed_post.py`, `src/surv_post.py`, `src/mc_post.py`, `src/assemble_results.py`, `code/post_extra.py`, `code/assemble_retry.py` (each < 0.1 s; `logs/t4b_postproc_rerun.log`). The regenerated `annealed_summary.tsv`, `survivors_NAG.tsv`, `delta_G2_montecarlo.tsv`, `annealed_overview.tsv`, `annealed_buckets.tsv`, `kitamura_11p5_comparison.tsv` and `results_retry.json` are byte-identical to the versions left by T4 (`cmp` / JSON equality), i.e. T4's tables were already computed on the complete data.

Independent re-derivation: `code/t4b_final.py` (this task; shares no code with `src/*_post.py`) parses only the raw program outputs, the note's exact census `publish-erdos404/review/computation/census_p2_32.out` and `kitamura/p2_exact_table_1_256.csv`, recomputes every quantity with exact rationals, and writes `data/results_final.json` (`logs/t4b_final.out`). Every number below comes from that script; all agree with `writeup.md` §1–4 to the printed precision.

## C. Extended annealed tables (exact; `results_final.json["annealed_all"]`)

Deepest levels per prime, all classes mod $p^G$ ($Z_G=p^G2^{-M_G}N_G$):

| $p$ | $G$ | $M_G$ | $\delta_G$ (exact) | $EZ$ | $EZ^2$ | $EZ^2/(EZ)^2$ | $EZ^2/(p^G/4)$ | $E[Z\mid Z>0]$ |
|---|---|---|---|---|---|---|---|---|
| 2 | 26 | 29 | 0.1236173 | 20.6152 | $3.3332\cdot10^7$ | $7.843\cdot10^4$ | 1.9867 | 166.8 |
| 2 | 27 | 31 | 0.1193804 | 22.0459 | $6.6665\cdot10^7$ | $1.372\cdot10^5$ | 1.9868 | 184.7 |
| 2 | 28 | 31 | 0.1164025 (=31 246 552/$2^{28}$) | 23.6162 | $1.3334\cdot10^8$ | $2.391\cdot10^5$ | 1.9869 | 202.9 |
| 3 | 16 | 35 | 0.3636087 | 7.8693 | $1.5827\cdot10^7$ | $2.556\cdot10^5$ | 1.4707 | 21.6 |
| 3 | 17 | 35 | 0.3632933 (=46 915 750/$3^{17}$) | 8.3770 | $4.748\cdot10^7$ | $6.766\cdot10^5$ | 1.4707 | 23.1 |
| 5 | 10 | 44 | 0.5216163 | 4.5506 | $3.0072\cdot10^6$ | $1.452\cdot10^5$ | 1.2317 | 8.72 |
| 5 | 11 | 49 | 0.5216023 (=25 468 861/$5^{11}$) | 4.9587 | $1.5036\cdot10^7$ | $6.115\cdot10^5$ | 1.2317 | 9.51 |
| 7 | 8 | 48 | 0.6239378 | 3.6519 | $1.618\cdot10^6$ | $1.213\cdot10^5$ | 1.1227 | 5.85 |
| 7 | 9 | 55 | 0.6239187 (=25 177 371/$7^9$) | 4.0413 | $1.1326\cdot10^7$ | $6.935\cdot10^5$ | 1.1227 | 6.48 |

The full table (42 cases: $p=2$, $G=4,8,12,16,18,20,22,24,26,27,28$; $p=3$, $G=2,4,6,8,10,\dots,17$; $p=5$, $G=2..11$; $p=7$, $G=1..9$) is in the JSON. Proposition 2 ($EZ^2\ge p^G/4$) holds in all 42 cases (asserted). $EZ$ slopes between the two deepest levels: $1.57$ ($p=2$, $27\to28$; the average slope over $G=16..28$ is $\approx1.2$, the local value jumps where $M_G$ jumps), $0.508$ ($p=3$), $0.408$ ($p=5$), $0.389$ ($p=7$). $\delta_G$ reproduces the note's §4.7 values exactly at every overlapping level; $\delta_{11}(5)$ and $\delta_9(7)$ are new relative to the note (as T4 reported).

**Conditioned moments $E[\,\cdot\mid \mathrm{maxv}\le K]$ including the new $G$** (`results_final.json["annealed_conditioned"]`; measure of $\{\mathrm{maxv}\le K\}$, $E[Z\mid\cdot]$, $E[Z^2\mid\cdot]$, ratio):

| $p$ | $K$ | $G$ | measure | $EZ$ | $EZ^2$ | ratio |
|---|---|---|---|---|---|---|
| 2 | 6 | 24 / 26 / 27 / 28 | .789 / .773 / .758 / .758 | 3.94 / 4.02 / 4.02 / 4.03 | 300 / 307 / 314 / 322 | 19.3 / 19.0 / 19.4 / **19.8** |
| 2 | 8 | 24 / 26 / 27 / 28 | .947 / .943 / .939 / .939 | 6.14 / 6.10 / 6.10 / 6.11 | 1546 / 1541 / 1548 / 1558 | 41.0 / 41.5 / 41.6 / **41.8** |
| 2 | 10 | 24 / 26 / 27 / 28 | .987 / .986 / .985 / .985 | 8.24 / 8.25 / 8.44 / 8.70 | 5381 / 5715 / 6276 / 7640 | 79.2 / 84.0 / 88.2 / **101.0** |
| 2 | 12 | 24 / 26 / 27 / 28 | .997 / .996 / .996 / .996 | 10.2 / 10.5 / 10.8 / 11.1 | 17950 / 20890 / 25000 / 26350 | 172 / 191 / 213 / **214** |
| 3 | 4 | 14 / 15 / 16 / 17 | .881 / .868 / .856 / .856 | 1.93 / 1.96 / 1.97 / 1.97 | 48.8 / 49.4 / 50.5 / 50.6 | 13.1 / 12.9 / 13.0 / **13.0** |
| 3 | 5 | 14 / 15 / 16 / 17 | .960 / .956 / .952 / .952 | 2.45 / 2.46 / 2.47 / 2.47 | 158 / 162 / 163 / 162 | 26.5 / 26.7 / 26.6 / **26.5** |
| 3 | 7 | 14 / 15 / 16 / 17 | .996 / .995 / .995 / .995 | 3.49 / 3.50 / 3.52 / 3.52 | 1412 / 1396 / 1446 / 1467 | 115.7 / 113.9 / 116.7 / **118.2** |
| 5 | 3 | 8 / 9 / 10 / 11 | .946 / .938 / .930 / .922 | 1.64 / 1.65 / 1.66 / 1.66 | 35.2 / 35.9 / 36.2 / 36.5 | 13.1 / 13.2 / 13.2 / **13.2** |
| 5 | 4 | 8 / 9 / 10 / 11 | .989 / .988 / .986 / .984 | 2.01 / 2.01 / 2.02 / 2.02 | 162 / 163 / 165 / 165 | 40.3 / 40.3 / 40.6 / **40.5** |
| 5 | 5 | 8 / 9 / 10 / 11 | .998 / .998 / .997 / .997 | 2.41 / 2.40 / 2.41 / 2.41 | 811 / 798 / 798 / 818 | 140 / 138 / 138 / **140** |
| 7 | 2 | 6 / 7 / 8 / 9 | .880 / .860 / .860 / .840 | 1.26 / 1.27 / 1.27 / 1.22 | 11.8 / 12.1 / 12.1 / 10.6 | 7.42 / 7.46 / 7.46 / **7.11** |
| 7 | 3 | 6 / 7 / 8 / 9 | .983 / .980 / .980 / .977 | 1.60 / 1.60 / 1.60 / 1.60 | 72.7 / 73.0 / 73.0 / 73.0 | 28.4 / 28.4 / 28.4 / **28.6** |
| 7 | 4 | 6 / 7 / 8 / 9 | .998 / .997 / .997 / .997 | 1.98 / 1.98 / 1.98 / 1.98 | 498 / 499 / 498 / 498 | 127.4 / 127.6 / 127.3 / **127.4** |

The new levels do not change T4's reading (§1.5 of `writeup.md`): for odd $p$ the conditioned moments are flat in $G$ to 1–3 % (the $p=7$, $K=2$ dip at $G=9$ is the bucket $\mathrm{maxv}=2$ losing measure as $M_G$ grows from 48 to 55), while for $p=2$ they keep growing ($K=10$: $79\to101$; $K=12$: $172\to214$ over $G=24\to28$). Per-bucket contributions to $EZ$ at the deepest level: $p=2$, $G=28$: $1.0002,1.0001,1.0002,1.0000,1.0000,1.0000$ for $\mathrm{maxv}=16..21$ (reproduced); $p=3$, $G=17$: $0.50$–$0.54$ for $\mathrm{maxv}=8..13$; $p=5$, $G=11$: $0.40$–$0.41$ ($6..9$); $p=7$, $G=9$: $0.39$–$0.40$ ($5..8$).

## D. Survivor table $N(A,G)=\#\{a\le A: g_2(a)\ge G\}$ at caps 1022 / 2046 / 4094 (exact)

Caps 32, 254, 1022, 2046, 4094 each give 4096 values, no population overflow, 0 mismatches of $g_{c_1}(a)=\min(g_{c_2}(a),c_1)$ over all 10 cap pairs; all odd $a$ have $g_2=0$; for $G\le12$ and $A\in\{256,1024,4096\}$, $N(A,G)/A$ equals the exact census $\delta_G$ (asserted: locality). Columns: $N(256,G)$, $N(1024,G)$, $N(4096,G)$; $NG/A$ and $N\sqrt G/A$ for the three $A$.

| $G$ | $N_{256}$ | $N_{1024}$ | $N_{4096}$ | $NG/A$ (256 / 1024 / 4096) | $N\sqrt G/A$ (256 / 1024 / 4096) | $\delta_G$ |
|---|---|---|---|---|---|---|
| 8 | 62 | 248 | 992 | 1.94 / 1.94 / 1.94 | .685 / .685 / .685 | .242188 exact |
| 16 | 38 | 158 | 622 | 2.38 / 2.47 / 2.43 | .594 / .617 / .607 | .151703 exact |
| 32 | 26 | 102 | 411 | 3.25 / 3.19 / 3.21 | .575 / .564 / .568 | .101636 exact |
| 48 | 22 | 76 | 314 | 4.13 / 3.56 / 3.68 | .595 / .514 / .531 | — |
| 64 | 18 | 64 | 263 | 4.50 / 4.00 / 4.11 | .563 / .500 / .514 | .06416(4) MC |
| 96 | 17 | 48 | 198 | 6.38 / 4.50 / 4.64 | .651 / .459 / .474 | .04855(3) MC |
| 128 | 14 | 39 | 167 | 7.00 / 4.88 / 5.22 | .619 / .431 / .461 | .03770(4) MC |
| 192 | 9 | 23 | 118 | 6.75 / 4.31 / 5.53 | .487 / .311 / .399 | .02698(4) MC |
| 256 | 5 | 15 | 85 | 5.00 / 3.75 / 5.31 | .313 / .234 / .332 | .02052(3) MC |
| 384 | 5 | 13 | 55 | 7.50 / 4.88 / 5.16 | .383 / .249 / .263 | .01425(8) MC |
| 512 | 5 | 11 | 40 | 10.0 / 5.50 / 5.00 | .442 / .243 / .221 | .01068(7) MC |
| 768 | 3 | 7 | 27 | 9.00 / 5.25 / 5.06 | .325 / .189 / .183 | .00758(9) MC |
| 1022 | 2 | 6 | 20 | 7.98 / 5.99 / 4.99 | .250 / .187 / .156 | — |
| 1024 | 2 | 6 | 20 | 8.00 / 6.00 / 5.00 | .250 / .188 / .156 | .00562(7) MC |
| 1536 | 1 | 4 | 13 | 6.00 / 6.00 / 4.88 | .153 / .153 / .124 | .00370(14) MC |
| 2046 | 1 | 4 | 13 | 7.99 / 7.99 / 6.49 | .177 / .177 / .144 | .00266(12) MC |
| 3072 | 1 | 4 | 10 | 12.0 / 12.0 / 7.50 | .217 / .217 / .135 | — |
| 4094 | 1 | 2 | 5 | 16.0 / 8.00 / 5.00 | .250 / .125 / .078 | — |

Survivors to cap 4094: $a=34,594,1102,2210,3456$. Reading unchanged: at $A=4096$ the column $NG/A$ is flat at $5.0$–$7.5$ from $G=128$ to $4094$ while $N\sqrt G/A$ falls from $0.46$ to $0.08$; with only $N\le20$ survivors beyond $G=1024$ the Poisson noise is $\gtrsim20\%$, so this is consistent with $\delta_G\approx5.5/G$ and not with $c/\sqrt G$.

**Kitamura check.** `kitamura/p2_exact_table_1_256.csv` has 256 rows ($a=1..256$), all `status=exact` (methods: 128 `odd_formula`, 96 `bisect_dp`, 31 `normalized_dp`, 1 `scaled_gate_dp` for $a=34$). The numbers $594,1102,2210,3456$ are outside the table; for $594$ Kitamura's `README.md` (l. 349) states only the lower bound $f(594,2)\ge66126$, i.e. $g_2(594)\ge65536$, "no death found yet", consistent with our survival to cap 16382. Per-$a$: $\min(g^{\rm Kit}(a),4094)=g^{\rm ours}_{4094}(a)$ for all 256 $a$, **0 mismatches**. $N(256,G)$ from Kitamura's table versus ours at $G=1,2,4,8,16,24,32,48,64,96,128,192,256,384,512,768,1024,1536,2048,4094$: identical at all 20 levels ($128,128,96,62,38,32,26,22,18,17,14,9,5,5,5,3,2,1,1,1$).

**Deep lifts, reproducibility re-run** (`logs/t4b_p2add_recheck.log`): `code/p2add 4900 3456 22` $\to g_2(3456)=4823$ (0.6 s); `p2add 6300 2210 22` $\to g_2(2210)=6261$ (2.2 s); `p2add 1600 14 22` $\to g_2(14)=1522$ (0.07 s). Same values as T4 and as Kitamura's $f(3456,2)=8275$, $f(14,2)=1533$.

## E. Monte Carlo $\delta_G(2)$ (exact decision per sample; `results_final.json["delta_G2_estimates"]`)

Runs (cap: samples, seed, max population, overflow): 126: $4\cdot10^7$, 20261012, 4835, 0; 256: $2\cdot10^7$, 20261013, 15135, 0; 512: $2\cdot10^6$, 20261014, 34936, 0; 1024: $10^6$, 20261015, 100994, 0; 2046: $2\cdot10^5$, 20261016, 159288, 0.

**Sanity check against the exact census at every $G\le32$** (census from `publish-erdos404/review/computation/census_p2_32.out`, which agrees with `archive/E/tree_p2.txt` to $G=29$): for each of the 5 runs and each $G=1,\dots,32$, $z=(\hat\delta_G-\delta_G)/\sqrt{\delta_G(1-\delta_G)/n_s}$. Result over the 160 tests: $\max|z|=2.26$ (cap-2046 run, $G=1,2,3$: $100\,506/200\,000=0.50253$ vs $1/2$; these three are one event, since $\delta_1=\delta_2=\delta_3=1/2$ is the fraction of even $x$), 3 tests with $|z|>2$, none with $|z|>3$; per run $\max|z|=1.21,1.97,0.95,1.99,2.26$ for caps $126,256,512,1024,2046$. (Within one run the $G$-values are nested and strongly correlated, so 160 is an upper bound on the effective number of tests.) The Monte Carlo is consistent with the exact census throughout.

**Estimates.** "best" = run with the most samples at that $G$; "pooled" = inverse-variance pooling of all runs with cap $\ge G$ (independent seeds); $\pm$ = binomial standard error.

| $G$ | $\delta_G$ best | $\pm$ | run | $\delta_G$ pooled | $\pm$ | $\delta_GG$ | $\delta_G\sqrt G$ | $2\delta_GG$ |
|---|---|---|---|---|---|---|---|---|
| 64 | 0.06416 | 0.00004 | 126 | 0.06415 | 0.00003 | 4.107 | 0.513 | 8.21 |
| 96 | 0.04855 | 0.00003 | 126 | 0.04854 | 0.00003 | 4.661 | 0.476 | 9.32 |
| **126** | **0.03829** | **0.00003** | 126 | 0.03829 | 0.00002 | 4.825 | 0.430 | 9.65 |
| 128 | 0.03770 | 0.00004 | 256 | 0.03769 | 0.00004 | 4.825 | 0.427 | 9.65 |
| 192 | 0.02698 | 0.00004 | 256 | 0.02697 | 0.00003 | 5.180 | 0.374 | 10.36 |
| **256** | **0.02052** | **0.00003** | 256 | 0.02051 | 0.00003 | 5.253 | 0.328 | 10.51 |
| 384 | 0.01425 | 0.00008 | 512 | 0.01432 | 0.00007 | 5.473 | 0.279 | 10.95 |
| **512** | **0.01068** | **0.00007** | 512 | 0.01073 | 0.00006 | 5.469 | 0.242 | 10.94 |
| 768 | 0.00758 | 0.00009 | 1024 | 0.00756 | 0.00008 | 5.821 | 0.210 | 11.64 |
| **1024** | **0.00562** | **0.00007** | 1024 | 0.00562 | 0.00007 | 5.758 | 0.180 | 11.52 |
| 1536 | 0.00370 | 0.00014 | 2046 | 0.00370 | 0.00014 | 5.691 | 0.145 | 11.38 |
| **2046** | **0.00266** | **0.00012** | 2046 | 0.00266 | 0.00012 | 5.442 | 0.120 | 10.88 |

**Least-squares fits $\delta_G\approx CG^{-c}$** (log–log; weights $(\delta/\sigma)^2$ for "weighted"; best-run values; the $G=126$ point is omitted as a near-duplicate of 128):

| range | points | weighted $C$, $c$ | $\chi^2/$dof | unweighted $C$, $c$ |
|---|---|---|---|---|
| $[64,2046]$ | 11 | $1.921$, $0.813\pm0.001$ | $4593/9$ | $3.260$, $0.921$ |
| $[128,2046]$ | 9 | $2.803$, $0.886\pm0.002$ | $307/7$ | $3.989$, $0.951$ |
| $[256,2046]$ | 7 | $3.568$, $0.930\pm0.005$ | $19.2/5$ | $4.700$, $0.975$ |
| $[512,2046]$ | 5 | $3.767$, $0.939\pm0.016$ | $14.1/3$ | $5.923$, $1.007$ |

The pooled estimates give the same fits to $\pm0.004$ in $c$. The $\chi^2$ values say plainly that **a single power law does not describe $[64,2046]$** (the weighted fit is dominated by the ultra-precise low-$G$ points and its formal $\pm0.001$ is meaningless as a model error); the exponent drifts upward with $G$. The alternative form $\delta_GG=a+b/G$ fitted on $G\ge256$ (weighted) gives $a=5.64$, $b=-64$, i.e. $\delta_G\approx5.64/G-64/G^2$, which is the "$\delta_GG\to5.5$–$5.8$" reading of T4 with a finite-size correction; it is a description, not a theorem.

**Local exponents** $c_{G_1\to G_2}=-\log(\delta_{G_2}/\delta_{G_1})/\log(G_2/G_1)$ with propagated errors: $64\to96$: $0.688(2)$; $96\to128$: $0.880(5)$; $128\to192$: $0.825(4)$; $192\to256$: $0.951(7)$; $256\to384$: $0.899(15)$; $384\to512$: $1.003(31)$; $512\to768$: $0.846(33)$; $768\to1024$: $1.038(61)$; $1024\to1536$: $1.029(96)$; $1536\to2046$: $1.156(198)$. From $G\approx384$ on, every local exponent is within $2\sigma$ of $1$ (the $512\to768$ value $0.846(33)$ is the only one more than $3\sigma$ below 1, and it pairs with $1.003$ before and $1.038$ after it). [heuristic reading: consistent with $\delta_G(2)\asymp1/G$; the $G^{-1/2}$ regime of $G\le128$ is transient.]

## F. Gate-block ratios for $p=11,13$ (and 5, 7 for comparison; double precision)

$B(p,i)=p^i(1-1/p)I_p$, $I_p=\int_0^1\prod_{u<p}|\cos(\pi e_u\theta)|d\theta$ by Gauss–Legendre on the $(p-1)!$ unit pieces.

| $p$ | $I_p$ (nodes) | second node count | $I_p/(2/\pi)^p$ | $L^{\rm unit}(p,i)/B(p,i)$, $i=1..8$ |
|---|---|---|---|---|
| 5 | 0.1220287868 (16) | — | 1.16698 | 0.5726, 1.1313, 0.9168, 1.00026, 1.000027, 1.0000004, 1.0000000, 1.0000000 |
| 7 | 0.0496033637 (16) | — | 1.17044 | 0.6825, 0.5361, 1.0024, 1.0047, 0.99946, 0.9999961, 1.0000000, 1.0000000 |
| 11 | 0.00816212220575 (16) | 0.00816212220551 (32) | 1.17252 | 0.7396, 1.5673, 0.9116, 1.00008, 0.99931, 0.99970, 1.0000287, 1.0000000 |
| 13 | 0.00330918392005 (12) | 0.00330918392125 (8) | 1.17295 | 0.1963, 0.9610, 0.8659, 1.0285, 0.99772, 0.99992, 1.0000067, 1.0000000 |

(Ratios printed to 7 decimals; the $i=8$ values differ from 1 by less than $5\cdot10^{-8}$ for all four primes. The all-residue ratios $L^{\rm all}/(p^iI_p)$ converge too: $0.99998$, $1.00000$, $1.00000$, $1.00000$ at $i=8$.) The node-count checks agree to $3\cdot10^{-11}$ ($p=11$) and $4\cdot10^{-10}$ ($p=13$) relative. The sequence $I_p/(2/\pi)^p=1.1670,1.1704,1.1725,1.1729$ is the "$\approx1.17$" of note §10.5.

## G. Gaps

- Same as `writeup.md` §5: every limit/rate statement is a reading of finite data; the only proved items are Lemmas 1–3, Proposition 2, and the DP correctness. This addendum adds no theorem.
- The power-law fits are descriptive; the $\chi^2$ shows the model is wrong on wide ranges. The $1/G$ reading rests on the local exponents for $G\ge384$, which have 3–20 % errors.
- $g_2(594)$: Kitamura reports the lower bound $g_2(594)\ge65536$ (README l. 349, not in the exact table); we only reached cap 16382 (population $2.1\cdot10^6$ at cap 16382; a cap of 65537 would need roughly $4\times$ the population and more than the $2^{22}$ limit, so it was not attempted within this task's budget).
- The $p=7$, $G=9$ annealed run (65 min) exceeded the per-run time guideline; it was launched by T4, not by this task.
- All checks against Kitamura compare values only; Kitamura's witness files were not re-verified.

## H. Commands (this task; all < 3 s each, 1 core)

```
cd e404r3/T4-computations
python3 -I src/annealed_post.py; python3 -I src/surv_post.py; python3 -I src/mc_post.py
python3 -I src/assemble_results.py; python3 -I code/post_extra.py; python3 -I code/assemble_retry.py   # logs/t4b_postproc_rerun.log
python3 -I code/t4b_final.py > logs/t4b_final.out      # writes data/results_final.json (1 s)
./code/p2add 4900 3456 22; ./code/p2add 6300 2210 22; ./code/p2add 1600 14 22   # logs/t4b_p2add_recheck.log
```

Credit as in `writeup.md` §7 (Kitamura's table and records; Tao, Kovač, Lin; round-1/2 tracks). The exact census used in §E is the note's (round 1 track E / D and the round-2 computational referee).

## I. Re-verification on 2026-10-21 (second instance of T4b-finish) [computer-assisted]

The first instance of this task (2026-10-20) wrote §A–H above and `data/results_final.json` but was cut off before returning its structured result. This instance re-derived everything it relies on instead of trusting the file:

- `python3 -I code/t4b_final.py` re-run (0.1 s): the regenerated `data/results_final.json` is identical to the 2026-10-20 file except the `generated` timestamp (JSON equality asserted).
- `code/t4b_indep_check.py` (new, 2026-10-21; written without reading `t4b_final.py`, parses only the raw `mc_cap*.txt`, `surv_cap*.txt`, `gatesum_p*.txt`, the note's census and Kitamura's CSV; output in `logs/t4b_indep_check_2026-10-21.out`) reproduces: all five Monte Carlo files complete and monotone with 0 overflows; max $|z|$ versus the exact census over $G\le32$ = 1.21, 1.97, 0.95, 1.99, 2.26 for caps 126, 256, 512, 1024, 2046; every $\delta_G$ estimate, standard error and $\delta_GG$ of the table in §E; the four weighted fits ($c=0.813, 0.886, 0.930, 0.939$; $\chi^2=4593, 307, 19.2, 14.1$) and unweighted exponents ($0.921, 0.951, 0.975, 1.007$); all ten local exponents with errors; the cap-consistency $g_{1022}=\min(g_{2046},1022)$, $g_{2046}=\min(g_{4094},2046)$ for all 4096 $a$; $N(A,G)$ for $A=256,1024,4096$ at the eleven $G$ of §D; survivors $\{34,594,1102,2210,3456\}$; $N(4096,8)/4096=\delta_8$ exactly; Kitamura comparison with the correct conversion $g_2(a)=f(a,2)-v_2(a!)$: 0 mismatches over $a\le256$ and identical $N(256,G)$ at all 20 levels; $f(2210,2)=2206+6261=8467$; the gate-block ratios for $p=11,13$ at $i=1..8$ and $I_p/(2/\pi)^p=1.17252, 1.17295$, with the second-node-count integrals agreeing to $2.4\cdot10^{-13}$ absolute ($p=11$) and $1.2\cdot10^{-12}$ ($p=13$).
- A note for anyone re-checking Kitamura's CSV: its `value` column is $f(a,2)=v_2(a!)+g_2(a)$, not $g_2(a)$; comparing it to the capped $g_2$ without subtracting $v_2(a!)$ produces 255 spurious mismatches (the only agreement being $a=1$). The §D statement "0 mismatches" uses the correct conversion.
- $N(4096,G)/4096$ versus the census: equal at $G=8$ ($0.2421875$), but $0.15186$ vs $0.15170$ at $G=16$ and $0.10034$ vs $0.10164$ at $G=32$; so the locality statement in §D holds for $G\le12$ as written (the census class size $2^G$ exceeds $A=4096$ beyond that), not for all $G$.

Nothing in §A–H needed correction. No new runs were launched (all queued runs were already complete); total compute of this instance < 2 s on 1 core.
