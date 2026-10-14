# Check of round-4 track M4D: Theorem P and Corollary P1 (deep-gate localisation, plateau bounds)

Date: 2026-10-14. Lens: LOGIC AND INDEPENDENT RECOMPUTATION. Made by the `verify_D_P_recompute` track of round 4, which did not write the work it checks. Classification: Internal (research working file).

- **Claim checked:** `data/round4/reports/M4D.md` §4 (Theorem P, Corollary P1, the table of values, the paragraph "What Theorem P says about μ(K_7)"), the headline item 3, the §0 row "Thm P, Cor P1", and the §6 rows `cov_verify.py` and `plateau_check.py`.
- **Definitions and results re-read:** note.md §1.2–1.4 (normal form, $g_p$, Tao's predicate, Lemma 1.3), §3.1 (Theorem 3.1), §3.7 (definition of $\mathrm{Cov}(p,t,H)$, Theorem 3.12), §4.7 (census), §10.2 (Proposition 10.10, the certificate tables, minimal $H_t$); M4D.md §1 (F1), (F2) and the equivalence $P(x,n)\iff g_p(x)\ge V_n(x)$.
- **Data audited:** the round-2 certificate logs `data/round2/logs_original/R3/` (programs A and B) and `data/round2/review/computation/logs/` (program C); the census trees `archive/E/tree_p*.txt`.
- **My code** (written from the definitions; it shares nothing with `code/round4/M4D/` or the round-1/2 programs): `code/round4/verify_D_P_recompute/`
  - `bounds.py`: Corollary P1 arithmetic in exact rationals, plus the exact Haar measure of $\{V_{n_0}>G_0\}$;
  - `census.c`: exact class census $\delta_G(p)$ by lifting and a memoised DFS, plus the exact mass of $\{P(x,n_0)\}$ (`pmass` mode); validator `census_brute.py`;
  - `covchk.c`: $\mathrm{Cov}(p,t,H)$ by explicit enumeration plus cyclic shift-OR on one bitset; validator `cov_brute.py` (numpy brute force);
  - `covfib.c`: the same check fibred over residues mod $p^k$, for the modulus $13^9$; validator `covfib_validate.py`;
  - `audit_logs.py`: completeness audit of the round-2 certificate logs;
  - `thmP_test.c`: end-to-end test of Theorem P with exact decisions of $P(x,n)$, with controls;
  - `meaning.py`, batch scripts `cov_batch.sh`, `batch2.sh`, `thmP_batch.sh`, and the logging wrapper `run.sh`.
- **Logs:** `data/round4/verify_D_P_recompute/*.log`. Each run starts with its command line and UTC start time and ends with its exit code and wall time.
- **Budget:** one core under `nice -n 10`, about 43 core-minutes in total: 40 minutes logged over 85 runs, plus about 3 minutes of unlogged compile and smoke tests. Peak memory about 1.7 GB (one hash table for depth-7 gates at $p=13$). The longest job, $\mathrm{Cov}(13,7,39)$ over 156 classes, took 11 minutes.
- **Rule deviation:** at the end I ran one `git status` by mistake. It is read-only and changed nothing. No other git command was run, and no file of the track was modified.

## Verdict

**confirmed.** Theorem P and Corollary P1 are correct as stated, and every number M4D states for them is reproduced exactly by my own code.
- **Logic.** Theorem P is Theorem 3.12(a) transported from natural numbers $a$ to $x\in\mathbb Z_p$, run as a first-failure argument (the uniform branch of Proposition 10.10). Every step holds, with all hypotheses used and stated (§2). Corollary P1 is a correct three-term union bound, and $B_p$ is a valid lower bound for $\mu\{P(x,n_0)\}$ (§2.4). The statement does **not** use Theorem 11.14 (C3), so there are no C3 hypotheses to check.
- **Certificates.** Every certificate $\mathrm{Cov}(p,t,H_t)$, $t\le T(p)$, that Theorem P cites is in `data/round2` with exactly the stated $H_t$: in program A, program B and program C, for every unit class (§3.1). With my own code I re-ran 37 of the 38 certificates over all classes. The exception is $\mathrm{Cov}(17,7,43)$ (modulus $17^9$), which I did not re-run. All 37 hold (§3.2).
- **Census inputs.** I recomputed the six census values $\delta_{G_0}(p)$ from scratch with my own code (a memoised DFS, validated against brute force). The survivor counts agree exactly with the round-1 archive, and so do the child histograms (§4).
- **Numbers.** $T$, $n_0$, $G_0$, $b$, $k_1$, $k_0$, $n_0p^{-k_0}$, $B_p$, the 18 $G$-thresholds and the three headline bounds all agree exactly with the report (§5).
- **End-to-end.** I decided $P(x,n)$ exactly on 1101 Haar-random points that satisfy the hypotheses, at $p=7,11,13$, with gates of every depth $1\le t\le T$ forced after $n_0$. $P(x,N)$ held every time. The controls that drop a hypothesis do fail: 52/210, 71/223 and 4/91 (§6).
- **Meaning.** The result is a rigorous lower bound on $\delta_G(p)=\mu\{g_p\ge G\}$ for $G$ up to the stated ranges, sandwiching $\delta_G(p)$, for $G$ up to the $\varepsilon=0.01$ threshold, in an interval just below the census value. The interval's width is 0.010–0.019 across the six primes: 0.012 at $p=7$, 0.011 at $p=13$. It says nothing about $\mu(K_p)=\lim_G\delta_G(p)$: the bound decreases linearly in $N$ and is vacuous from $G\approx8.5\cdot10^4$ at $p=7$ (§7). M4D says this correctly in its headline.

There are two optional wording points and one optional sharpening, none of which affects correctness (§8).

## 1. The claim, restated

Fix an odd prime $p$ with uniform certificates $\mathrm{Cov}(p,t,H_t)$, $1\le t\le T$, $H_t+1<p^t$, and put $n_0=\max_tH_t$. Notation is M4D's §1: $\pi_j(x)=\prod_{i\le j}(x+i)$, $V_n=v_p(\pi_n(x))$, and $P(x,n)$ means that some $e\in\{0,1\}^n$ with $e_0=1$ has $v_p(\sum_{j<n}e_j\pi_j(x))\ge V_n(x)$.
- **Theorem P.** If $x$ is not a negative integer, $P(x,n_0)$ holds, and $v_p(x+i)\le T$ for all $n_0<i\le N$, then $P(x,N)$ holds, hence $g_p(x)\ge V_N(x)\ge v_p(N!)$.
- **Corollary P1.** $\delta_{v_p(N!)}(p)\ge B_p-(N-n_0)p^{-(T+1)}$ for $N\ge n_0$, where $B_p=\delta_{G_0}(p)-10^{-5}-n_0p^{-k_0}$, $k_0=G_0-b+k_1$, $b=\sum_{p^k\le n_0}\lceil n_0/p^k\rceil$, $k_1=\min\{k:p^k>n_0\}$. The values are the table of M4D §4, e.g. $\delta_G(7)\ge0.6119$ for $G\le1376$, $\delta_G(13)\ge0.7431$ for $G\le679\,775$, $\delta_G(13)\ge0.6531$ for $G\le6.79\cdot10^6$.

## 2. Logic, line by line

### 2.1 Standing facts (M4D §1), re-derived

1. **(F2).** For $e$ alive at $n$ with target $\tau=-S_e/\pi_n\in\mathbb Z_p$ and a window word $f$, $S_{(e,f)}=S_e+\pi_nQ_f=\pi_n(Q_f-\tau)$, so $v(S_{(e,f)})=V_n+v(Q_f-\tau)\ge V_N=V_n+D$ iff $Q_f\equiv\tau\pmod{p^D}$. Correct.
2. **Backward monotonicity.** $S_e=S_{(e,f)}-\sum_{j\ge n}f_{j-n}\pi_j$, and $p^{V_n}\mid\pi_j$ for $j\ge n$. So $P(x,N)\Rightarrow P(x,n)$ for $1\le n\le N$. Correct.
3. **$P(x,n)\iff g_p(x)\ge V_n(x)$.** (⇒) is the definition of $g_p$ (note §1.2), with $B=\{j\ge1:e_j=1\}$. (⇐) $g_p$ is integer-valued or $\infty$, so some finite $B$ has $v(S_B)\ge V_n$. Deleting the $b\ge n$ changes $S_B$ by a multiple of $\pi_n$. Correct.
4. **$V_N(x)\ge v_p(N!)$.** Among $N$ consecutive elements of $\mathbb Z_p$, at least $\lfloor N/p^k\rfloor$ are divisible by $p^k$. Correct.

### 2.2 Theorem P

| step | M4D's argument | check |
|---|---|---|
| first failure | $N^*$ = least $n\in(n_0,N]$ with $\neg P(x,n)$; $P(x,n)$ for $n\le n_0$ by 2.1(2), for $n_0<n<N^*$ by minimality | correct |
| non-gate | $v(x+N^*)=0\Rightarrow V_{N^*}=V_{N^*-1}$, and digit $0$ extends a path alive at $N^*-1\ge n_0$ | correct |
| depth | so $t=v(x+N^*)\in[1,T]$ by hypothesis; $t<\infty$ because $x\notin-\mathbb N$ | correct |
| window | $H=H_t\le n_0<N^*$; for $1\le s\le H-1$, $s<p^t$ (from $H_t+1<p^t$), so $v(p^tK''-s)=v(s)$; elements $y_i=\prod_{s\le i}(x+N^*-H+s)=y_i(K'')$; jump $D=t+\sum_{s<H}v(s)=t+c$ | correct ($H_t\le p^t$ would already suffice) |
| reduction | $\prod_s(X-(H-s))=\sum_ka_kX^k$, $X=p^tK''$: for $k\ge1$ the term mod $p^{t+c}$ depends on $K''\bmod p^{t+c-tk}$, and $t+c-tk\le c$; so $\mathrm{Cov}(p,t,H)$, a statement about integer representatives $K'<p^c$, applies to every unit $K''\in\mathbb Z_p^\times$ | correct; also tested (§3.2, lifted representatives) |
| contradiction | $N^*-H\ge1$; take $e$ alive at $N^*-H$ and $f$ with $Q_f\equiv\tau\pmod{p^{t+c}}$; by (F2) $(e,f)$ is alive at $N^*$ | correct |

So Theorem P holds exactly as stated, conditional only on the certificates.
- **Prop 10.10 / Theorem 3.12.** M4D uses only the uniform branch of Proposition 10.10, i.e. Theorem 3.12(a) at every depth $t\le T$. The positions branch, which certifies specific integers $K''$, is not used. M4D correctly explains why: it covers only 42 of the 14 406 unit classes mod $7^5$ at depth 7.
- **What replaces $N^*-H>a$.** Theorem 3.12(a) needs $N^*-H>a$ for a natural number $a$. Here the role of $a$ is played by the index origin, and the condition becomes $N^*-H\ge1$, which $n_0\ge\max_tH_t$ guarantees.
- **Credit.** M4D attributes the method to Theorem 3.12, Proposition 10.10 and Tao's first-failure idea. That is right.

### 2.3 The exact localisation identity

$K_7\subseteq\{P(x,34)\}$ by 2.1(3), since $g=\infty$. By Theorem P, $\{P(x,34)\}\setminus K_7$ is the set of $x$ whose first failure after $34$ is at an index $i$ with $v(x+i)\ge7$. So M4D's identity $\mu(K_7)=\mu\{P(x,34)\}-\mu\{P(x,34)\text{ and the population dies at a gate of depth}\ge7\}$ is correct.

### 2.4 Corollary P1: why $B_p$ is a valid starting mass, and the union bound over gates

- **(i)** If $g_p\ge G_0$ and $V_{n_0}\le G_0$, then $g_p\ge V_{n_0}$, so $P(x,n_0)$ by 2.1(3). Hence $\mu\{P(x,n_0)\}\ge\delta_{G_0}-\mu\{V_{n_0}>G_0\}$. Correct.
- **(ii) Bound on $\mu\{V_{n_0}>G_0\}$.**
  - $V_{n_0}=\sum_{k\ge1}\#\{i\le n_0:p^k\mid x+i\}$.
  - Levels with $p^k\le n_0$ contribute at most $\lceil n_0/p^k\rceil$ each, so at most $b$ in total.
  - Each level with $p^k>n_0$ contributes $0$ or $1$, and it contributes $1$ iff $m^*:=\max_{i\le n_0}v(x+i)\ge k$.
  - So $V_{n_0}\le b+\max(0,m^*-k_1+1)$, and $V_{n_0}>G_0$ forces $m^*\ge G_0-b+k_1=k_0$. This needs $b\le G_0$, which holds in all six cases.
  - A union bound over $i\le n_0$ gives $\mu\le n_0p^{-k_0}$.

  Correct. I also computed the **exact** $\mu\{V_{n_0}>G_0\}$ (`bounds.py`, cross-checked by brute force mod $p^3$ or $p^4$ on six cases). It is never larger than the union bound and equals it at $p=11,13$ (table in §5).
- **Rounding.** The printed census values are rounded to 5 decimals. From the exact counts they exceed the true values by at most $2.6\cdot10^{-6}$ (at $p=11$), so the allowance $10^{-5}$ is safe.
- **(iii) Union bound over gates.** By Theorem P, $\{P(x,n_0)\}\setminus\bigcup_{n_0<i\le N}\{v(x+i)\ge T+1\}\subseteq\{P(x,N)\}\subseteq\{g_p\ge v_p(N!)\}$. The removed set has measure at most $(N-n_0)p^{-(T+1)}$. For $N-n_0\le p^{T+1}$, which covers every tabulated case, the events are pairwise disjoint (two indices less than $p^{T+1}$ apart cannot both be $\equiv-x\bmod p^{T+1}$). So this is an equality for the removed set: the loss term is not slack in the union bound. The slack lies in charging every deep gate as fatal, which, by M4D's own data, most are not.
- **Monotonicity.** $\delta_G$ is non-increasing (Theorem 3.1(c)), so the bound at $G=v_p(N!)$ holds for every $G\le v_p(N!)$. Correct.

## 3. The certificates

### 3.1 Existence audit (`audit_logs.py`, log `audit_logs.log`)

M4D's lists of $H_t$ coincide with the uniform column of the note §10.2 table, and the minimal-$H_t$ table, for all six primes:
- $p=7$: $4,7,19,26,28,34$;
- $p=11$: $5,10,18,22,30,33$;
- $p=13$: $6,10,19,24,32,35,39$;
- $p=17$: $5,11,16,25,30,34,43$;
- $p=19$: $5,12,17,27,31,35$;
- $p=23$: $7,12,18,23,33,37$.

This gives $T=6,6,7,7,6,6$, and $H_t+1<p^t$ holds in every case.

For each of the 38 triples, the audit parsed every per-class line of program A (`U_p*_A.log`; for $(13,7,39)$, `R1_A_cov_13_7_39_all.log`), program B (`U_p*_B*.log`; for $(13,7,39)$, `R1_B_cov_13_7_39_all_lift1.log`) and program C (`review/computation/logs/U_p*.log`, `U17_t7_H43_*.log`).
- Result: **in every case and in each of the three programs, the classes reported covered are exactly the full set of units mod $p^c$, with no reported miss.** The headers' $c$ and $M=t+c$ also agree with $c=v_p((H-1)!)$.
- Program B's $\mathrm{Cov}(17,7,43)$ is split over four files (32+80+80+80 classes). The first file has no summary line, but all 32 of its class lines report coverage.

### 3.2 Own re-run (`covchk.c`, `covfib.c`)

**Validation.**
- `covchk` agreed with a numpy brute force (`np.roll` subset sums) on the **exact number of missed residues** for 1020 classes in 35 configurations, 16 of which have failing classes. Lifted representatives $K'+jp^c$, with $j$ up to 123 457, gave identical counts (`cov_validate.log`).
- `covfib` agreed with `covchk` on exact miss counts in 20 configurations with fibre levels $k=1,2,3$, and on single classes at modulus $7^{10}$ and $11^8$ (`covfib_validate.log`).

**Results** (logs `cov_p7.log` … `cov_p23.log`, `cov_p13_t7.log`, `cov_lift.log`, `cov_controls.log`, `cov13_controls.log`):

| $p$ | certificates re-run over **all** unit classes | classes | result |
|---|---|---|---|
| 7 | $t=1..6$ ($H=4,7,19,26,28,34$; largest modulus $7^{10}$) | 1, 1, 42, 294, 294, 2058 | all covered |
| 11 | $t=1..6$ | 1, 1, 10, 10, 110, 110 | all covered |
| 13 | $t=1..6$; $t=7$ ($H=39$, modulus $13^9$, fibred, $k=2$) | 1, 1, 12, 12, 156, 156; 156 | all covered ($t=7$: 660 s) |
| 17 | $t=1..6$ | 1, 1, 1, 16, 16, 16 | all covered |
| 19 | $t=1..6$ | 1, 1, 1, 18, 18, 18 | all covered |
| 23 | $t=1..6$ | 1, 1, 1, 1, 22, 22 | all covered |

- **Not re-run:** $\mathrm{Cov}(17,7,43)$ (modulus $17^9\approx1.2\cdot10^{11}$). It rests on the round-2 programs A, B and C (§3.1). It enters only the $p=17$ row of M4D's table.
- **Class invariance at the deepest levels:** with representatives $K'+3\cdot7^4$, $K'+5\cdot11^2$ and $K'+2\cdot13^2$, $(7,6,34)$, $(11,6,33)$ and $(13,6,35)$ are again covered for all classes.
- **Controls (the checker can fail):**
  - $\mathrm{Cov}(7,6,33)$ at $K'=5$ misses exactly 2 residues mod $7^{10}$ (94 559 789 and 241 978 387), as note §10.2 states.
  - $\mathrm{Cov}(7,3,18)$ fails at 21 of the 42 classes, as M4D states.
  - $\mathrm{Cov}(7,3,H)$ fails for every $H\le18$, so $H_3(7)=19$ is indeed minimal. At $K'=1$, the exact miss counts for $H=12,\dots,18$ (549, 101, 4, 12 013, 9612, 2417, 8) equal round-2 program A's unfibred scan (`scan_p7_t1-6.log`).
  - $\mathrm{Cov}(13,7,38)$ at $K'=1$ misses 64 residues mod $13^9$; fibre levels $k=1$ and $k=2$ agree. Its first failing fibre ($r=1$) misses exactly 1 residue, and $\mathrm{Cov}(13,7,37)$, $K'=1$, has first failing fibre $r=0$ with exactly 3732 missed. These are exactly the values in round-2 program A's scan (`scan_p13_t1-7.log`, lines 238–239). That scan runs with `FIBCOV_FIBRESTOP=1`, so it reports the first failing fibre only. This is an independent agreement at the full modulus $13^9$.

## 4. Census inputs (`census.c`; logs `census.log`, `census_validate.log`)

**Method.** `census.c` decides $g_p(c)\ge G$ for each class $c\bmod p^G$ by a memoised DFS over (index, target mod $p^{G-V_n}$). It lifts only the children of survivors, which is valid because $\{g\ge G\}\subseteq\{g\ge G-1\}$ and both are unions of classes (Theorem 3.1). It is validated class by class against a numpy brute force (is $-1$ a subset sum of $\{\pi_b(c)\bmod p^G:1\le b<pG\}$?) on 22 configurations up to 2401 classes, with 0 mismatches.

**Results.**

| $p$ | $G_0$ | survivors (mine) | archive/E | exact $\delta_{G_0}$ | printed in note §4.7 |
|---|---|---|---|---|---|
| 7 | 8 | 3 596 877 | 3 596 877 | 0.6239377560 | .62394 |
| 11 | 6 | 1 239 663 | 1 239 663 | 0.6997574456 | .69976 |
| 13 | 5 | 280 157 | 280 157 | 0.7545442548 | .75454 |
| 17 | 4 | 63 219 | 63 219 | 0.7569234085 | .75692 |
| 19 | 4 | 101 379 | 101 379 | 0.7779176035 | .77792 |
| 23 | 3 | 10 417 | 10 417 | 0.8561683242 | .85617 |

All lower levels and all child-survival histograms also agree with the archive. Total CPU: 83 s.

The runs in `census.log` predate the `pmass` tally. That edit did not touch the decision code, and I re-ran the validator after each edit (`census_validate.log`, three runs). The later `pmass` runs (`census_pmass.log`) reproduce the same survivor counts.

## 5. Recomputed numbers (`bounds.py`, log `bounds.log`; exact rationals)

| $p$ | $T$ | $n_0$ | $b$ | $k_1$ | $G_0$ | $k_0$ | $n_0p^{-k_0}$ | exact $\mu\{V_{n_0}>G_0\}$ | $B_p$ (mine) | report |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 6 | 34 | 5 | 2 | 8 | 5 | 2.0230e-3 | 1.8190e-3 | 0.6219070 | 0.62191 |
| 11 | 6 | 33 | 3 | 2 | 6 | 5 | 2.0490e-4 | 2.0490e-4 | 0.6995451 | 0.69955 |
| 13 | 7 | 39 | 3 | 2 | 5 | 4 | 1.3655e-3 | 1.3655e-3 | 0.7531645 | 0.75316 |
| 17 | 7 | 43 | 3 | 2 | 4 | 3 | 8.7523e-3 | 5.6872e-3 | 0.7481577 | 0.74816 |
| 19 | 6 | 35 | 2 | 2 | 4 | 4 | 2.6857e-4 | 2.4676e-4 | 0.7776414 | 0.77764 |
| 23 | 6 | 37 | 2 | 2 | 3 | 3 | 3.0410e-3 | 2.3335e-3 | 0.8531190 | 0.85312 |

**$G$-thresholds.** $N=n_0+\lfloor\varepsilon p^{T+1}\rfloor$ is the largest $N$ with loss at most $\varepsilon$. For each $\varepsilon\in\{0.01,0.05,0.1\}$ and each prime, $G=v_p(N!)$ agrees with the report: all 18 entries, from 1376 / 6867 / 13 728 at $p=7$ to 1 547 647 / 7 738 240 / 15 476 478 at $p=23$.

**Headline values:**
- $\delta_G(7)\ge0.6119076$ for $G\le1376$;
- $\delta_G(13)\ge0.7431645$ for $G\le679\,775$;
- $\delta_G(13)\ge0.6531645$ for $G\le6\,797\,756$, which is at least $6.79\cdot10^6$.

All three are at least the stated values. All checks pass (`ALL OK`).

## 6. End-to-end tests of Theorem P (`thmP_test.c`, log `thmP.log`)

**Method.**
- **Exact decision of $P(x,n)$.** I decide $P(x,n)$ exactly through $P(x,n)\iff g_p(x)\ge V_n(x)$ (§2.1(3)), running the validated census DFS with $G=V_n(x)$ on $x\bmod p^G$.
- **Sampling.** $x$ is Haar-random mod $p^L$ ($7^{21}$, $11^{17}$, $13^{16}$). Optionally I force a gate of exact depth $t$ at a random index $i>n_0$.
- **What counts as a violation.** $P(x,n_0)$ holds and $\max_{n_0<j\le N}v(x+j)\le T$, but $P(x,N)$ fails.

| run | $p$ | forced gate (exact depth, index) | premise | $N$ | samples | premise holds (decided) | $\neg P(x,N)$ | result |
|---|---|---|---|---|---|---|---|---|
| main | 7 | depth 1–6, $i\in[35,70]$ | $P(x,34)$ | 70 | 600 | 378 | 0 | **0 violations**; depths 1–6 all present (18/101/74/59/68/58) |
| main | 7 | none (plain Haar) | $P(x,34)$ | 100 | 300 | 190 | 0 | **0 violations** (natural depths 2–4) |
| main | 11 | depth 1–6, $i\in[34,70]$ | $P(x,33)$ | 70 | 400 | 289 | 0 | **0 violations** |
| main | 13 | depth 1–6, $i\in[40,60]$ | $P(x,39)$ | 60 | 300 | 215 | 0 | **0 violations** |
| main | 13 | depth 7, $i\in[40,50]$ | $P(x,39)$ | 50 | 16 + 32 | 9 + 20 (7 undecided) | 0 | **0 violations** |
| control: premise before $\max H_t$ | 7 | depth 4–6, $i\in[21,30]$ | $P(x,20)$ | 40 | 300 | 210 | 52 (10 at depth 5, 42 at depth 6) | implication fails, as it may |
| control: gate deeper than $T$ | 7 | depth 7–8, $i\in[35,45]$ | $P(x,34)$ | 45 | 150 | 91 | 4 (all at depth 8; 0 of 56 at depth 7) | deep gates can kill |
| control: premise before $\max H_t$ | 13 | depth 4–6, $i\in[21,33]$ | $P(x,20)$ | 40 | 300 | 223 | 71 (15 at depth 5, 56 at depth 6) | implication fails, as it may |

- **Totals.** In total 1101 decided samples satisfy the hypotheses of Theorem P (568 at $p=7$, 289 at $p=11$, 244 at $p=13$), with gates of every depth $1\le t\le T$ forced after $n_0$. $P(x,N)$ held in every one: 0 violations.
- **Controls.** The controls show that the test detects failures when the hypotheses are dropped. With the premise taken at $n=20<\max_tH_t$, 52/210 and 71/223 chains die at a depth-5 or depth-6 gate. Gates of depth $T+2=8$ at $p=7$ kill 4/35 chains.
- **Exactness.** Every decision in these runs is exact: a found path is a witness, and a refutation is an exhaustive memoised search. The only exception is the depth-7 run at $p=13$. There the memo (at most $9.4\cdot10^7$ states) ran out on 7 of 48 points, which are reported as undecided and excluded; none of them was refuted. The first attempt of that run, with the old build, stopped at the first full memo (exit 2, in the log) and produced no counts.
- **Comparison with M4D.** M4D's own test (`plateau_check.py`, 268 premise samples at $p=7$, depths 1–6) is the first row's analogue. Mine extends it to $p=11,13$, to a depth-7 gate, and to plain Haar sampling up to $N=100$.

**Calibration of the exact decision.** A Monte Carlo of $\mu\{P(x,n_0)\}$ on 40 000 points (`pmass_mc.log`) gives:
- $0.6238\pm0.0024$ at $p=7$;
- $0.7590\pm0.0021$ at $p=17$;
- $0.7775\pm0.0021$ at $p=19$.

Each lies in, or within one standard error of, the exact bracket $[\underline m,\underline m+\mu\{V_{n_0}>G_0\}]$ of §8 item 3.

## 7. What the result means

- **It is a statement about $\delta_G(p)$ at finite $G$.** For $G_0\le G\le$ the $\varepsilon=0.01$ threshold, Corollary P1 and the census give
$$B_p-0.01\ \le\ \delta_G(p)\ \le\ \delta_{G_0}(p).$$
  For example, $\delta_G(7)\in[0.6119,0.62394]$ for $8\le G\le1376$, and $\delta_G(13)\in[0.7431,0.75454]$ for $5\le G\le679\,775$ (`meaning.log`).
- **Interpretation.** Read through Theorem 3.1(c), the natural density of $\{a:f(a,7)\ge v_7(a!)+G\}$ stays in that window for all $G\le1376$. So the census plateau is now proved to persist far beyond the census levels, where before only $G\le8$ was known at $p=7$.
- **Consistency with round 1.** The bound is consistent with the round-1 census (note §4.7) at every level where both apply. For every prime, $B_p$ is below the exact census values $\delta_G(p)$, $G\le G_0$, and $B_p$ at $N=n_0$ is below $\delta_{v_p(n_0!)}(p)$; for example $0.6219<\delta_4(7)=0.62516$.
- **It is not a statement about $K_p$.**
  - $\mu(K_p)=\lim_G\delta_G(p)\le\delta_G(p)$, so a lower bound on $\delta_G$ at finite $G$ gives no lower bound on $\mu(K_p)$.
  - The bound loses $p^{-(T+1)}$ per index and becomes vacuous at $G\approx8.5\cdot10^4$ ($p=7$), $1.4\cdot10^6$ ($p=11$), $5.1\cdot10^7$ ($p=13$), $3.3\cdot10^8$ ($p=17$), $3.9\cdot10^7$ ($p=19$) and $1.3\cdot10^8$ ($p=23$) (`meaning.log`).
  - What Theorem P does say about $K_p$ is the localisation identity of §2.3: at $p=7$ the whole question is decided at gates of depth at least 7.
  - M4D states both points correctly (headline items 3 and 4 and the sentence "Nothing here bears on Q3"). The sentence "the rigorous lower bounds sit within about 0.01 of the conjectured limits" compares a bound on $\delta_G$ with numerical estimates of $\mu(K_p)$. That is a comparison of numbers, not a bound on $\mu(K_p)$, and M4D does not present it as one.

## 8. Remarks (optional; none affects correctness)

1. **Wording.** "within about 0.01 of the conjectured limits" (M4D §4): the gaps are $0.6239-0.6119=0.012$ at $p=7$ and $0.7545-0.7432=0.011$ at $p=13$. Suggest "within about 0.012".
2. **Wording.** In §6 (`cov_verify.py` row), "Cov(7,3,18) fails at 21 of 42 classes (so $H_3=19$ is minimal)" does not follow from one length alone, because coverage is not monotone in $H$ (note §10.2). The conclusion is true: I find every $H\le18$ failing, and so do the round-2 scans. Suggest citing the scans.
3. **Optional sharpening of $B_p$.** $\mu\{P(x,n_0)\}=\sum_k\mu\{V_{n_0}=k,\ g_p\ge k\}$, and on a class mod $p^k$ the event $\{V_{n_0}=k\}$ is decided exactly. The cases where one $x+i$ is $\equiv0\bmod p^k$ are handled with the factor $1-1/p$. My census in `pmass` mode (log `census_pmass.log`) gives the rigorous lower bound $\underline m=\sum_{k\le G_0}(\cdots)$, compared below with $B_p$. Using $\underline m$ in place of $B_p$ would raise every bound in the table by these amounts at no cost. The true value is at most $\underline m+\mu\{V_{n_0}>G_0\}$ (§5).

| $p$ | $\underline m$ | $B_p$ | gain |
|---|---|---|---|
| 7 | 0.62338 | 0.62191 | 0.0015 |
| 11 | 0.69969 | 0.69955 | 0.0001 |
| 13 | 0.75390 | 0.75316 | 0.0007 |
| 17 | 0.75456 | 0.74816 | 0.0064 |
| 19 | 0.77781 | 0.77764 | 0.0002 |
| 23 | 0.85499 | 0.85312 | 0.0019 |

4. **A hypothesis stronger than needed.** Theorem P assumes $H_t+1<p^t$, but uses only $H_t\le p^t$. This is harmless, since all certificates satisfy the stronger form.

## 9. Files

- Code: `code/round4/verify_D_P_recompute/`:
  - `bounds.py`, `meaning.py`;
  - `census.c`, `census_brute.py`;
  - `covchk.c`, `cov_brute.py`, `covfib.c`, `covfib_validate.py`;
  - `audit_logs.py`, `thmP_test.c`;
  - `cov_batch.sh`, `batch2.sh`, `thmP_batch.sh`, `run.sh`.
- Logs: `data/round4/verify_D_P_recompute/`:
  - `bounds.log`, `meaning.log`;
  - `census.log`, `census_validate.log`, `census_pmass.log`, `pmass_mc.log`;
  - `cov_validate.log`, `covfib_validate.log`, `cov_controls.log`, `cov13_controls.log`;
  - `cov_p7.log`, `cov_p11.log`, `cov_p13.log`, `cov_p17.log`, `cov_p19.log`, `cov_p23.log`, `cov_p13_t7.log`, `cov_lift.log`;
  - `audit_logs.log`, `thmP.log`.
- Scratch binaries: `/tmp/r4_verify_D_P_recompute/`.
