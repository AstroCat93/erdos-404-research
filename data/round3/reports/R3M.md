# Round 3, track R3M: odd primes, Haar measure of $K_p$ (Conjecture 5.2)

Date: 2026-10-13. Code: `code/round3/R3M/`. Logs: `data/round3/R3M/`.
Notation follows note.md (§1.2, §1.4, §10.1); everything needed is restated in §1 below.

## Headline

**$\mu(K_p)>0$ is still not proved for any odd prime $p$.** What this track establishes:

1. **[proved]** The exact first-moment machinery of note.md §10.1 carries over to every odd prime: an odd-$p$ linearisation lemma (Lemma 2), the one-window identity with truncation at $p\lambda$ terms and frozen-state weights $p^\lambda a^{(\lambda)}$ (Proposition A), and the resulting quenched martingale with the exponentially decaying normaliser $c_n=2^{-n}p^{V_n}$ (Corollary A′). Tested exactly, state by state, by two programs sharing no code at $p=3,5,7$ **[computer-assisted corroboration; the proof does not depend on it]**.
2. **[proved]** An exact second-moment identity for the slope-0 population (Proposition B): the conditional variance of the martingale after one window equals the Fourier overlap between the window's subset-sum law and the *Newton points* (Hensel roots) of the population's polynomials $S_e$. This makes precise which independence fails in the branching-process-in-random-environment picture: the offspring counts of different parents are deterministic functions of the **same** fresh digits $w$ of $x$, namely $X_e(w)=m_W(\beta_e(\varphi_e-w))$.
3. **[obstruction, proved]** The Cauchy–Schwarz route of the task description cannot work, for any choice of windows and independently of gates: every window has $\chi^2_W\ge(p-1)4^{-p}$ (the mod-$p$ shell alone; Proposition N), so $\prod_\ell(1+\chi_\ell^2)=\infty$.
4. **[proved] A way around it, and a conditional theorem.** Applying Cauchy–Schwarz only at *high* frequencies, through two consecutive windows, gives an exact-constant inequality (Lemma C1, Proposition C2):
$$\mathbb E\big[M_{\ell+1}^2-M_\ell^2\,\big|\,\mathcal G_{\ell-1}\big]\le\varepsilon_\ell\,M_{\ell-1}^2,$$
where $\varepsilon_\ell$ is the $L^2$ Fourier mass of the composite window $[n_{\ell-1},n_{\ell+1})$ in the frequency band $(p^{D_{\ell-1}},p^{D_{\ell-1}+D_\ell}]$ ("fine-scale equidistribution"). Consequently (**Theorem C3**): if on one cylinder $A$ with a nonempty slope-0 population the probability that some later window violates $\varepsilon_\ell\le\bar\varepsilon_\ell$ (with $\sum\bar\varepsilon_\ell<\infty$) or the linear-regime condition is below an explicit threshold, then $\mu(K_p\cap A)>0$. **The hypothesis no longer mentions the population at all**: it is a statement about subset sums of the products $(x+n+1)\cdots(x+j)$ for Haar-random $x\in A$. Its linear-regime part is controlled rigorously (Lemma C4); the equidistribution part is **unproved** and is of barrier-lemma type (§6). Numerically FE is plausible at $p=7$ (and $p=5$) but doubtful at $p=3$, where a deep gate near the start of a window inflates $\varepsilon_\ell$ by $\approx p^{\text{depth}}$ with a prefactor that does not visibly decay (Proposition N3 and the discussion after it).
5. **[proved, negative]** The averaged form of FE cannot be obtained naively: the signed densities $\Lambda_t$ that control $\varepsilon_\ell$ (Lemma C5) have infinite mean, because of the double root of $(x+2)^2$ at $-2$ (Proposition N3).
6. **[heuristic]** Monte Carlo (two independent counters, cross-checked): the slope-0 martingale has constant mean and a second moment that stabilises at $p=3,5,7,11$. Paley–Zygmund ratios $\mathbb E[M^2]/\mathbb E[M]^2\approx20.6,\,5.4,\,2.2,\,1.8$. The true conditional variance is $0.4$–$0.8$ times the "independent" (diagonal) value and $4\cdot10^{-4}$–$2\cdot10^{-2}$ times the Cauchy–Schwarz bound (medians, $p=3$). The fine-scale masses $\varepsilon_\ell$ decay steadily along the windows at $p=7$, more slowly at $p=5$, and not visibly at $p=3$; their tails are driven by deep gates.

Even a proof of $\mu(K_p)>0$ would not place a natural number in $K_p$: $K_p$ is nowhere dense (note.md Theorem 3.6), and a measure statement cannot see a countable set. Nothing here bears on Q3.

## 0. Results at a glance

| # | Statement | Status |
|---|---|---|
| Lemma 1 | valuation facts at odd $p$ | proved |
| Lemma 2 | odd-$p$ linearisation (analogue of note Lemma 10.5) | proved |
| Prop A | one-window identity, slope $\le L$, truncation $p\lambda$, weights $p^\lambda a^{(\lambda)}$ (analogue of note Prop 10.6) | proved; exact tests by two programs |
| Cor A′ | quenched martingale $c_n\sum\rho$, $c_n=2^{-n}p^{V_n}\to0$ | proved |
| Prop B | pointwise child counts and exact conditional second moment (slope 0) | proved; exact tests |
| Prop N | $\chi^2_W\ge(p-1)4^{-p}$ for every window; the per-window Cauchy–Schwarz recursion diverges | obstruction (proved) |
| Lemma C1 | fresh randomness: child targets have conditional Fourier mean $0$; one-window Fourier bound | proved; exact tests |
| Prop C2 | two-window inequality $\mathbb E[M_{\ell+1}^2-M_\ell^2\mid\mathcal G_{\ell-1}]\le\varepsilon_\ell M_{\ell-1}^2$ | proved; exact tests |
| Thm C3 | conditional positive measure on a cylinder, hypothesis FE (fine-scale equidistribution of composite windows) | proved (hypothesis unproved) |
| Lemma C4 | deep gates are rare on a cylinder (explicit bound for the linear-regime part of the stopping time) | proved |
| Lemma C5 | exact decomposition of the fine-scale mass $\varepsilon$ through the signed carry process | proved; exact tests |
| Remark C6 | reduction of an averaged FE to a first-moment statement (S) about high-slope signed paths | sketch; (S) open |
| Prop N3 | the signed densities $\Lambda_t$ have infinite mean (double root at $-2$); averaged FE needs truncation at deep gates | negative (proved) |
| §7 | Monte Carlo: $L^2$-boundedness of the slope-0 martingale; spectral flatness; scans of $\varepsilon_\ell$ | heuristic |

## 1. Notation and standing facts

Throughout, $p$ is an **odd** prime, $v=v_p$, $\mu$ is Haar probability measure on $\mathbb Z_p$, $e(t)=\exp(2\pi i t)$.

