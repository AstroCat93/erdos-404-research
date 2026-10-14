# Logic check of round-4 track M4C (Theorem M: $\mu(K_p)>0$ for $11\le p\le97$)

Date: 2026-10-14. Lens: LOGIC. Made by the `verify_C_logic` track of round 4. Classification: Internal (research working file).

- **Checked:** `data/round4/reports/M4C.md` §§1–8, i.e. Lemma H2, Proposition H′, Lemmas P and Q, §4 (the constants $q_1,q_2,q_3$ and which block gets which constant), Lemma 5.1, Proposition W, Proposition P1, Lemmas L, T, T′, and the proof of Theorem M with the table of §7.3. I also read `code/round4/M4C/assemble.py`, `early_phase.py`, the header of `check_assemble.py`, and the logs `assemble.log`, `check_assemble.log` and `qtable.log` in `data/round4/M4C/`.
- **Foundations re-read:** R3M Theorem C3 and its setting (`data/round3/reports/R3M.md` §5, including the definition of $B_\ell$, $\tau_j$, admissibility and $\Pi_A$), Lemma 1, Lemma 2, Prop A, Prop B and Prop C2. As instructed, C3 is taken as given; I checked that its hypotheses are met exactly.
- **Checker code** (new; it shares no code with `code/round4/M4C/`): `code/round4/verify_C_logic/`
  - `vcl_q.py`: exact $q_1,q_2,q_3$ from the definitions of §4.1;
  - `vcl_propW.py`: Proposition W;
  - `vcl_assemble.py`: the whole of Theorem M, re-derived from the report text, including an explicit far-tail remainder (§8 below);
  - `vcl_lemmaQ.py`, `vcl_H2direct.py`, `vcl_H2.py`: exact tests of Lemma Q (with Lemma P), Lemma H2, and Prop H′;
  - `runlog.sh`.
- **Logs:** `data/round4/verify_C_logic/`: `q_consts.log`, `propW.log`, `assemble_indep.log`, `lemmaQ.log`, `H2direct.log` and `H2ball.log`. Each run starts with `=== command:` and ends with `=== exit:`.
- **Budget used:** about 15 core-minutes at `nice -n 10`.

## Headline

**Verdict: confirmed-with-fixes.** Theorem M holds as stated, and its label [computer-assisted] is right. For every prime $11\le p\le97$,
$$\mu(K_p\cap p^3\mathbb Z_p)\ \ge\ c_p\,p^{-3},$$
with $c_{11}\ge1.254\cdot10^{-4}$, $c_{13}\ge0.572$, and $c_p\ge0.69$ for $17\le p\le97$.

I checked every link of the chain line by line. Every hypothesis of R3M Theorem C3 is met exactly:
- the admissible atom $A=p^3\mathbb Z_p$ at $n_0=3p$;
- $1+\chi^2_{W_0}=q_1$;
- deterministic thresholds $\bar\varepsilon_\ell$, fixed before $x$ is seen;
- the union bound for $\mu_A(\tau_0<\infty)$;
- Paley–Zygmund.

The new lemmas (H2, H′, P, Q, P1, L, T, T′, W) are correct as proved. The three steps I judged most delicate pass exact tests that I wrote independently:
- the value/derivative digit bookkeeping of Lemma Q;
- the Hensel increment of Lemma H2;
- the first-nonzero-index identity of Prop H′.

My independent re-implementation of the assembly agrees with the track's two programs. It reproduces, for all 21 primes:
- the exact constants $q_1,q_2,q_3$;
- the phase-1 schedules;
- $\delta_A$ to every printed digit;
- $\Pi_A$;
- $c_p$.

Every printed bound in §7.3 is rounded in the safe direction.

