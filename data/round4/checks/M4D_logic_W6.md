# Logic check of round-4 track M4D, part II: Theorem W6 with Lemmas W1–W3, Proposition W4 and Corollary W5

Date: 2026-10-14. Lens: LOGIC. Track: `verify_M4D_logic` (round 4), second claim of M4D.
Part I of this track (Lemma L, Theorem F, Corollary F1) is `data/round4/checks/M4D_logic.md`. That file now ends with a short Part II section that summarises this report and points here.

- **Checked:** `data/round4/reports/M4D.md` §3, line by line: Lemma W1, Lemma W2, Lemma W3, Proposition W4, Corollary W5 with its interpretation, Theorem W6 and Remarks 1–3. Also the rows of §0 and §6 that concern them, and headline item 2.
- **Definitions and proofs re-read:**
  - `data/round3/reports/R3M.md` §1–§5: (F1), (F2), Lemma 1, Lemma 2, Prop A, Cor A′, Prop B, Lemma C1, Prop C2, the setting of Theorem C3, and Theorem C3;
  - `data/round3/checks/R3M.md` (the round-3 check of Theorem C3);
  - note.md §11.3 (Props 11.10–11.14).
- **M4D's code, read only:** `code/round4/M4D/weighted_twowin_check.py` and `cw5_check.py`, with their logs. My code shares nothing with them.
- **Checker code** (new, written for this check), in `code/round4/verify_M4D_logic/`:
  - library `wlib.py`;
  - tests `w1_abstract.py`, `w2_concrete.py`, `w3_chain.py`, `w4_cw5_adv.py`;
  - the logged batches `wbatch.sh` and `wbatch2.sh`, run through the existing `runlog.sh`.
  - The Part I files (`vF.py`, `t*.py`, `batch.sh`) are untouched.
- **Logs:** `data/round4/verify_M4D_logic/w1_abstract.log`, `w2_concrete.log`, `w3_chain.log`, `w4_cw5_adv.log`. Every run starts with its command line and start time and ends with its exit code and wall time.

## Headline

__HEADLINE__

## 1. What exactly is claimed, and what I checked it against

