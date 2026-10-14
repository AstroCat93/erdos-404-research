# Logic checks of round-4 track M4A (Theorem M and Corollary M′)

This file has two parts, both made by the `verify_M4A_logic` track of round 4:

- **Part I** checks Theorem M, $\mu(K_7)>0$. Verdict: confirmed-with-fixes, (F1)–(F3).
- **Part II** checks Corollary M′, $\mu(K_p)>0$ for $p=11,13,17,19,23$. Verdict: **confirmed-with-fixes**. The conclusion holds. Three of the five stated lower bounds ($p=11,13,23$) are rounded up and must be rounded down, to $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$ and $2.06\cdot10^{-1}$. See Part II §II.0 and §II.7.

# Part I. Logic check of Theorem M ($\mu(K_7)>0$)

Date: 2026-10-14. Lens: LOGIC. Made by the `verify_M4A_logic` track of round 4.

- **Checked:** `data/round4/reports/M4A.md` §§1–7, i.e. Lemma H, Theorem 1, Lemma F, Lemma Q, Props D/E/E′ and Theorem M. I also read `code/round4/M4A/` (`bounds.py`, `fe_lib.py`, `fe_verify.py`) and the log `data/round4/M4A/fe_verify_final.log`.
- **Foundations re-read:** `data/round3/reports/R3M.md` §§1–5 (Lemma 1, Lemma 2, Prop A, Cor A′, Prop B, Prop C2, Theorem C3, Lemma C4), the round-3 check `data/round3/checks/R3M.md`, and note.md §1.2 and §11.3.
- **Checker code** (new; it shares no code with `code/round4/M4A/`): `code/round4/verify_M4A_logic/`:
  - `vl_lib.py`, `test_small.py`, `q2d_test.py`, `eprime_test.py` and `fe_indep.py`;
  - `batch_small.sh` and `runlog.sh`.
- **Logs:** `data/round4/verify_M4A_logic/`: `lemmaQ.log`, `lemmaQ_2D.log`, `thm1_propDE.log`, `eprime.log` and `fe_indep.log`. Each run starts with `=== command:` and ends with `=== exit:`.
- **Budget:** about 2 core-minutes in total, at `nice -n 10`.

**The claim checked.** Let $p=7$, $n_0=300$, $n_{\ell+1}=\lceil27n_\ell/20\rceil$, $x_A=8482778585152010705975786324668215228635086$ and $A=x_A+7^{51}\mathbb Z_7$ (so $V_{300}(x_A)=51$).
- $A$ is an admissible atom; an explicit slope-0 path is re-verified by exact integer evaluation.
- FE of R3M Theorem C3 holds, with $\Pi_A\le10^{25.7344}$, $\delta_A\le1.0006\cdot10^{-45}$ and $\Pi_A\delta_A\le10^{-19.265}$.
- Hence $\mu(K_7\cap A)/\mu(A)\ge1.843\cdot10^{-26}$, and so $\mu(K_7)\ge1.843\cdot10^{-26}\cdot7^{-51}>0$.
- Status claimed: [computer-assisted].

## Headline

**Verdict: confirmed-with-fixes.** The claim holds, and so does its label [computer-assisted].

I went through every step that Theorem M depends on, line by line:
- R3M Theorem C3 as used;
- Lemma H and Theorem 1;
- Lemma F;
- Lemma Q, Steps 0–4, including the mod-$p^2$ analyticity argument;
- Props D, E and E′;
- the five phases of Theorem M.

Every hypothesis is stated and satisfied where it is used. The quantifier order is right: the thresholds $\bar\varepsilon_\ell$ depend only on the fixed atom. The filtration, stopping-time, Markov, union-bound and Paley–Zygmund steps are valid, as is the step "survival implies $x\in K_7$".

I recomputed every explicit constant with independent code, which reads only $x_A$ and the path from the atom file. All of them reproduce:
- $\chi_0^2\le0.50464$ and the eight phase-1 thresholds;
- $\log_{10}\Pi_A=25.73437$, $\delta_A=1.00052\cdot10^{-45}$ and $\log_{10}(\Pi_A\delta_A)=-19.2654$;
- the lower bound $1.84344\cdot10^{-26}$.

I also re-derived the phase-4 tail argument in my own form, and it passes.

The fixes are to the write-up. None changes a number or a conclusion.
- **(F1)** M4A §1 cites R3M Lemma 1(c) as $V_j-V_n\ge v((j-n)!)$. R3M proves only $V_j-V_n\ge\lfloor(j-n)/p\rfloor$. The stronger form is true and is used in phase 4. It needs its one-line proof, given in §4.
- **(F2)** The proof of Prop E′ omits several one-line justifications. All of them hold; §2.5 writes them out.
- **(F3)** Minor wording, optional; see §4.

## 1. Dependency chain and how each hypothesis is met

| step | source | hypotheses | where met in Theorem M | my finding |
|---|---|---|---|---|
| (F1) survival $\Rightarrow K_p$ | R3M §1, note Prop 1.2 | an alive path at every $n$ | on $\{Y>0\}$: $Z^0_{n_\ell}\ge1$ for all $\ell$, then backward integrality (F2) | correct; $g_p=\sup_Bv(S_B)\ge V_n\ge v(n!)\to\infty$ |
| Thm C3 | R3M §5 (checked in round 3) | deterministic $2p\le n_0<n_1<\cdots$; admissible atom; deterministic $\bar\varepsilon_\ell\ge0$ with $\Pi<\infty$; FE | $n_0=300\ge14$; times fixed; atom checked; $\bar\varepsilon_\ell$ fixed numbers; FE computed | correct as used. $\chi_j^2$ enters only as an upper bound ($a_{j+1}\le M_j^2(1+\chi_j^2)$), so replacing it by the Prop D bound is legitimate |
| Lemma H | M4A §2 | $S\in\mathbb Z_p[X]$, $1\le k\le k'$, $\theta=\min(\lceil k/2\rceil,k-b+1)$ | $S=S_\delta\in\mathbb Z[X]$, $k=D$, $k'=K$ | correct (§2.2) |
| Thm 1 | M4A §2 | ball $B$ with $v(x+i)$ constant for $n<i\le N'$ | phases 2–3: $B=A$, $n_{\ell+1}<i_A$; phase 4: radius $7^{-(\sigma_\ell+1)}$ inside $G_\ell$ | correct; exact identity 152/152 |
| Lemma F | M4A §3 | Thm 1 setting and $M_W\le K-\theta$ | asserted for every window of phases 2–3 (re-checked); phase 4 from $D\ge2\sigma_\ell$ | correct; tested directly, 80/80 |
| Lemma Q | M4A §4 | $1\le k\le V_t(u)$, any integer $f$ | $k=K-a_c=V_{H-c}(x+n+c)$ | correct (§2.4); 9580 exact tests, 0 failures |
| Props D, E | M4A §5 | as above; Prop E replaces $M_{r+1}$ by $M_W\ge M_{r+1}$ | — | correct; 152/152 each |
| Prop E′ | M4A §5 | Prop E setting, $\sigma\ge M_W$, $\kappa>0$ | $\sigma=M_{n_{\ell+1}}$ (phase 3), $\sigma=$ an upper bound for $\sigma_\ell$ (phase 4); $\kappa=0.9117$ | correct, with the gaps of (F2) filled; $E'\ge E$ in 205/205 windows |
| Lemma 1(c), strong form | cited from R3M, but R3M has only the weak form | — | phase 4: $D\ge v((n_\ell-n)!)$ | **true, needs its own proof (F1)** |

## 2. The line-by-line audit

### 2.1 Theorem C3 as used (R3M §5)

I re-read the proof of C3 against how M4A uses it.

