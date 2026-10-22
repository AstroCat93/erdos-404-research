# Track R3C (round 3, 2026-10-13): the certified covering frontier at p = 29 (and p = 31)

*Lead's note after the adversarial check (`data/round3/checks/R3C.md`): the check confirms R1–R5, R8 and R9. It qualifies R6: program D shares no verbatim code with A beyond boilerplate, but with identifiers renamed it follows A's skeleton, doubling loop and shift-OR kernel, and B's counting-sort block (the same level of overlap as A and C, accepted in round 2). For R7 it notes that the registration's rule "minimal H_t = first HOLD-band H" misses at (29,2) (registered 14, observed 13). note.md §11.5 states both.*

## Headline

**$f(1,29)\ge v_{29}((29^8-1)!)=17\,865\,943\,312$.** [computer-assisted]

The previous best bound was $f(1,29)\ge616\,067\,009$ (round 1, note.md §4.4, from Theorem 3.9(c) and a two-block window). The new bound is about $29$ times larger.

It follows from Proposition 10.10 (chain criterion) with $D=8$ and these certificates:
- uniform $\mathrm{Cov}(29,t,H_t)$ for $t\le6$, with $H_t=7,13,19,24,29,40$, each over all unit classes, checked by programs A, C and D;
- the $28$ depth-7 positions $N^*=29^7K''$, $1\le K''\le28$, each with a block of length $H=45$, checked by programs A and D.

Programs A and D were written by different track instances (R3 in round 2, R3C in round 3), and they share no code beyond four generic boilerplate lines (§4.2). Both chain checkers report CHAIN OK on these logs: the new checker `chain_r3.py`, and `chain_c_r3.py`, which is the round-2 computational referee's `chain_c.py` with its exclusion logic unchanged (two parsing changes, §1.3).

Other results:
- **Minimal uniform $H_t$ at $p=29$ and $p=31$, $t\le6$** [computer-assisted, programs A and C]: $7,13,19,24,29,40$ and $7,14,19,25,30,41$.
- **Lemma R3C.1** [proved]: for odd $p$, $2\le t\le L_p$ and $p<H\le2p$, $\mathrm{Cov}(p,t,H)$ holds if and only if $H\ge p+1+\rho_0(p)$.
- **Program D** (`code/round3/R3C/covfast.c`) is a new covering program. It agrees with an independent brute force in 7 680 comparisons, with 0 mismatches. It also reproduces, at full size, the exact miss counts of eight configurations that round 2 established with other programs. In one of them, $(11,7,40,K''=37)$, it finds the same two missed residues that round 2 listed. Section 4 has the details.
- **Registered predictions of the bottleneck law (Conjecture 10.24).** The predictions were registered at 06:12:36 UTC, before any of the runs whose outcome they predict. Of the 64 band predictions that were genuine tests, 63 were confirmed and 1 was falsified.
  - The falsified one is uniform $\mathrm{Cov}(29,5,36)$: the law predicted FAIL ($\nu=1.112$), but it holds. Lemma R3C.1 explains why, after the fact.
  - One of the confirmations was run at completion: the registered FAIL prediction for $H=44$ at depth 7. The block of length 44 ending at $29^7\cdot3$ misses exactly 2 residues mod $29^8$, the same two in programs A, C and D.
  - Section 5 lists what was known in advance and what was not run.
- **$p=31$ is partial.** The uniform depths $t\le6$ are certified by A and C. They give $f(1,31)\ge v_{31}((31^7-1)!)=917\,087\,130$, which is **5 less than** the round-1 bound $917\,087\,135$. So there is no new bound at $p=31$. The 30 depth-7 positions were not run.
- **Timing only:** one depth-7 position at $p=19$; 48 classes of $\mathrm{Cov}(5,5,39)$ with A and C, and 4 of them with D.

*Provenance.* An external spending limit cut off the original R3C instance at about 08:12–08:20 UTC. By then it had registered its predictions, run the scans, run program D's uniform certificates and validations, and certified the depth-7 positions $K''=1,\dots,5$. The lead then resumed its position queue at 15:08 UTC, as two parallel queues ($K''=6..17$ and $18..28$), which finished at 17:41 UTC. The report was then written by a completing instance, which:
- re-read every log and source file;
- rebuilt the binaries and checked their provenance (§4.2);
- wrote the chain specifications and ran both chain checkers, including negative controls and a re-validation on round-2 logs (§1.3);
- added large-scale exact checks of program D (§4.4);
- ran the registered $H=44$ prediction, which the original instance had left for "if budget allows" (§5.4).

All of this was done on 2026-10-13. Code: `code/round3/R3C/`. Logs: `data/round3/R3C/`.

*Status labels* follow the round-3 rules:
- [proved]: written out in full here and checked by this track only; no referee or human has checked it.
- [computer-assisted]: rests on exact computations, each by two programs that share no code.
- [negative]: a certified failure of coverage, with the same rule.
- [heuristic]: evidence or fitted laws, not proofs.

---

## 0. Results at a glance

| # | statement | status |
|---|---|---|
| R1 | $f(1,29)\ge v_{29}((29^8-1)!)=17\,865\,943\,312$ | computer-assisted (A+D for every certificate; C also for $t\le6$) |
| R2 | for $1\le a<29^8-45$: either $f(a,29)<v_{29}((a+45)!)$ or $f(a,29)\ge17\,865\,943\,312$ | computer-assisted (same certificates; Prop. 10.10, general $a$) |
| R3 | minimal uniform $H_t(29)=7,13,19,24,29,40$ and $H_t(31)=7,14,19,25,30,41$ ($t=1,\dots,6$) | computer-assisted (A decides; C confirms each failing class with the same exact miss count, and every hold over all classes) |
| R4 | $\mathrm{Cov}(29,6,39)$ and $\mathrm{Cov}(31,6,40)$ are false: class $K'=2$ misses exactly 2 residues, the same residues in A and D. The depth-7 block of length 44 ending at $29^7\cdot3$ misses exactly 2 residues mod $29^8$ (§5.4) | negative, computer-assisted (A, C, D) |
| R5 | Lemma R3C.1 (exact $\mathrm{Cov}$ criterion in the window $p<H\le2p$ for $2\le t\le L_p$) | proved |
| R6 | program D is correct on every test and independent of A | computer-assisted validation (§4) |
| R7 | registered predictions of Conj. 10.24: 63 confirmed, 1 falsified, 11 known in advance, 20 refuted by proofs (not tests), 4 MIXED, 21 not run (§5) | heuristic (the law itself) |
| R8 | $p=31$: uniform $t\le6$ only; $f(1,31)\ge917\,087\,130$, which is not an improvement | computer-assisted (A+C); partial |
| R9 | $p=19$ depth 7 at $K''=20$; $\mathrm{Cov}(5,5,39)$ on 48 classes (A, C) and 4 classes (D): timings only | timing only |

---

## 1. The $p=29$ chain

### 1.1 Statement

**Result R1 [computer-assisted].** $f(1,29)\ge v_{29}((29^8-1)!)=17\,865\,943\,312$.

