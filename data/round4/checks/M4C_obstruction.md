# Obstruction-and-scope check of round-4 track M4C (Theorem M: $\mu(K_p)>0$ for $11\le p\le97$)

Date: 2026-10-14. Lens: OBSTRUCTIONS AND SCOPE. Made by the `verify_C_obstruction` track of round 4. I did not write any of the work checked here.

- **Checked:** `data/round4/reports/M4C.md`, the whole report, with most care on the headline, §§5–9 (Theorem M), §8 ("How the obstructions of the brief are respected") and §§9, 12–13 (scope). I read `code/round4/M4C/assemble.py` and `early_phase.py`, and the logs `assemble.log`, `check_assemble.log` and `qtable.log`.
- **Obstructions re-read:**
  - in note.md: Theorem 3.6, Theorem 3.5 (with $\Phi_p$), Theorem 3.10, Corollary 10.20, Propositions 11.12, 11.15, 11.23 and 11.24, and Theorem 11.14;
  - in `data/round3/reports/R3M.md`: §5 (Lemma C1, Proposition C2, Theorem C3, Lemmas C4–C5, Remark C6, Proposition N3) and §6;
  - the round-4 brief.
- **For comparison:** `data/round4/reports/M4A.md` (Lemma Q constants, Corollary M′) and `data/round4/checks/M4A_obstruction.md` (Proposition O1, Remark O2).
- **Code:** `code/round4/verify_C_obstruction/` (`qfourier.py`, `propW_check.py`, `reassemble.py`, `phase1_pointwise.py`, `context_checks.py`, `compare_logs.py`, `run.sh`).
  - No M4C code is imported or called.
  - `reassemble.py` follows the report's text (§§6–7). I had read `assemble.py` before writing it, so it is a third implementation by a different author, but not a blind one.
- **Logs:** `data/round4/verify_C_obstruction/*.log`. Each run starts with `### command:` and ends with `### wall:`.
- **Budget:** about 4 core-minutes in total, at `nice -n 10`. The longest job took 117 s.

**The claim checked (Theorem M, status [computer-assisted]).**
- For every prime $11\le p\le97$, $\mu(K_p\cap p^3\mathbb Z_p)\ge c_p\,p^{-3}$.
- The constants are $c_{11}\ge1.25\cdot10^{-4}$ (also printed as $1.254\cdot10^{-4}$), $c_{13}\ge0.572$, and $c_p\ge0.69$ for $17\le p\le97$, with per-$p$ values in §7.3.
- The proof applies R3M Theorem C3 (note Theorem 11.14) with $j=0$, atom $A=p^3\mathbb Z_p$, $n_0=3p$ and $n_k=b_kp$.
- It has a deterministic phase 1 (blocks $<p^2$, Prop P1), an explicit phase 2 (Lemmas L, T, T′), and a far tail with a hand-proved remainder beyond $b=10^{60}$.

## Headline

**Verdict: confirmed-with-fixes.**

Theorem M respects every listed obstruction. For each one I can name the step of the proof that gets past it (§2).

**Every hypothesis of C3 is met exactly** (§3):
- $n_0=3p\ge2p$;
- $A$ is an atom of $\mathcal G_0$;
- $A$ is admissible, with $D_0=1\le m_0-M_{4p}=2$, $M_{4p}=1<3$, and $Z^0_{3p}\ge1$ on all of $A$;
- the thresholds are deterministic, and $1+\chi^2_{W_0}(A)=q_1(p)$.

The slope-0 path of Proposition W, including the special block at the Wilson prime $13$, and the admissibility data were re-verified for all 22 primes $7\le p\le97$ with my own code (`propW_check.log`).

**Every number of the scope table reproduces.** A third implementation (`reassemble.py`; $q$-constants by a different method, `qfourier.py`) reproduces, for all 21 primes:
- the phase-1 schedule (identical at all 21 primes);
- every phase-2 window printed in both logs: all 81 tuples $(\ell,b_{\ell-1},b_\ell,b_{\ell+1},s_\ell,N_W,N,I)$ agree (`compare_logs.log`);
- $\Pi_A$ and $\delta_A$ to 7 significant digits or better (limited by the 7-digit $q$-values I pass in);
- $c_p$ and the $\mu(K_p)$ bounds of §7.3, to all printed digits.

Every $c_p$ printed in §7.3 is a valid (rounded-down) lower bound.

**Fixes.** All of them are to M4C's wording and labels. None changes a number or the conclusion.
- **(F1) "with no truncation" is wrong.**
  - The headline says FE is verified "with no truncation". The proof truncates at deep gates through the events $G_\ell\subseteq G'_\ell$ (Lemma L, Lemma T).
  - The truncation is necessary. Without it, $\mathbb E_A[\varepsilon_{k_0+1}]=+\infty$ at every listed $p$ (Proposition O1′ below, proved).
  - It is also the dominant cost. The truncation terms $\sum\mu_A(G_k^c)$ are $23\%$ of $\delta_A$ at $p=11$, $69\%$ at $p=13$, and at least $99.6\%$ for every $17\le p\le97$ (§2.3).
