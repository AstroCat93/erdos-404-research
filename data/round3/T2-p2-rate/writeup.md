# Track T2 (round 3, 2026-10-21): an explicit decay rate for $\delta_G(2)$ off the shadow of $-2$, and the $1/G$ law

*AI-generated (Claude), not human-refereed. Nathan Durfee (composer/prompter) has not verified any mathematics. Every claim carries one label: **[proved]** (complete proof in this file), **[computer-assisted]**, **[heuristic]**, **[conjecture]**, **[sketch]**. The work directory was empty at the start of this round (the earlier instances left no files), so everything here was derived afresh.*

Work directory: `e404r3/T2-p2-rate/` (code in `code/`, logs in `logs/`). Core cap 1; every run below took < 4 minutes and < 200 MB.

## 0. Summary

**Rigorous (new).** Let $\mu$ be Haar measure on $\mathbb Z_2$ and $R:=\mathbb Z_2\setminus(14+16\mathbb Z_2)$ (all $2$-adic integers except the "deep shadow" $v_2(x+2)\ge4$ of $-2$).

> **Corollaries 5.4–5.5 [proved].** For all $G\ge4$,
> $$\mu\{x\in R:\ g_2(x)\ge G\}\ \le\ C\,G^{-0.227}$$
> with an explicit constant $C$ (§5; $C\le 2\cdot10^5$, and on the sub-class $8\mathbb Z_2$ one may take $C=29$). Equivalently (Corollary 5.5), the natural density of $\{a\ge1:\ a\not\equiv14\ (\mathrm{mod}\ 16),\ f(a,2)\ge v_2(a!)+G\}$ is at most $C\,G^{-0.227}$.

The exponent is $\alpha^*=0.22709\ldots$, the root of $\alpha=1-H_2(\alpha)$ ($H_2$ the binary entropy); any $\alpha<\alpha^*$ works, and $0.227$ is used for definiteness. This is the first explicit rate for $p=2$ on a set of positive measure; Theorem 10.1 of the note gives no rate. It does **not** give a rate for $\delta_G(2)$ itself, because the class $14+16\mathbb Z_2$ (measure $1/16$) is excluded, and numerically that class carries most of the survivors at large $G$ (about $62\%$ of them at $G=128$ and $64\%$ at $G=512$, §6.3).

