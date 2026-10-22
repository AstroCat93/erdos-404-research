# Track T4 (computations), round 3, Erdős #404 — 2026-10-12

Work dir: `e404r3/T4-computations/` (`src/` programs, `data/` outputs, `logs/` timings, `kitamura/` read-only fetches, `data/results.json` machine-readable aggregate). All arithmetic in items (1)–(3) is exact integer/residue arithmetic; item (4) is double precision (diagnostic, not a certificate). Every label below is one of [proved] / [computer-assisted] / [heuristic] / [conjecture] / [sketch].

**Status of the runs at the time of writing.** The harness forced the final report at ~14:46 local time while a background batch was still running (launched with `nohup`, 4 threads, each run ≤ 45 min; see §6). Everything reported below was complete and checked when written. Runs listed in §6 as "pending" may have finished later and written files into `data/` (`annealed_p5_G11.txt`, `annealed_p7_G9.txt`, `annealed_p2_G28.txt`, `surv_cap1022/2046/4094.txt`, `gatesum_p11/p13.txt`, `mc_cap256/512/1024/2046.txt`); those files were **not** inspected by this track and the post-processors `src/*_post.py` + `src/assemble_results.py` must be re-run on them before use.

---

## 1. Annealed moments (task 1)

### 1.1 The cutoff $M_G$ [proved]

**Lemma 1.** For $x\in\mathbb Z_p$ and $b\ge1$, $b!\mid\pi_b(x)=(x+1)\cdots(x+b)$ in $\mathbb Z_p$. Hence $v_p(\pi_b(x))\ge v_p(b!)$ for all $x$, with equality at $x=0$. Consequently
$$M_G:=\min\{M:\ \pi_b(x)\equiv0\ (\mathrm{mod}\ p^G)\ \forall x\in\mathbb Z_p,\ \forall b>M\}=\max\{b: v_p(b!)<G\},$$
and $M_G\le pG-1$.

*Proof.* $\pi_b(x)/b!=\binom{x+b}{b}$ is a polynomial with rational coefficients taking integer values on $\mathbb N$; $\mathbb N$ is dense in $\mathbb Z_p$ and $\mathbb Z_p$ is closed, so it takes values in $\mathbb Z_p$ on $\mathbb Z_p$. Equality at $x=0$ is $\pi_b(0)=b!$. Since $v_p(b!)$ is nondecreasing in $b$, "$v_p(\pi_b(x))\ge G$ for all $x$ and all $b>M$" holds iff $v_p((M+1)!)\ge G$, giving the formula; $v_p((pG)!)\ge G$ gives $M_G\le pG-1$. ∎

The program computes $M_G$ by this formula (values: $M_G=5,9,15,17,19,23,23,27,29$ for $p=2$, $G=4,8,12,16,18,20,22,24,26$; $M_G=26$ for $p=3,G=12$; $M_G=44$ for $p=5,G=10$; $M_G=48$ for $p=7,G=8$).

### 1.2 Definitions and method [computer-assisted]

$N_G(x)=\#\{B\subseteq[1,M_G]: p^G\mid S_B(x)\}$, $Z_G(x)=p^G2^{-M_G}N_G(x)$, $x$ uniform mod $p^G$ (locality, Theorem 3.1). `src/annealed.c` runs, for every class $x$ mod $p^G$, a count-array DP over residues: partial sums are kept modulo $p^{G-L}$ after division by $p^{L}$ once every remaining term is divisible by $p^L$ (exact pruning: a partial sum not divisible by $p^L$ can never reach $0$); sparse sorted pairs while the support is small, dense array afterwards; the terms $b$ with $v_p(\pi_b(x))\ge G$ ("free" terms, $F(x)$ of them) each double the count, so $N_G=N'_G\,2^{F}$ where $N'_G$ counts witnesses using only non-vanishing terms. Note $Z_G(x)=p^G N'_G(x)/2^{M_G-F(x)}$, i.e. $Z_G$ is exactly the count of non-trivial witnesses normalised by its random-model expectation. Classes are bucketed by $\mathrm{maxv}(x)=\max_{1\le i\le M_G}v_p(x+i)$; sums $\sum N$, $\sum N^2$ are exact 128-bit integers (overflow-checked). Cross-checked against a brute-force enumeration of all $2^{M_G}$ subsets (`src/brute_check.py`) for $(p,G)=(2,6),(2,8),(3,3),(3,4),(5,2),(7,2)$: identical $\sum N,\sum N^2$, survivor count and $\max N$. The survivor counts $\delta_G(p)$ reproduce every entry of note §4.7 that overlaps ($p=2$: $G\le26$; $p=3$: $G\le17$; $p=5$: $G\le10$; $p=7$: $G\le8$).

