# Round-3 logic referee report on note.md §11 (revision 3, 2026-10-13)

Referee: round-3 logic referee (an AI instance; not a human). Scope as assigned:
1. every [proved] / [computer-assisted] statement of §11 (and the (c), (d), (e) items) against the track report that proves it and the adversarial check that confirms it;
2. a line-by-line re-check of the proofs seen by only one checker: Theorem 11.14 with Propositions 11.12–11.13 (R3M §§4–5), the reduction in Theorem 11.7 (R3Q), Theorems 11.17 and 11.22 (R3F (a), (b));
3. S0's Lemma S0.1, which nobody had checked;
4. the "[Round 3]" edits outside §11 and the status lines.

§11.5 (R3C) is a placeholder and was not reviewed.

Material read: README.md; note.md §0, §2, §5, §8, Remarks 10.8, §§10.5–10.6, §10.8 and all of §11; `data/round3/reports/{S0,R3N,R3Q,R3M,R3F}.md` (in full for R3M, R3Q, R3F; the relevant sections of R3N and S0); `data/round3/checks/{R3N,R3Q,R3M,R3F}.md` in full; the R3N survey CSVs and witness log; the R3Q check's `table.log`.

Own code: `code/round3/referee_logic/` (README there). Logs: `code/round3/referee_logic/logs/`. Scratch: `/tmp/r3_ref_logic/`. CPU used: about 20 core-minutes on one core, `nice -n 10`, one job at a time.

## Verdict

**No fatal and no serious error.** Every proved statement of §11 that I re-checked line by line is correct, and every labelled item of §11 agrees in substance with its track report and its check. Lemma S0.1 is correct; I also prove S0's conjectured exact value at $n=2^m$. The status lines do not overstate Q1 or Q3.

There are **17 minor findings** (§6). The most substantive:
- the note states as fact that FE "is of barrier type" and that "a proof must use unboundedly many digits", which R3M itself labels heuristic (F1);
- Theorem 11.22 drops the hypothesis $H_t+1<p^t$, and its "only for $p\ge11$" reason is incomplete (F2);
- §11.0 says S0 re-checked "the first four rungs" of Kitamura's 594 ladder, but S0 checked only $G\le8192$ and says explicitly that the higher rungs were not reproduced (F3);
- one item labelled [proved] contains an uncertified floating-point illustration (F4).

## 1. Statement-by-statement comparison (task item 1)

"Match" means: same hypotheses, quantifiers, constants and label as the report, after the check's fixes. Any deviation is listed in §6.

