# Adversarial check of track R3M (round 3): odd primes, Haar measure of $K_p$

Date: 2026-10-13. Checker: `check_R3M`, round 3. This is the second checker instance; the first was cut off by the external spending limit.
Report checked: `data/round3/reports/R3M.md`. Track code and logs: `code/round3/R3M/`, `data/round3/R3M/`.
Checker code: `code/round3/check_R3M/`. Checker logs: `data/round3/check_R3M/`. Scratch: `/tmp/r3_check_R3M/`.
Budget used: about 65 core-minutes on one core, under `nice -n 10`, with at most one heavy job at a time. Every exact or heuristic run is listed in §4.

## Verdicts at a glance

| id | R3M label | verdict | one line |
|---|---|---|---|
| Lemma 1 | proved | **confirmed** | All five parts are correct as stated. Hypothesis $x+i\ne0$ is needed and is stated. |
| Lemma 2 | proved | **confirmed** | The Taylor and $(1+E)^{-1}$ argument is correct. The modulus $p^{m-M_n}$ is right, and one digit more fails in 33–68 % of cases. |
| Prop A | proved | **confirmed** | Each use of (W1)–(W3) is checked. Exact tests pass, including at the boundary $D+L=m-M_n$. |
| Cor A′ | proved | **confirmed-with-fixes** | The identity is correct. The phrase "$c_n\to0$" (results table, headline) holds only for a.e. $x$. |
| Prop B | proved | **confirmed-with-fixes** | (i)–(iii) are correct, and the equality case $\lvert P\rvert=1$ is now tested exactly. A remark after the proposition ("never independent") is unproved and false at the stated generality. |
| Prop N | obstruction (proved) | **confirmed** | The shell bound, the minimiser and $r\le p$ are correct. |
| Lemma C1 | proved | **confirmed** | Well-definedness of $g$, $\hat g$, the mean-0 statement and CS+Parseval are all correct. |
| Prop C2 | proved | **confirmed** | Proof correct. For a single parent the proof is lossless, and the predicted **exact equality** holds in 95/95 cases under (5.2) ($p=3,5,7$, 16 of them at its boundary). It also holds in 47/47 cases outside (5.2). |
| Thm C3 | proved (hyp. FE unproved) | **confirmed** | Checked: partition, filtration, stopping time, martingale, $L^2$ recursion, the step "survival ⇒ $K_p$", and Paley–Zygmund. The theorem is conditional on FE, as labelled. |
| Lemma C4 | proved | **confirmed-with-fixes** | The lemma is correct. The remark after it ("tiny for most atoms") holds only for $n_j$ large. For moderate $n_j$ the lemma's hypothesis on $A$ fails for every atom tested. |
| Lemma C5 | proved | **confirmed** | The first-nonzero-index decomposition is correct. The identity is exact in 120/120 new cases. |
| Remark C6 | sketch | **confirmed** (as a sketch) | Honestly labelled. The quoted percentages are shares of an 80-sample mean of a variable whose true mean is infinite (Prop N3); the report should say so. |
| Prop N3 | negative (proved) | **confirmed-with-fixes** | $\int\Lambda_t\,d\mu=\infty$ is proved. The glosses "averaged FE cannot be obtained naively / needs truncation" (headline 5, table) and "FE needs $\kappa_\ell\to0$" rest on numerics and should carry [heuristic]. |
| §7 | heuristic | **confirmed-with-fixes** | Labelled heuristic. Every number spot-checked matches the logs, and my independent Monte Carlo agrees. $\mathbb E[(M^0)^2]$ is heavy-tailed: estimates vary by up to ×1.5. The "Paley–Zygmund bound" column needs standard errors and a caveat. |

No [proved] item is wrong. Two wording overstatements need fixing (Cor A′, the independence remark), and three labels or scopes need fixing (Lemma C4 remark, the N3 consequences, the §7.1 PZ column). §3 adds one new observation (G, proved and exactly tested). It explains the support of the slope-0 population and cuts off the deep-gate tail of $\mathbb E[(M^0_n)^2]$.

## 1. Method

1. **Line-by-line reading** of every proof in R3M §§1–5, done independently of the first checker instance. For each step I recorded which hypothesis it uses (§2).
2. **Exact tests**, in three groups:
   - **The first instance's tests** (`ck_lib.py`, `ck_propA.py`, `ck_propB.py`, `ck_C1C2.py`, `ck_C5_N3_C4.py`). They were written from the report's statements and share no code with `code/round3/R3M/`. I read them critically before reusing them, then completed the runs that had been cut off.
   - **Their base.** `ck_lib.py` (DFS of alive paths with prefix pruning) is validated against brute force over all $2^{n-1}$ paths: 4392 alive paths, 0 failures (`validate_lib.log`). The prefix pruning is justified by (F2): if $e$ is alive at $N$, every prefix is alive.
   - **New tests by this instance:**
     - `ck_lemma12.py`: Lemma 1 and Lemma 2.
     - `ck_edge.py`: equality cases of Prop B and Prop C2, and boundary or outside cases of (W2), (5.2).
     - `ck_C3_struct.py`: partition and measurability claims in Thm C3, (F1) with integer factorials, Lemma C4's union bound.
     - `ck_gate_kill.py`: Observation G.
     - `ck_indep_search.py`: the independence remark.
