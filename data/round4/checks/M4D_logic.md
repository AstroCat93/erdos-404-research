# Logic check of round-4 track M4D: Lemma L, Theorem F and Corollary F1

Date: 2026-10-14. Lens: LOGIC. Track: `verify_M4D_logic` (round 4).
- **Checked:** `data/round4/reports/M4D.md` §1 ((F1), (F2)) and §2 (Lemma L, Theorem F, the two special cases, Corollary F1). I also checked the parts of §2 that the claim's framing leans on: Prop F2(a),(b), Cor F3, and "How Theorem F sits relative to the obstructions". I read `code/round4/M4D/lift_lemma_check.py` and `thmF_e2e.py` with their logs; my code shares nothing with them.
- **Definitions re-read:**
  - note.md §1.2 ($S_B$, $g_p$), §1.3 ($K_p$, Prop 1.2) and §1.4 (Tao's predicate; Lemma 1.3(iii));
  - note.md §10.3 (R2b's Theorem 10.12 and Cor 10.13);
  - `data/round3/reports/R3M.md` §1 ((F1), (F2), Lemma 1(a)).
- **Checker code** (new, independent), in `code/round4/verify_M4D_logic/`:
  - library `vF.py`;
  - tests `t1_lemmaL.py`, `t2_recursion.py`, `t3_thmF_chain.py`, `t4_corF1_exhaustive.py`;
  - the logged batch `batch.sh` with `runlog.sh`, and a `README.md`.
- **Logs:** `data/round4/verify_M4D_logic/t1_lemmaL.log`, `t2_recursion.log`, `t3_thmF_chain.log`, `t4_corF1.log`. Every run starts with its command line and start time and ends with its exit code and wall time.
- **Budget:** one core, `nice -n 10`, 3248 s of wall time in total, peak memory below 1 GB. The total includes two runs killed by hand (591 s and 615 s, see §3) and one accidental duplicate (148 s).

## Headline

**Verdict: confirmed-with-fixes.** Lemma L, Theorem F and Corollary F1 are correct as M4D states them in §2. I re-derived every step:
- every hypothesis used is stated or forced;
- the quantifier order is right;
- the measurability argument in Corollary F1 is right;
- the step "survival implies $x\in K_p$" is right.

The claim involves no probability beyond a union bound: no filtration, stopping time, martingale or Paley–Zygmund step. Exact tests at $p=3,5,7,11,13$ found no counterexample to anything the proof uses:
- Lemma L: 31 310 alive parents, every child found by brute force;
- the strong form $|T_\ell|\ge\theta_\ell p^{D_\ell}$ of Theorem F: 1512 (sample, $\theta$-schedule) pairs that satisfy the hypotheses, from 705 exact chains;
- Corollary F1 (finite horizon): exhaustively over about 1.5·10^5 cylinders, with local constancy re-checked at 7747 random far points.

The tests can fail: the wrong-unit control breaks Lemma L for 964 parents, and "(I) alone ⇒ alive" fails 9 times.

**The fixes all concern the one-line form of the claim**, plus hypotheses that M4D states only once, in §1:
- **(a)** "θ = 1 recovers R2b's Theorem 10.12" overstates. $\theta\equiv1$ gives only the **(ii)⇒(i) direction** of Theorem 10.12, chained, and only at input level $D=\delta$. It does not give the converse (i)⇒(ii) (worst-case necessity, R2b's Lean-checked core), nor other input levels. M4D's own §2 says this correctly ("the chained form of its implication (ii)⇒(i)").
- **(b)** Implicit hypotheses that should be explicit:
  - $x$ is not a negative integer (a null set). Otherwise $\pi_n(x)=0$ and targets and jumps are undefined.
  - The times form a strictly increasing **infinite** sequence, so $n_\ell\to\infty$; (II$_\ell$) is needed for **every** $\ell>j$.
  - Lemma L needs a parent **alive at $n$**, and uses $W'$ only through the integer $D'\ge0$.
  - Corollary F1 needs Borel events. Deterministic times and $\theta$'s qualify, and so do locally constant $\theta$'s such as $\theta_\ell=p^{-D_\ell}$.
- **(c)** Nothing restricts $p$ to be odd, or the slope, or the regime. The theorem holds verbatim for every prime. Also, $\theta_\ell\in(0,1]$ need not be assumed: the hypotheses force it (§2.3).

**What this does not do.** Corollary F1 converts $\mu(K_p)>0$ into LIFT ($\sum_{\ell>j}\mu(A\setminus L_\ell)<\mu(A\cap I_j)$), which is **unproved**. M4D labels it so everywhere. Nothing here proves $\mu(K_p)>0$ for any $p$.

| item | M4D label | verdict |
|---|---|---|
| (F2) (one-window step, target formula, converse) | standing fact (R3M) | **confirmed**: re-derived; 0 failures for the 31 310 parents of t1 (all their children) |
| (F1) (survival $\Rightarrow x\in K_p$) | standing fact (R3M) | **confirmed**: needs $V_n\ge v(n!)$, i.e. $x$ not a negative integer |
| Lemma L | proved | **confirmed**: re-derived; t1: 0 failures for 31 310 parents, including $D=0$ (34 samples) and $D'=0$ (45 samples) |
| Theorem F | proved | **confirmed**: re-derived; t3: 0 violations of $\lvert T_\ell\rvert\ge\theta_\ell p^{D_\ell}$ in 1512 cases |
| special case $\theta=p^{-D_\ell}$ = chained Tao block lemma | (remark) | **confirmed** |
| special case $\theta\equiv1$ = R2b Theorem 10.12 | (remark) | **correct as M4D §2 words it** ((ii)⇒(i), chained); the one-line claim overstates it, fix (a) |
| Corollary F1 | proved | **confirmed**: union bound plus Borel events; t4: exact finite-horizon inequality and pointwise implication on about 1.5·10^5 cylinders, 0 local-constancy mismatches |
| "no second moment, no independence" | (remark) | **confirmed** |
| LIFT | hypothesis, not proved | correctly labelled; unproved |

## 1. The claim, with every hypothesis explicit

The claim passed to this check (M4D §2):
- **Lemma L.** The children's targets modulo $p^{D'}$ are a bijective affine image of the parent's fibre lifts $\mathrm{Lift}(r)=\{s\in\Sigma\bmod p^{D+D'}:s\equiv r\ (p^D)\}$.
- **Theorem F.** If (I) $T_j$ meets $G_j$ and (II$_\ell$) $|G_\ell|>(1-\theta_\ell)p^{D_\ell}$ for every $\ell>j$, then $x\in K_p$. Minimal $\theta$ recovers Tao's block lemma; $\theta=1$ recovers R2b's Theorem 10.12.
- **Corollary F1.** $\mu(K_p\cap A)\ge\mu(A\cap I_j)-\sum_{\ell>j}\mu(A\setminus L_\ell)$, so LIFT implies $\mu(K_p)>0$. No second moment, no independence.

