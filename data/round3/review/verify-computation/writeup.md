# Round-3 computational referee report (§11 of note_v3.md)

Referee: AI instance (Claude), computation lens, 2026-10-21. No human has checked this report.
Scope: every computational claim of §11 (and the §0 round-3 block) that could be re-run within the
resource limits (at most 3 cores, each run < 45 min, < 2.2 GB). All programs below were written from
the definitions in the note only; no track or lead code was read (track *data files* were read as data
where stated, to compare numbers or to re-process them). Commands and timings: `COMMANDS.log`;
programs: `code/`; outputs: `out/`.

Labels: **[re-run, agrees]** = independent recomputation reproduces the stated number;
**[not re-run]** = beyond budget or not attempted; **[finding]** = a discrepancy or a problem.

## 1. Summary of findings

| # | severity | item | finding |
|---|---|---|---|
| F1 | minor (serious if the densities are advertised as "two programs") | Computation 11.55 | The two *new* exact densities $\delta_{11}(5)=0.5216022$ and $\delta_9(7)=0.6239187$ rest on **one** program (`annealed.c`). T4's second program `xcheck_annealed.c` was run only on $p=2$ ($G\le18$), $p=3$ ($G\le11$), $p=5$ ($G\le7$), $p=7$ ($G\le6$) (`T4-computations/logs/xcheck_annealed.log`). The note's sentence "Two programs sharing no code … agree … in every one of 10 overlapping cases" is true but reads as if it covered the headline values. My independent Monte Carlo (below) agrees with both values within its precision ($\approx5\cdot10^{-4}$), which cannot distinguish them from the round-1 values $\delta_{10}(5)$, $\delta_8(7)$ (they differ by $\approx2\cdot10^{-5}$). An exact independent census at these sizes was out of budget for my decision procedure (estimated 2.4 h and 23 h CPU). |
| F2 | minor | Theorem 11.38 table | $\theta_3=0.2294000283\ldots$ (two independent summations), so the printed upper bound "$\theta_3\le0.22940$" is false by $2.8\cdot10^{-8}$; it should read $\le0.22941$ (or $0.2294001$). All other entries of the row are valid upper bounds (the track report's $\theta_5\le0.11013$ was likewise below the true $0.1101338$; the note's $0.11014$ is correct). |
| F3 | minor | Corollary 11.39(b), §0 item 23, numbered-results list | "$\dim_HE_{N_0}\ge0.99966$ at $p=13$": the bound actually proved is $1-\theta^{\rm set}_{13}=0.99965675$, which is **below** $0.99966$. Rounding a lower bound up; should be "$\ge0.99965$" (the §11.4 table's $0.999656$ is correct). |
| F4 | minor (presentation/data) | Computation 11.43 | The archived `T3a-q3-fourier/data/l2_summary.txt` reports "TheoremD checks=12 viol=1" for $(p,N_0)=(3,1)$, while the note says Theorem 11.36(iv) "holds on all 12 data sets". The flagged ratio is the first, *partial* group $\{1!,2!\}$ at level 0 (ratio $1.125$) compared with the full-block bound $1+\Gamma_3(1)=1.03125$; with the group's own $\Gamma_{G_0}(1)=1/8$ the inequality holds with equality. So no mathematical violation, but the note should say the checker's flag is an artefact (or the checker should use $\Gamma_{G_a}$). |
| F5 | minor (statistics) | Computation 11.57 fits | The weighted log–log fits use, within each Monte Carlo run, estimates of $\delta_G$ at several $G$ that come from the **same nested samples** (a survivor at $G$ is a survivor at every smaller $G$), treated as independent. The quoted $\chi^2/\mathrm{dof}$ ($4593/9$, $14.1/3$) and the error $\pm0.001$ on the exponent are therefore not valid goodness-of-fit/uncertainty statements. The qualitative reading (local exponent rising towards 1) survives; the numbers should be described as descriptive. I reproduced the fits from T4's table: exponents $0.813,0.886,0.930,0.939$, $\chi^2=4560,308,19.1,14.0$ (T4: $4593,307,19.2,14.1$; the small $\chi^2$ difference comes from the rounded values in the TSV). |
| F6 | minor (wording) | Conjecture 11.44 evidence | "Validated against exact values ($p=3$, $k=17$: $1.2989$ vs $1.3105$)": the SMC excess $C_k-1=0.2989$ is $3.7\%$ below the exact $0.3105$ (exact value re-derived here only to $k=16$, $1.3095763$, matching T3a). At this precision the SMC cannot support the quoted estimate "$C_\infty(3,1)\approx1.31$" beyond the exact data themselves; "validated" should be "agrees to about 1%". |

No fatal or serious error was found. Every other number I re-ran agrees (Section 2).

## 2. What was re-run, item by item

### 2.1 Hausdorff-dimension constants (Corollary 11.19, Computation 11.59) — [re-run, agrees, all 19 cases]
Program `code/dimref.c` (cyclic bitset subset-sum count over $\mathbb Z/p^{G}$, from the definition of $D_p(w,K)$);
validated against a brute-force enumeration `code/dimbrute.py` on 7 small cases (identical to 12 digits).
Results (`out/dim_table.txt`, 2 threads; $(2,9,22)$ took 66 s):

| $(p,w,K)$ | mine | note |
|---|---|---|
| (2,1,2) (2,3,16) (2,5,16) (2,7,22) (2,9,22) | 0.646240625 0.754308851 0.805446118 0.833392955 **0.853045340** | 0.6462 0.7543 0.8054 0.8333 **0.8530** (T1b log: 0.8333929553, 0.8530453403) |
| (3,1,8) (3,2,10) (3,4,12) (3,5,13) | 0.806873279 0.859186460 0.911156522 **0.924735670** | 0.8068 0.8591 0.9111 **0.9247** |
| (5,1,7) (5,2,8) (5,3,8) | 0.923694746 0.954843005 **0.969113107** | 0.9236 0.9548 **0.9691** |
| (7,1,5) (7,2,6) | 0.985556826 **0.992137617** | 0.9855 **0.9921** |
| (11,1,5) (13,1,5) | 0.998268316 0.999656750 | 0.9982, 0.9996 |
| (17,1,4) (19,1,4) (23,1,4) | 0.999963399 0.999990619 0.999996427 | 0.99996, 0.99999, 0.99999 |

Computation 11.59: my $D_p(1,K)$ and my independent $1-\theta^{\rm set}_p$ (2.2) agree to all printed digits with
both values quoted in the note ($p=13$: $0.999656750$ at $K=5$ vs $0.9996567512$ in the limit).
Note: $D_{23}(1,4)=1-23^{-4}$ exactly (to 12 digits), consistent with $L_{23}\ge4$.

### 2.2 Gate-block law, $\Gamma_p$, $J_0$, ${\rm dist}_p$, $\theta_p$, $\theta^{\rm set}_p$ (Lemma 11.37, Theorem 11.38) — [re-run, agrees; F2]
`code/gblock.c` enumerates all $3^p$ sign vectors ($p\le19$) with exact 128-bit weights; `code/theta_ref.py`
(exact rationals, closed-form tail, mpmath 40 digits) and `code/theta_direct.py` (direct truncated sum).
- $\mathbb P(W=0)=3/2^{p+1}$ and exactly $3\cdot2^{p-2}$ distinct integer subset sums: true for all 8 primes.
- $\Gamma_p(1)$: $0, 1/32, 9/256, 117/8192, 753/2^{19}, 739/2^{25}, 2617/2^{32}, 13507/2^{37}$ — identical.
- $J_0$: 2,2,3,4,5,6,7,7; $\max\{j:{\rm dist}_p(j)=p^j\}$: 1,1,1,2,2,2,3,3 — identical. Affinity of $\Gamma_p(j)$ for $j\ge J_0$ checked exactly up to $j=23$.
- $\theta_p$: $0.396240625$ ($=\log_23/4$ to 40 digits), **$0.2294000283$**, $0.1101338076$, $0.0266079305$, $6.23569904\cdot10^{-3}$, $9.07675515\cdot10^{-4}$, $8.41065355\cdot10^{-5}$, $3.40665064\cdot10^{-5}$. All note entries are valid upper bounds except $\theta_3\le0.22940$ (F2).
- $1-\theta^{\rm set}_p$: $0.6462406252, 0.8068732786, 0.9236947455, 0.9855568255, 0.9982683160, 0.9996567512, 0.9999654327, 0.9999932255$ — all note entries valid lower bounds; but see F3 for "$0.99966$".

### 2.3 Exact $L^2$ masses $C_k$ (Computation 11.43) — [re-run, agrees at every level reached]
`code/l2ref.c`: exact subset counts mod $p^{k_{\max}}$ (uint32/uint64), lower levels by folding, $C_k=p^kS/4^M$
converted exactly (`code/l2post.py`); a double-precision variant for $p=11,13$ (counts exceed $2^{64}$ there);
brute-force cross-check `code/l2brute.py` on 5 tiny cases.
- $p=2$, $N_0=1$, $k\le27$: every $C_k$ identical to T3a's per-level list (e.g. $C_{27}=4.4366709590$). $k=28$ not reached (2 GB).
- $p=3$, $k\le16$: identical ($C_{16}=1.3095763303$). $k=17$ not reached.
- $p=5$, $k\le11$: identical ($C_{11}=1.0790025263$). $p=7$, $k\le9$: identical ($1.0193292342$).
- $p=11$, $k=7$: $C_7-1=2.0685590\cdot10^{-3}$; $p=13$, $k=7$: $2.8658616\cdot10^{-5}$; $p=13$, $N_0=13$, $k=6$: $2.2537692\cdot10^{-5}$ (double precision; all agree with the note).
- "Product bound" column recomputed (`code/prodbound.py`; first partial group exact, full blocks $1+\Gamma_p(J)$): $410.0625, 33.9466, 5.12419, 1.251455, 1.010732, 1.000161, 1.000132$ — identical.
- F4 (the archived "viol=1") found while reading T3a's summary file.

### 2.4 Corollary 11.30 constants (Theorem 11.29) — [re-run, agrees]
`code/cor1130.py`, own piecewise evaluation over all right endpoints of the intervals on which $(n_0,K)$ is constant, $2^{10}\le G\le2^{400}$ (integer 4th roots, mpmath 60 digits):
main terms $20.884603$, $1316.3726$, $197159.18$; sup of side terms $\times G^{0.227}$: $1.58437$, $1.70053$, $1.87547$ (note: 1.585, 1.701, 1.876); totals $22.469$, $1318.07$, $197161.06$ (note: $22.47$, $1318.1$, $1.97162\cdot10^5$; all $\le29,1325,1.98\cdot10^5$).
Sup of $\min(\mu(C),\mathrm{RHS})G^{0.227}$: $17.526$, $1121.34$, $167988$ (note $17.53$, $1121$, $1.680\cdot10^5$). $1-H_2(0.227)=0.227255>0.227$. $0.61\cdot2^{-2.27}=0.12647\ge1/8$. Table data $s_L$, $E_C$ re-derived by hand from Prop. 11.26.
With the fixed $c$ of Cor. 11.30 the bound first beats $\mu(C)$ at $G=2^{32},2^{58},2^{95}$ (the note's $2^{18},2^{29},2^{44}$ are for an optimised $c$ — consistent, not checked).

### 2.5 $p=2$ finite certificates (Props 11.25, 11.16, 11.32; Lemma 11.24) — [re-run, agrees]
`code/p2_checks.py`: (a) values $\{1,-5,7,1,-2,-8,4,-2\}$, max valuation 3; (b) $\{4/5,34/5,-26/5\}$ (val. $\le2$) and $\{-16/5,14/5,-46/5\}$ (val. $\le4$); (c) histogram over 64 cases $\{1{:}32,3{:}16,4{:}8,5{:}3,6{:}4,7{:}1\}$ — identical. Lemma 11.24(c) identity: 0 failures in 200 symbolic random tests. $S_{\{1,3\}}=(x+2)^3$. Prop. 11.16: for $X\equiv6,14\pmod{16}$, every unit $U$ and all 16 sign patterns, the four normalised run elements reach every odd residue mod 8; for $J_{u+1}=2$ ($X\equiv2,10$) 8 of 16 sign patterns fail — matching the note's remark.

### 2.6 Census, deep values, $N(A,G)$ (Computations 11.55, 11.56; §4.7) — [re-run, agrees; F1]
`code/gdec.c` (normalised-state recursion with dedup, 128-bit; digit-tree DFS census; Monte Carlo) and
`code/g2deep.py` (big-integer version for natural $a$), both written for this report.
- Exact census $p=2$ to $G=28$ (1573 s, 19 MB): survivors mod $2^{28}$ = **31 246 552** — identical to the note; $\delta_{25}(2)=0.1266146898$ ($1-\delta_{25}=0.873385$ as in §4.7). Small censuses reproduce §4.7 ($p=3$, $G\le12$; $p=5$, $G\le7$; $p=7$, $G\le5$, incl. $\delta_2(7)=31/49$).
- Annealed moments by brute force (`code/annref.c`) for $(p,G)=(2,12),(3,6),(5,5),(7,4)$: survivors, $\sum N$, $\sum N^2$, $\max N$ identical to T4's files; Prop. 11.53's $N_G(-2)=2^{M_G-1}$ confirmed in 8 cases (and $\max N=N(-2)$ in all of them).
- Monte Carlo of the two new densities (F1): $p=5$, cap 11, $2\cdot10^6$ samples: $\hat\delta_{11}(5)=0.52108\pm0.00035$ (note $0.5216022$, $z=-1.5$); the ratio $\hat\delta_{11}/\hat\delta_1=0.869329$ vs exact $0.869337$. $p=7$, cap 9, $2.4\cdot10^5$: $\hat\delta_9(7)=0.62256\pm0.00099$ ($z=-1.4$); ratio to $\hat\delta_1$: $0.87263$ vs $0.87349$ ($z\approx-1.1$). No sample had $g_7=2$. Consistent, but cannot resolve the $\approx2\cdot10^{-5}$ improvement over round 1.
- $g_2(a)$ for all $a\le4096$ at cap 1024 (22 s): **0 mismatches** with Kitamura's table ($a\le256$, after $f\to g$); $N(4096,G)=992,622,411,263,167,85,40,20$ at $G=8,\dots,1024$, and from cap 4094 on the 20 survivors: $13,10,5$ at $G=2048,3072,4094$ — all identical; survivors at 4094: $\{34,594,1102,2210,3456\}$.
- **$g_2(2210)=6261$, $f(2210,2)=8467$** (cap 8000, 354 s) and $g_2(3456)=4823$ (157 s): a third independent program agrees with the new exact value.
- Conjecture 11.34(b) counts recomputed from my table: $27,15,6,3,3,2,1$ for $\lambda=1,\dots,64$ — identical.

### 2.7 Gate constants and other small items — [re-run, agrees]
- Computation 11.58 / Remark 11.9 (`code/gateconst.py`, mpmath 30 digits): $c_3=1/8$, $c_5=0.13237712$, $c_7=0.082366223$, $c_{11}=0.026681268$, $c_{13}=3.2999177\cdot10^{-3}$, $c_{53}=4.0255207\cdot10^{-14}$; $c_p/(2/\pi)^p=0.01455$ at $p=41$ and $175.2$ at $p=43$ — identical. $I_5/(2/\pi)^5=1.166975$, $I_7/(2/\pi)^7=1.170443$ (midpoint rule, $2\cdot10^7$ and $4\cdot10^7$ nodes agree) vs note $1.1670,1.1704$. $I_{11},I_{13}$ not re-run.
- Lemma 11.54: geometric mean $\times2^p=1$ to 15 digits for all odd $p\le53$.
- Theorem 11.48(c): $\min_\rho c_1(13,\rho)=2.20239\cdot10^{-5}$ (at $\rho=12$), so "$c_1\ge2.2\cdot10^{-5}$" holds; $1/c_1=45405$, between $13^4$ and $13^5$, so "nothing with $M\ge5$" is right.
- Remark 11.49 (`code/cov_check.py`, direct subset-sum DP over $\mathbb Z/13^{3+c}$ for every unit $K'$): $\mathrm{Cov}(13,3,H)$ holds for $H=19,\dots,26$ ($c=1$), **fails** for $H=27,\dots,31$ ($c=2$; worst-unit misses $314171, 285610, 199927, 85683, 57122$ of $13^5$), holds at $H=32$ — identical.
- Theorem 11.50 arithmetic: $v_{19}((19^9-1)!)=17\,927\,094\,312$, $v_{19}((19^8-1)!)=943\,531\,272$, $v_{19}(44!)=v_{19}(48!)=2$, 342 units mod $19^2$ — identical.
- Proposition 11.13(b): Newton roots of $H(y)=y+(y-1)\pi_c(y)$ for 16 pairs $(p,c)$, $p\le7$: $v(y_c)=v(c!)$ and $H'(y_c)$ a unit in all cases.
- Theorem 11.45 (a)–(d): 92 064 random instances ($p\le13$, $D\le3$, $t\le D+4$), 0 failures.
- Theorem 11.15 Step 0(b): for $p\le13$ and every $k\le300$ the residues $f(u)\bmod k$, $p\mid u$, cover $\mathbb Z/k$ (digit sumset over 400 positions). (Using only $u<4000$ they do not, e.g. $(p,k)=(5,25)$: the lemma needs large $B$, as its proof says.)

- $g_2(1102)=11536$ ($f=12633$, cap 12000, 2258 s) — Kitamura's record reproduced by a third program. $g_2(34)$ at cap 19000 was started and stopped (would exceed the 45-min limit); it was confirmed in round 1 and by the lead.

### 2.8 Monte Carlo $\delta_G(2)$ (Computation 11.57) and the $14\bmod16$ share (Prop. 11.32) — [re-run at reduced size, agrees]
- `gdec mc 2 126`, $4\cdot10^6$ samples: $\delta_8=0.242421(214)$, $\delta_{16}=0.151566(179)$, $\delta_{24}=0.128975(168)$, $\delta_{29}=0.113202(158)$, $\delta_{32}=0.101558(151)$, $\delta_{64}=0.064164(123)$, $\delta_{126}=0.038286(96)$; all within $1.4\sigma$ of the exact census values ($G\le32$) and of the note ($G=64$: $0.06416$).
- Python big-integer sampler (`code/mc256.py`, different code path): cap 256, $10^6$ samples: $\delta_{64}=0.064207$, $\delta_{128}=0.037717(190)$, $\delta_{256}=0.020533(142)$ (note: $0.06416$, $0.03770$, $0.02052$); cap 512, $3\cdot10^5$: $\delta_{384}=0.01437(22)$, $\delta_{512}=0.01086(19)$ (note: $0.01068(7)$, $z=0.9$).
- Share of $x\equiv14\ (16)$ among survivors: $41.2\%$ ($G=16$), $57.7\%$ ($G=64$), $59.7\%$ ($G=126$); note (60 000 samples): $41.5\%$, $58.2\%$ ($G=64$) — consistent within the note's sampling error ($\approx0.6\%$).
- Fits re-done from T4's table: see F5.

## 3. Not re-run (stated explicitly)
- §11.1 (T1a): the `winvar` window statistics behind Conjecture 11.10 ($R|P^L|$, $\kappa$, Weyl sums) and the atom Monte Carlo. Not re-implemented (time). These support a conjecture only.
- Theorem 11.50 coverage runs (≈25 core-hours; fibres of $19^8$ bits) and Computation 11.51 ($(19,8,47)$: 2 739 774 misses; $(19,8,49)$ covered). Only the arithmetic and the logic of the position count were checked. The certificates therefore rest on A′/C′ as described in the note (programs derived from the round-2 programs A and C, not fully independent re-implementations — the note says so).
- Deepest $L^2$ levels: $p=2$, $k=28$; $p=3$, $k=17$; $p=5$, $k=12$; $p=7$, $k=10$ (memory). SMC of Conjecture 11.44.
- Exact census at $(5,11)$ and $(7,9)$ (F1) and the annealed moments $\mathbb EZ_G$, $\mathbb EZ_G^2$ at the large $G$ of the table (only small $G$ re-run, exact match).
- T2's predictor (Heuristic 11.33) and its tests; the 300-sample slope statistics of family B; T1b's `hensel_check`.
- $\delta_G(2)$ Monte Carlo above cap 512 (my Python runs at caps 256/512 are in 2.8).
