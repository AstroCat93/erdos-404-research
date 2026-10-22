# Logic checks of round-4 track M4B

This file holds two logic checks of track M4B, made by the `verify_M4B_logic` track of round 4:
- **Part II** (below, 2026-10-14): Lemma B2a and Corollary B2′ (deep gate at distance $d$). Verdict: **confirmed-with-fixes**. All the fixes are to the one-line statement of the claim; the proof needs none.
- **Part I** (further below, 2026-10-13/14): Theorem B1 / B1′ (adaptive window times). Verdict: confirmed-with-fixes. Its test results are in the logs `t1_partition.log`, `t2_atom_c2.log`, `t3_global_finite.log` and `t4_Qbound.log` in `data/round4/verify_M4B_logic/`.

---

# Part II. Logic check of M4B Lemma B2a and Corollary B2′ (deep gate at distance $d$)

Date: 2026-10-14. Lens: LOGIC.
- **Checked:** `data/round4/reports/M4B.md` §3 (Prop B2, Lemma B2a, Cor B2′ and the paragraph after it), together with the later uses of B2′ in N4 and B5. I also read the track's test `code/round4/M4B/b2_gate_split_check.py` and its log.
- **Definitions re-read:** `data/round3/reports/R3M.md`: Prop C2 (the definition of $\varepsilon$), the proof of Lemma C5 (signed digits), and §7.3 (the round-3 heuristic for $\kappa$).
- **Checker code** (new; it shares no code with `code/round4/M4B/`): `code/round4/verify_M4B_logic/b2lib.py`, `b2a_exhaustive.py`, `b2p_identity.py`, `batch_b2.sh`.
- **Logs:** `data/round4/verify_M4B_logic/t5_b2a.log` and `t6_b2p.log`. Each run starts with its command line.
- **Budget:** under one core-minute in total, `nice -n 10`.

## Headline

**Verdict: confirmed-with-fixes.**

I checked every line of the proof, re-derived it, and tested it in exact arithmetic. Every step holds:
- the factorial-cancellation lemma;
- the reduction of $A\equiv0\pmod{p^g}$ to an integer equation;
- the three surviving pre-patterns and their exact valuations;
- the two probabilities;
- the values $r_a$;
- the final identity and the $[\frac12,\frac32]$ bracket.

There are no measure-theoretic, filtration or uniformity issues. The result is a pointwise identity, valid for every $x$ that satisfies the gate hypothesis.

The fixes concern the **one-line form of the claim** that was passed to this check. M4B's own statement in §3 is correct as written.

- **(F1, the $d=1$ case.)** The one-line claim says "Coll$^{\rm pre}_g=\frac32 2^{-d}$ exactly" and gives the $\Delta$-formula for a deep gate at any distance $d$. Both hold only for $d\ge2$.
  - At $d=1$, $\mathrm{Coll}^{\rm pre}_g=\frac12$, not $\frac34$.
  - At $d=1$, the $\Delta$-formula is false. In exact tests it differs from $\varepsilon$ in 61 of 63 cases.
  - The correct $d=1$ statement, $\varepsilon=\frac{p^s}2\varepsilon^{\rm post}$, is the one the claim lists separately.
  - M4B §3 states the case split correctly.