Restated with everything that is used:

**Standing.**
- $p$ is any prime. Oddness is never used; everything below also holds at $p=2$.
- $x\in\mathbb Z_p$ is **not a negative integer**, so $\pi_n(x)\neq0$ for every $n$. This is a null set. M4D states it once, in §1; the one-line claim omits it.
- $\pi_0=1$, $\pi_j(x)=\prod_{i\le j}(x+i)$ and $V_n=v(\pi_n(x))$.
- A path of length $n$ is $e\in\{0,1\}^n$ with $e_0=1$, and $S_e=\sum_{j<n}e_j\pi_j$; this is $S_B$ of note §1.2 with $B=\{j\ge1:e_j=1\}$.
- $e$ is alive at $n$ iff $v(S_e(x))\ge V_n$. Its target is $\tau_n(e)=-S_e/\pi_n\in\mathbb Z_p$.

**Lemma L.** Data:
- consecutive windows $W=[n,N)$ and $W'=[N,N')$ with $n<N<N'$, jumps $D=V_N-V_n\ge0$ and $D'=V_{N'}-V_N\ge0$, and $K=D+D'$;
- the window elements $y_i=\pi_{n+i}/\pi_n$ and sums $Q_f=\sum f_iy_i$, with $\Sigma=\{Q_f\bmod p^K\}$;
- the unit $u=\pi_N/(p^D\pi_n)$;
- a path $e$ **alive at $n$**, with exact target $\tau$, and $r=\tau\bmod p^D$.

Claim: $\lambda(s)=u^{-1}(\tau-\tilde s)/p^D\bmod p^{D'}$ is a well-defined bijection $\mathrm{Lift}(r)\to C(e)=\{\tau_N((e,f))\bmod p^{D'}:(e,f)\text{ alive at }N\}$. Note that $W'$ enters **only through the integer $D'$**; any $D'\ge0$ works.

