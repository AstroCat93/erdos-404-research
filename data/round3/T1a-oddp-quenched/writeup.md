# Track T1a (round 3): the quenched martingale at odd primes and an $L^2$ criterion for $\mu(K_p)>0$

Date: 2026-10-21 (retry of the instance cut off on 2026-10-12). Author: AI track T1a; prompted by Nathan Durfee. **Nothing here has been human-refereed.** Every claim is labelled [proved] / [computer-assisted] / [heuristic] / [conjecture] / [sketch]. The previous instance left `window_exact.py`, `cp_const.py`, `l2mc.c` and the logs in `logs/`; its writeup was never written (its docstrings refer to "Prop. A, Prop. C, Theorem C" of a file that does not exist). Everything below is re-derived; the old exact-arithmetic logs are reused only as additional cross-checks (§6.1), and `l2mc.c` was **not** used (its window list would overflow the population cap and its resampling loop could spin forever).

## 0. Summary

Target: Conjecture 5.2 of the note, $\mu(K_p)>0$ for odd $p$, by the quenched route of note §10.1.3.

1. **[proved] Theorem D.** The exact martingale of note §10.1 transfers to every odd $p$: with frozen-state weights $\rho_n(e)=p^{\lambda_e}a_n^{(\lambda_e)}(\tau_n(e)\bmod p^{\lambda_e})$ and truncation at $p\lambda$ terms, $M_\ell=2^{-n_\ell}p^{V_{n_\ell}}\sum_{e\in P^L_{n_\ell}}\rho_{n_\ell}(e)$ is a nonnegative martingale for the atom filtration $A_\ell(x)=x+p^{V_{n_\ell}(x)}\mathbb Z_p$ along any deterministic window scheme $n_{\ell+1}=\max(\lfloor rn_\ell\rfloor,n_\ell+p(L+1))$, $1<r<2$, frozen at the first window where the (explicit, $\mathcal G_\ell$-measurable) hypotheses (W2),(W3),(ENV) fail. The hypotheses hold for all large $\ell$ for $\mu$-a.e. $x$ (Lemma F).
2. **[proved] Theorem E ($L^2$ criterion).** If on one atom $A$ of $\mathcal G_j$ with $M_j(A)>0$ one has $\sup_\ell\mathbb E_A[M_\ell^2]\le\Lambda M_j(A)^2$ and $\mu_A(\text{some later window hypothesis fails})<1/\Lambda$, then $\mu(K_p\cap A)\ge\mu(A)\,(1/\Lambda-\mu_A(\text{fail}))>0$. The second condition is automatic for all but a vanishing fraction of atoms as $j\to\infty$ (Lemma F). Hence **Hypothesis H(p)** (§4.1): *the per-window relative variances $R_\ell$ are summable, uniformly on the atoms below $A$*, implies $\mu(K_p)>0$ (Corollary G). Theorem J gives the cleaner sufficient condition H'(p): *bounded $\kappa_\ell r^{\max}_\ell$* (aggregate parent-correlation ratio times single-parent relative variance) on the unfrozen atoms, with an explicit $\Lambda=1+p^LK S_j/M_j(A)$, $S_j=\sum_{\ell\ge j}(p^{1/(p-1)}/2)^{n_\ell}n_\ell^3$, which uses $p^{1/(p-1)}<2$ and is where odd $p$ differs from $p=2$. This is deliverable (b).
3. **[proved] Theorem H (exact one-window second moment).** On an atom satisfying the window hypotheses, the weighted child sum $\Sigma(w)=\sum_eX_e(w)$ has the exact representation $X_e(w)=\Phi_{\lambda_e,s_e}(\theta_e-\beta_ew\bmod p^D)$ with a profile $\Phi$ built from the window map alone, and
$$\mathrm{Var}_w\Sigma=p^{-2D}\sum_{\eta\ne0}\Big|\sum_e e\big(-\eta\,y^*_e/p^D\big)\,\widehat{\Phi}_{\lambda_e,s_e}(-\eta/\beta_e)\Big|^2,\qquad y^*_e=\theta_e/\beta_e,$$
i.e. the correlation between parents is exactly "window Fourier coefficients $\times$ Weyl sums of the parents' phase points", and $R\le\sum_c\pi_c\sum_{\zeta\ne0}|\hat\varphi_c(\zeta)|^2|w_c(-\beta_c\zeta)|^2$ (Proposition H.3). The children's phase points obey an explicit recursion (Proposition I) in which the window's Fourier coefficients at frequencies of order $p^{D+\lambda+d}$ multiply Weyl sums of the parents' targets at the finer scale; **this is where a proof would have to contract, and we show why sup-type bounds cannot do it (Remark I.2)**.
4. **[computer-assisted] Numerics (deliverable (c)).** New C program `winvar.c` (exact integer arithmetic mod $p^P$, $p^P<2^{126}$, additive path representation), cross-validated to all printed digits against the previous instance's independent Python brute force on four windows ($p=3,5,7$). Along quenched trajectories the window relative variance $R_\ell$ decays geometrically and $R_\ell\cdot|P^L_{n_\ell}|$ stays $O(1)$ (e.g. $p=3$, $L=4$: $R=1.1\cdot10^{-2},1.1\cdot10^{-3},3.2\cdot10^{-5},9.4\cdot10^{-6}$ while $|P|=28,410,6018,89168$); atom Monte Carlo of $\mathbb E[M_\ell^2]$ is flat within statistical error over the accessible windows. Tables in §6. This **supports H(p)** for $p=3,5,7$ at the accessible depths; it is not a proof and does not reach the deep-gate regime.
5. **Not achieved:** a proof of H(p). The obstruction is the same decorrelation problem as RMF (note Thm 10.16/Cor 10.20): the contraction factor in Proposition I is a product of cosines at *deep* $p$-adic scales whose supremum over phases is $1-o(1)$; only an averaged (random-phase/$L^2$ over the $p^D$ lifted frequencies) bound can work, and such a bound is exactly a Fourier-decay statement about factorial unit parts that nobody has.

## 1. Setting and notation

