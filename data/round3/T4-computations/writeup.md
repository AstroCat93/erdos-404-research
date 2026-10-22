# Track T4 (computations), round 3, Erdős #404 — retry of 2026-10-20 (first attempt 2026-10-12)

Work dir: `e404r3/T4-computations/`. Layout: `src/` (programs of the first attempt, 2026-10-12), `code/` (programs added in this retry: independent cross-check `xcheck_annealed.c`, add-only lifting program `p2add.c`, `post_extra.py`, run scripts), `data/` (all outputs; `results.json` and `results_retry.json` machine-readable), `logs/` (every command with timing; `logs/writeup_2026-10-12_first_attempt.md` is the superseded first report), `kitamura/` (read-only fetches from `KitaKen1/erdos-404-p2-landscape`).

**What happened.** The first attempt launched every requested run under `nohup` but was forced to report before most of them finished; its report flagged those outputs as unverified. All of them completed (last at 16:23 on 2026-10-12; `logs/annealed.log`, `logs/queue.log`, every run well inside 45 min and 4 threads). This retry (a) re-read every program, (b) re-ran all post-processors on the complete data, (c) re-computed the annealed sums with an independently written dense-array DP (`code/xcheck_annealed.c`) on overlapping cases, (d) re-computed the deep survivor values with an independently written add-only carry program (`code/p2add.c`) and pushed the five deepest $a\le4096$ further, (e) checked the Gauss–Legendre integrals at a second node count, and (f) rewrote this report. Nothing from the first attempt had to be retracted; several of its "pending" items are now delivered (Monte Carlo fit to $G=2046$, gate sums for $p=11,13$, survivors to cap 4094, one new exact value $g_2(2210)=6261$).

All arithmetic in items (1)–(3) is exact integer/residue arithmetic. Item (4) is floating point (double / mpmath), diagnostic only. Labels: [proved] / [computer-assisted] / [heuristic] / [conjecture] / [sketch]. Nothing here is human-refereed.

---

## 0. Headline numbers

1. **Annealed moments** (exact, all classes mod $p^G$): $p=2$ to $G=28$, $p=3$ to $G=17$, $p=5$ to $G=11$, $p=7$ to $G=9$. $E Z_G$ grows linearly in $G$ (slopes $\approx1.2,\,0.52,\,0.41,\,0.39$). $E Z_G^2\sim c_p\,p^G/4$ with $c_2\to1.987$, $c_3\to1.471$, $c_5\to1.232$, $c_7\to1.123$ (stable to 4 digits over the last 3–5 levels). Hence $EZ^2/(EZ)^2$ **diverges like $p^G/G^2$ for every $p$**, odd or even [computer-assisted + Proposition 2, proved]. The requested dichotomy (bounded for odd $p$, divergent for $p=2$) is **not** present in the raw annealed moments; it appears only after truncating to classes with $\max_{i\le M_G}v_p(x+i)\le K$, and even there the truncated ratio grows like $p^K$ (§1.5). New exact densities: $\delta_{11}(5)=25\,468\,861/5^{11}=0.5216022$, $\delta_9(7)=25\,177\,371/7^9=0.6239187$; every other $\delta_G$ reproduces note §4.7.
2. **Natural $a$ at $p=2$**: $N(A,G)$ for $A=256,1024,4096$ and all $G\le4094$ (exact capped $g_2(a)$ for every $a\le4096$). $N(4096,G)\,G/4096\in[4.8,7.5]$ for $256\le G\le3072$ and $N\sqrt G/A$ falls steadily: the natural numbers follow $\approx5$–$6/G$, not $1/\sqrt G$, beyond $G\approx200$. Five $a\le4096$ have $g_2(a)\ge4094$: $34,594,1102,2210,3456$. Independent re-computation gives $g_2(34)=18412$, $g_2(1102)=11536$, $g_2(3456)=4823$ — **Kitamura's three shipped records reproduced exactly by a different program** — and the **new exact value $g_2(2210)=6261$, i.e. $f(2210,2)=2206+6261=8467$**; $g_2(594)\ge16382$ here (Kitamura: $\ge65536$). Kitamura's "$\sim11.5/G$" is explained: it is the fraction among **even** $a$, i.e. $2\delta_G(2)$, and our Monte Carlo gives $2\delta_G G=10.5,10.9,11.6,11.5,11.4,10.9$ at $G=256,512,768,1024,1536,2046$.
3. **$\delta_G(2)$ Monte Carlo** (exact decision per sample; $4\cdot10^7$ samples at cap 126, $2\cdot10^7$ at 256, $2\cdot10^6$ at 512, $10^6$ at 1024, $2\cdot10^5$ at 2046; no population overflow): $\delta_{64}=0.06416(4)$, $\delta_{128}=0.03770(4)$, $\delta_{256}=0.02052(3)$, $\delta_{512}=0.01068(7)$, $\delta_{1024}=0.00562(7)$, $\delta_{2046}=0.00266(12)$. Weighted fit $\delta_G\approx3.57\,G^{-0.93}$ on $G\ge256$; local exponents rise from $0.69$ ($64$–$96$) to $1.0$–$1.16$ ($768$–$2046$); $\delta_G\,G\approx5.5$–$5.8$ for $G\ge512$. [heuristic reading of exact-decision Monte Carlo]
4. **Constants**: $c_p$ for $p\le53$ (table §4.1); geometric mean over $\xi$ is exactly $2^{-p}$ (Lemma 3, proved). Gate-block $L^1$ sums for $p=5,7,11,13$, $i\le8$: $L^{\rm unit}(p,i)/\big(p^i(1-\tfrac1p)I_p\big)\to1$ with relative error $\le10^{-7}$ at $i=8$ for all four primes, and $I_p/(2/\pi)^p=1.1670,1.1704,1.1725,1.1729$ — the "$\approx1.17$ per-level ratio" of note §10.5 (track R2b) is this quantity. [computer-assisted, double precision]

---

## 1. Annealed moments (task 1)

### 1.1 The cutoff $M_G$ [proved]

**Lemma 1.** For $x\in\mathbb Z_p$ and $b\ge1$, $b!\mid\pi_b(x)=(x+1)\cdots(x+b)$ in $\mathbb Z_p$, with equality of valuations at $x=0$. Hence
$$M_G:=\min\{M:\pi_b(x)\equiv0\ (\mathrm{mod}\ p^G)\ \forall x\in\mathbb Z_p,\ \forall b>M\}=\min\{M: v_p((M+1)!)\ge G\}=\max\{b: v_p(b!)<G\}\le pG-1 .$$