| note item | source | label in note | verdict |
|---|---|---|---|
| Lemma 11.1 (i)–(iii) | R3N Lemmas 1–2 | proved | **match**. (iii) omits "or a final candidate" from R3N Lemma 2(b). That is harmless: under the hypothesis every final candidate has valuation $<K\le v(N_K!)$, so it is itself a death candidate at stage $N_K$. |
| Theorem 11.2 + table | R3N Thm R3N.1, §4.3; check §§2–3, 6 | computer-assisted | **match**. The 17662 witness that the check required now exists: `witness_17662_K221465.txt.gz`, 101480 terms, max 221465, verified by three methods (`data/round3/R3N/verify_17662_221465.log`). |
| Corollary 11.3 | R3N Cor R3N.2 (with the check's fix: Thm 3.1(a) for $\mathbb Z_2$) | proved | **match** |
| Theorem 11.4, the "largest excesses" and the $a\le4096$ ranking | R3N §4.1; check §§3.3, 4 | computer-assisted | **match**. I recomputed the top-8 list, the $a\le4096$ top ten, and $G\cdot\#\{g\ge G\}/16384\in[8.0,11.75]$ for $256\le G\le131072$ from the CSVs myself. |
| Lemma 11.5 | R3Q Lemma 3; check §1.3 | computer-assisted, three programs | **match** (reduction re-derived: valuation patterns on $C_0,C_2,C_6,C_{10},C_4$ and the propagation step) |
| Lemma 11.6 | R3Q Lemma 8 + remark | proved | **match** (proof re-derived; §2.2) |
| "Further lemmas" | R3Q Lemmas 5, 6, Prop 7, Lemma 9 / Prop 10 | proved | **match**, except that the one-step identity drops a hypothesis (F11) |
| Theorem 11.7 | R3Q Thm C; check §1.10 | computer-assisted | **statement matches.** The sentence describing the closed-form check is self-contradictory (F5). |
| Corollary 11.8 | R3Q Cor D; check F1 | computer-assisted | **match**. Every entry is rounded up. I compared all seven with the check's exact values: 0.1005059, 0.0910330, 0.0632239, 0.0455551, 0.0205533, 4.935928e-6, 6.494454e-13. |
| Theorem 11.9 | R3Q Thm A′; check F2 | computer-assisted | **match**. The sentence after it still says "proved analogue" (F14). |
| Prop 11.10 | R3M Prop A, Cor A′ | proved | **match** (proof re-read; my independent test, §4) |
| Prop 11.11 | R3M Prop B, Remark B′ | proved | **match**, but "that fails here" (F10) |
| Prop 11.12 | R3M Prop N | proved | **match** (§2.1) |
| Prop 11.13 | R3M Lemma C1, Prop C2 | proved | **match in substance.** Hypothesis (5.2) and the cylinder are not stated (F11). |
| Theorem 11.14 | R3M Thm C3, Lemma C4 | proved; FE unproved | **match**. $n_0\ge2p$ is not stated (F11). |
| Prop 11.15 (a), (b) | R3M Lemma C5, Prop N3 | proved | **match** (both proofs re-derived). The consequence drawn after it is unlabelled (F6). |
| Lemma 11.16 | R3F Lemma A1 | proved | **match** |
| Theorem 11.17 | R3F Thm A2 | proved | **match** (§2.4) |
| Theorem 11.18 | R3F Thm A4, Prop A6 | proved | **match** |
| Theorem 11.19 | R3F Thm A5; check §2 | computer-assisted | **constants match.** The program count in the label overstates at $p=13$, $d=9$, and "$d\le j+1$" is implicit (F12). |
| Prop 11.20 | R3F Prop B1 | proved | **match** |
| budgets | R3F B2; check §3.2 | constants proved, relevance heuristic | **match** ($\Lambda'_7=2.0496$ as fixed) |
| certified $L^2$ shells | R3F B3; check §3.3 | computer-assisted | **match** (wording fixes applied) |
| Prop 11.21 + data | R3F Prop B4, Cor B4′, B4-data | proved / computer-assisted | **match**. Two totals are rounded down (F13). |
| Theorem 11.22 | R3F Thm B5 | proved; hypothesis unproved | **proof correct; a hypothesis is dropped** (F2) |
| Prop 11.23 | R3F Prop B6 | proved | **match** |
| Prop 11.24 | R3F Prop B7 | proved | **match** |
| (c) | R3F C1–C5 | proved; small cases certified; negative | **match** |
| (d) | R3F D1, D2, D4 | **[proved]** | **label too strong for the second bullet**, which is R3F's D2, a floating-point "computer-assisted illustration" (F4) |
| (e) | R3F (e); check row (e) | computer-assisted | **match** |

## 2. Line-by-line re-checks (task item 2)

### 2.1 R3M: Propositions N (11.12), C1/C2 (11.13), Theorem C3 (11.14)

**Prop N.**
- The mod-$p$ shell of $\chi^2_W$ is $p\sum_a\mu_{W,1}(a)^2-1$, with $\mu_{W,1}(a)=c_a/2^r$.
- The balanced minimiser gives exactly $p[s(q+1)^2+(p-s)q^2]-(qp+s)^2=s(p-s)$, and $s\ne0$ because $p$ is odd.
- $r\le p$: if $D\ge1$, the first multiple of $p$ among $x+n+1,\dots$ lies at or before $x+N$, and the $r$ valuation-0 elements precede it.
- Equality for $|P|=1$ is immediate from B(ii).

Correct. The "Consequence" holds for every window sequence: infinitely many windows have $D\ge1$ because $V_n\to\infty$.

**Lemma C1.**
- Under $D+k\le m-M_N$ and $M_N<m$, I re-derived the following:
  - $\tau_n(e,x')\equiv\tau^0_e-\beta_ew\pmod{p^{D+k}}$, from Lemma 2(b) with $D+k\le m-M_n$;
  - $q_f$ is constant modulo $p^{D+k}$;
  - the unit $u$ is constant modulo $p^k$;
  - $\tau_N\equiv u^{-1}(t-q_f)/p^D\pmod{p^k}$.
- $G=g*m$ with $\hat g=p^k\mathbf 1[\zeta\equiv\xi u^{-1}\ (p^k)]$.
- Mean zero, then Cauchy–Schwarz over parents, Parseval, and $c_NTp^{-D}=c_n$.
- $F_W(0)=1+\chi_W^2$.

Correct.

**Prop C2.**
- *Step 0.* (5.2) implies (W2′), (W3′) for $W$ at $x$ and for $W'$ at every $x'$ (base valuation $m+D$, and $D'\le m-M_{N'}-D\le m+D-M_N$), and it implies (5.1) with $k=D'$.
- *Step 1.* Variance decomposition over $C'=x'+p^{m+D}\mathbb Z_p$.
- *Step 2.* The class-wise computation follows B(iii). Minkowski's inequality in $L^2(w,w')$ is legitimate because the class index $b\mapsto P_{bu}$ does not depend on $w$ ($u$ is fixed by $x$).
- *Step 3.* $v(\pi_j'(x'))\ge V_j-M_j\ge m-M_N\ge D'$ for $n\le j<N$. Also $\pi_n(x')/p^m\equiv\omega$ and $\pi_N(x')/(p^D\pi_n(x'))\equiv u$, both modulo $p^{D'}$. Hence $\beta_{e'}\equiv\beta_eu^{-1}$.
- *Step 4.* $\sum_b|P_{bu}|=Z^0_n$.
- *Identification.* $\hat\nu_{D+D'}(\zeta)=\hat\mu_{W,D+D'}(\zeta)\hat\mu_{W'}(\zeta u)$, and the fibres over $\xi\ne0\pmod{p^{D'}}$ give $\varepsilon$.

Correct. For a single parent, both Cauchy–Schwarz and Minkowski are equalities, so equality is predicted. I confirmed it independently (§4).

**Theorem C3.** Each step checked:
- *Partition.* For $n\ge2p$ there are at least two multiples of $p$ among $x+1,\dots,x+n$, so $V_n\ge M_n+1$ and $m_\ell$ is constant on its cylinder. The partition is defined up to the null set of negative integers.
- *Nesting.* $\mathcal G_\ell\subseteq\mathcal G_{\ell+1}$.
- *Measurability.* $B_\ell\in\mathcal G_{\ell-1}$, since $\{M_{n_{\ell+1}}<m_{\ell-1}\}$ is a residue condition modulo $p^{m_{\ell-1}}$ and $\varepsilon_\ell$ depends on $x\bmod p^{D_{\ell-1}+D_\ell}$ with $D_{\ell-1}+D_\ell\le m_{\ell-1}$. Hence $\{\tau_j>\ell\}\in\mathcal G_{\ell-1}$.
- *Window conditions.* On $\{\tau_j>\ell\}$, (W2′) and (W3′) hold for $W_\ell$:
  - $D_\ell\le m_{\ell-1}-M_{n_{\ell+1}}-D_{\ell-1}=m_\ell-2D_{\ell-1}-M_{n_{\ell+1}}\le m_\ell-M_{n_\ell}$;
  - $M_{n_{\ell+1}}<m_{\ell-1}\le m_\ell$.
