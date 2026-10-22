# Track T3a (round 3): the $L^2$ (collision) form of the Fourier route to Q3

*Erdős problem #404. Round 3 of an AI-driven project; written 2026-10-21 by an AI instance (Claude) as a track report for the lead author. Nothing here has been checked by a human. The human author (Nathan Durfee) has not verified any mathematics.*

Labels: **[proved]** full proof given here; **[computer-verified]** exact finite computation, programs supplied and re-run; **[proved + computer-verified constants]** a proof whose numerical constants come from such a computation (here with interval arithmetic); **[heuristic]** numerics or reasoning that is not a proof; **[conjecture]**.

Work directory: `e404r3/T3a-q3-fourier/` (`code/`, `data/`, `logs/`). A previous instance of this track (2026-10-20/21) wrote the exact $L^2$ programs `l2dp.c`, `l2dp_twoarray.c` and the Python checks `gamma_exact.py`, `carry_check.py`, `defect_table.py`, but no report. Everything used below was re-derived and re-checked by this instance (§6.1, §9); the new code of this instance is `verify_l2_r3.py`, `verify_wide_r3.py`, `gamma_enum.c`, `gamma_table.py`, `theta.py`, `summary_r3.py`, `smc_l2.py`, `smc2.c`, `smc_dstats.py`, `smc_table.py`, `run_smc.sh`, `run_smc2.sh`.

---

## 0. Summary

The task was rigorous progress on the Fourier route to Q3 (note §10.4: Theorem 10.16, Theorem 10.18, Conjecture 10.22). **No unconditional decay of the $L^1$ shell sums $T_p(k)$ was obtained, and none of RMF, MI-13 or Q3 is settled.** What was obtained concerns the $L^2$ version, i.e. collision probabilities of signed factorial sums, which is the "cheaper intermediate target" of note §10.6 item 2 (an $L^2$ density for the uniform tail measure would give positive Haar measure of the tail set).

1. **Exact carry cocycle for the $L^2$ mass [proved] (Theorem 1).** $C_k=p^k\,\mathbb P(\sum_n\eta_n\,n!/p^{v(N_0!)}\equiv0\bmod p^k)$ (with $\eta_n\in\{-1,0,1\}$ of law $\tfrac14,\tfrac12,\tfrac14$) factorises exactly over level groups: $C_{a+j}=C_a(1+D_a^{(j)})$, where $1+D_a^{(j)}=\sum_{\xi}\hat\rho_a(\xi)\varphi_a(\xi)$ pairs the characteristic function $\hat\rho_a\in[0,1]$ of the conditional carry with the nonnegative block profile $\varphi_a$. The carry functions obey a positive transfer-operator recursion on $\mathbb Q_p/\mathbb Z_p$. In the $L^2$ setting the "sums over the new digit are averages" idea of the brief is exact.
2. **Gate-block constants [proved; exact table computer-verified] (Lemma 2).** $\Gamma_p(J)=p^J\mathbb P(\sum_u\eta_ue_u\equiv0\bmod p^J)-1$ for the gate pattern $e_u=(-1)^u(p-1)!/u!$ equals $\tfrac32p^J2^{-p}-1$ for all $J\ge J_0(p)$, with $J_0=2,2,3,4,5,6,7,7$ for $p=2,3,5,7,11,13,17,19$. The values below $J_0$ are exact rationals.
3. **First unconditional quantitative bounds [proved + computer-verified constants] (Theorem 3, Corollaries 3.1–3.3).** For every prime $p$ and every $N_0$: $C_k\le p^{\theta_pk+O(\log^2k)}$, with explicit $\theta_p$ ($\theta_2=0.3963$, $\theta_3=0.2294$, $\theta_5=0.1102$, $\theta_7=0.0267$, $\theta_{11}=6.24\cdot10^{-3}$, $\theta_{13}=9.08\cdot10^{-4}$, $\theta_{19}=3.41\cdot10^{-5}$). Consequences:
   - the collision probability of the uniform tail measure is $\le p^{-(1-\theta_p)k+o(k)}$;
   - its correlation dimension, and the Hausdorff dimension of every Borel set it charges (in particular of the tail set $E_{N_0}$), is $\ge1-\theta_p$; with optimised block measures, $\dim_HE_{N_0}\ge1-\theta^{\rm set}_p$ (e.g. $\ge0.99966$ at $p=13$);
   - the $L^1$ shell sums of note §10.4 satisfy $T_p(k)\le p^{(1+\theta_p)k/2+o(k)}$, a square-root saving over the trivial bound $p^k$, but **not decay**.
4. **Obstructions [proved] (Propositions 4–5).**
   - For odd $p$, every bound that takes a supremum over the incoming carry law at the start of a window pays a factor $\ge1+\Gamma_p(1)>1$ per window, and the supremum is attained by a genuine carry law (the point mass at $0$). So no argument of this type, with infinitely many windows, can prove $\sup_kC_k<\infty$. This is the $L^2$ analogue of Corollary 10.20.
   - No single block, and no window of $s$ elements, has a spectral gap that is uniform in the depth: at depth $d$ some nonzero frequency has $\varphi\ge1-s\pi^2p^{-2\lfloor(d-1)/s\rfloor}$ (pigeonhole). At deep gates the conditional block law is exactly the three-point law $\tfrac23\delta_0+\tfrac16(\delta_{U'}+\delta_{-U'})$. Interpretation (§5.2, not a theorem): a sup-norm transfer argument at depth $d$ must use windows of $\gtrsim d/\log d$ elements, hence unboundedly many $p$-adic digits of the unit parts. This is a Fourier-side companion of the barrier lemma (Theorem 3.10).
   - Criterion (Proposition 6): for odd $p$, summability over all blocks of the conditional carry's excess at $0$ implies $C_\infty<\infty$, and $C_\infty<\infty$ implies summability over the non-gate blocks.
5. **Computations.**
   - Exact $C_k$ [computer-verified] for $p=2$ ($k\le28$), $3$ ($\le17$), $5$ ($\le12$), $7$ ($\le10$), $11,13$ ($\le7$), at $N_0=1$ and $N_0=p$. Two in-memory layouts agree. 111 cases were re-checked exactly by independent code and the Fourier formula, and 11 deeper cases (including every 128-bit-count run) modulo $\approx2^{95}$. Two runs were reproduced bit-for-bit.
   - At odd $p$ the per-block defects collapse far below the worst case (at $p=13$: $D/\Gamma=1,\ 2\cdot10^{-2},\ 2\cdot10^{-8},\dots,4\cdot10^{-15}$).
   - Sequential Monte Carlo on the exact carry recursion **[heuristic]**: at $p=2$, $C_k\approx5.35,8.96,13.9,21.8,34.9,51.2$ for $k=32,64,\dots,512,1000$, growing like $k^{\alpha}$ with $\alpha\approx0.6$–$0.75$ (the random model gives $\alpha=\log_2(3/2)=0.585$). At $p=3,5,7$ there is no growth to depth $2000/1000/400$: the pooled per-block defects beyond level 20 are $0$ within $\sim10^{-5}$ (non-gates) and $10^{-4}$ (level-1 gates).
   - So the heuristic $L^2$ picture matches the project's critical/supercritical dichotomy. At $p=2$ the uniform tail measure has no $L^2$ density. At odd $p$ it apparently does, with $C_\infty(3)\approx1.31$, $C_\infty(5)\approx1.079$, $C_\infty(7)\approx1.0193$, $C_\infty(13)\approx1.0000287$ ($N_0=1$). If so, then $\lambda(E_{N_0})\ge1/C_\infty$ — unproved.

**Bottom line.** The $L^2$ route is now an exact, positive, purely $p$-adic cocycle with a proved worst case and a proved unconditional exponent bound. Its only missing ingredient is the same one as in $L^1$: equidistribution of the carry at depth, i.e. control of deep digits of Morita's $\Gamma_p$. Propositions 4–5 show precisely which classes of arguments cannot supply it.

---

## 1. Setting and standard facts

Fix a prime $p$ and $N_0\ge1$. Put $e_0=v_p(N_0!)$ and $x_n=n!/p^{e_0}\in\mathbb Z_p$ for $n\ge N_0$. Let $\varepsilon_n$ be i.i.d. fair coins, $X=\sum_{n\ge N_0}\varepsilon_nx_n$, and let $\nu=\nu_{p,N_0}$ be the law of $X$ on $\mathbb Z_p$. Its support is $p^{-e_0}E_{N_0}$, where $E_N=\{\sum_{n\in B}n!:B\subseteq[N,\infty)\}$ is the tail set of note §1.5 (Prop. 3.13(c)). Write $e(t)=e^{2\pi i\{t\}_p}$ for the standard character of $\mathbb Q_p/\mathbb Z_p$. Then
$$\hat\nu(\xi)=\prod_{n\ge N_0}\tfrac12(1+e(\xi x_n)),\qquad|\hat\nu(\xi)|^2=\prod_{n\ge N_0}\cos^2(\pi\xi x_n),$$
where for $\xi$ of order $p^k$ only the finitely many $n$ with $v(x_n)<k$ give factors $\ne1$. Let $\eta_n=\varepsilon_n-\varepsilon'_n$ (independent copies), so $\eta_n\in\{-1,0,1\}$ with probabilities $\tfrac14,\tfrac12,\tfrac14$ and $\mathbb Ee(\xi\eta_nx)=\cos^2(\pi\xi x)$.

