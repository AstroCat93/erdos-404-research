# Adversarial check of track R3C (round 3, 2026-10-13): certified covering frontier at p = 29 (and p = 31)

Checker: check_R3C. Code: `code/round3/check_R3C/`. Logs: `data/round3/check_R3C/`. Binaries: fresh `clang -O3 -march=native` builds of the committed sources, in the session scratch directory; the sha256 of the binary is written into every log.
Track material read (read-only): `data/round3/reports/R3C.md` (all 485 lines, the version of 19:14 UTC), every file in `code/round3/R3C/` and `code/round3/R3C/specs/`, every log in `data/round3/R3C/` (with `p29_t7/`, `p29_t7_H44/`, `valD/`), the original instance's scratch files in `/tmp/r3_R3C/`, and note.md §1.4, §3.5, §3.7, §4.2, §4.4, §10.2, §10.5, §10.7 (rows C1–C6). The sources of programs A, B and C were read in full: `code/round2/R3/src/fibcov.c`, `fibcov2.c`, `code/round2/review/computation/covchk.c`; program D (`code/round3/R3C/covfast.c`) was read line by line.
CPU used: about 1.5 core-hours (A 16 min, C 39 min, D 8 min of CPU on depth-7 positions; own brute force 24 min; everything else under 2 min), wall time about 1 h 15 min. All jobs ran at `nice -n 10`, never more than two of mine at a time, never more than 8.7 GB resident in total (each A and C job under a `ulimit -v` cap of 4.7 GB; D jobs alone). Another agent's job (`rsolve`, about 2.5 GB, one core) was running on the machine at the same time and was not touched.
Every program of this check was written for this check; `indep.py` shares no code with programs A–D, `bigbrute.py` or anything else in `code/round2` and `code/round3/R3C`.

## 0. Verdicts

| id | claim (short) | verdict |
|---|---|---|
| R1 | $f(1,29)\ge v_{29}((29^8-1)!)=17\,865\,943\,312$ | **confirmed** [computer-assisted]. Chain logic checked against Prop. 10.10; all 68 certificate logs audited line by line; bound value recomputed; binaries rebuilt byte-identically; A and D re-run at $K''=4,27$, and C (a third program) at $K''=15,21$: all COVERED; both chain checkers re-run (CHAIN OK) with new controls. The independence wording behind it needs a fix (see R6) |
| R2 | for $1\le a<29^8-45$: $f(a,29)<v_{29}((a+45)!)$ or $f(a,29)\ge17\,865\,943\,312$ | **confirmed** (general-$a$ form of Prop. 10.10 re-derived; same certificates) |
| R3 | minimal uniform $H_t$: $7,13,19,24,29,40$ ($p=29$), $7,14,19,25,30,41$ ($p=31$) | **confirmed** [computer-assisted]. Scan logic and logs checked; for $t\le5$ every non-trivial $H\le H_t$ re-decided by an own brute force without fibres, with the same exact miss counts as A and C |
| R4 | three two-residue failures | **confirmed** [negative, computer-assisted]. In addition, an own meet-in-the-middle test (no fibres, exact integers) confirms that all six listed residues are not subset sums |
| R5 | Lemma R3C.1 | **confirmed** [proved]: proof checked line by line; own numerical check (all classes) for $p=7..23$ and, at $p=29$, for $t=2,3,4$, $30\le H\le58$ and for $t=5$, $H=36..39$ |
| R6 | program D correct and independent of A | **confirmed-with-fixes**. Correctness: confirmed (code read, re-runs, own brute force). Independence: the statement "shares no code beyond four generic boilerplate lines" holds only for verbatim lines. With identifiers renamed, D reproduces A's program skeleton, A's subset-sum doubling loop and A's shift-OR inner expression, and B's counting-sort block. This is the same level of overlap as between A and C, which round 2 accepted. The report must say so (§5) |
| R7 | predictions: 63 confirmed, 1 falsified, 11 known, 20 proved, 4 MIXED, 21 not run | **confirmed-with-fixes**. Counts reproduced by an own recount. Not reported: the registration's own headline prediction "minimal $H_t$ = first HOLD-band $H$" is wrong at $(29,2)$ (registered 14, observed 13). Two smaller inaccuracies (§8) |
| R8 | $p=31$: uniform $t\le6$ only; $f(1,31)\ge917\,087\,130$, not an improvement | **confirmed** |
| R9 | timing only: $p=19$ depth 7, $K''=20$; $\mathrm{Cov}(5,5,39)$ on 48 + 4 classes | **confirmed** (as timings; correctly not counted as results) |

No mathematical or computational error was found in the certificate behind R1. The fixes are about wording: the independence of D (R6), the registered minimal-$H$ prediction at $(29,2)$ and two provenance details (R7).

## 1. The chain behind R1 and R2 (Proposition 10.10)

