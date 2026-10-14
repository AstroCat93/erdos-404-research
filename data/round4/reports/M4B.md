# Round 4, track M4B: adaptive windows (strategy B) for $\mu(K_p)>0$

Date: 2026-10-13. Code: `code/round4/M4B/`. Logs: `data/round4/M4B/`. Notation: note.md §10.1 and the round-3 R3M report (`data/round3/reports/R3M.md`, §1), restated in §1 below.

## Headline

**$\mu(K_p)>0$ is still not proved for any odd prime $p$.** This track realises strategy B (window starts chosen from the digit filtration) and settles several questions that round 3 left heuristic. Every item marked [proved] has a complete proof below. The identities among them (B2, B2′, B3 and the mechanism of N4) were also tested in exact arithmetic at $p=3,5,7$; the structural statements (B1, B1′, B2a, B4, B4′, B5, B7) have no numerical content to test.

1. **[proved] Theorem B1 (adaptive windows).** Theorem 11.14 (R3M Theorem C3) holds verbatim for random window times $n_\ell$, provided $n_0,n_1$ are deterministic and each $n_{\ell+1}$ is a function of $x \bmod p^{V_{n_{\ell-1}}(x)}$ ("two-step predictable"). A global form (B1′) replaces "one good atom" by global Haar quantities.
2. **[proved] Proposition B2 (gate splitting).** For every split point $n+d$ of a composite window, $\varepsilon(W,W')$ equals $p^{g}$ times an average, over the values $a$ of the signed pre-sum, of density increments of the post-window's signed law. Here $g=V_{n+d}-V_n$. Consequently $\varepsilon\le p^g\,\mathrm{Coll}^{\rm pre}_g\,\varepsilon^{\rm post}$, and the error term is bounded explicitly.
3. **[proved] Corollary B2′ (the round-3 decomposition, made exact).** If the gate at $n+d$ has depth $s$ with $p^s>e\,(d-1)!$, then
$$\varepsilon(W,W')=\frac{c_{n+d}}{c_n}\Big[\varepsilon^{\rm post}+\tfrac12\Delta^{\rm post}\big(\tfrac{1}{x+n+d-1}\big)\Big],\qquad |\Delta^{\rm post}|\le\varepsilon^{\rm post},$$
with $c_{n+d}/c_n=2^{-d}p^{v((d-1)!)+s}$. So the heuristic $\kappa\approx p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}$ of round 3 is **true up to a factor in $[\frac12,\frac32]$**. The correction is the exact double-root structure $(y+2)^2$ (Lemma B2a). For $d=1$ the identity is $\varepsilon=\frac{p^s}{2}\varepsilon^{\rm post}$ for every $s\ge1$.
4. **[proved] Proposition N4 (the plain annealed mean of $\varepsilon$ is infinite).** For every fixed composite window whose factorial band is nonempty, $\int_{\mathbb Z_p}\varepsilon(W,W')\,d\mu=+\infty$. In round 3 this was labelled heuristic; the round-3 check sketched a global proof for windows with $N'-N\ge3$ (double root placed in the second window). N4 is a different, complete proof (gate at distance $1$) that identifies the divergent coefficient exactly. The divergent part is $\frac{p^s}{2}\varepsilon_{\rm fact}$, where $\varepsilon_{\rm fact}>0$ is the fine-scale mass of the **factorial** window $0!,1!,2!,\dots$. This also explains the round-3 observation that $\kappa$ does not decay at $p=3$: the deep-gate prefactor is $\varepsilon_{\rm fact}/2$, and the exact values of $\varepsilon_{\rm fact}$ do not decay at $p=3$ or $p=5$ in the computed range (they do at $p=7$). Our predictions match the round-3 log to three digits.
5. **[proved] Proposition B5 (ladder starts).** If the window start is a $C'$-ladder point ($c_{n+d}/c_n\le C'$ for all $d$), then a gate deeper than $\log_p(e\,(N'-n)!)$ contributes at most $\frac32C'(N'-n)\,p^{(N'-n)/(p-1)}/(e\,(N'-n)!)$ to $\int\varepsilon$. That is super-exponentially small, against $+\infty$ for fixed starts. **Lemma B7 [proved]:** a start right after a multiple of $p$ fails to be a $1$-ladder point with probability $\le0.028$ at $p=7$.
6. **[proved] Lemma B3 (conservation on Hensel balls).** The unweighted signed mass of a slope-$\lambda$ string is conserved in expectation over a window only after integrating over its Hensel ball $z'+p^{V-\lambda}\mathbb Z_p$, not over the fine cylinder $z'+p^V\mathbb Z_p$. This repairs a gap in R3M Remark C6, which applied the $\rho$-weighted martingale to the unweighted densities $\Lambda_t$. Exact tests: the ball identity holds 74/74, while the fine-cylinder ratio $\ne1$ in 74/74. With hypothesis (H) violated, the identity fails in 54 of 72 parents.
7. **[proved] Theorem B4 (reduction).** $\int\varepsilon\,\mathbf 1_G\,d\mu\le$ boundary terms $+$ late births $+\sum$ (Haar mass at the next time of the descendants of signed strings outside the Hensel/linear regime). **[proved; conditional on (S_B)] Corollary B4′.** If the non-regime mass decays exponentially in the age (hypothesis (S_B), stated in §6 so that strategy A's (S) can be plugged in), then $\sum_{\ell>j}\mu(B_\ell^c)\le Ce^{-cn_j}$, i.e. the probability form of FE holds for all late windows.
8. **[obstruction] The initial phase (§7).** Even granting (S_B), FE for *late* windows does not give $\mu(K_p)>0$. Both the per-atom theorem and the global form need control of the first windows after the starting time. That is either a finite but very large exact computation, or new input. Round 3 described FE as "the only genuinely open part"; this is a second, independent gap.
9. **[heuristic] Numerics.**
   - Ladder starts cut the mean of $\varepsilon$ by $\times2.4$ to $\times13$ at $p=7$, and its 99% quantile by up to $\times24$, against fixed starts (§8.4).
   - The high-slope (Hensel-failure) part of the signed mass is concentrated on processes with a gate of depth $\ge2$ within $p$ steps of their start. Without such a gate its share is about 8–35% at the accessible ages, where the regime threshold is only $0$ or $1$ (§8.5).
   - (S_B) itself cannot be tested at accessible sizes.

Nothing here bears on Q3: a measure statement cannot see a countable set, and $K_p$ is nowhere dense (note Theorem 3.6).

## 0. Results at a glance

| # | statement | status |
|---|---|---|
| Thm B1, B1′ | Theorem 11.14 with two-step predictable random window times; global Paley–Zygmund form | proved |
| Prop B2 | exact gate-splitting identity for $\varepsilon$; bounds (B2.3)–(B2.5) | proved; exact tests, 1048 (sample, split) pairs, 0 failures; negative control fails 114/120 |
| Lemma B2a | $\sum_{k<d}\epsilon_k/k!=0$ with $\epsilon_k\in\{-1,0,1\}$ forces $\epsilon_0=-\epsilon_1$ and $\epsilon_k=0$ for $k\ge2$ | proved |
| Cor B2′ | deep gate at distance $d$: exact formula, $\varepsilon\in[\frac12,\frac32]\frac{c_{n+d}}{c_n}\varepsilon^{\rm post}$; $d=1$: $\varepsilon=\frac{p^s}2\varepsilon^{\rm post}$ | proved; exact tests (2^d Coll = 3/2 exactly) |
| Prop N4 | $\int_{\mathbb Z_p}\varepsilon\,d\mu=+\infty$ for every fixed composite window with nonempty factorial band | proved; mechanism tested exactly (56/56) |
| Table F | fine-scale masses $\varepsilon_{\rm fact}$ of factorial windows | exact numbers [computer-assisted]; reading as asymptotics [heuristic] |
| Prop B5 | ladder starts make the deep-gate tail of $\int\varepsilon$ super-exponentially small | proved |
| Lemma B7 | existence of ladder starts after a multiple of $p$ ($p\ge5$) | proved |
| Lemma B3 | conservation of unweighted signed mass on Hensel balls | proved; exact tests 74/74; controls |
| Thm B4 | reduction of $\int\varepsilon\mathbf 1_G$ to non-regime masses | proved |
| Cor B4′ | (S_B) ⟹ $\sum_{\ell>j}\mu(B_\ell^c)\le Ce^{-cn_j}$ | proved; conditional on (S_B) |
| §7 | the initial-phase gap; per-atom loss factor $p^{m_j}$ | obstruction (proved statements, open problem) |
| §8.4–8.5 | ladder vs fixed starts; slope profiles | heuristic |

## 1. Notation and what is used

$p$ is an odd prime, $v=v_p$, $\mu$ is Haar probability on $\mathbb Z_p$, $e(t)=\exp(2\pi it)$.
- $\pi_j(x)=\prod_{i=1}^j(x+i)$, $V_n=v(\pi_n(x))$, $M_n=\max_{i\le n}v(x+i)$, $c_n=2^{-n}p^{V_n}$, $\theta:=p^{1/(p-1)}/2<1$.
- Composite window $[n,N')=[n,N)\cup[N,N')$; elements $y_j=\pi_j(x)/\pi_n(x)$ for $n\le j<N'$; $D=V_N-V_n$, $K=V_{N'}-V_n$.
- $\varepsilon(W,W')=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D=\sum_{\zeta:\ \mathrm{ord}(\zeta)\in(p^D,p^K]}|\hat\nu(\zeta)|^2\ \ge0$ (R3M Prop C2). Here $\nu$ is the law modulo $p^K$ of a uniform subset sum of the $y_j$.
- Signed digits $\delta_c\in\{-1,0,1\}$ are i.i.d. with $P(0)=\frac12$, $P(\pm1)=\frac14$. $\mathrm{Coll}_k=P(\sum_j\delta_jy_j\equiv0\bmod p^k)$.
- For $y\in\mathbb Z_p$: the **$\Lambda$-process from $y$** consists of the signed strings $\delta=(\delta_0,\dots,\delta_{a-1})$ with $\delta_0=1$ and weight $P(\delta)=\prod_{c\ge1}P(\delta_c)$, with $F_\delta(Z)=\sum_{c<a}\delta_c\pi_c(Z)$.
  - $\delta$ is *alive at age $a$* if $v(F_\delta(y))\ge V_a(y)$; its slope is $\lambda_\delta(y)=v(F'_\delta(y))$.
  - $\Lambda_a(y)=p^{V_a(y)}\sum_{\delta\text{ alive}}P(\delta)$.
- Lemma C5 (R3M, proved):
$$\varepsilon=\frac{c_{N'}-c_N}{c_n}+\sum_{n\le j<N}\frac{c_j}{2c_n}\big[\Lambda_{N'-j}-\Lambda_{N-j}\big](x+j)+\sum_{N\le j<N'}\frac{c_j}{2c_n}\Lambda_{N'-j}(x+j).$$

Used from round 3 (all proved and checked):
- R3M Lemma 1: (b) $V_n\le n/(p-1)+M_n$; (c) $V_j-V_n\ge\lfloor(j-n)/p\rfloor$; (e) Taylor with integral coefficients.
- Lemma 2, Prop A, Cor A′, Prop B, Prop C2, Theorem C3 (= note Thm 11.14), Lemma C5.
- The checker's Observation G (`data/round3/checks/R3M.md` §3): a slope-0 path alive at $n$ with $v(x+i)=s<V_n$ has $v(S_{e|_i}(-i))=s$; hence $Z^0_n=0$ when $p^{v(x+i)}>e\,(i-1)!$ for some $i\le n$ with $V_n>v(x+i)$.

Prop A holds for any product measure on digit strings: its proof counts per string $f$ (R3M Remark C6, checked as a sketch). For signed strings this is used in Lemma B3. We re-prove the needed instance there, so nothing rests on the sketch.

Two auxiliary facts:
- **(F3) Window valuation bound.** For $n\le j$: $V_j-V_n\le(j-n)/(p-1)+\max_{n<i\le j}v(x+i)$. Hence $c_j/c_n\le\theta^{j-n}p^{\max_{n<i\le j}v(x+i)}$. *Proof:* as R3M Lemma 1(b), applied to the $j-n$ consecutive elements $x+n+1,\dots,x+j$. ∎
- **(F4) Backward integrality for signed strings.** If $(\delta,f)$ is alive at age $a'$, then $\delta$ is alive at age $a<a'$. *Proof:* $F_\delta=F_{(\delta,f)}-\sum_{a\le c<a'}f_c\pi_c$ and $v(\pi_c(y))=V_c(y)\ge V_a(y)$. ∎

## 2. Adaptive window times (Theorem B1) [proved]

**Setting.**
- $n_0<n_1$ are deterministic with $n_0\ge2p$.
- For $\ell\ge1$, $n_{\ell+1}$ is a function of $x\bmod p^{m_{\ell-1}(x)}$ with $n_{\ell+1}>n_\ell$, where $m_\ell(x):=V_{n_\ell(x)}(x)$.
- $A_\ell(x):=x+p^{m_\ell(x)}\mathbb Z_p$, and $\mathcal G_\ell$ is generated by these sets.

**Lemma B1a (partition).** For every $\ell$:
- $n_0,\dots,n_{\ell+1}$ are constant on $A_\ell(x)$;
- $m_\ell$ is constant on $A_\ell(x)$;
- $\{A_\ell(x)\}$ is a partition of $\mathbb Z_p$ (up to the countable set of negative integers) that refines $\{A_{\ell-1}(x)\}$.

*Proof.* Induction on $\ell$.
- *Constancy of $m_\ell$.* Since $n_\ell\ge2p$, at least two of $x+1,\dots,x+n_\ell$ are divisible by $p$, so $M_{n_\ell}(x)<V_{n_\ell}(x)=m_\ell(x)$.
- *Base.* $n_0,n_1$ are deterministic, and for $y\in A_0(x)$, $v(y+i)=v(x+i)$ for $i\le n_0$. So $m_0(y)=m_0(x)$.
- *Step.* $m_\ell(x)\ge m_{\ell-1}(x)$, because $n_\ell\ge n_{\ell-1}$ and $V$ is nondecreasing. So $A_\ell(x)\subseteq A_{\ell-1}(x)$.
  - $n_{\ell+1}$ is a function of $x\bmod p^{m_{\ell-1}}$, hence constant on $A_{\ell-1}(x)\supseteq A_\ell(x)$. By induction, $n_0,\dots,n_\ell$ are constant on $A_{\ell-1}(x)$.
  - For $y\in A_\ell(x)$: $n_\ell(y)=n_\ell(x)$ and $v(y+i)=v(x+i)$ for $i\le n_\ell$, so $m_\ell(y)=m_\ell(x)$ and $A_\ell(y)=A_\ell(x)$. ∎

Define, as in R3M:
- $W_\ell=[n_\ell,n_{\ell+1})$, $D_\ell=m_{\ell+1}-m_\ell$, $M_\ell:=c_{n_\ell}Z^0_{n_\ell}$, $\chi^2_\ell=\chi^2_{W_\ell}$, $\varepsilon_\ell=\varepsilon(W_{\ell-1},W_\ell)$;
- $B_\ell=\{D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}},\ M_{n_{\ell+1}}<m_{\ell-1}\}\cap E_\ell\cap\{\varepsilon_\ell\le\bar\varepsilon_\ell\}$, where $E_\ell$ is any further $\mathcal G_{\ell-1}$-measurable event (a truncation, a ladder condition, ...);
- $\tau_j=\min\{\ell>j:x\notin B_\ell\}$, and admissibility of an atom of $\mathcal G_j$ as in R3M.

**$B_\ell$ is $\mathcal G_{\ell-1}$-measurable.**
- $n_{\ell-1},n_\ell,n_{\ell+1}$ are constant on atoms of $\mathcal G_{\ell-1}$ (Lemma B1a).
- $\{M_{n_{\ell+1}}<m_{\ell-1}\}$ says that $x+i\not\equiv0\bmod p^{m_{\ell-1}}$ for all $i\le n_{\ell+1}$, which is a condition on $x\bmod p^{m_{\ell-1}}$.
- On that event all valuations up to $n_{\ell+1}$ are determined.
- $\varepsilon_\ell$ depends only on $x\bmod p^{K}$, $K=D_{\ell-1}+D_\ell\le m_{\ell-1}$, because the $y_j$ are integer polynomials in $x$.

**Theorem B1.** With these random times, the statement and proof of Theorem 11.14 (R3M Theorem C3) hold verbatim. For an admissible atom $A$ of $\mathcal G_j$ with $\delta_A:=\mu_A(\tau_j<\infty)<1/\Pi_A$, where $\Pi_A=(1+\chi_j^2(A))\prod_{\ell>j}(1+\bar\varepsilon_\ell)$:
$$\mu(K_p\cap A)/\mu(A)\ \ge\ (1-\sqrt{\Pi_A\delta_A})^2/\Pi_A.$$

*Proof.* We re-check every step of R3M Theorem C3 that uses determinism of the times.
- *Martingale step.* On $\{\tau_j>\ell\}\in\mathcal G_{\ell-1}\subseteq\mathcal G_\ell$, Cor A′ is applied on an atom of $\mathcal G_\ell$ to the window $[n_\ell,n_{\ell+1})$. Both ends are constant on the atom (Lemma B1a), and (W2′), (W3′) follow from $B_\ell$ exactly as in R3M.
- *$L^2$ step.* Prop C2 is applied on an atom of $\mathcal G_{\ell-1}$ to the composite window $[n_{\ell-1},n_{\ell+1})$. All three times are constant there, because $n_{\ell+1}$ is a function of $x\bmod p^{m_{\ell-1}}$. This is why two-step predictability is required.
- *The rest* (monotonicity of $a_\ell$, the recursion $a_{\ell+1}\le(1+\bar\varepsilon_\ell)a_\ell$, Doob's $L^2$ convergence, survival ⟹ $K_p$ by Prop A(i), (F1) and backward integrality, Paley–Zygmund) does not use determinism of the times. ∎

**Theorem B1′ (global form).** Let $\mathrm{adm}_j\in\mathcal G_j$ be the union of the admissible atoms. Put $m_j^*:=\mathbb E[M_j\mathbf 1_{\mathrm{adm}_j}]$, $Q_j:=\mathbb E[(1+\chi_j^2)M_j^2\mathbf 1_{\mathrm{adm}_j}]$, $\Pi:=\prod_{\ell>j}(1+\bar\varepsilon_\ell)$ and $\delta:=\mu(\mathrm{adm}_j\cap\{\tau_j<\infty\})$. If $m_j^*>\sqrt{\Pi Q_j\delta}$, then
$$\mu(K_p)\ \ge\ \frac{(m_j^*-\sqrt{\Pi Q_j\delta})^2}{\Pi Q_j}.$$

*Proof.* Put $\tilde M_\ell:=M_{\min(\ell,\tau_j)}\mathbf 1_{\mathrm{adm}_j}$ for $\ell\ge j$ on all of $\mathbb Z_p$. On atoms inside $\mathrm{adm}_j$ this is R3M's stopped martingale; elsewhere it is $0$. So it is a $(\mathcal G_\ell)$-martingale.
- *Second moments.* $a_\ell:=\mathbb E\tilde M_\ell^2$ satisfies $a_j\le a_{j+1}\le Q_j$ (Prop B on each atom) and $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}$ (Prop C2 on atoms of $\mathcal G_{\ell-1}$ inside $\{\tau_j>\ell\}$, then integrate). Since $a_\ell$ is nondecreasing, $\sup a_\ell\le\Pi Q_j$.
- *$Q_j<\infty$.* By Observation G, $Z^0_{n_j}=0$ whenever some $i\le n_j$ has $p^{v(x+i)}>e\,(i-1)!$ and $v(x+i)<V_{n_j}$. On $\{Z^0_{n_j}\neq0\}$ every such valuation is therefore at most $\log_p(e\,(n_j-1)!)$; the case $v(x+i)\ge V_{n_j}$ is excluded because $V_{n_j}>M_{n_j}$. So $M_j\le p^{V_{n_j}}\le p^{n_j/(p-1)+\log_p(e(n_j-1)!)}$ there, and $M_j$ is bounded.
- *Conclusion.* With $Y:=\mathbf 1_{\{\tau_j=\infty\}}\tilde M_\infty$ we have $\{Y>0\}\subseteq K_p$ (as in R3M), $\mathbb EY\ge m_j^*-\sqrt{\Pi Q_j\delta}$ by Cauchy–Schwarz, and $\mathbb EY^2\le\Pi Q_j$. Paley–Zygmund finishes the proof. ∎

**Example of an admissible adaptive rule** (used in §4).
- Choose $n_{\ell+1}$ as the least $n\ge\lceil rn_\ell\rceil$ such that $n$ is a $C'$-ladder point for a horizon $T_{\max}$. The test uses the truncated valuations $\min(v(x+i),m_{\ell-1})$, which are functions of $x\bmod p^{m_{\ell-1}}$.
- If there is none below $\lceil rn_\ell\rceil+R$, take $n_{\ell+1}=\lceil rn_\ell\rceil+R$ and put this outcome into $E^c_{\ell+1}$, a $\mathcal G_\ell$-measurable stopping event.
- The ladder property is exact on $\{M_{n_{\ell+1}+T_{\max}}<m_{\ell-1}\}$, which is again $\mathcal G_{\ell-1}$-measurable; its complement also goes into the stopping event.

## 3. Gate splitting (Proposition B2) and deep gates [proved]

Fix a composite window and a split point $n+d$ with $1\le d\le N-n$. Put
- $g:=V_{n+d}-V_n$, so $0\le g\le D$;
- $A:=\sum_{n\le j<n+d}\delta_jy_j$ (the pre-sum);
- $B':=\sum_{n+d\le j<N'}\delta_j\,\pi_j(x)/\pi_{n+d}(x)$ (the signed sum of the post window $[n+d,N')$);
- $u:=y_{n+d}/p^g\in\mathbb Z_p^\times$, and $\rho'_k(r):=p^kP(B'\equiv r\bmod p^k)$ with $\rho'_0\equiv1$;
- $\varepsilon^{\rm post}:=\varepsilon([n+d,N),[N,N'))$ and $\Delta(r):=\rho'_{K-g}(r)-\rho'_{D-g}(r)$.

**Proposition B2.**
- (B2.1) $\displaystyle\varepsilon(W,W')=p^g\sum_{a\in p^g\mathbb Z_p}P(A=a)\,\Delta(r_a)$, with $r_a:=-(a/p^g)u^{-1}$.
- (B2.2) $\Delta(0)=\varepsilon^{\rm post}$.
- (B2.3) $|\Delta(r)|\le\varepsilon^{\rm post}$ for every $r$, and $\Delta(-r)=\Delta(r)$.
- (B2.4) $\varepsilon\le p^g\,\mathrm{Coll}^{\rm pre}_g\,\varepsilon^{\rm post}$, where $\mathrm{Coll}^{\rm pre}_g:=P(A\equiv0\bmod p^g)$.
- (B2.5) $\big|\varepsilon-p^gP(A\equiv0\bmod p^K)\,\varepsilon^{\rm post}\big|\le p^g\big(\mathrm{Coll}^{\rm pre}_g-P(A\equiv0\bmod p^K)\big)\varepsilon^{\rm post}$.

*Proof.*
- (B2.1) $\mathrm{Coll}_k=P(A+p^guB'\equiv0\bmod p^k)$ for $k\in\{D,K\}$, with $A$ and $B'$ independent. Since $k\ge g$, the event forces $p^g\mid A$. Given $A=a$ with $p^g\mid a$, it is the event $B'\equiv r_a\bmod p^{k-g}$, which has probability $p^{-(k-g)}\rho'_{k-g}(r_a)$. ($A$ takes finitely many values.) Multiply by $p^k$ and subtract.
- (B2.2) $B'$ has the signed law of the difference of two independent uniform subset sums of the post window. Also $K-g=V_{N'}-V_{n+d}$ and $D-g=V_N-V_{n+d}$. So $\Delta(0)$ is $\varepsilon$ of $([n+d,N),[N,N'))$ by definition.
- (B2.3) Let $\psi(\xi):=\mathbb Ee(\xi B'/p^{K-g})=|\mathbb Ee(\xi X/p^{K-g})|^2\ge0$. Fourier inversion gives $\rho'_{K-g}(r)=\sum_{\xi\bmod p^{K-g}}\psi(\xi)e(-\xi r/p^{K-g})$. The characters modulo $p^{D-g}$ are those with $\xi\in p^{K-D}\mathbb Z$. So
$$\Delta(r)=\sum_{\xi\notin p^{K-D}\mathbb Z}\psi(\xi)e(-\xi r/p^{K-g}),\qquad|\Delta(r)|\le\sum_{\xi\notin p^{K-D}\mathbb Z}\psi(\xi)=\Delta(0).$$
  Symmetry holds because $\psi$ is real and even.
- (B2.4) Take absolute values in (B2.1) and use (B2.3).
- (B2.5) Split off the values $a\equiv0\bmod p^K$, for which $r_a\equiv0\bmod p^{K-g}$ and so $\Delta(r_a)=\varepsilon^{\rm post}$. ∎

**Lemma B2a (factorial cancellation).** Let $\epsilon_0,\dots,\epsilon_{d-1}\in\{-1,0,1\}$ with $\sum_{k<d}\epsilon_k/k!=0$. Then $\epsilon_k=0$ for all $k\ge2$ and $\epsilon_0=-\epsilon_1$.

*Proof.* Suppose $\epsilon_k\neq0$ for some $k\ge2$, and let $k^*\ge2$ be the least such $k$.
- $(k^*+1+m)!\ge(k^*+1)!\,(k^*+2)^m$, so $\sum_{k>k^*}1/k!\le\frac{1}{(k^*+1)!}\cdot\frac{k^*+2}{k^*+1}<\frac1{k^*!}$, since $k^*+2<(k^*+1)^2$.
- Hence $0<|\sum_{k\ge k^*}\epsilon_k/k!|\le\sum_{k\ge2}1/k!=e-2<1$.
- But $\epsilon_0+\epsilon_1=-\sum_{k\ge k^*}\epsilon_k/k!$ is an integer. Contradiction. ∎

**Corollary B2′ (deep gate at distance $d$).** Let $s:=v(x+n+d)$ satisfy $p^s>e\,(d-1)!$ and assume $K>g$ (otherwise $D=K$ and $\varepsilon=0$). Then:
- (a) $v(x+n+i)=v(d-i)$ for $1\le i<d$, so $g=v((d-1)!)+s$ and $c_{n+d}/c_n=2^{-d}p^{v((d-1)!)+s}$.
- (b) For $d\ge2$: $\mathrm{Coll}^{\rm pre}_g=\frac32\,2^{-d}$ and $P(A\equiv0\bmod p^K)=2^{-d}$. For $d=1$ both are $\frac12$.
- (c) $\varepsilon=\dfrac{c_{n+d}}{c_n}\Big[\varepsilon^{\rm post}+\tfrac12\Delta\big(\tfrac1{x+n+d-1}\big)\Big]$ for $d\ge2$, and $\varepsilon=\dfrac{c_{n+1}}{c_n}\varepsilon^{\rm post}=\dfrac{p^s}2\varepsilon^{\rm post}$ for $d=1$ (here only $s\ge1$ is needed). In particular
$$\tfrac12\,\tfrac{c_{n+d}}{c_n}\,\varepsilon^{\rm post}\ \le\ \varepsilon\ \le\ \tfrac32\,\tfrac{c_{n+d}}{c_n}\,\varepsilon^{\rm post}.$$

*Proof.*
- (a) $x+n+i=(x+n+d)+(i-d)$ with $v(i-d)\le\log_p(d-1)<s$.
- (b), first part. $y_{n+i}=\prod_{k=1}^i(k-d+p^sw)$ with $w=(x+n+d)/p^s$, so $y_{n+i}\equiv(-1)^i(d-1)_i\bmod p^s$, where $(d-1)_i=(d-1)!/(d-1-i)!$. If $A\equiv0\bmod p^g$, then (as $g\ge s$) the integer $A_0:=\sum_{i<d}\delta_{n+i}(-1)^i(d-1)_i$ is divisible by $p^s$. But $|A_0|<e\,(d-1)!<p^s$, so $A_0=0$.
- Writing $k=d-1-i$ and $\epsilon_k=(-1)^k\delta_{n+d-1-k}$ gives $A_0=(-1)^{d-1}(d-1)!\sum_k\epsilon_k/k!$. By Lemma B2a the only solutions are $\delta_{\rm pre}=0$ and $\delta_{\rm pre}=\pm(e_{n+d-2}+e_{n+d-1})$.
- The latter give $A=\pm y_{n+d-2}(1+x+n+d-1)=\pm y_{n+d-2}(x+n+d)$, of valuation exactly $v((d-1)!)+s=g$. So $A\equiv0\bmod p^g$ and $A\not\equiv0\bmod p^K$.
- The probabilities are $2^{-d}$ and $2\cdot\frac1{16}2^{-(d-2)}=\frac12 2^{-d}$. For $d=1$, $A=\delta_n$.
- (c) Insert (b) into (B2.1). The two nonzero values $a=\pm y_{n+d-2}(x+n+d)$ give $r_a=\mp1/(x+n+d-1)$, and $\Delta$ is even. The bounds follow from (B2.3). ∎

So the round-3 heuristic $\kappa_\ell\approx p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}_\ell$ is **proved up to the factor $[\frac12,\frac32]$**. The correction is exactly the double root $(y+2)^2$ of note Prop 3.4, now seen from the window: the pair $\delta_{n+d-2}=\delta_{n+d-1}=\pm1$ just before the gate. In the exact tests the ratio is exactly $1$ for $d=1$, and lies strictly inside $[\frac12,\frac32]$ for $d\ge2$ ($1.352$, $1.434$, $1.357$; §8.1).

**Proposition N4 (the plain annealed mean is infinite).** Let $n<N<N'$ be fixed. Put $L:=N'-n-1$, $D_f:=v((N-n-1)!)$, $K_f:=v(L!)$, and assume $K_f>D_f$. Then $\int_{\mathbb Z_p}\varepsilon(W,W')\,d\mu=+\infty$.

*Proof.* Recall $\varepsilon\ge0$.
- Let $v(x+n+1)=s$. By Cor B2′ with $d=1$, $\varepsilon=\frac{p^s}2\varepsilon^{\rm post}$.
- The post elements are $z_k=\prod_{c=1}^k(c+p^sw)$, $0\le k<L$. Take $s\ge s_0:=K_f+\lfloor\log_pL\rfloor+1$. Then:
  - $v(c+p^sw)=v(c)$ for $c\le L$, so $D_{\rm post}=D_f$ and $K_{\rm post}=K_f$;
  - $z_k=k!\prod(1+p^sw/c)\equiv k!\bmod p^{K_f}$.
- So $\varepsilon^{\rm post}=\varepsilon_{\rm fact}$, the fine-scale mass of the elements $0!,\dots,(L-1)!$ in the band $(p^{D_f},p^{K_f}]$.
- $\varepsilon_{\rm fact}=\sum_{\rm band}|\hat\nu_{\rm fact}(\zeta)|^2>0$. The band is nonempty, and every factor $(1+e(\zeta k!/p^{K_f}))/2$ is nonzero because $p$ is odd.
- Hence $\int\varepsilon\,d\mu\ge\sum_{s\ge s_0}(1-p^{-1})p^{-s}\cdot\frac{p^s}2\varepsilon_{\rm fact}=\infty$. ∎

*Remarks.*
1. N4 upgrades the [heuristic] label that the round-3 check attached to "$\mathbb E[\varepsilon]$ is very probably infinite" (global Haar version). The check had sketched a proof for $N'-N\ge3$ via a double root in the second window; N4 uses a gate at distance $1$ instead and needs only a nonempty factorial band. Under admissibility ($M_{n_{\ell+1}}<m_{\ell-1}$) the deep gate is excluded. That is why every annealed route must truncate or use ladder starts (§4).
2. The divergent part has prefactor $\varepsilon_{\rm fact}/2$, which is **position-independent**: it is fixed by factorials. Table F (§8.3) shows that $\varepsilon_{\rm fact}$ does not decay at $p=3$ (about $0.02$–$0.1$ for $L=L'\le14$, i.e. up to $28$ factorials) and plateaus at $\approx4.5\cdot10^{-4}$ at $p=5$ ($L=L'=10$ to $20$), while it decays at $p=7$ ($6\cdot10^{-4}\to2.3\cdot10^{-8}$ up to $48$ factorials). This explains the round-3 finding that $\kappa$ "does not visibly decrease" at $p=3$. Our exact predictions $(3^s/2)\varepsilon_{\rm fact}$ reproduce the round-3 log $4.59,\ 13.8,\ 41.3$ as $4.587,\ 13.76,\ 41.28$ (§8.3). The literal round-3 heuristic "$\kappa_\ell$ decays exactly when typical $\varepsilon$ decays" is therefore **refuted** for deep gates [proved for the mechanism; the non-decay at $p=3,5$ is read off finitely many exact values, hence heuristic as an asymptotic statement]. At deep gates $\kappa$ is governed by the factorial window, not by the random one. [heuristic] A truncation level $s_\ell$ below about $D_{\ell-1}/2$ should keep the factorial part outside the band of $\varepsilon^{\rm post}$.

## 4. Ladder starts [proved]

**Definition.** A time $n$ is a *$C'$-ladder point for horizon $T$* if $c_{n+d}/c_n=2^{-d}p^{V_{n+d}-V_n}\le C'$ for $1\le d\le T$.

**Proposition B5.** Fix a composite window $[n,N')$, $C'\ge1$, and let $L$ be the event that $n$ is a $C'$-ladder point for $T=N'-n$. Let $s_1:=\lceil\log_p(e\,(N'-n)!)\rceil$ and $\mathrm{Deep}:=\{\exists\,d\le N'-n:\ v(x+n+d)\ge s_1\}$. Then
$$\int\varepsilon\,\mathbf 1_L\mathbf 1_{\rm Deep}\,d\mu\ \le\ \tfrac32C'\,(N'-n)\,p^{(N'-n)/(p-1)}\,p^{-s_1}\ \le\ \frac{\tfrac32C'(N'-n)\,p^{(N'-n)/(p-1)}}{e\,(N'-n)!}.$$
For fixed starts the same integral is $+\infty$ (Prop N4).

*Proof.*
- Since $p^{s_1}>N'-n$, at most one deep gate lies in $(n,N']$. Call its position $n+d$ ($1\le d\le N'-n$, in either window) and its depth $s\ge s_1$; then $p^s>e\,(d-1)!$.
- Put $g=V_{n+d}-V_n\le K$. The first step of the proof of (B2.1) uses only $K\ge g$, so it applies to this split point even when $n+d>N$. It gives
$$p^K\mathrm{Coll}_K=p^g\sum_{a\in p^g\mathbb Z_p}P(A=a)\rho'_{K-g}(r_a)\le p^g\,\mathrm{Coll}^{\rm pre}_g\,p^{K-g}.$$
- The argument of Cor B2′(b) uses only the pre-elements modulo $p^s$ and $p^s>e\,(d-1)!$, not $d\le N-n$. So $\mathrm{Coll}^{\rm pre}_g\le\frac32 2^{-d}$, hence $p^g\mathrm{Coll}^{\rm pre}_g\le\frac32c_{n+d}/c_n\le\frac32C'$ on $L$.
- After a gate this deep the valuations are factorial ($v(x+n+d+c)=v(c)$ for $c\le N'-n$), so $K-g=v((N'-n-d)!)\le(N'-n)/(p-1)$.
- Hence $\varepsilon\le p^K\mathrm{Coll}_K\le\frac32C'p^{(N'-n)/(p-1)}$ on $L\cap\mathrm{Deep}$, and $\mu(\mathrm{Deep})\le(N'-n)p^{-s_1}$. ∎

**Lemma B7 (ladder points exist).** Let $p\ge5$ and $C'=1$. Put $\alpha_p:=p\log_p2-1$ and $\beta_p:=\alpha_p-\frac1{p-1}$. Let $x+n\equiv0\bmod p$ and $z':=(x+n)/p$. If $M_k(z')\le\lfloor\beta_pk\rfloor$ for all $1\le k\le T/p$, then $n$ is a $1$-ladder point for horizon $T$. For Haar-random $x$ conditioned on $x+n\equiv0\bmod p$,
$$P(\text{not a ladder point})\le\sum_{k\ge1}k\,p^{-\lfloor\beta_pk\rfloor-1}.$$
This is $\le0.028$ at $p=7$, $\le0.32$ at $p=5$, and $\le8\cdot10^{-4}$ at $p=11$ (values $0.0275$, $0.3125$, $7.6\cdot10^{-4}$).

*Proof.*
- In $(n,n+d]$ only $i=kp$ has $v(x+n+i)\ge1$, and $v(x+n+kp)=1+v(z'+k)$. So $V_{n+d}-V_n=k+V_k(z')$ with $k=\lfloor d/p\rfloor$.
- By R3M Lemma 1(b), $V_k(z')<k/(p-1)+M_k(z')$. So $V_{n+d}-V_n<k(1+\alpha_p)=kp\log_p2\le d\log_p2$.
- $z'$ is Haar-distributed, and $P(M_k(z')>b)\le kp^{-(b+1)}$. ∎

At $p=3$ this crude criterion is useless; numerically, ladder points exist in every sample (§8.4). The probability that the search range contains no ladder point is a $\mathcal G$-measurable stopping event in Theorem B1. We do not bound it rigorously beyond the single-candidate bound of Lemma B7 [heuristic: 0 failures in 2400 samples, §8.4].

**What ladder starts buy, and what they do not.**
- *Deterministically* they bound the gate inflation of every gate by $C'$ times the accidental-collision factor $2^d\mathrm{Coll}^{\rm pre}_g$ (Prop B2). For deep gates that factor is exactly $\frac32$ (Cor B2′). So deep gates no longer inflate $\varepsilon$ (Prop B5).
- They do **not** give a deterministic bound on $\varepsilon$. For moderate gates the factor $2^d\mathrm{Coll}^{\rm pre}_g$ is only bounded by $2^{d-r}$, and $\varepsilon^{\rm post}$ is again a fine-scale mass of the same kind.
- A deterministic bound on the good event is not available by this route. Whether one exists at all is the barrier question (R3M §6, [heuristic]). An expectation bound is needed, and it is reduced to (S_B) in §6.

## 5. Conservation on Hensel balls (Lemma B3) [proved]

Let $y'\in\mathbb Z_p$ and ages $a<a'$. Let $\delta$ be a signed string of length $a$ (any $\delta_0$, finite slope) alive at age $a$ at $y'$, with slope $\lambda$. Put $m:=V_a(y')$, $M:=M_a(y')$, $M':=M_{a'}(y')$, $D:=V_{a'}(y')-m$. Assume

$$\text{(H) } m\ge2\lambda+M+1,\quad\text{(W1) } a'-a\ge p\lambda,\quad\text{(W2) } D+\lambda\le m-M,\quad\text{(W3) } \lambda<m-M'.$$

Let $B:=y'+p^{m-\lambda}\mathbb Z_p$ (the *Hensel ball*) and $\kappa_\delta(y):=\sum_{f\in\{-1,0,1\}^{a'-a}}P(f)\mathbf 1[(\delta,f)\text{ alive at }a'\text{ at }y]$.

**Lemma B3.**
- (a) On $B$: $v(y+i)=v(y'+i)$ for $i\le a'$, $\delta$ is alive at age $a$, and its slope is $\lambda$.
- (b) $\mathbb E_{y\in B}\big[p^{V_{a'}(y)}\kappa_\delta(y)\big]=p^{m}$. That is, the unweighted mass of $\delta$ is conserved on $B$.
- (c) On a single fine cylinder $C\subset B$ (modulo $p^m$) the same average is $p^m\rho(\delta)$ with $\rho=p^\lambda a^{(\lambda)}(s_\delta)$ (R3M Prop A). In general this is not $p^m$.

*Proof.*
- (a) $v(y'+i)\le M'<m-\lambda$ by (W3).
  - Write $F=F_\delta$ and $y=y'+h$ with $v(h)\ge m-\lambda$. Then $F(y)=F(y')+hF'(y')+\sum_{i\ge2}F^{[i]}(y')h^i$. The terms have valuations $\ge m$, $\ge m$ and $\ge2(m-\lambda)\ge m$ (by (H)).
  - Also $F'(y)=F'(y')+O(h)$ with $v(h)>\lambda$, so the slope is $\lambda$.
- (b) *Fine cylinders.* Let $y_u=y'+p^{m-\lambda}u$, $u\in\mathbb Z/p^\lambda$; these index the fine cylinders $C_u=y_u+p^m\mathbb Z_p$ inside $B$.
  - On $C_u$ the hypotheses of R3M Prop A hold with $L=\lambda$: they are (W1)–(W3) at $y_u$, with the same valuations.
  - *Per-string count.* R3M Lemma 2(b) holds for any integer polynomial alive on $C_u$, in particular for $F_\delta$. So, by the proof of R3M Prop A(iii), for each fixed $f$ the child $(\delta,f)$ is alive at $y_u+p^mw$ for a set of $w$ of probability $p^{\lambda-D}$ if $Q_f(y_u)\equiv\tau_a(\delta,y_u)\bmod p^\lambda$, and of probability $0$ otherwise. Summing over $f$ with the weights $P(f)$ gives
  - $\mathbb E_{C_u}\kappa_\delta=p^{\lambda-D}a^{(\lambda)}(s_u)$. Here $s_u=\tau_a(\delta,y_u)\bmod p^\lambda$, and $a^{(\lambda)}$ is the signed law of the next $p\lambda$ window elements modulo $p^\lambda$. (This uses $D\ge\lambda$, from (W1) and R3M Lemma 1(c).)
  - $a^{(\lambda)}$ is the same function for all $u$: it depends on $y\bmod p^\lambda$, and $m-\lambda\ge\lambda$.
  - Hence $\mathbb E_B[p^{V_{a'}}\kappa_\delta]=p^{m+D}p^{-\lambda}\sum_up^{\lambda-D}a^{(\lambda)}(s_u)=p^m\sum_ua^{(\lambda)}(s_u)$.
  - *The map $u\mapsto s_u$ is a bijection of $\mathbb Z/p^\lambda$.* Taylor's formula gives $F(y_u)/p^m=k_0+\beta u+p\,g(u)$, with $k_0=F(y')/p^m$, $\beta=F'(y')/p^\lambda$ a unit, and $g\in\mathbb Z_p[u]$. The terms $i\ge2$ carry $p^{i(m-\lambda)-m}$ with $i(m-\lambda)-m\ge m-2\lambda\ge1$ by (H).
  - Also $\pi_a(y_u)/p^m\equiv\pi_a(y')/p^m\bmod p^{m-\lambda-M}$, and $m-\lambda-M>\lambda$ by (H).
  - So $s_u\equiv-\omega^{-1}(k_0+\beta u+pg(u))\bmod p^\lambda$ with $\omega=\pi_a(y')/p^m$. A map $u\mapsto\beta u+pg(u)$ with $\beta$ a unit is injective modulo $p^\lambda$, because the difference quotient is $\beta+p(\cdots)$, a unit. So $\sum_ua^{(\lambda)}(s_u)=\sum_sa^{(\lambda)}(s)=1$.
- (c) This is R3M Prop A(iii) on one cylinder. ∎

*Why this matters.* R3M Remark C6 said that on slope classes visible to the windows the expected increments of $\Lambda$ vanish, because $p^{V}\sum P(\delta)\rho$ is a martingale. But $\Lambda$ and $\varepsilon$ involve the **unweighted** mass, and on a fine cylinder the increment of a slope-$\lambda\ge1$ string is $p^mP(\delta)(\rho-1)\neq0$. The exact tests find $\rho\ne1$ for 74/74 tested parents with $\lambda\ge1$ (§8.2). Lemma B3 shows the increment does vanish once one integrates over the whole Hensel ball. Under the global Haar measure, or on cylinders coarser than the ball, this repairs the sketch. Hypothesis (H) is used in an essential way: with (H) violated, the ball identity fails in 54 of 72 tested parents.

## 6. The reduction to non-regime mass (Theorem B4) and hypothesis (S_B)

Fix a composite window $[n,N')$ and $s\ge0$. Let $G:=\{\max_{n<i\le N'}v(x+i)\le s\}$, and let $\Omega$ be any further event determined by $(\min(v(x+i),s+1))_{n<i\le N'}$, for example a ladder condition.

For a $\Lambda$-process at $y$, a chain step $[a,a']$ and $s$, define the **regime**
$$R_s(a,a';y)=\Big\{\lambda:\ \lambda\le\min\Big(\Big\lfloor\tfrac{V_a-M_a-1}2\Big\rfloor,\ V_a-M_a-(V_{a'}-V_a),\ V_a-M_{a'}-1,\ \Big\lfloor\tfrac{a'-a}p\Big\rfloor,\ V_a-s-1\Big)\Big\},$$
with all valuations taken at $y$. The first four entries are (H), (W2), (W3), (W1). The last makes $\mathbf 1_G$, $\Omega$ and the weights $c_j/c_n$ constant on Hensel balls.

The **non-regime child mass** is
$$\mathrm{NR}_s(a,a';y):=\sum_{\delta\text{ alive at }a,\ \lambda_\delta(y)\notin R_s}P(\delta)\,p^{V_{a'}(y)}\kappa_\delta(y).$$

For each $j\in[n,N)$ fix a chain of ages $N-j=a^{(j)}_0<\dots<a^{(j)}_{k_j}=N'-j$.

**Theorem B4.**
$$\int\varepsilon\,\mathbf 1_G\mathbf 1_\Omega\,d\mu\ \le\ \int\frac{c_{N'}}{c_n}\mathbf 1_G\,d\mu+\frac12\sum_{n\le j<N}\sum_{i<k_j}\int\frac{c_j}{c_n}\mathbf 1_G\,\mathrm{NR}_s(a^{(j)}_i,a^{(j)}_{i+1};x+j)\,d\mu+\frac12\sum_{N\le j<N'}\int\frac{c_j}{c_n}\mathbf 1_G\,\Lambda_{N'-j}(x+j)\,d\mu .$$

*Proof.*
- *Expand.* Apply Lemma C5, telescope $\Lambda_{N'-j}-\Lambda_{N-j}$ along the chain, and drop $\mathbf 1_\Omega\le1$ in the first and last sums. By (F4), every string alive at $a'$ is uniquely $(\delta,f)$ with $\delta$ alive at $a$. So
$$\Lambda_{a'}(y)-\Lambda_a(y)=\sum_{\delta\text{ alive at }a}P(\delta)\big(p^{V_{a'}(y)}\kappa_\delta(y)-p^{V_a(y)}\big).$$
- *Regime part.* Fix $j$, a chain step and a string $\delta$. The set $S_\delta$ of $y$ at which $\delta$ is alive at $a$ with $\lambda_\delta(y)\in R_s(a,a';y)$ is a disjoint union of Hensel balls $B=y'+p^{V_a(y')-\lambda}\mathbb Z_p$.
  - By Lemma B3(a), every condition defining $R_s$ is constant on $B$.
  - Two balls of the same radius are equal or disjoint.
- *Constancy of the weights on each ball.* The ball radius exponent is $V_a-\lambda\ge s+1$. Hence on $G$ every $v(x+i)$ with $n<i\le N'$ is constant on the ball. So $\mathbf 1_G\mathbf 1_\Omega$ and $c_j/c_n$ are constant on the ball. Off $G$, $\mathbf 1_G=0$ on the whole ball.
- *The regime part vanishes.* By Lemma B3(b), $\int_B(p^{V_{a'}}\kappa_\delta-p^{V_a})\,d\mu=0$. The integrand is bounded on $G$, so summing over countably many balls and finitely many $\delta$ is legitimate. Hence the regime part of every increment integrates to $0$.
- *Non-regime part.* Bound it above by its positive part, which is $\mathrm{NR}_s$. ∎

**Hypothesis (S_B)$(p;\kappa,\vartheta,C_S)$.** For every $s\ge0$, every age $a\ge1$ and every chain step $a'\in(a,\lceil\frac32a\rceil+p]$,
$$h_s(a,a'):=\int_{\mathbb Z_p}\mathbf 1\{M_{a'}(y)\le s\}\,\mathrm{NR}_s(a,a';y)\,d\mu(y)\ \le\ C_S\,p^{\kappa s}\,\vartheta^a,\qquad\vartheta<1.$$
In words: under Haar measure, with forward gates truncated at depth $s$, the mass at the next chain time of the descendants of signed strings that are outside the Hensel/linear regime decays exponentially in the age, with at most a factor $p^{O(s)}$ lost to the truncation.

*Relation to strategy A's (S).* On $\{M_{a'}\le s\}$ with $a'\approx\frac32a$, the regime contains every $\lambda\le\frac{a}{2p}-2s-O(\log a)$ (use $V_a\ge v(a!)$, $V_{a'}-V_a\le(a'-a)/(p-1)+s$ and (F3)). So a bound on the Haar mass of descendants of strings with slope $>\theta a$ for some fixed $\theta<\frac1{2p}$, of the form $Cp^{\kappa s}\vartheta^a$, implies (S_B). Any such bound from strategy A should therefore be stated (i) under the global Haar measure (not per cylinder), (ii) with the forward truncation $M_{a'}\le s$, and (iii) for the child mass at the next chain time, not only the parent mass.

**Corollary B4′ [proved; conditional on (S_B)].** Assume (S_B). Take windows $n_{\ell+1}=\lceil rn_\ell\rceil$ with $1<r<\sqrt2$, and truncation levels $s_\ell=\lfloor\sigma(n_\ell-n_{\ell-1})\rfloor$ with $\sigma(1+\kappa)\log p\le\frac14\log\frac1{\max(\theta,\vartheta)}$. Let $B_\ell$ be defined with $E_\ell=G_\ell$ and $\bar\varepsilon_\ell=\max(\theta,\vartheta)^{(n_\ell-n_{\ell-1})/2}$. Then there are $C,c>0$ with $\mu(B_\ell^c)\le Ce^{-cn_\ell}$ for all $\ell$. In particular $\sum_{\ell>j}\mu(B_\ell^c)\le C'e^{-cn_j}$.

*Proof.*
- *Weights.* On $G$, (F3) gives $c_j/c_n\le\theta^{j-n}p^s$ and $\mathbf 1_G(x)\le\mathbf 1\{M_{a'}(x+j)\le s\}$. Shift $y=x+j$, which preserves Haar measure.
- *Boundary.* $c_{N'}/c_n\le\theta^{N'-n}p^s$ on $G$.
- *Middle sum.* By (S_B) it is at most $\frac12p^{(1+\kappa)s}C_S\sum_{j<N}\theta^{j-n}\sum_i\vartheta^{a^{(j)}_i}$. The chain ages are distinct and $\ge N-j$, so this is $\le\frac{C_S}{2(1-\vartheta)}p^{(1+\kappa)s}(N-n)\max(\theta,\vartheta)^{N-n}$.
- *Late births.* Telescope $\Lambda_b$ from age $1$ along a chain with the same Hensel-ball argument and weight $\mathbf 1\{M\le s\}$, and use $\Lambda_1\le1$. This gives $\int\mathbf 1\{M_b\le s\}\Lambda_b\le1+C_Sp^{\kappa s}/(1-\vartheta)$. So the last sum is $\le\frac{1+C_Sp^{\kappa s}/(1-\vartheta)}{2(1-\theta)}p^s\theta^{N-n}$.
- *Markov.* Altogether $\int\varepsilon_\ell\mathbf 1_{G_\ell}\le C''(N-n+1)p^{(1+\kappa)s_\ell}\max(\theta,\vartheta)^{N-n}\le C''(N-n+1)\max(\theta,\vartheta)^{3(N-n)/4}$ by the choice of $\sigma$. Markov's inequality with $\bar\varepsilon_\ell=\max(\theta,\vartheta)^{(N-n)/2}$ gives $\mu(G_\ell\cap\{\varepsilon_\ell>\bar\varepsilon_\ell\})\le C''(N-n+1)\max(\theta,\vartheta)^{(N-n)/4}$, and $\sum_\ell\bar\varepsilon_\ell<\infty$.
- *Measurability.* $G_\ell$ is defined through $\min(v(x+i),m_{\ell-1})$, so it is $\mathcal G_{\ell-1}$-measurable; it coincides with $\{\max v(x+i)\le s_\ell\}$ once $s_\ell<m_{\ell-1}$, which holds for all large $\ell$ when $\sigma$ is small.
- *Truncation and linear regime.* $\mu(G_\ell^c)\le(n_{\ell+1}-n_{\ell-1})p^{-s_\ell}$. The linear-regime part has measure $\le n_{\ell+1}p^{-\lfloor\gamma_\ell/2\rfloor-1}$ by the global form of R3M Lemma C4 (same union bound, with no atom).
- All three are exponentially small in $n_\ell$, because $n_\ell-n_{\ell-1}\ge(r-1)n_{\ell-1}$ and $\gamma_\ell\asymp(2-r^2)n_{\ell-1}/(p-1)$. ∎

The same holds for ladder windows. One takes a union over the possible positions of $(n_{\ell-1},n_\ell,n_{\ell+1})$, which costs a polynomial factor, and uses Theorem B4 with $\Omega=$ the ladder event.

## 7. The initial-phase gap [obstruction]

Corollary B4′ makes late failures exponentially rare. It still does not give $\mu(K_p)>0$. Both conclusions available need the start of the process:

- **Per atom (Theorem B1).** One needs an admissible atom $A$ at some time $j$ with $\delta_A<1/\Pi_A$.
  - For the first $k_0\approx\log\frac1{r-1}/\log r$ windows after $j$ (about $6$ for $r=1.25$), the oldest $\Lambda$-processes in $\varepsilon_\ell$ are younger than the atom's resolution, i.e. $V_{\rm age}<m_j$. Their Hensel balls are not contained in $A$, so Lemma B3 cannot be applied inside $A$. For $\ell=j+1$, $\varepsilon_{j+1}$ is even a constant on $A$, since $K_{j+1}\le m_j$.
  - There is a trivial transfer: $\mu_A(B^c_\ell)\le p^{m_j}\mu(B^c_\ell)$. With Cor B4′ it gives
$$\delta_A\le\sum_{j<\ell\le\ell_1}\mu_A(B^c_\ell)+p^{m_j}C'e^{-cn_{\ell_1}}\qquad\text{for every }\ell_1>j.$$
  So the gap is a **finite computation** for one atom: the exact failure probabilities $\mu_A(B^c_\ell)$ for $j<\ell\le\ell_1$, where $\ell_1$ makes $p^{m_j}C'e^{-cn_{\ell_1}}$ small.
  - With $j$ small, the factor $p^{m_j}$ is a constant (e.g. $m_j=2$, $n_j=14$ at $p=7$), but early linear-regime failures are frequent. With the rates expected from (S_B) at $p=7$ ($\vartheta\approx p^{-1/(2(p-1))}\approx0.85$ [heuristic]), $n_{\ell_1}$ is in the hundreds and the windows have $K$ in the tens. Exact evaluation of $\varepsilon$ costs $p^K$, so this is far beyond reach.
- **Global (Theorem B1′).** One needs $m^*_j>\sqrt{\Pi Q_j\delta}$ at a time $j$ where $\delta\le C'e^{-cn_j}$ is small. This amounts to a lower bound on the Paley–Zygmund ratio $m_j^{*2}/Q_j$ at large $j$. That in turn requires second-moment control from the start, which is circular.
- **Survival lower bounds do not close it.** A good atom with $Z^0\neq0$ is guaranteed if $\mu(Z^0_{n_j}\neq0,\mathrm{adm}_j)>\Pi\,\mu(\tau_j<\infty)$. Single-path constructions give only $\mu(Z^0_{n}\ne0)\gtrsim p^{-n/(p-1)}$, i.e. rate $\log p/(p-1)\approx0.32$ at $p=7$ (per unit of $n$). The failure rates obtainable here are smaller, for every $r>1$.
  - The linear-regime failure $\{M_{n_{\ell+1}}>m_{\ell-1}-K_\ell\}$ has probability of order $n_{\ell+1}p^{-(2-r^2)n_{\ell-1}/(p-1)}$. Its rate $(2-r^2)\log p/(p-1)$ is $<\log p/(p-1)$ for every $r>1$ (it is $0.14$ at $p=7$, $r=1.25$).
  - The FE failures from Cor B4′ decay at rate at most $\frac14(r-1)\log\frac1{\max(\theta,\vartheta)}$, which tends to $0$ as $r\to1$.

So a proof of $\mu(K_7)>0$ along these lines needs (S_B) **and** either an explicit-constant version of it plus a large finite computation for one atom, or a new idea for the early windows. Round 3 did not identify this second gap.

## 8. Numerical tests

All runs are in `data/round4/M4B/`, each with its command line at the top. Exact means Python integers and `Fraction`; heuristic runs use float64. Every run was under `nice -n 10` and took at most about 6 minutes.

### 8.1 Proposition B2 and Corollary B2′ (exact) — `b2_gate_split.log`
- *Random $x$:* $p=3$ ($n=16,24,40$), $p=5$ ($20,30$), $p=7$ ($21,28$), every split point $d$.
- *Forced gates:* $(p,d,s)=(3,4,5),(3,1,5),(5,2,5),(7,3,4),(7,1,4)$.
- *Results:* (B2.1)–(B2.5) hold in **1048 (sample, split) pairs, 0 failures** (142 samples). (One forced-gate configuration, $(3,1,6)$ with KMAX 12, had no sample under the cap; it was re-run as $(3,1,5)$.)
- *Negative control:* replacing $u^{-1}$ by $1$ (`NEG=1`) makes the identity fail in 114/120 pairs.
- *Corollary B2′:* at forced deep gates the run finds $2^d\mathrm{Coll}^{\rm pre}_g=1.5$ and $2^dP(A\equiv0\bmod p^K)=1$ exactly. The ratio $\varepsilon/((c_{n+d}/c_n)\varepsilon^{\rm post})$ is $1$ for $d=1$ (exact) and $1.352,\ 1.434,\ 1.357$ for $d=4,2,3$, all inside $[\frac12,\frac32]$.

### 8.2 Lemma B3 (exact) — `b3_ball.log`
- *Design.* Parents (slope $\lambda\ge1$, or $\ge2$ in the second run, satisfying (H), (W1)–(W3)) are found by a pruned randomised search. Children are found by direct evaluation of $F$ at every $y$ in the ball modulo $p^{m+D}$.
- *Results.*

| $p$ | ages $a\to a'$ | parents | ball identity exact | fine-cylinder $\rho\neq1$ |
|---|---|---|---|---|
| 3 | 18→21 ($\lambda\ge1$) | 24 | 24/24 | 24/24 |
| 3 | 24→30 ($\lambda\ge2$) | 18 | 18/18 | 18/18 |
| 5 | 25→30 | 24 | 24/24 | 24/24 |
| 7 | 35→42 | 8 | 8/8 | 8/8 |

- *Controls.*
  - Parents violating (H), at ages $12\to15$ ($p=3$) and $10\to15$ ($p=5$): the identity holds in only 18/27 and 0/45.
  - Parents violating at least one of (H), (W1)–(W3), at ages $18\to21$ ($p=3$) and $20\to24$ ($p=5$): the identity held in 33/33. A re-enumeration shows that these were mostly (W1) violations, some together with (H).
  - So (H) cannot be dropped in general. The hypotheses are sufficient; whether (W1)–(W3) can be relaxed was not tested systematically.

### 8.3 Proposition N4 and factorial windows (exact) — `n4_infinite_mean.log`, `eps_factorial.log`, `r3m_kappa_compare.log`
- *N4 mechanism.* $\varepsilon=(p^s/2)\varepsilon_{\rm fact}$ holds exactly for $s_0\le s\le s_0+3$ in 12/12 ($p=3$, $n=20$), 12/12 ($p=5$), and 12/12 + 8/8 ($p=7$).
  - The first version used a dense residue array and was too slow at large $K$. Its $p=5$ run was killed by hand after three exact agreements (logged). The re-run uses a sparse subset-sum dictionary; it agrees with the dense version on the overlapping $p=3$ run.
- *Table F (exact values of $\varepsilon_{\rm fact}$, split after $L$ factorials, second part $L'$):*

| $p$ | $(L,L')$ → $\varepsilon_{\rm fact}$ |
|---|---|
| 3 | (4,4) 0.0146; (6,6) 0.102; (8,8) 0.104; (10,10) 0.0224; (12,12) 0.0214; (14,14) 0.0360 |
| 5 | (5,5) 0.0212; (8,8) 0.0216; (10,10) 4.10e-4; (12,12) 4.10e-4; (15,15) 4.47e-4; (18,18) 4.76e-4; (20,20) 4.49e-4 |
| 7 | (7,7) 6.09e-4; (14,14) 1.27e-5; (21,21) 3.61e-6; (14,7) 9.11e-6; (28,14) 2.34e-8; (32,16) 2.34e-8 |

- *Comparison with round 3 ($p=3$, gate at distance 1).* For the window $[16,26)$ the prediction $(3^s/2)\varepsilon_{\rm fact}=4.587,\ 13.76,\ 41.28$ at $s=4,5,6$ matches the round-3 medians $4.59,\ 13.8,\ 41.3$. For $[24,40)$: $4.23,12.7,38.0$ vs $4.12,12.5,38$. For $[32,52)$ the depths $s\le6$ are below the factorial regime ($K_{\rm post}=8$), and the round-3 values lie below the $s\to\infty$ prediction, as Cor B2′ allows.

### 8.4 Ladder vs fixed starts [heuristic] — `ladder_vs_fixed.log`
Haar-random $x$; exact $\varepsilon$ per sample; $C'=1$, $r=1.25$; the ladder start is the first $1$-ladder point $\ge n_0$.

| $p$, $n_0$ | samples | fixed: median / 99% / max / mean | ladder: median / 99% / max / mean | $P(\varepsilon>0.05)$ fixed → ladder |
|---|---|---|---|---|
| 7, 21 | 400 | 0.016 / 2.28 / 11.2 / 0.111 | 0.014 / 0.12 / 0.28 / 0.017 | 0.172 → 0.060 |
| 7, 28 | 400 | 0.016 / 2.28 / 10.9 / 0.108 | 0.0026 / 0.093 / 0.18 / 0.0083 | 0.255 → 0.028 |
| 7, 35 | 300 | 0.0064 / 0.73 / 2.32 / 0.035 | 0.0035 / 0.13 / 0.18 / 0.011 | 0.107 → 0.053 |
| 7, 42 | 300 | 0.0034 / 0.18 / 0.44 / 0.011 | 0.0011 / 0.059 / 0.17 / 0.0048 | 0.023 → 0.010 |
| 5, 20 | 400 | 0.063 / 72.7 / 228 / 1.88 | 0.021 / 1.2 / 1.24 / 0.084 | 0.603 → 0.170 |
| 5, 30 | 300 | 0.087 / 8.67 / 43.8 / 0.50 | 0.022 / 1.25 / 1.28 / 0.094 | 0.567 → 0.313 |
| 3, 24 | 300 | 0.32 / 59.9 / 127 / 2.66 | 0.070 / 1.47 / 1.48 / 0.16 | 0.907 → 0.660 |

- A ladder point was found within 30–40 steps in every sample (2400 total).
- The gain is not only in the tail. Shallow gates at distance 1 or 2 already inflate $\varepsilon$ by exactly $p^s/2$ or by a factor of order $p/4$ (Cor B2′, $d=1,2$). A $1$-ladder start excludes them.
- For an initial-phase computation (§7) this is the most useful practical consequence of strategy B.

### 8.5 Slope profile of the signed process [heuristic] — `slope_profile.log`
Haar $y$, truncated at $M_a\le s_G$, float64 DP over $(F\bmod p^{V_a},F'\bmod p^{LL})$. The *Hensel-failure share* is the share of $\Lambda_a$ carried by strings with $\lambda>(V_a-M_a-1)/2$.
- *Unstratified shares* (heavy-tailed): $p=7$, $a=14,21,28$: $0.62,0.63,0.34$; $p=5$, $a=10,\dots,25$: $0.53,0.63,0.30,0.32$; $p=3$, $a=6,\dots,15$: $0.76,0.76,0.51,0.45$.
- *Stratified by an early gate of depth $\ge2$ within $p$ steps of the start:*
  - $p=7$, $a=21$: 21 samples with such a gate carry $\mathbb E\Lambda=5.6$ and share $0.94$; the other 177 have $\mathbb E\Lambda=0.73$, share $0.35$, median per-sample share $0.047$.
  - $p=5$, $a=20$: $2.46$, $0.89$ vs $0.73$, $0.10$.
  - $p=3$, $a=15$: $1.11$, $0.87$ vs $0.49$, $0.08$.
- *Reading.* The high-slope mass at accessible ages is mostly the gate-induced exact-double-root mass of Cor B2′/Prop N3. Its slope is about the gate depth, so it should enter the regime once $V_a/2$ exceeds the gate depth plus $M$. In the stratum without early gates the Hensel-failure share is 8–35% (median per-sample share $\le5\%$). The thresholds there are $0$ or $1$, so this share is essentially the mass of slopes $\ge1$ or $\ge2$.
- A 30-sample pilot at $p=7$, $a=21$, $s_G=2$ (logged at the end of `slope_profile.log`) gave unstratified slope shares close to the Kac–Rice shares $(1-\frac1p)p^{-\lambda}$. The 200-sample run shows that the heavy tail from early gates dominates the mean, so that agreement was a small-sample effect.
- *Limits.* The thresholds reachable here are $\le1$, so (S_B), an asymptotic statement, **cannot** be tested in the regime where it matters. This is evidence for plausibility only.

## 9. Failed attempts and where they break

1. **A deterministic bound on $\varepsilon$ on the adaptive good event.** Prop B2 reduces a window with a deep gate near its start to the post-gate window, with an exactly known factor (Cor B2′). For shallow gates the accidental-collision factor $p^g\mathrm{Coll}^{\rm pre}_g$ has only the deterministic bound $p^g2^{-r}$ ($r$ = number of distinct levels), which grows exponentially. And $\varepsilon^{\rm post}$ is the same kind of object. The route breaks there; an expectation bound is unavoidable.
2. **Markov on the plain annealed mean.** It breaks at Prop N4: $\int\varepsilon\,d\mu=\infty$ for every fixed composite window with nonempty factorial band.
3. **"Slope classes visible to the windows have zero expected increment" (R3M Remark C6), on fine cylinders.** It breaks for every slope $\lambda\ge1$: $\rho\neq1$ (74/74 exact). Lemma B3 repairs it on Hensel balls, at the price of the additional hypothesis (H), i.e. $\lambda\le(V-M-1)/2$ (not comparable with (W2) in general).
4. **Applying Theorem B4 per atom right after the atom's time.** It breaks because the Hensel balls of the oldest processes are larger than the atom for about $\log\frac1{r-1}/\log r$ windows (§7).
5. **Existence of a good atom from global bounds and a survival lower bound.** It breaks at the mismatch of rates: the single-path survival bound decays at rate $\log p/(p-1)$, faster than any failure rate available here for $r>1$ (§7).
6. **Testing (S_B) numerically.** The thresholds where (S_B) is meaningful need $V_a\gtrsim10$, i.e. $a\gtrsim60$ at $p=7$, and a state space $p^{V_a+LL}$. At accessible ages the non-regime share is dominated by gate-induced double roots (§8.5), so the test is inconclusive.

## 10. What remains open, exactly

1. **(S_B)** (§6): a Haar first-moment bound $h_s(a,a')\le C_Sp^{\kappa s}\vartheta^a$ for the non-regime child mass of the signed carry process. This is the coordination point with strategy A's (S): any bound on high-slope signed mass of that shape (global Haar, forward truncation $M\le s$, loss $p^{O(s)}$, child mass at the next chain time) suffices.
   - The heuristic rate is $\vartheta\approx p^{-1/(2(p-1))}$, from the Kac–Rice picture; this needs a proof.
   - [heuristic] Gate-induced exact double roots have slope about the gate depth, hence at most about $s$ on the truncation event. They fall inside the regime once its threshold (about $\min(V_a/2,\frac a{2p})-2s$) exceeds $s$. Cor B4′ keeps $s_\ell=\sigma(n_\ell-n_{\ell-1})$ small compared with the ages involved, so these strings should not obstruct (S_B) asymptotically.
2. **The initial phase** (§7): an atom $A$ at some time $j$ with $\sum_{j<\ell\le\ell_1}\mu_A(B^c_\ell)+p^{m_j}C'e^{-cn_{\ell_1}}<1/\Pi_A$, or a new argument for the first windows. This needs explicit constants in (S_B). Ladder starts reduce the early failure probabilities by large factors (§8.4).
3. **Ladder search failure:** a rigorous bound, beyond Lemma B7's single-candidate bound, for the probability that no ladder point lies in the search range, and a version for $p=3$.
4. **$\varepsilon_{\rm fact}$:** whether the factorial fine-scale masses decay at $p=3,5$. Table F says no in range. This only affects how low the truncation level must be, not the logic.

## 11. Credit

- The window identity, second-moment identity, two-window inequality, Theorem C3, Lemmas C4 and C5 and Remark C6 are track R3M's (round 3). Observation G is the round-3 checker's.
- The $p=2$ quenched martingale and frozen weights are track R1b's (round 2; note §10.1). The stopped-martingale bookkeeping with explicit failure events follows track R3Q (round 3).
- Classical tools: the Paley–Zygmund inequality, Doob's $L^2$ martingale convergence, Hensel's lemma, Fourier inversion on $\mathbb Z/p^k$. The second-moment method on trees follows Lyons (1990, 1992); branching processes in random environments: Smith–Wilkinson (1969), Athreya–Karlin (1971), Afanasyev–Geiger–Kersting–Vatutin (2005). The Kac–Rice comparison in §8.5 is a heuristic in the spirit of Kac's formula for real zeros, transplanted to $\mathbb Z_p$ without proof.
- The double root $(x+2)^2$ is note Proposition 3.4. The problem is due to Erdős and Graham.
- Everything here was produced in an AI-assisted session (track M4B of round 4). It has not been checked by a human or by an independent checker.