- *First moment.* Corollary A′ gives the martingale property. On $\{\tau_j\le\ell\}$ the process is frozen, and $M_{\tau_j}$ is $\mathcal G_{\tau_j}$-measurable.
- *Second moment.* $\mathbb E[\tilde M^2_{\ell+1}-\tilde M^2_\ell\mid\mathcal G_{\ell-1}]=\mathbf 1_{\{\tau_j>\ell\}}(\cdots)\le\bar\varepsilon_\ell\tilde M^2_{\ell-1}$, using $\tilde M_{\ell-1}=M_{\ell-1}$ there. Then $a_{\ell+1}\le a_\ell+\bar\varepsilon_\ell a_{\ell-1}\le(1+\bar\varepsilon_\ell)a_\ell$, by monotonicity (conditional Jensen). Finiteness holds by induction.
- *Limit.* Doob's $L^2$ convergence theorem.
- *Survival.* If $Z^0_{n_\ell}=0$ for some $\ell$, then on $\{\tau_j=\infty\}$ Prop A(i) kills every later slope-0 population. So $Y>0$ gives an alive path at every $n_\ell$, hence at every $n$ (prefixes are alive), hence $x\in K_p$ by (F1). (F1) is direct, since $g_p(x)=\sup_Bv(S_B(x))$; the note's citation of Prop 1.2 and König's lemma is unnecessary but harmless.
- *Paley–Zygmund.* $\mathbb EY\ge M_j(1-\sqrt{\Pi_A\delta_A})$ and $\mathbb EY^2\le M_j^2\Pi_A$.

Correct as a conditional theorem.

**Lemma C4.**
- *Deterministic part.* $V+M\le n/(p-1)+2M\le n/(p-1)+\gamma_\ell=2v(n_{\ell-1}!)\le2m_{\ell-1}$, which is the first event of $B_\ell$. Moreover $D_{\ell-1}+D_\ell\ge1$ forces $M<m_{\ell-1}$.
- *Probability part.* For $i\notin I_A$ the valuation is constant on $A$. For $i\in I_A$, $\mu_A(v\ge s)=p^{m-s}$ when $s\ge m$, and $|I_A\cap[1,n]|\le1+n/p^m$.

Correct. The note's gloss "small only for $n_j$ large enough" reflects the check's Fix 3. The lemma also has a hypothesis on $A$, and the check found that it fails for every tested atom at moderate $n_j$.