- **Filtration.** Since $n_\ell\ge2p$, there are at least two gates in $[1,n_\ell]$, so $M_{n_\ell}<m_\ell$. Hence $m_\ell$ is constant on its own cylinder. The cylinders form a partition, and it refines as $\ell$ grows ($m_{\ell+1}\ge m_\ell$). So $(\mathcal G_\ell)$ is a filtration.
- **Measurability.** $M_\ell=c_{n_\ell}Z^0_{n_\ell}$ is $\mathcal G_\ell$-measurable. Aliveness depends on $x\bmod p^{m_\ell}$, and slope 0 on $x\bmod p$.
- **The stopping time.** $B_\ell$ is $\mathcal G_{\ell-1}$-measurable. The event $\{M_{n_{\ell+1}}\ge m_{\ell-1}\}$ is a union of $\mathcal G_{\ell-1}$-atoms. On its complement, the linear-regime inequality and $\varepsilon_\ell$ depend only on $x\bmod p^{K}$ with $K\le m_{\ell-1}$. So $\{\tau>\ell\}\in\mathcal G_{\ell-1}$, i.e. $\tau-1$ is a stopping time.
- **Martingale.** $\tilde M_{\ell+1}-\tilde M_\ell=\mathbf 1_{\tau>\ell}(M_{\ell+1}-M_\ell)$. On $\{\tau>\ell\}$, $B_\ell$ gives (W2′) and (W3′) for $W_\ell$: $D_\ell\le2m_{\ell-1}-m_\ell-M_{n_{\ell+1}}\le m_\ell-M_{n_\ell}$ and $M_{n_{\ell+1}}<m_\ell$. Then Cor A′ applies.
- **Second moments.** $\tilde M^2_{\ell+1}-\tilde M^2_\ell=\mathbf 1_{\tau>\ell}(M^2_{\ell+1}-M^2_\ell)$. Prop C2 on each $\mathcal G_{\ell-1}$-atom in $\{\tau>\ell\}$ bounds it by $\varepsilon_\ell M_{\ell-1}^2\le\bar\varepsilon_\ell\tilde M_{\ell-1}^2$. The recursion $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}\le(1+\bar\varepsilon_\ell)a_\ell$ needs $a_{\ell-1}\le a_\ell$, which holds for a martingale. It gives $\sup a_\ell\le M_j^2\Pi_A$.
- **Limit and Paley–Zygmund.** $L^2$-boundedness gives a.s. and $L^2$ convergence. For $Y=\mathbf 1_{\tau=\infty}\tilde M_\infty$: $\mathbb EY\ge M_j(1-\sqrt{\Pi_A\delta_A})\ge0$ and $\mathbb EY^2\le M_j^2\Pi_A$. So $\mu_A(Y>0)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$, and squaring is monotone because $\Pi_A\delta_A<1$.
- **Survival.** Suppose $Y(x)>0$. Then $\tau(x)=\infty$ and $M_\ell(x)\to M_\infty(x)>0$, so $Z^0_{n_\ell}(x)\ge1$ for all large $\ell$. By (F2) a path is alive at every $n$. By (F1), $g_7(x)\ge V_n(x)\ge v(n!)\to\infty$ (note §1.2: $g_p=\sup_Bv_p(S_B)$). So $\{Y>0\}\subseteq K_7\cap A$ up to a null set.
- **The identity for $\varepsilon$.** The identification $\varepsilon(W,W')=p^K\mathrm{Coll}_K-p^D\mathrm{Coll}_D$ (R3M C2) holds at every $x$, because $\pi_N/\pi_n=p^Du$ exactly. So Theorem 1, which averages this collision form, averages exactly C3's $\varepsilon_\ell$.

C3 was confirmed in round 3. I found nothing to add, and M4A uses it exactly as stated.

### 2.2 Lemma H and Theorem 1

**Lemma H.** For $z\in\mathcal L$ we have $\lambda\le\theta-1\le\lceil k/2\rceil-1<k/2$, so $\rho=k-\lambda>\lambda$. Also $\lambda\le k-b$, so $\rho\ge b$ and $U_z\subseteq B$.

For $u,u'\in p^\rho\mathbb Z_p$, the Taylor remainder terms have valuation $\ge(i-1)\rho\ge\rho>\lambda$. This uses $S^{[i]}(z)\in\mathbb Z_p$. It gives (i), (ii) and (iii) exactly as written:
- (ii) shows that the balls $U_z$ partition $\mathcal L$;
- (iii) shows that $U_z$ maps cosets bijectively onto $p^k\mathbb Z_p/p^{k+j}$.

Degenerate cases cause no trouble:
- $\theta\le0$ gives $\mathcal L=\emptyset$;
- $S'\equiv0$ puts $z$ in $\mathcal H$;
- a constant $S_\delta=\pm1$ never satisfies $v(S)\ge k$.

**Theorem 1.** Fubini gives the result over $\delta$. The term $\delta=0$ has probability $2^{-H}$. For $\delta\ne0$, $S_\delta\in\mathbb Z[X]$ and Lemma H applies with $k=D$, $k'=K$. The sentence "both are constant on $B$" means that $D$ and $K$ are constant on $B$.

**The parameters in Theorem M.**
- Phases 2–3: $b=51$, $D\ge194$, so $\theta=\lceil D/2\rceil$.
- Phase 4: $b=\sigma_\ell+1$ and $D\ge2\sigma_\ell$, so $\lfloor D/2\rfloor\ge\sigma_\ell$ and $\theta=\lceil D/2\rceil$.

### 2.3 Lemma F

- The first nonzero index $c$ of $\delta$ has probability $2^{-c-1}$, and given it the later digits are still i.i.d. signed.
- $y_{c+t}=y_c\,\pi_t(x+n+c)$.
- On the value event, $v(y_c'T)\ge a_c-M_W+K-a_c\ge\theta$, so $v(S'_\delta)\ge\theta$ forces $v(T')\ge\theta-a_c$.
- Finally $K-a_c=V_{H-c}(x+n+c)$, which is Lemma Q's hypothesis $k\le V_t(u)$.

All correct.

### 2.4 Lemma Q (the new ingredient), Steps 0–4

**Step 0.**
- (a) For $c>g_r$ and $g_r<i\le c$: $V_c(u)\ge L_r+v(u+i)$, so each term of $R_r-R_r^{<g_r}$ has valuation $\ge L_r+1$.
- (b) $v(H_{g_r})\ge-M_r$.
- The events $E^T_r$ follow from $v(T-T_{<g_{r+1}})\ge L_{r+1}$.
- A 2D block $r$ has $L_{r+1}\le k-M_{r+1}<k$, so block $r+1$ is also in the product, and $E^R_{r+1}$ depends only on blocks $\le r$.

**Step 1.** The chain rule over independent blocks: each $A_r$ depends on blocks $\le r$, and the sup runs over histories in $A_0\cap\dots\cap A_{r-1}$. Dropping events only enlarges the probability.

**Step 2.** $u\equiv-g_1\pmod{p^{s_1}}$ gives $P(A_0)=P_0(g_1,\min(s_1,k))$ exactly.

**Step 3.**
- $\tau\in\mathbb Z_p$ because the history lies in $E^T_{r-1}$ and $L_r<k$.
- $\pi_{g+k'}(u)=\pi_g(u)\pi_{k'}(y)$.
- $d\le s_{r+1}$, so $\pi_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^d}$.
- The block digits $\tilde\delta_{g},\dots,\tilde\delta_{g+p-1}$ (with $g\ge1$) are i.i.d. signed and independent of the history.

Hence $P\le q_d/p^d$.

**Step 4.** I re-derived the decomposition of $R^{<g+p}_{r+1}$ term by term:
- $pH_{g+p}-pH_g=1/\alpha+pN$;
- $pH_{g+k'}-pH_{g+p}=-(1/\alpha+pE_{k'})$;
- $\alpha p=y+p$.