The fixes are to the write-up. None changes a number or a conclusion.
- **(F1)** The far-tail remainder ($b_{k-1}>10^{60}$) is asserted with an unspecified $O(\ln b)$ term, and `assemble.py` hard-codes it as $10^{-1000}$. I supply an explicit majorant (§8). It gives $\sum_{k\ge\ell_*}\sqrt{\mathfrak B'_k}\le10^{-2.6\cdot10^{58}}$ or less for every listed $p$, so the claim holds.
- **(F2)** §4.2 has a displayed inequality that is false as written when $e_i<3$. It also has an unjustified "$\le q_2$" when $e_i=1$. Both need the one-line monotonicity of $e\mapsto p^e\max_aP(X\equiv a\bmod p^e)$. In every application $e_i=d_{i+1}$, so nothing downstream is affected.
- **(F3)** In the proof of Lemma Q, the events $C^T_i,C^{T'}_i$ should be defined explicitly, and one justification in step (b) is misattributed. This is wording only.
- **(F4)–(F6)** Wording and labelling:
  - "no truncation" in the headline;
  - the status of Cor M′ in the §0 table;
  - the $p=11$ row of §7.3, from which $c_{11}$ cannot be recomputed.

## 1. The application of Theorem C3 (report §5, §7.2)

R3M's statement: with deterministic times $2p\le n_0<n_1<\cdots$, take an admissible atom $A$ of $\mathcal G_j$ and nonnegative $\bar\varepsilon_\ell$ with $\Pi=\prod_{\ell>j}(1+\bar\varepsilon_\ell)<\infty$. Let $B_\ell=\{\mathrm{lin}_\ell\}\cap\{\varepsilon_\ell\le\bar\varepsilon_\ell\}$ and $\tau_j=\min\{\ell>j:x\notin B_\ell\}$. If $\delta_A=\mu_A(\tau_j<\infty)<1/\Pi_A$ with $\Pi_A=(1+\chi_j^2(A))\Pi$, then $\mu(K_p\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$.

| hypothesis | M4C | check |
|---|---|---|
| times | $n_k=b_kp$, $b_0=3$, $b_1=4$, so $n_0=3p\ge2p$ | ✓ deterministic: $b_{k+1}$ depends only on $k$, $b_{k-1}$, $b_k$ and $s_k$, and $s_k$ only on $k$ and $b_{k-1}$ |
| $A$ is an atom of $\mathcal G_0$ | $A=p^3\mathbb Z_p$ | ✓ For $x\in A$ and $i\le3p<p^2$, $v(x+i)=v(i)$, so $m_0=V_{3p}(x)=3$ and the atom of $x$ is $x+p^3\mathbb Z_p=A$. |
| admissibility | $D_0=v(x+4p)=1\le m_0-M_{4p}=2$ and $M_{4p}=1<3$ | ✓ (for $p\ge5$) |
| $Z^0_{3p}\ne0$ on all of $A$ | Prop W | ✓ See §4. Since $x\equiv0\pmod{p^3}$, $S_e(x)\equiv S_e(0)$ and $S'_e(x)\equiv S'_e(0)\pmod{p^3}$, so one path serves all of $A$. |
| $1+\chi^2_{W_0}$ | $=q_1$ | ✓ The window $[3p,4p)$ has elements $\prod_{i=3p+1}^{3p+u}(x+i)\equiv u!\pmod p$ and $D_0=1$. So $1+\chi^2=p\,\mathrm{Coll}_1=p\,P(\sum\delta_uu!\equiv0)$. The maximum in $q_1$ is attained at $0$, because $P(A\equiv a)=\sum_r\mu(r)\mu(r-a)\le\sum_r\mu(r)^2$. |
| $\varepsilon_\ell$ | $p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$ of the composite at $z=x+n_{\ell-1}$, with lazy signed $\delta$ including $\delta_0$ | ✓ This is R3M's identification in Prop C2. That identification uses only $\pi_N/\pi_n=p^D\cdot$unit, so it holds whether or not $\mathrm{lin}_\ell$ does. |
| thresholds | phase 1: $q_1^{n_1}q_2^{n_2}-1$; phase 2: $\sqrt{\mathfrak B'_k}$ | ✓ deterministic and summable (§§5–8) |
| $\delta_A$ | $\sum_{k>k_0}[\mu_A(G_k^c)+\mu_A(G'_k\cap\{\varepsilon_k>\bar\varepsilon_k\})]$ | ✓ Phase 1 never stops $\tau$ (Prop P1, pointwise on $A$). In phase 2, $\{\tau=k\}\subseteq\mathrm{lin}_k^c\cup(\mathrm{lin}_k\cap\{\varepsilon_k>\bar\varepsilon_k\})\subseteq G_k^c\cup(G'_k\cap\{\varepsilon_k>\bar\varepsilon_k\})$, using Lemma L(b) and $G_k\subseteq G'_k$. |
| Markov | needs $\varepsilon\ge0$ | ✓ §8 item 13: $p^k\mathrm{Coll}_k=\sum_\psi|\mathbb E\psi|^2$ over the characters of $\mathbb Z/p^k$, which is nondecreasing in $k$. So $\mu_A(G'\cap\{\varepsilon>\bar\varepsilon\})\le\mathfrak B/\bar\varepsilon=\sqrt{\mathfrak B}$. |
| conclusion | $c_p=(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$ | ✓ The function is decreasing in both $\Pi_A$ and $\delta_A$, so upper bounds for them give a valid lower bound. |

## 2. Lemma H2 and Proposition H′ (report §2)

**Lemma H2.** Correct. I re-derived each step.
1. *Hensel.* Uniqueness of the root in $y+p^{\lambda+1}\mathbb Z_p$, and $v(F)=\lambda+v(y'-\rho)$ on $U_\rho$ (eq. 2.1).
2. *Disjointness.* Two balls $U_\rho,U_{\rho'}$ that meet have the same $\lambda$, hence they are equal, hence $\rho'\in U_\rho$ and $v(F(\rho'))<\infty$, which is a contradiction.
3. *The root lies in $B$:* $v(y-\rho)\ge D-\lambda>D/2\ge r$.
4. *The ball $\rho+p^{k-\lambda}\mathbb Z_p$ lies in $U_\rho\cap B$:* $k-\lambda>\lambda$ and $k-\lambda>D/2\ge r$. So each root contributes exactly $p^{\lambda_\rho}$ at both $k=D$ and $k=K$.
5. *The remainder:* $Y_K\setminus\bigcup U_\rho\subseteq\{2v(F')\ge D\}$, because a point of $Y_K$ with $2v(F')<D$ lies in $S$.

The case $F\equiv0$ (all $\delta=0$) is trivially consistent: $p^K-p^D\le p^K$. A polynomial $F\ne0$ has finitely many roots.

**Proposition H′.** Correct.
- The bracket identity uses only that $D,K$ are constant on $B$ (Fubini over $\delta$).
- The first nonzero index $j$ with sign $\sigma$ has probability $2^{-j}\cdot\frac14$. Both signs give the same law of $\delta'=\sigma\delta_{j+\cdot}$, and $\sigma\delta$ is again lazy signed.
- The bookkeeping is right:
  - $T_\delta(z)=\sigma\pi_j(z)R_{\delta'}(z+j)$, and $V_{j+t}(z)=V_j(z)+V_t(z+j)$;
  - $v(\pi'_j R)\ge V_j-M_j+V_t(y)=K-M_j\ge K-M\ge\lceil D/2\rceil$ on the event, by R3M Lemma 1(d) and (2.2);
  - hence $v(T')\ge\lceil D/2\rceil\iff v(R'(y))\ge\lceil D/2\rceil-V_j=\lambda_j$.
- The weights are right: $2\cdot2^{-j}/4\cdot p^K=\frac{c_j}2p^{V_t(y)}$ with $c_j=c_j(z)$, and the $\delta=0$ term is $c_{L+L'}$.

**Tests (my code).**
- `vcl_H2direct.py` tests Lemma H2 exactly on single polynomials: random ones, planted double roots, planted near-double roots, and signed window sums. Both sides were computed as exact rationals over $z\in B\bmod p^K$.
  - $p=3,5,7$: 1500, 800 and 500 trials, **0 failures**.
  - The left side was positive in 430 trials, and the largest ratio of left to right side was $0.994$, $0.996$ and $0.990$, so the inequality is nearly sharp.
  - The control, which uses $2v(F')\ge D+2$, was violated 44, 46 and 36 times.
- `vcl_H2.py` tests the setting where H′ is used: composite windows at $p=3$, averaged over environment balls with $D\ge2r$ and $\lceil D/2\rceil\le K-M$.
  - $\mathbb E_B[\varepsilon]\le H$ held on 9 balls; few distinct balls fit the size limits.
  - The pointwise identity $H(z)=c_n+\sum_j\frac{c_j}2\Lambda^{(\lambda_j)}_{n-j}(z+j)$ held exactly at 9/9 points.

## 3. Lemmas P and Q, and §4.2 (report §§3–4)

**Block decomposition.** For $c\in B_i$, $v(\pi_c(y))=\ell_i$. Consecutive gates are exactly $p$ apart, and (1.1) holds for every block of $p$ consecutive indices that starts at a gate, including the last block $[g_I,t)$ whenever $t-g_I=p$, as in all applications. Lemma P is the chain rule over blocks in increasing order. The event $v(T)\ge k$ forces $v(T_{<i+1})\ge\min(\ell_{i+1},k)$ for every $i$. Given the lower blocks, this prescribes $S_i$ modulo $p^{e_i}$, and the digits of block $i$ are independent of the lower blocks. ✓

**Lemma Q.** I re-derived (a)–(d) in full.
- **(a)** Abel summation: $\sum_c\delta_c\pi_c\sum_{i:g_i\le c}(y+g_i)^{-1}=\sum_i(T-T_{<i})/(p^{d_i}w_i)$. On $\{v(T)\ge k\}$ the $T$-terms have valuation $\ge k-d_{\max}\ge f$. ✓
- **(b)** For $i\in J$ we have $\ell_{i+1}=\ell_i+1\le f\le k-d_{\max}<k$, so $e_{i'}=d_{i'+1}$ for all $i'\le i$, and on $\bigcap_{i'\le i}C^T_{i'}$ we get $v(T_{<i'})\ge\ell_{i'}$ for $i'\le i+1$. Hence $Y_i\in\mathbb Z_p$.
  - The terms of $Y-Y_i$ are of two kinds. Block-$>i$ $h$-terms have valuation $\ge\ell_{i+1}$.
  - The terms $T_{<i'}/(p^{d_{i'}}w_{i'})$ with $i'\ge i+2$ have valuation $\ge\ell_{i'-1}\ge\ell_{i+1}$ if $\ell_{i'}\le k$, and $\ge k-d_{\max}\ge f>\ell_i$ otherwise. This uses $v(T_{<i'})=v(T-T_{\ge i'})\ge\min(k,\ell_{i'})$.
  - So $Y\equiv Y_i\pmod{p^{\ell_i+1}}$. ✓
- **(c), the statistic.** Given the lower blocks, write $u_0=U_i\bmod p$, and let $a_0,a_1$ be the digits $0,1$ of $A_i=\sum_r\delta_{g_i+r}r!$.
  - $C^T_i$ fixes $a_0$.
  - Digit 1 of $S_i$ is $u_0(a_1+\epsilon_iw_iB_i)+\kappa(a_0,\text{lower})$, from $S_i\equiv U_i(A_i+\epsilon_ipw_iB_i)\pmod{p^2}$.
  - Digit 1 of $\tau+S_i$, where $\tau=T_{<i}p^{-\ell_i}$, is that digit plus a carry known from $\tau$.
  - The level-$\ell_i$ digit of $Y_i$ is linear once the lower part is fixed, because the block-$i$ terms are all $\equiv0\pmod{p^{\ell_i}}$. It equals (known) $+\,u_0(h_{g_i}a_0+B_i)-(s_1+\kappa')/w_{i+1}$, where I used $h_c\equiv h_{g_i}+H_r\pmod p$.
  - The coefficient of $B_i$ is $u_0(1-\epsilon_iw_i/w_{i+1})$, and it equals $u_0/w_{i+1}$ in both cases:
    - $d_i=1$: then $w_{i+1}=w_i+1$, a unit because $d_{i+1}=1$;
    - $d_i\ge2$: then $\epsilon_i=0$ and $w_{i+1}\equiv1\pmod p$.

  So $C^T_i\cap C^{T'}_i$ prescribes the pair $(a_0,\ a_1-B_i\bmod p)$. ✓

  This is why $(A\bmod p,\lfloor A/p\rfloor-B\bmod p)$ is the right statistic:
  - $a_1$ enters only through the carry of $T$ into level $\ell_i+1$, which the depth-1 end gate divides back down to level $\ell_i$;
  - $B_i$ enters through the $h$-terms of block $i$;
  - both enter with the same nonzero coefficient $u_0/w_{i+1}$.

  It is equivalent to the law of $\sum_r\delta_r r!(1-pH_r)\bmod p^2$, the bijection used in §4.2. I computed $q_2$ both ways for $p\le31$, and the values agree exactly (`q_consts.log`).
- **(d), independence and pointwise in $y$.** The digits of different blocks are disjoint sets of i.i.d. variables, and the events for block $i$ are functions of blocks $\le i$. The conditional bound holds uniformly in the lower blocks, so the chain rule gives the product. $y$ is fixed throughout, and the only randomness is $\delta$. So the bound holds for every $y$ separately. No averaging over $x$ is used; that averaging enters only through H2. ✓

**§4.2 (F2).**
- The displayed chain "$p^{e_i}\max P(S_i\equiv a\bmod p^{e_i})\le p^{e_i-3}\cdot p^3\max P(\cdot\bmod p^3)$" is false when $e_i<3$, because a coarser modulus has a *larger* maximum.
- Similarly, "factor $\le q_2$" for a depth-2 end gate with $e_i=1$ is not justified as written.
- Both conclusions are true, by the monotonicity of $e\mapsto p^e\max_aP(X\equiv a\bmod p^e)$: each class modulo $p^{e-1}$ splits into $p$ classes modulo $p^e$. This gives $q_1\le q_2$, and $\le q_3\le p^{d-3}q_3$ for $e_i\le3$.
- In every application (Prop P1 with $k=K$; Lemma T with $k=V_t(y)$) one has $e_i=d_{i+1}$ for all blocks concerned, so the gap never bites. Add the remark.

**Which constant goes with which block** is correct on $A$ (Lemma 5.1).
- A depth-2 end gate $j$ ($p\,\|\,j$) has its start gate $j-1$ of depth 1, with unit $\xi+j-1\equiv-1\pmod p$.
- A $p^2$-multiple end gate has unit $\equiv-1\pmod{p^2}$ at the start, so the block law modulo $p^3$ is that of $\sum\delta_rF_r$.
- Block 0 of each phase-1 composite also qualifies: $z=x+b_{k-1}p$, and if $p\mid b_{k-1}+1$ then $d_0=1$ and $w_0\equiv-1$.

**Constants.** `vcl_q.py` computes $q_1,q_2,q_3$ exactly for all 23 primes in `qtable.log`. All three constants agree with `qtable.log` to the printed 4 digits (0 mismatches), and with the §4.3 table. The prime 13 is a Wilson prime ($w_{13}\equiv0$). This changes only Proposition W, not the constants.

**Tests (my code).** `vcl_lemmaQ.py` computes $P(v(T)\ge k,v(T')\ge f)$ exactly, by an integer DP over $(T\bmod p^k,T'\bmod p^f)$ with $\delta_0=1$ as in $\Lambda$. The bound uses exact per-block maxima for the non-$J$ blocks and the exact $q_2$ for the $J$ blocks. The environments include planted depth-2 gates preceded by a unit $\equiv-1$, deep gates, and a deep first gate (so that $\epsilon_i=0$ occurs).

| $p$ | trials | with $J\ne\emptyset$ | failures | max LHS/RHS (all / $J\ne\emptyset$) | control ($J$-factor $q_2/p^3$) violated |
|---|---|---|---|---|---|
| 5 | 270 | 76 | 0 | 0.480 / 0.239 | 7 |
| 7 | 200 | 33 | 0 | 0.490 / 0.436 | 5 |
| 11 | 120 | 13 | 0 | 0.499 / 0.478 | 3 |

So the gain $q_2/p$ per $J$-block is attained up to a factor $\approx2$, and one more factor of $p$ is false.

## 4. Proposition W (report §5)

I re-derived the computation. I also replaced it by a cleaner equivalent: since $x\equiv0\pmod{p^3}$ on $A$, it suffices that
$$\sum_je_jj!\equiv0\pmod{p^3}\qquad\text{and}\qquad\sum_je_jj!H_j\not\equiv0\pmod p,$$
where $j!H_j=\pi'_j(0)$ is an integer. The report's slope formula $S'_e\equiv-w_p/(\xi+1)\equiv-w_p\pmod p$ uses three facts:
- $H_{p-1}\equiv0$;
- $\pi'_j\equiv(p-1)!(j-p)!$ for $p\le j<2p$;
- $v(\pi'_j)\ge1$ for $2p\le j<3p$.

The Cauchy–Davenport steps for blocks 2 and 3 are right: there are $p$ nonzero residues $u!$, and the third-block units are $\equiv2u!$.

`vcl_propW.py` builds the path by the report's recipe (blocks 2 and 3 are found by a subset-sum DP) for every prime $7\le p\le97$:
- it checks both congruences exactly;
- it confirms $S'_e(0)\equiv-w_p\pmod p$ for every non-Wilson $p$;
- it re-evaluates $S_e(x),S'_e(x)$ directly (modulo $p^{12}$) at 20 random $x\in A$ for each $p$, and finds alive and slope 0 in 20/20.

At the Wilson prime 13, the block $\{0,12\}$ gives $k_e=\lambda_e=0$ (slope $\ge1$). The report's block $\{0,1,2,3,4,8,9\}$ gives $\sum j!=403234=13\cdot31018$, $k_e\equiv0$ and $\lambda_e\equiv12$, so the path has slope 0. ✓ (`propW.log`: ALL OK.)

## 5. Proposition P1 (report §6)

- **(i)** On $A$, for $b<p^2$: $V_{bp}=V(b)$ and $M_{bp}=\mathrm{Mx}(b)$ with $d_j=1+v_p(j)$, so (6.1) is literally $\mathrm{lin}_k$.
- **(ii)** The composite at $z=x+n_{k-1}\equiv0\pmod p$ has gates at $p,2p,\dots,Np$. Lemma P with $k=K$ gives $\sum e_i=K$ and $e_i=d_{i+1}\in\{1,2\}$. By §4.2, $p^K\mathrm{Coll}_K\le q_1^{n_1}q_2^{n_2}$, and $\varepsilon\le p^K\mathrm{Coll}_K-1$ because $p^D\mathrm{Coll}_D\ge1$.
- The bound is pointwise for every $x\in A$, so phase 1 adds nothing to $\delta_A$.

Minor wording: "with $U=1$" holds only for block 0; the unit is irrelevant.

My code recomputes the greedy schedule from (6.1), allowing $b_{k+1}\le p^2-1$ and nothing else. It gives exactly the track's schedule for all 21 primes, and the same $\log\Pi_{\rm phase1}$.

## 6. Lemmas L, T and T′ (report §7.1): every constant

- **Lemma L(a).** $v(x+jp)>s$ forces $p^2\mid j$ and $v(\xi'+j/p^2)\ge s-2$, where $\xi'=x/p^3$ is Haar on $\mathbb Z_p$ under $\mu_A$. There are $\lfloor b_{\ell+1}/p^2\rfloor$ such $j$. ✓
- **Lemma L(b).**
  - $K=N+\#\{p\mid j\}+\#\{p^2\mid j\}+\sum_{p^2\mid j}v(\xi'+j/p^2)$, which on $G_\ell$ is at most $N+\lceil N/p\rceil+U_N+\Xi(U_N)$. Among $U$ consecutive integers at most $\lceil U/p^a\rceil$ have $v\ge a$, and each $v\le s-3$.
  - $m_{\ell-1}\ge b_{\ell-1}+\lfloor b_{\ell-1}/p\rfloor$.
  - $M_{n_{\ell+1}}\le s$, a cap that also counts earlier gates. This is crude but valid.
  - So (T1) gives both parts of $\mathrm{lin}_\ell$. ✓
- **Lemma T, step 1 (the balls).**
  - $\mathcal B=z+p^{M+1}\mathbb Z_p$ fixes every $v(z+i)$, $i\le Np$. It also fixes the gate units modulo $p^{M+1-d_i}$, which is enough for the $\equiv-1$ conditions.
  - $N\ge p$ gives $M\ge2$, so $\mathcal B\subseteq n_{\ell-1}+A$.
  - $G'_\ell$ is a union of such balls.
- **Lemma T, step 2.** $r=M+1\le s+1$ and $D\ge N_W\ge2s+2\ge2r$; also $\lceil D/2\rceil\le D-s\le K-M$. ✓
- **Lemma T, step 3.**
  - With $j_0=\lfloor j/p\rfloor$: $V_j(z)=V_{j_0p}(z)$, $k=K-V_{j_0p}=V_t(y)$, and $f=\lceil D/2\rceil-V_{j_0p}\le k-M\le k-d_{\max}$.
  - The $y$-blocks are the partial block $[j,(j_0+1)p)$, with factor $\le p^{d_{j_0+1}}$ (crude but valid), and the composite blocks $i'=j_0+1,\dots,N-1$. Their end gates are $j_0+2,\dots,N$, and the last one has $e=d_N$.
  - A composite block $i'\in(j_0,I]$ whose end gate has depth 1 lies in $J$. This uses three facts:
    - $V_{i'p}\le V^+(i')\le V^+(I)<\lceil D^-/2\rceil\le\lceil D/2\rceil$ ($V^+$ is nondecreasing);
    - $i'\le I\le N_W-1\le N-2$, so the block is full;
    - $i'-j_0\ge1$.
  - All constants are $\ge1$ and $q_2/p<1$, so $(q_2/p)^{|J|}\le(q_2/p)^{\nu(j_0)}$ and double counting is harmless.
  - $\sum_{p^2\mid j}(d_j-3)\le\Xi(U)$ on $G'$. ✓
- **Lemma T, step 4.**
  - $\sum_{\lfloor j/p\rfloor=j_0}2^{-j-1}=2^{-j_0p}(1-2^{-p})\le2^{-j_0p}$;
  - $p^{V_{j_0p}}p^{d_{j_0+1}}=p^{V_{(j_0+1)p}}\le p^{V^+(j_0+1)}$;
  - $c_{L+L'}\le2^{-Np}p^{V^+(N)}$. ✓
- **Lemma T′.**
  - $V^+(i)\le i+(i/p+1)+(i/p^2+1)+(i/p^2+1)/(p-1)+s-3<\alpha i+s$.
  - $I\ge I'$, because $V^+(I')<\lceil N_W/2\rceil\le\lceil D^-/2\rceil$ (and $V^+(0)=0$).
  - $\nu(j_0)\ge(I-j_0)(1-1/p)-1$, and $\rho^{\max(0,a)}\le\rho^a$.
  - The terms with $j_0>I$ are dominated using $(1-1/p)j_0\ge I(1-1/p)-1$.
  - The geometric sum in $r_1<1$ follows. Every constant is right. `assemble.py` even uses $2/(1-r_1)$ in place of $1/(1-r_1)$, which is conservative.

## 7. Assembly and the stated $c_p$ (report §7.2–7.3)

`vcl_assemble.py` re-derives everything from the report text. It uses its own exact $q$'s, its own schedule code, its own Lemma T and Lemma T′ evaluation (50-digit mpmath, outward factor $1+10^{-30}$), and its own far-tail remainder (§8). It checks (T1), (T2), $N\ge p$ and $b_{k+1}\le2b_{k-1}$ on every window up to $b_{k-1}>10^{60}$, all by assertions. All 21 primes pass.

| $p$ | my $\Pi_A\le$ | my $\delta_A\le$ | my C3 value | report $c_p\ge$ | report $\mu(K_p)\ge$ (my $c_p/p^3$) |
|---|---|---|---|---|---|
| 11 | 10.6182220580 | 0.0874274368 | $1.254979\cdot10^{-4}$ | $1.254\cdot10^{-4}$ | $9.42\cdot10^{-8}$ ($9.4289\cdot10^{-8}$) |
| 13 | 1.2206606473 | 0.0219904750 | 0.5727774 | 0.572 | $2.60\cdot10^{-4}$ ($2.6071\cdot10^{-4}$) |
| 17 | 1.0084339606 | 0.0093868644 | 0.8080638 | 0.808 | $1.64\cdot10^{-4}$ |
| 19 | 1.0164461970 | 0.0094124405 | 0.8007730 | 0.800 | $1.16\cdot10^{-4}$ |
| 23 | 1.0001001527 | 0.0085874792 | 0.8231593 | 0.823 | $6.76\cdot10^{-5}$ |
| 29 | 1.0000041977 | 0.0056753529 | 0.8550016 | 0.855 | $3.50\cdot10^{-5}$ |
| 31 | 1.0000075521 | 0.0045243329 | 0.8699910 | 0.869 | $2.91\cdot10^{-5}$ |
| 37 | 1.0000000151 | 0.0054797365 | 0.8574292 | 0.857 | $1.69\cdot10^{-5}$ |
| 41 | 1.0000000005 | 0.0282693583 | 0.6919995 | 0.691 | $1.00\cdot10^{-5}$ |
| 43 | 1.0000000027 | 0.0268080974 | 0.6993445 | 0.699 | $8.79\cdot10^{-6}$ |
| 47–97 | $1+O(10^{-13})$ | as in `assemble.log` to all 10 printed digits | as in `assemble.log` | 0.710 … 0.727 | as in §7.3 |

- Every $\delta_A$ agrees with the track's to all printed digits.
- Every $\Pi_A$ agrees to the printed 15 digits. For $p\ge71$ my $\log\Pi_A$ is larger, because my outward factor of $10^{-30}$ per $q$ is cruder; this is irrelevant to $c_p$.
- The windows evaluated explicitly after phase 1, $\ell_*-k_0$, match the table (595, 595, 592, …, 581).
- The decay rate per unit $b$ of the Lemma T′ bound beyond $b=10^{60}$ matches the $\kappa_p$ column ($0.2267$ to $0.5601$).
- **Rounding direction.** Checked for every row of §7.3:
  - each printed $\log\Pi_A$ and $\delta_A$ is $\ge$ the computed upper bound;
  - each printed $c_p$ is $\le$ the computed C3 value;
  - each printed $\mu(K_p)$ is $\le c_p/p^3$.

  At $p=11$ both "$1.25\cdot10^{-4}$" (`assemble.log`, floor to $10^{-6}$) and "$1.254\cdot10^{-4}$" are valid. ✓
- **Remark (F6).** $c_{11}$ is very sensitive: $\Pi_A\delta_A=0.9283$. At the table's rounded values $\log\Pi_A\le2.4$ and $\delta_A\le0.0875$, the C3 formula gives only $2.9\cdot10^{-5}$. The $p=11$ row should print $\Pi_A\le10.61823$ and $\delta_A\le0.0874275$ (so $\Pi_A\delta_A\le0.928324$), so that $c_{11}\ge1.254\cdot10^{-4}$ can be recomputed from the table.
- **Cosmetic.** `assemble.py` rounds $q_2$ up, by a relative $10^{-40}$. This is not conservative in two places: the exponent $-1$ of $\rho$ when $I'=0$, and $r_1$. The effect is $\le10^{-40}$ relative and is absorbed by the final outward factor. My code, with independent rounding, reproduces every printed digit.

## 8. The far tail $b_{k-1}>10^{60}$ (F1)

The report's §7.2 "Fine scale" bullet asserts that $\log\mathfrak B'_k\le-\kappa_pb+O(\ln b)$ and that $\sum_{k\ge\ell_*}\sqrt{\mathfrak B'_k}<10^{-1000}$. `assemble.py` adds a hard-coded $10^{-1000}$ and only *prints* the value at $b=10^{60}$ together with the slope. The claim is true, but it needs the following explicit majorant, which `vcl_assemble.py` (function `remainder`) evaluates for each $p$.

For $k\ge\ell_*$ write $b=b_{k-1}\ge b_*:=b_{\ell_*-1}>10^{60}$ and $\Delta=\ell_*-k_0$. With the far-tail rule:
- $N_W\ge b/4-1$ and $N\le9b/16$;
- $b_{k-1}\ge b_*1.2499^{k-\ell_*}$;
- $s_k\le S(b):=4+\log_p\frac{2b}{p^2\eta}+\big(\Delta+\log_{1.2499}(b/b_*)\big)\log_p2=:\sigma_1\ln b+\sigma_0$.

From Lemma T′, using $\lceil x\rceil\le x+1$, $\Xi(U)\le U/(p-1)+s-3$ and $I'\ge(b/8-\frac12-s)/\alpha-1$:
$$\ln\mathfrak B'_k\le\ln2+a\,b+c\,S(b)+c_0,$$
where:
- $a=\max\big\{\tfrac14(\alpha\ln p-p\ln2),\ \tfrac9{16}[\ln q_1+\tfrac{\ln q_2}p+\tfrac{\ln q_3}{p^2}+\tfrac{\ln p}{p^2(p-1)}]+\tfrac{(1-1/p)\ln\rho}{8\alpha}\big\}<0$;
- $c=\max\{\ln p,\ 2\ln p+(1-1/p)|\ln\rho|/\alpha\}$;
- $c_0$ is an explicit constant.

The program checks two things:
- $b_*\ge2c\sigma_1/|a|$;
- $g(b_*)=ab_*/2+c\sigma_1\ln b_*+c\max(\sigma_0,0)+c_0+\ln2\le0$.

Since $g$ is decreasing beyond $2c\sigma_1/|a|$, this gives $\ln\mathfrak B'_k\le ab/2$ for all $k\ge\ell_*$. Hence
$$\sum_{k\ge\ell_*}\bar\varepsilon_k\le2e^{ab_*/4},$$
and the same bound holds for $\sum\log(1+\bar\varepsilon_k)$.

**Result:** $\sum_{k\ge\ell_*}\bar\varepsilon_k\le10^{-2.63\cdot10^{58}}$ ($p=11$), up to $10^{-7.38\cdot10^{58}}$ ($p=97$), with $a=-\kappa_p$ in every case. The same bounds on $s$, $N$ and $N_W$ give (T1), (T2) and $N\ge p$ for all $b\ge10^{60}$. The deep-gate remainder $\eta2^{-(\ell_*-k_0)+1}$ is added explicitly by both programs; it is $\le1.3\cdot10^{-176}$. (The prose "$\approx10^{-178}$" is low for $p\ge37$: there $\ell_*-k_0\le587$, and the amount reaches $1.3\cdot10^{-176}$ at $p=89,97$. The code adds the exact amount.)

## 9. Fixes (all to the write-up; no number changes)

- **(F1)** §7.2, "Fine scale": replace the $O(\ln b)$ sketch with the explicit majorant of §8. In `assemble.py`, derive the remainder instead of adding a constant $10^{-1000}$.
- **(F2)** §4.2: add "$e\mapsto p^e\max_aP(X\equiv a\bmod p^e)$ is nondecreasing". Correct the displayed chain for $d\ge3$ to "$\le\max(q_3,\,p^{e_i-3}q_3)\le p^{d-3}q_3$". Note that $e_i=d_{i+1}$ in all applications.
- **(F3)** Lemma Q, (b)–(c):
  - define $C^T_i:=\{v(T_{<i+1})\ge\min(\ell_{i+1},k)\}$ and $C^{T'}_i:=\{Y_i\in\mathbb Z_p,\ Y_i\equiv0\pmod{p^{\ell_i+1}}\}$, which is what the proof uses (§8 item 14);
  - the reason for $v(T_{<i'})\ge\ell_{i'}$ ($i'\le i+1$) is $\ell_{i+1}\le f<k$, so that $e_{i'}=d_{i'+1}$ for $i'\le i$. It is not "$d_{i+1}=1$ and $e_i=1$".
- **(F4)** Headline: "verifies FE completely, with no truncation" is inaccurate. The proof truncates at deep gates ($G_\ell,G'_\ell$ with caps $s_k$) and pays for it through Lemma L(a) in $\delta_A$. Say "with no Monte Carlo; the deep-gate truncation is paid for explicitly".
- **(F5)** The §0 table lists Cor M′ as "reduction", while §9.2 labels it [heuristic, not proved]. Use the latter in both places.
- **(F6)** §7.3: print enough digits of $\Pi_A,\delta_A$ at $p=11$ (see §7). Harmonise the $\mu(K_{11})$ entry: $9.42\cdot10^{-8}$ in the table, $9.391\cdot10^{-8}$ in the log; both are valid.
- Optional: in the proof of Prop P1, "with $U=1$" applies to block 0 only.

## 10. Scope, and comparison with M4A

- Not checked in depth, because Theorem M does not use them:
  - Theorems E and F;
  - Lemma D1 and Theorem D2;
  - Proposition Q;
  - the arithmetic discussion of §9.

  Cor M′ was checked only for its label.
- R3M Theorem C3 was taken as given, as instructed. Its hypotheses were matched against the statement in R3M §5 (§1 above).
- Track M4A independently proves $\mu(K_p)>0$ for $p=7$ and $11\le p\le23$. It uses a different atom and schedule, and its proof was verified separately. On $11\le p\le23$ the two arguments agree in conclusion. M4C's atom $p^3\mathbb Z_p$ is much coarser, and its constants are much larger. M4C alone covers $29\le p\le97$.