- **(F2) Inconsistent label for Corollary M′.**
  - §9.2 labels Corollary M′ (all $p\ge p_0$) **[heuristic, not proved]**.
  - The headline (item 2) calls it "a precise reduction", and the §0 table calls it a "reduction".
  - Both should say: heuristic, conditional on AC($p$) *and* on an unwritten $p$-uniform analysis of the schedule.
- **(F3) "Makes Remark C6 rigorous" needs a qualifier.**
  - Proposition H′ is a statement about averages over balls with a **frozen gate pattern** and radius $r\le D/2$.
  - It is not R3M's cylinder-level reduction to "boundary terms $O(c_{n_\ell}/c_{n_{\ell-1}})$". On a cylinder where a gate depth is random, that boundary term already has infinite mean (Proposition O1′).
  - Nor is it (S) uniformly on cylinders, which is impossible (M4A_obstruction, Remark O2).
- **(F4) Make the obstruction paragraph of §8 precise.** The barrier-lemma bullet should state the actual mechanism (§2.4).
  - Every deterministic bound in the proof grows with the window length or the gate depth, as Theorem 3.10 and Proposition 11.23 require:
    - the phase-1 thresholds $q_1^{n_1}q_2^{n_2}-1$;
    - Lemma Q's 1D factors $q_1$, $q_2$ and $p^{d-3}q_3$;
    - the block-0 factor $p^{e_0}$.
  - The decay comes only from Hensel averaging over balls of radius $\le D/2$ (Lemma H2), combined with the 2D factor $q_2/p$.
  - The Prop 11.15(b) bullet should cite the necessity of $G'_\ell$ (Proposition O1′).
- **(F5) Record the outside reproduction.** §8 item 12 and §13 item 5 say that no program by another author exists. This check provides one, together with an independent evaluation of $q_1,q_2,q_3$ by a different method. It is still not a human check.
- **(F6) (optional) Positive definiteness.**
  - The law of any lazy-signed sum is positive definite: its characteristic function is $\prod\cos^2\ge0$.
  - So the maxima defining $q_2$ and $q_3$, not only $q_1$, are attained at $0$. This gives the closed formula $q_k(p)=\sum_{\xi\bmod p^k}\prod_{r<p}\cos^2(\pi\xi F_r/p^k)$.
  - It is a simplification (and a fast route to the constants for larger $p$), not a correction.

## 1. Results of this check

| # | statement | status | evidence |
|---|---|---|---|
| S1 | $q_1-1$, $q_2-1$ and $q_3-1$ for all 23 primes $5\le p\le97$ agree with M4C §4.3 and `qtable.log` to every printed digit. At $p=7,11,13$ they also agree with M4A's independently computed $q_1,q_2,q_3$ | computer-assisted (Fourier formula, float64, relative accuracy about $10^{-12}$) | `qfourier.log` |
| S2 | Proposition W and admissibility: for all primes $7\le p\le97$ the path is alive at $3p$ with $V_{3p}=3$ and has slope $0$, with $S'_e\equiv-w_p\pmod p$. At $p=13$ the block $\{0,p-1\}$ fails and $\{0,1,2,3,4,8,9\}$ works ($\lambda_e-k_e\equiv12$). Also $D_0=1$, $M_{4p}=1$ and $m_0=3$ | computer-assisted (exact integers; reduction to $x=0$ plus 20 random $x\in A$ at precision $p^{12}$) | `propW_check.log` |
| S3 | Independent reassembly of Theorem M for all 21 primes: the schedule, the 81 explicit phase-2 windows printed by both programs (0 mismatches), $\Pi_A$, $\delta_A$ and $c_p$ agree with `assemble.log` and `check_assemble.log` | computer-assisted | `reassemble.log`, `compare_logs.log` |
| **O1′** | for every listed $p$, the first phase-2 window $\ell^*=k_0+1$ has its unique random-depth gate ($j=p^2$) in its second half, and the untruncated $\mathbb E_A[\varepsilon_{\ell^*}]=+\infty$ | **proved** (two lines; the window data are exact integers) | §2.3, `reassemble.log` |
| T1 | phase 1 at $p=7,11,13$: the exact pointwise $\varepsilon$ (DP over all residues) satisfies Prop P1, at $\le1.4\%$ of $\bar\varepsilon$. The true $\varepsilon$ decreases overall along the windows, while the deterministic $\bar\varepsilon$ does not decrease | computer-assisted (float64 DP) | `phase1_pointwise.log` |
| T2 | Prop 11.12 floor: $\chi^2_{W_0}(A)=q_1-1\ge(p-1)4^{-p}$ for all listed $p$ | computer-assisted | `context_checks.log` |
| T3 | $0\notin\Phi_p$ for all $p\le31$. Round-1 densities restricted to the classes with $g\not\equiv0$ are $0.96$–$0.99$ at $p=11,\dots,23$ | computer-assisted | `context_checks.log` |
| T4 | $p=7$ is correctly excluded: the greedy phase 1 ends with $N_W=4<8\le2s+2$, so (T2) fails | computer-assisted | `scope_p7.log` |

