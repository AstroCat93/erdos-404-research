# Obstruction-and-scope checks of round-4 track M4A (Theorem M and Corollary M′)

This file has two parts, both made by the `verify_M4A_obstruction` track of round 4 under the lens OBSTRUCTIONS AND SCOPE.

- **Part I** checks Theorem M, $\mu(K_7)>0$. Verdict: **confirmed-with-fixes**, (F1)–(F6).
- **Part II** checks Corollary M′, $\mu(K_p)>0$ for $p=11,13,17,19,23$. Verdict: **confirmed-with-fixes**, (G1)–(G6).
  - The conclusion holds. The argument respects every listed obstruction at each of the five primes.
  - It assumes no deterministic covering or equidistribution statement of barrier type.
  - Three of the five stated lower bounds ($p=11,13,23$) are rounded up and must be rounded down, to $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$ and $2.06\cdot10^{-1}$ (G1).
  - The phase-4 truncation is necessary at every $p$ (G2).
  - "The rate is positive for $p\ge7$" is verified only at finitely many primes (G3).

# Part I. Obstruction-and-scope check of Theorem M ($\mu(K_7)>0$)

Date: 2026-10-14. Lens: OBSTRUCTIONS AND SCOPE. Made by the `verify_M4A_obstruction` track of round 4.

- **Checked:** `data/round4/reports/M4A.md`, mainly the headline, §6 (Theorem M), §7 ("How the proof respects each obstruction") and §8. I also read `code/round4/M4A/fe_verify.py` and `bounds.py`, and the log `data/round4/M4A/fe_verify_final.log`.
- **Obstructions re-read:**
  - in note.md: Theorem 3.6 (with Theorem 3.2), Theorem 3.10, Corollary 10.20 and Propositions 11.12, 11.15, 11.23 and 11.24;
  - in R3M's report: §5 (Theorem C3, Lemmas C4–C5, Proposition N3) and §6;
  - in R3F's report: Propositions B6 and B7 (the $L^2$ barrier and the $L^2$ renormalisation);
  - the round-4 brief.
- **Also read:** `data/round4/checks/M4A_logic.md` (the logic check), so as not to repeat its line-by-line audit.
- **Code:** `code/round4/verify_M4A_obstruction/`, i.e. `vo_lib.py`, `atom_scope.py`, `obstr_tests.py`, `phase_contrast.py` and `run.sh`.
  - All exact values come from this track's own code.
  - M4A's `bounds.py` is imported read-only, and only to evaluate the bounds under test.
  - M4A's `fe_verify.py` was run read-only for one robustness variant (§3).
- **Logs:** `data/round4/verify_M4A_obstruction/*.log`. Each run starts with `=== command:` and ends with `=== exit:`.
- **Budget:** about 1 core-minute in total, at `nice -n 10`. The longest job took 16 s.

**The claim checked (Thm M, status [computer-assisted]).**
- Let $p=7$, $n_0=300$, $n_{\ell+1}=\lceil27n_\ell/20\rceil$, $x_A=8482778585152010705975786324668215228635086$ and $A=x_A+7^{51}\mathbb Z_7$, where $V_{300}(x_A)=51$.
- $A$ is an admissible atom.
- FE of R3M Theorem C3 holds, with $\Pi_A\le10^{25.7344}$, $\delta_A\le1.0006\cdot10^{-45}$ and $\Pi_A\delta_A\le10^{-19.265}$.
- Hence $\mu(K_7\cap A)/\mu(A)\ge1.843\cdot10^{-26}$, and $\mu(K_7)\ge1.843\cdot10^{-26}\cdot7^{-51}>0$.

## Headline

**Verdict: confirmed-with-fixes.** Theorem M respects every obstruction on the list. For each one I can name the step that gets past it, and an exact test exercises that step.

**No hidden deterministic statement of barrier type.** Theorem M does not assume a deterministic covering or equidistribution statement of that type (§2.6):
- the only deterministic $L^2$ bounds it uses are pattern-specific numbers for nine windows;
- those numbers grow, as Propositions 11.23 and 11.24 force (§2.4–2.5);
- all of the decay comes from M4A's Theorem 1, an exact Hensel identity under Haar measure on a ball (re-tested here, 14/14 exact, 14/14 negative controls fail).

**Scope.** The claim states exactly what is proved: one prime ($p=7$), one explicit atom, and no open hypothesis. It does rest on note Theorem 11.14 (R3M Theorem C3) from round 3, and on interval arithmetic. All the numbers reproduce. Nothing in the claim itself is overstated. Its constant is in fact conservative: M4A's own script gives $1.45\cdot10^{-9}$ in place of $1.843\cdot10^{-26}$ when it switches to Markov two windows earlier (§3).

**Fixes.** All of them are to M4A's wording; none changes a number or the conclusion.
- **(F1)** The headline says the proof "uses no truncation beyond working on one atom". This is wrong for Theorem M. Without a truncation the mean is infinite: $\mathbb E_A[\varepsilon_{307}]=+\infty$ (Proposition O1 below, proved). So phase 4's event $G'$ is mathematically necessary, not cosmetic.
- **(F2)** "This proves (S)" should be qualified. The normalised high-slope mass is unbounded over cylinders (Remark O2, proved). So (S) holds only in the gate-pattern-dependent form of Lemma Q, and that form is what Theorem M uses.
- **(F3)–(F6)** Smaller wording points, listed in §4.

## 1. Results of this check

| # | statement | status | evidence |
|---|---|---|---|
| S1 | $V_{300}(x_A)=51$; the stored path has $v_7(S_e(x_A))=51$ and $S_e'(x_A)\equiv6\pmod7$, so $Z^0_{300}\ge1$ on $A$; $M_{405}=4$, $D_0=17$, and $W_0$ satisfies (W2′), (W3′) | computer-assisted (own exact code) | `atom_scope.log` |
| S2 | $i_A=4106476713379874320366176059319330216123657$; every composite window $\ell\le306$ ends below $i_A$, with maximal depth $\le50$; the linear regime holds for all of them; max depth is 4 in phase 1 and 5 in phase 2 | computer-assisted | `atom_scope.log` |
| S3 / **Prop O1** | the window $\ell^*=307$ has $i_A$ in its second half, and the untruncated $\mathbb E_A[\varepsilon_{307}]=+\infty$ | **proved** (the data are exact integers) | §2.3, `atom_scope.log` |
| S4 | $(1-\sqrt{\Pi\delta})^2/\Pi\ge1.84332\cdot10^{-26}\ge1.843\cdot10^{-26}$, and $\mu(K_7)\ge1.464\cdot10^{-69}$ | computer-assisted (arithmetic) | `atom_scope.log` |
| **Remark O2** | the normalised high-slope mass $G(u;t,k,f)$ is unbounded over $u$, and its first moment over a cylinder where $v(u+2)$ is not frozen is infinite | **proved** | §2.4, T5 |
| T1 | Prop 11.12's floor holds for every single window; the composite $\varepsilon$ falls below it in 220/1080 cases | computer-assisted (exact) | `floor.log` |
| T2 | for a gate at distance 2 in the second half, $\varepsilon\approx\kappa p^s$; Prop D dominates and grows like $p^s$ | computer-assisted (exact) | `shadow.log` |
| T3 | exact $q_s$ and $P_0$ at $p=3,\dots,13$; $q_1>1$ and $q_2/p<1$; only $g=2$ has an exact zero | computer-assisted (exact enumeration) | `consts.log` |
| T4 | on balls with a frozen pattern, Prop D $-1\ge\sup_B\varepsilon$ and Prop E $\ge\mathbb E_B\varepsilon$ | computer-assisted (exact) | `ball.log` |
| T5 | the high-slope mass at $v(u+2)=s$ grows by about a factor $p$ per unit of $s$; the path bound and Lemma Q both hold | computer-assisted (exact) | `nonuniform.log` |
| T6 | M4A Theorem 1 holds exactly on frozen balls containing a gate of the maximal frozen depth; negative control $\theta+1$ fails | computer-assisted (exact) | `thm1.log` |
| PC | on the atom: the pointwise Prop D $-1$ grows from $10^{0.21}$ to $10^{14.40}$ ($\ell=1..10$), while Prop E falls to $10^{-45.30}$ ($\ell=9$) | computer-assisted (exact rationals) | `phase_contrast.log` |

## 2. Obstruction by obstruction

### 2.1 Theorem 3.6 ($K_p$ has empty interior; no residue-class criterion)

- **What the theorem forbids.** No property of $a$ that depends only on $a\bmod p^{k_0}$ can imply $f(a,p)=\infty$. By Theorem 3.6(a), every class, $A$ included, contains infinitely many natural $a$ with $f(a,7)<\infty$. $K_7$ is closed (note §1.3: it is $\bigcap_G\{x:\exists B\subseteq[1,pG),\ p^G\mid S_B(x)\}$), so $A\setminus K_7$ is a nonempty open set.
- **How Theorem M respects it.**
  - The only residue-class property used is admissibility: $Z^0_{300}\ge1$ on $A$. It seeds the population and nothing more.
  - Membership in $K_7$ is shown only on the event $\{Y>0\}$ of C3, whose measure is bounded below, by $1.843\cdot10^{-26}\mu(A)$, not shown to be all of $A$.
  - The small $\delta_A\approx10^{-45}$ is the probability that the *window conditions* fail. It is not the probability of extinction: on $\{\tau=\infty\}$ the population may still die.
  - So the claim is a fat-Cantor-set statement and is consistent with Theorem 3.6.