**Definitions.**
- $C_k:=\sum_{\xi\in p^{-k}\mathbb Z_p/\mathbb Z_p}|\hat\nu(\xi)|^2=p^k\,\mathbb P(X\equiv X'\bmod p^k)=p^k\,\mathbb P\big(\sum_n\eta_nx_n\equiv0\bmod p^k\big)$, by Parseval on $\mathbb Z/p^k$. We have $C_0=1\le C_1\le C_2\le\cdots$, and $C_\infty:=\lim C_k\in[1,\infty]$.
- $T^{(2)}(k):=C_k-C_{k-1}=\sum_{\mathrm{ord}\,\xi=p^k}|\hat\nu(\xi)|^2$ is the $L^2$ shell, and $T(k):=\sum_{\mathrm{ord}\,\xi=p^k}|\hat\nu(\xi)|$ the $L^1$ shell. For $N_0=p$, $T(k)$ is $T_p(k)$ of note §10.4.
- *Level groups.* $G_a=\{n\ge N_0:v(x_n)=a\}$, a (possibly empty) interval of integers. $a$ is *attained* if $G_a\ne\emptyset$. For attained $a$ let $a'$ be the next attained level and $J=a'-a$ the *jump*.
- *Blocks.* When $N_0=pm_0$, the groups are the blocks $\{pm,\dots,pm+p-1\}$ ($m\ge m_0$). Block $m$ has level $e_m-e_0$ with $e_m=v_p((pm)!)$ and jump $J_m=1+v_p(m+1)$ (note §3.5). For general $N_0$ the first group is a partial block and all later groups are full blocks.

**Lemma 0 [proved].**
- (a) If $C_\infty<\infty$, then $\nu\ll\lambda$ (Haar measure) with a density $f\in L^2$, $\|f\|_2^2=C_\infty$. The tail set then has relative Haar measure $\lambda(E_{N_0})/\lambda(p^{e_0}\mathbb Z_p)\ge1/C_\infty$.
- (b) For every $k$, the proportion of residue classes of $p^{e_0}\mathbb Z_p/p^{e_0+k}$ that contain an element of $E_{N_0}$ is $\ge1/C_k$.
- (c) $T^{(2)}(k)\le T(k)$, so $\sum_kT(k)<\infty\Rightarrow C_\infty<\infty$. Also $T(k)\le\big(p^k(1-\tfrac1p)\,T^{(2)}(k)\big)^{1/2}\le(p^kC_k)^{1/2}$.

*Proof.*
- (a) Let $\lambda$ be normalised Haar measure on $\mathbb Z_p$ and $f_k(x)=p^k\nu(x+p^k\mathbb Z_p)$. Then $(f_k)$ is a $\lambda$-martingale for the filtration of residues mod $p^k$, and $\|f_k\|_2^2=\sum_{r\bmod p^k}p^k\nu(r)^2=p^k\mathbb P(X\equiv X')=C_k$. A martingale bounded in $L^2$ converges in $L^2$ to some $f$, and $\int_Bf\,d\lambda=\lim\int_Bf_k\,d\lambda=\nu(B)$ for every ball $B$, so $\nu=f\lambda$. Since $\nu$ is carried by the compact set $S=p^{-e_0}E_{N_0}$, Cauchy–Schwarz gives $1=\int_Sf\le\|f\|_2\lambda(S)^{1/2}$.
- (b) is the same Cauchy–Schwarz at level $k$: $1=\sum_{r\in R}\nu(r)\le|R|^{1/2}(\sum_r\nu(r)^2)^{1/2}=|R|^{1/2}(C_kp^{-k})^{1/2}$, where $R$ is the set of classes charged by $\nu$.
- (c) $\cos^2\le|\cos|$, then Cauchy–Schwarz over the $p^k(1-1/p)$ frequencies of exact order $p^k$. ∎

So $C_\infty<\infty$ for some $(p,N_0)$ is exactly the "$L^2$ analogue" of note §10.6 item 2, and it would give positive Haar measure of a tail set. By Lemma 0(c) it is implied by any of the $L^1$ hypotheses of the note for the uniform measure. It is strictly weaker than full coverage $E_{N_0}=p^{e_0}\mathbb Z_p$, which is what Q3 needs via Lemma 1.4. Positive measure alone does not decide Q3.

---

## 2. Theorem 1: the exact carry cocycle

**Theorem 1 [proved].** Let $a$ be an attained level with jump $J$ ($J=\infty$ if $a$ is the last attained level considered). Put
$$Z_{<a}=\sum_{v(x_n)<a}\eta_nx_n,\qquad Y_a=\sum_{n\in G_a}\eta_n\,x_n/p^a,\qquad c_a=Z_{<a}/p^a\ \ (\text{on }\{p^a\mid Z_{<a}\}).$$
For $\xi\in\mathbb Q_p/\mathbb Z_p$ define
$$\hat\kappa_a(\xi)=\mathbb E\big[e(\xi Z_{<a}/p^a)\,\mathbf 1\{p^a\mid Z_{<a}\}\big],\qquad\varphi_a(\xi)=\mathbb Ee(\xi Y_a)=\prod_{n\in G_a}\cos^2(\pi\xi x_n/p^a).$$
Then:
- (i) $\hat\kappa_a(\xi)=p^{-a}\sum_{t\in\mathbb Z/p^a}\prod_{v(x_n)<a}\cos^2\big(\pi\tfrac{\xi+t}{p^a}x_n\big)\ \ge0$ (for any lift of $\xi$ to $\mathbb Q_p$; the sum does not depend on the lift), and $\hat\kappa_a(0)=p^{-a}C_a$. Hence $\hat\rho_a:=\hat\kappa_a/\hat\kappa_a(0)$ takes values in $[0,1]$. It is the characteristic function of the law of the carry $c_a$ conditioned on $\{p^a\mid Z_{<a}\}$.
- (ii) *(Block factorisation.)* For $1\le j\le J$,
$$C_{a+j}=C_a\,\big(1+D_a^{(j)}\big),\qquad1+D_a^{(j)}=\sum_{\xi\in p^{-j}\mathbb Z/\mathbb Z}\hat\rho_a(\xi)\,\varphi_a(\xi)=p^j\,\mathbb P\big(c_a+Y_a\equiv0\bmod p^j\ \big|\ p^a\mid Z_{<a}\big).$$
- (iii) *(Transfer operator.)* $\hat\kappa_{a+J}(\xi)=p^{-J}\sum_{\zeta:\,p^J\zeta=\xi}\hat\kappa_a(\zeta)\,\varphi_a(\zeta)$ for $\xi\in\mathbb Q_p/\mathbb Z_p$, the sum running over the $p^J$ solutions in $\mathbb Q_p/\mathbb Z_p$.
- (iv) *(Worst case.)* $0\le D_a^{(j)}\le\Gamma_{G_a}(j):=\sum_{0\ne\xi\in p^{-j}\mathbb Z/\mathbb Z}\varphi_a(\xi)=p^j\,\mathbb P(Y_a\equiv0\bmod p^j)-1$. Equality holds when the conditional carry is $\equiv0\bmod p^j$ almost surely. Among all laws of a carry independent of $Y_a$, the quantity $p^j\mathbb P(c+Y_a\equiv0\bmod p^j)$ is maximised by $c\equiv0$.

*Proof.*
- (i) Use $\mathbf 1\{p^a\mid z\}=p^{-a}\sum_{t\in\mathbb Z/p^a}e(tz/p^a)$ for $z\in\mathbb Z_p$, independence of the $\eta_n$, and $\mathbb Ee(\theta\eta_nx)=\cos^2(\pi\theta x)$. At $\xi=0$ the sum is $p^{-a}\sum_{\zeta\in p^{-a}\mathbb Z/\mathbb Z}|\hat\nu_{<a}(\zeta)|^2=p^{-a}C_a$, because the elements of level $\ge a$ contribute factor $1$ at frequencies of order $\le p^a$. $\hat\kappa_a(\xi)/\hat\kappa_a(0)=\mathbb E[e(\xi c_a)\mid p^a\mid Z_{<a}]$ by definition.
- (ii) The elements of level $<a+j$ are those of level $<a$ together with $G_a$, because no level lies strictly between $a$ and $a+J$. So $Z_{<a+j}=Z_{<a}+p^aY_a$, and with $\mathbf 1\{p^j\mid w\}=p^{-j}\sum_{\xi\in p^{-j}\mathbb Z/\mathbb Z}e(\xi w)$:
$$C_{a+j}=p^{a+j}\,\mathbb E\big[\mathbf 1\{p^a\mid Z_{<a}\}\,\mathbf 1\{p^j\mid c_a+Y_a\}\big]=p^a\sum_{\xi\in p^{-j}\mathbb Z/\mathbb Z}\hat\kappa_a(\xi)\varphi_a(\xi),$$
  since $Y_a$ is independent of $Z_{<a}$. Divide by $C_a=p^a\hat\kappa_a(0)$. The probabilistic form is the same computation read backwards.
- (iii) Similarly, $\hat\kappa_{a+J}(\xi)=\mathbb E[\mathbf 1\{p^a\mid Z_{<a}\}\,e(\xi(c_a+Y_a)/p^J)\,\mathbf 1\{p^J\mid c_a+Y_a\}]$. Expanding the last indicator gives $p^{-J}\sum_{t\bmod p^J}\mathbb E[\mathbf 1\{p^a\mid Z_{<a}\}e(\tfrac{\xi+t}{p^J}(c_a+Y_a))]$, and $\zeta=(\xi+t)/p^J$ runs over the solutions of $p^J\zeta=\xi$.
- (iv) $0\le\hat\rho_a\le1$ and $\varphi_a\ge0$, with $\hat\rho_a(0)=\varphi_a(0)=1$. For an arbitrary independent carry $c$, $p^j\mathbb P(c+Y_a\equiv0)=\sum_\xi\mathbb Ee(\xi c)\varphi_a(\xi)\le\sum_\xi\varphi_a(\xi)$, because $\varphi_a\ge0$ and $|\mathbb Ee(\xi c)|\le1$. ∎

*Remarks.*
- (1) Iterating (iii) from $\hat\kappa\equiv1$ at the first level recovers $C_k=\sum_\xi|\hat\nu(\xi)|^2$. So the $L^2$ mass is the value at $0$ of a product of positive operators on functions on the Prüfer group $\mathbb Q_p/\mathbb Z_p$. This is the exact form of idea (1) of the brief: each operator *averages* over the $p^J$ lifts $\zeta$ of $\xi$. The obstruction (§5) is that its natural norms are not $<1$ uniformly in the depth.
- (2) Positivity has a concrete meaning. Conditional on survival, the carry is never more likely to lie in a class $w\bmod p^j$ than in the class $0$. In particular $D_a^{(j)}\ge0$ and $C_k$ is nondecreasing. All of this was checked exactly on the data (§6.1: 0 violations in 12 runs).
- (3) Theorem 1 holds verbatim for any independent law on each group, not only fair coins. Replace $\varphi_a$ by $|\hat\mu_a|^2$, where $\mu_a$ is the law of the group's (unsigned) sum. This is used in Corollary 3.2(b).
- (4) The previous instance of this track had already found the factorisation (ii) ("Theorem B" in its `carry_check.py`) and verified it by exact rational arithmetic on small cases at $p=2,5$ (`logs/carry_check.log`). This instance re-derived it with the proof above and re-checked $0\le D\le\Gamma$ on all 12 exact data sets (§6.1).

## 3. Lemma 2: the gate-block law

Let $e_u=(-1)^u(p-1)!/u!$ for $0\le u<p$ (for $p=2$: $e=(1,-1)$), $W=\sum_u\eta_ue_u\in\mathbb Z$, $\Sigma_p=\sum_u|e_u|<e\,(p-1)!$, and
$$\varphi_p(\xi)=\prod_u\cos^2(\pi\xi e_u),\qquad\Gamma_p(j)=\sum_{0\ne\xi\in p^{-j}\mathbb Z/\mathbb Z}\varphi_p(\xi)=p^j\,\mathbb P(W\equiv0\bmod p^j)-1,$$
$$\mathrm{dist}_p(j)=\#\{\textstyle\sum_{u\in S}e_u\bmod p^j:\ S\subseteq\{0,\dots,p-1\}\}.$$

**Lemma 2 [proved].**
- (a) *(Gate congruence, all $p$.)* Let $N_0=pm_0$ and $m\ge m_0$, and let $a=e_m-e_0$ be the level of block $m$. For $n=pm+r$:
$$x_n/p^a=U_m\,P_m(r),\qquad U_m=(pm)!/p^{e_m}\in\mathbb Z_p^\times,\qquad P_m(r)=\prod_{i=1}^r(pm+i)\equiv\epsilon_p\,e_{p-1-r}\pmod{p^{J_m}},$$
  with $\epsilon_p=1$ for odd $p$ and $\epsilon_2=-1$. Consequently, for $1\le j\le J_m$ and $\xi\in p^{-j}\mathbb Z/\mathbb Z$, $\varphi_{\text{block }m}(\xi)=\varphi_p(\epsilon_pU_m\xi)$. Hence $\Gamma_{\text{block }m}(j)=\Gamma_p(j)$, and block $m$ has exactly $\mathrm{dist}_p(j)$ distinct subset sums mod $p^j$.
- (b) $W=0$ iff $\eta_0=\eta_1$ and $\eta_u=0$ for all $u\ge2$. Hence $\mathbb P(W=0)=3/2^{p+1}$. The $2^p$ subset sums of $(e_u)$ take exactly $3\cdot2^{p-2}$ distinct integer values.
- (c) $\mathbb P(W\equiv0\bmod p^j)$ is nonincreasing in $j$, and $\mathrm{dist}_p(j)$ is nondecreasing; both are constant from the first $j$ with $p^j>\Sigma_p$. Let $J_0(p)$ be the least $j$ with $\mathbb P(W\equiv0\bmod p^j)=\mathbb P(W=0)$. Then for all $j\ge J_0(p)$, $\{p^j\mid W\}=\{W=0\}$ as events, and
$$\Gamma_p(j)=\tfrac32\,p^j\,2^{-p}-1.$$
  For all $j$, $\Gamma_p(j)\ge\tfrac32p^j2^{-p}-1$, and $\Gamma_p$ is nondecreasing in $j$.
- (d) $\Gamma_p(1)>0$ for odd $p$, while $\Gamma_2(1)=0$.

*Proof.*
- (a) For odd $p$ this is note Theorem 3.9(b): $pm+i=(i-p)+p(m+1)$ with $p^{J_m}\mid p(m+1)$, and $\prod_{i\le r}(i-p)=(p-1)!(-1)^u/u!$ with $u=p-1-r$. For $p=2$: $P_m(0)=1=-e_1$ and $P_m(1)=2(m+1)-1\equiv-1=-e_0\pmod{2^{J_m}}$. The rest holds because multiplication by the unit $\epsilon_pU_m$ permutes $p^{-j}\mathbb Z/\mathbb Z$ and preserves the event $\{\equiv0\}$ and the number of distinct residues.
- (b) $e_0=-e_1=(p-1)!$. For $u\ge2$, $\sum_{v>u}|e_v|<|e_u|\sum_{i\ge1}(u+1)^{-i}=|e_u|/u<|e_u|$, so $|e_u|_{u\ge2}$ is superincreasing. Also $\sum_{u\ge2}|e_u|=(p-1)!\sum_{u=2}^{p-1}1/u!<(e-2)(p-1)!<(p-1)!$.
  - If $W=0$ then $|\eta_0-\eta_1|(p-1)!=|\sum_{u\ge2}\eta_ue_u|<(p-1)!$, so $\eta_0=\eta_1$. Then $\sum_{u\ge2}\eta_ue_u=0$. If some $\eta_u\ne0$, let $u^*$ be the least such $u$; its term has absolute value $|e_{u^*}|>\sum_{v>u^*}|e_v|$, a contradiction.
  - $\mathbb P(\eta_0=\eta_1)=\tfrac1{16}+\tfrac14+\tfrac1{16}=\tfrac38$ and $\mathbb P(\eta_u=0\ \forall u\ge2)=2^{2-p}$.
  - Distinct sums: a subset sum is $s+\sum_{u\ge2}\epsilon_ue_u$ with $s\in\{0,(p-1)!,-(p-1)!\}$ and $\epsilon_u\in\{0,1\}$. The same two estimates show that these $3\cdot2^{p-2}$ values are pairwise distinct.
- (c) Monotonicity is clear, since $p^{j+1}\mid W\Rightarrow p^j\mid W$, and residues mod $p^{j+1}$ refine those mod $p^j$. Since $|W|\le\Sigma_p$ and differences of subset sums are bounded by $\Sigma_p$, once $p^j>\Sigma_p$ we have $p^j\mid W\iff W=0$ and all distinct sums stay distinct mod $p^j$. If $\mathbb P(W\equiv0\bmod p^{j})=\mathbb P(W=0)$, then the events coincide, because $\{W=0\}\subseteq\{p^j\mid W\}$ and every sign vector has positive probability. The formula follows from (b). The lower bound uses $\{W=0\}\subseteq\{p^j\mid W\}$.
- (d) For odd $p$, $\xi e_u$ never lies in $\tfrac12+\mathbb Z$, so every term of $\Gamma_p(1)$ is $>0$. For $p=2$, $\varphi_2(1/2)=\cos^2(\pi/2)\cos^2(\pi/2)=0$. ∎

**Exact values [computer-verified].** Exhaustive enumeration of all $3^p$ sign vectors and all $2^p$ subsets (`gamma_enum.c`, exact 128-bit integers; $p=19$ takes 7.4 s) gives the following (full table: `data/gamma_table.txt`). The values for $p\le13$ agree exactly with the previous instance's independent dictionary DP (`data/gamma_exact.txt`).

| $p$ | $\Gamma_p(1)$ | $\Gamma_p(2)$ | $\Gamma_p(3)$ | $J_0(p)$ | $\mathrm{dist}_p(j)=p^j$ for $j\le$ ($=L_p$) |
|---|---|---|---|---|---|
| 2 | $0$ | $1/2$ | $2$ | 2 | 1 |
| 3 | $1/32$ | $11/16$ | $65/16$ | 2 | 1 |
| 5 | $9/256$ | $61/64$ | $311/64$ | 3 | 1 |
| 7 | $117/8192$ | $461/4096$ | $25079/8192$ | 4 | 2 |
| 11 | $753/2^{19}$ | $117017/2^{20}$ | $840113/2^{20}$ | 5 | 2 |
| 13 | $739/2^{25}$ | $8519/2^{20}$ | $1614333/2^{23}$ | 6 | 2 |
| 17 | $2617/2^{32}$ | $2489427/2^{33}$ | $193865805/2^{33}$ | 7 | 3 |
| 19 | $13507/2^{37}$ | $63684863/2^{37}$ | $738783497/2^{36}$ | 7 | 3 |

The last column reproduces the covering depths $L_p$ of note §3.5. $\Gamma_p(1)$ is the $L^2$ analogue of the constant $A_p$ (the $L^1$ sum at level 1). For example $\Gamma_{13}(1)=2.2\cdot10^{-5}$, while $J_0(13)=6$: from level-5 gates on, the gate block is the three-point configuration of Lemma 2(b).

---

## 4. Theorem 3: an unconditional exponent bound

For $j\ge0$ put $f_p(j)=\log_p(1+\Gamma_p(j+1))$, so that $0\le f_p(j)\le j+1$, and
$$F_p=\sum_{j\ge0}\Big(1-\frac1p\Big)p^{-j}f_p(j),\qquad\theta_p=\frac{p-1}{p}\,F_p .$$
Similarly, with $\mathrm{dist}_p$ in place of $1+\Gamma_p$: $\theta^{\rm set}_p=\frac{p-1}p\sum_{j\ge0}(1-\frac1p)p^{-j}\log_p\big(p^{j+1}/\mathrm{dist}_p(j+1)\big)$. By Lemma 2(c) the summands are explicit affine functions of $j$ for $j+1\ge J_0(p)$, so both series are summed in closed form.

**Theorem 3 [proved; the numerical values of $\theta_p$ are computer-verified in interval arithmetic].** For every prime $p$ and every $N_0\ge1$ there are constants $A_p,B_{p,N_0}$ such that for all $k\ge2$
$$\log_pC_k(p,N_0)\ \le\ \theta_p\,k+A_p\log_p^2k+B_{p,N_0}.$$
In particular $\limsup_k\frac1k\log_pC_k\le\theta_p$, with the values in the table below.

*Proof.* Let $m_0=\lceil N_0/p\rceil$.
- *First group.* If $p\nmid N_0$, the first group $\{N_0,\dots,pm_0-1\}$ is a partial block at level $0$, and the next level is $v_p(pm_0)=1+v_p(m_0)$. By Theorem 1(iv) and the trivial bound $1+\Gamma\le p^j$, its factor is at most $p^{1+v_p(m_0)}$. All later groups are full blocks $m\ge m_0$, at levels $a_m=e_m-e_0$ with jumps $J_m=1+v_p(m+1)$.
- *Chaining.* Given $k$, let $M$ be the largest $m$ with $a_m<k$. Apply Theorem 1(ii),(iv) block by block, with $j=J_m$ for $m<M$ and $j=k-a_M\le J_M$ for $m=M$. By Lemma 2(a),(c), $\Gamma_{\text{block }m}(j)=\Gamma_p(j)\le\Gamma_p(J_m)$. Hence
$$\log_pC_k\le1+v_p(m_0)+\sum_{m=m_0}^{M}f_p(v_p(m+1))\le B+\sum_{i=1}^{M+1}f_p(v_p(i)).$$
  (If $k\le a_{m_0}$, then simply $C_k\le p^k\le p^{a_{m_0}}$.)
- *Counting.* $\#\{i\le X:v_p(i)=j\}=\lfloor X/p^j\rfloor-\lfloor X/p^{j+1}\rfloor\le X(1-\frac1p)p^{-j}+1$, and this is $0$ for $j>\log_pX$. Since $0\le f_p(j)\le j+1$,
$$\sum_{i\le X}f_p(v_p(i))\le X\,F_p+\sum_{0\le j\le\log_pX}(j+1)\le X\,F_p+\tfrac12(\log_pX+2)^2.$$
- *Size of $M$.* $e_M=M+v_p(M!)=(pM-s_p(M))/(p-1)\ge\frac{p}{p-1}M-\log_pM-1$, and $e_M<k+e_0$. Hence $X=M+1\le\frac{p-1}p(k+e_0+\log_pk+O(1))$, so $XF_p\le\theta_pk+O(\log k)$. ∎

**Corollary 3.1 (collision probabilities) [proved].** For every prime $p$, every $N_0$ and every $\epsilon>0$,
$$\mathbb P\Big(\sum_{n\ge N_0}\eta_n\frac{n!}{p^{v(N_0!)}}\equiv0\bmod p^k\Big)\le C_\epsilon\,p^{-(1-\theta_p-\epsilon)k}.$$
(The signed sums $\sum_n\eta_nn!$ over finite supports are pairwise distinct integers. The statement is about their distribution mod $p^k$.)

**Corollary 3.2 (dimension) [proved].**
- (a) For $\nu$-almost every $x$ and every $s<1-\theta_p$, $\nu(x+p^k\mathbb Z_p)\le p^{-sk}$ for all large $k$. Hence every Borel set $A$ with $\nu(A)>0$ has $\dim_HA\ge1-\theta_p$, for the metric $|\cdot|_p$, in which $\dim_H\mathbb Z_p=1$. In particular $\dim_HE_{N_0}\ge1-\theta_p$, and the lower correlation dimension of $\nu$ is $\ge1-\theta_p$.
- (b) $\dim_HE_{N_0}\ge1-\theta^{\rm set}_p$.

*Proof.*
- (a) $\int\nu(x+p^k\mathbb Z_p)\,d\nu(x)=\mathbb P(X\equiv X'\bmod p^k)=C_kp^{-k}$. By Markov's inequality, $\nu\{x:\nu(x+p^k\mathbb Z_p)>p^{-sk}\}\le p^{sk}C_kp^{-k}$, which is summable in $k$ by Theorem 3 when $s<1-\theta_p$. Borel–Cantelli gives the first claim.
  - *Mass distribution in $\mathbb Z_p$.* Let $\nu(A)>0$. Choose $k_0$ such that $A'=\{x\in A:\nu(x+p^k\mathbb Z_p)\le p^{-sk}\ \forall k\ge k_0\}$ has $\nu(A')>0$; note $\nu$ has no atoms on $A'$. Let $\{U_i\}$ cover $A'$ with $0<\operatorname{diam}U_i\le p^{-k_0}$, each $U_i$ meeting $A'$ (points of diameter $0$ have measure $0$ and can be discarded). Pick $x_i\in U_i\cap A'$ and $k_i$ with $p^{-k_i-1}<\operatorname{diam}U_i\le p^{-k_i}$. By the ultrametric inequality $U_i\subseteq x_i+p^{k_i}\mathbb Z_p$. So $\nu(A')\le\sum_ip^{-sk_i}\le p^s\sum_i(\operatorname{diam}U_i)^s$. Hence $\mathcal H^s(A')\ge p^{-s}\nu(A')>0$, and $\dim_HA\ge s$.
  - Since $\operatorname{supp}\nu=p^{-e_0}E_{N_0}$ and scaling does not change dimension, the claim for $E_{N_0}$ follows.
- (b) Replace the fair coins on block $m$ by the law $\mu_m$ that is uniform on one subset of the block per distinct residue mod $p^{J_m}$ (first group: the empty set). The resulting $\nu'$ is carried by $p^{-e_0}E_{N_0}$. By Theorem 1 with Remark (3), the block factor is $\le p^{J_m}\sum_w\mu_m(w)^2=p^{J_m}/\mathrm{dist}_p(J_m)$, because the law of the sum is uniform on $\mathrm{dist}_p(J_m)$ residues. For the partial top block use the trivial factor $p^{J_M}$. Then repeat the proofs of Theorem 3 and of (a). ∎

**Corollary 3.3 ($L^1$ shells: a square-root saving, not decay) [proved].** For the shells of note §10.4 ($N_0=p$),
$$T_p(k)\le\big(p^k(1-\tfrac1p)\,T^{(2)}(k)\big)^{1/2}\le(p^kC_k)^{1/2}\le p^{\frac{1+\theta_p}{2}k+O(\log^2k)} .$$
*Proof.* Lemma 0(c) and Theorem 3. ∎

**Values [computer-verified; interval arithmetic, `code/theta.py`, mpmath `iv` at 100 bits; upper endpoints shown].**

| $p$ | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 |
|---|---|---|---|---|---|---|---|---|
| $\theta_p\le$ | 0.39624 | 0.22940 | 0.11013 | 0.026608 | 6.2357e-3 | 9.0768e-4 | 8.4107e-5 | 3.4067e-5 |
| $1-\theta_p\ge$ | 0.60375 | 0.77059 | 0.88986 | 0.97339 | 0.99376 | 0.999092 | 0.999915 | 0.999965 |
| $1-\theta^{\rm set}_p\ge$ | 0.64624 | 0.80687 | 0.92369 | 0.98555 | 0.99826 | 0.999656 | 0.999965 | 0.999993 |
| naive covering bound $1-p^{-L_p}$ | 0.5 | 0.667 | 0.8 | 0.9796 | 0.9917 | 0.99408 | 0.99980 | 0.99985 |

Cross-check by hand: $f_2(0)=0$ and $f_2(j)=j-2+\log_23$ for $j\ge1$, so $\theta_2=\frac12\sum_{j\ge1}2^{-j-1}(j-2+\log_23)=\frac12\big(1+\frac{\log_23-2}{2}\big)=\frac{\log_23}{4}=0.396241\ldots$

*Remarks on Theorem 3.*
- (1) *What it is.* It is the first unconditional quantitative non-concentration statement for the uniform tail measure that we know of. Previously there were only certified values at depths $\le7$–$8$ (note §10.4.1), and T4's geometric-mean identity for single gate blocks.
  - It holds at every prime, including $p=2$ and $p=3,5$, where the $L^1$ random-model budget $\Lambda_p$ of Theorem 10.16 is $\ge1$.
  - It uses only the gate congruence, i.e. the first $J_m$ digits of each block. In line with the barrier lemma (Theorem 3.10), such shallow information cannot control the deep levels, and Theorem 3 does not try to: it charges each block its worst case.
- (2) *What it is not.* It gives no decay of $T_p(k)$ and no bound on $C_\infty$. The exponent $\theta_p>0$ comes from charging every block its worst case $1+\Gamma_p(J_m)$ (Theorem 1(iv)), and Proposition 4 shows that this is unavoidable for sup-type arguments. The bound is very far from the truth: at $p=13$, $N_0=13$, the product bound at $k=6$ is $1.000132$ against the exact $C_6=1.0000225$ (§6.1).
- (3) *Dimension bounds for $E_{N_0}$ alone are cheap.* The naive covering construction (row 4; it is the measure of Corollary 3.2(b) with $\mu_m$ uniform mod $p^{\min(J_m,L_p)}$) already gives $1-p^{-L_p}$. The certified windows of note §§4.2, 10.2 (Theorem 3.12) would push $\dim_HE_{N_0}$ much closer to $1$ at $p=13$; this was not pursued. The content of Theorem 3 is the bound for the *natural* measure $\nu$, without any certificate.

---

## 5. Obstructions and a criterion

### 5.1 Supremum over the incoming carry (the $L^2$ analogue of Corollary 10.20)

**Proposition 4 [proved].** Let $p$ be odd and $N_0=pm_0$. A *window* $\mathcal W$ is a run of consecutive full blocks $m_1\le m<m_2$ (with $m_1\ge m_0$). Write $a_1=a_{m_1}$, $J_{\mathcal W}=a_{m_2}-a_1$, $Y_{\mathcal W}=\sum_{n\in\mathcal W}\eta_nx_n/p^{a_1}$ and $\Gamma_{\mathcal W}=p^{J_{\mathcal W}}\mathbb P(Y_{\mathcal W}\equiv0\bmod p^{J_{\mathcal W}})-1$.
- (a) $C_{a_{m_2}}=C_{a_1}\cdot p^{J_{\mathcal W}}\,\mathbb P\big(c_{a_1}+Y_{\mathcal W}\equiv0\bmod p^{J_{\mathcal W}}\ \big|\ p^{a_1}\mid Z_{<a_1}\big)$. For every random variable $c$ independent of $Y_{\mathcal W}$, $p^{J_{\mathcal W}}\mathbb P(c+Y_{\mathcal W}\equiv0)\le1+\Gamma_{\mathcal W}$, with equality for $c\equiv0$.
- (b) $\Gamma_{\mathcal W}\ge\Gamma_p(1)>0$.
- (c) Consequently, if the blocks $m_0\le m<M$ are cut into $r$ consecutive windows $\mathcal W_1,\dots,\mathcal W_r$, the chained supremum bound $C_{a_M}\le C_{a_{m_0}}\prod_i(1+\Gamma_{\mathcal W_i})$ (valid by (a)) has right-hand side $\ge(1+\Gamma_p(1))^r$. Chaining supremum bounds at infinitely many window boundaries therefore never proves $\sup_kC_k<\infty$, and a proof that $C_\infty<\infty$ must use the actual law of the carry at all but finitely many boundaries.

*Proof.*
- (a) Same computation as Theorem 1(ii), with the window in place of a group (the window's elements are exactly those of level in $[a_1,a_{m_2})$). The inequality is Theorem 1(iv) for the window.
- (b) The frequencies of order $p$ in $p^{-J_{\mathcal W}}\mathbb Z/\mathbb Z$ are $t/p$ with $p\nmid t$. At these, every element of relative level $\ge1$ contributes $\cos^2(\pi\cdot\text{integer})=1$, so $\varphi_{\mathcal W}(t/p)=\varphi_{\text{block }m_1}(t/p)=\varphi_p(U_{m_1}t/p)$ by Lemma 2(a). Summing over $t$ gives $\Gamma_p(1)$, and the remaining terms are $\ge0$. $\Gamma_p(1)>0$ by Lemma 2(d).
- (c) Multiply (a) over the windows and apply (b). ∎

*Remarks.*
- The maximising carry law $c\equiv0$ is not artificial. It is the law at the first level, and the event "all $\eta_n=0$ so far" has positive probability at every level.
- For $p=2$, (b) fails ($\Gamma_2(1)=0$: non-gate pairs are exactly uniform). At $p=2$ only windows that contain a gate pair pay.
- With Corollary 10.20 (sup-type $L^1$ renormalisation) and T3b's Theorem S5 ($L^2$ covering), Proposition 4 completes the picture for this family. Any bound that, at infinitely many places, forgets the carry law in favour of its worst case loses a fixed factor each time, in $L^1$ and in $L^2$ alike.

### 5.2 No uniform spectral gap at depth; the deep-gate law

**Proposition 5 [proved].**
- (a) *(Pigeonhole.)* Let $y_1,\dots,y_s\in\mathbb Z_p$ and $\varphi(\xi)=\prod_{i\le s}\cos^2(\pi\xi y_i)$. For every $d\ge s+1$ there is $\xi\ne0$ in $p^{-d}\mathbb Z/\mathbb Z$ with
$$\varphi(\xi)\ \ge\ \cos^{2s}\!\big(\pi p^{-\lfloor(d-1)/s\rfloor}\big)\ \ge\ 1-s\pi^2p^{-2\lfloor(d-1)/s\rfloor}.$$
- (b) *(Deep gates.)* Let $J_m\ge J_0(p)$. Conditional on $p^{J_m}\mid Y_m$ (the block's normalised signed sum), $Y_m/p^{J_m}$ has law $\tfrac23\delta_0+\tfrac16(\delta_{U'}+\delta_{-U'})$, where $U'=U_mP_m(p-2)(m+1)p^{-v_p(m+1)}\in\mathbb Z_p^\times$. Its characteristic function at $\xi=U'^{-1}p^{-d}$ equals $\tfrac23+\tfrac13\cos(2\pi p^{-d})\to1$.
- (c) *(Conditional window laws.)* If $c\equiv0$ enters a window $\mathcal W$ of $s$ elements, the carry leaving it is $Y_{\mathcal W}/p^{J_{\mathcal W}}$ conditioned on $p^{J_{\mathcal W}}\mid Y_{\mathcal W}$, a law with at most $K\le3^s$ atoms. For every $d\ge K+1$, its characteristic function satisfies $\max_{0\ne\xi\in p^{-d}\mathbb Z/\mathbb Z}\mathrm{Re}\,\psi(\xi)\ge\cos\big(2\pi p^{-\lfloor(d-1)/K\rfloor}\big)$.

*Proof.*
- (a) Put $M=p^{\lfloor(d-1)/s\rfloor}$, so $M^s\le p^{d-1}<p^d$. Map $t\in\mathbb Z/p^d$ to the point $\big((ty_i\bmod p^d)/p^d\big)_{i\le s}\in[0,1)^s$, and cut $[0,1)^s$ into $M^s$ cubes of side $1/M$. Two distinct $t,t'$ fall in the same cube. For $\delta=t-t'\ne0$, every $\|\delta y_i/p^d\|_{\mathbb R/\mathbb Z}<1/M$, so $|\cos(\pi\delta y_i/p^d)|\ge\cos(\pi/M)$, using $M\ge p\ge2$ (because $d\ge s+1$). The last form is trivial when $s\pi^2/M^2\ge1$; otherwise it follows from $\cos x\ge1-x^2/2$ and Bernoulli's inequality.
- (b) By Lemma 2(a), $Y_m\equiv\epsilon_pU_mW\pmod{p^{J_m}}$, so $\{p^{J_m}\mid Y_m\}=\{p^{J_m}\mid W\}$, which equals $\{W=0\}$ by Lemma 2(c). On $\{W=0\}$, by Lemma 2(b), only the elements with $r=p-1$ and $r=p-2$ (i.e. $u=0,1$) carry a common sign $\eta$, and
$$Y_m=\eta\,U_m\big(P_m(p-1)+P_m(p-2)\big)=\eta\,U_mP_m(p-2)(pm+p)=\eta\,U_mP_m(p-2)\,p(m+1).$$
  Here $p(m+1)=p^{J_m}\cdot(m+1)p^{-v_p(m+1)}$. The conditional weights of $\eta=0,\pm1$ are $4:1:1$. For $p=2$ read $P_m(p-2)=P_m(0)=1$.
- (c) Write $\psi(\xi)=\sum_{k\le K}w_ke(\xi z_k)$ and apply the argument of (a) to the atoms $z_k$, with $\mathrm{Re}\,e(\delta z_k/p^d)\ge\cos(2\pi/M)$. ∎

*Interpretation (not a theorem).*
- By Theorem 1(iii), the carry's Fourier coefficients at depth $d$ are averages of the kernel $\varphi$ over lifts. Any "spectral gap" estimate of the form $\sup_{\xi\ne0}\hat\rho_{\rm after}(\xi)\le\lambda<1$, for frequencies of order $\le p^d$, needs a window whose kernel has no near-$1$ values there.
- By (a), with $s$ elements this forces $s\ge(d-1)/\big(1+\tfrac12\log_p(s\pi^2/(1-\lambda))\big)$. So the window must grow essentially linearly in the depth.
- By Theorem 3.12(a) and Proposition 3.14, the residues of such windows modulo $p^d$ depend on the position modulo a power of $p$ growing with $d$: unboundedly many digits of $\Gamma_p$, as in the barrier lemma (Theorem 3.10).
- (b) makes this concrete at deep gates. Conditional on survival, a deep gate block is a three-point law, whose near-$1$ frequencies are those aligned with the unit $U'_m$. Whether these alignments are cancelled by the neighbouring blocks is exactly a question about the deep digits of $U_m$ and $m+1$.

*Remark ($L^1$ versus $L^2$).* In $L^2$ the kernel $\cos^2$ is a trigonometric polynomial. This is why the $L^2$ mass has an exact probabilistic carry representation (Theorem 1), with no analogue in $L^1$, where $|\cos|$ has an infinite Fourier series and the renormalisation profile $H_W$ of Proposition 10.19 lives on the real line. The archimedean resonance behind Corollary 10.20 nevertheless reappears in $L^2$ through Proposition 5: a kernel is near $1$ exactly at frequencies $\xi$ with every $\xi x_n$ close to $0$ in $\mathbb R/\mathbb Z$.

### 5.3 A criterion for $C_\infty<\infty$

**Proposition 6 [proved].** Let $p$ be odd, $N_0=pm_0$, and for blocks $m\ge m_0$ let
$$\Delta_m=p^{J_m}\,\mathbb P\big(c_{a_m}\equiv0\bmod p^{J_m}\ \big|\ p^{a_m}\mid Z_{<a_m}\big)-1=\sum_{0\ne\xi\in p^{-J_m}\mathbb Z/\mathbb Z}\hat\rho_{a_m}(\xi)\ \ \ge0$$
be the carry's excess at $0$. Then $D_m:=D_{a_m}^{(J_m)}$ satisfies $D_m\le\Delta_m\max_{\xi\ne0}\varphi_p(\xi)\le\Delta_m$, and for non-gate blocks ($J_m=1$) also $D_m\ge\varphi_{\min}\Delta_m$, where $\varphi_{\min}=\min_{p\nmid t}\varphi_p(t/p)>0$. Hence
$$\sum_m\Delta_m<\infty\ \Longrightarrow\ C_\infty<\infty\ \Longrightarrow\ \sum_{m:\,J_m=1}\Delta_m<\infty .$$
*Proof.* Theorem 1(ii) with $\hat\rho\ge0$ and $\varphi\ge0$; and $C_\infty=C_{a_{m_0}}\prod_m(1+D_m)$, which is finite iff $\sum_mD_m<\infty$. ∎

So the $L^2$ problem is exactly a quantitative equidistribution statement for the conditional carry at the residue $0$, summed over the blocks. Theorem 3 bounds each $\Delta_m$ only trivially. The data of §6 show the defects $D_m$ (hence, at non-gates, $\Delta_m$) collapsing super-exponentially at $p\ge5$ and very fast at $p=3$. At $p=2$ (not covered by Proposition 6) the gate defects decay only like $\approx2/\text{level}$.

---

## 6. Computations

### 6.1 Exact $L^2$ masses [computer-verified]

$C_k$ is computed as the exact rational $p^kS/4^M$, where $S=\sum_rN(r)^2$ and $N(r)$ is the number of subsets $B$ of the $M$ elements of level $<E$ (relative to $N_0$) with $\sum_Bx_n\equiv r\bmod p^{E}$. We use $\sum_rN(r)^2=4^M\,\mathbb P(\sum\eta_nx_n\equiv0)$.
- *Programs.* `l2dp.c` (previous instance; in place, 1.5 arrays) and `l2dp_twoarray.c` (previous instance; two arrays) fold the counts level by level. They accumulate $S$ mod $2^{128}$ and mod $2^{61}-1$ and reconstruct it by CRT. This is exact because all runs have $M\le90$, so $S\le4^M\le2^{180}<2^{128}(2^{61}-1)$. Counts are held in 64-bit words for $M\le64$ and in 128-bit words for $64<M\le120$ ("wide" mode).
- *Checks by this instance.*
  - The two layouts agree on all 9 common runs (`logs/`).
  - `verify_l2_r3.py` (independent numpy/Python code) recomputes $C_k$ for 111 cases with $p^k\le4\cdot10^6$: 0 mismatches. For $p^k\le2\cdot10^5$ the Fourier formula $\sum_\xi\prod\cos^2$ in double precision agrees to $\le1.3\cdot10^{-15}$.
  - `verify_wide_r3.py` (independent numpy code; counts mod $2^{64}$ and mod $2^{31}-1$) checks $S$ modulo $2^{64}(2^{31}-1)\approx2^{95}$ for 11 deeper cases. These include the wide-mode runs $(13,1,k{=}6,7)$, $(11,1,7)$ and $(13,13,6)$, and $(2,1,24)$, $(3,1,15)$, $(3,3,15)$, $(5,1,10)$, $(5,5,10)$, $(7,1,8)$, $(7,7,8)$. All agree (`logs/verify_wide_r3.log`).
  - `l2dp.c`, recompiled, reproduced $(p,E,N_0)=(13,7,13)$ and $(3,17,1)$ bit for bit.
  - `summary_r3.py` checks Theorem 1(iv) ($0\le D\le\Gamma_{\rm group}$, with $\Gamma_{\rm group}$ computed from the group's own elements) and $C_k\le$ product bound on all 12 data sets: 0 violations.
  - Lemma 0(b) (hit fraction $\ge1/C_k$) holds in all 12.

*Status.* The deepest levels not reached by the independent checks (e.g. $p=2$, $k=25$–$28$; $p=3$, $k=16,17$; $p=5$, $k=11,12$; $p=7$, $k=9,10$) rest on `l2dp.c` alone, in two memory layouts written by one author. Both are exact integer programs.

| $p$ | $N_0$ | depth $k$ | $C_k-1$ (exact rational, shown in floating point) | product bound of Thm 3 at $k$ | hit fraction (Lemma 0(b)) |
|---|---|---|---|---|---|
| 2 | 1 | 28 | 3.47616 ($=2403120323/2^{29}-1$) | 410.06 | 0.36587 |
| 3 | 1 | 17 | 0.310525 | 33.95 | 0.94996 |
| 3 | 3 | 16 | 0.332452 | 30.17 | 0.92494 |
| 5 | 1 | 12 | 0.0790030 | 5.124 | 1 |
| 5 | 5 | 11 | 0.0415557 | 4.858 | 1 |
| 7 | 1 | 10 | 0.0193292 | 1.2515 | 1 |
| 7 | 7 | 9 | 0.0149568 | 1.2287 | 1 |
| 11 | 1 | 7 | 2.06856e-3 | 1.01073 | 1 |
| 11 | 11 | 6 | 1.44014e-3 | 1.00865 | 1 |
| 13 | 1 | 7 | 2.86586e-5 | 1.000161 | 1 |
| 13 | 13 | 6 | 2.25377e-5 | 1.000132 | 1 |

The column "$C_k-1$" is the $L^2$ distance squared of $\nu\bmod p^k$ from the uniform law: $\sum_{0\ne\xi\in p^{-k}\mathbb Z/\mathbb Z}|\hat\nu(\xi)|^2$. For $p=13$, $N_0=13$ it equals $2.25\cdot10^{-5}$. Compare the certified $L^1$ sum $\sum_{k\le7}T_{13}(k)\le9.3\cdot10^{-3}$ of note §10.4.1.

### 6.2 Block defects versus the worst case [computer-verified; reading of the trend: heuristic]

$D/\Gamma$ for consecutive groups ($D=C_{a'}/C_a-1$, worst case $\Gamma$ from Theorem 1(iv)). Full listing: `data/summary_r3.txt`.

| $p,N_0$ | $D/\Gamma$ along the groups (level of group end) |
|---|---|
| $13,13$ | 1 (1), 2.3e-2 (2), 2.0e-8 (3), 6.1e-12 (4), 8.1e-14 (5), 4.2e-15 (6) |
| $11,1$ | 1 (1), 2.0e-3 (2), 3.0e-6 (3), 1.3e-8 (4), 3.5e-11 (5), 3.1e-12 (6), 3.3e-16 (7) |
| $7,1$ | 1, 5.2e-2, 8.1e-4, 6.6e-4, 3.8e-7, 1.4e-6, 2.5e-7 (gate, level 8), 9.2e-8, 1.6e-9 |
| $5,1$ | 1, 0.62, 1.5e-2, 1.0e-3, 4.8e-4 (gate, 6), 4.8e-4, 8.8e-4, 5.4e-6, 2.8e-7, 5.5e-7 (gate, 12) |
| $3,1$ | 1, 0.5, 0.15 (gate, 4), 0.090, 0.077, 0.022 (gate, 8), 0.030, 0.028, 3.2e-3 (level-2 gate, 13), 0.016, 0.016, 1.1e-3 (gate, 17) |
| $2,1$ | gates only ($D=0$ at non-gates): 1 (3), 0.19 (7), 0.37 (10), 0.050 (15), 0.33 (18), 0.085 (22), 0.13 (25), 0.018 (28) |

At $p\ge5$ the carry equidistributes super-exponentially fast at the depths reached, so $D\ll\Gamma$. At $p=3$ they decay more slowly: by a factor of about 5 over 9 levels at non-gates, and by a factor of 140 from level 4 to level 17 at level-1 gates. At $p=2$ they decay slowly.

### 6.3 Sequential Monte Carlo on the exact carry recursion [heuristic]

*Method* (`smc_l2.py`, any $p$; `smc2.c`, $p=2$, fixed-width carries up to $1024$ bits). Each particle holds an exact carry $c\bmod p^{K-a}$. At each group the exact survival probability $f=\mathbb P(Y\equiv-c\bmod p^J)$ is read off the enumerated group law ($3^{|G|}$ sign vectors). A surviving configuration is drawn from the conditional law, the carry is updated by $c\leftarrow(c+y)/p^J$, and particles are resampled systematically in proportion to $f$. $\prod_{\rm groups}\overline f$ is an unbiased estimator of $p^{-K}C_K$; per-group estimates of $D$ are $\hat D=p^J\overline f-1$. Everything uses the true factorials, so the deep digits of the unit parts are included. The only error is statistical.

*Validation.* $p=3$, $K=17$: $1.2989$ (one run, $P=2\cdot10^4$) against the exact $1.3105$. $p=2$: at $k=16$, the mean of 6 runs with $P=2\cdot10^6$ is $3.0634\pm0.0014$ against the exact $3.0623$; at group end $26$, $4.4398\pm0.003$ against the exact $C_{26}=4.4367$.

*$p=2$, $N_0=1$, $K=1000$* (`data/smc_p2_table_P*.txt`; mean over runs, sd between runs):

| $k$ (group end) | 32 | 64 | 128 | 256 | 512 | 1000 |
|---|---|---|---|---|---|---|
| $P=8\cdot10^6$ (2 runs) | 5.346 (0.004) | 8.955 (0.010) | 13.91 (0.02) | 21.81 (0.19) | 34.90 (0.22) | 51.17 (0.13) |
| $P=2\cdot10^6$ (6 runs) | 5.347 (0.018) | 8.98 (0.06) | 13.98 (0.23) | 21.95 (0.58) | 34.5 (1.8) | 50.3 (5.5) |
| $P=5\cdot10^5$ (4 runs) | 5.358 (0.025) | 8.95 (0.09) | 13.96 (0.27) | 21.50 (0.38) | 33.2 (2.2) | 49.4 (7.9) |
| refined random model $1+\sum_j\mathrm{rm}(j)$ | 5.06 | 7.59 | 11.39 | 17.09 | 25.63 | 37.40 |

- The growth factor per doubling of $k$ is $1.55$–$1.68$ (exponent $0.63$–$0.75$), against the random model's $3/2$ (exponent $\log_2\frac32=0.585$). Here $\mathrm{rm}(j)=2^{j-1-m_j}$ when no element has level exactly $j-1$, and $0$ otherwise.
- Pooled gate defects: $\hat D\approx0.039,\ 0.010,\ 0.0024$ for $J=2$ gates at levels $[20,100),[100,300),[300,1000)$, and about twice that for $J\ge3$. That is $\hat D\cdot\text{level}\approx2$ (`data/smc_p2_dstats.txt`).
- **Heuristic conclusion:** $C_k(2,1)\asymp k^{\alpha}$ with $\alpha\approx0.6$–$0.75$. So $C_\infty=\infty$ at $p=2$, and the uniform tail measure at $p=2$ has no $L^2$ density. Whether it is singular is not addressed. By Prop. 3.13(c) it is either absolutely continuous or singular.

*$p=3,5,7$, $N_0=1$* (`data/smc_p{3,5,7}_dstats.txt`). Pooled $\hat D$ over levels $\ge20$ (6 runs at $p=3$ to $K=1500$–$2000$; 4 runs at $p=5$ to $K=600$–$1000$; 2 runs at $p=7$ to $K=400$), mean $\pm$ 1 s.e.:

| $p$ | levels | non-gates ($J=1$) | $J=2$ gates | $J\ge3$ gates |
|---|---|---|---|---|
| 3 | $[20,100)$ | $(1.2\pm0.9)\cdot10^{-5}$ | $(-1.0\pm1.8)\cdot10^{-4}$ | $(1.9\pm1.2)\cdot10^{-3}$ |
| 3 | $[100,300)$ | $(-0.4\pm0.6)\cdot10^{-5}$ | $(-0.7\pm1.1)\cdot10^{-4}$ | $(0.5\pm1.0)\cdot10^{-3}$ |
| 3 | $[300,1000)$ | $(0.06\pm0.37)\cdot10^{-5}$ | $(0.2\pm0.7)\cdot10^{-4}$ | $(-0.4\pm0.9)\cdot10^{-3}$ |
| 3 | $[1000,2000)$ | $(-0.5\pm0.3)\cdot10^{-5}$ | $(1.0\pm0.6)\cdot10^{-4}$ | $(-0.2\pm0.8)\cdot10^{-3}$ |
| 5 | $[20,1000)$ | $\le10^{-5}$ in every bin | $\le4\cdot10^{-4}$ | $|\hat D|\le4\cdot10^{-3}$ |
| 7 | $[20,400)$ | $\le10^{-5}$ | $\le2\cdot10^{-4}$ | noise only |

- At $p=2$ the same statistic is $0.039\to0.0024$ and clearly positive.
- At $p=3$ the exact data give $D\approx5\cdot10^{-4}$ (non-gates) and $10^{-3}$ (gates) at levels 13–17. Beyond level 20 everything is $0$ within errors.
- **Heuristic conclusion:** at odd $p$, $C_k$ stops growing. Summing bin means plus 2 s.e. over the groups of one run, the growth of $\log C$ from level 20 to 2000 at $p=3$ is $\lesssim0.3$, dominated by the noisy $J\ge3$ bins. At $p=2$, from level 20 to 1000, it is $\approx2.6$. This is consistent with $C_\infty(3,1)\approx1.31$, $C_\infty(5,1)\approx1.079$, $C_\infty(7,1)\approx1.0193$, i.e. with an $L^2$ density and positive Haar measure of $E_1$ at $p=3,5,7$. It is **not** a proof, and slow growth at $p=3$ (say $\log C$ rising by $<0.1$ per decade) is not excluded by these runs. Single-run trajectories of $C$ at odd $p$ wander by $\pm10$–$15\%$ because of resampling noise (e.g. $p=3$: $1.13$–$1.47$ at $K=2000$). Only the pooled defect statistic is informative.

**Conjecture 7 ($L^2$ dichotomy) [conjecture; evidence §§6.1–6.3].** For every odd prime $p$ and $N_0\in\{1,p\}$ (and plausibly every $N_0$), $C_\infty(p,N_0)<\infty$; hence the tail set $E_{N_0}$ has positive Haar measure, with relative measure $\ge1/C_\infty$. For $p=2$, $C_k(2,N_0)\asymp k^{\alpha}$ with some $\alpha\in(0.55,0.75)$.

The odd-$p$ half follows from MI-13-type $L^1$ bounds (Lemma 0(c)) and is strictly weaker. By Lemma 0(a) it would give, e.g., relative measure $\ge0.99997$ for $E_{13}$ if $C_\infty(13,13)$ is close to the computed $1.0000225$.

### 6.4 Exponents [computer-verified]

See the table after Corollary 3.3 (`data/theta.txt`).

---

## 7. Assessment against the brief, and gaps

**The three ideas of the brief.**
1. *Digit-by-digit factorisation as a cocycle.*
   - In $L^2$ this is now exact and positive (Theorem 1(iii)): $C_k$ is the value at $0$ of a product of positive averaging operators on $\mathbb Q_p/\mathbb Z_p$.
   - Its growth exponent is bounded unconditionally by $\theta_p$ (Theorem 3), but not by $0$.
   - Bounding the exponent by $0$, let alone proving $C_\infty<\infty$, requires decorrelation of the carry from the block kernels at depth. By Propositions 4–5, neither sup-norm transfer bounds nor bounded windows can supply it.
   - The $p$-automatic structure of $U(n)\bmod p^d$ (Prop. 3.14) was not exploited. The automaton grows with $d$, and Proposition 5 shows that depth-$d$ control needs windows of length $\gtrsim d/\log d$.
   - In $L^1$ no analogue of Theorem 1 exists, because $|\cos|$ is not a trigonometric polynomial.
2. *The $L^2$ collision count.* Proved: $\mathbb P(\text{collision mod }p^k)\le p^{-(1-\theta_p)k+o(k)}$ (Corollary 3.1), and exact values at small depth (§6.1). Not proved: $\le Cp^{-k}$, i.e. $C_\infty<\infty$. The obstruction is identified (Propositions 4–6).
3. *Factorial-base digits.* Proposition 5(a) is the digit-side statement. For any $s$ consecutive elements and any $\epsilon>0$, once $d\ge1+s\big(1+\tfrac12\log_p(s\pi^2/\epsilon)\big)$ there are nonzero frequencies of order $\le p^d$ at which the product of their $s$ factors is $\ge1-\epsilon$, i.e. all $s$ "digits" $\tau_m$ are extreme. So counting $u$ with many extreme digits cannot be done block by block. It needs joint control across $\gtrsim d/\log d$ consecutive $m$, which is the barrier again.

**Gaps (explicit).**
- (G1) No decay bound $T_p(k)\le C\lambda^k$ with $\lambda<1$ was obtained, for any $p$. Corollary 3.3 gives only $T_p(k)\le p^{(1+\theta_p)k/2+o(k)}$.
- (G2) $C_\infty<\infty$ (positive measure of a tail set) is not proved for any $(p,N_0)$. $C_\infty=\infty$ at $p=2$ is not proved either. Both rest on the Monte Carlo of §6.3, which is heuristic. At odd $p$ it cannot exclude slow growth of $\log C$ (below $\sim0.1$ per decade of depth at $p=3$).
- (G3) Theorem 3's constants $\theta_p$ use interval arithmetic on exact rational inputs. The exact inputs come from one enumeration program (`gamma_enum.c`), cross-checked for $p\le13$ against an independent Python DP. For $p=17,19$ they were checked only internally: the count identity $\mathrm{weight}(W=0)=3\cdot2^{p-1}$ and $\mathrm{dist}=3\cdot2^{p-2}$ match Lemma 2(b).
- (G4) The deepest exact $C_k$ (the last 1–4 levels of each run) come from one author's program in two memory layouts. Everything up to $p^k\le4\cdot10^6$ is re-checked exactly, and 11 deeper cases (including all wide-mode runs) modulo $\approx2^{95}$, by independent code.
- (G5) Nothing here bears directly on Q3. Positive measure of $E_{N_0}$ would not by itself give $f(a,p)=\infty$ for any $a$; full coverage would (Lemma 1.4).
- (G6) Proposition 5's "interpretation" paragraph is a heuristic reading of a proved pigeonhole statement, not an impossibility theorem for all transfer methods. Proposition 4 is an impossibility statement only for chained supremum bounds.
- (G7) The previous instance's data files `data/l2_summary.{txt,json}` and `data/defect_table.txt` contain a check ("Theorem D", with sup-constants $c_p(J)$) that this instance did not adopt. Its single reported "violation" at $p=3$ is the partial first block $\{1!,2!\}$, to which that bound does not apply. `data/summary_r3.txt` supersedes those files.

**Most promising next step.**
- *Caution.* A finite computation cannot certify $\Delta_m\le\epsilon$ uniformly in the position $m$ by taking the worst incoming carry at a window start. The worst incoming carry is a point mass, and for some point masses only one configuration survives, so $\Delta_m$ is then of order $p^{J}$. This is Proposition 4 again.
- *Rigorous step.* Prove $C_\infty<\infty$ almost surely in a *random-unit model* that keeps everything forced by the factorial structure. That means valuations, the gate congruence mod $p^{J_m}$, and the shadow windows of Theorem 3.12(a), with the remaining $p$-adic digits of $U(n)$ i.i.d. uniform. With Propositions 4–5 this would show that the only obstruction to the odd-$p$ half of Conjecture 7 is pseudo-randomness of the digits of Morita's $\Gamma_p$. Theorem 1 makes this a second-moment computation for a positive random cocycle.
- *Computational step.* A C implementation of the odd-$p$ SMC with multiprecision carries ($P\sim10^7$, depth $10^4$) would test Conjecture 7 at $p=3$, where the heuristic margin is thinnest.

---

## 8. Credit and relation to prior work

- The objects $T_p(k)$, Theorem 10.16 (RMF), Theorem 10.18 / Conjecture 10.22 (MI-13), the renormalisation identity and Corollary 10.20 are from round 2 of this project (track R2a/R2b, note §10.4–10.5). Theorem 3.9 (gate congruence) and Theorem 3.10 (barrier lemma) are from round 1 (tracks B, C). Prop. 3.13 (Fourier criterion, pure type) is from round 1, track F.
- Lemma 2(a) is the gate congruence of note Theorem 3.9(b); only the $p=2$ case and the packaging as a block law are added here.
- The block factorisation of Theorem 1(ii) was first written down by the previous instance of this track, in code and comments, without a report. The proof, the positivity, the transfer operator form, Theorem 3, Propositions 4–6 and the SMC are from this instance.
- T4 (round 3) computed $c_p$, the single-gate $L^1$ sums and the annealed moments; T3b (round 3) proved that the $L^2$/Chebyshev *covering* criterion is useless at depth (Theorem S5). Neither overlaps with the results here. Theorem S5 concerns covering windows; Theorem 3 here concerns the tail measure.
- The martingale and energy arguments in Lemma 0 and Corollary 3.2 are standard: Frostman / mass-distribution principle, $L^2$-bounded martingales; see e.g. Falconer, *Fractal Geometry*, and Kahane, *Some Random Series of Functions*. Lemma 0(a) is the textbook fact that an $L^2$-bounded density martingale gives absolute continuity.
- The SMC estimator (sequential importance resampling with unbiased normalising-constant estimates) is standard (Del Moral, *Feynman–Kac Formulae*, 2004). Here it is applied to the exact carry recursion.
- We know of no prior unconditional bound on collision probabilities of signed factorial sums modulo $p^k$, or on the dimension of the tail sets $E_N$. This is a limited search: the round-3 literature gate covered #404-specific work, Kurepa-type results mod $p$, and Garaev–Luca–Shparlinski / Klurman–Munsch for $n!\bmod p$, none of which treats $p^k$. As far as their public material summarised in note §2 shows, Kitamura (July 2026), Tao, Kovač and Lin did not consider the $L^2$ mass.

---

## 9. Reproduction

All commands run from the work directory `e404r3/T3a-q3-fourier` on 2026-10-21 (this instance), at most 2 cores, each run $\le2.2$ GB and $\le2$ min. Python is run without `-I` because numpy and mpmath live in the user site; all scripts are this project's own.

| step | command | output | time |
|---|---|---|---|
| independent check of exact $C_k$ | `python3 code/verify_l2_r3.py` | `logs/verify_l2_r3.log` (111 cases, 0 mismatches) | 1.8 s |
| modular check of deep / wide-mode exact runs | `python3 code/verify_wide_r3.py p N0 k` (11 cases, see §6.1) | `logs/verify_wide_r3.log` (all agree) | 0.05–9.6 s each |
| rebuild + rerun two exact runs | `clang -O2 code/l2dp.c`; `l2dp 13 7 13`, `l2dp 3 17 1` | identical to `data/l2/` (`logs/rerun_l2dp_r3.log`) | 3.3 s, 2.0 s |
| exact summary + Theorem 1/3 checks | `python3 code/summary_r3.py` | `data/summary_r3.txt` (0 violations) | <1 s |
| gate constants | `clang -O2 -o code/gamma_enum code/gamma_enum.c`; `code/gamma_enum p 16` for $p=2,\dots,19$ | `data/gamma_enum.txt` | $\le7.4$ s each |
| exact $\Gamma$ table + cross-check | `python3 code/gamma_table.py` | `data/gamma_table.txt` | <1 s |
| exponents (interval arithmetic) | `python3 code/theta.py` | `data/theta.txt` | <1 s |
| SMC, Python (any $p$) | `code/run_smc.sh LANE "p N0 K P seed" ...` | `data/smc/p*_*.txt`, `logs/smc_lane_*.log` | 70 s ($p=3$, $K=2000$, $P=5\cdot10^4$); 189 s ($p=3$, $K=1500$, $P=2\cdot10^5$); 40 s ($p=5$, $K=600$, $P=10^5$) |
| SMC, C ($p=2$) | `clang -O2 -o code/smc2 code/smc2.c -lm`; `code/run_smc2.sh "N0 K P seed" ...` | `data/smc/c2_*.txt`, `logs/smc2_lane.log` | 22 s ($P=2\cdot10^6$), 88 s and 2.1 GB ($P=8\cdot10^6$) |
| SMC tables | `python3 code/smc_table.py 32,64,128,256,512,1000 data/smc/c2_N1_K1000_P8000000_s3*.txt` etc.; `python3 code/smc_dstats.py FILES` | `data/smc_p2_table_P*.txt`, `data/smc_p{2,3,5,7}_dstats.txt` | <5 s |

Exact runs inherited from the previous instance (2026-10-20, `code/run_l2.sh`, logs in `logs/p*_E*_N*.log`) took $\le8.1$ s and $\le3.7$ GB each.

Not re-run by this instance: `l2dp` at $p=2$ ($E=28$), $p=5$ ($E=12$), $p=7$ ($E=10$), $p=11$ ($E=7$), $p=13$ ($N_0=1$). Their shallow levels are covered by `verify_l2_r3.py`, and their two-layout agreement is in the logs.

A process note: one superseded Python SMC lane (`smc_lane_A`, $p=2$) was stopped part-way. Its completed runs `p2_N1_K4000_P50000_s{1,2,4}` are kept (high variance at $P=5\cdot10^4$) but are not used in the tables. The C runs supersede them.