**Hypotheses, item by item** ($p=29$, $D=8$; note.md Prop. 10.10, Thm 3.12(a), Lemma 1.3):
- Depths $t=1..6$ use the uniform branch: $\mathrm{Cov}(29,t,H_t)$ with $H_t=7,13,19,24,29,40$ over all unit classes $K'\bmod29^{c}$, where $c=v_{29}((H_t-1)!)=0,0,0,0,0,1$ (recomputed). Then $H_t+1<29^t$ for every $t$: $8<29$, and the rest are obvious.
- Depth $t=7$ uses the position branch. The positions needed are all $K''<29^{8-7}=29$ with $29\nmid K''$, i.e. exactly $K''=1,\dots,28$. For $H=45$, $c=v_{29}(44!)=1$, so the modulus is $29^{t+c}=29^8$. Also $29^7K''-45>1$.
- A first failure $N^*<29^8$ has $29\mid N^*$ (Lemma 1.3(iv)) and $v_{29}(N^*)\le7$, so it is covered by one of the two branches. No depth is missing, and no depth $\ge8$ can occur below $29^8$.
- The block that the programs test is the one of Theorem 3.12(a): A computes $y_i=\prod_{s\le i}(29^7K''-(H-s))\bmod29^8$, C and D compute $(N^*-H+1)\cdots(N^*-H+i)$, which is the same product ($N^*-H+s=N^*-(H-s)$). D computes it exactly with GMP and checks $M=v_p(N^*!)-v_p((N^*-H)!)=t+c$ by Legendre; A and C use $M=t+c$ directly.

**The value of the bound.** $v_{29}((29^8-1)!)=(29^8-1-8\cdot28)/28=500\,246\,412\,736/28=17\,865\,943\,312$, recomputed both by Legendre's sum and by the digit-sum formula. Also recomputed: $v_{29}((29^7-1)!)=616\,067\,004$, $v_{31}((31^7-1)!)=917\,087\,130$ (5 below round 1's $917\,087\,135$), $v_{31}((31^8-1)!)=28\,429\,701\,240$, and the ratio $17\,865\,943\,312/616\,067\,009=29.0000001$.

**R2.** In the general-$a$ form, a first failure $N^*=29^tK''<29^8$ is excluded whenever $N^*-H>a$. Otherwise $N^*\le a+H\le a+45$, and then $f(a,29)<v_{29}(N^*!)\le v_{29}((a+45)!)$. If no first failure lies below $29^8$, then $P(a,29,29^8-1)$ holds; this needs $29^8-1>a$, which $a<29^8-45$ gives, and then $f(a,29)\ge v_{29}((29^8-1)!)$. This is what R2 states. Its status (computer-assisted, same certificates) is right, and the report is right not to apply it to any particular $a$.

## 2. Audit of every certificate log (`logaudit.py`, log `logaudit.log`)

The script re-derives $c$, $M$ and the expected class or position set for every certificate. It then reads each log line by line and checks:
- the command line: the binary path is `/tmp/r3_R3C/bin/{fibcov,covchk,covfast}`, and the arguments $p\ t\ H\ k$ and mode are the stated ones;
- the program's header line and per-$K$ lines: $c$, $M$ and $k$ as stated;
- the set of $K$ values. A uses $K'=1..28$, C uses $K'+2\cdot29=59..86$ and D uses $K'+3\cdot29=88..115$ (one $K$ when $c=0$). Every one must report `missing=0 COVERED` / `miss=0 COVERED`;
- the summary line: `ALL_COVERED`, with the right `nK`, `fail=0` and `worst_missing=0`;
- the end line is present, and the log contains no other output (for example an error message).

| certificates | program(s) | logs | result |
|---|---|---|---|
| uniform $t=1..6$, $p=29$ | A and C (via `scan_r3.py`) | `scan_p29_t{1..6}.log` | 6/6 OK: the HOLDS line, A over 1/1/1/1/1/28 classes, C over the same numbers with lifted representatives, all covered |
| uniform $t=1..6$, $p=29$ | D | `U29_D_t*_H*.log` | 6/6 OK (`cls 3`; $K=4$ for $c=0$, $K=88..115$ for $t=6$) |
| depth 7, $K''=1..28$, $H=45$ | A and D | `p29_t7/P29_t7_H45_{A,D}_K*.log` | **56/56 OK**: command, header `c=1 M=8 k=1` (D: `ZMAX=16777216`), one line `K=K'' … missing=0 COVERED`, `SUMMARY … nK=1 fail=0 … ALL_COVERED`, end line, no other output |
| uniform $t=1..6$, $p=31$ (R8) | A and C | `scan_p31_t{1..6}.log` | 6/6 OK (30 classes at $t=6$) |
| holds above the minimum (R3) | A and C | `scanall_p{29,31}_t*.log` | 23/23 OK, including $(29,5,36..39)$ and $(31,5,38,39)$ over all 28 or 30 classes |

**Timings in the report.** Wall time per position is 460–854 s for A and 242–508 s for D, 4.16 h and 2.28 h in total. User time is 3.63 h for A and 1.92 h for D. All of these match §1.2 and §7 of the report.

**Contradictory lines** (`contradictions.py`). Both chain checkers accept a certificate if any line reports it covered, and they ignore other lines for the same $K$. I therefore listed every (program, $p$, $t$, $H$, $K$) in all 642 result lines of `data/round3/R3C/**`. None has two different miss counts. Of the 32 $(p,t,H,K)$ that two or more programs ran, none disagrees.

**Binaries.** Fresh `clang -O3 -march=native` builds (Ubuntu clang 18.1.3) of the committed sources are byte-identical to `/tmp/r3_R3C/bin/`:
- A: `4b551a73…`;
- B: `f3504700…`;
- C: `0ceec1e3…`;
- D: `7596867116ee…`, which is also identical to `covfast_check`.

`fibcov.c` still has the round-2 sha256 `1dc737f9…` of `data/round2/logs_original/R3/binary_hashes.txt`. The file times are consistent with the report:
- `covfast` was built at 06:20:29, before the first D run (the stopped validation, 06:22);
- `covfast.c` was last touched at 06:56:00;
- the round-2 sources date from 05:34.