The proof has four ingredients, three of them new to this project:
1. **Taylor certificates** (§2): evaluating $S_e$ (or a renormalised version of it) at a negative integer $-m$ and expanding around $x$ gives, for every alive path, an upper bound on its slope $\lambda_e=v(S_e'(x))$. On $8\mathbb Z_2$ every alive path has slope $\le1$; on $2+8\mathbb Z_2$ slope $\le3$; on $6+16\mathbb Z_2$ slope $\le6$. This removes the slope cut-off $L$, the steep paths and the multiplicity $\ge2$ case of Theorem 10.1 on these classes.
2. **A Hensel first-moment bound** (§3): $\int_{8\mathbb Z_2}2^{-W_n}|P_n|\,d\mu\le1$ for every $n\ge6$ (and analogues on the other classes). This replaces the a-priori control of the martingale's initial value, with no exceptional set.
3. The **exact window martingale** of note §10.1 (Prop. 10.6, track R1b; re-proved in §4).
4. A **predictable-barrier stopping argument** (§5): because the environment walk $W$ is predictable, $\mathbb P(\text{survive past the window ending at }N\mid\mathcal F)\le2^{W_N}M$, so one optional-stopping step at the first time $W\le-c$ costs only $2^{-c}$, without the $2^{L}$ loss of the note's threshold argument.

**Why the exponent is $0.227$ and not $\log_2(4/3)=0.415$** (§6.1). The plan's bound "$\mathbb E[2^{W_{N_K}}M]\le C\,\mathbb E[2^{-s_2(x\bmod2^K)}]=C(3/4)^K$" needs $M$ and the low digits of $x$ to be uncorrelated. They are not independent: the martingale reads the same digits, and $E[M\mid\text{low digits}]$ is *not* the initial value. Without any decorrelation, the optimal bound from "$E M\le C$, barrier $1-s_2(x\bmod 2^K)$" is $2^{-\alpha^*K}$, and this is what we prove. A decorrelation hypothesis (H$_{\rm dec}$, §6.1) would give $0.415$. The true exponent is numerically $1$ (§7).

**Heuristic (new).** A branching-process-in-varying-environment (Agresti-type) predictor
$$\mathbb P(g_2(x)\ge G\mid x)\approx\min\big(1,\kappa/A_G(x)\big),\qquad A_G(x)=\sum_{k<n_G(x),\ x+k+1\ \text{odd}}2^{-W_{k+1}(x)},$$
with one constant $\kappa\approx2.6$ fitted to Monte Carlo, reproduces: (i) $\delta_G(2)\sim c/G$ (it gives $G\,\mathbb E[1/(2A_G)]=2.09$–$2.12$ for every $G$ from $16$ to $16384$); (ii) the natural-number counts $N(A,G)=\#\{a\le A:g_2(a)\ge G\}$ for $A=256,1024,4096$ and $256\le G\le4094$ within Poisson error; (iii) the counts $\#\{a:g_2(a)\ge\lambda a\}$ for $\lambda=1,\dots,64$. It **predicts a new regime** for natural numbers: for $G\gg a$, $\mathbb P(g_2(a)\ge G)\asymp2^{-s(a)}G^{-\log_2(3/2)}$, i.e. exponent $0.585$, slower than $1/G$. A testable form (Conjecture 7.3) is $\#\{a\le X:g_2(a)\ge\lambda a\}\sim q(\lambda)\log_2X$ with $q(\lambda)\asymp\lambda^{-0.585}$ as $\lambda\to\infty$.

**Kitamura's "$\sim11.5/G$" versus the note's "$\approx0.7/\sqrt G$"** (§7.4). There are three separate effects:
- a factor-$2$ normalisation: Kitamura counts even $a$ only, and $11.5/G\approx2\delta_G$;
- a pre-asymptotic window: the $1/\sqrt G$ fit used $G\le254$, where the local exponent is still rising from $0.6$ to $1$;
- a difference of regime: natural $a$ with $G\lesssim a$ behave like Haar points ($1/G$), and only $G\gg a$ is different ($G^{-0.585}$).

Kitamura's data ($A=256$, $G\le1024$) lies in the crossover. Kitamura's repository gives no definition of the fit (T4).

**Not achieved.** A rate for $\delta_G(2)$ itself. The obstruction is explicit (§6.2). Near $-2$ the path $B=\{1,3\}$ gives $S_B=(x+2)^3$, a triple root. All integer-point certificates then fail: $\gamma_2(2+2^ku)\ge3k$. The measured slopes on $\{v(x+2)=t\}$ are $2t+1$ for odd $t$ and have tails up to about $5t$ for even $t$.

## Contents
1. Notation and standing facts
2. Taylor certificates and slope bounds
3. A Hensel first-moment bound
4. The window identity
5. Stopping argument and the main theorem
6. What does not work, and the class $14+16\mathbb Z_2$
7. Heuristic theory of the $1/G$ law; Kitamura's fit
8. Computations
9. Gaps, status, credit

## 1. Notation and standing facts

We use the notation of note §10.1:
- $v=v_2$; $s(\cdot)$ is the binary digit sum; $\mu$ is Haar probability measure on $\mathbb Z_2$.
- $\pi_j(x)=\prod_{i=1}^{j}(x+i)$, $V_n(x)=v(\pi_n(x))$, $W_n(x)=n-V_n(x)$, $M_n(x)=\max_{1\le i\le n}v(x+i)$.
- $F^{[i]}=F^{(i)}/i!$. For $F\in\mathbb Z_2[X]$ every $F^{[i]}$ has coefficients in $\mathbb Z_2$, and $F(y+h)=\sum_iF^{[i]}(y)h^i$ exactly.
- A *path of length $n$* is $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$, and $S_e=\sum_{j<n}e_j\pi_j\in\mathbb Z[X]$.
- $e$ is *alive at $n$* (at $x$) if $v(S_e(x))\ge V_n(x)$. $P_n(x)$ is the set of paths of length $n$ alive at $n$.
- The *target* of an alive path is $\tau_n(e,x)=-S_e(x)/\pi_n(x)\in\mathbb Z_2$, and its *slope* is $\lambda_e(x)=v(S_e'(x))$.
- *Children:* for $N>n$ and $f\in\{0,1\}^{N-n}$, $(e,f)$ is the path of length $N$ extending $e$ by $f$.
- $Z_n(x):=2^{-W_n(x)}|P_n(x)|$.

Throughout, $x\in2\mathbb Z_2$; odd $x$ have $g_2=0$.

**Lemma 1.1 (valuations) [proved; (a)–(e) are note Lemma 10.2].** Let $x\in2\mathbb Z_2$ not be a negative integer, and $n\ge1$.
- (a) $V_n\ge n-s(n)\ge n-\log_2n-1$; hence $W_n\le s(n)$.
- (b) $V_n<n+M_n$ (for $M_n\ge1$).
- (c) $V_j-V_n\ge\lfloor (j-n)/2\rfloor$ for $j\ge n$.
- (d) For $K\ge1$ let $r=x\bmod2^K\in[0,2^K)$ and $N_K=\min\{N\ge1:2^K\mid x+N\}$, so $N_K=2^K-r$ (or $2^K$ if $r=0$). Then $W_{N_K}\le1-s(r)$.
- (e) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$.
- (f) **(new)** For $0\le\delta<2^K$: $W_{N_K+\delta}=W_{N_K}+s(\delta)$.
- (g) **(new)** For $n\ge4$, $V_n\ge M_n+1$. If $n\ge6$, then $V_n\ge M_n+2$.
- (h) **(new)** For $N>n$: $D:=V_N-V_n\le(N-n)+M_N$.

*Proof.*
- (a) At least $\lfloor n/2^\ell\rfloor$ of $n$ consecutive elements are divisible by $2^\ell$; summing over $\ell$ gives $V_n\ge v(n!)=n-s(n)$.
- (b) At most $\lceil n/2^\ell\rceil\le n/2^\ell+1$ of them are divisible by $2^\ell$, and none by $2^{M_n+1}$. So $V_n\le\sum_{\ell=1}^{M_n}(n/2^\ell+1)<n+M_n$.
- (c) $x+i$ is even for every second $i$.
- (d) For $1\le i<N_K$, $r+i\in(r,2^K)$ and $v(x+i)=v(r+i)<K$. So $\sum_{i<N_K}v(x+i)=v((2^K-1)!)-v(r!)=(2^K-1-K)-(r-s(r))$. Also $v(x+N_K)\ge K$. So $V_{N_K}\ge N_K-1+s(r)$.
- (e) $\pi_j^{[i]}=\pi_j\cdot e_i\big(\tfrac1{x+1},\dots,\tfrac1{x+j}\big)$, and each monomial of $e_i$ has valuation $\ge -iM_j$.
- (f) $x+N_K=2^Ku$. For $1\le i\le\delta<2^K$, $v(x+N_K+i)=v(2^Ku+i)=v(i)$, because $v(i)<K$. So $V_{N_K+\delta}-V_{N_K}=v(\delta!)=\delta-s(\delta)$.
- (g) The terms $x+2,x+4$ (and $x+6$ if $n\ge6$) are even. The term of maximal valuation contributes $M_n$, and the remaining even terms contribute at least $1$ each.
- (h) $D=\sum_{\ell\ge1}\#\{i\in(n,N]:2^\ell\mid x+i\}\le\sum_{\ell=1}^{M_N}\big(\lfloor (N-n)/2^\ell\rfloor+1\big)\le(N-n)+M_N$. ∎

**Lemma 1.2 (survival forces alive populations) [proved].** If $g_2(x)\ge G$, then $P_n(x)\ne\emptyset$ for every $n\ge1$ with $V_n(x)\le G$.

*Proof.* Take a finite $B$ with $v(S_B(x))\ge G$, and let $e$ be its indicator word with $e_0=1$, extended by zeros. Then $S_{e|_n}=S_B-\sum_{j\ge n}e_j\pi_j$, and $v(\pi_j(x))\ge V_n(x)$ for $j\ge n$. So $v(S_{e|_n}(x))\ge\min(G,V_n)=V_n$. ∎

**Lemma 1.3 (cylinders) [proved].** For $n\ge4$, the sets $C_n(x):=x+2^{V_n(x)}\mathbb Z_2$ ($x\in2\mathbb Z_2$) partition $2\mathbb Z_2$, and the partition at $n+1$ refines the one at $n$. On $C_n(x)$:
- the valuations $v(\cdot+i)$, $i\le n$, are constant;
- the set $P_n(\cdot)$ is constant;
- $W_n$ is constant.

*Proof.* If $y\in C_n(x)$ then $v(y-x)\ge V_n(x)>M_n(x)$ by Lemma 1.1(g). So $v(y+i)=v(x+i)$ for $i\le n$, hence $V_n(y)=V_n(x)$ and $C_n(y)=C_n(x)$. Aliveness at $n$ is the congruence $S_e(\cdot)\equiv0\pmod{2^{V_n}}$, and $S_e\in\mathbb Z[X]$. Refinement holds because $V_{n+1}\ge V_n$. ∎

We write $\mathcal F_n$ for the $\sigma$-algebra generated by this partition. Conditional expectation given $\mathcal F_n$ is the normalised Haar average over $C_n(x)$.

## 2. Taylor certificates and slope bounds

**Lemma 2.1 (Taylor inequality) [proved].** Suppose $\Phi(y+h)=\sum_{i\ge0}\varphi_ih^i$ is a convergent expansion in $\mathbb Q_2$, with every $\varphi_i\in\mathbb Z_2$. Then
$$\min_{i\ge0}\big(v(\varphi_i)+i\,v(h)\big)\ \le\ v(\Phi(y+h)).$$
*Proof.* If every term had valuation $>v(\Phi(y+h))$, so would the (convergent) sum. ∎

The idea: choose $y+h$ to be a **negative integer** $-m$. Then $S_e(-m)=\sum_{j<m}e_j\pi_j(-m)$ involves only finitely many path entries, and its valuation is bounded by a finite computation. Lemma 2.1 then turns this into an upper bound on some Taylor coefficient of $S_e$ at $x$. For alive paths, $v(S_e(x))$ is huge, so the $i=0$ term cannot be the small one, and we get a bound on the slope or on a higher derivative. (The bound $v(S_e(-m))\le\gamma_2(m)$ is the "shadow of $-m$" of note §3.2. What is new is to use it on the *Taylor coefficients at $x$*, not just on values.)

**Lemma 2.2 (the renormalisation near $-2$) [proved].** Let $x\equiv2\pmod4$, $y:=x+2$, $t:=v(y)\ge2$.
- (i) If $v(S_e(x))\ge t+1$, then $e_1=1$ and $e_2+e_3=1$.
- (ii) For every path with $e_1=1$, as rational functions,
$$S_e(x)=y(y-1)\,\Phi_e(y),\qquad \Phi_e(y):=e_2-\frac1{1-y}+\sum_{k\ge1}e_{k+2}\,\pi_k(y).$$
- (iii) For $y\in2\mathbb Z_2$ and $h\in2\mathbb Z_2$, $\Phi_e(y+h)=\sum_i\Phi_e^{[i]}(y)h^i$ with all $\Phi_e^{[i]}(y)\in\mathbb Z_2$.
- (iv) $S_e'(x)=(2y-1)\Phi_e(y)+y(y-1)\Phi_e'(y)$. If $v(\Phi_e(y))>t+v(\Phi_e'(y))$, then $\lambda_e(x)=t+v(\Phi'_e(y))$.

*Proof.*
- (i) For $b\ge4$, $\pi_b(x)$ contains $(x+2)(x+4)$, so it has valuation $\ge t+1$. Modulo $2^{t+1}$,
$$S_e(x)\equiv1+e_1(x+1)+e_2(x+1)(x+2)+e_3(x+1)(x+2)(x+3).$$
  If $e_1=0$ the right side is odd. If $e_1=1$ it equals $y\,[1+e_2(x+1)+e_3(x+1)(x+3)]$, and the bracket is $\equiv1+e_2+e_3\pmod2$. So it must be even, i.e. $e_2+e_3=1$. (This is the argument of the halving lemma, note Theorem 3.7.)
- (ii) $x+1=y-1$, and for $j\ge2$, $\pi_j(x)=(y-1)\,y\,\pi_{j-2}(y)$. Hence
$$S_e=1+(y-1)+(y-1)y\sum_{j\ge2}e_j\pi_{j-2}(y)=y+y(y-1)\big[e_2+\textstyle\sum_{k\ge1}e_{k+2}\pi_k(y)\big],$$
  and $y=y(y-1)\cdot\frac{1}{y-1}=y(y-1)\cdot\big(-\frac1{1-y}\big)$.
- (iii) The polynomial part is exact Taylor. Also $-\frac1{1-y-h}=-\sum_ih^i(1-y)^{-i-1}$, where $1-y$ is a unit and $v(h)\ge1$.
- (iv) Differentiate. Then $v((2y-1)\Phi_e)=v(\Phi_e)$ and $v(y(y-1)\Phi_e')=t+v(\Phi_e')$. ∎

**Proposition 2.3 (slope certificates) [proved; the finite checks are in `code/certs.py`, output `logs/certs.out`].** Let $n\ge1$, $x\in\mathbb Z_2$, and let $e$ be alive at $n$ (at $x$).
- **(a) $C_0:=8\mathbb Z_2$, $L=1$.** If $x\in C_0$ and $V_n(x)\ge4$, then $\lambda_e(x)\le1$.
- **(b) $C_2:=2+8\mathbb Z_2$, $L=3$.** If $x\in C_2$ and $V_n(x)\ge7$, then $\lambda_e(x)\le3$.
- **(c) $C_6:=6+16\mathbb Z_2$, $L=6$.** If $x\in C_6$ and $V_n(x)\ge11$, then $\lambda_e(x)\le6$.

*Proof.*
- (a) Take $h=-4-x$; $v(h)=2$ since $x+4\equiv4\pmod8$. Since $\pi_j(-4)=0$ for $j\ge4$, $S_e(-4)=1-3e_1+6e_2-6e_3\in\{1,-5,7,1,-2,-8,4,-2\}$, of valuation $\le3$. By Lemma 2.1 some $i$ has $v(S_e^{[i]}(x))+2i\le3$.
  - $i=0$ is excluded, because $v(S_e(x))\ge V_n\ge4$.
  - $i\ge2$ is impossible, because $2i\ge4$.
  - So $i=1$ and $v(S_e'(x))\le1$.
- (b) Here $t=2$, $y\equiv4\pmod8$, and $h:=-4-y$ has $v(h)\ge3$. Since $V_n\ge7\ge t+1$, Lemma 2.2(i) applies. Note $\pi_k(-4)=-3,6,-6$ for $k=1,2,3$ and $0$ for $k\ge4$.
  - *Case $e_2=1$, $e_3=0$.* Then $\Phi_e(-4)=\tfrac45+6e_4-6e_5\in\{\tfrac45,\tfrac{34}5,-\tfrac{26}5\}$, of valuation $\le2$.
    - Since $v(h)\ge3$, Lemma 2.1 forces $i=0$: $v(\Phi_e(y))\le2$.
    - Then $v(S_e(x))=t+v(\Phi_e(y))\le4<7$, a contradiction. This case does not occur.
  - *Case $e_2=0$, $e_3=1$.* Then $\Phi_e(-4)=-\tfrac15-3+6e_4-6e_5\in\{-\tfrac{16}5,\tfrac{14}5,-\tfrac{46}5\}$, of valuation $\le4$.
    - $i=0$ would give $v(S_e(x))\le t+4=6<7$.
    - $i\ge2$ is impossible, as $2v(h)\ge6$.
    - So $i=1$ and $v(\Phi'_e(y))\le4-3=1$.
    - Since $v(\Phi_e(y))\ge V_n-t\ge5>t+1$, Lemma 2.2(iv) gives $\lambda_e=t+v(\Phi'_e)\le3$.
- (c) Here $t=3$ and $y\equiv8\pmod{16}$.
  - *Case $e_2=1$, $e_3=0$.* Take $h=-4-y$, with $v(h)=2$. Again $v(\Phi_e(-4))\le2$.
    - $i=0$ would give $v(S_e(x))\le5<11$.
    - $i\ge2$ is impossible, as $v(\Phi_e^{[i]})+2i\ge4>2$.
    - So $v(\Phi_e'(y))=0$, and $\lambda_e=3$ by Lemma 2.2(iv) (as $v(\Phi_e)\ge V_n-3\ge8$).
  - *Case $e_2=0$, $e_3=1$.* Take $h=-8-y$, with $v(h)\ge4$ since $y+8\equiv0\pmod{16}$.
    - $\Phi_e(-8)=-\tfrac19+\sum_{k=1}^7e_{k+2}\pi_k(-8)$ depends on $(e_4,\dots,e_9)$. Over all $64$ cases its valuation is at most $7$ (exact rational arithmetic; histogram of valuations $\{1{:}32,3{:}16,4{:}8,5{:}3,6{:}4,7{:}1\}$).
    - $i=0$ would give $v(S_e(x))\le3+7=10<11$.
    - $i\ge2$ is impossible, as $2v(h)\ge8>7$.
    - So $v(\Phi'_e(y))\le7-4=3$.
    - Since $v(\Phi_e)\ge V_n-3\ge8>3+3$, we get $\lambda_e=3+v(\Phi'_e)\le6$. ∎

*Remarks.*
1. On $4+8\mathbb Z_2$ one has $g_2=3$ (note Corollary 3.7.1(iii), Lean `E404.g_eq_three`), and odd $x$ have $g_2=0$. So $R=\mathbb Z_2\setminus(14+16\mathbb Z_2)$ is covered by $C_0,C_2,C_6$ and two trivial classes.
2. Numerically the bounds in (b), (c) are not sharp. In 20 000 random points of each class (depth $\le64$, `logs/check_cert_big.out`), the largest slope seen was $1$, $3$ and $3$ respectively, with zero violations.
3. Proposition 2.3 replaces three ingredients of note §10.1 on these classes: the slope cut-off $L$, the classes $P^{1,L}$, and the multiplicity-$\ge2$ classes $P^{k,L}$. **Every** alive path has bounded slope, at **every** time with $V_n$ above a fixed threshold.

## 3. A Hensel first-moment bound

**Lemma 3.1 [proved/standard].** Let $f\in\mathbb Z_2[X]$ be nonzero.
- (a) *(Hensel, strong form.)* If $x\in\mathbb Z_2$ and $v(f(x))>2\lambda$ where $\lambda:=v(f'(x))$, then there is a root $r\in\mathbb Z_2$ of $f$ with $v(r-x)=v(f(x))-\lambda>\lambda$, and $v(f'(r))=\lambda$.
- (b) *(Root separation.)* If $r_1\ne r_2$ are roots of $f$, then $v(f'(r_1))\ge v(r_1-r_2)$.

*Proof.*
- (a) This is the standard Newton iteration; we include it for completeness.
  - Put $x_0=x$ and $x_{k+1}=x_k-f(x_k)/f'(x_k)$. Write $v(f(x_k))=2\lambda+\delta_k$, with $\delta_0>0$, and $h_k=x_{k+1}-x_k$.
  - By exact Taylor expansion, $f(x_{k+1})=h_k^2\sum_{i\ge2}f^{[i]}(x_k)h_k^{i-2}$, so $v(f(x_{k+1}))\ge2v(h_k)=2\lambda+2\delta_k$.
  - Also $f'(x_{k+1})\equiv f'(x_k)\pmod{2^{v(h_k)}}$ with $v(h_k)=\lambda+\delta_k>\lambda$, so $v(f'(x_{k+1}))=\lambda$. Inductively $\delta_k\ge2^k\delta_0$.
  - So $x_k\to r$ with $f(r)=0$ and $v(f'(r))=\lambda$. Moreover $v(r-x)=v(h_0)=v(f(x))-\lambda$, because $v(h_k)>v(h_0)$ for $k\ge1$.
- (b) Put $h=r_2-r_1$. Then $0=f(r_2)=\sum_{i\ge0}f^{[i]}(r_1)h^i$ and $f(r_1)=0$, so $f'(r_1)=-h\sum_{i\ge2}f^{[i]}(r_1)h^{i-2}$, with $f^{[i]}(r_1)\in\mathbb Z_2$. ∎

**Proposition 3.2 (Hensel first-moment bound) [proved].** Let $C=r_0+2^k\mathbb Z_2\subseteq2\mathbb Z_2$, $L\ge0$ and $n\ge6$. Let $\Gamma\subseteq\mathbb Z_2$ be a set on which
$$V_n\ge\max(2L+1,\,L+k),\qquad V_n-L>M_n.$$
Suppose every $e\in P_n(x)$ has $\lambda_e(x)\le L$, for every $x\in C\cap\Gamma$. Then
$$\int_{C\cap\Gamma}Z_n\,d\mu\ \le\ 2^{\,L-1+\max(0,\,L+1-k)}.$$

*Proof.* Write $A_e=\{x:e\in P_n(x)\}$, so $\int_{C\cap\Gamma}Z_n=\sum_e\int_{A_e\cap C\cap\Gamma}2^{V_n(x)-n}\,d\mu(x)$, the sum running over the $2^{n-1}$ paths of length $n$. Fix $e$ and $x\in A_e\cap C\cap\Gamma$, and let $\lambda=\lambda_e(x)\le L$.
- Since $v(S_e(x))\ge V_n(x)\ge2L+1>2\lambda$, Lemma 3.1(a) gives a root $r$ of $S_e$ with $v(r-x)\ge V_n(x)-\lambda\ge V_n(x)-L>M_n(x)$ and $v(S'_e(r))=\lambda$. ($S_e\ne0$, since $S_e(0)=\sum e_jj!\ge1$.)
- Hence $v(r+i)=v(x+i)$ for $i\le n$, so $V_n(r)=V_n(x)$ and $M_n(r)=M_n(x)$. Also $v(r-x)\ge V_n-L\ge k$, so $r\in C$.
- So $r$ lies in $R_e:=\{r\in C:\ S_e(r)=0,\ \lambda_r:=v(S_e'(r))\le L,\ V_n(r)-\lambda_r>M_n(r)\}$, and $x\in B_r:=r+2^{V_n(r)-\lambda_r}\mathbb Z_2$.
- For any $x'\in B_r$, $v(x'-r)>M_n(r)$, so $V_n(x')=V_n(r)$.

Therefore
$$\int_{A_e\cap C\cap\Gamma}2^{V_n-n}\,d\mu\le\sum_{r\in R_e}2^{V_n(r)-n}\mu(B_r)=\sum_{r\in R_e}2^{\lambda_r-n}\le|R_e|\,2^{L-n}.$$
By Lemma 3.1(b), distinct $r_1,r_2\in R_e$ satisfy $k\le v(r_1-r_2)\le\lambda_{r_1}\le L$. So $|R_e|\le1$ if $k>L$, and otherwise the elements of $R_e$ are pairwise incongruent mod $2^{L+1}$ inside one class mod $2^k$, so $|R_e|\le2^{L+1-k}$. Summing over the $2^{n-1}$ paths gives the claim. ∎

**Corollary 3.3 [proved].** Let $\Gamma_*(n)$ be the event on which:
- $V_n\ge\max(V_{\rm cert},2L+1,L+k)$, where $V_{\rm cert}=4,7,11$ for $C_0,C_2,C_6$;
- $V_n-L>M_n$.

Then for $n\ge6$:
- $\int_{C_0\cap\Gamma_*}Z_n\le1$;
- $\int_{C_2\cap\Gamma_*}Z_n\le8$;
- $\int_{C_6\cap\Gamma_*}Z_n\le256$.

(Proposition 2.3 supplies the slope hypothesis.)

*Remarks.*
1. Numerically, $E[Z_n\mid C]\approx0.52$, $0.97$ and $2.0$ for $n=16,\dots,40$ (`logs/check_cert_big.out`). That is, $\int_CZ_n\approx0.065$, $0.12$, $0.125$, and it is flat in $n$, as a martingale should be. So the constants are crude but the order is right.
2. Proposition 3.2 is the step that is unavailable for unbounded slopes. Near a $k$-fold near-root, the ball where $e$ is alive has measure about $2^{\lambda-V}$ with $\lambda$ unbounded, and nothing caps $\sum_e\sum_r2^{\lambda_r}$. This is exactly what happens on $14+16\mathbb Z_2$ (§6.2). There T4's annealed means $E Z$ grow linearly, one unit per shadow depth.

## 4. The window identity

This section re-proves, in the form needed here, the one-window identity of note §10.1 (Lemma 10.5, Proposition 10.6). These are due to round-2 track R1b. The only additions are:
- a single hypothesis $\Gamma_L(n)$ that implies (W1)–(W3);
- the unweighted count in Corollary 4.3(a).

**Weights.** For $\lambda\ge0$ put $Q^{(n)}_f(X):=\sum_{i<2\lambda}f_i\,\pi_{n+i}(X)/\pi_n(X)\in\mathbb Z[X]$ for $f\in\{0,1\}^{2\lambda}$, where $\pi_{n+i}/\pi_n=\prod_{j=n+1}^{n+i}(X+j)$. Define
$$a^{(\lambda)}_n(x;t):=2^{-2\lambda}\#\{f\in\{0,1\}^{2\lambda}:Q^{(n)}_f(x)\equiv t\ (2^\lambda)\},\qquad \rho_n(e;x):=2^{\lambda}a^{(\lambda)}_n\big(x;\tau_n(e,x)\bmod2^\lambda\big),$$
with $\lambda=\lambda_e(x)$. Then:
- $\sum_ta^{(\lambda)}_n(x;t)=1$ and $0\le\rho\le2^\lambda$;
- $a^{(\lambda)}_n(x;\cdot)$ depends only on $n$, $\lambda$ and $x\bmod2^\lambda$;
- **for $\lambda\le1$, $\rho\equiv1$**: for $\lambda=1$, $f_0+f_1(x+n+1)$ is uniform mod $2$;
- *(stability)* for $J\ge2\lambda$, the law of $\sum_{i<J}f_i\pi_{n+i}/\pi_n\bmod2^\lambda$ ($f$ uniform in $\{0,1\}^J$) is $a^{(\lambda)}_n(x;\cdot)$, because the terms with $i\ge2\lambda$ have valuation $\ge\lambda$ (Lemma 1.1(c)).

**Setting.** $x\in2\mathbb Z_2$, $n\ge6$, $L\ge0$, $\ell_0:=2L+2$, $N:=n+\ell_0$, $m:=V_n(x)$, $D:=V_N(x)-m$, $C:=x+2^m\mathbb Z_2$. Write $x'=x_0+2^mw$ ($w\in\mathbb Z_2$) for the points of $C$, where $x_0\in[0,2^m)$, and $Q_f:=\sum_{j=n}^{N-1}f_j\pi_j/\pi_n$ for $f\in\{0,1\}^{\ell_0}$. Define the event
$$\Gamma_L(n):\qquad 2M_N(x)+3L+3\le V_n(x).$$
On $\Gamma_L(n)$:
- $M_N<m$;
- $D\le\ell_0+M_N$ by Lemma 1.1(h), so $D+L\le m-M_n$ (this is (W2));
- $L<m-M_N$ (this is (W3));
- (W1) holds by construction;
- $D\ge\lfloor\ell_0/2\rfloor=L+1$ by Lemma 1.1(c).

$\Gamma_L(n)$ is decided by $x\bmod2^m$: it says $v(x+i)\le(m-3L-3)/2$ for all $i\le N$, and each such inequality is decided mod $2^m$.

**Lemma 4.1 (linearisation; note Lemma 10.5) [proved].** Assume $M_N(x)<m$.
- (a) $v(x'+i)=v(x+i)$ for $i\le N$. Hence $V_n,V_N,M_N,W_n,W_N$ are constant on $C$. Aliveness at $n$ is constant on $C$, and so is $F(x')\bmod2^m$ for $F\in\mathbb Z[X]$.
- (b) If $e$ is alive at $n$, then $\tau_n(e,x')\equiv\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)\,w\pmod{2^{m-M_n}}$, where $\omega=\pi_n(x_0)/2^m\in\mathbb Z_2^\times$.
- (c) $(e,f)$ is alive at $N$ at $x'$ iff $e$ is alive at $n$ and $\tau_n(e,x')\equiv Q_f(x')\pmod{2^D}$. In that case $\tau_N((e,f),x')=(\tau_n(e,x')-Q_f(x'))\,\pi_n(x')/\pi_N(x')$.

*Proof.*
- (a) $v(x'-x)\ge m>v(x+i)$.
- (b) With $h=2^mw$, $S_e(x')=S_e(x_0)+hS_e'(x_0)+h^2R$ with $R\in\mathbb Z_2$. Also $\pi_n(x')=\pi_n(x_0)(1+E)$, $1+E=\prod_{i\le n}(1+h/(x_0+i))$, and $v(E)\ge m-M_n$. So $\tau_n(e,x')=[\tau_0-\omega^{-1}S_e'(x_0)w-\omega^{-1}2^mw^2R](1+E)^{-1}$, where $\tau_0=\tau_n(e,x_0)\in\mathbb Z_2$ and the bracket is in $\mathbb Z_2$.
- (c) $S_{(e,f)}=\pi_n(Q_f-\tau_n)$, $V_N=m+D$, and backward integrality (if $(e,f)$ is alive at $N$ then $e$ is alive at $n$, because $2^{V_n}\mid\pi_j$ for $j\ge n$). ∎

**Proposition 4.2 (one-window identity; note Prop. 10.6) [proved].** Assume $\Gamma_L(n)$, and let $e\in P_n(x)$ with $\lambda:=\lambda_e(x)\le L$.
- (i) $\lambda_e(x')=\lambda$ on $C$, and every child $(e,f)$ alive at $N$ at $x'\in C$ has slope $\lambda$ at $x'$.
- (ii) $s_e:=\tau_n(e,x')\bmod2^\lambda$ is constant on $C$; hence so is $\rho_n(e;x')$.
- (iii) For every $s\in\mathbb Z/2^\lambda$,
$$\mathbb E_{x'\in C}\#\{f:(e,f)\in P_N(x'),\ \tau_N((e,f),x')\equiv s\ (2^\lambda)\}=2^{W_N-W_n}\,a^{(\lambda)}_n(x;s_e).$$

*Proof.*
- (i) $S_e'(x')\equiv S_e'(x)\pmod{2^m}$ and $\lambda<m$, so $\lambda_e(x')=\lambda$. For the child, $S'_{(e,f)}=S'_e+\sum_{j=n}^{N-1}f_j\pi_j'$ and $v(\pi'_j(x'))\ge V_j-M_j\ge m-M_N>L\ge\lambda$ by Lemma 1.1(e) and (W3).
- (ii) $v(\omega^{-1}S_e'(x_0))=\lambda\le L\le m-M_n$. Apply Lemma 4.1(b).
- (iii) Let $\beta:=\omega^{-1}S'_e(x_0)/2^\lambda\in\mathbb Z_2^\times$ and $\tau_0:=\tau_n(e,x_0)$.
  - By Lemma 4.1(b) and $D+\lambda\le m-M_n$, $t(w):=\tau_n(e,x_0+2^mw)\bmod2^{D+\lambda}$ equals $(\tau_0-2^\lambda\beta w)\bmod2^{D+\lambda}$. So $w\bmod2^D\mapsto t$ is a bijection onto the coset $\tau_0+2^\lambda\mathbb Z/2^{D+\lambda}$.
  - Since $D+\lambda\le m$, two quantities are constant on $C$: $q_f:=Q_f(x')\bmod2^{D+\lambda}$, and $u:=\big(\pi_N(x')/\pi_n(x')\big)/2^D\bmod2^\lambda$, a unit.
  - Fix $f$. If $q_f\not\equiv\tau_0\pmod{2^\lambda}$, no $t$ in the coset satisfies $t\equiv q_f\pmod{2^D}$, because $D>\lambda$. So there is no child.
  - Otherwise the admissible $t$ are $t=q_f+2^Dz$, $z\in\mathbb Z/2^\lambda$. Each lies in the coset and comes from exactly one class $w\bmod2^D$. By Lemma 4.1(c) the child then has $\tau_N\equiv zu^{-1}\pmod{2^\lambda}$, a bijection $z\leftrightarrow s$.
  - So the expectation equals $2^{-D}\#\{f\in\{0,1\}^{\ell_0}:Q_f(x)\equiv s_e\ (2^\lambda)\}=2^{\ell_0-D}a^{(\lambda)}_n(x;s_e)$, by stability ($\ell_0\ge2\lambda$). Finally $\ell_0-D=W_N-W_n$. ∎

**Corollary 4.3 [proved].** Under the hypotheses of Proposition 4.2:
- (a) $\mathbb E_{x'\in C}\#\{f:(e,f)\in P_N(x')\}=2^{W_N-W_n}\rho_n(e;x)$;
- (b) $\mathbb E_{x'\in C}\sum_{f:(e,f)\in P_N(x')}\rho_N((e,f);x')=2^{W_N-W_n}\rho_n(e;x)$.

*Proof.* Sum (iii) over the $2^\lambda$ values of $s$.
- For (a), the right side of (iii) does not depend on $s$, so the sum is $2^{W_N-W_n}2^\lambda a_n(s_e)$.
- For (b), weight by $\rho_N=2^\lambda a^{(\lambda)}_N(x';s)$ (child slope $=\lambda$ by (i)). The function $a^{(\lambda)}_N(x';\cdot)$ depends only on $x'\bmod2^\lambda$, so it is constant on $C$, and $\sum_sa_N(s)=1$. ∎

## 5. Stopping argument and the main theorem

Fix one of the three classes, with data

| class | $k$ | $r_0$ | $s(r_0)$ | $L$ | $V_{\rm cert}$ | $\ell_0=2L+2$ | $s_L:=\max_{0\le\delta<\ell_0}s(\delta)$ | $E_C$ |
|---|---|---|---|---|---|---|---|---|
| $C_0=8\mathbb Z_2$ | 3 | 0 | 0 | 1 | 4 | 4 | 2 | $1$ |
| $C_2=2+8\mathbb Z_2$ | 3 | 2 | 1 | 3 | 7 | 8 | 3 | $2^3\cdot8=64$ |
| $C_6=6+16\mathbb Z_2$ | 4 | 6 | 2 | 6 | 11 | 14 | 3 | $2^6\cdot256=16384$ |

Here $E_C:=2^L\cdot2^{L-1+\max(0,L+1-k)}$ for $C_2,C_6$, and $E_{C_0}:=1$ (because $\rho\equiv1$ when $L=1$).

**Windows.** Fix $n_0\ge19$, so that $V_{n_0}\ge n_0-\log_2n_0-1\ge13\ge\max(V_{\rm cert},2L+1,L+k)$ for all three classes. Put $n_\ell=n_0+\ell\ell_0$, $\mathcal F_\ell:=\mathcal F_{n_\ell}$ (Lemma 1.3), and let $\Gamma_\ell:=\Gamma_L(n_\ell)\in\mathcal F_\ell$. Define
$$M_\ell(x):=2^{-W_{n_\ell}(x)}\sum_{e\in P_{n_\ell}(x)}\rho_{n_\ell}(e;x),\qquad Y_\ell:=M_\ell\,\mathbf 1_{\Gamma_0\cap\dots\cap\Gamma_\ell}.$$
$C\in\mathcal F_0$, because $V_{n_0}\ge4$.

**Lemma 5.1 [proved].** On $C$:
- (a) $Y_\ell$ is $\mathcal F_\ell$-measurable.
- (b) On $C\cap\Gamma_\ell$: $\mathbb E[M_{\ell+1}\mid\mathcal F_\ell]=M_\ell$, $\ \mathbb E[|P_{n_{\ell+1}}|\mid\mathcal F_\ell]=2^{W_{n_{\ell+1}}}M_\ell$, and $W_{n_{\ell+1}}$ is $\mathcal F_\ell$-measurable.
- (c) $(Y_\ell\mathbf 1_C)_{\ell\ge0}$ is a nonnegative $(\mathcal F_\ell)$-supermartingale.

*Proof.*
- (a) On $C\cap\Gamma_\ell$, every $e\in P_{n_\ell}$ has $\lambda_e\le L$ by Proposition 2.3, since $V_{n_\ell}\ge V_{n_0}\ge V_{\rm cert}$. So $\rho_{n_\ell}(e;\cdot)$ is constant on the atom by Proposition 4.2(ii). $P_{n_\ell}$ and $W_{n_\ell}$ are constant on atoms by Lemma 1.3, and $\Gamma_0,\dots,\Gamma_\ell\in\mathcal F_\ell$.
- (b) Let $N=n_{\ell+1}$. By backward integrality, $P_N(x')$ is the disjoint union over $e\in P_{n_\ell}$ of the alive children of $e$. Every $e$ has slope $\le L$, and $W_N$ is constant on the atom (Lemma 4.1(a)). Sum Corollary 4.3(b), resp. (a), over $e$.
- (c) $\mathbb E[Y_{\ell+1}\mid\mathcal F_\ell]=\mathbf 1_{\Gamma_0\cap\dots\cap\Gamma_\ell}\,\mathbb E[M_{\ell+1}\mathbf 1_{\Gamma_{\ell+1}}\mid\mathcal F_\ell]\le\mathbf 1_{\Gamma_0\cap\dots\cap\Gamma_\ell}M_\ell=Y_\ell$ on $C$, by (b). ∎

**Proposition 5.2 (predictable-barrier bound) [proved].** Let $c\in\mathbb R$ and $\ell^*\ge0$. Put
$$A_\ell:=\Gamma_0\cap\dots\cap\Gamma_\ell\cap\{W_{n_{\ell+1}}\le-c\}\in\mathcal F_\ell,\qquad \mathrm{Hit}:=\bigcup_{\ell\le\ell^*}A_\ell.$$
Then
$$\mu\big(C\cap\mathrm{Hit}\cap\{P_{n_{\ell+1}}\ne\emptyset\ \forall\ell\le\ell^*\}\big)\le2^{-c}\,\mathbb E[Y_0\mathbf 1_C].$$

*Proof.* $\sigma:=\min\{\ell\le\ell^*:x\in A_\ell\}$ ($=\infty$ if there is none) is a stopping time, since $\{\sigma=\ell\}=A_\ell\setminus\bigcup_{\ell'<\ell}A_{\ell'}\in\mathcal F_\ell$. On $\{\sigma=\ell\}$ we have $\Gamma_\ell$, $Y_\ell=M_\ell$ and $2^{W_{n_{\ell+1}}}\le2^{-c}$. By Lemma 5.1(b),
$$\mu(\cdots)\le\sum_{\ell\le\ell^*}\mathbb E\big[\mathbf 1_C\mathbf 1_{\sigma=\ell}|P_{n_{\ell+1}}|\big]=\sum_\ell\mathbb E\big[\mathbf 1_C\mathbf 1_{\sigma=\ell}2^{W_{n_{\ell+1}}}M_\ell\big]\le2^{-c}\,\mathbb E\big[\mathbf 1_CY_{\sigma\wedge(\ell^*+1)}\big]\le2^{-c}\,\mathbb E[\mathbf 1_CY_0].$$
The last step is optional stopping for the bounded stopping time $\sigma\wedge(\ell^*+1)$ and the nonnegative supermartingale of Lemma 5.1(c). ∎

*Why this matters.* The note's argument used "$P_{n_{\ell+1}}\ne\emptyset\Rightarrow M_\ell\ge2^{-W-L}$", which costs $2^L$. Here the unweighted count (Corollary 4.3(a)) and the **predictability of $W_{n_{\ell+1}}$** give the barrier at cost $2^{-c}$ only. Correlations between $M$ and the walk never enter: the barrier event $A_\ell$ is $\mathcal F_\ell$-measurable, and optional stopping does the rest.

**Theorem 5.3 (explicit bound) [proved].** For each class $C$ above, all integers $G$, $n_0\ge19$, $c$ with
$$T:=\lfloor G/2\rfloor\ge n_0+\ell_0,\qquad K:=\lfloor\log_2(T-\ell_0+1)\rfloor,\qquad 2^K\ge\ell_0,\ K>k,$$
we have
$$\mu\big(C\cap\{g_2\ge G\}\big)\ \le\ B_L(n_0)\ +\ n_0\,2^{-K}\ +\ 2^{-c}E_C\ +\ 2^{-k}\,\mathbb P\big(\mathrm{Bin}(K-k,\tfrac12)\le c+s_L-s(r_0)\big),$$
where $h_L(n):=\tfrac12(n-\log_2n-3L-4)$ and $B_L(n_0):=\sum_{i\ge1}2^{-\lfloor h_L(\max(n_0,\,i-\ell_0))\rfloor-1}$.

*Proof.* Let $\ell^*:=\max\{\ell:n_{\ell+1}\le T\}$ and $E_{\rm good}:=\Gamma_0\cap\dots\cap\Gamma_{\ell^*}$. Then
$$\mu(C\cap\{g\ge G\})\le\mu(E_{\rm good}^c)+\mu(C\cap\{g\ge G\}\cap E_{\rm good}\cap\mathrm{Hit})+\mu(C\cap E_{\rm good}\setminus\mathrm{Hit}).$$
- *Bad windows.* $\neg\Gamma_\ell$ gives $2M_{n_\ell+\ell_0}>V_{n_\ell}-3L-3\ge n_\ell-\log_2n_\ell-3L-4$ (Lemma 1.1(a)). So some $i\le n_\ell+\ell_0$ has $v(x+i)>h_L(n_\ell)\ge h_L(\max(n_0,i-\ell_0))$, since $h_L$ is nondecreasing for $n\ge2$. As $\mu\{v(x+i)>h\}=2^{-\lfloor h\rfloor-1}$, a union bound over $i$ gives $\mu(E_{\rm good}^c)\le B_L(n_0)$.
- *Barrier term.* On $\Gamma_\ell$, $M_N\le(V_n-3L-3)/2<V_n/2$. With Lemma 1.1(b), $V_N<N+V_N/2$, so $V_N<2N\le2T\le G$ for $N=n_{\ell+1}\le T$. On $\{g\ge G\}\cap E_{\rm good}$, Lemma 1.2 therefore gives $P_{n_{\ell+1}}\ne\emptyset$ for all $\ell\le\ell^*$. Proposition 5.2 bounds the second term by $2^{-c}\mathbb E[Y_0\mathbf 1_C]$. Since $Y_0\le2^LZ_{n_0}\mathbf 1_{\Gamma_0}$ (and $Y_0=Z_{n_0}\mathbf 1_{\Gamma_0}$ when $L=1$), and $\Gamma_0\subseteq\Gamma_*(n_0)$ (as $2M+3L+3\le V$ implies $V-L>M$), Corollary 3.3 gives $\mathbb E[Y_0\mathbf 1_C]\le E_C$.
- *Walk term.* Suppose $N_K>n_0$, and take $\ell$ with $n_\ell<N_K\le n_{\ell+1}$. Then $\delta:=n_{\ell+1}-N_K<\ell_0\le2^K$ and $n_{\ell+1}\le2^K+\ell_0-1\le T$, so $\ell\le\ell^*$. By Lemma 1.1(d),(f), $W_{n_{\ell+1}}=W_{N_K}+s(\delta)\le1-s(x\bmod2^K)+s_L$. Off $\mathrm{Hit}$ (and on $E_{\rm good}$) this is $>-c$, so $s(x\bmod2^K)\le c+s_L$ for integer $c$. Finally:
  - $\mu\{N_K\le n_0\}\le\sum_{N\le n_0}\mu\{x\equiv-N\ (2^K)\}=n_02^{-K}$;
  - on $C$, the digits of $x$ in positions $k,\dots,K-1$ are i.i.d. fair bits, and $s(x\bmod2^K)=s(r_0)+(\text{their sum})$.

  This gives the last two terms. ∎

**Corollary 5.4 (power law) [proved; constants evaluated by `code/constants.py`, `code/constants2.py`].** Take $\alpha=0.227$ ($<\alpha^*=0.22709$, so $1-H_2(\alpha)>\alpha$), $n_0=\lceil4\log_2G\rceil+3L+40$ and $c=\lfloor\alpha(K-k)\rfloor-s_L+s(r_0)$. Then for all $G\ge2$,
$$\mu(C_0\cap\{g_2\ge G\})\le29\,G^{-0.227},\quad\mu(C_2\cap\{g_2\ge G\})\le1325\,G^{-0.227},\quad\mu(C_6\cap\{g_2\ge G\})\le1.98\cdot10^5\,G^{-0.227}.$$

*Proof.*
- *Main terms.* By Chernoff, $\mathbb P(\mathrm{Bin}(N,\frac12)\le\alpha N)\le2^{-N(1-H_2(\alpha))}\le2^{-\alpha N}$. Also $2^{-c}\le2^{1+s_L-s(r_0)}2^{-\alpha(K-k)}$. For $G\ge4\ell_0$, $2^K>(T-\ell_0+1)/2\ge(G-2\ell_0)/4\ge G/8$. So the two main terms total at most
$$\big(2^{1+s_L-s(r_0)}E_C+2^{-k}\big)2^{\alpha k}(8/G)^{\alpha},$$
  i.e. $20.88$, $1316$ and $1.972\cdot10^5$ times $G^{-\alpha}$.
- *Side terms.* $B_L(n_0)+n_02^{-K}\le B_L(n_0)+8n_0/G$. Times $G^\alpha$, this is $\le3.7$ at every $G=2^j$, $10\le j<400$, computed with exact floor functions. Between consecutive powers of $2$ it is at most twice the neighbouring values, because $n_0(G)$ is increasing and $B_L$ is decreasing; so it is $\le7.4$ for all $G\ge2^{10}$. Adding this to the main-term constants gives $29$, $1325$ and $1.98\cdot10^5$. For $j\ge400$ it is $<10^{-6}$, since the terms decay like $G^{-1.7}$.
- *Small $G$.* For small $G$, where the hypotheses of Theorem 5.3 fail, use $\mu(C)\le CG^{-\alpha}$, which holds for $G\le2^{10}$ in all three cases.
- *Check.* A dense-grid evaluation ($G<2^{16}$ exhaustively, then 256 points per octave up to $2^{300}$) gives $\sup_G\min(\mu(C),\text{bound})\,G^{0.227}=17.8$, $1120$ and $1.68\cdot10^5$ (`logs/constants2.out`). ∎

**Corollary 5.5 (main result) [proved].** With $R=\mathbb Z_2\setminus(14+16\mathbb Z_2)$:
$$\mu\{x\in R:g_2(x)\ge G\}\le2.0\cdot10^5\,G^{-0.227}\qquad(G\ge4).$$
Equivalently (note Theorem 3.1(c)), the natural density of $\{a\ge1:\ a\not\equiv14\ (16),\ f(a,2)\ge v_2(a!)+G\}$ is at most $2.0\cdot10^5G^{-0.227}$.

*Proof.* $R$ is the union of $C_0,C_2,C_6$ and of the odd and $4\bmod8$ classes, on which $g_2\le3$. ∎

*Remarks.*
1. *Size of the constants.* The bound beats the trivial $\mu(C)$ only for very large $G$. With the optimised choice of $c$ (exact binomial tail, `code/constants_opt.py`), the thresholds are $G\approx2^{18}$ for $C_0$, $2^{29}$ for $C_2$ and $2^{44}$ for $C_6$ (`logs/constants_opt.out`). For all practical $G$ the census bound $\delta_G(2)\le\delta_{32}(2)=0.1016$ (note §4.7) is far better. The content of the result is the **existence of an explicit polynomial rate**, not its numerical value. The constants $E_{C_2},E_{C_6}$ come from crude bounds ($\rho\le2^L$, root counts $2^{L+1-k}$); numerically $\mathbb E[Z|C]\approx1$–$2$.
2. *Comparison with R1a's Claim 10.9.* Round-2 track R1a claimed, without a verified proof, a bound $\lesssim(3/4)^{D/2}\approx G^{-0.2075}$ on exactly these three classes, also excluding $14\bmod16$. Corollary 5.4 proves a bound of the same type and slightly better exponent ($0.227$) by a different route (Taylor certificates, Hensel first moment, predictable barrier). It does not use R1a's conservation lemmas. That both routes stop at $14\bmod16$ is not a coincidence; see §6.2.

## 6. What does not work, and the class $14+16\mathbb Z_2$

### 6.1 The planned first-moment bound $(3/4)^K$ and the correlation obstruction

The track plan proposed: bound $\delta_G$ by $\mathbb E[2^{W_{N_K}+L}M]\le C\,\mathbb E[2^{-s(x\bmod2^K)}]=C(3/4)^K\approx CG^{-0.415}$, "using that $W_{N_K}$ is determined by the low digits while $\mathbb E[M\mid\text{low digits}]$ is the initial value".

**The last claim is false as stated.** The martingale property holds along the digit filtration $\mathcal F_\ell=\sigma(x\bmod2^{V_{n_\ell}})$. The low digits $x\bmod2^K$ ($K\approx\log_2G$) are revealed during the windows with $n_\ell\lesssim K$, and those are exactly the windows in which $M$ moves. So $\mathbb E[M_\ell\mid x\bmod2^K]$ is $M_{\ell_K}$, the martingale at the time $\ell_K$ when the $K$ low digits are known. It is not the initial value, and it may be correlated with $s(x\bmod2^K)$.

The rigorous bounds available are:
- **(no decorrelation; what §5 does)** $\mathbb P(\text{survive})\le2^{-c}\,\mathbb E M_0+\mathbb P(s(x\bmod2^K)\le c+O(1))$, optimised at $c=\alpha^*K$. This gives $2^{-\alpha^*K}=G^{-0.227}$.
- **This is optimal for the method [sketch].** If the only information is $\mathbb E M\le1$ and $s\sim\mathrm{Bin}(K,\frac12)$, an adversarial coupling puts $M=2^{s-c}$ on $\{s\le\alpha^*K\}$. Then $\mathbb E\min(1,M2^{-(s-c)})$ is $\asymp2^{-\alpha^*K}$ up to polynomial factors. So no argument that only uses $(\mathbb EM,\ \text{law of }s)$ can beat $\alpha^*$.

**Proposition 6.1 (conditional improvement) [proved, conditional on H$_{\rm dec}$].** Use the windows of §5 with $n_0=\lceil4\log_2G\rceil+3L+40$, so that $V_{n_0}>K$ and $x\bmod2^K$ is $\mathcal F_0$-measurable. Suppose:
> **(H$_{\rm dec}$)** for some $A$ and all large $G$: $\ \mathbb E\big[Y_0\mathbf 1_C\,2^{-s(x\bmod2^K)}\big]\le A\,2^{-k}(3/4)^{K-k}$.

Then $\mu(C\cap\{g_2\ge G\})\le A'\,G^{-\log_2(4/3)}+O(G^{-1}\log G)$, i.e. exponent $0.415$.

*Proof.* Run Proposition 5.2 with the $\mathcal F_0$-measurable level $c(x):=s(x\bmod2^K)-1-s_L$. Its proof is unchanged, because $\{\sigma=\ell\}$ stays in $\mathcal F_\ell$. On $\{N_K>n_0\}\cap E_{\rm good}$, the walk argument of Theorem 5.3 shows that $\mathrm{Hit}$ occurs: $W\le1-s(r)+s_L=-c(x)$ at the window containing $N_K$. So
$$\mu(C\cap\{g\ge G\})\le B_L(n_0)+n_02^{-K}+2^{1+s_L}\,\mathbb E[2^{-s(x\bmod2^K)}Y_0\mathbf 1_C].$$
Apply H$_{\rm dec}$ and $2^{-K}\le8/G$. ∎

H$_{\rm dec}$ is a statement about how the population at time $\approx K$ correlates with the digit sum of the first $K$ digits. Via Proposition 3.2 it reduces to an equidistribution statement: the good roots of the $2^{n_0-1}$ polynomials $S_e$ ($e$ of length $n_0$) should be spread over the classes mod $2^K$, to within a constant factor in weighted form. We could not prove this. The heuristic of §7 suggests the *true* exponent is $1$, so even H$_{\rm dec}$ would not be sharp: it ignores the "variance" factor $(3/2)^{-K}$ (§7.1).

### 6.2 The shadow of $-2$: a triple root

On $14+16\mathbb Z_2=\{v(x+2)\ge4\}$ the certificates of Proposition 2.3 have no analogue, for a structural reason.

**Proposition 6.2 [proved].**
- (a) $S_{\{1,3\}}(x)=1+(x+1)+(x+1)(x+2)(x+3)=(x+2)^3$.
- (b) Consequently $\gamma_2(m)\ge3v(m-2)$ for every $m\ge3$, where $\gamma_2(m)=g_2(-m)$ (note §3.2).
- (c) For $x$ with $v(x+2)=t$ and any integer $m\ne2$, the Taylor inequality (Lemma 2.1) applied to $S_{\{1,3\}}$ at $-m$ always has its minimum at $i\ge2$ when $v(m-2)<t$. Hence no single integer point can force "slope $\le$ const" for the paths extending $\{1,3\}$.

*Proof.* (a) Expand. (b) $S_{\{1,3\}}(-m)=(2-m)^3$. (c) $S_{\{1,3\}}=(x+2)^3$ has $S'=3(x+2)^2$ (valuation $2t$) and $S^{[3]}=1$. At $-m$ with $v(x+m)=v(m-2)=:k<t$, the term $i=3$ has valuation $3k$, which is the valuation of $(2-m)^3$, while $i=1$ has valuation $2t+k>3k$. ∎

So near $-2$ the paths extending $(1,1,0,1)$ are perturbations of a **triple root**, and Lemma 2.2(ii) only peels off one factor of $(x+2)$. In the notation of Lemma 2.2 (with $e_2=0$, $e_3=1$), $\Phi_e(y)=-y^2/(1-y)+\sum_{k\ge2}e_{k+2}\pi_k(y)$, which has a double zero at $y=0$ for $e=(1,1,0,1,0,0,\dots)$.

The two families on $\{v(x+2)=t\}$, $t\ge4$, behave differently:
- *Family A ($e_2=1$, $e_3=0$).* As in Proposition 2.3(c), $\Phi_e(-4)$ has valuation $\le2$ and $v(y+4)=2$, so $\lambda_e=t$ **exactly** (for $V_n\ge2t+3$) [proved, same proof]. Hence Theorem 5.3 applies to family A on each class $\{v(x+2)=t\}$ with $L=t$ and $k=t+1$. Summing $\min(2^{-t-1},\ 2^{-c}2^{3t}+\dots)$ over $t$ gives a polynomial rate for the family-A survivors [sketch; the bookkeeping is as in §5, with $\ell_0=2t+2$ and $s(r_0)=t-1$].
- *Family B ($e_2=0$, $e_3=1$).* Slopes are unbounded on each class. Measured maximal slopes at depth $\le90$ and $V_n\ge3t+8$, 300 samples per $t$ (`logs/slope_depth.out`):
  - for odd $t=5,7,9,11$: exactly $2t+1$, in every sample;
  - for even $t=4,6,8,10,12$: mostly $2t+1$, with tails up to $22=5.5t$ ($t=4$) and $29$ ($t=6$).

  [heuristic] We expect these tails to be near-double roots of the renormalised function $\Omega=R-y^2/(1-y^2)$ obtained by peeling a second factor (§6.4), i.e. the same phenomenon one level down. This was not checked path by path.

### 6.3 How much of $\delta_G$ is covered

The share of survivors by class, among even $x$, from 60 000 exact samples to cap 512 (`code/gcap.py`, an independent Python reimplementation of the carry recursion; `logs/classsplit_cap512_run2.out`):

| $G$ | $2\delta_G$ (MC) | $0\bmod8$ | $2\bmod8$ | $6\bmod16$ | $14\bmod16$ |
|---|---|---|---|---|---|
| 16 | 0.3039 | 0.202 | 0.225 | 0.158 | 0.415 |
| 64 | 0.1280 | 0.154 | 0.164 | 0.100 | 0.582 |
| 128 | 0.0750 | 0.146 | 0.142 | 0.096 | 0.616 |
| 256 | 0.0408 | 0.131 | 0.143 | 0.096 | 0.631 |
| 512 | 0.0213 | 0.121 | 0.143 | 0.094 | 0.642 |

(Measure shares among even $x$: $1/4$, $1/4$, $1/8$, $1/8$; the remaining $1/4$ is $4\bmod8$, where $g_2=3$.)

The class $14\bmod16$ carries about $64\%$ of the survivors at $G=512$, and its share is levelling off. All classes appear to decay at the same rate, roughly $1/G$. So Corollary 5.5 controls about a third of the survivors. The rest is the triple-root region. Consistency check: $2\delta_{512}=0.0213$ here, against $2\times0.010682=0.02136$ from T4's 2-million-sample run.

### 6.4 What a full proof would need [sketch]

1. *Window identity without (W1).* The identity $\mathbb E_C\sum_{\rm children}\rho_N=2^{W_N-W_n}\rho_n$ holds for **any** window, including single steps, whenever $D+\lambda\le m-M_n$, $\lambda<m-M_N$ and $M_N<m$, even if $D\le\lambda$.
   - Proof: if $D\le\lambda$, aliveness is deterministic on $C$, and the child state is uniform on a coset of $2^{\lambda-D}$. Averaging $a_N$ over that coset reproduces the $f_2$-part of the decomposition $a_n(\tau_0)=2^{-(N-n)}\sum_{f_1}\mathbb P_{f_2}(q_{f_1}+2^DuQ^{(N)}_{f_2}\equiv\tau_0\ (2^\lambda))$.
   - We checked this algebra by hand but did not test it numerically. Only the *weighted* identity survives: for $D\le\lambda$ the unweighted count is not $2^{\Delta W}\rho$.
   - With it, every **frozen** slope ($\lambda\lesssim n-3\log_2n$) is a martingale class.
2. *Young paths.* Paths with $\lambda\gtrsim n$ (unfrozen) must be shown rare. Note Proposition 10.7 (subcritical decay $2^{-n/16}$ per window) does this for multiplicity-$\ge2$ classes with bounded higher derivative. On family B the relevant derivative is the second ($\Phi^{[2]}$ is a unit near the double root). The gap between frozen and young slopes, $\lambda\in(n/8,n)$, is the obstacle already met in round 2.
3. *A first-moment bound with unbounded slopes.* Proposition 3.2 must be replaced by a count of near-double roots, weighted by $2^{\lambda}$. By T4's annealed data this weighted count grows linearly (one unit per shadow depth), which is compatible with a polynomial rate but needs a proof.

A natural route is a **renormalisation at $-2$**. Write $x=-2+y$ and $S_e=y(y^2-1)\Omega_e$ for family B, with $\Omega_e=R_e(x)-y^2/(1-y^2)$ and $R_e=\sum_{k\ge1}e_{k+3}\pi_k(x+3)$. This is a problem of the same type at the odd point $x+3$, with a target of valuation $2t$. One would need to show that the renormalised problem is "subcritical relative to the original" by a factor that beats $2^{-t}$ (the measure of depth $t$). We did not attempt it.

## 7. Heuristic theory of the $1/G$ law; Kitamura's fit

Nothing in this section is proved.

### 7.1 A varying-environment model [heuristic]

Fix $x$ and condition on the **environment**, i.e. the valuations $v(x+i)$. These are a function of $O(\log n)$ low digits up to time $n$. The randomness that decides which paths survive a step comes from the digits of $x$ around position $V_n\approx n$ (Lemma 4.1(b)), which are fresh. So, given the environment, the population is approximately a branching process in a **varying environment** (BPVE):
- at a step $n\to n+1$ with $x+n+1$ odd ($D=0$), every alive path has exactly two alive children (deterministic doubling);
- at a step with $D\ge1$, a slope-$\ge1$ path keeps at most one child, with conditional mean $2^{1-D}$.

The mean population after $n$ steps is $\prod m_k=2^{W_n}$, so the critical walk of note §10.1 is the log-mean of the BPVE.

For a BPVE, the survival probability is governed (Agresti 1975; Kersting 2020, "A unifying approach to branching processes in a varying environment", J. Appl. Probab. 57; bibliographic details as recalled, not re-verified this round) by
$$\mathbb P(Z_n>0)\asymp\Big(\frac1{\mu_n}+\sum_{k<n}\frac{\nu_k}{\mu_{k+1}}\Big)^{-1},\qquad \mu_k=2^{W_k},$$
where $\nu_k=\mathbb E\xi_k(\xi_k-1)/m_k^2$. Here $\nu_k=\tfrac12$ at doubling steps and $\nu_k=0$ at the other steps ($\xi\in\{0,1\}$). This suggests the **predictor**
$$\mathbb P(g_2(x)\ge G\mid\text{environment})\approx\min\big(1,\kappa/A_G(x)\big),\qquad A_G(x):=\sum_{\substack{k<n_G(x)\\ x+k+1\ \mathrm{odd}}}2^{-W_{k+1}(x)},$$
where $n_G(x)$ is the first $n$ with $V_n\ge G$ and $\kappa$ is a fitted constant. Paths are **not** independent (they share the digit $w$), so $\kappa$ absorbs the correlation; it is the only free parameter.

**Scaling.**
- *Haar $x$.* Write $s_K:=s(x\bmod2^K)$. Between the records $N_K$ and $N_{K+1}$, $W_{N_K+\delta}=W_{N_K}+s(\delta)\approx-s_K+s(\delta)$ (Lemma 1.1(f)). Using the exact identity $\sum_{j<2^K}2^{-s(j)}=(3/2)^K$ (checked for $K\le14$; it follows from the product formula $\prod_{i<K}(1+\tfrac12)$),
$$A_G(x)\approx2^{s_K}(3/2)^K\ \text{(up to bounded factors, heuristically)},\qquad \mathbb E\big[1/A_G\big]\approx\mathbb E[2^{-s_K}]\,(2/3)^K=(3/4)^K(2/3)^K=2^{-K}\approx1/G.$$
  So **the exponent $1$ is $\log_2\frac43+\log_2\frac32$**. The first summand is the drift of the walk (the "first-moment" factor of the plan); the second is the accumulated variance at doubling steps.
- *Natural $a$.* Here $W_n=s(a+n)-s(a)\ge1-s(a)$, so the walk does **not** drift down. The bottleneck value $1-s(a)$ is reached at $n=2^K-a$ for every large $K$, as the plan observes. Then $A_G(a)\approx2^{s(a)-1}\big((a+G)/2\big)^{\log_2(3/2)}$, and
$$\mathbb P(g_2(a)\ge G)\approx2\kappa\,2^{-s(a)}\big((a+G)/2\big)^{-0.585}.$$
  This is $\asymp1/G$ (Haar-like) for $G\lesssim a$, and $\asymp2^{-s(a)}G^{-0.585}$ for $G\gg a$.

### 7.2 Tests [computer-assisted]

**(a) Haar.** Over 4000 random $x$ (`code/agresti.py`, `logs/agresti_haar.out`), $G\cdot\mathbb E[1/(2A_G)]$ is flat in $G$:

| $G$ | 16 | 64 | 256 | 1024 | 4096 | 16384 |
|---|---|---|---|---|---|---|
| $G\,\mathbb E[1/(2A_G)]$ | 2.11 | 2.09 | 2.11 | 2.10 | 2.10 | 2.12 |

The Monte Carlo values (T4) have $\delta_G\,G=5.5$–$5.8$ for $512\le G\le2046$, which fixes $\kappa\approx2.6$. With $\kappa=2.6$, the ratios predicted/MC are:

| $G$ | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |
|---|---|---|---|---|---|---|---|---|
| ratio | 2.05 | 1.71 | 1.33 | 1.14 | 1.06 | 1.01 | 0.96 | 0.99 |

The predictor captures the asymptotic $1/G$ law but overshoots at small $G$, where the $\min(1,\cdot)$ truncation and the halving structure (slopes $\ge1$ or $\ge3$) matter. This explains the slowly rising local exponent ($0.6$ at $G\approx64$, $1$ at $G\gtrsim700$) seen in all Monte Carlo runs.

**(b) Natural numbers, $N(A,G)=\#\{a\le A:g_2(a)\ge G\}$.** Observed values are T4's exact capped table (`survivors_NAG.tsv`); predicted values use $\kappa=2.6$, with no refitting (`logs/agresti2.out`):

| $A$ \ $G$ | 256 | 512 | 1024 | 2048 | 4094 |
|---|---|---|---|---|---|
| 256 (pred/obs) | 7.1/5 | 4.1/5 | 2.6/2 | 1.6/1 | 1.1/1 |
| 1024 | 23.1/15 | 12.4/11 | 7.2/6 | 4.2/4 | 2.6/2 |
| 4096 | 89.4/85 | 45.1/40 | 23.2/20 | 12.4/13 | 7.2/5 |

All entries agree within $2$ Poisson standard deviations; the largest deviation is $1.7\sigma$, at $A=1024$, $G=256$. Beyond the table: the predictor gives $N(4096,8192)\approx4.2$ and $N(4096,16384)\approx2.6$. The known exact deep values (T4 and Kitamura) give $3$ ($34$, $594$, $1102$) and $2$ ($34$ with $g=18412$, and $594$ with $g\ge16382$).

**(c) The regime $G\gg a$: counts of $g_2(a)\ge\lambda a$.** For even $16\le a\le4094/\lambda$ (`code/lambda_test.py`, `logs/lambda_test.out`):

| $\lambda$ | 1 | 2 | 4 | 8 | 16 | 32 | 64 |
|---|---|---|---|---|---|---|---|
| observed | 27 | 15 | 6 | 3 | 3 | 2 | 1 |
| predicted ($\kappa=2.6$) | 33.6 | 16.4 | 8.1 | 4.0 | 2.0 | 0.9 | 0.4 |

The counts fall more slowly than $\lambda^{-1}$ would allow. Normalising by $\sum1/a$, the "exponent-1" model's constant drifts from $9.6$ to $89$ across the table, while the "exponent-$0.585$" model's stays in $5.7$–$16$. The counts for $\lambda\ge16$ are, however, too small to be decisive.

### 7.3 Predictions stated as conjectures

**Conjecture 7.1 (Haar $1/G$ law).** $G\,\delta_G(2)\to c_2\in(0,\infty)$, with $c_2\approx5.5$–$6$. The local exponent of $\delta_G$ tends to $1$ from below; it is $\approx0.69$ on $[64,96]$ and $\approx1.0$ on $[768,2046]$ (T4).

**Conjecture 7.2 (exponent decomposition).** The decay exponent $1$ splits as
- $\log_2(4/3)$ from the environment walk, which is the best that any first-moment (annealed-walk) argument can give;
- $\log_2(3/2)$ from the variance accumulated at the doubling steps.

In particular, any proof of a rate better than $G^{-0.415}$ must use second-moment or genealogical information about the population, not just the mean $2^{W}$.

**Conjecture 7.3 (natural numbers, $G\gg a$).** For each fixed $\lambda>0$, the limit
$$q(\lambda):=\lim_{X\to\infty}\frac{\#\{a\le X:\ g_2(a)\ge\lambda a\}}{\log_2X}$$
exists and is positive. Moreover $q(\lambda)\asymp\lambda^{-\log_2(3/2)}=\lambda^{-0.585}$ as $\lambda\to\infty$, and $q(\lambda)\asymp\lambda^{-1}$ as $\lambda\to0$.

The $\log X$ arises because, under the predictor, each dyadic block $[2^{j-1},2^j)$ contributes $O(1)$: $\sum_{a<2^j}2^{-s(a)}=(3/2)^j$ while $a^{-0.585}\approx(2/3)^j$. This is a sharp, testable distinction from the Haar law: at fixed $\lambda$ the count grows only logarithmically, and its $\lambda$-dependence has exponent $0.585$, not $1$.

### 7.4 Kitamura's "$\sim11.5/G$" and the note's "$\approx0.7/\sqrt G$"

*What Kitamura wrote* (local copies fetched by T4 under `T4-computations/kitamura/`):
- README l.234: "The measured survival density decays like `~ 11.5/G`".
- witness_gallery.md l.135: "Survival to depth G has measured probability `~ 11.5/G`".
- determining_exact_values.md l.216–219, which attaches it to "the complete classification of all even classes with `g <= 24`… the surviving fraction decays like `~ 11.5/G`".

There is no definition, data table or script for the fit in the repository (T4). The phrase "even classes" indicates the fraction among **even** $a$, i.e. $2\delta_G$.

*Reconciliation.*
1. **Normalisation.** $11.5/G$ matches $2\delta_G$: $2\delta_GG=10.5$–$11.6$ for $256\le G\le2046$ (T4's Monte Carlo, `kitamura_11p5_comparison.tsv`). It does not match $\delta_G$ (a factor of $2$). At Kitamura's own level $G=24$, $2\delta_{24}\cdot24=6.2$, not $11.5$; so the fit must come from deeper data, presumably the $a\le256$ table to $G\approx1000$.
2. **Pre-asymptotics.** The note's $0.7/\sqrt G$ (§5, §10.1 Remark 4) was fitted on $8\le G\le254$. There the local exponent is $0.5$–$0.85$, and the predictor of §7.1 reproduces this transient. Beyond $G\approx500$ the decay is $\approx c/G$. So the two fits are the same curve seen in two windows, plus the factor $2$.
3. **Natural versus Haar.** The plan suggested that Kitamura's measurement (natural $a\le A$) differs from Haar because the bottleneck walk value is the constant $1-s(a)$. The model confirms the mechanism but locates its effect in the regime $G\gg a$, where it **slows** the decay to $G^{-0.585}$ (Conjecture 7.3). For $G\lesssim a$, natural numbers behave like Haar points. Kitamura's table ($a\le256$, $G\lesssim1024$) and T4's ($a\le4096$, $G\le4094$) are mostly in the crossover $G\approx A$, where both regimes give $\approx A/G$ up to constants (table 7.2(b)).

So there is no contradiction left. Kitamura's $11.5/G$ is $2\delta_G$ at $G\in[256,2000]$, the note's $0.7/\sqrt G$ is the small-$G$ transient, and the true Haar law is (conjecturally) $c_2/G$ with $c_2\approx5.5$–$6$.

## 8. Computations (all single-core Python 3, run 2026-10-21; paths relative to `e404r3/T2-p2-rate/`)

| script | purpose | command | time | output |
|---|---|---|---|---|
| `code/certs.py` | finite cases behind Prop. 2.3 (exact rationals; 8+4+4+64 cases) | `python3 certs.py` | <1 s | `logs/certs.out` |
| `code/gamma.py` | $\gamma_2(m)$, $3\le m\le26$ (exact subset sums) | `python3 gamma.py` | ~20 s | `logs/gamma.out` |
| `code/ftilde.py` | max valuation of $\Phi_e(-m)$ for $e_2\in\{0,1\}$, $m\le24$ | `python3 ftilde.py` | ~30 s | `logs/ftilde.out` |
| `code/check_cert.py` | slope bounds and $E[Z_n\mid C]$ on random points (BFS over all alive paths, 300-bit arithmetic) | `python3 check_cert.py 2 64 20000` | 8.4 s | `logs/check_cert_big.out` (also seed 1: `check_cert.out`) |
| `code/slope_depth.py` | max slope vs $t=v(x+2)$, $4\le t\le12$ | `python3 slope_depth.py 3 300 90` | 6.6 s | `logs/slope_depth.out` |
| `code/gcap.py` | exact $\min(g_2(x),\mathrm{cap})$ by the carry recursion with deduplication (independent Python reimplementation of T4's `p2add.c`); class split | `python3 gcap.py 5 60000 512` | 116 s | `logs/classsplit_cap512_run2.out` |
| `code/agresti.py` | predictor $A_G(x)$; Haar averages | `python3 agresti.py haar 4000` | ~40 s | `logs/agresti_haar.out` |
| `code/agresti2.py` | predictor vs MC and vs $N(A,G)$ | `python3 agresti2.py` | 9 s | `logs/agresti2.out` |
| `code/agresti3.py` | predictor for $G\gg A$ (local exponents $\to0.585$) | `python3 agresti3.py` | 190 s | `logs/agresti3_GggA.out` |
| `code/lambda_test.py` | counts $g_2(a)\ge\lambda a$ vs predictor (uses T4's `data/surv_cap4094.txt`) | `python3 lambda_test.py <T4>/data/surv_cap4094.txt` | ~60 s | `logs/lambda_test.out` |
| `code/constants.py`, `constants2.py`, `constants_opt.py` | evaluation of the explicit bound of Thm 5.3 / Cor 5.4 | `python3 constants2.py` etc. | ≤ 4 min | `logs/constants*.out` |

Validation of `gcap.py`:
- It reproduces small exact values: $g_2(4)=3$, $g_2(8)=6$, $g_2(22)=11$, $g_2(32)=6$, $g_2(36)=3$ and $g_2(40)=7$. Hence $f(32,2)=37$, $f(36,2)=37$ and $f(40,2)=45$, as in Kitamura's gallery. It also gives $g_2(38)\ge40$, consistent with $f(38,2)=828$.
- Its Monte Carlo $2\delta_{512}=0.0213$ agrees with T4's independent C code ($0.02136$).

Exploratory script `code/slopes.py` (first look at slopes, no logged output) is superseded by `slope_depth.py`.

## 9. Gaps, status, credit

**Status of the deliverables.**
1. *Explicit rate (target).* Achieved on $R=\mathbb Z_2\setminus(14+16\mathbb Z_2)$, i.e. for the natural density of $\{a\not\equiv14\ (16):f(a,2)\ge v_2(a!)+G\}$: $\le2\cdot10^5G^{-0.227}$ [proved] (Cor. 5.4–5.5). **Not achieved for $\delta_G(2)$ itself, and not even the fallback $C/\log G$.** The excluded class carries about $64\%$ of the survivors (§6.3). The obstruction is the triple root $(x+2)^3=S_{\{1,3\}}$ at $-2$ (Prop. 6.2), which produces unbounded slopes, and these defeat both the Taylor certificates and the Hensel first-moment bound.
2. *Discrepancy with Kitamura.* Explained (§7.4): a factor-$2$ normalisation ($11.5/G\approx2\delta_G$), a pre-asymptotic window for $0.7/\sqrt G$, and a new natural-number regime $G\gg a$ with exponent $\log_2(3/2)$ (Conj. 7.3), all supported by the predictor of §7.1 with one fitted constant [heuristic, computer-tested].

**Gaps and risks (explicit).**
- G1. Everything was checked only by the author (this AI instance), not by an independent referee. The points most worth a referee's attention are:
  - the measurability claims ($\Gamma_\ell$, $M_\ell$, $W_{n_{\ell+1}}$ are $\mathcal F_\ell$-measurable on $\Gamma_\ell$; Lemma 1.3, Lemma 5.1);
  - the Hensel-ball argument in Prop. 3.2 (that $V_n$ is constant on $B_r$, and the root count);
  - that Prop. 2.3 is applied only at times with $V_n\ge V_{\rm cert}$, and to every parent of every window;
  - the union bound for bad windows (monotonicity of $h_L$).
- G2. Prop. 2.3 relies on $8+4+4+64$ exact finite evaluations (`certs.py`). They are trivial in size and could be put in Lean. Lemma 2.2(i) re-derives the halving-lemma parity argument.
- G3. Lemma 3.1(a) is standard (proof included). Prop. 4.2 is the note's Prop. 10.6 (R1b), re-proved here; the round-2 numerical checks of that identity (note §10.1.1) apply.
- G4. The constants are crude (§5, Remark 1). The exponent $0.227$ is optimal for the method that uses only "$\mathbb EM\le C$ plus the law of the walk minimum" (§6.1), but is far from the conjectured $1$.
- G5. §6.2 "family A" rate and §6.4 (generalised window identity, renormalisation at $-2$) are sketches.
- G6. §7 is heuristic. The BPVE model ignores the dependence between paths (shared digits), and $\kappa$ is fitted. The Agresti/Kersting references are cited from memory and were not re-verified this round. Conjecture 7.3 is tested only on $a\le4096$ with small counts for $\lambda\ge8$.
- G7. Kitamura's definition of "$\sim11.5/G$" is inferred; the repository gives none.

**Credit.**
- The martingale framework (frozen-state weights $\rho$, window identity, environment walk $W$) is round-2 track R1b's proof of Theorem 10.1 (note §10.1). §4 re-proves its Lemma 10.5/Prop. 10.6.
- The split into $8\mathbb Z_2$, $2+8\mathbb Z_2$, $6+16\mathbb Z_2$ with $14+16\mathbb Z_2$ left over, and an exponent near $0.21$, appeared first in round-2 track R1a's **unverified** Claim 10.9 (note §10.1.4). Our proof is independent of R1a's lemmas, but the class split and the expectation that $14\bmod16$ is the hard case are R1a's.
- The halving lemma (tracks D/E, Lean), the shadows of negative integers $\gamma_p(m)$ (tracks A, C, D, E; note §3.2), and $g_2=3$ on $4+8\mathbb Z_2$ (Kitamura; Lean) are used as inputs.
- K. Kitamura (KitaKen1/erdos-404-p2-landscape, July 2026) supplied:
  - the determinacy lemma and the exact table for $a\le256$;
  - the deep certified values ($f(34,2)=18444$, $f(1102,2)=12633$, $f(3456,2)=8275$);
  - the critical-branching picture and the "$\sim11.5/G$" statement analysed in §7.4.
- Track T4 (round 3) supplied:
  - the Monte Carlo $\delta_G(2)$ to $G=2046$;
  - the exact capped $g_2(a)$ for $a\le4096$ and $N(A,G)$;
  - the deep values including $g_2(2210)=6261$;
  - the identification of $11.5/G$ with $2\delta_G$, used in §7.
- The strategy "nonnegative martingale + environment walk unbounded below ⟹ extinction" is the classical BPRE mechanism (Smith–Wilkinson 1969; Athreya–Karlin 1971; Afanasyev–Geiger–Kersting–Vatutin 2005), as credited in note §10.1 Remark 2. The BPVE survival estimate used heuristically in §7 is due to Agresti (1975) and, in sharp form, Kersting (2020).
- New here, as far as we know:
  - the integer-point Taylor certificates for slopes (Prop. 2.3);
  - the Hensel first-moment bound (Prop. 3.2);
  - the predictable-barrier stopping bound (Prop. 5.2);
  - the explicit rate (Thm 5.3, Cor. 5.4–5.5);
  - the triple-root obstruction (Prop. 6.2);
  - the BPVE predictor and the exponent decomposition $1=\log_2\frac43+\log_2\frac32$;
  - the $G\gg a$ prediction (Conj. 7.3).