*Proof.* $\pi_b(x)/b!=\binom{x+b}{b}$ is a polynomial with rational coefficients that is integer-valued on $\mathbb N$; $\mathbb N$ is dense in $\mathbb Z_p$ and $\mathbb Z_p$ is closed, so it maps $\mathbb Z_p$ into $\mathbb Z_p$. Equality at $0$: $\pi_b(0)=b!$. Since $b\mapsto v_p(b!)$ is nondecreasing, "$v_p(\pi_b(x))\ge G$ for all $x$ and all $b>M$" holds iff $v_p((M+1)!)\ge G$ (if: divisibility by $b!$; only if: take $x=0$, $b=M+1$). Finally $v_p((pG)!)\ge G$. ∎

Both programs compute $M_G$ by this formula. Values: $M_G=5,9,15,17,19,23,23,27,29,31,31$ for $p=2$, $G=4,8,12,16,18,20,22,24,26,27,28$; $M_G=35$ for $p=3,G=17$; $M_G=49$ for $p=5,G=11$; $M_G=55$ for $p=7,G=9$. Note that $Z_G$ does not depend on the cutoff: replacing $M_G$ by any $M\ge M_G$ multiplies $N_G$ by $2^{M-M_G}$ and $2^{-M}$ compensates. So the "pG is safe" cutoff would give the same $Z_G$.

### 1.2 The carry DP and its correctness [proved]

Fix $x$ mod $p^G$ (locality, note Thm 3.1). Write $S_n=\sum_{b<n}e_b\pi_b(x)$ ($e_0=1$), $V_n=v_p(\pi_n(x))$ computed with $v_p(x+i)$ capped at $G$ (then $V_n$ is a function of $x$ mod $p^G$), $n_0=\min\{n: V_n\ge G\}$, so $n_0\le M_G+1$ by Lemma 1.

**Lemma 2 (reduction to prefixes).** For $B\subseteq[1,M_G]$: $p^G\mid S_B(x)$ iff $p^G\mid S_{n_0}$ for the prefix word $e|_{[0,n_0)}$ of $B$, and then $v_p(S_n)\ge V_n$ for every $n<n_0$. Consequently
$$N_G(x)=2^{\,M_G+1-n_0}\cdot\#\{e\in\{0,1\}^{n_0}: e_0=1,\ p^G\mid S_{n_0}\},$$
and the second factor is computed exactly by the recursion below.

*Proof.* Terms $b\ge n_0$ have $v_p(\pi_b)\ge V_{n_0}\ge G$ (each $\pi_b$, $b\ge n$, is a multiple of $\pi_n$), so $S_B\equiv S_{n_0}\pmod{p^G}$ and the $M_G+1-n_0$ terms $b\in[n_0,M_G]$ are free. For $n<n_0$: $S_n=S_{n_0}-\sum_{n\le j<n_0}e_j\pi_j$, every $\pi_j$ with $j\ge n$ is divisible by $p^{V_n}$, and $V_n<G\le v_p(S_{n_0})$, so $v_p(S_n)\ge V_n$. ∎

*Recursion.* State after $n$ steps: $c_n:=S_n/p^{V_n}\bmod p^{r_n}$, $r_n=G-V_n$, with a count array `cnt[c]`; $\omega_n:=\pi_n(x)/p^{V_n}\bmod p^{r_n}$ (a unit). Start $c_0=0$, $r_0=G$, $\omega_0=1$. Step $n\to n+1$ with $t=\min(v_p(x+n+1),r_n)$: for each $c$ and $e\in\{0,1\}$ ($e=1$ only at $n=0$), $y=c+e\,\omega_n \bmod p^{r_n}$ represents $S_{n+1}/p^{V_n}$; if $t\ge r_n$ then $n+1=n_0$ and $y\equiv0$ is the acceptance condition; otherwise $y$ must be $\equiv0\bmod p^t$ (Lemma 2) and $c_{n+1}=y/p^t\bmod p^{r_n-t}$, $\omega_{n+1}=\omega_n\cdot\big((x+n+1)/p^t\big)\bmod p^{r_n-t}$. Counts add; two words with the same $c_n$ have identical futures, so merging is lossless for counting. This is exactly `code/xcheck_annealed.c` (dense arrays of size $p^{r_n}$, counts in `uint64`, sums in 128-bit). The first attempt's `src/annealed.c` implements the same recursion with the un-normalised state $S_n\bmod p^{G}$ pruned to multiples of $p^{V_n}$ (sparse sorted pairs while the support is small, dense array afterwards) and buckets the classes by $\mathrm{maxv}(x)=\max_{1\le i\le M_G}v_p(x+i)$. The two programs share no code.

*Decision version (used in §2–§3).* With a set of distinct carries instead of counts, the same recursion decides $g_2(x)\ge G$, and when every branch dies at step $n$ (no $y$ with $v(y)\ge t$) it returns $V_n+\max_{c,e}v(y)$, which equals $g_2(x)$ exactly: any $B$ with an element $\ge n+1$ has $v(S_B)<V_{n+1}$ (else all prefixes would be alive, Lemma 2), hence $S_B\equiv S_{B\cap[0,n]}\pmod{p^{V_{n+1}}}$ and $v(S_B)=v(S_{B\cap[0,n]})$; and a $B\subseteq[0,n]$ whose first dead prefix is at stage $m\le n$ has $v(S_B)=v(S_m)<V_m\le V_n\le V_n+\max v(y)$. [proved]

### 1.3 Validation [computer-assisted]

- Brute force: `src/brute_check.py` enumerates all $2^{M_G}$ subsets for $(p,G)=(2,6),(2,8),(3,3),(3,4),(5,2),(7,2)$: identical $\sum N$, $\sum N^2$, survivors, $\max N$ (first attempt, `logs/quick.log`).
- Independent program: `code/xcheck_annealed` (this retry) agrees with `src/annealed` in all of survivors, $\sum N$, $\sum N^2$, $\max N$ for $(2,8),(3,8),(2,14)$ [vs brute force at (2,8)], $(2,16)$ and the cases listed in `logs/xcheck_annealed.log` (see §6 for the final list; every finished case agreed).
- Survivor counts: every $\delta_G(p)$ in note §4.7 that overlaps is reproduced exactly ($p=2$: $G\le28$ against `archive/E/tree_p2.txt`, e.g. $31\,246\,552$ survivors at $G=28$; $p=3$: $G\le17$; $p=5$: $G\le10$; $p=7$: $G\le8$).

