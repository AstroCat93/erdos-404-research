# Round 4, track M4D: decoupling and thinning (strategy D) for $\mu(K_p)>0$

Date: 2026-10-13. Code: `code/round4/M4D/`. Logs: `data/round4/M4D/` (every run is preceded by its command line).
Notation follows note.md §10.1 and the R3M report (`data/round3/reports/R3M.md`, §1); what is needed is restated in §1.

## Headline

**$\mu(K_p)>0$ is still not proved for any prime $p$.** Strategy D asks for a sub-population or functional whose offspring decouple. What this track establishes:

1. **[proved] A first-moment criterion that needs no decoupling at all (Theorem F, Corollary F1).** A deterministic *$\theta$-lifting* criterion for $x\in K_p$. It follows **one** parent per window but uses the full set of its children's targets, which is an exact affine image of the window's *fibre lifts* (Lemma L). It interpolates between Tao's block lemma ($\theta$ minimal: each window covers its own jump) and track R2b's fullness propagation (note Theorem 10.12; $\theta=1$: each window contains a complete coset modulo the next window's jump). For Haar measure it gives
$$\mu(K_p\cap A)\ \ge\ \mu(A\cap I_j)\ -\ \sum_{\ell>j}\mu(A\setminus L_\ell),$$
a union bound over windows of **bounded indicators**: no second moment, no independence between parents, no slope restriction, no linear-regime condition, no unbounded densities. So Prop 11.12 (per-window Cauchy–Schwarz) and Prop 11.15(b) (infinite annealed mean) do not touch it. A gate enters only through the probability that it occurs. Gates deep enough to make the criterion fail for every choice of $\theta$ ($p^s\gtrsim2^{H_\ell}$) occur with probability about $H_\ell2^{-H_\ell}$, which is summable (Proposition F2(c)). Numerically the criterion already fails from a smaller threshold depth $s^*(H)$, but that threshold still grows linearly in $H$ (§7.2). In FE, by contrast, a gate of depth $s$ contributes about $\kappa p^s$ with probability $p^{-s}$, i.e. about $\kappa$ per level. **The hypothesis (LIFT: the failure probabilities are summable and small) is not proved.** It is of barrier type (it uses unboundedly many digits of $x$), and Proposition F2(b) shows that the certified set always has empty interior, as Theorem 3.6 requires.
2. **[proved] Thinning by weights in the R3M second-moment machinery (Theorem W6).** The window identity, the one-window variance identity and the two-window inequality (note Props 11.10, 11.11, 11.13) hold for **arbitrary adapted probability weights** on the window digit strings. So does Theorem 11.14, with $\varepsilon_\ell$ replaced by the weighted fine-scale mass. Uniform weights give back Theorem 11.14 exactly. For every window, the minimum over weights of the fine-scale mass equals an explicit harmonic mean of *missing-lift ratios* (Corollary W5). It is $0$ exactly when the window contains a complete coset (R2b's condition). Then the conditional variance of the next window vanishes identically: the dependence between siblings, which is what defeats a branching-process-in-random-environment comparison, cancels exactly. This realises idea (i) of the strategy ("keep children with separated Newton points") in the strongest possible form: *exact balance*, not independence. Hence FE may be replaced by its infimum over weight schedules, which is at most the uniform-weight FE.
3. **[computer-assisted] Deep-gate localisation and plateau bounds (Theorem P, Corollary P1).** By the round-2 covering certificates, after time $n_0=\max_tH_t$ the alive population of $x$ can die only at a gate of depth $>T(p)$, where $T(7)=T(11)=T(19)=T(23)=6$ and $T(13)=T(17)=7$. With the round-1 census this gives explicit uniform lower bounds over enormous ranges of $G$. Examples: $\delta_G(7)\ge0.6119$ for $G\le1376$; $\delta_G(13)\ge0.7431$ for all $G\le679\,775$; $\delta_G(13)\ge0.6531$ for all $G\le6.79\cdot10^6$ (table in §4). At $p=7$ the whole question $\mu(K_7)>0$ is thus localised at the gates of depth $\ge7$, which have density $7^{-7}$.
4. **[obstruction, proved] Thinning to a single lineage cannot work unless it also proves Q3 (Proposition O3).** The unit parts $K''$ of successive depth-$t$ gates run through all residue classes (cycling lemma). So a single lineage that crosses each gate with a block shorter than $p^t$ dies almost surely as soon as one class at one depth is not covered by any such block. If no class is ever bad, this is the hypothesis UC′ of note §10.3, which gives $f(1,p)=\infty$ and Q3. The literal goal of strategy D, conditional independence given the environment, is also unattainable (§8.1): fates are deterministic functions of one uniform variable, and children with equal next-window targets have identical fates.
5. **[heuristic] Numerics (§7).** The lifting criterion is counting-feasible along growing windows only if $2^{p-1}>p^2$, i.e. $p\ge7$ (Proposition F2(a) and the typical jump $D\approx H/(p-1)$).
   - $p=13$: a complete class was missing in 3 of 3891 computed windows. In a run with no censoring, the adaptive criterion certified all 140 samples that were alive at $n_0$ through five windows (to $n=186$).
   - $p=11$: the per-window rate of missing complete classes falls from about 3–5 % (lengths 22–28) to 0–0.5 % (lengths 31–34). Without censoring, 141 of 143 alive samples were certified through five windows (to $n=162$).
   - Forced deep gates defeat the criterion only from a depth $s^*(H)$ that grows linearly with the window length $H$ (at $p=13$, $H=26$: depth 4).
   - $p=7$: at the reachable lengths (24–33) complete classes are usually missing, but the adaptive-$\theta$ form still certifies most uncensored chains.
   - $p=3,5$: the criterion fails in every window, as counting predicts.
   - In all 790 certified chains, the exact recursion confirmed survival.

Even an unconditional $\mu(K_p)>0$ would not put a natural number in $K_p$ (note Remark 10.8.5, Theorem 3.6). Nothing here bears on Q3.

## 0. Results at a glance

| # | Statement | Status |
|---|---|---|
| Lemma L | children's targets $=$ affine bijective image of the fibre lifts of the parent's class | proved; exact tests (brute force, 2 directions, NEG control) |
| Thm F | $\theta$-lifting criterion: (I) + (II) $\Rightarrow x\in K_p$ | proved |
| Cor F1 | $\mu(K_p\cap A)\ge\mu(A\cap I_j)-\sum_\ell\mu(A\setminus L_\ell)$ | proved; end-to-end exact tests of the finite-horizon conclusion |
| Cor F3 | under the lifting hypothesis the tail achievement set contains $|G_j|$ cylinders of level $D_j$ | proved |
| Prop F2 | (a) necessary counting condition; (b) the certified set has empty interior; (c) gates with $p^s\gtrsim2^{H}$ force failure for every $\theta$; their probability $\approx H\,2^{-H}$ is summable | (a),(b),(c) proved; the comparison with FE in (c) is heuristic |
| Lemmas W1–W3, Prop W4 | weighted window identity, weighted variance identity, weighted fresh-randomness lemma, weighted two-window inequality | proved; exact tests at $p=3,5,7$ |
| Cor W5 | optimal weights; harmonic-mean formula; zero variance under a complete coset | proved; exact tests |
| Thm W6 | weighted conditional positive measure (contains Theorem 11.14) | proved (hypothesis unproved) |
| Thm P, Cor P1 | deep-gate localisation; plateau bounds for $\delta_G(p)$, $p=7,11,13,17,19,23$ | computer-assisted (round-2 certificates, round-1 census); exact simulation tests; my own re-check of the certificates with $t\le5$ |
| Lemma O1, Lemma O2, Prop O3 | single-lineage first-moment bound; cycling lemma; single lineage dies a.s. unless UC′ | proved |
| §7 | Monte Carlo of the lifting criterion at $p=3,5,7,11,13$; comparison with FE's $\varepsilon_\ell$ | heuristic |

## 1. Notation and standing facts

$p$ is an odd prime, $v=v_p$, $\mu$ is Haar probability on $\mathbb Z_p$, and $x\in\mathbb Z_p$ is not a negative integer (a null set).
- $\pi_j(x)=\prod_{i\le j}(x+i)$, $V_n=v(\pi_n(x))$ and $M_n=\max_{i\le n}v(x+i)$.
- A *path* of length $n$ is $e\in\{0,1\}^n$ with $e_0=1$, and $S_e=\sum_{j<n}e_j\pi_j$. It is *alive at $n$* if $v(S_e(x))\ge V_n(x)$. Its *target* is $\tau_n(e,x)=-S_e(x)/\pi_n(x)\in\mathbb Z_p$ and its *slope* is $v(S_e'(x))$. $P^0_n(x)$ is the set of slope-$0$ alive paths.
- A *window* $W=[n,N)$ has length $H=N-n$, elements $y_i=\pi_{n+i}(x)/\pi_n(x)=\prod_{s=1}^i(x+n+s)$ for $0\le i<H$, sums $Q_f=\sum_if_iy_i$ for $f\in\{0,1\}^H$, *jump* $D=V_N-V_n$, and unit $u=\pi_N/(p^D\pi_n)\in\mathbb Z_p^\times$.

**(F1)** If some path is alive at every $n$, then $x\in K_p$, because $g_p(x)\ge V_n(x)\ge v(n!)\to\infty$ (R3M §1).

**(F2)** If $e$ is alive at $n$, then $(e,f)$ is alive at $N$ iff $Q_f\equiv\tau_n(e,x)\pmod{p^D}$, and in that case
$$\tau_N((e,f),x)=u^{-1}\,(\tau_n(e,x)-Q_f)/p^D .$$
Conversely, $(e,f)$ alive at $N$ implies $e$ alive at $n$. *Proof.* $S_{(e,f)}=S_e+\pi_nQ_f=\pi_n(Q_f-\tau_n)$, and $v(\pi_N)=v(\pi_n)+D$. For the converse, $S_e=S_{(e,f)}-\sum_{j\ge n}f_{j-n}\pi_j$ with $p^{V_n}\mid\pi_j$. ∎

*Write $P(x,n)$ for "some path of length $n$ is alive at $n$".* By the converse in (F2), $P(x,N)\Rightarrow P(x,n)$ for $n\le N$. Also $P(x,n)\iff g_p(x)\ge V_n(x)$: if $v(S_B(x))\ge V_n$, delete the elements $b\ge n$ of $B$, which have $p^{V_n}\mid\pi_b$.

## 2. The lifting lemma and the $\theta$-lifting criterion

Let $W=[n,N)$ and $W'=[N,N')$ be consecutive windows with jumps $D,D'\ge0$, and $K=D+D'$. Put
$$\Sigma=\{Q_f\bmod p^K:f\in\{0,1\}^H\}\subseteq\mathbb Z/p^K,\qquad \mathrm{Lift}(r)=\{s\in\Sigma:s\equiv r\ (p^D)\}\quad(r\in\mathbb Z/p^D).$$
The *lift fraction* of $r$ is $\varphi(r)=|\mathrm{Lift}(r)|/p^{D'}\in[0,1]$. A class $r$ is *complete* if $\varphi(r)=1$, i.e. if $\Sigma\supseteq r+p^D\mathbb Z/p^K$.

**Lemma L (lifting) [proved].** Let $e$ be alive at $n$ with target $\tau$, and let $r=\tau\bmod p^D$. Then
$$\lambda:\ \mathrm{Lift}(r)\to\mathbb Z/p^{D'},\qquad s\mapsto u^{-1}(\tau-\tilde s)/p^D\bmod p^{D'}$$
($\tilde s$ any integer representative of $s$) is a well-defined bijection onto $C(e):=\{\tau_N((e,f),x)\bmod p^{D'}:(e,f)\text{ alive at }N\}$. In particular, $e$ has exactly $|\mathrm{Lift}(r)|$ distinct child targets modulo $p^{D'}$.

*Proof.*
- *Well defined.* $\tau-\tilde s\equiv0\pmod{p^D}$, and its class modulo $p^K$ depends only on $s$. Hence $(\tau-\tilde s)/p^D\bmod p^{D'}$ depends only on $s$. Multiplication by the unit $u^{-1}$ is a bijection of $\mathbb Z/p^{D'}$.
- *Image in $C(e)$.* For $s\in\mathrm{Lift}(r)$ pick $f$ with $Q_f\equiv s\pmod{p^K}$. Then $Q_f\equiv r\equiv\tau\pmod{p^D}$, so $(e,f)$ is alive at $N$ by (F2). Its target $u^{-1}(\tau-Q_f)/p^D$ is congruent to $\lambda(s)$ modulo $p^{D'}$, because $\tau-Q_f\equiv\tau-\tilde s\pmod{p^K}$.
- *Onto.* If $(e,f)$ is alive at $N$, then $s:=Q_f\bmod p^K$ lies in $\Sigma$, and $s\equiv\tau\pmod{p^D}$ by (F2). So $s\in\mathrm{Lift}(r)$, and $\lambda(s)$ is the child's target modulo $p^{D'}$.
- *Injective.* If $\lambda(s)=\lambda(s')$, then $(\tau-\tilde s)/p^D\equiv(\tau-\tilde s')/p^D\pmod{p^{D'}}$, so $\tilde s\equiv\tilde s'\pmod{p^K}$. ∎

For $D'=0$ the lemma says only that $e$ has a child iff $r\in\Sigma\bmod p^D$; that is Tao's block lemma (note Lemma 1.3(iii)).

**Chains.** Fix times $n_j<n_{j+1}<\cdots$, which may depend on $x$ arbitrarily. Put $W_\ell=[n_\ell,n_{\ell+1})$, $H_\ell=n_{\ell+1}-n_\ell$ and $D_\ell=V_{n_{\ell+1}}-V_{n_\ell}$. Let $\mathrm{Lift}_\ell$ and $\varphi_\ell$ be the objects above for the pair $(W_\ell,W_{\ell+1})$, so the *band* is $D_{\ell+1}$. Let
$$T_\ell=\{\tau_{n_\ell}(e,x)\bmod p^{D_\ell}:\ e\text{ alive at }n_\ell\}\subseteq\mathbb Z/p^{D_\ell}.$$

**Theorem F ($\theta$-lifting criterion) [proved].** Let $\theta_{j+1},\theta_{j+2},\dots\in(0,1]$ (they may depend on $x$), and put $G_\ell=\{r\in\mathbb Z/p^{D_\ell}:\varphi_\ell(r)\ge\theta_{\ell+1}\}$ for $\ell\ge j$. Assume
- **(I)** $T_j\cap G_j\neq\emptyset$;
- **(II$_\ell$)** $|G_\ell|>(1-\theta_\ell)\,p^{D_\ell}$ for every $\ell\ge j+1$.

Then $|T_\ell|\ge\theta_\ell\,p^{D_\ell}$ for every $\ell\ge j+1$. In particular, some path is alive at every time, and $x\in K_p$.

*Proof.* By induction on $\ell\ge j+1$.
- *$\ell=j+1$.* By (I) there is $e$ alive at $n_j$ whose target class $r$ lies in $G_j$. By Lemma L, its children have $|\mathrm{Lift}_j(r)|=\varphi_j(r)p^{D_{j+1}}\ge\theta_{j+1}p^{D_{j+1}}$ distinct targets modulo $p^{D_{j+1}}$. So $|T_{j+1}|\ge\theta_{j+1}p^{D_{j+1}}$.
- *$\ell\to\ell+1$.* Suppose $|T_\ell|\ge\theta_\ell p^{D_\ell}$. By (II$_\ell$), $|T_\ell|+|G_\ell|>p^{D_\ell}$, so the two subsets of $\mathbb Z/p^{D_\ell}$ meet. Take $e$ alive at $n_\ell$ with target class in $G_\ell$ and apply Lemma L as before: $|T_{\ell+1}|\ge\theta_{\ell+1}p^{D_{\ell+1}}$.

Since $\theta_\ell>0$, every $T_\ell$ is nonempty, so some path is alive at every $n_\ell$. By (F2) a path is then alive at every $n$, and (F1) gives $x\in K_p$. ∎

**Special cases.**
1. *Tao's block lemma* ($\theta$ minimal). Take $\theta_\ell=p^{-D_\ell}$. Then $G_\ell=\{r:\mathrm{Lift}_\ell(r)\ne\emptyset\}$, and (II$_\ell$) says $|G_\ell|=p^{D_\ell}$, i.e. $W_\ell$ covers its own jump. Theorem F becomes the chained block lemma.
2. *Fullness propagation* ($\theta\equiv1$). Then $G_\ell$ is the set of complete classes, and (II$_\ell$) says that $\Sigma_\ell$ contains a complete coset $r+p^{D_\ell}\mathbb Z/p^{D_\ell+D_{\ell+1}}$. This is condition (ii) of track R2b's Theorem 10.12 (note §10.3), and Theorem F is then the chained form of its implication (ii)⇒(i): "fullness mod $p^{D_\ell}$ propagates to fullness mod $p^{D_{\ell+1}}$". **Credit: round 2, track R2b.** R2b used it for deterministic covering stretches towards Q3. Lemma L, the intermediate $\theta$, and the measure-theoretic use below are new here.
3. *Intermediate $\theta$.* A window may fail to cover its own jump, for instance because of a gate near its start. This is compensated by the previous window lifting a fraction $\theta>1-|G|/p^{D}$ of its band. The optimal $\theta$-sequence over finitely many windows is computed by a backward recursion (§7).

**Corollary F1 (first-moment form) [proved].** Let $A\subseteq\mathbb Z_p$ be Borel. Choose the times $n_\ell(x)$ and the $\theta_\ell(x)$ so that the events $I_j=\{T_j\cap G_j\ne\emptyset\}$ and $L_\ell=\{(\mathrm{II}_\ell)\text{ holds}\}$ are Borel; deterministic times and $\theta$'s qualify. Then
$$\mu(K_p\cap A)\ \ge\ \mu(A\cap I_j)\ -\ \sum_{\ell\ge j+1}\mu(A\setminus L_\ell).$$
Hence **$\mu(K_p)>0$ whenever $\sum_{\ell>j}\mu(A\setminus L_\ell)<\mu(A\cap I_j)$ for some $A$ and $j$** (hypothesis **LIFT**).

*Proof.* $A\cap I_j\cap\bigcap_\ell L_\ell\subseteq K_p$ by Theorem F; take complements and apply a union bound. With deterministic times, each event depends on $x$ modulo a power of $p$ that is finite outside the null set of negative integers. So each event is a countable union of cylinders, hence Borel. ∎

**Proposition F2 [(a), (b) proved; (c) proved bound, heuristic reading].**
- **(a) Necessary counting condition.** If (II$_\ell$) holds, then $(1-\theta_\ell)\,\theta_{\ell+1}\,p^{D_\ell+D_{\ell+1}}<2^{H_\ell}$, and $\theta_{\ell+1}p^{D_{\ell+1}}\le2^{H_\ell}$ in every case. *Proof.* The sets $\mathrm{Lift}_\ell(r)$ are disjoint subsets of $\Sigma_\ell$, and $|\Sigma_\ell|\le2^{H_\ell}$. So $|G_\ell|\,\theta_{\ell+1}p^{D_{\ell+1}}\le2^{H_\ell}$, and $|G_\ell|>(1-\theta_\ell)p^{D_\ell}$, $|G_\ell|\ge1$. ∎
- *[heuristic] Consequence.* For Haar-random $x$ the jump of a window of length $H$ is $H/(p-1)$ on average (Legendre). For $\theta$ bounded away from $0$ and $1$ and non-decreasing window lengths, (a) therefore needs $2^H\gtrsim p^{2H/(p-1)}$, i.e. $2^{p-1}>p^2$, i.e. $p\ge7$ (the ratios $2^{p-1}/p^2$ are $0.44, 0.64, 1.31, 8.46, 24.2$ for $p=3,5,7,11,13$). At $p=3,5$ Theorem F is useful only with $\theta$ near its minimum, i.e. essentially as Tao covering.
- **(b) The certified set has empty interior.** Take deterministic times with $H_\ell\to\infty$, and let $E$ be the set of $x$ for which **some** choice of $j$ and of $\theta$'s satisfies (I) and all (II$_\ell$). Then $E$ contains no cylinder. This is consistent with Theorem 3.6 ($K_p$ is nowhere dense).
  - *Key step.* Suppose $n_{\ell+1}<i<n_{\ell+2}$, put $d=i-n_{\ell+1}$ (so $1\le d<H_{\ell+1}$), and suppose $v(x+i)\ge s$. The elements $y_{i'}$ of $W_{\ell+1}$ with $i'\ge d$ contain the factor $x+i$, so they vanish modulo $p^s$. Hence $|\Sigma_{\ell+1}\bmod p^s|\le2^d$. Since $D_{\ell+1}\ge s$, at most $2^dp^{D_{\ell+1}-s}$ classes modulo $p^{D_{\ell+1}}$ have nonempty lifts, so $|G_{\ell+1}|\le2^dp^{D_{\ell+1}-s}$. If $G_\ell\ne\emptyset$, (a) gives $\theta_{\ell+1}\le2^{H_\ell}p^{-s}$. Then (II$_{\ell+1}$) would need $2^dp^{-s}>1-2^{H_\ell}p^{-s}$, which is false once $p^s>2^d+2^{H_\ell}$. If $G_\ell=\emptyset$, then (II$_\ell$) fails (if $\ell>j$) or (I) fails (if $\ell=j$). So **for every $j\le\ell$ and every choice of $\theta$'s the criterion fails at $x$**.
  - *Construction.* Let $B=c+p^k\mathbb Z_p$. Build integers $i_1<i_2<\cdots$, exponents $k=s_0<s_1<s_2<\cdots$ and indices $\ell_1<\ell_2<\cdots$ inductively.
    - Given $i_t$ and $s_t$ (start with $i_0:=-c$), choose $\ell_{t+1}>\ell_t$ with $H_{\ell_{t+1}+1}>p^{s_t}$. Let $i_{t+1}$ be the least $i$ with $n_{\ell_{t+1}+1}<i<n_{\ell_{t+1}+2}$ and $i\equiv i_t\pmod{p^{s_t}}$. Its distance $d_{t+1}$ from the window start satisfies $1\le d_{t+1}\le p^{s_t}$, and $d_{t+1}<H_{\ell_{t+1}+1}$, so the key step applies.
    - Choose $s_{t+1}>s_t$ with $p^{s_{t+1}}>2^{d_{t+1}}+2^{H_{\ell_{t+1}}}$.
    - Then $x:=\lim_t(-i_t)$ exists in $\mathbb Z_p$, lies in $B$, and has $v(x+i_t)\ge s_t$ for all $t\ge1$. It is not a negative integer, because $v(x+a)\ge s_t$ for all $t$ would force $i_t=a$ for all large $t$.
  - By the key step, the criterion with any start $j$ fails at $x$ (take $t$ with $\ell_t\ge j$). So $B\not\subseteq E$. ∎
- **(c) The deep-gate cost.** The same mechanism shows $\mu(\neg L_\ell\text{ or }\neg L_{\ell+1})\ge\mu\{v(x+n_{\ell+1}+1)\ge s_\ell\}=p^{-s_\ell}$, with $p^{s_\ell}\approx2^{H_\ell}$, for every $\theta$-choice. This is the unavoidable price of deep gates. It is **summable** over growing windows ($\approx2^{-H_\ell}$). By contrast, in FE a gate of depth $s$ contributes $\approx\kappa p^s$ with probability $\approx p^{-s}$, so about $\kappa$ per level; that is the infinite-mean phenomenon of Prop 11.15(b). In LIFT the indicators are bounded, so deep gates contribute only their probability. *Whether gates of moderate depth, and non-gate structure, make LIFT fail with non-summable probability is exactly the open question.*

**Corollary F3 (positive-measure tail achievement sets) [proved].** Let $A'_n(x)=\{\sum_{i\ge0}f_i\,\pi_{n+i}(x)/\pi_n(x):f\in\{0,1\}^{\mathbb N}\}$ be the tail achievement set at time $n$ (note §1.5, rescaled). If (II$_\ell$) holds for every $\ell\ge j+1$, then
$$A'_{n_j}(x)\ \supseteq\ \{\tau\in\mathbb Z_p:\ \tau\bmod p^{D_j}\in G_j\},\qquad\text{so}\qquad \mu(A'_{n_j}(x))\ \ge\ |G_j|\,p^{-D_j}.$$
*Proof.* Lemma L uses the parent only through its target $\tau\in\mathbb Z_p$. For an arbitrary $\tau$, the "children" are the $f$ with $Q_f\equiv\tau\pmod{p^{D}}$, and the new target is $u^{-1}(\tau-Q_f)/p^D$. So the induction in the proof of Theorem F, started from any $\tau$ with $\tau\bmod p^{D_j}\in G_j$, gives for every $\ell$ a word $f^{(\ell)}\in\{0,1\}^{n_\ell-n_j}$ whose sum is $\equiv\tau$ modulo $p^{V_{n_\ell}-V_{n_j}}$. Prefixes of good words are good, so König's lemma gives an infinite $f$ with $\sum_if_i\pi_{n_j+i}/\pi_{n_j}=\tau$. ∎

So the hypothesis of Theorem F also gives positive-measure (though not full) tail achievement sets. This is the object of R3M's unproved route (c) (R3M §9 item 5); fullness itself is impossible on a set with interior (Theorem 3.6). Exactly: $x\in K_p$ iff some path alive at $n_j$ has its (exact) target in $A'_{n_j}(x)$.

**How Theorem F sits relative to the obstructions in the brief.**
- *Theorem 3.6.* See F2(b): the certified set is nowhere dense, as it must be.
- *Prop 11.12 (per-window CS) and Prop 11.15(b) (infinite mean).* Not used: Theorem F needs no second moment and no expectation of an unbounded quantity.
- *Barrier lemmas (Theorem 3.10, Prop 11.23).* (II$_\ell$) concerns the residues of window sums modulo $p^{D_\ell+D_{\ell+1}}$. These are the digits of the unit parts up to the level of the next window's jump, so a proof of LIFT must use unboundedly many digits of $x$. That is allowed for Haar-random $x$, but it is exactly what is not proved.
- *Corollary 10.13 (gate and window transparency, R2b).* It shows that fullness cannot propagate through windows that are short relative to a deep gate, where window sums are integers modulo $p^t$. With windows of length tending to infinity, a depth-$t$ gate meets such a short configuration only in the finitely many windows with $H_\ell\lesssim p^t$. Those windows are rare (probability $\approx H_\ell p^{-t}$), and this is the cost already counted in F2(c).
- *The single-lineage obstruction (Proposition O3).* It does not apply: Theorem F uses the diversity of all children of the chosen parent, and $\theta<1$ tolerates missing lifts.

## 3. Thinning by weights: the R3M second-moment machinery with adapted weights

Throughout this section the setting is that of R3M §2–§5 (slope $0$). Fix a cylinder $C=x+p^m\mathbb Z_p$ with $m=V_n(x)$, and write $x'=x_0+p^mw$ for its points ($w\in\mathbb Z_p$ Haar). For $e\in P^0_n(x)$ write $\tau^0_e$, $\beta_e$ (a unit) and $\varphi_e=\tau^0_e\beta_e^{-1}$ as in R3M Prop B. A *weight* on a window of length $H$ is a probability vector $q$ on $\{0,1\}^H$. For weights $q$ and residues define
$$\mu^q_k(r)=\sum_{f:\,Q_f(x)\equiv r\ (p^k)}q(f),\qquad\hat\mu^q_k(\zeta)=\sum_fq(f)\,e(-\zeta Q_f(x)/p^k),\qquad \chi^2_q=\sum_{0\ne\xi\in\mathbb Z/p^D}|\hat\mu^q_D(\xi)|^2=p^D\sum_r\mu^q_D(r)^2-1 .$$
Uniform weights $q\equiv2^{-H}$ give R3M's $\mu_W$ and $\chi^2_W$.

**Lemma W1 (weighted window identity) [proved].** Assume (W2′) $D\le m-M_n$ and (W3′) $M_N<m$. Let $w:P^0_n(x)\to[0,\infty)$ and let $q$ be a weight on $W$. For $x'\in C$ put $Z(x')=\sum_{e\in P^0_n(x)}w(e)\sum_{f:\,(e,f)\text{ alive at }N\text{ for }x'}q(f)$. Then:
- (a) $P^0_N(x')$ is exactly the set of alive children of $P^0_n(x)$, all of slope $0$ (R3M Prop A(i) with $L=0$);
- (b) $\mathbb E_C[p^{V_N}Z]=p^m\sum_ew(e)$.

*Proof.* (a) is R3M Prop A(i). (b) By R3M Prop B(i), $(e,f)$ is alive at $x'$ iff $Q_f(x)\equiv\tau^0_e-\beta_ew\pmod{p^D}$. For fixed $e,f$ this has probability $p^{-D}$, since $w\bmod p^D$ is uniform and $\beta_e$ is a unit. So $\mathbb E_CZ=p^{-D}\sum_ew(e)\sum_fq(f)=p^{-D}\sum_ew(e)$. Finally $p^{V_N}=p^{m+D}$ on $C$. ∎

**Lemma W2 (weighted variance identity) [proved].** In the setting of W1,
$$\operatorname{Var}_C(p^{V_N}Z)=p^{2m}\sum_{\eta\ne0}\Big|\sum_ew(e)\,\hat\mu^q_D(\eta\beta_e^{-1})\,e(\eta\varphi_e/p^D)\Big|^2\ \le\ \Big(p^m\sum_ew(e)\Big)^2\chi^2_q .$$
*Proof.* As in R3M Prop B(ii), $Z(w)=\sum_ew(e)\,\mu^q_D(\beta_e(\varphi_e-w))$. Fourier inversion, $\mu^q_D(r)=p^{-D}\sum_\xi\hat\mu^q_D(\xi)e(r\xi/p^D)$, and the substitution $\eta=\beta_e\xi$ give $Z=p^{-D}\sum_\eta e(-\eta w/p^D)A(\eta)$ with $A(\eta)=\sum_ew(e)\hat\mu^q_D(\eta\beta_e^{-1})e(\eta\varphi_e/p^D)$. Parseval over $w\bmod p^D$ gives $\mathbb E|Z|^2=p^{-2D}\sum_\eta|A(\eta)|^2$. The $\eta=0$ term is $(\mathbb EZ)^2$, because $\hat\mu^q_D(0)=1$.
For the inequality, apply Cauchy–Schwarz with weights: $|A(\eta)|^2\le(\sum_ew(e))\sum_ew(e)|\hat\mu^q_D(\eta\beta_e^{-1})|^2$. For each $e$, $\eta\mapsto\eta\beta_e^{-1}$ permutes the nonzero residues. ∎

**Lemma W3 (weighted fresh-randomness lemma) [proved].** Assume (5.1) $D+k\le m-M_N$ and $M_N<m$. Let $P\subseteq P^0_n(x)$, with weights $w$ on $P$ and a weight $q$ on $W$. For $\xi\in\mathbb Z/p^k$ and $x'\in C$ put
$$\Psi(\xi;x')=\sum_{e\in P}w(e)\sum_{f:(e,f)\text{ alive at }N}q(f)\,e\big(\xi\tau_N((e,f),x')/p^k\big),\qquad F^q(\xi)=\sum_{\zeta\in\mathbb Z/p^{D+k}:\ \zeta\equiv\xi u^{-1}\,(p^k)}|\hat\mu^q_{D+k}(\zeta)|^2 .$$
Then (a) $\mathbb E_C\Psi(\xi)=0$ for $\xi\not\equiv0$, and (b) $\mathbb E_C|p^{V_N}\Psi(\xi)|^2\le(p^mW(P))^2F^q(\xi)$, where $W(P)=\sum_{e\in P}w(e)$.

*Proof.* This is R3M's Lemma C1 with the counting measure $m(s)=\#\{f:q_f=s\}$ replaced by $m^q(s)=\sum_fq(f)\mathbf 1[q_f=s]$, where $q_f=Q_f(x)\bmod p^{D+k}$.
- As there, $t_e(w)=\tau^0_e-\beta_ew\pmod{p^{D+k}}$ and $g(r)=\mathbf 1[r\equiv0\ (p^D)]\,e(\xi u^{-1}r/p^{D+k})$.
- $\Psi=\sum_ew(e)G(t_e(w))$ with $G=g*m^q$, because each child contributes $q(f)\,e(\xi u^{-1}(t_e-q_f)/p^{D+k})$.
- $\hat g(\zeta)=p^k\mathbf 1[\zeta\equiv\xi u^{-1}\ (p^k)]$ and $\widehat{m^q}=\hat\mu^q_{D+k}$.
- For each $e$, $w\bmod p^{D+k}\mapsto t_e(w)$ is a bijection. Hence $\mathbb E\,G(t_e)=p^{-(D+k)}\hat g(0)\widehat{m^q}(0)=0$ for $\xi\not\equiv0$, which is (a).
- For (b), apply Cauchy–Schwarz with weights, $|\Psi|^2\le W(P)\sum_ew(e)|G(t_e)|^2$, and Parseval: $\mathbb E|G(t_e)|^2=p^{-2(D+k)}\sum_\zeta|\hat g(\zeta)|^2|\hat\mu^q_{D+k}(\zeta)|^2=p^{-2D}F^q(\xi)$. Multiply by $p^{2V_N}=p^{2(m+D)}$. ∎

**Proposition W4 (weighted two-window inequality) [proved].** Let $W=[n,N)$ and $W'=[N,N')$ satisfy (5.2): $D+D'\le m-M_{N'}$ and $M_{N'}<m$. Let $w\ge0$ on $P^0_n(x)$, let $q$ be a weight on $W$ (fixed on $C$), and let $q'$ be a weight on $W'$ that is constant on each sub-cylinder $C'=x'+p^{m+D}\mathbb Z_p$ (it may vary with $C'$). Define
$$M_n=p^m\sum_ew(e),\qquad M_N(x')=p^{V_N}\!\!\sum_{(e,f)\in P^0_N(x')}\!\!w(e)q(f),\qquad M_{N'}(x')=p^{V_{N'}}\!\!\sum_{(e,f,f')\in P^0_{N'}(x')}\!\!w(e)q(f)q'(f').$$
Then
$$\mathbb E_C[M_{N'}^2]-\mathbb E_C[M_N^2]\ \le\ \tilde\varepsilon^{\,q}\,M_n^2,\qquad\tilde\varepsilon^{\,q}:=\sum_{0\ne\xi\in\mathbb Z/p^{D'}}F^q(\xi)=p^{D+D'}\mathrm{Coll}_{D+D'}(\mu^q)-p^D\mathrm{Coll}_D(\mu^q),$$
where $\mathrm{Coll}_k(\mu^q)=\sum_r\mu^q_k(r)^2$. If $q'$ is constant on all of $C$, the sharper bound $\varepsilon^{q,q'}:=\sum_{\xi\ne0}|\hat\mu^{q'}_{W'}(\xi)|^2F^q(\xi)$ holds. It equals $p^{D+D'}\mathrm{Coll}_{D+D'}(\nu)-p^D\mathrm{Coll}_D(\nu)$, where $\nu$ is the law of $Q_f+p^DuQ'_{f'}$ modulo $p^{D+D'}$ for independent $f\sim q$ and $f'\sim q'$ (the weighted composite law). For uniform $q,q'$ this is exactly R3M's Proposition C2.

*Proof.* Follow R3M's Steps 0–4 and record where the weights enter.
- *Step 0.* (5.2) gives (W2′), (W3′) for $W$ at $x$ and for $W'$ at every $x'\in C$, and (5.1) for $W$ with $k=D'$.
- *Step 1.* On $C'$, apply W1 and W2 to $W'$ with parent set $P^0_N(x')$, parent weights $w(e)q(f)$ and window weight $q'(C')$. This gives $\mathbb E_{C'}[M_{N'}]=M_N(C')$ and $\mathbb E_{C'}[M_{N'}^2]=M_N(C')^2+\operatorname{Var}_{C'}(M_{N'})$.
- *Step 2 (classes).* Split $P^0_N(x')$ into classes $b\in(\mathbb Z/p^{D'})^\times$ according to $\beta_{e'}\bmod p^{D'}$. Then $M_{N'}-\mathbb E_{C'}M_{N'}=\sum_bX_b$ with
$$X_b=p^{V_{N'}}\sum_{e'\in b}w'(e')\big(\mu^{q'}_{W'}(\tau_N(e',x')-bw'')-p^{-D'}\big),\qquad w'((e,f))=w(e)q(f).$$
  The Fourier computation of W2 within one class (all $\beta$ equal modulo $p^{D'}$) gives
$$\mathbb E_{w''}|X_b|^2=p^{2V_N}\sum_{\xi\ne0}|\hat\mu^{q'(C')}_{W'}(\xi)|^2|\Psi_b(\xi;x')|^2\le p^{2V_N}\sum_{\xi\ne0}|\Psi_b(\xi;x')|^2,$$
  where $\Psi_b(\xi;x')=\sum_{e'\in b}w'(e')e(\xi\tau_N(e',x')/p^{D'})$. Moving the base point inside $C'$ multiplies $\Psi_b$ by a unimodular factor, so $|\Psi_b|$ is well defined on $C'$.
  By Minkowski's inequality in $L^2(C)$: $\mathbb E_C\operatorname{Var}_{C'}(M_{N'})=\mathbb E_C|\sum_bX_b|^2\le(\sum_b\|X_b\|_2)^2$.
- *Step 3 (inheritance).* As in R3M, $\beta_{(e,f)}\equiv\beta_eu^{-1}\pmod{p^{D'}}$. So the class-$b$ members are the alive children of $P_{bu}=\{e:\beta_e\equiv bu\}$, and $\Psi_b(\xi;x')=\Psi(\xi;x')$ of W3 for $P=P_{bu}$ with $k=D'$. By W3(b), $\|X_b\|_2^2\le(p^mW(P_{bu}))^2\tilde\varepsilon^{\,q}$. With $q'$ constant on $C$, the factor $|\hat\mu^{q'}_{W'}(\xi)|^2$ can be kept inside, which gives $\varepsilon^{q,q'}$.
- *Step 4.* $(\sum_b\tilde\varepsilon^{1/2}p^mW(P_{bu}))^2=\tilde\varepsilon\,M_n^2$. Combine with Step 1 averaged over $C'\subset C$.
- *Identifications.* By Parseval, $\sum_{\xi\ne0}F^q(\xi)=\sum_{\zeta\not\equiv0\,(p^{D'})}|\hat\mu^q_{D+D'}(\zeta)|^2=p^{D+D'}\mathrm{Coll}_{D+D'}(\mu^q)-p^D\mathrm{Coll}_D(\mu^q)$.
  For $\nu$: $\hat\nu(\zeta)=\hat\mu^q_{D+D'}(\zeta)\hat\mu^{q'}_{D'}(\zeta u)$, and the same Parseval argument applies (R3M's identification). ∎

**Corollary W5 (optimal weights; complete cosets) [proved].** Fix $W$, the band $D'$, and $\mathrm{Lift}(r)$ as in §2 (with $\Sigma$ the sums of $W$ modulo $p^{D+D'}$). Put $a_r=p^{D'}/|\mathrm{Lift}(r)|-1\in[0,\infty]$, with $a_r=\infty$ if $\mathrm{Lift}(r)=\emptyset$, and
$$m(W;D')=\frac{p^D}{\sum_ra_r^{-1}}\quad(\text{the harmonic mean of the }a_r\text{ over all }p^D\text{ classes; }m=0\text{ if some }a_r=0).$$
- (a) Every weight $q$ satisfies $\tilde\varepsilon^{\,q}\ge m(W;D')$.
- (b) Equality holds for $q^*$, defined as follows. Give class $r$ total mass $\nu_r=a_r^{-1}/\sum_sa_s^{-1}$ (or $\nu$ uniform on the complete classes, if there are any). Spread $\nu_r$ uniformly over the residues of $\mathrm{Lift}(r)$, and uniformly over the $f$ representing each residue.
- (c) If $W$ contains a complete coset ($m=0$, R2b's condition), then $F^{q^*}(\xi)=0$ for every $\xi\not\equiv0$. Consequently, in Proposition W4 with $q=q^*$ and **any** $q'$, $\operatorname{Var}_{C'}(M_{N'})=0$ for every sub-cylinder $C'$. So $M_{N'}\equiv M_N(C')$ on $C'$: the next window adds no randomness at all.

*Proof.*
- (a) Write $\mu^q_{D+D'}(s)=\mu^q_D(r)\,\mu(s\mid r)$. Then $\tilde\varepsilon^{\,q}=\sum_rp^D\mu^q_D(r)^2\big(p^{D'}\sum_{s\equiv r}\mu(s\mid r)^2-1\big)$. For $\mu^q_D(r)>0$ the conditional law is supported in $\mathrm{Lift}(r)$, so by Cauchy–Schwarz the bracket is at least $a_r$. Classes with $a_r=\infty$ have $\mu^q_D(r)=0$. Finally, for any probability vector $\nu$, Cauchy–Schwarz gives $1=(\sum_r\nu_ra_r^{1/2}a_r^{-1/2})^2\le(\sum_r\nu_r^2a_r)(\sum_ra_r^{-1})$, so $\sum_rp^D\nu_r^2a_r\ge m$. If some $a_r=0$, then $m=0$ and the bound is trivial.
- (b) The conditional laws of $q^*$ are uniform on $\mathrm{Lift}(r)$, so the first inequality is an equality. The choice $\nu_r\propto a_r^{-1}$ is the equality case of the second.
- (c) $F^{q^*}\ge0$ and $\sum_{\xi\ne0}F^{q^*}(\xi)=0$. In the proof of W4, every $\|X_b\|_2=0$, so $\mathbb E_C\operatorname{Var}_{C'}=0$. The $C'$ are finitely many with equal mass, so each $\operatorname{Var}_{C'}=0$. ∎

*Interpretation.* Under $q^*$ the weighted children of one parent have targets **exactly equidistributed** modulo $p^{D'}$ on the complete classes. Their total offspring in $W'$ is then $\sum_r\mu^{q'}_{W'}(r)\cdot(\text{const})$, independent of the fresh digits. This is the exact form of "children with separated Newton points" (strategy idea (i)). It gives exact *balance*, not independence. With $\theta=1$ it is the $L^2$ shadow of Theorem F.

**Theorem W6 (weighted conditional positive measure) [proved; the hypothesis is unproved].** Use the setting of Theorem 11.14 (R3M Theorem C3): deterministic times $2p\le n_0<n_1<\cdots$, the partitions $\mathcal G_\ell$, the linear-regime events, and an admissible atom $A$ of $\mathcal G_j$. Let $q_\ell$ ($\ell\ge j$) be weights on $W_\ell$ such that $q_\ell$ is constant on the atoms of $\mathcal G_\ell$ (adapted). Put $w_j\equiv1$ and $w_{\ell+1}((e,f))=w_\ell(e)q_\ell(f)$, $M_\ell=p^{m_\ell}\sum_{e\in P^0_{n_\ell}}w_\ell(e)$, and $\tilde\varepsilon_\ell=\tilde\varepsilon^{\,q_{\ell-1}}(W_{\ell-1};D_\ell)$. If moreover each $q_\ell$ is constant on the atoms of $\mathcal G_{\ell-1}$ (predictable), one may use $\varepsilon_\ell=\varepsilon^{q_{\ell-1},q_\ell}$ instead. Let $(\bar\varepsilon_\ell)$ satisfy $\Pi=\prod_{\ell>j}(1+\bar\varepsilon_\ell)<\infty$. Let $\tau$ be the first $\ell>j$ at which the linear-regime condition of R3M's $B_\ell$ fails or $\tilde\varepsilon_\ell>\bar\varepsilon_\ell$. Put $\Pi_A=(1+\chi^2_{q_j}(A))\,\Pi$ and $\delta_A=\mu_A(\tau<\infty)$. If $\delta_A<1/\Pi_A$, then
$$\mu(K_p\cap A)/\mu(A)\ \ge\ (1-\sqrt{\Pi_A\delta_A})^2/\Pi_A .$$
*Proof.* R3M's proof of Theorem C3, line by line, with the following substitutions:
- Cor A′ becomes W1 (on atoms of $\mathcal G_\ell$, where $q_\ell$ is constant), so $M$ stopped at $\tau$ is a martingale;
- Prop B becomes W2 (first window, $\chi^2_{q_j}$);
- Prop C2 becomes W4, applied on atoms of $\mathcal G_{\ell-1}$, where $q_{\ell-1}$ is constant and $q_\ell$ is constant on each $C'$. Note that $\tilde\varepsilon_\ell$ depends only on $q_{\ell-1}$ and on $x\bmod p^{D_{\ell-1}+D_\ell}$, so $\{\tau>\ell\}\in\mathcal G_{\ell-1}$, as in R3M;
- survival: $M_\infty>0$ forces positive weight on alive paths at every $n_\ell$, so $x\in K_p$ by (F1) and (F2);
- Paley–Zygmund is unchanged. ∎

*Remarks.*
1. Uniform weights are predictable, and for them $\varepsilon_\ell$ is R3M's $\varepsilon_\ell$. So Theorem W6 contains Theorem 11.14. Its hypothesis is the infimum over weight schedules, hence at most FE.
2. Choose $q_\ell=q^*$ of Corollary W5 for $(W_\ell;D_{\ell+1})$. This is $\mathcal G_\ell$-measurable on the regime event, since $D_\ell+D_{\ell+1}\le m_\ell$. Then $\tilde\varepsilon_\ell=m(W_{\ell-1};D_\ell)$, the harmonic-mean missing-lift ratio. It is $0$ whenever $W_{\ell-1}$ contains a complete coset, and then $M_{\ell+1}=M_\ell$ identically. For a random-like window with fibres of size $\lambda p^{D'}$, $m\approx e^{-\lambda}$, whereas the uniform-weight $L^2$ mass is $\approx1/\lambda$ times a Fourier factor [heuristic].
3. The weighted theorem keeps R3M's restriction to slope $0$ and the linear regime. Theorem F needs neither, and its bound has no Paley–Zygmund loss; but it tolerates no window with $m>0$ unless $\theta<1$ absorbs it. The two are complementary.

## 4. Deep-gate localisation and plateau bounds (Theorem P)

The round-2 certificates (note §10.2, track R3) give uniform covering $\mathrm{Cov}(p,t,H_t)$ for all depths $t\le T(p)$, with $H_t+1<p^t$:
- $p=7$: $H_t=4,7,19,26,28,34$ ($T=6$);
- $p=11$: $5,10,18,22,30,33$ ($T=6$);
- $p=13$: $6,10,19,24,32,35,39$ ($T=7$);
- $p=17$: $5,11,16,25,30,34,43$ ($T=7$);
- $p=19$: $5,12,17,27,31,35$ ($T=6$);
- $p=23$: $7,12,18,23,33,37$ ($T=6$).

Recall (note Theorem 3.12(a)): $\mathrm{Cov}(p,t,H)$ says that for every unit $K'\bmod p^{c}$, with $c=v_p((H-1)!)$, the subset sums of $y_i(K')=\prod_{s=1}^i(p^tK'-(H-s))$, $0\le i<H$, cover $\mathbb Z/p^{t+c}$.

**Theorem P (deep-gate localisation) [computer-assisted: rests on the round-2 certificates].** Let $\mathrm{Cov}(p,t,H_t)$ hold for $1\le t\le T$, with $H_t+1<p^t$, and let $n_0\ge\max_tH_t$. Let $x\in\mathbb Z_p$ not be a negative integer, and suppose $P(x,n_0)$ holds and $v(x+i)\le T$ for all $n_0<i\le N$. Then $P(x,N)$ holds, so $g_p(x)\ge V_N(x)\ge v_p(N!)$.

*Proof.* Suppose not, and let $N^*\in(n_0,N]$ be the least $n$ with $\neg P(x,n)$.
- $P(x,n)$ holds for all $n<N^*$: for $n\le n_0$ by backward integrality (§1), and for $n_0<n<N^*$ by minimality.
- If $v(x+N^*)=0$, then $V_{N^*}=V_{N^*-1}$, and a path alive at $N^*-1$, extended by the digit $0$, is alive at $N^*$. So $t:=v(x+N^*)\in[1,T]$.
- Let $H=H_t\le n_0<N^*$ and write $x+N^*=p^tK''$ with $K''\in\mathbb Z_p^\times$. For $1\le s\le H-1$ we have $0<s<p^t$, so $v(x+N^*-s)=v(p^tK''-s)=v(s)$. Hence the elements of the window $[N^*-H,N^*)$ are $y_i=\prod_{s=1}^i(x+N^*-H+s)=y_i(K'')$, and its jump is $\sum_{s=1}^{H-1}v(s)+t=c+t$.
- Expanding $\prod_s(X-(H-s))$ in powers of $X=p^tK''$, the term $X^k$ ($k\ge1$) modulo $p^{t+c}$ depends only on $K''\bmod p^{c}$. So $\mathrm{Cov}(p,t,H)$ applies to $K''\bmod p^c$, and the window's sums cover $\mathbb Z/p^{t+c}$.
- Take $e$ alive at $N^*-H$ (this uses $N^*-H\ge1$) and $f$ with $Q_f\equiv\tau_{N^*-H}(e,x)\pmod{p^{t+c}}$. By (F2), $(e,f)$ is alive at $N^*$, which is a contradiction. ∎

This is the Haar-measure form of the "first-failure dichotomy" of note Theorem 3.12(b) and Proposition 10.10, which are stated for natural numbers $a$.

**Corollary P1 (plateau bounds) [computer-assisted: census and certificates].** For the six primes above put $n_0=\max_tH_t$, let $G_0$ and $\delta_{G_0}(p)$ be the round-1 census values (note §4.7: $\delta_8(7)=.62394$, $\delta_6(11)=.69976$, $\delta_5(13)=.75454$, $\delta_4(17)=.75692$, $\delta_4(19)=.77792$, $\delta_3(23)=.85617$, five decimals), and let $k_0$ be the least valuation that $V_{n_0}>G_0$ forces (below). Then for every $N\ge n_0$:
$$\delta_{v_p(N!)}(p)\ \ge\ B_p-(N-n_0)\,p^{-(T+1)},\qquad B_p:=\delta_{G_0}(p)-10^{-5}-n_0\,p^{-k_0}.$$
*Proof.*
- (i) $\{g_p\ge G_0\}\setminus\{V_{n_0}>G_0\}\subseteq\{P(x,n_0)\}$, because $P(x,n)\iff g_p(x)\ge V_n(x)$ (§1).
- (ii) Among $n_0$ consecutive elements of $\mathbb Z_p$, at most $\lceil n_0/p^k\rceil$ are divisible by $p^k$, and at most one if $p^k>n_0$. So $V_{n_0}\le b+\max(0,\,m^*-k_1+1)$, where $b=\sum_{p^k\le n_0}\lceil n_0/p^k\rceil$, $k_1$ is the least $k$ with $p^k>n_0$, and $m^*=\max_{i\le n_0}v(x+i)$. In all six cases $b\le G_0$, so $V_{n_0}>G_0$ forces $m^*\ge k_0:=G_0-b+k_1$, an event of measure $\le n_0p^{-k_0}$ (union bound over $i\le n_0$).
- (iii) By Theorem P, $\{P(x,n_0)\}\setminus\{\exists i\in(n_0,N]:v(x+i)\ge T+1\}\subseteq\{g_p\ge v_p(N!)\}$, and the removed set has measure $\le(N-n_0)p^{-(T+1)}$.
- The $10^{-5}$ accounts for the rounding of the census values. Then use $\delta_G$ non-increasing. ∎

Values (`plateau_bounds.py`, log `plateau_bounds.log`; exact rationals, printed rounded):

| $p$ | $T$ | $n_0$ | $G_0$ | $k_0$ | $n_0p^{-k_0}$ | $B_p$ | $\delta_G(p)\ge B_p-0.01$ for $G\le$ | $\ge B_p-0.05$ for $G\le$ | $\ge B_p-0.1$ for $G\le$ |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 6 | 34 | 8 | 5 | $2.02\cdot10^{-3}$ | 0.62191 | 1 376 | 6 867 | 13 728 |
| 11 | 6 | 33 | 6 | 5 | $2.05\cdot10^{-4}$ | 0.69955 | 19 488 | 97 437 | 194 874 |
| 13 | 7 | 39 | 5 | 4 | $1.37\cdot10^{-3}$ | 0.75316 | 679 775 | 3 398 877 | 6 797 756 |
| 17 | 7 | 43 | 4 | 3 | $8.75\cdot10^{-3}$ | 0.74816 | 4 359 848 | 21 799 241 | 43 598 483 |
| 19 | 6 | 35 | 4 | 4 | $2.69\cdot10^{-4}$ | 0.77764 | 496 595 | 2 482 976 | 4 965 952 |
| 23 | 6 | 37 | 3 | 3 | $3.04\cdot10^{-3}$ | 0.85312 | 1 547 647 | 7 738 240 | 15 476 478 |

(The $G$-columns are $v_p(N!)$ for $N=n_0+\lfloor\epsilon p^{T+1}\rfloor$.) Compare the numerical values $\mu(K_7)\approx0.62$ and $\mu(K_{13})\approx0.75$ (note §5): over these ranges the rigorous lower bounds sit within about $0.01$ of the conjectured limits. Before this, the note had rigorous lower bounds for $\delta_G(p)$, $p$ odd, only at the census levels ($G\le8$ at $p=7$).

*What Theorem P says about $\mu(K_7)$.* Exactly:
$$\mu(K_7)=\mu\{P(x,34)\}-\mu\{P(x,34)\text{ and the population dies at some gate of depth}\ge7\}.$$
Gates of depth $\ge7$ have density $7^{-7}$. At each of them the population survives if the pre-gate block covers the gate's class $K''$, or if the alive targets avoid the missed residues; the latter needs fine-scale information. The round-2 depth-7 "positions" certificates (note §10.2) concern specific integers $K''<49$. For Haar-random $x$ they cover only 42 of the 14 406 unit classes modulo $7^5$, so they do not improve these bounds. A uniform certificate $\mathrm{Cov}(7,7,H)$ over all classes was not attempted: about $1.4\cdot10^4$ checks modulo $7^{12}$, beyond this track's one-core budget. Even complete certificates for every depth would be UC$(7)$, which gives Q3 (note Theorem 3.12(c)). Proposition O3 explains why some fine-scale input is unavoidable as long as UC′ is not known.

## 5. Thinning to a single lineage, and why it cannot suffice (Proposition O3)

**Lemma O1 (single-lineage first-moment bound) [proved].** In the setting of Theorem 11.14 (deterministic times, linear regime, $A$ an admissible atom of $\mathcal G_j$), a *lineage* is a rule that picks, on each atom of $\mathcal G_\ell$ where it is alive, one path $e_\ell\in P^0_{n_\ell}$ that is a child of $e_{\ell-1}$. Let $\eta_\ell:=1-|\Sigma_{W_\ell}\bmod p^{D_\ell}|/p^{D_\ell}$ be the uncovered fraction of window $\ell$. Then, on the event that the lineage is alive at $\ell$ and the regime holds, $\mu(\text{alive at }\ell+1\mid\mathcal G_\ell)=1-\eta_\ell$. Hence
$$\mu(K_p\cap A)/\mu(A)\ \ge\ 1-\sum_\ell\mathbb E_A[\eta_\ell\mathbf 1_{\tau>\ell}]-\mu_A(\tau<\infty),$$
where $\tau$ is the first regime failure. *Proof.* By R3M Prop B(i), $e_\ell$ has a child at $x'$ iff $\beta(\varphi-w)\in\Sigma_{W_\ell}\pmod{p^{D_\ell}}$, where $w\bmod p^{D_\ell}$ is uniform and $\beta$ is a unit. Then apply a union bound. ∎

**Lemma O2 (cycling) [proved].** Let $x\in\mathbb Z_p$ not be a negative integer and $t\ge1$. The indices $i\ge1$ with $v(x+i)\ge t$ are $i_0+kp^t$ ($k\ge0$), where $i_0\in[1,p^t]$ and $i_0\equiv-x\pmod{p^t}$. Their parts $K''_k=(x+i_0+kp^t)/p^t$ satisfy $K''_k=K''_0+k$. Hence for every $c\ge1$ and every unit class $a\bmod p^c$, infinitely many $k$ (one in every $p^c$ consecutive) give a gate of depth exactly $t$ with $K''\equiv a\pmod{p^c}$. ∎

**Proposition O3 (single lineage with short blocks) [proved].** Fix $t\ge1$. Call $a\in\mathbb Z_p^\times$ *bad at depth $t$* if for every $H$ with $1\le H\le p^t-2$ the sums of $(y_i(a))_{i<H}$ miss a residue modulo $p^{t+c(H)}$, where $c(H)=v_p((H-1)!)$. Badness depends only on $a\bmod p^{c^*}$, with $c^*=c(p^t-2)$.

Consider a lineage that crosses every gate $N^*$ of exact depth $t'\ge t$ by committing, at some time $N^*-H$ with $1\le H\le p^{t'}-2$ (a *short block*: $H<p^{t'}-1$), to one alive slope-$0$ path and continuing only through its descendants. If a bad class exists at depth $t$, the lineage dies for Haar-almost every $x$.

*Proof.*
- Let $\eta_0>0$ be the minimum, over the finitely many sub-classes modulo $p^{c^*}$ of a bad class and the finitely many $H\le p^t-2$, of the uncovered fraction. Each of these is positive by badness.
- For a.e. $x$, $M_n=O(\log n)$. So for all but finitely many depth-$t$ gates $N^*$ the linear regime holds for the block $[N^*-H,N^*)$: $t+c(H)\le V_{N^*-H}-M_{N^*}$.
- At such a gate with $K''$ bad (infinitely many, by O2), the committed path's target modulo $p^{t+c(H)}$ is uniform given the cylinder at time $N^*-H$ (R3M Lemma 2(b): it is $\tau^0-\beta w$ with $\beta$ a unit). The missed set of the block is determined by that cylinder.
- So the conditional probability that the lineage dies at $N^*$ is at least $\eta_0$. By induction along these gates, $\mu(\text{survive }k\text{ bad gates})\le(1-\eta_0)^k\to0$. ∎

*Consequence.* Suppose single-lineage thinning with short blocks proves $\mu(K_p)>0$. Then no bad class exists at any depth. That is the hypothesis UC′ of note §10.3 (for every depth $t$ and unit class $K''$, some covering $H\le p^t-2$), and it gives $f(1,p)=\infty$ by note Theorem 3.12(c), i.e. **Q3**. So this thinning can prove the measure statement only in a situation where it also proves the much stronger Q3. At $p=7$ no bad class exists for $t\le6$ (certificates); nothing is known for $t\ge7$.

## 6. Exact tests (corroboration; no proof depends on them)

Every identity and inequality used above was tested in exact arithmetic (Python integers and `Fraction`; one C helper for bitset subset sums, validated against numpy). Each test was written to be able to fail, and a negative control shows that it can.

| program | what is tested | runs ($p$; parameters) | result | log |
|---|---|---|---|---|
| `lift_lemma_check.py` | Lemma L: for every alive parent, the set of child targets mod $p^{D'}$ (children found by **brute force over all** $2^H$ digit strings, aliveness by direct valuation) equals $\lambda(\mathrm{Lift}(r))$; sizes; "children cover $\mathbb Z/p^{D'}$ iff $r$ complete"; the inductive step of Theorem F; numpy lift sizes vs Python sets | $p=3$: $(n,H,H')=(12,12,6),(18,12,8)$; $p=5$: $(15,12,8),(20,13,10)$; $p=7$: $(14,12,8),(21,14,10)$; $p=11$: $(22,14,12)$ | 5012 parents (2211 with complete lift, 2801 without, 1471 childless): **0 failures** of any kind. NEG control (wrong unit $2u$): set equality fails for 37/148 ($p=5$) and 128/692 ($p=7$) parents | `lift_lemma.log` |
| `weighted_twowin_check.py` | W1 (martingale, exact), W2 (variance bound, exact), W4 sharp form with $\varepsilon^{q,q'}$ from the weighted composite collisions (exact), W4 adapted form with $\tilde\varepsilon^{\,q}$ and $q'$ **different on each** $C'$ (exact), Cor W5(c) ($\varepsilon=0$ and $M_{N'}$ **exactly constant** on each $C'$), slope inheritance | modes unif / rand / fib / vary; $p=3$: $(n,H,H')=(20,5,4),(26,6,5)$; $p=5$: $(20,5,5)$; $p=7$: $(21,7,7)$ with 25 randomly chosen weighted parents (the $n=14$ runs never meet (5.2) and are void) | 91 cylinder samples (every $w\bmod p^{D+D'}$ enumerated): **0 failures** of W1, W2, W4 (both forms) and slope inheritance; largest ratio LHS/RHS in W4: 0.21 (sharp form), 0.043 (adapted form). Cor W5(c): $\varepsilon=0$ and $M_{N'}$ exactly constant on every $C'$ in 20/20 fibre-uniform samples. Control: with uniform or random weights $M_{N'}$ is non-constant on some $C'$ in 52/52 samples | `weighted_twowin.log` |
| `cw5_check.py` | Cor W5(a): $\tilde\varepsilon^{\,q}\ge m(W;D')$ for uniform, random and point-mass weights; (b) equality for $q^*$ (exact) | $p=3,5,7$: 20 windows each, $p=11$: 12; 13 weightings per window | 0 violations of (a) in 936 weightings (min ratio $\tilde\varepsilon^{\,q}/m$ over $m>0$: 1.0013); (b) exact equality in 72/72 | `cw5.log` |
| `thmF_e2e.py` | Theorem F end to end (finite horizon): whenever the optimal-$\theta$ chain (or the $\theta=1$ chain) certifies windows $W_0,\dots,W_{L-1}$, the **exact** target recursion (independent code) finds a path alive at $n_L$ | $p=13$: 400 samples, windows $[13,39,68,100)$; $p=11$: 300, $[11,33,58,86)$; $p=7$: 300, $[14,28,44,62)$ and 100, $[14,32,52,74,98)$; $p=5$: 200, $[10,24,40,58)$ | 790 certified chains (opt-$\theta$), 511 certified with $\theta=1$: **0 violations**. Not certified but alive: 0 ($p=13$), 1 ($p=11$), 35 and 6 ($p=7$), 34 ($p=5$); not certified and dead: 105, 94, 94+36, 105 (so the test is not vacuous) | `thmF_e2e.log` |
| `liftprof_validate.py` | C bitset helper vs numpy: supports and per-class lift counts | 400 random cases, $p\in\{3,5,7,11,13\}$ | 0 mismatches | `liftprof_validate.log` |
| `alive_targets_validate.py` | numpy DP for the alive targets $T_0$ vs DFS | 300 random cases, $p\in\{3,5,7,11\}$ | 0 mismatches | `alive_targets_validate.log` |
| `cov_verify.py` (own bitset code) | round-2 certificates used in Theorem P | $\mathrm{Cov}(7,t,H_t)$, $t\le5$: all classes (1, 1, 42, 294, 294); $\mathrm{Cov}(7,6,34)$: 121 of 2058 classes incl. $K'=5$; $\mathrm{Cov}(13,t,H_t)$, $t\le4$: all classes; $\mathrm{Cov}(11,4,22)$ all, $\mathrm{Cov}(11,5,30)$ 60 of 110 | all cover. Controls: $\mathrm{Cov}(7,6,33)$ misses exactly 2 residues at $K'=5$ (as in note §10.2) and at 9 of 41 sampled classes; $\mathrm{Cov}(7,3,18)$ fails at 21 of 42 classes (so $H_3=19$ is minimal) | `cov_verify.log` |
| `plateau_check.py` | Theorem P at $p=7$: forced gate of exact depth $t\in[1,6]$ at $i\in[35,50]$; $P(x,34)\Rightarrow P(x,i+6)$ by the exact target-set recursion; recursion vs DFS | 400 draws, 268 with $P(x,34)$ (depths 1–6: 35, 42, 47, 47, 39, 58 cases) | **0 failures**; recursion vs DFS 0/60 mismatches. Control (gate of depth 2–6 at $i\le30$, i.e. too close to the start): $P(x,i-1)$ and $\neg P(x,i)$ in 77/200 | `plateau_check.log` |

The certificates for $t=6$ at $p=7$, $t\ge5$ at $p=11,13$, and all of $p=17,19,23$ were not re-checked over all classes here. They rest on round 2's two-program certificates and the round-2 referee's third program (note §10.2).

## 7. Heuristic numerics: how often does the lifting criterion hold? [heuristic]

`lift_scan.py` (log `lift_scan.log`) samples Haar-random $x$, fixes deterministic windows $W_\ell=[n_\ell,n_{\ell+1})$ with lengths $H_0+h\ell$, and computes for each pair $(W_\ell,W_{\ell+1})$ the exact lift counts $|\mathrm{Lift}_\ell(r)|$ for all classes $r$ (bitsets modulo $p^{D_\ell+D_{\ell+1}}$). It also computes the alive targets $T_0$ at $n_0$ (exact DP). It records:
- whether a complete class exists (the $\theta=1$ step, "FL");
- the constant-$\theta$ criteria;
- the optimal adaptive-$\theta$ chain (the best certificate Theorem F gives over the computed windows);
- the harmonic-mean ratio $m$ of Corollary W5;
- R3M's fine mass $\varepsilon$ (uniform weights) when the modulus is small.

A sample is *censored* at the first pair whose modulus exceeds the computational cap $p^{K_{\max}}$. That happens exactly when gates are deep, so censoring biases the counts towards shallow gates; the deep-gate behaviour is measured separately in §7.2.

**7.1 Window chains.**

| $p$ | windows (lengths) | samples | $\mathbb P(\text{alive at }n_0)$ | P(no complete class) per window $\ell=0,1,2,\dots$ | $\theta=1$ chain: failures after $I_0$ / certified / censored | opt-$\theta$: certified / not / censored | median $\varepsilon$ (R3M) | median $m$ |
|---|---|---|---|---|---|---|---|---|
| 13 (cap $13^7$) | 26, 29, 32, 35, 38 | 800 | 0.750 | 0.0025, 0.0013, 0, 0, 0 | 1 / 539 / 59 | 540 / 183 / 77 | $2.7\cdot10^{-9}$, $2.5\cdot10^{-10}$ | 0 |
| 13 (cap $13^8$) | 26, 29, 32, 35, 38 | 200 | 0.700 | 0, 0.005, 0, 0, 0 | 1 / 139 / **0** | **140** / 60 / **0** | — | 0 |
| 11 (cap $11^9$; 2 seeds) | 22, 25, 28, 31, 34 | 200 | 0.715 | 0.05, 0.025, 0.03, 0.005, 0 | 6 / 132 / **0** | **141** / 59 / **0** | — | 0 |
| 11 (cap $11^7$) | 22, 25, 28, 31, 34 | 300 | 0.690 | 0.033, 0.037, 0.007, 0, 0 | 10 / 117 / 78 | 120 / 64 / 116 | $3.8\cdot10^{-6}$, $4.0\cdot10^{-7}$, $9.1\cdot10^{-8}$ | 0 |
| 7 | 24, 26, 28, 30 | 150 | 0.56 (exact check on 3000 samples: 0.627) | 0.78, 0.68, 0.37, 0.57 | all 150 fail or are censored | 52 / 34 / 64 | (modulus too large) | 0.05, 0.10, 0, 0.003 |
| 7 | 33, 33, 33 | 40 | 0.40 | 0.08, 0.25, 0.38 (25, 16, 8 computed) | 3 / 2 / 24 | 5 / 3 / 32 | — | 0 |
| 5 | 20, 22, 24, 26 | 150 | 0.55 | 1, 1, 1, 1 | no chain certified | 12 / 57 / 81 | $4.7\cdot10^{-4}$ | 9–17 |
| 3 | 16, 18, … | 150 | 0.33 | 1, 1 (125, 50 computed) | — | all censored | — | $\approx10^3$ |

Reading:
- **Without censoring** (the rows with the larger caps, where no sample was censored), the optimal-$\theta$ criterion certified, through five windows (up to $n=186$ at $p=13$ and $n=162$ at $p=11$), **140 of the 140** samples alive at $n_0$ at $p=13$ and **141 of 143** at $p=11$. The $\theta=1$ chain failed after the initial condition in 1 of 140 ($p=13$) and 6 of 138 ($p=11$) chains.
- **$p=13$.** A complete class existed in every computed window except 3 of about 3900. Among the 540 chains that passed the initial condition and were not censored, the $\theta=1$ chain failed **once**. Apart from that one chain, every failure of the full criterion is a failure of the initial condition, essentially always because $x$ has no alive path at $n_0$ (frequency $1-0.750$; compare $\mu(K_{13})\approx0.7545$).
- **$p=11$.** The per-window rate of missing complete classes falls from about 3–5 % (lengths 22–28) to 0–0.5 % (lengths 31–34), as the counting margin $2^{H}/p^{D+D'}$ grows.
- **$p=7$.** At the reachable lengths (24–33) the margin per pair of levels is only $64/49$. A complete class is usually missing, but the optimal adaptive $\theta$ still certifies most uncensored chains, with $\theta<1$ absorbing incomplete lifts.
- **$p=3,5$.** The criterion fails in every window, as the counting heuristic predicts (Prop F2(a)).
- **Comparison with FE.** On the same windows R3M's $\varepsilon_\ell$ is tiny at $p=11,13$, and $m$ is exactly $0$ in all but a handful of windows. At $p=5$ (this scan: median $\varepsilon\approx5\cdot10^{-4}$ against $m\approx9$–$17$) and at $p=7$ (R3M's scan, note §11.3: median $\varepsilon$ between $10^{-2}$ and $2\cdot10^{-4}$ on comparable windows, against $m\approx0.05$–$0.1$ here), the $L^2$ quantity of FE is the better-behaved one in the regime reachable by computation, and the $L^0$ advantage of $m$ (decay like $e^{-\lambda}$ rather than $1/\lambda$) appears only once the fibres are much larger than the bands.

**End-to-end check (exact, §6):** in 790 chains certified by the criterion, a path was alive at the end in every case. Among uncensored samples the criterion missed 0 alive samples at $p=13$ and 1 at $p=11$ (two windows), so over these horizons it is essentially sharp there. It missed 9–17 % of alive samples at $p=7$ and about 35 % at $p=5$.

**7.2 Deep-gate stress test** (`lift_gate_stress.py`, log `gate_stress.log`; 25 samples per cell). Three windows of equal length $H$. A gate of exact depth $s$ is forced in the middle window $W_1$, either at its first index ("start") or at its middle ("mid"). The table gives the fraction of samples for which the optimal-$\theta$ chain over $(W_0,W_1)$ certifies survival; in parentheses, the fraction with a complete class in $W_0$ (the $\theta=1$ step into the band containing the gate).

| $p$, $H$ | $s=2$ start / mid | $s=3$ | $s=4$ | $s=5$ | $s=6$ |
|---|---|---|---|---|---|
| 13, 26 | 1 (1) / 1 (1) | 1 (1) / 1 (1) | 0 (0) / 0 (0) | 0 / 0 | — |
| 11, 22 | 1 (1) / 1 (1) | 1 (1) / 1 (0) | 0 / 0 | 0 / 0 | 0 / 0 (counting fails) |
| 7, 24 | 1 (0) / 1 (1) | 0 (0) / 1 (0) | 0 / 0 | — | — |

So, at these lengths, the criterion survives gates of depth below a threshold $s^*(H)$ and fails from depth $s^*(H)$ on: $s^*=4$ at $(p,H)=(13,26)$ and $(11,22)$, and $s^*=3$ (gate at the window start) or $4$ (gate in the middle) at $(7,24)$. In every failing cell at depth 4–5 the necessary counting condition $2^{H}\ge p^{D_1}$ still holds, so the threshold is set by the fibre sizes ($\approx2^H/p^{D_0}$ against $p^{D_1}$ lifts), not by the absolute count. The counting heuristic $s^*(H)\approx1+H\,(1/\log_2p-2/(p-1))$ gives $3.7$ at $(13,26)$ and $3.0$ at $(11,22)$. A gate of depth $\ge s^*$ falls in a window of length $H$ with probability about $Hp^{-s^*}$: about $10^{-3}$ at $(13,26)$ and $(11,22)$. This matches the rare failures of §7.1.

**7.3 A heuristic first-moment estimate.** Corollary F1 asks for $\sum_{\ell}\mu(\neg L_\ell)<\mu(I_j)$. At $p=13$ the computed windows give $\mu(\neg L_\ell)\lesssim10^{-3}$ per window, and the deep-gate failures of §7.2 have probability about $H_\ell p^{-s^*(H_\ell)}$. Here $s^*(H)$ is the least depth that defeats the chain; by the counting heuristic of §7.2 it grows linearly in $H$, so these failures decay geometrically along growing windows. Taken at face value, this suggests $\mu(K_{13})\ge\mu(I_0)-O(10^{-2})\approx0.74$ along windows of lengths $26+3\ell$. **This is not a proof.** It extrapolates finitely many windows to infinitely many, it is subject to censoring and sampling error, and the structural (non-counting) failures of LIFT at large lengths are exactly what is unproved.

## 8. Failed attempts and where they break

1. **Conditional independence by thinning (strategy idea (i) taken literally; Smith–Wilkinson, Athreya–Karlin, AGKV).** Within a window, all fates are deterministic functions of one uniform variable $w\in\mathbb Z/p^D$ (R3M Prop B(i)). Two concrete coincidences break any comparison with conditionally independent offspring:
   - two children of one parent whose sums agree modulo $p^{D+D'}$ have the same target modulo $p^{D'}$ (Lemma L), hence identical offspring counts in the next window;
   - the death event of a parent is $\{w\in\varphi_e-\beta_e^{-1}B\}$ for the missed set $B$, so parents of one class whose Newton points agree modulo $p^D$ die together.

   Excluding these coincidences means keeping children with distinct next-window targets. Done optimally, that is Corollary W5: it gives exact balance (zero variance), which is better than independence but available only when a complete coset exists. *Break point:* independence is false in general; balance is the attainable substitute.
2. **Disjoint digit blocks for consecutive generations (idea (ii)).** In the linear regime the fresh digits of window $\ell$, positions $[m_\ell,m_\ell+D_\ell)$, are already disjoint from those of other windows. That is what gives R3M's Lemma C1(a) (conditional Fourier mean $0$). It does nothing about dependence *within* a generation, which is where Prop 11.12 bites. No gain.
3. **Galton–Watson domination via a coupling (idea (iii)).** A lower coupling by an i.i.d.-offspring process needs, for $k$ parents, $\mathbb P(\text{all die})\le\eta^k$ up to constants. For two parents in one class at Newton-point distance $\delta$, $\mathbb P(\text{both die})=|B\cap(B+\delta)|/p^D$, and this equals $\eta$ when $\delta$ is a period of $B$. If a gate of depth $s$ sits $d$ elements after the window start, the sums modulo $p^s$ take at most $2^d$ values, so $B$ contains the union $B_0$ of the cosets $r+p^s\mathbb Z/p^D$ with $r\bmod p^s$ not attained. Two parents at distance $\delta\in p^s\mathbb Z$ then die together with probability at least $|B_0|/p^D$, which is of the order of $\eta$ when $B_0$ dominates $B$. *Break point:* the needed decorrelation holds only after spreading Newton points at the levels where the missed set is periodic, which is again fine-scale information.
4. **Lyons-type energy on the tree of alive paths (idea (iv)).** Lyons' second-moment criterion asks for $\sum_{e,e'}\mathbb P(e,e'\text{ both alive})\le C\big(\sum_e\mathbb P(e\text{ alive})\big)^2$ (with the weights $2^{-n}p^{V_n}$), which is $\mathbb E[M_n^2]\le C(\mathbb EM_n)^2$ verbatim. Lyons' quasi-independence fails pairwise: paths whose roots agree modulo $p^{V_n}$ are alive together with conditional probability $1$. In size-biased (spine) form, $\mathbb E_\mu[M_n^2]=\int M_n\,d\nu_n$, the normalised population seen from the root of a uniformly random path. The off-spine pair terms are exactly R3M's signed densities $\Lambda$ (Lemma C5), with obstruction (S) and Prop 11.15(b). A reformulation, no gain.
5. **Single lineage with gate-adapted short blocks.** This is Proposition O3: it dies a.s. unless UC′ holds.
6. **Proving LIFT by a second moment over $x$.** For a fixed coarse class and lift $s$, the number of $f$ with $Q_f\equiv s$ has a variance over $x$ given by pair collisions of window sums at fine scale, i.e. again by the signed carry process. A union bound over the $p^{D'}$ lifts needs Poisson-like collisions at every fine scale: R3M's open problem (S), now in an $L^0$ guise. *Break point:* (S).
7. **Unions over parents (to beat the counting threshold at $p=3,5$).** $T_{\ell+1}=\bigcup_e\big(u^{-1}(\tau_e-\mathrm{Lift}(r_e))/p^{D}\big)$ is a union of translates by the parents' high digits. Using it needs the joint law of those digits, i.e. FE-type information. Not pursued beyond this observation.
8. **Haar use of the depth-7 position certificates.** See §4: they cover a negligible set of classes.

## 9. What remains open

1. **LIFT.** For some $p\ge7$ (or all $p\ge p_0$), prove that along suitable windows (for instance $H_\ell=H_0+h\ell$) the failure probabilities $\mu(\neg L_\ell)$ of Theorem F are summable with sum below $\mu(I_j)$. This would give $\mu(K_p)>0$ by Corollary F1. By Prop F2(c) the deep-gate part costs $\approx2^{-H_\ell}$, so what is needed is a probabilistic over-covering lemma: *for Haar-random $x$ and a window of length $H$ whose gates have depth at most $s_0(H)$, the probability that fewer than $(1-\theta)p^{D}$ classes have lift fraction $\ge\theta$ at the next window's band is at most $\psi(H)$, with $\sum_\ell\psi(H_\ell)<\infty$.* This is of barrier type: it concerns digits of unit parts up to the next window's jump. Numerically (§7) it fails rarely at $p=13$ (3 of 3891 computed windows), and at $p=11$ at a rate falling to 0 as the windows lengthen.
2. **Weighted FE.** Prove the hypothesis of Theorem W6 for some weight schedule, for instance the harmonic-mean missing ratios $m(W_{\ell-1};D_\ell)$ for $q^*$. This is the $L^2$ version of item 1 and tolerates small failures.
3. **At $p=7$ specifically:** by Theorem P everything is decided at gates of depth $\ge7$. A proof that the population survives such a gate with conditional probability $1-o(1)$, summably over the gates, would suffice. The counting margin at $p=7$ is thin ($64/49$ per pair of levels), so item 1 needs windows of length in the hundreds there. $p\ge11$ looks much more favourable.
4. The counting threshold $2^{p-1}>p^2$ suggests that this route is closed at $p=3,5$. There, only $\theta$ near its minimum (Tao covering) or $L^2$ methods remain.

## 10. Computational record

Every run went through `code/round4/M4D/run.sh`. It writes the command line and start time (UTC) before the output, and the exit code and wall time after it. Runs were made under `nice -n 10`, one at a time (batches chained by `chain.sh`), on the shared 4-core machine (load average 3–5 from other tracks), with a wall-time limit per run and peak memory below 1 GB. The exception is one killed run, noted below.

| log | program | runs | total wall | notes |
|---|---|---|---|---|
| `lift_lemma.log` | `lift_lemma_check.py` | 10 | 394 s | one run ($p=11$, $n=33$) killed by hand at 4.8 GB (DFS over $\sim10^7$ alive paths); marked in the log, no result taken |
| `weighted_twowin.log` | `weighted_twowin_check.py` | 19 | 1353 s | one run ($p=7$, $n=21$, all ~$10^3$ parents) killed by hand after 433 s as too slow; replaced by the 25-parent runs; marked in the log. The $n=14$ runs at $p=7$ have 0 admissible samples and are void |
| `cw5.log` | `cw5_check.py` | 4 | 7 s | |
| `thmF_e2e.log` | `thmF_e2e.py` | 5 | 147 s | |
| `liftprof_validate.log`, `alive_targets_validate.log`, `alive_freq.log` | validators | 3 | 8 s | |
| `cov_verify.log` | `cov_verify.py` + `bin/liftprof` | 14 | 940 s | |
| `plateau_check.log`, `plateau_bounds.log` | Theorem P checks, Corollary P1 arithmetic | 3 | 132 s | |
| `lift_scan.log` | `lift_scan.py` (+ `bin/liftprof`) | 9 | 1428 s | heuristic |
| `gate_stress.log` | `lift_gate_stress.py` | 24 | 881 s | heuristic |

Smoke tests made during development are not logged. Their results were superseded by the logged runs.

## 11. Credit

- **Machinery reweighted in §3:** track R3M (round 3): the odd-$p$ window identity, Prop B, Lemma C1, Prop C2, Theorem C3, Lemma C5. Its checker (`check_R3M`) wrote the validated library from which `m4d_lib.py` copies the exact-arithmetic core.
- **Template of the quenched martingale:** track R1b (round 2; note §10.1, $p=2$).
- **Fullness propagation:** track R2b (round 2), note Theorem 10.12 and Corollary 10.13. The case $\theta=1$ of Theorem F is the chained form of Theorem 10.12; the remark UC′ after note Proposition 10.14 is R2b's.
- **Covering certificates** used in Theorem P: track R3 (round 2) and the round-2 computational referee (note §10.2). **Census values** $\delta_G(p)$: round 1 (tracks D, E; reproduced by the round-1 computational referee; note §4.7).
- Tao's block lemma and first-failure idea (forum, 29 Sep 2025), and round-1 track B's Theorem 3.12, underlie Theorem P.
- Track R3Q (round 3; $p=2$ explicit rate) was read for its stopped-martingale bounds; nothing here depends on it.
- **Classical:** the Cauchy–Schwarz, Minkowski and Paley–Zygmund inequalities, Doob's $L^2$ martingale convergence, and König's lemma. Branching processes in random environments (Smith–Wilkinson 1969, Athreya–Karlin 1971, Afanasyev–Geiger–Kersting–Vatutin 2005) are the comparison targeted in §8 items 1 and 3. Lyons's second-moment and energy method (1990, 1992) and the spine decomposition (Lyons–Pemantle–Peres 1995) are the reformulation in §8 item 4.
- The problem is due to Erdős and Graham.

*This report was produced in an AI-assisted session (round 4, track M4D). It has not been checked by a human.*
