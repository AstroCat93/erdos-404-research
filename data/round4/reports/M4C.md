# Round 4, track M4C: strategy C ("large $p$") for $\mu(K_p)>0$

*Lead's note after the adversarial verification (`data/round4/checks/M4C_*.md`): Theorem M is confirmed under three lenses, with two independent recomputations of every certificate. Required corrections, applied in note.md §12: "verifies FE completely, with no truncation" is withdrawn — the proof truncates at deep gates and pays for it via Lemma L(a), and the truncation is necessary (Proposition O1′ of the obstruction check); Corollary M′ is [heuristic, not proved] throughout (including the §0 table); the far tail beyond 10^60 now has an explicit majorant (≤ 10^(−2.6·10^58), derived by the logic check) in place of the hard-coded remainder; two displayed inequalities of §4.2 are corrected (conclusions unchanged); the p = 11 row should print Π_A ≤ 10.61823 and δ_A ≤ 0.0874275.*


Date: 2026-10-13/14. Code: `code/round4/M4C/`. Logs: `data/round4/M4C/` (every run starts with `### command:` and `### start:` and ends with `### wall:`). Scratch: `/tmp/r4_M4C/`.
Notation: note.md §10.1 and `data/round3/reports/R3M.md` §1 (restated in §1 below).

## Headline

**$\mu(K_p)>0$ for every prime $11\le p\le97$ [computer-assisted] (Theorem M, §7).** For each such $p$ we prove
$$\mu\big(K_p\cap p^3\mathbb Z_p\big)\ \ge\ c_p\,p^{-3},$$
with an explicit $c_p$: $c_{11}\ge1.25\cdot10^{-4}$, $c_{13}\ge0.572$, and $c_p\ge0.69$ for $17\le p\le97$ (table in §7.3). The proof applies R3M's conditional Theorem C3 (note Theorem 11.14) to the single atom $A=p^3\mathbb Z_p$ at time $n_0=3p$, and verifies its hypothesis FE completely, with no truncation and no Monte Carlo. The only computer input is the exact evaluation of three rational constants $q_1(p),q_2(p),q_3(p)$ (anti-concentration constants of one gate block, §4.3), of finitely many integer inequalities, and of explicit closed-form sums. Every lemma used is proved in full below. All of them except the elementary Lemmas 5.1 and L were also tested in exact arithmetic (§10), and the whole assembly was re-implemented independently and reproduced to all printed digits (§8, item 12).

This is a measure statement. It does not place any natural number in $K_p$ ($K_p$ is nowhere dense, note Theorem 3.6), and it says nothing about Q3.

**What strategy C ("large $p$") delivers, and what it does not.**
1. *Large $p$ makes the method easy, for an arithmetic reason.* Every bound reduces to the constants $q_1(p)$ and $q_2(p)$ of §4.3, which measure how far signed subset sums of $\{r!\}_{r<p}$ (and of the pairs $(r!,\,r!H_r)$) are from equidistribution modulo $p$. They converge to $1$ extremely fast: $q_1-1=1.4\cdot10^{-2},\,2.2\cdot10^{-5},\,6.1\cdot10^{-7},\,5.4\cdot10^{-9}$ and $q_2-1=0.11,\,8.1\cdot10^{-3},\,2.9\cdot10^{-4},\,2.3\cdot10^{-6}$ at $p=7,13,17,23$ (§4.3, exact). With $q_1,q_2$ this close to $1$, the whole "initial phase" up to time $p^3$ is handled *pointwise* (Proposition P1), and the remaining tail is $p^{-\Omega(\text{window})}$.
2. *An "all $p\ge p_0$" theorem needs one arithmetic input that is not available.* The proof works for every $p$ for which $q_1,q_2,q_3$ are close enough to $1$. Uniform bounds on them for all large $p$ are statements about the distribution of $r!$ and $r!H_r$ modulo $p$ (and of falling factorials modulo $p^3$). We could not prove them, and we know of no result that gives them; even equidistribution of $\{r!\bmod p\}$ is open (§9). So for all $p\ge p_0$ we only have a precise reduction (Corollary M′, conditional on the hypothesis AC($p$) of §9) together with the computations for $p\le97$.
3. *$p=7$ is not covered* by this proof: the deterministic phase leaves too short a window at time $p^3$ (§7). Track M4A reports a separate proof at $p=7$ (and at $p\le23$); we have not checked it, and the two proofs were written independently (§14).