## 3. Re-runs at depth 7 (logs `X_*_p29_t7_H45_K*.log`)

These are fresh builds with the same hashes, at $H=45$, $k=1$, and with the same environment as the archived runs (D: `COVFAST_ZMAX=16777216`). I chose positions from all three provenance batches: the original instance ($K''=4$), the lead's first queue ($K''=15$, whose A log was committed half-finished in `2311c5f`) and the second queue ($K''=21$, and $K''=27$, also committed half-finished).

| program | $K''$ | result | wall | archived result |
|---|---|---|---|---|
| A | 4 | `missing=0 COVERED` | 501 s | COVERED (567 s) |
| A | 27 | `missing=0 COVERED` | 484 s | COVERED (476 s) |
| D | 4 | `missing=0 COVERED`; all 29 fibres end in the complement phase | 242 s | COVERED (336 s) |
| D | 27 | `missing=0 COVERED`; all 29 fibres end in the complement phase | 245 s | COVERED (324 s) |
| **C** (third program) | 15 | `miss=0 COVERED` | 603 s | not run before |
| **C** (third program) | 21 | `miss=0 COVERED` | 576 s | not run before |

So two positions now carry three programs, A, D and C. C has a different element arithmetic (128-bit products), a different construction of the fibre start sets (two-list split, lowest-set-bit recursion) and a different cyclic kernel (two `or_off` passes with bit-by-bit heads). It is the program whose independence from A round 2 accepted.

## 4. Chain checkers (log `chains_rerun.log`)

**Re-run.** Both checkers were re-run from the archived logs (`R3C_LOGS=data/round3/R3C:data/round3/R3C/p29_t7`). Every line of the report's §1.3 is reproduced:
- `chain_r3.py`: CHAIN OK $17\,865\,943\,312$ for `p29_AD` and `p29_AC_AD`; CHAIN OK $616\,067\,004$ for `p29_ACD_D7`; CHAIN OK $917\,087\,130$ for `p31_AC_D7`. The five negative controls give CHAIN PARTIAL.
- `chain_c_r3.py`: `[A]` and `[D]` give CHAIN OK $17\,865\,943\,312$ at $D=8$. `[C]` is INCOMPLETE at $D=8$, which is correct because C has no depth-7 logs there. At $D=7$, A, C and D give CHAIN OK at $p=29$, and A and C at $p=31$; D is INCOMPLETE at $p=31$.
- On program C's round-2 logs, `chain_c_r3.py` reproduces `data/round2/review/computation/chain_c.out` line for line (six primes).

**Additional controls of mine:**
- I copied the 56 depth-7 logs and deleted the D log for $K''=17$. Both checkers then fail at exactly that position: `NOT certified: [17]`, CHAIN PARTIAL at $N=29^7\cdot17$ ($f\ge10\,473\,139\,180$), and `[D] INCOMPLETE ['pos t=7 K=17']`.
- I left that log in but edited its line to `missing=1 NOT_COVERED`. The result is the same.
- `chain_c_r3.py A` with the depth-7 length set to 44 and the H44 directory added gives INCOMPLETE.

**Logic of the checkers, read against Prop. 10.10.**
- `chain_r3.py` excludes a depth by a uniform certificate (all units mod $p^c$ covered, from $K\bmod p^c$ of the covered lines, and $H+1<p^t$) or position by position ($p^tK''-H>1$). It then takes $N=\min(p^D,\min_tp^tK_t)$, where $K_t$ is the first position that is not excluded, and outputs $v_p((N-1)!)$. The "PARTIAL" bound is valid. If $N^*<N$, then $N^*=p^tK''$ with $t<D$ and $K''<K_t$, so $N^*$ is excluded. Hence $P(1,p,N-1)$ holds, and Lemma 1.3(i) gives the bound.
- `chain_c_r3.py`: the exclusion logic is that of the round-2 `chain_c.py`. I diffed the two files. The differences are the command-line plan, the log directories, the choice of program, a generic exception syntax (`t:H:K=H'`, which replaces the hard-coded $K''=37\mapsto41$), `strip()` of each line, and computing $K\bmod p^c$ instead of reading `Kmodpc=`. The `strip()` is needed because the scan logs indent the per-class lines. I checked that no indented line other than a genuine per-class result can match: the prefixed lines `A: A p=…` and `C: C p=…` do not match.
- Both checkers ignore NOT_COVERED lines for a $K$ that also has a COVERED line (§2). No such pair exists in these logs.

**Minor.** The docstring of `chain_c_r3.py` still says "three changes and no change to its logic", and it lists neither the two parsing changes nor the exception syntax. The report's §1.3 states them correctly.

## 5. Program D: correctness and independence (R6)

### 5.1 Correctness: code read line by line