**Theorem F.** Data:
- a strictly increasing **infinite** sequence of times $n_j<n_{j+1}<\cdots$ (arbitrary functions of $x$), with windows $W_\ell=[n_\ell,n_{\ell+1})$ and jumps $D_\ell$;
- $\mathrm{Lift}_\ell$ formed for the pair $(W_\ell,W_{\ell+1})$, i.e. modulo $p^{D_\ell+D_{\ell+1}}$, and $\varphi_\ell(r)=|\mathrm{Lift}_\ell(r)|/p^{D_{\ell+1}}$;
- $T_\ell=\{\tau_{n_\ell}(e)\bmod p^{D_\ell}:e\text{ alive at }n_\ell\}$, **all** alive paths, of every slope;
- reals $\theta_{j+1},\theta_{j+2},\ldots\in(0,1]$ (arbitrary functions of $x$), and $G_\ell=\{r:\varphi_\ell(r)\ge\theta_{\ell+1}\}$.

Hypotheses (I) and (II$_\ell$) for **all** $\ell\ge j+1$. Conclusion: $|T_\ell|\ge\theta_\ell p^{D_\ell}$ for all $\ell\ge j+1$, hence $x\in K_p$.

**Corollary F1.** In addition:
- $A$ is Borel;
- the events $I_j$ and $L_\ell$ are Borel. This holds for deterministic times and $\theta$'s, and also for $\theta$'s that are locally constant functions of $x$, such as $\theta_\ell=p^{-D_\ell}$.

## 2. Line-by-line check

### 2.1 The two standing facts

- **(F2) [confirmed].**
  - $S_{(e,f)}=S_e+\sum_{i<H}f_i\pi_{n+i}=S_e+\pi_nQ_f=\pi_n(Q_f-\tau_n)$, so $v(S_{(e,f)})=V_n+v(Q_f-\tau_n)$, and this is $\ge V_N=V_n+D$ iff $Q_f\equiv\tau_n\pmod{p^D}$.
  - Then $\tau_N=-S_{(e,f)}/\pi_N=(\tau_n-Q_f)\pi_n/\pi_N=u^{-1}(\tau_n-Q_f)/p^D$, because $\pi_N/\pi_n=p^Du$.
  - Converse: $\pi_j/\pi_n\in\mathbb Z_p$ for $j\ge n$, so $p^{V_n}\mid\pi_j$, and $V_N\ge V_n$.
  - The only hypothesis used is $\pi_n(x),\pi_N(x)\ne0$.
  - (t1 tests the equivalence, and the target formula, child by child, with aliveness decided from the exact integer $S_{(e,f)}$ and $Q_f$ computed separately from the window elements.)
- **(F1) [confirmed].**
  - "For every $n$ some path of length $n$ is alive at $n$" gives $g_p(x)=\sup_Bv(S_B(x))\ge V_n(x)$ for every $n$.
  - $V_n(x)\ge v(n!)\to\infty$ (R3M Lemma 1(a), Legendre's count; it needs $x+i\ne0$). Hence $g_p(x)=\infty$, i.e. $x\in K_p$ (note §1.3).

### 2.2 Lemma L [confirmed]

I re-derived each of the four bullets.
- *Well defined.* Write $\tilde s$ for an integer representative of $s\in\mathrm{Lift}(r)$. Then $\tilde s\equiv r\equiv\tau\pmod{p^D}$, so $p^D\mid\tau-\tilde s$. Changing $\tilde s$ by $p^K$ changes $(\tau-\tilde s)/p^D$ by $p^{D'}$, and $u^{-1}\bmod p^{D'}$ exists because $u$ is a unit.
- *Into $C(e)$.* Pick $f$ with $Q_f\equiv\tilde s\pmod{p^K}$. Then $Q_f\equiv\tau\pmod{p^D}$, so $(e,f)$ is alive by (F2). Its exact target is $u^{-1}(\tau-Q_f)/p^D$, and $(\tau-Q_f)/p^D\equiv(\tau-\tilde s)/p^D\pmod{p^{D'}}$.
- *Onto.* By (F2), an alive child has $Q_f\equiv\tau\pmod{p^D}$, so $Q_f\bmod p^K\in\mathrm{Lift}(r)$.
- *Injective.* $u^{-1}(\tau-\tilde s)/p^D\equiv u^{-1}(\tau-\tilde s')/p^D\pmod{p^{D'}}$ gives $\tilde s\equiv\tilde s'\pmod{p^{D+D'}}$.