## 2. Obstruction by obstruction

### 2.1 Theorem 3.6 ($K_p$ has empty interior; no residue-class criterion)

- **What it forbids.** No property of $x\bmod p^{k_0}$ implies $x\in K_p$. By Theorem 3.6(a), $A=p^3\mathbb Z_p$ contains infinitely many natural $a$ with $f(a,p)<\infty$, and $K_p$ is closed, so $A\setminus K_p$ is a nonempty open set.
- **How Theorem M respects it.**
  - The only properties of $A$ used pointwise are these:
    - $Z^0_{3p}\ge1$, which depends on $x\bmod p^3$ only;
    - the deterministic gate depths for blocks $<p^2$ (Lemma 5.1);
    - Prop P1's bounds on $\varepsilon_k$ and the linear regime in phase 1.
  - All of these are statements about the *window conditions* of C3, not about membership in $K_p$.
  - Membership is obtained only on the Paley–Zygmund event $\{Y>0\}$ of C3. Its conditional measure is bounded below by $c_p\le1/\Pi_A\le1/q_1(p)<1$, never by $1$.
  - So the claim is a fat-Cantor-set statement inside $A$, consistent with Theorem 3.6.
- **Q3 is untouched.** No natural number is placed in $K_p$, and none is claimed.
- **Verdict:** evaded correctly.

### 2.2 Proposition 11.12 (per-window Cauchy–Schwarz fails, $\chi^2_W\ge(p-1)4^{-p}$)

- **How Theorem M respects it.** C3 pays the single-window $\chi^2$ once, as $1+\chi^2_{W_0}=q_1(p)$, which is exact on $A$. The window $W_0=[3p,4p)$ has $D_0=1$ and elements $\equiv r!\pmod p$. Every later window pays only the composite band mass $\varepsilon_\ell$ (R3M Prop C2), which does not contain the mod-$p$ shell of a single window.
- **Check T2.** $q_1-1\ge(p-1)4^{-p}$ holds at every listed $p$, as it must. For example, at $p=97$ it is $2.1\cdot10^{-43}$ against $3.8\cdot10^{-57}$. Proposition 11.12 is therefore paid once, not per window.
- **Verdict:** evaded correctly, by R3M's Theorem C3, which M4C uses unchanged.

### 2.3 Proposition 11.15(b) (infinite annealed mean): the truncation is necessary

**Phase 1 needs no expectation.**
- All composite windows of phase 1 lie in blocks $\le b_{k_0+1}\le p^2-1$, where every gate depth is deterministic on $A$ (Lemma 5.1).
- Prop P1 bounds $\varepsilon_k$ pointwise on all of $A$, so phase 1 contributes only to $\Pi_A$ and nothing to $\delta_A$.
- Check T1 confirms the bound exactly on the first windows at $p=7,11,13$. The ratio of the true $\varepsilon$ to $\bar\varepsilon$ is at most $0.014$, with no failure.