I confirm every point of the report's §4.3. In more detail:
- **Elements** (GMP). The valuation of each exact product is compared with $v((H-1)!)-v((H-1-i)!)$, $M$ is compared with Legendre's formula at the position, and an element vanishing mod $Q$ aborts the run.
- **The split.** $L=\{v<k\}$; the elements of $U$ are divisible by $p^k$, which is checked at run time, and $U$ is stored as $(y/p^k)\bmod F$.
- **$\Sigma(L)$.** It is built by doubling with reduction mod $Q$ and counting-sorted by residue mod $p^k$. The start lists are $(s-r)/p^k\in[0,F)$, because $s\equiv r$ and $0\le r<p^k$.
- **Phases.** In the list phase each list doubles while $2m\le$ `LISTMAX` (duplicates are harmless). The bitset is built from the list.
- **The `or_rot` kernel.** For output words $j<\lceil w/64\rceil$ the source starts at $F-w+64j$. Where it passes $F$, the overshoot is at most 63 bits. This stays inside the 128-bit pad written by `make_pad`, which is redone after every step, including when $F<128$, where it wraps several times. Later words read $64j-w+b<F$ for output bits below $F$. All reads stay within `NW+3` words. Bits $\ge F$ of the last word are masked before they are counted.
- **The complement step.** $Z\leftarrow Z\cap(Z+w)$ is exact, because $x$ is missed after adding $w$ iff $x$ and $x-w$ were both missed. The binary search splits the sorted $Z$ at $F-w$. The wrapped part ($<w$) followed by the unwrapped part ($\ge w$) is sorted, so the merge intersection is valid. The phase starts only when the number missing is $\le$ `ZCAP`$=\min($`ZMAX`$,F)$. The extraction is cross-checked against the popcount.
- **Loop conditions.** The bitset loop stops when the set is full or when at most `ZMAX` residues are missing. An empty fibre counts $F$ missed residues. `cls` mode builds $K=K'+\mathrm{LIFT}\cdot p^c$, or $1+\mathrm{LIFT}$ when $c=0$.

I found no defect. A conceptual point: a false COVERED needs spurious reachable residues. Neither the doubling loop nor the counting sort can create one unless the modular arithmetic is wrong, and both are elementary. The places where a subtle error could hide are the cyclic kernel, the phase switching and the element arithmetic, and those are the parts that differ from A (§5.2).

### 5.2 Independence (`simcheck.py`, log `simcheck.log`)

**Exact-line count.** With comments removed and all whitespace deleted, I reproduce the report's counts of identical lines of at least 20 characters: A–D 4, C–D 8, B–D 3. The counts for the round-2 pairs are A–B 2, A–C 5 and B–C 4.

**Renamed-identifier comparison.** Exact lines miss copies in which the variables have been renamed. I therefore replaced every identifier that is not a C keyword or a standard-library or GMP name by `ID`, and every literal number by `NUM`, and compared again:

| pair | identical lines after renaming (≥ 8 tokens) | 10-gram containment (X in Y, Y in X) | shared runs ≥ 25 tokens (longest) |
|---|---|---|---|
| A–B (one author) | 15 | 0.187, 0.149 | 12 (42) |
| A–C (accepted as independent in round 2) | 19 | 0.298, 0.327 | 20 (67) |
| **A–D** | **20** | **0.299, 0.217** | **20 (69)** |
| C–D | 19 | 0.261, 0.173 | 15 (70) |
| B–D | 6 | 0.141, 0.128 | 13 (91) |

