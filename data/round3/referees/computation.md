# Round-3 computational referee report (note.md §11, revision 3)

*Referee:* the round-3 computational referee, an AI instance working separately from the tracks, the checkers and the lead. No human has checked this report.
*Date:* 2026-10-13.
*Scope:* the decisive computations of note.md §11.1–§11.4, plus Proposition 11.11 of §11.3. §11.5 (track R3C) is out of scope.
*Code and logs:* `code/round3/referee_computation/` (README there; every log starts with its command line). Scratch and binaries: `/tmp/r3_ref_computation/`.
*Independence:* every program was written for this report and shares no code with the tracks (R3N, R3Q, R3M, R3F) or their checkers. From the tracks I used only the shipped data (witnesses, survey CSVs) and the parameters printed in their logs and reports.
*Resources:* one core, `nice -n 10`, sequential jobs. Peak memory was 2.5 GB, for the optional 17662 run; everything else stayed under 0.5 GB. Total CPU was about 47 minutes, 29 of them for the 17662 run, which hit its timeout. No job ran longer than 30 minutes.

## 0. Verdict

**No fatal and no serious discrepancy.** Every computation I re-ran agrees exactly with the note. Exact quantities agree exactly, and floating-point quantities agree to all printed digits. The five assigned items, and a few extras, are all confirmed:

| # | claim (note.md line) | my method | result |
|---|---|---|---|
| 1 | witnesses for $f(594,2)\ge90394$ and $f(17662,2)\ge221465$ (l. 1891–1892) | third verifier: binary splitting of $\sum n!$ in CPython integers, then $v_2$ | **confirmed**: $v_2$ is exactly 90394 and exactly 221465; minimum $=a$; strictly increasing; 44801 / 101480 terms |
| 2a | survey rows, Theorem 11.4 (l. 1903–1910) | own exhaustive solver `rsolve.c`, both directions at $K=f$ and $K=f+1$; witnesses re-verified; an independent breadth-first oracle for rows with $g\le300$ | **confirmed**: 320 random rows plus $a=34,1102,17534$, 0 failures (306 rows also confirmed by the oracle) |
| 2b | $f(594,2)=90394$, Theorem 11.2 (l. 1887–1891) (optional) | `rsolve 594 90395` and `rsolve 594 90394` | **confirmed**: unreachable at 90395, with maximum valuation over all $P$ equal to 90394; reachable at 90394, with a new 44804-term witness that verifies; tree size identical to programs B, C and D |
| 3a | Lemma 11.5 certificate (l. 1936–1941) | integer evaluation; $v(S')$ from a divided difference at step $2^{40}$; two representatives per class | **confirmed**: 4/32/128 qualifying words, 0 violations; (d) and (e) empty |
| 3b | Corollary 11.8 rows (l. 1962–1966), Theorem 11.9 total (l. 1971) | Theorems A and B of R3Q.md re-implemented from their statements, in exact rationals | **confirmed**: $K=37$: 0.1005059170; $K=40$: 0.0910330229; $K=448$: 0.0455551120 (incl. Theorem B on $C_{14}$); the three-class total at $2^{40}$ is 0.0285330 |
| 4a | $\rho_d$ of a single gate block, Theorem 11.19 (l. 2046) | mpmath, 40 digits, exact phase reduction; float64 for higher $d$ | **confirmed**: $p=7$, $d\le6$ (to $d\le8$ in float64); $p=13$, $d\le4$ (to $d\le6$); every table entry is a correct upward rounding |
| 4b | Theorem 11.17: the only relation, and $L^2$ ratio $3/2$ (l. 2042) | enumeration of $\{-1,0,1\}^p$ ($p=7,11$, also 13); direct summation of $Q_d$ | **confirmed**: only $\pm(e_{p-2}+e_{p-1})$; weight ratio exactly $3/2$; direct $Q_d/(N_d2^{-p})=1.500000000000$ at $p=7$, $d=5,6,7$ and $p=11$, $d=8$ |
| 5 | Proposition 11.11 (l. 1995–2000) at $p=5$ | brute-force child counts at every $x'=x_0+5^mw$, against the identity | **confirmed** on 5 windows ($D=2,2,2,2,3$): 0 mismatches in (i); $\mathbb E Y$ exact; $\mathbb E Y^2$ and Var agree to $10^{-46}$ and $10^{-54}$; Cauchy–Schwarz bound holds |
| extra | closed-form checks behind Theorems 11.7 and 11.9 (l. 1958, 1971) | own transcription of the majorants in R3Q.md | **confirmed**: largest failing $K$ is 3071; margin 0.6252 bits; $q\le0.3565$; Theorem A′ form holds on $[1024,4\cdot10^6]$ |
| extra | table-level claims of §11.1 (l. 1906–1919) | bookkeeping on the CSVs | **confirmed** |
| extra | the four shadows $a=2^t-2$, $t=14..17$ (l. 1916) | `rsolve` in both directions plus witnesses | **confirmed**: 20215, 37403, 90619, 135292 |
| extra | $f(17662,2)\le221465$ (l. 1892) | `rsolve 17662 221466` | **not completed** within the 30-minute job limit (§2.5); the witness side is confirmed (item 1) |

The findings in §7 are all **minor**: wording, file naming, and one rounding slip in a track report. None changes a number in §11.

## 1. Witnesses (task item 1)

`verify_witness_bsplit.py` writes $A=\{n_1<\dots<n_k\}$, $n_1=a$, as $S=(a-1)!\cdot T$ with $T=\sum_i\prod_{m=a}^{n_i}m$. It computes $T$ by **binary splitting** over the index range. A block $[i,j)$ carries the pair $(R,T)$, with $R=\prod_{m=n_{i-1}+1}^{n_{j-1}}m$ and $T=\sum_{l=i}^{j-1}\prod_{m=n_{i-1}+1}^{n_l}m$. Two blocks combine as $R=R_1R_2$ and $T=T_1+R_1T_2$. Leaf ranges are product trees. The arithmetic is CPython's own big integers, not GMP. $v_2((a-1)!)$ is taken both from Legendre's formula and from `math.factorial`.

This is a third method. The track used running products in Python and GMP; the checker used backward Horner and odd parts. The verifier passed a self-test against direct sums on 400 random sets, and has negative controls.

| file | terms | min | max | strictly increasing | $v_2(\sum n!)$ | claimed | time |
|---|---|---|---|---|---|---|---|
| `witness_594_K90394.txt.gz` | 44801 | 594 | 90397 | yes | **90394** | 90394 | 1.2 s |
| `witness_17662_K221465.txt.gz` | 101480 | 17662 | 221465 | yes | **221465** | 221465 | 4.0 s |

Controls: dropping the last term gives 90389 and 221457; dropping the second term gives 590 and 17653. The SHA-256 of the decompressed files are `ea44330f…` and `9e37ef6d…`, matching `witness_sha256.txt`; see finding F2 on the file names there.

Hence $g_2(594)=90394-v_2(594!)=90394-590=89804$ and $g_2(17662)=221465-17653=203812$, as stated.

## 2. Exact values of $f(a,2)$ (task item 2)

### 2.1 The solver `rsolve.c`

It decides $R(a,K)$: is there a finite $P$ with $\min P=a$ and $2^K\mid\sum_{n\in P}n!$?

**Reduction.** Let $N_K=\min\{N:v(N!)\ge K\}$. Then only $P\subseteq[a,N_K)$ matters. A prefix up to stage $N<N_K$ survives iff $2^{v(N!)}\mid S_N$, and the last stage needs $2^K\mid S_{N_K}$.

**State.** $t_N=S_N/2^{v(N!)}$ modulo $2^{K-v(N!)}$, updated by $t_{N+1}=(t_N+xU_N)/2^{v(N+1)}$, where $U_N$ is the odd part of $N!$.

**Speed.** A 128-bit window carries $t_N$ between rebase stages. The rebase stages are fixed in advance. At a rebase, a per-level exact accumulator is updated by signed shifted additions, only at the stages where the current path differs from the cached one, and then shifted. Every rebase makes two consistency assertions:
- the bits shifted out are zero;
- the window value agrees with the exact value on its valid bits.

Neither assertion ever fired. When $K$ is unreachable, the program also reports the **maximum valuation over all $P$** (the "best" value), so one exhaustive run at $K=f+1$ gives $f$ exactly. When $K$ is reachable, it writes a witness.

**Validation.**
- Known values: $f(2,2)=254$ (Lin), $f(14,2)=1533$, $f(38,2)=828$, $f(34,2)=18444$, $f(1102,2)=12633$.
- **Tree size.** At $K=f+1$ my count of alive nodes satisfies $\mathrm{steps}_B=2\cdot\mathrm{nodes}+1$ exactly, against program B's logged step counts:

  | $a$ | steps (B) | my nodes |
  |---|---|---|
  | 2 | 19479 | 9739 |
  | 14 | 1233471 | 616735 |
  | 38 | 345081 | 172540 |
  | 34 | 95198259 | 47599129 |
  | 594 | 8306671179 | 4153335589 |

  So my program enumerates exactly the same tree as B, C and D.

*Remark on independence.* My window schedule turned out to coincide with that of the checker's program D. At $a=594$, $K=90395$ my rebase count is 51 825 254, which equals D's "surv". My exact-update count is 210 608 144, against D's "updates" 210 608 143. I did not read D's code. The coincidence means the two programs share a design choice, not code. So mine is an independent implementation, not a structurally different algorithm from D. The breadth-first oracle (§2.2) and the binary-splitting witness checks are structurally different.

### 2.2 Survey sample, and $a=34$, 1102, 17534 (`check_survey.py`, log `survey_sample.log`)

The survey CSVs contain 16 382 distinct exact rows, every even $a\le32768$ except 594 and 17662 (see F3). They contain no conflicting duplicates, and their $v_2(a!)$ and $g$ columns are consistent.

From these rows I drew a random sample of 320 (seed 404). Its excess $g$ ranges from 3 to 44 786, with median 8. The sample happens to include $a=16846$, the fourth-largest excess ($f=61625$, 0.93·10⁹ nodes, 90 s), and $a=22050$ ($g=16628$). Each sampled row, and also $a=34,1102,17534$, was run in both directions:
- `rsolve a f` must be reachable, and its witness must verify, by binary splitting, with $v_2$ **exactly** $f$;
- `rsolve a f+1` must be unreachable, with best $=f$;
- for the 306 rows with $g\le300$, a pure-Python breadth-first oracle must also give reachable$(f)=1$ and reachable$(f+1)=0$. Its states are partial sums mod $2^K$, deduplicated, with no windows.

**Result: 323/323 rows OK, 0 failures** (226 s in total).

| $a$ | $f$ | $K=f$ | $K=f+1$: best | nodes at $f+1$ | time (both directions) |
|---|---|---|---|---|---|
| 34 | 18444 | reachable; witness $v_2=18444$ | 18444 | 47 599 129 | 2.2 s |
| 1102 | 12633 | reachable; witness $v_2=12633$ | 12633 | 34 190 128 | 1.9 s |
| 17534 | 77053 | reachable; witness $v_2=77053$ | 77053 | 1 375 047 316 | 116 s |

### 2.3 $a=594$ at $K=90395$ (optional; log `rsolve_594.log`)

- `rsolve 594 90395`: reachable=0, best=**90394**, nodes=4 153 335 589 $=(\mathrm{steps}_B-1)/2$; 367 s, 0.5 GB.
- `rsolve 594 90394`: reachable=1, with a **new** witness (44 804 terms, in $[594,90399]$, different from the shipped one). My verifier gives $v_2=90394$ exactly; 111 s.

So $f(594,2)=90394$ is confirmed in both directions by a fourth exhaustive implementation and a fourth witness check.

### 2.4 Shadows (log `rsolve_shadow.log`)

All four shadow values of l. 1916 are confirmed in both directions, with own witnesses verified by binary splitting:

| $a$ | $f$ | witness terms |
|---|---|---|
| 16382 | 20215 | 1903 |
| 32766 | 37403 | 2292 |
| 65534 | 90619 | 12 558 |
| 131070 | 135292 | 2105 |

### 2.5 $a=17662$ at $K=221466$ (optional extra; log `rsolve_17662.log`)

**Not completed.** `timeout 1750 rsolve 17662 221466` hit the 30-minute per-job limit (exit 124) and gave no result. It needed 2.5 GB for its table of exact odd parts. My program prints no partial progress, so the run says nothing either way.

The upper bound $f(17662,2)\le221465$ therefore still rests on the two programs named in the note: the track's dfsW4 and the checker's D, with identical tree sizes. I independently confirmed only the lower bound, through the shipped witness (§1). For comparison, the tree is about $0.7\times$ the size of the 594 tree (by D's count), but each exact update works on numbers about $2.3\times$ longer. The checker's D needed about 0.5 h for this case and the track's dfsW4 about 1.5 h, so a run beyond this referee's 30-minute job limit is to be expected.

### 2.6 Table-level claims of §11.1 (`csv_claims.py`)

This takes the CSV values, with 594 and 17662 set to the exact values of Theorem 11.2. It confirms:
- All 16 384 even $a\le32768$ are covered.
- $g\notin\{1,2,4,5\}$, and $g=3\iff a\equiv4\pmod8$, with 0 violations (l. 1910).
- The largest-excess list (l. 1914), including "594 is the largest for $a\le16384$" and the $a\le4096$ list 34, 1102, 2210, 3456, 1438, 574, 1602, 640, 2662.
- The survival law (l. 1919): $G\cdot\#\{g\ge G\}/16384=10.25,11.47,10.88,11.75,10.75,9.50,10.00,10.00,8.00,8.00$ for $G=2^8,\dots,2^{17}$. All are in $[8,12]$; the last two rest on counts of 2 and 1.

## 3. R3Q (task item 3)

### 3.1 Lemma 11.5 (`lemma3_cert.py`)

The derivative is never formed symbolically. For an integer polynomial $S$ and $h=2^{40}$,
$$\big(S(x+h)-S(x)\big)/h\equiv S'(x)\pmod{2^{40}},$$
so $v(S'(x))$ is read off from two exact integer evaluations. Each residue class is evaluated at two integer representatives ($r$ and $r+2^c\cdot7919$), which agree everywhere.

| check | qualifying $(x,e)$ | violations |
|---|---|---|
| (a) $x\equiv0\ (8)$, mod $2^4$, $n_0=6$, slope 1 | 4 | 0 |
| (b) $x\equiv2\ (16)$, mod $2^7$, $n_0=8$, slope 3 | 32 | 0 |
| (c) $x\equiv6\ (16)$, mod $2^{11}$, $n_0=10$, slope 3 | 128 | 0 |
| (d) $x\equiv10\ (16)$, mod $2^7$, $n_0=6$: none | 0 | 0 |
| (e) $x\equiv4\ (8)$, mod $2^4$, $n_0=4$: none | 0 | 0 |

These counts equal R3Q's 4/32/128. The largest case is (c): $128\cdot2^9=2^{16}$, as the note says.

As a consequence test, not part of the certificate, I took 200 random 2-adic $x$ per class and enumerated every path alive at every $n\le24$. Every alive path at $n\ge n_0$ has the claimed slope: 11 296, 20 674 and 7 883 (path, $n$) pairs on $C_0$, $C_2$, $C_6$, all with the claimed slope. I also confirmed $g_2<7$ on $10+16\mathbb Z_2$ and $g_2<4$ on $4+8\mathbb Z_2$ for 200 random $x$ each, by the exact truncation criterion.

### 3.2 Corollary 11.8 rows (`cord_row.py`)

Theorem A (each of $C_0,C_2,C_6$) and Theorem B with Proposition 10 ($C_{14}$) are re-implemented from their statements in R3Q.md §4 and §6. All hypotheses are asserted, including the window conditions (W1)–(W3) of the chain. The arithmetic is exact rational, with $T=2^K-2K-12$ and the logged parameters $(n_s,k,m_1)$. Sums are taken exactly up to $n_s+6000$ terms, plus a rigorous tail majorant (below $2^{-5800}$).

| $K$ | $C_0$ | $C_2$ | $C_6$ | $C_{14}$ | **total (exact)** | note |
|---|---|---|---|---|---|---|
| 37 | 6.655701e-3 | 2.050320e-2 | 1.084701e-2 | 1/16 | **0.1005059170** | 0.10051 |
| 40 | 8.041400e-3 | 1.368294e-2 | 6.808681e-3 | 1/16 | **0.0910330229** | 0.09104 |
| 448 | 9.813758e-25 | 1.222289e-24 | 4.465779e-24 | 4.555511e-2 | **0.0455551120** | 0.04556 |

At $K=448$ the Theorem B terms are $B_1=2.6\cdot10^{-141}$, $B_2=2.679443\cdot10^{-2}$, $B_3=5.203247\cdot10^{-3}$, $B_4=1.525902\cdot10^{-5}$ and $B_5=1.354217\cdot10^{-2}$, with $\Lambda=183$, $K_t=447$ and $\ell_B=105$. All agree with `scan_D.log`.

Every note value is the correct upward rounding. The three-class total at $2^{40}$ is 0.0285330, so "$\le0.02854$" (l. 1971) is right. For the other staircase columns ($2^{64}$, $2^{512}$, $2^{1024}$, $2^{2048}$), the note's roundings agree with the track's independent `verify.log`; I did not recompute them.

### 3.3 Extra: the closed-form checks (`rule_check.py`)

I transcribed the nine-term majorant of the proof of Theorem C from R3Q.md §7. Under the rule $R(K)$ I computed $q$ and $q_A$ exactly for every $K$.
- The largest $K\in[2400,4\cdot10^6]$ where the majorant exceeds $2^{-K/80}$ is **3071**.
- The minimum margin on $[3072,4\cdot10^6]$ is **0.6252 bits** (at $K=3135$).
- $\max q=0.35641\le0.36$ and $\max q_A=0.03543\le0.04$.
- The Theorem A′ closed form holds on $[1024,4\cdot10^6]$ with margin $\ge4.5$ bits and $\max q=0.25538\le0.26$.

This confirms l. 1958 and Theorem 11.9. The wording of l. 1958 is defective; see F1. A rounding slip in R3Q.md is F4.

## 4. R3F (task item 4; `gate_shells.py`)

$\sigma_i=(-1)^i(p-1)!/(p-1-i)!$, and $\rho_d=S_d/(N_d(2/\pi)^p)$. The last column is the table of R3F Theorem A5, whose entries are certified upper bounds rounded up in the 4th decimal. Each of my values lies below its table entry, by less than $10^{-4}$.

| $p$ | $d$ | $S_d$ (mpmath, 15 digits shown) | $\rho_d$ | table |
|---|---|---|---|---|
| 7 | 1 | 0.203125 | 0.7988243 | 0.7989 |
| 7 | 2 | 1.11692863497354 | 0.6275022 | 0.6276 |
| 7 | 3 | 14.6179274063679 | 1.1732150 | 1.1733 |
| 7 | 4 | 102.567569077682 | **1.1759905** | **1.1760** (sup) |
| 7 | 5 | 714.197536388996 | 1.1698066 | 1.1699 |
| 7 | 6 | 5002.08296311101 | 1.1704384 | 1.1705 |
| 7 | 7, 8 (float64) | 35014.716847, 245103.017667 | 1.1704430, 1.1704430 | 1.1705, 1.1705 |
| 13 | 1 | 0.00779521409915467 | 0.2302530 | 0.2303 |
| 13 | 2 | 0.496094796892467 | 1.1271935 | 1.1272 |
| 13 | 3 | 5.81086941548264 | 1.0156208 | 1.0157 |
| 13 | 4 | 89.7287668156242 | **1.2063652** | **1.2064** (sup) |
| 13 | 5, 6 (float64) | 1131.57392941, 14742.90177 | 1.1702716, 1.1728524 | 1.1703, 1.1729 |

Float64 and mpmath agree to all printed digits at every common level. $\rho_8(7)=1.1704430$ lies in R3F's enclosure $J_7\in[1.17036,1.17053]$.

**Lemma 11.16 spot check.** For actual gate blocks $y_i(K')=\prod_{s\le i}(p^tK'-(p-s))$, I checked $p=7$, $t=6$, $K'\in\{1,3,5,12\}$ and $p=13$, $t=4$, $K'\in\{1,2,7\}$. In every case $y_i\equiv\sigma_i\pmod{p^d}$ and the shells are identical for all $d\le t$.

**Theorem 11.17.** I enumerated all of $\{-1,0,1\}^p$.
- The only nonzero $\delta$ with $\langle\delta,\sigma\rangle=0$ are $\pm(e_{p-2}+e_{p-1})$, for $p=7,11$ and also 13.
- $\sum_{\langle\delta,\sigma\rangle=0}2^{z(\delta)}/2^p=1.5$ exactly.
- $R_p=\sum|\sigma_i|=1957$, 9 864 101 and 1 302 061 345, each equal to $\lfloor e(p-1)!\rfloor$.

Direct summation of $Q_d=\sum_u\prod_i\cos^2(\pi u\sigma_i/p^d)$, without the collision formula, gives $Q_d/(N_d2^{-p})=1.500000000000$ at $p=7$, $d=5,6,7$ and at $p=11$, $d=8$ ($11^8$ points). Just outside the regime, at $p=7$, $d=4$ (where $7^3=343\le1957$), the value is $1.497396$. So the threshold in Theorem 11.17 is not vacuous.

## 5. R3M Proposition 11.11 at $p=5$ (task item 5; `propB_check.py`)

For each window $(x_0,n,N)$ with (W2′) and (W3′), I enumerated the slope-0 population $P^0_n(x_0)$ by depth-first search. This enumeration was cross-checked against plain enumeration of all $2^{n-1}$ paths on two windows (`propB_population_crosscheck.log`). Then, **from scratch**, I computed the child count of every parent at every integer $x'=x_0+5^mw$, $w\in[0,5^{D+1})$, using exact valuations of $S_{(e,f)}(x')$ against $V_N(x')$. These counts were compared with
- (i) $m_W(\tau^0_e-\beta_ew)$;
- (ii) the exact rational $\mathbb E_CY$ and $\mathbb E_C[Y^2]$ against $|P|Tp^{-D}$ and $p^{-2D}\sum_\eta|A(\eta)|^2$ (explicit DFT, 50 digits), and the variance identity;
- the Cauchy–Schwarz bound $M^2\chi_W^2$.

| $(x_0,n,N)$ | $m$ | $D$ | $\lvert P\rvert$ | distinct $\beta$ | (i) mismatches | $\mathbb E Y$ | $\mathbb E Y^2$ exact | spectral diff | Var / $(M^2\chi^2)$ |
|---|---|---|---|---|---|---|---|---|---|
| (80,15,22) | 3 | 2 | 45 | 3 | 0/5625 | 1152/5 ✓ | 266432/5 | 0 | 0.0040 |
| (565,16,25) | 4 | 2 | 34 | 2 | 0/4250 | 17408/25 ✓ | 2438546/5 | 0 | 0.0974 |
| (561,17,27) | 4 | 2 | 16 | 2 | 0/2000 | 16384/25 ✓ | 11232768/25 | 0 | 0.0498 |
| (335,16,25) | 4 | 2 | 18 | 2 | 0/2250 | 9216/25 ✓ | 3413798/25 | 0 | 0.0621 |
| (100,20,25) | 4 | **3** | 347 | 16 | 0/216875 | 11104/125 ✓ | 200852/25 | $4\cdot10^{-47}$ | 0.0037 |

In every case:
- $Y$ depends on $w$ only modulo $p^D$;
- the variance identity holds to $<3\cdot10^{-54}$;
- $\chi_W^2\ge(p-1)4^{-p}$ (Proposition 11.12).

The ratios Var$/(M^2\chi^2)\ll1$ agree with R3M's observation that the Cauchy–Schwarz bound is far from tight when the population is spread.

## 6. Not done

- I did not complete the exhaustive upper bound $f(17662,2)\le221465$ (§2.5).
- I did not look at §11.5 or track R3C, which are out of scope.
- I did not recompute the staircase columns at $K=64,512,1024,2048$. I also did not check $p=5,11$ of Theorem 11.19, the interval sums of §11.4(e), Propositions 11.10 and 11.13, or the Monte Carlo of §11.3.
- I did not compare the 128 values $a\le256$ with Kitamura's table itself. My sample includes $a=110,152,170,206,252$, which agree with the CSV.

## 7. Findings

**F1 (minor), note.md l. 1958 (Theorem 11.7).** The text reads: "a check that a closed-form majorant built from nine explicit terms is $\le-K/80$ for every $K\in[2400,4\cdot10^6]$. The largest failing $K$ is 3071". This contradicts itself: it claims the bound on all of $[2400,4\cdot10^6]$, then names a failing $K$ inside that range. It also compares the majorant itself, not its $\log_2$, with $-K/80$.

*Fix:* replace the bullet with: "a check that a closed-form majorant built from nine explicit terms is at most $2^{-K/80}$ for every integer $K\in[3072,4\cdot10^6]$ (the check was run on $[2400,4\cdot10^6]$; the largest failing $K$ is 3071, and the minimum margin on $[3072,4\cdot10^6]$ is 0.62 bits)." The numbers are confirmed (§3.3).

**F2 (minor), `data/round3/R3N/witness_sha256.txt`, cited at note l. 1894.** The 594 witness is listed under the name `w594_90394.txt`, which is the hash of the *decompressed* content. The shipped file is `witness_594_K90394.txt.gz`, and no hash of the .gz is given. The 17662 witness, by contrast, has both hashes under its shipped name.

*Fix:* add the two lines

`7274780bc39c08adf464fda3940a2a221f88865da739fdf8650a732992596912  witness_594_K90394.txt.gz`

`ea44330fa8074a8e02c3fc6c9cc86b0499a5efeb4fe47c01319e91e5e2da80f5  witness_594_K90394.txt (uncompressed)`

Then either rename the existing `w594_*`, `wB594_*`, `w17662_*` and `best17662_*` entries to the shipped names, or state which shipped file each one is.

**F3 (minor), survey CSVs cited as the record of Theorem 11.4 (note l. 1908).** The row $a=594$ in `survey_2_4096.csv`, and the row $a=17662$ in `survey_16386_32768.csv` and `survey_16386_32768_merged.csv`, still have status `lower`, with $f=66126$ and $148725$. These are the superseded doubling-run bounds. A reader who checks Theorem 11.4 against the CSVs alone finds two non-exact rows.

*Fix:* add one sentence after l. 1908: "In the survey CSVs the rows 594 and 17662 are lower bounds from the doubling run; their exact values are those of Theorem 11.2." Alternatively, append exact rows for them, citing the Theorem 11.2 logs.

**F4 (minor; track report, not the note), `data/round3/reports/R3Q.md` §4, proof of Theorem A′.** The constant in "$A_4\le\dots\le0.911K^22^{-K/6}$" is rounded down. The derivation gives $2.05\cdot2^3\cdot(K/6)^2\cdot2\cdot2^{-K/6}=(32.8/36)K^22^{-K/6}=0.91111\ldots K^22^{-K/6}$. The closed-form check still passes with the exact constant: the minimum margin on $[1024,4\cdot10^6]$ is 4.5153 bits, against 4.5154 with 0.911 (§3.3). So the theorem is unaffected.

*Fix:* write $0.912$, both in R3Q.md and in `rule_A.py`.

There is no finding against the computational content of Theorems 11.2, 11.4, 11.17 and 11.19, Lemmas 11.5 and 11.16, Corollary 11.8, Theorem 11.9 or Proposition 11.11.

## 8. Reproduction

The commands are in `code/round3/referee_computation/README.md`; each log in `logs/` starts with its command line. The witness checks take 5 s, the survey sample 226 s and the 594 runs 8 min. The R3Q checks take under 1 min, the shells 70 s and Proposition 11.11 25 s.