- $\pi_j(x)=\prod_{i=1}^j(x+i)$, $V_n(x)=v(\pi_n(x))$, $M_n(x)=\max_{1\le i\le n}v(x+i)$, $c_n(x)=2^{-n}p^{V_n(x)}$.
- For a polynomial $F$, $F^{[i]}=F^{(i)}/i!$.
- A *path of length $n$* is $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$; $S_e(X)=\sum_{j<n}e_j\pi_j(X)\in\mathbb Z[X]$. This is $S_B$ of note §1.2 with $B=\{j\ge1:e_j=1\}$.
- $e$ is *alive at $n$* (for $x$) if $v(S_e(x))\ge V_n(x)$. Its *target* is $\tau_n(e,x)=-S_e(x)/\pi_n(x)\in\mathbb Z_p$ and its *slope* is $\lambda_e(x)=v(S_e'(x))$.
- For $n<N$ and $f\in\{0,1\}^{N-n}$: $Q_f(X)=\sum_{j=n}^{N-1}f_{j-n}\pi_j(X)/\pi_n(X)\in\mathbb Z[X]$ (note $\pi_j/\pi_n=(X+n+1)\cdots(X+j)$), and $(e,f)\in\{0,1\}^N$ is the concatenation. We call $W=[n,N)$ a *window*, $D=V_N(x)-V_n(x)$ its *jump*.
- $P^{1,L}_n(x)$ is the set of paths alive at $n$ with $\lambda_e(x)\le L$; $P^0_n(x):=P^{1,0}_n(x)$ is the *slope-0 population*, $Z^0_n=|P^0_n|$.

**(F1) Survival implies $K_p$.** If for every $n$ some path is alive at $n$, then $x\in K_p$: such a path gives $B\subseteq[1,n)$ with $v(S_B(x))\ge V_n(x)\ge v(n!)\to\infty$, so $g_p(x)=\infty$.

**(F2) Backward integrality.** If $(e,f)$ is alive at $N$ then $e$ is alive at $n$: $S_e=S_{(e,f)}-\sum_{n\le j<N}f_{j-n}\pi_j$ and $p^{V_n}\mid\pi_j$ for $j\ge n$. Moreover $S_{(e,f)}=\pi_n\,(Q_f-\tau_n(e,\cdot))$, so for $e$ alive at $n$: $(e,f)$ is alive at $N$ iff $\tau_n(e,x)\equiv Q_f(x)\pmod{p^{D}}$, and then $\tau_N((e,f),x)=(\tau_n(e,x)-Q_f(x))\,\pi_n(x)/\pi_N(x)$.

**Lemma 1 (valuations) [proved].** Let $x\in\mathbb Z_p$ with $x+i\ne0$ for $1\le i\le n$.
- (a) $V_n\ge v(n!)=(n-s_p(n))/(p-1)$.
- (b) $V_n\le n/(p-1)+M_n$.
- (c) $V_j-V_n\ge\lfloor (j-n)/p\rfloor$ for $j\ge n$.
- (d) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$ for $i\ge0$.
- (e) For $S\in\mathbb Z_p[X]$ and $y,h\in\mathbb Z_p$: $S(y+h)=\sum_iS^{[i]}(y)h^i$ with $S^{[i]}(y)\in\mathbb Z_p$.

*Proof.* (a) Among $n$ consecutive elements of $\mathbb Z_p$ at least $\lfloor n/p^\ell\rfloor$ are divisible by $p^\ell$; sum over $\ell\ge1$ (Legendre). (b) At most $\lceil n/p^\ell\rceil\le n/p^\ell+1$ of them are divisible by $p^\ell$, and none by $p^{M_n+1}$; so $V_n\le\sum_{\ell=1}^{M_n}(n/p^\ell+1)<n/(p-1)+M_n$. (c) Among $x+n+1,\dots,x+j$ at least $\lfloor(j-n)/p\rfloor$ are divisible by $p$. (d) $\pi_j^{[i]}(x)=\pi_j(x)\,e_i\big(\frac1{x+1},\dots,\frac1{x+j}\big)$ ($e_i$ elementary symmetric), and each $1/(x+i)$ has valuation $\ge-M_j$. (e) Taylor's formula; $S^{[i]}$ has coefficients in $\mathbb Z_p$. ∎

## 2. The odd-$p$ window identity (Result A) [proved]

**Lemma 2 (linearisation).** Let $n<N$, $m:=V_n(x)$, $D:=V_N(x)-m$, and assume $M_N(x)<m$. Let $C=x+p^m\mathbb Z_p$ with normalised Haar measure; write $x_0\in[0,p^m)$ for the integer with $x_0\equiv x\pmod{p^m}$ and $x'=x_0+p^mw$ ($w\in\mathbb Z_p$) for the points of $C$.
- (a) $v(x'+i)=v(x+i)$ for $i\le N$, so $V_n,V_N,M_N$ are constant on $C$. For every path $e$ of length $n$, aliveness at $n$ is constant on $C$, as are $S_e^{[i]}(x')\bmod p^m$ and $Q_f(x')\bmod p^m$.
- (b) If $e$ is alive at $n$, then with the unit $\omega:=\pi_n(x_0)/p^m$:
$$\tau_n(e,x')\equiv\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)\,w\pmod{p^{m-M_n}}.$$
- (c) (F2) holds at every $x'\in C$ with the same $D$.

*Proof.* (a) $v(x+i)\le M_N<m$ and $x'\equiv x\pmod{p^m}$. The rest is reduction of integer polynomials modulo $p^m$; aliveness at $n$ means $S_e(x')\equiv0\pmod{p^m}$.
(b) Put $h=p^mw$. By Lemma 1(e), $S_e(x')=S_e(x_0)+hS'_e(x_0)+h^2R$ with $R\in\mathbb Z_p$, and $\pi_n(x')=\pi_n(x_0)(1+E)$ with $1+E=\prod_{i\le n}(1+h/(x_0+i))$, $v(E)\ge m-M_n\ge1$. Since $\pi_n(x_0)=p^m\omega$,
$$\tau_n(e,x')=\big[\tau_n(e,x_0)-\omega^{-1}S'_e(x_0)w-\omega^{-1}p^mw^2R\big](1+E)^{-1},$$
the bracket lies in $\mathbb Z_p$, and $(1+E)^{-1}\equiv1\pmod{p^{m-M_n}}$. (c) is (F2) at $x'$, with $V_N(x')-V_n(x')=D$ by (a). ∎

*Frozen-state weights.* For $\lambda\ge0$ put
$$a_n^{(\lambda)}(t):=\mathbb P_{f\in\{0,1\}^{p\lambda}}\Big(\sum_{i<p\lambda}f_i\,\frac{\pi_{n+i}(x)}{\pi_n(x)}\equiv t\pmod{p^\lambda}\Big),\qquad \rho_n(e):=p^{\lambda_e}\,a_n^{(\lambda_e)}\big(\tau_n(e,x)\big).$$
It depends only on $n,\lambda$ and $x\bmod p^\lambda$, and $\sum_{t\bmod p^\lambda}a^{(\lambda)}_n(t)=1$. By Lemma 1(c) the terms $j\ge n+p\lambda$ of any $Q_f$ vanish modulo $p^\lambda$, so for $N-n\ge p\lambda$:
$$\#\{f\in\{0,1\}^{N-n}:Q_f(x)\equiv t\ (p^\lambda)\}=2^{N-n}a^{(\lambda)}_n(t).\tag{2.1}$$
For $\lambda=0$, $\rho\equiv1$. In general $\rho$ is not constant (the exact tests of §8 meet many non-constant weight vectors).

**Proposition A (one-window identity, slope $\le L$).** In the setting of Lemma 2 let $L\ge0$ and assume
$$\text{(W1) } N-n\ge pL,\qquad\text{(W2) } D+L\le m-M_n,\qquad\text{(W3) } L<m-M_N.$$
Let $e\in P^{1,L}_n(x)$ (a property of $C$ by (a) and $L<m$), $\lambda=\lambda_e(x)$. Then:
- (i) every child $(e,f)$ alive at $N$ at any $x'\in C$ has slope $\lambda$; every $e''\in P^{1,L}_N(x')$ has $e''|_n\in P^{1,L}_n(x)$;
- (ii) $s_e:=\tau_n(e,x')\bmod p^\lambda$ is constant on $C$;
- (iii) for every $s\in\mathbb Z/p^\lambda$:
$$\mathbb E_{x'\in C}\,\#\{f:(e,f)\text{ alive at }N,\ \tau_N((e,f),x')\equiv s\ (p^\lambda)\}=2^{N-n}p^{-D}\,a^{(\lambda)}_n(s_e).$$

*Proof.* By Lemma 1(c) and (W1), $D\ge\lfloor(N-n)/p\rfloor\ge L\ge\lambda$.
(i) $S'_{(e,f)}=S'_e+\sum_{n\le j<N}f_{j-n}\pi'_j$, and by Lemma 1(d) and (W3), $v(\pi'_j(x'))\ge V_j-M_j\ge m-M_N>L$. So a child of a slope-$\lambda$ parent has slope $\lambda$, and a parent of slope $>L$ has only children of slope $>L$. Also $\lambda_e(x')=\lambda_e(x)$ since $S'_e(x')\equiv S'_e(x)\pmod{p^m}$ and $L<m$. With (F2) this gives (i).
(ii) $v(S'_e(x_0))=\lambda$ (as $\lambda<m$) and $\lambda\le m-M_n$ by (W2); apply Lemma 2(b).
(iii) Write $\omega^{-1}S'_e(x_0)=p^\lambda\beta$ with $\beta$ a unit, and $\tau_0=\tau_n(e,x_0)$. By Lemma 2(b) and (W2), $t(w):=\tau_n(e,x_0+p^mw)\bmod p^{D+\lambda}$ equals $(\tau_0-p^\lambda\beta w)\bmod p^{D+\lambda}$. So $t$ depends only on $w\bmod p^D$, and $w\bmod p^D\mapsto t$ is a bijection onto the coset $\tau_0+p^\lambda\mathbb Z/p^{D+\lambda}$; under Haar measure on $C$, $w\bmod p^D$ is uniform. Since $D+\lambda\le m$, $q_f:=Q_f(x')\bmod p^{D+\lambda}$ is constant on $C$, and so is the unit $u:=\pi_N(x')/(p^D\pi_n(x'))\bmod p^\lambda$ (each factor $(x'+i)/p^{v(x+i)}$ is constant modulo $p^{m-M_N}$ and $m-M_N>\lambda$).
Fix $f$. By (F2), $(e,f)$ is alive at $x'$ iff $t(w)\equiv q_f\pmod{p^D}$.
- If $q_f\not\equiv\tau_0\pmod{p^\lambda}$, no $t$ in the coset satisfies this (as $D\ge\lambda$).
- If $q_f\equiv\tau_0\pmod{p^\lambda}$, the admissible $t$ are exactly $t=q_f+p^Dz$, $z\in\mathbb Z/p^\lambda$, all in the coset; for such $t$ the child has $\tau_N\equiv zu^{-1}\pmod{p^\lambda}$ by (F2), a bijection $z\leftrightarrow s$. So for each $s$ exactly one class $w\bmod p^D$ (probability $p^{-D}$) produces a child in state $s$.

Summing over $f$ and using (2.1) (note $N-n\ge p\lambda$ and $q_f\equiv Q_f(x)\pmod{p^\lambda}$): the expectation is $p^{-D}\#\{f:Q_f(x)\equiv s_e\ (p^\lambda)\}=2^{N-n}p^{-D}a_n^{(\lambda)}(s_e)$. ∎

**Corollary A′ (odd-$p$ martingale identity).** Under (W1)–(W3),
$$\mathbb E_{x'\in C}\Big[c_N(x')\sum_{e''\in P^{1,L}_N(x')}\rho_N(e'';x')\Big]=c_n(x)\sum_{e\in P^{1,L}_n(x)}\rho_n(e;x).$$
In particular, for $L=0$ (where (W1) is void and $\rho\equiv1$): $\mathbb E_{C}[c_NZ^0_N]=c_nZ^0_n$.

*Proof.* By (i) the left side is a sum over parents $e$ of their children. A child in state $s$ has weight $p^\lambda a^{(\lambda)}_N(s)$, constant on $C$ ($a_N^{(\lambda)}$ depends on $x'\bmod p^\lambda$ and $\lambda<m$), and $c_N$ is constant on $C$. By (iii) the expected weighted child mass of $e$ is $\sum_s2^{N-n}p^{-D}a_n(s_e)p^\lambda a_N(s)=2^{N-n}p^{-D}\rho_n(e)$, and $c_N2^{N-n}p^{-D}=c_n$. ∎

*Remarks.*
1. Along windows $n_0<n_1<\cdots$ whose hypotheses are checked on the digit filtration (as in note §10.1, or with deterministic times as in §5 below), $M_\ell:=c_{n_\ell}\sum_{P^{1,L}_{n_\ell}}\rho$ is a nonnegative martingale. The difference from $p=2$ is the normaliser: by Lemma 1(b), $c_n\le(p^{1/(p-1)}/2)^np^{M_n}$, and $p^{1/(p-1)}<2$ for $p\ge3$, so $c_n\to0$ exponentially on the good set where $M_n=O(\log n)$. The expected unnormalised weighted population therefore grows exponentially (supercriticality). This confirms note §10.1.3, which had only sketched the transfer.
2. The proof is the $p=2$ proof (note Prop 10.6, track R1b) with $2\to p$ in three places: truncation at $p\lambda$ terms (Lemma 1(c)), (W1) $N-n\ge pL$, and the normaliser.

## 3. The exact second moment for slope 0 (Result B) [proved]

Fix a window $W=[n,N)$ with (W2′) $D\le m-M_n$ and (W3′) $M_N<m$ (these are (W2), (W3) with $L=0$). Let $m_W(r):=\#\{f\in\{0,1\}^{N-n}:Q_f(x)\equiv r\pmod{p^D}\}$ for $r\in\mathbb Z/p^D$ (constant on $C$ since $D\le m$), $T:=2^{N-n}$, $\mu_W:=m_W/T$, and for $\xi\in\mathbb Z/p^D$
$$\hat m_W(\xi)=\sum_rm_W(r)\,e(-r\xi/p^D),\qquad\hat\mu_W=\hat m_W/T,\qquad\chi_W^2:=\sum_{\xi\ne0}|\hat\mu_W(\xi)|^2=p^D\sum_r\mu_W(r)^2-1.$$
For a slope-0 path $e$ alive at $n$ put
$$\tau_e^0:=\tau_n(e,x_0)\bmod p^D,\qquad\beta_e:=\omega^{-1}S'_e(x_0)\bmod p^D\ (\text{a unit}),\qquad\varphi_e:=\tau^0_e\beta_e^{-1}.$$

**Proposition B.** Let $P\subseteq P^0_n(x)$. For $x'=x_0+p^mw\in C$:
- (i) **(pointwise child counts)** $\#\{f:(e,f)\text{ alive at }N\text{ for }x'\}=m_W(\tau^0_e-\beta_ew\bmod p^D)=m_W\big(\beta_e(\varphi_e-w)\big)$ for every $e\in P$.
- (ii) **(second moment)** with $Y(x'):=\sum_{e\in P}\#\{\text{children of }e\}$:
$$\mathbb E_CY=|P|\,Tp^{-D},\qquad\mathbb E_C[Y^2]=p^{-2D}\sum_{\eta\in\mathbb Z/p^D}\Big|\sum_{e\in P}\hat m_W(\eta\beta_e^{-1})\,e(\eta\varphi_e/p^D)\Big|^2,$$
hence, with $M:=c_n|P|$,
$$\operatorname{Var}_C(c_NY)=c_n^2\sum_{\eta\ne0}\Big|\sum_{e\in P}\hat\mu_W(\eta\beta_e^{-1})\,e(\eta\varphi_e/p^D)\Big|^2\ \le\ M^2\chi_W^2.$$
- (iii) If all $\beta_e$ are equal to $\beta$, then $\operatorname{Var}_C(c_NY)=c_n^2\sum_{\xi\ne0}|\hat\mu_W(\xi)|^2\,\big|\sum_{e\in P}e(\xi\tau^0_e/p^D)\big|^2$.

*Proof.* (i) By Lemma 2(b) and (W2′), $\tau_n(e,x')\equiv\tau^0_e-\beta_ew\pmod{p^D}$. By (F2), $(e,f)$ is alive iff $Q_f(x')\equiv\tau_n(e,x')\pmod{p^D}$, and $Q_f(x')\equiv Q_f(x)\pmod{p^D}$.
(ii) $Y$ depends only on $w\bmod p^D$, which is uniform. Write $m_W(r)=p^{-D}\sum_\xi\hat m_W(\xi)e(r\xi/p^D)$; then
$$Y=p^{-D}\sum_{e}\sum_\xi\hat m_W(\xi)e(\beta_e\xi(\varphi_e-w)/p^D)=p^{-D}\sum_\eta e(-\eta w/p^D)\,A(\eta),\qquad A(\eta)=\sum_e\hat m_W(\eta\beta_e^{-1})e(\eta\varphi_e/p^D),$$
substituting $\eta=\beta_e\xi$ (a bijection of $\mathbb Z/p^D$ for each $e$). Parseval over $w\in\mathbb Z/p^D$ gives $\mathbb E_w|Y|^2=p^{-2D}\sum_\eta|A(\eta)|^2$. The term $\eta=0$ is $(|P|T)^2p^{-2D}=(\mathbb EY)^2$. Multiply by $c_N^2$ and use $c_NTp^{-D}=c_n$. The inequality is Cauchy–Schwarz, $|A(\eta)|^2\le|P|\sum_e|\hat m_W(\eta\beta_e^{-1})|^2$, and $\sum_{\eta\ne0}|\hat\mu_W(\eta\beta_e^{-1})|^2=\chi_W^2$ for each $e$.
(iii) Substitute $\xi=\eta\beta^{-1}$. ∎

**Remark B′ (Newton points).** $x_0+p^m\varphi_e$ is, modulo $p^{m+D}$, the Hensel root of $S_e$ in $C$: $S_e(x_0+p^m\varphi)=S_e(x_0)+p^m\varphi S_e'(x_0)+O(p^{2m})$ vanishes to the required order exactly when $\varphi\equiv-S_e(x_0)/(p^mS'_e(x_0))=\tau_e^0\beta_e^{-1}$. So (i) says that, inside the cylinder, the alive region of the children of $e$ is the translate by the root of $e$ of the scaled window sum set, and (ii) says that the conditional variance is the Fourier overlap between the window law and the empirical distribution of the population's roots at scale $p^{-(m+D)}$.

**What independence fails (task item (c)).** The survival criteria of Smith–Wilkinson (1969) and Athreya–Karlin (1971) for branching processes in random environments assume that, given the environment, distinct individuals reproduce independently. Here the environment of the window is $x\bmod p^m$ (it fixes the valuations, the window law $m_W$, the parents and their $(\tau^0_e,\beta_e)$). Given it, the offspring numbers $X_e=m_W(\beta_e(\varphi_e-w))$ of all parents are deterministic functions of **one** uniform variable $w\in\mathbb Z/p^D$, the fresh digits of $x$. They are never independent when $|P|\ge2$ and $\chi_W^2>0$. Proposition B(ii) measures the dependence exactly: the covariances sum to the off-diagonal part $c_n^2\sum_{\eta\ne0}\sum_{e\ne e'}(\cdots)$. In the numerics of §7 this part is negative on average (anti-correlation).

## 4. The Cauchy–Schwarz route is closed (Result N) [obstruction; proved]

**Proposition N.** Let $W=[n,N)$ be a window with $D\ge1$ and let $r$ be the number of its elements $\pi_j/\pi_n$ of valuation $0$ (so $1\le r\le p$). Let $s:=2^r\bmod p\in[1,p-1]$. Then
$$\chi_W^2\ \ge\ \frac{s(p-s)}{4^r}\ \ge\ \frac{p-1}{4^p}.$$
Moreover the inequality $\operatorname{Var}_C(c_NY)\le M^2\chi_W^2$ of Proposition B is an equality whenever all $\beta_e$ coincide and all $\tau^0_e$ coincide modulo $p^D$, in particular whenever $|P|=1$.

*Proof.* $\chi^2_W$ is at least its mod-$p$ shell, $\sum_{\xi\in p^{D-1}\mathbb Z/p^D,\ \xi\ne0}|\hat\mu_W(\xi)|^2=p\sum_{a\bmod p}\mu_{W,1}(a)^2-1$, where $\mu_{W,1}$ is the law of $Q_f\bmod p$. Elements of positive valuation vanish modulo $p$, so $\mu_{W,1}(a)=c_a/2^r$ where $c_a$ counts the subsets of the $r$ valuation-0 elements with sum $\equiv a$; $\sum_ac_a=2^r=qp+s$ with $s\ne0$ because $p$ is odd. For nonnegative integers with this sum, $\sum_ac_a^2\ge s(q+1)^2+(p-s)q^2$, and $p\,[s(q+1)^2+(p-s)q^2]-(qp+s)^2=s(p-s)$. Finally $s(p-s)\ge p-1$ and $4^r\le4^p$; $r\le p$ because a window with $D\ge1$ contains a multiple of $p$ among $x+n+1,\dots,x+n+p$. The equality case is immediate from Proposition B(ii). ∎

**Consequence.** For every infinite sequence of windows, $\prod_\ell(1+\chi^2_{W_\ell})=\infty$. So the recursion $\mathbb E[M_{\ell+1}^2\mid\mathcal G_\ell]\le(1+\chi_\ell^2)M_\ell^2$, which is the best bound that uses only $M_\ell$ and the window (by the equality case), never gives $\sup_\ell\mathbb E[M_\ell^2]<\infty$. This holds **whatever the windows and wherever the gates are**. The obstruction is the lowest shell ($\bmod\,p$), not the deep gates that the task description anticipated: deep gates only make $\chi_W^2$ larger. Lengthening windows does not help either, because the mod-$p$ law of a window is fixed by its first $\le p$ elements. A proof must therefore use cancellation in the population's roots (Proposition B(ii)), and Section 5 shows how to get it from the *previous* window.

## 5. Two-window bound and a conditional theorem (Result C) [proved; hypothesis FE unproved]

**Lemma C1 (fresh randomness; one-window Fourier bound).** Let $W=[n,N)$, $k\ge0$, and assume
$$D+k\le m-M_N\qquad\text{and}\qquad M_N<m.\tag{5.1}$$
Let $P\subseteq P^0_n(x)$. For $\xi\in\mathbb Z/p^k$ and $x'\in C$ put $\Psi_P(\xi;x'):=\sum_{e\in P}\sum_{f:(e,f)\text{ alive at }N}e\big(\xi\,\tau_N((e,f),x')/p^k\big)$. Let $u:=\pi_N(x)/(p^D\pi_n(x))\bmod p^k$, $\hat\mu_{W,D+k}(\zeta):=T^{-1}\sum_fe(-\zeta Q_f(x)/p^{D+k})$ for $\zeta\in\mathbb Z/p^{D+k}$, and the *fibre mass*
$$F_W(\xi):=\sum_{\zeta\in\mathbb Z/p^{D+k}:\ \zeta\equiv\xi u^{-1}\ (\mathrm{mod}\ p^k)}|\hat\mu_{W,D+k}(\zeta)|^2 .$$
Then (a) $\mathbb E_C\Psi_P(\xi)=0$ for $\xi\not\equiv0$, and (b) $\mathbb E_C|c_N\Psi_P(\xi)|^2\le(c_n|P|)^2F_W(\xi)$. Also $F_W(0)=1+\chi_W^2$.

*Proof.* Since $D+k\le m-M_n$, Lemma 2(b) gives $\tau_n(e,x')\equiv t_e(w):=\tau_e^0-\beta_ew\pmod{p^{D+k}}$, now with $\tau^0_e:=\tau_n(e,x_0)\bmod p^{D+k}$ and $\beta_e:=\omega^{-1}S_e'(x_0)\bmod p^{D+k}$. Since $D+k\le m$, $q_f:=Q_f(x')\bmod p^{D+k}=Q_f(x)\bmod p^{D+k}$. Since $k\le m-M_N$, $\pi_N(x')/(p^D\pi_n(x'))\equiv u\pmod{p^k}$. By (F2), $(e,f)$ is alive iff $t_e(w)\equiv q_f\pmod{p^D}$, and then $\tau_N((e,f),x')\equiv u^{-1}(t_e(w)-q_f)/p^D\pmod{p^k}$. Define $g(r):=\mathbf 1[r\equiv0\ (p^D)]\,e(\xi u^{-1}r/p^{D+k})$ on $\mathbb Z/p^{D+k}$ and $m(s):=\#\{f:q_f=s\}$. Then $\Psi_P(\xi;x')=\sum_{e\in P}G(t_e(w))$ with $G=g*m$, and
$$\hat g(\zeta)=\sum_{r\equiv0\,(p^D)}e\big((\xi u^{-1}-\zeta)r/p^{D+k}\big)=p^k\,\mathbf 1[\zeta\equiv\xi u^{-1}\ (p^k)].$$
For each $e$, $w\bmod p^{D+k}\mapsto t_e(w)$ is a bijection ($\beta_e$ a unit), and $w\bmod p^{D+k}$ is uniform on $C$. Hence $\mathbb E_wG(t_e(w))=p^{-(D+k)}\hat g(0)\hat m(0)=0$ when $\xi\not\equiv0$, giving (a), and by Cauchy–Schwarz over $e$ and Parseval,
$$\mathbb E_w|\Psi_P|^2\le|P|\sum_e\mathbb E_w|G(t_e(w))|^2=|P|^2p^{-2(D+k)}\sum_\zeta|\hat g(\zeta)|^2|\hat m(\zeta)|^2=|P|^2\,(Tp^{-D})^2F_W(\xi).$$
Multiply by $c_N^2$ and use $c_NTp^{-D}=c_n$. For $\xi=0$ the fibre is $\zeta=p^k\zeta'$, $\zeta'\in\mathbb Z/p^D$, which gives $1+\chi_W^2$. ∎

**Proposition C2 (two-window inequality).** Let $W=[n,N)$, $W'=[N,N')$ with jumps $D,D'$, and assume
$$D+D'\le m-M_{N'}\qquad\text{and}\qquad M_{N'}<m.\tag{5.2}$$
Let $Z^0_N(x'),Z^0_{N'}(x')$ be the slope-0 populations, $\hat\mu_{W'}$ the law of the window $W'$ modulo $p^{D'}$ (constant on $C$), and
$$\varepsilon(W,W'):=\sum_{0\ne\xi\in\mathbb Z/p^{D'}}|\hat\mu_{W'}(\xi)|^2F_W(\xi)\qquad(k=D'\text{ in }F_W).$$
Then
$$\mathbb E_C\big[(c_{N'}Z^0_{N'})^2\big]-\mathbb E_C\big[(c_NZ^0_N)^2\big]\ \le\ \varepsilon(W,W')\,(c_nZ^0_n)^2 .$$
Moreover $\varepsilon(W,W')=p^{D+D'}\mathrm{Coll}_{D+D'}-p^D\mathrm{Coll}_D$, where $\mathrm{Coll}_j=\sum_r\nu_j(r)^2$ and $\nu_j$ is the law modulo $p^j$ of a uniformly random subset sum of the **composite** window $\{\pi_j(x)/\pi_n(x):n\le j<N'\}$. Equivalently, $\varepsilon$ is the $L^2$ Fourier mass of the composite law at the frequencies of order in $(p^D,p^{D+D'}]$.

*Proof.*
*Step 0 (hypotheses).* (5.2) implies (W2′), (W3′) for $W$ at $x$ and for $W'$ at every $x'\in C$ (as $V_N(x')=m+D$ and $M_{N}\le M_{N'}$), and (5.1) for $W$ with $k=D'$. By Proposition A(i) ($L=0$), $P^0_N(x')$ consists of the alive children of $P^0_n(x)$, and $P^0_{N'}(x')$ of the alive children of $P^0_N(x')$.
*Step 1.* Condition on the cylinder $C'=x'+p^{m+D}\mathbb Z_p$ and apply Proposition B to $W'$ with parent set $P^0_N(x')$:
$$\mathbb E_{C'}[(c_{N'}Z^0_{N'})^2]=(c_NZ^0_N)^2+\operatorname{Var}_{C'}(c_{N'}Z^0_{N'}).$$
Proposition B may use any reference point of $C'$ in place of $x'_0$: moving it by $p^{m+D}s$ changes every $\varphi_{e'}$ by $-s$ and leaves $|A(\eta)|$ unchanged. We use $x'$ itself.
*Step 2 (classes).* Split $P^0_N(x')$ into classes $b\in(\mathbb Z/p^{D'})^\times$ by $\beta_{e'}\bmod p^{D'}$. Then $c_{N'}(Z^0_{N'}-\mathbb E_{C'}Z^0_{N'})=\sum_bX_b(w')$ with $X_b=c_{N'}\sum_{e'\in b}\big(m_{W'}(\tau_N(e',x')-bw')-T'p^{-D'}\big)$. Within a class the $\beta$ agree modulo $p^{D'}$, so the computation of Proposition B(iii) gives
$$\mathbb E_{w'}|X_b|^2=c_N^2\sum_{\xi\ne0}|\hat\mu_{W'}(\xi)|^2\,|\Psi_b(\xi;x')|^2,\qquad \Psi_b(\xi;x'):=\sum_{e'\in b}e(\xi\tau_N(e',x')/p^{D'}).$$
By Minkowski's inequality in $L^2$ of $(w,w')$, $\mathbb E_C\operatorname{Var}_{C'}=\mathbb E\big|\sum_bX_b\big|^2\le\big(\sum_b(\mathbb E|X_b|^2)^{1/2}\big)^2$.
*Step 3 (inheritance of classes).* For a child $e'=(e,f)$: $S'_{e'}(x')\equiv S'_e(x_0)\pmod{p^{D'}}$, because $v(\pi'_j(x'))\ge m-M_N\ge D'$ for $j\ge n$, and $D'\le m$. Also $\pi_N(x')/p^{m+D}\equiv\omega u\pmod{p^{D'}}$, because $D'\le m-M_N$. Hence $\beta_{e'}\equiv\beta_eu^{-1}\pmod{p^{D'}}$, and the class-$b$ members of $P^0_N(x')$ are exactly the alive children of $P_{bu}:=\{e\in P^0_n(x):\beta_e\equiv bu\ (p^{D'})\}$. So $\Psi_b(\xi;x')=\Psi_{P_{bu}}(\xi;x')$, and Lemma C1(b) with $k=D'$ gives $\mathbb E_C[c_N^2|\Psi_b(\xi)|^2]\le(c_n|P_{bu}|)^2F_W(\xi)$. Since $\hat\mu_{W'}$ is constant on $C$, $\mathbb E|X_b|^2\le\varepsilon\,(c_n|P_{bu}|)^2$.
*Step 4.* $\mathbb E_C\operatorname{Var}_{C'}\le\big(\sum_b\varepsilon^{1/2}c_n|P_{bu}|\big)^2=\varepsilon\,(c_nZ^0_n)^2$.
*Identification of $\varepsilon$.* The composite sums are $Q_f+(\pi_N/\pi_n)Q'_{f'}\equiv Q_f+p^DuQ'_{f'}\pmod{p^{D+D'}}$, so $\hat\nu_{D+D'}(\zeta)=\hat\mu_{W,D+D'}(\zeta)\,\hat\mu_{W'}(\zeta u)$. As $\zeta$ runs over residues mod $p^{D+D'}$ with $\zeta u\equiv\xi\not\equiv0\pmod{p^{D'}}$, i.e. over $\zeta\not\equiv0\pmod{p^{D'}}$, this sums to $\varepsilon$. By Parseval, $\sum_{\text{all }\zeta}|\hat\nu|^2=p^{D+D'}\mathrm{Coll}_{D+D'}$, and $\sum_{\zeta\equiv0\,(p^{D'})}|\hat\nu|^2=p^D\mathrm{Coll}_D$. ∎

So, unlike Proposition B, the loss from Cauchy–Schwarz is taken **only at frequencies above $p^D$ of the earlier window**, where a long window is equidistributed. The mod-$p$ shell of Proposition N enters only through the exact conditional mean $0$ of Lemma C1(a).

**Setting for the theorem.** Fix deterministic times $2p\le n_0<n_1<\cdots$ (e.g. $n_{\ell+1}=\lceil rn_\ell\rceil$ with $1<r<\sqrt2$), write $m_\ell=V_{n_\ell}(x)$, $D_\ell=m_{\ell+1}-m_\ell$, $W_\ell=[n_\ell,n_{\ell+1})$, $M_\ell:=c_{n_\ell}Z^0_{n_\ell}$, $\chi^2_\ell=\chi^2_{W_\ell}$, and $\varepsilon_\ell(x):=\varepsilon(W_{\ell-1},W_\ell)$. Let $\mathcal G_\ell$ be generated by the cylinders $x+p^{m_\ell(x)}\mathbb Z_p$. This is a partition, because $n_\ell\ge2p$ gives $M_{n_\ell}<m_\ell$, so $m_\ell$ is constant on its own cylinder. For $\ell>j$ let
$$B_\ell:=\{D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}},\ M_{n_{\ell+1}}<m_{\ell-1}\}\cap\{\varepsilon_\ell(x)\le\bar\varepsilon_\ell\},\qquad\tau_j:=\min\{\ell>j:\ x\notin B_\ell\}.$$
$B_\ell$ is $\mathcal G_{\ell-1}$-measurable: on $\{M_{n_{\ell+1}}<m_{\ell-1}\}$, which is determined by $x\bmod p^{m_{\ell-1}}$, all valuations up to $n_{\ell+1}$ are determined, and $\varepsilon_\ell$ depends on $x\bmod p^{D_{\ell-1}+D_\ell}$. An atom $A$ of $\mathcal G_j$ is *admissible* if $D_j\le m_j-M_{n_{j+1}}$ and $M_{n_{j+1}}<m_j$ on $A$, and $Z^0_{n_j}\ne0$ on $A$.

**Theorem C3 (conditional positive measure).** Let $(\bar\varepsilon_\ell)_{\ell>j}$ be nonnegative with $\Pi:=\prod_{\ell>j}(1+\bar\varepsilon_\ell)<\infty$, let $A$ be an admissible atom of $\mathcal G_j$, and put $\Pi_A:=(1+\chi_j^2(A))\,\Pi$. If
$$\delta_A:=\mu_A(\tau_j<\infty)<1/\Pi_A\qquad\textbf{(hypothesis FE}(A,\bar\varepsilon)\textbf{)},$$
then
$$\frac{\mu(K_p\cap A)}{\mu(A)}\ \ge\ \frac{\big(1-\sqrt{\Pi_A\,\delta_A}\big)^2}{\Pi_A}\ >\ 0.$$
In particular $\mu(K_p)>0$.

*Proof.* Work in the probability space $(A,\mu_A)$. Let $\tilde M_\ell:=M_{\min(\ell,\tau_j)}$ for $\ell\ge j$.
- *Martingale.* For $\ell\ge j$, on $\{\tau_j>\ell\}$ the window $W_\ell$ satisfies (W2′) and (W3′): for $\ell=j$ by admissibility, and for $\ell>j$ by $B_\ell$, since $D_\ell\le m_{\ell-1}-M_{n_{\ell+1}}-D_{\ell-1}\le m_\ell-M_{n_\ell}$ and $M_{n_{\ell+1}}<m_{\ell-1}\le m_\ell$. Since $\{\tau_j>\ell\}\in\mathcal G_{\ell-1}\subseteq\mathcal G_\ell$, Corollary A′ gives $\mathbb E[\tilde M_{\ell+1}\mid\mathcal G_\ell]=\tilde M_\ell$.
- *Second moments.* By Proposition B, $\mathbb E[\tilde M_{j+1}^2\mid\mathcal G_j]\le M_j^2(1+\chi_j^2)$. For $\ell>j$, on $\{\tau_j>\ell\}$ hypothesis (5.2) holds for $(W_{\ell-1},W_\ell)$, so Proposition C2 on each atom of $\mathcal G_{\ell-1}$ gives
$$\mathbb E[\tilde M_{\ell+1}^2-\tilde M_\ell^2\mid\mathcal G_{\ell-1}]=\mathbf 1_{\{\tau_j>\ell\}}\mathbb E[M_{\ell+1}^2-M_\ell^2\mid\mathcal G_{\ell-1}]\le\bar\varepsilon_\ell\tilde M_{\ell-1}^2 .$$
With $a_\ell:=\mathbb E_A\tilde M_\ell^2$, nondecreasing because $\tilde M$ is a martingale, $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}\le(1+\bar\varepsilon_\ell)a_\ell$. Hence $\sup_\ell a_\ell\le M_j(A)^2\Pi_A$, where $M_j(A)>0$ is the constant value of $M_j$ on $A$.
- *Limit.* $\tilde M$ is an $L^2$-bounded martingale, so $\tilde M_\ell\to\tilde M_\infty$ a.s. and in $L^2$, with $\mathbb E_A\tilde M_\infty=M_j(A)$ and $\mathbb E_A\tilde M_\infty^2\le M_j(A)^2\Pi_A$.
- *Survival.* Let $Y:=\mathbf 1_{\{\tau_j=\infty\}}\tilde M_\infty$. If $Y(x)>0$ then $M_\ell(x)>0$ for all $\ell\ge j$. Indeed, if $Z^0_{n_\ell}=0$ for some $\ell$, then by Proposition A(i) every later slope-0 population is empty and $M_\infty=0$. So by (F1) $x\in K_p$, and $\{Y>0\}\subseteq K_p\cap A$.
- *Paley–Zygmund.* $\mathbb E_AY\ge M_j(A)-\mathbb E_A[\tilde M_\infty\mathbf 1_{\{\tau_j<\infty\}}]\ge M_j(A)\big(1-\sqrt{\Pi_A\delta_A}\big)$ by Cauchy–Schwarz, and $\mathbb E_AY^2\le M_j(A)^2\Pi_A$. So $\mu_A(Y>0)\ge(\mathbb E_AY)^2/\mathbb E_AY^2$, and $M_j(A)$ cancels. ∎

**Lemma C4 (deep gates are rare on a cylinder; the linear-regime part of $\tau_j$).** Put $\gamma_\ell:=2v(n_{\ell-1}!)-n_{\ell+1}/(p-1)$ and $s_\ell:=\lfloor\gamma_\ell/2\rfloor+1$. If $M_{n_{\ell+1}}(x)<s_\ell$ and $n_{\ell+1}-n_{\ell-1}\ge p$, then the first event in $B_\ell$ holds. For an atom $A=x_A+p^{m}\mathbb Z_p$ of $\mathcal G_j$ ($m=m_j$), let $I_A=\{i\ge1:\ x_A+i\equiv0\ (p^m)\}$ and $i_1=\min I_A$. Suppose that for every $\ell>j$, every $i\le n_{\ell+1}$ with $i\notin I_A$ has $v(x_A+i)<s_\ell$ (a condition on $A$ alone). Then
$$\mu_A\big(\exists\ell>j:\ M_{n_{\ell+1}}\ge s_\ell\big)\le\sum_{\ell>j:\ n_{\ell+1}\ge i_1}\Big(1+\frac{n_{\ell+1}}{p^m}\Big)\min\big(1,p^{\,m-s_\ell}\big).$$
*Proof.* By Lemma 1(b), $V_{n_{\ell+1}}+M_{n_{\ell+1}}\le n_{\ell+1}/(p-1)+2M_{n_{\ell+1}}$. If $M_{n_{\ell+1}}\le s_\ell-1\le\gamma_\ell/2$, this is $\le n_{\ell+1}/(p-1)+\gamma_\ell=2v(n_{\ell-1}!)\le2V_{n_{\ell-1}}$ (Lemma 1(a)), which is $D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}}$. Since $D_{\ell-1}+D_\ell\ge1$ when $n_{\ell+1}-n_{\ell-1}\ge p$, also $M_{n_{\ell+1}}<m_{\ell-1}$. For $i\notin I_A$, $v(x+i)=v(x_A+i)$ on $A$. For $i\in I_A$, $\mu_A(v(x+i)\ge s)=p^{-(s-m)}$ for $s\ge m$. There are at most $1+(n-i_1)/p^m$ elements of $I_A$ up to $n$, and none if $n<i_1$. A union bound finishes the proof. ∎