$p$ is an odd prime, $v=v_p$, $\mu$ Haar probability on $\mathbb Z_p$, $e(t)=\exp(2\pi it)$. For $x\in\mathbb Z_p$, $j\ge0$:
$$\pi_j(x)=\prod_{i=1}^j(x+i),\qquad V_n(x)=v(\pi_n(x)),\qquad M_n(x)=\max_{1\le i\le n}v(x+i).$$
A *path of length $n$* is $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$; $S_e(X)=\sum_{j<n}e_j\pi_j(X)\in\mathbb Z[X]$ (this is $S_B$ of note §1.2 with $B=\{j\ge1:e_j=1\}$). $e$ is *alive at $n$* (for $x$) if $v(S_e(x))\ge V_n(x)$; its *target* is $\tau_n(e,x)=-S_e(x)/\pi_n(x)\in\mathbb Z_p$ and its *slope* is $\lambda_e(x)=v(S_e'(x))\in\mathbb Z_{\ge0}\cup\{\infty\}$. For $F\in\mathbb Z_p[X]$ write $F^{[i]}=F^{(i)}/i!$. For an infinite word $e$ with $e_0=1$, $F_e(x)=\sum_je_j\pi_j(x)$ (convergent: $V_j\ge v(j!)\to\infty$).

*Basic facts (note §1, §10.1).* $x\in K_p$ iff $F_e(x)=0$ for some infinite $e$ (Prop. 1.2). If $x\equiv-1\pmod p$ then $p\mid\pi_j(x)$ for all $j\ge1$, so $S_e(x)\equiv1$ and $K_p\cap(-1+p\mathbb Z_p)=\emptyset$. *Backward integrality:* if $(e,f)$ is alive at $N>n$ then $e$ is alive at $n$, since $S_e=S_{(e,f)}-\sum_{n\le j<N}f_j\pi_j$ and $p^{V_n}\mid\pi_j$ for $j\ge n$.

Everything in §§2–4 is the odd-$p$ transcription of note §10.1 (track R1b's $p=2$ argument, rewritten by the lead), with the changes announced in note §10.1.3 (truncation at $p\lambda$ terms, weights $p^\lambda a$, normaliser $2^{-n}p^{V_n}$) and with the new ingredient §4 (the $L^2$ half, which at $p=2$ was not needed because the normaliser does not decay). Credit for the quenched idea: track R1b (note §10.1); for the branching-in-random-environment template: Smith–Wilkinson (1969), Athreya–Karlin (1971) (note Remark 10.8.2); the $L^2$/Kesten–Stigum template: Kesten–Stigum (1966), Lyons–Pemantle–Peres (1995), Tanny (1988) (gate list, item (a)).

## 2. Valuations and linearisation at odd $p$

**Lemma A (valuations) [proved].** Let $x\in\mathbb Z_p$ not be a negative integer.
- (a) $V_n\ge v(n!)=(n-s_p(n))/(p-1)$, where $s_p$ is the base-$p$ digit sum; in particular $V_n\ge n/(p-1)-\log_pn-1$.
- (b) For $n<N$: $V_N-V_n<(N-n)/(p-1)+M_N$. In particular $V_n<n/(p-1)+M_n$.
- (c) $V_j-V_n\ge\lfloor(j-n)/p\rfloor$ for $j\ge n$.
- (d) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$ for $i\ge0$, $j\ge1$.
- (e) For $S\in\mathbb Z_p[X]$ and $y,h\in\mathbb Z_p$: $S(y+h)=\sum_iS^{[i]}(y)h^i$ with all $S^{[i]}(y)\in\mathbb Z_p$.
- (f) If $n\ge2p$ then $M_n<V_n$.

*Proof.* (a) Among $n$ consecutive elements of $\mathbb Z_p$ at least $\lfloor n/p^k\rfloor$ are divisible by $p^k$; sum over $k\ge1$ and use Legendre; $s_p(n)\le(p-1)(\log_pn+1)$. (b) Among the $N-n$ consecutive elements $x+n+1,\dots,x+N$ at most $\lceil(N-n)/p^k\rceil\le(N-n)/p^k+1$ are divisible by $p^k$, and none by $p^{M_N+1}$; so $V_N-V_n\le\sum_{k=1}^{M_N}((N-n)/p^k+1)<(N-n)/(p-1)+M_N$. (c) Among $p$ consecutive elements one is divisible by $p$. (d) $\pi_j^{[i]}(x)=\pi_j(x)\,e_i(1/(x+1),\dots,1/(x+j))$ with $e_i$ the elementary symmetric polynomial, each monomial of which has valuation $\ge-iM_j$. (e) Taylor's formula; $S^{[i]}$ has coefficients in $\mathbb Z_p$. (f) For $n\ge2p$ at least two of $x+1,\dots,x+n$ are divisible by $p$; $V_n$ is the sum of all valuations, $M_n$ the largest one, and the second one contributes $\ge1$. $\square$

**Lemma B (linearisation on an atom) [proved].** Let $x\in\mathbb Z_p$ not be a negative integer, $n<N$, $m=V_n(x)$, $D=V_N(x)-m$, and assume $M_N(x)<m$. Let $C=x+p^m\mathbb Z_p$ with normalised Haar measure, fix any base point $x_0\in C$, and write $x'=x_0+p^mw$, $w\in\mathbb Z_p$. For $f\in\{0,1\}^{N-n}$ put $Q_f(X)=\sum_{j=n}^{N-1}f_j\pi_j(X)/\pi_n(X)\in\mathbb Z[X]$.
- (a) $V_n,V_N,M_n,M_N$ are constant on $C$. For every path $e$ of length $n$, aliveness at $n$ is constant on $C$, and so are $S_e^{[i]}(x')\bmod p^m$, $Q_f(x')\bmod p^m$, and $(x'+i)/p^{v(x+i)}\bmod p^{m-M_N}$ for $i\le N$.
- (b) If $e$ is alive at $n$ then, with $\omega=\pi_n(x_0)/p^m\in\mathbb Z_p^\times$,
$$\tau_n(e,x')\equiv\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)\,w\pmod{p^{m-M_n}}.$$
- (c) $(e,f)$ is alive at $N$ iff $e$ is alive at $n$ and $\tau_n(e,x')\equiv Q_f(x')\pmod{p^D}$; then $\tau_N((e,f),x')=(\tau_n(e,x')-Q_f(x'))\,\pi_n(x')/\pi_N(x')$.

*Proof.* (a) For $i\le N$, $v(x+i)\le M_N<m$ and $x'-x\in p^m\mathbb Z_p$, so $v(x'+i)=v(x+i)$ and $(x'+i)/p^{v(x+i)}\equiv(x+i)/p^{v(x+i)}\pmod{p^{m-v(x+i)}}$; the rest is reduction of integer polynomials mod $p^m$. (b) Put $h=p^mw$. By Lemma A(e), $S_e(x')=S_e(x_0)+hS_e'(x_0)+h^2R$, $R\in\mathbb Z_p$. Also $\pi_n(x')=\pi_n(x_0)\prod_{i\le n}(1+h/(x_0+i))=\pi_n(x_0)(1+E)$ with $v(E)\ge m-M_n\ge1$ (Lemma A(f) is not needed here: $m-M_n\ge1$ follows from $M_n\le M_N<m$). Since $e$ is alive at $n$, $S_e(x_0)\in p^m\mathbb Z_p$, and
$$\tau_n(e,x')=\big[\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)w-\omega^{-1}p^mw^2R\big](1+E)^{-1},$$
with the bracket in $\mathbb Z_p$, $(1+E)^{-1}\equiv1$ and $p^m\equiv0\pmod{p^{m-M_n}}$. (c) $S_{(e,f)}(x')=S_e(x')+\sum_{n\le j<N}f_j\pi_j(x')=\pi_n(x')\,(Q_f(x')-\tau_n(e,x'))$ (using backward integrality for the "only if"); $v(S_{(e,f)})\ge V_N=m+D$ iff $v(Q_f-\tau_n)\ge D$. $\square$

**Frozen-state weights.** For $\lambda\ge0$, $n\ge1$, $t\in\mathbb Z/p^\lambda$:
$$a_n^{(\lambda)}(t):=\mathbb P_{f\in\{0,1\}^{p\lambda}}\Big(\sum_{i<p\lambda}f_i\,\frac{\pi_{n+i}(x)}{\pi_n(x)}\equiv t\pmod{p^\lambda}\Big),\qquad\rho_n(e):=p^{\lambda_e}a_n^{(\lambda_e)}\big(\tau_n(e,x)\bmod p^{\lambda_e}\big)\ (\lambda_e<\infty).$$
- $\pi_{n+i}/\pi_n=\prod_{k=1}^i(x+n+k)$ is an integer polynomial, so $a_n^{(\lambda)}$ depends only on $n,\lambda$ and $x\bmod p^\lambda$; $\sum_ta_n^{(\lambda)}(t)=1$; $a_n^{(\lambda)}\in2^{-p\lambda}\mathbb Z$, so $\rho_n(e)>0\Rightarrow\rho_n(e)\ge(p2^{-p})^{\lambda_e}$.
- By Lemma A(c), the terms $j\ge n+p\lambda$ of $Q_f$ vanish mod $p^\lambda$. So if $N-n\ge p\lambda$, $a_n^{(\lambda)}(t)=\mathbb P_{f\in\{0,1\}^{N-n}}(Q_f(x)\equiv t\bmod p^\lambda)$. (*)
- $\rho\equiv1$ for $\lambda=0$. It is not constant in general (`winvar.c` prints the tables on request; e.g. $p=3$, $\lambda=1$, $x+n\equiv0\pmod3$: $a=(1/2,1/4,1/4)$ so $\rho\in\{3/2,3/4\}$).

## 3. The one-window identity and the martingale

Fix $L\ge0$. $P^L_n(x)=\{e\text{ alive at }n:\lambda_e(x)\le L\}$.

**Proposition C (one window) [proved].** In the setting of Lemma B assume
$$\text{(W1) }N-n\ge p(L+1),\qquad\text{(W2) }D+L\le m-M_n,\qquad\text{(W3) }L<m-M_N.$$
Let $e\in P^L_n(x)$ and $\lambda=\lambda_e$. Then:
- (i) membership in $P^L_n$ is constant on $C$; every child $(e,f)$ alive at $N$ at any $x'\in C$ has slope $\lambda$; every $e''\in P^L_N(x')$ has $e''|_n\in P^L_n(x)$.
- (ii) $s_e:=\tau_n(e,x')\bmod p^\lambda$ is constant on $C$.
- (iii) (*affine profile*) Let $\tau_0=\tau_n(e,x_0)\bmod p^{D+\lambda}=s_e+p^\lambda\theta_e$ with $\theta_e\in\mathbb Z/p^D$, and $\beta_e=\omega^{-1}S_e'(x_0)/p^\lambda\in(\mathbb Z/p^D)^\times$. Let $q_f=Q_f(x_0)\bmod p^{D+\lambda}$ and $u=\pi_N(x_0)/(p^D\pi_n(x_0))\bmod p^\lambda$ (both constant on $C$). Define, for $y\in\mathbb Z/p^D$,
$$\Phi_{\lambda,s}(y):=\sum_{f\in\{0,1\}^{N-n}}\mathbf 1\big[q_f\equiv s+p^\lambda y\ (p^D)\big]\;p^\lambda a_N^{(\lambda)}\Big(u^{-1}\,\frac{s+p^\lambda y-q_f}{p^D}\bmod p^\lambda\Big),$$
where $s+p^\lambda y-q_f$ is computed in $p^D\mathbb Z/p^{D+\lambda}$ (well defined: $p^\lambda y\bmod p^{D+\lambda}$ depends only on $y\bmod p^D$). Then for every $w\in\mathbb Z/p^D$ (the digits of $x'$ at positions $m,\dots,m+D-1$ relative to $x_0$),
$$X_e(w):=\sum_{f:\ (e,f)\text{ alive at }N\text{ for }x'}\rho_N((e,f))=\Phi_{\lambda,s_e}\big(\theta_e-\beta_ew\bmod p^D\big).$$
- (iv) (*first moment*) $\mathbb E_{w\in\mathbb Z/p^D}X_e(w)=2^{N-n}p^{-D}\rho_n(e)$. More precisely, for each state $s\in\mathbb Z/p^\lambda$, $\mathbb E_{x'\in C}\#\{f:(e,f)\text{ alive at }N,\ \tau_N((e,f),x')\equiv s\ (p^\lambda)\}=2^{N-n}p^{-D}a_n^{(\lambda)}(s_e)$.

*Proof.* By (W1) and Lemma A(c), $D\ge\lfloor(N-n)/p\rfloor\ge L+1>\lambda$.

(i) Slope: $S'_{(e,f)}=S'_e+\sum_{n\le j<N}f_j\pi'_j$, and by Lemma A(d) ($i=1$) and (W3), $v(\pi'_j(x'))\ge V_j-M_j\ge m-M_N>L$ for $n\le j<N$. So $v(S'_{(e,f)})=v(S'_e)$ if $v(S'_e)\le L$, and $>L$ otherwise. Constancy on $C$: $S'_e(x')\equiv S'_e(x_0)\pmod{p^m}$ (Lemma B(a)) and $L<m$ (from (W2)). Together with backward integrality this gives (i).

(ii) $v(S'_e(x_0))=\lambda\le L<m-M_n$, and $\omega^{-1}S'_e(x_0)w\in p^\lambda\mathbb Z_p$; apply Lemma B(b) and reduce mod $p^\lambda$ ($\lambda\le m-M_n$).

(iii) By (W2), $D+\lambda\le m-M_n$, so Lemma B(b) gives $t(w):=\tau_n(e,x')\bmod p^{D+\lambda}=\tau_0-p^\lambda\beta_ew=s_e+p^\lambda(\theta_e-\beta_ew)$. By Lemma B(a), $q_f$ is constant on $C$ ($D+\lambda\le m$), and so is $u$ (the unit parts $(x'+i)/p^{v(x+i)}$ are constant mod $p^{m-M_N}$ and $\lambda\le L<m-M_N$). By Lemma B(c), $(e,f)$ is alive iff $t(w)\equiv q_f\pmod{p^D}$, and then $\tau_N((e,f),x')\equiv u^{-1}(t(w)-q_f)/p^D\pmod{p^\lambda}$, where $t(w)-q_f\in p^D\mathbb Z/p^{D+\lambda}$ (here $\pi_N(x')/(p^D\pi_n(x'))\equiv u\pmod{p^\lambda}$ is used). The weight of this child is $p^\lambda a_N^{(\lambda)}(\tau_N\bmod p^\lambda)$ ($a_N^{(\lambda)}$ depends on $x'\bmod p^\lambda$, constant on $C$). Summing over $f$ gives $\Phi_{\lambda,s_e}(\theta_e-\beta_ew)$.

(iv) $w\mapsto\theta_e-\beta_ew$ is a bijection of $\mathbb Z/p^D$, so $\mathbb E_wX_e=p^{-D}\sum_{y}\Phi_{\lambda,s_e}(y)$. Fix $f$. If $q_f\not\equiv s_e\pmod{p^\lambda}$ no $y$ contributes ($D\ge\lambda$). If $q_f\equiv s_e\pmod{p^\lambda}$, the condition $q_f\equiv s_e+p^\lambda y\pmod{p^D}$ fixes $y\bmod p^{D-\lambda}$, leaving $p^\lambda$ values of $y\in\mathbb Z/p^D$; as $y$ runs over them, $p^\lambda y\bmod p^{D+\lambda}$ runs over $(q_f-s_e)+p^D\mathbb Z/p^{D+\lambda}$, so $(s_e+p^\lambda y-q_f)/p^D$ runs over all of $\mathbb Z/p^\lambda$ exactly once, and so does $u^{-1}(\cdot)$. Hence $\sum_y\Phi_{\lambda,s_e}(y)=p^\lambda\#\{f:q_f\equiv s_e\ (p^\lambda)\}\sum_ta_N^{(\lambda)}(t)=p^\lambda2^{N-n}a_n^{(\lambda)}(s_e)$ by (*) (valid since $N-n\ge p\lambda$). The state-by-state statement is the same count with the weight $p^\lambda a_N$ replaced by $\mathbf 1[\text{state}=s]$: exactly one of the $p^\lambda$ values of $y$ (equivalently of $w$) produces state $s$. $\square$

*Remark C.1.* For $\lambda=0$: $\Phi_{0,0}(y)=\#\{f:q_f\equiv y\ (p^D)\}$ is the fibre count of the window map, and $X_e(w)$ is the number of alive children. The previous instance's Python code checked (iii) and (iv) in exact rational arithmetic on $21$ windows (logs `logs/window_p*_L*.log`: 700/700, 7476/7476, 4557/4557 state-by-state first-moment identities exact; "affine=True" in every window satisfying (W2)). The single "affine=False" case ($p=7$, x#5) violates (W2) and is the expected failure of the hypothesis, not of the statement.

### 3.1 Window scheme, filtration, martingale

Fix $L\ge0$, a ratio $1<r<2$, and $n_0\ge2p$. Define deterministic window times
$$n_{\ell+1}=\max\big(\lfloor rn_\ell\rfloor,\ n_\ell+p(L+1)\big),\qquad\ell\ge0,$$
so (W1) holds for every window $[n_\ell,n_{\ell+1})$. For $x\in\mathbb Z_p\setminus(-1+p\mathbb Z_p)$ not a negative integer put $m_\ell(x)=V_{n_\ell}(x)$ and $A_\ell(x)=x+p^{m_\ell(x)}\mathbb Z_p$.

**Lemma D.0 (atoms) [proved].** $\{A_\ell(x)\}_x$ is a partition of $\mathbb Z_p\setminus(\text{negative integers})$ into cylinders, $A_{\ell+1}(x)\subseteq A_\ell(x)$, and $m_\ell$ is constant on $A_\ell(x)$.
*Proof.* By Lemma A(f) ($n_\ell\ge2p$), $M_{n_\ell}(x)<m_\ell(x)$, so for $y\in A_\ell(x)$ we have $v(y+i)=v(x+i)$ for $i\le n_\ell$, hence $m_\ell(y)=m_\ell(x)$ and $A_\ell(y)=A_\ell(x)$. Since $m_{\ell+1}\ge m_\ell$, $A_{\ell+1}(x)\subseteq A_\ell(x)$. $\square$

Let $\mathcal G_\ell$ be the $\sigma$-algebra generated by the atoms $A_\ell$; $(\mathcal G_\ell)$ is a filtration, and conditional expectation given $\mathcal G_\ell$ is the Haar average over the atom. The *window hypotheses* for window $\ell$ are
$$\mathcal C_\ell:\qquad\text{(W2) }D_\ell+L\le m_\ell-M_{n_\ell},\qquad\text{(W3) }L<m_\ell-M_{n_{\ell+1}},\qquad\text{(ENV) }M_{n_{\ell+1}}<m_\ell,$$
with $D_\ell=m_{\ell+1}-m_\ell$. **$\mathcal C_\ell$ is $\mathcal G_\ell$-measurable:** for $y\in A_\ell(x)$ and $i\le n_{\ell+1}$, either $v(x+i)<m_\ell$ and then $v(y+i)=v(x+i)$, or $v(x+i)\ge m_\ell$ and then $v(y+i)\ge m_\ell$ too; so (ENV) is constant on the atom, and on (ENV) all of $v(y+i)$, $i\le n_{\ell+1}$, hence $D_\ell$ and $M_{n_{\ell+1}}$, are constant.

Fix $j\ge0$. Let $\sigma_j=\min\{\ell\ge j:\mathcal C_\ell\text{ fails}\}\in[j,\infty]$ (a stopping time). Define
$$M_\ell:=2^{-n_\ell}p^{m_\ell}\sum_{e\in P^L_{n_\ell}(x)}\rho_{n_\ell}(e)\quad(j\le\ell\le\sigma_j),\qquad M_\ell:=M_{\sigma_j}\ (\ell\ge\sigma_j),\qquad M_\ell:=0\ \forall\ell\ge j\text{ on }\{\sigma_j=j\}.$$

**Theorem D (quenched martingale, odd $p$) [proved].** $(M_\ell)_{\ell\ge j}$ is a nonnegative martingale with respect to $(\mathcal G_\ell)_{\ell\ge j}$ (on $\mathbb Z_p\setminus(-1+p\mathbb Z_p)$, i.e. on every atom of $\mathcal G_j$). Moreover $M_\ell=0\Rightarrow M_{\ell+1}=0$, and if $\sigma_j(x)=\infty$ and $M_\ell(x)>0$ for all $\ell\ge j$ then $x\in K_p$.

*Proof.* *Measurability.* On $\{\sigma_j>\ell\}$ (a $\mathcal G_\ell$-event, since $\mathcal C_j,\dots,\mathcal C_\ell$ are $\mathcal G_\ell$-measurable) we must show that $M_\ell$ is constant on $A_\ell(x)$. Aliveness at $n_\ell$ is constant (Lemma B(a)); "$\lambda_e\le L$" is constant because $S'_e\bmod p^{m_\ell}$ is and $L<m_\ell$ (from (W2) of window $\ell$); $\tau_{n_\ell}(e)\bmod p^{\lambda_e}$ is constant by Lemma B(b) provided $\lambda_e\le m_\ell-M_{n_\ell}$: for $\ell=j$ this is (W2) of window $j$; for $\ell>j$ it follows from (W3) of window $\ell-1$, $L<m_{\ell-1}-M_{n_\ell}\le m_\ell-M_{n_\ell}$. Finally $a^{(\lambda)}_{n_\ell}$ depends on $x\bmod p^\lambda$, $\lambda\le L<m_\ell$. After freezing, measurability is inherited.

*Martingale property.* On $\{\sigma_j>\ell\}$, window $\ell$ satisfies (W1)–(W3) and (ENV), so Proposition C applies on $A_\ell(x)$ with $n=n_\ell$, $N=n_{\ell+1}$, $m=m_\ell$, $D=D_\ell$. By C(i), $P^L_N(x')$ is the disjoint union over $e\in P^L_n$ of the alive children of $e$, each of slope $\lambda_e$, with weight $\rho_N((e,f))=p^{\lambda_e}a_N^{(\lambda_e)}(\tau_N\bmod p^{\lambda_e})$. Hence $M_{\ell+1}=2^{-N}p^{m+D}\sum_{e\in P^L_n}X_e(w)$ where $w$ is the digit block of $x'$ at positions $m,\dots,m+D-1$, which is Haar-uniform on $\mathbb Z/p^D$ under $\mu_{A_\ell(x)}$ (the digits at positions $\ge m$ are i.i.d. uniform). By C(iv),
$$\mathbb E[M_{\ell+1}\mid\mathcal G_\ell]=2^{-N}p^{m+D}\sum_e2^{N-n}p^{-D}\rho_n(e)=2^{-n}p^m\sum_e\rho_n(e)=M_\ell .$$
On $\{\sigma_j\le\ell\}$ the process is constant. Nonnegativity is clear.

*Zero is absorbing.* If $M_\ell=0$ on $\{\sigma_j>\ell\}$ then every $e\in P^L_n$ has $a_n^{(\lambda_e)}(s_e)=0$, i.e. (by (*)) no $f$ with $q_f\equiv s_e\pmod{p^{\lambda_e}}$; since a child requires $q_f\equiv t(w)\equiv s_e\pmod{p^{\lambda_e}}$ ($D\ge\lambda_e$), no $e\in P^L_n$ has a child, so by C(i) $P^L_N=\emptyset$ and $M_{\ell+1}=0$.

*Survival gives $K_p$.* If $M_\ell(x)>0$ for all $\ell\ge j$ and $\sigma_j=\infty$, then $P^L_{n_\ell}(x)\ne\emptyset$ for all $\ell$, so alive paths exist at every $n_\ell$, hence (backward integrality) at every $n\ge1$. The set of alive finite paths is a prefix-closed tree, finitely branching, with a node at every level; by König's lemma it has an infinite branch $e$. Then $v(S_{e|_n}(x))\ge V_n(x)\to\infty$ (Lemma A(a)), so $F_e(x)=\lim_nS_{e|_n}(x)=0$ and $x\in K_p$ (Prop. 1.2). $\square$

*Remark D.1 (what differs from $p=2$).* Nothing in the martingale half. The difference is in the normaliser: $2^{-n}p^{V_n}\approx(p^{1/(p-1)}/2)^n$ with $p^{1/(p-1)}<2$ for $p\ge3$, so $\mathbb E\sum\rho$ grows like $(2p^{-1/(p-1)})^n$ (supercritical, note §10.1.3), and the extinction argument of §10.1 (an environment walk unbounded below) is unavailable: $W_n:=n-V_n\log_2p\to+\infty$. The question becomes whether $M_\ell$ converges to a nonzero limit with positive probability, which is the $L^2$ question of §4.

**Lemma F (hypotheses hold eventually, a.e.) [proved].** For $\mu$-a.e. $x$ there is $\ell_0(x)$ with $\mathcal C_\ell(x)$ true for all $\ell\ge\ell_0$. Consequently $\mu(\sigma_j<\infty)\downarrow0$ as $j\to\infty$, and for every $\varepsilon>0$ the union of the atoms $A$ of $\mathcal G_j$ with $\mu_A(\sigma_j<\infty)\ge\varepsilon$ has measure $\le\mu(\sigma_j<\infty)/\varepsilon\to0$.

*Proof.* $\mu\{\exists i\le n:v(x+i)\ge K\}\le np^{-K}$. With $K_\ell=\lceil3\log_pn_{\ell+1}\rceil$, $\mu\{M_{n_{\ell+1}}\ge K_\ell\}\le n_{\ell+1}^{-2}$, which is summable since $n_\ell\ge n_0+\ell p(L+1)$. By Borel–Cantelli, a.e. $x$ has $M_{n_{\ell+1}}<3\log_pn_{\ell+1}+1$ for all large $\ell$. For such $\ell$, Lemma A(a),(b) give $m_\ell\ge n_\ell/(p-1)-\log_pn_\ell-1$ and $D_\ell<(n_{\ell+1}-n_\ell)/(p-1)+M_{n_{\ell+1}}\le(r-1)n_\ell/(p-1)+3\log_pn_{\ell+1}+2$ (for large $\ell$, $n_{\ell+1}-n_\ell\le(r-1)n_\ell+1$). Since $r-1<1$, (W2), (W3) and (ENV) hold once $n_\ell$ is large. The rest is monotonicity of the events $\{\sigma_j<\infty\}=\{\exists\ell\ge j:\mathcal C_\ell\text{ fails}\}$ (decreasing in $j$ with null intersection) and Markov's inequality applied to $\mu(\sigma_j<\infty)=\sum_A\mu(A)\mu_A(\sigma_j<\infty)$. $\square$

## 4. The $L^2$ criterion

**Theorem E ($L^2$ criterion) [proved].** Let $p$ be odd, fix $L$, $r$, $n_0$, $j$ as above, and let $A$ be an atom of $\mathcal G_j$ on which $M_j(A)>0$ (so $\mathcal C_j$ holds on $A$). Suppose there is $\Lambda\ge1$ with
$$\text{(E1)}\quad\sup_{\ell\ge j}\mathbb E_A[M_\ell^2]\le\Lambda\,M_j(A)^2,\qquad\text{(E2)}\quad\mu_A(\sigma_j<\infty)<1/\Lambda .$$
Then $\mu(K_p\cap A)\ge\mu(A)\big(1/\Lambda-\mu_A(\sigma_j<\infty)\big)>0$. In particular $\mu(K_p)>0$.

*Proof.* On the probability space $(A,\mu_A)$, $(M_\ell)_{\ell\ge j}$ is an $L^2$-bounded martingale (Theorem D, (E1)), so it converges a.s. and in $L^2$ to some $M_\infty\ge0$ with $\mathbb E_AM_\infty=M_j(A)$ and $\mathbb E_AM_\infty^2\le\Lambda M_j(A)^2$. By Cauchy–Schwarz, $\mathbb E_AM_\infty=\mathbb E_A[M_\infty\mathbf 1_{M_\infty>0}]\le(\mathbb E_AM_\infty^2)^{1/2}\mu_A(M_\infty>0)^{1/2}$, so $\mu_A(M_\infty>0)\ge(\mathbb E_AM_\infty)^2/\mathbb E_AM_\infty^2\ge1/\Lambda$. On $\{M_\infty>0\}\cap\{\sigma_j=\infty\}$ we have $M_\ell>0$ for every $\ell\ge j$ (zero is absorbing, Theorem D), hence $x\in K_p$ (Theorem D). The measure of this event is at least $\mu_A(M_\infty>0)-\mu_A(\sigma_j<\infty)$. $\square$

*Remark E.1.* (E2) is cheap: by Lemma F, for every $\Lambda$ and all large $j$, all but a vanishing fraction of the atoms of $\mathcal G_j$ satisfy (E2). The content of the criterion is (E1), uniform in $\ell$. Note also that (E1) is not a statement about one $x$ but about the Haar average over the atom of the *squared* weighted population, so the "shadow" atoms (near negative integers), on which the unconditioned second moment of track T4 blows up, enter only through their own conditional second moment, weighted by their small measure in the filtration. The annealed divergence $\mathbb EZ_G^2\ge p^G/4$ (T4, Prop. 2) is not in contradiction with (E1): T4's $Z_G$ counts all witnesses with weight 1 over all of $\mathbb Z/p^G$, and the $x\equiv-2\pmod{p^G}$ class alone contributes $p^G/4$; in the quenched martingale that class is an atom of its own (its $V_n$ is huge), and what matters is $\mathbb E[M^2]$ on *fixed* atoms chosen at a fixed level $j$.

### 4.1 Window relative variance

For an atom $A'$ of $\mathcal G_\ell$ on which $\mathcal C_\ell$ holds and $M_\ell(A')>0$ define the *window relative variance*
$$R_\ell(A'):=\frac{\mathrm{Var}_{w}\,\Sigma(w)}{(\mathbb E_w\Sigma)^2},\qquad\Sigma(w)=\sum_{e\in P^L_{n_\ell}}X_e(w),$$
and $R_\ell(A')=0$ if $M_\ell(A')=0$. Since $M_{\ell+1}=2^{-N}p^{m+D}\Sigma(w)$ and, by Proposition C(iv), $\mathbb E_w\Sigma=2^{N-n}p^{-D}\sum_e\rho_n(e)$, we have $M_\ell=2^{-n}p^m\sum_e\rho_n(e)=2^{-N}p^{m+D}\,\mathbb E_w\Sigma$, and therefore the exact identities
$$\mathbb E[(M_{\ell+1}-M_\ell)^2\mid\mathcal G_\ell]=M_\ell^2R_\ell,\qquad\mathbb E[M_{\ell+1}^2\mid\mathcal G_\ell]=M_\ell^2(1+R_\ell)\quad\text{on }\{\sigma_j>\ell\}.$$

**Corollary G (summable relative variances) [proved].** Let $A$ be an atom of $\mathcal G_j$ with $M_j(A)>0$, and let $\bar R_\ell:=\sup\{R_\ell(A'):A'\subseteq A\text{ an atom of }\mathcal G_\ell\text{ with }\mathcal C_j,\dots,\mathcal C_\ell\text{ true}\}$. If $\sum_{\ell\ge j}\bar R_\ell<\infty$ then (E1) holds with $\Lambda=\prod_{\ell\ge j}(1+\bar R_\ell)$. Hence, if in addition $\mu_A(\sigma_j<\infty)<1/\Lambda$, $\mu(K_p\cap A)>0$.
*Proof.* $\mathbb E_A[M_{\ell+1}^2]=\mathbb E_A[M_\ell^2(1+R_\ell\mathbf 1_{\sigma_j>\ell})]\le(1+\bar R_\ell)\mathbb E_A[M_\ell^2]$; induct. $\square$

**Hypothesis H(p) (the precise form of deliverable (b)).** *There exist $L$, $r\in(1,2)$, $n_0\ge2p$, $j$, an atom $A$ of $\mathcal G_j$ with $M_j(A)>0$, and a summable sequence $(c_\ell)_{\ell\ge j}$ with $R_\ell(A')\le c_\ell$ for every atom $A'\subseteq A$ of $\mathcal G_\ell$ on which $\mathcal C_j,\dots,\mathcal C_\ell$ hold, such that $\mu_A(\sigma_j<\infty)<\prod_{\ell\ge j}(1+c_\ell)^{-1}$.*

**Theorem (H(p) $\Rightarrow\mu(K_p)>0$) [proved].** Immediate from Corollary G and Theorem E.

*How checkable is H(p)?* Each $R_\ell(A')$ is a finite exact computation (Theorem H below: $p^D$ evaluations of a sum over the parent population, all in exact integer arithmetic; `winvar.c` does it in double precision), and $\mu_A(\sigma_j<\infty)$ can be bounded by Lemma F's Borel–Cantelli estimate explicitly. What cannot be done by computation is the sup over all atoms at all levels $\ell$; §6 measures $R_\ell$ along quenched trajectories and on sampled atoms. The weaker averaged form $\sum_\ell\mathbb E_A[M_\ell^2R_\ell]<\infty$ is equivalent to (E1) and is what the atom Monte Carlo of §6.3 estimates directly.

## 5. The one-window second moment: exact structure

Throughout this section fix an atom with (W1)–(W3), parents $P=P^L_n$ with data $(\lambda_e,s_e,\theta_e,\beta_e)$ and profiles $\Phi_e:=\Phi_{\lambda_e,s_e}$ (Proposition C). For $F:\mathbb Z/p^D\to\mathbb C$ put $\widehat F(\zeta)=\sum_yF(y)e(-\zeta y/p^D)$. Write $\mu_e=\mathbb E_wX_e=2^Hp^{-D}\rho_n(e)$ ($H=N-n$), $y^*_e=\theta_e\beta_e^{-1}\in\mathbb Z/p^D$ (the *phase point* of $e$: the digit block $w\equiv y^*_e$ is the one at which $\tau_n(e,x')\equiv s_e\pmod{p^{D+\lambda}}$).

**Theorem H (exact variance) [proved].**
$$\widehat\Sigma(\eta)=\sum_{e\in P}e\big(-\eta\beta_e^{-1}\theta_e/p^D\big)\,\widehat{\Phi}_e(-\eta\beta_e^{-1}),\qquad
\mathrm{Var}_w\Sigma=p^{-2D}\sum_{\eta\in\mathbb Z/p^D\setminus0}\big|\widehat\Sigma(\eta)\big|^2 .$$
*Proof.* $\widehat{X_e}(\eta)=\sum_w\Phi_e(\theta_e-\beta_ew)e(-\eta w/p^D)$; substitute $y=\theta_e-\beta_ew$, $w=\beta_e^{-1}(\theta_e-y)$ (a bijection since $\beta_e$ is a unit): $\widehat{X_e}(\eta)=e(-\eta\beta_e^{-1}\theta_e/p^D)\sum_y\Phi_e(y)e(\eta\beta_e^{-1}y/p^D)$. Sum over $e$ and apply Parseval on $\mathbb Z/p^D$. $\square$

Grouping parents into *classes* $c$ with equal $(\lambda,s,\beta\bmod p^D)$ (so equal $\Phi_c$ and equal frequency $-\eta/\beta_c$), with $\pi_c=\rho_c|c|/\sum_e\rho_e$, normalised profile transform $\hat\varphi_c(\zeta)=\widehat\Phi_c(\zeta)/\widehat\Phi_c(0)$ and class Weyl sum $w_c(\eta)=|c|^{-1}\sum_{e\in c}e(-\eta y^*_e/p^D)$:

**Proposition H.3 (Fourier $\times$ Weyl form; Jensen bound) [proved].**
$$R=\frac{\mathrm{Var}_w\Sigma}{(\mathbb E_w\Sigma)^2}=\sum_{\eta\ne0}\Big|\sum_c\pi_c\,\hat\varphi_c(-\eta/\beta_c)\,w_c(\eta)\Big|^2\ \le\ \sum_c\pi_c\sum_{\zeta\ne0}|\hat\varphi_c(\zeta)|^2\,|w_c(-\beta_c\zeta)|^2 .$$
*Proof.* $\widehat\Phi_c(0)=\sum_y\Phi_c=2^H\rho_c$ (proof of C(iv)) and $\mathbb E_w\Sigma=2^Hp^{-D}\sum_e\rho_e$; insert into Theorem H and use $(\sum_c\pi_ca_c)^2\le\sum_c\pi_ca_c^2$ ($\sum_c\pi_c=1$). $\square$

This is the precise form of the heuristic "correlation = window Fourier coefficients $\times$ Weyl sums of parent targets": $\sum_{\zeta\ne0}|\hat\varphi_c(\zeta)|^2=p^D\,\mathrm{Var}\Phi_c/(\text{mean}\,\Phi_c)^2$ is the single-parent relative variance, and $|w_c|^2$ measures the equidistribution of the class's phase points. Classes with $w_c\equiv0$ off $0$ (phase points exactly equidistributed mod $p^D$) contribute nothing; a class whose parents all have the same phase point ($w_c\equiv1$) contributes its full single-parent relative variance, independently of $|c|$. The Jensen bound is useful only when the classes are large; for singleton classes it loses the factor $1/|P|$ that independent parents would give, so the quantity we actually measure is the *aggregate correlation ratio*
$$\kappa:=\frac{\mathrm{Var}_w\Sigma}{\sum_e\mathrm{Var}_wX_e}\quad(\kappa:=1\text{ if the denominator vanishes}),\qquad r_e:=\frac{\mathrm{Var}_wX_e}{\mu_e^2}\ (\mu_e>0),\qquad r^{\max}=\max_{\mu_e>0}r_e .$$
For $\lambda_e=0$, $r_e=\sum_{\zeta\ne0}|\hat h_D(\zeta)|^2$ with $\hat h_D(\zeta)=\prod_{j=n}^{N-1}\tfrac12(1+e(-\zeta y_j/p^D))$, $y_j=\pi_j(x_0)/\pi_n(x_0)$: the Parseval ($L^2$) Fourier mass of the window map at precision $p^D$, a quantity of the same kind as the $L^1$ sums of note §10.4–10.5 and of track T4 item (4), but smaller.

**Theorem J (a cleaner sufficient condition) [proved].** Let $\mathcal C'_\ell=\mathcal C_\ell\wedge\{M_{n_\ell}\le3\log_pn_\ell\}$ (still $\mathcal G_\ell$-measurable; still true for all large $\ell$ for a.e. $x$ by the proof of Lemma F), and run the martingale of Theorem D with $\mathcal C'_\ell$ in place of $\mathcal C_\ell$. Let $A$ be an atom of $\mathcal G_j$ with $M_j(A)>0$. Suppose there is $K<\infty$ such that $\kappa_\ell(A')\,r^{\max}_\ell(A')\le K$ for every $\ell\ge j$ and every atom $A'\subseteq A$ of $\mathcal G_\ell$ on which $\mathcal C'_j,\dots,\mathcal C'_\ell$ hold. Then
$$\sup_{\ell\ge j}\mathbb E_A[M_\ell^2]\le M_j(A)^2+p^LK\,M_j(A)\,S_j,\qquad S_j:=\sum_{\ell\ge j}\Big(\frac{p^{1/(p-1)}}2\Big)^{n_\ell}n_\ell^{3}<\infty,$$
so (E1) holds with $\Lambda=1+p^LKS_j/M_j(A)$; and if $\mu_A(\sigma_j<\infty)<1/\Lambda$ then $\mu(K_p\cap A)>0$.

*Proof.* On an unfrozen atom $A'$ of $\mathcal G_\ell$, with $n=n_\ell$, $N=n_{\ell+1}$, $m=m_\ell$: $M_\ell^2R_\ell=(2^{-N}p^{V_N})^2\mathrm{Var}_w\Sigma\le(2^{-N}p^{V_N})^2\kappa\sum_e\mathrm{Var}_wX_e\le(2^{-N}p^{V_N})^2\kappa r^{\max}\sum_e\mu_e^2$. Now $\sum_e\mu_e^2\le(\max_e\mu_e)\sum_e\mu_e$, $\max_e\mu_e=2^Hp^{-D}\max_e\rho_e\le2^Hp^{-D}p^L$ (as $\rho_e=p^{\lambda_e}a\le p^{\lambda_e}$), and $\sum_e\mu_e=\mathbb E_w\Sigma=2^Np^{-V_N}M_\ell$. Multiplying out, $M_\ell^2R_\ell\le2^{-n}p^{m}\,p^L\kappa r^{\max}M_\ell\le p^LK\,2^{-n}p^mM_\ell$. By Lemma A(b) and $\mathcal C'_\ell$, $p^m<p^{n/(p-1)}p^{M_n}\le p^{n/(p-1)}n^3$. Hence, by §4.1, $\mathbb E_A[M_{\ell+1}^2]-\mathbb E_A[M_\ell^2]=\mathbb E_A[M_\ell^2R_\ell\mathbf 1_{\sigma_j>\ell}]\le p^LK(p^{1/(p-1)}/2)^{n_\ell}n_\ell^3\,\mathbb E_A[M_\ell]=p^LK(p^{1/(p-1)}/2)^{n_\ell}n_\ell^3M_j(A)$. Sum over $\ell\ge j$; $S_j<\infty$ because $p^{1/(p-1)}<2$ for $p\ge3$ and $n_\ell\ge n_0+\ell p(L+1)$. $\square$

*Remarks J.1.* (a) $S_j\to0$ as $j\to\infty$, so under a uniform $K$ the constant $\Lambda$ tends to $1$ on atoms with $M_j(A)$ bounded below; then $\mu_A(M_\infty>0)\to1$ on such atoms, which is the natural guess (the martingale limit is positive on the whole survival set). (b) The two ingredients of $K$ are of different nature: $r^{\max}$ is a property of the window map alone (fibre fluctuations of $f\mapsto Q_f\bmod p^D$ plus the state weights), while $\kappa$ is the decorrelation between parents. In a random model where the window elements of valuation $\ell_j$ have independent uniformly random unit parts, $\mathbb E|\hat h_D(\zeta)|^2\approx2^{-\#\{j:\ell_j<d\}}\approx2^{-pd}$ for $\zeta$ of exact order $p^d$, giving $\mathbb E\,r_0\approx\sum_{d\ge1}(1-1/p)\,(p/2^p)^d<\infty$ for every $p\ge3$ ([heuristic]; T4 found the $L^1$ analogue of this budget reproduced to $10^{-7}$ by the true single-gate-block sums, so the random-model budget is credible for $r$). For $\kappa$: within a class, $\kappa_c=|c|\sum_{\zeta\ne0}|\hat\varphi_c|^2|w_c|^2/\sum_{\zeta\ne0}|\hat\varphi_c|^2$, so $\kappa=O(1)$ requires square-root cancellation $|w_c(\zeta)|^2\lesssim1/|c|$ of the phase-point Weyl sums at the frequencies carrying the profile's Fourier mass. §6 measures exactly this ($\kappa\in[0.02,10]$ over 60 windows; $\rho$-weighted Weyl sums of all parents at orders $p,p^2,p^3$ decaying like $|P|^{-1/2}$).

### 5.1 Where the fresh digits enter: the phase points of the children

Let $D'$ be the depth of the *next* window $[N,N')$ and strengthen the hypotheses to
$$\text{(W2}^+)\ D+D'+L\le m-M_n,\qquad\text{(W3}^+)\ D'+L<m-M_N .$$
For a parent $e$ (slope $\lambda$) and a digit block $w\in[0,p^D)$ put $t^+_e(w):=\tau_n(e,x_0)-p^\lambda\beta_ew\in\mathbb Z/p^{D+D'+\lambda}$ (here $\tau_n(e,x_0)$ and $\beta_e$ are taken modulo $p^{D+D'+\lambda}$ and $p^{D+D'}$), $q_f:=Q_f(x_0)\bmod p^{D+D'+\lambda}$, and $u':=\pi_N(x_0)/(p^D\pi_n(x_0))\bmod p^{D'+\lambda}$.

**Proposition I (children's data) [proved].** Under (W1), (W2$^+$), (W3$^+$): $\tau_n(e,x')\equiv t^+_e(w)\pmod{p^{D+D'+\lambda}}$; $q_f$ and $u'$ are constant on the atom; the child $(e,f)$ is alive iff $q_f\equiv t^+_e(w)\pmod{p^D}$, and then, with $\zeta_{e,f}(w):=(t^+_e(w)-q_f)/p^D\in\mathbb Z/p^{D'+\lambda}$,
$$\tau_N((e,f),x')\equiv u'^{-1}\zeta_{e,f}(w)\ (p^{D'+\lambda}),\qquad\beta_{(e,f)}\equiv\beta_eu'^{-1}\ (p^{D'}),\qquad y^*_{(e,f)}=\frac{\zeta_{e,f}(w)-u'\,s'}{p^\lambda\beta_e}\bmod p^{D'},\ s'=u'^{-1}\zeta_{e,f}(w)\bmod p^\lambda .$$
Consequently the $\rho$-weighted Weyl sum of the children of $e$ at order $p^d$ ($d\le D'$), frequency $\xi$, is
$$W_e(\xi,d;w):=\sum_{f:(e,f)\text{ alive}}\rho_N((e,f))\,e\big(\xi y^*_{(e,f)}/p^d\big)=p^{-K}\sum_{\chi\in\mathbb Z/p^K}\hat g_e(\chi\bmod p^{\lambda+d})\;e\big(\chi\,t^+_e(w)/p^K\big)\;\widehat S(\chi),\qquad K=D+\lambda+d,$$
where $g_e(\zeta)=p^\lambda a_N^{(\lambda)}(u'^{-1}\zeta\bmod p^\lambda)\,e\big(\xi(\zeta-u'(u'^{-1}\zeta\bmod p^\lambda))/(p^{\lambda+d}\beta_e)\big)$ on $\mathbb Z/p^{\lambda+d}$, $\hat g_e$ its Fourier transform there, and
$$\widehat S(\chi)=\sum_{f\in\{0,1\}^H}e\big(-\chi q_f/p^K\big)=2^H\prod_{j=n}^{N-1}\tfrac12\big(1+e(-\chi y_j/p^K)\big),\qquad y_j=\pi_j(x_0)/\pi_n(x_0),$$
is the window subset-sum transform at precision $p^{K}$ (the extra $d$ digits beyond the current window's $D+\lambda$ are the next window's fresh digits).

*Proof.* The first three statements are Lemma B(b),(a),(c) at the higher precision allowed by (W2$^+$) (for $\tau_n$) and (W3$^+$) (for $u'$ and for $S'_{(e,f)}\equiv S'_e$ mod $p^{D'+\lambda}$, since $v(\pi'_j)\ge m-M_N>D'+L$ on the window), exactly as in Proposition C; $\omega_N=\pi_N(x')/p^{V_N}=\omega(x')u'$ with $\omega(x')\equiv\omega(x_0)$ mod $p^{m-M_n}$ gives $\beta_{(e,f)}=\omega_N^{-1}S'_{(e,f)}/p^\lambda\equiv\beta_eu'^{-1}$, and $y^*=\theta'/\beta'$ with $\tau_N=s'+p^\lambda\theta'$. For the Weyl sum: $W_e=\sum_fG_e(t^+_e(w)-q_f)$ with $G_e(z)=\mathbf 1[p^D\mid z]\,g_e(z/p^D)$ on $\mathbb Z/p^K$; its transform is $\widehat{G_e}(\chi)=\sum_{\zeta\bmod p^{\lambda+d}}g_e(\zeta)e(-\chi\zeta/p^{\lambda+d})=\hat g_e(\chi\bmod p^{\lambda+d})$; invert and sum over $f$. $\square$

*Remark I.1 (the induction one would like).* Writing $\chi=\chi_0+p^{\lambda+d}\zeta'$ ($\chi_0\in\mathbb Z/p^{\lambda+d}$, $\zeta'\in\mathbb Z/p^D$) and summing Proposition I over the parents of a class, the children's Weyl sums are $p^{-K}\sum_{\chi_0}\hat g(\chi_0)\sum_{\zeta'}\widehat S(\chi_0+p^{\lambda+d}\zeta')\cdot\big[\text{Weyl sum of the parents' targets }t^+_e(w)\text{ at precision }p^K\big]$. The expected fibre size is $2^Hp^{-D}$, so the *normalised* children's Weyl sum is bounded by $p^{D}\max_\chi|\widehat S(\chi)|/2^H$ times the normalised parent Weyl sums at the finer precision $K=D+\lambda+d$. An induction on "(weighted population, Weyl sums of targets at all available precisions)" is therefore well posed: the parents' targets at precision $p^{D+\lambda+d}$ involve the digits of $x$ at positions up to $m+D+d$, i.e. the current window's digits plus $d$ fresh ones; these fresh digits are Haar-uniform given the atom, which is what should make the parent Weyl sums at precision $p^K$ small (they are the Weyl sums of the *previous* window's children, which Proposition I expresses through the previous window's $\widehat S$, and so on). We did not carry this induction out; see the next remark for why its natural form cannot close.

*Remark I.2 (why sup-type bounds cannot close the induction) [proved facts, interpretation heuristic].* The contraction factor in Remark I.1 is $p^D\max_\chi|\widehat S(\chi)|/2^H$ over frequencies $\chi$ of order up to $p^{K}$. The window contains $\approx H/p$ complete blocks of $p$ consecutive elements following a multiple of $p$; inside such a block the unit parts are $r!\cdot(\text{unit})$, $r=0,\dots,p-1$, so the block contributes $\prod_{r<p}|\cos(\pi\chi'r!/p^k)|$ to $|\widehat S(\chi)|/2^H$ at some scale $k\ge\lambda+d\ge1$. At $k=1$ the supremum over $\chi'$ is $c_p=\max_\xi\prod_{r<p}|\cos(\pi\xi r!/p)|$ ($=1/8,0.1324,0.0824,0.0267,0.0033$ for $p=3,5,7,11,13$; `logs/cp_const.log`, agreeing with T4), and for an incomplete block of $p-r_0$ units it is $c_p(r_0)$, which equals $\cos^2(\pi/p)$ for the worst block (two units): $0.25,0.65,0.81,0.92,0.94$. At scale $k\ge2$ the supremum over units $\chi'$ of $\prod_r|\cos(\pi\chi'r!/p^k)|$ tends to $1$ as $k\to\infty$ (take $\chi'=1$: all phases $r!/p^k\to0$). So a bound that takes the supremum over $\chi$ block by block has no contraction at all at deep scales, and even at $k=1$ the worst incomplete block gives only $\cos^2(\pi/p)\to1$. This is the same obstruction as note Corollary 10.20 (sup-type renormalisation cannot give Fourier decay) and the barrier lemma (Theorem 3.10): a proof must use cancellation *across* blocks, i.e. Diophantine independence of the unit parts $\prod(x_0+i)/p^{v}$ at deep $p$-adic scales, which are the digits of Morita's $\Gamma_p$-type products. Averaged bounds are what is needed: $\sum_{\zeta'}|\widehat S(\chi_0+p^{\lambda+d}\zeta')|^2$ rather than $p^D\max|\widehat S|$. **[heuristic]** In a random-phase model ($|\widehat S(\chi)|\approx2^{H/2}$ for typical $\chi$, square-root cancellation over the $p^D$ values of $\zeta'$), the normalised contraction factor of Remark I.1 is $\approx p^{D/2+\lambda}2^{-H/2}$, which is $<1$ for large windows for every $p\ge3$ (as $2^{p-1}>p$); without the $\zeta'$-cancellation it is $\approx p^{D+\lambda}2^{-H/2}$, which needs $2^{p-1}>p^2$, i.e. $p\ge7$; and with the supremum over $\chi$ as well there is no contraction at all. So the induction of Remark I.1 can only close through genuine cancellation in the lifted-frequency sum, which is a statement about the joint distribution of the deep digits of the unit parts of $\pi_j(x_0)/\pi_n(x_0)$; we did not prove it, and it is the same missing input as RMF (note Theorem 10.16).

### 5.2 The "$-1\in A'_x$" route

The task also asked about the sufficient route $\mu\{x:-1\in A'_x\}>0$, $A'_x=\{\sum_{j\ge1}e_j\pi_j(x)\}$. This is a restatement: $-1\in A'_x$ iff $1+\sum_{j\ge1}e_j\pi_j(x)=0$ for some $e$ iff $x\in K_p$ (Proposition 1.2 with $e_0=1$). The natural way to attack it is through the law $\nu_x$ of $\sum_{j\ge1}\varepsilon_j\pi_j(x)$ for fair coins (note Proposition 3.13(c): pure type), via $\mathbb E_x[p^G\nu_x(-1+p^G\mathbb Z_p)]$ and its second moment. The first moment is $\mathbb E Z_G$ of track T4 (up to normalisation) and the second moment is T4's annealed $\mathbb EZ_G^2\ge p^G/4$, which diverges; so this route is the annealed version of ours and is closed by T4's Proposition 2 unless one conditions on the environment, which brings one back to the quenched martingale. We did not pursue it further.

## 6. Numerics [computer-assisted; double precision for the statistics, exact integers for all $p$-adic data]

### 6.1 Programs and validation

- `winvar.c` (new, this instance; 1 core, $\le512$ MB at `maxpop=8e6`). Paths are stored as $(S_e(x)\bmod p^P,\ S'_e(x)\bmod p^P)$ with $p^P<2^{126}$ (`unsigned __int128`), updated additively ($S\mathrel{+}=e_j\pi_j$, $S'\mathrel{+}=e_j\pi'_j$); a path is killed at the first $j$ with $p^{V_{j+1}}\nmid S$. All $p$-adic quantities ($V_n$, $M_n$, $\lambda_e$, $\tau_n\bmod p^{D+\lambda}$, $\theta_e$, $\beta_e$, $q_f$, $u$, $a^{(\lambda)}$) are exact integers; $\Phi$, $\Sigma$, variances and Weyl sums are doubles. **Mode 1** (trajectory): for a Haar-random $x$ (all $P$ digits random, $x\not\equiv-1$ mod $p$) it follows the population along $x$ and, at each window $[n_\ell,n_{\ell+1})$, evaluates on the atom $x+p^{m_\ell}\mathbb Z_p$ the exact affine profile of Proposition C(iii), $\mathbb E_w\Sigma$ (exact from the profiles) against the prediction $2^Hp^{-D}\sum\rho$ (a `WARNING` is printed if they differ by more than $10^{-6}$ relative; none occurred), $\mathrm{Var}_w\Sigma$ (exact by enumerating all $p^D$ digit blocks when $p^D|P|\le2\cdot10^9$, otherwise from $K=256$ random blocks; every window below was exact), the by-order decomposition, $\sum_e\mathrm{Var}_wX_e$, $\kappa$, and the $\rho$-weighted Weyl sums of all parents' phase points at orders $p,p^2,p^3$. **Mode 2** (atom Monte Carlo): fixes an atom $x_0+p^{m_0}\mathbb Z_p$ at $n_0$ and samples the higher digits, recording $\mathbb E M_\ell$, $\mathbb EM_\ell^2$, $\mathbb E(M_\ell-M_{\ell-1})^2$, $\mathbb P(M_\ell=0)$ and the failure frequencies of (W2) (with $L$, and with $\lambda_{\max}$ of the parents actually present), (W3), (ENV).
- `window_exact2.py` = the previous instance's `window_exact.py` plus an explicit-$x$ option and a slope histogram. It shares no code with `winvar.c`: it finds parents by a DFS on targets, finds children by brute force at every $x_w$, and computes everything in exact rationals.
- **Cross-validation** (`logs/r3/python_xcheck.log` vs `logs/r3/xcheck_p*.txt`): on the identical $(x,n,N)$ for $p=3$ ($x=9931185549497379070$, $[22,28)$, $D=4$, 180 parents), $p=5$ ($[24,34)$, 888 and 221 parents) and $p=7$ ($[20,34)$, 84 parents, a window where (W2) fails for $L=1$ but holds for the actual $\lambda_{\max}=0$), the two programs agree to all printed digits in $\mathbb E\Sigma$, $\mathrm{Var}\Sigma$, $\sum_e\mathrm{Var}X_e$, the by-order variances and (where defined in both) the Weyl sums; the slope histogram of all 140 parents of a fourth $x$ ($3{:}72,\ 5{:}12,\ 6{:}56$) also agrees. Python confirmed `firstmoment=True inherit=True const=True affine=True` in all four.
- Determinism: the trajectory batch was run twice (before and after adding two diagnostic columns); the sequences of all relative variances are byte-identical (`md5`).
- `cp_const.py` (previous instance) re-run: $c_3=1/8$, $c_5=0.132377$, $c_7=0.082366$, $c_{11}=0.026681$, $c_{13}=0.003300$, identical to T4; and $\max_{r_0}c_p(r_0)=\cos^2(\pi/p)$ (`logs/r3/cp_const_rerun.log`).

### 6.2 Window relative variances along quenched trajectories (mode 1)

Runs (`logs/r3/traj_p{3,5,7}.log`, total 23 s): $p=3$: $L=4$, windows $24,39,54,69,86$, 14 trajectories, and $L=6$, windows $24,45,66,87$, 6 trajectories (most windows skipped because $p^{D+L}>4\cdot10^7$); $p=5$: $L=2$, windows $20,35,50$ and $L=1$, windows $20,30,40,50$, 12 trajectories each; $p=7$: $L=1$, windows $16,30$ and $L=0$, windows $16,23,30,37$, 12 and 10 trajectories. Trajectories whose population dies ($g_p(x)<\infty$ visible early) or overflows the cap are reported as such. Full tables: `logs/r3/tables.md` (reproduced in §6.4). Aggregates over the windows with a nonempty $P^L$ on which (W2) (with $\lambda_{\max}$), (W3), (ENV) hold:

| $p$ | windows | $\lvert P^L\rvert$ range | $R$ range | $R\cdot\lvert P^L\rvert$ range (median) | $\kappa$ range | $W_1\sqrt{\lvert P^L\rvert}$ range (median) |
|---|---|---|---|---|---|---|
| 3 | 24 | 10 – 89168 | $4\cdot10^{-6}$ – $1.2\cdot10^{-2}$ | 0.04 – 4.3 (0.22) | 0.10 – 2.1 | 0.19 – 3.6 (0.90) |
| 5 | 26 | 68 – 528488 | $2.4\cdot10^{-7}$ – $3.7\cdot10^{-3}$ | 0.0007 – 7.6 (0.20) | 0.02 – 6.3 | 0.25 – 2.6 (1.16) |
| 7 | 16 | 96 – 201780 | $9\cdot10^{-7}$ – $7.6\cdot10^{-3}$ | 0.01 – 1.2 (0.43) | 0.04 – 9.7 | 0.24 – 2.8 (1.00) |

($W_1$ = $\rho$-weighted Weyl sum of all parents' phase points at order $p$, normalised by $\sum\rho$.) Consecutive-window ratios $R_{\ell+1}/R_\ell$ along a trajectory: median $0.14$ ($p=3$), $0.10$ ($p=5$), $0.26$ ($p=7$); 95%, 73%, 71% of the ratios are $<1$; the exceptions are windows whose depth $D$ jumps (a deeper gate inside the window), e.g. the $p=5$ ratio $990$ is $R=2.4\cdot10^{-7}\to9.1\cdot10^{-6}$ across $D=2\to3$, after which $R$ falls again. On windows where a hypothesis fails ($n$ too small for the chosen $L$) $R$ can be much larger ($R\cdot|P|$ up to $96$ at $p=3$, window $[24,39)$, where (W2) fails), as expected: the affine representation is then not guaranteed and the window is not one the martingale would use.

Reading: (i) $R$ decays geometrically along trajectories, at roughly the rate at which $|P^L|$ grows, i.e. $R\cdot|P^L|=O(1)$ (medians $0.2$–$0.4$), which is what independent parents with single-parent relative variance $O(1)$ would give; (ii) the aggregate correlation ratio $\kappa$ stays within $[0.02,10]$ over 66 windows with growing populations, with no trend; (iii) the phase-point Weyl sums decay like $|P^L|^{-1/2}$ ($W_1\sqrt{|P^L|}$ of order $1$ at all population sizes from $10$ to $5\cdot10^5$): square-root cancellation, i.e. the phase points of the parents are as equidistributed as random points. This is the content of hypothesis H'(p) of Theorem J (bounded $\kappa\,r^{\max}$) at the accessible depths; $r^{\max}$ itself was not tabulated separately, but $\sum_e\mathrm{Var}X_e/(\mathbb E\Sigma)^2\cdot|P^L|$ is $R|P^L|/\kappa$, of order $1$ throughout.

### 6.3 Atom Monte Carlo of $\mathbb E[M_\ell^2]$ (mode 2)

Runs (`logs/r3/atom2_p{3,5,7}.log`; 200 or 150 samples of the higher digits per atom; atoms chosen at random by the seed; total 2.5 min): $p=3$, $L=4$, $n_0=33$, windows $33,48,63,78$, four atoms; $p=5$, $L=1$, $n_0=25$, windows $25,35,45$, four atoms, and $L=2$, $n_0=30$, windows $30,45$, two atoms; $p=7$, $L=0$, $n_0=16$, windows $16,23,30,37$, five atoms, and $L=1$, $n_0=20$, windows $20,34$, four atoms. On every atom with $M_{n_0}>0$: $\mathbb EM_\ell$ is constant within statistical error (the martingale identity), $\mathbb E M_\ell^2$ is flat, and the increments $\mathbb E(M_\ell-M_{\ell-1})^2$ decay geometrically. Examples ($\mathbb E M_\ell^2$ along the windows; increments in brackets):
- $p=3$ seed 11: $3.134,\ 3.104,\ 3.110,\ 3.112$ $[1.0\cdot10^{-2},\ 1.6\cdot10^{-3},\ 2.4\cdot10^{-4}]$, $\mathbb E|P|$ from $118$ to $1.3\cdot10^5$; seed 13 (an atom with $M=18.7$, $\mathbb E|P|$ up to $2.2\cdot10^6$): $350.5,\ 350.9,\ 351.1,\ 351.0$ $[9.2\cdot10^{-2},\ 2.4\cdot10^{-2},\ 1.7\cdot10^{-3}]$.
- $p=5$ seed 21: $0.7482,\ 0.7480,\ 0.7480$ $[4.1\cdot10^{-5},\ 3.8\cdot10^{-7}]$, $\mathbb E|P|$ up to $4.9\cdot10^6$; seed 22: $3.1353,\ 3.1449,\ 3.1441$ $[7.8\cdot10^{-4},\ 2.1\cdot10^{-5}]$; $L=2$ seed 25: $13.942,\ 13.942$ $[2.9\cdot10^{-5}]$.
- $p=7$ seed 47 ($L=0$): $0.2771,\ 0.2811,\ 0.2860,\ 0.2861$ $[7.9\cdot10^{-4},\ 6.7\cdot10^{-4},\ 8.0\cdot10^{-6}]$; $L=1$ seeds 34–37: increments $8\cdot10^{-7}$, $4\cdot10^{-5}$, $1.4\cdot10^{-6}$, $2.6\cdot10^{-5}$ on the single window $[20,34)$.
- Hypothesis failures: none at $p=3$ ($n_0=33$) and $p=5$ ($L=1$); at $p=5$, $L=2$, seed 26, (W2) fails on all samples of the window $[30,45)$ (a level-3 gate inside the window makes $D+L>m-M_n$); at $p=7$ the accessible depths ($n\le37$, limited by the population cap $|P|\lesssim8\cdot10^6$ at $p=7$) are too shallow for (W2) with $L=1$ (fails on all samples of $[20,34)$ except the all-slope-0 atom, seed 34, where (W2) with $\lambda_{\max}=0$ holds). Several $p=7$ atoms have $M\equiv0$ (all parents of slope $\ge1$ with $L=0$) or are dead ($g_7<\infty$ on the atom); they are listed in the log and carry no information about (E1).

So, within the accessible range (populations up to a few $10^6$, $n\le86$ at $p=3$, $\le50$ at $p=5$, $\le37$ at $p=7$), the data are consistent with (E1) with $\Lambda$ close to $1+\mathrm{Var}(M_j)/M_j^2$-type constants and with the geometric decay that Theorem J predicts from a bounded $\kappa r^{\max}$. They say nothing about the deep-gate regime ($M_n$ comparable to $m$, windows containing gates of level $\gg\log n$), where the window map's Fourier structure changes (note §10.3–10.5) and which no computation of this kind reaches.

### 6.4 Tables

The complete per-window and per-atom tables generated by `summarize.py` from the logs are in `logs/r3/tables.md` and are appended verbatim at the end of this file (Appendix A).

## 7. Gaps, and what is and is not proved

**Proved here (AI-only, not refereed):** Lemmas A, B, D.0, F; Propositions C, H.3, I; Theorems D, E, H, J; Corollary G; the implication H(p) $\Rightarrow\mu(K_p)>0$ and H'(p) $\Rightarrow\mu(K_p)>0$. All are elementary ($p$-adic Taylor expansion, counting, Parseval, $L^2$ martingale convergence, König) and transcribe or extend note §10.1; the odd-$p$-specific points are: $D\ge\lambda$ from (W1) via Lemma A(c) with $p$ in place of $2$; truncation at $p\lambda$ terms in $a^{(\lambda)}$; the $L^2$ step and the explicit summable factor $(p^{1/(p-1)}/2)^{n_\ell}n_\ell^3$ in Theorem J, which uses $p^{1/(p-1)}<2$.

**Not proved:** H(p) or H'(p) for any $p$; hence Conjecture 5.2 remains open. Specifically:
1. *Decorrelation of parents* ($\kappa$ bounded): equivalent, by Proposition H.3, to square-root cancellation of the phase-point Weyl sums within classes at the frequencies carrying the profile's Fourier mass. Proposition I shows that the next generation's phase points are governed by the window transform $\widehat S$ at frequencies of order $p^{D+\lambda+d}$ and by the parents' targets at that finer precision; Remark I.2 shows that supremum bounds on $\widehat S$ give no contraction (the per-block factor is $\cos^2(\pi/p)$ at worst at scale $p$ and $\to1$ at deep scales). What is needed is cancellation in the lifted-frequency sum $\sum_{\zeta'}$, i.e. equidistribution of the deep digits of the unit parts of $\pi_j(x_0)/\pi_n(x_0)$, the same input as RMF (note Theorem 10.16, Conjecture 10.23) and the barrier lemma. We did not find a way around it.
2. *Single-parent relative variance* $r^{\max}$ bounded: a statement about the fibre fluctuations of the window map $f\mapsto Q_f\bmod p^D$ (its $L^2$ Fourier mass) together with the weights $a_N^{(\lambda)}$. In the random-unit model the budget $\sum_d(1-1/p)(p/2^p)^d$ converges for all $p\ge3$; T4's exact single-block $L^1$ sums match the corresponding $L^1$ budget to $10^{-7}$. Not proved for the actual windows, and in particular not for windows containing deep gates.
3. *Deep gates.* All numerics are at $M_n\le5$ or so. A window containing a gate of level $t$ has $D\ge t$ and a window map whose top $t$ digits come from a single element; Theorem J's hypothesis must hold on such atoms too (they are rare: measure $\approx n p^{-t}$, but the sup in H(p) runs over them). Theorem J only needs $\kappa r^{\max}\le K$ on atoms with $M_n\le3\log_pn$, which still includes gates of level up to $3\log_pn$.
4. *The slope threshold $L$.* The martingale discards parents of slope $>L$. At $p=3$ slopes $3$–$6$ are common (slope histograms in `logs/r3/traj_p3.log`; e.g. $3{:}72,5{:}12,6{:}56$ at $n=22$), so $L$ must be at least $4$–$6$ for the martingale to see most of the population; this costs $p^{D+L}$ memory in the window computation and forces long windows ($H\ge p(L+1)$). None of this affects the theorems, only the numerics' reach. The relation between slopes and the "third halving" phenomenon of note §10.1.2 ($\lambda=2$ absent at $p=2$) was not investigated at odd $p$.
5. *Numerical caveats.* Mode-1 variances are exact enumerations over all $p^D$ digit blocks in every reported window, but in double precision (sums of up to $\sim10^5$ profile values of size $\sim10^3$; relative rounding $\ll10^{-9}$); Mode-2 expectations carry binomial/Monte Carlo errors (150–200 samples: $\mathbb EM^2$ to about $\pm3\%$ relative on the wide atoms, better on narrow ones), so "flat" means flat to that accuracy, and the real evidence is the geometric decay of the exactly computed increments. The hypothesis failure counters in mode 2 use $L$ or $\lambda_{\max}$; the theorems use $L$ (the refinement with $\lambda_{\max}$ in (W2) is valid, since Proposition C(iii)–(iv) only need $D+\lambda_e\le m-M_n$ for the parents present, and $\lambda_{\max}$ is $\mathcal G_\ell$-measurable, but we did not restate the theorems with it).
6. *Not checked:* the Lean project was not used (no small lemma seemed worth it within budget); the previous instance's `l2mc.c` was neither used nor validated.

## 8. Reproduction

All in this directory (`e404r3/T1a-oddp-quenched`); 1 core; macOS/clang; Python 3 with `fractions` only.

```
clang -O2 -o winvar winvar.c -lm
# trajectory mode (exact window statistics):   winvar 1 seed p L P n0 nwin ratio nsamp [maxpop] [K]
./winvar 1 101 3 4 79 24 4 1.25 14 8000000 256     # p=3, L=4  (17 s)
./winvar 1 202 3 6 79 24 3 1.25 6  8000000 256     # p=3, L=6  (2 s; most windows skipped: p^(D+L) > 4e7)
./winvar 1 303 5 2 54 20 2 1.25 12 8000000 256     # p=5, L=2  (3 s)
./winvar 1 404 5 1 54 20 3 1.25 12 8000000 256     # p=5, L=1  (1 s)
./winvar 1 505 7 1 44 16 1 1.25 12 8000000 256     # p=7, L=1  (<1 s)
./winvar 1 606 7 0 44 16 3 1.25 10 8000000 256     # p=7, L=0  (<1 s)
# atom Monte Carlo:   winvar 2 seed p L P n0 nwin ratio nsamp [maxpop]
./winvar 2 11 3 4 79 33 3 1.25 200 8000000         # seeds 11-14 (p=3); 21-24 (p=5, L=1, n0=25); 25-26 (p=5, L=2, n0=30)
./winvar 2 43 7 0 44 16 3 1.25 150 8000000         # seeds 43-47 (p=7, L=0); 34-37 (p=7, L=1, n0=20)
# the two batches: run_batch_r3.sh (traj + first atom runs, 4 min incl. aborted atoms), run_batch_r3b.sh (atom runs, 2.5 min)
# cross-checks against the independent Python brute force (shares no code):
python3 window_exact2.py 3 1 1 22 28 40 1 x=9931185549497379070           # 1.7 s
python3 window_exact2.py 5 1 1 24 34 30 1 x=444893912871598826503         # 33 s
python3 window_exact2.py 5 1 1 24 34 30 1 x=249015097408679049541         # 27 s
python3 window_exact2.py 7 1 1 20 34 30 1 x=20365253102807151669121665    # 55 s
python3 window_exact2.py 3 1 1 22 31 40 2 x=7168108343363332108           # 120 s (slope histogram 3:72 5:12 6:56)
python3 summarize.py > logs/r3/tables.md
python3 cp_const.py 3 5 7 11 13
```
Logs: `logs/r3/` (this instance; `old_prelim/` holds the first, byte-identical trajectory run), `logs/` (previous instance's exact-rational window checks and `cp_const.log`). The previous instance's files were not deleted or modified (`window_exact2.py` is a copy with two additions). Peak memory: `winvar` preallocates two path buffers of `maxpop` entries (32 bytes each), so every run with `maxpop=8e6` has a resident set of about 850 MB (measured 854 MB at $p=5$, $n=45$, $|P|\approx5\cdot10^6$, `/usr/bin/time -l`); all runs $<1$ GB and $<1$ min each.

## 9. Credit

- The quenched-martingale construction, the atom filtration, frozen-state weights and the one-window identity are track R1b's (note §10.1, $p=2$; lead's rewrite), transferred here to odd $p$ as note §10.1.3 anticipated. The window hypotheses (W1)–(W3) and the proof pattern of Proposition C follow note Proposition 10.6 line by line, with $2\to p$.
- The $L^2$/second-moment template is classical: Kesten–Stigum (1966), the size-biased proof of Lyons–Pemantle–Peres (1995), and for random environments Tanny (1988) and Kersting–Vatutin (2017) (gate list (a)); none of their theorems is used, only the strategy "bounded second moment $\Rightarrow$ positive probability of a nonzero limit".
- The obstruction analysis (sup-type bounds cannot contract) restates note Corollary 10.20 and the barrier lemma (Theorem 3.10, track C) in the language of Proposition I; the constants $c_p$ are T4's (and the previous instance's `cp_const.py`, whose log we re-verified).
- T4's annealed divergence $\mathbb EZ_G^2\ge p^G/4$ (Proposition 2 of T4) is what motivates the quenched formulation of §4; §5.2 uses it to close the "$-1\in A'_x$" route.
- Prior external work: S. Lin (1960), V. Kovač (2025), T. Tao (2025), K. Kitamura (July 2026) as listed in note §2; nothing in this writeup overlaps with their results (none of them treats measure statements at odd $p$). No new external work on #404 was found by the gate on 2026-10-20.
- The exact-rational window checker `window_exact.py` and `cp_const.py` are the previous instance's (2026-10-12); their logs were reused as described in Remark C.1 and §6.1.

## Appendix A. Tables (generated by summarize.py from logs/r3/)

**p = 3** (trajectory mode; columns: L, sample, window [n,N), D, hypotheses W1W2W3ENV and W2' (with lambda_max), |P^L| (parents with slope <= L), M_l, relative variance R, R*|P^L|, kappa, rho-weighted Weyl sums of phase points at orders p,p^2,p^3 and W_1*sqrt(|P^L|)):

| L | x# | [n,N) | D | hyp | W2' | lam_max | \|P^L\| | M_l | R | R·\|P^L\| | κ | Weyl p/p²/p³ | W₁√\|P^L\| | exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 1 | [24,39) | 7 | 1011 | 0 | 4 | 28 | 2.245 | 0.011 | 0.31 | 0.93 | 0.291/0.287/0.462 | 1.54 | 1/0 |
| 3 | 1 | [39,54) | 7 | 1111 | 1 | 4 | 410 | 2.612 | 0.00113 | 0.46 | 0.71 | 0.032/0.067/0.077 | 0.65 | 1/0 |
| 3 | 1 | [54,69) | 7 | 1111 | 1 | 4 | 6018 | 2.524 | 3.17e-05 | 0.19 | 0.93 | 0.046/0.011/0.052 | 3.57 | 1/0 |
| 3 | 1 | [69,86) | 9 | 1111 | 1 | 4 | 89168 | 2.519 | 9.41e-06 | 0.84 | 0.52 | 0.003/0.007/0.012 | 0.90 | 1/0 |
| 3 | 2 | [24,39) | 9 | 1011 | 0 | 0 | 43 | 0.1513 | 0.355 | 15 | 0.96 | 0.023/0.303/0.237 | 0.15 | 1/0 |
| 3 | 2 | [39,54) | 8 | 1111 | 1 | 0 | 33 | 0.06977 | 0.0123 | 0.41 | 1.1 | 0.139/0.190/0.286 | 0.80 | 1/0 |
| 3 | 2 | [54,69) | 6 | 1111 | 1 | 0 | 183 | 0.07746 | 0.0006 | 0.11 | 0.93 | 0.077/0.111/0.163 | 1.04 | 1/0 |
| 3 | 2 | [69,86) | 8 | 1111 | 1 | 0 | 8006 | 0.0754 | 0.000182 | 1.5 | 1.3 | 0.004/0.019/0.018 | 0.36 | 1/0 |
| 3 | 3 | [24,39) | 9 | 1011 | 0 | 4 | 76 | 2.375 | 0.0196 | 1.5 | 1.1 | 0.251/0.144/0.270 | 2.19 | 1/0 |
| 3 | 3 | [39,54) | 6 | 1111 | 1 | 4 | 108 | 2.077 | 0.000389 | 0.042 | 0.34 | 0.101/0.187/0.157 | 1.05 | 1/0 |
| 3 | 3 | [54,69) | 8 | 1111 | 1 | 4 | 4896 | 2.08 | 0.000104 | 0.51 | 0.72 | 0.010/0.027/0.050 | 0.70 | 1/0 |
| 3 | 3 | [69,86) | 8 | 1111 | 1 | 4 | 24390 | 2.063 | 5.29e-06 | 0.13 | 1.7 | 0.006/0.012/0.011 | 0.94 | 1/0 |
| 3 | 5 | [24,39) | 10 | 1011 | 0 | 4 | 388 | 1.415 | 0.246 | 96 | 1 | 0.080/0.304/0.233 | 1.58 | 1/0 |
| 3 | 5 | [39,54) | 8 | 1111 | 1 | 4 | 310 | 2.032 | 0.000794 | 0.25 | 0.41 | 0.075/0.079/0.116 | 1.32 | 1/0 |
| 3 | 5 | [54,69) | 6 | 1111 | 1 | 4 | 1638 | 2.067 | 0.000119 | 0.19 | 2.1 | 0.006/0.046/0.025 | 0.24 | 1/0 |
| 3 | 5 | [69,86) | 9 | 1111 | 1 | 4 | 72586 | 2.052 | 1.67e-05 | 1.2 | 0.45 | 0.005/0.008/0.007 | 1.35 | 1/0 |
| 3 | 11 | [24,39) | 8 | 1011 | 0 | 2 | 96 | 1.259 | 0.00492 | 0.47 | 0.7 | 0.075/0.146/0.258 | 0.73 | 1/0 |
| 3 | 11 | [39,54) | 7 | 1111 | 1 | 2 | 608 | 1.288 | 9.74e-05 | 0.059 | 0.095 | 0.016/0.085/0.086 | 0.39 | 1/0 |
| 3 | 11 | [54,69) | 8 | 1111 | 1 | 2 | 9210 | 1.295 | 0.000466 | 4.3 | 0.8 | 0.010/0.011/0.012 | 0.96 | 1/0 |
| 3 | 11 | [69,86) | 8 | 1111 | 1 | 2 | 45068 | 1.264 | 4.04e-06 | 0.18 | 0.64 | 0.004/0.012/0.018 | 0.85 | 1/0 |
| 3 | 12 | [24,39) | 7 | 1011 | 0 | 4 | 14 | 0.6715 | 0.00447 | 0.063 | 0.44 | 0.692/0.518/0.604 | 2.59 | 1/0 |
| 3 | 12 | [39,54) | 8 | 1111 | 1 | 4 | 326 | 0.6689 | 0.000677 | 0.22 | 0.73 | 0.191/0.148/0.184 | 3.45 | 1/0 |
| 3 | 12 | [54,69) | 6 | 1111 | 1 | 4 | 1504 | 0.6347 | 0.00011 | 0.17 | 0.76 | 0.018/0.074/0.048 | 0.70 | 1/0 |
| 3 | 12 | [69,86) | 9 | 1111 | 1 | 4 | 67656 | 0.6374 | 7.33e-06 | 0.5 | 1.3 | 0.010/0.019/0.023 | 2.60 | 1/0 |
| 3 | 13 | [24,39) | 6 | 1011 | 1 | 0 | 10 | 0.3168 | 0.00949 | 0.095 | 0.91 | 0.200/0.576/0.808 | 0.63 | 1/0 |
| 3 | 13 | [39,54) | 8 | 1111 | 1 | 0 | 480 | 0.3383 | 0.00443 | 2.1 | 0.5 | 0.013/0.039/0.077 | 0.28 | 1/0 |
| 3 | 13 | [54,69) | 9 | 1111 | 1 | 0 | 2313 | 0.3264 | 0.000709 | 1.6 | 1.6 | 0.023/0.024/0.054 | 1.11 | 1/0 |
| 3 | 13 | [69,86) | 6 | 1111 | 1 | 0 | 3690 | 0.3128 | 4.1e-05 | 0.15 | 1 | 0.032/0.015/0.030 | 1.94 | 1/0 |
| 3 | 3 | [45,66) | 9 | 1111 | 1 | 0 | 376 | 0.3354 | 0.000348 | 0.13 | 0.43 | 0.032/0.112/0.082 | 0.62 | 1/0 |
| 3 | 4 | [45,66) | 9 | 1111 | 1 | 0 | 542 | 0.4834 | 0.000148 | 0.08 | 0.25 | 0.008/0.117/0.064 | 0.19 | 1/0 |

**p = 5** (trajectory mode; columns: L, sample, window [n,N), D, hypotheses W1W2W3ENV and W2' (with lambda_max), |P^L| (parents with slope <= L), M_l, relative variance R, R*|P^L|, kappa, rho-weighted Weyl sums of phase points at orders p,p^2,p^3 and W_1*sqrt(|P^L|)):

| L | x# | [n,N) | D | hyp | W2' | lam_max | \|P^L\| | M_l | R | R·\|P^L\| | κ | Weyl p/p²/p³ | W₁√\|P^L\| | exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 0 | [20,35) | 4 | 1001 | 0 | 2 | 2256 | 1.344 | 0.00136 | 3.1 | 0.59 | 0.010/0.067/0.094 | 0.47 | 1/0 |
| 5 | 0 | [35,50) | 4 | 1111 | 1 | 2 | 111848 | 1.271 | 1.5e-06 | 0.17 | 0.54 | 0.002/0.006/0.009 | 0.67 | 1/0 |
| 5 | 3 | [20,35) | 3 | 1011 | 0 | 1 | 99 | 0.2793 | 0.00031 | 0.031 | 1.2 | 0.098/0.208/0.234 | 0.98 | 1/0 |
| 5 | 3 | [35,50) | 4 | 1111 | 1 | 1 | 23907 | 0.2717 | 7.9e-06 | 0.19 | 0.19 | 0.003/0.005/0.011 | 0.46 | 1/0 |
| 5 | 5 | [20,35) | 4 | 1011 | 0 | 2 | 1248 | 3.7 | 0.000296 | 0.37 | 0.31 | 0.052/0.083/0.085 | 1.84 | 1/0 |
| 5 | 5 | [35,50) | 3 | 1111 | 1 | 2 | 64496 | 3.666 | 2.8e-07 | 0.018 | 0.49 | 0.009/0.004/0.011 | 2.29 | 1/0 |
| 5 | 7 | [20,35) | 4 | 1001 | 0 | 0 | 464 | 0.2766 | 0.0011 | 0.51 | 0.35 | 0.038/0.062/0.093 | 0.82 | 1/0 |
| 5 | 7 | [35,50) | 4 | 1111 | 1 | 0 | 23446 | 0.2666 | 4.47e-06 | 0.1 | 0.76 | 0.004/0.011/0.016 | 0.61 | 1/0 |
| 5 | 9 | [20,35) | 3 | 1011 | 1 | 0 | 120 | 0.3576 | 0.00188 | 0.23 | 2.8 | 0.119/0.269/0.255 | 1.30 | 1/0 |
| 5 | 9 | [35,50) | 6 | 1011 | 1 | 0 | 31750 | 0.361 | 0.000239 | 7.6 | 0.86 | 0.009/0.008/0.010 | 1.60 | 1/0 |
| 5 | 1 | [20,30) | 2 | 1111 | 1 | 1 | 88 | 0.2611 | 0.000305 | 0.027 | 0.56 | 0.102/0.169/0.000 | 0.96 | 1/0 |
| 5 | 1 | [30,40) | 2 | 1111 | 1 | 1 | 3673 | 0.2674 | 5.97e-07 | 0.0022 | 0.066 | 0.009/0.029/0.000 | 0.55 | 1/0 |
| 5 | 1 | [40,50) | 3 | 1111 | 1 | 1 | 150567 | 0.2675 | 3.72e-06 | 0.56 | 0.58 | 0.003/0.005/0.006 | 1.16 | 1/0 |
| 5 | 2 | [20,30) | 2 | 1111 | 1 | 0 | 104 | 0.3099 | 0.00368 | 0.38 | 6.3 | 0.258/0.292/0.000 | 2.63 | 1/0 |
| 5 | 2 | [30,40) | 4 | 1111 | 1 | 0 | 4008 | 0.2916 | 0.000379 | 1.5 | 0.83 | 0.031/0.033/0.046 | 1.96 | 1/0 |
| 5 | 2 | [40,50) | 2 | 1111 | 1 | 0 | 6612 | 0.2936 | 4.26e-05 | 0.28 | 3.6 | 0.024/0.025/0.000 | 1.95 | 1/0 |
| 5 | 5 | [20,30) | 2 | 1111 | 1 | 1 | 87 | 0.2569 | 0.000458 | 0.04 | 0.8 | 0.072/0.137/0.000 | 0.67 | 1/0 |
| 5 | 5 | [30,40) | 2 | 1111 | 1 | 1 | 3516 | 0.2557 | 2.74e-06 | 0.0096 | 0.28 | 0.022/0.029/0.000 | 1.30 | 1/0 |
| 5 | 5 | [40,50) | 3 | 1111 | 1 | 1 | 143927 | 0.2557 | 1.37e-06 | 0.2 | 0.2 | 0.001/0.005/0.006 | 0.38 | 1/0 |
| 5 | 7 | [20,30) | 3 | 1011 | 0 | 1 | 1536 | 0.9142 | 0.00256 | 3.9 | 0.5 | 0.024/0.061/0.069 | 0.94 | 1/0 |
| 5 | 7 | [30,40) | 2 | 1111 | 1 | 1 | 13096 | 0.9393 | 5.95e-07 | 0.0078 | 0.14 | 0.009/0.026/0.000 | 1.03 | 1/0 |
| 5 | 7 | [40,50) | 3 | 1111 | 1 | 1 | 528488 | 0.9391 | 4.87e-07 | 0.26 | 0.21 | 0.002/0.003/0.005 | 1.45 | 1/0 |
| 5 | 8 | [20,30) | 2 | 1111 | 1 | 0 | 76 | 0.2265 | 0.00359 | 0.27 | 4.5 | 0.257/0.238/0.000 | 2.24 | 1/0 |
| 5 | 8 | [30,40) | 3 | 1111 | 1 | 0 | 2824 | 0.2055 | 0.000149 | 0.42 | 0.7 | 0.005/0.022/0.043 | 0.27 | 1/0 |
| 5 | 8 | [40,50) | 2 | 1111 | 1 | 0 | 23664 | 0.2102 | 2.51e-06 | 0.059 | 0.76 | 0.006/0.016/0.000 | 0.92 | 1/0 |
| 5 | 9 | [20,30) | 2 | 1111 | 1 | 1 | 68 | 0.207 | 0.000546 | 0.037 | 0.81 | 0.130/0.229/0.000 | 1.07 | 1/0 |
| 5 | 9 | [30,40) | 2 | 1111 | 1 | 1 | 2916 | 0.2121 | 2.41e-07 | 0.0007 | 0.023 | 0.026/0.019/0.000 | 1.40 | 1/0 |
| 5 | 9 | [40,50) | 3 | 1111 | 1 | 1 | 119418 | 0.2121 | 9.07e-06 | 1.1 | 1.1 | 0.002/0.004/0.006 | 0.69 | 1/0 |
| 5 | 11 | [20,30) | 2 | 1111 | 1 | 0 | 96 | 0.2861 | 0.000927 | 0.089 | 1.4 | 0.129/0.431/0.000 | 1.26 | 1/0 |
| 5 | 11 | [30,40) | 3 | 1111 | 1 | 0 | 3948 | 0.2873 | 0.000528 | 2.1 | 1.5 | 0.004/0.025/0.058 | 0.25 | 1/0 |
| 5 | 11 | [40,50) | 2 | 1111 | 1 | 0 | 31652 | 0.2811 | 8.75e-06 | 0.28 | 4.6 | 0.013/0.009/0.000 | 2.31 | 1/0 |

**p = 7** (trajectory mode; columns: L, sample, window [n,N), D, hypotheses W1W2W3ENV and W2' (with lambda_max), |P^L| (parents with slope <= L), M_l, relative variance R, R*|P^L|, kappa, rho-weighted Weyl sums of phase points at orders p,p^2,p^3 and W_1*sqrt(|P^L|)):

| L | x# | [n,N) | D | hyp | W2' | lam_max | \|P^L\| | M_l | R | R·\|P^L\| | κ | Weyl p/p²/p³ | W₁√\|P^L\| | exact |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 0 | [16,30) | 4 | 1000 | 0 | 1 | 242 | 1.264 | 0.000507 | 0.12 | 1 | 0.035/0.120/0.136 | 0.54 | 1/0 |
| 7 | 1 | [16,30) | 2 | 1001 | 0 | 0 | 640 | 0.4785 | 0.000279 | 0.18 | 0.11 | 0.014/0.075/0.000 | 0.35 | 1/0 |
| 7 | 2 | [16,30) | 2 | 1011 | 0 | 1 | 250 | 1.313 | 2.5e-06 | 0.00063 | 0.37 | 0.068/0.103/0.000 | 1.08 | 1/0 |
| 7 | 4 | [16,30) | 4 | 1000 | 0 | 0 | 704 | 0.5264 | 0.00937 | 6.6 | 1.1 | 0.047/0.123/0.086 | 1.25 | 1/0 |
| 7 | 5 | [16,30) | 2 | 1001 | 0 | 0 | 352 | 0.2632 | 1.69e-05 | 0.006 | 0.018 | 0.005/0.088/0.000 | 0.09 | 1/0 |
| 7 | 7 | [16,30) | 2 | 1011 | 0 | 1 | 233 | 1.214 | 1.82e-07 | 4.2e-05 | 0.37 | 0.047/0.112/0.000 | 0.72 | 1/0 |
| 7 | 8 | [16,30) | 2 | 1001 | 0 | 0 | 76 | 0.3978 | 0.000586 | 0.045 | 1.6 | 0.201/0.262/0.000 | 1.75 | 1/0 |
| 7 | 9 | [16,30) | 2 | 1001 | 0 | 0 | 352 | 0.2632 | 2.14e-05 | 0.0075 | 0.023 | 0.005/0.088/0.000 | 0.09 | 1/0 |
| 7 | 0 | [16,23) | 2 | 1000 | 0 | 0 | 552 | 0.4127 | 0.00386 | 2.1 | 0.59 | 0.049/0.091/0.000 | 1.15 | 1/0 |
| 7 | 0 | [23,30) | 1 | 1111 | 1 | 0 | 1384 | 0.3961 | 0.000104 | 0.14 | 0.97 | 0.032/0.000/0.000 | 1.19 | 1/0 |
| 7 | 0 | [30,37) | 1 | 1111 | 1 | 0 | 25080 | 0.3926 | 9.55e-07 | 0.024 | 0.16 | 0.004/0.000/0.000 | 0.63 | 1/0 |
| 7 | 2 | [16,23) | 1 | 1111 | 1 | 0 | 272 | 0.2034 | 0.000557 | 0.15 | 0.48 | 0.092/0.000/0.000 | 1.52 | 1/0 |
| 7 | 2 | [23,30) | 2 | 1111 | 1 | 0 | 4832 | 0.1976 | 0.000111 | 0.54 | 0.066 | 0.018/0.013/0.000 | 1.25 | 1/0 |
| 7 | 2 | [30,37) | 1 | 1111 | 1 | 0 | 12432 | 0.1946 | 9.24e-07 | 0.011 | 0.037 | 0.003/0.000/0.000 | 0.33 | 1/0 |
| 7 | 4 | [16,23) | 2 | 1000 | 0 | 0 | 640 | 0.4785 | 0.0119 | 7.6 | 0.44 | 0.033/0.043/0.000 | 0.83 | 1/0 |
| 7 | 4 | [23,30) | 1 | 1111 | 1 | 0 | 1568 | 0.4488 | 5.02e-05 | 0.079 | 0.048 | 0.006/0.000/0.000 | 0.24 | 1/0 |
| 7 | 4 | [30,37) | 1 | 1111 | 1 | 0 | 28864 | 0.4518 | 1.48e-05 | 0.43 | 0.26 | 0.003/0.000/0.000 | 0.51 | 1/0 |
| 7 | 5 | [16,23) | 1 | 1111 | 1 | 0 | 600 | 0.4486 | 2.7e-05 | 0.016 | 0.64 | 0.025/0.000/0.000 | 0.61 | 1/0 |
| 7 | 5 | [23,30) | 1 | 1111 | 1 | 0 | 10976 | 0.4488 | 2.25e-05 | 0.25 | 9.7 | 0.023/0.000/0.000 | 2.41 | 1/0 |
| 7 | 5 | [30,37) | 2 | 1111 | 1 | 0 | 201780 | 0.4512 | 5.94e-06 | 1.2 | 0.71 | 0.004/0.004/0.000 | 1.80 | 1/0 |
| 7 | 6 | [16,23) | 1 | 1111 | 1 | 0 | 96 | 0.5024 | 0.00764 | 0.73 | 0.45 | 0.076/0.000/0.000 | 0.74 | 1/0 |
| 7 | 6 | [23,30) | 1 | 1111 | 1 | 0 | 1696 | 0.4854 | 0.000504 | 0.86 | 0.53 | 0.019/0.000/0.000 | 0.78 | 1/0 |
| 7 | 6 | [30,37) | 1 | 1111 | 1 | 0 | 30272 | 0.4738 | 3.62e-05 | 1.1 | 0.67 | 0.005/0.000/0.000 | 0.87 | 1/0 |
| 7 | 7 | [16,23) | 1 | 1111 | 1 | 0 | 272 | 0.2034 | 0.000557 | 0.15 | 0.48 | 0.092/0.000/0.000 | 1.52 | 1/0 |
| 7 | 7 | [23,30) | 2 | 1111 | 1 | 0 | 5072 | 0.2074 | 0.000137 | 0.7 | 0.085 | 0.014/0.019/0.000 | 1.00 | 1/0 |
| 7 | 7 | [30,37) | 1 | 1111 | 1 | 0 | 13440 | 0.2104 | 3.64e-05 | 0.49 | 1.6 | 0.024/0.000/0.000 | 2.78 | 1/0 |


### Atom Monte Carlo (mode 2): E[M_l], E[M_l^2] over the digits above the atom


`logs/r3/atom2_p3.log` seed 2: p=11, L=3, n0=79, atom: x0 mod p^17 = 116146048 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 33 | 118.0 | 1.77024 | 3.13375 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 48 | 1753.7 | 1.75897 | 3.10401 | 0.01004 | 1.01698e-02 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 63 | 26284.4 | 1.76007 | 3.11014 | 0.01231 | 1.60152e-03 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 78 | 131300.7 | 1.76058 | 3.11243 | 0.01280 | 2.39262e-04 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p3.log` seed 2: p=12, L=3, n0=79, atom: x0 mod p^16 = 10275804 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 33 | 106.0 | 0.53120 | 0.28217 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 48 | 523.4 | 0.52515 | 0.27818 | 0.00239 | 2.42598e-03 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 63 | 7850.1 | 0.52571 | 0.27878 | 0.00242 | 1.11116e-04 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 78 | 117623.1 | 0.52573 | 0.27882 | 0.00243 | 9.41265e-06 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p3.log` seed 2: p=13, L=3, n0=79, atom: x0 mod p^18 = 30987925 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 33 | 674.0 | 18.72284 | 350.54456 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 48 | 9865.9 | 18.73051 | 350.92416 | 0.09202 | 9.20801e-02 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 63 | 147528.6 | 18.73597 | 351.14154 | 0.10507 | 2.38842e-02 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 78 | 2210413.6 | 18.73254 | 351.01110 | 0.10311 | 1.65354e-03 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p3.log` seed 2: p=14, L=3, n0=79, atom: x0 mod p^16 = 13633846 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 33 | 424.0 | 1.66471 | 2.77126 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 48 | 2106.1 | 1.66617 | 2.77966 | 0.00353 | 3.52830e-03 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 63 | 94702.0 | 1.66722 | 2.78320 | 0.00357 | 8.83451e-05 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 78 | 157773.0 | 1.66762 | 2.78478 | 0.00381 | 2.24100e-04 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=21, L=5, n0=54, atom: x0 mod p^6 = 6828 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 25 | 3008.0 | 0.86497 | 0.74817 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 35 | 120051.0 | 0.86484 | 0.74799 | 0.00004 | 4.10508e-05 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 45 | 4917263.3 | 0.86486 | 0.74802 | 0.00004 | 3.75282e-07 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=22, L=5, n0=54, atom: x0 mod p^6 = 3818 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 25 | 5712.0 | 1.77068 | 3.13530 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 35 | 46697.2 | 1.77318 | 3.14494 | 0.00077 | 7.79630e-04 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 45 | 1913395.0 | 1.77293 | 3.14410 | 0.00082 | 2.14034e-05 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=23, L=5, n0=54, atom: x0 mod p^6 = 11330 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 25 | 588.0 | 0.23392 | 0.05472 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 35 | 24229.2 | 0.23393 | 0.05473 | 0.00000 | 2.44308e-06 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 45 | 39650.2 | 0.23379 | 0.05466 | 0.00000 | 2.07682e-06 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=24, L=5, n0=54, atom: x0 mod p^6 = 10650 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 25 | 681.0 | 0.31662 | 0.10025 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 35 | 27844.5 | 0.31655 | 0.10021 | 0.00000 | 2.94443e-06 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 45 | 1140348.2 | 0.31651 | 0.10018 | 0.00000 | 1.00241e-07 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=25, L=5, n0=54, atom: x0 mod p^8 = 33523 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 30 | 17760.0 | 3.73390 | 13.94202 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 45 | 4649842.2 | 3.73393 | 13.94223 | 0.00003 | 2.88305e-05 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p5.log` seed 2: p=26, L=5, n0=54, atom: x0 mod p^7 = 72563 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 30 | 5568.0 | 0.40749 | 0.16605 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 45 | 293773.5 | 0.40768 | 0.16622 | 0.00002 | 1.85986e-05 | 0.0000 | 1.0000 | 1.0000 |

`logs/r3/atom2_p7.log` seed 2: p=43, L=7, n0=44, atom: x0 mod p^2 = 23 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 272.0 | 0.20337 | 0.04136 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 23 | 4983.6 | 0.20377 | 0.04155 | 0.00002 | 2.22173e-05 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 30 | 11340.9 | 0.20245 | 0.04111 | 0.00012 | 1.03893e-04 | 0.0000 | 0.1467 | 0.1467 |
| 3 | 37 | 207453.3 | 0.20238 | 0.04106 | 0.00011 | 3.62245e-06 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=44, L=7, n0=44, atom: x0 mod p^5 = 12689 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 304.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 1 | 23 | 5565.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 2 | 30 | 101778.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 3 | 37 | 1861364.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=45, L=7, n0=44, atom: x0 mod p^3 = 192 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 0.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 1 | 23 | 0.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 2 | 30 | 0.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 3 | 37 | 0.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=46, L=7, n0=44, atom: x0 mod p^3 = 26 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 320.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 1 | 23 | 863.2 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 2 | 30 | 15766.7 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |
| 3 | 37 | 288280.0 | 0.00000 | 0.00000 | 0.00000 | 0.00000e+00 | 1.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=47, L=7, n0=44, atom: x0 mod p^2 = 24 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 704.0 | 0.52637 | 0.27706 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 23 | 12948.1 | 0.52943 | 0.28108 | 0.00078 | 7.92746e-04 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 30 | 30416.0 | 0.53360 | 0.28600 | 0.00127 | 6.73016e-04 | 0.0000 | 0.1267 | 0.1267 |
| 3 | 37 | 556241.5 | 0.53372 | 0.28610 | 0.00125 | 7.98696e-06 | 0.0000 | 0.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=34, L=7, n0=44, atom: x0 mod p^3 = 246 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 1287.0 | 0.42099 | 0.17723 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 34 | 430306.3 | 0.42097 | 0.17721 | 0.00000 | 8.00897e-07 | 0.0000 | 1.0000 | 0.0000 |

`logs/r3/atom2_p7.log` seed 2: p=35, L=7, n0=44, atom: x0 mod p^3 = 22 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 1323.0 | 0.43277 | 0.18729 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 34 | 63318.2 | 0.43361 | 0.18806 | 0.00004 | 4.02618e-05 | 0.0000 | 1.0000 | 1.0000 |

`logs/r3/atom2_p7.log` seed 2: p=36, L=7, n0=44, atom: x0 mod p^3 = 250 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 4832.0 | 1.21844 | 1.48461 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 34 | 1617461.5 | 1.21840 | 1.48451 | 0.00000 | 1.43973e-06 | 0.0000 | 1.0000 | 1.0000 |

`logs/r3/atom2_p7.log` seed 2: p=37, L=7, n0=44, atom: x0 mod p^3 = 215 (low 64 bits), samples=150 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 4976.0 | 1.25880 | 1.58458 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 34 | 236480.0 | 1.25806 | 1.58275 | 0.00003 | 2.61206e-05 | 0.0000 | 1.0000 | 1.0000 |

`logs/r3/atom_p3.log` seed 2: p=11, L=3, n0=79, atom: x0 mod p^13 = 1354792 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 24 | 18.0 | 1.63925 | 2.68714 | -0.00000 | 0.00000e+00 | 0.0000 | 0.0000 |  |
| 1 | 39 | 768.0 | 1.62406 | 2.66746 | 0.02987 | 3.01040e-02 | 0.0000 | 1.0000 |  |
| 2 | 54 | 3834.7 | 1.62301 | 2.67650 | 0.04234 | 1.26127e-02 | 0.0000 | 0.0000 |  |
| 3 | 69 | 19173.0 | 1.62494 | 2.68264 | 0.04222 | 3.04645e-04 | 0.0000 | 0.0000 |  |
| 4 | 86 | 383019.7 | 1.62505 | 2.68301 | 0.04224 | 1.15878e-05 | 0.0000 | 0.0000 |  |

`logs/r3/atom_p3.log` seed 2: p=12, L=3, n0=79, atom: x0 mod p^12 = 178425 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 24 | 21.0 | 0.66520 | 0.44250 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 |  |
| 1 | 39 | 310.1 | 0.65552 | 0.44899 | 0.01928 | 1.93754e-02 | 0.0000 | 1.0000 |  |
| 2 | 54 | 1546.8 | 0.65478 | 0.45059 | 0.02186 | 1.41323e-03 | 0.0000 | 0.0000 |  |
| 3 | 69 | 69480.4 | 0.65433 | 0.44995 | 0.02181 | 3.24909e-05 | 0.0000 | 0.0000 |  |
| 4 | 86 | 1387469.5 | 0.65406 | 0.44958 | 0.02179 | 1.00724e-05 | 0.0000 | 0.0000 |  |

`logs/r3/atom_p3.log` seed 2: p=13 L=3 n0=79: **no completed samples** (population cap exceeded on this atom at the last window).

`logs/r3/atom_p5.log` seed 2: p=21 L=5 n0=54: **no completed samples** (population cap exceeded on this atom at the last window).

`logs/r3/atom_p5.log` seed 2: p=22 L=5 n0=54: **no completed samples** (population cap exceeded on this atom at the last window).

`logs/r3/atom_p5.log` seed 2: p=23, L=5, n0=54, atom: x0 mod p^5 = 1955 (low 64 bits), samples=200 aborts=0

| l | n | E\|P\| | E[M] | E[M²] | Var M | E[(M_l−M_{l−1})²] | P(M=0) | fail(W2 with L) | fail(W2 with λ_max) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 93.0 | 0.26846 | 0.07207 | 0.00000 | 0.00000e+00 | 0.0000 | 0.0000 |  |
| 1 | 35 | 24466.8 | 0.26897 | 0.07242 | 0.00007 | 7.06691e-05 | 0.0000 | 1.0000 |  |
| 2 | 50 | 256397.4 | 0.26892 | 0.07239 | 0.00007 | 2.32855e-06 | 0.0000 | 1.0000 |  |