"Affine": $\lambda$ is the restriction to $\mathrm{Lift}(r)$ of the map $s\mapsto u^{-1}(\tau-s)/p^D$. That map is an affine bijection from the coset $r+p^D\mathbb Z/p^K$ (which has $p^{D'}$ elements) onto $\mathbb Z/p^{D'}$. So "bijective affine image of the fibre lifts" is exact. The lemma is a repackaging of (F2): it is (F2) applied to all $f$ at once, read modulo $p^{D'}$.

Edge cases:
- $D=0$: then $\mathrm{Lift}(0)=\Sigma$.
- $D'=0$: then $\lambda$ maps into $\mathbb Z/1$, and the lemma says "a child exists iff $r\in\Sigma\bmod p^D$".

Both are covered by the proof as written, and both occur in t1 (§3).

### 2.3 Theorem F [confirmed]

- **Base case $\ell=j+1$.** (I) gives $r\in T_j\cap G_j$, i.e. a path $e$ alive at $n_j$ with $\tau_{n_j}(e)\bmod p^{D_j}=r$ and $|\mathrm{Lift}_j(r)|\ge\theta_{j+1}p^{D_{j+1}}$.
  - Lemma L for the pair $(W_j,W_{j+1})$, i.e. with $D=D_j$ and $D'=D_{j+1}$, gives $|\mathrm{Lift}_j(r)|$ distinct values $\tau_{n_{j+1}}((e,f))\bmod p^{D_{j+1}}$ of alive paths.
  - These lie in $T_{j+1}$ by its definition. The moduli match: $T_{\ell+1}$ is taken modulo $p^{D_{\ell+1}}$, and the band of $\mathrm{Lift}_\ell$ is $D_{\ell+1}$.
- **Inductive step.** From $|T_\ell|\ge\theta_\ell p^{D_\ell}$ and (II$_\ell$): $|T_\ell|+|G_\ell|>\theta_\ell p^{D_\ell}+(1-\theta_\ell)p^{D_\ell}=p^{D_\ell}$. The inequality is strict because (II$_\ell$) is strict. So the two subsets of $\mathbb Z/p^{D_\ell}$ meet (pigeonhole), and the base-case argument applies.
- **Survival.**
  - $\theta_\ell>0$ gives $|T_\ell|\ge1$ for every $\ell\ge j+1$, so some path is alive at every $n_\ell$.
  - Since $(n_\ell)$ is a strictly increasing sequence of integers, $n_\ell\to\infty$, and every $n$ is $\le$ some $n_\ell$. The length-$n$ prefix of a path alive at $n_\ell$ is alive at $n$, by the (F2) converse applied to the window $[n,n_\ell)$.
  - (F1) then gives $x\in K_p$.

**Points checked specifically under this lens:**
- **Quantifiers.** The theorem is pointwise in $x$. Times and $\theta$'s may be arbitrary functions of $x$: nothing in the proof requires measurability or adaptedness, and no probability enters.
- **The range $\theta_\ell\in(0,1]$ is forced by the hypotheses.**
  - If some $\theta_\ell\le0$ ($\ell\ge j+1$), then (II$_\ell$) asks $|G_\ell|>p^{D_\ell}$, which is impossible.
  - If $\ell^*\ge j+1$ is the least index with $\theta_{\ell^*}>1$, then $G_{\ell^*-1}=\emptyset$, because $|\mathrm{Lift}|\le p^{D_{\ell^*}}$. So (I) fails (if $\ell^*=j+1$) or (II$_{\ell^*-1}$) fails (its right side is $\ge0$).
  - So the restriction in the statement costs nothing, and no hidden case is excluded.
- **No slope restriction, no linear regime, no condition on $M_n$.** $T_\ell$ ranges over all alive paths. Lemma L holds for every alive parent, whatever its slope and however deep the gates (the unit $u$ absorbs them).
- **One parent per window.** The proof follows a single parent per step. The weaker bound $|T_{\ell+1}|\ge\max_{r\in T_\ell}|\mathrm{Lift}_\ell(r)|$ is all it needs, and it holds unconditionally (t3, §3).
- **The strictness in (II$_\ell$) is used**, and is necessary for the pigeonhole step. With "$\ge$", $T_\ell$ could be exactly the complement of $G_\ell$.
- **The infinitely many hypotheses.** (II$_\ell$) is required for every $\ell>j$. A finite truncation proves only aliveness up to the last window, which is how t3 and t4 test it (finite horizon $L$).
- **Explicit constants.** None, apart from the threshold $(1-\theta_\ell)p^{D_\ell}$, which is exactly what the pigeonhole step needs.

### 2.4 The special cases

- **Minimal $\theta$, i.e. $\theta_\ell=p^{-D_\ell}$ [confirmed].**
  - $G_\ell=\{r:\mathrm{Lift}_\ell(r)\ne\emptyset\}=\Sigma_\ell\bmod p^{D_\ell}$, and (II$_\ell$) $\iff|G_\ell|=p^{D_\ell}$, i.e. $W_\ell$ covers its own jump.
  - (I) $\iff$ some parent alive at $n_j$ has a child at $n_{j+1}$, which is $P(x,n_{j+1})$ by the (F2) converse.
  - So Theorem F becomes "$P(x,n_{j+1})$ and every later window covers its own jump $\Rightarrow x\in K_p$". That is Tao's block lemma (note Lemma 1.3(iii)) iterated, in the $x\in\mathbb Z_p$ normal form.
  - These $\theta$'s depend on $x$; the theorem allows that.
- **$\theta\equiv1$ [confirmed as M4D's §2 states it; the one-line claim overstates it, fix (a)].**
  - $G_\ell$ is the set of complete classes, and (II$_\ell$) says $\Sigma_\ell$ contains a complete coset $c+p^{D_\ell}\mathbb Z/p^{D_\ell+D_{\ell+1}}$.
  - Translate R2b's Theorem 10.12 with carries $=-$targets, $\pi=p^{D_\ell}u_\ell$ (so $\delta=D_\ell$), input fullness level $D=\delta=D_\ell$, and output level $D'=D_{\ell+1}$. Its condition (ii) is then exactly (II$_\ell$) with $\theta=1$, and its conclusion (i) is $|T_{\ell+1}|=p^{D_{\ell+1}}$. Negation $T\mapsto-T$ preserves fullness.
  - So the $\theta=1$ case of Theorem F is the chained **(ii)⇒(i) direction** of Theorem 10.12, in the special case $D=\delta$.
  - It does **not** recover the converse (i)⇒(ii), which is the worst-case necessity statement and the content of R2b's Lean core `worst_case_iff`. Nor does it cover input levels $D\neq\delta$.
  - M4D §2 says this correctly ("the chained form of its implication (ii)⇒(i)"). The one-line claim "θ = 1 recovers R2b's Theorem 10.12" should say so too.

### 2.5 Corollary F1 [confirmed]

- **Inclusion.** Off the null set of negative integers, $A\cap I_j\cap\bigcap_{\ell>j}L_\ell\subseteq K_p\cap A$ by Theorem F.
- **Union bound.** By countable subadditivity, $\mu(A\cap I_j\setminus\bigcap_\ell L_\ell)\le\sum_\ell\mu(A\cap I_j\setminus L_\ell)\le\sum_\ell\mu(A\setminus L_\ell)$.
- **$K_p$ is Borel.** It is closed (note §1.3). Even without that, $\{g_p\ge G\}$ is open, so $K_p$ is a $G_\delta$.
- **Measurability of the events (deterministic times and $\theta$'s).** $I_j$ and $L_\ell$ depend only on finitely many objects:
  - the valuations $v(x+i)$ for $i\le n_{\ell+2}$;
  - the alive set and targets modulo $p^{D_\ell}$;
  - the window sums modulo $p^{D_\ell+D_{\ell+1}}$.

  Off the **finite** set $\{-1,\dots,-n_{\ell+2}\}$ all of these are locally constant. Concretely, everything is constant on $c+p^k\mathbb Z_p$ as soon as $v(c+i)<k$ for $i\le n_{\ell+2}$ and $V_{n_{\ell+2}}(c)\le k$; t4 uses exactly this criterion. So each event is a union of cylinders, up to a finite set, and is Borel. The same holds for locally constant $\theta$'s, e.g. $\theta_\ell=p^{-D_\ell}$.

  M4D's wording "finite outside the null set of negative integers" is correct. The negative integers are dense in $\mathbb Z_p$, but each event involves only finitely many of them.
- **No hidden probabilistic input.** There is no filtration, stopping time, optional stopping, martingale or Paley–Zygmund step. Those parts of the LOGIC lens are void for this claim.
- **"No second moment, no independence."** Confirmed. The only probabilistic tool is the union bound.

### 2.6 What the claim does not do, and the obstructions

Corollary F1 is an implication. **LIFT** ($\sum_{\ell>j}\mu(A\setminus L_\ell)<\mu(A\cap I_j)$) is not proved, and M4D does not claim it. M4D labels LIFT correctly throughout (headline, §2, §9).

I checked that the claim does not collide with the brief's obstructions.
- **Theorem 3.6 (nowhere density).** A deterministic criterion that certified a whole cylinder would contradict it. M4D's Prop F2(b) shows that the certified set has empty interior.
  - I checked F2(b)'s key step. If $v(x+i)\ge s$ at distance $d\ge1$ inside $W_{\ell+1}$, then $|\Sigma_{\ell+1}\bmod p^s|\le2^d$, because $y_{i'}\equiv0\pmod{p^s}$ for $i'\ge d$. So $|G_{\ell+1}|\le2^dp^{D_{\ell+1}-s}$.
  - (II$_\ell$) forces $G_\ell\neq\emptyset$, and then $\theta_{\ell+1}\le2^{H_\ell}p^{-s}$. So (II$_{\ell+1}$) fails once $p^s>2^d+2^{H_\ell}$.
  - I also checked the inductive construction (the choice of $\ell_{t+1}$ with $H_{\ell_{t+1}+1}>p^{s_t}$ guarantees $1\le d_{t+1}\le p^{s_t}<H$; the limit lies in the given cylinder and is not a negative integer). No error.
- **Prop 11.12 and Prop 11.15(b).** Not used: there is no second moment and no unbounded expectation.
- **Barrier lemmas (Theorem 3.10, Prop 11.23).** Respected. (II$_\ell$) for all $\ell$ involves unboundedly many digits of $x$, and the claim proves nothing deterministic about them.

Two remarks on F2, which is not part of the verified claim:
- F2(a)'s phrase "$\theta_{\ell+1}p^{D_{\ell+1}}\le2^{H_\ell}$ in every case" is correct: under (II$_\ell$), $|G_\ell|\ge1$ even when $\theta_\ell=1$.
- F2(c) is a **lower** bound on the failure probability, $\approx2^{-H_\ell}$ per window, i.e. the unavoidable deep-gate cost. It is not an upper bound, and it does not show that LIFT's failures are summable. M4D says so in F2(c) and §9.

## 3. Numerical tests (exact arithmetic; corroboration only, the verdict rests on §2)

Every test point $x$ is a **nonnegative integer**: a genuine point of $\mathbb Z_p$, never a negative integer. So every valuation, product and target is exact; there is no truncation error. The checker computes the alive-target sets by two routes that share no code with the window-sum route used for the lifts:
- brute force over all $2^{n-1}$ paths;
- a single-step carry recursion, $\tau\mapsto u^{-1}(\tau-f)/p^{v(x+n+1)}$ with $f\in\{0,1\}$.

t2 validates each against the other.

| test | what is tested | runs | result | negative control |
|---|---|---|---|---|
| t2 `t2_recursion.py` | brute force (all paths, no pruning) vs DFS with prefix pruning (the (F2) converse); target sets vs carry recursion (Python and numpy versions); $V_n\ge v(n!)$ | $p=3,5,7$, $n\le14$, random $x$ and forced gates ($p^4\mid x+6$ at $p=3$; $p^3\mid x+7$; $p^3\mid x+9$; $p^2\mid x+2$) | 1400 $(x,n)$ checks, 29 418 alive paths: **0 mismatches** | — |
| t1 `t1_lemmaL.py` | per alive parent, children by brute force over all $f\in\{0,1\}^H$ with aliveness from the exact integer $S_{(e,f)}$: (F2) aliveness $\iff Q_f\equiv\tau$; (F2) target formula; Lemma L set equality with $\lambda(\mathrm{Lift}(r))$; $\lvert C(e)\rvert=\lvert\mathrm{Lift}(r)\rvert$; $\lambda$ bijective on the whole coset; full lift $\iff$ children cover $\mathbb Z/p^{D'}$ | $p=3$: $(n,H,H')=(9,8,6),(12,10,6)$; $p=5$: $(10,9,8),(15,10,8)$; $p=7$: $(14,10,8),(21,12,10),(14,8,3)$; $p=11$: $(11,10,9)$; $p=13$: $(13,6,4)$; forced gates at window start, inside $W$ and inside $W'$ ($p^3\mid x+16$, $p^4\mid x+26$ at $p=7$; $p^4\mid x+12$ at $p=5$; $p^3\mid x+14$ at $p=3$) | **31 310 parents** (complete lifts 15 452, incomplete 15 858, childless 10 708), including 34 samples with $D=0$ and 45 with $D'=0$: **0 failures of any of the six checks** | with $2u$ in place of $u$: set equality fails for 235 of 501 ($p=5$) and 729 of 2469 ($p=7$) parents (only parents with incomplete lifts can fail) |
| t3 `t3_thmF_chain.py` | Theorem F, **strong form** $\lvert T_\ell\rvert\ge\theta_\ell p^{D_\ell}$ for $\ell=1..L$ under (I) and (II$_1$)..(II$_{L-1}$), finite horizon $L$. $\theta$ schedules, all in exact Fractions: optimal backward ($t_L=1$, $\lceil p^{D_L}/2\rceil$, $p^{D_L}$); constants $1,\frac34,\frac12,\frac14,\frac1{10}$; Tao ($p^{-D_\ell}$); 6 random draws per sample. Also the unconditional per-step bound $\lvert T_{\ell+1}\rvert\ge\max_{r\in T_\ell}\lvert\mathrm{Lift}_\ell(r)\rvert$, and the exact union identity $T_{\ell+1}=\bigcup_t\lambda_t(\mathrm{Lift}_\ell(t\bmod p^{D_\ell}))$ | $p=3$: times $[3,8,14,22,32,44]$, 150 samples; $p=5$: $[5,12,20,30,42]$, 120; $p=7$: $[8,18,30,44,60]$, 300; $p=7$: $[10,34,60,88]$, 25; $p=7$ with a forced gate $p^3\mid x+19$ (first element of $W_1$), 30; $p=11$: $[11,33,58,86]$, 40; $p=13$: $[13,39,65,91]$, 40 | 705 exact chains; hypotheses held in **1512** (sample, schedule) pairs: **0 violations**. Smallest ratio $\lvert T_\ell\rvert/(\theta_\ell p^{D_\ell})$ for a non-trivial $\theta$: 1.0013 ($p=13$, opt). Equality is attained in some cases (e.g. $p=7$, opt and random lattice $\theta$), so the bound is sharp. Per-step bound: 0 failures. Union identity: 2042 checks, 0 failures | NEG1, "(I) alone ⇒ alive at $n_L$": fails 6/55 ($p=3$) and 3/61 ($p=5$). NEG2, (II) with "$\ge$": never failed here, because the borderline configuration $T_\ell=G_\ell^c$ did not occur; the strictness is needed for the pigeonhole step, but these samples cannot show it |
| t4 `t4_corF1_exhaustive.py` | Corollary F1, finite horizon, **exhaustively** over all cylinders of $A$, with exact Fraction measures: $\mu(A\cap\text{ALIVE}_{n_L})\ge\mu(A\cap I_0)-\sum\mu(A\setminus L_\ell)$, with the undetermined mass $U$ charged against the inequality; the pointwise implication; **local constancy** (the Borel claim), by re-evaluating all events at random points $c+p^kw$ ($w<p^{30}$) of 5% of the determined cylinders | $p=7$: $A=\mathbb Z_7$, Tao $\theta$, times $[7,13,20,28]$; $p=7$: $A=3+7\mathbb Z_7$, $\theta=\frac12$; $p=5$: $A=\mathbb Z_5$, Tao and $\frac12$, $[5,10,16,23]$; $p=3$: $A=\mathbb Z_3$, Tao, $[3,7,12,18]$ | 154 011 determined cylinders (the duplicated run counted once): **pointwise violations 0**, **local-constancy mismatches 0** (7747 re-evaluations). The inequality holds in all 5 runs. It is non-trivial in three of them: right side $0.1327$ vs left side $0.6239$ ($p=7$, Tao); $0.3499$ vs $0.8438$ ($p=7$, $A=3+7\mathbb Z_7$); $0.0175$ vs $0.5231$ ($p=5$, Tao). At $p=3$ the hypotheses hold on a set of measure $0.041$ | — |

Computational record:
- Two runs were killed by hand. No result was taken from either; both are marked in `batch.sh` and appear in the logs with exit 143.
  - `t1_lemmaL.py 3 23 20 9 8 6 200 0 12 5`, after 591 s. The forced class $x\equiv-12\pmod{3^5}$ fixes $x\bmod p^{V_9}$, and that class has no path alive at $n=9$, so the sampling loop never ended. A draw guard was added, and the run was replaced by a forced gate $p^3\mid x+14$.
  - `t3_thmF_chain.py 13 38 15 6 13 39 65 91 --gate 41 3`, after 615 s at 0.9 GB. The forced gate raises the precision needed, and the exact target sets grew too large. The gated case is covered at $p=7$.
- I edited `batch.sh` while it was running, so the first t4 run was executed twice. Both copies are in `t4_corF1.log`, with identical results.
- The $p=7$ chain with windows $[10,34,60,88]$ censored 125 of 150 draws, those with $D_\ell+D_{\ell+1}>8$. This biases that row towards shallow gates. It does not affect the logic test, which is pointwise.

## 4. Fixes requested (all to the statement of the claim; the proofs need none)

1. Replace "θ = 1 recovers R2b's Theorem 10.12" by: "θ ≡ 1 recovers the chained (ii)⇒(i) direction of R2b's Theorem 10.12, at input level $D=\delta$". M4D §2 already says this.
2. State in Theorem F:
   - $x\in\mathbb Z_p$ is not a negative integer;
   - $(n_\ell)_{\ell\ge j}$ is strictly increasing and infinite;
   - (II$_\ell$) is required for every $\ell\ge j+1$.

   Optionally add that the hypotheses force $\theta_\ell\in(0,1]$.
3. State in Lemma L that the parent $e$ is alive at $n$, and that only the integer $D'=V_{N'}-V_N\ge0$ of the second window enters.
4. State in Corollary F1 that the events must be Borel (deterministic or locally constant times and $\theta$'s), and that the inclusion $A\cap I_j\cap\bigcap L_\ell\subseteq K_p$ holds off the null set of negative integers.
5. Optional: say that Theorem F and Lemma L hold for every prime $p$, $p=2$ included, with no condition on slopes or regime. This was tested at $p=3,5,7,11,13$.

## 5. What remains open

- **LIFT** (M4D §9 item 1) is the whole content of a proof of $\mu(K_p)>0$ by this route. Theorem F and Corollary F1 reduce $\mu(K_p)>0$ to a statement about window sums alone, with no population left in it: the failure probabilities $\mu(\neg L_\ell)$ must be summable, with sum below $\mu(A\cap I_j)$. This is an $L^0$, barrier-type statement about the digits of unit parts up to the next window's jump.
- Prop F2(c) gives only a **lower** bound ($\approx2^{-H_\ell}$ per window) on what LIFT must pay for deep gates. Upper bounds for moderate-depth gates, and for non-gate structure, are not available.
- My t3 run with a forced depth-3 gate at the first element of $W_1$ ($p=7$, windows of length 10–16) defeated every $\theta$-schedule in 30 of 30 samples, although all 30 survived. This agrees with M4D's §7.2 observation that the criterion fails from a threshold depth $s^*(H)$ that grows with $H$. It is the quantitative obstacle any proof of LIFT must overcome.