For $n_{\ell+1}=\lceil rn_\ell\rceil$ with $1<r<\sqrt2$, $\gamma_\ell\approx(2-r^2)n_{\ell-1}/(p-1)$ grows geometrically while $i_1\ge n_j$ is typically of size $p^{m}$, the bound of Lemma C4 is tiny for most atoms. **So the only genuinely open part of FE is the fine-scale equidistribution $\varepsilon_\ell(x)\le\bar\varepsilon_\ell$.**

*Note on the deviation from the suggested plan.* The task suggested a hypothesis on the windows just before level-$d$ gates, which are position-independent modulo $p^d$. Proposition N shows that no per-window hypothesis can close a Cauchy–Schwarz recursion, because the obstruction sits in the lowest shell of every window. The quantity that has to be small is the cross-scale (fibre) mass $\varepsilon_\ell$ of two consecutive windows. Deep gates still matter: they are where $\varepsilon_\ell$ is large (§7.3). But $\varepsilon_\ell$ also depends on the high digits of $x$ above the gate level, so it is not a fixed finite computation for each $d$.

**Lemma C5 (the fine-scale mass through the signed carry process) [proved].** For $y\in\mathbb Z_p$ and $t\ge1$ (with $y+i\ne0$ for $i\le t$) put
$$\Lambda_t(y):=p^{V_t(y)}\ \mathbb P_\delta\Big(1+\sum_{1\le c<t}\delta_c\,\pi_c(y)\equiv0\pmod{p^{V_t(y)}}\Big),$$
where the $\delta_c$ are i.i.d. with $\mathbb P(\delta_c=0)=\tfrac12$ and $\mathbb P(\delta_c=\pm1)=\tfrac14$ (the law of the difference of two independent fair bits). Then for a composite window $[n,N')=[n,N)\cup[N,N')$,
$$\varepsilon(W,W')=\frac{c_{N'}-c_N}{c_n}+\sum_{n\le j<N}\frac{c_j}{2c_n}\big[\Lambda_{N'-j}(x+j)-\Lambda_{N-j}(x+j)\big]+\sum_{N\le j<N'}\frac{c_j}{2c_n}\Lambda_{N'-j}(x+j).$$
*Proof.* $\mathrm{Coll}_K$ is the probability that $\sum_j\delta_jy_j\equiv0\pmod{p^K}$, where $y_j=\pi_j(x)/\pi_n(x)$ and $\delta=f-f'$ has i.i.d. coordinates with the law above. Split according to the first index $j$ with $\delta_j\ne0$; this has probability $2^{-(j-n)}\cdot\frac12$, and with probability $2^{-(N'-n)}$ there is none. Given $j$ and the sign $\sigma=\delta_j$, $\sum\delta_iy_i=\sigma y_j\,T$ with $T=1+\sum_{c\ge1}\sigma\delta_{j+c}\pi_c(x+j)$, and $\sigma\delta$ has the same law as $\delta$. Since $v(y_j)=V_j-V_n$ and $V_t(x+j)=V_{j+t}(x)-V_j(x)$, the event "$\equiv0\pmod{p^K}$" is the event "$v(T)\ge V_{N'-j}(x+j)$", which has probability $p^{-V_{N'-j}(x+j)}\Lambda_{N'-j}(x+j)$. For $\mathrm{Coll}_D$: if $j\ge N$ the event holds automatically ($v(y_j)\ge D$); if $j<N$ it is the event $v(T)\ge V_{N-j}(x+j)$, and the terms $c\ge N-j$ of $T$ are irrelevant because they have valuation $\ge V_{N-j}(x+j)$. Multiply by $p^K$ and $p^D$ and use $2^{-(j-n)}p^{V_j-V_n}=c_j/c_n$. ∎

$\Lambda_t(y)$ is the density, relative to Haar measure, at $0$ and at scale $p^{-V_t(y)}$, of the law of the signed sum $\sum_{c\ge0}\delta_c\pi_c(y)$ with $\delta_0=1$. So FE says that these densities are already stable between the resolutions $p^{-V_{N-j}}$ and $p^{-V_{N'-j}}$, with weights $c_j/c_n$ that decay exponentially in $j-n$. Lemma C5 is checked in exact rational arithmetic by `lemma_c5_check.py` (§8).

**Remark C6 (what the signed process gives, and where it stops) [sketch / heuristic].** The signed process satisfies Proposition A verbatim. The proof of A uses only the per-$f$ counting in (iii), so the uniform measure on $\{0,1\}^{N-n}$ may be replaced by any product measure on digit strings, for instance by the law of $\delta$; the frozen weights are then defined with the same measure. Hence on every slope class $\lambda\le L$ that the windows can see, $p^{V_t}\sum\mathbb P(\delta)\rho$ is a martingale, and the expected increments $\mathbb E[\Lambda^{\le L}_{t'}-\Lambda^{\le L}_t\mid\mathcal F_c]$ vanish whenever $[c,t]$ is a valid window and $[c,t']$ is reached by a chain of valid windows.

So if one could show (S) that the normalised mass of signed paths whose slope is comparable to $V_t$ is small, then $\mathbb E_A[\varepsilon_\ell]$ would reduce to boundary terms of size $O(c_{n_\ell}/c_{n_{\ell-1}})$ plus failure events. Markov's inequality would then give FE, and Theorem C3 would give $\mu(K_p)>0$. Such slopes correspond to near-multiple roots of the signed polynomials, the analogue of the multiplicity $k\ge2$ case of note Proposition 10.7. **(S) is not proved.** A small heuristic experiment (`signed_slopes.py`, log `signed_slopes.log`; $76$–$80$ Haar points $y$, $t\le16$, float64) shows heavy tails. At $p=3$, slopes $\ge4$ carry $16\%$, $70\%$ and $71\%$ of the sample mean of $\Lambda_t$ at $t=8,12,16$. At $p=5$ ($t=16$), slopes $\ge3$ carry $7\%$. So (S) is not a formality, at least at $p=3$. This is the recommended next step (§10).

**Proposition N3 (the plain expectation is infinite) [proved].** For every odd $p$ and every $t\ge3$, $\int_{\mathbb Z_p}\Lambda_t\,d\mu=+\infty$.

*Proof.* Let $y$ satisfy $v(y+2)=s$. The signed path $\delta=(1,1,1,0,\dots,0)$ has $S_\delta(y)=1+(y+1)+(y+1)(y+2)=(y+2)^2$ (note Proposition 3.4), so $v(S_\delta(y))=2s$, and $\mathbb P(\delta)=\frac14\cdot\frac14\cdot2^{-(t-3)}=2^{-(t+1)}$. Now $V_t(y)=s+V'_t(y)$ with $V'_t(y)=\sum_{i\le t,\,i\ne2}v(y+i)$. Once $p^s>t$, every $i\le t$ with $i\ne2$ has $v(y+i)=v(i-2)$, so $V'_t(y)=v((t-2)!)$. Hence for $s\ge s_0(t,p)$ the path is alive at $t$, and $\Lambda_t(y)\ge p^{V_t(y)}2^{-(t+1)}=p^{s+v((t-2)!)}2^{-(t+1)}$. Since $\mu\{v(y+2)=s\}=(1-p^{-1})p^{-s}$,
$$\int\Lambda_t\,d\mu\ \ge\ \sum_{s\ge s_0}(1-p^{-1})\,p^{v((t-2)!)}2^{-(t+1)}=\infty.\qquad∎$$

So the density of the signed law at $0$ has infinite mean, because of the double root of $S_{\{1,2\}}=(x+2)^2$ at $-2$. More generally, near any point $x+j$ that sits close to a negative integer, i.e. near a deep gate, $\Lambda$ is inflated by roughly $p^{\text{depth}}$.

Numerically $\varepsilon_\ell$ behaves the same way. `eps_gate_depth.py` (log `eps_gate_depth.log`, $p=3$, $8$ samples per point) forces $v(x+n+d)=s$ for a gate at distance $d\in\{1,4\}$ from the start of the composite windows $[16,26)$, $[24,40)$ and $[32,52)$. For $s\ge4$ it finds $\varepsilon\approx\kappa\,3^{s}$, almost independently of the other digits: the median equals the mean. The factor $\kappa$ is between about $0.006$ and $0.06$, and it does **not** decrease clearly with the window length in this range. For example, at $d=4$, $\kappa\approx0.008,\ 0.030,\ 0.027$.

Two consequences:
- **$\mathbb E_A[\varepsilon_\ell]$ is very probably infinite.** A gate of depth $s$ at a fixed distance from the start has probability $\asymp p^{-s}$ and contributes $\asymp\kappa p^{s}$. So Remark C6 cannot be completed by Markov's inequality on $\mathbb E_A[\varepsilon_\ell]$ itself; a truncation at deep gates near window starts is needed first.
- **The probability form of FE needs $\kappa=\kappa_\ell\to0$.** The same estimate gives $\mu(\varepsilon_\ell>\bar\varepsilon_\ell)\gtrsim\kappa_\ell/\bar\varepsilon_\ell$. FE with a summable $(\bar\varepsilon_\ell)$ is therefore possible only if $\sum_\ell\kappa_\ell/\bar\varepsilon_\ell<\infty$, which requires $\kappa_\ell$ to decay (for instance geometrically in $n_\ell$, with $\bar\varepsilon_\ell=\kappa_\ell^{1/2}$).

A heuristic decomposition supports $\kappa_\ell\approx p^{v_{\rm pre}}2^{-d}\,\varepsilon^{\rm post}_\ell$: the few elements before the gate times the fine-scale mass of the window after it. This suggests that $\kappa_\ell$ decays exactly when typical $\varepsilon$ decays. That is the case numerically at $p=7$ and $p=5$ (§7.3), but **not visibly at $p=3$** in the accessible range. So at $p=3$ the hypothesis FE may well be false for every summable $\bar\varepsilon$, and Theorem C3 is most plausibly applicable at larger $p$.

## 6. Relation to the known obstructions

The rules ask how a measure argument sits relative to the structural obstructions of note.md. Theorem C3 is only conditional, but the comparison explains what kind of input FE is.
- **Theorem 3.6 (no finite-depth certificate; $K_p$ nowhere dense).** Nothing here is a residue-class criterion. Theorem C3 is a statement about the Haar measure of a closed nowhere dense set (a "fat Cantor set" is not excluded by Theorem 3.6), and FE is probabilistic in the digits of $x$. Even an unconditional $\mu(K_p)>0$ would not put a natural number in $K_p$ and would say nothing about Q3.
- **Theorem 3.8 ($p=2$).** Covering is not used. At $p=2$ the construction is empty: alive paths of even $x$ have slope $\ge1$ (note Remark 10.8.3), and the normaliser $c_n=2^{-W_n}$ does not decay. Theorem 10.1 shows that there the martingale dies.
- **Theorem 3.10 (barrier lemma).** FE **is of barrier type.** $\varepsilon_\ell$ is the $L^2$ mass of the composite window law modulo $p^{K_\ell}$ with $K_\ell=D_{\ell-1}+D_\ell\to\infty$. Replace the unit parts of $\pi_j(x)/\pi_n(x)$ by their truncations to $c$ digits, as in the proof of Theorem 3.10. Within each block of equal valuation the truncated elements are then integers in $[1,p^c)$, so the subset sums occupy only a small fraction of the residues at levels about $c$ above each valuation. The high-band mass $\varepsilon_\ell$ then cannot be small once $K_\ell$ exceeds the valuations by more than $c$ plus a constant. (This is the mechanism of Theorem 3.10, stated here heuristically and not as a proved claim.) So a proof of FE must use unboundedly many digits of the unit parts. The difference from the setting of Theorem 3.10: for Haar-random $x$, those digits are (polynomial images of) **digits of $x$ itself**, not fixed constants such as Morita's $\Gamma_p(n)$. FE is therefore an equidistribution question about random polynomial images, where averaging over $x$ is available. Lemma C5 turns the averaged form into a first-moment question, and Remark C6 says where that stops.
- **Corollary 10.13 (fullness cannot be propagated through a gate block).** No fullness or covering information is used anywhere.
- **Corollary 10.20 (sup-type Fourier transfer bounds give no decay).** Proposition N is the analogue in the present setting: any per-window bound in terms of $\sup$ or Cauchy–Schwarz over the population cannot close. The way around it (Proposition C2) is to apply Cauchy–Schwarz only after transporting the low frequencies of window $\ell$ to the high frequencies of window $\ell-1$, by the exact rank-one structure of Lemma C1. This is the "decorrelation" that Corollary 10.20 identified as necessary, realised exactly, one window deep.

## 7. Numerical evidence [heuristic; Monte Carlo and exact small cases]

### 7.1 The slope-0 martingale looks $L^2$-bounded

`oddp_mc` follows every alive path (carry recursion, exact residues) for Haar-random $x$ (`K` random digits). Its counts were cross-checked against an independent recount (`mc_crosscheck.py`, direct evaluation of $S_e,S'_e$): $12/12$, $10/10$, $10/10$ and $5/5$ samples agree at $p=3,5,7,11$ (§8). The table gives the last row before any censoring. $M^0_n=c_nZ^0_n$.

| $p$ | samples | $n$ | $\mathbb P(Z_n>0)$ | $\mathbb P(Z^0_n>0)$ | $\mathbb E M^0_n$ | $\mathbb E (M^0_n)^2$ | $\mathbb E(M^0)^2/(\mathbb EM^0)^2$ | Paley–Zygmund bound | known $\mu(K_p)$ (note §5) |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 20000 | 60 | 0.3605 | 0.1067 | 0.0712 | 0.1046 | 20.6 | 0.049 | ≈0.36 |
| 5 | 4000 | 40 | 0.5323 | 0.3110 | 0.0981 | 0.0523 | 5.44 | 0.184 | ≈0.5216 |
| 7 | 1500 | 32 | 0.6553 | 0.5000 | 0.1927 | 0.0806 | 2.17 | 0.46 | ≈0.6239 |
| 11 | 400 | 28 | 0.7175 | 0.6375 | 0.3159 | 0.1843 | 1.85 | 0.54 | ≈0.6998 |

- At $p=3$, $\mathbb EM^0_n$ is $0.0741,0.0718,0.0719,0.0717,0.0710,0.0712$ for $n=8,12,16,20,28,60$: constant within Monte Carlo error, as Corollary A′ predicts once the window conditions hold.
- $\mathbb E(M^0_n)^2$ is $0.074,0.089,0.100,0.106,0.103,0.105$: it stabilises after $n\approx20$.
- The same pattern holds at $p=5,7,11$ (log `mc_population.log`).
- The slope-0 sub-population carries a fraction of $K_p$ that grows with $p$: $\mathbb P(Z^0>0)/\mathbb P(Z>0)\approx0.30,0.58,0.76,0.89$.
- The Paley–Zygmund ratio improves with $p$, towards the value $\approx1$ of an independent branching process.
- The values $\mathbb P(Z_n>0)$ at $p=7,11$ are not converged, because $V_n$ is only $5$–$6$ levels at the $n$ reachable. They are upper estimates for $\mu(K_p)$.

### 7.2 The population's roots are spread: the true variance is diagonal-sized

`spectral_mc.py` computes, for the slope-0 population and one window, the exact conditional variance via Proposition B(i). It compares this with the diagonal (independent-offspring) value $Z\chi_W^2$ and with the Cauchy–Schwarz bound $Z^2\chi_W^2$ (in units $(Tp^{-D})^2$). At $p=3$, $1500$ samples per row, window $[n,n+n/4)$:

| $n$ | median $Z^0$ | median var/diag | mean var/diag | median var/CS | $\mathbb E[c_n^2\mathrm{Var}]$ | $\mathbb E[c_n^2Z\chi^2]$ | $\mathbb E[c_n^2Z^2\chi^2]$ |
|---|---|---|---|---|---|---|---|
| 16 | 18 | 0.39 | 0.45 | 1.6e-2 | 5.2e-3 | 9.7e-3 | 0.24 |
| 24 | 46 | 0.48 | 0.69 | 9.9e-3 | 8.5e-4 | 1.3e-3 | 0.086 |
| 32 | 456 | 0.46 | 0.59 | 9.7e-4 | 1.3e-3 | 1.4e-3 | 1.11 |
| 40 | 1093 | 0.63 | 0.74 | 5.4e-4 | 4.5e-4 | 6.2e-4 | 0.94 |
| 48 | 1064 | 0.65 | 0.79 | 4.1e-4 | 5.8e-5 | 7.6e-5 | 0.14 |

So the covariances between parents are on average **negative**, and the Cauchy–Schwarz bound overestimates the variance by factors of about $60$ to $2400$ (medians), and $50$ to $2400$ in expectation. The per-window increments of $\mathbb E[M^2]$ decay. This is what the exact identity of Proposition B predicts if the Newton points (roots) of the population are spread at least as well as independent points.

### 7.3 The hypothesis FE: size of the fine-scale masses $\varepsilon_\ell$

`epsilon_scan.py` computes $\varepsilon_\ell(x)$ for Haar-random $x$ and deterministic times $n_{\ell+1}=\lceil1.25\,n_\ell\rceil$, together with the fraction of samples meeting the linear-regime condition, and $\varepsilon$ grouped by the deepest gate $d$ in the composite window. There were $200$ samples per prime. The precision cap ($K\le13,8,6$ at $p=3,5,7$) silently drops samples whose composite window has a large jump, i.e. a deep gate. So the later rows are **biased towards shallow gates** (their sample counts are given), and are optimistic. Medians of $\varepsilon_\ell$ over the samples meeting the linear condition:

| $p$ | windows $[n_{\ell-1},n_{\ell+1})$ | median $\varepsilon_\ell$ | 99% quantile | by deepest gate $d$ (median) |
|---|---|---|---|---|
| 3 | [20,32), [25,40), [32,50), [40,63) | 0.14, 0.14, 0.19, 0.24 | 3.3, 4.0, 5.7, 4.4 | $d=2$: 0.11→0.03; $d=3$: 0.90→0.23; $d=4$: 3.3→0.83 |
| 5 | [16,25) … [50,79), [63,99) (66 samples) | 0.035, 0.027, 0.025, 0.046, 0.050, 0.013, 0.0024 | 0.95 … 0.28, 0.051 | $d=1$: 0.035→0.0009; $d=2$: 0.95→0.010; $d=3$: 0.28→0.088 |
| 7 | [21,34) … [54,85), [68,107) (95 samples) | 0.014, 0.0048, 0.0021, 0.0017, 0.00053, 0.00017 | 0.050 … 0.034, 0.0040 | $d=1$: 0.014→0.00006; $d=2$: 0.0093→0.00035 |

Reading:
- At fixed depth of the deepest gate, $\varepsilon_\ell$ decreases with the window length at all three primes.
- For a given window, $\varepsilon_\ell$ grows by roughly a factor $p$ per extra level of the deepest gate. The gate-depth runs after Proposition N3 (`eps_gate_depth.log`) show the same growth, exactly $\times p$ per level once $s\ge4$.
- At $p=7$ (and less clearly at $p=5$) the typical $\varepsilon_\ell$ decays steadily, which is consistent with FE for a summable $\bar\varepsilon_\ell$.
- At $p=3$, over the accessible range, the typical $\varepsilon_\ell$ does not yet decrease, because the deepest gate in a window grows with its length. The data are inconclusive there.

This is evidence about plausibility only. FE needs control of **all** later windows, which no finite computation provides.

### 7.4 Exact checks of the two-window machinery

`twowin_check.py` checks, by brute force over all $w\bmod p^{D+D'}$ and all children and grandchildren:
- the martingale identity over two windows, in exact rationals;
- Lemma C1(b) for every frequency $\xi\in\mathbb Z/p^{D'}$, in floating point with relative tolerance $10^{-9}$ (the left side is computed from the actual child targets);
- Proposition C2, in exact rationals, with $\varepsilon$ computed independently from the composite collision probabilities.

| $p$ | $n$, $H$, $H'$ | samples | martingale | C1 (all $\xi$) | C2 | max of LHS$/(\varepsilon M^2)$ |
|---|---|---|---|---|---|---|
| 3 | 20, 4, 4 | 12 | 12/12 | 150/150 | 12/12 | 0.28 |
| 3 | 26, 5, 5 | 6 | 6/6 | 216/216 | 6/6 | 0.060 |
| 5 | 20, 5, 5 | 5 | 5/5 | 25/25 | 5/5 | 0.11 |
| 7 | 21, 7, 7 | 2 | 2/2 | 14/14 | 2/2 | 0.013 |

The two-window bound holds in every case, with slack factors of $4$ to $80$. This slack is expected, because Cauchy–Schwarz over the parents is applied at the high frequencies.

## 8. Computational record

All programs are in `code/round3/R3M/`. All logs are in `data/round3/R3M/`, each run preceded by `### command:` and `### start:` lines and followed by `### wall:`. Runs were made on the shared 4-core machine (load average about 7 from other tracks), under `nice -n 10`, at most one or two processes at a time. Every exact test below is **corroboration**: no proved statement depends on it.

**Exact tests (corroboration of proved statements).**

| program (what it checks) | independent of | runs: $p$, $(n,N)$ or $(n,H,H')$ → result | log | wall per run |
|---|---|---|---|---|
| `oddp_window_check.py`: Prop A(iii) state by state, slope inheritance, constancy on $C$; aliveness by direct evaluation of $S_{(e,f)}(x_w)$ mod $p^{120}$ | R1b's `mart_check2.py`, `brute_window.py`, the lead's `lead_window_check.py` | $p=3$: (20,26), (24,33), (30,39), (36,45) → 1125, 1716, 1063, 3089 parents exact (slopes 0–3); $p=5$: (16,26), (24,34), (30,40) → 250, 90, 65 (slopes 0–2); $p=7$: (21,35), (28,42) → 20, 12 (slopes 0–1). Total 7430 parents, 62132 (parent, state) identities, 0 failures | `window_check_A.log` | 9–614 s |
| `oddp_window_check_B.py`: the same identity by the carry recursion with tracked precision, slopes from python-flint polynomials, weights by a residue DP | `oddp_window_check.py` (no shared code) | $p=3$: (20,26), (24,33), (30,39) → 421, 28, 24; $p=5$: (24,34) → 30; $p=7$: (21,35) → 9. Total 512 parents, 0 failures (slopes 0–2). One run with a too small `DMAX` found no admissible parent and is superseded | `window_check_B.log` | 3–26 s |
| `spectral_check.py`: Prop B(i) pointwise for every $w$ and parent (exact); Prop B(ii) via an explicit DFT (float, rel. tol. $10^{-9}$) | — | $p=3$ (20,26), (30,38); $p=5$ (20,28); $p=7$ (14,22) → 84560 pointwise counts exact, 44/44 identities. A $p=11$ attempt found no admissible $x$ ($n$ too small) | `spectral_check.log` | 2–42 s |
| `twowin_check.py`: Cor A′ over two windows, Lemma C1(b), Prop C2 (§7.4) | — | 25 samples at $p=3,5,7$, 0 failures | `twowin_check.log` | 5–221 s |
| `lemma_c5_check.py`: Lemma C5, both sides in exact rationals | — | $p=3$ (10,5,5), (16,6,6); $p=5$ (12,6,6); $p=7$ (14,8,8) → 48/48 exact | `lemma_c5_check.log` | <1 s |

**Monte Carlo and scans (heuristic).**

| program | purpose | validation | log | wall |
|---|---|---|---|---|
| `oddp_mc.c` (`gcc -O2 -o bin/oddp_mc oddp_mc.c -lm`) | populations $Z_n$, $Z^0_n$, moments of $M^0_n$ (§7.1); carry recursion in exact residues mod $p^K$ ($K=39,27,22,18$), slopes mod $p^{KD}$ | `mc_crosscheck.py` recounts $Z_n,Z^0_n$ by direct polynomial evaluation (no shared code): 12/12, 10/10, 10/10, 5/5 samples agree at $p=3,5,7,11$ | `mc_population.log`, `mc_crosscheck.log` | 16–302 s |
| `spectral_mc.py` | exact conditional variance via Prop B vs diagonal and CS (§7.2) | uses the identity tested by `spectral_check.py` | `spectral_mc_p3.log` | 1–194 s |
| `epsilon_scan.py` | $\varepsilon_\ell$ along windows $\times1.25$ (§7.3); counts exact, sums of squares float64 | identity with the exact collision formula (as in `twowin_check.py`) | `epsilon_scan.log` | 61–127 s |
| `signed_slopes.py` | slope profile of $\mathbb E\Lambda_t$ (Remark C6); float64 DP | — | `signed_slopes.log` | 1–59 s |
| `eps_gate_depth.py` | $\varepsilon$ vs depth of a forced gate (after Prop N3) | — | `eps_gate_depth.log` | 29 s |

Exact command lines are at the top of each run in the logs. Typical forms are `python3 code/round3/R3M/oddp_window_check.py p SEED NX n N DMAX [MAXPAR]`, `code/round3/R3M/bin/oddp_mc p SEED NX NMAX K KD CAP [NVERB]` and `python3 code/round3/R3M/epsilon_scan.py p SEED NX n0 ratio KMAX`. `runlog.sh` is the logging wrapper. Several runs were killed by hand because they were too slow on the loaded machine; each such kill is marked in the log, followed by the re-run with smaller parameters. No result is taken from a killed run.

## 9. Failed attempts and where they break

1. **Per-window Cauchy–Schwarz (the suggested route (b)).** It breaks at Proposition N: every window has $\chi^2_W\ge(p-1)4^{-p}$ from the mod-$p$ shell alone, so $\prod(1+\chi^2_\ell)=\infty$. Neither choosing windows that end just after deep gates and start $Cd$ steps before them, nor averaging over the environment, removes the low shell. The bound is attained when the population is a single path.
2. **One long composite window, Cauchy–Schwarz once.** The exact identities need the linear regime: the targets must be affine in the fresh digits at the precision of the whole window, i.e. $D_{\rm total}\le m-M$. Beyond a factor of about $2$ in time this fails in two ways. The targets are no longer affine in $w$, and the window law itself depends on the fresh digits, with a lag of $m$ digits. Restarting Cauchy–Schwarz once per doubling gives $\mathbb E[M_n^2]\le\prod_{\text{epochs}}(1+\chi^2)$, which grows at least polynomially in $n$ by Proposition N. Paley–Zygmund then only gives a survival probability $\ge n^{-C}$.
3. **A finite computation for each gate level $d$.** The windows just before a level-$d$ gate are position-independent only modulo $p^d$. The quantity that controls the variance, $\varepsilon_\ell$, involves the composite law modulo $p^{D_{\ell-1}+D_\ell}$, which depends on digits of $x$ above the gate level (note Theorem 3.12(a): a dependence on $K'\bmod p^c$). So no single finite check per $d$ suffices, and by item 1 gate windows alone cannot close the argument.
4. **Unconditional FE by annealing (Lemma C5, Remark C6).** The averaged fine-scale mass reduces exactly to increments of the normalised survival $\Lambda_t$ of the signed carry process. Slope classes visible to the windows contribute zero in expectation. The argument stops in two places:
   - at (S), the high-slope (near-multiple-root) signed mass, which the heuristic data of Remark C6 show is not negligible at $p=3$;
   - at Proposition N3, by which $\Lambda_t$ has infinite mean, so a truncation at deep gates near window starts is unavoidable.
5. **Positive measure of achievement sets (route (c), explored only).** Requiring $\mu(A_y)>0$ for a.e. $y$ amounts to an $L^2$ density for the Bernoulli measure $\nu_y$. The annealed $L^2$ norm of $\nu_y$ is again a collision probability, i.e. the density at $0$ of the signed law, so it meets the same obstruction (S). Even granted, it would not give $x\in K_p$: the target $\tau_n(e,x)$ (an isometric function of the fresh digits) and the set $A_{x+n}$ (which depends on the same digits with a lag) are coupled. No soft argument for this coupling was found. A "full set" route ($\mu(\mathcal G_p)>0$) was not pursued, because fullness is a covering statement and runs into Theorem 3.10 and Corollary 10.13 directly.

## 10. Open issues and recommended next steps

1. **Prove (S)** (Remark C6). This is a first-moment bound for the signed carry process (digits $-1,0,1$ with weights $\frac14,\frac12,\frac14$) restricted to paths whose slope exceeds a fraction of $V_t$, uniformly on cylinders. It is the odd-$p$, signed analogue of note Proposition 10.7 (multiplicity $k\ge2$, subcritical). The distinct-valuation counting of that proof transfers, because two different digits $d\ne d'\in\{-1,0,1\}$ cannot agree modulo $p$ (as $|d-d'|\le2<p$), so each distinct-level index costs a factor $\le\frac12$. Proposition N3 forces a truncation first. The target is then: $\mathbb E_A[\varepsilon_\ell\,\mathbf 1_{G_\ell}]$ is exponentially small in $n_{\ell-1}$, where $G_\ell$ is the event that no gate deeper than a slowly growing threshold $s_\ell$ lies near the start of $W_{\ell-1}$, and $\sum_\ell\mu_A(G_\ell^c)$ is small (as in Lemma C4). Given (S), this would follow from Lemma C5 and Remark C6. FE would then follow by Markov's inequality, and Theorem C3 would give $\mu(K_p)>0$. The discussion after Proposition N3 indicates that this can only work where the deep-gate prefactor $\kappa_\ell$ decays. The numerics (§7) suggest trying large $p$ first, where the slope-0 population carries most of $K_p$ and the high-slope signed mass is small.
2. **Positive slopes.** Extend Proposition B and Proposition C2 to the frozen-weight martingale on slopes $\le L$. This would capture all of $K_p$ rather than the slope-0 part, which is $\approx30\%$ of $K_3$ and $\approx89\%$ of $K_{11}$ numerically. It matters for constants, not for positivity.
3. **A stronger test of FE.** For one explicit admissible atom $A$ (say at $p=7$ or $11$), estimate $\mu_A(\exists\ell\le\ell_{\max}:\varepsilon_\ell>\bar\varepsilon_\ell)$ by sampling, with $\ell_{\max}$ limited by the cost $p^{K_\ell}$. This can only ever be heuristic for the tail.

## 11. Credit

- The quenched first-moment window identity, the frozen-state weights and the martingale at $p=2$ are track R1b's (round 2; note §10.1, `code/round2/R1b/muK2_proof.tex`). R1b also sketched the odd-$p$ transfer (note §10.1.3). Proposition A and Corollary A′ carry it out in full.
- Branching processes in random environments: Smith–Wilkinson (1969) and Athreya–Karlin (1971) for survival and extinction criteria under conditional independence, and Afanasyev–Geiger–Kersting–Vatutin (2005). The Paley–Zygmund inequality, Doob's $L^2$ martingale convergence and Minkowski's inequality are classical.
- The problem is due to Erdős and Graham. Tao's block lemma and position-independence programme (forum, 29 Sep 2025) and Kitamura's branching-process picture at $p=2$ (July 2026) are the background of note §§1–2 and 5. The barrier lemma (Theorem 3.10) is round-1 track C's. Corollary 10.13 is round-2 track R2b's, and Proposition 10.19 and Corollary 10.20 are round-2 track R2a's. The values $\mu(K_p)\approx0.36,0.52,0.62,0.70$ are from note §5 (round 1).
- Everything in this report was produced in an AI-assisted session (track R3M of round 3) and has not been checked by a human.