*Proof.* This is Proposition 10.10 with $p=29$ and $D=8$; its hypotheses are verified as follows.
- **Depths $t=1,\dots,6$ (uniform).** $\mathrm{Cov}(29,t,H_t)$ holds for $H_t=7,13,19,24,29,40$, over all unit classes $K'\bmod29^{c}$ (Table 1.2). Also $H_t+1<29^t$.
- **Depth $t=7$ (positions).** We need every $K''<29^{8-7}=29$ with $29\nmid K''$, i.e. $K''=1,\dots,28$. For each, the block of length $H=45$ ending at $N^*=29^7K''$ covers $\mathbb Z/29^{t+c}=\mathbb Z/29^8$, where $c=v_{29}(44!)=1$. Also $29^7K''-45>1$.

So no first failure of $a=1$ lies below $29^8$, and Lemma 1.3(i) gives the bound. By Legendre's formula, $v_{29}((29^8-1)!)=(29^8-1-8\cdot28)/28=17\,865\,943\,312$. ∎

The general-$a$ form of Proposition 10.10 (the largest block length used is $45$) gives **R2**: for $1\le a<29^8-45$, either $f(a,29)<v_{29}((a+45)!)$ or $f(a,29)\ge17\,865\,943\,312$. No landscape at $p=29$ was computed, so R2 is not applied to any particular $a$.

*Comparison.*
- With the uniform depths alone ($D=7$), the chain gives $v_{29}((29^7-1)!)=616\,067\,004$. That is below the round-1 bound $616\,067\,009$. The depth-7 positions are what produce the improvement.
- Depth 8 at $p=29$ ($D=9$) is out of reach for the fibre method on this machine. The modulus is $29^{8+c}$, with $c=v_{29}((H-1)!)\ge1$ for any plausible $H$ (the law predicts $H_8\approx50$). A fibre level $k\le c$ gives bitsets of at least $29^{8}$ bits (62.5 GB). A level $k>c$ puts the whole block into the enumerated low part ($2^H$ sums).

### 1.2 The certificates

**Table 1.2.** In the "programs" column, A = `fibcov` (round 2, track R3), C = `covchk` (round-2 computational referee) and D = `covfast` (round 3, this track). Class representatives were $K'$ for A, $K'+2\cdot29^c$ for C and $K'+3\cdot29^c$ for D. At depth 7, all programs used the actual positions $K''$.