### 1.4 Results [computer-assisted, exact]

`data/annealed_overview.tsv` (from `code/post_extra.py`), raw rows in `data/annealed_p*_G*.txt`. $EZ=2^{-M_G}\sum_xN_G(x)$, $EZ^2=p^G4^{-M_G}\sum_xN_G(x)^2$, exact rationals printed to 6 digits.

| $p$ | $G$ | $M_G$ | $\delta_G$ | $EZ$ | $EZ^2$ | $EZ^2/(EZ)^2$ | $EZ^2/(p^G/4)$ | $E[Z\mid Z>0]$ |
|---|---|---|---|---|---|---|---|---|
| 2 | 8 | 9 | .242188 | 2.875 | 117.3 | 14.19 | 1.833 | 11.87 |
| 2 | 12 | 15 | .195801 | 5.1875 | 1959 | 72.8 | 1.9135 | 26.5 |
| 2 | 16 | 17 | .151703 | 9.25 | $3.244\cdot10^4$ | 379 | 1.9802 | 61.0 |
| 2 | 20 | 23 | .141685 | 13.406 | $5.207\cdot10^5$ | 2897 | 1.9862 | 94.6 |
| 2 | 24 | 27 | .129170 | 18.305 | $8.333\cdot10^6$ | $2.49\cdot10^4$ | 1.9867 | 141.7 |
| 2 | 26 | 29 | .123617 | 20.615 | $3.333\cdot10^7$ | $7.84\cdot10^4$ | 1.9867 | 166.8 |
| 2 | 27 | 31 | .119380 | 22.046 | $6.667\cdot10^7$ | $1.37\cdot10^5$ | 1.9868 | 184.7 |
| 2 | 28 | 31 | .116402 | 23.616 | $1.333\cdot10^8$ | $2.39\cdot10^5$ | 1.9869 | 202.9 |
| 3 | 8 | 17 | .393690 | 3.588 | 2408 | 187 | 1.4678 | 9.11 |
| 3 | 12 | 26 | .370420 | 5.748 | $1.954\cdot10^5$ | 5913 | 1.4707 | 15.5 |
| 3 | 15 | 32 | .364524 | 7.349 | $5.276\cdot10^6$ | $9.77\cdot10^4$ | 1.4707 | 20.2 |
| 3 | 16 | 35 | .363609 | 7.869 | $1.583\cdot10^7$ | $2.56\cdot10^5$ | 1.4707 | 21.6 |
| 3 | 17 | 35 | .363293 | 8.377 | $4.748\cdot10^7$ | $6.77\cdot10^5$ | 1.4707 | 23.1 |
| 5 | 6 | 24 | .523456 | 2.932 | 4813 | 560 | 1.2321 | 5.60 |
| 5 | 8 | 34 | .521869 | 3.739 | $1.203\cdot10^5$ | 8604 | 1.2318 | 7.16 |
| 5 | 10 | 44 | .521616 | 4.551 | $3.007\cdot10^6$ | $1.45\cdot10^5$ | 1.2317 | 8.72 |
| 5 | 11 | 49 | .521602 | 4.959 | $1.504\cdot10^7$ | $6.11\cdot10^5$ | 1.2317 | 9.51 |
| 7 | 4 | 27 | .625156 | 2.093 | 674.4 | 154 | 1.1235 | 3.35 |
| 7 | 6 | 41 | .624094 | 2.872 | $3.302\cdot10^4$ | 4003 | 1.1227 | 4.60 |
| 7 | 8 | 48 | .623938 | 3.652 | $1.618\cdot10^6$ | $1.21\cdot10^5$ | 1.1227 | 5.85 |
| 7 | 9 | 55 | .623919 | 4.041 | $1.133\cdot10^7$ | $6.93\cdot10^5$ | 1.1227 | 6.48 |

(All $G$ in the ranges $2\le G\le28$ ($p=2$, even $G$ plus 27), $2\le G\le17$ ($p=3$), $2\le G\le11$ ($p=5$), $1\le G\le9$ ($p=7$) are in the TSV.)

**Observation A (second moment is a shadow effect).**

**Proposition 2 [proved].** For every prime $p$ and $G\ge1$: $EZ_G^2\ge p^G/4$.
*Proof.* On the class $x\equiv-2\pmod{p^G}$ we have $S_{\{1\}}(x)=x+2\equiv0$ and $\pi_b(x)\equiv0$ for every $b\ge2$ (factor $x+2$). So the $M_G-1$ terms $b\ge2$ are free, the term $b=1$ is forced, and $N_G(x)=2^{M_G-1}$, $Z_G(x)=p^G/2$. This class has Haar weight $p^{-G}$, so $EZ^2\ge p^{-G}(p^G/2)^2$. ∎

The data show $EZ^2/(p^G/4)\to c_p$ with $c_2=1.9869$, $c_3=1.4707$, $c_5=1.2317$, $c_7=1.1227$ (constant to four digits over the last levels), i.e. the $-2$ shadow and its neighbours ($x\equiv-m\bmod p^k$, $k$ close to $G$) carry essentially the whole second moment. Since $EZ$ grows only linearly (next item), $EZ^2/(EZ)^2\ge p^G/(4(EZ)^2)\to\infty$ for **every** $p$. [Proposition proved; the limits $c_p$ are computer-assisted observations]

**Observation B (linear growth of $EZ$ by shadow buckets) [computer-assisted].** Bucket the classes by $v=\mathrm{maxv}(x)$ (`data/annealed_buckets.tsv`). Each bucket contributes $\sum_{x:\mathrm{maxv}=v}N_G(x)/2^{M_G}$ to $EZ$. For $p=2$, $G=28$ the contributions are $1.917,1.105,1.477,1.208,1.425,1.404,1.258,1.223,1.252,1.128,1.063$ for $v=5..15$ and then $1.00016,1.00009,1.00016,1.00002,1.00001,1.00000$ for $v=16..21$, dropping to $0.625,0.5,0.5,0.5,0.25,0.25,0.5$ for $v=22..28$. For $p=3$ ($G=17$) the plateau is $\approx0.50$–$0.54$ ($v=8..13$); $p=5$ ($G=11$): $0.40$–$0.41$ ($v=6..9$); $p=7$ ($G=9$): $0.39$–$0.40$ ($v=5..8$). So $EZ\approx(\text{slope})\cdot G$ with slope $\approx1$ ($p=2$), $0.52$, $0.41$, $0.39$: the excess of $EZ$ over the random-model value $1$ is a sum of $O(1)$ contributions from the $O(G)$ shadow buckets, not a uniform multiplicity. The exact value $1.0000$ per bucket for $p=2$, $G/2\lesssim v\lesssim G-7$ suggests an identity ("each $S_B$ has on average exactly one root in the bucket") that we did not try to prove. [heuristic mechanism]

