# Track R3Q (round 3, 2026-10-13, restarted): an explicit rate for $\delta_G(2)\to0$

## Headline

**For every $G\ge2^{3072}$: $\delta_G(2)=\mu\{x\in\mathbb Z_2:g_2(x)\ge G\}\le2^{1/80}\,G^{-1/80}$.** [computer-assisted]

The proof is complete and written out below. It uses two finite computations:
- an exhaustive certificate of size at most $2^{16}$ cases (Lemma 3), run by two programs that share no code;
- a check of an explicit closed-form inequality for $K=\log_2G\in[2400,4\cdot10^6]$. Beyond that range a one-line argument covers it.

The equivalent statement for natural numbers: the set of $a$ with $f(a,2)\ge v_2(a!)+G$ has natural density $\le2^{1/80}G^{-1/80}$.

This turns the qualitative Theorem 10.1 of the note ($\mu(K_2)=0$; Remark 10.8.4, §10.6 item 3) into an explicit rate. It also gives a second, quantitative proof of $\mu(K_2)=0$. That proof rests on the same martingale idea as track R1b's, but it is organised around explicit finite-time estimates rather than martingale convergence.

**The bound is meaningful only at astronomically large $G$.**
- *Corollary D (exact evaluation, two programs).* $\delta_G(2)\le0.1005$ for $G\ge2^{37}$. This is the first improvement on the census value $\delta_{32}(2)=0.10164$; the census is better for all $G<2^{37}$. The bound is $\le0.0910$ for $G\ge2^{40}$.
- The bound is $\le0.0456$ for $G\ge2^{448}$. This is the first time the $1/16$ floor of the class $14+16\mathbb Z_2$ is beaten.
- Further values: $\le4.9\cdot10^{-6}$ for $G\ge2^{1024}$, and $\le6.5\cdot10^{-13}$ for $G\ge2^{2048}$.
- The data (Monte Carlo $0.064,0.038,0.021$ at $G=64,128,254$; track R3N's survey $G\cdot P(g_2(a)\ge G)\approx4$ to $6$ over all $a$ for $256\le G\le131072$) point to $\delta_G(2)\approx c/G$. The proved exponent $1/80$ (about $0.02$ with optimised parameters) is far from $1$.

**Sharper statements on three residue classes.** Theorems A, A′ [computer-assisted, via Lemma 3 only]:
- On $C_0\cup C_2\cup C_6=8\mathbb Z_2\cup(2+16\mathbb Z_2)\cup(6+16\mathbb Z_2)$ every surviving path has a certified uniform slope ($1$, $3$, $3$). There, $\mu(C\cap\{g_2\ge G\})\le2^{1/7}G^{-1/7}$ for $G\ge2^{1024}$.
- Exact values: $\le0.0285$ in total at $G=2^{40}$; $\le7\cdot10^{-24}$ at $G=2^{448}$.
- With $g_2\le6$ on $10+16\mathbb Z_2$, $g_2\le3$ on $4+8\mathbb Z_2$ and $g_2=0$ on odd $x$, this proves $\delta_G(2)\le1/16+\varepsilon(G)$ with an explicit $\varepsilon(G)\to0$. This is a proved analogue of R1a's unverified Claim 10.9, with a weaker rate than that claim asserts.

**New lemmas, of some independent interest:**
- **Lemma 8 [proved].** If $x\equiv2\pmod4$, $j=v(x+2)$ and $v(S_e(x))\ge3j+1$, then $v(S_e'(x))\le2j$ or $v(S_e^{[2]}(x))\le j$. Hence, on the full-measure set $\Omega$ of note §10.1, every zero of an $F_e$ has multiplicity $\le2$, and multiplicity $1$ on $8\mathbb Z_2$ (remark after Lemma 8).
- **Lemma 9 [proved].** A window bound for the high-slope population, on coarse atoms $x+2^{V_n-M_n}\mathbb Z_2$.
- **Lemma 6(b) [proved].** The upper bound $\rho\le2^{(\lambda+\tilde M)/2-1}$ for the harmonic weights of note §10.1.

Nothing here bears on Q3, or on whether $f(a,2)<\infty$ for *every* $a$. A measure bound cannot see a countable set.

*Provenance.* An earlier R3Q instance was cut off after about two hours, leaving code but no report. This report re-derives every statement from scratch and uses that code only as a map. §9 lists what was confirmed and what was changed. Programs: `code/round3/R3Q/v2/`. Logs: `data/round3/R3Q/`.

*Status labels* follow the round-3 rules. "[proved]" means written out in full below and checked line by line by this track only; no referee or human has checked it yet.

---

## 0. Statements at a glance

| | statement | status |
|---|---|---|
| Lemma 1 | valuation facts; $V_n-M_n\ge\beta(n)=n-s(n)-\lfloor\log_2n\rfloor$; walk drop $W_{n_0+N_K}-W_{n_0}\le1-s(x+n_0\bmod2^K)$ | proved |
| Lemma 2 | truncation, backward integrality | proved |
| Lemma 3 | uniform slopes $1,3,3$ on $C_0,C_2,C_6$; $g_2\le6$ on $10+16\mathbb Z_2$, $\le3$ on $4+8\mathbb Z_2$ | computer-assisted (2 programs, exhaustive) |
| Lemma 4 | population bound $Z_n\le2^{\lceil n/2\rceil-1}$ | proved |
| Lemma 5 | one-step martingale identity for every slope | proved |
| Lemma 6 | weights: $\rho\le2^{\min(\lambda-1,\lfloor(\lambda+\tilde M)/2\rfloor-1)}$; $\rho\ge2^{-\lfloor\log_22\lambda\rfloor}$ on paths that survive $2\lambda$ steps | proved |
| Prop. 7 | stopped martingale bound with a digit-sum split | proved |
| Thm A | explicit bound on $C_0,C_2,C_6$ | computer-assisted (via Lemma 3) |
| Thm A′ | $\mu(C\cap\{g_2\ge2^K\})\le2^{-K/7}$, $K\ge1024$ | computer-assisted (Lemma 3; closed-form check on $[1024,4\cdot10^6]$) |
| Lemma 8 | no high slope with high second derivative near $-2$ | proved |
| Lemma 9, Cor. 9′ | U-window bound on coarse atoms | proved |
| Prop. 10 | the high-slope population dies (split by $v(x+2)$) | proved |
| Thm B | explicit bound on $C_{14}$ | proved |
| Cor. D | staircase for $\delta_G(2)$ (table in §7) | computer-assisted (exact evaluation, 2 programs) |
| Thm C | $\delta_{2^K}(2)\le2^{-K/80}$ for all $K\ge3072$ | computer-assisted (Lemma 3; closed-form check on $[2400,4\cdot10^6]$) |
## 1. Setting, notation, and what is used from the note

Notation follows note §10.1.
- $v=v_2$; $s(n)$ is the binary digit sum; $\mu$ is Haar probability measure on $\mathbb Z_2$; $\mathrm{Bin}(N)$ is a binomial variable with $N$ trials and success probability $1/2$ (with $P(\mathrm{Bin}(N)<k)=1$ if $N\le0<k$).
- $\pi_j(x)=\prod_{i\le j}(x+i)$, $V_n=v(\pi_n(x))$, $W_n=n-V_n$, $M_n=\max_{i\le n}v(x+i)$. For a polynomial $F$, $F^{[i]}=F^{(i)}/i!$.
- A *path* of length $n$ is $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$; $S_e(X)=\sum_{j<n}e_j\pi_j(X)$. It is *alive at $n$* if $v(S_e(x))\ge V_n(x)$; then its *target* is $\tau_n(e)=-S_e(x)/\pi_n(x)\in\mathbb Z_2$ and its *slope* is $\lambda_e=v(S_e'(x))$. $P_n(x)$ is the set of paths alive at $n$ and $Z_n=|P_n|$.
- New in this report: $\beta(n)=n-s(n)-\lfloor\log_2n\rfloor$ and $z(n)=\lceil n/2\rceil-1$.
- Classes: $C_0=8\mathbb Z_2$, $C_2=2+16\mathbb Z_2$, $C_6=6+16\mathbb Z_2$, $C_{14}=14+16\mathbb Z_2$.
- $x$ always denotes an element of $\mathbb Z_2$ that is not a negative integer. The excluded set is countable, so it does not affect any measure.

From the note we use only: the normal form ($f(a,2)=v_2(a!)+g_2(a)$, Lemma 1.1), locality and $\delta_G(2)=\mu\{g_2\ge G\}$ non-increasing in $G$ (Theorem 3.1), and Taylor's formula with integral coefficients (Lemma 10.2(f)). Every other ingredient is proved below, including the statements re-used from note Lemma 10.2 and Lemma 10.5(b).

## 2. Elementary lemmas

**Lemma 1 (valuations) [proved].** Let $x$ be even.
- (a) $V_{n+i}-V_n\ge i-s(i)$ and $V_{n+i}-V_n\ge\lfloor i/2\rfloor$ for all $n,i\ge0$. In particular $V_n\ge n-s(n)$.
- (b) For $y\in\mathbb Z_2$ (not a negative integer), $L\ge1$ and $\mu_L:=\max_{1\le i\le L}v(y+i)$: $\sum_{i=1}^Lv(y+i)\le L-1+\mu_L$, and $\le L+\mu_L-2$ if $L\ge2$ and $\mu_L\ge1$. The same holds with every $v(y+i)$ replaced by $\min(v(y+i),c)$ and $\mu_L$ by $\max_i\min(v(y+i),c)$, for any $c\ge1$. In particular $V_n\le n+M_n-2$ for $n\ge2$.
- (c) $V_n-M_n\ge\beta(n)$ for $n\ge1$. Both $n\mapsto V_n-M_n$ and $n\mapsto\beta(n)$ are non-decreasing. Also $n-2\lfloor\log_2n\rfloor-1\le\beta(n)\le n-1-\lfloor\log_2n\rfloor$.
- (d) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$ for $j\ge1$, $i\ge0$.
- (e) *(Walk drop.)* Let $n_0\ge0$, $K\ge1$, $z=x+n_0$, $r=z\bmod2^K$ and $N_K=\min\{N\ge1:2^K\mid z+N\}$. Then $W_{n_0+N_K}-W_{n_0}\le1-s(r)$, and $N_K\le2^K$.

*Proof.*
- (a) Among $i$ consecutive elements of $\mathbb Z_2$ at least $\lfloor i/2^\ell\rfloor$ are divisible by $2^\ell$; summing over $\ell\ge1$ gives $v(i!)=i-s(i)$. Since $x$ is even, $x+n+t$ is even for every $t\in[1,i]$ with $n+t$ even, and there are at least $\lfloor i/2\rfloor$ of these.
- (b) For each $\ell\ge1$ at most $\lceil L/2^\ell\rceil\le(L-1)/2^\ell+1$ of the $y+i$ are divisible by $2^\ell$, and none is divisible by $2^{\mu_L+1}$. So the sum is at most $(L-1)(1-2^{-\mu_L})+\mu_L$. This is $<L-1+\mu_L$, and for $L\ge2,\mu_L\ge1$ it is strictly smaller than the integer $L-1+\mu_L$, hence $\le L+\mu_L-2$. For the truncated version, $\sum_i\min(v(y+i),c)=\sum_{\ell=1}^{c}\#\{i:2^\ell\mid y+i\}$, and the count vanishes for $\ell$ above the truncated maximum. Apply the general case with $y=x$, $L=n$.
- (c) Let $c_\ell=\#\{i\le n:2^\ell\mid x+i\}\ge\lfloor n/2^\ell\rfloor$. Then $V_n=\sum_{\ell\ge1}c_\ell$ and $M_n=\#\{\ell\ge1:c_\ell\ge1\}$. So $V_n-M_n=\sum_\ell(c_\ell-1)^+\ge\sum_{\ell=1}^{\lfloor\log_2n\rfloor}(\lfloor n/2^\ell\rfloor-1)=n-s(n)-\lfloor\log_2n\rfloor$.
  - Monotonicity of $V-M$: if $v(x+n+1)\le M_n$ then $V$ grows and $M$ does not; otherwise $V_{n+1}-M_{n+1}=V_n+v(x+n+1)-v(x+n+1)=V_n\ge V_n-M_n$.
  - Monotonicity of $\beta$: $s(n+1)=s(n)+1-t$ where $t$ is the number of trailing ones of $n$. So $\beta(n+1)-\beta(n)=t-[n+1\text{ is a power of }2]$. If $n+1=2^a$ then $t=a\ge1$. Either way the difference is $\ge0$.
  - The two-sided bound follows from $1\le s(n)\le\lfloor\log_2n\rfloor+1$.
- (d) $\pi_j^{[i]}=\pi_j\,e_i\big(\tfrac1{x+1},\dots,\tfrac1{x+j}\big)$, where $e_i$ is the elementary symmetric function, and each $1/(x+t)$ has valuation $\ge-M_j$.
- (e) If $r=0$ then $N_K=2^K$, $\sum_{i<2^K}v(z+i)=v((2^K-1)!)=2^K-1-K$ and $v(z+2^K)\ge K$. If $r>0$ then $N_K=2^K-r$; for $1\le i<N_K$ we have $v(z+i)=v(r+i)<K$, so $\sum_{i<N_K}v(z+i)=v((2^K-1)!)-v(r!)=2^K-1-K-r+s(r)$, and $v(z+N_K)\ge K$. In both cases $V_{n_0+N_K}-V_{n_0}\ge N_K-1+s(r)$, i.e. $W_{n_0+N_K}-W_{n_0}\le1-s(r)$. ∎

Parts (a), (d), (e) are note Lemma 10.2(a),(e),(d) in a slightly sharper form; (c) is new here (the earlier R3Q code states it as "Lemma 2(e)").

**Lemma 2 (truncation; backward integrality) [proved].**
- (a) If $g_2(x)\ge G$ and $V_N(x)\le G$, then $P_N(x)\neq\emptyset$.
- (b) If $(e,f)$ is alive at $N$, then $e$ is alive at every $n\le N$.
- (c) If $M_T(x)\le G-T+2$ and $T\ge2$, then $V_T(x)\le G$.

*Proof.* (a) Take $B$ with $v(S_B(x))\ge G$ and let $e$ be the length-$N$ word of $B\cup\{0\}$ truncated. Then $S_e=S_B-\sum_{j\in B,j\ge N}\pi_j$, and $2^{V_N}\mid\pi_j$ for $j\ge N$, so $v(S_e(x))\ge\min(G,V_N)=V_N$. (b) $S_e=S_{(e,f)}-\sum_{n\le j<N}f_j\pi_j$ with $2^{V_n}\mid\pi_j$. (c) Lemma 1(b). ∎

**Lemma 3 (slope certificates) [computer-assisted, two programs; reduction proved].**
- (i) If $x\in C_0$ and $n\ge6$, every $e\in P_n(x)$ has $\lambda_e=1$.
- (ii) If $x\in C_2$ and $n\ge8$, every $e\in P_n(x)$ has $\lambda_e=3$.
- (iii) If $x\in C_6$ and $n\ge10$, every $e\in P_n(x)$ has $\lambda_e=3$.
- (iv) $g_2\le6$ on $10+16\mathbb Z_2$, $g_2\le3$ on $4+8\mathbb Z_2$, and $g_2=0$ on odd $x$.

Consequently, for $G\ge7$: $\{g_2\ge G\}\subseteq C_0\cup C_2\cup C_6\cup C_{14}$, and $\delta_G(2)=\sum_{c\in\{0,2,6,14\}}\mu(C_c\cap\{g_2\ge G\})$.

*Finite checks* (exhaustive over the listed residues of $x$ and all words $e_1,\dots,e_{n_0-1}$, with $e_0=1$):
- (a) $x\equiv0\pmod 8$, $x\bmod16$, $n_0=6$: $16\mid S_e(x)\Rightarrow v(S_e'(x))=1$;
- (b) $x\equiv2\pmod{16}$, $x\bmod2^7$, $n_0=8$: $2^7\mid S_e(x)\Rightarrow v(S_e'(x))=3$;
- (c) $x\equiv6\pmod{16}$, $x\bmod2^{11}$, $n_0=10$: $2^{11}\mid S_e(x)\Rightarrow v(S_e'(x))=3$;
- (d) $x\equiv10\pmod{16}$, $x\bmod2^7$, $n_0=6$: no $e$ has $2^7\mid S_e(x)$;
- (e) $x\equiv4\pmod8$, $x\bmod16$, $n_0=4$: no $e$ has $16\mid S_e(x)$.

The checks find $4$, $32$ and $128$ qualifying words in (a), (b), (c), all with the stated slope, and none in (d), (e). They were run by `code/round3/R3Q/v2/cert_classes.py` (direct integer products) and `cert_classes_sympy.py` (sympy-expanded polynomials, Horner evaluation, gmpy2 valuations), which share no code; both report 0 violations (log `data/round3/R3Q/certificates.log`, under 5 s each).

*Reduction.* $S_e(x)\bmod2^c$ depends only on $x\bmod2^c$ and $S_e'(x)\bmod2^{\lambda+1}$ only on $x\bmod2^{\lambda+1}$, since both are integer polynomials. For $x\equiv0\pmod8$: $v(x+2)=1$, $v(x+4)=2$, $v(x+6)=1$, so $V_6=4$ and $M_6=2$. For $x\equiv2\pmod{16}$: $v(x+2),\dots,v(x+8)=2,1,3,1$, so $V_8=7$, $M_8=3$. For $x\equiv6\pmod{16}$: $v(x+2),\dots,v(x+10)=3,1,2,1,\ge4$, so $V_{10}=7+v(x+10)\ge11$ and $V_{10}-M_{10}=7$. Let $n\ge n_0$ and $e\in P_n(x)$. By Lemma 2(b), $e|_{n_0}$ is alive at $n_0$, so $v(S_{e|n_0}(x))\ge V_{n_0}\ge c$, and the check gives $v(S'_{e|n_0}(x))=\lambda$. For $j\ge n_0$, Lemma 1(c),(d) give $v(\pi_j'(x))\ge V_j-M_j\ge V_{n_0}-M_{n_0}\ge\lambda+1$ ($2>1$, $4>3$, $7>3$). Hence $\lambda_e=\lambda$.
- For (iv) with $x\equiv10\pmod{16}$: $v(x+2),v(x+4),v(x+6)=2,1,\ge4$, so $V_6\ge7$. If $g_2(x)\ge7$, the truncation argument of Lemma 2(a) gives a word of length $6$ with $v(S_e(x))\ge\min(7,V_6)=7$, which contradicts (d).
- For $x\equiv4\pmod8$: $V_4\ge1+3=4$, and (e) excludes $g_2\ge4$ in the same way.
- For odd $x$, every $S_B(x)$ is odd. ∎

Parts (iv) are consistent with the known value set $g_2\in\{0,3\}\cup[6,\infty]$ (note Cor. 3.7.1(iii)). Part (i)–(iii) are the "anchor" facts that the earlier R3Q instance had tested numerically (`check_anchor.py`, L1, L2, L2'); here they are certified exhaustively.

**Lemma 4 (population bound) [proved].** For even $x$ and $n\ge2$: $Z_n\le2^{z(n)}$.

*Proof.* Fix $e_0=1$. The coefficients $\pi_1(x),\dots,\pi_{n-1}(x)$ have valuations $V_1=0\le V_2\le\dots\le V_{n-1}$, which increase strictly at every even index. Take one index for each distinct valuation that is $<V_n$; there are at least $r=\lfloor n/2\rfloor$ of them (the levels $V_1$ and $V_j$ for even $j\le n-1$, minus possibly the top level when $n$ is odd and $V_{n-1}=V_n$). For any fixed values of the other coordinates, two different choices of the chosen coordinates give sums that differ by $\sum\varepsilon_j\pi_j$ with $\varepsilon\in\{-1,0,1\}$ not all zero; its lowest-valuation term is unique, so the difference has valuation $<V_n$. So at most one choice makes $2^{V_n}\mid S_e(x)$, and $Z_n\le2^{(n-1)-r}=2^{z(n)}$. ∎
## 3. The slope martingale

*Weights.* For $\lambda\ge1$, $n\ge0$ and $s\in\mathbb Z/2^\lambda$ put
$$\rho^{(\lambda)}_n(s)=2^\lambda\,\mathbb P\Big(Q_n\equiv s\pmod{2^\lambda}\Big),\qquad Q_n=\sum_{i\ge0}g_i\,c_i,\quad c_i=\frac{\pi_{n+i}(x)}{\pi_n(x)}=\prod_{t=1}^{i}(x+n+t),$$
with $g_0,g_1,\dots$ independent fair bits. Let $I=I_n(\lambda)=\min\{i:V_{n+i}-V_n\ge\lambda\}$; by Lemma 1(a), $I\le2\lambda$. Since $v(c_i)=V_{n+i}-V_n$ is non-decreasing, $Q_n\bmod2^\lambda=\sum_{i<I}g_ic_i\bmod2^\lambda$. For a path $e\in P_n$ with slope $\lambda\ge1$ write $\rho_n(e)=\rho_n^{(\lambda)}(\tau_n(e)\bmod2^\lambda)$. These are the weights of note §10.1 (there with $2\lambda$ explicit terms; the law mod $2^\lambda$ is the same).

**Lemma 5 (one-step identity) [proved].** Let $x$ be even, $m=V_n(x)$, $D=v(x+n+1)$, and let $e\in P_n(x)$ have slope $\lambda\ge1$ with
$$\lambda+D\le m-M_n,\qquad \lambda<m-M_n .$$
Let $C=x+2^m\mathbb Z_2$ with normalised Haar measure and write $x'=x+2^mw$, $w\in\mathbb Z_2$. Then:
- (a) $V_n,M_n$, $V_{n+1}=m+D$ and $P_n$ are the same at every $x'\in C$; $e$ has slope $\lambda$ at every $x'\in C$; every child $(e,f)$ alive at $n+1$ at any $x'$ has slope $\lambda$.
- (b) $\tau_n(e,x')\equiv\tau_n(e,x)-\omega^{-1}S_e'(x)\,w\pmod{2^{m-M_n}}$, where $\omega=\pi_n(x)/2^m\in\mathbb Z_2^\times$. In particular $\tau_n(e,x')\bmod2^\lambda$ is constant on $C$.
- (c) $\displaystyle\mathbb E_{x'\in C}\sum_{f\in\{0,1\}:\,(e,f)\in P_{n+1}(x')}\rho_{n+1}\big((e,f)\big)\;=\;2^{1-D}\,\rho_n(e).$

*Proof.*
- (a) The hypotheses give $M_n<m$ and $D<m$, so $v(x'+i)=v(x+i)$ for $i\le n+1$. Aliveness at $n$ depends on $S(x')\bmod2^m$, and $S_e'(x')\equiv S_e'(x)\pmod{2^m}$ with $\lambda<m$. A child has $S'_{(e,f)}=S_e'+f\pi_n'$, and $v(\pi_n'(x'))\ge m-M_n>\lambda$ by Lemma 1(d).
- (b) By Taylor's formula, $S_e(x')=S_e(x)+2^mwS_e'(x)+2^{2m}w^2R$ with $R\in\mathbb Z_2$, and $\pi_n(x')=\pi_n(x)(1+E)$ with $1+E=\prod_{i\le n}(1+2^mw/(x+i))\equiv1\pmod{2^{m-M_n}}$. Hence $\tau_n(e,x')=\big[\tau_n(e,x)-\omega^{-1}S_e'(x)w-\omega^{-1}2^mw^2R\big](1+E)^{-1}$, and the claim follows. Since $\lambda\le m-M_n$ and $2^\lambda\mid S_e'(x)$, the class mod $2^\lambda$ is constant.
- (c) Let $t(w)=\tau_n(e,x')\bmod2^{\lambda+D}$. By (b) and $\lambda+D\le m-M_n$, $t(w)=\tau_0-2^\lambda\beta w\bmod2^{\lambda+D}$ with $\tau_0=\tau_n(e,x)$ and $\beta$ a unit. So, as $w$ ranges over $\mathbb Z_2$, $t$ is uniformly distributed on the $2^D$ residues $\equiv\tau_0\pmod{2^\lambda}$. The child $(e,f)$ is alive at $n+1$ iff $v\big(\pi_n(x')(f-\tau_n(e,x'))\big)\ge m+D$, i.e. iff $t\equiv f\pmod{2^D}$; its target is $(\tau_n-f)/(x'+n+1)$, whose class mod $2^\lambda$ is $(t-f)/(2^Du)$, where $u=(x'+n+1)/2^D\bmod2^\lambda$ is constant on $C$ (because $D+\lambda\le m$). Also $\rho_{n+1}^{(\lambda)}$ depends only on $x'\bmod2^\lambda$ (each $c_i\bmod2^\lambda$ does), hence is constant on $C$. So the left side equals
$$2^{-D}\sum_{f}\ \sum_{\substack{t\bmod 2^{\lambda+D}\\ t\equiv\tau_0\,(2^\lambda),\ t\equiv f\,(2^D)}}\rho^{(\lambda)}_{n+1}\Big(\frac{t-f}{2^Du}\Big)=2^{\lambda-D}\sum_f\mathbb P\big(2^Du\,Q'\equiv\tau_0-f\pmod{2^\lambda}\big),$$
  where $Q'$ has the law of $Q_{n+1}$: substitute $t=f+2^Dy$, $y\bmod2^\lambda$, and note that $t\equiv\tau_0\ (2^\lambda)$ iff $2^Dy\equiv\tau_0-f$. On the other hand $Q_n=g_0+(x+n+1)Q'$ with $g_0$ independent of $Q'$, so $\rho_n^{(\lambda)}(\tau_0)=2^\lambda\cdot\tfrac12\sum_f\mathbb P\big(2^DuQ'\equiv\tau_0-f\big)$. Multiplying by $2^{1-D}$ gives the same expression. ∎

This is the one-step version of note Proposition 10.6(iii) (there over windows of length $\ge2\lambda+2$, with the same weights). The window hypotheses (W1)–(W3) of the note are replaced by the single-step condition $\lambda+D\le m-M_n$.

**Lemma 6 (weights) [proved].** Let $x$ be even and $\lambda\ge1$.
- (a) $\rho_n^{(\lambda)}$ depends only on $n$, $\lambda$ and $x\bmod2^\lambda$; its average over $s$ is $1$. If $\lambda=1$ then $\rho\equiv1$.
- (b) $\rho_n^{(\lambda)}(s)\le2^{\min(\lambda-1,\ \lfloor(\lambda+\tilde M)/2\rfloor-1)}$, where $\tilde M=\max_{1\le i\le2\lambda}\min(v(x+n+i),\lambda)$.
- (c) If $e\in P_n$ has slope $\lambda$ and some extension of $e$ is alive at $n+2\lambda$, then $\rho_n(e)\ge2^{-\lfloor\log_2(2\lambda)\rfloor}$.

*Proof.*
- (a) Each $c_i\bmod2^\lambda$ is an integer polynomial in $x$. The average is $2^\lambda\cdot2^{-\lambda}\sum_s\mathbb P(\cdot)=1$. For $\lambda=1$, $Q_n\equiv g_0+(\text{independent})\pmod2$ is uniform, so $\rho=2\cdot\frac12=1$.
- (b) The levels $v(c_i)$, $0\le i<I$, are all $<\lambda$; they take at least $r=1+\#\{1\le i\le I-1:x+n+i\text{ even}\}\ge\lceil I/2\rceil$ distinct values. Choose one index per level. Conditioning on the other bits, the subset sums of the chosen $c_i$ are pairwise distinct mod $2^\lambda$ (the lowest-level term of a difference dominates), so $\mathbb P(Q_n\equiv s)\le2^{-r}$ and $\rho\le2^{\lambda-r}$. Since $r\ge1$, $\rho\le2^{\lambda-1}$. If $I\ge2$, Lemma 1(b) (truncated at $c=\lambda$) gives $\lambda\le\sum_{i\le I}\min(v(x+n+i),\lambda)\le I+\tilde M-2$, so $r\ge\lceil(\lambda+2-\tilde M)/2\rceil$ and $\rho\le2^{\lfloor(\lambda+\tilde M)/2\rfloor-1}$. If $I=1$ then $\tilde M\ge\lambda$ and the second bound is implied by the first.
- (c) Let $(e,f)$ be alive at $n+2\lambda\ge n+I$. Then $(e,f|_{I})$ is alive at $n+I$ (Lemma 2(b)), i.e. $\tau_n(e)\equiv\sum_{i<I}f_ic_i\pmod{2^{V_{n+I}-V_n}}$, and $V_{n+I}-V_n\ge\lambda$. So the event $\{g_i=f_i,\ i<I\}$ (probability $2^{-I}$) forces $Q_n\equiv\tau_n(e)\pmod{2^\lambda}$, and $\rho_n(e)\ge2^{\lambda-I}$. By minimality of $I$ and Lemma 1(a), $(I-1)-s(I-1)\le V_{n+I-1}-V_n\le\lambda-1$, so $\lambda-I\ge-s(I-1)$. Finally $I-1\le2\lambda-1$, and every integer in $[0,2\lambda-1]$ has digit sum $\le\lfloor\log_2(2\lambda)\rfloor$. ∎

The earlier R3Q code used the lower bound $\rho\ge1/(4\lambda)$ (its "(6a)"), which follows from (c), and the upper bound $\rho\le2^\lambda$. The upper bound (b), with exponent about $(\lambda+\tilde M)/2$, is new here; it halves the dominant cost in Theorem B.

*Slope $0$.* For $\lambda=0$ put $\rho^{(0)}\equiv1$. Lemma 5 holds for $\lambda=0$ with the same proof (the state space is trivial), and Lemma 6(c) holds trivially. Lemma 6(b) is only used for $\lambda\ge1$; where all slopes $\le\Lambda$ are tracked (Theorem B), the bound used is $\ge1$, so slope-$0$ paths are covered too.

**Proposition 7 (stopped martingale bound) [proved].** Let $C=r_C+2^a\mathbb Z_2$ ($a\ge3$) be a class of even numbers. Let $\Lambda\ge1$, $n_s\ge4$ with $\beta(n_s)\ge\Lambda+1$ and $n_s-s(n_s)\ge a$; let $T$, $K_t\ge a$ with $n_s+2^{K_t}+2\Lambda\le T$; let $k\ge1$ and $m_1\in\{0\}\cup[a,\min(n_s-s(n_s),K_t)]$. For $x\in C$ and $n\ge n_s$ let $Q_n(x)=\{e\in P_n(x):\lambda_e\le\Lambda\}$. Let $\rho_*>0$ satisfy $\rho_n(e)\ge\rho_*$ for every $e\in Q_n$ with an extension alive at $n+2\Lambda$ (by Lemma 6, $\rho_*=1$ works if $\Lambda=1$ and $\rho_*=2^{-\lfloor\log_2 2\Lambda\rfloor}$ always works). Let $E\subseteq C$ be a union of sets $x+2^{V_{n_s}(x)}\mathbb Z_2$, and $R\ge\sum_{e\in Q_{n_s}(x)}\rho_{n_s}(e)$ on $E$ a constant. Write $\ell_0=s((r_C+n_s)\bmod2^a)$. Then $\mu\big(E\cap\{Q_T\neq\emptyset\}\big)$ is at most
$$\sum_{i=n_s+1}^{T}\mu\big(C\cap\{v(x+i)\ge\beta(i-1)-\Lambda+1\}\big)\;+\;\mu(C)\Big[\mathbb P\big(\mathrm{Bin}(K_t-m_1)<k\big)+\frac{2^{1-k}R}{\rho_*}\,2^{-\ell_0}(3/4)^{m_1-a}\Big]$$
if $m_1\ge a$, and the same with the bracket replaced by $\mathbb P\big(\mathrm{Bin}(K_t-a)<k-\ell_0\big)+2^{1-k}R/\rho_*$ if $m_1=0$.

*Proof.*
- *Failures.* Say step $n\ge n_s$ *fails* if $v(x+n+1)\ge V_n-M_n-\Lambda+1$. Since $V_n-M_n\ge\beta(n)\ge\beta(n_s)\ge\Lambda+1$ (Lemma 1(c)), a step that does not fail satisfies the hypotheses of Lemma 5 for every $e\in Q_n$. A failing step has $v(x+n+1)\ge\beta(n)-\Lambda+1$. Let $\sigma$ be the first failing step ($\infty$ if none).
- *Filtration.* For $n\ge n_s$ let $\mathcal A_n$ be the partition into the sets $x+2^{V_{\min(n,\sigma)}(x)}\mathbb Z_2$ (on $\{\sigma<n\}$ the atom is frozen at time $\sigma$). This is a nested sequence of partitions: whether step $n$ fails depends on $x\bmod2^{V_n}$, and if it does not fail then $v(x+n+1)<V_n$, so $V_{n+1}$ is constant on the atom. Let $\mathcal F_n=\sigma(\mathcal A_n)$.
- *Martingale.* Put $Y_n=2^{-W_n}\sum_{e\in Q_n}\rho_n(e)$ and $\hat Y_n=Y_{\min(n,\sigma)}$. By Lemma 5(a),(b) and Lemma 6(a) (the slopes are $<V_n$), $\hat Y_n$ is constant on atoms of $\mathcal A_n$. On $\{\sigma>n\}$, $Q_{n+1}$ is the disjoint union of the alive children of the $e\in Q_n$: such children keep slope $\lambda_e$ (Lemma 5(a)), while a child of a path of slope $>\Lambda$ has slope $\ge\min(\Lambda+1,v(\pi_n'))\ge\min(\Lambda+1,V_n-M_n)=\Lambda+1$. Lemma 5(c) and $W_{n+1}=W_n+1-D$ give $\mathbb E[Y_{n+1}\mid\mathcal F_n]=Y_n$. So $(\hat Y_n)$ is a non-negative martingale.
- *Stopping.* Let $\tau=n_s+N_{K_t}(x+n_s)\le n_s+2^{K_t}$ (Lemma 1(e)) and $\hat\tau=\min(\tau,\sigma)$. On an atom of $\mathcal A_t$ with $\sigma\ge t$, the event $\{\tau=t\}$ is decided: if $2^{K_t}\mid x+t$ then $V_t\ge K_t$, and otherwise $v(x+t)\le M_t<V_t$. So $\hat\tau$ is a bounded stopping time and $\mathbb E[\hat Y_{\hat\tau}\mid\mathcal F_{n_s}]=Y_{n_s}$.
- *Survival forces weight.* Suppose $Q_T(x)\ne\emptyset$ and $\sigma\ge\tau$. Take $e'\in Q_T$. Its prefix $e=e'|_\tau$ is alive (Lemma 2(b)) and has slope $\le\Lambda$, since otherwise all its descendants would have slope $>\Lambda$. As $\tau+2\Lambda\le T$, $e$ has an extension alive at $\tau+2\Lambda$, so $\rho_\tau(e)\ge\rho_*$ and $\hat Y_{\hat\tau}=Y_\tau\ge2^{-W_\tau}\rho_*$. By Lemma 1(e), $W_\tau\le W_{n_s}+1-s(r)$ with $r=(x+n_s)\bmod2^{K_t}$.
- *Digit split, $m_1\ge a$.* Write $s(r)=s_{\rm lo}+s_{\rm hi}$, where $s_{\rm lo}$ is the digit sum of $r\bmod2^{m_1}$. On $E\cap\{Q_T\ne\emptyset,\ \sigma\ge\tau,\ s_{\rm hi}\ge k\}$ we get $1\le\hat Y_{\hat\tau}2^{W_{n_s}+1-s_{\rm lo}-k}/\rho_*$. Hence
$$\mathbf 1_E\mathbf 1\{Q_T\ne\emptyset\}\le\mathbf 1_C\mathbf 1\{\sigma<\tau\}+\mathbf 1_C\mathbf 1\{s_{\rm hi}<k\}+\mathbf 1_E\,\hat Y_{\hat\tau}\,2^{W_{n_s}+1-s_{\rm lo}-k}/\rho_* .$$
  - $\{\sigma<\tau\}$ requires a failing step $n\in[n_s,T)$, which gives the first sum.
  - For $x$ uniform in $C$, the digits of $x+n_s$ in positions $m_1,\dots,K_t-1$ are uniform (as $m_1\ge a$), so $\mu(C\cap\{s_{\rm hi}<k\})=\mu(C)\mathbb P(\mathrm{Bin}(K_t-m_1)<k)$.
  - $\mathbf 1_E$, $W_{n_s}$ and $s_{\rm lo}$ are $\mathcal F_{n_s}$-measurable, because $m_1\le n_s-s(n_s)\le V_{n_s}$. Conditioning on $\mathcal F_{n_s}$ turns the last term into $\mathbf 1_E2^{1-s_{\rm lo}-k}\sum_{e\in Q_{n_s}}\rho_{n_s}(e)/\rho_*\le\mathbf 1_E2^{1-s_{\rm lo}-k}R/\rho_*$. Finally $\int_C2^{-s_{\rm lo}}d\mu=\mu(C)2^{-\ell_0}(3/4)^{m_1-a}$, since the low $a$ digits of $x+n_s$ are those of $r_C+n_s$ and the next $m_1-a$ digits are uniform.
- *Digit split, $m_1=0$.* Use $\{s(r)<k\}$ directly: on $C$, $s(r)=\ell_0+\mathrm{Bin}(K_t-a)$ in law, and on $\{s(r)\ge k\}$ we get $1\le\hat Y_{\hat\tau}2^{W_{n_s}+1-k}/\rho_*$. ∎

*Remark.* The digits in positions below $m_1$ pay for the crude population bound $2^{z(n_s)}$ through the factor $(3/4)^{m_1-a}$. The digits above $m_1$ enter an unconditional binomial tail. The earlier R3Q code used the full-digit version only ($m_1=0$); the split is a small improvement and is optimised numerically.

## 4. Theorem A: the three classes with certified uniform slope

For $C=C_c$ with $(r_C,a,\lambda_C,n_C)=(0,3,1,6)$, $(2,4,3,8)$, $(6,4,3,10)$ for $c=0,2,6$, put $\ell_C=0$ if $\lambda_C=1$ and $\ell_C=(\lambda_C-1)+\lfloor\log_2(2\lambda_C)\rfloor=4$ if $\lambda_C=3$.

**Theorem A [proved, given Lemma 3, which is computer-assisted].** Let $C$ be one of $C_0,C_2,C_6$. Let $G\ge7$, $T\le G$, $n_s\ge n_C$ with $\beta(n_s)\ge\lambda_C+1$, $K_t=\lfloor\log_2(T-n_s-2\lambda_C)\rfloor\ge a$, $k\ge1$, and $m_1\in\{0\}\cup[a,\min(n_s-s(n_s),K_t)]$. Then
$$\mu(C\cap\{g_2\ge G\})\le A_1+A_4+A_5,$$
- $A_1=\sum_{i=1}^{T}\mu\big(C\cap\{v(x+i)\ge G-T+3\}\big)$;
- $A_4=\sum_{i=n_s+1}^{T}\mu\big(C\cap\{v(x+i)\ge\beta(i-1)-\lambda_C+1\}\big)$;
- $A_5=\mu(C)\big[\mathbb P(\mathrm{Bin}(K_t-m_1)<k)+2^{1-k+\ell_C+z(n_s)-\ell_0}(3/4)^{m_1-a}\big]$ if $m_1\ge a$, and $A_5=\mu(C)\big[\mathbb P(\mathrm{Bin}(K_t-a)<k-\ell_0)+2^{1-k+\ell_C+z(n_s)}\big]$ if $m_1=0$, where $\ell_0=s((r_C+n_s)\bmod2^a)$.

*Proof.* Outside the set counted by $A_1$, $M_T\le G-T+2$, so $V_T\le G$ (Lemma 2(c)), and $g_2(x)\ge G$ gives $P_T(x)\ne\emptyset$ (Lemma 2(a)). By Lemma 3, every path alive at a time $n\ge n_C$ has slope $\lambda_C$, so $P_n=Q_n$ with $\Lambda=\lambda_C$. Apply Proposition 7 with $E=C$, $\Lambda=\lambda_C$, $R=2^{z(n_s)}\rho_{\max}$ (Lemma 4), where $\rho_{\max}=1$ and $\rho_*=1$ for $\lambda_C=1$ (Lemma 6(a)), and $\rho_{\max}=2^{\lambda_C-1}=4$, $\rho_*=2^{-2}$ for $\lambda_C=3$ (Lemma 6(b),(c)). Then $R/\rho_*=2^{z(n_s)+\ell_C}$. ∎

All terms are explicit finite sums; $A_1,A_4$ are evaluated exactly, using $\mu(C\cap\{v(x+i)\ge b\})=2^{-b}[2^a\mid r_C+i]$ for $b>a$, $=2^{-a}[2^b\mid r_C+i]$ for $b\le a$. Beyond $3000$ explicit terms, the tail of $A_4$ is bounded by $\sum_{i\ge i_0}2^{-(\beta(i-1)-\lambda+1)}\le2.05\cdot2^{\lambda+1}(i_0-1)^22^{-i_0}$, which follows from Lemma 1(c) (each term is $\le2^{\lambda+1}(i-1)^22^{-i}$, and the ratio of consecutive terms is $\le0.5116$ for $i_0\ge88$).

**Numbers** (exact evaluation of the bound, parameters chosen by a float search; `bounds.py A`, verified by `verify_bounds.py`). Each entry is an absolute measure; $\mu(C_0)=1/8$ and $\mu(C_2)=\mu(C_6)=1/16$.

| $G$ | $\mu(C_0\cap\{g\ge G\})\le$ | $\mu(C_2\cap\cdot)\le$ | $\mu(C_6\cap\cdot)\le$ | sum |
|---|---|---|---|---|
| $2^{32}$ | 9.94e-3 | 4.09e-2 | 2.20e-2 | 7.28e-2 |
| $2^{36}$ | 7.09e-3 | 2.40e-2 | 1.24e-2 | 4.35e-2 |
| $2^{40}$ | 8.04e-3 | 1.37e-2 | 6.81e-3 | 2.85e-2 |
| $2^{48}$ | 2.25e-3 | 4.13e-3 | 1.98e-3 | 8.36e-3 |
| $2^{64}$ | 2.01e-4 | 3.47e-4 | 1.76e-4 | 7.24e-4 |
| $2^{448}$ | 9.8e-25 | 1.2e-24 | 4.5e-24 | 6.7e-24 |
| $2^{1024}$ | (rule A′) $2^{-162.0}$ | $2^{-159.0}$ | $2^{-170.9}$ | |

(The search is heuristic, so the table is not monotone in every column. Since $\mu(C\cap\{g\ge G\})$ is non-increasing in $G$, any entry also bounds every larger $G$.)

**Theorem A′ (rate on the three classes) [proved, given Lemma 3].** For each $C\in\{C_0,C_2,C_6\}$ and every $K\ge1024$:
$$\mu(C\cap\{g_2\ge2^K\})\le2^{-K/7}.\qquad\text{Hence }\mu(C\cap\{g_2\ge G\})\le2^{1/7}G^{-1/7}\text{ for all }G\ge2^{1024}.$$

*Proof.* Apply Theorem A with $T=2^K-2K-12$, $n_s=\lfloor K/6\rfloor$, $m_1=0$ and $k=\ell_C+z(n_s)+\lceil K/6\rceil+1$. Then $K_t=K-1$, and:
- $A_1\le(T2^{-a}+1)2^{-2K-15}\le2^{-K-15}$.
- $A_4\le\sum_{i\ge n_s+1}2^{-(\beta(i-1)-\lambda+1)}\le2.05\cdot2^{\lambda}n_s^22^{-n_s}\le0.911K^22^{-K/6}$, using $\lambda\le3$ and $K/6-1\le n_s\le K/6$.
- $A_5\le\mu(C)\big[\mathbb P(\mathrm{Bin}(K-1-a)\le k-1)+2^{-\lceil K/6\rceil}\big]$. Here $k-1\le4+n_s/2+K/6+1\le K/4+5$ and $K-1-a\ge K-5$, so $q:=(k-1)/(K-1-a)\le(K/4+5)/(K-5)\le0.26$. The Chernoff bound $\mathbb P(\mathrm{Bin}(N)\le qN)\le2^{-N(1-H(q))}$ ($q\le1/2$, $H$ the binary entropy) gives $\le2^{-0.1732(K-5)}$, since $1-H(0.26)=0.17325$.

So $\mu(C\cap\{g_2\ge2^K\})$ is at most $2^{-K-15}+0.911K^22^{-K/6}+\mu(C)\big(2^{-0.1732(K-5)}+2^{-K/6}\big)$. `rule_A.py` checks that this closed form is $\le2^{-K/7}$, and that $q\le0.26$, for every integer $K\in[1024,4\cdot10^6]$ (no violation; about 30 s). For $K>4\cdot10^6$ each of the four terms is below $2^{-K/7-3}$, because $K/6-K/7=K/42$ exceeds $2\log_2K+3$ there and the other exponents exceed $K/6$. The statement for general $G$ follows from monotonicity in $G$. The script also evaluates the exact bound of Theorem A under this rule at $K=1024,1536,2048,4096$ and confirms that it lies below the closed form. ∎

For comparison: R1a's unverified Claim 10.9 asserts about $G^{-0.2075}$ on $C_0\cup C_2\cup C_6$. Theorem A′ proves $G^{-1/7}\approx G^{-0.143}$, and the optimised exact evaluations behave like $G^{-0.16}$ to $G^{-0.18}$ ($2^{-80}$ at $G=2^{448}$; $2^{-671}$ at $G=2^{4096}$ under the rule).

## 5. Large slopes near $-2$

**Lemma 8 (no high slope with high second derivative) [proved].** Let $x\equiv2\pmod4$, $j=v(x+2)$ (so $j\ge2$), and let $e$ be a path with $v(S_e(x))\ge3j+1$. Then $v(S_e'(x))\le2j$ or $v(S_e^{[2]}(x))\le j$.

*Proof.* Put $h=x+2$ and $S=S_e$. Suppose $v(S'(x))\ge2j+1$ and $v(S^{[2]}(x))\ge j+1$. Write $c_k=S^{[k]}(-2)\in\mathbb Z$, the coefficients of $S$ as a polynomial in $h$. Taylor's formula at $x$ evaluated at $-2=x-h$ gives:
- $c_0=\sum_i(-h)^iS^{[i]}(x)\equiv-h^3S^{[3]}(x)\pmod{2^{3j+1}}$, since the terms $i=0,1,2$ and $i\ge4$ have valuation $\ge3j+1$. But $c_0=S(-2)=1-e_1\in\{0,1\}$, and $c_0=1$ is impossible (the right side is $\equiv0\bmod2^{3j}$). So $e_1=1$, $c_0=0$, and $S^{[3]}(x)$ is even.
- $c_1=\sum_i(-h)^i(i+1)S^{[i+1]}(x)$. The terms have valuations $\ge2j+1$ ($i=0$), $\ge2j+2$ ($i=1$), $\ge2j+1$ ($i=2$, as $S^{[3]}(x)$ is even) and $\ge3j\ge2j+1$ ($i\ge3$). So $v(c_1)\ge2j+1$.
- $c_2=\sum_i(-h)^i\binom{i+2}2S^{[i+2]}(x)$ has terms of valuation $\ge j+1$ ($i=0$), $\ge j+1$ ($i=1$, $S^{[3]}(x)$ even) and $\ge2j\ge j+1$ ($i\ge2$), so $v(c_2)\ge j+1$. Likewise $c_3=\sum_i(-h)^i\binom{i+3}3S^{[i+3]}(x)\equiv S^{[3]}(x)\equiv0\pmod 2$.

On the other hand, $\pi_1(x)=h-1$ and $\pi_j(x)=(h-1)h\,P_{j-2}(h)$ for $j\ge2$, with $P_m(h)=(h+1)\cdots(h+m)=\sum_k\alpha_{m,k}h^k$. So, with $a_m=e_{m+2}$ and $\alpha_k=\sum_ma_m\alpha_{m,k}$,
$$S=h+(h^2-h)\sum_ma_mP_m(h),\qquad c_1=1-\alpha_0,\quad c_2=\alpha_0-\alpha_1,\quad c_3=\alpha_1-\alpha_2 .$$
Hence $\alpha_0\equiv1\pmod{2^{2j+1}}$, in particular mod $16$ (as $j\ge2$), and $\alpha_2\equiv\alpha_1\equiv\alpha_0\equiv1\pmod2$.
- Now $\alpha_{m,0}=m!\equiv1,1,2,6,8,8,0,0,\dots\pmod{16}$ for $m=0,1,2,\dots$.
- Modulo $2$, $P_m(h)\equiv(h+1)^{\lceil m/2\rceil}h^{\lfloor m/2\rfloor}$, so $\alpha_{m,2}$ is odd exactly for $m\in\{2,4,5\}$ and $\alpha_2\equiv a_2+a_4+a_5\pmod2$.
- From $\alpha_0\equiv a_0+a_1+2a_2+6a_3+8(a_4+a_5)\pmod{16}$: mod $2$, $a_0+a_1=1$. Then mod $4$, $2(a_2+a_3)\equiv0$, so $a_2=a_3$. Then mod $16$, $1+8a_2+8(a_4+a_5)\equiv1$, so $a_2+a_4+a_5$ is even. This contradicts $\alpha_2$ odd. ∎

*Remark.* The earlier R3Q code tested this statement numerically ("L4" in `check_anchor.py`); we found no proof on disk, so the proof above is our own. Together with Lemma 3(i), it implies that every zero $F_e(x)=0$ (infinite word $e$) at a point $x$ of the full-measure set $\Omega$ of note §10.1 has multiplicity $1$ if $x\in8\mathbb Z_2$ and multiplicity $\le2$ if $x\equiv2\pmod4$ (apply the lemma to the truncations, using note Lemma 10.3). In the language of note §10.1, the classes $K^{k,L}$ with $k\ge3$ are empty on $\Omega$. *[proved; a side remark, not used below]*

**Lemma 9 (window bound for the high-slope population, coarse atoms) [proved].** Let $x\equiv2\pmod4$, $j=v(x+2)$, $n<N$, $L=N-n$, $m=V_n(x)$, $D=V_N(x)-m$ and $m'=m-M_n(x)$. Let $\Theta_n\le\Theta_N$ be integers, and for $y$ put $U_t(y)=\{e\in P_t(y):\lambda_e(y)\ge\Theta_t\}$. Assume:
- (H1) $\max(M_n,\,2j+1,\,D+M_n)\le\Theta_n\le m'$;
- (H2) $M_N<m'$ and $D\le m'-M_N$;
- (H3) $\Theta_N\le2m'$;
- (H4) $m\ge3j+1$ and $m-2M_N>j$.

Let $x'=x+2^{m'}w$ with $w$ Haar-distributed in $\mathbb Z_2$. Then:
- (a) $v(x'+i)=v(x+i)$ for $i\le N$, and $U_n(x')=U_n(x)$.
- (b) If $e''\in U_N(x')$ then $e''|_n\in U_n(x)$.
- (c) For $e\in U_n(x)$, the set $F_0(e)=\{f\in\{0,1\}^L:(e,f)\in P_N(x')\}$ does not depend on $w$, and $|F_0(e)|\le2^{L-\lfloor(L-1)/2\rfloor}$.
- (d) $\mathbb E_w|U_N(x')|\le|U_n(x)|\cdot2^{\,L-\lfloor(L-1)/2\rfloor-\max(0,\ \Theta_N-m'-1-j)}$.

*Proof.*
- (a) The first claim follows from $M_N<m'$. For $e\in U_n(x)$, Taylor gives $S_e(x')-S_e(x)=\sum_{i\ge1}(2^{m'}w)^iS_e^{[i]}(x)$. The $i=1$ term has valuation $\ge m'+\Theta_n\ge m'+M_n=m$, and the others $\ge2m'\ge m$ (as $m'\ge\Theta_n\ge M_n$). So $e$ is alive at $n$ at $x'$. Also $S_e'(x')-S_e'(x)$ has valuation $\ge m'\ge\Theta_n$, so $\lambda_e(x')\ge\Theta_n$. Thus $U_n(x)\subseteq U_n(x')$. The hypotheses are the same at $x'$, so the reverse inclusion holds as well.
- (b) $e=e''|_n$ is alive at $n$ (Lemma 2(b)). Moreover $S_e'=S_{e''}'-\sum_kf_k\pi'_{n+k}$, where $v(\pi'_{n+k}(x'))\ge V_{n+k}-M_{n+k}\ge m'\ge\Theta_n$ (Lemma 1(c),(d)) and $v(S'_{e''}(x'))\ge\Theta_N\ge\Theta_n$.
- (c) $S_e(x')\equiv S_e(x)\pmod{2^{\min(m'+\Theta_n,2m')}}$, and both exponents are $\ge V_N=m+D$ by (H1) and (H2) ($2m'-m=m-2M_n\ge m'-M_N\ge D$). Also $\pi_{n+k}(x')=\pi_{n+k}(x)\prod_{t\le n+k}(1+2^{m'}w/(x+t))\equiv\pi_{n+k}(x)\pmod{2^{m+m'-M_N}}$, and $m+m'-M_N\ge V_N$ by (H2). So aliveness at $N$ of every $(e,f)$ is the same at $x'$ as at $x$. For the size: the coefficients $\pi_{n+k}(x)$, $0\le k<L$, have non-decreasing valuations, strictly increasing at each $k\ge1$ with $x+n+k$ even. So at least $\lfloor(L-1)/2\rfloor$ distinct values lie below $V_N$, and the injectivity argument of Lemma 4 applies.
- (d) Fix $f\in F_0(e)$ and $c=(e,f)$. Taylor gives $S_c'(x')\equiv S_c'(x)+2^{m'+1}wS_c^{[2]}(x)\pmod{2^{2m'}}$. Lemma 8 applies to $e$ at $x$ ($v(S_e(x))\ge m\ge3j+1$, $\lambda_e\ge\Theta_n\ge2j+1$), so $\kappa:=v(S_e^{[2]}(x))\le j$. The added terms $\pi^{[2]}_{n+k}(x)$ have valuation $\ge V_{n+k}-2M_{n+k}\ge m-2M_N>j$ (Lemma 1(d), (H4)), so $v(S_c^{[2]}(x))=\kappa$. As $\Theta_N\le2m'$, the event $\lambda_c(x')\ge\Theta_N$ says $S_c'(x)+2^{m'+1+\kappa}uw\equiv0\pmod{2^{\Theta_N}}$ with $u$ a unit. This confines $w$ to at most one class modulo $2^{\Theta_N-m'-1-\kappa}$ when that exponent is positive, an event of probability $\le2^{-(\Theta_N-m'-1-\kappa)}\le2^{-(\Theta_N-m'-1-j)}$. Summing over $e\in U_n(x)$ and $f\in F_0(e)$, and using (b), gives (d). ∎

The bound (d) is attained in tests (ratio $1.000$). The earlier R3Q code stated and tested a version on the fine atoms $x+2^{m}\mathbb Z_2$ ($m=V_n$), where the exponent loses an extra $M_n$ per window. Conditioning only on the digits below $m'=V_n-M_n$ removes that loss: the high-slope paths stay alive and keep their slope under perturbation at level $m'$, so the coarser atom is legitimate. (The control in `test_uwin.py` shows that an even coarser atom, $\lceil V_n/2\rceil-1$, does change $U_n$.)

**Corollary 9′ [proved].** Let $M^*\ge M_N(x)$ and assume
$$\text{(W1) }\beta(n)\ge2M^*+1,\qquad\text{(W2) }L+2M^*\le\beta(n)+1,\qquad\text{(W3) }\beta(N)\le2\beta(n).$$
Then Lemma 9 applies with $\Theta_t=\beta(t)$, and the factor in (d) is at most $2^{\varphi_j(n,N)}$, where $\varphi_j(n,N)=L-\lfloor(L-1)/2\rfloor-\max(0,\beta(N)-n+1-j)$.

*Proof.* Note $j\le M_n\le M^*$.
- (H1): $\beta(n)\ge2M^*+1\ge\max(M_n,2j+1)$. By Lemma 1(b), $D\le L-1+M_N\le L-1+M^*$, so $D+M_n\le L-1+2M^*\le\beta(n)$. And $\beta(n)\le V_n-M_n=m'$ by Lemma 1(c).
- (H2): $M_N\le M^*<\beta(n)\le m'$, and $D\le L-1+M^*\le\beta(n)-M^*\le m'-M_N$.
- (H3): $\beta(N)\le2\beta(n)\le2m'$.
- (H4): $m\ge\beta(n)+M_n\ge2M^*+1+j\ge3j+1$, and $m-2M_N\ge\beta(n)+M_n-2M^*\ge M_n+1>j$.
- The factor: $m'\le n-2$ by Lemma 1(b). ∎

**Proposition 10 (the high-slope population dies) [proved].** Let $M^*\ge4$ and let $n_1<\dots<n_t$ be such that each window $[n_i,n_{i+1}]$ satisfies (W1)–(W3). Then
$$\mu\big(C_{14}\cap\{U_{n_t}\ne\emptyset,\ M_{n_t}\le M^*\}\big)\le B_3:=\sum_{J=4}^{M^*}2^{-J-1}\,2^{\,z(n_1)+\sum_{i<t}\varphi_J(n_i,n_{i+1})},\qquad U_t=\{e\in P_t:\lambda_e\ge\beta(t)\}.$$

*Proof.* Let $C_J=\{x\in C_{14}:v(x+2)=J\}$, so that $\mu(C_J)=2^{-J-1}$. If $v(x+2)>M^*$ then $M_{n_t}>M^*$, so only $4\le J\le M^*$ matter. Put $\tilde Z_i=|U_{n_i}|\cdot\mathbf 1\{M_{n_i}\le M^*\}$.
- On $C_J\cap\{M_{n_i}\le M^*\}$, the sets $x+2^{V_{n_i}(x)-M_{n_i}(x)}\mathbb Z_2$ form a partition: all valuations $v(x+t)$, $t\le n_i$, are $\le M^*<\beta(n_i)\le V_{n_i}-M_{n_i}$, so they are constant on the set.
- On such an atom, $\mathbf 1\{M_{n_{i+1}}\le M^*\}$ is constant, because a valuation $>M^*$ at some $t\le n_{i+1}$ is either $<m'$ and then common to the atom, or $\ge m'>M^*$ everywhere on it.
- Where the indicator is $1$, Corollary 9′ (with $j=J$) gives $\mathbb E_{\rm atom}\tilde Z_{i+1}\le2^{\varphi_J(n_i,n_{i+1})}\tilde Z_i$. Here $\tilde Z_i$ is constant on the atom by Lemma 9(a).
- $\tilde Z_{i+1}$ vanishes off $\{M_{n_i}\le M^*\}$. Integrating over $C_J$ gives $\int_{C_J}\tilde Z_{i+1}\le2^{\varphi_J}\int_{C_J}\tilde Z_i$, and $\int_{C_J}\tilde Z_1\le2^{z(n_1)}\mu(C_J)$ by Lemma 4. Conclude with Markov's inequality and sum over $J$. ∎

*Remark (why the split by $J$ matters).* With $j$ replaced by its worst case $M^*$, every window would pay $M^*$. Weighting the class $\{v(x+2)=J\}$ by its measure $2^{-J-1}$ reduces the cost to roughly $(t-2)M^*$ over $t-1$ windows. Together with the coarse atoms, this is what moves the threshold of Theorem B from about $G=2^{1000}$ (earlier R3Q code) to about $G=2^{450}$.

## 6. Theorem B: the class $C_{14}=14+16\mathbb Z_2$

**Theorem B [proved].** Let:
- $G\ge7$ and $T\le G$;
- $M^*\ge4$ and $M_f\ge M^*$;
- $n_1<\dots<n_t=:n_U$ with every window satisfying (W1)–(W3) for $M^*$, and $\Lambda:=\beta(n_U)-1$;
- $n_s\ge n_U$ with $n_s-s(n_s)\ge4$, and $K_t=\lfloor\log_2(T-n_s-2\Lambda)\rfloor\ge4$;
- $k\ge1$ and $m_1\in\{0\}\cup[4,\min(n_s-s(n_s),K_t)]$.

Then $\mu(C_{14}\cap\{g_2\ge G\})\le B_1+B_2+B_3+B_4+B_5$, where $B_3$ is as in Proposition 10 and:
- $B_1=\sum_{i\le T}\mu\big(C_{14}\cap\{v(x+i)\ge G-T+3\}\big)$;
- $B_2=\sum_{i\le n_U}\mu\big(C_{14}\cap\{v(x+i)\ge M^*+1\}\big)+\sum_{n_U<i\le n_s+2\Lambda}\mu\big(C_{14}\cap\{v(x+i)\ge M_f+1\}\big)$;
- $B_4=\sum_{i=n_s+1}^{T}\mu\big(C_{14}\cap\{v(x+i)\ge\beta(i-1)-\Lambda+1\}\big)$;
- $B_5=\tfrac1{16}\big[\mathbb P(\mathrm{Bin}(K_t-m_1)<k)+2^{1-k+\ell_B+z(n_s)-\ell_0}(3/4)^{m_1-4}\big]$ if $m_1\ge4$, and $B_5=\tfrac1{16}\big[\mathbb P(\mathrm{Bin}(K_t-4)<k-\ell_0)+2^{1-k+\ell_B+z(n_s)}\big]$ if $m_1=0$. Here $\ell_B=\min\big(\Lambda-1,\lceil(\Lambda+M_f)/2\rceil-1\big)+\lfloor\log_2(2\Lambda)\rfloor$ and $\ell_0=s((14+n_s)\bmod16)$.

*Proof.*
- *Slopes after $n_U$.* For $t\ge n_U$, if $e\in P_t$ has $\lambda_e\ge\Lambda+1=\beta(n_U)$, then its prefix at $n_U$ lies in $U_{n_U}$. Indeed, a prefix slope $<\beta(n_U)$ would be inherited, since $v(\pi_j')\ge V_j-M_j\ge\beta(n_U)$ for $j\ge n_U$. So on $\{U_{n_U}=\emptyset\}$ we have $P_t=Q_t$ (slopes $\le\Lambda$) for all $t\ge n_U$.
- *Decomposition.* Let $G_f=\{\max_{1\le i\le2\Lambda}\min(v(x+n_s+i),\Lambda)\le M_f\}$. This event depends only on $x\bmod2^{\Lambda}$, and $\Lambda<\beta(n_s)\le V_{n_s}$, so $E:=C_{14}\cap G_f$ is a union of atoms $x+2^{V_{n_s}}\mathbb Z_2$. Then
$$C_{14}\cap\{g_2\ge G\}\subseteq\{M_T>G-T+2\}\cup\{M_{n_U}>M^*\}\cup G_f^c\cup\{U_{n_U}\ne\emptyset,M_{n_U}\le M^*\}\cup\big(E\cap\{Q_T\ne\emptyset\}\big),$$
  all intersected with $C_{14}$. The first three sets have measure at most $B_1+B_2$ (union bounds; $\min(v,\Lambda)>M_f$ implies $v\ge M_f+1$). The fourth has measure at most $B_3$ by Proposition 10.
- *The last set.* Apply Proposition 7 with $C=C_{14}$, $a=4$, $\rho_*=2^{-\lfloor\log_22\Lambda\rfloor}$ and $R=2^{z(n_s)}2^{\min(\Lambda-1,\lceil(\Lambda+M_f)/2\rceil-1)}$. This $R$ is valid on $E$: $Z_{n_s}\le2^{z(n_s)}$ by Lemma 4. For each tracked path, $\rho\le2^{\min(\lambda-1,\lfloor(\lambda+\tilde M)/2\rfloor-1)}$ by Lemma 6(b). On $G_f$, $\tilde M\le M_f$, and $\lambda\le\Lambda$. Slope-$0$ paths have $\rho=1\le R2^{-z(n_s)}$. This gives $B_4+B_5$. ∎

**Numbers.** At $G=2^{448}$, Theorem B gives $\mu(C_{14}\cap\{g\ge G\})\le0.0456$, below the trivial $1/16$; at $2^{512}$, $0.0206$; at $2^{1024}$, $4.9\cdot10^{-6}$; at $2^{2048}$, $6.5\cdot10^{-13}$ (full table in §7). For $G\le2^{384}$ the bound is no better than $1/16$.

*Where the cost goes.* $\Lambda\approx n_U$ is forced: every slope $\le\Lambda$ must be carried by the martingale, and every slope $>\Lambda$ must have died by time $n_U$. The term $B_5$ then needs $k\gtrsim\ell_B+z(n_s)\approx\Lambda/2+\Lambda/2=\Lambda$, i.e. a digit-sum deficit of order $\Lambda$ among about $\log_2G$ digits. Meanwhile $B_2,B_3$ decay only like $2^{-M^*}$, with $M^*\approx n_U/16$ to $n_U/20$. This balance produces an exponent near $0.02$ in $\log_2G$, not near $1$; see §8.
## 7. The bound for $\delta_G(2)$: a staircase, and an explicit rate for all large $G$

**Corollary D [proved, given Lemma 3].** For every $G\ge7$,
$$\delta_G(2)\le\sum_{C\in\{C_0,C_2,C_6\}}\big(\text{bound of Theorem A}\big)+\min\Big(\tfrac1{16},\ \text{bound of Theorem B}\Big),$$
for any admissible parameters. Since $\delta_G(2)$ is non-increasing in $G$, the value at $G=2^K$ bounds $\delta_{G'}(2)$ for all $G'\ge2^K$.

*Proof.* Lemma 3 (consequence) and Theorems A, B; $\mu(C_{14})=1/16$. ∎

Exact values of the right-hand side, with parameters from a float search (`bounds.py D`; each line re-derived from its printed parameters by the independent `verify_bounds.py`, agreement to all printed digits):

| $G$ | bound on $\delta_G(2)$ | $C_0+C_2+C_6$ part | $C_{14}$ part | Theorem B parameters |
|---|---|---|---|---|
| $2^{32}$ | 0.1352 ($2^{-2.89}$) | 0.0727 | 0.0625 | — |
| $2^{36}$ | 0.1059 ($2^{-3.24}$) | 0.0434 | 0.0625 | — |
| $2^{37}$ | 0.1005 ($2^{-3.31}$) | 0.038 | 0.0625 | — |
| $2^{38}$ | 0.09606 ($2^{-3.38}$) | 0.0336 | 0.0625 | — |
| $2^{39}$ | 0.0946 ($2^{-3.40}$) | 0.0321 | 0.0625 | — |
| $2^{40}$ | 0.09103 ($2^{-3.46}$) | 0.0285 | 0.0625 | — |
| $2^{44}$ | 0.07778 ($2^{-3.68}$) | 0.0153 | 0.0625 | — |
| $2^{48}$ | 0.07085 ($2^{-3.82}$) | 0.00835 | 0.0625 | — |
| $2^{56}$ | 0.06492 ($2^{-3.95}$) | 0.00242 | 0.0625 | — |
| $2^{64}$ | 0.06322 ($2^{-3.98}$) | 0.000724 | 0.0625 | — |
| $2^{96}$ | 0.06253 ($2^{-4.00}$) | 3.18e-05 | 0.0625 | — |
| $2^{128}$ | 0.0625 ($2^{-4.00}$) | 5.89e-07 | 0.0625 | — |
| $2^{192}$ | 0.0625 ($2^{-4.00}$) | 2.36e-10 | 0.0625 | — |
| $2^{256}$ | 0.0625 ($2^{-4.00}$) | 5.65e-14 | 0.0625 | — |
| $2^{320}$ | 0.0625 ($2^{-4.00}$) | 2.02e-17 | 0.0625 | — |
| $2^{384}$ | 0.0625 ($2^{-4.00}$) | 1.86e-20 | 0.0625 | — |
| $2^{448}$ | 0.04555 ($2^{-4.46}$) | 6.67e-24 | 0.0456 | $M^*=8,M_f=13$, chain $[46, 67, 110, 194]$, $n_s=202,k=209$ |
| $2^{512}$ | 0.02055 ($2^{-5.60}$) | 1.04e-27 | 0.0206 | $M^*=12,M_f=17$, chain $[56, 80, 128, 224]$, $n_s=232,k=241$ |
| $2^{576}$ | 0.008596 ($2^{-6.86}$) | 6.89e-31 | 0.0086 | $M^*=12,M_f=17$, chain $[60, 88, 144, 254]$, $n_s=256,k=268$ |
| $2^{640}$ | 0.001901 ($2^{-9.04}$) | 5.97e-34 | 0.0019 | $M^*=14,M_f=19$, chain $[66, 96, 152, 264]$, $n_s=280,k=290$ |
| $2^{768}$ | 0.0004322 ($2^{-11.18}$) | 4.82e-35 | 0.000432 | $M^*=18,M_f=18$, chain $[80, 115, 184, 320]$, $n_s=328,k=345$ |
| $2^{896}$ | 4.291e-05 ($2^{-14.51}$) | 4.82e-35 | 4.29e-05 | $M^*=21,M_f=26$, chain $[90, 128, 206, 358]$, $n_s=374,k=393$ |
| $2^{1024}$ | 4.936e-06 ($2^{-17.63}$) | 4.82e-35 | 4.94e-06 | $M^*=24,M_f=29$, chain $[102, 146, 235, 410]$, $n_s=424,k=448$ |
| $2^{1280}$ | 7.434e-08 ($2^{-23.68}$) | 4.82e-35 | 7.43e-08 | $M^*=30,M_f=35$, chain $[126, 180, 288, 506]$, $n_s=518,k=551$ |
| $2^{1536}$ | 2.108e-09 ($2^{-28.82}$) | 4.82e-35 | 2.11e-09 | $M^*=33,M_f=38$, chain $[134, 192, 309, 540]$, $n_s=578,k=623$ |
| $2^{2048}$ | 6.495e-13 ($2^{-40.49}$) | 4.82e-35 | 6.49e-13 | $M^*=54,M_f=54$, chain $[200, 282, 445, 768]$, $n_s=810,k=861$ |
| $2^{2560}$ | 1.217e-15 ($2^{-49.55}$) | 4.82e-35 | 1.22e-15 | $M^*=70,M_f=70$, chain $[254, 354, 556, 960]$, $n_s=1010,k=1074$ |
| $2^{3072}$ | 4.023e-20 ($2^{-64.43}$) | 4.82e-35 | 4.02e-20 | $M^*=82,M_f=82$, chain $[298, 420, 664, 1152]$, $n_s=1202,k=1285$ |
| $2^{3584}$ | 8.752e-21 ($2^{-66.63}$) | 4.82e-35 | 8.75e-21 | $M^*=72,M_f=77$, chain $[220, 285, 414, 670, 1181]$, $n_s=1236,k=1360$ |
| $2^{4096}$ | 1.394e-22 ($2^{-72.60}$) | 4.82e-35 | 1.39e-22 | $M^*=81,M_f=86$, chain $[296, 418, 662, 1148]$, $n_s=1202,k=1337$ |

(The $C_0+C_2+C_6$ column stops improving at $4.8\cdot10^{-35}$ only because the search for Theorem A restricts $n_s\le n_C+119$; Theorem A′ gives far smaller values, e.g. $2^{-159}$ per class at $G=2^{1024}$. Since $\delta_G(2)$ is non-increasing, each row also bounds every larger $G$. In particular $\delta_G(2)\le0.1005$ for all $G\ge2^{37}$, $\le0.0456$ for $G\ge2^{448}$, and $\le4.9\cdot10^{-6}$ for $G\ge2^{1024}$.)

**Theorem C (an explicit rate for all large $G$) [proved, given Lemma 3].** For every integer $K\ge3072$,
$$\delta_{2^K}(2)\le2^{-K/80}.\qquad\text{Consequently}\qquad\delta_G(2)\le2^{1/80}\,G^{-1/80}\quad\text{for all }G\ge2^{3072}.$$

*Parameter rule $R(K)$* (no search). Put $M=\lfloor K/64\rfloor$ and $T=2^K-2K-12$.
- Theorem B: $M^*=M_f=M$; chain $n_1=6M$, $n_{i+1}=n_i+\lfloor n_i/2\rfloor$ for $i=1,2,3$, and $n_U=n_4$; $\Lambda=\beta(n_U)-1$; $n_s=n_U+2M$; $m_1=0$; $k=\ell_B+z(n_s)+M$.
- Theorem A, for each of the three classes: $n_s=2M+16$, $m_1=0$, $k=\ell_C+z(n_s)+M$.

*Proof.* Let $K\ge2400$, so $M\ge37$.
- *Chain.* $n_2=9M$, $13.5M-0.5\le n_3\le13.5M$ and $20.25M-1.25\le n_U\le20.25M$. For $n\in\{n_1,n_2,n_3\}$ and $N=n+\lfloor n/2\rfloor$, Lemma 1(c) gives $\beta(n)\ge n-2\log_2n-1$:
  - (W2) holds because $n/2\ge3M\ge2M+2\log_2(13.5M)$ when $M\ge22$;
  - (W1) follows from (W2);
  - (W3) holds because $\beta(N)\le1.5n-1\le2(n-2\log_2n-1)$ when $n\ge54$.

  Also $\Lambda\le n_U-2$, $K_t=K-1$ and $\beta(n_s)\ge\Lambda+1$.
- *$B_2$.* There are at most $(n_s+2\Lambda)/16+2\le3.93M+2$ indices $i\equiv2\pmod{16}$ involved, each contributing $2^{-M-1}$. So $B_2\le(2M+1)2^{-M}$.
- *$B_3$.* $\varphi_J(n,N)\le L/2+1-(\beta(N)-n+1-J)\le-L/2+1+2\lfloor\log_2N\rfloor+J$ with $L=\lfloor n/2\rfloor$. Summing over the three windows ($\sum L=n_U-n_1$) gives $\sum\varphi_J\le-(n_U-6M)/2+3+6\log_2(20.25M)+3J$. With $z(6M)=3M-1$ and $\sum_{J\le M}2^{2J}\le\frac43 4^M$, we get $B_3\le2^{-2.125M+2.05+6\log_2(20.25M)}$.
- *$B_4$.* Each term is $\le2^{-(\beta(i-1)-\Lambda+1)}\le2^{\Lambda+1}(i-1)^22^{-i}$. Summing (ratio $\le0.5116$) gives $B_4\le2.05\,n_s^22^{\Lambda-n_s}\le2^{-2M+2\log_2(22.25M+1)}$.
- *$B_5$.* The second part equals $\frac1{16}2^{1-M}=2^{-M-3}$. For the first part, $k-1\le22.75M-1.5+\log_2(40.5M)$, so $q=(k-1)/(K-5)\le0.36$ (checked for every $K\in[2400,4\cdot10^6]$; for larger $K$, $q\to22.75/64<0.356$). The Chernoff bound with $1-H(0.36)=0.05732$ gives $\le2^{-0.0573(K-5)-4}$.
- *Theorem A terms.* $\sum_C A_5\le\frac14\big(2^{1-M}+2^{-0.75(K-5)}\big)$, since $k_A-1\le2M+10$, so $q\le0.04$ and $1-H(0.04)>0.757$. Next, $\sum_CA_4\le3\cdot2.05\cdot2^3(2M+16)^22^{-2M-16}$. Finally, $A_1$ and $B_1$ total $\le2^{-K+1}$.

The sum of these nine closed-form terms (function `majorant` in `rule.py`) is $\le2^{-K/80}$ for every $K\in[3072,4\cdot10^6]$, checked exhaustively by `rule_K0.py`. The largest violating $K$ in $[2400,4\cdot10^6]$ is $3071$. For $K>4\cdot10^6$ every term is $\le2^{-K/80-4}$, since $K/64-1-K/80=K/320-1$ exceeds $\log_2(K/32+1)+4$ by a wide margin. ∎

Exact evaluation of the bound under the rule (`rule.py`; parameters re-checked by `verify_bounds.py`):

| $K$ | exact bound under $R(K)$ | $-\log_2(\cdot)/K$ | closed-form majorant | $-K/80$ |
|---|---|---|---|---|
| 3072 | $2^{-41.44}$ (largest term B2) | 0.0135 | $2^{-39.81}$ | -38.40 |
| 3584 | $2^{-49.22}$ (largest term B2) | 0.0137 | $2^{-49.16}$ | -44.80 |
| 4096 | $2^{-57.03}$ (largest term B2) | 0.0139 | $2^{-56.98}$ | -51.20 |
| 8192 | $2^{-120.03}$ (largest term B2) | 0.0147 | $2^{-119.99}$ | -102.40 |
| 16384 | $2^{-247.03}$ (largest term B2) | 0.0151 | $2^{-247.00}$ | -204.80 |

So under the rule the actual bound behaves like $\delta_{2^K}(2)\le2^{-0.0135K}$ to $2^{-0.015K}$ in this range. Theorem C states the cleaner, slightly weaker exponent $1/80=0.0125$. With searched parameters (staircase table), the exponent is about $0.02$ for $2048\le K\le3072$. The values at $K=3584,4096$ are slightly lower because the search grid is coarse.
## 8. How good is this? Comparison with the census and the numerics

The proved bounds are honest but weak. They are meaningful only at astronomically large $G$.

| $G$ | proved bound (this report) | best proved before | numerics (not proofs) |
|---|---|---|---|
| $32$ | $\le1$ (trivial) | $\delta_{32}(2)=0.101636$ exactly (census, note §4.7) | — |
| $64$ | trivial | $0.1016$ | Monte Carlo $0.0644$ (note §5) |
| $254$ | trivial | $0.1016$ | Monte Carlo $0.0208$ |
| $2^{36}$ | $0.1059$ | $0.1016$ | $c/G$ law: about $5/G\approx7\cdot10^{-11}$ |
| $2^{37}$ | $0.1005$ | $0.1016$ | about $4\cdot10^{-11}$ |
| $2^{40}$ | $0.0910$ | $0.1016$ | about $5\cdot10^{-12}$ |
| $2^{64}$ | $0.0632$ | $0.1016$ | about $3\cdot10^{-19}$ |
| $2^{448}$ | $0.0456$ | $0.1016$ | about $2^{-446}$ |
| $2^{1024}$ | $4.9\cdot10^{-6}$ | $0.1016$ | about $2^{-1022}$ |
| $2^{2048}$ | $6.5\cdot10^{-13}$ ($=2^{-40.5}$) | $0.1016$ | about $2^{-2046}$ |
| $G\ge2^{3072}$ | $2^{1/80}G^{-1/80}$ (Theorem C) | — | about $5G^{-1}$ |

*Reading the table.*
- **The census is better for every $G<2^{37}$.** Our first improvement on $\delta_{32}(2)=0.10164$ comes at $G=2^{37}$ ($0.1005$; $0.0910$ at $2^{40}$). Up to about $G=2^{384}$ the improvement comes only from the classes $C_0,C_2,C_6$ (Theorem A), and the bound is stuck at the floor $1/16=\mu(C_{14})$. The floor is beaten only from about $G=2^{448}$ on.
- **The rate is very far from the truth.**
  - Theorem C gives exponent $1/80$, and the searched parameters give about $0.02$ at $G=2^{2048}$.
  - The natural-number survey of track R3N (§6 of its report) finds $G\cdot P(g_2(a)\ge G)$ between $8$ and $12$ over even $a\le32768$, for $256\le G\le131072$. That is about $5/G$ over all $a$, in line with Kitamura's $\approx11.5/G$ for even $a$.
  - The note's small-$G$ fit $\approx0.7/\sqrt G$ (§5) is consistent with this, as R3N explains.
  - If the $c/G$ law is right, the true exponent is $1$; ours is $1/80$.
- **The three good classes do much better.** On $C_0\cup C_2\cup C_6$ (one quarter of $\mathbb Z_2$, all of the measure outside $C_{14}$ where $g_2$ can exceed $6$), Theorem A′ proves $G^{-1/7}$ and the optimised evaluations behave like $G^{-0.16}$ to $G^{-0.18}$. This still uses a single digit-sum drop of the critical walk, which caps the method at about $G^{-0.23}$ even with perfect constants (see §11).
- **What the hard class costs.** On $C_{14}$ (the neighbourhood of $-2$, where Kitamura's cube identity $S_{\{1,3\}}=(x+2)^3$ creates near-double roots), the method must carry slopes up to $\Lambda\approx n_U$. The weights $\rho$ can then be as large as $2^{\Lambda/2}$ (Lemma 6(b); numerically the median of $\max_s\rho$ grows roughly like $2^{0.25\lambda}$, with outliers near $2^{\lambda/2}$). This cost, together with the slow decay ($2^{-M^*}$) of the high-slope population bound, is what limits the exponent to about $0.02$.

**In plain words.** $\delta_G(2)\to0$ now has an explicit, fully proved rate, $\delta_G(2)\le2^{1/80}G^{-1/80}$ for $G\ge2^{3072}$. The proof also gives explicit (computed) bounds below the census value from $G=2^{40}$ on, and below $1/16$ from $G=2^{448}$ on. These statements say nothing useful at any $G$ one could reach by computation, where the census and Monte Carlo values are far smaller. Equivalently, for natural numbers: the set of $a$ with $f(a,2)\ge v_2(a!)+G$ has natural density at most $2^{1/80}G^{-1/80}$ for $G\ge2^{3072}$, at most $0.1005$ for $G\ge2^{37}$, and at most $0.091$ for $G\ge2^{40}$.
## 9. Relation to the earlier R3Q instance and to Claim 10.9

An earlier R3Q instance was cut off before writing a report. Its code is in `code/round3/R3Q/*.py`, and its three surviving logs are copied to `data/round3/R3Q/earlier_instance/` (from `/tmp/r3_R3Q/`). It references a "Theorem B" (one certified class), a "Theorem C" (all of $\mathbb Z_2$, about $2^{-0.01\log_2G}$, below $1$ only near $G=2^{1000}$) and a "Corollary D" ($1/16$ plus class bounds). Its reasoning is lost. We used the code as a map and re-derived everything:
- **Confirmed and proved here:**
  - the $\beta$-lemma (our Lemma 1(c));
  - the population bound (Lemma 4);
  - the one-step weighted identity (Lemma 5; their `check_step_identity.py` tests the same identity);
  - $\rho\ge1/(4\lambda)$ (Lemma 6(c));
  - the uniform-slope anchors on $C_0,C_2,C_6$ (Lemma 3, now an exhaustive two-program certificate);
  - the second-derivative statement "L4" (Lemma 8; on disk it had only a numerical test, here it has a proof);
  - the structure "martingale for slopes $\le\Lambda$, window bound for slopes $\ge\beta(n)$, digit-sum drop at a stopping time".
- **Changed:**
  - (i) The window lemma for the high-slope population is proved on coarse atoms $x+2^{V_n-M_n}\mathbb Z_2$, which removes a loss of $M_n$ per window (Lemma 9).
  - (ii) The window overhead uses the exact $j=v(x+2)$, weighted by $2^{-j-1}$ (Proposition 10), rather than $j\le M^*$.
  - (iii) A new upper bound $\rho\le2^{(\lambda+\tilde M)/2-1}$ (Lemma 6(b)) replaces $\rho\le2^\lambda$.
  - (iv) An optional digit split $m_1$ (Proposition 7).
  - (v) The failure-sum tails are bounded rigorously for $T\approx2^K$ with $K>3000$. A first version of our own evaluator used a crude tail (count of terms times the last threshold), which is valid but useless for $K>3000$. It was replaced before the $K\ge2560$ runs. For the $K\le2048$ lines of `scan_D.log` it made no visible difference: the independent verifier, which uses the sharp tail, reproduces them to all printed digits.
- **Effect.**
  - At $G=2^{1024}$ the earlier code's exact evaluation gave $0.086$ for all of $\mathbb Z_2$; Corollary D gives $4.9\cdot10^{-6}$.
  - The $C_{14}$ bound becomes non-trivial near $G=2^{448}$ instead of near $G=2^{1000}$.
  - The fixed-rule exponent is $1/80$ for all $K\ge3072$ (Theorem C), against the earlier instance's fixed-rule script (`calc_C_rule.py`/`calc_C_analytic.py`, whose closed-form proof is lost).
- **Not adopted.** The earlier code also uses $V_n\le n-s(n)+M_n$, which is valid (each $c_\ell\le\lfloor n/2^\ell\rfloor+1$) and slightly sharper than our $V_n\le n+M_n-2$. It would improve $\varphi$ by $s(n)-2$ per window. We did not use it, so every number here is computed with the weaker bound.

*Claim 10.9 (track R1a, unverified).* It asserts $(2\cdot3^{-3/2}+1/9)(3/4)^{D/2}+2^{D-2^D}$ on $C_0\cup C_2\cup C_6$, i.e. about $0.662G^{-0.2075}$, plus the floor $1/16$. Theorem A and A′ are proved bounds of the same shape on the same three classes. They are weaker in rate ($G^{-1/7}$ proved; about $G^{-0.17}$ computed) and in constants (at $G=2^{40}$ we get $0.0285$ on the three classes where Claim 10.9 gives $0.002$). Theorem B removes the $1/16$ floor. Claim 10.9 remains unverified; nothing here confirms or refutes it.

## 10. Verification and reproduction

All programs are in `code/round3/R3Q/v2/` and were run with `nice -n 10 python3 -I` on one core. Logs are in `data/round3/R3Q/`.

| item | program(s) | log | wall time | result |
|---|---|---|---|---|
| Lemma 3 certificates | `cert_classes.py`, `cert_classes_sympy.py` (no shared code); the earlier instance's `../slope_cert.py` as a third check of (a)–(c) | `certificates.log` | <5 s each | 0 violations in (a)–(e); 4/32/128 qualifying words, identical counts in all three programs |
| Lemma 1, 4, 6, 8 | `test_elementary.py` (random even $x$, $x$ near $-2$, the four classes; exact integers mod $2^{640}$) | `lemma_tests.log` | 43 s | 0 failures; 88500 valuation checks, 1500 population checks, 14097 upper/2439 lower weight checks, 20441 Lemma 8 checks (7779 with slope $>2j$) |
| Lemma 5 | `test_step.py` (every child recomputed from scratch at every $x'=x+2^mw$; control with $\rho:=1$) | `lemma_tests.log` | 215 s | 3344 parents (3222 with $\lambda\ge3$), 0 failures; control differs in 928 |
| Lemma 9 / Cor. 9′ | `test_uwin.py` (general thresholds; and $\beta$ thresholds) | `lemma_tests.log` | 35 s + 1 s | 2074 windows, 330 non-empty, 0 failures, max ratio 1.000, control changed $U_n$ in 59/330; 2036 windows, 4 non-empty, 0 failures, max ratio 0.062, control changed $U_n$ in 0/4 |
| Corollary D table | `bounds.py D K K 1` | `scan_D.log`, `scan_D2.log`, `scan_D3.log` | 19 s–251 s per $K$ | table of §7 |
| independent re-derivation of every table entry | `verify_bounds.py` | `verify.log` | 1 s | all ratios $1.0000$ |
| Theorem C | `rule.py`, `rule_K0.py` | `rule.log` | under 30 s in total | largest bad $K$ in $[2400,4\cdot10^6]$ is $3071$; exact rule values at $K=3072,\dots,16384$ re-derived by `verify_bounds.py` |
| Theorem A′ | `rule_A.py` | `rule.log` | 10 s | no bad $K$ in $[1024,4\cdot10^6]$ |

*Validation on known values.*
- The certificates reproduce the known value set $g_2\in\{0,3\}\cup[6,\infty]$ on the relevant classes (note Cor. 3.7.1(iii)).
- The lemma tests use exact integer arithmetic only (no floating point), and each is non-vacuous: Lemma 8 had 7779 high-slope instances; Lemma 9 had 334 non-empty windows, and its bound is attained. The tests of Lemma 5 and Lemma 9 have negative controls: replacing $\rho$ by $1$ breaks the identity for 928 parents, and a coarser atom changes $U_n$ in 59 windows.
- `verify_bounds.py` self-tests its residue counter against brute force, its $\beta$ against the digit-sum definition (for $n<3000$) and its binomial tail on a hand value.
- Floating point is used only to choose parameters. Every reported bound is an exact rational, recomputed by a second program.

## 11. Failed attempts, limitations, open issues

- **[failed attempt] One drop of the walk is not enough for a good rate.** The argument uses the critical walk $W_n$ at a single stopping time ($2^K\mid x+n$, where $W$ drops by $s(x\bmod2^K)-1$). Even with a perfectly known initial martingale value, the best this gives is $\min_k\big(2^{-k}+\mathbb P(\mathrm{Bin}(K)<k)\big)\approx2^{-0.227K}=G^{-0.227}$, because the martingale value and the digit sum may be correlated adversarially. The ideal $(3/4)^K=G^{-0.415}$ would need the digit sum to be measurable at the start time, i.e. $V_{n_s}\ge K$. That forces $n_s\gtrsim\log_2G$, where the deterministic population bound $2^{n_s/2}$ is too crude. Combining several drops (a multi-scale argument) was not attempted.
- **[obstruction for this method] Large slopes.** Per-slope accounting cannot work with the available bounds. A slope-$\lambda$ path costs up to $\rho_{\max}/\rho_*\approx2^{\lambda/2}\cdot2\lambda$, while the probability of a slope $\ge\lambda$ appears (numerically, `data/round3/R3Q/earlier_instance/slope_tail_4000.log`) to decay only like $2^{-\lambda/2}$, driven by $v(x+2)\approx\lambda/2$. We therefore cut at $\Lambda$ and pay $2^{\Lambda/2}$ once. A proof that the *average* weight of the tracked population is $O(\mathrm{poly}\,\Lambda)$ (an equidistribution statement for targets) would roughly halve the cost; we did not find one.
- **[heuristic] Weights.** For random even $x$ and $n\in[50,500]$, the median of $\max_s\rho_n^{(\lambda)}(s)$ is $2,4,16,24,34$ for $\lambda=4,8,12,16,20$, and the maximum over 30 samples is $8,32,224,448,1056$ (`explore_rhomax.py`; 30 samples, not a proof). Lemma 6(b) is therefore not wasteful by more than a factor of about $2^{\lambda/4}$ typically.
- **Limitations.**
  - Lemma 3 is computer-assisted (two programs, exhaustive, tiny).
  - Everything else is proved by hand here and has not been checked by a referee or a human.
  - The search tables depend on a float search, but each printed bound is exact for its printed parameters.
- **Open.**
  - (1) An exponent comparable to the observed $1$ (or even $1/2$) seems to need new ideas: control of the martingale's initial value without the deterministic population bound, an averaged bound on $\rho$, and a multi-scale use of the walk.
  - (2) A sharper U-window lemma whose overhead does not repeat at every window.
  - (3) Nothing here bears on whether $K_2\cap\mathbb N=\emptyset$, i.e. on Q1 at $p=2$ for every $a$, or on Q3.

## Credits

- **Problem and statement.** Erdős–Graham (1980); Kovač's correction (2025).
- **Normal form and determinacy at $p=2$.** K. Kitamura. Kitamura also gave the critical-branching picture, the measured decay of the surviving fraction ($\approx11.5/G$), and the cube identity used in Lemma 8's setting.
- **Martingale weights and the qualitative theorem $\mu(K_2)=0$.** Round-2 track R1b (note §10.1).
- **Claim 10.9.** Round-2 track R1a.
- **Branching-process strategy.** Smith–Wilkinson; Athreya–Karlin; Afanasyev–Geiger–Kersting–Vatutin, as credited in note §10.1.
- **The $c/G$ survey.** Round-3 track R3N.
- **The map of lemmas.** The earlier, interrupted R3Q instance.
- **This report.** All proofs and programs were written anew by the restarted R3Q track.