| depth $t$ | $H$ | $c$ | modulus | classes / positions | programs | logs (in `data/round3/R3C/`) |
|---|---|---|---|---|---|---|
| 1 | 7 | 0 | $29$ | 1 | A, C, D | `scan_p29_t1.log`, `U29_D_t1_H7.log` |
| 2 | 13 | 0 | $29^2$ | 1 | A, C, D | `scan_p29_t2.log`, `scanall_p29_t2.log`, `U29_D_t2_H13.log` |
| 3 | 19 | 0 | $29^3$ | 1 | A, C, D | `scan_p29_t3.log`, `U29_D_t3_H19.log` |
| 4 | 24 | 0 | $29^4$ | 1 | A, C, D | `scan_p29_t4.log`, `U29_D_t4_H24.log` |
| 5 | 29 | 0 | $29^5$ | 1 | A, C, D | `scan_p29_t5.log`, `scanall_p29_t5.log`, `U29_D_t5_H29.log` |
| 6 | 40 | 1 | $29^7$ | 28 | A, C, D | `scan_p29_t6.log` (A: $K'=1..28$; C: $K=59..86$), `U29_D_t6_H40.log` (D: $K=88..115$) |
| 7 | 45 | 1 | $29^8\approx5.0\cdot10^{11}$ | 28 positions | A, D | `p29_t7/P29_t7_H45_{A,D}_K{1..28}.log` |

All 56 depth-7 logs report `missing=0 COVERED`, and none contains `NOT_COVERED`. No $H=46$ fallback was needed, and none was run. Program A used a fibre bitset of $29^7=17\,249\,876\,309$ bits (2 056 MB, two buffers). Program D used the same size, plus a complement buffer of $2^{24}$ entries. Wall times per position were 460–854 s for A and 242–507 s for D.

*Which binaries ran the scans.* The scan logs record the command `env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/scan_r3.py ...`. That script runs `$R3C_BIN/fibcov` (program A) and `$R3C_BIN/covchk` (program C), and both output formats in the logs match those sources (`A p=… missing=…`, and `C p=… Kmodpc=… miss=…` / `END C …`). The scans therefore certify with **A and C**; program D was run on the uniform depths separately (`U29_D_*`). The binaries in `/tmp/r3_R3C/bin/` are byte-identical to fresh `clang -O3 -march=native` builds of the committed sources `code/round2/R3/src/fibcov.c`, `code/round2/review/computation/covchk.c` and `code/round3/R3C/covfast.c` (§4.2). The two round-2 sources are unchanged since round 2; `fibcov.c` still has the hash recorded in `data/round2/logs_original/R3/binary_hashes.txt`.

### 1.3 Chain checks

Both checkers read only the logs. Spec files are in `code/round3/R3C/specs/`. Each command below is run from the repository root with `R3C_LOGS=data/round3/R3C:data/round3/R3C/p29_t7`.

**`chain_r3.py`** (new in round 3; it requires every program listed by `require` for every certificate). Output: `data/round3/R3C/CHAIN_p29_p31_chain_r3.txt`.

| spec | required programs | result |
|---|---|---|
| `p29_AD.txt` | A, D for everything | **CHAIN OK**, $f(1,29)\ge17\,865\,943\,312$ |
| `p29_AC_AD.txt` | A, C for $t\le6$; A, D for depth 7 | **CHAIN OK**, $17\,865\,943\,312$ |
| `p29_ACD_D7.txt` | A, C, D, uniform only, $D=7$ | CHAIN OK, $616\,067\,004$ |
| `p31_AC_D7.txt` | A, C, $p=31$, $D=7$ | CHAIN OK, $917\,087\,130$ |
| `neg_p29_H44.txt` (control) | positions at $H=44$ (no logs in these directories) | PARTIAL, $616\,067\,004$ |
| `neg_p29_K27.txt` (control) | positions $K''\le27$ only | PARTIAL (first open position $29^7\cdot28$) |
| `neg_p29_C_pos.txt` (control) | C required for depth 7 | PARTIAL |
| `neg_p29_t6_H39.txt` (control) | uniform $(29,6,39)$, which is false | PARTIAL, depth 6 open |
| `neg_p31_D8.txt` (control) | $p=31$, $D=8$, no positions | PARTIAL |

**`chain_c_r3.py`** (the round-2 referee's `chain_c.py`; one program at a time). Output: `data/round3/R3C/CHAIN_p29_p31_chain_c_r3.txt`.
- **$p=29$, $D=8$:** `[A] CHAIN OK f(1,p) >= 17865943312` and `[D] CHAIN OK f(1,p) >= 17865943312`. Program C gives INCOMPLETE (it has no depth-7 logs).
- $p=29$, $D=7$: A, C and D each give CHAIN OK, 616 067 004.
- $p=31$, $D=7$: A and C each give CHAIN OK, 917 087 130. D gives INCOMPLETE (not run at $p=31$).
- Controls: $H=44$, uniform $(29,6,39)$ and $p=31$, $D=8$ give INCOMPLETE for A and for D.

*The adaptation of `chain_c.py`.* `chain_c_r3.py` reads the plan from the command line and the log directories from `$R3C_LOGS`, and accepts A and D logs as well as C logs. It also changes two parsing details. First, it strips leading blanks, because the scan logs indent the per-class lines. Second, it computes $K\bmod p^c$ itself instead of reading the `Kmodpc=` field. The exclusion logic (uniform certificate over all unit classes with $H+1<p^t$, or position certificate with $N-H>1$) is unchanged. Its docstring says "no change to its logic"; the two parsing changes are the only differences.

*Re-validation on round-2 logs* (`data/round3/R3C/CHAIN_checker_validation_round2.txt`):
- `chain_r3.py` on the lead's 2026-10-12 re-run logs (A and B) reproduces CHAIN OK for $p=7,11,13,19,23$ with the bounds of note.md §10.2.
- Its two round-2 controls (`r2_p23_neg`: uniform $(23,6,36)$; `r2_p23_partial`: positions $K''\le10$) give PARTIAL.
- `chain_c_r3.py` on program C's round-2 logs reproduces `data/round2/review/computation/chain_c.out` line for line: CHAIN OK for all six primes. Its controls behave as expected: with no logs it gives INCOMPLETE, and without the exception $K''=37\mapsto H=41$ the $p=11$ chain gives INCOMPLETE.

---

## 2. Minimal uniform $H_t$ at $p=29$ and $p=31$ [computer-assisted]

**Table 2.** Minimal $H$ with $\mathrm{Cov}(p,t,H)$. In brackets is the largest failing $H$ below the minimum, with the exact number of residues missed by its first failing class ($K'=1$ unless stated). A and C agree on every count.

| $p$ | $t=1$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 29 | 7 [6: Lemma 10.11] | 13 [12: 67] | 19 [18: 2] | 24 [23: 30] | 29 [28: 730] | 40 [39: $K'=2$, 2] |
| 31 | 7 [6: Lemma 10.11] | 14 [13: 4] | 19 [18: 42] | 25 [24: 2] | 30 [29: 10] | 41 [40: $K'=2$, 2] |

*Method* (`scan_r3.py`). For each $H$ in increasing order:
- An $H$ is refuted by counting ($2^H<p^{t+c}$) or by Lemma 10.11 ($(H-1)\bmod p<\rho_0(p)=6$); both are proved.
- Otherwise program A runs over all classes and stops at the first failing one. Program C then recomputes that class and must report the same exact miss count.
- An $H$ is declared HOLDS only if A covers every class and C, using its own representatives, also covers every class.

Every failing $H$ in the scans is refuted in one of these three ways. The scan logs are `scan_p{29,31}_t{1..6}.log`.

*Remarks.*
- $H_1=\rho_0+1=7$ is Lemma 10.11, so it was known.
- $\mathrm{Cov}(29,5,29)$ and $\mathrm{Cov}(31,5,31)$ were known to hold, because $L_{29}=L_{31}=5$ (note.md §3.5).
- **Non-monotonicity again.** At $(29,5,\cdot)$: $H=29$ holds, $H=30,\dots,35$ fail (Lemma 10.11), and $H=36,\dots,39$ hold (`scanall_p29_t5.log`, A and C over all 28 classes). At $(31,5,\cdot)$: $30,31$ hold, $32,\dots,37$ fail, and $38,39$ hold. Lemma R3C.1 explains the second run of holds.
- Further holds above the minimum (A and C, all classes): $(29,t,H)$ for $t=2$, $H=14,15,16$; $t=3$, $H=20,21$; $t=4$, $H=25,26$. Similarly $(31,t,H)$ for $t=2$, $H=15,16$; $t=3$, $H=20,21$; $t=4$, $H=26,27$.

**R4. Two-residue negative certificates [negative, computer-assisted].** Programs A and D list the missed residues explicitly (`N29_t6_H39_K2_dump_{A,D}.log`, `N31_t6_H40_K2_dump_{A,D}.log`); program C finds the same count of 2 in the scans.
- $\mathrm{Cov}(29,6,39)$ fails at $K'=2$. Exactly the residues $9\,681\,558\,076$ and $7\,454\,824\,172$ mod $29^7$ are missed.
- $\mathrm{Cov}(31,6,40)$ fails at $K'=2$. Exactly the residues $25\,349\,343\,487$ and $3\,557\,184\,957$ mod $31^7$ are missed.

In both cases $K'=1$ is covered, and the other classes were not run.

---

## 3. Lemma R3C.1 [proved]

Recall $E_p=\{(-1)^u/u!:0\le u<p\}$ and $L_p=\max\{L:\Sigma(E_p)\bmod p^L=\mathbb Z/p^L\}$ (Theorem 3.9). Recall also $\rho_0(p)$ from Lemma 10.11: the least $\rho$ such that the subset sums of $\{(-1)^u/u!:u\le\rho\}$ cover $\mathbb Z/p$.

**Lemma R3C.1.** Let $p$ be odd, $2\le t\le L_p$ and $p<H\le2p$. Then $\mathrm{Cov}(p,t,H)$ holds if and only if $H\ge p+1+\rho_0(p)$. In that case the block covers $\mathbb Z/p^{t+1}$ for every $X\equiv0\pmod{p^t}$ in place of $p^tK'$; it does not depend on the class at all.

*Proof.* Write $\rho=(H-1)\bmod p=H-1-p\in[0,p-1]$. Since $p\le H-1<2p\le p^2$, we have $c=v_p((H-1)!)=1$ and $M=t+1$. Put $X=p^tK'$ and $y_i=\prod_{s=1}^{i}(X-m_s)$ with $m_s=H-s$, for $0\le i<H$. As $s$ runs over $1,\dots,H-1$, $m_s$ runs over $p+\rho,\dots,1$, and $m_s=p$ exactly when $s=\rho+1$.

- *Valuations.* For $m\ne p$ with $1\le m\le p+\rho<2p$, the factor $X-m$ is a unit. The factor $X-p=p(p^{t-1}K'-1)$ has valuation exactly $1$, because $t\ge2$. Hence $y_0,\dots,y_\rho$ are units and $v(y_i)=1$ for $\rho+1\le i\le H-1$. There are exactly $p$ elements of the second kind.
- *The units, mod $p$.* $H\equiv\rho+1\pmod p$, so $y_i\equiv\prod_{s\le i}(s-\rho-1)=(-1)^i\rho!/(\rho-i)!\pmod p$. With $w=\rho-i$, this is $(-1)^\rho\rho!\cdot(-1)^w/w!$. So $\Sigma(\{y_0,\dots,y_\rho\})\bmod p$ is a unit multiple of $\Sigma(\{(-1)^w/w!:w\le\rho\})\bmod p$. It is all of $\mathbb Z/p$ iff $\rho\ge\rho_0$ (Lemma 10.11(d); adding elements can only enlarge a set of subset sums).
- *The valuation-1 layer, mod $p^{t+1}$.* For $0\le j\le p-1$,
  $$y_{\rho+1+j}=y_{\rho+1}\prod_{m=p-j}^{p-1}(X-m),\qquad\prod_{m=p-j}^{p-1}(X-m)\equiv(-1)^j\frac{(p-1)!}{(p-1-j)!}\pmod{p^t},$$
  because $X\equiv0\pmod{p^t}$. Write $y_{\rho+1}=p\,U_0$ with $U_0$ a unit, and put $u=p-1-j$, so that $(-1)^j=(-1)^u$ because $p$ is odd. Then
  $$y_{\rho+1+j}/p\equiv U_0(p-1)!\cdot(-1)^u/u!\pmod{p^t}.$$
  So the $p$ numbers $y_i/p$ ($i>\rho$) are, modulo $p^t$, the unit $U=U_0(p-1)!$ times the elements of $E_p$. Since $t\le L_p$, their subset sums cover $\mathbb Z/p^t$.
- *Combination.* Let $x\in\mathbb Z/p^{t+1}$. If $\rho\ge\rho_0$, choose $S\subseteq\{0,\dots,\rho\}$ with $\sum_Sy_i\equiv x\pmod p$, so that $x-\sum_Sy_i=pz$. Then choose $T\subseteq\{\rho+1,\dots,H-1\}$ with $\sum_Ty_i/p\equiv z\pmod{p^t}$. The sum over $S\cup T$ is $\equiv x\pmod{p^{t+1}}$.
- *Converse.* If $\rho<\rho_0$, Lemma 10.11(c) with $k=1$ shows that $\mathrm{Cov}$ fails: the units do not cover $\mathbb Z/p$, and every other element vanishes mod $p$.

Finally, $H\le2p\le p^t$, so $\mathrm{Cov}(p,t,H)$ is defined. ∎

*Remarks.*
- The lemma is the $\mathrm{Cov}$ form of the gate congruence (Theorem 3.9(b)). In the window $p<H\le2p$ the valuation-1 layer is a full gate-type copy of $E_p$, so it covers exactly what $E_p$ covers.
- At $t=L_p+1$ the lemma no longer applies. For $H=2p$ that case is the round-1 two-block window of level $j=L_p$ (note.md §4.4), which needs a computation.
- For $p=29,31$ ($L_p=5$, $\rho_0=6$), the lemma gives $\mathrm{Cov}(29,t,H)$ for $2\le t\le5$, $36\le H\le58$, and $\mathrm{Cov}(31,t,H)$ for $2\le t\le5$, $38\le H\le62$.
- The lemma does not improve any chain: the minimal $H_t$ for $t\le L_p$ are smaller (Table 2).
- What the lemma does do is explain the falsified prediction of §5: the counting law treats the valuation-1 layer as random, while here it is a scaled copy of $E_p$ and covers with certainty.

*Numerical check* [single program, sanity check only] (`lemma_check.py`, `lemma_check.log`). The independent big-integer brute force `bigbrute.py` was run on every class $K'=1,\dots,p-1$ for $p\in\{7,11,13,17,19,23\}$, $2\le t\le L_p$ with $p^{t+1}\le7\cdot10^6$, and $p<H\le2p$:
- all 126 triples with $H\ge p+1+\rho_0$ hold;
- all 46 triples with $H<p+1+\rho_0$ fail.

At $p=29,31$ the lemma's range was hit in the scans at $(29,5,36..39)$ and $(31,5,38..39)$, and in `validate_AC.log` / `validate_D.log` at $(29,2,40)$, $(29,3,40)$, $(29,4,36)$, $(29,4,45)$, $(31,3,45)$, $(31,4,41)$. All of these hold.

*Timing.* The lemma was formulated after the outcome at $(29,5,36)$ had been seen: `scanall_p29_t5.log` ended at 06:16:51, and `lemma_check.log` started at 06:56:58. The lemma is an explanation after the fact, not a prediction.

---

## 4. Program D: independence and correctness

### 4.1 What it does

`covfast.c` (305 lines, `cc -O3 -march=native … -lgmp`) decides whether the subset sums of the block $y_i=(N_1+1)\cdots(N_1+i)$, $N_1=N^*-H$, cover $\mathbb Z/p^M$. It prints the exact number of residues that are missed.
1. **Elements.** Exact GMP products at the actual position. Each $p$-adic valuation is checked against Legendre's formula, and $M=v_p(N^*!)-v_p(N_1!)$ is checked against $t+c$.
2. **Fibres.** Split by the low $k$ digits. $\Sigma(L)$ is enumerated completely by doubling and counting-sorted by residue mod $p^k$.
3. **Three exact phases per fibre:**
   - an explicit list while it is short;
   - a bitset with a constant-offset shift-OR kernel on a 128-bit cyclic pad;
   - once at most `ZMAX` residues are missing, a sorted complement list $Z\leftarrow Z\cap(Z+w)$.

### 4.2 Independence

- **Authorship.** D was written in round 3 by the R3C track instance. Program A was written in round 2 by track R3, program B by the same round-2 track, and program C by the round-2 computational referee. So A and D have different authors, and so do C and D.
- **Code.** A line-by-line comparison, ignoring whitespace and comments and keeping only lines of at least 20 characters, finds the following lines shared with the other sources:
  - with `fibcov.c` (A): 4 lines (`int main(...)`, `const char *mode = argv[5];`, a loop header `for (size_t q = 0; q < nK; q++)`, and the "bad mode" error);
  - with `fibcov2.c` (B): 3 such lines;
  - with `covchk.c` (C): 8 lines. Besides the same boilerplate, these include the two lines of a counting-sort prefix sum (`size_t *start = calloc(PK + 1, …)`, `for (r…) start[r+1] += start[r];`) and the `lift` argument parse.
- **Assessment.** No algorithmic code is shared with A. The few lines shared with C suggest that its author had seen C's source. They are standard idioms outside the covering kernel: C's kernel is a two-pass `or_off` with bit-by-bit heads, and its elements are computed by 128-bit modular products, whereas D uses a padded single-pass kernel, exact GMP products and a complement phase.
- **Common method.** A, C and D all use the same mathematical reduction: fibres by the low $k$ digits (note.md §10.2). It is a short exact identity, and it is tested directly against `bigbrute.py`, which uses no fibre split, at every legal $k$, including $k=0$.
- **Binary provenance.** `clang -O3 -march=native -o covfast code/round3/R3C/covfast.c -lgmp` reproduces `/tmp/r3_R3C/bin/covfast` byte for byte (sha256 `7596867116ee…`). All D logs were produced by that binary. The source file was last modified at 06:56:00, after the binary was built (06:20:29). The rebuild (and the original instance's own rebuild `covfast_check`, at 06:56:01) is identical, so that edit did not change the compiled program. The same check holds for A (`4b551a73…`), B (`f3504700…`) and C (`0ceec1e3…`).

### 4.3 Code review (by the completing instance)

The following points were checked by reading the source:
- **The rotate kernel.** For $0<w<F$, words $j<\lceil w/64\rceil$ read source bits $F-w+64j+b$. When this is $\ge F$, the offset beyond $F$ is $\le63$, and the 128-bit pad stores bit $F+i=$ bit $(i\bmod F)$. Later words read $64j-w+b<F$. Every read stays inside the three pad words. Bits $\ge F$ of the last word are masked out of the popcount.
- **Shifts by zero.** $w=0$ is skipped, which is correct because $X\cup(X+0)=X$.
- **The complement step.** $x$ is missed after adding $w$ iff both $x$ and $x-w$ were missed before, so the step $Z\leftarrow Z\cap(Z+w)$ is exact. The sort order of $Z+w$ is handled by a binary search for the wrap point.
- **Edge cases.**
  - An empty fibre counts all $F$ of its residues as missed.
  - The program aborts on any of: a valuation mismatch, an element vanishing mod $Q$, an element of $U$ not divisible by $p^k$, an $M$ mismatch, or a mismatch in complement extraction.
  - Integer ranges: $Q<2^{62}$, and sums are $<2Q$.
- **Classes.** In `cls` mode, $K=K'+\text{LIFT}\cdot p^c$ for every unit $K'$, and $K=1+\text{LIFT}$ when $c=0$.

No defect was found.

**One performance defect** (not a correctness issue). The list phase is not capped by the fibre size $F$. When $F$ is much smaller than `LISTMAX`$=2^{24}$, every fibre builds a list of up to $2^{24}$ entries. At $(5,5,39)$, with $F=5^8$ and $5^5$ fibres, this makes D about $900$ times slower than A (§6).

### 4.4 Validation record

| check | what | result | log |
|---|---|---|---|
| brute force | `validate_r3.py D 20261013`: 41 cases ($p=2,\dots,31$; including $c=0,1$ cases at $p=29,31$), 8 random $K$ each; every fibre level $k$ with $\lvert L_k\rvert\le22$; five LISTMAX/ZMAX settings that force each phase and each phase switch | **7 680 comparisons, 0 mismatches**; 141 failing (case, $K$) pairs, with exact miss counts compared | `validate_D.log` |
| same suite, A and C | `validate_r3.py A,C` | A: 1 600 comparisons, C: 1 664, **0 mismatches** | `validate_AC.log` |
| missed residues, mid size | $(29,6,39,K'=2)$, $(31,6,40,K'=2)$; $F=29^6$, $31^6$ bits | D lists exactly the same 2 residues as A in both cases; C's count is also 2 | `N29_*`, `N31_*` |
| **large, against round-2 counts** (added at completion) | $(11,7,40,K''=37)$ | **2 missed: $23\,022\,655\,245$ and $18\,038\,488\,330$**, the two residues listed by the round-2 logic referee's `covmiss.c`; A, B and C also counted 2 | `valD/VD_11_7_40_K37.log` |
| | $(11,7,39,K''=1)$ | **1 389 738 missed**, the count of `cov_pos.c`, `rcover.c`, A and B | `valD/VD_11_7_39_K1.log` |
| | $(11,7,41,K''=37)$ | covered (as A, B, C, `covmiss.c`) | `valD/VD_11_7_41_K37.log` |
| | $(17,7,42)$, $K'=5$ and $K'=6$ | $K'=6$: **2 missed**; $K'=5$: covered (both as found by C) | `valD/VD_17_7_42_K56.log` |
| | $(7,6,33,K'=5)$ and $(7,6,34,K'=5)$ | $H=33$: **2 missed** ($241\,978\,387$ and $94\,559\,789$ mod $7^{10}$); $H=34$: covered. These agree with the round-2 logic and novelty referees' checkers, which recorded the count of 2 | `valD/VD_7_6_33_K5.log`, `valD/VD_7_6_34_K5.log` |
| | $(13,8,46,K''=1)$; $k=2$, fibre $13^9$ bits, modulus $13^{11}\approx1.8\cdot10^{12}$ | **26 missed** (A and C also found 26); the 26 residues are listed in the log | `valD/VD_13_8_46_K1.log` |

The large checks run D at fibre sizes up to $13^9\approx1.06\cdot10^{10}$ bits. That is the same order as the $29^7\approx1.7\cdot10^{10}$ bits of the depth-7 certificates. The verbose output of the $K''=1$ certificate shows that all 29 of its fibres finished in the complement phase. The brute-force suite forces that phase, and every switch between phases, through its `ZMAX` settings. All eight configurations agree exactly with the earlier programs.

**Verdict.** Program D is independent of program A. It is correct on every test, including exact agreement with miss counts that other programs established in round 2 at full size. This is enough for D to serve as the second program behind R1.

---

## 5. Registered predictions of the bottleneck law (Conjecture 10.24)

### 5.1 Registration

`data/round3/R3C/PREDICTIONS_registered.txt` carries the internal stamp "registered: 2026-10-13 06:12:36 UTC". Its file time is 06:12:37.
- **Running order.** The first run whose outcome it predicts is `P29_t7_H45_A_K1.log`, which started at 06:14:49. The first scan started at 06:15:20.
- **Earlier runs.** The only runs before registration were a memory-bandwidth probe (`bw.c`) and timing runs at $p=23$ and $p=5$ (`timing_early.log`, about 05:58–06:05 UTC), whose outcomes were already known from round 2. No $p=29$ or $p=31$ computation precedes the registration.
- **Reproducibility.** The file body is reproduced exactly by `predict.py 29 1 7 pos:28` and `predict.py 31 1 7 pos:30` (checked at completion).
- **Caveat.** The file entered git only with commit `40fc251` at 15:10 UTC, after the runs. The 06:12 timestamps are therefore not anchored externally. They are the file's own stamp and its file-system time.
- **The bands.** $\nu<1.17$: FAIL; $\nu>1.47$: HOLD; otherwise MIXED, which makes no prediction.
- **How $R^*$ is computed.** `predict.py` uses round 2's `bottleneck.py`, whose $R^*$ also includes the level-0 ratio $R_0=2^H/p^M$. For $c=0$ that is the only level.

### 5.2 Classification of every registered row

`code/round3/R3C/pred_eval.py` compares each row with the logs; its output is `data/round3/R3C/PREDICTIONS_evaluation.txt`.

| class | rows | meaning |
|---|---|---|
| **genuine test, confirmed** | **63** | band FAIL or HOLD, outcome unknown at registration, run afterwards by A and C (uniform) or A and D (positions; C also at $H=44$) |
| **genuine test, falsified** | **1** | uniform $\mathrm{Cov}(29,5,36)$: band FAIL ($\nu=1.112$), but it **holds** (A and C, all 28 classes) |
| known in advance | 11 | all $t=1$ rows (Lemma 10.11: $\mathrm{Cov}(p,1,H)$ iff $H\ge7$); $\mathrm{Cov}(29,5,29)$, $\mathrm{Cov}(31,5,31)$ hold and $\mathrm{Cov}(31,6,31)$ fails ($L_{29}=L_{31}=5$) |
| refuted by a proof (not tests) | 20 | rows the registration itself marks "FAIL (proved, Lemma 10.11)" |
| MIXED (no prediction) | 4 | $(29,2,13)$ holds; $(31,2,13)$ fails (4 missed); $(31,4,24)$ fails (2 missed); $(31,7,45)$ positions not run |
| not run | 21 | see §5.3 |

The two rows with $n=1$ at the end of the file ($\nu$ per single position for $H=44$ and $H=45$) annotate the $n=28$ rows and are not counted separately.

The 63 confirmed tests break down as follows.
- **Uniform FAIL band (39):**
  - $p=29$: $t=2$: $H=10..12$; $t=3$: $15..18$; $t=4$: $20..23$; $t=5$: $25..28$; $t=6$: $36..39$.
  - $p=31$: $t=2$: $10..12$; $t=3$: $15..18$; $t=4$: $20..23$; $t=5$: $25..29$; $t=6$: $30$, $38..40$.
  - Most of these lie far below the threshold; only a few test the threshold itself (see below).
- **Uniform HOLD band (22):**
  - $p=29$: $t=2$: $14..16$; $t=3$: $19..21$; $t=4$: $24..26$; $t=6$: $40$.
  - $p=31$: $t=2$: $14..16$; $t=3$: $19..21$; $t=4$: $25..27$; $t=5$: $30$, $38$; $t=6$: $41$.
- **Positions (2):**
  - $(29,7,45)$ covers at all 28 positions ($\nu=2.308$, HOLD). This is the planned certificate behind R1, run after registration by two programs.
  - $(29,7,44)$ fails at one or more positions ($\nu=1.149$, FAIL): it fails at $K''=3$ (§5.4, run at completion).

*The cases that test the thresholds themselves* (closest to $\nu\in[1.17,1.47]$):

| case | $\nu$ | band | outcome |
|---|---|---|---|
| $(29,3,18)$ | 1.064 | FAIL | fails, 2 residues ($K'=1$) |
| $(31,5,29)$ | 1.092 | FAIL | fails, 10 residues |
| $(31,6,40)$ | 1.058 | FAIL | fails, 2 residues at $K'=2$ ($K'=1$ covered) |
| $(29,6,39)$ | 1.107 | FAIL | fails, 2 residues at $K'=2$ ($K'=1$ covered) |
| $(29,7,44)$ positions | 1.149 | FAIL | fails at $K''=3$, 2 residues ($K''=1,2$ covered) |
| **$(29,5,36)$** | **1.112** | **FAIL** | **holds for all 28 classes: falsified** |
| $(29,3,19)$, $(31,3,19)$ | 2.128, 1.708 | HOLD | hold |
| $(29,4,24)$ | 1.761 | HOLD | holds |
| $(31,5,30)$, $(31,6,41)$, $(29,6,40)$, $(29,7,45)$ pos. | 2.184–2.308 | HOLD | hold |

*The falsified prediction.*
- Why the law says FAIL: at $(29,5,36)$ the bottleneck is level 1. There are 7 units and 29 elements of valuation 1, $\min_rm_1(r)=1$, and $R^*=R_1=2^{29}/29^5=26.17$; this is numerically the same as $R^*=R_0$ at $(29,5,29)$. With $n=1$ this would give $\nu=1.30$ (MIXED). The $\ln n$ term for $n=28$ classes moves it to $1.112$ (FAIL).
- What actually happens (Lemma R3C.1, proved after the outcome was seen): the 29 elements of valuation 1 form a unit multiple of $E_{29}$ modulo $29^5$. They therefore cover $\mathbb Z/29^5$ for every class. The law's random model does not apply to such a layer.
- $(31,5,38)$ (HOLD, confirmed) lies in the range of the same lemma, so its confirmation also says nothing about the counting mechanism.

The status of Conjecture 10.24 stays [heuristic]. Its FAIL side now has a registered counterexample. A corrected law would have to treat gate-type layers exactly; we did not attempt this.

### 5.3 Registered but not run (21 rows)

| rows | why not run |
|---|---|
| uniform $(29,6,41)$, $(29,6,42)$, $(31,6,42)$, $(31,6,43)$ (HOLD) | the scans at $t=6$ stop at the first $H$ that holds |
| $p=29$ positions $H=39..43$ (FAIL) | never planned; only $H=44$ was planned "if budget allows" |
| $p=29$ positions $H=46,47$ (HOLD) | not needed ($H=45$ covered everywhere, so the $H=46$ fallback never triggered) |
| $p=29$ positions $H=58$ (HOLD, two-block window) | not run |
| $p=31$ positions $H=40..44$ (FAIL), $46..48$ (HOLD), $62$ (HOLD) | $p=31$ depth 7 was not run at all (§6.1) |

The $t=1$ rows at $p=31$ with $H=8,9,10$ were not run either; they are counted as known (Lemma 10.11).

### 5.4 The registered $H=44$ prediction (run at completion)

The registration predicts that blocks of length $H=44$ fail at one or more of the 28 depth-7 positions ($\nu=1.149$, FAIL band, $n=28$). It marks this run "only if budget allows", and the original instance did not run it. At completion:
- **Program D** ran $K''=1,\dots,8$ and stopped at the first position that is not covered (`queue_completion_h44.sh`; log `p29_t7_H44/P29_t7_H44_D_K1-8.log`, 18:37–18:50 UTC). Positions $K''=1,2$ are covered. **$K''=3$ is not covered.** Exactly 2 residues mod $29^8$ are missed: $197\,789\,838\,580$ and $169\,097\,737\,247$.
- **Program A** recomputed $K''=3$ (`queue_completion_h44_A.sh`; log `p29_t7_H44/P29_t7_H44_A_K3.log`, 506 s). It lists **the same two residues**.
- **Program C** recomputed $K''=3$ as a third program (log `p29_t7_H44/P29_t7_H44_C_K3.log`, 555 s). It reports `miss=2 UNCOVERED`. Program C prints only the count, which agrees.

**Negative certificate [negative, computer-assisted, A and D, plus C].** The block of length 44 ending at $N^*=29^7\cdot3$ does not cover $\mathbb Z/29^8$; it misses exactly the two residues above.

*Outcome for the prediction.* The registered prediction is **confirmed**. It was a genuine out-of-sample test: the prediction was registered at 06:12:36, and the run was at 18:37. It is included in the totals of §5.2: 63 confirmed and 1 falsified, out of 64 genuine tests.

*Not concluded.*
- Positions $K''=4,\dots,28$ were not run at $H=44$, so the number of failing positions is unknown.
- At $K''=3$ itself the per-position band is MIXED ($\nu=1.292$, $n=1$).
- Nothing follows about $H<44$: those rows were not run, and coverage is not monotone in $H$.

*A remark on Conjecture 10.25 (hardest carries) [heuristic; not registered by this track].* Both missed residues lie in the classes $r\equiv11$ and $r\equiv23\pmod{29}$. These are exactly the two classes where the level-1 multiplicity $m_1(r)$ of `bottleneck.py` is smallest (1 118, against a mean of 1 130). The same holds at $(31,6,40,K'=2)$: the missed residues are $\equiv20,26\pmod{31}$, and those are the argmin classes, with $m_1=12$ against a mean of $16.5$. At $(29,6,39,K'=2)$, however, the missed residues are $\equiv6,14\pmod{29}$. There $m_1=34$, while the minimum is 33, attained at $9,11,24,25$; the profile is almost flat (33–39). So the concentration predicted by Conjecture 10.25 is seen in two of these three cases.

---

## 6. Partial and timing-only results

### 6.1 $p=31$ [partial]

- **Done.** The uniform depths $t\le6$ are certified by A and C with $H_t=7,14,19,25,30,41$ (Table 2). The two chain checkers give $f(1,31)\ge v_{31}((31^7-1)!)=917\,087\,130$.
- **Not an improvement.** That is **5 less** than the round-1 bound $917\,087\,135$ (note.md §4.4). Program D was run at $p=31$ only on the dump $(31,6,40,K'=2)$.
- **Missing for the next bound.** The 30 depth-7 positions $N^*=31^7K''$, $K''=1,\dots,30$, are missing, each needed from two programs. The planned length is $H=46$ (registered $\nu=2.614$, HOLD); then $c=1$ and the modulus is $31^8$. If all 30 cover, Proposition 10.10 with $D=8$ gives $f(1,31)\ge v_{31}((31^8-1)!)=28\,429\,701\,240$.
- **Cost estimate.** At fibre level $k=1$ each job needs two bitsets of $31^7$ bits (6.9 GB in all). Scaling the mean $p=29$ timings (A 535 s, D 293 s) by $(31/29)^7\approx1.6$ gives about 14 min for A and 8 min for D per position, so about 11 CPU-hours in total. With 9 GB, only one such job can run at a time. This does not fit the remaining budget of the track and was not started.

### 6.2 $\mathrm{Cov}(5,5,39)$ [timing only]

Note.md Conjecture 10.24 predicts that uniform $\mathrm{Cov}(5,5,39)$ holds. Only 104 of its $312\,500$ classes had been checked before.

| program | classes | outcome | time | source |
|---|---|---|---|---|
| A | 48 ($K'=1..59$, $5\nmid K'$) | all covered | 7.3 s | `timing_early.log` (terminal capture, before registration) |
| C | the same 48 | all covered | 11.5 s | `timing_early.log` (terminal capture) |
| D | 4 ($K'=1..4$) | all covered | 130–147 s each | `T5_t5_H39_D_48cls.log` (cut off by the spending limit; no end line) |

- **Weak provenance.** The A and C lines in `timing_early.log` were copied from the session's terminal, not written by `run.sh`.
- **Estimated cost of the full check.** Extrapolating to all classes gives about $312\,500\times0.15\text{ s}\approx13$ core-hours for A and $\approx21$ for C. D in its current form is not usable here (§4.3).
- **Not a certificate.** The full check was not run. This is not a certificate, nor evidence beyond the 104 classes known before.

### 6.3 $p=19$, depth 7, $K''=20$ [timing only]

- **Run.** One position beyond those needed for the round-2 bound: $N^*=19^7\cdot20$, $H=45$, $k=2$ (fibre $19^7$ bits). Both programs report it covered:
  - A: 292 s wall, 194 s CPU (`T19_t7_H45_K20_A.log`);
  - D: 249 s wall, 161 s CPU (`T19_t7_H45_K20_D.log`).
- **What a $D=9$ chain at $p=19$ would need.** All 342 depth-7 positions $K''<361$ with $19\nmid K''$, plus 18 depth-8 positions. The depth-7 part alone is about $342\times(194+161)\text{ s}\approx34$ CPU-hours.
- **Status.** A single position extends no bound; this is a timing measurement.

---

## 7. Computational record

All runs were on the round-3 VM (Intel Xeon @ 2.10 GHz) at `nice -n 10`, wrapped by `code/round3/R3C/run.sh`, which writes the command, start, end and wall/user/sys times into each log. Mostly one or two jobs ran at a time. Three overlapped for a few minutes: 06:22–06:26 (the stopped D validation), about 06:57 (`lemma_check.py`, 35 s) and 07:29–07:32 (`scanall_p31_*`). The completion runs used at most two cores. Binaries are in `/tmp/r3_R3C/bin/` and are rebuilt by the commands of §10.

| what | program(s) | command (from the repository root) | log(s) in `data/round3/R3C/` | wall time |
|---|---|---|---|---|
| validation, A and C | A, C, `bigbrute.py` | `env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/validate_r3.py A,C 20261013` | `validate_AC.log` | 75 s |
| validation, D | D, `bigbrute.py` | `… validate_r3.py D 20261013` | `validate_D.log` | 482 s |
| scans $p=29$, $t=1..5$ | A, C | `… scan_r3.py 29 t 2 58` ($t=1$: `29 1 2 10 --all`) | `scan_p29_t{1..5}.log` | < 1 s each |
| scan $p=29$, $t=6$ | A, C | `… scan_r3.py 29 6 2 58` | `scan_p29_t6.log` | 1 506 s |
| holds above the minimum, $p=29$ | A, C | `… scan_r3.py 29 t Hlo Hhi --all` | `scanall_p29_t{2..5}.log` | 80 s (t=5), < 1 s otherwise |
| scans $p=31$, $t=1..6$ | A, C | `… scan_r3.py 31 t 2 62` | `scan_p31_t{1..6}.log` | 3 429 s (t=6), < 2 s otherwise |
| holds above the minimum, $p=31$ | A, C | `… scan_r3.py 31 t Hlo Hhi --all` | `scanall_p31_t{2..5}.log` | 118 s (t=5), < 1 s otherwise |
| uniform $p=29$, $t\le6$, third program | D | `/tmp/r3_R3C/bin/covfast 29 t H_t k cls 3` | `U29_D_t{1..6}_H*.log` | 349 s ($t=6$), < 1 s otherwise |
| depth-7 positions, $p=29$ | A | `/tmp/r3_R3C/bin/fibcov 29 7 45 1 pos K` ($K=1..28$) | `p29_t7/P29_t7_H45_A_K*.log` | 460–854 s each; 4.2 h total |
| depth-7 positions, $p=29$ | D | `env COVFAST_ZMAX=16777216 /tmp/r3_R3C/bin/covfast 29 7 45 1 pos K` | `p29_t7/P29_t7_H45_D_K*.log` | 242–507 s each; 2.3 h total |
| missed-residue dumps | A, D | `env FIBCOV_DUMP=10 fibcov 29 6 39 1 pos 2` (and 31 6 40); `env COVFAST_DUMP=10 covfast …` | `N29_*`, `N31_*` | 9–37 s each |
| Lemma R3C.1 check | `bigbrute.py` | `python3 code/round3/R3C/lemma_check.py` | `lemma_check.log` | 36 s |
| timing $p=19$ | A, D | `fibcov 19 7 45 2 pos 20`; `covfast 19 7 45 2 pos 20` | `T19_t7_H45_K20_{A,D}.log` | 292 s, 249 s |
| timing $\mathrm{Cov}(5,5,39)$ | D | `covfast 5 5 39 5 pos <48 classes>` | `T5_t5_H39_D_48cls.log` | cut off after 4 classes (about 9 min) |
| timing $p=23$, $p=5$ (before registration) | A, C | see the log | `timing_early.log` | 60–74 s, 7–12 s |
| chain checks *(completion)* | `chain_r3.py`, `chain_c_r3.py` | §1.3 | `CHAIN_p29_p31_chain_r3.txt`, `CHAIN_p29_p31_chain_c_r3.txt`, `CHAIN_checker_validation_round2.txt` | < 5 s each |
| prediction evaluation *(completion)* | `pred_eval.py` | `python3 code/round3/R3C/pred_eval.py` | `PREDICTIONS_evaluation.txt` | < 1 s |
| large D checks *(completion)* | D | `code/round3/R3C/queue_completion_val.sh` | `valD/VD_*.log` | 1 103 s in total ($(13,8,46)$: 879 s) |
| $H=44$ test *(completion)* | D; then A and C on $K''=3$ | `code/round3/R3C/queue_completion_h44.sh`, `queue_completion_h44_A.sh` | `p29_t7_H44/*.log` | D 766 s ($K''=1,2,3$); A 506 s; C 555 s |

CPU totals (user time):
- A: 3.6 h on the depth-7 positions;
- D: 1.9 h on the depth-7 positions;
- scans: about 0.9 h;
- everything else: under 0.5 h.

---

## 8. Failed attempts and incidents

- [failed attempt] **First validation of D, stopped.** A first run of `validate_r3.py D`, at 06:22–06:30 UTC, was stopped after 12 of the 41 cases. Its partial output is in `/tmp/r3_R3C/validate_D_killed.log` and is not in the repository. `validate_r3.py` was edited at 06:35 before the complete run, and the edit itself is not recorded. All 12 cases of the stopped run have the same reference counts as the complete run, which is the one cited.
- **No `/usr/bin/time`.** An attempt to time the validation with `/usr/bin/time` failed because the VM does not have it (`/tmp/r3_R3C/val_time.txt`). `run.sh` uses bash's `time` instead.
- [failed attempt] **D on $\mathrm{Cov}(5,5,39)$.** D is unusable here in its current form (130–147 s per class, against 0.15 s for A), because its list phase is not capped by the fibre size (§4.3, §6.2). The run was then cut off by the spending limit.
- **Cut-off at about 08:12–08:20 UTC.** The external spending limit stopped the original instance. The last completed position job ended at 08:12:18, and the last line written by the original runs is at 08:19 (`T5_t5_H39_D_48cls.log`). At that point:
  - the depth-7 positions $K''=1..5$ were done by both programs;
  - the D timing run for $\mathrm{Cov}(5,5,39)$ was interrupted;
  - the report was a stub.

  The lead resumed the queue at 15:08 UTC with `queue_p29_t7.sh 6 17` and `queue_p29_t7.sh 18 28` in parallel (`/tmp/r3_R3C/queue_p29_{a,b}.out`).
- **Two logs committed half-finished.** The lead's work-in-progress commit `2311c5f` (17:12 UTC) caught `P29_t7_H45_A_K15.log` and `…_A_K27.log` while those runs were still going. Commit `307a07a` (18:33 UTC) has the complete versions, and the chain checks use them. In the same way, commit `024b87e` (19:12 UTC) caught `p29_t7_H44/P29_t7_H44_C_K3.log` before it finished at 19:13; the working-tree version is complete.
- [negative] **A falsified prediction.** The prediction that $(29,5,36)$ fails was falsified (§5.2). It is a failed prediction, not a failed computation.

---

## 9. Open issues

1. **$p=31$, depth 7.** 30 position certificates at $H=46$ are needed, each by two programs, for $f(1,31)\ge28\,429\,701\,240$ (about 11 CPU-hours; §6.1).
2. **$p=29$ beyond $D=8$.** Depth 8 needs fibre bitsets of $29^8$ bits (62.5 GB) or a different method (§1.1).
3. **Third-program check at depth 7.** Program C has not checked the 28 positions with $H=45$ at $p=29$. The two-program rule does not require it, but a referee might want it. C was run once at this size, on $(29,7,44,K''=3)$, where it took 555 s and about $2\times2$ GB, so all 28 would take about 4.5 CPU-hours.
4. **Lemma R3C.1** has been checked by this report only.
5. **Conjecture 10.24** has a registered counterexample on its FAIL side ($(29,5,36)$). A version that treats gate-type layers exactly has not been formulated or tested.
6. **Registered predictions not run:** 21 rows (§5.3). At $H=44$ only $K''\le3$ was run (§5.4).
7. **Registration time** is anchored only by the file's own timestamp and its file time; there is no external record from before 15:10 UTC.
8. **Program D's list phase** should be capped by the fibre size before D is used on small moduli.

---

## 10. Reproduction

From the repository root:

```sh
# binaries (the hashes of section 4.2 are reproduced with Ubuntu clang 18.1.3 on the round-3 VM)
mkdir -p /tmp/r3_R3C/bin
clang -O3 -march=native -o /tmp/r3_R3C/bin/fibcov  code/round2/R3/src/fibcov.c                   # A
clang -O3 -march=native -o /tmp/r3_R3C/bin/fibcov2 code/round2/R3/src/fibcov2.c                  # B (not used here)
clang -O3 -march=native -o /tmp/r3_R3C/bin/covchk  code/round2/review/computation/covchk.c       # C
clang -O3 -march=native -o /tmp/r3_R3C/bin/covfast code/round3/R3C/covfast.c -lgmp               # D

# validations (about 10 min)
env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/validate_r3.py A,C 20261013
env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/validate_r3.py D 20261013
python3 code/round3/R3C/lemma_check.py

# scans (p = 29: about 30 min; p = 31: about 1 h)
for t in 1 2 3 4 5 6; do env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/scan_r3.py 29 $t 2 58; done
for t in 1 2 3 4 5 6; do env R3C_BIN=/tmp/r3_R3C/bin python3 code/round3/R3C/scan_r3.py 31 $t 2 62; done

# program D on the uniform depths at p = 29 (about 6 min)
for th in "1 7 0" "2 13 0" "3 19 0" "4 24 0" "5 29 0" "6 40 1"; do set -- $th; /tmp/r3_R3C/bin/covfast 29 $1 $2 $3 cls 3; done

# depth-7 positions at p = 29: 28 x (A about 9 min + D about 5 min), about 4.3 GB per job, one log per (program, K'').
# NOTE: the script writes into data/round3/R3C/p29_t7/ and overwrites the archived logs; change OUT first.
sh code/round3/R3C/queue_p29_t7.sh 1 28

# chain checks on the archived logs
L=data/round3/R3C:data/round3/R3C/p29_t7
R3C_LOGS=$L python3 code/round3/R3C/chain_r3.py code/round3/R3C/specs/p29_AD.txt
R3C_LOGS=$L python3 code/round3/R3C/chain_c_r3.py A 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"
R3C_LOGS=$L python3 code/round3/R3C/chain_c_r3.py D 29 8 "1:7,2:13,3:19,4:24,5:29,6:40" "7:45"

# completion runs: large exact checks of D (about 18 min), and the H = 44 test (D about 13 min, then A and C about 9 min each)
sh code/round3/R3C/queue_completion_val.sh
sh code/round3/R3C/queue_completion_h44.sh && sh code/round3/R3C/queue_completion_h44_A.sh

# predictions: regenerate the registered table and compare it with the outcomes
python3 code/round3/R3C/predict.py 29 1 7 pos:28; python3 code/round3/R3C/predict.py 31 1 7 pos:30
python3 code/round3/R3C/pred_eval.py
```

Python 3 (3.13 here) with `numpy` (2.5 here; needed by `bottleneck.py` through `predict.py`). GMP is needed for D.