The shared material between A and D is concrete:
- **The whole driver.** This covers the argument order and parsing (`P = strtoull(argv[1], 0, 10); T = atoi(argv[2]); …`), the `pos`/`cls` class enumeration with `nsplit`/`split`, and the per-$K$ loop (`if (miss) { n…++; if (miss > worst) worst = miss; if (stop) break; }`). It also covers the result and summary format: `SUMMARY D p=… mode=%s nK=%zu fail=%zu worst_missing=%llu %s total=%.1fs` is A's format string with one letter changed, with the same `COVERED`/`NOT_COVERED`/`ALL_COVERED`/`SOME_NOT_COVERED` tokens.
- **The subset-sum doubling loop.** A's `S1`/`S2` loops and D's `sums` loop are token for token the same: `size_t h = (size_t)1 << j; for (…) { s = S[a] + L[j]; if (s >= Q) s -= Q; S[h + a] = s; }`.
- **The counting sort.** `size_t *fill = malloc(sizeof(size_t) * PK); memcpy(fill, …, sizeof(size_t) * PK);` is A's line with `bst` renamed. The enclosing block `{ … memcpy …; for (…) srt[fill[sums[a] % PK]++] = sums[a]; free(fill); }` is a 91-token run shared with B (`fibcov2.c`). The prefix-sum lines are C's, with C's variable name `start`.
- **The shift-OR inner expression.** `v = in[j] | (src[j - j0] >> o) | (src[j - j0 + 1] << oo)` with a constant offset is A's `seg_or` expression.
- **Smaller items.** The `w == 0` skip, the Legendre and timer helpers, and the tail masking (B's `clear_tail`) are also shared.

What is not shared:
- the element computation: exact GMP products at the position with valuation and Legendre checks, against A's 128-bit modular products of $p^tK-(H-s)$;
- the cyclic wrap: D's 128-bit pad, against A's per-segment kernel with a bit-by-bit slow path `grab`;
- the list phase (D's own, though B also starts from an explicit list) and the complement phase (D's own);
- A's meet-in-the-middle split. At depth 7 this is idle: $|L|=16$, so $n_1=0$.

**Assessment.**
- D is not "independent of A" in the sense of "written without A's code". It is a re-implementation of the same fibre method by an author who had A, B and C open. It keeps A's skeleton and enumeration code with renamed variables and adds new code at the points where the computation is delicate.
- The report's sentences "they share no code beyond four generic boilerplate lines" (headline) and "No algorithmic code is shared with A" (§4.2) are therefore not accurate. The doubling enumeration of $\Sigma(L)$ and the counting sort build the fibre start sets, which is algorithmic code, though elementary.
- The overlap is of the same size as the A–C overlap that round 2 accepted. The shared fragments are short, correct by inspection and covered by the brute-force validation at every $k$. They cannot produce a spurious covered residue except through faulty modular arithmetic, which inspection rules out.
- **So the two-program certificate A+D is meaningful, but the text must describe the relation honestly.** Suggested wording: "D was written in round 3 by a different instance, with the sources of A, B and C at hand. It re-implements the same fibre method. Its driver, its enumeration of $\Sigma(L)$ and its counting sort follow A and B closely, with renamed variables. Its element arithmetic (exact GMP products at the actual position), its cyclic kernel (padded, single pass) and its list and complement phases are new."
- Cleanest remedy, optional: run C on the remaining 26 depth-7 positions, about 4.3 CPU-hours at about 590 s each. R1 would then also rest on A+C, the pair round 2 accepted, with D as a third program everywhere. This check ran C on $K''=15$ and $21$ (§3).

### 5.3 Validation record of D

- `validate_D.log` reports 7 680 comparisons and 0 mismatches against `bigbrute.py`, with 141 failing (case, $K$) pairs. `validate_r3.py` forces every phase and every switch between phases (`LISTMAX=1`; `LISTMAX=64` with `ZMAX=0`; `ZMAX=10^9`; `LISTMAX=4096` with `ZMAX=17`) at every legal $k$.
- The seven `valD/` logs say what §4.4 of the report says: $(11,7,39,1)=1\,389\,738$; $(11,7,40,37)=2$ with the two residues of `covmiss.c`; $(11,7,41,37)=0$; $(17,7,42)$ with $K'=5$ covered and $K'=6$ missing 2; $(7,6,33,5)=2$; $(7,6,34,5)=0$; $(13,8,46,1)=26$, with the 26 residues listed.
- My own meet-in-the-middle test (§6.2) confirms that every residue D lists in these logs is indeed missed. That covers all 2 + 2 + 26 of them.
- `bigbrute.py` is not fully independent of the track: it was written by the same instance as D. Its method, a single big-integer bitset without fibres, is the same as that of my `bitcover` (§6), which was written separately.

## 6. Own brute force without fibres (`indep.py`; logs `indep_*.log`)

`indep.py` builds the block as exact Python integers $(N_1+1)\cdots(N_1+i)$ at the actual position, and computes $M$ by Legendre at the position. It uses no fibre split. It has two independent engines:
- `bitcover`: the reachable set as one Python integer of $p^M$ bits, updated by $S\leftarrow S\mid\mathrm{rot}(S,y)$. It gives the exact miss count, for $p^M$ up to about $6\cdot10^8$.
- `mitm`: for single residues $x$ at any size. All subset sums of the two halves of the block are enumerated exactly (numpy int64), and $x-a\pmod{p^M}$ is looked up in the sorted second half.

**Self-test** (`indep_selftest.log`). I ran 582 small cases $(p,t,H,K)$ with $p\le13$, $t\le3$ and $p^M\le30\,000$; 387 of them fail. For every residue, the two engines agree on whether it is reached, with 0 mismatches, and $M=t+c$ in every case.

### 6.1 R3: the scans for $t\le5$ (`indep_scans.log`)

For $t\le5$ every $H\le H_t$ has $c=0$, so one class decides. I re-decided every $H$ that is not excluded by counting, at the position $K=5$; A used $K=1$, C used $K=1$ or $3$, D used $K=4$. Every miss count equals the count of A and C in the scan logs:

| $p$, $t$ | $H$ : exact number of residues missed (mine) |
|---|---|
| 29, 1 | 5, 6: Lemma 10.11; **7: 0** |
| 29, 2 | 10: 451, 11: 236, 12: 67, **13: 0** |
| 29, 3 | 15: 7865, 16: 2184, 17: 244, 18: 2, **19: 0** |
| 29, 4 | 20: 217553, 21: 68067, 22: 5475, 23: 30, **24: 0** |
| 29, 5 | 25: 5738438, 26: 1596825, 27: 112912, 28: 730, **29: 0** |
| 31, 1 | 5, 6: Lemma 10.11; **7: 0** |
| 31, 2 | 10: 489, 11: 151, 12: 14, 13: 4, **14: 0** |
| 31, 3 | 15: 12150, 16: 4204, 17: 646, 18: 42, **19: 0** |
| 31, 4 | 20: 377755, 21: 147391, 22: 31352, 23: 1066, 24: 2, **25: 0** |
| 31, 5 | 25: 11567544, 26: 4565402, 27: 684050, 28: 18070, 29: 10, **30: 0** |

Also recomputed: $\rho_0=6$ for $p=29,31$, and $\rho_0$ for $p=3,\dots,23$ as in note.md §10.2; $L_p=2,2,2,3,3,4$ for $p=7,\dots,23$; and $L_{29},L_{31}\ge5$ (I tested only up to $p^5$). The counting refutations ($2^H<p^M$) and the Lemma-10.11 refutations ($(H-1)\bmod p<6$) in the scan logs were checked by hand for $t=6$. At $p=29$: $H\le34$ by counting, $H=35$ by the lemma. At $p=31$: $H\le29$ and $32..34$ by counting, $35..37$ by the lemma. The minimality at $t=6$ ($H=36..39$ at $p=29$; $30,31,38,39,40$ at $p=31$) rests on A and C, with identical exact counts in the scan logs (§2). It is out of reach of a fibre-free bitset ($p^7$ bits).

### 6.2 R4 and R6: the listed missed residues (`indep_negatives.log`)

For each listed residue, the meet-in-the-middle engine decides exactly whether it is a subset sum. For each case it also tests 20 random residues, which should be covered:

| case | modulus | listed residues (from) | not subset sums? | random residues covered |
|---|---|---|---|---|
| $(29,6,39)$, $K'=2$ | $29^7$ | 9681558076, 7454824172 (A, D dumps) | **both** | 20/20 |
| $(31,6,40)$, $K'=2$ | $31^7$ | 25349343487, 3557184957 (A, D dumps) | **both** | 20/20 |
| $(29,7,44)$, $K''=3$ | $29^8$ | 197789838580, 169097737247 (A, D, `p29_t7_H44/`) | **both** | 20/20 |
| $(11,7,40)$, $K''=37$ | $11^{10}$ | 23022655245, 18038488330 (D, `valD/`; round-2 `covmiss.c`) | **both** | 20/20 |
| $(7,6,33)$, $K'=5$ | $7^{10}$ | 241978387, 94559789 (D, `valD/`) | **both** | 20/20 |
| $(13,8,46)$, $K''=1$ | $13^{11}$ | the 26 residues of `valD/VD_13_8_46_K1.log` | **all 26** | 20/20 |

So the three negative certificates of R4 are confirmed by a third method that has no fibre split and uses exact integers. This method shows only that the listed residues are missed. That they are the **only** ones rests on A, C and D.

### 6.3 R5 and R7: Lemma R3C.1 and the falsified prediction (`indep_lemma.log`, `indep_lemma29.log`)

**Lemma R3C.1 for $p=7,\dots,23$** (`indep_lemma.log`). I took every class $K'=1..p-1$, with representatives $K'+7p$, for $2\le t\le L_p$ with $p^{t+1}\le7\cdot10^6$ and $p<H\le2p$. That is 172 triples $(p,t,H)$. In all 172 the outcome is the same for every class, and it is exactly what the lemma says:
- the 126 triples with $H\ge p+1+\rho_0$ are covered in every class;
- in the 46 others, **no** class is covered.

This reproduces the counts of `lemma_check.log` (126 and 46) with a separately written program and other class representatives.

**$p=29$** (`indep_lemma29.log`).
- $t=2,3,4$: for every $H=30..58$ and all 28 classes ($K'+5\cdot29$), the outcome agrees with the lemma, uniformly in the class, with no mismatch.
- $t=5$: $\mathrm{Cov}(29,5,H)$ holds over all 28 classes for $H=36,37,38,39$ (a fibre-free bitset of $29^6$ bits; 260–275 s per $H$).

So the falsified registered prediction, FAIL at $(29,5,36)$, is confirmed to be falsified by a fourth program, which has no fibre split. The run of holds at $(29,5,36..39)$ in §2 of the report is reproduced.

## 7. Lemma R3C.1, line by line (R5)

Setting: $p$ odd, $2\le t\le L_p$, $p<H\le2p$, $\rho=H-1-p\in[0,p-1]$.
- $c=v_p((H-1)!)=1$, because $p\le H-1\le2p-1$. So $M=t+1$. Also $H\le2p\le p^2\le p^t$, so $\mathrm{Cov}$ is defined. Correct.
- $m_s=H-s$ runs over $p+\rho,\dots,1$, and $m_s=p$ iff $s=\rho+1$. Correct.
- *Valuations.* For $1\le m\le p+\rho<2p$ and $m\ne p$, the number $m$ is prime to $p$. Since $X\equiv0\pmod{p^t}$, $X-m$ is a unit. Next, $X-p=p(X/p-1)$ with $X/p\equiv0\pmod{p^{t-1}}$ and $t\ge2$, so its valuation is exactly 1. Hence $y_0,\dots,y_\rho$ are units, and the $p$ elements $y_{\rho+1},\dots,y_{H-1}$ have valuation exactly 1. Correct. This is where $t\ge2$ is needed; at $t=1$, $X-p$ can have valuation $\ge2$.
- *Units mod $p$.* $y_i\equiv\prod_{s\le i}(s-H)\equiv(-1)^i\rho!/(\rho-i)!$, and with $w=\rho-i$ this is $(-1)^\rho\rho!\cdot(-1)^w/w!$. This is Lemma 10.11(d). The set $\{(-1)^w/w!:w\le\rho\}$ covers $\mathbb Z/p$ iff $\rho\ge\rho_0$: by minimality of $\rho_0$ in one direction, and because adding elements only enlarges $\Sigma$ in the other. Correct.
- *The valuation-1 layer.* $y_{\rho+1+j}=y_{\rho+1}\prod_{m=p-j}^{p-1}(X-m)$, because the factors $s=\rho+2,\dots,\rho+1+j$ have $m_s=p-1,\dots,p-j$. Modulo $p^t$, the product is $(-1)^j(p-1)!/(p-1-j)!$. With $y_{\rho+1}=pU_0$ ($U_0$ a unit), $y_{\rho+1+j}/p\equiv U_0(p-1)!\,(-1)^u/u!\pmod{p^t}$, where $u=p-1-j$ and $(-1)^j=(-1)^u$ because $p-1$ is even. As $j$ runs over $0..p-1$, $u$ runs over all of $0..p-1$, so the layer divided by $p$ is $U\cdot E_p$ modulo $p^t$. Since $t\le L_p$ and $U$ is a unit, its subset sums cover $\mathbb Z/p^t$. Correct.
- *Combination.* Choose $S$ among the units to fix $x$ mod $p$, then $T$ in the layer with $\sum_Ty_i\equiv pz\pmod{p^{t+1}}$, since $\sum_Ty_i/p\equiv z\pmod{p^t}$. Correct.
- *Converse.* If $\rho<\rho_0$, the units miss a class mod $p$ and every other element is $\equiv0\pmod p$. This is Lemma 10.11(c) with $k=1\le t$. Correct.
- *Class independence.* Only $X\equiv0\pmod{p^t}$ was used, so coverage holds or fails for every $K'$ at once. My numerical check also found the outcome identical for all classes (§6.3).
- *Remarks.* The ranges $36\le H\le58$ ($p=29$) and $38\le H\le62$ ($p=31$) for $2\le t\le5$ are right. So is "no chain is improved": the minimal $H_t$ for $t\le5$ are below $p+1+\rho_0$. The identification of the case $t=L_p+1$, $H=2p$ with the round-1 two-block window of level $L_p$ is also right.

The label [proved] is correct, with "checked by the track and by this check only". The report is right that the lemma came after the $(29,5,36)$ outcome: `scanall_p29_t5.log` ended at 06:16:51 and `lemma_check.log` started at 06:56:58. It is an explanation after the fact.

## 8. Registered predictions (R7; logs `predictions_check.log`, `pred_recount.log`, `predict_extra_rows.log`)

**Recount.** `pred_recount.py` has its own parser and its own classification rules, and gives exactly the report's numbers. Of 120 rows: 63 confirmed, 1 falsified ($(29,5,36)$), 11 known in advance, 20 refuted by proofs, 4 MIXED, 21 not run. `pred_eval.py`, re-run, reproduces the archived `PREDICTIONS_evaluation.txt` byte for byte (apart from its two header lines). I checked the list of near-threshold cases in §5.2 of the report against the registration file and the scan logs, and the $\nu$ values for $(29,5,36)$ ($R^*=2^{29}/29^5=26.17$; $\nu=1.296$ for $n=1$ and $1.112$ for $n=28$).

**Timing of the registration.** The file time 06:12:37 agrees with its internal stamp 06:12:36. No R3C log at $p=29$ or $31$ starts before it. As the report says, the stamp is not anchored outside the machine before commit `40fc251` (15:10 UTC).

**Findings to fix:**
1. **The registration's headline prediction is not confirmed at $(29,2)$.** The registration file says, under "GENUINE PREDICTIONS": "minimal uniform $H_t$ for $p=29,31$, $t=2..6$, = 'predicted minimal H' below", and that value is defined as the first HOLD-band $H$. For $(29,2)$ the registered minimal $H$ is **14**, but the observed minimal $H_2(29)$ is **13**: $H=13$ is in the MIXED band and holds. The other nine registered minimal values are right ($19,24,29,40$ at $p=29$; $14,19,25,30,41$ at $p=31$). The report's per-row accounting treats $H=13$ as "no prediction" and never mentions this. It should add one sentence, for example: "Of the ten registered minimal-$H_t$ values, nine are right; at $(29,2)$ the registered value 14 is wrong, because the MIXED-band $H=13$ holds." Also, at $(29,5)$ the registered value 29 was known in advance ($L_{29}=5$).
2. **"Reproduced exactly by `predict.py`."** The two `predict.py` commands of §5.1 reproduce the registration body except for its last four `extra:` lines. `predict.py` never prints those lines. They are reproduced exactly by `predict.nu_of` with $(p,t,H,n)=(29,7,58,28),(31,7,62,30),(29,7,44,1),(29,7,45,1)$ (`predict_extra_rows.log`). The report should say so.
3. **"The first run whose outcome it predicts is `P29_t7_H45_A_K1.log` (06:14:49)."** In fact `validate_AC.log` started earlier, at 06:13:29. It computes several registered rows with `bigbrute.py`, A and C: $(29,2,13)$, $(29,2,14)$, $(29,3,18)$, $(29,3,19)$, $(31,2,13)$, $(31,2,14)$, $(31,3,19)$. That is still after the registration, so the conclusion stands, but the sentence should be corrected.
4. *(Suggestion.)* The headline "63 confirmed and 1 falsified out of 64 genuine tests" is arithmetically right, but 35 of the 63 are uniform FAIL-band rows with $\nu\le0.89$, far below the threshold. Near the thresholds ($\nu\in[1.0,1.17)$ on the FAIL side, $\nu\in(1.47,2.4]$ on the HOLD side), the record is:
   - FAIL side, 6 tests: 5 confirmed and 1 falsified;
   - HOLD side, 7 tests: all confirmed.

   The report gives this breakdown in §5.2. The headline should point to it.

## 9. R8, R9 and other statements

- **R8.** The $p=31$ scan logs are audited in §2, and both chain checkers give CHAIN OK at $917\,087\,130=v_{31}((31^7-1)!)$. The comparison with round 1's $917\,087\,135$ and the cost estimate of §6.1 ($(31/29)^7=1.595$; two bitsets of $31^7$ bits are 6.9 GB; about 11 CPU-hours) are right. **Confirmed.**
- **R9.** `T19_t7_H45_K20_{A,D}.log` say what the report says: A 292 s wall, 194 s user; D 249 s wall, 161 s user; both covered. In `T5_t5_H39_D_48cls.log`, D covers 4 classes in 130–147 s each and the log has no end line. The A and C lines of `timing_early.log` are a terminal capture, as the report says. The report correctly labels all of this timing only. **Confirmed.**
- **The $H=44$ negative** (§5.4 of the report). The three logs in `p29_t7_H44/` say exactly what §5.4 says:
  - D: $K''=1,2$ covered, $K''=3$ missing 2 (766 s for $K''=1..3$);
  - A: the same two residues at $K''=3$ (506 s);
  - C: `miss=2 UNCOVERED` (555 s).

  The working-tree copy of the C log is complete; the copy committed in `024b87e` is not. The residues lie in the classes 11 and 23 mod 29, as stated.
- **Provenance statements** (cut-off, resumed queues, the half-committed logs). They are consistent with the log times, with `/tmp/r3_R3C/queue_*.out` and with git history. The A logs of $K''=15$ and $27$ in the working tree are complete, and this check re-ran $K''=27$ with A and $K''=15$ with C.
- **The Conjecture 10.25 remark** (§5.4, [heuristic]). I did not recompute the $m_1(r)$ profiles. The residue classes mod $p$ of the missed residues ($11,23$; $20,26$; $6,14$) agree with the dumps.

## 10. Required and suggested changes to the track report

Required:
1. **Independence of D** (headline, §0 R6, §4.2, and wherever the note cites it). Replace "share no code beyond four generic boilerplate lines" and "No algorithmic code is shared with A" by an accurate statement (wording suggested in §5.2): D was written with A, B and C at hand. After identifier renaming it shares A's driver, A's $\Sigma(L)$ doubling loop and shift-OR expression, and B's counting-sort block. Its element arithmetic, cyclic kernel and list and complement phases are new. The overlap is comparable to that between A and C.
2. **The registered minimal-$H_t$ prediction at $(29,2)$** was wrong (14 registered, 13 observed). Say so in §5 and in the headline's prediction sentence (§8 item 1).
3. **§5.1 "reproduced exactly by `predict.py`"**: add that the four `extra:` lines come from `predict.nu_of` (§8 item 2).
4. **§5.1 "first run whose outcome it predicts"**: this was `validate_AC.log` at 06:13:29, not the depth-7 run at 06:14:49 (§8 item 3).

Suggested:
5. Run C on the remaining 26 depth-7 positions (about 4.3 CPU-hours). R1 would then also rest on the pair A+C, accepted in round 2, and on three programs everywhere. This check ran C on $K''=15,21$ (both covered).
6. Update the docstring of `chain_c_r3.py`: it lists three changes but omits the two parsing changes and the exception syntax.
7. In the headline, refer to the near-threshold breakdown of §5.2 when quoting "63 of 64" (§8 item 4).

None of these changes touches the bound $f(1,29)\ge17\,865\,943\,312$, its status [computer-assisted], or any other status label of the report.

## 11. Commands and logs

All commands run from the repository root. Logs are in `data/round3/check_R3C/`. Each log starts with its command line, the sha256 of the binaries, the start time and the memory cap, and ends with wall/user/sys time, the exit status and the end time (`run_logged.sh`).

```sh
B=<scratch>/chkR3C_bin                    # fresh builds, hashes in every log
clang -O3 -march=native -o $B/fibcov  code/round2/R3/src/fibcov.c                 # A  4b551a73...
clang -O3 -march=native -o $B/fibcov2 code/round2/R3/src/fibcov2.c                # B  f3504700...
clang -O3 -march=native -o $B/covchk  code/round2/review/computation/covchk.c     # C  0ceec1e3...
clang -O3 -march=native -o $B/covfast code/round3/R3C/covfast.c -lgmp             # D  7596867116ee...
python3 code/round3/check_R3C/logaudit.py      > logaudit.log      # section 2
python3 code/round3/check_R3C/contradictions.py > contradictions.log
python3 code/round3/check_R3C/simcheck.py      > simcheck.log       # section 5.2
BIN=$B sh code/round3/check_R3C/batch_depth7.sh   # section 3: A K''=4,27 | C K''=15,21 (parallel), then D K''=4,27
sh code/round3/check_R3C/batch_light.sh           # sections 4, 6, 8: chains_rerun.log, predictions_check.log, indep_*.log
python3 code/round3/check_R3C/pred_recount.py  > pred_recount.log   # section 8
```

| log | content | wall |
|---|---|---|
| `X_A_p29_t7_H45_K{4,27}.log` | A at depth 7 | 501 s, 484 s |
| `X_C_p29_t7_H45_K{15,21}.log` | C at depth 7 | 603 s, 576 s |
| `X_D_p29_t7_H45_K{4,27}.log` | D at depth 7 | 242 s, 245 s |
| `chains_rerun.log` | both chain checkers, all specs, new controls, round-2 re-validation | < 10 s |
| `predictions_check.log`, `pred_recount.log`, `predict_extra_rows.log` | registration regenerated, pred_eval re-run, own recount | < 10 s |
| `indep_{rho0,selftest,scans,negatives,lemma,lemma29}.log` | own brute force | 0.5 s, 10 s, 1.3 s, 73 s, 15 s, 1222 s |
| `logaudit.log`, `contradictions.log`, `simcheck.log` | audits | < 2 s |

