# Round 4, track M4A: strategy A ("(S) + truncation") for $\mu(K_p)>0$

Date: 2026-10-13. Code: `code/round4/M4A/`. Logs: `data/round4/M4A/` (every run starts with `=== command:` and ends with `=== exit:`). Notation: note.md §10.1 and data/round3/reports/R3M.md §1. Everything this report needs from there is restated in §1.

## Headline

**$\mu(K_7)>0$ [computer-assisted].** For an explicit cylinder $A=x_A+7^{51}\mathbb Z_7$ we prove $\mu(K_7\cap A)\ge1.84\cdot10^{-26}\,\mu(A)$, so $\mu(K_7)\ge1.4\cdot10^{-69}$. The same proof, with other explicit atoms, gives $\mu(K_p)>0$ for $p=11,13,17,19,23$. Conjecture 5.2 therefore holds for these six primes. This says nothing about Q3: $K_p$ is nowhere dense (note Theorem 3.6), and a countable set such as $\mathbb N$ is Haar-null.

The proof verifies the hypothesis FE of R3M's conditional Theorem C3 (note Theorem 11.14) for one admissible atom. It uses three new ingredients, all proved here.

1. **Theorem 1 (exact averaged identity) [proved].** Averaged over a ball $B$ on which the gate pattern is fixed, the fine-scale mass $\varepsilon$ of a composite window equals the change, between the scales $p^{-D}$ and $p^{-K}$, of the mass of signed paths whose slope is at least about $D/2$. This turns R3M's Remark C6 into an identity. The proof is Hensel's lemma for each signed polynomial; no martingale is needed.
2. **Lemma Q (quenched anti-concentration for the signed process) [proved; universal constants computed exactly].** The probability that a signed path satisfies $v(T)\ge k$ and $v(T')\ge f$ is bounded by a product over gate blocks. Each block whose end gate has depth 1 and whose level is below $f$ contributes a factor $q_2/p^2$. Every other block contributes $q_d/p^d$. Here $q_s=p^s\max_zP(\sum_{k<p}\zeta_k\pi_k(-p)\equiv z\bmod p^s)$ is a universal constant: at $p=7$, $q_1=8309/8192$ and $q_2=4557/4096$. The 2D factor is exactly attained in the exact tests.
3. **Propositions D, E, E′ [proved].** These give explicit bounds, pointwise for $p^K\mathrm{Coll}_K$ (D) and averaged for $\varepsilon$ (E, and its closed form E′). By Theorem 1 and Lemma Q, the averaged bound decays like $\approx0.57^{D}$ at $p=7$. This proves (S), the open sub-problem of the brief, in the form needed, and it uses no truncation beyond working on one atom.

**FE for an explicit atom [computer-assisted].** The atom is $A=x_A+7^{51}\mathbb Z_7$ at time $n_0=300$. The window times are $n_{\ell+1}=\lceil27n_\ell/20\rceil$.
- Its slope-0 population is nonempty: an explicit path is re-verified by exact integer evaluation.
- The first eight windows get pointwise thresholds $\bar\varepsilon_\ell$ from Proposition D.
- All later windows get $\bar\varepsilon_\ell=2^{-(\ell-8)}$ and Markov's inequality with Proposition E or E′.
- Beyond $n\approx4\cdot10^{42}$, random deep gates are truncated by an event of measure $\le2.5\cdot10^{-94}$, and a closed-form estimate covers all remaining windows.

The result is $\log_{10}\Pi_A\le25.74$, $\delta_A\le1.0006\cdot10^{-45}$ and $\Pi_A\delta_A\le10^{-19.26}<1$. All bounds are evaluated in outward-rounded interval arithmetic. Phases 0–2 were re-computed in exact rationals by a second code path, with identical results.

**Where this stops.** The method needs the per-level 2D gain $q_2/p$ to beat the per-level 1D growth: the asymptotic rate $\gamma(p-1)(r-1)/(2p^2)-(r^2-1)\rho_1/(p-1)$ must be positive. This holds for $p\ge7$ and fails for $p=3,5$, where $\rho_1=0.22$ is too large (§8). A statement for **all** $p\ge p_0$ would need uniform-in-$p$ bounds on $q_1,q_2$, i.e. anti-concentration of signed subset sums of $\{k!\bmod p\}$, which we do not have. So the result is prime by prime: $p=7,11,13,17,19,23$.

## 0. Results at a glance

| # | Statement | Status |
|---|---|---|
| Lemma H | Hensel step: $p^{k'}\mu_B\{v(S)\ge k'\}-p^k\mu_B\{v(S)\ge k\}$ depends only on the high-slope set | proved; exact tests |
| Thm 1 | $\mathbb E_B[\varepsilon]=2^{-H}(p^K-p^D)+$ (high-slope mass at scale $K$) $-$ (high-slope mass at scale $D$) | proved; 51/51 exact identities ($p=3,5,7$) |
| Lemma F | first-index reduction of the high-slope mass to the signed process at shifted points | proved; 36/36 exact tests (with Lemma Q) |
| Lemma Q | quenched anti-concentration (block product; 2D factor $q_2/p^2$) | proved; exact tests (bound attained; negative controls fail); algebra checked exactly at levels up to $\sim30$ |
| Prop D | pointwise bound for $p^K\mathrm{Coll}_K$, hence for $\varepsilon$ and $\chi^2$ | proved; exact tests (ratio up to 0.98) |
| Prop E | averaged bound for $\mathbb E_B[\varepsilon]$ | proved; exact tests |
| Prop E′ | closed form of Prop E | proved; dominates Prop E in 140/140 windows |
| **Thm M** | **FE for the explicit atom; $\mu(K_7\cap A)\ge1.84\cdot10^{-26}\mu(A)$; $\mu(K_7)>0$** | **computer-assisted** |
| Cor M′ | the same for $p=11,13,17,19,23$ (explicit atoms) | computer-assisted |
| §8 | $p=3,5$: the method's rate is negative; no conclusion | negative (for the method) |

## 1. Setting and what is used from round 3

$p$ is an odd prime, $v=v_p$ and $\mu$ is Haar probability measure on $\mathbb Z_p$.
- $\pi_c(y)=(y+1)\cdots(y+c)$, $V_t(y)=v(\pi_t(y))$, $M_t(y)=\max_{i\le t}v(y+i)$, $c_n=2^{-n}p^{V_n}$.
- A *gate* of $y$ is a position $i\ge1$ with $p\mid y+i$; its depth is $v(y+i)$.
- $F^{[i]}=F^{(i)}/i!$ for a polynomial $F$.
- A *signed digit* has law $P(0)=\tfrac12$, $P(\pm1)=\tfrac14$: the difference of two independent fair bits.

**Composite windows.** Fix $n<N<N'$, $H=N'-n$, $y_c(x)=\pi_{n+c}(x)/\pi_n(x)=\prod_{i=1}^c(x+n+i)$ ($0\le c<H$), $a_c=v(y_c)=V_{n+c}-V_n$, $D=V_N-V_n$, $K=V_{N'}-V_n$.
- $\mathrm{Coll}_j(x)$ is the probability that two independent uniformly random subset sums of $\{y_c\}$ agree mod $p^j$. Equivalently, $\mathrm{Coll}_j=P_\delta(S_\delta(x)\equiv0\bmod p^j)$, where $S_\delta=\sum_{c<H}\delta_cy_c$ and $\delta$ is i.i.d. signed.
- $\varepsilon:=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D\ge0$.

Under the linear-regime condition (5.2) this is R3M's fine-scale mass $\varepsilon(W,W')$ (R3M Prop C2, "Identification of $\varepsilon$"). Since $p^D\mathrm{Coll}_D\ge1$ by Cauchy–Schwarz, $\varepsilon\le p^K\mathrm{Coll}_K-1$.

**Used from round 3 (proved there; checked by an independent instance and a referee):**
- R3M Lemma 1: (a) $V_n\ge v(n!)$; (b) $V_n\le n/(p-1)+M_n$; (c) $V_j-V_n\ge v((j-n)!)$; (d) $v(\pi^{[i]}_j)\ge V_j-iM_j$; (e) Taylor's formula.
- **R3M Theorem C3 (note Theorem 11.14).** The setting:
  - deterministic times $2p\le n_0<n_1<\cdots$, with $m_\ell=V_{n_\ell}$ and $D_\ell=m_{\ell+1}-m_\ell$;
  - $\varepsilon_\ell=\varepsilon(W_{\ell-1},W_\ell)$ for the composite window $[n_{\ell-1},n_{\ell+1})$;
  - an admissible atom $A=x_A+p^{m_j}\mathbb Z_p$, i.e. $Z^0_{n_j}\ne0$ on $A$, $D_j\le m_j-M_{n_{j+1}}$ and $M_{n_{j+1}}<m_j$;
  - nonnegative $(\bar\varepsilon_\ell)_{\ell>j}$ with $\Pi_A=(1+\chi^2_j)\prod_{\ell>j}(1+\bar\varepsilon_\ell)<\infty$;
  - $B_\ell=\{D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}},\ M_{n_{\ell+1}}<m_{\ell-1}\}\cap\{\varepsilon_\ell\le\bar\varepsilon_\ell\}$ and $\tau=\min\{\ell>j:x\notin B_\ell\}$.

  If $\delta_A:=\mu_A(\tau<\infty)<1/\Pi_A$, then $\mu(K_p\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$. The proof (R3M §5) uses only an upper bound on $\chi^2_j$ (through $\mathbb E[\tilde M^2_{j+1}\mid\mathcal G_j]\le M_j^2(1+\chi_j^2)$). So $\chi^2_j$ may be replaced by any upper bound, which is what we do. I re-read the proof of C3 line by line (martingale, $L^2$ recursion $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}$, survival $\Rightarrow K_p$, Paley–Zygmund) and found nothing to add.