**New results used in the proof [proved]:**
- **Lemma P** (quenched 1D anti-concentration). $P(v(T)\ge k)\le\prod_{\rm blocks}\max_aP(S_i\equiv a)$ for any signed sum $T=\sum\delta_c\pi_c(y)$ with independent digits, pointwise in $y$.
- **Lemma Q** (quenched value–derivative anti-concentration). Every full block ending at a depth-1 gate below level $f$ contributes $q_2(p)/p^2$ to $P(v(T)\ge k,\ v(T')\ge f)$. The block statistic is $\big(A\bmod p,\ \lfloor A/p\rfloor-B\bmod p\big)$ with $A=\sum\delta_rr!$, $B=\sum\delta_rr!H_r$.
- **Lemma H2 and Proposition H′** (multi-scale Hensel reduction). The ball-averaged fine-scale mass $\mathbb E_B[\varepsilon]$ is bounded by the normalised mass of signed paths whose slope is at least $\lceil D/2\rceil-V_j$. This makes R3M's Remark C6 rigorous, with an explicit threshold and without any martingale argument. Track M4A states an identity of the same kind (its Theorem 1); we have not compared the proofs.
- **Proposition W** (an explicit slope-0 path). For every prime $p\ge7$ and every $x\in p^3\mathbb Z_p$ there is a slope-0 path alive at $3p$. For non-Wilson $p$ its first block is $\{0,p-1\}$, and the slope is $-w_p/(\xi+1)\bmod p$ with $w_p$ the Wilson quotient; for the Wilson prime $13$ an explicit first block is given.
- **Proposition P1** (deterministic phase). On $A$, every window before time $p^3$ satisfies the linear-regime condition, and $\varepsilon_\ell\le q_1^{n_1}q_2^{n_2}-1$ pointwise.
- **Lemmas T, T′** (tail). Explicit bounds for $\mathbb E_A[\varepsilon_\ell\mathbf 1_{G_\ell}]$ and $\mu_A(G_\ell^c)$ for all later windows.

**Secondary results [proved], not needed for Theorem M:**
- Theorem E / F: a pathwise Chebyshev form of R3M's two-window bound. It gives $\mu(K_p\cap A)/\mu(A)\ge\frac1{4(1+\chi^2)}-\sum_\ell\mathbb E_A[\min(1,16\varepsilon_\ell)]-(\text{lin failures})$. This needs no summable thresholds and no truncation (the $\min(1,\cdot)$ caps deep gates), and it averages over atoms.
- Lemma D1 / Theorem D2: a deterministic two-window recursion for *all* alive paths, with no linear-regime or slope condition. Its hypothesis is an $L^1$ (sup-norm) band bound.
- Proposition Q: an exact formula for the annealed band mass of two-block composites. Exact values: $6.7\cdot10^{-4}$ ($p=7$), $6.5\cdot10^{-8}$ ($p=13$), $7.4\cdot10^{-15}$ ($p=23$).

## 0. Results at a glance

| # | statement | status |
|---|---|---|
| Lemma H2 | $p^K\mu_B(v(F)\ge K)-p^D\mu_B(v(F)\ge D)\le p^K\mu_B\{v(F)\ge K,\ 2v(F')\ge D\}$ for $D\ge2r$ | proved; exact tests: 0 failures in 6152 trials |
| Prop H′ | $\mathbb E_B[\varepsilon]\le c_{L+L'}+\sum_j\frac{c_j}2\mathbb E_B\Lambda^{(\lceil D/2\rceil-V_j)}_{L+L'-j}(z+j)$ | proved; the underlying pointwise identity holds exactly at 364/364 points ($p=3,5,7$) |
| Lemma P | quenched 1D block bound | proved; exact tests |
| Lemma Q | quenched value/derivative block bound with $q_2(p)/p^2$ | proved; exact tests |
| §4.3 | exact $q_1,q_2,q_3$ for $p\le97$ | computer-assisted (two independent DPs; brute force for $p\le13$) |
| Prop W | explicit slope-0 path alive at $3p$ on $p^3\mathbb Z_p$ | proved; exact checks |
| Prop P1 | deterministic phase on $A$: lin and $\varepsilon_\ell\le q_1^{n_1}q_2^{n_2}-1$ | proved (+ finite integer checks) |
| Lemma T, T′ | tail bounds on $A$ | proved; T′ dominates T on 3866/3866 test windows |
| **Thm M** | $\mu(K_p\cap p^3\mathbb Z_p)\ge c_pp^{-3}$ for every prime $11\le p\le97$ | **computer-assisted** |
| Cor M′ | all $p\ge p_0$ under the arithmetic hypothesis AC($p$) | reduction; see §9 for exactly what is proved |
| Thm E/F | pathwise two-window Chebyshev; $\min(1,16\varepsilon)$ series | proved; exact tests $p=3,5$ |
| Lemma D1/Thm D2 | deterministic $L^1$ two-window recursion | proved; exact tests |
| Prop Q | exact annealed band mass of two-block composites | proved; formula = direct computation, 6/6 primes |

## 1. Notation and standing facts

Throughout, $p$ is an odd prime, $v=v_p$, $\mu$ is Haar probability measure, and for a ball $B$, $\mu_B$ is normalised Haar measure on $B$.
- $\pi_c(y)=(y+1)\cdots(y+c)$, $V_n(y)=v(\pi_n(y))$, $M_n(y)=\max_{i\le n}v(y+i)$, $c_n(y)=2^{-n}p^{V_n(y)}$. Points $y$ that are negative integers are excluded (a null set).
- A *lazy signed* variable takes the values $0,\pm1$ with probabilities $\frac12,\frac14,\frac14$. It is the law of $f-f'$ for two independent fair bits.
- Paths, aliveness, targets, slopes, $P^0_n$, $Z^0_n$, windows $W=[n,N)$ and jumps $D$ are as in R3M §1. (F1) survival implies $x\in K_p$, and (F2) backward integrality, are used freely.
- **Composite window.** For times $n<N<N'$ put $L=N-n$, $L'=N'-N$ and $z=x+n$. Since $\pi_{n+c}(x)/\pi_n(x)=\pi_c(x+n)$, the composite window has elements $\pi_c(z)$, $0\le c<L+L'$, with $D=V_L(z)$ and $K=V_{L+L'}(z)$. Its fine-scale mass (R3M Prop C2) is
$$\varepsilon=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D,\qquad \mathrm{Coll}_k=P_\delta\big(T_\delta(z)\equiv0\bmod p^k\big),\quad T_\delta=\sum_{c<L+L'}\delta_c\pi_c(z),$$
with $\delta_c$ i.i.d. lazy signed. ($\mathrm{Coll}_k$ is the collision probability of two independent uniform subset sums: R3M Lemma C5, proof.) $\varepsilon$ is a function of $z$ and $(L,L')$ only. Since $p^D\mathrm{Coll}_D\ge1$ (Cauchy–Schwarz), $\varepsilon\le p^K\mathrm{Coll}_K-1$.
- **Signed survival masses.** For $t\ge1$, $y\in\mathbb Z_p$ and $\lambda\in\mathbb Z$:
$$\Lambda^{(\lambda)}_t(y):=p^{V_t(y)}\,P_\delta\Big(v(R_\delta(y))\ge V_t(y),\ v(R'_\delta(y))\ge\lambda\Big),\qquad R_\delta(y)=1+\sum_{1\le c<t}\delta_c\pi_c(y),$$
with $\delta_c$ i.i.d. lazy signed. For $\lambda\le0$ the slope condition is void, and $\Lambda^{(0)}_t=\Lambda_t$ of R3M Lemma C5.
- **Gates and blocks of a point.** For $y$ and $t$, the *gates* are the $g\in[1,t-1]$ with $p\mid y+g$, listed as $g_1<\dots<g_I$ (so $g_{i+1}=g_i+p$). The *depth* is $d_i=v(y+g_i)$ and the *unit* is $w_i=(y+g_i)p^{-d_i}$. The *levels* are $\ell_0=0$ and $\ell_i=d_1+\dots+d_i$. The *blocks* are $B_0=[0,g_1)$ and $B_i=[g_i,g_{i+1})$, with $g_{I+1}:=t$. For $c\in B_i$ we have $v(\pi_c(y))=\ell_i$. Block $i$ is *full* if $1\le i\le I-1$; then $B_i=\{g_i+r:0\le r<p\}$ and
$$\pi_{g_i+r}(y)=p^{\ell_i}U_i\prod_{s=1}^r(p^{d_i}w_i+s),\qquad U_i:=\pi_{g_i}(y)p^{-\ell_i}\in\mathbb Z_p^\times. \tag{1.1}$$
- $H_r=\sum_{s\le r}1/s$, read in $\mathbb Z_{(p)}$ for $r<p$.

## 2. Hensel reduction of the fine-scale mass

**Lemma H2 (multi-scale Hensel increment) [proved].** Let $F\in\mathbb Z_p[X]$, let $B=b+p^r\mathbb Z_p$ ($r\ge0$), and let $D<K$ be integers with $D\ge2r$. Then
$$p^K\mu_B\{v(F)\ge K\}-p^D\mu_B\{v(F)\ge D\}\ \le\ p^K\mu_B\{y\in B:\ v(F(y))\ge K,\ 2v(F'(y))\ge D\}.$$

*Proof.* Work with unnormalised Haar measure $\mu$; both sides scale by $\mu(B)$. Let $Y_k=\{y\in B:v(F(y))\ge k\}$ and $S=\{y\in Y_D:2v(F'(y))<D\}$.
1. *Hensel balls.* Let $y\in S$ and $\lambda=v(F'(y))<D/2$. Since $v(F(y))\ge D>2\lambda$, Hensel's lemma gives a unique root $\rho\in\mathbb Z_p$ with $v(\rho-y)\ge v(F(y))-\lambda>\lambda$. Put $U_\rho=\rho+p^{\lambda+1}\mathbb Z_p$. For $y'\in U_\rho$, $F'(y')\equiv F'(\rho)\pmod{p^{\lambda+1}}$ (Taylor, integral coefficients), so $v(F'(y'))=\lambda$. Moreover $F(y')=(y'-\rho)\big(F'(\rho)+(y'-\rho)G(y')\big)$ with $G$ integral, and $v((y'-\rho)G)\ge\lambda+1$. Hence
$$v(F(y'))=\lambda+v(y'-\rho)\qquad(y'\in U_\rho). \tag{2.1}$$
2. *$S$ is a disjoint union.* By step 1, every $y\in S$ lies in $U_\rho\cap B\cap Y_D$ for its root $\rho$, and every point of $U_\rho\cap B\cap Y_D$ is in $S$, with the same root. Two such balls are disjoint, since a root $\rho'\in U_\rho$ would satisfy $v(F(\rho'))=\lambda+v(\rho'-\rho)<\infty$. If $y\in U_\rho\cap B\cap Y_D$ then $v(y-\rho)\ge D-\lambda>D/2\ge r$, so $\rho\in B$.
3. *Constancy.* Let $k\in[D,K]$ and let $\rho\in B$ be a root with $\lambda=\lambda_\rho<D/2$. By (2.1), $Y_k\cap U_\rho=\rho+p^{k-\lambda}\mathbb Z_p$, because $k-\lambda>\lambda$. This ball lies in $B$, because $k-\lambda>D/2\ge r$. Hence $p^k\mu(Y_k\cap U_\rho)=p^\lambda$, which does not depend on $k$.
4. Write $\Sigma=\sum_\rho p^{\lambda_\rho}$. Steps 2–3 give $p^k\mu(Y_k)=\Sigma+p^k\mu(Y_k\setminus\bigcup U_\rho)$ for $k=D,K$, and $Y_K\setminus\bigcup U_\rho\subseteq Y_K\cap\{2v(F')\ge D\}$. Subtract, and drop $-p^D\mu(Y_D\setminus\bigcup U_\rho)\le0$. ∎

**Proposition H′ (reduction to high-slope signed mass) [proved].** Let $L,L'\ge1$, and let $B=z_0+p^r\mathbb Z_p$ be a ball on which $v(z+i)$ is constant for $1\le i\le L+L'$. Then $D,K,V_j,M:=M_{L+L'}$ and $c_j$ are constant on $B$. Assume
$$D\ge2r\qquad\text{and}\qquad\lceil D/2\rceil\le K-M.\tag{2.2}$$
Then, with $\lambda_j:=\lceil D/2\rceil-V_j$,
$$\mathbb E_{z\in B}[\varepsilon(z)]\ \le\ c_{L+L'}+\sum_{j=0}^{L+L'-1}\frac{c_j}2\,\mathbb E_{z\in B}\Big[\Lambda^{(\lambda_j)}_{L+L'-j}(z+j)\Big].$$

*Proof.* Since $D,K$ are constant on $B$,
$$\mathbb E_B\varepsilon=\sum_\delta P(\delta)\Big(p^K\mu_B\{v(T_\delta)\ge K\}-p^D\mu_B\{v(T_\delta)\ge D\}\Big),$$
and $T_\delta\in\mathbb Z[z]$. Lemma H2 bounds each bracket by $p^K\mu_B\{v(T_\delta)\ge K,\ v(T'_\delta)\ge\lceil D/2\rceil\}$, with $'=d/dz$. Now decompose by the first index $j$ with $\delta_j\ne0$.
- If $\delta=0$, the term is $P(\delta=0)p^K=2^{-(L+L')}p^K=c_{L+L'}$.
- Otherwise $\delta_j=\sigma=\pm1$, with probability $2^{-j}\cdot\frac14$ for each sign. Then $T_\delta(z)=\sigma\pi_j(z)R_{\delta'}(z+j)$ with $\delta'_c=\sigma\delta_{j+c}$, $1\le c<t:=L+L'-j$, which is again i.i.d. lazy signed. Write $y=z+j$, so that $V_{j+t}(z)=V_j(z)+V_t(y)$. Then $v(T_\delta)\ge K$ iff $v(R(y))\ge V_t(y)$. Also $T'_\delta=\sigma(\pi'_jR+\pi_jR')$, and $v(\pi'_j(z))\ge V_j-M_j$, so on that event $v(\pi'_jR)\ge K-M\ge\lceil D/2\rceil$ by (2.2). Hence $v(T'_\delta)\ge\lceil D/2\rceil$ iff $v(R'(y))\ge\lambda_j$.
- Both signs give the same probability, so the term for $j$ equals $2^{-j-1}p^{V_j}\,\mathbb E_B\big[p^{V_t(y)}P_{\delta'}(\cdots)\big]=\frac{c_j}2\mathbb E_B\Lambda^{(\lambda_j)}_t(z+j)$. ∎

*Remark.* Only signed paths whose slope is at least about $D/2$ minus their starting level contribute. This is R3M's Remark C6, now proved, with the threshold $\lceil D/2\rceil$, and with no martingale or visible-slope argument. The identity behind the decomposition was checked pointwise in exact arithmetic (§10).

## 3. Quenched anti-concentration of signed sums

In this section $y$, $t$ and the gate/block data are fixed (§1). Let $\delta_0,\dots,\delta_{t-1}$ be independent random variables with values in $\mathbb Z_p$. Put $T=\sum_{c<t}\delta_c\pi_c(y)$, $T'=\sum_{c<t}\delta_c\pi'_c(y)$, and $S_i=\sum_{c\in B_i}\delta_c\pi_c(y)p^{-\ell_i}\in\mathbb Z_p$. For an integer $k\ge1$ and a block with $\ell_i<k$, let $e_i=\min(\ell_{i+1},k)-\ell_i\ge1$, with $\ell_{I+1}:=+\infty$.

**Lemma P [proved].** $\displaystyle P\big(v(T)\ge k\big)\le\prod_{i:\ \ell_i<k}\ \max_{a\in\mathbb Z/p^{e_i}}P\big(S_i\equiv a\bmod p^{e_i}\big).$

*Proof.* $T=\sum_ip^{\ell_i}S_i$. Process the blocks in increasing order. Condition on the digits of blocks $<i$ and write $T_{<i}=\sum_{i'<i}p^{\ell_{i'}}S_{i'}$. Blocks $>i$ contribute multiples of $p^{\ell_{i+1}}$. So the event $v(T)\ge k$ forces $T_{<i}\equiv0\pmod{p^{\ell_i}}$ and $S_i\equiv-T_{<i}p^{-\ell_i}\pmod{p^{e_i}}$. The second condition concerns block $i$ alone, which is independent of the conditioning, so its conditional probability is at most $\max_aP(S_i\equiv a\bmod p^{e_i})$. The chain rule gives the product. ∎

For the derivative we need the structure (1.1) of full blocks. For a full block $i$ write $c=g_i+r$, $0\le r<p$, and
$$A_i=\sum_{r<p}\delta_{g_i+r}\,r!\ \in\mathbb Z_p,\qquad B_i=\sum_{r<p}\delta_{g_i+r}\,r!\,H_r\ \bmod p,\qquad \Phi_i=\big(A_i\bmod p,\ \ \lfloor A_i\rfloor_1-B_i\bmod p\big),$$
where $\lfloor a\rfloor_1$ is the $p$-adic digit of index 1 of $a$ (for an integer $a$ it equals $\lfloor a/p\rfloor\bmod p$).

**Lemma Q [proved].** Assume moreover that $\delta_1,\dots,\delta_{t-1}$ are i.i.d. lazy signed ($\delta_0$ arbitrary and independent of them). Let $1\le f<k$ with $f\le k-d_{\max}$, where $d_{\max}=\max_id_i$. Let
$$J=\{i:\ 1\le i\le I-1,\ d_{i+1}=1,\ \ell_i<f\}$$
(full blocks below level $f$ that end at a depth-1 gate). Then
$$P\big(v(T)\ge k,\ v(T')\ge f\big)\ \le\ \Big(\frac{q_2(p)}{p^2}\Big)^{|J|}\prod_{i:\ \ell_i<k,\ i\notin J}\max_aP\big(S_i\equiv a\bmod p^{e_i}\big),$$
where $q_2(p):=p^2\max_{\varphi\in(\mathbb Z/p)^2}P(\Phi=\varphi)$ for $\Phi$ built from $p$ i.i.d. lazy signed digits (§4).

*Proof.*
*(a) Reduction of $T'$.* We have $\pi'_c(y)=\pi_c(y)\sum_{j\le c}(y+j)^{-1}$. Split the sum into gates and non-gates: put $h_c=\sum_{1\le j\le c,\ j\notin\{g_i\}}(y+j)^{-1}\in\mathbb Z_p$. Then $\sum_{i:g_i\le c}(y+g_i)^{-1}=\sum_{i:g_i\le c}p^{-d_i}w_i^{-1}$. Summing over $c$ and exchanging the order (Abel summation),
$$T'=T'_0+\sum_{c\ge g_1}\delta_c\pi_c(y)h_c+\sum_{i=1}^{I}\frac{T-T_{<i}}{p^{d_i}w_i},\qquad T'_0:=\sum_{c\in B_0}\delta_c\pi'_c(y).$$
On $\{v(T)\ge k\}$ the terms $T/(p^{d_i}w_i)$ have valuation $\ge k-d_{\max}\ge f$. So, on that event, $v(T')\ge f$ iff $v(Y)\ge f$, where $Y:=T'_0+\sum_{c\ge g_1}\delta_c\pi_ch_c-\sum_iT_{<i}/(p^{d_i}w_i)$.
*(b) The events.* For each block $i$ with $\ell_i<k$ let $C^T_i$ be the event of Lemma P's proof ($S_i$ prescribed modulo $p^{e_i}$ given the lower blocks). For $i\in J$ let
$$Y_i:=T'_0+\sum_{c\in B_1\cup\dots\cup B_i}\delta_c\pi_ch_c-\sum_{i'=1}^{i+1}\frac{T_{<i'}}{p^{d_{i'}}w_{i'}},$$
a function of blocks $\le i$. On $\bigcap_{i'\le i}C^T_{i'}$ we have $v(T_{<i'})\ge\ell_{i'}$ for $i'\le i+1$, because $d_{i+1}=1$ and $e_i=1$. So $Y_i\in\mathbb Z_p$. Let $C^{T'}_i$ be the event that the digit of $Y_i$ at level $\ell_i$ vanishes. On $\{v(T)\ge k\}\cap\{v(T')\ge f\}$, $Y-Y_i$ consists of $h$-terms of blocks $>i$ (valuation $\ge\ell_{i+1}$) and of terms $T_{<i'}/(p^{d_{i'}}w_{i'})$ with $i'\ge i+2$. The valuation of the latter is $\ge\ell_{i'-1}\ge\ell_{i+1}$ if $\ell_{i'}\le k$, and $\ge k-d_{\max}\ge f>\ell_i$ otherwise, because $v(T_{<i'})=v(T-T_{\ge i'})\ge\min(k,\ell_{i'})$. Hence $Y\equiv Y_i\pmod{p^{\ell_i+1}}$, and $C^{T'}_i$ holds, since $\ell_i<f$. Therefore
$$\{v(T)\ge k,\ v(T')\ge f\}\subseteq\bigcap_{i:\ell_i<k}C^T_i\ \cap\ \bigcap_{i\in J}C^{T'}_i .$$
*(c) Block $i\in J$, given blocks $<i$.* By (1.1), modulo $p^2$, $\pi_c(y)p^{-\ell_i}\equiv U_i\,r!\,(1+\epsilon_ipw_iH_r)$, with $\epsilon_i=1$ if $d_i=1$ and $\epsilon_i=0$ if $d_i\ge2$. Hence $S_i\equiv U_i(A_i+\epsilon_ipw_iB_i)\pmod{p^2}$. Also, for $0\le r<p$, $h_c\equiv h_{g_i}+H_r\pmod p$. Write $u_0=U_i\bmod p$ and $a_0,a_1$ for the digits $0,1$ of $A_i$.
- $C^T_i$ fixes $S_i\bmod p=u_0a_0$, i.e. it fixes $a_0$.
- Given $a_0$ and the lower blocks, digit 1 of $S_i$ is $s_1=u_0(a_1+\epsilon_iw_iB_i)+\kappa$, with $\kappa$ known.
- The digit of $Y_i$ at level $\ell_i$ collects four kinds of term. Lower blocks (including $T'_0$ and the terms $i'\le i$) give a known value. Block $i$'s $h$-terms give $u_0(h_{g_i}a_0+B_i)$. The term $i'=i+1$ gives $-(\text{digit }\ell_i+1\text{ of }T_{<i+1})/w_{i+1}=-(s_1+\kappa')/w_{i+1}$, where $T_{<i+1}=T_{<i}+p^{\ell_i}S_i$ and $\kappa'$ is known.
- Since $y+g_{i+1}=p^{d_i}w_i+p$ and $d_{i+1}=1$: if $d_i=1$ then $w_{i+1}=w_i+1$, and if $d_i\ge2$ then $w_{i+1}\equiv1\pmod p$. In both cases $1-\epsilon_iw_i/w_{i+1}\equiv1/w_{i+1}\pmod p$.
- So the digit equals $\frac{u_0}{w_{i+1}}\big(B_i-a_1\big)+(\text{known})$.

Thus, given blocks $<i$, the event $C^T_i\cap C^{T'}_i$ says that $\Phi_i$ equals one prescribed value (or it is empty). Its probability is at most $q_2(p)/p^2$, because block $i$'s digits are i.i.d. lazy signed and independent of the lower blocks.
*(d)* The chain rule over blocks in increasing order gives the product. Blocks $i\notin J$ with $\ell_i<k$ use only $C^T_i$, as in Lemma P. ∎

*Remarks.* (i) The factor $q_2/p^2$ covers two digits, $T$ at level $\ell_i$ and $T'$ at level $\ell_i$, while a 1D block covers one. After normalising by $p^k$, each block in $J$ therefore contributes $q_2/p$: this is the slope gain. (ii) The statistic does not depend on the gate units $w_i$, nor on whether the block starts at a deep gate. (iii) Lemma Q was tested exactly against a full DP of $P(v(T)\ge k,v(T')\ge f)$ (§10). There, the observed ratio left side/(bound with the $J$-blocks given only their 1D factor) is $\approx p^{-|J|}\cdot0.1$. So the gain $p^{-1}$ per $J$-block is real, and the extra $\approx0.1$ is the unused derivative constraint of block 0.

## 4. The arithmetic constants of a gate block

### 4.1 Definitions
Let $\delta_0,\dots,\delta_{p-1}$ be i.i.d. lazy signed, $A=\sum_{r<p}\delta_rr!$ (integers $r!$), $B=\sum_r\delta_rr!H_r\bmod p$, and $F_r=\prod_{s=1}^r(s-p)$ (so $F_r=(-1)^r(p-1)!/(p-1-r)!$). Put
$$q_1(p)=p\max_aP(A\equiv a\bmod p),\qquad q_2(p)=p^2\max_{a,b}P\big(A\equiv a,\ \lfloor A/p\rfloor-B\equiv b\pmod p\big),$$
$$q_3(p)=p^3\max_aP\Big(\sum_r\delta_rF_r\equiv a\bmod p^3\Big).$$
Each is $\ge1$ (a maximum is at least the mean). The law of $A$ is symmetric and is the autocorrelation of the subset-sum law, so the maximum in $q_1$ is attained at $a=0$. Hence $q_1=p\,\mathrm{Coll}=1+\chi^2$, where $\chi^2$ is the mod-$p$ shell of one full block (note Prop 11.12).

### 4.2 Which block has which constant
Let block $i$ be full (1.1) and let $d=d_{i+1}$ be the depth of the gate that ends it. Its 1D factor in Lemmas P and Q, *normalised*, is $p^{e_i}\max_aP(S_i\equiv a\bmod p^{e_i})$ with $e_i\le d$. Multiplication by the unit $U_i$ does not change maxima.
- If $e_i=1$: the elements are $\equiv U_ir!\pmod p$, so the factor is $q_1$.
- If $d=2$ and the starting unit satisfies $w_i\equiv-1\pmod p$ (and $d_i=1$): modulo $p^2$ the elements are $U_ir!(1-pH_r)$, so $S_i/U_i\equiv A-pB$. The map $(A-pB)\bmod p^2\mapsto(A\bmod p,\lfloor A/p\rfloor-B\bmod p)$ is a bijection, so the factor is $\le q_2$ (it equals $q_2$ when $e_i=2$).
- If $d\ge3$, $d_i=1$ and $w_i\equiv-1\pmod{p^2}$: modulo $p^3$ the elements are $U_i\prod_{s\le r}(s-p)=U_iF_r$, so $p^{e_i}\max P(S_i\equiv a\bmod p^{e_i})\le p^{e_i-3}\cdot p^3\max P(\cdot\bmod p^3)\le p^{d-3}q_3$.

### 4.3 Values [computer-assisted]
Exact rationals were computed by a DP (`early_phase.py`, `qconst.py`). For $p\le13$ they were recomputed independently by brute force over all $3^p$ signed vectors (`qconst_brute.py`); the values agree exactly (§10). Rounded:

| $p$ | Wilson? | $q_1-1$ | $q_2-1$ | $q_3-1$ |
|---|---|---|---|---|
| 5 | yes | $0.0352$ | $0.953$ | $4.86$ |
| 7 | no | $0.0143$ | $0.113$ | $3.06$ |
| 11 | no | $1.44\cdot10^{-3}$ | $0.112$ | $0.801$ |
| 13 | yes | $2.20\cdot10^{-5}$ | $8.12\cdot10^{-3}$ | $0.192$ |
| 17 | no | $6.09\cdot10^{-7}$ | $2.90\cdot10^{-4}$ | $0.0226$ |
| 19 | no | $9.83\cdot10^{-8}$ | $4.63\cdot10^{-4}$ | $0.0107$ |
| 23 | no | $5.42\cdot10^{-9}$ | $2.26\cdot10^{-6}$ | $1.16\cdot10^{-3}$ |
| 29 | no | $7.32\cdot10^{-11}$ | $7.86\cdot10^{-8}$ | $7.91\cdot10^{-6}$ |
| 31 | no | $7.46\cdot10^{-11}$ | $1.23\cdot10^{-7}$ | $2.15\cdot10^{-5}$ |
| 37 | no | $8.93\cdot10^{-14}$ | $2.40\cdot10^{-10}$ | $5.04\cdot10^{-7}$ |
| 41 | no | $3.69\cdot10^{-20}$ | $6.99\cdot10^{-12}$ | $1.98\cdot10^{-8}$ |
| 43 | no | $8.36\cdot10^{-13}$ | $8.75\cdot10^{-13}$ | $1.71\cdot10^{-9}$ |
| 47 | no | $3.54\cdot10^{-21}$ | $1.24\cdot10^{-15}$ | $1.10\cdot10^{-10}$ |
| 53 | no | $6.07\cdot10^{-27}$ | $1.17\cdot10^{-16}$ | $2.29\cdot10^{-11}$ |
| 59 | no | $4.26\cdot10^{-19}$ | $1.98\cdot10^{-18}$ | $2.27\cdot10^{-14}$ |
| 61 | no | $2.81\cdot10^{-24}$ | $6.54\cdot10^{-19}$ | $1.39\cdot10^{-16}$ |
| 67 | no | $2.30\cdot10^{-28}$ | $9.14\cdot10^{-19}$ | $1.56\cdot10^{-16}$ |
| 71 | no | $1.15\cdot10^{-26}$ | $1.11\cdot10^{-22}$ | $6.50\cdot10^{-19}$ |
| 73 | no | $1.33\cdot10^{-32}$ | $2.87\cdot10^{-24}$ | $1.17\cdot10^{-16}$ |
| 79 | no | $3.23\cdot10^{-31}$ | $9.46\cdot10^{-27}$ | $3.54\cdot10^{-23}$ |
| 83 | no | $5.91\cdot10^{-36}$ | $1.22\cdot10^{-25}$ | $2.87\cdot10^{-24}$ |
| 89 | no | $1.96\cdot10^{-40}$ | $1.44\cdot10^{-30}$ | $8.29\cdot10^{-27}$ |
| 97 | no | $2.09\cdot10^{-43}$ | $4.07\cdot10^{-34}$ | $3.09\cdot10^{-29}$ |

(Values are rounded to three digits; the proofs use the exact rationals. The second DP in `check_assemble.py` gives the same values for $11\le p\le97$ (`check_assemble.log`), and for $p\le13$ they also agree with brute force over all $3^p$ vectors.) The decay is fast but irregular: for example $q_1(43)-1=8.4\cdot10^{-13}$, while $q_1(41)-1=3.7\cdot10^{-20}$.

The decay of $q_1-1$ and $q_2-1$ is the arithmetic heart of "large $p$": a full block of $p$ factorials behaves, modulo $p$ (and modulo $p\times p$ for the pair statistic), almost exactly like $p$ independent uniform residues. We have no proof that this continues for all $p$ (§9).

## 5. The atom $A=p^3\mathbb Z_p$ and an explicit slope-0 path

Write $x\in A$ as $x=p\xi$ with $\xi\in p^2\mathbb Z_p$, and write $\xi=p^2\xi'$.

**Lemma 5.1 (environment on $A$) [proved].** For $x\in A$ and $i\ge1$: $v(x+i)=0$ if $p\nmid i$. For $i=jp$, the gate at block $j$, $v(x+jp)=1+v(\xi+j)$, which is
- $1$ if $p\nmid j$;
- $2$ if $p\,\|\,j$;
- $3+v(\xi'+j/p^2)\ge3$ if $p^2\mid j$.

The unit of the gate at block $j-1$ is $w=\xi+j-1$. Hence if $p\mid j$ then $w\equiv-1\pmod p$, and if $p^2\mid j$ then $w\equiv-1\pmod{p^2}$. In particular, every gate before block $p^2$ has a deterministic depth on $A$.

*Proof.* Immediate from $v(\xi)\ge2$. ∎

**Proposition W (slope-0 path at $3p$) [proved; the Wilson case $p=13$ by an explicit block].** Let $p\ge7$, $x\in A$. Let $w_p=((p-1)!+1)/p$ be the Wilson quotient. Let $e$ be the path of length $3p$ with
- first block $e_0=e_{p-1}=1$, all other $e_j=0$ for $j<p$;
- second block $\{e_{p+u}\}_{u<p}$ any choice with $\sum_ue_{p+u}u!\equiv w_p/(\xi+1)\pmod p$;
- third block $\{e_{2p+u}\}_{u<p}$ any choice making $S_e(x)\equiv0\pmod{p^3}$.

Such choices exist, $e$ is alive at $3p$ ($V_{3p}(x)=3$), and
$$S'_e(x)\equiv-\,w_p/(\xi+1)\pmod p .$$
So $e$ has slope 0 iff $p^2\nmid(p-1)!+1$, i.e. iff $p$ is not a Wilson prime. More generally, for a first block $e_{<p}$ with $e_0=1$ and $\sum_{j<p}e_jj!=pk_e$, the completed path is alive at $3p$ and has slope $0$ iff $\lambda_e:=\sum_je_jj!H_j\not\equiv k_e\pmod p$. For the Wilson prime $p=13$ the first block $\{j:e_j=1\}=\{0,1,2,3,4,8,9\}$ satisfies this: $\sum_jj!=403234=13\cdot31018$, so $k_e\equiv31018\equiv0$, while $\lambda_e\equiv12\pmod{13}$.

*Proof.* On $A$, $\xi\equiv0\pmod{p^2}$, so the gates at $p,2p,3p$ have depth 1 and $V_{3p}=3$.
- *First block.* $\pi_j(x)=\prod_{s\le j}(p\xi+s)\equiv j!(1+p\xi H_j)\pmod{p^2}$ for $j<p$. With $e=\{0,p-1\}$ the sum is $1+(p-1)!(1+p\xi H_{p-1})\equiv pw_p\pmod{p^2}$, because $H_{p-1}\equiv0\pmod p$ for $p\ge3$.
- *Second block.* For $u<p$, $\pi_{p+u}(x)=\pi_{p-1}(x)\,(x+p)\prod_{s\le u}(x+p+s)\equiv(p-1)!\,p(\xi+1)\,u!\equiv-p(\xi+1)u!\pmod{p^2}$. So $S_e\equiv p\big(w_p-(\xi+1)\sum_ue_{p+u}u!\big)\pmod{p^2}$, and the prescribed residue makes this $\equiv0$. It can be achieved because the $p$ nonzero residues $u!$ ($u<p$) have subset sums covering $\mathbb Z/p$ (Cauchy–Davenport: $|\{0,a_1\}+\dots+\{0,a_p\}|\ge\min(p,p+1)$).
- *Third block.* The elements have valuation exactly 2 and unit parts $\equiv(\xi+1)(\xi+2)u!\not\equiv0\pmod p$. By Cauchy–Davenport again the digit at $p^2$ can be cancelled.
- *Slope.* $\pi'_j(x)\equiv j!H_j\pmod p$ for $j<p$; the chosen terms give $0\cdot H_0$ and $(p-1)!H_{p-1}\equiv0$. For $p\le j<2p$, $\pi'_j\equiv\pi_j/(x+p)\equiv(p-1)!\,(j-p)!\pmod p$, the other summands of $\pi'_j=\pi_j\sum1/(x+i)$ being divisible by $p$. For $2p\le j<3p$, $v(\pi'_j)\ge V_j-M_j=1$. Hence $S'_e(x)\equiv(p-1)!\sum_ue_{p+u}u!\equiv-w_p/(\xi+1)\pmod p$.
- *General first block.* The same computation gives $S_e\equiv p(k_e+\xi\lambda_e)-p(\xi+1)t'$ and $S'_e\equiv\lambda_e-t'$ with $t'=\sum_ue_{p+u}u!$. Aliveness forces $t'\equiv(k_e+\xi\lambda_e)/(\xi+1)$, so $S'_e\equiv(\lambda_e-k_e)/(\xi+1)$. ∎

The construction was checked by direct exact evaluation of $S_e,S'_e$ at random $x\in A$ for all primes $7\le p\le97$ (§10).

**Admissibility.** For $x\in A$ the atom of $\mathcal G_0$ at $n_0=3p$ is $x+p^{V_{3p}(x)}\mathbb Z_p=x+p^3\mathbb Z_p=A$. The first window $W_0=[3p,4p)$ has $D_0=v(x+4p)=1\le m_0-M_{4p}=3-1$ and $M_{4p}=1<3$. By Proposition W, $Z^0_{3p}\ge1$ on $A$. So $A$ is an admissible atom in the sense of R3M Theorem C3. Its elements are units $\equiv r!\pmod p$, so $1+\chi^2_{W_0}=p\,\mathrm{Coll}_1=q_1(p)$.

## 6. Phase 1: the deterministic phase on $A$ (up to time $p^3$)

Window times are $n_k=b_kp$ with integers $b_0=3<b_1=4<b_2<\cdots$, so $n_0=3p\ge2p$. For $j<p^2$ put $d_j:=1+v_p(j)$, $V(b):=\sum_{j\le b}d_j$ and $\mathrm{Mx}(b):=\max_{j\le b}d_j$.

**Proposition P1 [proved].** Suppose $b_{k_0+1}\le p^2-1$ and, for $1\le k\le k_0$,
$$V(b_{k+1})-V(b_{k-1})\le V(b_{k-1})-\mathrm{Mx}(b_{k+1})\quad\text{and}\quad \mathrm{Mx}(b_{k+1})<V(b_{k-1})\tag{6.1}$$
(finitely many integer inequalities). Then for every $x\in A$ and $1\le k\le k_0$:
- (i) the linear-regime condition $\mathrm{lin}_k$ of R3M Theorem C3 holds at $x$;
- (ii) $\varepsilon_k(x)\le\bar\varepsilon_k:=q_1^{\,n_1(k)}q_2^{\,n_2(k)}-1$, where $n_\delta(k)=\#\{j\in(b_{k-1},b_{k+1}]:d_j=\delta\}$.

*Proof.* (i) By Lemma 5.1, $V_{bp}(x)=V(b)$ and $M_{bp}(x)=\mathrm{Mx}(b)$ for $b<p^2$. Then (6.1) is exactly $D_{k-1}+D_k\le m_{k-1}-M_{n_{k+1}}$, $M_{n_{k+1}}<m_{k-1}$.
(ii) Let $z=x+n_{k-1}\equiv0\pmod p$. The composite window has elements $\pi_c(z)$, $c<(b_{k+1}-b_{k-1})p$. Its gates are at $ip$, $1\le i\le b_{k+1}-b_{k-1}$; the $i$-th is the gate of $x$ at block $b_{k-1}+i$. Every block has the form (1.1), block 0 included, with $U=1$ and starting point $z=p^{d}w$. Its end-gate depth is $1$ or $2$, and when it is $2$ the starting gate has depth 1 and unit $\equiv-1\pmod p$ (Lemma 5.1). Apply Lemma P with all $\delta_c$ lazy signed and $k=K$, so that $\sum e_i=K$. By §4.2, $p^K\mathrm{Coll}_K=p^KP(v(T)\ge K)\le q_1^{n_1}q_2^{n_2}$. Finally $\varepsilon\le p^K\mathrm{Coll}_K-1$ (§1). ∎

A greedy choice (largest $b_{k+1}$ satisfying (6.1)) gives, for example,
- $b=(3,4,5,7,9,12,15,21,28,39,54,77,106,151,168)$ at $p=13$;
- $b=(3,4,5,7,9,13,16,23,29,44,55,85,108,169,214,288)$ at $p=17$.

The products $\prod_k(1+\bar\varepsilon_k)$ are $e^{0.19}$ at $p=13$, $e^{0.0084}$ at $p=17$ and $e^{10^{-4}}$ at $p=23$ (§7). This is where large $p$ pays: the phase up to time $p^3$, which round 3 and track M4B single out as an obstacle, costs almost nothing.

## 7. Phase 2, and Theorem M

### 7.1 Tail lemmas
For a phase-2 window $\ell$ (blocks $b_{\ell-1}<b_\ell<b_{\ell+1}$) and an integer $s\ge3$ put $N_W=b_\ell-b_{\ell-1}$, $N=b_{\ell+1}-b_{\ell-1}$, and $\Xi(U):=\sum_{a=1}^{s-3}\lceil U/p^a\rceil$. Let
$$G_\ell=\{x\in A:\ v(x+jp)\le s\ \text{for all}\ j\le b_{\ell+1}\},\qquad G'_\ell=\{x\in A:\ v(x+jp)\le s\ \text{for}\ b_{\ell-1}<j\le b_{\ell+1}\}\supseteq G_\ell .$$

**Lemma L (linear regime and deep gates on $A$) [proved].**
- (a) $\mu_A(G_\ell^c)\le\lfloor b_{\ell+1}/p^2\rfloor\,p^{-(s-2)}$.
- (b) If (T1) $N+\lceil N/p\rceil+U_N+\Xi(U_N)+s\le b_{\ell-1}+\lfloor b_{\ell-1}/p\rfloor$ with $U_N=\lceil N/p^2\rceil$, then $\mathrm{lin}_\ell$ holds on $G_\ell$.

*Proof.* (a) By Lemma 5.1, $v(x+jp)>s$ forces $p^2\mid j$ and $v(\xi'+j/p^2)\ge s-2$. Under $\mu_A$, $\xi'$ is Haar distributed, so each such $j$ has probability $p^{-(s-2)}$.
(b) We have $m_{\ell-1}=V_{n_{\ell-1}}\ge b_{\ell-1}+\lfloor b_{\ell-1}/p\rfloor$, because every $p$-multiple $j$ has depth $\ge2$. Also
$$K=\sum_{b_{\ell-1}<j\le b_{\ell+1}}v(x+jp)=N+\#\{p\mid j\}+\#\{p^2\mid j\}+\sum_{p^2\mid j}v(\xi'+j/p^2).$$
On $G_\ell$ each $v(\xi'+u)\le s-3$, and among $U$ consecutive $u$ at most $\lceil U/p^a\rceil$ have $v\ge a$; so $K\le N+\lceil N/p\rceil+U_N+\Xi(U_N)$. Finally $M_{n_{\ell+1}}\le s$. ∎

**Lemma T (phase-2 window bound) [proved].** Assume (T2) $N_W\ge2s+2$. Define, for $0\le i\le N$ and $j=b_{\ell-1}+i$:
- $d^0_j=1+v_p(j)$ if $p^2\nmid j$, and $d^0_j=3$ if $p^2\mid j$;
- $V^0(i)=\sum_{0<i'\le i}d^0_{b_{\ell-1}+i'}$, $U(i)=\#\{0<i'\le i:p^2\mid b_{\ell-1}+i'\}$, and $V^+(i)=V^0(i)+\Xi(U(i))$;
- $D^-=V^0(N_W)$ and $I=\max\{i\le N-1:V^+(i)<\lceil D^-/2\rceil\}$;
- for $0\le j_0<N$, $\nu(j_0)=\#\{i\in(j_0,I]:\ p\nmid b_{\ell-1}+i+1\}$.

Let $n_1,n_2,U$ count the $j\in(b_{\ell-1},b_{\ell+1}]$ with $p\nmid j$, with $p\,\|\,j$, and with $p^2\mid j$. Then
$$\mathbb E_A\big[\varepsilon_\ell\mathbf 1_{G'_\ell}\big]\le\mathfrak B_\ell:=2^{-Np}p^{V^+(N)}+q_1^{n_1}q_2^{n_2}q_3^{U}p^{\Xi(U)}\sum_{j_0=0}^{N-1}2^{-j_0p}\,p^{V^+(j_0+1)}\Big(\frac{q_2}p\Big)^{\nu(j_0)}.$$

*Proof.*
1. *Environment balls.* Let $z=x+n_{\ell-1}$, so $z$ is Haar distributed on $n_{\ell-1}+A$. Let $M$ be the largest depth among the composite's gates; $M\ge2$, since the window contains a multiple of $p$ ($N\ge p$ in phase 2). The balls $\mathcal B=z+p^{M+1}\mathbb Z_p$ partition $n_{\ell-1}+A$ up to a null set, lie inside it, and on each of them all $v(z+i)$, $i\le Np$, are constant. $G'_\ell$ is a union of such balls. Hence $\mathbb E_A[\varepsilon\mathbf 1_{G'}]\le\sup_{\mathcal B\subseteq G'}\mathbb E_{\mathcal B}[\varepsilon]$.
2. *Proposition H′ applies on each $\mathcal B\subseteq G'$.* Here $r=M+1\le s+1$ and $D\ge N_W\ge2s+2\ge2r$. Also $\lceil D/2\rceil\le D/2+1\le D-s\le K-M$.
3. *Lemma Q for each $j$.* Let $y=z+j$, $j_0=\lfloor j/p\rfloor$, $t=Np-j$, $f=\lambda_j=\lceil D/2\rceil-V_{j_0p}$ and $k=K-V_{j_0p}=V_t(y)$. Then $f\le k-d_{\max}$ by step 2 and $d_{\max}\le s$. If $f\le0$, use Lemma P instead (Lemma Q with $J=\emptyset$).
   - The blocks of $y$ are: block 0, the partial block $[j,(j_0+1)p)$, with normalised factor $\le p^{e_0}\le p^{d_{j_0+1}}$; and, for $i\ge1$, the composite blocks $i'=j_0+i$.
   - Composite block $i'$ ($i'>j_0$) has relative level $V_{i'p}-V_{j_0p}$. It lies in $J$ iff $V_{i'p}<\lceil D/2\rceil$ and its end gate has depth 1. Since $V_{i'p}\le V^+(i')$ and $D\ge D^-$, every $i'\le I$ with $p\nmid b_{\ell-1}+i'+1$ is in $J$ (note $I\le N_W-1\le N-2$, so the end gate is $<t$). So $|J|\ge\nu(j_0)$.
   - The other blocks have normalised factors $q_1$ (depth-1 end), $q_2$ (depth 2) or $p^{d-3}q_3$ (depth $d\ge3$), by Lemma 5.1 and §4.2. Their product is at most $q_1^{n_1}q_2^{n_2}q_3^{U}p^{\Xi(U)}$, using $\sum_{p^2\mid j}(d_j-3)\le\Xi(U)$ on $G'$. All constants are $\ge1$, so counting a block twice only weakens the bound.
   - Hence $\Lambda^{(\lambda_j)}_t(y)\le p^{d_{j_0+1}}\,q_1^{n_1}q_2^{n_2}q_3^Up^{\Xi(U)}(q_2/p)^{\nu(j_0)}$.
4. *Sum over $j$.* Here $c_j=2^{-j}p^{V_{j_0p}}$, and $\sum_{j:\lfloor j/p\rfloor=j_0}2^{-j-1}\le2^{-j_0p}$. Also $p^{V_{j_0p}}p^{d_{j_0+1}}=p^{V_{(j_0+1)p}}\le p^{V^+(j_0+1)}$, and $c_{L+L'}=2^{-Np}p^{K}\le2^{-Np}p^{V^+(N)}$ on $G'$. ∎

**Lemma T′ (closed form) [proved].** Under (T2), with $\alpha=1+\frac1p+\frac1{p^2}+\frac1{p^2(p-1)}$, $\rho=q_2/p<1$, $r_1=2^{-p}p^{\alpha}\rho^{-(1-1/p)}<1$ and $I'=\max\big(0,\lceil(\lceil N_W/2\rceil-s)/\alpha\rceil-1\big)$,
$$\mathfrak B_\ell\le2^{-Np}p^{\alpha N+s}+\frac{1}{1-r_1}\,q_1^{N}q_2^{\lceil N/p\rceil}q_3^{\lceil N/p^2\rceil}p^{\Xi(\lceil N/p^2\rceil)}\,p^{\alpha+s}\rho^{I'(1-1/p)-1}.$$

*Proof.*
- $V^0(i)\le i+\lceil i/p\rceil+\lceil i/p^2\rceil$ and $\Xi(U(i))\le U(i)/(p-1)+s-3$ with $U(i)\le i/p^2+1$; hence $V^+(i)\le\alpha i+s$. Consequently $I\ge I'$.
- $\nu(j_0)\ge(I-j_0)-\lceil(I-j_0)/p\rceil\ge(I-j_0)(1-1/p)-1$. Since $\rho<1$, $\rho^{\nu(j_0)}\le\rho^{\max(0,(I-j_0)(1-1/p)-1)}$.
- For $j_0\le I$ the $j_0$-term is $\le p^{\alpha+s}\rho^{I(1-1/p)-1}r_1^{j_0}$. For $j_0>I$ it is $\le p^{\alpha+s}(2^{-p}p^\alpha)^{j_0}=p^{\alpha+s}r_1^{j_0}\rho^{(1-1/p)j_0}\le p^{\alpha+s}r_1^{j_0}\rho^{I(1-1/p)-1}$.
- Sum the geometric series and use $I\ge I'$. Bound the counts by $n_1\le N$, $n_2\le\lceil N/p\rceil$, $U\le\lceil N/p^2\rceil$. ∎

### 7.2 Theorem M

**Theorem M [computer-assisted].** For every prime $p$ in the table below, $\mu(K_p\cap p^3\mathbb Z_p)\ge c_p\,p^{-3}$ with the stated $c_p>0$. In particular $\mu(K_p)>0$.

*Proof.* Apply R3M Theorem C3 (note Theorem 11.14) with $j=0$, the admissible atom $A$ (§5), and deterministic times $n_k=b_kp$. The schedule is:
- *Phase 1* ($k\le k_0$): the greedy schedule of §6.
- *Phase 2* ($k>k_0$): $s_k$ is the least integer $s\ge3$ with $\lfloor2b_{k-1}/p^2\rfloor p^{-(s-2)}\le\eta2^{-(k-k_0)}$. Then $b_{k+1}=\min\big(\max\{b\le2b_{k-1}:(T1)\},\ b_k+\lceil\gamma(b_k-b_{k-1})\rceil\big)$, with $\eta=0.05$ and $\gamma=1.6$.
- *Far tail* ($b_{k-1}>3000$): the same $s_k$, and $b_{k+1}=\lfloor\frac54b_k\rfloor$. For $p\ge59$ phase 1 ends near or above $b=3000$, so phase 2 has at most one window before the far-tail rule takes over.

The thresholds are $\bar\varepsilon_k=q_1^{n_1}q_2^{n_2}-1$ in phase 1 and $\bar\varepsilon_k=\sqrt{\mathfrak B'_k}$ in phase 2, where $\mathfrak B'_k$ is $\mathfrak B_k$ (Lemma T) for $N\le6000$ and the right side of Lemma T′ otherwise. For every window the program checks (T1) and (T2) exactly (integer arithmetic).
- In phase 1, $\mathrm{lin}_k$ and $\varepsilon_k\le\bar\varepsilon_k$ hold on all of $A$ (Prop. P1), so they never stop the process.
- In phase 2, $\mathrm{lin}_k$ holds on $G_k$ (Lemma L(b)). Hence
$$\mu_A(\tau<\infty)\le\sum_{k>k_0}\Big[\mu_A(G_k^c)+\mu_A\big(G'_k\cap\{\varepsilon_k>\bar\varepsilon_k\}\big)\Big]\le\sum_{k>k_0}\Big[\lfloor b_{k+1}/p^2\rfloor p^{-(s_k-2)}+\sqrt{\mathfrak B'_k}\Big]=:\delta_A,$$
  by Lemma L(a), Markov's inequality and Lemma T/T′.
- $\Pi_A=q_1\prod_k(1+\bar\varepsilon_k)$, because $1+\chi^2_{W_0}=q_1$.

`assemble.py` evaluates every term explicitly while $b_{k-1}\le10^{60}$, with 60-digit arithmetic and outward rounding. Let $\ell_*$ be the first window with $b_{\ell_*-1}>10^{60}$; the logs show $\ell_*-k_0\le600$ for every listed $p$. For $k\ge\ell_*$:
- *Deep gates.* By the $s$-rule and $b_{k+1}\le2b_{k-1}$, $\mu_A(G_k^c)\le\lfloor2b_{k-1}/p^2\rfloor p^{-(s_k-2)}\le\eta2^{-(k-k_0)}$. So $\sum_{k\ge\ell_*}\mu_A(G_k^c)\le\eta2^{-(\ell_*-k_0)+1}\approx10^{-178}$. This amount is added to $\delta_A$ explicitly.
- *Schedule.* Write $b=b_{k-1}$. The rule $b_{k+1}=\lfloor\frac54b_k\rfloor$ gives $N_W\ge b/4-1$ and $N\le\frac9{16}b+1$. The $s$-rule gives $s_k\le4+\log_p\frac{2b}{p^2\eta}+(k-k_0)\log_p2$, and $k-k_0\le600+\log_{1.24}(b/10^{60})+1$. For $p\ge11$ and $b\ge10^{60}$ this yields $s_k\le3+10\ln b$. Hence (T1), (T2) and $N\ge p$ hold.
- *Fine scale.* With these values, the logarithm of the Lemma T′ bound is $\le-\kappa_pb+O(\ln b)$. The constant $\kappa_p$ is printed by the program; it is $\ge0.22$ for every listed $p$. At $b=10^{60}$ the logarithm is $\le-2.2\cdot10^{59}$. Since $b_{k-1}$ grows geometrically, $\sum_{k\ge\ell_*}\sqrt{\mathfrak B'_k}<10^{-1000}$ and $\sum_{k\ge\ell_*}\log(1+\bar\varepsilon_k)<10^{-1000}$. Both are added, to $\delta_A$ and to $\log\Pi_A$.

So $\Pi_A\delta_A<1$, and C3 gives $\mu(K_p\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A=:c_p$. ∎

### 7.3 The numbers

Every row comes from `assemble.py p 0.05 3000 1.6` (log `assemble.log`, runs after the line "re-run after the remainder fix") and was reproduced by `check_assemble.py p 3000` (log `check_assemble.log`).
- Upper bounds are rounded up and lower bounds down. $c_p$ is the C3 bound $(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$ for $\mu(K_p\cap A)/\mu(A)$, and $\mu(K_p)\ge c_pp^{-3}$.
- $\log\Pi_A$ is the cost of phase 1 plus the explicit phase-2 windows (e.g. $0.192+0.007$ at $p=13$). The far-tail factors add less than $10^{-130}$.
- $\kappa_p$ is the decay rate per unit $b$ of the Lemma T′ bound beyond $10^{60}$ (§7.2).
- $\ell_*-k_0$ counts the windows after phase 1 that are evaluated explicitly.

| $p$ | $\log\Pi_A\le$ | $\delta_A\le$ | $c_p\ge$ | $\mu(K_p)\ge$ | $\kappa_p\ge$ | $\ell_*-k_0$ | independent check |
|---|---|---|---|---|---|---|---|
| 11 | $2.4$ | $0.0875$ | $1.254\cdot10^{-4}$ | $9.42\cdot10^{-8}$ | $0.226$ | 595 | agrees |
| 13 | $0.20$ | $0.0220$ | $0.572$ | $2.60\cdot10^{-4}$ | $0.270$ | 595 | agrees |
| 17 | $8.4\cdot10^{-3}$ | $9.39\cdot10^{-3}$ | $0.808$ | $1.64\cdot10^{-4}$ | $0.313$ | 592 | agrees |
| 19 | $0.017$ | $9.42\cdot10^{-3}$ | $0.800$ | $1.16\cdot10^{-4}$ | $0.329$ | 593 | agrees |
| 23 | $1.1\cdot10^{-4}$ | $8.59\cdot10^{-3}$ | $0.823$ | $6.76\cdot10^{-5}$ | $0.358$ | 591 | agrees |
| 29 | $4.2\cdot10^{-6}$ | $5.68\cdot10^{-3}$ | $0.855$ | $3.50\cdot10^{-5}$ | $0.392$ | 589 | agrees |
| 31 | $7.6\cdot10^{-6}$ | $4.53\cdot10^{-3}$ | $0.869$ | $2.91\cdot10^{-5}$ | $0.401$ | 592 | agrees |
| 37 | $1.6\cdot10^{-8}$ | $5.48\cdot10^{-3}$ | $0.857$ | $1.69\cdot10^{-5}$ | $0.427$ | 587 | agrees |
| 41 | $5.3\cdot10^{-10}$ | $0.0283$ | $0.691$ | $1.00\cdot10^{-5}$ | $0.441$ | 587 | agrees |
| 43 | $2.8\cdot10^{-9}$ | $0.0269$ | $0.699$ | $8.79\cdot10^{-6}$ | $0.448$ | 586 | agrees |
| 47 | $1.1\cdot10^{-13}$ | $0.0247$ | $0.710$ | $6.83\cdot10^{-6}$ | $0.460$ | 587 | agrees |
| 53 | $1.1\cdot10^{-14}$ | $0.0223$ | $0.723$ | $4.85\cdot10^{-6}$ | $0.477$ | 585 | agrees |
| 59 | $3.0\cdot10^{-15}$ | $0.0191$ | $0.742$ | $3.61\cdot10^{-6}$ | $0.492$ | 585 | agrees |
| 61 | $7.1\cdot10^{-17}$ | $0.0187$ | $0.745$ | $3.28\cdot10^{-6}$ | $0.497$ | 585 | agrees |
| 67 | $1.2\cdot10^{-16}$ | $0.0166$ | $0.759$ | $2.52\cdot10^{-6}$ | $0.510$ | 584 | agrees |
| 71 | $1.5\cdot10^{-20}$ | $0.0156$ | $0.766$ | $2.14\cdot10^{-6}$ | $0.517$ | 583 | agrees |
| 73 | $3.7\cdot10^{-22}$ | $0.0157$ | $0.765$ | $1.96\cdot10^{-6}$ | $0.521$ | 583 | agrees |
| 79 | $1.5\cdot10^{-24}$ | $0.0144$ | $0.775$ | $1.57\cdot10^{-6}$ | $0.532$ | 582 | agrees |
| 83 | $1.9\cdot10^{-23}$ | $0.0255$ | $0.706$ | $1.23\cdot10^{-6}$ | $0.539$ | 582 | agrees |
| 89 | $2.3\cdot10^{-28}$ | $0.0237$ | $0.716$ | $1.01\cdot10^{-6}$ | $0.548$ | 581 | agrees |
| 97 | $7.3\cdot10^{-32}$ | $0.0217$ | $0.727$ | $7.96\cdot10^{-7}$ | $0.560$ | 581 | agrees |

*Reading the table.*
- At $p=11$ the deterministic phase is expensive: $\Pi_A\approx10.6$. The main cost is $q_2(11)-1=0.11$, paid about $2p$ times at the depth-2 gates; $q_1(11)-1=1.4\cdot10^{-3}$, paid about $2p^2$ times, adds less. $\Pi_A\delta_A=0.93$ is still $<1$, so $c_{11}$ is positive but small.
- From $p=13$ on, $\Pi_A$ is close to 1, and $c_p$ is limited only by the deep-gate probabilities in $\delta_A$.
- The jumps at $p=41$ and $p=83$ are a threshold effect of the $s$-rule. Near $b=p^2$ there is one $p^2$-multiple gate, and the cap $s=3$ (cost $1/p$) is accepted as soon as $1/p\le\eta2^{-(k-k_0)}$. For $p\ge41$ this happens in the first window after phase 1 ($1/p\le0.025$), and for $p\ge83$ also in the second ($1/p\le0.0125$). Each such window adds $\approx1/p$ to $\delta_A$; see §9.1.

## 8. Adversarial re-check of the chain (done twice)

Theorem M is the only result here labelled as proving $\mu(K_p)>0$, so we re-checked every link twice. The second pass was done after writing the code, by re-deriving each inequality from the report text alone. The dependencies are:

| link | content | where proved | tested |
|---|---|---|---|
| C3 | conditional positive measure (R3M; note Thm 11.14) | R3M §5, checked in round 3 | round 3 |
| Prop B, Cor A′ | base of C3 ($\mathbb E M_1=M_0$, $\mathbb EM_1^2\le(1+\chi^2)M_0^2$) | R3M §§2–3 | round 3 |
| Prop W | $Z^0_{3p}\ge1$ on $A$ | §5 | exact, all primes $7\le p\le97$ |
| Lemma 5.1 | environment on $A$ | §5 | trivial |
| Lemma P | quenched 1D bound | §3 | exact (inside test_Q) |
| §4.2 | block-constant identification | §4 | q-values two programs |
| Prop P1 | phase 1 pointwise | §6 | integer checks in code |
| Lemma L | lin on $G_\ell$; $\mu_A(G^c)$ | §7.1 | — |
| Lemma H2 | Hensel increment | §2 | exact, 0 failures in 6152 trials |
| Prop H′ | reduction to $\Lambda^{(\lambda)}$ | §2 | identity exact, 0 fails |
| Lemma Q | value/derivative block bound | §3 | exact DP |
| Lemma T, T′ | bookkeeping | §7.1 | T′ ≥ T on 3866 windows (`test_Tprime.py`); Lemma T re-implemented independently (`check_assemble.py`) |

*Points checked specifically.*
1. **Sign and unit of $w_{i+1}$ in Lemma Q.** The coefficient of $B_i$ is $1-\epsilon_iw_i/w_{i+1}$. It equals $1/w_{i+1}$ in both cases ($d_i=1$: $w_{i+1}=w_i+1$; $d_i\ge2$: $w_{i+1}\equiv1$). If it vanished, the 2D gain would be lost; it never does.
2. **Measurability of the events $C^{T'}_i$.** They are defined through $Y_i$, which depends on blocks $\le i$ only. The inclusion $\{v(T)\ge k,v(T')\ge f\}\subseteq C^{T'}_i$ uses the alive condition, and the term-by-term valuations hold on that event (proof of Lemma Q (b)).
3. **Hypothesis $f\le k-d_{\max}$.** It is needed to replace $T'$ by $Y$. In Lemma T, $d_{\max}\le s$ on $G'$, and $f\le\lceil D/2\rceil\le K-M$ holds by (T2).
4. **Environment balls inside $n+A$.** This needs radius exponent $\ge3$, i.e. a gate of depth $\ge2$ in the composite. It is guaranteed by $N\ge p$, which the code asserts. Without it, $G'$ would not be a union of whole balls.
5. **Lemma H2 needs $D\ge2r$.** In Lemma T, $r=M+1\le s+1$ and $D\ge N_W\ge2s+2$.
6. **Depth-2 blocks.** $q_2$ is used only for blocks that end at a depth-2 gate and start at a depth-1 gate with unit $\equiv-1\pmod p$; on $A$ this is always the case (Lemma 5.1). The same holds for $q_3$ with unit $\equiv-1\pmod{p^2}$.
7. **Phase 1 bounds hold for every $x\in A$** (not just on average), so phase 1 contributes nothing to $\delta_A$, only to $\Pi_A$.
8. **The first-nonzero-index decomposition in Prop H′** uses that both signs have the same law. It needs $\lceil D/2\rceil\le K-M$ to discard $\pi'_jR$. Both points were tested exactly (pointwise identity).
9. **Outward rounding.** $q_1,q_2,q_3$ are exact rationals, rounded up by a relative $10^{-40}$. Each logarithm used as an upper bound is multiplied by $1+10^{-40}$; mpmath runs at 60 digits. The margins in Theorem M are many orders larger.
10. **The far tail.** The closed form needs (T1), (T2) and $N\ge p$; the code asserts all three up to $b=10^{60}$, and beyond that they follow from the schedule (§7.2). The printed slope $-\kappa_p$ is negative for every listed $p$ (§7.3).
11. **An error found in the second pass, and fixed.** The first version of `assemble.py` added only $10^{-1000}$ for all windows with $b_{k-1}>10^{60}$. That covers the fine-scale terms, but not the deep-gate terms $\mu_A(G_k^c)$: their tail is only $\le\eta2^{-(\ell_*-k_0)+1}\approx10^{-178}$. The current version adds this amount explicitly (§7.2). No printed digit of $c_p$ changed. The final lower bounds are now rounded *down* (the first version printed values rounded to nearest).
12. **Independent re-implementation.** `check_assemble.py` shares no code with `assemble.py` or `early_phase.py`. It recomputes $q_1,q_2,q_3$ with its own DP. It then redoes, from the report's text alone:
    - phase 1 and the explicit part of phase 2 ($b_{k-1}\le3000$), in exact rational arithmetic;
    - the far tail up to $10^{60}$, with its own implementations of Lemma T (in logarithms) and Lemma T′;
    - the remainder $\eta2^{-(\ell_*-k_0)+1}$.

    For every listed $p$ it reproduces the schedule, every $s_k$, and $\Pi_A$, $\delta_A$ and $c_p$ to all printed digits (§10). Separately, Lemma T′ was tested against Lemma T on 3866 windows (`test_Tprime.py`).

13. **Markov's inequality needs $\varepsilon_\ell\ge0$.** This holds: $p^k\mathrm{Coll}_k=\sum_{\psi}|\mathbb E\psi(X)|^2$ over the characters $\psi$ of $\mathbb Z/p^k$, which is nondecreasing in $k$. So $\varepsilon=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D\ge0$, and $\mu_A(G'\cap\{\varepsilon>\bar\varepsilon\})\le\mathbb E_A[\varepsilon\mathbf 1_{G'}]/\bar\varepsilon$.
14. **Digits versus carries in Lemma Q (c).** The level-$\ell_i$ digit of $Y_i$ is linear in the block-$i$ data only after the lower part has been fixed. Given the lower blocks and $a_0$, the lower part of $Y_i$ is known; if it is not $\equiv0\pmod{p^{\ell_i}}$ the event is empty. The term $T_{<i+1}/(pw_{i+1})$ is integral at level $\ell_i$ only on $C^T_i$, where $\tau+S_i\equiv0\pmod p$, and then its digit is $s_1+(\text{known carry})$. Both points are in the proof; we re-derived them in the second pass.
15. **Hypotheses of C3 itself.**
    - $n_0=3p\ge2p$.
    - $A$ is an atom of $\mathcal G_0$: $m_0=V_{3p}=3$ on $A$, so the atom of $x$ is $x+p^3\mathbb Z_p=A$.
    - Admissibility: $D_0=1\le m_0-M_{4p}=2$ and $M_{4p}=1<3$.
    - $Z^0_{3p}\ne0$ on all of $A$, not just almost everywhere: $S_e(x)\bmod p^3$ and $S'_e(x)\bmod p$ are constant on $A$.
    - The $\bar\varepsilon_\ell$ are deterministic with $\prod(1+\bar\varepsilon_\ell)<\infty$.
    - $\delta_A$ bounds $\mu_A(\tau_0<\infty)$ by a union bound over $\ell$ of $\mu_A(B_\ell^c)$.

*How the obstructions of the brief are respected.*
- **Theorem 3.6 (no residue-class criterion).** None is used. The conclusion is a positive-measure statement for a fat closed set inside $p^3\mathbb Z_p$, which has no interior.
- **Prop 11.12 (per-window Cauchy–Schwarz fails).** We use R3M's two-window inequality (C3), as R3M intended. The mod-$p$ shell enters only through $\chi^2_{W_0}=q_1-1$ for the first window.
- **Prop 11.15(b) (infinite annealed mean).** We never average $\Lambda$ over deep gates. On $G'_\ell$ all depths are $\le s$; deep gates enter only through $\mu_A(G_\ell^c)$, whose union bound is summable.
- **Barrier lemmas (Thm 3.10, Prop 11.23).** These concern bounds that use finitely many digits of unit parts, uniformly in the position. Our bounds use the actual structure of $A$:
  - phase 1 is a finite deterministic computation for each $p$ (finitely many windows);
  - the tail uses averaging over $x$ through Hensel's lemma (Prop H′), as the brief suggests;
  - the constants $q_1,q_2,q_3$ are fixed numbers for each $p$, not uniform covering statements.

  Nothing claims a deterministic covering of all residues at all depths.

## 9. The "large $p$" question: what an all-$p$ theorem needs

**9.1 Where $p$ enters.** In the proof of Theorem M, $p$ enters only through:
- the three constants $q_1(p),q_2(p),q_3(p)$;
- the Wilson condition in Proposition W;
- elementary quantities ($\alpha$, $r_1=2^{-p}p^\alpha\rho^{-(1-1/p)}$, and counts of $p$- and $p^2$-multiples), which only get better as $p$ grows.

As $p$ grows, $\Pi_A\to1$ (phase 1 costs $\log\Pi\approx2p^2(q_1-1)+2p(q_2-1)$), and $\delta_A$ is dominated by the deep-gate terms $\mu_A(G_k^c)$ of the first windows that reach past $b=p^2$. There the cheapest admissible cap $s=3$ costs about $1/p$ per $p^2$-multiple gate. So $c_p\approx(1-\sqrt{\delta_A})^2$ lies between $0.69$ and $0.87$ for $17\le p\le97$ (§7.3), and it is not monotone in $p$: it depends on where the schedule crosses $p^2$. A smaller $\eta$, or a schedule tuned near $p^2$, would give a larger $c_p$; we did not optimise this.

**9.2 Hypothesis AC($p$) (arithmetic anti-concentration).**
$$q_1(p)\le1+p^{-3},\qquad q_2(p)\le1+p^{-1},\qquad q_3(p)\le2.$$
These hold for every prime $13\le p\le97$, and fail at $p=11$ ($q_1(11)-1=1.4\cdot10^{-3}>11^{-3}$) and at $p\le7$ (§4.3). In the random model (independent uniform residues in place of $r!$, $r!H_r$, $F_r$) the deviations are $O(p^{c}2^{-p})$.

**Corollary M′ [heuristic, not proved].** AC($p$) for all $p\ge p_0$ would give $\mu(K_p)>0$ for all non-Wilson $p\ge p_1$, with $p_1$ computable from $p_0$. What is missing for a proof is routine but unwritten: a $p$-uniform version of the schedule estimates of §§6–7, i.e. an analytic proof that the greedy phase-1 schedule satisfies (6.1) up to $p^2$, and that the phase-2 bounds of Lemma T′ sum to $\le$ an explicit constant uniformly in $p$. We did not write it, so this item is labelled heuristic. Wilson primes would additionally need a first block with $\lambda_e\ne k_e$ (Prop W). One is given at $p=13$; for the third known Wilson prime 563, and for any further one, we have none.

**9.3 Why AC is genuinely arithmetic.**
- $q_1(p)-1=\chi^2$ of the subset-sum law of $\{r!\bmod p\}_{r<p}$, i.e. $\sum_{b\ne0}\prod_{r<p}\cos^2(\pi br!/p)$.
- A uniform bound $q_1(p)\le1+o(1)$ would require that, for every $b\ne0$, the products $\prod_r|\cos(\pi br!/p)|$ are small. This is an equidistribution statement for the dilates $b\cdot\{r!\bmod p\}$.
- To our knowledge even the weaker statement that $r!\bmod p$ ($r<p$) takes a positive proportion of residues is open; the known lower bounds for the number of distinct values are of order $\sqrt p$. We did not search the literature systematically, so this is a reported belief, not a verified claim. *[Lead's note, after the round-4 novelty referee: the best published lower bound is $(\sqrt2-o(1))\sqrt p$ (Grebennikov–Sagdeev–Semchankau–Vasilevskii 2024); an unrefereed preprint, arXiv:2608.01781 (Aug 2026), claims $\gg p^{8/15}$. Whether $|\{r!\bmod p\}|\sim(1-1/e)p$ is Erdős Problem #478.]*
- Similarly $q_2$ concerns the pairs $(r!,\,r!H_r)$ modulo $p$, with $r!H_r=|s(r+1,2)|$ (Stirling numbers of the first kind), together with the $p^2$-digit of $\sum\delta_rr!$.
- $q_3$ concerns the falling factorials $(p-1)!/(p-1-r)!$ modulo $p^3$. Note R3F's Theorem 11.17: their only signed relation over $\mathbb Z$ is $\pm(e_{p-2}+e_{p-1})$.

**9.4 A large-$p$ trap we checked: "one random digit per level".** Before finding Lemma Q we tried to get the fine-scale decay purely from averaging over the digits of $x$, block by block. Each level supplies exactly one fresh random digit (the gate unit $w$, through its first-order effect $pwH_r$), while the band contains one new frequency digit per level. So averaging alone gives a per-level factor $\approx1$, not $\approx1/p$ (§12, item 2). The decay must come from a two-dimensional constraint per block (value and derivative), and its size is the arithmetic constant $q_2(p)/p$ of Lemma Q.

**9.5 Proposition Q (exact annealed band mass of two-block composites) [proved; formula verified against direct computation].** Let $z$ be Haar on $p\mathbb Z_p$, conditioned on $v(z+p)=v(z+2p)=1$, and let $L=L'=p$ (so $D=1$, $K=2$). With $A,B$ as in §4.1, $N=\sum_{u<p}\delta_uu!$, $k=N/p\bmod p$ when $p\mid N$, $s=\sum_u\delta'_uu!\bmod p$ for an independent lazy signed $\delta'$, and $\Lambda=B$,
$$\mathbb E[\varepsilon]=\frac{p^2}{p-2}\,\mathbb E\Big[\mathbf 1_{p\mid N}\cdot\mathrm{cnt}(k,\Lambda,s)\Big]-p\,\mathrm{Coll}_1,\qquad \mathrm{Coll}_1=P(N\equiv0\bmod p)=q_1(p)/p .$$
Here $\mathrm{cnt}=1-[k=\Lambda]-[s=2\Lambda-k]$ if $\Lambda\ne s$, and $\mathrm{cnt}=(p-2)[k=s]$ if $\Lambda=s$.

*Proof.* Write $z=p\zeta$.
- Modulo $p^2$: $\pi_u(z)\equiv u!(1+p\zeta H_u)$ for $u<p$, and $\pi_{p+u}(z)\equiv-p(\zeta+1)u!$ (Wilson). So $T\equiv N+p\zeta\Lambda-p(\zeta+1)s\pmod{p^2}$.
- $T\equiv0\pmod{p^2}$ iff $p\mid N$ and $(\Lambda-s)\zeta\equiv s-k\pmod p$.
- Count the admissible $\zeta\in\mathbb Z/p\setminus\{-1,-2\}$: if $\Lambda\ne s$ there is one root, excluded exactly when $k=\Lambda$ (root $-1$) or $s=2\Lambda-k$ (root $-2$); if $\Lambda=s$ every $\zeta$ works when $k=s$. Average over $\zeta$.
- $\mathrm{Coll}_1=P(N\equiv0)$ does not depend on $\zeta$. ∎

Exact values (`twoblock_exact.py`; formula and direct computation agree exactly for $p=7,\dots,23$):

| $p$ | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|
| $\mathbb E[\varepsilon_{\text{2-block}}]$ | $6.73\cdot10^{-4}$ | $3.71\cdot10^{-5}$ | $6.50\cdot10^{-8}$ | $9.67\cdot10^{-11}$ | $4.54\cdot10^{-12}$ | $7.36\cdot10^{-15}$ |

In the random model the bracket equals $1/p$ exactly and $\mathbb E\varepsilon\approx0$. The real value is an arithmetic correlation sum of the kind discussed in 9.3.

## 10. Numerical tests

All tests use exact integer or rational arithmetic unless marked otherwise. Logs are in `data/round4/M4C/`, and each run starts with its command line. "Control" means a deliberately wrong variant of the inequality that the same test must catch; it shows that the test can fail.

| object | script (log) | what is compared | runs | result |
|---|---|---|---|---|
| Lemma H2 | `test_H2.py` (`test_H2.log`) | both sides exactly, on balls $B$; $F$ random polynomials, signed window sums, and polynomials with planted double roots; control: threshold $D+2$ in place of $D$ | $p=3$: 3000; $p=5$: 2000; $p=7$: 1152 trials | 0 failures in 6152; left side $>0$ in 861 trials; max left/right $0.944,\,0.980,\,0.993$; control violated 294, 185, 123 times |
| Prop H′ (identity) | `test_Hprime.py … pointwise` (`test_Hprime.log`) | first-nonzero-index identity with the derivative condition, both sides exact | $p=3$: 169, $p=5$: 116, $p=7$: 79 points | 364/364 exact equalities |
| Prop H′ (ball average) | `test_Hprime.py` | the inequality itself, averaged over a ball | $p=3$: 6 qualifying balls (of 300 drawn) | 0 failures; max ratio $0.0067$ |
| Lemma Q (and P) | `test_Q.py` (`test_Q.log`) | exact DP of $P(v(T)\ge k,v(T')\ge f)$ against the bound; control: $J$-factor $q_2/p^4$ | $p=5$: 134; $p=7$: 149; $p=11$: 103 trials (22, 59, 21 with $J\ne\emptyset$) | 0 failures; max ratio $0.488,\,0.497,\,0.4996$; control violated 18, 54, 16 times |
| $q_1,q_2,q_3$ | `qconst_brute.py` (`qconst_brute.log`) | enumeration of all $3^p$ signed vectors against the DP of `early_phase.py` | $p=5,7,11,13$ | equal as rationals |
| $q_1,q_2,q_3$ | `check_assemble.py` (`check_assemble.log`) | a second, independent DP | $11\le p\le97$ | agree with `qtable.log` |
| Prop W | `test_base.py` (`test_base.log`) | $S_e(x)\bmod p^{12}$ and $S'_e(x)$ evaluated directly | primes $7\le p\le97$, 20 random $x\in A$ each (plus 30 generic $x\in p\mathbb Z_p$ for $p\le61$) | alive with $V_{3p}=3$ and slope 0 in every case; at the Wilson prime 13 the block $\{0,p-1\}$ gives slope 0 in 0/20 cases (as predicted) and the explicit block in 20/20 |
| Lemma T′ vs T | `test_Tprime.py` (`test_Tprime.log`) | closed form $\ge$ term-by-term bound | 3866 windows, $p=11,13,17,23,31$, $3\le s\le11$ | 0 failures; margin $\ge10^{5.9}$ |
| Theorem M | `assemble.py` (`assemble.log`) and `check_assemble.py` (`check_assemble.log`) | full assembly; independent re-implementation | all 21 primes $11\le p\le97$ | $\Pi_A\delta_A<1$ for each, so $c_p>0$ (§7.3). The checker reproduces the schedule, $\Pi_A$ (15 digits), $\delta_A$ (10 digits) and $c_p$ for every $p$ |
| Prop Q | `twoblock_exact.py` (`twoblock_exact.log`) | closed formula against direct enumeration | $p=7,\dots,23$ | equal as rationals |
| Lemma D1 | `test_D1.py` (`test_D1.log`) | identities, fibre inequality, recursion; control $B/8$ | $p=3,5,7$ | 0 failures in all checks (several hundred recursion checks); max fibre ratio $0.93$; control violated in every nonempty sample |
| Theorem E | `test_E.py` (`test_E.log`) | mean, variance and Chebyshev bound on atoms | $p=3,5$ | 0 failures; the $p=7$ run was too slow and was stopped (noted in the log) |

Exploratory Monte Carlo (`afe_terms.py`, `afe_series.py`, `afe_cond.py`, `winpair_stats.py`) was used only for orientation, is [heuristic], and enters no proof.

## 11. Secondary results (not used in Theorem M)

### 11.1 A pathwise form of the two-window bound (Theorems E, F)

Setting of R3M Theorem C3: deterministic times $2p\le n_0<n_1<\cdots$, the atoms of $\mathcal G_k$ are the cylinders $x+p^{m_k(x)}\mathbb Z_p$, $M_k=c_{n_k}Z^0_{n_k}$, and $\mathrm{lin}_k$ is (5.2) of R3M for $(W_{k-1},W_k)$.

**Theorem E [proved].** Let $A'$ be an atom of $\mathcal G_{k-1}$ on which $\mathrm{lin}_k$ holds, let $\varepsilon_k(A')$ be the (constant) fine-scale mass, and let $\theta>0$. Then
$$\mu_{A'}\big(M_{k+1}<M_k-\theta M_{k-1}\big)\ \le\ \min\big(1,\varepsilon_k(A')/\theta^2\big).$$

*Proof.*
- Let $P=P^0_{n_{k-1}}$, which is constant on $A'$. By R3M Prop A(i) for both windows and (F2), at every $x'=x_0+p^{m}w\in A'$:
$$Z^0_{n_k}=\sum_{g\in P}m_W(\tau_g\bmod p^{D}),\qquad Z^0_{n_{k+1}}=\sum_{g\in P}m(\tau_g\bmod p^K),$$
  where $m$ is the composite count. $m$ is constant on $A'$ because $K\le m-M$.
- By R3M Lemma 2(b), $\tau_g(x')\equiv\tau^0_g-\beta_gw\pmod{p^K}$ with $\beta_g$ a unit, so each $\tau_g\bmod p^K$ is uniform when $w$ is.
- Let $d(r)=m(r)-2^{L'}p^{-D'}m_W(r\bmod p^D)$ and $X=\sum_gd(\tau_g)$. Then $M_{k+1}-M_k=c_{n_{k+1}}X$.
- Cauchy–Schwarz over $g$ and Parseval give $\mathbb E_wX^2\le|P|^2p^{-K}\sum_rd(r)^2=|P|^2\,4^{L+L'}p^{-2K}\varepsilon$, i.e. $\mathbb E[(M_{k+1}-M_k)^2]\le M_{k-1}^2\varepsilon$.
- Chebyshev's inequality finishes the proof. ∎

**Theorem F [proved].** Let $A$ be an admissible atom of $\mathcal G_0$ with $Z^0_{n_0}\ge1$. Then
$$\frac{\mu(K_p\cap A)}{\mu(A)}\ \ge\ \frac1{4(1+\chi^2_{W_0})}-\sum_{k\ge1}\Big[\mu_A(\mathrm{lin}_k^c)+\mathbb E_A\big[\mathbf 1_{\mathrm{lin}_k}\min(1,16\varepsilon_k)\big]\Big].$$
Averaging over atoms (stationarity: $\varepsilon_k$ depends on $x$ only through $z=x+n_{k-1}$) turns the series into $\sum_k\mathbb E_{z}[\min(1,16\varepsilon_{L_{k-1},L_k}(z))]$ over Haar-random $z$.

*Proof.*
- By Paley–Zygmund with R3M Prop B, $\mu_A(M_1\ge M_0/2)\ge1/(4(1+\chi^2))$.
- On that event, and on $\bigcap_k\big(\mathrm{lin}_k\cap\{M_{k+1}\ge M_k-M_{k-1}/4\}\big)$, induction gives $M_k\ge M_{k-1}/2>0$ for all $k$, hence $x\in K_p$.
- Union bound, using Theorem E with $\theta=\frac14$ on each atom of $\mathcal G_{k-1}$. ∎

The $\min(1,\cdot)$ makes every term finite without any truncation at deep gates (compare note Prop 11.15(b)). For the deterministic phase of §6, R3M's C3 is much better: it costs $\prod(1+\bar\varepsilon)\approx1$, not the factor $16$ and the base $1/4$. That is why Theorem M uses C3.

### 11.2 A deterministic two-window recursion (Lemma D1, Theorem D2)

**Lemma D1 [proved].** Let $x$ be arbitrary (no linear-regime or slope condition), let $n_0<n_1<n_2$, and let $\mathcal P$ be any set of paths alive at $n_0$. Let $Z_i$ be the number of its descendants alive at $n_i$ and $M_i=c_{n_i}Z_i$. Let $B=\sum_{\zeta\not\equiv0\ (p^{D'})}|\hat\nu(\zeta)|$ be the $L^1$ band mass of the composite law $\nu$ modulo $p^{K}$. Then for every $\theta>0$
$$M_2\ \ge\ \big(1-B/\theta\big)^+\big(M_1-\theta M_0\big).$$

*Proof.*
- By (F2), $Z_1=\sum_{g\in\mathcal P}m_W(\tau_g)$ and $Z_2=\sum_gm(\tau_g)$, exactly, at the point $x$.
- Fourier inversion gives $|\nu(r)-p^{-D'}\nu_D(\bar r)|\le p^{-K}B$.
- On fibres with $\nu_D(\bar r)\ge\theta p^{-D}$ this gives $m(r)\ge(1-B/\theta)2^{L'}p^{-D'}m_W(\bar r)$.
- The light fibres carry at most $\theta p^{-D}2^{L}|\mathcal P|$ children.
- Normalise using $c_{n_2}2^{L'}p^{-D'}=c_{n_1}$ and $c_{n_1}p^{-D}2^L=c_{n_0}$. ∎

**Theorem D2 [proved].** If $M_1\ge a_1M_0>0$, $B_1\le a_1/8$, and $B_k\le3/64$ for all $k\ge2$ (with $\theta_k=a_k/2$, where $a_1$ is given and $a_k=3/8$ for $k\ge2$), then $M_k>0$ for all $k$, so $x\in K_p$. A deterministic base valid for every $p$ is: $x\equiv0\pmod p$, $v(x+p)=1$, $\mathcal P=\{(1)\}$, $n_0=1$, $n_1=p$. By Cauchy–Davenport $Z_1\ge1$, so $a_1=p2^{1-p}$.

*Status.* The hypothesis is an $L^1$ (sup-norm) fine-scale bound. We found no route to it that avoids the arithmetic of §9.3, and it is stronger than what Lemma Q gives, so Theorem D2 is recorded only as a criterion. Lemma D1 was tested exactly (§10).

## 12. Failed attempts and where they break

1. **Deterministic bounds on $\varepsilon$ for windows of length $\approx p$ (the brief's first suggestion).**
   - Pointwise bounds are available: Prop P1's $q_1^{n_1}q_2^{n_2}-1$, and the analogous bound with $q_d$ for deeper gates.
   - But they do not decay with the window length; they grow like $K(q_1-1)$. Summed over infinitely many windows they diverge, so pointwise bounds alone can never close Theorem C3.
   - They are used only for the finitely many windows of phase 1.
2. **Decay of $\varepsilon$ from the randomness of $x$ alone ("one random digit per level", §9.4).** For a frequency of order $p^d$, the averaging over the gate unit of each level gives a per-level factor $p\cdot P(\text{2D relation})$.
   - Without arithmetic input this is only bounded by $p\cdot P(\text{1D relation})\ge1$; it breaks at the per-level step.
   - Lemma Q supplies exactly the missing 2D anti-concentration, at the cost of the arithmetic constant $q_2(p)$.
3. **The $L^1$ route (Theorem D2) at large $p$.** In the random model, $B\approx p^{D+1}(2/\pi)^{L}$ decays for $p\ge5$. But no averaging identity such as Lemma H2 exists for $L^1$ masses, and the Cauchy–Schwarz passage $B\le\sqrt{p^K\varepsilon}$ needs $\varepsilon\le p^{-K}$, which the Hensel terms $\approx p^{-D/2}$ violate. It breaks at "$L^1$ from $L^2$".
4. **Uniform-in-$p$ constants (Corollary M′).**
   - Bounding $q_1(p)$ for all $p$ by Littlewood–Offord or Cauchy–Davenport arguments gives only $\max_aP(\sum\delta_rr!\equiv a)\le\frac12$, i.e. $q_1\le p/2$. That is useless.
   - Equidistribution of $b\cdot\{r!\bmod p\}$ would be needed (§9.3). The proof breaks at "for all $p$".
5. **Theorem F with the Chebyshev constant.** The base $\frac14(1+\chi^2)^{-1}$ and the factor 16 make the deterministic phase too expensive at $p=11,13$, where $\sum_k\varepsilon_k\approx0.2$–$2$ in phase 1. Using C3's product $\prod(1+\bar\varepsilon_k)$ instead fixed this (Theorem M).
6. **$p=7$.** With the greedy phase-1 schedule on $p^3\mathbb Z_7$, the window entering phase 2 has $N_W=4$, while (T2) needs $N_W\ge2s+2\ge8$. Lengthening phase 1 (atom $p^4\mathbb Z_p$) makes $\Pi_{\rm phase1}\approx e^{10}$, because $q_1(7)-1=0.014$. We did not pursue $p=7$ further; it is the case M4A reports.
7. **Monte Carlo of the AFE series** (`afe_terms.py`, `afe_cond.py`, `winpair_stats.py`) was useful only as orientation. Its estimates are heuristic and are not used anywhere in the proofs.

## 13. What remains open

1. **All $p\ge p_0$.** This needs AC($p$) of §9.2 (uniform anti-concentration of signed sums of $r!$, of $(r!,r!H_r)$, and of falling factorials modulo $p^3$) and a $p$-uniform write-up of the schedule estimates. The second part is routine; the first is an open arithmetic problem as far as we know. The computation of Theorem M is polynomial in $p$ ($O(p^3)$ for the constants, plus a short schedule computation), so it can be pushed to larger $p$ with an optimised $q_2$ routine.
2. **Wilson primes.** The Wilson prime $563$, and any unknown Wilson prime ($>2\cdot10^{13}$), needs some first block with $\lambda_e\ne k_e$ (Prop W). At $563$ a random search as in `test_base.py` would very likely find one. Any such block works; there is no reason to expect none, but we have no proof.
3. **$p=3,5,7$.** At $p=3,5$, Lemma Q's gain $q_2/p$ is too weak against the deep-gate costs ($q_2(5)=1.95$). At $p=7$ the obstruction is the transition between phases (§12, item 6). M4A reports $p=7$.
4. **Q3** is untouched: $K_p$ is nowhere dense, and Theorem M gives no natural number in $K_p$.
5. **Independent verification.** Theorem M rests on the lemmas of §§2–7 and on two programs that agree: `assemble.py`, and `check_assemble.py`, written separately from the report text. Both were written in this session, so they could share a misreading of the report. What is still missing is a check by a human, or by a program written by someone else, of (i) the proofs of Lemmas H2, Q and T and Prop H′, and (ii) the assembly. The most delicate points are listed in §8.
6. **Better constants.** Nothing was optimised. Two places would pay off: the $s$-rule near $b=p^2$ (§9.1), and the phase-1 schedule at $p=11$, where $\Pi_A\approx10.6$.

## 14. Credit

- R3M (round 3): the window identity, Prop B, the two-window inequality (Prop C2) and the conditional Theorem C3, which Theorem M applies; also Lemma C5, Remark C6 and Prop N3, whose programme §§2–3 carry out.
- R1b (round 2): the quenched martingale at $p=2$ (note §10.1), of which C3 is the odd-$p$ descendant. R3Q (round 3): the $p=2$ explicit-rate machinery, in particular the idea of controlling high slopes through the second derivative (its Lemma 8), the 2-adic precursor of Lemma Q.
- R3F (round 3): the gate-block Fourier analysis, the factorial measure and Theorem 11.17, which motivated the constants of §4.
- Track M4A (round 4, in parallel) reports a proof of $\mu(K_p)>0$ for $p=7,\dots,23$ by a related route: an averaged Hensel identity (its Theorem 1) and a quenched anti-concentration lemma (its Lemma Q). We saw only its headline, after our Lemmas H2, Q and P were written and tested, and we have not compared the proofs in detail. Agreement of the two independent arguments on $11\le p\le23$ is evidence for both; it is not a check of either.
- Classical tools: Hensel's lemma; the Cauchy–Davenport theorem; Paley–Zygmund; Chebyshev, Markov and Cauchy–Schwarz; Minkowski (inside C3). The branching-process context is Smith–Wilkinson, Athreya–Karlin and Afanasyev–Geiger–Kersting–Vatutin, and the second-moment method on trees is Lyons'.
- Wilson's theorem and the Wilson quotient (Prop W). Wolstenholme-type facts: only $H_{p-1}\equiv0\pmod p$ is used.
- All of this was produced in an AI-assisted session (track M4C of round 4). The computation was reproduced by a second program from the same session (§8, item 12). Nothing here has yet been checked by a human or by an outside checker.