### 1.3 Results (exact; `data/annealed_p*_G*.txt`, `data/annealed_summary.tsv`)

Unconditioned moments ($E$ over all classes mod $p^G$):

| $p$ | $G$ | $\delta_G$ | $EZ$ | $EZ^2$ | $EZ^2/(EZ)^2$ |
|---|---|---|---|---|---|
| 2 | 8 | .24219 | 2.875 | 117.3 | 14.2 |
| 2 | 16 | .15170 | 9.25 | $3.24\cdot10^4$ | 379 |
| 2 | 20 | .14169 | 13.41 | $5.21\cdot10^5$ | 2897 |
| 2 | 24 | .12917 | 18.30 | $8.33\cdot10^6$ | $2.49\cdot10^4$ |
| 2 | 26 | .12362 | 20.62 | $3.33\cdot10^7$ | $7.84\cdot10^4$ |
| 2 | 27 | .11938 | (file `annealed_p2_G27.txt`) | | |
| 3 | 8 | .39369 | 3.588 | 2408 | 187 |
| 3 | 12 | .37042 | 5.748 | $1.95\cdot10^5$ | 5913 |
| 3 | 16 | .36361 | 7.869 | $1.58\cdot10^7$ | $2.56\cdot10^5$ |
| 3 | 17 | .36329 | (file) | | |
| 5 | 6 | .52346 | 2.932 | 4813 | 560 |
| 5 | 8 | .52187 | 3.739 | $1.20\cdot10^5$ | 8604 |
| 5 | 10 | .52162 | 4.551 | $3.01\cdot10^6$ | $1.45\cdot10^5$ |
| 7 | 4 | .62516 | 2.093 | 674 | 154 |
| 7 | 6 | .62409 | 2.872 | $3.30\cdot10^4$ | 4003 |
| 7 | 8 | .62394 | 3.652 | $1.62\cdot10^6$ | $1.21\cdot10^5$ |

**Observation A [computer-assisted + proved lower bound].** The unconditioned ratio diverges like $p^G$ for **every** $p$, including odd $p$ — so the raw annealed second moment cannot distinguish $p=2$ from odd $p$. This is forced by the shadow of $-2$:

**Proposition 2 [proved].** For every prime $p$ and $G\ge1$, $E Z_G^2\ge p^G/4$.
*Proof.* In the class $x\equiv-2\pmod{p^G}$: $S_{\{1\}}(x)=x+2\equiv0$, and $\pi_b(x)\equiv0$ for all $b\ge2$ (factor $x+2$). So exactly one non-vanishing term, $N'=1$, $F=M_G-1$, $Z=p^G/2$. Its Haar weight is $p^{-G}$, giving $EZ^2\ge p^{-G}(p^G/2)^2$. ∎
(Observed $EZ^2/(p^G/4)$: $2.0$ at $p=2,G=26$; $3.7$ at $p=3,G=16$; $1.2$ at $p=5,G=10$; $1.1$ at $p=7,G=8$ — the $-2$ class carries most of the second moment at odd $p$.)