The terms $N$, $E_{k'}$ and $P_{k'}(y)$ are $p$-integral, because $y+i\equiv i-p\not\equiv0$ for $1\le i\le p-1$. So $\varrho\notin\mathbb Z_p$ makes the event impossible. Otherwise the event pins $\tilde Z\bmod p^2$ to one residue determined by the history.

The congruence $P_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^2}$ holds on $\{v(y+p)\ge1\}$, for three reasons:
- each $1/(y+i)$ expands in powers of $(y+p)$ with $p$-integral coefficients;
- $(y+p)^2$ has valuation $\ge2$;
- $P'_{k'}(-p)=-\pi_{k'}(-p)H_{p-1}\equiv0\pmod p$. I recomputed $\pi'_{k'}(-p)+\pi_{k'}(-p)E_{k'}(-p)$ to get this.

Hence $P(A_r\mid h)\le P(E^R_{r+1}\mid h)\le q_2/p^2$.

**Uniformity.** The bound is quenched: it holds for every $u$, with no averaging. That is why Prop E may take the sup over $x\in B$, which depends only on the gate pattern.

### 2.5 Props D, E, E′

**Prop D and Prop E.** I checked the translation of Lemma Q to absolute gate indices. For $u=x+n+c$, gate $r$ of $u$ is $G_{\beta(c)+r-1}$, with relative levels $\lambda-a_c$. The conditions $L_r<k$, the 1D exponent $d$ and the 2D condition $\lambda_{\beta'+1}\le\min(\theta,K-M_{r+1})$ are therefore independent of $c$, so one suffix product per gate suffices.

Prop E replaces $M_{r+1}$ by $M_W$. This only removes 2D blocks, and $q_2/p^2\le q_1/p$. `fe_lib.blocklevel` implements exactly this.

**Prop E′: the omitted justifications (F2).** All of the following hold, and the write-up should state them:

1. **$\tilde q_s$ is nondecreasing.** Each class mod $p^{s-1}$ splits into $p$ classes mod $p^s$, so $\max P_s\ge\max P_{s-1}/p$, i.e. $q_s\ge q_{s-1}$. Also $q_s\le\tilde q_s$, because $q_s\le pq_{s-1}$. So $\Delta_s\ge0$, and $\log q_d\le\log\tilde q_{s_{\rm end}}$ for $d\le s_{\rm end}$.
2. **$R\le K-\lambda_\beta$.** The exponents telescope: $\sum d=K-\lambda_\beta$, and each $d\ge1$. The only gate with $\lambda_\beta\ge K$ is the last one, where $\lambda_\beta=K$ and $R=0$. So the inequality also holds there.
3. **The 2D count.** "$\#2D\ge J(1-1/p)-1$" holds for the actual $J$. When the stated lower bound for $J$ is negative, the inequality $-\gamma\#2D\le-\gamma(\text{lower bound})$ still holds, because $\#2D\ge0$.
4. **The gates in the 2D count exist.** They lie inside the window: their levels are $\le f'<K$.
5. **The count of deep end gates.** The count $\#\{s_{\rm end}\ge s'\}\le R/p^{s'-1}+1$ is used only for $s'\le\sigma$. This yields the term $\log(\tilde q_\sigma/q_1)$.
6. **Monotonicity in $\sigma$, $K$ and $f'$.** The bound increases in $\sigma$ (for fixed $f'$) and in $K$ (for fixed $f'$; uses $\rho_1>0$), and decreases in $f'$. This justifies inserting an upper bound for $\sigma_\ell$ that need not be an integer, an upper bound for $K$, and the lower bound $f'\ge D/2$ in phase 4.

Tests: E′ dominates E in 197/197 random windows at $p=7,11$, half of them with a planted deep gate of depth 3–7 near the window start. It also dominates in all 8 actual phase-2 windows. The closest case is $\log_{10}(E/E')=-4.7$.

### 2.6 Theorem M, phase by phase

**Atom.** I verified these independently with exact integers:
- $V_{300}(x_A)=51$ and $M_{300}=4<51$, so $A$ is a $\mathcal G_0$-atom;
- the path has $e_0=1$, $v(S_e(x_A))=51$ and $v(S'_e(x_A))=0$ (with $S'\equiv6\bmod 7$);
- $D_0=17$ and $M_{405}=4$, so $17\le47$;
- $i_A=4.1065\cdot10^{42}$, and $\ell^*=307$ is the first window with $n_{\ell+1}\ge i_A$.

$Z^0_{300}$ is constant and positive on $A$, because $S_e$ and $S'_e$ are constant modulo $7^{51}$.

**Digit formula.** My version is $\#\{i\le N:p^s\mid x_A+i\}=\lfloor(x_A+N)/p^s\rfloor-\lfloor x_A/p^s\rfloor$. For $x\in A$ and $i<i_A$ we have $v(x+i)=v(x_A+i)\le50$, so $V_N$ and $M_N$ are exact and constant on $A$. This was cross-checked against direct valuations.

**Phase 0 and phase 1 (pointwise).** The thresholds $\bar\varepsilon_\ell$ are Prop D values computed from $A$'s fixed pattern. They are deterministic, so C3's quantifier order is respected. They bound $\varepsilon_\ell$ on all of $A$, because $p^D\mathrm{Coll}_D\ge1$. I re-checked the linear regime exactly for $\ell=1,\dots,8$. These windows contribute nothing to $\delta_A$.

**Phases 2–3 (Markov on $B=A$).**
- $\varepsilon_\ell\ge0$, and $\mathbb E_A$ is exactly the measure in FE.
- The linear regime is re-checked exactly for all 306 windows.
- Lemma F's $M_W\le K-\theta$ is asserted for every window.
- Phase 3 uses $\sigma=M_{n_{\ell+1}}\ge M_W$.
- The truncation of the $c$-sum in `fe_lib.py` is rigorous: each omitted term is $\le2^{-c-1}p^K$, because $P_0\cdot\mathrm{Suf}\le1$. My full-sum values for $\ell=14$–$16$ are smaller, as they should be.

**Phase 4 (all $\ell\ge307$).**

*The event $G'$.* For $i\in I_A$, $\mu_A(v(x+i)>m+2\log_7i+10)\le7^{-10}i^{-2}$, and summing over $I_A$ gives $\mu_A(G'^c)\le2.4668\cdot10^{-94}$. On $G'$, every gate up to $n_{\ell+1}$ has depth $<\sigma_\ell$, so $G'\subseteq G_\ell$. $G_\ell$ is a union of balls of radius $7^{-(\sigma_\ell+1)}$, and the pattern is constant on each of them.

*The union bound.* $\{\tau<\infty\}\subseteq\bigcup_{\ell\le306}\{\varepsilon_\ell>\bar\varepsilon_\ell\}\cup G'^c\cup\bigcup_{\ell\ge307}(\{\varepsilon_\ell>\bar\varepsilon_\ell\}\cap G_\ell)$. This uses that the linear regime holds on $G'$ for $\ell\ge307$.

*The tangent-line code.* I checked the tangent-line argument of `fe_verify.py`, including the direction of each inequality:
- the failure bound plus $c'n$ is concave, because every logarithm enters with a positive coefficient, and its slope at $n^*$ is bounded above;
- the side conditions ($D-2\sigma_\ell$ and $m_{\ell-1}-K-M$) are convex (linear minus concave), and their slopes at $n^*$ are bounded below.

*My own argument.* I wrote each bound as $-an+b\ln n+c$ and checked $g(n^*)>0$ and $g'(n^*)>0$ for the convex function $g$. It gives the same conclusion:
- $\ln\mathrm{fail}_\ell\le-0.015718\,n_{\ell-1}$ for every $\ell\ge307$;
- $D\ge2\sigma_\ell$ (margin $1.3\cdot10^{41}$);
- the linear regime holds (margin $6.8\cdot10^{40}$).

**Totals.** I recomputed every total independently (320-bit mpmath):

| quantity | M4A | mine |
|---|---|---|
| $\chi^2_0$ | ≤ 0.504642 | ≤ 0.504642 |
| $\bar\varepsilon_1,\dots,\bar\varepsilon_8$ | 1.637, 12.93, 98.64, 137.8, 336.3, 3835, 4.643e5, 4.956e7 | 1.63688, 12.9262, 98.6367, 137.821, 336.303, 3834.74, 464266, 4.95628e7 |
| $\log_{10}\mathbb E_A\varepsilon_9$ | ≤ −45.301 | −45.3008 |
| $\delta_A$ | ≤ 1.000520e-45 | 1.0005204e-45 |
| $\log_{10}\Pi_A$ | ≤ 25.7344 | 25.73437 |
| $\log_{10}(\Pi_A\delta_A)$ | ≤ −19.2654 | −19.265404 |
| $\mu(K_7\cap A)/\mu(A)$ | ≥ 1.8434e-26 | ≥ 1.84344e-26 |
| $\mu(K_7)$ | ≥ 1.4e-69 (report) | ≥ 1.4643e-69 |

Every stated constant of the claim is implied, including $\Pi_A\delta_A\le10^{-19.265}$ and the lower bound $\ge1.843\cdot10^{-26}$.

My evaluation is not interval arithmetic. It is an independent 320-bit re-evaluation; the M4A evaluation itself uses outward-rounded intervals. The margin in FE is 19 orders of magnitude.

### 2.7 Uniformity, quantifiers and measurability

- **In $p$.** No uniformity is claimed or used. The statement is for $p=7$ and one atom.
- **In the cylinder.**
  - Lemma Q is pointwise in $u$.
  - Prop D is pointwise in $x$, depending on the pattern only.
  - Theorem 1 is an identity on any ball with a constant pattern.
  - The only averages are $\mathbb E_A$ (phases 2–3) and $\mathbb E_B$ over balls inside $G_\ell$ (phase 4). Both are the measure that FE uses.
- **In the slope.** Only the slope-0 population is used, inside C3.
- **Thresholds.** They are fixed before the event $\{\tau<\infty\}$ is evaluated: they depend on $A$, never on $x$.
- **Measurability.** $\varepsilon_\ell$ is locally constant, and $G'$ is closed.
- **No hidden adaptivity.** Window times are deterministic, as C3 requires.

## 3. Numerical tests

All tests are exact (Python integers and Fractions; int64 counts below $4^{31}$) unless stated. The code is new and written from the statements in M4A.md.

| claim tested | program (mode) | runs | result | log |
|---|---|---|---|---|
| Lemma Q inequality, random $u$, planted first gate (incl. $g=2$, the double root), integer-like $u$, planted later deep gate | `test_small.py Q` | $p=3$ ($k\le8,f\le3$), $p=5$ ($k\le5,f\le2$), $p=7$ ($k\le4,f\le2$); 3000 each | **9000 tests, 0 violations**; max P/bound = 1.000000 (attained) | `lemmaQ.log` |
| control: 2D factor $q_2/p^3$ (this also changes 1D blocks with $d=2$) | `test_small.py Q … 1` | 1500 each | 195 violations; the tests are sensitive | `lemmaQ.log` |
| Lemma Q with many 2D blocks (long runs of depth-1 gates, large $f$) | `q2d_test.py` | $p=3$ ($k\le7,f\le5$), $p=5$, $p=7$ ($k\le4,f\le3$) | **580 tests, 0 violations**. At $p=7$ the max ratio is 0.87 with one 2D block and 0.78 with two, so the 2D factor is nearly tight | `lemmaQ_2D.log` |
| control for the 2D test | `q2d_test.py … 1` | $p=3,5$ | 31 violations out of 250 | `lemmaQ_2D.log` |
| Theorem 1 identity (exact equality), on balls $x_0+p^b\mathbb Z_p$ with constant pattern | `test_small.py T1` | $p=3$ ($b=3,4$), $p=5$ ($b=2$), $p=7$ ($b=2$); $\theta$ from $-2$ to $4$, 29+ cases with $\theta\ge2$ | **152/152 exact** | `thm1_propDE.log` |
| Prop D (pointwise $\varepsilon\le$ bound $-1$) | same | same | 152/152; max $(\varepsilon+1)$/bound = 0.959 | `thm1_propDE.log` |
| Prop E ($\mathbb E_B\varepsilon\le$ bound) | same | same | 152/152 | `thm1_propDE.log` |
| Lemma F + Q directly (high-slope mass $\le$ Prop E $-2^{-H}p^K$) | same (seeds 41–44) | 80 cases | 80/80 | `thm1_propDE.log` |
| Prop E′ ≥ Prop E | `eprime_test.py` (256-bit) | $p=7,11$, windows $n\in[60,4000]$, half with planted deep gates | 197/197, plus 8/8 actual phase-2 windows | `eprime.log`, `fe_indep.log` |
| constants $q_s$, $P_0$, $\rho_1$, $\gamma$, $\kappa$ at $p=7$ | `vl_lib.py` (enumeration) | — | all equal to M4A §4 and §5 | `fe_indep.log` |
| atom, digits, linear regime ($\ell\le306$), phases 0–4, totals | `fe_indep.py` (320-bit) | $p=7$ | reproduced (table in §2.6) | `fe_indep.log` |

## 4. Required fixes

**(F1) Lemma 1(c) is mis-cited.** M4A §1 lists "(c) $V_j-V_n\ge v((j-n)!)$" among the results proved in round 3. R3M Lemma 1(c) states only $V_j-V_n\ge\lfloor(j-n)/p\rfloor$.

The strong form is used in phase 4: $D\ge v((n_\ell-n)!)$ in the text, and `Dm` in `fe_verify.py`. It is true. Proof: $V_j-V_n=v(\pi_{j-n}(x+n))$, and the Legendre count in the proof of R3M Lemma 1(a) applies to any $j-n$ consecutive elements of $\mathbb Z_p$. Equivalently, $\pi_t(y)/t!=\binom{y+t}{t}\in\mathbb Z_p$ by density of $\mathbb N$ in $\mathbb Z_p$.

Fix: state it as a one-line lemma in §1, or cite "(proof of) R3M Lemma 1(a)". Even the weak form would suffice for phase 4, with a smaller decay rate ($\approx0.0257n$ instead of $0.0314n$), so no number in the claim depends on this.

**(F2) Prop E′ omits justifications.** Insert items 1–6 of §2.5 into its proof:
- monotonicity of $\tilde q$;
- $R\le K-\lambda_\beta$, including the last gate;
- $\#2D\ge0$ when the lower bound for $J$ is negative;
- that the gates in the 2D count exist;
- the deep-gate count used only up to $\sigma$;
- monotonicity in $\sigma$, $K$ and $f'$ (it is used in phase 4 with a non-integer $\sigma$).

**(F3) Wording (optional).**
- Theorem 1's proof: write "$D$ and $K$ are constant on $B$" in place of "both are constant on $B$".
- Lemma Q, Remark 2 ("the bound is sharp"): the attained cases (ratio 1) are the block-0/1D cases. With 2D blocks, the observed maximum is 0.87 at $p=7$; nearly tight, but not shown attained.
- `fe_verify.py`, phase-4 comment: say that the side-condition functions are convex. This is what makes "value and slope at $n^*$" sufficient.

## 5. How the proof respects the obstructions of the brief

- **Theorem 3.6 (nowhere dense).** No residue-class criterion is used. The output is a measure lower bound for one atom.
- **Prop 11.12 (per-window Cauchy–Schwarz fails).** Not used. The only per-window factor is $1+\chi_0^2$, once, as in C3.
- **Prop 11.15(b) ($\int\Lambda_t=\infty$).** The average is never over $\mathbb Z_p$.
  - Up to $i_A\approx4\cdot10^{42}$ the gate pattern on $A$ is deterministic, with depths at most 50. The double root $(y+2)^2$ appears as the finite factor $P_0(2,s)=\frac14$.
  - Beyond $i_A$, random deep gates are cut off by $G'$, at cost $2.5\cdot10^{-94}$. This is exactly the deep-gate truncation that R3M §5 said was needed before Markov's inequality.
- **Barrier lemmas (Theorem 3.10 / Prop 11.23).**
  - The deterministic bound (Prop D) is used for only 8 windows. It grows with depth like $q_s\propto p^s$, as the barrier requires.
  - The decay comes from averaging over the digits of $x$ in a ball (Theorem 1) together with the quenched anti-concentration bound (Lemma Q). This is the loophole named in the brief.

## 6. What this check does not cover; what remains open

- **The round-3 foundation.** Theorem M rests on R3M Props A, B, C2 and Theorem C3. These were checked by an independent instance and a referee in round 3. I re-read C3 and the uses of C2 here, but did not re-test C2.
- **Interval arithmetic.** My recomputation used 320-bit floating point, not interval arithmetic. It agrees with M4A's interval evaluation to all printed digits, and the decisive margin is 19 orders of magnitude.
- **Corollary M′** ($p=11,\dots,23$) was not part of this check. It is checked in Part II below.
- **Human refereeing.** None of the chain has been refereed by a human.
- **Reach of the result.** As M4A says, the result does not place a natural number in $K_7$ (Q3 is untouched), and it is not uniform in $p$.

## Credit

- **The proof checked here.** The proof of Theorem M (Lemma H, Theorem 1, Lemma F, Lemma Q, Props D/E/E′, the atom and the FE certificate) is track M4A's (round 4).
- **Round-3 machinery.** The frame in which it works (window identity, second moment, two-window inequality, Theorem C3) is track R3M's (round 3). It was checked by the round-3 checker and referee.
- **Earlier work.** The quenched martingale at $p=2$ is track R1b's (round 2). The $p=2$ quantitative templates are track R3Q's (round 3).
- **Classical tools.** Hensel's lemma; Paley–Zygmund; Doob's $L^2$ convergence; the second-moment method on trees (Lyons); branching processes in random environments as background (Smith–Wilkinson, Athreya–Karlin, Afanasyev–Geiger–Kersting–Vatutin); Legendre's formula.
- **This check.** This check was produced in an AI-assisted session (track verify_M4A_logic of round 4). It has not been checked by a human.

---

# Part II. Logic check of Corollary M′ ($p=11,13,17,19,23$)

Date: 2026-10-14. Lens: LOGIC. Made by the `verify_M4A_logic` track of round 4 (second run; Part I above is the first run, on Theorem M at $p=7$).

- **Checked:** `data/round4/reports/M4A.md`, Corollary M′ (§6), against everything it inherits from §§1–6. I also re-read `code/round4/M4A/` (`bounds.py`, `fe_lib.py`, `fe_verify.py`, `find_atom.py`, `qdp_check.py`) and the logs `data/round4/M4A/fe_verify_final.log`, `qdp_check.log` and `fe_crosscheck.log`.
- **New checker code** (`code/round4/verify_M4A_logic/`; it shares no code with `code/round4/M4A/`):
  - `cm_consts.py`: block constants by three methods (numpy residue DP, full enumeration, Fourier formula);
  - `cm_indep.py`: independent FE evaluation for any $p$ (derived from Part I's `fe_indep.py`);
  - `cm_eprime.py`: checks that Prop E′ dominates Prop E;
  - `cm_qtest.py`: exact Lemma Q tests at $p>13$.
  - `vl_lib.py` now has an int64-overflow guard; see §II.6.
- **Logs** (`data/round4/verify_M4A_logic/`): `corM_consts.log`, `corM_indep.log`, `corM_indep_S5.log`, `corM_lemmaQ.log`, `corM_thm1_propDE.log` and `corM_eprime.log`. Each run starts with `=== command:` and ends with `=== exit:`.
- **Budget:** about 4 core-minutes, at `nice -n 10`.

**The claim checked** (M4A Corollary M′, status [computer-assisted]). The verification of Theorem M is repeated with:
- $n_0=300$ and $r=27/20$;
- $\ell_1=6$ (Prop D thresholds for $\ell\le6$, then $\bar\varepsilon_\ell=2^{-(\ell-6)}$);
- the atoms in `data/round4/M4A/atom_p{11,13,17,19,23}.txt`.

It is claimed to give $\mu(K_p\cap A_p)/\mu(A_p)\ge1.06\cdot10^{-4}$ ($p=11$), $4.90\cdot10^{-2}$ ($13$), $3.48\cdot10^{-3}$ ($17$), $1.09\cdot10^{-1}$ ($19$) and $2.07\cdot10^{-1}$ ($23$). Hence $\mu(K_p)>0$ for these five primes.

## II.0 Headline

**Verdict: confirmed-with-fixes.**
- The conclusion holds: $\mu(K_p)>0$ for $p\in\{11,13,17,19,23\}$.
- Its label [computer-assisted] is right.
- FE holds for each of the five atoms with a margin of 16.6 to 21.9 decimal orders.

**Three of the five explicit constants are rounded up.** The certificate does not imply them.

| $p$ | claimed | certificate value (M4A's interval code, and my independent code) | proved, 3 digits rounded down |
|---|---|---|---|
| 11 | $\ge1.06\cdot10^{-4}$ | $1.0587\cdot10^{-4}$ / $1.05875\cdot10^{-4}$ | **$\ge1.05\cdot10^{-4}$** (claim not implied) |
| 13 | $\ge4.90\cdot10^{-2}$ | $4.8954\cdot10^{-2}$ / $4.89550\cdot10^{-2}$ | **$\ge4.89\cdot10^{-2}$** (claim not implied) |
| 17 | $\ge3.48\cdot10^{-3}$ | $3.4825\cdot10^{-3}$ / $3.48258\cdot10^{-3}$ | $\ge3.48\cdot10^{-3}$ (claim correct) |
| 19 | $\ge1.09\cdot10^{-1}$ | $1.0909\cdot10^{-1}$ / $1.09096\cdot10^{-1}$ | $\ge1.09\cdot10^{-1}$ (claim correct) |
| 23 | $\ge2.07\cdot10^{-1}$ | $2.0671\cdot10^{-1}$ / $2.06713\cdot10^{-1}$ | **$\ge2.06\cdot10^{-1}$** (claim not implied) |

The bound of Theorem C3, $(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$, decreases in $\Pi_A$ and in $\delta_A$. Inserting the certified upper bounds therefore gives exactly the middle column, and nothing larger is proved. The overstatement is 0.1–0.14%. It does not affect positivity, but a stated lower bound must be rounded down. This is fix **(C1)**.

Everything else checks out:
- Every step of the chain is p-generic, and each p-specific input is met (§II.1–II.3).
- I recomputed every constant independently: atoms, block constants, $\chi^2_0$, the $6\times5$ phase-1 thresholds, the phase-2 to phase-4 failure sums, $\Pi_A$, $\delta_A$ and the final bounds. All agree with M4A to every printed digit (§II.4).
- The remaining fixes are to the write-up: (C2)–(C5) in §II.7.

## II.1 What changes between $p=7$ and $p\ge11$

Part I audited the whole chain line by line at $p=7$: C3 as used, Lemma H, Theorem 1, Lemma F, Lemma Q (Steps 0–4), Props D/E/E′, and phases 0–4. I re-read every step with $p$ as a free odd prime and list here each place where $p$ or the atom enters.

| step | p-dependence | status at $p=11,\dots,23$ |
|---|---|---|
| R3M Theorem C3 (note Thm 11.14) | needs deterministic times $2p\le n_0$ and an admissible atom; no other condition on $p$ | $n_0=300\ge46$. Atoms re-verified (§II.2) |
| Survival $\Rightarrow x\in K_p$ (note Prop 1.2, R3M (F1)–(F2)) | odd $p$ | p-generic |
| Lemma H, Theorem 1 | none | p-generic (Hensel) |
| Lemma F | none | p-generic. Hypothesis $M_W\le K-\theta$ re-asserted in every window (§II.3) |
| Lemma Q, Step 2 | $g_1\le p$ and $u\equiv-g_1\pmod{p^{s_1}}$ | p-generic |
| Lemma Q, Step 3 | $\pi_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^d}$ | p-generic |
| Lemma Q, Step 4 | the poles $-i$, $1\le i\le p-1$, are units away from $-p$; $H_{p-1}\equiv0\pmod p$ | true for every odd $p$ (pair $i$ with $p-i$) |
| constants $q_s$, $P_0(g,s)$ | finite computations, separate for each $p$ | recomputed three ways (§II.2) |
| truncation $\tilde q_s=q_Sp^{s-S}$ ($S=4$ for $p>13$) | needs $q_s\le pq_{s-1}$ | proved: $\max_zP(Z\equiv z\bmod p^s)\le\max_zP(Z\equiv z\bmod p^{s-1})$ |
| $P_0$ table cut at $S_0=4$ ($p>13$) | `P0[g][min(s1,k,S0)]` | valid, since $P_0(g,s)$ is nonincreasing in $s$ |
| Prop E′ | needs $\kappa>0$ | $\kappa=2.65,3.58,5.75,6.89,9.24$ |
| phase-4 rate | needs $c=\gamma\frac{(p-1)(r-1)}{2p^2}-\frac{(r^2-1)\rho_1}{p-1}>0$ | positive at each $p$; the decay rate used is $c'=c/2\in[0.0114,0.0159]$ |
| phase-2 slope threshold | $\theta=\min(\lceil D/2\rceil,D-m+1)$ with $b=m$ | at the first Markov window ($\ell=7$) $\lfloor D/2\rfloor+1\ge m$ holds for every $p$, so $\theta=\lceil D/2\rceil$ (table in §II.3) |
| event $G'$ | $\mu_A(G'^c)\le p^{-10}(i_A^{-2}+p^{-2m}\pi^2/6)$ | p-generic. Values $1.4\cdot10^{-72}$ … $2.0\cdot10^{-51}$ |

One point is new at these primes. With $\ell_1=6$ the first Markov window is $\ell=7$, where $D$ is close to $2m$, so Theorem 1's threshold could in principle fall below $\lceil D/2\rceil$. It does not, as the table in §II.3 shows. Both codes in any case use the general $\theta=\min(\lceil D/2\rceil,D-b+1)$, which is what Theorem 1 states. So no window relies on the special case.

## II.2 The p-specific inputs, checked independently

**Atoms.** `cm_indep.py` checks each atom with exact integers.

| $p$ | $m=V_{300}(x_A)$ | $M_{300}$ | $v(S_e(x_A))$ | $S'_e(x_A)\bmod p$ | $D_0$, $M_{405}$ | $i_A$ | $\ell^*$ (first phase-4 window) |
|---|---|---|---|---|---|---|---|
| 11 | 30 | 3 | 30 | 1 | 11, 3 | $5.73\cdot10^{30}$ | 216 |
| 13 | 26 | 3 | 26 | 5 | 8, 3 | $8.12\cdot10^{28}$ | 202 |
| 17 | 18 | 2 | 18 | 6 | 8, 2 | $1.36\cdot10^{22}$ | 150 |
| 19 | 16 | 1 | 16 | 2 | 6, 2 | $4.04\cdot10^{19}$ | 131 |
| 23 | 14 | 2 | 14 | 7 | 4, 2 | $3.79\cdot10^{18}$ | 123 |

Here $\ell^*$ is the first window with $n_{\ell+1}\ge i_A$. The checks run as follows:
- The path has $e_0=1$, $v(S_e(x_A))\ge m$ and $p\nmid S'_e(x_A)$. Both properties are constant on $A$, because $S_e\in\mathbb Z[X]$. So $Z^0_{300}\ge1$ on $A$.
- $M_{300}<m$, so $A$ is a $\mathcal G_0$-atom.
- $D_0\le m-M_{405}$ and $M_{405}<m$, so $A$ is admissible.
- The digit formula for $V_N$ on $A$ ($N<i_A$) matches direct valuations. For every block-level window the code asserts that $D$, $K$ and $M_{N'}$ from the formula equal those from the depth array.

**Block constants.** These are three methods with no shared code (`cm_consts.py`, log `corM_consts.log`).
1. **Numpy residue DP** modulo $p^S$, with $p^S\le2\cdot10^7$: $S=7,6,5,5,5$.
2. **Full enumeration** of the $3^p$ digit vectors, for $p\le13$ (`vl_lib.py`). It agrees exactly with the DP for every $s\le S$ and for the whole $P_0$ table.
3. **The Fourier formula** $P(Z\equiv z)=p^{-s}\sum_\xi e(-\xi z/p^s)\prod_k\cos^2(\pi\xi a_k/p^s)$, at 60 digits, for $q_1$ and $q_2$ at $p\ge11$. It agrees with the DP to $<3\cdot10^{-60}$.

Results:
- Monotonicity $q_{s-1}\le q_s\le pq_{s-1}$ holds for all computed $s$.
- $P_0(2,s)=\frac14$ for all $s$ computed: this is the double root of $(y+2)^2$.
- The derived constants equal M4A's printed values to every digit:

| $p$ | $q_1$ | $q_2$ | $\rho_1$ (M4A's $S$) | $\gamma$ | $\kappa$ |
|---|---|---|---|---|---|
| 11 | 1.001436 | 1.111596 | 0.016448 | 2.293534 | 2.654542 |
| 13 | 1.000022 | 1.008124 | 0.002522 | 2.556880 | 3.576696 |
| 17 | 1.0000006 | 1.000290 | 0.000261 | 2.832924 | 5.747961 |
| 19 | 1.0000001 | 1.000463 | 0.000114 | 2.943976 | 6.890086 |
| 23 | 1.000000005 | 1.000002 | 0.0000175 | 3.135492 | 9.244994 |

With $S=5$ in place of $S=4$ at $p=17,19,23$, $\rho_1$ is slightly smaller. Every final number is unchanged to 8 digits (`corM_indep_S5.log`), so the truncation choice is not load-bearing.

## II.3 Phases 1–4 at each prime

**Phase 0/1 (pointwise, $\ell\le6$).** The six windows $[n_{\ell-1},n_{\ell+1})$ end at $2457<i_A$, so their gate patterns are constant on $A$. In each:
- the linear regime holds exactly;
- Prop D is a bound for every $x\in A$;
- $\bar\varepsilon_\ell$ is a fixed number, so the quantifier order of C3 is respected;
- these windows contribute nothing to $\delta_A$.

My values ($\chi^2_0$; $\bar\varepsilon_1,\dots,\bar\varepsilon_6$):
- $p=11$: $3.63828$; 4.24547, 0.453086, 0.635356, 2.76092, 2.80530, 3.78773;
- $p=13$: $0.422094$; 0.433964, 1.47852, 0.457808, 0.0598492, 0.0431679, 0.0517123;
- $p=17$: $7.50249$; 7.50253, 3.01028e-4, 2.39594e-3, 0.594706, 8.97118e-4, 0.0409166;
- $p=19$: $1.44370\cdot10^{-3}$; 1.44449e-3, 0.0720314, 4.65730e-4, 4.75248e-4, 2.56747, 1.41195e-3;
- $p=23$: $2.22478\cdot10^{-8}$; 5.47860e-8, 0.0621592, 0.796879, 2.40656e-6, 8.83393e-4, 0.0621617.

All of these agree with `fe_verify_final.log` to its 4 printed digits.

**Phase 2 (Markov with Prop E on $B=A$, $7\le\ell\le16$).** First Markov window, $\ell=7$, $[1820,2457,3317)$:

| $p$ | $D$ | $K$ | $m=b$ | $\lfloor D/2\rfloor+1\ge b$? | $\theta$ | $M_W$ | $K-M_W\ge\theta$? | $\log_{10}\mathbb E_A\varepsilon_7$ | $\log_{10}$ fail$_7$ |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 62 | 149 | 30 | 32 ≥ 30 yes | 31 | 3 | yes | −25.038 | −24.737 |
| 13 | 52 | 124 | 26 | 27 ≥ 26 yes | 26 | 3 | yes | −23.528 | −23.227 |
| 17 | 39 | 93 | 18 | 20 ≥ 18 yes | 20 | 2 | yes | −20.861 | −20.560 |
| 19 | 34 | 83 | 16 | 18 ≥ 16 yes | 17 | 3 | yes | −17.893 | −17.592 |
| 23 | 28 | 68 | 14 | 15 ≥ 14 yes | 14 | 2 | yes | −17.702 | −17.401 |

This window dominates $\delta_A$ at every prime. The later windows have larger $D$, and both conditions are re-asserted for each.
- My Prop E values use the full $c$-sum. They agree with M4A's to 3 decimals wherever M4A's $c$-sum is not truncated.
- Where it is truncated (mostly $\ell=15,16$), my values are smaller. M4A caps the sum at $c^*$ and adds $2^{-c^*}$ (rigorous, but cruder).
- In the actual phase-2 windows, Prop E′ dominates Prop E in 50/50 cases.

**Phase 3 (Prop E′ with exact $D$, $K$, $\sigma=M_{n_{\ell+1}}\le m-1<b$).** The linear regime and Lemma F's condition are checked exactly in every window up to $\ell^*-1$. The phase-2 and phase-3 failure sums are:
- $1.8318\cdot10^{-25}$ at $p=11$;
- $5.9304\cdot10^{-24}$ at $p=13$;
- $2.7573\cdot10^{-21}$ at $p=17$;
- $2.5567\cdot10^{-18}$ at $p=19$;
- $3.9710\cdot10^{-18}$ at $p=23$.

**Phase 4 (all $\ell\ge\ell^*$).** Part I's own closed-form argument, with $p$ in place of 7:
- each bound is written as $-an+b\ln n+c$;
- convexity is used;
- the value and the slope are checked at $n^*=n_{\ell^*-1}$.

It gives $\ln\mathrm{fail}_\ell\le-c'n_{\ell-1}$ for all $\ell\ge\ell^*$. It also gives $D\ge2\sigma_\ell$ (so Theorem 1 applies on balls of radius $p^{-(\sigma_\ell+1)}$ with $\theta=\lceil D/2\rceil$, and $M_W\le K-\theta$) and the linear regime on $G'$:

| $p$ | $c'$ | $\ln$ tail $\le$ | $D-2\sigma$ at $n^*$ | $m_{\ell-1}-K-M$ at $n^*$ | $\mu_A(G'^c)\le$ |
|---|---|---|---|---|---|
| 11 | 0.015909 | $-5.0\cdot10^{28}$ | $1.1\cdot10^{29}$ | $5.6\cdot10^{28}$ | $1.38\cdot10^{-72}$ |
| 13 | 0.015800 | $-7.5\cdot10^{26}$ | $1.4\cdot10^{27}$ | $7.0\cdot10^{26}$ | $2.52\cdot10^{-69}$ |
| 17 | 0.013717 | $-1.1\cdot10^{20}$ | $1.7\cdot10^{20}$ | $8.8\cdot10^{19}$ | $6.81\cdot10^{-57}$ |
| 19 | 0.012842 | $-3.4\cdot10^{17}$ | $5.1\cdot10^{17}$ | $2.6\cdot10^{17}$ | $1.03\cdot10^{-52}$ |
| 23 | 0.011410 | $-2.7\cdot10^{16}$ | $3.8\cdot10^{16}$ | $1.9\cdot10^{16}$ | $1.97\cdot10^{-51}$ |

The slopes at $n^*$ are all positive (log `corM_indep.log`). M4A's tangent-line code (`fe_verify.py`) reaches the same conclusions with the same $c'$.

**Union bound and C3.** This step is identical to Part I §2.6. The bound is
$$\{\tau<\infty\}\subseteq\bigcup_{7\le\ell<\ell^*}\{\varepsilon_\ell>\bar\varepsilon_\ell\}\ \cup\ G'^c\ \cup\bigcup_{\ell\ge\ell^*}\big(G_\ell\cap\{\varepsilon_\ell>\bar\varepsilon_\ell\}\big).$$
It needs:
- $G'\subseteq G_\ell$;
- the linear regime on $G'$;
- $G_\ell$ a union of balls with constant pattern.

All three were checked above.

## II.4 Totals: independent recomputation against M4A

My values come from 320-bit mpmath; they are not intervals. M4A's values come from 200-bit outward-rounded intervals.

| $p$ | $\log_{10}\Pi_A$ (M4A / mine) | $\delta_A$ (M4A / mine) | $\log_{10}(\Pi_A\delta_A)$ | $\mu(K_p\cap A)/\mu(A)\ge$ (M4A / mine) | $\mu(K_p)\ge$ (mine, rounded down) |
|---|---|---|---|---|---|
| 11 | 3.9752 / 3.97521 | 1.831839e-25 / 1.831839e-25 | −20.7619 / −20.76191 | 1.0587e-4 / 1.05875e-4 | $6.06\cdot10^{-36}$ |
| 13 | 1.3102 / 1.31020 | 5.930408e-24 / 5.930408e-24 | −21.9167 / −21.91671 | 4.8954e-2 / 4.89550e-2 | $5.33\cdot10^{-31}$ |
| 17 | 2.4581 / 2.45810 | 2.757312e-21 / 2.757312e-21 | −18.1014 / −18.10142 | 3.4825e-3 / 3.48258e-3 | $2.47\cdot10^{-25}$ |
| 19 | 0.9622 / 0.96219 | 2.556695e-18 / 2.556695e-18 | −16.6301 / −16.63013 | 1.0909e-1 / 1.09096e-1 | $3.78\cdot10^{-22}$ |
| 23 | 0.6846 / 0.68463 | 3.970986e-18 / 3.970986e-18 | −16.7165 / −16.71647 | 2.0671e-1 / 2.06713e-1 | $1.78\cdot10^{-20}$ |

FE ($\Pi_A\delta_A<1$) holds with margins of $10^{16.6}$ to $10^{21.9}$, which no rounding error can approach. The last column is $(\text{lower bound})\cdot p^{-m}$; M4A does not state it for these primes.

## II.5 Numerical tests (exact unless stated)

| claim tested | program | runs | result | log |
|---|---|---|---|---|
| block constants (DP = enumeration) | `cm_consts.py` | $p=7,11,13$, all $s\le S$, full $P_0$ tables | equal | `corM_consts.log` |
| $q_1,q_2$ (DP = Fourier, 60 digits) | `cm_consts.py` | $p=11,13,17,19,23$ | $|\Delta|<3\cdot10^{-60}$ | `corM_consts.log` |
| Lemma Q inequality (random $u$, planted first gate incl. $g=2$, integer-like $u$, planted deep gate) | `test_small.py Q` | $p=11$: 5500 tests ($k\le3$, $f\le2$); $p=13$: 2000 | **0 violations**; max P/bound $=1.000000$ (attained) | `corM_lemmaQ.log` |
| Lemma Q with DP constants | `cm_qtest.py` | $p=17$: 300 ($k\le3$); $p=23$: 300 ($k\le2$) | **0 violations**; max ratio 1.000000 | `corM_lemmaQ.log` |
| Lemma Q, 2D blocks targeted | `q2d_test.py` | $p=11$: 200; $p=13$: 150 | 0 violations; with one 2D block the max ratio is 0.956 ($p=11$) and 0.997 ($p=13$) | `corM_lemmaQ.log` |
| negative controls (2D factor $q_2/p^3$) | `test_small.py Q … 1`, `q2d_test.py … 1` | $p=11$: 600 + 200; $p=13$: 600 | 10 + 9 + 9 violations, so the tests are sensitive | `corM_lemmaQ.log` |
| Theorem 1 identity; Prop D; Prop E; Lemma F+Q | `test_small.py T1` | $p=11$: 34 cases; $p=13$: 20; balls $b=2$, $H\le31$, $\theta\in\{0,1,2\}$ | **54/54 exact identities**; Prop D, Prop E and Lemma F hold in all; max $(\varepsilon+1)$/PropD $=0.994$ | `corM_thm1_propDE.log` (valid runs after the NOTE line) |
| Prop E′ ≥ Prop E | `cm_eprime.py` (256-bit) | $p=13,17,19,23$, $n\in[60,2500]$, half with planted deep gates (depth 3–7) | **194/194**; closest $\log_{10}(E/E')=-5.4$ | `corM_eprime.log` |
| FE certificates | `cm_indep.py` | $p=11,13,17,19,23$ ($S=4$ or $8$); $p=17,19,23$ also with $S=5$ | reproduced (§II.4) | `corM_indep.log`, `corM_indep_S5.log` |

The exact tests of Part I at $p=3,5,7$ (logs `lemmaQ.log`, `lemmaQ_2D.log`, `thm1_propDE.log` and `eprime.log`) cover the same lemmas at the small primes.

## II.6 Failed or superseded runs

1. **The first two `T1` runs at $p=11,13$ are invalid.** Their window lengths went up to $H=40$. The exact DP of `vl_lib.signed_dp_joint` keeps counts in int64 and overflows for more than 31 free digits ($4^{32}>2^{63}$). Every reported "failure" (14 lines) had $H\ge32$.
   - This was an error in my harness, not in M4A.
   - The runs are kept in `corM_thm1_propDE.log` with a NOTE line marking them as superseded.
   - `vl_lib.py` now asserts at most 31 free digits. The guard never fires in the earlier valid runs: all Part I cases had $H\le31$, which I checked.
   - The valid reruns ($H\le31$) pass 54/54.
2. **The negative control at $p=17$** (`cm_qtest.py … 1`, 150 tests) produced no violation. With $t\le30$ (the int64 limit) a $p=17$ path has at most two gates, so 2D blocks and $d=2$ blocks hardly occur. That control is uninformative. The controls at $p=11,13$ are sensitive.

## II.7 Required fixes

- **(C1) The constants of Cor M′ must be rounded down.**
  - Replace $1.06\cdot10^{-4}$, $4.90\cdot10^{-2}$ and $2.07\cdot10^{-1}$ by $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$ and $2.06\cdot10^{-1}$; or quote four digits: $1.058\cdot10^{-4}$, $4.895\cdot10^{-2}$, $2.067\cdot10^{-1}$.
  - The values for $p=17,19$ are correct.
  - The table in M4A §6 also rounds several *bounds* to nearest instead of outward. Examples: $\log_{10}\delta_A=-24.74$ at $p=11$, where the certificate gives $\le-24.737$; $\log_{10}\Pi_A=1.31$ at $p=13$, where it gives $\le1.3102$. Either round outward or label the columns as approximate values.
- **(C2) State the phase-2 slope threshold for $\ell_1=6$.** M4A states $\theta=\lceil D/2\rceil$ only for $p=7$ ("$D\ge194$"). For Cor M′ the first Markov window has $D=62,52,39,34,28$ against $m=30,26,18,16,14$. Add a sentence that $\lfloor D/2\rfloor+1\ge m$ holds from $\ell=7$ on (table in §II.3), or that the general $\theta=\min(\lceil D/2\rceil,D-m+1)$ is used, as both codes do.
- **(C3) Say where the large-prime constants come from.**
  - For $p>13$ the constants come from a residue DP with $S=S_0=4$. M4A validated the DP against enumeration only for $p\le13$, and `fe_crosscheck.py` covers only $p=7,11,13$.
  - The report should note that $S=4$ is legitimate because $q_s\le pq_{s-1}$ and $P_0$ is monotone in $s$.
  - It should also cite an independent confirmation of the DP values for $p=17,19,23$: this check gives one (DP = Fourier for $q_1,q_2$; full recomputation of the certificates).
- **(C4) Fixes inherited from Part I.** (F1) is the strong form of R3M Lemma 1(c) and its one-line proof; (F2) is the missing justifications in Prop E′; (F3) is wording. They apply verbatim to Cor M′, since phase 4 uses the strong form of Lemma 1(c) at every prime.
- **(C5) Optional.** State that the margins are $10^{16.6}$–$10^{21.9}$ and that $\delta_A$ is dominated by the single window $\ell=7$ at every prime. This is where any future tightening would act.

## II.8 Obstructions of the brief

Nothing changes from Part I §5:
- no residue-class criterion (Theorem 3.6);
- no per-window Cauchy–Schwarz (Prop 11.12);
- no average over $\mathbb Z_p$, since everything is on the atom or on balls inside $G_\ell$, which avoids $\int\Lambda_t=\infty$ (Prop 11.15(b));
- the deterministic Prop D is used for only six windows per prime, with $q_s\propto p^s$ for deep gates (barrier lemmas).

At these primes the pointwise windows have depths $\le4$, and the gain again comes from averaging over the digits of $x$ in the atom (Theorem 1 with Lemma Q).

## II.9 What this check does not cover; what remains open

- As in Part I, the round-3 foundation (R3M Props A, B, C2 and Theorem C3) is taken as checked in round 3. I re-read C3 and C2 as used here, and found no condition specific to $p=7$.
- My recomputation uses 320-bit floating point, not intervals. It agrees with M4A's interval evaluation to all printed digits.
- The result is prime by prime. Nothing here gives a statement for all $p\ge p_0$ (M4A §8.7), and nothing touches Q3.
- No part of the chain has been refereed by a human.

## Credit (Part II)

- **The result checked.** Corollary M′ and its proof machinery (Theorem 1, Lemma Q, Props D/E/E′ and the FE certificates) are track M4A's (round 4).
- **Round-3 machinery.** Theorem C3 and the window identities are track R3M's (round 3).
- **Earlier work.** The $p=2$ martingale is track R1b's (round 2), and the $p=2$ quantitative templates are track R3Q's (round 3).
- **Classical tools.** Hensel's lemma, Paley–Zygmund, Doob, Lyons, and the background of Smith–Wilkinson, Athreya–Karlin and Afanasyev–Geiger–Kersting–Vatutin. The Fourier check of $q_1,q_2$ uses the standard characteristic-function formula for lattice sums.
- **This check.** This check was produced in an AI-assisted session (track verify_M4A_logic of round 4). It has not been checked by a human.