3. **Heuristic probes** of §7.1:
   - an independent Monte Carlo of $M^0_n=c_nZ^0_n$ (`ck_mc_M.py`);
   - importance sampling over gate depth (`ck_deepgate_M2.py`), which looks for second-moment mass that plain Monte Carlo cannot see.

The tests try to break the statements in three ways:
- exact rational identities wherever the statement is an identity;
- the sharp equality cases that the proofs predict, which catch wrong constants;
- boundary and outside-hypothesis runs, which show whether the tests are sensitive.

## 2. Line-by-line audit

**(F1), (F2).**
- (F2) is correct. $S_e=S_{(e,f)}-\sum f_{j-n}\pi_j$ with $v(\pi_j)\ge V_n$. Also $S_{(e,f)}=\pi_n(Q_f-\tau_n)$, and $\tau_N=(\tau_n-Q_f)\pi_n/\pi_N$.
- (F1) is correct. $S_e(x)=1+\sum_{j\in B}\pi_j(x)$ with $B=\{j\ge1:e_j=1\}$, and $g_p(x)=\sup_Bv_p(1+\sum_{b\in B}\pi_b(x))$ (note §1.2). Alive at $n$ gives $g_p(x)\ge V_n(x)\ge v(n!)\to\infty$ for $x$ not a negative integer.
- New check with natural numbers $a$ (`C3struct.log`, `F1` mode). For 694 926 alive paths at $p=3,5,7$:
  - $v_p(a!+\sum_{j\in B}(a+j)!)=v_p(a!)+v_p(S_e(a))\ge v_p(a!)+V_n(a)\ge v_p(a!)+v_p(n!)$,
  - with exact factorials, and 0 failures.

**Lemma 1.**
- (a) Legendre count. Correct.
- (b) At most $\lceil n/p^\ell\rceil\le n/p^\ell+1$ multiples of $p^\ell$, and none of $p^{M_n+1}$. The inequality is in fact strict. Correct.
- (c) Correct.
- (d) $\pi_j^{[i]}=\pi_j\,e_i(1/(x+k))$. Correct; it needs $x+k\ne0$, which is stated.
- (e) Correct.
- Numerics (`lemma12.log`, $p=3,5,7$): (a), (b) 7200 cases each; (c) 147 600; (d) 720, with $\pi_j^{[i]}$ computed from the integer coefficients of $\pi_j(X)$; (e) 720 exact polynomial identities. 0 failures.