Setting (M4D §3 = R3M §2–§5): $p$ odd, slope $0$, a cylinder $C=x+p^m\mathbb Z_p$ with $m=V_n(x)$, points $x'=x_0+p^mw$. Here $M_n$ denotes the **maximal valuation** $\max_{i\le n}v(x+i)$. M4D reuses the same letters $M_n,M_N,M_{N'}$ for the weighted functionals (fix F3). Below I write $\mathcal M_n,\mathcal M_N,\mathcal M_{N'}$ for those.

A *weight* is a probability vector $q$ on $\{0,1\}^H$, and
$$\mu^q_k(r)=\sum_{f:Q_f(x)\equiv r\,(p^k)}q(f),\qquad\hat\mu^q_k(\zeta)=\sum_f q(f)e(-\zeta Q_f(x)/p^k),\qquad\chi^2_q=p^D\mathrm{Coll}_D(\mu^q)-1 .$$
The one-line claim under check bundles six statements. The table records each one's status after the check.

| item | M4D label | verdict | tests (this check) |
|---|---|---|---|
| W1 weighted window identity (slope 0) | proved | **confirmed**; it is the slope-0 case only (fix F1) | __T_W1__ |
| W2 weighted variance identity and bound | proved | **confirmed** (identity and bound) | __T_W2__ |
| W3 weighted fresh-randomness lemma | proved | **confirmed** | __T_W3__ |
| W4 weighted two-window inequality, adapted ($\tilde\varepsilon^{\,q}$) and sharp ($\varepsilon^{q,q'}$) forms | proved | **confirmed**; notation clash (fix F3) | __T_W4__ |
| W5 (a) $\tilde\varepsilon^{\,q}\ge m(W;D')$, (b) equality at $q^*$, (c) zero variance under a complete coset | proved | **confirmed**; the minimum is over $q$ of $\tilde\varepsilon^{\,q}$ only (fix F2) | __T_W5__ |
| W6 weighted conditional positive measure | proved, hypothesis unproved | **confirmed as a conditional theorem**; full proof written out in §2.6 (fix F5) | __T_W6__ |
| Remark 1 (W6 contains Thm 11.14) | — | **confirmed** (predictable uniform weights, sharp form; $\mathcal M_\ell=2^{n_j}c_{n_\ell}Z^0_{n_\ell}$) | `w3_chain` schedule U |
| Remark 2 ($q^*$ schedule) | — | **correct after fix F4** (measurability needs the full regime event $B_{\ell+1}$ and a default off it) | `w3_chain` schedule S (MEAS) |

## 2. Line-by-line re-derivation

Throughout, $x$ is not a negative integer (a null set), $e(t)=\exp(2\pi it)$, and Fourier inversion on $\mathbb Z/p^k$ reads $\mu(r)=p^{-k}\sum_\xi\hat\mu(\xi)e(r\xi/p^k)$.

### 2.1 Lemma W1

*Hypotheses:* (W2′) $D\le m-M_n$ and (W3′) $M_N<m$; parent weights $w\ge0$ on $P^0_n(x)$; $q$ fixed on $C$.

*(a)* This is R3M Prop A(i) with $L=0$. (W1) is void, (W2) is (W2′) and (W3) is (W3′).
- Children of slope-0 parents have slope 0.
- A slope-0 path alive at $N$ restricts to a slope-0 path alive at $n$: the restriction is alive by backward integrality, and has slope 0 because $v(\pi_j'(x'))\ge m-M_N>0$ for $j\ge n$.
- $P^0_n(x')=P^0_n(x)$ by Lemma 2(a).

**Correct.**

*(b)* By Lemma 2(b) with (W2′), $\tau_n(e,x')\equiv\tau^0_e-\beta_ew\pmod{p^D}$. By Lemma 2(a), $Q_f(x')\equiv Q_f(x)\pmod{p^D}$ (since $D\le m$). By (F2) at $x'$, $(e,f)$ is alive iff $Q_f(x)\equiv\tau^0_e-\beta_ew\pmod{p^D}$. For fixed $(e,f)$ this is one residue class of $w\bmod p^D$ ($\beta_e$ a unit), which has probability $p^{-D}$. Summing, $\mathbb E_CZ=p^{-D}\sum_ew(e)\sum_fq(f)=p^{-D}\sum_ew(e)$, using $\sum_fq(f)=1$. Also $V_N=m+D$ on $C$. **Correct.**

*Scope.* W1 reweights only the case $L=0$ of R3M Prop A / Cor A′ (note Prop 11.10). Prop 11.10 proper has slopes $\le L$ and frozen weights $\rho=p^\lambda a^{(\lambda)}$, and that case is not reweighted in M4D. The one-line claim's "Props 11.10, 11.11, 11.13 hold for arbitrary adapted weights" therefore overstates (fix F1).

A weighted slope-$\le L$ identity looks plausible. Replacing $a^{(\lambda)}_n$ by $\mu^{q_n}_\lambda$ seems to make the computation of Prop A(iii) go through, but I did not prove it. It is not needed for W6.

### 2.2 Lemma W2

By (b) of W1, the weighted child mass of $e$ is $\mu^q_D(\tau^0_e-\beta_ew)=\mu^q_D(\beta_e(\varphi_e-w))$, so $Z(w)=\sum_ew(e)\mu^q_D(\beta_e(\varphi_e-w))$. Apply Fourier inversion and substitute $\eta=\beta_e\xi$ (a bijection of $\mathbb Z/p^D$ for each $e$):
$$Z=p^{-D}\sum_\eta e(-\eta w/p^D)A(\eta),\qquad A(\eta)=\sum_ew(e)\,\hat\mu^q_D(\eta\beta_e^{-1})\,e(\eta\varphi_e/p^D).$$
Parseval over $w\bmod p^D$ gives $\mathbb E|Z|^2=p^{-2D}\sum_\eta|A(\eta)|^2$, and $A(0)=\sum_ew(e)$ because $\hat\mu^q_D(0)=1$. So the $\eta=0$ term is $(\mathbb EZ)^2$ and $\operatorname{Var}_C(p^{m+D}Z)=p^{2m}\sum_{\eta\ne0}|A(\eta)|^2$.

For the bound, use the weighted Cauchy–Schwarz inequality $|\sum_ew(e)a_e|^2\le(\sum_ew(e))\sum_ew(e)|a_e|^2$, which needs $w\ge0$. For each $e$, the map $\eta\mapsto\eta\beta_e^{-1}$ permutes the nonzero residues. Hence $\sum_{\eta\ne0}|A(\eta)|^2\le(\sum w)^2\chi^2_q$. **Correct.** I tested the identity itself, not only the bound, in floating point against the exact variance (§3).

### 2.3 Lemma W3

*Hypotheses:* (5.1) $D+k\le m-M_N$ and $M_N<m$. These give:
- $D+k\le m-M_n$, so Lemma 2(b) holds modulo $p^{D+k}$;
- $D+k\le m$, so $q_f:=Q_f\bmod p^{D+k}$ is constant on $C$;
- $k\le m-M_N$, so $u\bmod p^k$ is constant on $C$.

Each child contributes $q(f)\,e(\xi u^{-1}(t_e-q_f)/p^{D+k})$ when $t_e\equiv q_f\pmod{p^D}$, where $t_e=\tau^0_e-\beta_ew\bmod p^{D+k}$. So $\Psi=\sum_ew(e)G(t_e)$ with $G=g*m^q$ and $g(r)=\mathbf 1[p^D\mid r]e(\xi u^{-1}r/p^{D+k})$. The quotient $(t_e-q_f)/p^D\bmod p^k$ is well defined by $t_e-q_f\bmod p^{D+k}$, and $u^{-1}$ enters only modulo $p^k$.

I recomputed both transforms: $\hat g(\zeta)=p^k\mathbf 1[\zeta\equiv\xi u^{-1}\,(p^k)]$ and $\widehat{m^q}=\hat\mu^q_{D+k}$.
- (a) $t_e$ is uniform on $\mathbb Z/p^{D+k}$, so $\mathbb E\,G(t_e)=p^{-(D+k)}\hat g(0)\widehat{m^q}(0)=0$ for $\xi\not\equiv0$.
- (b) Weighted Cauchy–Schwarz, then $\mathbb E|G(t_e)|^2=p^{-2(D+k)}\sum_\zeta|\hat g|^2|\hat\mu^q_{D+k}|^2=p^{-2D}F^q(\xi)$. Then multiply by $p^{2V_N}=p^{2(m+D)}$.

**Correct.** M4D's tests do not exercise W3 directly, only through W4. Mine do (§3).

### 2.4 Proposition W4

*Hypotheses:* (5.2) $D+D'\le m-M_{N'}$ and $M_{N'}<m$; $w\ge0$; $q$ fixed on $C$; $q'$ constant on each $C'=x'+p^{m+D}\mathbb Z_p$.

- **Step 0.** On $C'$, (W2′) for $W'$ is $D'\le(m+D)-M_N$, which holds since $D'\le m-M_{N'}$. (W3′) is $M_{N'}<m+D$. Also (5.1) holds for $W$ with $k=D'$, since $M_N\le M_{N'}$. **OK.**
- **Step 1.** On $C'$ the parent set $P^0_N(x')$ and the parent weights $w(e)q(f)$ are constant: aliveness at $N$ depends on $x'\bmod p^{m+D}$, and slope on $x'\bmod p$. So W1 and W2 apply to $W'$ with weight $q'(C')$, giving $\mathbb E_{C'}\mathcal M_{N'}=\mathcal M_N(C')$. **OK.**
- **Step 2.** In class $b$, all $\beta_{e'}\equiv b\pmod{p^{D'}}$, so
$$X_b=p^{V_N}\sum_{\xi\ne0}\hat\mu^{q'}(\xi)\Psi_b(\xi)e(-b\xi w''/p^{D'}).$$
  Since $\xi\mapsto b\xi$ is a bijection, Parseval gives $\mathbb E_{w''}|X_b|^2=p^{2V_N}\sum_{\xi\ne0}|\hat\mu^{q'}(\xi)|^2|\Psi_b(\xi)|^2$.
  - The index set of classes, $(\mathbb Z/p^{D'})^\times$, does not depend on $x'$. So $\sum_bX_b$ is a fixed finite sum of functions on $C$, and Minkowski in $L^2(C)$ applies.
  - Moving the base point inside $C'$ multiplies $\Psi_b$ by $e(-\xi bs/p^{D'})$, by Lemma 2(b) at time $N$, which needs $D'\le m+D-M_N$. **OK.**
- **Step 3.** $\beta_{(e,f)}\equiv\beta_eu^{-1}\pmod{p^{D'}}$, as in R3M: $v(\pi_j'(x'))\ge m-M_N\ge D'$, and $\pi_N(x')/p^{m+D}\equiv\omega u\pmod{p^{D'}}$. So the class-$b$ members are the alive children of $P_{bu}$, and W3(b) with $k=D'$ applies. Dropping $|\hat\mu^{q'}|^2\le1$ gives $\tilde\varepsilon^{\,q}$. Keeping it, which needs $q'$ constant on $C$, gives $\varepsilon^{q,q'}$. **OK.**
- **Step 4.** The $P_{bu}$ partition $P^0_n(x)$ (each $\beta_e$ is a unit), so $\sum_bW(P_{bu})=\sum_ew(e)$. **OK.**
- **Identifications.**
  - $\sum_{\xi\ne0}F^q(\xi)=\sum_{\zeta\not\equiv0\,(p^{D'})}|\hat\mu^q_{D+D'}(\zeta)|^2$. Moreover $\hat\mu^q_{D+D'}(p^{D'}\zeta')=\hat\mu^q_D(\zeta')$, which gives $\tilde\varepsilon^{\,q}=p^{D+D'}\mathrm{Coll}_{D+D'}-p^D\mathrm{Coll}_D$.
  - For $\nu$: $\hat\nu(\zeta)=\hat\mu^q_{D+D'}(\zeta)\hat\mu^{q'}_{D'}(\zeta u)$, and $\nu\bmod p^D=\mu^q_D$.

  **Correct.**
- **Edge cases.** For $D'=0$ there is one class, $\tilde\varepsilon=0$ and $\mathcal M_{N'}=\mathcal M_N$. For $D=0$ the statement reduces to the one-window case. Both were tested.

**Notation (fix F3).** In the statement of W4, $M_{N'}$ in (5.2) is the maximal valuation, but the same symbol in the conclusion is the weighted functional. R3M avoided this by writing $c_nZ^0_n$. A reader can disambiguate, but in a statement that is meant to be quoted this should be repaired.

### 2.5 Corollary W5

- **(a)** Write $\mu^q_{D+D'}(s)=\mu^q_D(r)\mu(s\mid r)$. Then
$$\tilde\varepsilon^{\,q}=\sum_rp^D\mu^q_D(r)^2\Big(p^{D'}\sum_{s\equiv r}\mu(s\mid r)^2-1\Big).$$
  - $\mu(\cdot\mid r)$ lives on $\mathrm{Lift}(r)$ because every $Q_f\bmod p^{D+D'}$ lies in $\Sigma$. So Cauchy–Schwarz bounds the bracket below by $a_r$.
  - Then $1=(\sum_{r\in\mathrm{supp}}\nu_ra_r^{1/2}a_r^{-1/2})^2\le(\sum\nu_r^2a_r)(\sum_ra_r^{-1})$ when all $a_r>0$. The sum must be taken over the support, where $a_r<\infty$; M4D writes it over all $r$, which is harmless.
  - If some $a_r=0$, then $m=0$. Otherwise $\sum_ra_r^{-1}$ is a finite positive sum, so $m>0$. Hence **$m=0$ iff some class is complete**.

  **Correct.**
- **(b)** Take $q^*$ uniform on $\mathrm{Lift}(r)$ given the class, with class masses $\nu_r\propto a_r^{-1}$ (uniform on the complete classes if any exist). Both Cauchy–Schwarz steps are then equalities. $q^*$ is a probability vector because every $s\in\mathrm{Lift}(r)$ has at least one representing $f$. **Correct.**
- **Independent certificate.** $\tilde\varepsilon^{\,q}=q^TQq$ with $Q_{ff'}=p^{K}[s_f\equiv s_{f'}\,(p^K)]-p^D[s_f\equiv s_{f'}\,(p^D)]$. On each class, $Q$ is $p^D(p^{D'}I-J)$ in the lift-aggregated coordinates, so $Q\succeq0$ and $\tilde\varepsilon$ is convex on the simplex. At $q^*$ the gradient is $(Qq^*)_f=p^D\nu_ra_r=m$ on the support, and $\ge m$ off it ($=0=m$ in the complete case). These are the KKT conditions, so $q^*$ is a **global** minimiser and $\min_q\tilde\varepsilon^{\,q}=m$. Checked exactly (§3).
- **(c)** $F^{q^*}\ge0$ and $\sum_{\xi\ne0}F^{q^*}=0$, so $F^{q^*}(\xi)=0$ for all $\xi\ne0$.
  - Then W3(b) gives $\Psi_b\equiv0$, hence $X_b\equiv0$, hence $\operatorname{Var}_{C'}=0$ for every $C'$, for **any** admissible $q'$.
  - $X_b$ is locally constant, so it vanishes everywhere, not only almost everywhere.
  - This requires (5.2), which M4D states ("in Proposition W4").

  **Correct.**

**Scope of "the minimum over weights of the fine-scale mass" (fix F2).** W5 minimises the $q'$-free mass $\tilde\varepsilon^{\,q}$ over $q$. Theorem W6 in its predictable form uses the sharp mass $\varepsilon^{q,q'}$, which is also minimised over $q'$. Its infimum over $(q,q')$ can be strictly below $m(W;D')$:
- Suppose $W'$ covers $\mathbb Z/p^{D'}$, and let $q'$ be uniform over the residues mod $p^{D'}$.
- Then $\hat\mu^{q'}(\xi)=0$ for $\xi\ne0$, so $\varepsilon^{q,q'}=0$ whatever $m(W;D')$ is.
- In the language of W2, $\chi^2_{q'}=0$: every parent's weighted child mass is exactly $p^{-D'}$. This is the weighted shadow of Tao's block lemma.
- Such a $q'$ is predictable, because the cover of $W_\ell$ modulo $p^{D_\ell}$ is $\mathcal G_{\ell-1}$-measurable on the regime event.

`w4_cw5_adv.py` finds this situation in real window pairs (§3). This **does not contradict** W5, whose statement (a) is explicitly about $\tilde\varepsilon^{\,q}$. It does make the one-line claim, and headline item 2's "the minimum over weights of the fine-scale mass equals …", imprecise. It also strengthens rather than weakens M4D's "FE may be replaced by its infimum over weight schedules": that infimum can be smaller than any schedule of $m$'s.

**"Exact balance" (wording).** W5(c) is a statement about the $q^*$-weighted functional. Under $q^*$, children whose target class modulo $p^D$ is incomplete get weight $0$. So the zero variance concerns the followed sub-population, not the population. The unweighted population is not balanced: in every tested case with $m=0$, uniform weights give a non-constant $\mathcal M_{N'}$ on some $C'$ (controls in §3). M4D's §3(c) and its Interpretation say this correctly ("weighted children"). The one-line claim ("the next window's conditional variance is identically zero") should say "of the $q^*$-weighted functional".

### 2.6 Theorem W6: the full proof, checked step by step

M4D proves W6 as "R3M's proof of Theorem C3, line by line, with the following substitutions". I wrote the substituted proof out in full. Every step holds; the two places where M4D's sketch needs a sentence are marked.

**Setting.**
- Deterministic times $2p\le n_0<n_1<\cdots$, with $m_\ell=V_{n_\ell}$, $D_\ell=m_{\ell+1}-m_\ell$ and $W_\ell=[n_\ell,n_{\ell+1})$.
- $\mathcal G_\ell$ is generated by the cylinders $x+p^{m_\ell(x)}\mathbb Z_p$.
- $R_\ell:=\{D_{\ell-1}+D_\ell\le m_{\ell-1}-M_{n_{\ell+1}},\ M_{n_{\ell+1}}<m_{\ell-1}\}$ is the linear-regime part of R3M's $B_\ell$.
- $A$ is an admissible atom of $\mathcal G_j$.
- $q_\ell$ is a $\mathcal G_\ell$-measurable map from $x$ to probability vectors on $\{0,1\}^{H_\ell}$.

**(i) Filtration.**
- For $n\ge2p$, among $x+1,\dots,x+n$ at least two are divisible by $p$, so $V_n\ge M_n+1$.
- Hence $v(x'+i)=v(x+i)$ for $i\le n_\ell$ and $x'\in x+p^{m_\ell(x)}\mathbb Z_p$. So $m_\ell$ is constant on its own cylinder, the cylinders partition $\mathbb Z_p$ (minus a null set), and $\mathcal G_\ell$ refines $\mathcal G_k$ for $k\le\ell$ (since $m_\ell\ge m_k$).

This is R3M's argument; the round-3 checker verified it.

**(ii) Measurability of the weighted functional.** *M4D's sketch does not state this; it is needed.*
- For $e=(e_j,f_j,\dots,f_{\ell-1})\in P^0_{n_\ell}(x)$, put $w_\ell(e;x)=\prod_{k=j}^{\ell-1}q_k(x)(f_k)$. Each factor is $\mathcal G_k\subseteq\mathcal G_{\ell-1}$-measurable by (i).
- $P^0_{n_\ell}(x)$ is constant on $\mathcal G_\ell$-atoms: aliveness depends on $x\bmod p^{m_\ell}$, and slope on $x\bmod p$.
- Hence $\mathcal M_\ell=p^{m_\ell}\sum_{e\in P^0_{n_\ell}}w_\ell(e)$ is $\mathcal G_\ell$-measurable. `w3_chain` checks this constancy directly (MEAS).

**(iii) Stopping time.**
- $R_\ell\in\mathcal G_{\ell-1}$: R3M's argument, re-checked numerically (MEAS B2).
- On $R_\ell$, $\tilde\varepsilon_\ell=\tilde\varepsilon^{\,q_{\ell-1}}(W_{\ell-1};D_\ell)$ depends on three things: $q_{\ell-1}$ ($\mathcal G_{\ell-1}$); the valuations up to $n_{\ell+1}$, which are determined there; and $x\bmod p^{D_{\ell-1}+D_\ell}$ with $D_{\ell-1}+D_\ell\le m_{\ell-1}$.
- So $\{\tau>\ell\}=\bigcap_{j<k\le\ell}(R_k\cap\{\tilde\varepsilon_k\le\bar\varepsilon_k\})\in\mathcal G_{\ell-1}$, i.e. $\tau$ is a predictable stopping time. M4D says this.

In the predictable variant, $\varepsilon^{q_{\ell-1},q_\ell}$ also depends on $q_\ell$, on the sums of $W_\ell$ modulo $p^{D_\ell}$ ($D_\ell\le m_{\ell-1}$) and on $u\bmod p^{D_\ell}$. The unit $u$ is determined modulo $p^{m_{\ell-1}-M_{n_\ell}}$, and $D_\ell\le m_{\ell-1}-M_{n_\ell}$. So this variant needs $q_\ell\in\mathcal G_{\ell-1}$, exactly as M4D says.

**(iv) Martingale.** Fix $\ell\ge j$ and a $\mathcal G_\ell$-atom $C\subseteq A\cap\{\tau>\ell\}$.
- On $C$, $W_\ell$ satisfies (W2′) and (W3′): for $\ell=j$ by admissibility; for $\ell>j$ from $R_\ell$, since $D_\ell\le m_{\ell-1}-M_{n_{\ell+1}}-D_{\ell-1}\le m_\ell-M_{n_\ell}$ and $M_{n_{\ell+1}}<m_{\ell-1}\le m_\ell$.
- W1 with parent weights $w_\ell$ and window weight $q_\ell$ (both constant on $C$) gives $\mathbb E_C\mathcal M_{\ell+1}=\mathcal M_\ell(C)$, because $w_{\ell+1}((e,f))=w_\ell(e)q_\ell(f)$.
- On $\{\tau\le\ell\}\in\mathcal G_{\ell-1}$ the stopped process does not move.
- Hence $\tilde{\mathcal M}_\ell=\mathcal M_{\min(\ell,\tau)}$ is a $(\mathcal G_\ell)$-martingale on $(A,\mu_A)$, and it is nonnegative.

**(v) Second moments.**
- First window: $\mathbb E_A\tilde{\mathcal M}_{j+1}^2\le\mathcal M_j(A)^2(1+\chi^2_{q_j}(A))$ by W2, with $\mathcal M_j(A)=p^{m_j}|P^0_{n_j}|>0$ by admissibility and $w_j\equiv1$.
- Later windows: for $\ell>j$, take a $\mathcal G_{\ell-1}$-atom $C\subseteq\{\tau>\ell\}$. Apply W4 with $m=m_{\ell-1}$, $w=w_{\ell-1}$, $q=q_{\ell-1}$ and $q'=q_\ell$. Here (5.2) is $R_\ell$, and the sub-cylinders $C'$ are exactly the $\mathcal G_\ell$-atoms in $C$, because $m_\ell=m_{\ell-1}+D_{\ell-1}$ is constant on $C$. W4's three functionals are $\mathcal M_{\ell-1},\mathcal M_\ell,\mathcal M_{\ell+1}$. So
$$\mathbb E_C[\mathcal M_{\ell+1}^2-\mathcal M_\ell^2]\le\tilde\varepsilon_\ell\,\mathcal M_{\ell-1}(C)^2\le\bar\varepsilon_\ell\,\mathcal M_{\ell-1}(C)^2.$$
- Summing over atoms, with $\tilde{\mathcal M}=\mathcal M$ on $\{\tau>\ell\}$ and no increment elsewhere: $a_{\ell+1}-a_\ell\le\bar\varepsilon_\ell a_{\ell-1}$, where $a_\ell=\mathbb E_A\tilde{\mathcal M}_\ell^2$.
- $a_\ell$ is nondecreasing (conditional Jensen), so $a_\ell\le\mathcal M_j(A)^2\Pi_A$.

**(vi) Limit.** Doob's $L^2$ convergence theorem: $\tilde{\mathcal M}_\ell\to\tilde{\mathcal M}_\infty$ almost surely and in $L^2$, with $\mathbb E_A\tilde{\mathcal M}_\infty=\mathcal M_j(A)$ and $\mathbb E_A\tilde{\mathcal M}_\infty^2\le\mathcal M_j(A)^2\Pi_A$.

**(vii) Survival implies $x\in K_p$.** *M4D's one-line justification is correct, but this is the argument it needs.*
- Let $Y=\mathbf 1_{\{\tau=\infty\}}\tilde{\mathcal M}_\infty$. If $Y(x)>0$, then $\mathcal M_\ell(x)\to Y(x)>0$, so $\mathcal M_\ell(x)>0$ for all large $\ell$.
- So $P^0_{n_\ell}(x)\ne\emptyset$ for all large $\ell$.
- By the converse in (F2), a prefix of an alive path is alive. With $n_\ell\to\infty$, some path is alive at every $n$, and (F1) gives $x\in K_p$.

This uses neither $\tau=\infty$ nor the weights beyond positivity. So $\{Y>0\}\subseteq K_p\cap A$ up to a null set.

**(viii) Paley–Zygmund.**
- $\mathbb E_AY=\mathcal M_j-\mathbb E_A[\tilde{\mathcal M}_\infty\mathbf 1_{\tau<\infty}]\ge\mathcal M_j(1-\sqrt{\Pi_A\delta_A})$, by Cauchy–Schwarz and $\tilde{\mathcal M}_\infty\ge0$.
- $\mathbb E_AY^2\le\mathcal M_j^2\Pi_A$.
- Then $\mu_A(Y>0)\ge(\mathbb EY)^2/\mathbb EY^2$ when $\delta_A<1/\Pi_A$, and $\mathcal M_j$ cancels.

The constant is $(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$, as stated. **Correct.**

**Remark 1.** Uniform $q_\ell$ are predictable, and then:
- $\varepsilon^{q,q'}=\varepsilon(W,W')$ and $\chi^2_q=\chi^2_W$;
- $\tau$ is R3M's $\tau_j$;
- $\mathcal M_\ell=2^{n_j}c_{n_\ell}Z^0_{n_\ell}$, a constant multiple, so the bound is unchanged.

So W6 (predictable form) contains Theorem 11.14 exactly. The adapted form with uniform weights uses $\tilde\varepsilon\ge\varepsilon$ and is weaker; M4D's wording "for them $\varepsilon_\ell$ is R3M's $\varepsilon_\ell$" refers correctly to the predictable form.

**Remark 2 (fix F4).** M4D: "$q^*$ for $(W_\ell;D_{\ell+1})$ is $\mathcal G_\ell$-measurable on the regime event, since $D_\ell+D_{\ell+1}\le m_\ell$."
- The inequality alone does not make $D_{\ell+1}$ a function of the $\mathcal G_\ell$-atom. That also needs $M_{n_{\ell+2}}<m_\ell$, i.e. the event $R_{\ell+1}\in\mathcal G_\ell$.
- Off $R_{\ell+1}$, $q_\ell$ must be given some $\mathcal G_\ell$-measurable value (for instance uniform).
- With $q_\ell:=q^*$ on $R_{\ell+1}$ and uniform off it, the schedule is adapted, and $\tilde\varepsilon_\ell=m(W_{\ell-1};D_\ell)$ on $R_\ell$.

`w3_chain` (schedule S) checks this measurability: $q^*_1$ recomputed at an independent representative of every $\mathcal G_1$-atom.

**Quantifiers and uniformity.**
- W6 is a statement about one atom $A$ and one schedule fixed in advance. $\Pi_A$ depends on $A$ through $\chi^2_{q_j}(A)$.
- Nothing is uniform in $p$, in the cylinder or in the slope, and nothing is claimed to be.
- The slope restriction to $0$ and the linear regime are kept from R3M (Remark 3 says so).
- No optional stopping theorem is used: only the stopped martingale and Doob's $L^2$ convergence.

## 3. Numerical tests

__TESTS__

## 4. Attempts to break the claim that did not succeed

1. **Parent-dependent window weights.** Could $q$ be allowed to depend on the parent? W1 survives, since each parent's weighted child mass still has mean $p^{-D}$. But W3 and W4 then involve a different $F^{q_e}$ per parent, and the bound $\tilde\varepsilon^{\,q}$ is not defined. M4D never allows this: $w_{\ell+1}((e,f))=w_\ell(e)q_\ell(f)$ with one $q_\ell$ per atom. No gap.
2. **Weights that see the fresh digits.** If $q_\ell$ depends on digits beyond $m_\ell$, the martingale breaks. My control NEGM/NEG1 confirms this numerically. M4D's "adapted" ($\mathcal G_\ell$-measurable) is exactly the right condition.
   - Under $q^*$-weights with $m=0$ the control does not break the mean, because of exact balance (w3_chain at $p=5,7$, schedule S). That is consistent, not a failure.
3. **The sharp form with adapted (non-predictable) $q'$.** W4's sharp form needs $q'$ constant on all of $C$; otherwise $\varepsilon^{q,q'}$ is not even defined. W6 uses the sharp form only under predictability, and $\{\varepsilon_\ell\le\bar\varepsilon_\ell\}\in\mathcal G_{\ell-1}$ needs exactly that. No gap.
4. **Zero-weight populations.** Under $q^*$ the functional may vanish where alive children exist. That makes the theorem's conclusion weaker, not wrong: (vii) uses only $\mathcal M>0\Rightarrow$ alive.
5. **Edge cases $D=0$, $D'=0$.** Both behave as stated (§2.4; tests in §3).

## 5. Required fixes

- **F1 (scope; one-line claim and headline item 2).** Replace "note Props 11.10, 11.11, 11.13 hold for arbitrary adapted weights" by "the slope-0 cases of note Props 11.10, 11.11 and 11.13 (R3M Cor A′ with $L=0$, Prop B(i)–(ii), Lemma C1, Prop C2) hold for arbitrary adapted weights". The frozen-weight slope-$\le L$ identity is not reweighted.
- **F2 (Cor W5 wording).** Say "the minimum over $q$ of the $q'$-free fine-scale mass $\tilde\varepsilon^{\,q}$ is $m(W;D')$". Add that in the predictable form of Theorem W6 the sharp mass $\varepsilon^{q,q'}$ can be smaller, and is $0$ whenever the next window covers its own jump (take $q'$ uniform over residues). So the infimum over weight schedules in W6 is not in general given by the $m$'s; it is at most that.
- **F3 (notation).** In Prop W4 and Theorem W6, rename the weighted functionals (e.g. $\mathcal M$), since $M_n,M_N,M_{N'}$ also denote maximal valuations in the same statements.
- **F4 (Remark 2).** "$\mathcal G_\ell$-measurable on the regime event $R_{\ell+1}=\{D_\ell+D_{\ell+1}\le m_\ell-M_{n_{\ell+2}},\ M_{n_{\ell+2}}<m_\ell\}$, extended by uniform weights off it." The inequality $D_\ell+D_{\ell+1}\le m_\ell$ alone does not determine $D_{\ell+1}$ from the atom.
- **F5 (proof of W6).** Write the substituted proof out; §2.6 above can be used. In particular, state the $\mathcal G_\ell$-measurability of $w_\ell$ and $\mathcal M_\ell$ (step (ii)) and the survival step (vii).
- **F6 (one-line claim, W5(c)).** Specify "the conditional variance of the $q^*$-weighted functional". The unweighted population is not balanced.
- *Optional.* The docstrings of M4D's `weighted_twowin_check.py` and `cw5_check.py` use an older numbering (W3 for the two-window inequality, W4 for the zero-variance corollary). The report's §6 row should say that W2 was tested only as a bound and W3 only through W4. The present check closes both.

None of these changes a proof. They concern how the result is quoted.

## 6. What remains open

- **The weighted FE hypothesis is unproved** for every weight schedule, at every prime. Theorem W6 is a conditional theorem and proves nothing about $\mu(K_p)$ by itself.
- No result here gives $\mu(K_p)>0$ for any $p$.
- The open sub-problems of the brief, (S) and the deep-gate truncation, are untouched by the reweighting. Prop 11.15(b) (infinite annealed mean) applies to $\mathbb E[\tilde\varepsilon_\ell]$ for uniform weights. Whether some schedule (e.g. $q^*$) has a finite annealed mean was not examined by M4D or here.

## 7. Computational record

__RECORD__

## 8. Credit

- **Reweighted machinery:** track R3M (round 3): Lemma 2, Prop A / Cor A′, Prop B, Lemma C1, Prop C2, Theorem C3. The round-3 check of R3M (`data/round3/checks/R3M.md`) verified the unweighted versions, including the filtration and stopping-time arguments reused in §2.6.
- **Weights, Corollary W5 and Theorem W6:** track M4D (round 4).
- **Fullness condition** (complete coset): track R2b (round 2), note Theorem 10.12.
- **Template of the quenched martingale:** track R1b (round 2, $p=2$). Not used here directly.
- **Classical:** Cauchy–Schwarz, Minkowski, Parseval, Doob's $L^2$ martingale convergence, the Paley–Zygmund inequality, and KKT conditions for convex quadratic programs.

*This report was produced in an AI-assisted session (round 4, track verify_M4D_logic). It has not been checked by a human.*