**Lemma C5 and Prop N3.**
- *Lemma C5.* Re-derived from the first-nonzero-index decomposition:
  - $y_{j+c}/y_j=\pi_c(x+j)$;
  - $p^K2^{-(j-n)}p^{-V_{N'-j}(x+j)}/2=c_j/(2c_n)$;
  - for $\mathrm{Coll}_D$ the case $j\ge N$ holds automatically, and the terms $c\ge N-j$ are irrelevant.
- *Prop N3.* $S_\delta=1+(y+1)+(y+1)(y+2)=(y+2)^2$ and $\mathbb P(\delta)=2^{-(t+1)}$. For $p^s>t$, $V_t=s+v((t-2)!)$. The lower bound is $(1-p^{-1})p^{v((t-2)!)}2^{-(t+1)}$ per shell.

Both correct.

### 2.2 R3Q: the reduction and the stopped-martingale bound in Theorem 11.7

*From $g_2(x)\ge G$ to populations.*
- Outside $A_1$ (respectively $B_1$), $M_T\le G-T+2$. So $V_T\le T+M_T-2\le G$ by Lemma 1(b); that needs $M_T\ge1$, which holds for even $x$ and $T\ge2$.
- Lemma 2(a) then gives $P_T(x)\ne\emptyset$: truncate a $B$ with $v(S_B)\ge G$ at $T$; the dropped terms have valuation $\ge V_T$.

Correct.

*Uniform slopes (Lemma 3).* Re-derived:
- $C_0$: $V_6=4$, $M_6=2$.
- $C_2$: $(v(x+2),\dots,v(x+8))=(2,1,3,1)$, $V_8=7$, $M_8=3$.
- $C_6$: $(3,1,2,1,\ge4)$, $V_{10}-M_{10}=7$.
- $C_{10}$: $V_6\ge7$.
- $4+8\mathbb Z_2$: $V_4\ge4$.
- Propagation: $v(\pi_j')\ge V_j-M_j\ge V_{n_0}-M_{n_0}\ge\lambda+1$.

The use of the *proof* of Lemma 2(a) in (iv) is correct.

*Prop 7.* Each step checked:
- A non-failing step satisfies Lemma 5's hypotheses for every $e\in Q_n$: $\lambda+D\le\Lambda+D\le V_n-M_n$ and $\lambda\le\Lambda<\beta(n)\le V_n-M_n$.
- Failing steps are contained in the first sum.
- The frozen partition is nested, and failure at step $n$ is decided modulo $2^{V_n}$.
- The martingale step needs Lemma 5(c) and $W_{n+1}=W_n+1-D$. Children of paths of slope $>\Lambda$ keep slope $\ge\Lambda+1$, because $v(\pi'_n)\ge\beta(n)\ge\Lambda+1$; this holds whether or not the step fails.
- $\hat\tau$ is a bounded stopping time: $2^{K_t}\mid x+t$ either forces $V_t\ge K_t$ or is excluded.
- Survival forces weight $\ge2^{-W_\tau}\rho_*$, since $\tau+2\Lambda\le T$.
- The digit split: $s_{\rm lo}$ is $\mathcal F_{n_s}$-measurable because $m_1\le n_s-s(n_s)\le V_{n_s}$, and $\int_C2^{-s_{\rm lo}}=\mu(C)2^{-\ell_0}(3/4)^{m_1-a}$.
- Optional stopping is applied atom by atom with $R$ bounding the initial weight.

Correct.

*Lemma 8 (note Lemma 11.6).* Re-derived:
- the Taylor expansions of $c_0,\dots,c_3$ at $-2=x-h$;
- $c_0=1-e_1$ forces $e_1=1$ and $S^{[3]}(x)$ even;
- $c_1=1-\alpha_0$, $c_2=\alpha_0-\alpha_1$, $c_3=\alpha_1-\alpha_2$;
- $m!\bmod16=1,1,2,6,8,8,0,\dots$;
- $P_m\equiv(h+1)^{\lceil m/2\rceil}h^{\lfloor m/2\rfloor}\pmod2$, so $\alpha_{m,2}$ is odd exactly for $m\in\{2,4,5\}$;
- the chain mod 2, 4, 16 gives $a_2+a_4+a_5$ even, while $\alpha_2$ is odd.

Correct. The multiplicity remark needs $\Omega$ (so that $V_n-2M_n\to\infty$). It covers all of $\mathbb Z_2$: $8\mathbb Z_2$ by Lemma 3(i), $2+4\mathbb Z_2$ by Lemma 8, and no zeros elsewhere.

*Lemma 9, Cor 9′, Prop 10, Thm B, rule $R(K)$.* The window conditions of the rule were re-checked:
- (W2) needs $M\ge2\log_2(13.5M)$, true for $M\ge22$ (the rule has $M\ge37$);
- (W3) needs $n\ge54$;
- the $B_2$ count $\le(n_s+2\Lambda)/16+2\le3.93M+2$;
- the $B_3$ exponent $-2.125M+O(\log M)$.

I did not re-evaluate the nine-term majorant numerically. Two independent evaluators already agree on it (R3Q's `rule_K0.py` and the check's `bounds_check.py`, minimum margin 0.625 bits).

### 2.3 R3F: Theorem 11.17 (A2) and Theorem 11.22 (B5)

*A2(ii).*
- $\langle\delta,\sigma\rangle=\sum_w\delta'_wP_w$ with $\delta'_w=(-1)^{p-1-w}\delta_{p-1-w}$.
- For $u\ge2$, $u\mid u!/w!$ when $w<u$, so $u\mid\delta'_u$, hence $\delta'_u=0$; downward induction.
- $P_1=P_0$ gives $\delta'_1=-\delta'_0$, i.e. $\delta_{p-2}=\delta_{p-1}$ (with $p$ odd).

*A2(iii).*
- $|\langle\delta,\sigma\rangle|\le R_p=\sum_{w<p}(p-1)!/w!=\lfloor e(p-1)!\rfloor$.
- The relation weight is $2^p+2\cdot2^{p-2}=\tfrac32 2^p$.
- $Q_d=p^dA_2(p^d)-p^{d-1}A_2(p^{d-1})$ via $F_p(pu'/p^d)=F_p(u'/p^{d-1})$.

Correct.

*B5.*
- Fact F2 and (H2) give $\sum_{\xi\ne0}|\hat\nu_W|\le\sqrt C\sum_{d\le t+c}N_d2^{-n_d/2}$.
- $n_d=U_d$ for $d\le c_t$, since $U_d\le p^{t-1}-1$ when $d\le v_p((p^{t-1}-1)!)$; and $n_d=p^{t-1}$ for $c_t<d\le t+c_t$.
- $c_{t+1}-c_t=p^{t-1}-1$, so $\tau'_p(t+1)/\tau'_p(t)=(p2^{-(p-1)/2})^{p^{t-1}}<1$ for $p\ge7$.
- Fact F1 gives $\mathrm{Cov}(p,t,p^{t-1})$ for every $t\ge3$, and $p^{t-1}+1<p^t$.
- Theorem 3.12(c) then needs $\mathrm{Cov}(p,1,H_1)$ and $\mathrm{Cov}(p,2,H_2)$ **with $H_t+1<p^t$**. This is in R3F's (H1) and is missing from the note (F2).
- The thresholds $1/(\Lambda'_p+\tau'_p(3))^2=11.73$ ($p=11$) and $41.68$ ($p=13$) were recomputed; $\tau'_{11}(3)\approx2\cdot10^{-5}$ and $\tau'_{13}(3)\approx2\cdot10^{-9}$.

Correct as a conditional theorem.

I also checked B1, B4 and its corollary, B6, B7, C1–C3 and D4(ii) (including $\mathrm{mean}(|\cos|(1-\cos4x))=\tfrac{16}{15}\cdot\tfrac2\pi$); all correct.

## 3. Lemma S0.1 (task item 3): proved, and sharpened

**Statement** (S0 §5). Let $y$ be Haar-random in $\mathbb Z_2$, $D(y,k)=s_2(k)-c(y,k)$ (binary carries), $E_n=\{D(y,k)\ge0,\ 1\le k\le n\}$ and $m=\lfloor\log_2n\rfloor$. Then $(m+2)/2^{m+2}\le P(E_n)\le(m+2)/2^{m+1}$.

**Proof check.**
- *Identification.* $D(y,k)$ is the note's walk $W_k=k-V_k$. By Kummer, $c(y,k)=v_2\binom{y+k}{k}=V_k-(k-s(k))$ for natural $y$, and this extends by continuity.
- *Upper bound.* Let $j=v(y)<m$. If $y_{j+1}=\dots=y_{i-1}=0$, then $k=2^i-2^j<2^i\le n$ gives $i-j$ carries plus $t$ further carries through the 1-run of $y$ starting at bit $i$. So $D=-t$, and $E_n$ forces $y_i=0$. Each event $\{v=j,\ y_{j+1}=\dots=y_m=0\}$ has measure $2^{-(m+1)}$, and $P(v\ge m)=2^{-m}$.
- *Lower bound.* For $j\le m+1$ and $y=2^j+2^{m+2}w$ we have $2^j+k<2^{m+2}$, so $D(y,k)=s(2^j+k)-1\ge0$. The $m+2$ events are disjoint, each of measure $2^{-(m+2)}$.
- The displayed consequences follow from $2^m\le n<2^{m+1}$.

**Correct.**

**Sharpening (new, proved here).** $P(E_{2^m})=(2m+3)/2^{m+2}$ exactly. This is the value S0 conjectured from data.

*Proof.* Let $n=2^m$.
- By the upper-bound argument, $E_n\subseteq\bigcup_{j<m}\{v=j,\ y_{j+1}=\dots=y_m=0\}\cup\{v\ge m\}$.
- If $v(y)=m$, then $k=2^m\le n$ gives $D=-t$, where $t$ is the 1-run of $y$ starting at bit $m+1$. So $E_n$ forces $y_{m+1}=0$.
- Conversely, each of the following events lies in $E_n$:
  - $\{v=j<m,\ y_{j+1}=\dots=y_m=0\}$: there $y=2^j+2^{m+1}z$ and $2^j+k<2^{m+1}$;
  - $\{v=m,\ y_{m+1}=0\}$;
  - $\{v\ge m+1\}$: no carries.
- Their measures are $m\cdot2^{-(m+1)}+2^{-(m+2)}+2^{-(m+1)}=(2m+3)/2^{m+2}$. ∎

**Numerics** (`s0_lemma.c`, exact, no sampling). Write $y=Y+2^LH$ with $L=\lfloor\log_2n_{\max}\rfloor+2$.
- Every carry out of the window runs through the *same* 1-run $t$ of $H$, with $P(t\ge r)=2^{-r}$. So $P(E_n\mid Y)\in\{0,1,1-2^{-(d+1)}\}$, and $P(E_n)$ is an exact dyadic rational.
- For **all** $1\le n\le2^{18}$:
  - 0 violations of either bound;
  - $\min P/\text{lower}=1.0526$ and $\max P/\text{upper}=0.9750$;
  - $P(E_{2^m})=(2m+3)/2^{m+2}$ exactly for every $m\le18$.
- `s0_walk_mc.py`: on 4000 random 300-bit 2-adic $y$ and $k\le512$, $W_k=k-\sum_{i\le k}v_2(y+i)$ equals $D(y,k)$ in all cases (0 mismatches). The Monte Carlo $P(E_n)$ agrees with the exact values within sampling error.

So the note may label Lemma S0.1 [proved; checked by the round-3 logic referee] and state the bounds explicitly.

The heuristic built on it is unaffected; its open step is unchanged. That step is an AGKV-type comparison of $\delta_G(2)$ with this walk probability (F9).

## 4. Independent definition-level test of R3M's second-moment machinery

R3M's Props B and C2 had one checker. I therefore wrote `c2_test.py`, which uses none of R3M's structural lemmas:
- slope-0 populations at $n$, $N$ and $N'$ are found by a DFS over all 0/1 words, from the definitions of "alive" and "slope", so the inheritance of Prop A(i) is *tested*, not assumed;
- the cylinder $x_0+p^m\mathbb Z_p$ is sampled exhaustively over $w\bmod p^{D+D'}$, with fresh random digits above $m+D+D'$;
- $\varepsilon$ is computed from the composite window's collision counts.

All comparisons are in exact rationals.

| test | cylinders | result |
|---|---|---|
| Cor A′ ($L=0$), over one and two windows: $\mathbb E_C c_NZ^0_N=\mathbb E_Cc_{N'}Z^0_{N'}=c_nZ^0_n$ | 285 | 285/285 exact |
| Prop B(ii): $\mathbb E_C(c_NZ^0_N)^2-(c_nZ^0_n)^2\le\chi_W^2(c_nZ^0_n)^2$ | 285 | 285/285; **equality in 110/110 single-parent cases** |
| Prop C2 under (5.2) | 285 (40 of them trivial, with $D'=0$) | 285/285; **equality in 110/110 single-parent cases** (90 with $D=D'=1$, 20 with $D=1$, $D'=3$); max ratio LHS/RHS over the 135 multi-parent non-trivial cases 0.833 |
| Prop N: $\chi_W^2\ge(p-1)4^{-p}$ | 285 | 285/285 |
| populations and valuations independent of the digits above $m+D+D'$ | 285 | 285/285 |

Coverage: $p=3$ ($n=8$–$24$, window lengths 2–6) and $p=5$ ($n=20$, length 5; multi-parent only). At $p=7$ no tested sample at $n=14$ satisfied (5.2), and the $n=21$ run was too slow in Python; it was stopped and gives no result. The test is therefore independent but narrower than the checker's. It confirms the constant, the frequency band and the fibre identification of Prop C2 exactly in the single-parent case.

## 5. Round-3 edits outside §11, and the status lines (task item 4)

- **Status lines** (lines 14–16, §11.0 item 6, §11.6). Q3 is OPEN, and Q1 is open in general, with the right qualifiers: finiteness for $a\le32768$ and density 1 at $p=2$, nothing new at odd $p$. **No overstatement.** Two label gaps (F14):
  - line 14 cites Theorem 11.7 with no label;
  - §11.6's "Each of the following would suffice" needs the certified $\mathrm{Cov}(p,1,\cdot)$, $\mathrm{Cov}(p,2,\cdot)$ inputs for RMF and for Theorem 11.22 (F2).
- **§0 items 19–23.**
  - Items 19, 20 and 22 match §11, apart from the "rate is $G^{-1/7}$" wording (F14).
  - Item 21's bracket asserts "of barrier type" without a label (F1).
  - Item 23 is the R3C placeholder (not reviewed).
- **§2** (line 253): consistent. Line 252 still says the two fits are not reconciled, with no pointer to §11.1 (F15).
- **§5** (line 763): consistent with Theorem 11.4.
- **§8** (lines 954–960): consistent with §11.0. The S0 gate plus five research tracks match "six tracks".
- **Remarks 10.8.**
  - Item 4 is updated correctly.
  - Item 2 (line 1250) was not changed although S0 flagged it, and §11.6 item 4 now cites it for the opposite statement (F7).
  - Item 5 is consistent.
- **§10.5** (line 1587), **§10.6** (lines 1630, 1655): consistent.
- **README.md** still describes the state after round 2 ("$a=594$ is still a live test case"). This is outside the note, but it must be updated with the note (F16).

## 6. Findings

All findings are **minor**. None affects a proof, and none changes a main claim. They are listed roughly in order of importance.

**F1 (minor; label upgrade). "FE is of barrier type" is stated as fact.**
- Where: line 124 (§0 item 21: "[proved; FE unproved, of barrier type, …]"), line 1858 ("FE is unproved and is of barrier type"), and line 2022 ("FE is of barrier type, in the sense of Theorem 3.10. … so a proof must use unboundedly many digits of the unit parts").
- R3M §6 gives this explicitly as "the mechanism of Theorem 3.10, stated here heuristically and not as a proved claim". The R3M check did not examine it.
- The B6-type support count does not settle it. With unit parts truncated to $c$ digits, the composite window's subset sums lie in $[0,X]$ with $X\lesssim p^{w_{\max}+c+2}$, where $w_{\max}=V_{N'-1}-V_n$. That gives only $\varepsilon\gtrsim\tfrac{p-1}2p^{\,v(x+N')-c-2}-p^D\mathrm{Coll}_D$, which is large only when the composite window *ends* at a gate of depth $>c+2$. Whether FE then fails in the truncated model depends on how often $x+n_{\ell+1}$ is such a gate. That is plausible, but not shown.
- **Fix.**
  - Line 124: "[proved; FE unproved; heuristically of barrier type; numerically …]".
  - Line 1858: "FE is unproved and, heuristically, of barrier type."
  - Line 2022: "*Relation to the obstructions [heuristic].* FE appears to be of barrier type in the sense of Theorem 3.10 (R3M §6 gives the mechanism, not a proof). It concerns …, so a proof very probably must use unboundedly many digits of the unit parts."

**F2 (minor; dropped hypothesis and incomplete reason). Theorem 11.22.**
- Where: line 2064. The hypothesis reads "Suppose $\mathrm{Cov}(p,1,H_1)$ and $\mathrm{Cov}(p,2,H_2)$ hold". R3F B5 (H1) also requires $H_t+1<p^t$, and Theorem 3.12(c) needs it. The analogue for Theorem 10.16 was restored in round 2.
- "The budget condition can hold only for $p\ge11$, since $\Lambda'_7>1$." The constant $C$ is free, and a $C<1/\Lambda_7'^2\approx0.24$ is not excluded by $\Lambda'_7>1$ alone. The conclusion is still true:
  - by Prop 11.21 the levels $d\le t-1$ of every window equal the factorial-measure shells;
  - R3F B3 certifies $Q_{\rm fact}(8)/(N_82^{-U_8})=2.47$ at $p=7$;
  - so (H2) forces $C\ge2.47$ once $t\ge9$, and then $\sqrt C\Lambda'_7>3$.
- Line 2101–2104 (§11.6), "Each of the following would suffice", omits the $\mathrm{Cov}(p,1,\cdot)$, $\mathrm{Cov}(p,2,\cdot)$ inputs for RMF and for Theorem 11.22.
- **Fix.**
  - Line 2064: "Suppose $\mathrm{Cov}(p,1,H_1)$ and $\mathrm{Cov}(p,2,H_2)$ hold with $H_t+1<p^t$ (certified for $p=7,11,13$, §10.2)."
  - Replace "since $\Lambda'_7>1$" with "since $\Lambda'_p=\infty$ for $p=3,5$; at $p=7$, $\Lambda'_7=2.0496$, and the certified factorial-measure level $d=8$ (ratio 2.47, R3F B3) forces $C\ge2.47$ via Prop 11.21, so $\sqrt C\Lambda'_7>1$".
  - In §11.6 add "(each together with $\mathrm{Cov}(p,1,\cdot)$, $\mathrm{Cov}(p,2,\cdot)$ with $H_t+1<p^t$, certified for $p=7,11,13$)" after the RMF and Theorem 11.22 items.

**F3 (minor; verification overstated). §11.0, Kitamura's 594 ladder.**
- Where: line 1850, "It also re-checked … and the first four rungs for $a=594$. Everything agrees."
- S0 §2.5 checked $g_2(594)\ge1024,2048,4096,8192$. Kitamura's ladder is $8192,16384,32768,65536$, so S0 checked only its first rung. S0 says explicitly: "The rungs $G\ge16384$, and so the published bound 66126, have not been reproduced independently" (S0 headline 3, Open issue 1). Theorem 11.2 has since superseded the question, but the sentence misreports what S0 verified.
- **Fix.** "…, and the lower rungs $g_2(594)\ge1024,2048,4096,8192$ (only the first of Kitamura's four rungs; the higher rungs were not reproduced by S0, and are superseded by Theorem 11.2). Everything checked agrees."

**F4 (minor; label upgrade). (d) is labelled [proved].**
- Where: lines 2074–2076. The second bullet, "On the computed tail shells, all of the deviation from the random model is aliasing ($j\ne0$)", is R3F's D2. R3F labels D2 "[computer-assisted illustration]": $\Psi(0)$ is computed in floating point with truncated carries and is not interval-certified. The R3F check confirms it only "as an illustration".
- **Fix.** Split the label: "**(d) The factorial-base transfer picture [D1, D4 proved; D2 a floating-point illustration].**" Append "[computer-assisted illustration; floating point, not interval-certified]" to the second bullet.

**F5 (minor; misstatement). Theorem 11.7, the closed-form check.**
- Where: line 1958, "a check that a closed-form majorant built from nine explicit terms is $\le-K/80$ for every $K\in[2400,4\cdot10^6]$. The largest failing $K$ is 3071". The sentence contradicts itself: it holds on $[3072,4\cdot10^6]$, not on $[2400,\dots]$. Also, the majorant is $\le2^{-K/80}$; it is not $\le-K/80$.
- **Fix.** "a check that a closed-form majorant built from nine explicit terms is $\le2^{-K/80}$ for every $K\in[3072,4\cdot10^6]$ (scanned on $[2400,4\cdot10^6]$; the largest failing $K$ is 3071, and the minimum margin on $[3072,4\cdot10^6]$ is 0.62 bits)."

**F6 (minor; unlabelled consequence). After Prop 11.15.**
- Where: line 2020, "So FE cannot be obtained by Markov's inequality on $\mathbb E[\varepsilon_\ell]$." Prop 11.15(b) is a statement about $\int_{\mathbb Z_p}\Lambda_t$. But $\varepsilon$ is a *signed* combination of $\Lambda$'s (Lemma C5), and FE concerns $\mathbb E_A$ on atoms where $M_{n_{\ell+1}}<m_{\ell-1}$. The R3M check (Fix 5) asks for [heuristic] on exactly these consequences.
- **Fix.** "So FE very probably cannot be obtained by Markov's inequality on $\mathbb E_A[\varepsilon_\ell]$, and a truncation at deep gates is needed first [heuristic: $\int\Lambda_t=\infty$ does not by itself give $\mathbb E_A[\varepsilon_\ell]=\infty$]."

**F7 (minor; inconsistency created by round 3). Remark 10.8.2 versus §11.6 item 4.**
- Where: line 1250 says "For natural $x$, $W_n=s(n)-c(x,n)$ … It is bounded above by $\log_2n+1$, and it tends to $-\infty$ along record times." S0 (headline 6; Open issue 2) showed that for natural $x$, $W_n=s_2(x+n)-s_2(x)\ge1-s_2(x)$ is bounded below. The sentence was not changed. Line 2112 now cites "Remark 10.8.2; S0" for the boundedness below.
- **Fix.** In Remark 10.8.2 replace the sentence with: "It is bounded above by $\log_2n+1$. For $x\in\Omega$ it tends to $-\infty$ along record times (G1). **[Round 3]** For natural $x$, $W_n=s_2(x+n)-s_2(x)\ge1-s_2(x)$ is bounded below (S0), which is why Theorem 10.1 says nothing about integers."

**F8 (minor; checking claim overstated). S0 was never adversarially checked.**
- Where: line 11 ("Each round-3 track was checked by a separate AI instance with its own code") and line 1818 ("Every result below was checked in two stages: an adversarial check of each track…"). Line 120 is accurate, since items 19–22 come from checked tracks. There is no `data/round3/checks/S0.md`, and line 1926 itself says Lemma S0.1 is "not separately checked". S0's computations (S0.R1–R3) and Lemma S0.1 have no check by a separate instance; this report now checks Lemma S0.1 (§3).
- **Fix.**
  - Lines 11 and 1818: "Each research track (R3N, R3Q, R3M, R3F, R3C) was checked …; the status gate S0 was not, except that its Lemma S0.1 was checked by the logic referee (§11.8)."
  - Line 1926: "[proved by S0; checked by the round-3 logic referee, who also proved $P(E_{2^m})=(2m+3)/2^{m+2}$ exactly]". State the explicit bounds $\frac{\log_2n+1}{4n}<P(E_n)\le\frac{\log_2n+2}{n}$.

**F9 (minor; muddled open problem). §11.6 item 3.**
- Where: line 2111, "A proof that the odometer-environment survival probability behaves like $(\log n)/n$ (Lemma S0.1, heuristically) would be a natural route." Lemma S0.1 *proves* that the environment walk stays $\ge0$ with probability $\asymp(\log n)/n$. What is unproved is the AGKV-type comparison of $\delta_G(2)$ with that probability.
- **Fix.** "Lemma S0.1 proves that the environment walk stays $\ge0$ up to time $n$ with probability $\asymp(\log n)/n$. A comparison of AGKV type between $\delta_G(2)$ and this probability, not proved here because offspring are dependent and the environment is not i.i.d., would give $\delta_G(2)\asymp(\log G)/G$."

**F10 (minor; withdrawn remark survives). Prop 11.11.**
- Where: line 2000, "This is exactly the independence that the classical survival criteria … assume and that fails here." The R3M check (Fix 2) showed that two functions of one uniform $w$ can be independent, and the note says the "never independent" remark is withdrawn.
- **Fix.** "…assume, and which is not guaranteed here: the identity measures the dependence exactly."

**F11 (minor; hypotheses dropped in transcription).**
- (a) Prop 11.13 (lines 2004–2006) states the inequality with no hypothesis and with an unspecified $\mathbb E$. *Fix:* "On a cylinder $C=x+p^{V_n(x)}\mathbb Z_p$, under $D+D'\le V_n(x)-M_{N'}(x)$ and $M_{N'}(x)<V_n(x)$ ((5.2) of the report): $\mathbb E_C[\cdots]-\mathbb E_C[\cdots]\le\varepsilon(W,W')(c_nZ^0_n)^2$."
- (b) Theorem 11.14 (line 2008), "Fix deterministic window times": the partition into atoms needs $n_0\ge2p$. *Fix:* "Fix deterministic window times $2p\le n_0<n_1<\cdots$".
- (c) Line 1947, "A one-step martingale identity for every slope $\lambda$, valid under $\lambda+v(x+n+1)\le V_n-M_n$": R3Q Lemma 5 also needs $\lambda<V_n-M_n$, which is not implied when $v(x+n+1)=0$. *Fix:* "valid under $\lambda+v(x+n+1)\le V_n-M_n$ and $\lambda<V_n-M_n$".

**F12 (minor; program count). Theorem 11.19.**
- Where: line 2046, "[computer-assisted; two shell programs plus the checker's arb-certified third program at every computed level; …]". At $p=13$, $d=9$ only `gate_d` and the checker's `shellchk` exist; only 2 of the 6 `ivshell` chunks were run (R3F A5; check §2). The levels computed only beyond the analytic threshold (e.g. $p=5$, $d=11,12$) have one program, but they are not needed.
- Also, "For every gate block of every level, $\sup_d\rho_d$" should say $\sup_{d\le j+1}$, since the shells are level-independent only there (Lemma 11.16).
- **Fix.** "[computer-assisted; at least two independent programs at every level that is used (three except at $p=13$, $d=9$: `gate_d` and the checker's arb-certified `shellchk`); …]", and "$\sup_{1\le d\le j+1}\rho_d$".

**F13 (minor; rounding direction). Prop 11.21 data.**
- Where: line 2062. The totals "0.286" and "0.00830" are certified *upper* bounds (0.28644 and 0.0083017 in R3F B4-data; the check's own values are 0.286433 and 0.00830168), and they are rounded down. The R3Q check required upper bounds to be rounded up; the same rule applies here.
- **Fix.** "0.2865 ($p=7$, $d\le9$), 0.0668 ($p=11$, $d\le7$) and 0.00831 ($p=13$, $d\le7$)".

**F14 (minor; label and wording consistency for the $p=2$ rate).**
- Line 14: "(Theorem 11.7)" → "(Theorem 11.7, computer-assisted)".
- Line 123: "On the classes … the rate is $G^{-1/7}$" → "On each of the classes …, $\mu(C\cap\{g_2\ge G\})\le2^{1/7}G^{-1/7}$ for $G\ge2^{1024}$ [computer-assisted]".
- Line 1973: "That is a proved analogue" → "That is a computer-assisted analogue" (matching the relabelling the check required).
- Line 1969: "is where the bound first beats" → "is the first evaluated $G$ ($\log_2G$ was evaluated in steps of 64 there) at which the bound beats". R3Q evaluated $G=2^{384}$ and $2^{448}$ only, not the values in between.

**F15 (minor; stale text). §2, line 252.** "Kitamura's fit $\approx11.5/G$ and the fit $\delta_G(2)\approx0.7/\sqrt G$ of §5 differ. We have not reconciled them" now conflicts with §11.1, which reconciles them heuristically. *Fix:* append "**[Round 3]** §11.1 gives a heuristic reconciliation: $0.7/\sqrt G$ appears to be a small-$G$ effect, and the integer data and a re-fit of the published values suggest $c/G$, possibly with a $\log G$ factor."

**F16 (minor; outside the note). README.md** still reads "Status after round 2 (2026-10-12)", says that $a=594$ is still a live test case, and has no round-3 section. *Fix:* update the status bullets and add a round-3 table that mirrors §0 items 19–23 with the same labels.

**F17 (minor; nits).**
- Line 1993: "The exact state-by-state tests by two programs found 0 failures in 62132 identities" → "…by two programs (62132 identities for program A and 512 parents for program B) found 0 failures".
- Line 1922: "$\delta_G\,G/\log_2G\in[0.61,0.69]$" → "$[0.607,0.693]$" (S0's table: 0.607 at $G=16$, 0.693 at $G=128$).
- Line 1926: "In i.i.d. environments the corresponding probability is $\asymp n^{-1/2}$ (Kozlov; AGKV)". That a zero-mean finite-variance walk stays $\ge0$ with probability $\asymp n^{-1/2}$ is classical fluctuation theory (Sparre Andersen, Spitzer). Kozlov and AGKV relate the *BPRE survival probability* to it. Suggest: "(classical; for BPRE survival, Kozlov and AGKV)".

## 7. What I confirm

- Every [proved] statement of §11 that I re-checked is correct as stated in its track report: Props 11.10–11.13, Theorem 11.14, Lemma C4, Prop 11.15, Lemma 11.6, R3Q's Prop 7 and the reduction of Theorem 11.7, Theorem 11.17 and Theorem 11.22. The note's versions are correct once F2 and F11 are applied.
- The computer-assisted statements of §11.1, §11.2 and §11.4 carry the same constants as the reports and checks. Every rounded upper bound in Corollary 11.8 rounds up.
- Lemma S0.1 is correct. Its exact value at $n=2^m$ is $(2m+3)/2^{m+2}$, proved here and verified exactly for $m\le18$ and for all $n\le2^{18}$ against the bounds.
- No statement in the note claims progress on Q3, or finiteness of $f(a,p)$ beyond what is proved or certified.

*This report was produced by an AI referee instance in round 3. It has not been checked by a human.*