**Lemma 2.**
- (a) Correct, since $v(x+i)\le M_N<m$.
- (b) This holds for any base point $x_0\in C$, which matters for Prop C2, Step 1. Checks:
  - $\pi_n(x')=\pi_n(x_0)(1+E)$ with $v(E)\ge m-M_n\ge1$;
  - the bracket is in $\mathbb Z_p$ because $e$ is alive at $x_0$;
  - $(1+E)^{-1}\equiv1$ modulo $p^{m-M_n}$.
- Numerics: 103 305 (path, $w$) pairs, 0 failures. The congruence also holds modulo $p^{m-M_n+1}$ in 13514/20280, 14639/33843 and 18181/49182 cases. So the modulus is not generously loose and the test is sensitive.

**Prop A.**
- Setup. $D\ge\lfloor(N-n)/p\rfloor\ge L$ uses (W1) and Lemma 1(c). Slope class constancy on $C$ uses $L<m$, which follows from (W3).
- (i) $v(\pi'_j(x'))\ge V_j(x')-M_j\ge m-M_N>L$ for $n\le j<N$, using (W3) and Lemma 1(d) at $x'$. Both directions of the inheritance follow. Correct.
- (ii) needs $\lambda\le m-M_n$, which follows from (W2). Correct.
- (iii) Four points, all checked:
  - $t(w)\equiv\tau_0-p^\lambda\beta w$ modulo $p^{D+\lambda}$ needs $D+\lambda\le m-M_n$ (W2);
  - $q_f$ is constant modulo $p^{D+\lambda}$ (needs $D+\lambda\le m$);
  - $u$ is constant modulo $p^\lambda$ (needs $m-M_N>\lambda$, from (W3));
  - the two cases $q_f\not\equiv\tau_0$ and $q_f\equiv\tau_0$ (mod $p^\lambda$) use $D\ge\lambda$; the bijection $z\leftrightarrow s$ is right; (2.1) needs $N-n\ge p\lambda$, from (W1).
- Remark on (W3). It is implied by (W2) whenever $M_N=M_n$ and $D\ge1$. It can bind only when the deepest gate of $[1,N]$ lies inside the window. This is why no (W3)-boundary sample turned up in the runs.
- Numerics:
  - `propA.log` (first instance): 1388 parents and 4892 (parent, state) identities at $p=3,5,7$, slopes 0–3; 0 failures.
  - The non-vacuity control (W1–W3 dropped) gives failures in 54/215 parents.
  - New boundary runs (`edge.log`). At $D+L=m-M_n$ exactly: 78 parents, 198 states, 0 mismatches, at $p=3$ ($L=1,2$), $p=5$ and $p=7$. One digit outside (W2): still exact in 30/30, so (W2) is sufficient but not sharp. That is harmless.

**Cor A′.**
- The decomposition of $P^{1,L}_N(x')$ into children of $P^{1,L}_n(x)$ is (i).
- $\rho_N$ is constant on $C$ since $\lambda<m$. Also $\sum_sa_N(s)=1$, and $c_N2^{N-n}p^{-D}=c_n$.
- Correct. Exact: 36/36 (`propA.log`).
- **Fix 1 (wording).** The results table ("$c_n=2^{-n}p^{V_n}\to0$") and headline item 1 ("exponentially decaying normaliser") should say "for a.e. $x$". Remark 1 says "on the good set where $M_n=O(\log n)$", which is correct. But $c_n\not\to0$ for some $x$. Take $i_{k+1}=i_k+p^{k i_k}$ and $x=\lim(-i_k)$. Then $M_{i_k}\ge k\,i_k$, so $c_{i_k}\ge2^{-i_k}p^{k i_k}\to\infty$. No proof depends on this.

**Prop B.**
- (i) uses Lemma 2(b) modulo $p^{m-M_n}\supseteq p^D$ (W2′), and $Q_f(x')\equiv Q_f(x)$ (mod $p^D$) since $D\le m$.
- (ii) The inverse DFT, the substitution $\eta=\beta_e\xi$ (a bijection for each $e$), Parseval over $w\bmod p^D$, $c_NTp^{-D}=c_n$, and Cauchy–Schwarz are all correct.
- (iii) Correct.
- Remark B′ needs $D\le m$, which holds. Correct.
- Numerics:
  - `propB.log`: 178 250 pointwise child counts exact, and 70/70 Fourier identities at $p=3,5,7,11$.
  - The equality case $\lvert P\rvert=1$ was never reached there (0/0).
  - New (`edge.log`): $\operatorname{Var}_C(c_NY)=c_n^2\chi_W^2$ holds exactly for 95/95 single parents at $p=3,5,7$.
- **Fix 2.** The paragraph "What independence fails" says the offspring numbers of two parents "are never independent when $\lvert P\rvert\ge2$ and $\chi_W^2>0$". This is not proved. In this generality it is also false: two functions $F(w)$ and $F(bw+c)$ of one uniform $w$ can be independent even when $F$'s mod-$p$ class sums are non-uniform.
  - `ck_indep_search.py` finds 16 524 such configurations on $\mathbb Z/9$. Example: $F=(0,0,0,0,0,1,0,1,1)$, $b=1$, $c=1$.
  - Whether such an $F$ arises as a window law with two actual parents was not examined.
  - Suggested wording: "are in general not independent; Proposition B(ii) measures the dependence exactly". The claim is used nowhere.

**Prop N.**
- The mod-$p$ shell is $p\sum_a\mu_{W,1}(a)^2-1$, and $\mu_{W,1}(a)=c_a/2^r$.
- The balanced minimiser gives $s(p-s)$, and the algebra checks.
- $s\ne0$ since $p$ is odd, and $s(p-s)\ge p-1$.
- $r\le p$: the valuation-0 elements are $j=n,\dots,j_0-1$, where $x+j_0$ is the first multiple of $p$ after $x+n$, and $D\ge1$ forces $j_0\le N$.
- The equality case follows from B(ii).
- Correct. Numerics: bound 70/70; equality case 95/95 (above).
- The "Consequence" paragraph (no per-window CS recursion can close) is correct as a statement about that recursion.

**Lemma C1.**
- $g$ is well defined on $\mathbb Z/p^{D+k}$: for $r=p^Dr'$ it depends only on $r'\bmod p^k$.
- $\hat g(\zeta)=p^k\mathbf 1[\zeta\equiv\xi u^{-1}\ (p^k)]$.
- $t_e$ is a bijection of $\mathbb Z/p^{D+k}$, which uses $D+k\le m-M_N\le m-M_n$.
- The mean is $p^{-(D+k)}\hat g(0)\hat m(0)=0$, and CS over $e$ plus Parseval give (b).
- $F_W(0)=1+\chi_W^2$.
- Correct. Numerics (`C1C2.log`): 1018 ($\xi$, $P$) pairs under (5.1) at $p=3,5,7$, plus 648 in the NEG run; C1a and C1b, 0 failures. This includes the $p=7$ run that the first instance did not finish.

**Prop C2.** The steps:
- **Step 0.** All hypotheses follow from (5.2): (W2′), (W3′) for $W$ at $x$ and for $W'$ at every $x'\in C$ (base valuation $m+D$), and (5.1) with $k=D'$.
- **Step 1.** Lemma 2(b) holds for any base point of $C'$.
- **Step 2.**
  - The class of $e'$ (namely $\beta_{e'}\bmod p^{D'}$) is intrinsic to $C'$, because $\pi_N(x'')/p^{m+D}$ is constant modulo $p^{m+D-M_N}\supseteq p^{D'}$. So $X_b$ is a well-defined function on $C$.
  - B(iii) applies within a class, and Minkowski applies in $L^2(w,w')$.
- **Step 3.**
  - $S'_{e'}(x')\equiv S'_e(x_0)$ (mod $p^{D'}$), since $v(\pi'_j)\ge m-M_N\ge D'$.
  - $\omega'\equiv\omega u$ (mod $p^{D'}$), so $\beta_{e'}\equiv\beta_eu^{-1}$.
  - The map $b\mapsto P_{bu}$ does not depend on $x'$.
- **Step 4** and the identification $\hat\nu_{D+D'}(\zeta)=\hat\mu_{W,D+D'}(\zeta)\hat\mu_{W'}(\zeta u)$ are correct.

Expository suggestion (optional). Step 3 averages $\lvert\Psi_b(\xi;x')\rvert^2$ over $x'\in C$ by Lemma C1, but $X_b$ is computed from a reference point of each $C'$. Add one sentence: moving the reference point inside $C'$ multiplies $\Psi_b$ by a unimodular factor (all members of a class share $\beta$ modulo $p^{D'}$), so $\lvert\Psi_b\rvert^2$ is constant on $C'$. Step 1 says this only for $\lvert A(\eta)\rvert$.

Numerics:
- `C1C2.log`: C2 inequality 33/33. $\varepsilon$ by collisions equals $\varepsilon$ by Fourier fibres in 33/33 cases. Slack 0.009–0.28.
- **Sharp test (new, `edge.log`).** When the parent set is a single path, the proof loses nothing: CS over parents and Minkowski over classes are both equalities. It therefore predicts the exact identity $c_{N'}^2\mathbb E Z_2^2-c_N^2\mathbb EZ_1^2=\varepsilon\,c_n^2$. It holds **exactly in 79/79** single parents with (5.2) at $p=3,5,7$, plus 16/16 exactly at the boundary $D+D'=m-M_{N'}$. Any error in the constant, the frequency band or the fibre would show here.
- Outside (5.2) by 1, 2 and 4 digits the identity still holds (47/47). So (5.2) is conservative. The first instance's NEG control (no (5.2)) also found no violation of the inequality (10/10, max ratio 0.68). The inequality test alone is therefore not sensitive to (5.2); the equality test is the sensitive one.

**Thm C3.**
- **Partition.** For $n\ge2p$ there are two multiples of $p$ among $x+1,\dots,x+n$, so $V_n\ge M_n+1$. Hence $m_\ell$ is constant on $x+p^{m_\ell(x)}\mathbb Z_p$, the cylinders form a countable partition (up to the null set of negative integers), and $\mathcal G_\ell\subseteq\mathcal G_{\ell+1}$.
- **$B_\ell\in\mathcal G_{\ell-1}$.** On an atom $x_A+p^m\mathbb Z_p$ ($m=m_{\ell-1}$), $v(x+i)$ is constant if $x_A+i\not\equiv0$ (mod $p^m$), and $\ge m$ throughout otherwise. So $\{M_{n_{\ell+1}}<m\}$ is constant on atoms and, on it, all valuations up to $n_{\ell+1}$ are constant. $\varepsilon_\ell$ depends on $x\bmod p^K$ with $K\le m-M\le m$.
- **Stopping time.** $\{\tau_j>\ell\}=\bigcap_{j<k\le\ell}B_k\in\mathcal G_{\ell-1}$.
- **Martingale.** Cor A′ ($L=0$) is applied on atoms of $\mathcal G_\ell$ inside $\{\tau_j>\ell\}$. (W2′) $D_\ell\le m_\ell-M_{n_{\ell+1}}\le m_\ell-M_{n_\ell}$ and (W3′) both follow from $B_\ell$. For $\ell=j$ they follow from admissibility, since $\tau_j>j$ always.
- **Second moments.**
  - For $\ell=j$, Prop B(ii) applies with the full population, and $Z^0_{n_{j+1}}$ equals the alive children by A(i).
  - For $\ell>j$, C2 is applied on $\mathcal G_{\ell-1}$-atoms inside $\{\tau_j>\ell\}$, where $\tilde M_{\ell-1}=M_{\ell-1}$.
  - $B_{j+1}$ is $\mathcal G_j$-measurable, so on $A$ it holds everywhere or nowhere. In the latter case $\delta_A=1$ and FE fails, which is consistent.
  - Finiteness of $a_\ell$ follows by induction from the recursion, with nonnegative terms (Tonelli).
  - Monotonicity of $a_\ell$ is conditional Jensen.
  - Hence $a_\ell\le M_j^2(1+\chi_j^2)\prod(1+\bar\varepsilon_\ell)$.
- **Limit.** Doob's $L^2$ convergence theorem gives $\mathbb E\tilde M_\infty=M_j(A)$.
- **Survival ⇒ $K_p$.**
  - $Y>0$ implies $\tau_j=\infty$ and $M_\infty>0$.
  - If some $Z^0_{n_\ell}=0$, then A(i) applied to every later window (whose hypotheses hold on $\{\tau_j=\infty\}$) gives $M_k=0$ for all $k\ge\ell$, a contradiction.
  - So a path is alive at every $n_\ell$. By (F2) a path is alive at every $n$, and (F1) gives $x\in K_p$.
- **Paley–Zygmund.** $\mathbb E Y\ge M_j(1-\sqrt{\Pi_A\delta_A})>0$ by CS, and $\mathbb E Y^2\le M_j^2\Pi_A$.
- **Correct as a conditional theorem.** Numerics (`C3struct.log`):
  - $M_n<V_n$ for $n\ge2p$: 52 800 cases;
  - $V_n$ constant on its cylinder: 6400 cases;
  - first event of $B_\ell$ constant on $\mathcal G_{\ell-1}$-atoms: 5200 cases, with deep gates forced in half of the samples;
  - $\varepsilon_\ell$ unchanged under $x\mapsto x+p^{m_{\ell-1}}z$: 634 cases at $p=3,5,7$;
  - 0 failures throughout. (The first instance's version of the last test was vacuous at $n_0=60$, with 0 cases, because its composite jumps exceeded the cap.)

**Lemma C4.**
- The deterministic part is correct: $V+M\le n/(p-1)+2M\le n/(p-1)+\gamma_\ell=2v(n_{\ell-1}!)\le2m_{\ell-1}$, and $D_{\ell-1}+D_\ell\ge1$ once $n_{\ell+1}-n_{\ell-1}\ge p$.
- The probability part is correct: off $I_A$, $v(x+i)=v(x_A+i)$; on $I_A$, $\mu_A(v\ge s)=p^{m-s}$ for $s\ge m$; $\lvert I_A\cap[1,n]\rvert\le1+n/p^m$ (and 0 if $n<i_1$); then a union bound.
- Numerics:
  - implication 2491/2491 at $p=3$ (`C5_N3_C4.log`);
  - union bound never exceeded by the Monte Carlo frequency (`C3struct.log`; 199 atoms, half with a planted gate in $I_A$).
- **Fix 3 (scope of the remark after the lemma).** "The bound of Lemma C4 is tiny for most atoms" needs the qualifier "once $n_j$ is large enough (depending on $p$ and $r$)". The lemma's hypothesis on $A$ (every $i\le n_{\ell+1}$ outside $I_A$ has $v(x_A+i)<s_\ell$, for **every** $\ell>j$) roughly requires $p^{s_\ell}>n_{\ell+1}$ for all $\ell>j$, and $s_\ell$ is not monotone in $\ell$, because of digit sums.
  - At $p=3$, $r=1.25$, $n_j=30$ it fails for **all** 300 random atoms tested: $s_{j+1}=3$, and 48 consecutive integers contain a multiple of 27.
  - At $p=5$, $n_j=60$ it fails in all tries: at $\ell=j+3$, $s_\ell=3$ while $n_{\ell+1}=148>125$.
  - At $p=3$, $n_j=80$ it holds for 91/200 random atoms, and all 91 have bound $<0.01$.

  The lemma itself is unaffected.

**Lemma C5.**
- $\mathrm{Coll}_K=\mathbb P(\sum\delta_jy_j\equiv0)$, split at the first nonzero index (probability $2^{-(j-n)}/2$; none, $2^{-(N'-n)}$).
- $y_{j+c}/y_j=\pi_c(x+j)$, and the sign symmetry $\sigma\delta\sim\delta$ holds.
- $V_t(x+j)=V_{j+t}-V_j$.
- For $\mathrm{Coll}_D$: the case $j\ge N$ is automatic, and the terms $c\ge N-j$ are irrelevant.
- The prefactors $p^K2^{-(j-n)}p^{-V_{N'-j}(x+j)}/2=c_j/(2c_n)$ are right.
- Correct. Numerics: 120/120 exact at $p=3,5,7,11$, $(n,H,H')$ up to $(24,8,8)$ and $(20,10,10)$ (`C5_N3_C4.log`). The first instance also re-ran the track's own check, 28/28.

**Remark C6.** It is labelled sketch, and (S) is stated as open. Honest.
- **Fix 4 (minor).** By Prop N3, $\mathbb E\Lambda_t=\infty$. The quoted shares (16 %, 70 %, 71 %, 7 % of "the sample mean of $\Lambda_t$") are therefore properties of the 76–80 drawn samples, not estimates of a finite quantity. Say "in this sample". I re-derived the four percentages from `signed_slopes.log`: 0.3131/1.9114, 1.3956/1.9822, 1.4766/2.0905 and 0.0587/0.8488.
- The claim that Prop A transfers to any product measure on digit strings (per-$f$ counting) is plausible from the proof of A(iii). It is a sketch, as labelled.

**Prop N3.**
- $S_\delta=1+(y+1)+(y+1)(y+2)=(y+2)^2$, and $\mathbb P(\delta)=2^{-(t+1)}$.
- For $p^s>t$, $V_t=s+v((t-2)!)$.
- The path is alive once $s\ge v((t-2)!)$, and each shell contributes at least $(1-p^{-1})p^{v((t-2)!)}2^{-(t+1)}$.
- Correct. Numerics: lower bound 750/750 at $p=3,5,7$, $t\le9$. The sampled shell masses are constant in $s$ (e.g. $0.1667$ at $p=3$, $t=4$; $0.2021$ at $p=5$, $t=8$), as the proof predicts.
- **Fix 5 (labels).** Some consequences drawn from Prop N3 are stated without a [heuristic] label:
  - the gloss in headline item 5 ("the averaged form of FE cannot be obtained naively");
  - the results-table phrase "averaged FE needs truncation at deep gates";
  - the two "consequences" after the proposition ("$\mathbb E_A[\varepsilon_\ell]$ is very probably infinite"; "FE needs $\kappa_\ell\to0$", via $\mu(\varepsilon_\ell>\bar\varepsilon_\ell)\gtrsim\kappa_\ell/\bar\varepsilon_\ell$).

  What is proved is $\int_{\mathbb Z_p}\Lambda_t\,d\mu=\infty$. Since $\varepsilon$ is a *signed* combination of $\Lambda$'s (Lemma C5), this alone does not prove $\mathbb E[\varepsilon]=\infty$.

  The global (Haar on $\mathbb Z_p$) version can be proved in a few lines, but only for windows with $N'-N\ge3$:
  - put the double root at $x+j'\approx-2$ with $N\le j'\le N'-3$;
  - the positive term $\frac{c_{j'}}{2c_n}\Lambda_{N'-j'}(x+j')$ grows like $p^s$;
  - the negative terms involve only $v(x+k)$ for $k\le N$, which stay bounded.

  The *atom* version $\mathbb E_A$ is genuinely heuristic. On $\{M_{n_{\ell+1}}<m_{\ell-1}\}$ the atom contains no gate in the window, and $\kappa$ comes from an 8-sample-per-point scan.
- I checked $\kappa$ against `eps_gate_depth.log`: at $d=4$, 5.96/729, 21.6/729 and 19.4/729 give 0.0082, 0.030 and 0.027, as reported; the overall range is 0.007–0.057.

**§7 (heuristics).** All of it is labelled [heuristic], and it matches the logs.
- **Table 7.1** matches `mc_population.log` in every entry checked:
  - the rows for $p=3$ ($n=60$), $p=5$ ($n=40$), $p=7$ ($n=32$) and $p=11$ ($n=28$);
  - the $n$-sequences of $\mathbb EM^0_n$ and $\mathbb E(M^0_n)^2$ at $p=3$;
  - the ratios 0.30, 0.58, 0.76, 0.89.
- **§8 counts**: 7430 parents and 62 132 identities; 512; 84 560; 25; 48. All match the logs.

My independent Monte Carlo (`mc_M.log`, no shared code) agrees within one standard error, but its standard errors expose heavy tails.

| $p$, $n$ | samples | $\mathbb P(Z^0>0)$ | $\mathbb E M^0_n$ | $\mathbb E(M^0_n)^2$ | R3M |
|---|---|---|---|---|---|
| 3, 32 | 4000 | 0.110 | 0.0731 ± 0.0051 | 0.108 ± 0.020 | 0.107 / 0.0710 / 0.103 |
| 5, 30 | 2000 | 0.307 | 0.1026 ± 0.0052 | 0.064 ± 0.008 | 0.311 / 0.0980 / 0.0524 |

Stratifying on gate depth ($p=3$, $n=40$) gives further estimates of $\mathbb E(M^0_{40})^2$ (`deepgate_M2.log`):
- 0.125 from 3000 samples on $\{v(x+39)=1\}$. This event carries all slope-0 mass apart from $\{v(x+39)\ge2\}$, which contributed 0 in 100 samples per depth $s=2,\dots,14$; see Observation G.
- 0.152 from 1000 samples per depth on $\{v(x+33)=s\}$, $s\le3$.
- 0.105 from the track's 20 000 plain samples.

So $\mathbb E[(M^0)^2]$, and hence the "Paley–Zygmund bound" column (0.049 at $p=3$), is determined only to within roughly ×1.5. Its first moment is consistent: 0.075 and 0.083, against 0.071.

In these samples there is no sign of a hidden deep-gate tail.
- At $n=40$, conditional on $v(x+i)=s$ (100 samples per depth, $i\in\{9,12,\dots,39\}$, $s\le14$), the slope-0 population is nonempty only for $s\le10$. The strata with $s\ge8$ contribute at most $1.4\cdot10^{-3}$ each to $\mathbb E(M^0_{40})^2$.
- The 100-per-depth stratified estimates of $\mathbb E(M^0_{40})^2$ themselves range from 0.065 to 0.33, another sign of heavy tails.
- Observation G below gives the mechanism: an alive prefix must satisfy $v(S_{e|_i}(-i))=s$ exactly. It also gives a rigorous but weak cutoff at $p^s>e\,(i-1)!$.
- A stratum with zero successes in 100 samples does not exclude a rare large contribution. This is heuristic evidence only.

**Fix 6.** Give standard errors for $\mathbb E(M^0)^2$. Call the column "PZ ratio $(\mathbb EM)^2/\mathbb EM^2$ (heuristic)", and say that the estimates of the second moment are heavy-tailed. The statement "stabilises after $n\approx20$" is made on one fixed sample of $x$'s, so the values at different $n$ are strongly correlated.

## 3. A new observation (checker's own): deep gates kill the slope-0 population

**Observation G [proved; exact tests].** Let $p$ be odd, $x\in\mathbb Z_p$, $1\le i\le n$ with $s:=v(x+i)\ge1$, and $V_n(x)>s$. If $e$ is a path alive at $n$ with slope $0$, then $v\big(S_{e|_i}(-i)\big)=s$. Here $S_{e|_i}(-i)=\sum_{j<i}e_j\pi_j(-i)$ is an integer of absolute value $<e\,(i-1)!$.

*Proof.* By Taylor's formula, $S_e(-i)=S_e(x)-(x+i)S'_e(x)+(x+i)^2R$ with $R\in\mathbb Z_p$. The three terms have valuations $\ge V_n>s$, exactly $s$, and $\ge2s>s$. So $v(S_e(-i))=s$. Finally $\pi_j(-i)=0$ for $j\ge i$, and $\lvert\pi_j(-i)\rvert=(i-1)!/(i-1-j)!$. ∎

*Consequences.*
1. $S_e(-1)=1$ and $S_e(-2)=1-e_1\in\{0,1\}$ never have valuation exactly $s\ge1$. So $P^0_n(x)=\emptyset$ whenever $v(x+1)\ge1$ or $v(x+2)\ge1$ and $V_n$ exceeds that valuation.
   - The slope-0 population can survive only on $x\not\equiv-1,-2\pmod p$, a set of measure $1-2/p$. At $p=3$ this is $x\equiv0\pmod3$ alone.
   - This bounds the Monte Carlo values $\mathbb P(Z^0>0)=0.107,0.311,0.50,0.64$ by $1/3,3/5,5/7,9/11$, consistently.
   - It also confirms that the slope-0 route cannot see $K_p\cap\{x\equiv-2\}$, which the positive-slope (double-root) paths of Prop N3 may populate. This is in line with R3M §10 item 2.
2. If $p^{v(x+i)}>e\,(i-1)!$ for some $i\le n$ with $V_n>v(x+i)$, then $P^0_n(x)=\emptyset$. So the deep-gate contributions to $\mathbb E[(M^0_n)^2]$ are cut off rigorously at depth $\approx\log_p(e\,(i-1)!)$. In the samples of §2 (§7) they vanish much earlier ($s\le10$ at $n=40$, $p=3$); that part is heuristic.

*Tests* (`gatekill.log`):
- 882 652 (path, gate) pairs at $p=3,5,7$, $n=24$, with $v(S_{e|_i}(-i))=v(x+i)$ in all of them;
- 549 deep-gate samples, all with an empty slope-0 population;
- 303 samples with $v(x+1)\ge1$ or $v(x+2)\ge1$, all with an empty slope-0 population.

Relevance to R3M:
- Nothing in R3M is contradicted.
- Observation G supports the §7.1 heuristic (no hidden deep-gate tail).
- It bears on §10 item 1. The infinite mean in Prop N3 comes from a positive-slope (double-root) signed path, while the slope-0 population cannot sit on a deep gate (Observation G). I did not determine which slope classes drive the measured growth $\varepsilon\approx\kappa p^s$ in the gate-depth scans.

## 4. Computational record

Every run went through `ck_run.sh` or `ck_run2.sh`. The log header records the command line, start time (UTC), exit code and wall time; `ck_run2.sh` also adds a time limit, and its runs set `PYTHONDONTWRITEBYTECODE=1`. Batches: `ck_batch1.sh` (first instance, partially run), and `ck_batch3.sh`–`ck_batch6.sh` (this instance). Exact arithmetic means Python integers and `Fraction`; complex DFTs are used only where marked.

| log | program(s) | what | result | wall per run |
|---|---|---|---|---|
| `validate_lib.log` | `ck_validate_lib.py` | DFS vs brute force over all $2^{n-1}$ paths, $p=3,5,7$ | 4392 paths, 0 failures | 4–12 s |
| `propA.log` | `ck_propA.py` (first instance) | Prop A(i)–(iii), A′, (2.1), constancy; NEG control | 0 failures; NEG: 54/215 parents fail | 10–366 s |
| `propB.log` | `ck_propB.py` (first instance) | B(i) pointwise, B(ii) Fourier (float, rel. $10^{-9}$), Var ≤ $M^2\chi^2$, Prop N bound | 0 failures in 70 samples, $p=3,5,7,11$ | 1–15 s |
| `C1C2.log` | `ck_C1C2.py` (first instance) | martingale, C1a, C1b (float), $\varepsilon$ two ways, C2; $p=3,5$ and now $p=7$ (`7 324 3 21 7 7 0 300 2`); NEG | 0 failures (33 samples + 10 NEG) | 26–170 s |
| `C5_N3_C4.log` | `ck_C5_N3_C4.py` (first instance) | Lemma C5 exact; N3 lower bound and shell masses; C4 implication | 120/120; 750/750; 2491/2491 | <1 s |
| `lemma12.log` | `ck_lemma12.py` | Lemma 1 (a)–(e); Lemma 2 (a),(b) and sharpness | 0 failures | 2–533 s |
| `edge.log` | `ck_edge.py` | C2 single-parent equality (in, edge, out, s−2, s−4); Prop B equality; Prop A at the (W2) boundary and one digit outside | 95/95 exact inside (5.2), 47/47 outside; 95/95 exact; 0 mismatches | 0.1–108 s |
| `C3struct.log` | `ck_C3_struct.py` | partition, $B_\ell$ and $\varepsilon_\ell$ measurability, (F1) with integer factorials, Lemma C4 union bound and hypothesis frequency | 0 failures; C4 hypothesis 0/300 ($p=3$, $n_j=30$), 91/200 ($n_j=80$) | 0.1–69 s |
| `gatekill.log` | `ck_gate_kill.py` | Observation G and its consequences | 0 failures | 0.3–4 s |
| `indep_search.log` | `ck_indep_search.py` | abstract independence counterexamples ($\mathbb Z/9$) | 16 524 found | 3 s |
| `mc_M.log` | `ck_mc_M.py` | heuristic: independent MC of $M^0_n$ ($p=3$: 4000; $p=5$: 2000 samples) | table in §2 (§7) | 20, 146 s |
| `deepgate_M2.log` | `ck_deepgate_M2.py` | heuristic: gate-depth importance sampling, $p=3$ ($n=24,40$), $p=5$ ($n=30$) | cut-off at depth ≤ 10; second-moment spread ×1.5 | 0.1–57 s |
| `rerun_R3M_checks.log` | the track's own `lemma_c5_check.py`, `twowin_check.py` (unchanged) | re-run by the first instance | as reported | <16 s |

Runs without a result, all recorded in the logs:
- The first instance's $p=7$ C2 run (seed 304) was cut off by the spending limit.
- My re-run with `kmax 3` (seed 314) hit the 900 s limit (exit 124).
- One `C4` measurability run at $p=5$ (DP modulo $5^9$, too slow) was killed by hand after 648 s.

No result is taken from these runs. Smoke tests during development are not logged, and their results were reproduced by the logged runs.

## 5. Required and suggested changes to the R3M report

1. **Cor A′ (results table, headline item 1).** "$c_n\to0$" → "$c_n\to0$ for a.e. $x$ (wherever $M_n=o(n)$)".
2. **§3, "What independence fails".** "They are never independent when $\lvert P\rvert\ge2$ and $\chi_W^2>0$" → "They are in general not independent". The original statement is unproved and false at that generality (§2, Prop B).
3. **After Lemma C4.** Add "for $n_j$ large enough (depending on $p$ and $r$), since the hypothesis on $A$ requires roughly $p^{s_\ell}>n_{\ell+1}$ for all $\ell>j$". Example: at $p=3$, $r=1.25$ it fails for every atom when $n_j=30$, and holds for about half of the atoms when $n_j=80$.
4. **Prop N3.** Attach [heuristic] to:
   - headline item 5's second clause;
   - the results-table phrase "averaged FE needs truncation at deep gates";
   - the two consequences after the proof.

   Optionally add the short proof that the *global* Haar mean of $\varepsilon$ is infinite when $N'-N\ge3$.
5. **Remark C6.** The percentages describe the drawn sample, since the true mean is infinite.
6. **§7.1.** Add standard errors for $\mathbb E(M^0)^2$. Rename the "Paley–Zygmund bound" column. Note the heavy tails, with a spread of about ×1.5 between independent estimates at $p=3$.
7. Optional: in Prop C2, Step 3, add the one-sentence invariance of $\lvert\Psi_b\rvert$ within $C'$. Optional: cite Observation G (§3) for the support of the slope-0 population.

None of these changes affects a proof. The headline of R3M stands: $\mu(K_p)>0$ is not proved for any odd $p$. Theorem C3 is a correct conditional result, and its hypothesis FE is open.

*This check was produced in an AI-assisted session (round 3, `check_R3M`). It has not been verified by a human.*