### 1.5 Truncated moments and the answer to "bounded for odd $p$, divergent for $p=2$?" [computer-assisted; heuristic reading]

`data/annealed_summary.tsv` (from `src/annealed_post.py`) restricts to $\{\mathrm{maxv}\le K\}$, the finite-level form of the good-set condition (G2) of note §10.1. With $K$ fixed and $G$ growing:

| $p$ | $K$ | $G$ | measure | $E[Z\mid\mathrm{maxv}\le K]$ | $E[Z^2\mid\cdot]$ | ratio |
|---|---|---|---|---|---|---|
| 2 | 6 | 16, 20, 24, 28 | .867, .820, .789, .758 | 3.56, 3.72, 3.94, 4.03 | 178, 223, 300, 322 | 14.1, 16.1, 19.3, 19.8 |
| 2 | 10 | 20, 24, 28 | .989, .987, .985 | 7.35, 8.24, 8.70 | 4105, 5381, 7640 | 76, 79, 101 |
| 3 | 4 | 8, 10, 12, 13 | .930, .905, .893, .893 | 1.95, 1.99, 2.00, 1.99 | 48.6, 50.8, 51.0, 49.7 | 12.7, 12.8, 12.7, 12.6 |
| 3 | 7 | 14, 15, 16, 17 | .996, .995, .995, .995 | 3.49, 3.50, 3.52, 3.52 | 1412, 1396, 1446, 1467 | 116, 114, 117, 118 |
| 5 | 4 | 7, 8, 9, 10, 11 | .991, .989, .988, .986, .984 | 2.01, 2.01, 2.01, 2.02, 2.02 | 165, 162, 163, 165, 165 | 40.8, 40.3, 40.3, 40.6, 40.5 |
| 5 | 5 | 7, 8, 9, 10, 11 | .998, .998, .998, .997, .997 | 2.40, 2.41, 2.40, 2.41, 2.41 | 791, 811, 798, 798, 818 | 137, 140, 138, 138, 140 |
| 7 | 3 | 5, 6, 7, 8, 9 | .986, .983, .980, .980, .978 | 1.60, 1.60, 1.60, 1.60, 1.60 | 72.4, 72.7, 73.0, 73.0, 73.0 | 28.3, 28.4, 28.4, 28.4, 28.4 |
| 7 | 4 | 5, 6, 7, 8, 9 | .998, .998, .997, .997, .997 | 1.99, 1.98, 1.98, 1.98, 1.98 | 517, 498, 499, 498, 498 | 131, 127, 128, 127, 127 |

*Reading.* For odd $p$ the truncated first and second moments are **stable in $G$** to 1–3 % once $G\gtrsim2K$; for $p=2$ they still **grow** with $G$ (ratio at $K=6$: $14\to20$ over $G=16..28$; at $K=10$: $76\to101$). This is the only place where the requested dichotomy is visible. But the truncated ratio itself grows like $\approx c\,p^K$ in $K$ ($p=3$: $12.7,53,117$ for $K=4,6,7$; $p=5$: $40,138$ for $K=4,5$; $p=7$: $28,127$ for $K=3,4$), because the classes with $\mathrm{maxv}=K$ are shadows $x\equiv-m\pmod{p^K}$ with $Z\asymp p^K$, and the measure of $\{\mathrm{maxv}\le K\}$ tends to $0$ as $G\to\infty$ unless $K\gtrsim\log_pM_G$. A Paley–Zygmund bound from these moments therefore gives at best $\delta_G\gtrsim(\log G)^2/G\to0$. **Conclusion [heuristic, from exact data]: the annealed (subset-counting) second moment, truncated or not, cannot prove $\mu(K_p)>0$ for odd $p$; any second-moment proof must weight witnesses (frozen-state/quenched weights as in the $p=2$ martingale of note §10.1) rather than count them.**

---

## 2. Survival of natural $a$ at $p=2$ (task 2) [computer-assisted, exact]

### 2.1 Programs

- `src/gsampleN.c` (first attempt; generalises round-1 `code/D/gsample256.c` to $NL\cdot64$-bit fixed-width arithmetic; carries $\gamma_{N+1}=(\gamma_N+e_N)/(N+1)$ with a Newton inverse; hash-deduplicated carry sets; population limit $2^{20}$ with abort-and-report, never silent truncation). Range mode gives $\min(g_2(a),\mathrm{CAP})$ for every $a\le4096$ at caps $32,254,1022,2046,4094$ (`data/surv_cap*.txt`; 0 overflows; consistency $g_{c_1}=\min(g_{c_2},c_1)$ across all cap pairs: 0 mismatches, `logs/surv_post.out`).
- `code/p2add.c` (this retry; independent formulation): normalised carries $c_n=S_n/2^{V_n}$ with **additions only** ($\omega_n$ updated by one single-limb multiplication per step), variable limb width shrinking with $r_n$, hash-deduplicated. Agrees with `gsampleN` on every value tested (e.g. $g_2(1438)=3948$, $g_2(574)=3526$, $g_2(38)=793$, $g_2(254)=648$, $g_2(4094)=360$, $g_2(14)=1522$), and runs about $100\times$ faster at large caps (cap 4094 in $<1$ s per number).
- Oracle: **Kitamura's** certified exact table `kitamura/p2_exact_table_1_256.csv` ($g=f-v_2(a!)$): **0 mismatches** for all $a\le256$ against our capped values (cap 4094; `logs/surv_post.out`).

### 2.2 $N(A,G)=\#\{1\le a\le A: g_2(a)\ge G\}$ (`data/survivors_NAG.tsv`)