$EZ_G$ itself grows roughly linearly: increments per level $\approx1.15$ ($p=2$), $0.52$ ($p=3$), $0.41$ ($p=5$), $0.39$ ($p=7$). Under a random model $EZ=1$; the excess is real correlation (witness multiplicity), not a normalisation artefact. [computer-assisted; no proof of linear growth]

**Conditioned moments** (restrict to $\mathrm{maxv}(x)\le K$, i.e. the good-set condition (G2) of note §10.1 at finite level; `data/annealed_summary.tsv` has every $K$). With $K$ **fixed**, as $G$ grows:

| $p$ | $K$ | $G$ range | measure of $\{\mathrm{maxv}\le K\}$ | $E[Z\mid\cdot]$ | $E[Z^2\mid\cdot]$ | ratio |
|---|---|---|---|---|---|---|
| 3 | 4 | 10,12,13 | .905,.893,.893 | 1.99, 2.00, 1.99 | 50.8, 51.0, 49.7 | 12.8, 12.7, 12.6 |
| 3 | 6 | 10,12,13 | .990,.988,.988 | 2.98, 3.00, 2.98 | 461, 479, 475 | 51.7, 53.3, 53.3 |
| 3 | 7 | 14,15,16 | .996,.995,.995 | 3.49, 3.50, 3.52 | 1412, 1396, 1446 | 116, 114, 117 |
| 5 | 4 | 7,8,9,10 | .991,.989,.988,.986 | 2.01, 2.01, 2.01, 2.02 | 165, 162, 163, 165 | 40.8, 40.3, 40.3, 40.6 |
| 5 | 5 | 7,8,9,10 | .998,.998,.998,.997 | 2.40, 2.41, 2.40, 2.41 | 791, 811, 798, 798 | 137, 140, 138, 138 |
| 7 | 3 | 5,6,7,8 | .986,.983,.980,.980 | 1.60, 1.60, 1.60, 1.60 | 72.4, 72.7, 73.0, 73.0 | 28.3, 28.4, 28.4, 28.4 |
| 7 | 4 | 5,6,7,8 | .998,.998,.997,.997 | 1.99, 1.98, 1.98, 1.98 | 517, 498, 499, 498 | 131, 127, 128, 127 |
| 2 | 6 | 16,18,20,22,24,26 | .87,.85,.82,.82,.79,.77 | 3.56,3.50,3.72,3.88,3.94,4.02 | 178,183,223,258,300,307 | 14.1,15.0,16.1,17.1,19.3,19.0 |
| 2 | 10 | 20,22,24,26 | .989,.989,.987,.986 | 7.35,7.86,8.24,8.25 | 4105,4464,5381,5715 | 76,72,79,84 |

**Observation B [computer-assisted; heuristic reading].** For odd $p$ the truncated moments $E[Z;\mathrm{maxv}\le K]$ and $E[Z^2;\mathrm{maxv}\le K]$ are **stable in $G$** (to 1–3%) once $G\ge 2K$ or so, while for $p=2$ they still **grow** with $G$ at fixed $K$ (ratio at $K=6$: $14\to19$ over $G=16..26$). This is the only place where the requested "bounded for odd $p$, divergent for $p=2$" dichotomy is visible, and it is visible only after truncation. However, the truncated ratio grows with $K$ like $\approx c_p\,p^{K}$ ($p=3$: $12.7, 53, 117$ for $K=4,6,7$; $p=5$: $40, 138$ for $K=4,5$; $p=7$: $28, 127$ for $K=3,4$), because the classes with $\mathrm{maxv}=K$ are shadows $x\equiv-m\ (\mathrm{mod}\ p^K)$ with $Z\asymp p^{K}$. Since $\{\mathrm{maxv}\le K\}$ has measure $\to0$ as $G\to\infty$ unless $K\gtrsim\log_p M_G$, a Paley–Zygmund bound from these moments gives at best $\delta_G\gtrsim (\log G)^2/G\to0$: **the annealed second moment, truncated or not, cannot prove $\mu(K_p)>0$ for odd $p$**. A proof must weight witnesses by frozen-state/quenched weights (as the $p=2$ martingale of §10.1 does) rather than count them. [heuristic conclusion from exact data]