## 2. Theorem 1: the averaged fine-scale mass is a high-slope mass

**Lemma H (Hensel step) [proved].** Let $S\in\mathbb Z_p[X]$, let $B=x_0+p^b\mathbb Z_p$ with normalised Haar measure $\mu_B$, and let $1\le k\le k'$. Put $\theta=\min(\lceil k/2\rceil,\,k-b+1)$ and $\mathcal H=\{z\in B:v(S(z))\ge k,\ v(S'(z))\ge\theta\}$. Then
$$p^{k'}\mu_B\{v(S)\ge k'\}-p^k\mu_B\{v(S)\ge k\}=p^{k'}\mu_B(\mathcal H\cap\{v(S)\ge k'\})-p^k\mu_B(\mathcal H).$$

*Proof.* Let $\mathcal L=\{v(S)\ge k\}\setminus\mathcal H$, and for $z\in\mathcal L$ let $\lambda=v(S'(z))\le\theta-1$ and $\rho=k-\lambda$. Then $\lambda<k/2$, so $\rho>\lambda$, and $\lambda\le k-b$, so $\rho\ge b$ and $U_z:=z+p^\rho\mathbb Z_p\subseteq B$. For $u,u'\in p^\rho\mathbb Z_p$, Taylor's formula gives
$$S(z+u)-S(z+u')=(u-u')\Big[S'(z)+\sum_{i\ge2}S^{[i]}(z)\textstyle\sum_{a+b=i-1}u^au'^b\Big].$$
The sum has valuation $\ge\rho>\lambda$. Hence $v(S(z+u)-S(z+u'))=\lambda+v(u-u')$. Three consequences:
- (i) $v(S(z+u))\ge\min(k,\lambda+\rho)=k$.
- (ii) $S'(z+u)\equiv S'(z)\pmod{p^\rho}$, so $v(S'(z+u))=\lambda$. Hence $U_z\subseteq\mathcal L$, and $U_{z'}=U_z$ for $z'\in U_z$, so $\mathcal L$ is a disjoint union of such balls.
- (iii) $u\mapsto S(z+u)$ maps the $p^j$ cosets of $p^{\rho+j}\mathbb Z_p$ in $p^\rho\mathbb Z_p$ injectively, hence bijectively, onto the $p^j$ cosets of $p^{k+j}\mathbb Z_p$ in $S(z)+p^k\mathbb Z_p=p^k\mathbb Z_p$.

Hence the fraction of $U_z$ with $v(S)\ge k'$ is $p^{-(k'-k)}$, and $p^{k'}\mu_B(\mathcal L\cap\{v(S)\ge k'\})=p^k\mu_B(\mathcal L)$. Write $\{v(S)\ge k'\}$ and $\{v(S)\ge k\}$ as disjoint unions over $\mathcal L$ and $\mathcal H$, and subtract. ∎

**Theorem 1 [proved].** Let $B=x_0+p^b\mathbb Z_p$ be a ball on which $v(x+i)$ is constant for $n<i\le N'$ (so $D,K,a_c$ are constant on $B$), and let $\theta=\min(\lceil D/2\rceil,D-b+1)$. Then
$$\mathbb E_B[\varepsilon]=2^{-H}(p^K-p^D)+\mathbb E_\delta\Big[\mathbf 1_{\delta\ne0}\Big(p^K\mu_B\{v(S_\delta)\ge K,\,v(S'_\delta)\ge\theta\}-p^D\mu_B\{v(S_\delta)\ge D,\,v(S'_\delta)\ge\theta\}\Big)\Big].$$
In particular $\mathbb E_B[\varepsilon]\le2^{-H}p^K+p^K\,P_{\delta,\,x\in B}\big(\delta\ne0,\ v(S_\delta(x))\ge K,\ v(S_\delta'(x))\ge\theta\big)$.

*Proof.* By Fubini, $\mathbb E_B[p^j\mathrm{Coll}_j]=\mathbb E_\delta[p^j\mu_B\{S_\delta\equiv0\bmod p^j\}]$ for $j\in\{D,K\}$; both are constant on $B$. The term $\delta=0$ (probability $2^{-H}$) gives $2^{-H}(p^K-p^D)$. For $\delta\ne0$, $S_\delta\in\mathbb Z[X]$, and Lemma H applies with $k=D$, $k'=K$. ∎

When $\lfloor D/2\rfloor+1\ge b$ (always the case below), $\theta=\lceil D/2\rceil$: only signed paths whose slope is at least half the scale contribute. This is the rigorous form of R3M's Remark C6. The "low-slope classes visible to the windows" contribute exactly zero, by Hensel's lemma rather than by a martingale. The identity holds exactly in 51/51 tests, including general $\theta$ (`hensel_identity_check.py`, §9).

Both high-slope terms are typically of size $O(1)$ at small scales and cancel almost completely; the logs show $0.62$ against $0.63$ for an $\mathbb E_B\varepsilon$ of $0.008$. Only the first term is bounded below, so all the gain must come from the high-slope mass itself being small at large $D$. That is what Lemma Q provides.

## 3. Lemma F: reduction to the signed process at shifted points

For $u\in\mathbb Z_p$, $t\ge1$, $k\le V_t(u)$ and $f\in\mathbb Z$ put
$$G(u;t,k,f):=p^k\,P\big(v(T_u)\ge k,\ v(T_u')\ge f\big),\qquad T_u=\sum_{c<t}\tilde\delta_c\pi_c(u),\quad\tilde\delta_0=1,\ \tilde\delta_1,\dots\ \text{i.i.d. signed}.$$
For $f\le0$ there is no slope condition.

**Lemma F [proved].** In the setting of Theorem 1 assume also $M_W:=\max_{n<i\le N'}v(x+i)\le K-\theta$. Then
$$p^KP_{\delta,x\in B}\big(\delta\ne0,\ v(S_\delta)\ge K,\ v(S_\delta')\ge\theta\big)\le\sum_{c<H,\ a_c\ge K}2^{-c-1}p^K+\sum_{c<H,\ a_c<K}2^{-c-1}p^{a_c}\sup_{x\in B}G(x+n+c;\,H-c,\,K-a_c,\,\theta-a_c).$$

*Proof.*
- **Split by the first nonzero index.** The first nonzero index of $\delta$ is $c$ with probability $2^{-c}\cdot\frac12$. Given this and $\sigma=\delta_c$, we have $S_\delta(x)=\sigma y_c(x)T(x+n+c)$, because $y_{c+t}/y_c=\pi_t(x+n+c)$. Here $T=\sum_{t<H-c}\tilde\delta_t\pi_t$ with $\tilde\delta_0=1$ and $\tilde\delta_t=\sigma\delta_{c+t}$ i.i.d. signed.
- **The case $a_c\ge K$.** Bound the probability by 1.
- **The case $a_c<K$, value condition.** $v(S_\delta)\ge K$ iff $v(T)\ge K-a_c$.
- **The case $a_c<K$, slope condition.** We have $y_c'=y_c\sum_{i\le c}1/(x+n+i)$, so $v(y_c')\ge a_c-M_W$. Therefore $v(y_c'T)\ge K-M_W\ge\theta$. So $v(S_\delta')\ge\theta$ forces $v(y_cT')\ge\theta$, i.e. $v(T')\ge\theta-a_c$.
- **Conclusion.** Average over $x\in B$ and bound by the supremum. Note that $K-a_c=V_{H-c}(x+n+c)$. ∎

## 4. Lemma Q: quenched anti-concentration of the signed process

*Universal constants.* Let $\zeta_0,\dots,\zeta_{p-1}$ be i.i.d. signed and $Z=\sum_{k=0}^{p-1}\zeta_k\pi_k(-p)$, where $\pi_k(-p)=\prod_{i=1}^k(i-p)$. Put
$$q_s:=p^s\max_zP(Z\equiv z\bmod p^s)\ (s\ge1),\qquad P_0(g,s):=P\Big(\textstyle\sum_{c<g}\zeta_c\pi_c(-g)\equiv0\bmod p^s\Big)\ (\zeta_0=1,\ 1\le g\le p).$$
These are finite computations: exact enumeration of the $3^p$ configurations, and a residue DP for $p>13$, validated against the enumeration for $p\le13$ (`qdp_check.py`). Note $q_s\le pq_{s-1}$. At $p=7$:
$$q_1=\tfrac{8309}{8192}=1.01428,\quad q_2=\tfrac{4557}{4096}=1.11255,\quad q_3=\tfrac{33271}{8192}=4.0614,\quad q_s=7^s\cdot\tfrac3{256}\ (s\ge4).$$
- $P_0(2,s)=\tfrac14$ for all $s$: this is the double root of $(y+2)^2$, R3M's Proposition N3.
- $P_0(1,s)=P_0(3,s)=0$ for $s\ge1$.
- $P_0(4,1)=\tfrac9{64}$, $P_0(5,\cdot)=(\tfrac{33}{256},\tfrac1{64},0)$, $P_0(6,\cdot)=(\tfrac{37}{256},\tfrac7{1024},0)$, $P_0(7,\cdot)=(\tfrac{591}{4096},\tfrac{15}{1024},\tfrac1{4096},0)$.

At $p=11$, $(q_1,q_2,q_3)=(1.00144,1.11160,1.80119)$; at $p=13$, $(1.000022,1.00812,1.19244)$.

*Notation.* Fix $u\in\mathbb Z_p$ (not a negative integer) and $t\ge1$.
- The gates of $u$ in $[1,t]$ are $g_1<g_2<\cdots$; consecutive gates differ by exactly $p$, and $g_1\le p$.
- Write $s_r=v(u+g_r)$, $L_r=V_{g_r}(u)=\sum_{r'\le r}s_{r'}$, $M_r=\max_{r'\le r}s_{r'}$, and $g_0=L_0=0$.
- Block $r$ is $[g_r,g_{r+1})$. On it $v(\pi_c(u))=L_r$. For $r\ge1$ it has exactly $p$ elements.
- Put $T=T_u$, $T_{<g}=\sum_{c<g}\tilde\delta_c\pi_c(u)$ and $H_c=\sum_{i\le c}1/(u+i)$.

**Lemma Q [proved].** For $1\le k\le V_t(u)$ and every integer $f$,
$$P\big(v(T)\ge k,\ v(T')\ge f\big)\ \le\ P_0\big(g_1,\min(s_1,k)\big)\prod_{r\ge1:\ L_r<k}\pi_r,$$
$$\pi_r=\begin{cases}q_2/p^2&\text{if }s_{r+1}=1\text{ and }L_{r+1}\le\min(f,\,k-M_{r+1})\quad\text{("2D block")},\\ q_d/p^d,\ d=\min(s_{r+1},k-L_r)&\text{otherwise ("1D block")}.\end{cases}$$
(If $L_r<k\le V_t$, then $g_{r+1}\le t$, so every block in the product is full.)

*Proof.*

*Step 0 (events).*
- For $r\ge0$ with $L_r<k$ let $E^T_r=\{v(T_{<g_{r+1}})\ge\min(L_{r+1},k)\}$. Since $v(T-T_{<g_{r+1}})\ge L_{r+1}$, the event $\{v(T)\ge k\}$ is contained in $E^T_r$.
- For $r\ge1$ let $R_r=pT'-pH_{g_r}T$ and $R^{<g}_r=\sum_{c<g}\tilde\delta_c\pi_c(u)(pH_c-pH_{g_r})$.
- **(a)** For $c\ge g_r$: $pH_c-pH_{g_r}=\sum_{g_r<i\le c}p/(u+i)$ and $v(\pi_c/(u+i))=V_c-v(u+i)\ge L_r$. Hence $v(R_r-R^{<g_r}_r)\ge L_r+1$.
- **(b)** If $L_r\le\min(f,k-M_r)$, then on $\{v(T)\ge k,\,v(T')\ge f\}$ we have $v(pT')\ge f+1\ge L_r+1$ and $v(pH_{g_r}T)\ge1-M_r+k\ge L_r+1$. So, by (a), the event $E^R_r=\{v(R^{<g_r}_r)\ge L_r+1\}$ holds.
- Hence the event of the lemma is contained in $A_0\cap\bigcap_{r\ge1,\,L_r<k}A_r$, where:
  - $A_0=E^T_0$;
  - $A_r=E^T_r\cap E^R_{r+1}$ for 2D blocks;
  - $A_r=E^T_r$ otherwise.
- $A_r$ depends only on the digits $\tilde\delta_c$ with $c<g_{r+1}$, i.e. on blocks $\le r$.

*Step 1 (chain rule).* The blocks are independent, so
$$P\Big(\bigcap A_r\Big)\le P(A_0)\prod_{r\ge1}\sup_hP(A_r\mid h),$$
where $h$ ranges over histories (blocks $<r$) in $A_0\cap\cdots\cap A_{r-1}$.

*Step 2 (block 0).* As $u\equiv-g_1\pmod{p^{s_1}}$, we have $\pi_c(u)\equiv\pi_c(-g_1)\pmod{p^{s_1}}$. So $P(A_0)=P_0(g_1,\min(s_1,k))$ exactly.

*Step 3 (1D block $r\ge1$).* Let $g=g_r$, $L=L_r$, $y=u+g$, and $\omega=\pi_g(u)/p^L$ (a unit). Given $h\in E^T_{r-1}$:
- $\tau=T_{<g}/p^L\in\mathbb Z_p$ and $T_{<g+p}=p^L(\tau+\omega F)$, where $F=\sum_{k'<p}\tilde\delta_{g+k'}\pi_{k'}(y)$, because $\pi_{g+k'}(u)=\pi_g(u)\pi_{k'}(y)$.
- So $E^T_r$ says $\tau+\omega F\equiv0\pmod{p^d}$.
- Since $v(y+p)=s_{r+1}\ge d$, we have $\pi_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^d}$. So $F\bmod p^d$ has the law of $Z\bmod p^d$.

Hence $P(E^T_r\mid h)\le q_d/p^d$.

*Step 4 (2D block $r\ge1$).* Notation as in Step 3, now with $s_{r+1}=1$, $L_{r+1}=L+1$ and $\alpha=(y+p)/p$ a unit.
- $pH_{g+p}-pH_g=\sum_{i=1}^p p/(y+i)=1/\alpha+pN$, with $N=\sum_{i=1}^{p-1}1/(y+i)$.
- $pH_{g+k'}-pH_{g+p}=-(1/\alpha+pE_{k'})$, with $E_{k'}=\sum_{i=k'+1}^{p-1}1/(y+i)$.
- Therefore
$$R^{<g+p}_{r+1}=R^{<g}_r-p^L\big(\tfrac1\alpha+pN\big)\tau-p^L\tfrac\omega\alpha\tilde Z,\qquad\tilde Z=\sum_{k'<p}\tilde\delta_{g+k'}P_{k'}(y),\quad P_{k'}(y)=\pi_{k'}(y)\big(1+(y+p)E_{k'}(y)\big).$$
- $E^R_{r+1}$ requires $v(R^{<g+p}_{r+1})\ge L+2$. This forces $\varrho:=p^{-L}R^{<g}_r\in\mathbb Z_p$ (otherwise the probability is 0), and then
$$\tilde Z\equiv(\alpha/\omega)\big(\varrho-(1/\alpha+pN)\tau\big)\pmod{p^2},$$
one residue determined by $h$.
- **$\tilde Z\equiv\sum\tilde\delta_{g+k'}\pi_{k'}(-p)\pmod{p^2}$.** The function $P_{k'}$ is analytic on $\{v(y+p)\ge1\}$ with $p$-integral Taylor coefficients at $-p$: its poles $-i$, $1\le i\le p-1$, have $v(p-i)=0$. Also $P_{k'}(-p)=\pi_{k'}(-p)$, and
$$P'_{k'}(-p)=\pi_{k'}(-p)\sum_{i=1}^{p-1}\frac1{i-p}=-\pi_{k'}(-p)H_{p-1}\equiv0\pmod p,$$
because $H_{p-1}\equiv0\pmod p$ for odd $p$ (pair $i$ with $p-i$). So $P_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^2}$.

Hence $P(A_r\mid h)\le P(E^R_{r+1}\mid h)\le q_2/p^2$. ∎

*Remarks.*
1. Step 4 is where the derivative condition is paid for. The derivative digit of block $r+1$ is a multiple ($1/\alpha$) of its value digit. After eliminating it, the remaining condition falls on the **second** digits of block $r$, through the combination $Z=\sum\zeta_k\pi_k(-p)$, the signed polynomial evaluated at the gate. So every gate of depth 1 below level $f$ costs a factor $q_2/p^2\approx p^{-2}$ instead of $q_1/p\approx p^{-1}$.
2. The bound is sharp: with the exact block-0 factor, $\max P/\text{bound}=1.0000$ in the tests at $p=3,5,7$, and halving the 2D factor produces violations (§9).
3. Lemma Q is an anti-concentration (Littlewood–Offord-type) statement. It bounds the probability of a rare event through the min-entropy of single blocks. It is not an equidistribution statement, which is why it can hold quenched, for every $u$.

## 5. Explicit bounds: Propositions D, E, E′

For a composite window and a point $x$, let $G_1<G_2<\cdots$ be the gates of $x$ in $(n,N']$ and $\lambda_\beta=V_{G_\beta}-V_n$. For $c<H$ let $\beta(c)$ be the first gate after $n+c$, $g_1(c)=G_{\beta(c)}-n-c\in[1,p]$ and $s_1(c)$ its depth. By Lemma Q, applied at $u=x+n+c$ with $t=H-c$ and $k=K-a_c$ (relative levels are $\lambda-a_c$, and $k-L_r=K-\lambda_r$), the factor of each block depends only on the block of $x$. This gives the following.

**Proposition D (pointwise) [proved].** For every $x$ (not a negative integer),
$$p^K\mathrm{Coll}_K(x)\le p^K\Big[2^{-H}+\sum_{c:\,a_c\ge K}2^{-c-1}+\sum_{c:\,a_c<K}2^{-c-1}P_0\big(g_1(c),\min(s_1(c),K-a_c)\big)\,\mathrm{Suf}^{1D}_{\beta(c)}\Big].$$
Here $\mathrm{Suf}^{1D}_\beta=\prod_{\beta'\ge\beta,\ \lambda_{\beta'}<K}q_{d_{\beta'}}/p^{d_{\beta'}}$ with $d_{\beta'}=\min(s(G_{\beta'+1}),K-\lambda_{\beta'})$. Hence $\varepsilon(x)\le(\text{RHS})-1$. With $N'=N$ and $K\to D$ the same formula bounds $p^D\mathrm{Coll}_D=1+\chi_W^2$.

*Proof.* $p^K\mathrm{Coll}_K=2^{-H}p^K+\sum_c2^{-c-1}p^K\,P(v(y_cT)\ge K)$, by the decomposition of Lemma F without the slope condition, and $p^KP(v(T)\ge K-a_c)=p^{a_c}G(\cdot;\cdot,K-a_c,-\infty)$. Apply Lemma Q with $f=-\infty$. ∎

**Proposition E (averaged) [proved].** In the setting of Theorem 1 with $M_W\le K-\theta$,
$$\mathbb E_B[\varepsilon]\le\text{the same expression with }\mathrm{Suf}^{1D}\text{ replaced by }\mathrm{Suf}^{2D},$$
where a block whose end gate has depth 1 and $\lambda_{\beta'+1}\le f':=\min(\theta,K-M_W)$ contributes $q_2/p^2$ instead of $q_1/p$.

*Proof.* Combine Theorem 1, Lemma F and Lemma Q. The pattern is constant on $B$, so the supremum is attained by every point. Lemma Q's running maximum $M_{r+1}$ is replaced by $M_W\ge M_{r+1}$; this only turns some 2D factors into 1D factors, and $q_2/p^2\le q_1/p$. ∎

*Constants for Prop E′.* Put $\tilde q_s=q_s$ for $s\le S$ and $\tilde q_s=q_Sp^{s-S}$ for $s>S$ ($S=8$, or 4 for $p>13$). Then $\Delta_s=\log\tilde q_s-\log\tilde q_{s-1}\ge0$, and
$$\rho_1=\log q_1+\sum_{s\ge2}\Delta_s/p^{s-1},\qquad\gamma=\log q_1-\log(q_2/p),\qquad\kappa=(p-1)\log2-\log p+\rho_1-\gamma(p-1)^2/p^2.$$
At $p=7$: $\rho_1=0.06041$, $\gamma=1.85344$, $\kappa=0.91167$.

**Proposition E′ (closed form) [proved].** In the setting of Proposition E, let $\sigma\ge M_W$ and $f'=\min(\theta,K-\sigma)$. If $\kappa>0$, then
$$\mathbb E_B[\varepsilon]\le p^K2^{-H}(1+2^p)+2^{p+\sigma(p-1)}\exp\Big(K\rho_1+\log\tfrac{\tilde q_\sigma}{q_1}+\gamma\big(2-\tfrac1p\big)-\gamma(f'-\sigma+1)\tfrac{(p-1)^2}{p^2}\Big)\frac{e^{-\kappa}}{1-e^{-\kappa}}.$$

*Proof.*
- **Base terms.** The terms $a_c\ge K$ have $c\ge H-p$, because the last gate is within $p$ of $N'$; they contribute $\le p^K2^{-(H-p)}$. Use $P_0\le1$.
- **Grouping by first gate.** The $c$ with $\beta(c)=\beta$ satisfy $c\ge G_{\beta-1}-n\ge G_\beta-n-p$, so their weights sum to $\le2^{p-(G_\beta-n)}$. By R3M Lemma 1(b) on $(n,G_\beta]$, $G_\beta-n\ge(\lambda_\beta-\sigma)(p-1)$. Moreover $p^K\mathrm{Suf}_\beta=p^{\lambda_\beta}\prod_{\beta'}C_{\beta'}$, with $C=p^d\pi\in\{q_2/p,\ q_d\}$.
- **Deep end gates.** Over the $R\le K-\lambda_\beta$ blocks from $\beta$ on, the end-gate depths are $1+v(\mu+i)$ for consecutive $i$, with $\mu=(x+G_1)/p$. So $\#\{s\ge s_0\}\le R/p^{s_0-1}+1$, and $\sum\log C\le R\rho_1+\log(\tilde q_\sigma/q_1)-\gamma\cdot\#2D$.
- **2D blocks.** By Legendre on the depths, $\lambda_{\beta+t}-\lambda_\beta\le tp/(p-1)+\sigma-1$. So at least $J\ge(f'-\lambda_\beta-\sigma+1)(p-1)/p-1$ consecutive blocks have end level $\le f'$, and at most $J/p+1$ of them have a deep end. Hence $\#2D\ge J(1-1/p)-1$.
- **Sum over levels.** The $\lambda_\beta$ are distinct integers $\ge1$. Inserting these bounds, the summand is $\le\mathrm{const}\cdot e^{-\kappa\lambda}$; sum over $\lambda\ge1$. ∎

Proposition E′ dominates the block form in 140/140 random windows at $p=5,7,11$ (`eprime_check.py`), as its derivation requires.

## 6. Theorem M: FE for an explicit atom at $p=7$, hence $\mu(K_7)>0$

**The atom** (file `data/round4/M4A/atom_p7.txt`, found by `find_atom.py 7 1 300 405`):
$$x_A=8482778585152010705975786324668215228635086,\qquad m=V_{300}(x_A)=51,\qquad A=x_A+7^{51}\mathbb Z_7 .$$
The path $e\in\{0,1\}^{300}$ is stored as a bit string with $e_0=1$. By exact integer evaluation, $v_7(S_e(x_A))=51\ge m$ and $S_e'(x_A)\equiv6\pmod7$. So $e\in P^0_{300}$ on all of $A$ (R3M Lemma 2(a)) and $Z^0_{300}\ne0$ on $A$.

The window times are $n_0=300$, $n_{\ell+1}=\lceil27n_\ell/20\rceil$ ($r=1.35$), i.e. $300,405,547,739,998,1348,\dots$. For $W_0=[300,405)$: $D_0=17\le m-M_{405}=51-4$ and $M_{405}<51$. So $A$ is admissible (C3 with $j=0$).

*Digits.* For $s\le m-1$ put $i_s=(-x_A)\bmod7^s$ (or $7^s$). For $x\in A$ and $i<i_A:=i_{51}\approx4.1\cdot10^{42}$, $v(x+i)\ge s$ iff $i\equiv i_s\pmod{7^s}$. Hence, for $N<i_A$,
$$V_N=\sum_{s<m:\,i_s\le N}\big(\lfloor(N-i_s)/7^s\rfloor+1\big),\qquad M_N=\max\{s<m:i_s\le N\},$$
exactly and constant on $A$. This was checked against direct valuations.

**Theorem M [computer-assisted].** With the thresholds below, $\Pi_A\le10^{25.7344}$, $\delta_A\le1.0006\cdot10^{-45}$ and $\Pi_A\delta_A\le10^{-19.265}$. Hence, by Theorem C3,
$$\mu(K_7\cap A)\ge1.843\cdot10^{-26}\,\mu(A)=1.843\cdot10^{-26}\cdot7^{-51}\quad(\approx1.5\cdot10^{-69}),\qquad\text{so }\mu(K_7)>0.$$

*Proof* (each phase is evaluated by `fe_verify.py` in mpmath interval arithmetic at 200 bits; log `data/round4/M4A/fe_verify_final.log`).

*Phase 0.* Proposition D for $W_0$ gives $\chi^2_0\le0.5046$.

*Phase 1 ($1\le\ell\le8$, pointwise).* The composite windows $[n_{\ell-1},n_{\ell+1})$ end below $i_A$, so their gate patterns are constant on $A$. The linear-regime part of $B_\ell$ holds on all of $A$ (exact check). Set $\bar\varepsilon_\ell:=$ (Prop D bound) $-1$. Then $\varepsilon_\ell\le\bar\varepsilon_\ell$ on all of $A$, and these windows never stop $\tau$:

| $\ell$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $D,K$ | 17,40 | 23,56 | 33,76 | 43,101 | 58,136 | 78,184 | 106,249 | 143,337 |
| $\bar\varepsilon_\ell$ | 1.64 | 12.9 | 98.6 | 138 | 336 | 3835 | $4.64\cdot10^5$ | $4.96\cdot10^7$ |

*Phase 2 ($\ell\ge9$, $n_{\ell+1}\le60000$; Markov).* For $\ell>8$ set $\bar\varepsilon_\ell=2^{-(\ell-8)}$. Take $B=A$ ($b=51$) in Theorem 1: the window's pattern is constant on $A$, and $D\ge194$, so $\lfloor D/2\rfloor+1\ge51$ and $\theta=\lceil D/2\rceil$. Proposition E gives, e.g.:
- $\ell=9$, $[3317,4478,6046)$, $D=194$, $K=456$, $\theta=97$: $\mathbb E_A\varepsilon_9\le10^{-45.30}$;
- $\ell=10$: $\le10^{-61.0}$; $\ell=11$: $\le10^{-84.2}$;
- $\ell=12,\dots,16$: $\le10^{-114}$, $10^{-154}$, $10^{-209.8}$, $10^{-210.5}$, $10^{-210.4}$ (the last three are capped by the rigorous truncation of the $c$-sum at $c^*=\lfloor K\log_27\rfloor+700$).

Markov gives $\mu_A(\varepsilon_\ell>\bar\varepsilon_\ell)\le2^{\ell-8}\mathbb E_A\varepsilon_\ell$.

*Phase 3 ($n_{\ell+1}<i_A$, $\ell\le306$).* The same, with Proposition E′, exact $D,K$ from the digit formula, and $\sigma=M_{n_{\ell+1}}\le50<b$. Every window satisfies the linear regime (exact check), and $\log_{10}$ of the failure probability falls from $-476.9$ ($\ell=17$) to $-3.8\cdot10^{39}$ ($\ell=300$). The sum of phases 2–3 is $\le1.0006\cdot10^{-45}$, dominated by $\ell=9$.

*Phase 4 ($n_{\ell+1}\ge i_A$, all $\ell\ge307$).* Positions $i\in I_A=i_A+7^{51}\mathbb N_0$ are random gates of depth $\ge51$. Let $G'=\{\forall i\in I_A:\ v(x+i)\le m+2\log_7i+10\}$. Then
$$\mu_A(G'^c)\le7^{-10}\big(i_A^{-2}+7^{-102}\pi^2/6\big)\le2.47\cdot10^{-94}.$$
On $G'$, every gate up to $n_{\ell+1}$ has depth $\le\sigma_\ell=m+\lceil2\log_7n_{\ell+1}\rceil+11$. Partition $A\cap G_\ell$ into balls of radius $7^{-(\sigma_\ell+1)}$, on which the pattern is constant, and apply Proposition E′ on each.

With $n=n_{\ell-1}$ we have $n_{\ell+1}-n\le(r^2-1)n+r+1$, $D\ge v((n_\ell-n)!)\ge(r-1)n/6-\log_7H^+-1$, $K\le H^+/6+\sigma$, and $\ell\le1+\log(n/300)/\log r$. This gives $\log(\text{failure}_\ell)\le\Phi(n)$ with
$$\Phi(n)=-c\,n+O(\log n),\qquad c=\gamma\tfrac{(p-1)(r-1)}{2p^2}-\tfrac{(r^2-1)\rho_1}{p-1}=0.0314 .$$
Every logarithmic term is concave and increasing, so $\Phi(n)+c'n$, with $c'=c/2=0.015718$, is bounded by its tangent line at $n^*=n_{306}=2.29\cdot10^{42}$. The program checks that both its value ($\le-3.6\cdot10^{40}$) and its slope ($<0$) are negative, for both branches. The same tangent argument shows $D\ge2\sigma$ and the linear regime on $G_\ell$ for all $\ell\ge307$. Hence
$$\sum_{\ell\ge307}\text{failure}_\ell\le\sum_{N\ge n^*}e^{-c'N}\le10^{-1.56\cdot10^{40}} .$$

*Total.* Each $G_\ell^c$ is contained in $G'^c$, and on $G'$ the linear regime holds in phase 4. So $\delta_A\le\sum_{\ell=9}^{306}\text{failure}_\ell+\sum_{\ell\ge307}\text{failure}_\ell+\mu_A(G'^c)\le1.0006\cdot10^{-45}$, and
$$\log_{10}\Pi_A\le\log_{10}\Big[(1+\chi^2_0)\prod_{\ell\le8}(1+\bar\varepsilon_\ell)\cdot\prod_{i\ge1}(1+2^{-i})\Big]\le25.7344 .$$
The atom is admissible, and $\varepsilon_\ell$ and $\bar\varepsilon_\ell$ are exactly the objects of Theorem C3. Theorem C3 applies. ∎

**Corollary M′ [computer-assisted].** The same verification succeeds with $n_0=300$, the same $r$, $\ell_1=6$, and atoms found by `find_atom.py p p 300 405` (files `atom_p{11,13,17,19,23}.txt`). It gives $\mu(K_p\cap A_p)/\mu(A_p)\ge$:

| $p$ | $m=V_{300}(x_A)$ | $\log_{10}\Pi_A$ | $\log_{10}\delta_A$ | $\log_{10}(\Pi_A\delta_A)$ | lower bound for $\mu(K_p\cap A)/\mu(A)$ |
|---|---|---|---|---|---|
| 7 | 51 | 25.73 | −45.00 | −19.27 | $1.84\cdot10^{-26}$ |
| 11 | 30 | 3.98 | −24.74 | −20.76 | $1.06\cdot10^{-4}$ |
| 13 | 26 | 1.31 | −23.23 | −21.92 | $4.90\cdot10^{-2}$ |
| 17 | 18 | 2.46 | −20.56 | −18.10 | $3.48\cdot10^{-3}$ |
| 19 | 16 | 0.96 | −17.59 | −16.63 | $1.09\cdot10^{-1}$ |
| 23 | 14 | 0.68 | −17.40 | −16.72 | $2.07\cdot10^{-1}$ |

For $p\ge11$, $q_1$ is within $1.5\cdot10^{-3}$ of 1, so Proposition D is almost lossless and $\Pi_A$ is moderate.

## 7. The chain, re-checked adversarially

I re-checked the chain twice. The first pass followed the derivation as written. The second worked from the code and the tests back to the statements, looking for any place where a hypothesis was used but not verified.

**Every lemma Theorem M depends on.**

| ingredient | source | status | how its hypotheses are met in Theorem M |
|---|---|---|---|
| R3M Lemma 1 (a)–(e) | round 3 | proved, checked | used for Legendre bounds ($V$, $D$, $K$) and Taylor's formula |
| R3M Lemma 2, Prop A, Cor A′ | round 3 | proved, checked (exact tests by two programs) | inside C3, via the linear regime, which is checked for every window |
| R3M Prop B, Prop C2 | round 3 | proved, checked (C2 equality in 95/95 single-parent cases) | inside C3. The identification $\varepsilon=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$ is part of C2 under (5.2) |
| R3M Thm C3 (note Thm 11.14) | round 3 | proved, checked; re-read here | admissible atom (exhibited path), deterministic times, summable $\bar\varepsilon$, FE verified |
| Lemma H, Theorem 1 | §2 | proved; 51/51 exact | the ball is $A$ itself (phases 2–3) or radius $7^{-(\sigma_\ell+1)}$ (phase 4). Pattern constant on it; $\lfloor D/2\rfloor+1\ge b$ |
| Lemma F | §3 | proved; 36/36 exact (with Q) | $M_W\le K-\theta$ asserted for every window |
| Lemma Q | §4 | proved; tight exact tests; algebra exact at high levels | $k\le V_t(u)$ holds since $k=K-a_c=V_{H-c}(x+n+c)$ |
| constants $q_s$, $P_0$ | §4 | exact enumeration (DP for $p>13$, validated) | — |
| Props D, E, E′ | §5 | proved; exact tests; E′ dominates E | — |
| interval evaluation | `fe_lib.py`, `fe_verify.py` | computer-assisted | outward rounding; phases 0–2 recomputed in exact rationals by `fe_crosscheck.py` (different code path) with identical values |

**Points that were specifically attacked.**
1. *Is Lemma Q's 2D factor really $q_2/p^2$ uniformly in the history?*
   - The event $E^R_{r+1}$ alone pins $\tilde Z\bmod p^2$ to one residue determined by the history; the history need not satisfy the earlier $E^R$.
   - The algebra (decomposition (1), $\tilde Z\equiv\sum\zeta\pi(-p)\pmod{p^2}$, the valuation claim (a)) is checked exactly at levels up to about 30, with negative controls that fail.
   - With the exact block-0 factor the bound is attained, and halving the 2D factor gives violations at $p=3,5,7$.
2. *Is Theorem 1 applied on a legitimate ball?*
   - In phases 2–3 the ball is the atom $A$ itself. Every composite window ends before $i_A\approx4\cdot10^{42}$, so all valuations in it are those of $x_A$, constant on $A$.
   - $D\ge194\ge2\cdot51-2$ gives $\theta=\lceil D/2\rceil$.
   - In phase 4 the balls have radius $7^{-(\sigma_\ell+1)}$, with $D\ge2\sigma_\ell$, inside $G_\ell$.
3. *Does Markov's inequality apply?*
   - $\varepsilon\ge0$ (it is an $L^2$ band mass).
   - In phases 2–3, $\mathbb E_A$ is the normalised Haar average over the atom, exactly the measure in FE.
   - In phase 4, $\mathbb E_A[\varepsilon\mathbf 1_{G_\ell}]=\sum_B\mu_A(B)\mathbb E_B\varepsilon$, since $G_\ell$ is a union of such balls.
4. *Pointwise thresholds in phase 1.*
   - Proposition D is a bound for each $x$, depending only on the gate pattern, which is constant on $A$.
   - So $\varepsilon_\ell\le\bar\varepsilon_\ell$ on all of $A$, and these windows contribute nothing to $\delta_A$.
5. *Times, indices, ranges.*
   - $j=0$ and windows $\ell\ge1$ use $[n_{\ell-1},n_{\ell+1})$, with $D=D_{\ell-1}$ and $K=D_{\ell-1}+D_\ell$, as in C3.
   - Phases 1–3 cover $1\le\ell\le306$, and phase 4 covers every $\ell\ge307$.
   - The linear-regime condition is checked exactly for $\ell\le306$, and analytically (tangent-line argument) for $\ell\ge307$ on $G'$.
6. *Arithmetic.*
   - Intervals are evaluated at 200 bits, and the margin is 19 orders of magnitude.
   - The truncation of the $c$-sums is bounded rigorously (each omitted term $\le2^{-c-1}p^K$).
   - The infinite product $\prod_{i\ge1}(1+2^{-i})=2.38423\ldots$ is bounded by $2.3843$.
7. *Could the result contradict anything known?* See the next paragraph. It also agrees with the round-3 heuristics:
   - the median $\varepsilon_\ell$ at $p=7$ decays (R3M §7.3);
   - the Paley–Zygmund ratios improve with $p$ (R3M §7.1);
   - our lower bounds for $\mu(K_p\cap A)/\mu(A)$, e.g. $0.05$ at $p=13$ and $0.11$–$0.21$ at $p=19,23$, are below the numerical values of $\mu(K_p)$ (note §5).

**How the proof respects each obstruction of the brief.**
- *Theorem 3.6 ($K_p$ nowhere dense; no residue-class criterion).* Nothing here is a residue-class criterion. $K_7\cap A$ is a closed nowhere dense set of positive measure (a "fat Cantor set"), and the proof only produces a lower bound on its measure. No integer is placed in $K_7$, so Q3 is untouched.
- *Proposition 11.12 (per-window Cauchy–Schwarz fails).* Not used. The $L^2$ recursion is C3's two-window inequality, and the mod-$p$ shell $\chi^2_0$ of the first window enters once, as the factor $1+\chi^2_0\le1.51$.
- *Proposition 11.15(b) ($\int_{\mathbb Z_p}\Lambda_t\,d\mu=\infty$).*
  - We never average over $\mathbb Z_p$. We average over one atom, on which the gate pattern is fixed up to $4\cdot10^{42}$. Beyond that, random deep gates are truncated by $G'$, at cost $2.5\cdot10^{-94}$.
  - The double root of $(y+2)^2$ appears explicitly as $P_0(2,s)=\tfrac14$ for all $s$. A gate of depth $s$ two steps after $n+c$ costs a factor $p^s/4$, which is finite on the atom. This is exactly R3M's "$\kappa p^s$" growth, now with a proof.
- *Theorem 3.10 / Proposition 11.23 (barrier lemmas).*
  - The deterministic bounds (Prop D, phase 1) are not uniform. A gate of depth $s$ costs $q_s=7^s\cdot\frac3{256}$ for $s\ge4$, i.e. it uses $s$ digits of the unit parts and grows like $p^s$, as the $L^2$ barrier requires. They are only used for eight windows, where the depths are $\le5$.
  - All the decay comes from averaging over the digits of $x$ (Theorem 1): the loophole named in the brief. Lemma Q is an anti-concentration bound for rare events, not an equidistribution or covering statement.

**What the result does not say.** It does not give $f(a,7)=\infty$ for any natural $a$. The constant is tiny: $\mu(K_7)\ge1.4\cdot10^{-69}$, against the numerical value $\approx0.62$. It is not uniform in $p$. It rests on the round-3 results listed above, which were AI-checked but not human-refereed.

## 8. Failed attempts and where they break

1. **(S) as "the high-slope mass is small at every scale".** False at small scales. In the exact tests of Theorem 1 the two high-slope terms are $\approx0.6$–$1.3$ each, while $\mathbb E_B\varepsilon\approx0.01$; they cancel. The high-slope mass becomes small only as $D\to\infty$ (Lemma Q: $\approx(q_2/p)^{\#2D}$). So the bound must be taken at large $D$, and the early windows must be paid for pointwise (phase 1).
2. **Distinct-level counting (the brief's hint).** It gives a factor $\le\frac12$ per level, while each level costs $p$ in the normalisation, so at odd $p$ it can never beat $p^K$. It is replaced by the min-entropy of a whole gate block (the constants $q_s$). The derivative condition is paid through the second digit of the previous block (Lemma Q, Step 4), not through distinct levels.
3. **Second-derivative persistence inside one cylinder (the Prop 10.7 / R3Q Lemma 9 template).** The slope threshold $\theta\approx D/2$ is below the cylinder scale $m$. So within a fine cylinder the slope is frozen and nothing is gained. The gain must come from a coarse ball, which Theorem 1 provides.
4. **Averaging for the first windows after the atom.** On the atom ($b=m=51$), Theorem 1 gives a slope threshold $\theta=\min(\lceil D/2\rceil,D-50)$. This threshold is $\le0$ for $D\le50$ (windows 1–4: $D=17,23,33,43$) and small for the next windows. So the averaged bound is useless there, and it becomes small only once $D\gtrsim2m$. Averaging over balls coarser than the atom would destroy the Paley–Zygmund ratio, which equals 1 only on an atom. So these windows get pointwise thresholds (Prop D), at a cost $\Pi_A\approx10^{25.7}$ at $p=7$. At $p\ge11$ the cost is small ($10^{0.7}$–$10^{4}$).
5. **The choice $\bar\varepsilon_\ell=\sqrt{\mathbb E\varepsilon_\ell}$** gives $\log_{10}(\Pi_A\delta_A)\approx+7$ (exploration at $n_0=200$–$400$, $r=1.3$). The choice $\bar\varepsilon_\ell=2^{-(\ell-\ell_1)}$ works because $\mathbb E\varepsilon_\ell$ decays super-exponentially in $\ell$.
6. **$p=3,5$.** The closed-form rate $c=\gamma(p-1)(r-1)/(2p^2)-(r^2-1)\rho_1/(p-1)$ is negative for every $r>1$ at $p=5$ ($\rho_1=0.2216$, $\gamma=0.975$), and at $p=3$. The 1D growth per level, driven by $q_1=1.035$ and by $q_s$ for deep gates (depth-2 gates are frequent), beats the 2D gain. This is a failure of the method, not evidence against $\mu(K_p)>0$.
7. **All $p\ge p_0$.** A uniform version needs $\rho_1\lesssim\log p/(2(r+1))$, i.e. nontrivial anti-concentration of signed subset sums of $\{k!\bmod p\}$ and $\{\pi_k(-p)\bmod p^2\}$, uniformly in $p$. We do not know a Littlewood–Offord-type bound of this strength for these specific sets. The non-concentration of $\{k!\bmod p\}$ is itself flagged as open in note §10.5. We therefore verify prime by prime.
8. **The truncation event $G_\ell$ of the brief** ("no deep gate near the start of $W_{\ell-1}$") turned out to be unnecessary before $i_A\approx p^{m}$. On the atom the gate pattern is deterministic there, and its effect is priced exactly through $P_0$ and $q_s$. A truncation is used only for the random gates beyond $i_A$ (the event $G'$).

## 9. Numerical tests (all exact unless stated; logs in `data/round4/M4A/`)

| claim | program | runs | result | log |
|---|---|---|---|---|
| Thm 1 (identity) | `hensel_identity_check.py` | $p=3,5,7$; 11 parameter sets (5 of them met no ball satisfying the conditions) | **51/51 exact**; two-sided bound 51/51 | `hensel_identity.log` |
| Lemma Q (inequality) | `lemma_q_check.py` (exact integer DP over $(T\bmod p^k,T'\bmod p^f)$) | $p=3$ ($k\le9,f\le4$), $p=5$ ($k\le7,f\le3$), $p=7$ ($k\le5,f\le2$); random, planted deep gates, integer-like $u$ | **12093 tests, 0 failures**; with the exact block-0 factor max P/bound $=1.0000$ (bound attained); negative control (2D factor $\times\frac12$, exact block-0 factor): violations in all 5 control runs (101 cases); two earlier controls without the exact block-0 factor ($\times\frac13$) were insensitive and are superseded | `lemma_q_check.log` |
| Lemma Q (algebra of Step 4, Step 3) | `lemma_q_algebra_check.py` (exact rationals, $t\le150$) | $p=3,5,7,11$ | 510 identity checks + 5314 blocks, **0 failures**; controls (one digit stronger): 232 failures in 250 | `lemma_q_algebra.log` |
| Lemma F + Q (composite level) | `lemma_f_check.py` | $p=3,5,7$ | **36/36**, max HS/bound 0.55 | `lemma_f_check.log` |
| Props D, E | `bounds_check.py` | $p=3,5,7$ | **52/52** both; Prop D max ratio 0.98 (nearly tight) | `bounds_check.log` |
| Prop E′ ≥ Prop E | `eprime_check.py` (intervals) | $p=5,7,11$, 140 windows | **140/140** | `eprime_check.log` |
| DP constants | `qdp_check.py` | $p\le13$ | equal to enumeration | `qdp_check.log` |
| admissible atoms | `find_atom.py` (+ direct re-check in `fe_verify.py`) | $p=7,11,13,17,19,23$ | all admissible; the $p=7$ atom file reproduced identically | `find_atom.log` |
| FE (Thm M, Cor M′) | `fe_verify.py` (intervals) | $p=7$ ($\ell_1=8$), $p=11,\dots,23$ ($\ell_1=6$) | FE holds; table in §6 | `fe_verify_final.log` (also `fe_verify.log`: earlier runs, including one with too strict a phase-4 rate at $p=23$, superseded) |
| FE phases 0–2 (second code path) | `fe_crosscheck.py` (exact rationals) | $p=7,11,13$ | identical to `fe_verify.py` | `fe_crosscheck.log` |

Exploration scripts (not part of any proof) were run in `/tmp/r4_M4A/` and are not kept: float scans of the bounds along windows and of the choice of $r$ and $\ell_1$.

## 10. What remains open

1. **Independent verification** of Lemma Q, Theorem 1, Lemma F and the FE computation, by another instance or a referee. Ideally there should also be a fully independent re-implementation of `fe_verify.py`, phase 3 and the phase-4 tangent argument included. Human refereeing of the whole chain, including R3M's C3 on which it rests, has not happened.
2. **$p=3$ and $p=5$.** The method fails there (§8.6). A sharper treatment of depth-2 gates (whose blocks could pay two digits jointly with the previous block) or a different window schedule might change $\rho_1$, but we did not find one.
3. **All $p\ge7$.** This needs uniform anti-concentration of $\sum\zeta_kk!\bmod p$ and $\sum\zeta_k\pi_k(-p)\bmod p^2$ (§8.7). It could also be done by machine verification prime by prime, but only finitely many primes can be checked.
4. **Better constants.** At $p=7$ the bound $1.84\cdot10^{-26}$ comes from the pointwise phase. Averaging at an intermediate scale for the first eight windows, or a later starting atom, could improve it. The numerical $\mu(K_7)\approx0.62$ is far above.
5. **Positive slopes.** The slope-0 martingale sees only part of $K_p$. Extending Prop B/C2 to the frozen-weight martingale (R3M §10 item 2) would matter for constants, not for positivity.
6. **Q3** (a natural number in $K_p$) is untouched; the measure method cannot reach it.

## 11. Computational record

All runs used `code/round4/M4A/run.sh LOG TIMEOUT cmd...` (`nice -n 10`, wall-time limit, command and exit code logged). Budget used: about 21 core-minutes of logged runs plus about 5 minutes of unlogged exploration, on one core; the longest single job was 488 s. Commands (the log files contain all of them):
- `python3 hensel_identity_check.py p SEED NB n H1 H2 b KMAX [FORCE]`
- `python3 lemma_q_check.py p SEED NU tmin tmax KMAX FMAX [rand|deep|g2|p0|int [CTRL]]`
- `python3 lemma_q_algebra_check.py p SEED NTESTS tmax [1]`
- `python3 lemma_f_check.py p SEED NB n H1 H2 b KMAX`
- `python3 bounds_check.py p SEED NB n H1 H2 b KMAX`
- `python3 eprime_check.py p SEED NW nmin nmax`
- `python3 qdp_check.py`
- `python3 find_atom.py p SEED 300 405 2000000 data/round4/M4A/atom_pP.txt`
- `python3 fe_verify.py data/round4/M4A/atom_p7.txt 8 60000` (and `atom_pP.txt 6 60000` for $p=11,\dots,23$)
- `python3 fe_crosscheck.py data/round4/M4A/atom_pP.txt LMAX L1`

Library files: `m4a_lib.py` (valuations), `bounds.py` (exact constants and exact-rational bounds), `fe_lib.py` (interval bounds).

## 12. Credit

- **Machinery.** The odd-$p$ window identity, the second-moment identity, the two-window inequality and the conditional Theorem C3 are track R3M's (round 3; checked by the round-3 checker and referee). Theorem C3 is the frame in which this report works. Remark C6 of R3M proposed the route (S) + truncation that §§2–5 carry out.
- **Earlier work.** The quenched martingale at $p=2$ is track R1b's (round 2). The template of a high-slope window bound on coarse atoms and of second-derivative control near $-2$ is track R3Q's (round 3, Lemmas 8–9). Lemma Q replaces these by a block anti-concentration bound.
- **Block-0 probabilities.** The exact block-0 probabilities $P_0$ evaluate the signed polynomial at the integer point $-g$. This is the mechanism of the round-3 checker's Observation G and of R3M's Proposition N3.
- **Classical tools.** Hensel's lemma; the Paley–Zygmund inequality; Doob's $L^2$ martingale convergence; the second-moment method for trees (Lyons); branching processes in random environments as background (Smith–Wilkinson, Athreya–Karlin; Afanasyev–Geiger–Kersting–Vatutin); Littlewood–Offord-type anti-concentration as the guiding idea of Lemma Q; Legendre's formula.
- **Background.** The problem is due to Erdős and Graham. The normal form and the branching picture at $p=2$ are Kitamura's (note §§1–2).
- **This work.** Everything in this report was produced in an AI-assisted session (track M4A of round 4) and has not been checked by a human.