**Phase 2 and the far tail need the truncation.** Proposition H′ and Lemma T are applied to $\mathbb E_A[\varepsilon_\ell\mathbf 1_{G'_\ell}]$, where $G'_\ell$ caps every gate depth of the composite at $s_\ell$. This is not optional, as the next proposition shows.

**Proposition O1′ (the untruncated mean is infinite at the first phase-2 window) [proved].** Let $p$ be any of the 21 primes and $\ell^*=k_0+1$. With the exact schedule data of `reassemble.log`:
- the composite window $(b_{\ell^*-1},b_{\ell^*},b_{\ell^*+1}]$ contains exactly one multiple of $p^2$, namely $j=p^2$, and it lies in the second half $(b_{\ell^*},b_{\ell^*+1}]$;
- for example, the window is $(105,120,144]$ at $p=11$, $(214,288,407]$ at $p=17$ and $(7984,9408,11760]$ at $p=97$.

Then $\mathbb E_A[\varepsilon_{\ell^*}]=+\infty$, where $\varepsilon_{\ell^*}=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$ is taken with no truncation and no linear-regime restriction.

*Proof.*
1. *Valuations.* By Lemma 5.1, every gate $j\ne p^2$ of the composite has a deterministic depth ($1+v_p(j)\le2$). The gate $j=p^2$ has depth $v(x+p^3)=3+t$, with $t:=v(\xi'+1)$, where $x=p^3\xi'$. Hence the following are constant on $A$:
   - $D=\sum_{b_{\ell^*-1}<j\le b_{\ell^*}}v(x+jp)$;
   - $K_{\rm det}:=K-t$.
2. *Law of $t$.* Under $\mu_A$, $\xi'$ is Haar-distributed, so $\mu_A(t=u)=(1-\tfrac1p)p^{-u}$ for $u\ge0$.
3. *Lower bound.* The signed vector $\delta=0$ has probability $2^{-Np}$ and gives $T_\delta=0$. So $\mathrm{Coll}_K\ge2^{-Np}$. Also $\mathrm{Coll}_D\le1$. Hence $\varepsilon\ge2^{-Np}p^{K_{\rm det}+t}-p^D$ pointwise.
4. *Conclusion.* Since $\varepsilon\ge0$ everywhere (it is an $L^2$ band mass, M4C §8 item 13),
   $$\mathbb E_A[\varepsilon_{\ell^*}]\ \ge\ \sum_{u\ge0}\big(1-\tfrac1p\big)p^{-u}\big(2^{-Np}p^{K_{\rm det}+u}-p^D\big)^+=+\infty .\qquad∎$$

*Remarks.*
- The divergence lives at absurd depths. The term in step 3 is positive only once $t\ge Np\log_p2-(K_{\rm det}-D)$, i.e. $t\ge97$ at $p=11$, $t\ge127$ at $p=13$, and $t\ge53119$ at $p=97$. Each divergent term is of size about $2^{-Np}p^{K_{\rm det}}$. The infinite mean nevertheless rules out Markov's inequality on the untruncated mean.
- The divergent term is the $\delta=0$ term, i.e. the normaliser ratio $c_{N'}/c_n=2^{-(N'-n)}p^{K}$. It is the first term of R3M's Lemma C5, and the first term $c_{L+L'}$ of M4C's own Proposition H′.
  - It comes from $\mathbb E[p^{v(y)}]=\infty$ for Haar-random $y$, not from the double root at $-2$ of note Proposition 11.15(b) (that mechanism gives the same divergence, through the path $\delta_{i-2}=\delta_{i-1}=\delta_i$).
  - So the "boundary terms of size $O(c_{n_\ell}/c_{n_{\ell-1}})$" of R3M's Remark C6 have infinite mean themselves on such windows. This is the reason for (F3).
- The same argument applies to every window whose second half contains a multiple of $p^2$: condition on that gate being deeper than $\max v(u_1-u_2)$ over the other $p^2$-multiples $u_1$ of the window, and then $D$ is bounded. Every far-tail window qualifies. So *every* phase-2 or far-tail window of this kind needs the cap.
- Two truncations would each suffice: M4C's $G'_\ell$, or the linear-regime clause of C3's own stopping time, which bounds $t$ on $\{\tau>\ell^*\}$. M4C uses $G_\ell\subseteq\mathrm{lin}_\ell$ (Lemma L(b)) and $G_\ell\subseteq G'_\ell$.

**The truncation is also the main cost** (from `reassemble.log`, the "delta breakdown" lines):

| $p$ | $\sum_k\mu_A(G_k^c)$ | $\sum_k\sqrt{\mathfrak B'_k}$ | share of $\delta_A$ from truncation |
|---|---|---|---|
| 11 | 0.02032 | 0.06711 | 23% |
| 13 | 0.01507 | 0.00692 | 69% |
| 17 | 0.009387 | $2\cdot10^{-20}$ | 100% |
| 19 | 0.009379 | $3.4\cdot10^{-5}$ | 99.6% |
| 23–97 | 0.0045–0.0283 | $\le6.3\cdot10^{-9}$ | $\ge99.9999\%$ |

For $p\ge17$, $c_p\approx(1-\sqrt{\delta_A})^2$ is set almost entirely by the deep-gate cap. This matches M4C's own reading in §§7.3 and 9.1, and it is irreconcilable with the headline's "no truncation".

**Verdict:** evaded correctly, by the truncation $G'_\ell$, whose cost is summable (Lemma L(a)) and explicitly added to $\delta_A$. Fix (F1) applies.

### 2.4 Barrier lemmas (Theorem 3.10; Proposition 11.23)

**What they forbid.** A *deterministic* covering bound or $L^2$ bound for a run ending at a gate of level $j$ that uses the valuations and only $c$ digits of the unit parts cannot be good once $j\ge c+1$. For $L^2$ the bound is $\ge\frac{p-1}2p^{j-c-1}-1$. A bound uniform in depth therefore needs unboundedly many digits.

**The deterministic bounds in Theorem M, and why they comply.**
- *Phase-1 thresholds* $\bar\varepsilon_k=q_1^{n_1}q_2^{n_2}-1$.
  - These use 1 digit at depth-1 gates and 2 digits at depth-2 gates; the levels are $j\le2$, and $c=2$ makes the barrier vacuous.
  - They do not decay; they grow, not monotonically, along the windows. At $p=11$ they run $2.9\cdot10^{-3},4.3\cdot10^{-3},\dots,0.81,0.62$; at $p=13$ they rise from $4.4\cdot10^{-5}$ to $5.1\cdot10^{-2}$ (`reassemble.log`).
  - They are used only for finitely many windows, so their product is finite.
- *Lemma Q's 1D block factors.*
  - The factors are $q_1$, $q_2$, and $p^{d-3}q_3$ for a gate of depth $d\ge3$, using 3 digits: the law mod $p^3$ of the falling factorials $F_r$, fixed by the unit $w\equiv-1\pmod{p^2}$.
  - The factor $p^{d-3}q_3$ grows like $p^d$, which is exactly the growth Proposition 11.23 forces with $c=3$.
  - The block-0 factor $p^{e_0}$ likewise grows with the depth of the first gate.
- *How deep gates are paid for.* No deterministic bound is ever required to be small at a deep gate. Gates deeper than $s_\ell$ are removed by $G'_\ell$, at probability cost $\lfloor b_{\ell+1}/p^2\rfloor p^{-(s_\ell-2)}$.

**Where the decay comes from.**
- *Averaging.* Lemma H2 averages over a ball $B=z+p^{M+1}\mathbb Z_p$ with a frozen gate pattern, i.e. it integrates over all digits of $x$ from level $M+1\le s+1$ upward. It requires $D\ge2r$, so the ball stays below half the jump, and the number of averaged digits that matter (up to level $K$) grows without bound along the schedule.
  - This is the loophole named in the brief: for Haar-random $x$, the unit parts are polynomial images of the digits of $x$, and the proof averages over them instead of knowing them.
  - So the barrier's demand for unboundedly many digits is met by averaging, not by any statement about Morita's $\Gamma_p$.
- *The 2D factor.* After averaging, only signed paths of slope $\ge\lceil D/2\rceil-V_j$ remain (Proposition H′). For these, Lemma Q gives a factor $q_2/p<1$ for each depth-1 block below level $\lceil D/2\rceil$.
  - The second digit is the derivative digit $B=\sum\delta_rr!H_r$, i.e. the first-order harmonic-number term.
  - This is the same first-order (harmonic-number) information that note §6 (T3) identifies, via Theorem 3.10, as necessary for any gate-crossing step.

**Check T1 (phase contrast in phase 1).** At $p=7$ the exact pointwise $\varepsilon$ on $A$ is $1.0\cdot10^{-4}$, $2.0\cdot10^{-3}$, $3.3\cdot10^{-4}$, $1.7\cdot10^{-5}$ and $3.0\cdot10^{-6}$ for $k=1,\dots,5$, against $\bar\varepsilon=0.029$, $0.145$, $0.161$, $0.073$ and $0.194$ (similarly at $p=11,13$).
- The true band mass decays overall.
- The deterministic, supremum-based bound does not.
- This is exactly what Proposition 11.23 and Corollary 10.20/Proposition 11.24 predict for bounds of that type.

**Verdict:** evaded correctly. There is no barrier-type input (§2.6). Fix (F4) asks only that §8 state this mechanism instead of "uniformly in the position".

### 2.5 Corollary 10.20 and Proposition 11.24 (supremum-type transfer bounds give no decay)

- **Where a supremum appears.** The chain rule in Lemmas P and Q takes a maximum over the residue prescribed by the lower blocks, at every block.
  - For the value-only event the per-block normalised factor is $q_1\ge1$. In fact $q_1>1$ strictly, since $q_1-1$ is a sum of positive terms (F6).
  - So Prop P1 cannot decay, as Corollary 10.20 and Proposition 11.24 require, and it does not (§2.4).
- **Where the decay comes from.** It comes from the joint value/derivative event, with factor $q_2/p<1$: $0.101$ at $p=11$, $0.0775$ at $p=13$, and $\approx1/p$ beyond.
  - That event becomes relevant only after Proposition H′, whose ball average removes all low-slope Hensel balls.
  - This is the "decorrelation" that Corollary 10.20 says any decaying bound must supply, here realised one window deep.
  - The supremum in Lemma Q is over the 2D block statistic $\Phi$, not over the window's own profile $H_W$. Corollary 10.20 and Proposition 11.24 do not constrain it.
- **Verdict:** evaded correctly.

### 2.6 Does the argument secretly assume a deterministic covering or equidistribution statement?

**No.** Here is the full inventory of what Theorem M rests on:

| input | kind | covering or equidistribution content |
|---|---|---|
| note Thm 11.14 = R3M C3 (with Props 11.10, 11.11, 11.13, Prop 1.2, (F2)) | martingale, $L^2$ two-window inequality, Paley–Zygmund | none |
| Lemma H2, Prop H′ | Hensel's lemma under Haar measure on a ball | none; this is the averaging over the digits of $x$ |
| Lemmas P, Q | chain rule with *maximal-atom* constants $q_1,q_2,q_3$ of fixed finite random variables | anti-concentration only; nothing says that subset sums cover |
| Lemma 5.1, Prop W | valuations on $A$; Wilson's theorem; Cauchy–Davenport mod $p$ for a single block of $p$ nonzero residues | only mod-$p$ covering of one block, which is classical and never iterated through gates |
| Prop P1, Lemmas L, T, T′ | integer bookkeeping; union bound; Markov | none |

The constants $q_1,q_2,q_3$ are three numbers per prime: the computed maximal atoms of one block's law mod $p$, $p^2$ and $p^3$. Their closeness to 1 for $p\ge13$ is an observed fact (AC($p$), §4), used only at the 21 listed primes. Nothing of Morita's $\Gamma_p$ beyond 3 digits is used, consistent with the absence of any claim on Q3.

## 3. The hypotheses of C3, checked one by one

| C3 hypothesis (R3M §5, note Thm 11.14) | M4C | check |
|---|---|---|
| deterministic times $2p\le n_0<n_1<\cdots$ | $n_k=b_kp$, with $b$ fixed by $p$ alone (greedy, $s$-rule, (T1), the $\gamma$ rule, the $\frac54$ rule); $b_0=3$ | reproduced (S3); strictly increasing (asserted) |
| $A$ an atom of $\mathcal G_0$ | $m_0=V_{3p}=3$ on $A$, so the atom is $x+p^3\mathbb Z_p=A$ | S2 |
| admissible: $D_0\le m_0-M_{n_1}$, $M_{n_1}<m_0$, $Z^0_{n_0}\ne0$ on $A$ | $D_0=1$, $M_{4p}=1$, $m_0=3$; Prop W path | S2: all 22 primes, all of $A$ (reduction to $x=0$: $S_e\in\mathbb Z[X]$, $x\equiv0\bmod p^3$) |
| $(\bar\varepsilon_\ell)$ nonnegative, $\Pi<\infty$ | phase 1: $q_1^{n_1}q_2^{n_2}-1$; then $\sqrt{\mathfrak B'_k}$; tail $<10^{-1000}$ | S3 |
| $\Pi_A=(1+\chi^2_j(A))\Pi$ | $1+\chi^2_{W_0}=p\,\mathrm{Coll}_1=q_1$ (law of $\sum\delta_rr!$ mod $p$; maximum at 0) | S1, F6 |
| FE: $\delta_A=\mu_A(\tau_0<\infty)<1/\Pi_A$, with $\tau_0$ for lin **and** $\varepsilon_\ell\le\bar\varepsilon_\ell$ | union bound $B_\ell^c\subseteq G_\ell^c\cup(G'_\ell\cap\{\varepsilon_\ell>\bar\varepsilon_\ell\})$; Markov on $G'_\ell$ | $\Pi_A\delta_A\le0.92833$ at $p=11$, $\le0.0269$ at $p=13$, $\le0.029$ for $p\ge17$ (S3) |
| the C3 conclusion is monotone in $(\Pi_A,\delta_A)$ | $(1-\sqrt{\Pi\delta})^2/\Pi$ decreases in both, so upper bounds give a valid lower bound | yes |

Two consistency points:
- C3's $\varepsilon_\ell$ equals the Coll formula only under the linear-regime condition. Every bound is applied on $G'_\ell$, and the complement of $G_\ell$ is charged separately, so this is sound.
- The far tail beyond $b=10^{60}$ is a hand argument (§7.2). I re-derived its two inputs at the worst prime $p=11$. The $s$-rule gives $s_k\le4+\log_p\frac{2b}{p^2\eta}+(k-k_0)\log_p2\approx1.76\ln b+O(1)$, well below the stated $3+10\ln b$. The exponent of Lemma T′ is linear in $b$, with slope $-0.2267$ (re-derived by hand from §7.1; `assemble.log` prints $-0.226719$, and §7.3 gives $\kappa_{11}\ge0.226$), plus $O(\ln b)$. So the remainder $<10^{-1000}$ is justified.

## 4. Scope: what exactly is proved

- **Primes.** Exactly the 21 primes $11\le p\le97$.
  - Not $p=3,5$. At $p=7$, (T2) fails at the phase transition: $N_W=4$ (T4), as M4C §12 item 6 says.
  - Not $p>97$, and not the Wilson prime $563$.
  - The Wilson prime $13$ *is* covered, through the explicit block (S2).
- **Atom.** $A=p^3\mathbb Z_p$, with $j=0$ and $n_0=3p$. The statement is $\mu(K_p\cap A)/\mu(A)\ge c_p$, hence $\mu(K_p)\ge c_pp^{-3}$.
  - The headline states this correctly. The conditional bounds $c_p$ are not bounds on $\mu(K_p)$ itself.
- **Conditional on.** Only round-3 results labelled [proved] in note.md:
  - Theorem 11.14, i.e. R3M Theorem C3, AI-checked in round 3 and not human-refereed;
  - its inputs, Props 11.10, 11.11 and 11.13, and Prop 1.2.

  No unproved hypothesis enters (beyond the correctness of M4C's own lemmas, which is the logic lens). FE is verified, not assumed. The computer-assisted inputs are three rational constants per $p$ and integer bookkeeping, both reproduced here.
- **The "all $p\ge p_0$" statement.** Corollary M′ is correctly labelled [heuristic, not proved] in §9.2. It is conditional on:
  - AC($p$) (uniform anti-concentration for $r!$, $(r!,r!H_r)$ and $F_r$), an open arithmetic problem as far as anyone involved knows;
  - an unwritten $p$-uniform analysis of the schedule.

  The headline item 2 ("precise reduction") and the §0 table ("reduction") are stronger than this, which is (F2).

  A rough check of plausibility: AC($p$) bounds the phase-1 cost by $\log\Pi\lesssim2+2/p$, and the $s$-rule bounds the truncation cost by about $\eta=0.05$. So $\Pi_A\delta_A\lesssim0.4$. The heuristic is therefore reasonable, but it is not a proof.
- **Statements that are overstated:**
  - "with no truncation" (F1);
  - "precise reduction" (F2);
  - "makes Remark C6 rigorous" / "Remark C6, now proved" without the frozen-pattern qualifier (F3);
  - "§8: uniformly in the position" (F4, imprecise rather than wrong).

  Everything else checked in the claim is stated accurately:
  - the [computer-assisted] label;
  - the per-$p$ table, rounded down;
  - "$p=7$ is not covered";
  - "says nothing about Q3";
  - the credit to R3M and M4A.
- **A cosmetic point.** At $p=11$ the final line of `assemble.log` prints $\mu(K_{11})\ge9.391\cdot10^{-8}$ (from $c_p$ rounded to $0.000125$), while §7.3 prints $9.42\cdot10^{-8}$ (from $1.2549\cdot10^{-4}$). Both are valid.

## 5. Consistency with M4A and with the round-1 numerics

**M4A (verified track; different atoms $x_A+p^m\mathbb Z_p$ at $n_0=300$, different schedule and code).**
- *Constants.* M4A's $(q_1,q_2,q_3)$ are:
  - $(8309/8192,\ 4557/4096,\ 33271/8192)$ at $p=7$;
  - $(1.00144,1.11160,1.80119)$ at $p=11$;
  - $(1.000022,1.00812,1.19244)$ at $p=13$.

  M4A defines them through $Z=\sum\zeta_kF_k$ modulo $p^s$, which is the same object (F6). They equal M4C's and mine to every printed digit (S1).
- *Conclusions.* Both tracks conclude $\mu(K_p)>0$ at $p=11,13,17,19,23$.
  - M4A's conditional bounds, as corrected by their verifier (M4A_obstruction, (G1)), are $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$, $3.48\cdot10^{-3}$, $1.09\cdot10^{-1}$ and $2.06\cdot10^{-1}$, on their atoms.
  - M4C's are $1.25\cdot10^{-4}$, $0.572$, $0.808$, $0.800$ and $0.823$, on $p^3\mathbb Z_p$.

  These are lower bounds on different sets, so no numerical conflict is possible. For $p\ge13$, M4C's are much larger because its atom makes phase 1 deterministic with $\Pi_A\approx1$. At $p=11$ the two are of the same order.
- *How independent the two are.* The two proofs share R3M's C3 and the same mechanism: an averaged Hensel identity or inequality (M4A Theorem 1, M4C Lemma H2/Prop H′), and a 2D block factor $q_2/p^2$ (both Lemma Q). Their agreement is evidence for that mechanism, and the constants agree exactly. It is not independent evidence against a conceptual error in C3 or in the shared mechanism.

**Round-1 numerics (note §4.7, §5).**
- The exact census values $\delta_G(p)=\mu\{g_p\ge G\}$ are rigorous upper bounds on $\mu(K_p)$: $0.69976$ ($p=11$), $0.75454$ (13), $0.75692$ (17), $0.77792$ (19) and $0.85617$ (23). M4C's global lower bounds are all $\le2.6\cdot10^{-4}$, so they are trivially consistent.
- M4C's *conditional* bounds go up to $0.87$ on $A$, above the global densities. This is not a tension:
  - the global densities include the classes $r\bmod p$ in $\Phi_p$, where $g_p\equiv0$ (note Thm 3.5);
  - those classes are $\{7,8,10\}$ at $p=11$, $\{9,10,12\}$ at 13, $\{12,13,14,16\}$ at 17, $\{14,15,16,18\}$ at 19 and $\{19,20,22\}$ at 23 (T3);
  - $A$ lies in the class $0\notin\Phi_p$, where the first block is full.
- The round-1 values divided by $\delta_1(p)=1-|\Phi_p|/p$ are $0.962$, $0.981$, $0.990$, $0.985$ and $0.985$ at $p=11,\dots,23$. That is the average density of $K_p$, as bounded above by the census, over the classes where $g_p\not\equiv0$.
- Two caveats on this comparison:
  - the round-1 data give no upper bound on $\mu(K_p\cap A)/\mu(A)$ below $1$, so they could not refute any $c_p<1$;
  - the comparison only shows that $c_p\le0.87$ sits comfortably below the plausible true conditional density (close to 1 on $A$, where the slope-0 population at $3p$ is already of size about $2^{3p}/p^3$).

## 6. What I did not check

- The line-by-line proofs of Lemma H2, Proposition H′, Lemmas P, Q, T and T′ (the logic lens). I re-read them only far enough to locate where each obstruction is evaded, and found no step where an obstruction is violated.
- Theorem C3 itself: it is given by the task. I checked only that its hypotheses are met.
- The secondary results (Theorems D2, E and F, and Proposition Q), which Theorem M does not use.
- Outward rounding at the $10^{-40}$ level. My reassembly is in float64, and the margins ($\Pi_A\delta_A\le0.9284$ at $p=11$; $\le0.03$ elsewhere) are many orders larger than float error.

## 7. Proposed wording (for the integrator)

- **Headline, sentence 3:** "…and verifies its hypothesis FE completely, ~~with no truncation and no Monte Carlo~~ **using a deep-gate truncation (the events $G_\ell\subseteq G'_\ell$ of Lemmas L and T) whose cost is explicit, and no Monte Carlo. The truncation is necessary: without it $\mathbb E_A[\varepsilon_{k_0+1}]=+\infty$ (verify_C_obstruction, Proposition O1′). For $p\ge17$ it accounts for essentially all of $\delta_A$.**"
- **Headline item 2 and the §0 table:** "Cor M′ — **heuristic** reduction, conditional on AC($p$) and on an unwritten $p$-uniform schedule analysis (§9.2)".
- **Results list (Lemma H2/Prop H′) and the Remark after Prop H′:** add "on balls with a frozen gate pattern and $D\ge2r$. On a cylinder where a gate depth is random, the boundary term $c_{L+L'}$ itself has infinite mean, so this is not (S) uniformly on cylinders."
- **§8, obstruction paragraph:**
  - Barrier bullet: "Every deterministic bound used (P1's $\bar\varepsilon$; Lemma Q's 1D factors $q_1$, $q_2$, $p^{d-3}q_3$; the block-0 factor $p^{e_0}$) grows with window length or gate depth, as Theorem 3.10 and Proposition 11.23 require. Decay comes only from Lemma H2's average over the digits of $x$ between the ball radius and $D/2$, together with Lemma Q's 2D factor $q_2/p$, which uses the harmonic-number (first-order) digit."
  - Prop 11.15(b) bullet: add "and this truncation is necessary (Proposition O1′)".
- **§8 item 12 and §13 item 5:** add "An independent re-implementation by another track (verify_C_obstruction) reproduces $q_1,q_2,q_3$ (by a Fourier positivity formula), the schedule, $\Pi_A$, $\delta_A$ and every $c_p$."
- **note.md, after Proposition 11.15(b) (optional):** "The heuristic consequence is now a theorem for concrete atoms. On $p^3\mathbb Z_p$ with M4C's schedule, $\mathbb E_A[\varepsilon_{k_0+1}]=+\infty$, already through the normaliser term $c_{N'}/c_n$ (since $\mathbb E[p^{v(y)}]=\infty$ for Haar $y$). Likewise at M4A's window 307 through the double root (M4A_obstruction, Proposition O1). Markov's inequality is applicable only after a deep-gate truncation, which both proofs use."