| $G$ | $N(256,G)$ | $N(1024,G)$ | $N(4096,G)$ | $NG/A$ (256 / 1024 / 4096) | $N\sqrt G/A$ (256 / 1024 / 4096) | $\delta_G(2)$ |
|---|---|---|---|---|---|---|
| 8 | 62 | 248 | 992 | 1.94 / 1.94 / 1.94 | .685 / .685 / .685 | .2422 (exact) |
| 16 | 38 | 158 | 622 | 2.38 / 2.47 / 2.43 | .594 / .617 / .607 | .1517 (exact) |
| 32 | 26 | 102 | 411 | 3.25 / 3.19 / 3.21 | .575 / .564 / .568 | .1016 (exact) |
| 64 | 18 | 64 | 263 | 4.50 / 4.00 / 4.11 | .563 / .500 / .514 | .0642 (MC) |
| 128 | 14 | 39 | 167 | 7.00 / 4.88 / 5.22 | .619 / .431 / .461 | .0377 (MC) |
| 256 | 5 | 15 | 85 | 5.00 / 3.75 / 5.31 | .313 / .234 / .332 | .0205 (MC) |
| 512 | 5 | 11 | 40 | 10.0 / 5.50 / 5.00 | .442 / .243 / .221 | .0107 (MC) |
| 1024 | 2 | 6 | 20 | 8.00 / 6.00 / 5.00 | .250 / .188 / .156 | .0056 (MC) |
| 2048 | 1 | 4 | 13 | 8.00 / 8.00 / 6.50 | .177 / .177 / .144 | .0027 (MC) |
| 3072 | 1 | 4 | 10 | 12.0 / 12.0 / 7.50 | .217 / .217 / .135 | — |
| 4094 | 1 | 2 | 5 | 16.0 / 8.00 / 5.00 | .250 / .125 / .078 | — |

For $G\le12$, $N(A,G)=A\,\delta_G$ exactly (locality; $A$ is a multiple of $2^G$), so the first rows are consistency checks. Beyond that, $N(4096,G)/4096$ tracks $\delta_G$ within the binomial noise ($\sqrt{N}/A\approx0.1\,N/A$ at $N\approx100$): $N\sqrt G/A$ sits at $0.5$–$0.6$ for $G\le128$ and then falls, while $NG/A$ rises from $2$ to $\approx5$–$7$ and stays there for $256\le G\le4094$ (at $A=4096$). So the natural numbers below $4096$ follow the Haar density, which decays like $\approx5.5/G$ beyond $G\approx300$ (§3) — **not** like $1/\sqrt G$, and not faster than $1/G$ as far as these data reach.

### 2.3 Deep survivors and new exact values (`data/deep_lift.txt`, `logs/deep.log`)

Five $a\le4096$ have $g_2(a)\ge4094$: $34,594,1102,2210,3456$. Lifting them with `p2add` (one process each, $\le4$ in parallel; population limit $2^{22}$, never reached):

| $a$ | cap | result | max population | CPU s | comparison |
|---|---|---|---|---|---|
| 3456 | 4900 | $g_2=4823$ exact | 23 748 | 0.5 | Kitamura: $f(3456,2)=8275=3452+4823$ ✓ |
| 1102 | 11600 | $g_2=11536$ exact | 152 100 | 12.6 | Kitamura: $f(1102,2)=12633=1097+11536$ ✓ |
| 34 | 18500 | $g_2=18412$ exact | 128 928 | 25.4 | Kitamura: $f(34,2)=18444=32+18412$ ✓ (their largest record) |
| 2210 | 16382 | $g_2=6261$ exact | 79 504 | 8.9 | **new**: $f(2210,2)=v_2(2210!)+6261=2206+6261=8467$ |
| 594 | 16382 | see §6 (run in progress at the time of writing; result appended there) | | | Kitamura: $g_2(594)\ge65536$ |

So Kitamura's three shipped records are reproduced by an independently written program (lower side: the exact death level; we did not re-verify their witness files, but a death at level $g+1$ together with survival at level $g$ is a two-sided certificate by the exactness argument of §1.2). Largest exact values below 4094 for $a\le4096$: $g_2(1438)=3948$, $g_2(574)=3526$, $g_2(1602)=3486$, $g_2(640)=3196$, $g_2(2662)=3129$, $g_2(1086)=2609$, $g_2(3934)=2245$, $g_2(1890)=2210$, $g_2(14)=1522$ (Kitamura: $f(14,2)=1533=11+1522$ ✓).

### 2.4 Kitamura's "$\sim11.5/G$"

Fetched read-only (`gh api -H "Accept: application/vnd.github.raw"`): `README.md` (l. 234), `witness_gallery.md` (§6, l. 135–137), `determining_exact_values.md` (§5, l. 216–219), `data/p2_exact_table_1_256.csv`, `index.html`, `scripts/*.py`. The phrase occurs only as prose: "the surviving fraction decays like ~11.5/G" (attached to "the complete classification of all even classes with g ≤ 24 … 174,640 residue classes") and "Survival to depth G has measured probability ~11.5/G — … the predictable thin tail of a critical branching process". **No definition, data table, fitting script or residuals are in the repository.** Tests: (a) as the Haar density $\delta_G(2)$ it is inconsistent ($11.5/24=0.48$ vs exact $0.129$; $11.5/64=0.18$ vs $0.064$); (b) as the fraction among **even** classes/integers, i.e. $2\delta_G(2)$, it is consistent at depth: our Monte Carlo gives $2\delta_GG=9.65,10.4,10.5,10.9,10.9,11.6,11.5,11.4,10.9$ at $G=128,192,256,384,512,768,1024,1536,2046$ (`data/kitamura_11p5_comparison.tsv`), and Kitamura's own table gives $N(256,G)/128=0.141,0.133,0.109,0.070,0.039,0.016$ at $G=64,96,128,192,256,1024$ vs $11.5/G=0.180,0.120,0.090,0.060,0.045,0.011$. Reading (b) is our best inference of what was fitted; the shipped data cannot distinguish $1/G$ from $G^{-0.9}$.

---

## 3. $\delta_G(2)$ for large $G$ by Monte Carlo (task 3) [computer-assisted; estimates]