- **Q3 is untouched.** $x_A$ is a natural number, but nothing is claimed about $x_A$ or any other integer.
- **Verdict:** evaded correctly; nothing to fix.

### 2.2 Proposition 11.12 (per-window Cauchy–Schwarz fails: $\chi^2_W\ge(p-1)4^{-p}$)

- **How Theorem M respects it.** C3's $L^2$ recursion pays the single-window $\chi^2$ once, as $1+\chi^2_0\le1.5046$. Every later window pays the composite band mass $\varepsilon_\ell$, i.e. the $L^2$ mass of $[n_{\ell-1},n_{\ell+1})$ in the band $(p^D,p^K]$ (R3M Proposition C2). The floor of Proposition 11.12 comes from the mod-$p$ shell of a single window, and that shell is not in the band.
- **Test T1** (exact, $p=3,5,7$, 1080 composite windows):
  - no single-window $\chi^2$ falls below the floor. At $p=3$ the minimum equals the floor exactly, $1/32$, so Proposition 11.12 is sharp there.
  - the composite $\varepsilon$ falls below the floor in 220/1080 cases. The minimum at $p=7$ is $1.75\cdot10^{-6}$, against a floor of $3.66\cdot10^{-4}$.
- **Verdict:** evaded correctly, by R3M's Theorem C3, which M4A uses unchanged.

### 2.3 Proposition 11.15(b) (R3M Prop N3: $\int_{\mathbb Z_p}\Lambda_t\,d\mu=\infty$)

**How Theorem M respects it.**
- **Phases 1–3 ($\ell\le306$).** Every composite window ends below $i_A$ (S2). So every valuation in it is that of $x_A$, at most 50, and frozen on $A$. Then $\varepsilon_\ell\le p^{K_\ell}$ with $K_\ell$ constant, so $\mathbb E_A[\varepsilon_\ell]<\infty$ trivially. A deep gate at a fixed position is priced deterministically: $P_0(2,s)=\tfrac14$ times $p^s$, and $q_d\approx p^d$.
- **Phase 4 ($\ell\ge307$).** The random gates at $I_A=i_A+7^{51}\mathbb N_0$ are truncated by $G'$, at cost $\le2.47\cdot10^{-94}$. Markov is then applied to $\mathbb E_A[\varepsilon_\ell\mathbf 1_{G_\ell}]=\sum_B\mu_A(B)\,\mathbb E_B[\varepsilon_\ell]$, over balls with a frozen pattern.

The truncation is not optional, as the following shows.

**Proposition O1 (the untruncated phase-4 mean is infinite) [proved].** Let $\ell^*=307$, $n=n_{306}$, $N=n_{307}$, $N'=n_{308}$ (exact values in `atom_scope.log`). Let $\varepsilon_{\ell^*}(x)=p^{K(x)}\mathrm{Coll}_K(x)-p^D\mathrm{Coll}_D(x)$ for $x\in A$, as in M4A §1, with no truncation and no linear-regime restriction. Then $\mathbb E_A[\varepsilon_{\ell^*}]=+\infty$.