- **(F2, implicit hypotheses.)** These hypotheses should be stated explicitly:
  - The split point must lie in the first window, $1\le d\le N-n$. Otherwise $\varepsilon^{\rm post}=\varepsilon([n+d,N),[N,N'))$ is undefined, and the step $k\ge g$ for $k=D$ can fail.
  - $s=v(x+n+d)$ is the exact depth.
  - $x\notin\{-1,\dots,-N'\}$, so that all valuations are finite.
  - $P(A\equiv0\bmod p^K)=2^{-d}$ needs $K>g$. The identity (c) holds without it, because both sides are $0$ when $K=g$.
- **(F3, two glosses are interpretations, not theorems.)**
  - *"This proves the round-3 heuristic $\kappa\approx p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}$ up to $[\frac12,\frac32]$."* Round 3 never defined $\varepsilon^{\rm post}$ (R3M §7.3: "the fine-scale mass of the window after it"). B2′ supplies a precise version: $\kappa:=\varepsilon/p^s=p^{v((d-1)!)}2^{-d}[\varepsilon^{\rm post}+\frac12\Delta]$. It does not show that $\kappa$ is independent of $s$, which the round-3 observation also suggested. For large $s$ that independence comes from the N4-type argument, $\varepsilon^{\rm post}\to\varepsilon_{\rm fact}$.
  - *"The correction is the $(y+2)^2$ double root."* Precisely: the correction term comes from the pre-patterns $\pm(e_{n+d-2}+e_{n+d-1})$. Their partial sum is $\pm y_{n+d-2}(x+n+d)$, which is the two-term prefix of the string $(1,1,1)$. With $Z=x+n+d-2$ that string has polynomial $(Z+2)^2$. The term $\Delta(1/(x+n+d-1))$ counts the post-window completions $B'\equiv-1/(x+n+d-1)\pmod{p^{K-g}}$, and $B'=1$ reproduces $(Z+2)^2$. The algebra was checked exactly in 324/324 cases. As an interpretation it is fair; it is not a separate mathematical statement.

**What this does not do.** The result is an exact identity that moves a deep gate's contribution onto the post-gate window. It gives no bound on $\varepsilon^{\rm post}$ or on any mean. It does not by itself bring $\mu(K_p)>0$ closer: M4B's Prop N4 shows the plain annealed mean is still $+\infty$. (S_B) and the initial-phase gap (M4B §7) remain open.

| item | M4B label | verdict |
|---|---|---|
| Lemma B2a (factorial cancellation) | proved | **confirmed**; exhaustive for $d\le22$ |
| Prop B2 steps used: (B2.1), (B2.2), (B2.3) | proved | confirmed (re-derived; tested inside the end-to-end identity) |
| Cor B2′(a): $v(x+n+i)=v(d-i)$, $g=v((d-1)!)+s$ | proved | confirmed |
| Cor B2′(b): three pre-patterns; $\mathrm{Coll}^{\rm pre}_g$; $P(A\equiv0\bmod p^K)$ | proved | confirmed **for $d\ge2$, $K>g$**, as M4B states. The one-line claim omits $d\ge2$ (F1). |
| Cor B2′(c): exact identity; $d=1$ identity; $[\frac12,\frac32]$ bracket | proved | confirmed; 395/395 exact cases |
| "proves the round-3 heuristic up to $[\frac12,\frac32]$" | (gloss) | acceptable as an interpretation (F3) |
| "the correction is the $(y+2)^2$ double root" | (gloss) | acceptable as an interpretation (F3) |

## 1. The claim, with every hypothesis explicit

**Setting** (M4B §1, §3; R3M Prop C2).
- $p$ is an odd prime, $v=v_p$, and $x\in\mathbb Z_p\setminus\{-1,\dots,-N'\}$.
- $n<N<N'$ are integers. The window elements are $y_j=\pi_j(x)/\pi_n(x)=\prod_{i=n+1}^{j}(x+i)$ for $n\le j<N'$, so $y_n=1$.
- $D=V_N-V_n$, $K=V_{N'}-V_n$, and $\varepsilon(W,W')=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$. Here $\mathrm{Coll}_k=\sum_r\nu_k(r)^2=P(\sum_j\delta_jy_j\equiv0\bmod p^k)$, with $\delta_j$ i.i.d., $P(0)=\frac12$ and $P(\pm1)=\frac14$.
- Split point $n+d$ with $1\le d\le N-n$; $g=V_{n+d}-V_n$; $A=\sum_{n\le j<n+d}\delta_jy_j$; and $B'=\sum_{n+d\le j<N'}\delta_j\pi_j/\pi_{n+d}$.
- $\rho'_k(r)=p^kP(B'\equiv r\bmod p^k)$; $\Delta(r)=\rho'_{K-g}(r)-\rho'_{D-g}(r)$; $\varepsilon^{\rm post}=\varepsilon([n+d,N),[N,N'))$.

**Lemma B2a.** If $\epsilon_0,\dots,\epsilon_{d-1}\in\{-1,0,1\}$ and $\sum_{k<d}\epsilon_k/k!=0$, then $\epsilon_k=0$ for every $k\ge2$, and $\epsilon_0=-\epsilon_1$.

**Corollary B2′ (as verified).** Assume moreover that $s:=v(x+n+d)$ satisfies $p^s>e\,(d-1)!$. Then:
- (a) $v(x+n+i)=v(d-i)$ for $1\le i<d$. Hence $g=v((d-1)!)+s$ and $c_{n+d}/c_n=2^{-d}p^g$.
- (b) $\mathrm{Coll}^{\rm pre}_g:=P(A\equiv0\bmod p^g)$ equals $\frac12$ if $d=1$, and $\frac32 2^{-d}$ if $d\ge2$. If $K>g$, then $P(A\equiv0\bmod p^K)=2^{-d}$.
- (c) If $d=1$, then $\varepsilon=\frac{p^s}{2}\varepsilon^{\rm post}=\frac{c_{n+1}}{c_n}\varepsilon^{\rm post}$. If $d\ge2$, then
$$\varepsilon=\frac{c_{n+d}}{c_n}\Big[\varepsilon^{\rm post}+\tfrac12\Delta\big(\tfrac1{x+n+d-1}\big)\Big],\qquad|\Delta(r)|\le\varepsilon^{\rm post}\ \text{for all }r.$$
  In both cases $\frac12\frac{c_{n+d}}{c_n}\varepsilon^{\rm post}\le\varepsilon\le\frac32\frac{c_{n+d}}{c_n}\varepsilon^{\rm post}$.

For $d=1$ the hypothesis $p^s>e\cdot0!$ is the same as $s\ge1$, because $p\ge3>e$.

## 2. Line-by-line audit

### 2.1 Lemma B2a [confirmed]

Let $k^*\ge2$ be the least $k\ge2$ with $\epsilon_k\ne0$, and suppose it exists.
1. $(k^*+1+m)!\ge(k^*+1)!\,(k^*+2)^m$ for $m\ge0$. This is correct: each extra factor is at least $k^*+2$.
2. Hence $\sum_{k>k^*}1/k!\le\frac1{(k^*+1)!}\sum_{m\ge0}(k^*+2)^{-m}=\frac{k^*+2}{(k^*+1)\,(k^*+1)!}$.
3. This is $<\frac1{k^*!}=\frac{k^*+1}{(k^*+1)!}$ iff $k^*+2<(k^*+1)^2$, which holds for every $k^*\ge1$.
   - Checked with exact rationals for $k^*=2,\dots,60$ (`t5_b2a.log`).
4. Therefore $|\sum_{k\ge k^*}\epsilon_k/k!|\ge\frac1{k^*!}-\sum_{k>k^*}\frac1{k!}>0$, and also $|\sum_{k\ge k^*}\epsilon_k/k!|\le\sum_{k\ge2}\frac1{k!}=e-2<1$.
   - The lower bound uses $|\epsilon_{k^*}|=1$.
   - The upper bound uses $|\epsilon_k|\le1$.
5. Since $\epsilon_k=0$ for $2\le k<k^*$, the hypothesis gives $\epsilon_0+\epsilon_1=-\sum_{k\ge k^*}\epsilon_k/k!$. The left side is an integer; the right side has absolute value in $(0,1)$. Contradiction.
6. So $\epsilon_k=0$ for all $k\ge2$, and then $\epsilon_0+\epsilon_1=0$.

Every step is valid. The digit bound $|\epsilon_k|\le1$ is essential, both in step 4 and as the lower bound $|\epsilon_{k^*}|/k^*!$. With digits in $\{-2,\dots,2\}$ the conclusion fails: for example $(1,-2,2)$ gives $1-2+1=0$. This is shown by the negative control in `t5_b2a.log` (8 violating vectors for each $d=3,\dots,6$).

### 2.2 The parts of Prop B2 that B2′ uses [confirmed]

- **(B2.1)** $\varepsilon=p^g\sum_{a\in p^g\mathbb Z_p}P(A=a)\Delta(r_a)$ with $r_a=-(a/p^g)u^{-1}$ and $u=y_{n+d}/p^g$.
  - $\sum_j\delta_jy_j=A+y_{n+d}B'$, because $y_j=y_{n+d}\cdot\pi_j/\pi_{n+d}$ for $j\ge n+d$.
  - $u$ is a unit because $v(y_{n+d})=g$.
  - $A$ and $B'$ are independent, since they use disjoint digits.
  - For $k\in\{D,K\}$: $k\ge g$ (here $d\le N-n$ is used for $k=D$). So the event forces $p^g\mid A$, and given $A=a$ it reads $B'\equiv r_a\pmod{p^{k-g}}$.
  - $A$ takes at most $3^d$ values, so the sum is finite.
- **(B2.2)** $\Delta(0)=\varepsilon^{\rm post}$.
  - $K-g=V_{N'}-V_{n+d}$ and $D-g=V_N-V_{n+d}$ are the $K$ and $D$ of the post composite window.
  - $p^k\mathrm{Coll}_k^{\rm post}=\rho'_k(0)$ by the signed-digit description.
  - When $d=N-n$, the first post window is empty, $D-g=0$, $\rho'_0\equiv1$, and the definition still applies.
- **(B2.3)** $|\Delta(r)|\le\Delta(0)$, and $\Delta$ is even.
  - $\psi(\xi)=\mathbb Ee(\xi B'/p^{K-g})=|\mathbb Ee(\xi X/p^{K-g})|^2\ge0$, because $B'=X-X'$ with $X,X'$ i.i.d. uniform subset sums.
  - Fourier inversion gives $\rho'_{K-g}(r)=\sum_\xi\psi(\xi)e(-\xi r/p^{K-g})$.
  - The characters modulo $p^{D-g}$ are exactly $\xi\in p^{K-D}\mathbb Z/p^{K-g}$, because $\psi_{D-g}(\xi')=\psi(\xi'p^{K-D})$.
  - $\psi$ is real and even, and the set $\{\xi\notin p^{K-D}\mathbb Z\}$ is symmetric. So $\Delta$ is real and even.

### 2.3 Corollary B2′ [confirmed]

- **(a)** For $1\le i<d$: $x+n+i=(x+n+d)-(d-i)$ and $1\le d-i\le d-1<e(d-1)!<p^s$. So $v(d-i)<s$ and $v(x+n+i)=v(d-i)$ by the ultrametric equality.
  - Summing, $\sum_{i=1}^{d-1}v(d-i)=v((d-1)!)$.
  - Therefore $g=v((d-1)!)+s$ and $c_{n+d}/c_n=2^{-d}p^{V_{n+d}-V_n}=2^{-d}p^g$.
- **(b)**
  1. With $w=(x+n+d)/p^s\in\mathbb Z_p$: $y_{n+i}=\prod_{k=1}^i(k-d+p^sw)\equiv\prod_{k=1}^i(k-d)=(-1)^i(d-1)!/(d-1-i)!\pmod{p^s}$ for $0\le i\le d-1$. This is correct, and also correct for $i=0$, where both sides are $1$.
  2. If $A\equiv0\pmod{p^g}$, then $A\equiv0\pmod{p^s}$ because $g\ge s$. So $p^s$ divides the integer $A_0=\sum_{i<d}\delta_{n+i}(-1)^i(d-1)_i$.
  3. $|A_0|\le\sum_{k=0}^{d-1}(d-1)!/k!<e\,(d-1)!<p^s$ (the first inequality is strict as a partial sum of $e$). Hence $A_0=0$.
  4. Substitute $k=d-1-i$ and $\epsilon_k=(-1)^k\delta_{n+d-1-k}$. Since $(-1)^{d-1-k}=(-1)^{d-1}(-1)^k$, we get $A_0=(-1)^{d-1}(d-1)!\sum_k\epsilon_k/k!$. By B2a, $\epsilon_k=0$ for $k\ge2$ and $\epsilon_0=-\epsilon_1$. Since $\epsilon_0=\delta_{n+d-1}$ and $\epsilon_1=-\delta_{n+d-2}$, this means $\delta_{n+d-1}=\delta_{n+d-2}$. So the solutions are $\delta_{\rm pre}=0$ and, for $d\ge2$, $\delta_{n+d-2}=\delta_{n+d-1}=\pm1$ with all other pre-digits $0$.
  5. These are necessary conditions. Sufficiency: for the pair, $A=\pm(y_{n+d-2}+y_{n+d-1})=\pm y_{n+d-2}(x+n+d)$, with $v(y_{n+d-2})=\sum_{i=1}^{d-2}v(d-i)=v((d-1)!)$. So $v(A)=g$ exactly. Hence $A\equiv0\pmod{p^g}$ and, if $K>g$, $A\not\equiv0\pmod{p^K}$.
  6. Probabilities: $P(\delta_{\rm pre}=0)=2^{-d}$, and $P(\text{pair})=2\cdot\frac14\cdot\frac14\cdot2^{-(d-2)}=\frac12 2^{-d}$.
  7. For $d=1$: $A=\delta_n$ and $|\delta_n|\le1<p^s$, so $A\equiv0\pmod{p^g}$ iff $\delta_n=0$, which has probability $\frac12$.
  8. No other pattern takes the value $\pm y_{n+d-2}(x+n+d)$, since every pattern with $p^g\mid A$ is among the three. So $P(A=a_\pm)=2^{-d-2}$ each.
- **(c)** Insert into (B2.1).
  - $a=0$ gives $r_0=0$, so $\Delta(0)=\varepsilon^{\rm post}$, with weight $2^{-d}$.
  - $a=a_\pm=\pm y_{n+d-2}(x+n+d)$ give $r_{a_\pm}=-a_\pm/y_{n+d}=\mp1/(x+n+d-1)$, because $y_{n+d}=y_{n+d-2}(x+n+d-1)(x+n+d)$.
  - $x+n+d-1\equiv-1\pmod{p^s}$ is a unit, so $1/(x+n+d-1)\in\mathbb Z_p$.
  - $\Delta$ is even, so the two terms are equal.
  - Total: $p^g[2^{-d}\varepsilon^{\rm post}+2\cdot2^{-d-2}\Delta]=\frac{c_{n+d}}{c_n}[\varepsilon^{\rm post}+\frac12\Delta]$.
  - For $d=1$: $p^s\cdot\frac12\Delta(0)$.
  - The bracket follows from (B2.3).
  - If $K=g$, then $D=g$, $\Delta\equiv0$, $\varepsilon^{\rm post}=0$ and $\varepsilon=0$, so the identity holds trivially.

### 2.4 The lens checklist

| lens item | status for B2a / B2′ |
|---|---|
| every hypothesis stated and satisfied | yes, after F2: $1\le d\le N-n$; exact depth $s$; finite valuations; $K>g$ only for $P(A\equiv0\bmod p^K)$ |
| quantifier order | $\forall p$ odd, $\forall n<N<N'$, $\forall d\in[1,N-n]$, $\forall x$ with $p^{v(x+n+d)}>e(d-1)!$: identity. Nothing is chosen after $x$. |
| uniformity (cylinders, $p$, slope) | pointwise in $x$; no constant depends on $p$, $n$ or the window; no slope enters |
| measurability / filtration / stopping times / optional stopping | not used (a deterministic identity for each $x$) |
| Paley–Zygmund; "survival ⟹ $x\in K_p$" | not used by this claim |
| explicit constants | $e-2<1$; $k^*+2<(k^*+1)^2$; $|A_0|<e(d-1)!$; $2^{-d}$, $\frac12 2^{-d}$, $\frac32 2^{-d}$; $[\frac12,\frac32]$. All re-derived and tested. |
| sharpness of the depth hypothesis | sufficient, not necessary (e.g. $p=3$, $d=6$, $s=5$ already gives 3 solutions; `t5_b2a.log`). Below the threshold the conclusions do fail in general (§4). |

### 2.5 Downstream uses (read for consistency, not re-verified as separate claims)

- **Prop N4** uses only the case $d=1$, $s\ge1$ of (c). That case is valid.
- **Prop B5** uses the upper bound $\mathrm{Coll}^{\rm pre}_g\le\frac32 2^{-d}$ for a gate possibly in the second window.
  - The argument of (b) uses only the pre-elements modulo $p^s$ and $p^s>e(d-1)!$, not $d\le N-n$. So the transfer is valid.
  - At $d=1$ the true value $\frac12$ is below $\frac34$, so the bound holds there as well.

## 3. Obstructions in the brief

B2′ is a deterministic identity, so it should be compared with the barrier lemmas (Theorem 3.10 / Prop 11.23). It gives no deterministic bound on $\varepsilon$: it moves the deep gate's contribution onto $\varepsilon^{\rm post}$, which is again a fine-scale mass. It is therefore consistent with the barriers.

It also respects:
- Theorem 3.6: no residue-class criterion is claimed.
- Prop 11.12: no per-window Cauchy–Schwarz is used.
- Prop 11.15(b) / N4: B2′ is the mechanism of the divergence, not a way around it.

## 4. Numerical tests (exact arithmetic)

The tests are independent of M4B's code. $\varepsilon$ and $\varepsilon^{\rm post}$ are computed from the R3M definition (unsigned subset-sum collisions). $\Delta$ is computed from the signed law of the post window. The pre-patterns are enumerated exhaustively and evaluated exactly modulo $p^{\rm PREC}$, with PREC $=30$ or $40$ digits. All valuations are asserted to be below PREC, so each test covers the whole cylinder $x+p^{\rm PREC}\mathbb Z_p$.

**t5 — Lemma B2a** (`t5_b2a.log`, `b2a_exhaustive.py 22`).
- Meet-in-the-middle over $\{-1,0,1\}^d$ for $d=1,\dots,22$, i.e. up to $3^{22}\approx3.1\cdot10^{10}$ vectors. The zero-sum vectors are exactly $\{0,\pm(1,-1,0,\dots)\}$: 3 for $d\ge2$ and 1 for $d=1$. **0 failures.**
- Tail bound of the proof: exact for $k^*=2..60$.
- Negative control with digits in $[-2,2]$: the lemma fails, as it must.
- Depth table: below the threshold $p^s\le e(d-1)!$, the number of patterns with $A_0\equiv0\pmod{p^s}$ is often $>3$ (e.g. $p=7$, $d=6$, $s=1$: 101). At or above the threshold it is always 3.

**t6 — Corollary B2′ end to end** (`t6_b2p.log`, `b2p_identity.py`, 7 runs).
- Forced gates $v(x+n+d)=s$ with a random unit cofactor; every other digit of $x$ is random.
- Coverage:
  - $p=7$: $d\in\{1,\dots,9\}$ (including $d=8,9$ with $v((d-1)!)=1$);
  - $p=5$: $d\in\{1,\dots,8\}$;
  - $p=3$: $d\in\{1,\dots,8\}$ (including $v((d-1)!)=2$).
- Depths: $s$ from the threshold up to threshold $+2$.
- Edge cases covered:
  - $d=N-n$ (empty first post window);
  - $D>g$ and $D=g$;
  - $K=g$ (24 cases).

| check | cases under hypothesis | failures | cases below threshold (negative control) | failures there |
|---|---|---|---|---|
| (a) valuations, $g$ | 395 | 0 | 169 | 4 |
| (b) solution set $=\{0,\pm\text{pair}\}$ | 395 | 0 | 169 | 87 |
| (b) $v(A)=g$ exactly for the pair | 395 | 0 | 169 | 49 |
| (b) $\mathrm{Coll}^{\rm pre}_g$ ($\frac32 2^{-d}$, or $\frac12$ at $d=1$) | 395 | 0 | 169 | 87 |
| (b) $P(A\equiv0\bmod p^K)=2^{-d}$ | 395 | 0 | 169 | 9 |
| (B2.2) $\Delta(0)=\varepsilon^{\rm post}$; $\Delta$ even; $|\Delta|\le\varepsilon^{\rm post}$ | 371 ($K>g$) | 0 | 169 | 0 |
| **(c) exact identity** | **395** | **0** | 169 | 87 |
| (c) bracket $[\frac12,\frac32]$ | 395 | 0 | 169 | 15 |
| $(1,1,1)$ gloss: $y_{n+d-2}+y_{n+d-1}+y_{n+d}=y_{n+d-2}(x+n+d)^2$ | 324 ($d\ge2$) | 0 | — | — |

- **Negative control F1.** The $d\ge2$ formula (with its $\Delta(1/(x+n))$ term) applied at $d=1$ differs from the exact $\varepsilon$ in **61/63** cases. So the restriction to $d\ge2$ in the one-line claim is necessary, not cosmetic.
- **Ratios** $\varepsilon/((c_{n+d}/c_n)\varepsilon^{\rm post})$ under the hypothesis:
  - exactly $1$ at $d=1$;
  - between $0.75$ and $1.44$ for $d\ge2$;
  - below the threshold, they range from $0.29$ to $3.6$.
- **Agreement with M4B's own tests** (their §8.1). Ratios $1.352$, $1.434$, $1.357$; $2^d\mathrm{Coll}=1.5$. These are consistent with the above. Their forced-gate runs cover only $(p,d,s)\in\{(3,4,5),(3,1,5),(5,2,5),(7,3,4),(7,1,4)\}$; t6 extends this to every $d$ up to 8–9 and to depths at the threshold.

## 5. What remains open

- Nothing in B2a/B2′ itself, after F1–F3.
- Everything M4B lists as open is unchanged by this check: (S_B), the initial phase (§7), the ladder-search bound, and the decay of $\varepsilon_{\rm fact}$ at $p=3,5$. B2′ is an exact bookkeeping identity; it neither bounds $\varepsilon^{\rm post}$ nor averages over $x$.

## 6. Credit

- **Track M4B (round 4):** Lemma B2a, Prop B2 and Cor B2′, and the observation that the correction comes from the pre-gate pair.
- **Track R3M (round 3):** the definition of $\varepsilon$ (Prop C2), the signed-digit description (Lemma C5), and the deep-gate heuristic for $\kappa$ (§7.3).
- **The note:** the double root $(y+2)^2$ is note Proposition 3.4.
- **Classical tools:** the ultrametric inequality, Fourier inversion on $\mathbb Z/p^k$, and the tail bound for $\sum1/k!$.
- **This check:** the tests t5 and t6, and fixes F1–F3.
- AI-assisted session; not checked by a human.

---

# Logic check of round-4 track M4B: Theorem B1 / B1′ (adaptive window times)

Date: 2026-10-13. Check track: `verify_M4B_logic` (round 4), lens LOGIC.
- Report checked: `data/round4/reports/M4B.md`, §2 (with §1 and the uses of B1 in §6–§7). Track code `code/round4/M4B/` was read; it has no test of B1 (the track says B1 is structural).
- Round-3 sources re-read for the steps that B1 imports: `data/round3/reports/R3M.md` §1–§5 (Lemma 1, Lemma 2, Prop A, Cor A′, Prop B, Lemma C1, Prop C2, Theorem C3) and `data/round3/checks/R3M.md` (§2 audit of C3; Observation G in §3).
- Checker code: `code/round4/verify_M4B_logic/`. Logs: `data/round4/verify_M4B_logic/` (each run starts with its command line). Scratch: `/tmp/r4_verify_M4B_logic/`.
- Budget used: about 65 core-minutes on one core under `nice -n 10`. That includes about 23 core-minutes in two $p=7$ runs that were killed by hand (both are logged), and one $p=7$ run that timed out at 240 s. The longest completed job took 13 minutes.

## Headline

**Verdict: confirmed-with-fixes.**

Theorem B1 (the per-atom form) is correct as stated. I re-derived every step of R3M Theorem C3 with random times and found no place where determinism of the times is used beyond what Lemma B1a and two-step predictability provide.

Theorem B1′ (the global Paley–Zygmund form) is correct when $Q_j<\infty$. One sub-step of its proof is not justified in the stated generality: the claim "$M_j$ is bounded, so $Q_j<\infty$". The bound given is $M_j\le p^{n_j/(p-1)+\log_p(e(n_j-1)!)}$. That is finite for each value of $n_j$, but for $j\ge2$ the time $n_j$ is random, and the setting puts no bound on it. The fix is one added hypothesis: $n_j$ essentially bounded on $\mathrm{adm}_j$, or $Q_j<\infty$ assumed directly. Either one holds automatically for $j\le1$ and for every rule with $n_{\ell+1}\le F(n_\ell)$, including the track's own example rule. Without the fix, the displayed bound is vacuous or undefined exactly when $Q_j=\infty$, so no false conclusion can follow. That is why the verdict is "with fixes" and not "gap".

Three further fixes are needed:
- The thresholds $\bar\varepsilon_\ell$ must be deterministic. In the per-atom form they may at most be constant on the atom. They may not be functions of the random $n_\ell$.
- The one-line claim summary omits the hypothesis $m_j^*>\sqrt{\Pi Q_j\delta}$, without which the displayed bound is not proved. The report itself states it.
- The sentence "This is why two-step predictability is required" is too strong. Two-step predictability is used by the proof as written, but **one-step predictable times also work**: see Remark V1 below, proved here and tested exactly.

B1 and B1′ are conditional, structural results. They do not bring $\mu(K_p)>0$ any closer by themselves. FE (equivalently, M4B's (S_B) plus the initial-phase gap of M4B §7) remains open, as M4B says.

| item | M4B label | verdict |
|---|---|---|
| Lemma B1a (partition, constancy, refinement) | proved | confirmed |
| $B_\ell\in\mathcal G_{\ell-1}$; $\{\tau_j>\ell\}\in\mathcal G_{\ell-1}$ | proved | confirmed |
| Theorem B1 (per-atom) | proved | confirmed (needs F2 made explicit) |
| Theorem B1′ (global) | proved | confirmed-with-fixes (F1, F2, F3) |
| Example adaptive rule (§2, end) | — | confirmed (two-step predictable; $n_j$ bounded, so F1 holds for it) |
| "two-step predictability is required" | — | overstated: Remark V1 [proved here] |

## 1. The claim

**Setting (M4B §2).**
- $p$ is an odd prime, and $n_0<n_1$ are deterministic with $n_0\ge2p$.
- For $\ell\ge1$, $n_{\ell+1}>n_\ell$ is a function of $x\bmod p^{m_{\ell-1}(x)}$, where $m_\ell:=V_{n_\ell(x)}(x)$.
- $A_\ell(x)=x+p^{m_\ell(x)}\mathbb Z_p$, and $\mathcal G_\ell$ is generated by these cylinders.
- $B_\ell=\{D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}},\ M_{n_{\ell+1}}<m_{\ell-1}\}\cap E_\ell\cap\{\varepsilon_\ell\le\bar\varepsilon_\ell\}$ with $E_\ell\in\mathcal G_{\ell-1}$, and $\tau_j=\min\{\ell>j:x\notin B_\ell\}$.

**Theorem B1.** For an admissible atom $A$ of $\mathcal G_j$ with $\delta_A=\mu_A(\tau_j<\infty)<1/\Pi_A$, where $\Pi_A=(1+\chi_j^2(A))\prod_{\ell>j}(1+\bar\varepsilon_\ell)$:
$$\mu(K_p\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A.$$

**Theorem B1′.** Put $m_j^*=\mathbb E[M_j\mathbf 1_{\mathrm{adm}_j}]$, $Q_j=\mathbb E[(1+\chi_j^2)M_j^2\mathbf 1_{\mathrm{adm}_j}]$, $\Pi=\prod_{\ell>j}(1+\bar\varepsilon_\ell)$ and $\delta=\mu(\mathrm{adm}_j\cap\{\tau_j<\infty\})$. If $m_j^*>\sqrt{\Pi Q_j\delta}$, then
$$\mu(K_p)\ge(m_j^*-\sqrt{\Pi Q_j\delta})^2/(\Pi Q_j).$$

## 2. Line-by-line audit

### 2.1 Lemma B1a [confirmed]

The induction is correct. Written out:
- *Base $\ell=0$.* $n_0,n_1$ are constants. Since $n_0\ge2p$, two of $x+1,\dots,x+n_0$ are divisible by $p$, so $M_{n_0}(x)<V_{n_0}(x)=m_0(x)$ (for $x$ not a negative integer). For $y\in A_0(x)$ this gives $v(y+i)=v(x+i)$ for $i\le n_0$, hence $m_0(y)=m_0(x)$ and $A_0(y)=A_0(x)$. So the $A_0$ form a countable partition up to a countable set.
- *Step.* Assume that $n_0,\dots,n_\ell$ and $m_{\ell-1}$ are constant on $A_{\ell-1}(x)$ and that the $A_{\ell-1}$ form a partition.
  - Then "a function of $x\bmod p^{m_{\ell-1}(x)}$" is well defined: it means $\mathcal G_{\ell-1}$-measurable. So $n_{\ell+1}$ is constant on $A_{\ell-1}(x)$.
  - $m_\ell\ge m_{\ell-1}$, because $n_\ell>n_{\ell-1}$ and $V_n$ is nondecreasing in $n$. Hence $A_\ell(x)\subseteq A_{\ell-1}(x)$.
  - For $y\in A_\ell(x)$: $n_\ell(y)=n_\ell(x)$, and $M_{n_\ell}<m_\ell$ because $n_\ell>n_0\ge2p$. So all $v(y+i)$, $i\le n_\ell$, agree with those of $x$, and $m_\ell(y)=m_\ell(x)$.
- The definition is not circular. $n_{\ell+1}$ needs $m_{\ell-1}$, hence $n_{\ell-1}$, which is $\mathcal G_{\ell-3}$-measurable. Recursion on $\ell$ is well founded.

Tested from scratch at $p=3,5,7$ with two different two-step rules (`t1_partition.log`): 0 failures. A one-step negative control is detected (§5).

### 2.2 Measurability of $B_\ell$ and of $\tau_j$ [confirmed]

- $n_{\ell-1},n_\ell$ are constant on $\mathcal G_{\ell-1}$-atoms by Lemma B1a, and $n_{\ell+1}$ by two-step predictability.
- $\{M_{n_{\ell+1}}<m_{\ell-1}\}$ is the condition "$x+i\not\equiv0\bmod p^{m_{\ell-1}}$ for $i\le n_{\ell+1}$", a condition on the atom.
- On it all $v(x+i)$ with $i\le n_{\ell+1}$ are determined. Hence $D_{\ell-1}$, $D_\ell$ and the first event are determined.
- On the first event $K=D_{\ell-1}+D_\ell\le m_{\ell-1}$. Also $\varepsilon_\ell=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$ is computed from the integer polynomials $y_j=\pi_j/\pi_{n_{\ell-1}}$ modulo $p^K$. So it is a function of $x\bmod p^{m_{\ell-1}}$.
- Off the first event $B_\ell$ fails whatever $\varepsilon_\ell$ is. Hence $B_\ell\in\mathcal G_{\ell-1}$ (given $E_\ell\in\mathcal G_{\ell-1}$), and $\{\tau_j>\ell\}=\bigcap_{j<k\le\ell}B_k\in\mathcal G_{\ell-1}$.
- Admissibility of a $\mathcal G_j$-atom involves $n_{j+1}$, which is constant on it: deterministic for $j=0$, $\mathcal G_{j-1}$-measurable for $j\ge1$. $Z^0_{n_j}$ is constant on the atom by R3M Lemma 2(a), since slope $0$ is read modulo $p\le p^{m_j}$. So admissibility is a property of the atom.

Exact tests: the first event is invariant under $x\mapsto x+p^{m_{\ell-1}}z$ in 12 800/12 800 cases, and $\varepsilon_\ell$ is invariant in 6 983/6 983 cases (exact `Fraction`s), at $p=3,5,7$ (`t1_partition.log`).

### 2.3 Theorem B1: where C3 could use deterministic times [confirmed]

I list every step of the R3M C3 proof and what it needs from the times.

| step of C3 | what it needs | holds with random times because |
|---|---|---|
| $\mathcal G_\ell$ is a filtration of countable partitions | $M_{n_\ell}<m_\ell$; $n_\ell$ constant on its own cylinder | Lemma B1a |
| $M_\ell=c_{n_\ell}Z^0_{n_\ell}$ is $\mathcal G_\ell$-measurable | $n_\ell$ constant on $\mathcal G_\ell$-atoms; R3M Lemma 2(a) | Lemma B1a |
| martingale step (Cor A′, $L=0$) on a $\mathcal G_\ell$-atom inside $\{\tau_j>\ell\}$ | $W_\ell=[n_\ell,n_{\ell+1})$ fixed on the atom; (W2′) $D_\ell\le m_\ell-M_{n_\ell}$; (W3′) $M_{n_{\ell+1}}<m_\ell$ | $n_{\ell+1}$ is $\mathcal G_{\ell-1}\subseteq\mathcal G_\ell$-measurable. (W2′): $D_\ell\le m_{\ell-1}-D_{\ell-1}-M_{n_{\ell+1}}=2m_{\ell-1}-m_\ell-M_{n_{\ell+1}}\le m_\ell-M_{n_\ell}$. (W3′): $M_{n_{\ell+1}}<m_{\ell-1}\le m_\ell$. For $\ell=j$ both come from admissibility. |
| stopped process is a martingale | $\{\tau_j>\ell\}\in\mathcal G_\ell$ | §2.2 (even $\in\mathcal G_{\ell-1}$) |
| first $L^2$ step: Prop B at $\ell=j$ | $W_j$ fixed on $A$; Prop A(i), so the children are the whole slope-0 population | $n_{j+1}$ constant on $A$ |
| later $L^2$ steps: Prop C2 on a $\mathcal G_{\ell-1}$-atom inside $\{\tau_j>\ell\}$ | the composite window $[n_{\ell-1},n_{\ell+1})$ fixed on the atom; (5.2) | two-step predictability; (5.2) is the first event of $B_\ell$. Inside C2, Step 1 conditions on $x'+p^{m+D}\mathbb Z_p$, which is exactly the $\mathcal G_\ell$-atom ($m_\ell=m_{\ell-1}+D_{\ell-1}$). |
| $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}\le(1+\bar\varepsilon_\ell)a_\ell$ | $\bar\varepsilon_\ell$ a constant on $A$; $a_\ell$ nondecreasing (conditional Jensen); finiteness by induction | needs **F2** ($\bar\varepsilon_\ell$ deterministic, or $\mathcal G_j$-measurable in the per-atom form) |
| Doob $L^2$ convergence; $\mathbb E_A\tilde M_\infty=M_j(A)$ | $\sup a_\ell\le M_j(A)^2\Pi_A<\infty$ | $M_j(A)$ is a finite constant on the atom |
| survival $\Rightarrow K_p$ | $Y>0\Rightarrow\tau_j=\infty$ and $\lim M_\ell>0$; then Prop A(i) on every later window; (F2) backward integrality; (F1); $n_\ell\to\infty$ | A(i) holds on $\{\tau_j=\infty\}$ window by window. $n_\ell\to\infty$ because the $n_\ell$ are strictly increasing integers. |
| Paley–Zygmund | $\mathbb E_AY\ge M_j(A)(1-\sqrt{\Pi_A\delta_A})>0$ (Cauchy–Schwarz); $\mathbb E_AY^2\le M_j(A)^2\Pi_A$ | generic |

The constant is right. $\mu_A(Y>0)\ge(\mathbb E_AY)^2/\mathbb E_AY^2\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$, and $M_j(A)$ cancels.

(F1) was re-read against note §1.2. $g_p(x)=\sup_Bv_p(S_B(x))$ over finite $B$, and a path alive at $n$ gives $v_p(S_B(x))\ge V_n(x)\ge v(n!)$.

### 2.4 Theorem B1′ [confirmed-with-fixes]

- *Martingale.* $\tilde M_\ell=M_{\min(\ell,\tau_j)}\mathbf 1_{\mathrm{adm}_j}$. Every $\mathcal G_\ell$-atom ($\ell\ge j$) lies in one $\mathcal G_j$-atom, which is either inside $\mathrm{adm}_j$ or disjoint from it. The conditional-expectation identity therefore holds atom by atom. Integrability needs $m_j^*<\infty$, which follows from $Q_j<\infty$ (Cauchy–Schwarz). Correct, given $Q_j<\infty$.
- *Second moments.* $a_j\le a_{j+1}\le Q_j$ by Prop B on each admissible atom. Integrating Prop C2 over the $\mathcal G_{\ell-1}$-atoms in $\{\tau_j>\ell\}\cap\mathrm{adm}_j$ gives
$$a_{\ell+1}-a_\ell=\mathbb E\big[\mathbf 1_{\{\tau_j>\ell\}\cap\mathrm{adm}_j}\,\mathbb E[M_{\ell+1}^2-M_\ell^2\mid\mathcal G_{\ell-1}]\big]\le\bar\varepsilon_\ell a_{\ell-1}.$$
  This uses $\tilde M_{\ell-1}=M_{\ell-1}$ on $\{\tau_j>\ell\}$, $\ell-1\ge j$, and $\bar\varepsilon_\ell$ deterministic (**F2**). Correct.
- ***$Q_j<\infty$: not justified for $j\ge2$ (F1).*** The proof bounds $M_j\le p^{V_{n_j}}/2$, then $V_{n_j}<n_j/(p-1)+M_{n_j}$ (R3M Lemma 1(b)), then $M_{n_j}\le\log_p(e(n_j-1)!)$ on $\{Z^0_{n_j}\ne0\}$ (Observation G; the case $v(x+i)\ge V_{n_j}$ is excluded by $n_j\ge2p$).
  - Each step is right (tested in `t4_Qbound.log`). But the result is a bound depending on $n_j$. For $j\ge2$, $n_j$ is a random time chosen by an arbitrary $\mathcal G_{j-2}$-measurable rule, and nothing in the setting bounds it. For example, $n_{\ell+1}=n_\ell+p^{m_{\ell-1}(x)}$ is a legal rule with $\operatorname{ess\,sup}n_2=\infty$, because $m_0$ is unbounded.
  - Nor is $\chi_j^2$ addressed. It is bounded by $p^{D_j}-1\le p^{m_j}-1$, which is again finite only when $m_j$ is bounded on $\mathrm{adm}_j$.
  - Whether $\mathbb E[M_n^2\mathbf 1_{\mathrm{adm}}]$ stays bounded as $n\to\infty$ is essentially the open $L^2$ question itself (R3M §7.1 is heuristic). So it cannot be supplied for free.
  - *Consequence.* When $Q_j=\infty$, the hypothesis $m_j^*>\sqrt{\Pi Q_j\delta}$ fails if $\delta>0$. If $\delta=0$, the conclusion reads $\mu(K_p)\ge0$ (true) or $\infty/\infty$ (undefined). So the theorem never asserts anything false, but its proof contains an unjustified sentence.
  - *Fix.* Add the hypothesis "$n_j$ is essentially bounded on $\mathrm{adm}_j$". Then $m_j\le\sup n_j/(p-1)+\log_p(e(\sup n_j-1)!)$ on $\mathrm{adm}_j$, so both $M_j$ and $\chi_j^2$ are bounded. Alternatively, assume $Q_j<\infty$ directly. This holds for $j\in\{0,1\}$, and for every rule with $n_{\ell+1}\le F(n_\ell)$ for a deterministic $F$. The example rule has $n_{\ell+1}\le\lceil rn_\ell\rceil+R$, and §7's intended use takes $j$ small with explicit times, so no downstream use is affected.
- *Conclusion step.* Let $Y=\mathbf 1_{\{\tau_j=\infty\}}\tilde M_\infty$.
  - $\mathbb EY=m_j^*-\mathbb E[\tilde M_\infty\mathbf 1_{\{\tau_j<\infty\}\cap\mathrm{adm}_j}]\ge m_j^*-\sqrt{\Pi Q_j\delta}$, using $L^1$ convergence ($L^2$-bounded) and Cauchy–Schwarz on $\mathrm{adm}_j\cap\{\tau_j<\infty\}$.
  - $\mathbb EY^2\le\Pi Q_j$, and $\{Y>0\}\subseteq K_p$ (§2.3, last two rows).
  - Paley–Zygmund at level $0$ needs $\mathbb EY>0$, which is the hypothesis $m_j^*>\sqrt{\Pi Q_j\delta}$ (**F3**). Correct.
- *Consistency of constants.* With $\mathrm{adm}_j$ a single atom $A$: $m^*=\mu(A)M_j(A)$, $Q=\mu(A)(1+\chi^2)M_j(A)^2$ and $\delta=\mu(A)\delta_A$. B1′ then gives exactly $\mu(K_p)\ge\mu(A)(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$, the conclusion of B1. ✓
- *Strengthening (no fix needed).* The proof uses only that every atom of $\mathrm{adm}_j$ is admissible. B1′ therefore holds with $\mathrm{adm}_j$ replaced by any union $S\in\mathcal G_j$ of admissible atoms. I use this in the exact test of §5, with $S=\mathrm{adm}_j$ except at $p=7$.

### 2.5 The example adaptive rule [confirmed]

- The ladder test uses $\min(v(x+i),m_{\ell-1})$, a function of $x\bmod p^{m_{\ell-1}}$. With $n_\ell$ constant on $\mathcal G_{\ell-1}$-atoms, $n_{\ell+1}$ is $\mathcal G_{\ell-1}$-measurable.
- The fallback outcome and the event $\{M_{n_{\ell+1}+T_{\max}}\ge m_{\ell-1}\}$ are $\mathcal G_{\ell-1}$-measurable. Putting them into $E^c_{\ell+1}$ is legal, since $E_{\ell+1}$ only has to be $\mathcal G_\ell$-measurable.
- $n_{\ell+1}\ge\lceil rn_\ell\rceil>n_\ell$ for $r>1$.
- $n_{\ell+1}\le\lceil rn_\ell\rceil+R$, so F1 holds for this rule.
- Implemented as `vlib.rule_ladder` and tested in t1, t2 and t3.

### 2.6 Remark V1: two-step predictability is sufficient, not necessary [proved here]

M4B writes "This is why two-step predictability is required". It is required for the proof as written, because C2 is applied with all three times fixed on a $\mathcal G_{\ell-1}$-atom. But the theorem also holds for one-step predictable times.

**Claim.** Let $n_0<n_1$ be deterministic with $n_0\ge2p$, and let $n_{\ell+1}>n_\ell$ be $\mathcal G_\ell$-measurable. Define $B_\ell$ as in M4B, with $E_\ell\in\mathcal G_\ell$; then $B_\ell\in\mathcal G_\ell$. Then Theorems B1 and B1′ hold verbatim, with F1–F3.

*Proof.* Only the $L^2$ step changes. Fix a $\mathcal G_{\ell-1}$-atom $C\subseteq\{\tau_j>\ell-1\}$; this event is in $\mathcal G_{\ell-1}$ because $B_k\in\mathcal G_k$.
1. $C$ contains finitely many $\mathcal G_\ell$-atoms $C'$ ($p^{D_{\ell-1}}$ of them). If none lies in $B_\ell$, the increment is $0$ on $C$.
2. Otherwise let $N^*:=\max\{n_{\ell+1}(C'):C'\subseteq C\cap B_\ell\}$, attained at some $C'_*$.
3. (5.2) for $[n_{\ell-1},N^*)$ is a property of $C$ given the end time, and it holds because $C'_*\in B_\ell$. Likewise $\varepsilon(W_{\ell-1},[n_\ell,N^*))\le\bar\varepsilon_\ell$.
4. *Jensen step.* Let $C'\subseteq C\cap B_\ell$ and $n'=n_{\ell+1}(C')\le N^*$. The window $[n',N^*)$ satisfies (W2′) and (W3′) on every atom $x''+p^{V_{n'}}\mathbb Z_p\subseteq C'$:
   - (W2′): $V_{N^*}-V_{n'}\le V_{N^*}-V_{n_\ell}\le m_{\ell-1}-M_{N^*}-D_{\ell-1}\le V_{n'}-M_{n'}$;
   - (W3′): $M_{N^*}<m_{\ell-1}\le V_{n'}$.
   
   So Cor A′ makes $c_{N^*}Z^0_{N^*}$ a martingale extension of $M_{n'}$, and conditional Jensen gives $\mathbb E_{C'}[(c_{N^*}Z^0_{N^*})^2]\ge\mathbb E_{C'}[M_{\ell+1}^2]$.
5. For $C'\not\subseteq B_\ell$, the same Jensen argument (window $[n_\ell,N^*)$) gives $\mathbb E_{C'}[(c_{N^*}Z^0_{N^*})^2]-M_\ell^2\ge0$.
6. Summing,
$$\mathbb E_C[\mathbf 1_{B_\ell}(M_{\ell+1}^2-M_\ell^2)]\le\mathbb E_C[(c_{N^*}Z^0_{N^*})^2]-\mathbb E_C[M_\ell^2]\le\varepsilon(W_{\ell-1},[n_\ell,N^*))\,M_{\ell-1}^2\le\bar\varepsilon_\ell M_{\ell-1}^2,$$
   by Prop C2 for the fixed composite window $[n_{\ell-1},N^*)$ on $C$.
7. Hence $\mathbb E[\tilde M_{\ell+1}^2-\tilde M_\ell^2\mid\mathcal G_{\ell-1}]\le\bar\varepsilon_\ell\tilde M_{\ell-1}^2$, as before.

The martingale step needs only $\{\tau_j>\ell\}\in\mathcal G_\ell$. The rest is unchanged. ∎

*Tests (exact, `t2_atom_c2.log`).*
- The monotonicity used in step 4 holds on every $\mathcal G_\ell$-atom tested.
- The one-step adversarial choice is bounded by the cap, as the proof predicts.
- A naive one-step bound that averages $\varepsilon$ of the chosen window over $C'$ (instead of using $\varepsilon$ at $N^*$) **fails** in some atoms. So the cap $N^*$ is the load-bearing point.

V1 does not change any M4B conclusion, but it widens the class of admissible adaptive rules.

## 3. Fixes required

- **F1 (proof of B1′, "$Q_j<\infty$").** Add the hypothesis "$n_j$ essentially bounded on $\mathrm{adm}_j$" (or "$Q_j<\infty$"). Say that $\chi_j^2\le p^{D_j}-1$ is then also bounded. Without it the sentence "$M_j$ is bounded" is unjustified for $j\ge2$.
- **F2 (statements of B1 and B1′).** State that $(\bar\varepsilon_\ell)_{\ell>j}$ is a deterministic sequence. In B1 it may depend on the atom $A$, but not on later randomness; in particular it may not be defined through the random $n_\ell$. This matters for the sentence after Cor B4′ ("the same holds for ladder windows"). There, $\bar\varepsilon_\ell=\max(\theta,\vartheta)^{(n_\ell-n_{\ell-1})/2}$ would be random and must be replaced by a deterministic bound, e.g. from $n_\ell-n_{\ell-1}\ge(r-1)n_{\ell-1}$ and a deterministic lower bound on $n_{\ell-1}$.
- **F3 (claim summary).** The one-line summary of B1′ must keep the hypothesis $m_j^*>\sqrt{\Pi Q_j\delta}$. The report's §2 has it, but the summary passed to this check did not.
- **F4 (wording).** Replace "This is why two-step predictability is required" by "This is where two-step predictability is used". Optionally cite Remark V1.
- *Cosmetic.* The symbol $\delta$ is used both for the failure probability and for signed digit strings (§1, §5). B1's "proof" is a checklist against R3M C3, not a self-contained proof. That is acceptable only because C3 is fully proved and checked; §2.3 above writes the checklist out in full.

## 4. Obstructions (BRIEF.md) and what B1 does not do

- B1 and B1′ are conditional. Their hypotheses (FE for one atom, or $m^*_j>\sqrt{\Pi Q_j\delta}$) contain the whole difficulty.
- Theorem 3.6 (no residue-class criterion): B1 is a measure statement on cylinders with a hypothesis on a stopping time. It certifies no residue class.
- Prop 11.12 (per-window Cauchy–Schwarz fails): B1 uses Prop C2, the two-window inequality, unchanged. $\chi^2_j$ enters only once, at the first window.
- Prop 11.15(b) / N4 (infinite annealed mean): B1 uses no annealed mean. FE is a probability statement about $\tau_j$.
- Barrier lemmas: unaffected, since B1 makes no deterministic claim.
- M4B §7 (initial phase): B1′ does not close it. It turns the requirement into "$m^*_j>\sqrt{\Pi Q_j\delta}$ at some $j$ with small $\delta$", a lower bound on a Paley–Zygmund ratio at large $j$. M4B correctly lists this as open.

## 5. Numerical tests (exact arithmetic unless stated)

All runs: `code/round4/verify_M4B_logic/batch.sh` (and the t1 loop, the $p=7$ t2 run copied into `t2_atom_c2.log` from an earlier shell with the same code, and the timed-out $p=7$ t3 re-run), logs in `data/round4/verify_M4B_logic/` with the command line at the top. The helpers `PAdic`, `products`, `extend`, `alive_from_scratch`, `subset_sum_law` and `collision` are copied unchanged from the validated round-3 checker library `code/round3/check_R3M/ck_lib.py`. Two window rules are used: the M4B example ladder rule ($r=1.25$, $R=12$, $T=24$, $C'=1$) and an arbitrary two-step "hash" rule ($n_{\ell+1}=n_\ell+1+h(x\bmod p^{m_{\ell-1}})\bmod5$).

**t1 — Lemma B1a and the measurability of $B_\ell$** (`t1_partition.log`, `t1_partition.py`).
- *Setup.* Random $x$ with 220 $p$-adic digits; half of them carry a forced gate $v(x+i)=s\le12$ at a random $i\le n_L$. Random $z\ne0$. Everything is recomputed from scratch at $x'$.
- *Runs.* Both rules at $p=3$ ($n_0,n_1=6,8$, $L=7$), $p=5$ ($10,13$, $L=6$) and $p=7$ ($14,18$, $L=6$); 400 samples each.

| check | two-step rules | one-step rule (negative control) |
|---|---|---|
| (a) $M_{n_\ell}<m_\ell$, $m_\ell\ge m_{\ell-1}$ | 0/17 600 | 0/8 800 |
| (b) Lemma B1a: $n_0..n_{\ell+1}$ and $m_0..m_\ell$ unchanged at $x+p^{m_\ell}z$ | 0/15 200 | 0/7 600 |
| (c) $n_{\ell+1}$ unchanged at $x+p^{m_{\ell-1}}z$ (two-step predictability) | 0/12 800 | **1 559/6 400 fail** (detected) |
| (d1) first event of $B_\ell$ unchanged at $x+p^{m_{\ell-1}}z$ | 0/12 800 | 0/4 841 |
| (d2) $\varepsilon_\ell$ unchanged (exact), $K\le$ cap | 0/6 983 | 0/3 327 |

Lemma B1a also holds for one-step rules, as it should: its proof needs only that $n_{\ell+1}$ is constant on $A_\ell$.

**t2 — martingale and C2 steps on atoms of $\mathcal G_{\ell-1}$ with random times; one-step controls** (`t2_atom_c2.log`, `t2_atom_c2.py`).
- *Setup.* An atom $C=x+p^{m_{\ell-1}}\mathbb Z_p$ with a random $\ell\in[1,L-1]$, (5.2), $D_{\ell-1}\ge1$ and $Z^0_{n_{\ell-1}}\ge1$. Every $w\bmod p^K$ is enumerated, all in exact `Fraction`s.
- *Runs.* $p=3$ ($n_0,n_1=6,9$): hash 80 atoms, ladder 80 + 150 atoms. $p=5$ ($15,20$): hash 12, ladder 10. $p=7$ ($21,28$, ladder): 2 atoms. A larger $p=7$ run was killed for budget; see the log.
- *Totals over the 334 atoms:*
  - the window times recomputed at sample points of $C$ agree: 0/5 723 failures;
  - $c_N\mathbb E_CZ^0_N=c_nZ^0_n$: 0/334;
  - $c_{N'}\mathbb E_{C'}Z^0_{N'}=c_NZ^0_N$ on every $\mathcal G_\ell$-atom: 0/1 078;
  - Prop C2 with the rule's random $n_{\ell+1}$: 0/334 (max ratio LHS$/(\varepsilon M^2)=1$);
  - **exact equality** for single slope-0 parents: 30/30.
- *One-step controls (Remark V1):*
  - C2 for each fixed candidate end $N+h$: 0/1 764 failures;
  - monotonicity of $\mathrm{Var}_{C'}$ in the end time: 0/4 461;
  - the one-step choice bounded through the cap: 0/334.
  - The **naive one-step bound** (averaging $\varepsilon$ of the chosen window over $C'$) **fails in 33/334 atoms**. Those are 33 of the 40 atoms where the greedy choice is not constant; the largest ratio is $1.2586$, at $p=3$. So the cap $N^*$ in V1 is necessary, and the test is sensitive.

**t3 — the whole chain of B1′ (and B1 per atom), exact, at a finite horizon $L$** (`t3_global_finite.log`, `t3_global_finite.py`).
- *Setup.* $j=0$. **All** atoms of $\mathcal G_0$ are enumerated exactly: 8 073 at $p=3$ ($n_0,n_1=12,15$) and 5 750 at $p=5$ ($15,20$). The unresolved measure is $7.6\cdot10^{-10}$ and $3.1\cdot10^{-14}$; those cylinders have $p^{v}>e(n_0-1)!$ and are non-admissible by Observation G.
- $S=\mathrm{adm}_0$, with 42 atoms ($\mu=0.0951$) at $p=3$ and 150 atoms ($\mu=0.2312$) at $p=5$. Inside them every $\mathcal G_1$-, $\mathcal G_2$- and $\mathcal G_3$-atom is enumerated.
- *Checks.* $\mathbb E\tilde M_\ell=m^*$, $a_0\le\dots\le a_L$, $a_1\le Q$, $a_{\ell+1}\le a_\ell+\bar\varepsilon a_{\ell-1}$, Cauchy–Schwarz, $\mathbb EY_L=m^*-\mathbb E[\tilde M_L\mathbf 1_{\tau\le L-1}]$, Paley–Zygmund, the final bound, and the per-atom B1 bound.

| $p$ | rule | $\bar\varepsilon$ | $L$ | $\delta$ | $m^*$ vs $\sqrt{\Pi Q\delta}$ | final bound | exact $\mu(Y_L>0)$ | failures |
|---|---|---|---|---|---|---|---|---|
| 3 | hash | 1/4 | 2 | 0.0123 | 0.0625 > 0.0470 | 0.00135 | 0.0826 | 0 |
| 3 | ladder | 1/4 | 2 | 0.0494 | 0.0625 ≤ 0.0939 | (hypothesis fails) | 0.0456 | 0 |
| 3 | hash | 1/10 | 2 | 0.0498 | 0.0625 ≤ 0.0885 | (hypothesis fails) | 0.0452 | 0 |
| 3 | hash | 1/4 | 3 | 0.0412 | 0.0625 ≤ 0.0959 | (hypothesis fails) | 0.0538 | 0 |
| 3 | ladder | 1/10 | 3 | 0.0910 | 0.0625 ≤ 0.1254 | (hypothesis fails) | 0.0040 | 0 |
| 5 | hash | 1/4 | 2 | 0.0560 | 0.0811 > 0.0624 | 0.00503 | 0.1752 | 0 |
| 5 | ladder | 1/4 | 2 | 0.0896 | 0.0811 > 0.0789 | 6.8e-5 | 0.1416 | 0 |
| 5 | hash | 1/100 | 2 | 0.0772 | 0.0811 > 0.0658 | 0.00414 | 0.1540 | 0 |

- Every step of the chain holds exactly in every run. The $L^2$ recursion has slack between $5\cdot10^{-4}$ and $0.026$. The Paley–Zygmund ratios are small (0.004–0.09) at these tiny $n$, as expected.
- The per-atom bound was checked on 9–143 atoms per run with no failure. At these horizons, however, every atom with $\delta_A\Pi_A<1$ has $\delta_A=0$, so the per-atom check is non-trivial only through $\Pi_A$. This is M4B §7's observation that $\varepsilon_{j+1}$, and here also $\varepsilon_{j+2}$, is constant on the atom.
- The batch used `t3_global_finite.py` before two later edits: the $m_0$ cap is now applied before the path search, and a diagnostic line was added. Neither changes any output when `mcap=0`.
- At $p=7$ the global enumeration ($n_0=21$) did not fit the budget: one run was killed and one timed out, both logged. $p=7$ is covered by t1, t2 and t4.

**t4 — the ingredients of "$Q_j<\infty$"** (`t4_Qbound.log`, `t4_Qbound.py`).
- *Setup.* Haar samples plus forced gates up to the Observation G limit; $p=3$ with $n=12,18,24,30$ (300 samples), $p=5$ with $n=15,20,25$ (200), $p=7$ with $n=21,28$ (100).
- *Checks.* Observation G on $\{Z^0_n\ne0\}$, $V_n<n/(p-1)+M_n$, and $c_nZ^0_n\le p^{V_n}/2\le\mathrm{Bnd}(n)$: 0 failures.
- $\log_{10}\mathrm{Bnd}(n)$ grows from 10.6 to 38.2 ($p=3$, $n=12\to30$). That is the dependence on $n_j$ that F1 is about.
- The observed $\max c_nZ^0_n$ is between 0.55 and 5.7. That is far below the bound and says nothing either way about $\operatorname{ess\,sup}$ or the second moment for unbounded $n_j$. It is reported only as context.

## 6. What remains open

- Nothing in B1/B1′ itself, after F1–F3.
- Whether $Q_j<\infty$ for rules with unbounded $n_j$. This is equivalent in spirit to $L^2$-boundedness and should not be assumed.
- FE, i.e. M4B's (S_B), and the initial-phase gap of M4B §7. These are unchanged by this check.

## 7. Credit

- Theorem C3, Prop A, Cor A′, Prop B, Lemma C1, Prop C2: track R3M (round 3).
- Observation G and the validated helper library: the round-3 checker of R3M.
- Theorem B1/B1′, Lemma B1a and the example ladder rule: track M4B (round 4).
- The $p=2$ quenched martingale with stopped-martingale bookkeeping: tracks R1b (round 2) and R3Q (round 3).
- Classical tools: Doob's $L^2$ martingale convergence, conditional Jensen, Paley–Zygmund, Cauchy–Schwarz.
- Remark V1 and the tests of §5 are this check's own.
- AI-assisted session; not checked by a human.