`src/gsampleN` (exact decision per sample, uniform $x\bmod2^{\rm CAP}$ from xoshiro256 seeded per thread; 4 threads; `data/mc_cap{126,256,512,1024,2046}.txt`; population maxima 4 835, 15 135, 34 936, 100 994, 159 288; **0 overflow samples**). Each sample at cap $C$ yields exact $g_2(x)$ when $<C$, so one run gives $\delta_k$ for all $k\le C$. Validation against the exact census (cap 126, $4\cdot10^7$ samples): $\delta_8=0.24220(7)$ vs $.2421875$; $\delta_{16}=0.15166(6)$ vs $.1517029$; $\delta_{24}=0.12914(5)$ vs $.1291697$; $\delta_{29}=0.11337(5)$ vs $.1134133$; $\delta_{32}=0.10159(5)$ vs $.1016$ — all within $1.5\sigma$. Round-1 values ($\delta_{64}=0.0644$, $\delta_{128}=0.0379$, $\delta_{254}=0.0208$) reproduced.

Best estimates (largest sample at each $G$; `data/delta_G2_montecarlo.tsv`):

| $G$ | $\delta_G$ | $\pm$ | $\delta_G\sqrt G$ | $\delta_GG$ | local exponent to next $G$ |
|---|---|---|---|---|---|
| 64 | 0.06416 | 0.00004 | 0.513 | 4.11 | 0.688 |
| 96 | 0.04855 | 0.00003 | 0.476 | 4.66 | 0.880 |
| 128 | 0.03770 | 0.00004 | 0.427 | 4.83 | 0.825 |
| 192 | 0.02698 | 0.00004 | 0.374 | 5.18 | 0.951 |
| 256 | 0.02052 | 0.00003 | 0.328 | 5.25 | 0.899 |
| 384 | 0.01425 | 0.00008 | 0.279 | 5.47 | 1.003 |
| 512 | 0.01068 | 0.00007 | 0.242 | 5.47 | 0.846 |
| 768 | 0.00758 | 0.00009 | 0.210 | 5.82 | 1.038 |
| 1024 | 0.00562 | 0.00007 | 0.180 | 5.76 | 1.029 |
| 1536 | 0.00370 | 0.00014 | 0.145 | 5.69 | 1.156 |
| 2046 | 0.00266 | 0.00012 | 0.120 | 5.44 | — |