*Proof.*
1. *Valuations.* By S3, $N<i_A<N'$ and $i_A+7^{51}>N'$, so $I_A\cap[1,N']=\{i_A\}$. For $i\le N'$ with $i\ne i_A$, we have $i\notin I_A$, so $v(x_A+i)\le50$. Since $x+i\equiv x_A+i\pmod{7^{51}}$, it follows that $v(x+i)=v(x_A+i)$. Hence the following are constant on $A$:
   - $D=V_N-V_n$;
   - $a_c=V_{n+c}-V_n$ for $n+c<i_A$;
   - $K_0:=K(x)-s(x)$, where $s(x):=v(x+i_A)$.
2. *Law of $s$.* $x+i_A=(x_A+i_A)+7^{51}w$ with $w$ Haar-distributed and $7^{51}\mid x_A+i_A$. So $\mu_A(s=51+t)=\tfrac67\,7^{-t}$ for $t\ge0$.
3. *A colliding path.* Let $c=i_A-2-n$. Then $c\ge0$ and $c+2=i_A-n\le H-1$. For $\sigma=\pm1$ let $\delta^\sigma$ have $\delta_c=\delta_{c+1}=\delta_{c+2}=\sigma$ and all other entries $0$. With $u=x+n+c$ we have $y_{c+1}=y_c(u+1)$ and $y_{c+2}=y_c(u+1)(u+2)$, so
   $$S_{\delta^\sigma}(x)=\sigma y_c\,(1+(u+1)+(u+1)(u+2))=\sigma y_c(u+2)^2=\sigma y_c\,(x+i_A)^2 .$$
   Hence $v(S_{\delta^\sigma})=a_c+2s$. Moreover $P(\delta\in\{\delta^+,\delta^-\})=2\cdot4^{-3}\cdot2^{-(H-3)}=2^{-(H+2)}$.
4. *Lower bound for $\varepsilon$.* If $s\ge s_0:=\max(51,K_0-a_c)$, then $a_c+2s\ge K_0+s=K$, so $\mathrm{Coll}_K\ge2^{-(H+2)}$. Since $\mathrm{Coll}_D\le1$, $\varepsilon(x)\ge7^{K_0+s}2^{-(H+2)}-7^D$.
5. *Conclusion.* $\varepsilon\ge0$ everywhere (it is an $L^2$ band mass). So
   $$\mathbb E_A\varepsilon\ \ge\ \sum_{s\ge s_0}\tfrac67\,7^{51-s}\big(7^{K_0+s}2^{-(H+2)}-7^D\big)=\sum_{s\ge s_0}\tfrac67\,7^{51+K_0}2^{-(H+2)}\;-\;(\text{a finite sum})=+\infty. \qquad∎$$

The data are $H\approx1.886\cdot10^{42}$ and $s_0\approx1.21\cdot10^{40}$; each term of the divergent sum is about $10^{-3.02\cdot10^{41}}$. The divergence lives at absurd depths, but it rules out applying Markov to the untruncated mean.

Two truncations are available, and either suffices:
- M4A's $G'$;
- the linear-regime clause of C3's own stopping time, which forces $s\le m_{\ell^*-1}-K$ on $\{\tau>\ell^*\}$.

**Test T2** (exact; $p=3,5,7$; five windows with a gate at distance 2 in the second half; $s$ up to 9):
- $\varepsilon(x_s)/p^s$ settles at a positive constant: $\approx0.053$ at $p=3$, $0.005$–$0.02$ at $p=5$, and $0.001$–$0.003$ at $p=7$;
- so the partial sums $\sum_s\mu(\text{depth}=s)\,\varepsilon$ grow linearly in the truncation level;
- the rigorous lower bound holds in every case, and turns positive once $s\ge K_0-a_c$ (for example $s\ge7$ at $p=3$).

**Verdict:** evaded correctly. Fix (F1): M4A's headline should say that phase 4 needs the truncation, and why (Proposition O1).

**Note for note.md.** The heuristic after note Proposition 11.15(b), "FE very probably cannot be obtained by Markov's inequality on $\mathbb E_A[\varepsilon_\ell]$", should be qualified:
- on an atom, $\mathbb E_A[\varepsilon_\ell]$ is finite for every window that ends below the first random-depth position;
- M4A obtains FE by Markov exactly there;
- it is infinite (Proposition O1) for a window whose second half contains such a position.

### 2.4 Barrier lemmas (Theorem 3.10; Proposition 11.23 = R3F Proposition B6)

**What they forbid.** A *deterministic* covering or $L^2$ bound that uses the valuations and only $c$ digits of the unit parts must be at least $\tfrac{p-1}2p^{j-c-1}-1$ for a run ending at a gate of level $j$. So a bound that is uniform in the depth needs unboundedly many digits.

**The deterministic bounds in Theorem M.** These are Prop D for $W_0$ and for $\ell=1,\dots,8$, and nothing else. They are not uniform in the depth:
- a block whose end gate has depth $d$ costs $q_d=p^d\max_zP(Z\equiv z\bmod p^d)$, with $q_d/p^d\to$ the maximal atom of $Z$ ($3/256$ at $p=7$, T3), so the cost grows like $p^d$;
- a gate at distance 2 costs $\tfrac14p^s$, since $P_0(2,s)=\tfrac14$ for all $s$ (T3).

Prop D is not contradicted by the barrier, for the following reason. For products of consecutive terms, the valuations already fix the unit parts near a gate to $d$ digits: if $v(y+p)=d$, then $y+k'\equiv k'-p\pmod{p^d}$. So Prop D uses $d$ digits exactly where the barrier asks for them.

Tests:
- **T2.** Prop D always dominates the exact $p^K\mathrm{Coll}_K$, and it grows like $p^s$.
- **PC.** On the atom, Prop D $-1$ is $10^{0.21},10^{1.11},\dots,10^{7.70}$ for $\ell=1..8$, which are M4A's phase-1 thresholds, and $10^{10.84}$, $10^{14.40}$ at $\ell=9,10$. It never decays.

**Where the decay comes from.** It comes only from averaging over the digits of $x$, in M4A Theorem 1 (Lemma H, an exact Hensel identity under Haar measure on a ball $B$ with a frozen gate pattern). This is the loophole named in the brief: for Haar-random $x$, the unit parts are polynomial images of the digits of $x$, and Theorem 1 integrates over all digits below the radius of $B$ instead of knowing them.
- **T6** re-tests Theorem 1 with this track's own DP, on balls that contain a gate of the maximal frozen depth $b-1$: exact equality in 14/14 cases at $p=3,5,7$. The negative control (slope threshold $\theta+1$) fails in 14/14.
- **PC.** On the atom, the averaged bound Prop E is $10^{-11.58}$, $10^{-25.11}$, $10^{-33.55}$, $10^{-45.30}$, $10^{-61.00}$ for $\ell=6,\dots,10$. The value at $\ell=9$ reproduces M4A's log.

**Remark O2 ((S) cannot be uniform over cylinders) [proved].** Let $p$ be odd, $t\ge3$, and $u\in\mathbb Z_p$ with $v(u+2)=s$, $p^s>t$ and $s\ge v((t-2)!)$. Put $k=V_t(u)$, and let $f\le s$. Then
$$G(u;t,k,f)=p^kP\big(v(T_u)\ge k,\ v(T_u')\ge f\big)\ \ge\ p^{\,s+v((t-2)!)}\,2^{-(t+1)} .$$

*Proof.*
- For $i\le t$ with $i\ne2$ we have $|i-2|<p^s$, so $v(u+i)=v(i-2)$. Hence $k=V_t(u)=s+v((t-2)!)$.
- The path $\tilde\delta=(1,1,1,0,\dots,0)$ gives $T_u=(u+2)^2$ and $T_u'=2(u+2)$. So $v(T_u)=2s\ge k$ and $v(T_u')=s\ge f$, since $p$ is odd.
- That path has probability $4^{-2}2^{-(t-3)}=2^{-(t+1)}$. ∎

The bound tends to $\infty$ as $s\to\infty$. The same computation as R3M's Proposition N3 then gives an infinite first moment over any cylinder on which $v(u+2)$ is not frozen. So the brief's sub-problem (S), "uniformly on cylinders", can only hold after a deep-gate truncation or on cylinders whose gates are frozen.

M4A's Lemma Q is correctly pattern-dependent: its block-0 factor is $P_0(2,\cdot)=\tfrac14$, and it charges $p^k$. Theorem M uses it only where the pattern is frozen (phases 2–3) or truncated (phase 4).

**T5** (exact DP over $(T\bmod p^k,T'\bmod p^f)$, 14 cases at $p=3,5,7$):
- the exact $G$ grows by about a factor $p$ per unit of $s$, e.g. $0.25,0.48,2.0,14.1$ at $p=7$;
- the path bound and Lemma Q's bound hold in every case.

**Verdict:** evaded correctly; there is no barrier-type input (§2.6). Fix (F2): qualify "proves (S)".

### 2.5 Corollary 10.20 and Proposition 11.24 = R3F B7 (supremum-type transfer bounds give no decay)

- **Where a supremum appears.** Lemma Q's chain rule takes a supremum over histories. For the *value-only* event this is exactly a supremum-type transfer, and its per-level factor is $q_1=p\max_zP(Z\equiv z\bmod p)$, which is always $\ge1$. In fact $q_1>1$: the weights are multiples of $4^{-p}$, so the law mod $p$ cannot be uniform. Exact values: $33/32$, $265/256$, $8309/8192$, $1.00144$ and $1.000022$ at $p=3,5,7,11,13$ (T3).
- **Consequence for Prop D.** Prop D cannot decay, as Corollary 10.20 and Proposition 11.24 predict, and it does not (PC).
- **Where the decay comes from.** It comes from a *different* quantity: the joint event that value and slope are both high. Its 2D factor is $q_2/p<1$: $0.5625$, $0.391$, $0.159$, $0.101$ and $0.078$ at $p=3,\dots,13$ (T3).
- **How that quantity arises.** It appears only after Theorem 1, whose exact cancellation of all low-slope classes under averaging is the "decorrelation" that Corollary 10.20 says any decaying bound must supply. Corollary 10.20 and Proposition 11.24 constrain bounds that iterate a supremum of the window law's own profile, and the high-slope mass is not such a profile.
- **Verdict:** evaded correctly.

### 2.6 Does the argument secretly assume a deterministic covering or equidistribution statement?

**No.** Here is the full inventory of what Theorem M rests on:

| input | kind | covering or equidistribution content |
|---|---|---|
| note Theorem 11.14 = R3M C3, with Lemma 2, Props A, B, C2 | exact identities; a martingale; Cauchy–Schwarz only at band frequencies; Paley–Zygmund | none (R3M §6: "no fullness or covering information is used anywhere") |
| Lemma H, Theorem 1 | exact Hensel identity under Haar measure on a ball | none; this is the averaging over the digits of $x$ (the loophole) |
| Lemma F | algebra (first nonzero index, $y_c'=y_cH$) | none |
| Lemma Q | chain rule, with *maximal-atom* bounds $q_s$, $q_2$, $P_0$ of fixed finite random variables (exhaustive enumeration) | anti-concentration only; no statement that subset sums cover or equidistribute |
| Props D, E, E′ | the above, plus deterministic valuation counting (Legendre; valuations of consecutive $p$-adic numbers, $\#\{\text{depth}\ge s\}\le R/p^{s-1}+1$) | none |
| atom data $i_s$, $V_N$, $M_N$ | exact integers from $x_A$ | valuations only |
| Markov, union bound, $G'$, the interval tangent-line argument | probability and analysis | none |

- **Q3.** Nothing in this list says that subset sums of unit parts of factorial-type products cover, or are equidistributed, modulo $p^k$. In particular nothing about Morita's $\Gamma_p$ is used, which is why the argument cannot, and does not claim to, say anything about Q3.
- **The deterministic $L^2$ bounds** (Prop D) are specific numbers for nine windows of one atom. They grow.

## 3. Scope: what exactly is proved

- **Prime.** $p=7$ only. Corollary M′ ($p=11,\dots,23$) is a separate claim, checked in Part II.
- **Atom.** $A=x_A+7^{51}\mathbb Z_7$, an atom of $\mathcal G_0$ at $n_0=300$, with $x_A\in\mathbb N$. All atom facts reproduce with this track's own code (S1, S2):
  - the path is alive with slope 0;
  - $M_{405}=4$ and $D_0=17\le51-4$;
  - every phase-1–3 window ends below $i_A$, and the linear regime holds in all 306 of them.
- **Conclusion.** $\mu(K_7\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A\ge1.84332\cdot10^{-26}$, so $\mu(K_7)\ge1.843\cdot10^{-26}\cdot7^{-51}=1.464\cdot10^{-69}>0$ (S4).
  - The function $(1-\sqrt{\Pi\delta})^2/\Pi$ decreases in both $\Pi$ and $\delta$, so inserting upper bounds is legitimate.
  - M4A's "$\ge1.4\cdot10^{-69}$" and "$\approx1.5\cdot10^{-69}$" are both consistent with this.
- **Conditional or not.**
  - No hypothesis is left open: FE is verified, not assumed.
  - The result rests on (i) note Theorem 11.14 (R3M C3) and its round-3 ingredients, checked by an independent instance and a referee in round 3 but not by a human; (ii) M4A's Lemma H, Theorem 1, Lemma F, Lemma Q and Props D, E, E′, checked line by line by `verify_M4A_logic` and, for Theorem 1, also by T6 here; (iii) the outward-rounded interval evaluation, reproduced independently by `verify_M4A_logic`.
  - The label [computer-assisted] is therefore right. Wherever Theorem M is quoted, it should name its dependence on note Theorem 11.14 (F4).
- **Not claimed, correctly.**
  - Anything about Q3, about $x_A$, or about any natural number.
  - Uniformity in $p$.
  - $p=3$ or $p=5$, where the method's rate is negative.
- **The constant is conservative.** The phase-contrast table shows that Prop E is already $\le10^{-11.6}$ at $\ell=6$. Re-running M4A's `fe_verify.py` read-only with Markov from $\ell=6$ on ($L_1=5$) gives $\log_{10}\Pi_A\le8.79$, $\delta_A\le5.24\cdot10^{-12}$ and $\mu(K_7\cap A)/\mu(A)\ge1.45\cdot10^{-9}$. With $L_1=6$ it gives $4.24\cdot10^{-13}$. This uses the same chain and code; I did not re-verify it independently. It is an observation and not part of the verdict (`fe_L1_variants.log`).

## 4. Fixes (to the M4A report; none changes a number or the conclusion)

- **(F1) Headline, item 3: "it uses no truncation beyond working on one atom".** Replace with: Props D, E, E′ need no truncation on a ball whose gate pattern is frozen. Theorem M needs the truncation $G'$ for the random gates beyond $i_A$, because the untruncated $\mathbb E_A[\varepsilon_{307}]$ is $+\infty$ (this check, Proposition O1). Add the same sentence to the Proposition 11.15(b) bullet of M4A §7.
- **(F2) "This proves (S), the open sub-problem of the brief, in the form needed".** Replace with: "proves a quenched, gate-pattern-dependent block-product form of (S). No form uniform over cylinders exists (this check, Remark O2). The pattern-dependent form suffices on an atom whose gates are frozen up to $i_A$, together with the truncation $G'$."
- **(F3) "Conjecture 5.2 therefore holds for these six primes".** Conjecture 5.2 is a statement about every odd $p$. Prefer: "the cases $p=7$ (Theorem M) and $p=11,\dots,23$ (Corollary M′) of Conjecture 5.2 hold [computer-assisted]".
- **(F4) Dependence on round 3.** The headline and the statement of Theorem M should say that the result rests on note Theorem 11.14 (R3M C3), which round 3 proved and checked but no human has refereed. M4A §7 says this; the headline does not.
- **(F5) §8 item 4: "the averaged bound is useless there".** This is inaccurate for $\ell=5,\dots,8$, where Prop E gives $10^{-1.35}$, $10^{-11.58}$, $10^{-25.11}$ and $10^{-33.55}$. Choosing $L_1=5$ improves the constant to $1.45\cdot10^{-9}$ (§3). Optional.
- **(F6) §7: "where the depths are $\le5$"** (phase 1). The maximum is in fact 4. Cosmetic.

## 5. Numerical tests (all exact; logs in `data/round4/verify_M4A_obstruction/`)

Commands are relative to `code/round4/verify_M4A_obstruction/` and were run as `sh run.sh LOG TIMEOUT python3 ...`.

| test | command | cases | result | log |
|---|---|---|---|---|
| S1–S4 | `atom_scope.py data/round4/M4A/atom_p7.txt` | the atom, $\ell\le330$ | every fact reproduced; Proposition O1 data; arithmetic | `atom_scope.log` |
| T1 | `obstr_tests.py floor p SEED NT KMAX` (3 seeds × $p=3,5,7$) | 1080 composite windows | single-window $\chi^2\ge$ floor in all; composite $\varepsilon<$ floor in 220 | `floor.log` |
| T2 | `obstr_tests.py shadow p SEED n N N' i* SMAX` | 5 windows, $s\le9$ | $\varepsilon/p^s\to$ const $>0$; 0 failures (lower bound; Prop D $\ge$ exact) | `shadow.log` |
| T3 | `obstr_tests.py consts 13 6` | $p=3,\dots,13$ | $q_1>1$, $q_2/p<1$; M4A constants at $p=7$ equal; $P_0(2,s)=\tfrac14$; $P_0(g,\cdot)$ eventually 0 for $g\ne2$ | `consts.log` |
| T4 | `obstr_tests.py ball p SEED 6 b KMAX` | 18 balls | Prop D $-1\ge\sup_B\varepsilon$ and Prop E $\ge\mathbb E_B\varepsilon$ in all | `ball.log` |
| T5 | `obstr_tests.py nonuniform p SEED t SMAX` | 14 cases | $G$ grows by about $p$ per unit of $s$; path bound and Lemma Q hold | `nonuniform.log` |
| T6 | `obstr_tests.py thm1 p SEED NB b KMAX [1]` | 14 balls + 14 controls | Theorem 1 exact 14/14; control ($\theta+1$) fails 14/14 | `thm1.log` |
| PC | `phase_contrast.py data/round4/M4A/atom_p7.txt 10` | $\ell=1..10$ on the atom | Prop D grows, Prop E decays; reproduces M4A's thresholds and its $\ell=9,10$ values | `phase_contrast.log` |
| variant | `python3 code/round4/M4A/fe_verify.py data/round4/M4A/atom_p7.txt L1 60000`, $L_1=5,6$ (M4A's code, read-only) | 2 runs | FE holds; constants $1.45\cdot10^{-9}$ and $4.24\cdot10^{-13}$ | `fe_L1_variants.log` |

## 6. What this check did not do

- **No second line-by-line audit.** I did not re-audit Lemma Q, Props E and E′, or the phase-4 tangent-line argument line by line; `verify_M4A_logic` did, and found them correct. Here they were tested against exact values in the configurations the obstructions single out: shadows of negative integers, the double root at $-2$, and frozen balls containing the deepest allowed gate.
- **Corollary M′** ($p=11,\dots,23$) was not examined in this part; see Part II.
- **No human refereeing.** Neither Theorem M nor the round-3 results it rests on has been refereed by a human.

## 7. Credit

- **Under check.** Theorem M, Theorem 1, Lemmas H, F and Q, and Props D, E and E′ are track M4A's (round 4).
- **Machinery.** The window identity, the second moment, the two-window inequality, the conditional Theorem C3 and Proposition N3 are track R3M's (round 3).
- **Obstructions.** Proposition 11.12 is R3M's. The $L^2$ barrier lemma and the $L^2$ renormalisation (B6, B7) are track R3F's (round 3). Theorems 3.6 and 3.10 and Corollary 10.20 are from rounds 1–2 (tracks A and C; track R2a).
- **Related analogues.** The $p=2$ quenched martingale is track R1b's (round 2), and the $p=2$ explicit-rate machinery is track R3Q's (round 3).
- **Classical.** Hensel's lemma; Paley–Zygmund; Doob; Lyons (second moment on trees); Smith–Wilkinson, Athreya–Karlin and Afanasyev–Geiger–Kersting–Vatutin (branching processes in random environments, background); Littlewood–Offord-type anti-concentration; Legendre's formula.
- **This check.** Produced in an AI-assisted session (track `verify_M4A_obstruction`, round 4); not checked by a human.

# Part II. Obstruction-and-scope check of Corollary M′ ($p=11,13,17,19,23$)

Date: 2026-10-14. Lens: OBSTRUCTIONS AND SCOPE. Made by the `verify_M4A_obstruction` track of round 4. This is the second run; Part I above is the first run, on Theorem M.

- **Checked:** `data/round4/reports/M4A.md`, Corollary M′ (§6) and every place in §§1–8 where $p$ or the atom enters, in particular the headline paragraph "Where this stops", §7 ("How the proof respects each obstruction") and §8 items 6–7. Code read: `code/round4/M4A/fe_verify.py`, `fe_lib.py`, `bounds.py` and `find_atom.py`. Logs read: `data/round4/M4A/fe_verify_final.log` and `find_atom.log`.
- **Also read:** Part II of `data/round4/checks/M4A_logic.md`, the logic check of Corollary M′. I do not repeat its line-by-line audit or its independent recomputation of the certificates.
- **New code** (`code/round4/verify_M4A_obstruction/`):
  - `corM_scope.py`: atom facts, phase structure, Proposition O1 at each $p$, and consistency of the phase-1 thresholds with Proposition 11.12;
  - `corM_consts.py`: block constants (own DP, plus full enumeration for $p\le13$) and a survey of the sign of M4A's asymptotic rate;
  - `corM_chi0.py`: exact two-sided brackets for the first-window $\chi^2_0$;
  - `corM_phase_contrast.py`: pointwise Prop D against averaged Prop E on each atom;
  - `corM_improve.py`: an observation on the constants (§II.3);
  - `fe_verify_digits.py`: a verbatim copy of M4A's `fe_verify.py` that prints the certified interval endpoints with 12 digits. The diff is only the header, the import path and the RESULT lines.
  - `obstr_tests.py` from Part I, now also run at $p=11,13$.
- **Independence:**
  - `corM_scope.py`, `corM_consts.py` and `corM_chi0.py` import no M4A code.
  - `corM_phase_contrast.py` imports M4A's `bounds.py` read-only, and `corM_improve.py` imports M4A's `fe_lib.py` read-only. In both cases the M4A code computes the bounds under test.
- **Logs:** `data/round4/verify_M4A_obstruction/corM_*.log`. Each run starts with `=== command:` and ends with `=== exit:`.
- **Budget:** about 7 core-minutes in total, at `nice -n 10`. The longest job took 122 s (an exact Theorem 1 test at $p=11$).
- **Housekeeping.**
  - Two short unlogged exploration scripts were run in `/tmp/r4_verify_M4A_obstruction/`: gate positions near $n_0$, and a per-$c$ decomposition of Prop D for $W_0$. Neither is part of any claim.
  - One of them wrote a Python bytecode cache into `code/round4/M4A/__pycache__/`. I deleted it. No M4A file was modified.

**The claim checked (Corollary M′, status [computer-assisted]).**
- The verification of Theorem M is repeated with $n_0=300$, $r=27/20$, $\ell_1=6$, and the atoms $A_p=x_A+p^m\mathbb Z_p$ stored in `data/round4/M4A/atom_p{11,13,17,19,23}.txt`.
- It is claimed to give $\mu(K_p\cap A_p)/\mu(A_p)\ge1.06\cdot10^{-4}$ ($p=11$), $4.90\cdot10^{-2}$ ($13$), $3.48\cdot10^{-3}$ ($17$), $1.09\cdot10^{-1}$ ($19$) and $2.07\cdot10^{-1}$ ($23$).
- Hence $\mu(K_p)>0$ for $p\in\{11,13,17,19,23\}$.

## II.0 Headline

**Verdict: confirmed-with-fixes.**

- **Conclusion.** $\mu(K_p)>0$ for $p\in\{11,13,17,19,23\}$ holds, and the label [computer-assisted] is right. With Theorem M this covers every prime $7\le p\le23$.
- **Obstructions.** At each of the five primes the argument respects every obstruction on the list, by the same mechanism as at $p=7$ (Part I). I re-ran the relevant exact tests at the new primes. Nothing in the chain changes in kind with $p$. Only the numbers change, and each one is on the safe side (§II.2).
- **No hidden statement of barrier type.** The inputs that depend on $p$ are of three kinds:
  - the block constants: exact maximal-atom computations;
  - the atom data: valuations of $x_A+i$;
  - the deterministic phase-1 bounds (Prop D).

  At $p\ge17$ the phase-1 bounds are very small. For example, at $p=23$ and $\ell=1$, Prop D gives $p^K\mathrm{Coll}_K\le1+5.5\cdot10^{-8}$, a deterministic near-equidistribution statement. But these bounds are proved, not assumed. They are used for seven windows ($W_0$ and $\ell=1,\dots,6$) whose gates have depth $\le3$. And they are not uniform: the value-only per-level factor $q_1$ is $>1$ exactly, and a depth-$s$ gate costs a factor of order $p^s$. All the decay still comes from M4A's Theorem 1, i.e. from averaging over the atom.
- **Scope.**
  - The conclusion is exactly what is proved: five primes, five explicit atoms, no open hypothesis.
  - It rests on note Theorem 11.14 (R3M C3), on M4A's Theorem 1, Lemma F, Lemma Q and Props D, E, E′, and on interval arithmetic.
- **Overstatement.** Three of the five stated constants are rounded up (G1). This confirms the logic check's (C1) with M4A's own certified intervals.

**Fixes.** None of them changes the conclusion.
- **(G1) Constants.** The certified lower endpoints are $1.058719\cdot10^{-4}$ ($p=11$), $4.895356\cdot10^{-2}$ ($13$) and $2.067070\cdot10^{-1}$ ($23$). The claim should read $\ge1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$ and $2.06\cdot10^{-1}$. The constants at $p=17,19$ are correct.
- **(G2) The truncation is necessary at every $p$.** Part I's (F1) applies at each of the five primes. The untruncated mean of the first phase-4 window is $+\infty$: Proposition O1 is now verified with the exact data at each prime (§II.2.3). So the event $G'$ of phase 4 is necessary, not cosmetic.
- **(G3) "This holds for $p\ge7$"** (positivity of the asymptotic rate; M4A headline, "Where this stops"). M4A computed this only at $p\le23$. I computed a rigorous lower bound for the rate at every prime $7\le p\le211$: it is positive at all 44 of them (§II.3). For $p>211$ the statement is unproved. A positive rate is in any case only one ingredient of FE at a given prime.
- **(G4)** Part I's (F3) applies. "Conjecture 5.2 therefore holds for these six primes" should read "the cases $p=7,11,13,17,19,23$ of Conjecture 5.2 hold [computer-assisted]", which is every prime in $[7,23]$.
- **(G5) Provenance, cosmetic.** Corollary M′ says the atoms were "found by `find_atom.py p p 300 405`". But `find_atom.log` shows seeds 2 and 3 for $p=11$ and $13$; seed $p$ was used only for $17,19,23$. The atoms themselves are fixed by the files, so nothing depends on this.

**Observation (not part of the verdict; §II.3).** The constants are conservative, and at $p\ge13$ most of the slack is Prop 11.12's own mechanism. M4A's phase-1 threshold $\bar\varepsilon_\ell=(\text{Prop D})-1$ discards the mod-$p$ level of the first half of the composite window. That level is exactly computable and is large when a window starts just before a gate: $p\,\mathrm{Coll}_1=8.5$ at $p=17$, $\ell=1$. Subtracting it is legitimate, since $p^D\mathrm{Coll}_D\ge p\,\mathrm{Coll}_1$. Doing so raises the lower bounds, computed with M4A's own interval code:

| $p$ | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|
| raised lower bound | $3.75\cdot10^{-4}$ | $0.238$ | $0.0490$ | $0.414$ | $0.419$ |

## II.1 Results of this check

| # | statement | status | evidence |
|---|---|---|---|
| S1 | For each $p$: $V_{300}(x_A)=m$ and $M_{300}<m$; the stored path has $v(S_e(x_A))=m$ and $S_e'(x_A)\not\equiv0\pmod p$; $W_0$ is admissible | computer-assisted (own exact code) | `corM_scope.log` |
| S2 | For each $p$: $i_A$ and $\ell^*$; every phase-1–3 window ends below $i_A$ and has depths $\le m-1$; the linear regime holds in all of them; at every Markov window $\lfloor D/2\rfloor+1\ge m$ (so $\theta=\lceil D/2\rceil$) and $K-M_{N'}\ge\theta$ | computer-assisted | `corM_scope.log` |
| **O1 at each $p$** | the untruncated $\mathbb E_{A_p}[\varepsilon_{\ell^*}]=+\infty$ | **proved** (Part I's $p$-generic proof; the data are exact integers, computed by `corM_scope.py`) | §II.2.3, `corM_scope.log` |
| C | $q_1>1$ exactly, $q_2/p<1$, $P_0(2,s)=\tfrac14$ for all $s$ computed, $q_s/p^s\downarrow$ the maximal atom; M4A's $q_1,q_2,\rho_1,\gamma,\kappa$ and rates reproduced | computer-assisted (exact; own DP and enumeration) | `corM_consts.log` |
| R | M4A's asymptotic rate $c$ is positive at every prime $7\le p\le211$ (rigorous lower bound with $S=2$) | computer-assisted (exact constants) | `corM_rate_survey.log` |
| X | $\chi^2_0$ is bracketed exactly at each $p$: mod-$p$ level $\le\chi^2_0\le$ Prop D, with the mod-$p$ level $\ge(p-1)4^{-p}$; at $p=23$, $\chi^2_0=5.97868\cdot10^{-9}$ exactly | computer-assisted (exact) | `corM_chi0.log` |
| PC | on each atom, Prop D $-1$ fluctuates between $10^{-7.3}$ and $10^{3.1}$ for $\ell\le10$ and never decays; Prop E falls to $10^{-44}$ to $10^{-62}$ at $\ell=10$ | computer-assisted (exact rationals) | `corM_phase_contrast.log` |
| T1′ | Prop 11.12 at $p=11,13$: no single window below the floor; composite $\varepsilon$ below it in 1/120 ($p=11$) and 18/60 ($p=13$) cases | computer-assisted (exact) | `corM_floor_p11.log` |
| T2′ | $p=11$, a gate at distance 2 in the second half: $\varepsilon$ grows by about a factor $p$ per unit of depth; Prop D dominates and grows faster | computer-assisted (exact) | `corM_shadow_p11.log` |
| T5′ | Remark O2 at $p=11,13$: $G$ grows by about $p$ per unit of $s$; the path bound and Lemma Q hold | computer-assisted (exact) | `corM_nonuniform_p11.log` |
| T6′ | Theorem 1 at $p=11$ on frozen balls containing a gate of the maximal frozen depth: 5/5 exact; the control ($\theta+1$) fails 3/3 | computer-assisted (exact) | `corM_thm1_p11.log` |
| Dg | certified lower endpoints at 12 digits; three stated constants exceed them | computer-assisted (M4A's interval code, copied) | `corM_digits.log` |
| Im | the conservative constants of the observation in §II.0 | computer-assisted (observation) | `corM_improve.log` |

## II.2 Obstruction by obstruction, at $p=11,13,17,19,23$

The atoms (S1, S2; all values exact):

| $p$ | $m$ | $M_{300}$ | $D_0$, $M_{405}$ | $v(S_e(x_A))$, $S_e'(x_A)\bmod p$ | $i_A$ | phases 1 / 2 / 3 ($\ell$) | max depth inside the phase-1 windows | max depth in phase 3 |
|---|---|---|---|---|---|---|---|---|
| 11 | 30 | 3 | 11, 3 | 30, 1 | $5.730\cdot10^{30}$ | 1–6 / 7–16 / 17–215 | 3 | 29 |
| 13 | 26 | 3 | 8, 3 | 26, 5 | $8.120\cdot10^{28}$ | 1–6 / 7–16 / 17–201 | 2 | 25 |
| 17 | 18 | 2 | 8, 2 | 18, 6 | $1.359\cdot10^{22}$ | 1–6 / 7–16 / 17–149 | 2 | 17 |
| 19 | 16 | 1 | 6, 2 | 16, 2 | $4.043\cdot10^{19}$ | 1–6 / 7–16 / 17–130 | 2 | 15 |
| 23 | 14 | 2 | 4, 2 | 14, 7 | $3.793\cdot10^{18}$ | 1–6 / 7–16 / 17–122 | 2 | 13 |

Phase 4 is every $\ell\ge\ell^*=216,202,150,131,123$ respectively. The linear regime of C3 holds in all windows $\ell<\ell^*$ at every $p$ (0 failures). Note that `corM_scope.py` reports the maximal depth over $[1,n_{\ell+1}]$; the phase-1 column above is the maximum inside the windows $(n_{\ell-1},n_{\ell+1}]$, from `corM_phase_contrast.log`.

### II.2.1 Theorem 3.6 ($K_p$ has empty interior; no residue-class criterion)

- Nothing changes from Part I §2.1.
- The only residue-class input is admissibility: $Z^0_{300}\ge1$ on $A_p$. It is a property of $x_A\bmod p^m$ and only seeds the martingale.
- Membership in $K_p$ is shown on the event $\{Y>0\}$ of C3, of measure at least the stated fraction of $A_p$, which is at most $0.21$. By Theorem 3.6, $A_p\setminus K_p$ is a nonempty open set, and nothing claims otherwise.
- The atoms' centres $x_A$ are natural numbers, and nothing is said about them or about any other integer, so Q3 is untouched.
- **Verdict:** evaded correctly.

### II.2.2 Proposition 11.12 (per-window Cauchy–Schwarz fails: $\chi^2_W\ge(p-1)4^{-p}$)

**How Corollary M′ respects it.** As in Part I §2.2, C3 pays a single-window $\chi^2$ once, as $1+\chi^2_0$. Every later window pays the composite band mass $\varepsilon_\ell$, which has no floor.

**New at these primes: exact brackets for $\chi^2_0$** (`corM_chi0.py`). The mod-$p$ level $p\,P(S\equiv0\bmod p)-1$ is the part of $\chi^2_0=\sum_{\xi\ne0}|\hat\mu(\xi)|^2$ coming from $\xi\in p^{D-1}\mathbb Z/p^D\mathbb Z$, i.e. Prop 11.12's mechanism. So it is an exact lower bound for $\chi^2_0$.

| $p$ | first gate after $n_0$ | mod-$p$ level (exact) | M4A's bound for $\chi^2_0$ (Prop D) | floor $(p-1)4^{-p}$ |
|---|---|---|---|---|
| 11 | $n_0+2$, depth 1 | $3.125$ | $3.63828$ | $2.4\cdot10^{-6}$ |
| 13 | $n_0+4$, depth 1 | $0.421875$ | $0.422094$ | $1.8\cdot10^{-7}$ |
| 17 | $n_0+1$, depth 1 | $7.5$ | $7.50249$ | $9.3\cdot10^{-10}$ |
| 19 | $n_0+17$, depth 2 | $2.97\cdot10^{-7}$ | $1.44\cdot10^{-3}$ | $6.5\cdot10^{-11}$ |
| 23 | $n_0+22$, depth 1 | $5.978677\cdot10^{-9}$; exact $\chi^2_0=5.97868\cdot10^{-9}$ | $2.22478\cdot10^{-8}$ | $3.1\cdot10^{-13}$ |

- At $p=17$, $x_A+301\equiv0\pmod{17}$. So every element except $y_0=1$ is divisible by 17, and $S\equiv\delta_0\pmod{17}$. Hence $p\,P(S\equiv0)-1=17/2-1=7.5$ exactly, and Prop D's 7.50249 is tight.
- At $p=11$ the first gate is two steps after $n_0$, so $S\equiv\delta_0-\delta_1\pmod{11}$, with $P=3/8$. This is the double root $(y+2)^2$ of Prop 11.15(b), seen modulo $p$.
- In both cases the first window carries a large mod-$p$ shell. That is Prop 11.12's phenomenon at its largest. C3 pays it exactly once. M4A's thresholds pay it a second time, through $\bar\varepsilon_1$ (observation in §II.3).
- Every $\chi^2_0$ bound and every phase-1 threshold is $\ge$ the floor, as it must be. Each composite window $[n,N')$ read modulo $p^K$ is itself a single window, so $p^K\mathrm{Coll}_K-1\ge(p-1)4^{-p}$, and a Prop D value below $1+$floor would contradict Prop 11.12 (S4 of `corM_scope.log`).

**Exact tests at $p=11,13$ (T1′).**
- In 180 composite windows, no single-window $\chi^2$ is below the floor.
- The minimum single-window $\chi^2$ is $1.436\cdot10^{-3}$ at $p=11$ and $2.202\cdot10^{-5}$ at $p=13$. These agree, to the printed digits, with $q_1-1$ ($=753/524288$ and $739/33554432$). So the floor of Prop 11.12 and the strict inequality $q_1>1$ of §II.2.5 are the same phenomenon: the mod-$p$ law of one gate block is never uniform.
- The composite $\varepsilon$ falls below the floor in 1/120 cases at $p=11$ and 18/60 at $p=13$.

**Verdict:** evaded correctly, by R3M's Theorem C3, which M4A uses unchanged.

### II.2.3 Proposition 11.15(b) ($\int_{\mathbb Z_p}\Lambda_t\,d\mu=\infty$)

**How Corollary M′ respects it.**
- **Phases 1–3.** All gate depths are frozen on $A_p$ ($\le m-1$, S2), so every mean is finite.
- **The double root.** It is priced deterministically: $P_0(2,s)=\tfrac14$ for every $s$ computed, at each $p$ (`corM_consts.log`).
- **Phase 4.** The random gates in $I_A=i_A+p^m\mathbb N_0$ are truncated by $G'$, at cost $\mu_A(G'^c)\le1.4\cdot10^{-72},\,2.5\cdot10^{-69},\,6.8\cdot10^{-57},\,1.0\cdot10^{-52},\,2.0\cdot10^{-51}$ for $p=11,\dots,23$ (M4A's log).

**Proposition O1 at each prime [proved].** Part I's proof is $p$-generic. It needs:
- $N<i_A<N'$ for the window $\ell^*=[n,N,N')$;
- $i_A+p^m>N'$, so that $I_A\cap(n,N']=\{i_A\}$;
- $c=i_A-2-n\ge0$ and $c+2\le H-1$.

The law of $s=v(x+i_A)$ on $A$ is $\mu_A(s=m+t)=\frac{p-1}p\,p^{-t}$. The divergent sum is $\sum_{s\ge s_0}\frac{p-1}p\,p^{m+K_0}2^{-(H+2)}$. I checked these hypotheses with exact integers:

| $p$ | $\ell^*$ | $H$ | $s_0=\max(m,K_0-a_c)$ | each divergent term | hypotheses |
|---|---|---|---|---|---|
| 11 | 216 | $2.60\cdot10^{30}$ | $3.40\cdot10^{27}$ | $10^{-5.12\cdot10^{29}}$ | all hold |
| 13 | 202 | $3.89\cdot10^{28}$ | $4.26\cdot10^{26}$ | $10^{-8.11\cdot10^{27}}$ | all hold |
| 17 | 150 | $6.50\cdot10^{21}$ | $5.15\cdot10^{19}$ | $10^{-1.46\cdot10^{21}}$ | all hold |
| 19 | 131 | $2.17\cdot10^{19}$ | $4.27\cdot10^{17}$ | $10^{-4.99\cdot10^{18}}$ | all hold |
| 23 | 123 | $1.97\cdot10^{18}$ | $2.59\cdot10^{16}$ | $10^{-4.71\cdot10^{17}}$ | all hold |

So the untruncated $\mathbb E_{A_p}[\varepsilon_{\ell^*}]=+\infty$ at every prime of Corollary M′. Markov on the untruncated mean is impossible there, and some deep-gate truncation is mathematically necessary: either $G'$ or C3's own linear-regime clause. This is fix (G2).

**Exact tests at $p=11,13$.**
- **T2′** ($p=11$; windows $[22,34,52)$ and $[30,41,60)$; a gate at distance 2 in the second half, depth $s\le4$):
  - $\varepsilon$ grows by factors 13.5 and 13.7 from $s=3$ to $s=4$, i.e. about $p$ per unit of depth;
  - Prop D dominates the exact $p^K\mathrm{Coll}_K$ in all 8 cases and grows faster (to 45.3 and 11.0 at $s=4$);
  - Part I's rigorous lower bound only turns positive at $s\ge9$ (first window) or $s\ge10$ (second), which is out of reach at $p=11$.
- **T5′** (Remark O2 at $p=11,13$, $t=6$): the exact normalised high-slope mass $G$ is
  - $0.269,\ 2.84,\ 31.2$ at $p=11$ and $0.305,\ 3.96,\ 51.5$ at $p=13$, for $s=1,2,3$;
  - so it is unbounded over cylinders, as Remark O2 proves for every odd $p$;
  - the path lower bound and Lemma Q's upper bound hold in all six cases.

**Verdict:** evaded correctly. Fix (G2).

### II.2.4 Barrier lemmas (Theorem 3.10; Proposition 11.23 = R3F B6)

**The deterministic bounds of Corollary M′.** These are Prop D for $W_0$ and for $\ell=1,\dots,6$, at each prime. The gates inside these windows have depth $\le3$ at $p=11$ and $\le2$ at $p=13,\dots,23$.

**What Prop D uses.** At a gate of depth $d$, Prop D uses the ratio structure of consecutive products:
- $\pi_{g+k'}(u)=\pi_g(u)\,\pi_{k'}(y)$, with $\pi_{k'}(y)\equiv\pi_{k'}(-p)\pmod{p^d}$;
- this congruence holds because $y+p\equiv0\pmod{p^d}$, so the valuation pattern fixes it;
- the incoming unit $\pi_g(u)/p^L$ (the analogue of the factorial carry, i.e. of Morita's $\Gamma_p$) and the incoming residue are not used: they enter only through the maximum over $z$ in $q_d=p^d\max_zP(Z\equiv z\bmod p^d)$.

So Prop D is not a bound "from the valuations and $c$ digits of the unit parts" for a fixed $c$. It uses $d$ digits of the ratios at a depth-$d$ gate, and its cost grows with $d$, as the barrier requires:
- $q_s/p^s$ decreases to the maximal atom of $Z$, which is $3/4096$ at $p=11$ and $3/16384$ at $p=13$ (exact enumeration of $3^p$ configurations). So $q_s\approx p^s\cdot$(max atom): a depth-$s$ gate costs a factor of order $p^s$.
- $P_0(2,s)=\tfrac14$ for every $s$ at every $p$: a depth-$s$ gate two steps after a window position costs about $2^{-c-1}p^s/4$.

**Prop D does not decay; the decay comes only from averaging** (PC, `corM_phase_contrast.log`, $\ell=1..10$ on each atom):

| $p$ | range of $\log_{10}(\text{Prop D}-1)$, $\ell\le10$ | at $\ell=7,8,9,10$ | $\log_{10}$ Prop E at $\ell=7,8,9,10$ |
|---|---|---|---|
| 11 | $[-0.34,\ 3.06]$ | 0.77, 2.04, 1.61, 3.06 | −25.0, −32.8, −45.2, −61.9 |
| 13 | $[-1.37,\ 2.39]$ | −0.13, −0.10, 2.39, 0.94 | −23.5, −30.6, −42.2, −57.9 |
| 17 | $[-3.52,\ 0.88]$ | −2.79, 0.36, −1.60, −0.70 | −20.9, −27.9, −39.3, −50.7 |
| 19 | $[-3.33,\ 0.79]$ | −1.92, −1.07, 0.79, −2.33 | −17.9, −24.3, −36.4, −48.6 |
| 23 | $[-7.26,\ 0.06]$ | −5.15, 0.06, −4.86, −0.68 | −17.7, −21.6, −31.3, −44.2 |

- The phase-1 values reproduce M4A's thresholds, and the Prop E values reproduce M4A's phase-2 log.
- Prop D $-1$ returns to order 1 or more in several windows, e.g. $p=23$ at $\ell=3,8$ and $p=19$ at $\ell=5,9$. Where I checked ($\ell\le6$), this is the mod-$p$ shell of the first half, from a window that starts just before a gate (observation in §II.3).
- The averaged bound decays by tens of orders of magnitude over the same windows.

**Theorem 1 at $p=11$ (T6′).** This is the step that uses the loophole named in the brief: averaging over the digits of $x$.
- On frozen balls containing a gate of the maximal frozen depth, the identity holds exactly in 5/5 cases ($b=2,3$).
- The negative control (slope threshold $\theta+1$) fails in 3/3.
- The logic check reports 54/54 exact identities at $p=11,13$ on other configurations.

**Verdict:** evaded correctly. There is no barrier-type input (§II.2.6).

### II.2.5 Corollary 10.20 and Proposition 11.24 (supremum-type transfer bounds give no decay)

Exact values (`corM_consts.log`; own DP mod $p^S$ with $S=6,5,5,4,4$; full enumeration for $p\le13$):

| $p$ | $q_1$ (exact) | $q_1-1$ | $q_2/p$ | M4A's $\rho_1$, $\gamma$, $\kappa$ (reproduced) | rate $c$ ($c/2$ = M4A's CRATE) |
|---|---|---|---|---|---|
| 11 | $525041/524288$ | $1.44\cdot10^{-3}$ | 0.1011 | 0.016448, 2.293534, 2.654542 | 0.031818 |
| 13 | $33555171/33554432$ | $2.20\cdot10^{-5}$ | 0.0775 | 0.002522, 2.556880, 3.576696 | 0.031599 |
| 17 | $4294969913/2^{32}$ | $6.09\cdot10^{-7}$ | 0.0588 | 0.000261, 2.832924, 5.747961 | 0.027434 |
| 19 | $137438966979/2^{37}$ | $9.83\cdot10^{-8}$ | 0.0527 | 0.000114, 2.943976, 6.890086 | 0.025683 |
| 23 | $17592186139819/2^{44}$ | $5.42\cdot10^{-9}$ | 0.0435 | 0.0000175, 3.135492, 9.244994 | 0.022819 |

- **The value-only factor never decays.** Lemma Q's value-only per-level factor $q_1$ is $>1$ at every prime (the weights are multiples of $4^{-p}$ and $p\nmid4^p$), however close to 1 it is.
- **Consequence for Prop D.** Prop D is a supremum-type transfer bound (a chain rule with a supremum over the incoming history), and it cannot decay. It does not (PC). At $p\ge17$ it stays small over the six phase-1 windows only because $q_1-1$ is tiny and the gates there are shallow.
- **Where the decay comes from.** It comes from the joint value-and-slope event, with 2D factor $q_2/p\in[0.044,0.101]$. That event appears only after Theorem 1, which is the decorrelation that Corollary 10.20 and Proposition 11.24 say any decaying bound must supply.

**Verdict:** evaded correctly.

### II.2.6 Is a deterministic covering or equidistribution statement assumed?

**No.** Part I's inventory (§2.6) is unchanged. Corollary M′ adds only the following $p$-specific inputs:

| input | kind | covering or equidistribution content |
|---|---|---|
| $q_s$, $P_0(g,s)$ at $p=11,\dots,23$ | exact maximal-atom computations; residue DP for $p>13$ (validated by this check's own DP and enumeration, and three ways by the logic check) | none: anti-concentration |
| truncations $\tilde q_s=q_Sp^{s-S}$ ($S=4$ for $p>13$) and $P_0(g,\min(s,k,4))$ | use $q_s\le pq_{s-1}$, and that $P_0(g,s)$ is nonincreasing in $s$ | none |
| atom data | valuations of $x_A+i$ | none |
| phase-1 thresholds (Prop D) | deterministic $L^2$ upper bounds, proved, for seven windows per atom | proved, not assumed; not uniform (§II.2.4–II.2.5) |
| phases 2–4 | $p$-generic, as at $p=7$ | none |

**Why the small phase-1 thresholds at $p\ge17$ are not a hidden equidistribution assumption.** The only thing that could look like one is these thresholds, e.g. $\bar\varepsilon_1=5.5\cdot10^{-8}$ at $p=23$. They come from $q_1-1$ being tiny, which is a finite exact computation at each $p$: the anti-concentration of $\sum\zeta_kk!\bmod p$, computed and not assumed. The exact $\chi^2_0$ at $p=23$ ($5.98\cdot10^{-9}$, against Prop D's $2.22\cdot10^{-8}$) confirms the scale. A version uniform in $p$ would need exactly the non-concentration of $\{k!\bmod p\}$ flagged as open in note §10.5. M4A correctly does not claim it (§8 item 7).

## II.3 Scope: what exactly is proved

- **Primes.** Exactly $p=11,13,17,19,23$. With Theorem M, every prime in $[7,23]$. Not $p=3,5$, where the method's rate is negative. Not any $p\ge29$: no atom was searched for and no certificate was run there.
- **Atoms.** The five files. Every atom fact reproduces with this check's own code (S1, S2).
- **Conditional or not.**
  - No hypothesis is open: FE is verified, not assumed.
  - The result rests on:
    - (i) note Theorem 11.14 (R3M C3) and its round-3 ingredients, AI-checked and not human-refereed;
    - (ii) M4A's Lemma H, Theorem 1, Lemma F, Lemma Q and Props D, E, E′, checked line by line by the logic check (its Part I) and exercised here at $p=11,13$ (T2′, T5′, T6′);
    - (iii) outward-rounded interval arithmetic and the residue-DP constants, both reproduced independently by the logic check, with the constants also reproduced here.
  - So [computer-assisted] is the right label. When quoted, the corollary should name its dependence on note Theorem 11.14 (Part I, F4).
- **The constants** (`corM_digits.log`). The bound $(1-\sqrt{\Pi\delta})^2/\Pi$ decreases in $\Pi$ and in $\delta$, so the certified lower endpoint is the strongest constant the certificate supports.

| $p$ | stated | certified lower endpoint | implied? | correct statement (3 digits, rounded down) | $\mu(K_p)\ge$ (endpoint $\cdot\,p^{-m}$, rounded down) |
|---|---|---|---|---|---|
| 7 | $1.843\cdot10^{-26}$ | $1.84339\cdot10^{-26}$ | yes | $1.84\cdot10^{-26}$ | $1.46\cdot10^{-69}$ |
| 11 | $1.06\cdot10^{-4}$ | $1.058719\cdot10^{-4}$ | **no** | $1.05\cdot10^{-4}$ | $6.06\cdot10^{-36}$ |
| 13 | $4.90\cdot10^{-2}$ | $4.895356\cdot10^{-2}$ | **no** | $4.89\cdot10^{-2}$ | $5.33\cdot10^{-31}$ |
| 17 | $3.48\cdot10^{-3}$ | $3.482481\cdot10^{-3}$ | yes | $3.48\cdot10^{-3}$ | $2.47\cdot10^{-25}$ |
| 19 | $1.09\cdot10^{-1}$ | $1.090929\cdot10^{-1}$ | yes | $1.09\cdot10^{-1}$ | $3.78\cdot10^{-22}$ |
| 23 | $2.07\cdot10^{-1}$ | $2.067070\cdot10^{-1}$ | **no** | $2.06\cdot10^{-1}$ | $1.78\cdot10^{-20}$ |

  The certified upper bounds (rounded up) are $\log_{10}\Pi_A\le3.975220$, $1.310216$, $2.458112$, $0.962204$ and $0.684645$, and $\delta_A\le1.831840\cdot10^{-25}$, $5.930408\cdot10^{-24}$, $2.757313\cdot10^{-21}$, $2.556695\cdot10^{-18}$ and $3.970986\cdot10^{-18}$. FE holds with margins of $10^{16.6}$ to $10^{21.9}$. The overstatement is at most 0.14%, and positivity is unaffected; but a stated lower bound must be rounded down. This is fix (G1).
- **The rate sentence (G3).** "The asymptotic rate … must be positive. This holds for $p\ge7$" is more than M4A computed.
  - Using exact $q_1,q_2$ and the truncation $S=2$ (which gives an upper bound for $\rho_1$, hence a lower bound for $c$), $c>0$ at all 44 primes $7\le p\le211$. The smallest value is $c\ge0.0044$, at $p=211$.
  - The lower bounds at $p=3,5$ are negative. This is consistent with M4A's §8, though a lower bound alone does not prove negativity.
  - Beyond 211 the sign is unproved: a uniform statement needs uniform anti-concentration (M4A §8 item 7).
  - A positive rate is only the phase-4 ingredient. FE at a new prime also needs an admissible atom and the finite phases 0–3.
- **Not claimed, correctly.** Anything about Q3, about $x_A$, or about any natural number; uniformity in $p$; $p=3,5$.
- **Observation: the constants are conservative** (`corM_improve.log`; not part of the verdict).
  - *Why the improvement is valid.* By the Fourier form, $p^j\mathrm{Coll}_j=\sum_{\xi\bmod p^j}|\hat\mu(\xi/p^j)|^2$ is nondecreasing in $j$. Modulo $p^D$ the composite sum equals the first-half sum. So on all of $A$,
    $$\varepsilon_\ell\le(\text{Prop D bound for }p^K\mathrm{Coll}_K)-p\,\mathrm{Coll}_1(\text{first half}),$$
    and the subtracted term is an exact constant on $A$.
  - *How M4A loses.* M4A subtracts 1 instead. So its $\bar\varepsilon_\ell$ re-counts the mod-$p$ shell of the first half (Prop 11.12's quantity), which is not fine-scale mass. Examples: $\bar\varepsilon_1=7.503$ at $p=17$ against $0.0025$ after the subtraction; and $\bar\varepsilon_3=0.797$ at $p=23$ against $4.2\cdot10^{-6}$.
  - *The effect.* With M4A's own interval code for Prop D and the certified $\delta_A$, the lower bounds become:

| $p$ | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|
| raised lower bound | $1.870\cdot10^{-26}$ | $3.75\cdot10^{-4}$ | $0.238$ | $0.0490$ | $0.414$ | $0.419$ |

  - *Caveats.* This uses M4A's evaluator for Prop D and this check's exact mod-$p$ DP; I did not re-verify it independently. The numerical $\mu(K_{11})\approx0.70$ and $\mu(K_{13})\approx0.75$ (note Conjecture 5.2) are global values, not values on these atoms, so they are no direct check. Still, none of the bounds approaches 1.

## II.4 Fixes (to the M4A report; none changes the conclusion)

- **(G1)** In Corollary M′ and in the table of §6, replace $1.06\cdot10^{-4}$, $4.90\cdot10^{-2}$ and $2.07\cdot10^{-1}$ by $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$ and $2.06\cdot10^{-1}$. Equivalently, quote the certified $1.0587\cdot10^{-4}$, $4.8953\cdot10^{-2}$ and $2.0670\cdot10^{-1}$ truncated, not rounded. Same as the logic check's (C1).
- **(G2)** Extend Part I's (F1) to Corollary M′. The truncation $G'$ is necessary at each of the five primes, by Proposition O1 with the data of §II.2.3.
- **(G3)** In the headline paragraph "Where this stops", replace "This holds for $p\ge7$" by "This holds at the primes computed ($7\le p\le23$ by M4A; every prime $7\le p\le211$ by the obstruction check) and fails at $p=3,5$ (§8); it is not known for all $p$."
- **(G4)** Part I's (F3), restated: "the cases $p=7,11,13,17,19,23$ of Conjecture 5.2 (every prime in $[7,23]$) hold [computer-assisted]".
- **(G5)** In Corollary M′, replace "found by `find_atom.py p p 300 405`" by the actual seeds (2, 3, 17, 19 and 23 for $p=11,13,17,19,23$), or simply by "stored in the files". Cosmetic.
- **(G6, optional)** In §6, "For $p\ge11$, $q_1$ is within $1.5\cdot10^{-3}$ of 1, so Proposition D is almost lossless". Prop D is tight on $\chi^2_0$ at $p=13,17$ (ratios 0.9995 and 0.9997 to the exact mod-$p$ level). But the phase-1 thresholds lose up to a factor of about 14 in $\Pi_A$, through the "$-1$" (observation in §II.3). Either qualify the sentence or adopt the sharper threshold.

## II.5 Numerical tests (logs in `data/round4/verify_M4A_obstruction/`)

Commands are relative to the repository root and were run as `sh code/round4/verify_M4A_obstruction/run.sh LOG TIMEOUT python3 ...`. All values are exact unless the row says interval.

| test | command | cases | result | log |
|---|---|---|---|---|
| S1–S4, O1 | `corM_scope.py data/round4/M4A/atom_pP.txt L1 60000` ($P=7$ with $L_1=8$ as regression, $P=11..23$ with $L_1=6$) | 6 atoms, all $\ell<\ell^*$ | every atom fact; linear regime 0 failures; $\theta$ and Lemma F conditions 0 failures; O1 hypotheses hold; thresholds $\ge$ floor | `corM_scope.log` |
| C | `corM_consts.py consts 7 11 13 17 19 23` | 6 primes | $q_1>1$, $q_2/p<1$, monotonicity, $P_0(2,s)=\tfrac14$; DP = enumeration ($p\le13$); M4A's $q_1,q_2,\rho_1,\gamma,\kappa$, CRATE reproduced | `corM_consts.log` |
| R | `corM_consts.py survey 3 211` | 46 primes | $c>0$ at all 44 primes $7\le p\le211$ ($S=2$ lower bound); lower bounds negative at $p=3,5$ | `corM_rate_survey.log` |
| X | `corM_chi0.py data/round4/M4A/atom_pP.txt BOUND` | 5 atoms | mod-$p$ level $\le$ Prop D and $\ge$ floor; exact $\chi^2_0$ at $p=23$ | `corM_chi0.log` |
| PC | `corM_phase_contrast.py data/round4/M4A/atom_pP.txt 10` | 5 atoms × 10 windows | Prop D does not decay; Prop E decays; M4A's values reproduced | `corM_phase_contrast.log` |
| T1′ | `obstr_tests.py floor 11 {1,2} 60 5`; `floor 13 3 60 4` | 180 windows | 0 single windows below the floor; min $\chi^2=q_1-1$; composite $\varepsilon$ below it in 19 | `corM_floor_p11.log` |
| T2′ | `obstr_tests.py shadow 11 1 22 34 52 46 4`; `shadow 11 2 30 41 60 50 4` | 8 | 0 failures; $\varepsilon$ grows about $\times p$ per depth | `corM_shadow_p11.log` |
| T5′ | `obstr_tests.py nonuniform 11 1 6 3`; `nonuniform 13 2 6 3` | 6 | path bound and Lemma Q hold; $G$ unbounded in $s$ | `corM_nonuniform_p11.log` |
| T6′ | `obstr_tests.py thm1 11 1 2 3 4`; `thm1 11 3 3 2 3`; control `thm1 11 3 3 2 3 1` (also `thm1 11 2 2 3 4 1`, which found no admissible ball) | 5 + 3 balls | Theorem 1 exact 5/5; control fails 3/3 | `corM_thm1_p11.log` |
| Dg | `fe_verify_digits.py data/round4/M4A/atom_pP.txt L1 60000` (copy of M4A's code; interval) | 6 atoms | certified endpoints; FE holds; three stated constants not implied | `corM_digits.log` |
| Im | `corM_improve.py data/round4/M4A/atom_pP.txt L1 DELTA` (interval + exact) | 6 atoms | observation of §II.3 | `corM_improve.log` |

## II.6 What this check did not do

- **No second line-by-line audit.** I did not re-audit the chain line by line at $p\ge11$; the logic check (Part II of `M4A_logic.md`) did, and it also recomputed every certificate independently. Here the chain was tested in the configurations that the obstructions single out, at $p=11,13$.
- **No exact tests at $p=17,19,23$** beyond the constants, the atom data and $\chi^2_0$ at $p=23$. The logic check ran Lemma Q tests at $p=17,23$.
- **No independent check of phase 4** beyond Proposition O1. The tangent-line argument was re-derived by the logic check.
- **No human refereeing.** Neither Corollary M′ nor the round-3 results it rests on has been refereed by a human.

## Credit (Part II)

- **Under check.** Corollary M′, Theorem M and the lemmas they use are track M4A's (round 4).
- **Machinery.** The window identity, the second moment, the two-window inequality, Theorem C3 and Proposition N3 are track R3M's (round 3).
- **Obstructions.** Proposition 11.12 is R3M's. B6 and B7 are track R3F's (round 3). Theorems 3.6 and 3.10 and Corollary 10.20 are from rounds 1–2.
- **The logic check.** The independent recomputation and its fix (C1), which (G1) confirms, are the `verify_M4A_logic` track's (round 4).
- **Related analogues.** The $p=2$ quenched martingale is track R1b's (round 2), and the $p=2$ explicit-rate machinery is track R3Q's (round 3).
- **Classical.** Hensel's lemma; Paley–Zygmund; Doob; Lyons; Smith–Wilkinson, Athreya–Karlin and Afanasyev–Geiger–Kersting–Vatutin (background); Littlewood–Offord-type anti-concentration; Legendre's formula.
- **This check.** Produced in an AI-assisted session (track `verify_M4A_obstruction`, round 4); not checked by a human.