## 2. Survival of natural $a$ at $p=2$ (task 2) [computer-assisted]

`src/gsampleN.c` (generalisation of track D's `gsample256.c` to $NL\cdot64$-bit fixed-width arithmetic; Newton inverse; hash-deduplicated carry sets; exact) computes $\min(g_2(a),\mathrm{CAP})$ for every $a\le4096$; range mode. Completed: CAP $=32$ and CAP $=254$ (`data/surv_cap32.txt`, `surv_cap254.txt`, 1 s each). Checks: (i) the two caps are consistent ($g_{32}=\min(g_{254},32)$ for all $a$); (ii) against **Kitamura's** certified exact table `data/p2_exact_table_1_256.csv` ($g=f-v_2(a!)$): **0 mismatches** for all $a\le256$ at cap 254; (iii) spot values $g(2)=253$, $g(6)=129$, $g(30)=100$, $g(62)=197$, $g(126)=156$, $g(254)=648$, $g(510)=517$, $g(1022)=182$, $g(2046)=567$, $g(4094)=360$ (cap 1000, NL=17) all equal Kitamura's shadow-family row.

$N(A,G)$ (`data/survivors_NAG.tsv`; columns $N(A,G)G/A$ and $N(A,G)\sqrt G/A$):

| $G$ | $N(256,G)$ | $N(1024,G)$ | $N(4096,G)$ | $NG/A$ (256/1024/4096) | $N\sqrt G/A$ |
|---|---|---|---|---|---|
| 8 | 62 | 248 | 992 | 1.94/1.94/1.94 | .685/.685/.685 |
| 16 | 38 | 158 | 622 | 2.38/2.47/2.43 | .594/.617/.607 |
| 32 | 26 | 102 | 411 | 3.25/3.19/3.21 | .575/.564/.568 |
| 64 | 18 | 64 | 263 | 4.50/4.00/4.11 | .563/.500/.514 |
| 128 | 14 | 39 | 167 | 7.00/4.88/5.22 | .619/.431/.461 |
| 192 | 9 | 23 | 118 | 6.75/4.31/5.53 | .487/.311/.399 |
| 254 | 5 | 15 | 87 | 4.96/3.72/5.40 | .311/.234/.339 |

So $N(A,G)\sqrt G/A$ sits at $0.5$–$0.6$ for $8\le G\le128$ and starts to fall by $G\approx200$ ($A=1024,4096$), while $N(A,G)G/A$ rises from $2$ to $5$: for $G\le128$ the natural numbers $a\le4096$ follow the Haar density $\delta_G\approx0.55/\sqrt G$ (compare §3) rather than $11.5/G$, and beyond $G\approx150$ the decay steepens, consistent with the Monte Carlo exponent rising towards $0.7$–$0.9$. Note $N(A,G)$ for $G\le12$ is exactly $A\,\delta_G$ because $A$ is a multiple of $2^G$ (locality), so the first rows are a consistency check, not evidence.

87 values $a\le4096$ have $g_2(a)\ge254$ (list in `data/results.json`, key `g2_capped_a_le_4096`; includes 14, 34, 594, 1102, 3456, 8190's sibling 4094 excluded since $g=360$). Largest exact values below the cap: $g(2304)=253$, $g(2)=253$, $g(2830)=252$, $g(2822)=251$, $g(1810)=248$. Deeper caps (1022, 2046, 4094) were queued (§6) but had not finished.

**Kitamura's "$\sim11.5/G$".** Fetched read-only via `gh api` (Accept raw): `README.md` (l. 234), `witness_gallery.md` (§6, l. 135) and `determining_exact_values.md` (§5, l. 218–219) of `KitaKen1/erdos-404-p2-landscape`. The phrase appears only as prose ("the surviving fraction decays like ~11.5/G"; "Survival to depth G has measured probability ~11.5/G"), attached in `determining_exact_values.md` to "the complete classification of all even classes with g ≤ 24 (… 174,640 residue classes)". **No definition, data table, fitting script or fit residuals exist anywhere in the repository** (`data/` holds only the exact table $a\le256$ and three witness files; `scripts/` contain no density code; `index.html` does not mention it). Two candidate readings, tested against our exact data: (a) Haar density $\delta_G(2)$: $11.5/G$ gives $0.48$ at $G=24$ vs exact $0.129$, and $0.18$ at $G=64$ vs $0.064$ — **inconsistent**; (b) the fraction of **even** $a\le256$ with $g\ge G$, from Kitamura's own exact table (`kitamura/kitamura_N256.txt`): $N(256,G)/128=0.141,0.133,0.109,0.070,0.039,0.016$ at $G=64,96,128,192,256,1024$ vs $11.5/G=0.180,0.120,0.090,0.060,0.045,0.011$ — consistent within $\sim30\%$ over $64\le G\le1024$. Reading (b) is our best guess at what was fitted; it is a 128-point sample and should not be quoted as a rate for $\delta_G(2)$.

## 3. $\delta_G(2)$ for large $G$ by Monte Carlo (task 3) [computer-assisted; estimates, not certificates]

Completed before the forced report: `src/gsample_nl2 400000 7 126 1` (uniform $x$ mod $2^{126}$, exact decision, 4 s). Validation against the exact census: $\delta_8=0.2415\pm.0007$ (exact .2422), $\delta_{16}=0.1512\pm.0006$ (.1517), $\delta_{24}=0.1287\pm.0005$ (.1292), $\delta_{29}=0.1128\pm.0005$ (.1134), $\delta_{32}=0.1011\pm.0005$ (.1016). New: $\delta_{48}=0.0792\pm.0004$, $\delta_{64}=0.0642\pm.0004$, $\delta_{96}=0.0486\pm.0003$ (round-1 value $\delta_{64}=0.0644$ reproduced). Local exponent between 64 and 96: $0.69$; $\delta_G\sqrt G$ falls from $0.57$ ($G=32$) to $0.48$ ($G=96$), $\delta_G G$ rises $3.2\to4.7$. A 20 000-sample pilot at cap 254 gave $\delta_{254}\approx0.021$ (round 1: $0.0208$) and a 2 000-sample pilot at cap 1022 gave $\delta_{1022}\approx0.005$ (10 survivors; $\pm0.0016$). Larger runs ($4\cdot10^7$ at 126, $2\cdot10^7$ at 256, $2\cdot10^6$ at 512, $10^6$ at 1024, $2\cdot10^5$ at 2046; §6) were queued and had not finished; the fit $\delta_G\sim CG^{-c}$ over $64\le G\le1024$ is therefore **not delivered**. From what is in hand: $c\approx0.69$ on $[64,96]$ and the pilot points suggest $c\approx0.8$–$1$ on $[256,1024]$ ($0.021\to0.005$ over a factor 4 in $G$ is $c\approx1.0\pm0.3$). [heuristic]

## 4. Constants (task 4)

### 4.1 $c_p$ [computer-assisted, mpmath 30 digits; one identity proved]

`data/constants_cp.txt`: $c_p=\max_{\xi}\prod_{r<p}|\cos(\pi\xi r!/p)|$: $c_2=0$ (exact: $\cos(\pi/2)$), $c_3=1/8$, $c_5=0.13238$, $c_7=0.082366$, $c_{11}=0.026681$, $c_{13}=0.0032999$, $c_{17}=5.374\cdot10^{-4}$, $c_{19}=2.134\cdot10^{-4}$, $c_{23}=4.821\cdot10^{-5}$, $c_{29}=5.696\cdot10^{-6}$, $c_{31}=6.105\cdot10^{-6}$, $c_{37}=2.112\cdot10^{-7}$, $c_{41}=1.324\cdot10^{-10}$, $c_{43}=6.464\cdot10^{-7}$, $c_{47}=4.199\cdot10^{-11}$, $c_{53}=4.026\cdot10^{-14}$. The maximum is always attained at exactly two $\xi$ ($\pm\xi_0$); $c_p^{1/p}\in[0.56,0.72]$, i.e. $c_p$ is comparable to $(2/\pi)^p$ (ratio $c_p/(2/\pi)^p$: 1.27, 1.94, 3.8, 1.17, 1.16, 1.14, 1.56, 2.8, 7.3, 3.8, 0.015, 175, 0.07, 0.001 for $p=5..53$ — erratic, no monotone trend).

**Lemma 3 [proved].** For odd $p$, the geometric mean over $\xi\in(\mathbb Z/p)^\times$ of $\prod_{r=0}^{p-1}|\cos(\pi\xi r!/p)|$ is exactly $2^{-p}$.
*Proof.* For $0\le r\le p-1$, $r!$ is a unit mod $p$, so $\xi\mapsto\xi r!$ permutes the units and $\prod_\xi|\cos(\pi\xi r!/p)|=\prod_{k=1}^{p-1}|\cos(k\pi/p)|=2^{1-p}$ (classical; checked numerically to $10^{-14}$ for $p\le53$). Multiply over the $p$ values of $r$ and take the $(p-1)$-th root. ∎ (The table's geometric-mean column equals $2^{-p}$ to 15 digits for every odd $p\le53$.)

### 4.2 Single-gate-block $L^1$ sums [computer-assisted, double precision]

`src/gatesum.c`: $L^{\rm unit}(p,i)=\sum_{\xi\in(\mathbb Z/p^i)^\times}\prod_{u<p}|\cos(\pi\xi e_u/p^i)|$ with $e_u=(-1)^u(p-1)!/u!$ (integers; $e_0=(p-1)!$, $e_1=-(p-1)!$, …, $e_{p-1}=1$), and the budget $B(p,i)=p^i(1-1/p)\,I_p$, $I_p=\int_0^1\prod_u|\cos(\pi e_u\theta)|d\theta$.

*Computing $I_p$ [proved structure].* With $\Theta=(p-1)!\theta$ the integrand is $\prod_u|\cos(\pi\Theta/u!)|$; for $u\ge2$, $u!/2\in\mathbb Z$, so $\cos(\pi\Theta/u!)$ vanishes only at integer $\Theta$, and the $u=0,1$ factors give $\cos^2(\pi\Theta)$, smooth. Hence the integrand is analytic on each unit interval of $\Theta$, and $I_p=\frac1{(p-1)!}\sum_{k<(p-1)!}\int_0^1(\cdots)dt$ with Gauss–Legendre on each piece converges spectrally: 8/16/32 nodes agree to $3\cdot10^{-10}$ at $p=5$, and a $10^6$-point midpoint rule agrees to $10^{-9}$ (`logs`, §6).

Completed: $p=5$ and $p=7$, $i\le8$ (`data/gatesum_p5.txt`, `gatesum_p7.txt`):

| $p$ | $I_p$ | $(2/\pi)^p$ | $L^{\rm unit}/(p^i(1-1/p))$ for $i=1..8$ |
|---|---|---|---|
| 5 | 0.1220287868 | 0.1045684 | .0699, .1381, .1119, .1221, .12203, .122029, .1220288, .1220288 |
| 7 | 0.0496033637 | 0.0423800 | .0339, .0266, .0497, .04984, .04958, .049603, .0496034, .0496034 |

So $L^{\rm unit}(p,i)/B(p,i)\to1$ **exactly** (to $10^{-7}$ by $i=8$), while the random-phase budget $p^i(1-1/p)(2/\pi)^p$ is low by the factor $I_p/(2/\pi)^p=1.167$ ($p=5$), $1.170$ ($p=7$) — this is the "per-level ratio $\approx1.17$" that track R2b measured (note §10.5, Conjecture 10.23 evidence) and it is explained exactly: $e_0=-e_1$ makes two factors equal, $E\cos^2=1/2\ne(2/\pi)^2$ (indeed $(2/\pi)^{p-2}/2=0.1290,\ 0.0523$ overshoots slightly; the rest of the deficit is the arithmetic correlation among the $e_u$). The convergence $L^{\rm unit}/B\to1$ is a Weyl-equidistribution statement for the fixed finite set $\{e_u/p^i\}$ and is the "insufficient first step" named in note §10.6 item 1 — numerically it holds for $p=5,7$ with error $\ll p^{-i}$. $p=11,13$ ($i\le8$, $\sim10^{10}$ cosine evaluations) were queued (§6) and did not finish.

## 5. Gaps, honesty

- Items pending at the forced report: annealed $(5,11),(7,9),(2,28)$; survivors at caps 1022/2046/4094; Monte Carlo at caps 256/512/1024/2046 (so no delivered fit over $G\le1024$); gate sums $p=11,13$. The scripts `run_annealed.sh`, `run_queue.sh` were running under `nohup` and may have completed; outputs would be in `data/` but are unverified by this track.
- All "bounded / divergent" statements in §1 are empirical readings of exact finite data; no limit theorem is proved. Proposition 2 and Lemmas 1, 3 are the only proved statements.
- Double precision in §4.2; sums of $\sim10^5$–$10^6$ positive terms, accumulated in long double per thread; relative error $\lesssim10^{-9}$, adequate for the ratio statements but not a certificate.
- The reading of Kitamura's $11.5/G$ is an inference; the repository does not define it.

## 6. Commands and timings (log files in `logs/`)

- `clang -O3 -march=native -o src/annealed src/annealed.c -lpthread`; `src/annealed p G 4` for the list in `run_annealed.sh`. Timings: $p=2$: $G\le24$ ≤6 s, $G=26$ 25 s, $G=27$ 51 s; $p=3$: $G=16$ 29 s, $G=17$ 111 s; $p=5$: $G=10$ 55 s; $p=7$: $G=8$ 141 s. Memory < 100 MB (no per-class dump).
- `clang -O3 -march=native -DNL={2,4,5,9,17,33,65} -o src/gsample_nlN src/gsampleN.c -lpthread`; `src/gsample_nl2 -1 0 32 4096 1` (1 s), `src/gsample_nl4 -1 0 254 4096 1` (<1 s), `src/gsample_nl2 400000 7 126 1` (4 s); pilots `gsample_nl4 20000 1 254 1` (0.6 s), `gsample_nl17 2000 1 1022 1` (1.9 s).
- `clang -O3 -march=native -o src/gatesum src/gatesum.c -lpthread -lm`; `src/gatesum 5 8 1 16`, `src/gatesum 7 8 1 16` (<1 s each).
- `python3 src/constants.py` (mpmath), `python3 src/brute_check.py`, `python3 src/annealed_post.py`, `python3 src/surv_post.py`, `python3 src/mc_post.py`, `python3 src/assemble_results.py`.
- Kitamura fetches: `gh api -H "Accept: application/vnd.github.raw" repos/KitaKen1/erdos-404-p2-landscape/contents/{README.md,witness_gallery.md,determining_exact_values.md,index.html,data/p2_exact_table_1_256.csv,scripts/*.py}` (read-only, 2026-10-12 ~14:33 local).

## 7. Credit

Kitamura (KitaKen1, July 2026): exact $p=2$ table $a\le256$ used as the independent oracle for §2, the shadow-family values, the $11.5/G$ remark. Note round 1 track D (`gsample256.c`) is the ancestor of `gsampleN.c`; track E (`tree.c`) supplied the pruning idea of `annealed.c`. Track R2b (round 2) first measured the $\approx1.17$ gate-block ratio that §4.2 explains. Tao (2025) for the block framework; Kovač (2025) for the problem's corrected statement; Lin (1960) for the original computations. The cosine product identity is classical.