Fits $\delta_G\sim CG^{-c}$ (weighted log-log least squares, `src/mc_post.py`): over $64\le G\le2046$: $C=1.92$, $c=0.813$; over $G\ge128$: $C=2.80$, $c=0.886$; over $G\ge256$: $C=3.57$, $c=0.930$. The local exponent rises monotonically (up to noise) from $0.69$ to $\approx1.0$–$1.16$, and $\delta_GG$ is flat at $5.5$–$5.8$ for $512\le G\le1536$ (the $G=2046$ point has only 532 survivors). **Reading [heuristic]:** the data are consistent with $\delta_G(2)\sim c/G$ with $c\approx5.5$–$6$ (equivalently $\approx11.5/G$ among even $x$, Kitamura's figure), i.e. with the critical-branching survival exponent $1$ expected if the process behaved like a critical Galton–Watson process with the $n$-th level of the tree at depth $G\asymp n$; the $1/\sqrt G$ behaviour that fits $G\le128$ is a transient. No proof; Theorem 10.1 gives no rate. 3-digit precision is achieved for $G\le256$ (relative error $\le0.2\%$) and 2-digit for $G\le1536$ ($\le4\%$); at $G=2046$ the relative error is $4.5\%$.

---

## 4. Constants (task 4)

### 4.1 $c_p$ [computer-assisted, mpmath 30 digits; Lemma 3 proved]

`src/constants.py`, `data/constants_cp.txt`: $c_p=\max_{\xi\in(\mathbb Z/p)^\times}\prod_{r=0}^{p-1}|\cos(\pi\xi r!/p)|$.

| $p$ | $c_p$ | $\arg\max\xi$ | $(2/\pi)^p$ | $c_p^{1/p}$ |
|---|---|---|---|---|
| 2 | 0 (exact) | — | .405 | 0 |
| 3 | 1/8 (exact) | 1 | .258 | .500 |
| 5 | 0.1323771 | 1 | .1046 | .667 |
| 7 | 0.0823662 | 1 | .04238 | .700 |
| 11 | 0.0266813 | 2 | .006961 | .719 |
| 13 | $3.29992\cdot10^{-3}$ | 2 | $2.821\cdot10^{-3}$ | .644 |
| 17 | $5.37360\cdot10^{-4}$ | 2 | $4.634\cdot10^{-4}$ | .642 |
| 19 | $2.13364\cdot10^{-4}$ | 4 | $1.878\cdot10^{-4}$ | .641 |
| 23 | $4.82125\cdot10^{-5}$ | 2 | $3.085\cdot10^{-5}$ | .649 |
| 29 | $5.69609\cdot10^{-6}$ | 1 | $2.054\cdot10^{-6}$ | .659 |
| 31 | $6.10483\cdot10^{-6}$ | 4 | $8.323\cdot10^{-7}$ | .679 |
| 37 | $2.11192\cdot10^{-7}$ | 11 | $5.541\cdot10^{-8}$ | .660 |
| 41 | $1.32397\cdot10^{-10}$ | 2 | $9.101\cdot10^{-9}$ | .574 |
| 43 | $6.46370\cdot10^{-7}$ | 4 | $3.688\cdot10^{-9}$ | .718 |
| 47 | $4.19921\cdot10^{-11}$ | 8 | $6.059\cdot10^{-10}$ | .601 |
| 53 | $4.02552\cdot10^{-14}$ | 10 | $4.033\cdot10^{-11}$ | .559 |

The maximum is attained at exactly two $\xi$ ($\pm\xi_0$) for every odd $p$. $c_p/(2/\pi)^p$ is erratic ($0.015$ at $p=41$, $175$ at $p=43$): no monotone trend, so $c_p$ is not a clean "random-phase" constant.

**Lemma 3 [proved].** For odd $p$, the geometric mean over $\xi\in(\mathbb Z/p)^\times$ of $\prod_{r=0}^{p-1}|\cos(\pi\xi r!/p)|$ equals $2^{-p}$.
*Proof.* For $0\le r\le p-1$, $r!$ is a unit mod $p$, so $\xi\mapsto\xi r!$ permutes $(\mathbb Z/p)^\times$ and $\prod_{\xi}|\cos(\pi\xi r!/p)|=\prod_{k=1}^{p-1}|\cos(k\pi/p)|=2^{1-p}$ (for odd $n$, $\prod_{k=1}^{n-1}2\cos(k\pi/n)=\pm1$: the numbers $2\cos(2\pi j/n)$, $1\le j\le n-1$, are the roots of the monic polynomial $\prod_j(X-\zeta^j-\zeta^{-j})$ whose constant term is $\prod_j(-(\zeta^j+\zeta^{-j}))=\prod_j(-\zeta^{-j})(\zeta^{2j}+1)$, and $\prod_{j=1}^{n-1}(1+\zeta^{2j})=\prod_{j=1}^{n-1}(1+\zeta^j)=\Phi(-1)$ with $\Phi(X)=\prod_{j=1}^{n-1}(X-\zeta^j)=(X^n-1)/(X-1)$, so $|\Phi(-1)|=1$ for odd $n$; and $\{2\cos(2\pi j/n)\}=\{\pm2\cos(k\pi/n)\}$ as multisets of absolute values). Multiply over the $p$ values of $r$ and take the $(p-1)$-th root. ∎ The computed geometric-mean column equals $2^{-p}$ to 15 digits for every odd $p\le53$.

### 4.2 Single-gate-block $L^1$ sums [computer-assisted, double precision]

`src/gatesum.c`: $L^{\rm unit}(p,i)=\sum_{\xi\in(\mathbb Z/p^i)^\times}\prod_{u=0}^{p-1}\big|\cos(\pi\xi e_u/p^i)\big|$, $e_u=(-1)^u(p-1)!/u!\in\mathbb Z$ (so $e_0=-e_1=(p-1)!$, $e_{p-1}=1$), and the budget $B(p,i)=p^i(1-\tfrac1p)\,I_p$ with $I_p=\int_0^1\prod_u|\cos(\pi e_u\theta)|\,d\theta$.

*Computing $I_p$ [structure proved; quadrature floating point].* Put $\Theta=(p-1)!\,\theta$; the integrand is $F(\Theta)=\cos^2(\pi\Theta)\prod_{u=2}^{p-1}|\cos(\pi\Theta/u!)|$. For $u\ge2$, $u!/2\in\mathbb Z$, so $\cos(\pi\Theta/u!)$ vanishes only at $\Theta\in u!(\tfrac12+\mathbb Z)\subseteq\mathbb Z$; hence $F$ is real-analytic on every open unit interval $(k,k+1)$ and continuous on $[k,k+1]$, and $I_p=\frac1{(p-1)!}\sum_{k=0}^{(p-1)!-1}\int_0^1F(k+t)\,dt$ with each piece evaluated by $n$-point Gauss–Legendre (spectral convergence on each piece). Node-count checks: $p=5$: 8/16/32 nodes agree to $3\cdot10^{-10}$, and a $10^6$-point midpoint rule to $10^{-9}$ (first attempt); $p=11$: 16 vs 32 nodes, $I=0.00816212220575$ vs $0.00816212220551$ ($3\cdot10^{-11}$ relative); $p=13$: 12 vs 8 nodes, $0.00330918392005$ vs $0.00330918392125$ ($4\cdot10^{-10}$ relative; `data/gatesum_p13_ngl8.txt`, this retry).

| $p$ | $I_p$ | $I_p/(2/\pi)^p$ | $L^{\rm unit}(p,i)/B(p,i)$ for $i=1,\dots,8$ |
|---|---|---|---|
| 5 | 0.1220287868 | 1.1670 | 0.5726, 1.1313, 0.9168, 1.00026, 1.000027, 1.0000004, 1.0000000, 1.0000000 |
| 7 | 0.0496033637 | 1.1704 | 0.6825, 0.5361, 1.0024, 1.0047, 0.99946, 0.9999961, 1.0000000, 1.0000000 |
| 11 | 0.0081621222 | 1.1725 | 0.7396, 1.5673, 0.9116, 1.00008, 0.99931, 0.99970, 1.0000287, 1.0000000 |
| 13 | 0.0033091839 | 1.1729 | 0.1963, 0.9610, 0.8659, 1.0285, 0.99772, 0.99992, 1.0000067, 1.0000000 |

(raw $L^{\rm unit}$, $L^{\rm all}$, max term and argmax per $i$ in `data/gatesum_p*.txt`; e.g. $L^{\rm unit}(13,8)=2\,491\,756.687$ over $7.5\cdot10^8$ units.)

*Reading.* $L^{\rm unit}(p,i)/B(p,i)\to1$ with error $\ll p^{-i}$-fast (relative error below $10^{-7}$ at $i=8$ for all four primes; the printed ratios are rounded to 7 decimals): for a **fixed** finite set $\{e_u\}$ the unit points $\xi/p^i$ equidistribute against this (Riemann-integrable) integrand, as Weyl's criterion predicts, and the convergence is numerically far better than the trivial Lipschitz bound. The random-phase budget $p^i(1-\tfrac1p)(2/\pi)^p$ used in note §10.5 is low by the factor $I_p/(2/\pi)^p=1.167,1.170,1.173,1.173$ — this is exactly the "per-level ratio $\approx1.17$ for every $p$ tested" that track R2b measured (note §10.5, evidence for Conjecture 10.23), now identified as $I_p/(2/\pi)^p$: the two equal frequencies $e_0=-e_1$ give $E\cos^2=\tfrac12$ instead of $(2/\pi)^2$, which alone would give the factor $\tfrac12(\pi/2)^2=1.2337$; the arithmetic resonances among the $e_u$ ($e_{u-1}=-u\,e_u$) pull it down to $\approx1.17$. The value appears to converge in $p$ ($1.1670,1.1704,1.1725,1.1729$); we did not compute $p\ge17$ ($I_{17}$ needs $16!\approx2\cdot10^{13}$ pieces: out of budget). This is the "insufficient first step" of note §10.6 item 1 (single gate blocks, fixed level): it says nothing about the windows of length $p^{t-1}$ that RMF needs.

---

## 5. Gaps and honesty

- All limit statements in §1 ("$EZ^2\sim c_pp^G/4$", "truncated moments stable for odd $p$, growing for $p=2$"), the mechanism in Observation B, the fit in §3 and all of §4.2 are readings of finite data. The only proved statements are Lemmas 1–3, Proposition 2, and the correctness of the two DP formulations (§1.2).
- Monte Carlo errors are binomial standard errors of independent exact decisions; the PRNG is xoshiro256** seeded per thread; no overflow occurred, so no sample was mis-classified.
- Double precision in §4.2 (sums of up to $7.5\cdot10^8$ positive terms accumulated in long double per thread): relative error $\lesssim10^{-9}$, adequate for every ratio quoted, not a certificate. $I_p$ is not interval-verified.
- The reading of Kitamura's $11.5/G$ is an inference; the repository does not define it. We did not re-verify Kitamura's witness files; our reproduction of $g_2(34),g_2(1102),g_2(3456)$ is an independent two-sided computation (death level exact by §1.2).
- $g_2(594)$: we only reach cap 16382 (memory/time; Kitamura reports $\ge65536$).
- The first attempt's conditioned-moment table in `logs/writeup_2026-10-12_first_attempt.md` is superseded by §1.5 (same numbers, extended to the completed $G$).

## 6. Commands and timings

All runs: $\le4$ threads, each $\le45$ min, $<4$ GB (largest: `gsample_nl33` at cap 2046, two $2^{20}\times33\times8$-byte buffers $\approx0.6$ GB per thread). Machine shared with other agents (load 5–12).

First attempt (2026-10-12; `logs/annealed.log`, `logs/queue.log`, `logs/quick.log`):
- `clang -O3 -march=native -o src/annealed src/annealed.c -lpthread`; `src/annealed p G 4 > data/annealed_p{p}_G{G}.txt`. Timings: $p=2$: $G\le22$ $\le1$ s, 24: 6 s, 26: 25 s, 27: 51 s, 28: 127 s; $p=3$: 16: 29 s, 17: 111 s; $p=5$: 10: 55 s, 11: 490 s; $p=7$: 8: 141 s, 9: 3932 s.
- `clang -O3 -march=native -DNL=N -o src/gsample_nlN src/gsampleN.c -lpthread` ($N=2,4,5,9,17,33,65$); range mode `src/gsample_nlN -1 0 CAP 4096 4` for CAP $=32,254,1022,2046,4094$ (0, 1, 2, 10, 38 s); Monte Carlo `src/gsample_nl2 40000000 20261012 126 4` (155 s), `gsample_nl5 20000000 20261013 256 4` (375 s), `gsample_nl9 2000000 20261014 512 4` (141 s), `gsample_nl17 1000000 20261015 1024 4` (353 s), `gsample_nl33 200000 20261016 2046 4` (324 s).
- `clang -O3 -march=native -o src/gatesum src/gatesum.c -lpthread -lm`; `src/gatesum 5 8 4 16`, `7 8 4 16` (<1 s), `11 8 4 16` (12 s), `13 8 4 12` (152 s).
- `python3 -I src/constants.py`, `src/brute_check.py`.
- Kitamura fetches (read-only, 2026-10-12 and re-fetched 2026-10-20): `gh api -H "Accept: application/vnd.github.raw" repos/KitaKen1/erdos-404-p2-landscape/contents/{README.md,witness_gallery.md,determining_exact_values.md,index.html,data/p2_exact_table_1_256.csv,scripts/*.py}`.

This retry (2026-10-20; `logs/xcheck_annealed.log`, `logs/deep.log`, `logs/r3b_extra.log`):
- `python3 -I src/annealed_post.py; src/surv_post.py; src/mc_post.py; src/assemble_results.py; code/post_extra.py` (seconds).
- `clang -O3 -march=native -o code/xcheck_annealed code/xcheck_annealed.c`; `sh code/run_xcheck.sh` (two processes, chunked by class parity): results in `logs/xcheck_annealed.log` and §1.3.
- `clang -O3 -march=native -o code/p2add code/p2add.c`; `sh code/run_deep.sh` (`p2add CAP a 22`): 3456/4900 0.5 s, 2210/16382 8.9 s, 1102/11600 12.6 s, 34/18500 25.4 s; 594/16382 see below.
- `src/gatesum 13 0 2 8` (72 s), `src/gatesum 11 0 2 32` (GL node checks).

Late results (appended when the background runs finished):
- `p2add 16382 594 22`: **survived** (no death below $2^{16382}$): max population $2\,136\,196$, 116 s CPU; consistent with Kitamura's $g_2(594)\ge65536$. Row in `data/deep_lift.txt`.
- Cross-check (`code/compare_xcheck.py`, `data/xcheck_annealed.json`): `code/xcheck_annealed` **agrees exactly** with `src/annealed` in classes, survivors, $\sum N$, $\sum N^2$ and $\max N$ for $(p,G)=(2,16),(2,18),(3,10),(3,11),(5,6),(5,7),(7,5),(7,6)$ (plus $(2,8),(3,8)$ by hand); e.g. $(7,6)$: $\sum N=6\,316\,047\,228\,704$, $\sum N^2=1\,357\,291\,750\,527\,971\,456\,457\,138$. The case $(3,11)$ was added to `data/` in this retry (`src/annealed 3 11 2`, 1 s).
- Final machine-readable aggregate: `data/results_retry.json` (= `results.json` re-assembled on the complete data, plus `annealed_overview`, `annealed_buckets`, `kitamura_11p5_comparison`, `xcheck_annealed_independent_program`, `deep_lift_p2add`, `gate_integral_node_checks`, `mc_fits`).

## 7. Credit

- Kitamura (KitaKen1, `erdos-404-p2-landscape`, July 2026): the exact $p=2$ table $a\le256$ (our oracle in §2), the records $f(34,2)=18444$, $f(1102,2)=12633$, $f(3456,2)=8275$, $f(14,2)=1533$ (reproduced here), $f(594,2)\ge66126$, the critical-branching reading and the "$\sim11.5/G$" remark (interpreted in §2.4). Kitamura's determinacy lemma (= note Thm 3.1(a)) is what makes the class census meaningful.
- Tao (forum, 29 Sep 2025): block/gate framework behind the $e_u$ of §4.2. Kovač (2025): corrected statement. Lin (1960): original computations.
- Round 1 track D (`code/D/gsample256.c`) is the ancestor of `src/gsampleN.c`; round 1 track E (`code/E/tree.c`) and the census of note §4.7 supplied the reference densities; round 2 track R2b first measured the $\approx1.17$ gate-block ratio that §4.2 identifies as $I_p/(2/\pi)^p$; round 2 §10.1 (track R1b) motivates the $\mathrm{maxv}\le K$ truncation.
- The cosine-product identity in Lemma 3 is classical. Everything else in this track is routine computation; no claim of mathematical novelty beyond the new exact value $g_2(2210)=6261$ and the new exact densities $\delta_{11}(5)$, $\delta_9(7)$.
