# Erdős Problem #404 (sums of distinct factorials divisible by high prime powers): structure, finiteness families, certified lower bounds, and what remains

**Author:** Nathan Durfee (composer and prompter; has not personally verified the mathematics)

**AI assistance:** The mathematics, code, computations and text in this note were produced by Claude (Anthropic), model Claude Opus 5.5. It ran as a multi-agent workflow inside Claude Code, prompted and composed by the author. See §8 for the full disclosure.

**Date:** 2026-10-08. **Revision 2:** 2026-10-12.
- Revision 1 incorporates the corrections from three AI referee reports (logic, computation, novelty); see §9.
- **Revision 2 adds the round-2 results of 2026-10-11/12 in §10.** It also updates the summary (§0), the tables of §4 and the conjectures of §5 accordingly, marking each change "[Round 2]".
- §10 was then checked by a second set of three AI referee reports (logic, computation, novelty; 2026-10-12). They found no fatal or serious mathematical error. They did find two serious problems of credit and attribution, and several minor errors. All of these are corrected in this version; the reports are summarised in §10.8. **No human has refereed any part of §10.**

**Status:** Unrefereed research note. No human referee has checked any part of it. Below, "AI-refereed" means checked by AI referee instances (Claude), not by a person.
- **Q1:** open in general. *New in revision 2:* at $p=2$, $f(a,2)<\infty$ for all $a$ outside a set of natural density $0$ (Theorem 10.1). This is a complete proof, checked line by line by an AI logic referee and not by a human. Whether $f(a,2)<\infty$ for *every* $a$ is still open.
- **Q2:** partial results only.
- **Q3:** **OPEN.** Nothing here proves that $f(a,p)=\infty$ for any pair $(a,p)$.

---

## 0. Summary

Throughout, $p$ is a prime and $v=v_p$ is the $p$-adic valuation. For $a\ge1$, $f(a,p)$ is the supremum of the $k$ such that $p^k\mid a_1!+\dots+a_n!$ for some $a=a_1<a_2<\dots<a_n$.

Status labels used throughout:
- **[proved]** — a complete proof is given here.
- **[proved+Lean]** — in addition, a stated core was machine-checked in Lean 4 + Mathlib. Only the standard axioms are used, with no `sorry` and no `native_decide`.
- **[computer-assisted]** — the proof relies on a finite exact computation. The programs are supplied and were re-run, either today or as recorded in §7.
- **[heuristic]** and **[conjecture]** — not proofs.
- **[Round 2]** One exception to "exact": the certified Fourier shell sums of §10.4.1. They are floating point with explicit outward margins, computed by two implementations and reproduced by a third (the round-2 computational referee's); only the dominant shells were also computed in interval arithmetic. They are labelled accordingly.

### What was already known, and is only re-derived or repackaged here

A novelty referee (§9) found that several statements of an earlier draft were already public. We credit them here and in §2.
- **Normal form.** Writing $f(a,p)=v_p(a!)+g$, with $g$ the valuation of $1+\sum_{b\in B}(a+1)\cdots(a+b)$, is Kitamura's normalisation $W_J(a)$, $g(a,2)=f(a,2)-v_2(a!)$ (July 2026, `determining_exact_values.md` §3).
- **Compactness.** "$f(a,p)=\infty$ iff some infinite set $A\ni a$ has $\sum_{n\in A}n!=0$ in $\mathbb Z_p$, so Q3 holds iff some $f(a,p)=\infty$" appears in earlier public AI write-ups: neelsomani/gpt-erdos (2026-01-17, sketch), erichou1/erdos-open-problems (2026-06-10, with proof) and AItoBit/Erdosproblems-llm-hunter (2026-09-25, an explicit König-type proof).
- **Locality.** "$g\ge G$ depends only on $a \bmod p^G$" is Kitamura's *determinacy* lemma for $p=2$. The proof for general $p$ is the same one-line argument.
- **The $p=2$ value set.** Kitamura states that $g(a,2)=0$ for odd $a$ (a parity argument, with a Lean certificate for $a=5$), that $g\ge3$ for even $a$ (cube identity), that $g$ never takes the values $1,2,4,5$, and that $g=3$ exactly on $a\equiv4 \pmod 8$. These follow from Kitamura's determinacy lemma and certified classification of all even classes with $g\le24$ (174,640 residue classes). Kitamura also states the "sibling-pairing theorem" ($g$ is constant on $a \bmod 2^{g(a)}$), without a shipped proof, and the shadow family $a=2^t-2$ with $g\ge3t$.
- **Tao's programme.** Tao (forum, 29 Sep 2025) stated the block lemma and the step $P(a,p,N)\Rightarrow P(a,p,N+1)$ for $p\nmid N+1$. Tao also observed that each depth-$j$ step should reduce to one fixed finite computation, giving lower bounds of the shape $v_p((p^{J+1}-1)!)$. Our gate congruence (Theorem 3.9) and the $\mathrm{Cov}$/$\mathrm{UC}$ framework (Theorem 3.12) carry out this programme.
- **[Round 2] Criticality at $p=2$.** Kitamura had already described $p=2$ as a critical branching process. Kitamura also reported that the measured surviving fraction decays (the reported fit is about $11.5/G$), so that the census determines $f(a,2)$ for most integers (`witness_gallery.md` §6, `determining_exact_values.md` §5, `README.md`; July 2026). The heuristic H1 of §5 and the weak form of Conjecture 5.1 therefore have this public precursor. Round 1 did not credit it; the round-2 novelty referee found the omission (§10.8). Theorem 10.1 is the first *proof* of the density statement that we know of.

### New in this note

Each item below survived three AI referee reports (§9), after the corrections listed there. None has been checked by a human referee.

1. **$p$-adic packaging (Theorem 3.1).** $g_p$ is a function on $\mathbb Z_p$. The infinity set $K_p=\{g_p=\infty\}$ is closed, and $f(a,p)=\infty$ iff $a\in K_p$. The natural density of $\{a: f(a,p)\ge v_p(a!)+G\}$ exists and equals an explicit finite class count $\delta_G(p)$.
2. **Exact values on explicit residue classes (Theorem 3.2).** Put $\gamma_p(m):=g_p(-m)$, a finite computation over $2^{m-1}$ subsets; it is finite for every $m\neq2$. Then
$$f(a,p)=v_p(a!)+\gamma_p(m)\quad\text{whenever } a\equiv -m \pmod{p^{\gamma_p(m)+1}}.$$
   - Consequently $K_p\cap\mathbb Z_{<0}=\{-2\}$, and every residue class modulo every $p^k$ contains infinitely many $a$ with $f(a,p)<\infty$, with explicit values.
   - $f(a,p)=v_p(a!)$ holds **exactly** on an explicit set of classes mod $p$, of density $|\Phi_p|/p$ (Corollary 3.3). Before this, only the class $a\equiv-1$ was known.
   - Two special cases settle residue patterns that Kitamura listed "to audit further": $g(a,3)=1$ for $a\equiv6 \pmod 9$, and $g(a,5)=2$ for $a\equiv-5 \pmod{125}$.
3. **Finite values are unbounded at every prime (Proposition 3.4).** $3k\le\gamma_p(p^k+2)<\infty$. So for each $k$ there is an explicit residue class on which $f(a,p)-v_p(a!)$ is finite and at least $3k$, and there is no bound of the form "$g_p(a)\le C_p$ or $g_p(a)=\infty$". (At $p=2$, Kitamura's shadow family $a=2^t-2$ already has $g\ge3t$, with exact finite values up to $t=13$.)
4. **Hensel dichotomy and no finite-depth certificate (Theorems 3.5–3.6).**
   - On each class mod $p$, $g_p$ is either $\equiv0$ or unbounded.
   - $K_p$ and the set of "full" tails are nowhere dense. So no criterion depending on finitely many $p$-adic digits of $a$ can certify $f(a,p)=\infty$.
5. **$p=2$ halving lemmas [proved+Lean] (Theorem 3.7).**
   - For $G\ge2$, "$g_2(a)\ge G$" depends only on $a \bmod 2^{G-1}$. A sharper second halving lemma holds for $a\equiv2 \pmod 4$.
   - This proves Kitamura's sibling-pairing statement: if $g_2(a)\ge1$ then $g_2$ is constant on $a \bmod 2^{g_2(a)}$.
   - Together with a 64-class computation, it gives a second derivation of Kitamura's value-set facts.
6. **Tao-type covering cannot work at $p=2$ [proved+Lean] (Theorem 3.8).** Any chain of covering blocks gains at most 3 in valuation.
7. **Gate structure for odd $p$ (Theorem 3.9).** Factorials just below a gate of level $j$ are, modulo $p^{j+1}$, a fixed unit times the truncated series $\{(-1)^u/u!\}_{u<p}$ for $e^{-1}$. Consequences:
   - $f(1,p)\ge p+p^2+\dots+p^{L_p}$, where $L_p$ is the covering depth of that series.
   - A gap theorem: $g_p(a)\in\{\tau\}\cup[L_p+1,\infty]$.
   - A **barrier lemma** (Theorem 3.10): no argument that uses only $c$ digits of the unit parts of factorials can cross a gate of level $\ge c+1$.
8. **$p=3$ obstruction (Theorem 3.11).** For $v_3(N)\ge4$, the tail set $\{\sum_{n\in B}n!:B\subseteq[N,\infty)\}$ misses exactly the classes $N!\cdot\{68,77\}$ modulo $3^{v_3(N!)+4}$.
9. **Certified lower bounds [computer-assisted]** (§4). The previous published bounds were $\ge20000$ for $p=3,5,7$ and $\ge5000$ for $p=11,13$ (Kitamura).
   - *Explicit witnesses*, each checked by two independent verifiers: $f(1,3)\ge2\,000\,001$, $f(1,5)\ge1\,000\,000$ and $f(1,7)\ge1\,000\,000$.
   - *Certified covering, the "Theorem A" route (Theorem 3.12):* $f(1,13)\ge67\,977\,552$ and $f(1,11)\ge21\,435\,880$. The second bound was found during refereeing and re-checked here with a second implementation (§4.2). The same route gives $f(a,7)\ge960\,792$ for $a=2,3,5$.
   - *Two-block windows plus Theorem 3.9(c):* $f(1,17)\ge25\,646\,163$, $f(1,19)\ge49\,659\,537$, $f(1,23)\ge154\,764\,790$, $f(1,29)\ge616\,067\,009$ and $f(1,31)\ge917\,087\,135$.
   - *Theorem 3.9(c) alone* (covering depth $L_p\ge6$; no windows): $f(1,p)\ge p+\dots+p^6$ for $37\le p\le53$, e.g. $f(1,53)\ge2.26\cdot10^{10}$; and $f(1,p)\ge p+\dots+p^5$ for $59\le p\le97$.
   - *Dichotomies for $a\le1000$:* either $f(a,13)-v_{13}(a!)\in\{0,1\}$ or $f(a,13)\ge67\,977\,552$; either $f(a,11)-v_{11}(a!)\in\{0,1\}$ or $f(a,11)\ge21\,435\,880$; and either $f(a,7)-v_7(a!)\le3$ or $f(a,7)\ge960\,792$. In each case the finite alternative is an exact value.
   - **[Round 2]** The covering bounds for $p=7,11,13,17,19,23$, and the deep alternatives of the dichotomies, are superseded by item 14 below and §10.2.
10. **Densities beyond Kitamura's census [computer-assisted]** (§4.7). For $p=2$, Kitamura's classification of $g\le24$ already gives $f(a,2)<\infty$ on a set of density $1-\delta_{25}(2)=0.8734$. We extend this:
    - $f(a,2)\le v_2(a!)+28$ on density $1-\delta_{29}(2)=0.8866$ (three independent implementations), and $f(a,2)\le v_2(a!)+31$ on density $1-\delta_{32}(2)=0.8984$ (two implementations);
    - at odd primes, the first densities beyond the class $a\equiv-1 \pmod p$: $f(a,p)<\infty$ on density $\ge0.6367$ for $p=3$, $\ge0.4784$ for $p=5$, $\ge0.3761$ for $p=7$, $\ge0.3002$ for $p=11$ and $\ge0.2455$ for $p=13$.
    - **[Round 2]** At $p=2$ the census bounds are superseded qualitatively: $f(a,2)<\infty$ on a set of density $1$ (Theorem 10.1). The census values remain the best *explicit* bounds, e.g. $f(a,2)\le v_2(a!)+31$ on density $0.8984$, because Theorem 10.1 gives no rate.
11. **A negative coverage result [computer-assisted]** (§4.2). $\mathrm{Cov}(5,5,H)$ fails for every $H\le38$. So a uniform-covering proof at $p=5$ needs blocks of length at least $39$ at depth $5$.
12. **A precise target for Q3 (§6).**
    - Prove a uniform covering statement $\mathrm{UC}(p)$ for one prime $p\ge7$. It is already certified for all depths $t\le7$ at $p=13$.
    - Equivalently, prove a joint equidistribution statement for subset sums of the universal vectors $\big((-1)^u/u!,\,(-1)^uH_u/u!,\dots\big)$.

The heuristics (§5) point in a definite direction, but none of it is proved:
- $p=2$ is "critical", and $f(a,2)<\infty$ probably holds for almost all, perhaps all, $a$. Kitamura had already described $p=2$ as a critical branching process (see above). **[Round 2: "almost all" is now Theorem 10.1. "All" remains open.]**
- Every odd $p$ is "supercritical", with $\mu(K_p)\approx0.363$ for $p=3$, $0.522$ for $p=5$, $0.624$ for $p=7$ and $0.700$ for $p=11$.

### Round 2 additions (2026-10-11/12; §10; AI-refereed, not human-refereed)

These were produced in a second AI-assisted session. The lead-author AI instance (Claude; not the human author) checked every proof given as a theorem and re-ran the computations listed in §10.7. Three AI referee instances (logic, computation, novelty) then checked §10, each writing its own code. They found no fatal or serious mathematical error. They found two serious problems of credit and attribution and several minor errors, all corrected below (§10.8). **No human has checked any of it.**

13. **$\mu(K_2)=0$ [proved; AI-refereed] (Theorem 10.1).** Hence $\delta_G(2)\to0$, and $f(a,2)<\infty$ for all $a$ outside a set of natural density $0$. This is the weak form of Conjecture 5.1 and target T4 of §6. The density statement was anticipated empirically by Kitamura, who described $p=2$ as a critical branching process with a decaying surviving fraction (§2). We know of no earlier proof.
    - The proof builds an exact quenched martingale for the carry branching process. It conditions on $x\bmod2^{V_n}$ and weights each path by a "frozen-state" weight. A critical environment walk tends to $-\infty$ along record times, and Doob's maximal inequality finishes the argument; zeros of higher multiplicity are subcritical.
    - It does not decide whether any particular natural number has $f(a,2)=\infty$.
14. **Larger certified lower bounds [computer-assisted; every bound certified by at least two programs] (§10.2).**

    | $p$ | 7 | 11 | 13 | 17 | 19 | 23 |
    |---|---|---|---|---|---|---|
    | $f(1,p)\ge$ (revision 2) | $6\,725\,592$ | $235\,794\,760$ | $883\,708\,272$ | $7\,411\,742\,272$ | $943\,531\,272$ | $3\,559\,590\,232$ |
    | previous (§4) | $10^6$ | $21\,435\,880$ | $67\,977\,552$ | $25\,646\,163$ | $49\,659\,537$ | $154\,764\,790$ |

    The same certificates upgrade the dichotomies for $a\le1000$: every "deep" $a\le1000$ has $f(a,13)\ge883\,708\,272$, $f(a,11)\ge235\,794\,760$ and $f(a,7)\ge6\,725\,592$.
    - *Which programs.* Programs A and B were written by one track instance from one specification, though B builds its blocks from the true factorials. Program C was written from scratch by the round-2 computational referee, and it re-certified every bound in the table. For $f(1,17)\ge7\,411\,742\,272$, programs A (re-run by the lead-author instance) and C certify every component. Program B's half of that bound rests on the track's logs of 2026-10-11 and was not re-run.
    - Also a negative certificate: **$\mathrm{Cov}(11,7,40)$ is false** (four programs).
    - Also a proved *layer obstruction*: $\mathrm{Cov}(p,t,H)$ needs $(H-1)\bmod p\ge\rho_0(p)$ (Lemma 10.11).
15. **What fullness can propagate [proved; abstract core in Lean] (Theorem 10.12, Corollary 10.13).** An exact criterion for when "the incoming carries fill every class mod $p^D$" guarantees crossing a block. Fullness alone does **not** guarantee crossing in two cases. The first is a single level-$j$ gate block, entered with fullness mod $p^D$ for any $D$ with $D_p\le D\le j$, where $D_p=\lceil\log_p(e(p-1)!)\rceil$. The second is a window of length $H$ ending at depth $t$, entered with fullness mod $p^D$ for any $D$ with $e(H-1)!\le p^D\le p^{t-1}$. Whether fullness-only propagation across a whole gate-to-gate stretch (target T3 of §6) can hold is, by Theorem 10.12, a full-coset question about the stretch's subset sums. It is **not** decided here.
16. **Monotonicity of $\mathrm{Cov}$ in $H$ [proved; recursion in Lean] (Proposition 10.14).** If $p\nmid H$ then $\mathrm{Cov}(p,t,H)\Rightarrow\mathrm{Cov}(p,t,H+1)$; this is the $\mathrm{Cov}$-level form of Tao's step, Lemma 1.3(iv). If $1\le v_p(H)\le L_p$ then $\mathrm{Cov}(p,t,H)\Rightarrow\mathrm{Cov}(p,t,H+p)$.
17. **Two sufficient conditions for Q3 [proved; the conditions themselves are unproved].** These are implications, not equivalences.
    - Suppose $\mathrm{Cov}(p,1,H_1)$ and $\mathrm{Cov}(p,2,H_2)$ hold with $H_t+1<p^t$; these are certified for $p=7,11,13$ (§10.2). Suppose also that a random-model Fourier bound $\mathrm{RMF}(p,C)$ holds with $C(\Lambda_p+\tau_p(3))<1$. Then $f(1,p)=\infty$ (Theorem 10.16). Here $\Lambda_7=0.363$, $\Lambda_{13}=0.0351$, and $\Lambda_5=1.24>1$.
    - At $p=13$, every Fourier coefficient of order $\le13^{67\,977\,551}$ can be made to vanish exactly. So Q3 follows from an $L^1$ bound on deep-gate shells alone (Theorem 10.18).
18. **Fourier structure [proved / computer-assisted] (§10.4).**
    - Certified shell sums: $\sum_{k\le7}T_{13}(k)\le0.0093$ and $\sum_{k\le8}T_{11}(k)\le0.0669$.
    - An exact renormalisation identity, valid at the levels $W$ that are attained exactly. It shows that transfer bounds which take a supremum over the bottom levels cannot give decay (Corollary 10.20).
    - A factorial-base digit formula for the Fourier coefficients.

What is **not** new in round 2, and is credited:
- Kitamura (July 2026) described $p=2$ as a critical branching process and observed that the surviving fraction decays (§2). Round 1 formulated the heuristic H1 and target T4 (§5, §6) without crediting this.
- The martingale method follows the classical strategy for branching processes in random environments (Smith–Wilkinson, Athreya–Karlin; Remark 10.8.2).
- The covering framework is Tao's programme as carried out in §3.7.

---

## 1. The problem, notation, and reformulations

### 1.1 Statement

Problem #404 ([ErGr80, p. 79]; erdosproblems.com/404, statement as corrected after Kovač's comment of 13 Aug 2025):

- **(Q1)** For which $a\ge1$ and primes $p$ is $f(a,p)$ finite?
- **(Q2)** How does $f(a,p)$ behave?
- **(Q3)** Is there a prime $p$ and an infinite sequence $a_1<a_2<\cdots$ such that, if $p^{m_k}\,\|\,\sum_{i\le k}a_i!$, then $m_k\to\infty$?

Trivially $f(a,p)\ge v_p(a!)=(a-s_p(a))/(p-1)$, where $s_p$ is the base-$p$ digit sum. So $\lim_a f(a,p)=\infty$ for trivial reasons (Kovač's remark; also `eventual_lower_bound` in formal-conjectures PR #6936). The informative quantity is the **defect** $g$ defined next.

### 1.2 Normal form

Let $\pi_0(x)=1$ and $\pi_b(x)=(x+1)(x+2)\cdots(x+b)$. For finite $B\subset\mathbb Z_{\ge1}$ put
$$S_B(x)=1+\sum_{b\in B}\pi_b(x)\in\mathbb Z[x],\qquad g_p(x)=\sup_B v_p(S_B(x))\in\mathbb Z_{\ge0}\cup\{\infty\}\quad(x\in\mathbb Z_p).$$

**Lemma 1.1 (normal form) [proved+Lean].** For $a\ge1$, $f(a,p)=v_p(a!)+g_p(a)$.

*Proof.* $(a+b)!=a!\,\pi_b(a)$, so $a!+\sum_{b\in B}(a+b)!=a!\,S_B(a)$. Finite sets $T$ with $\min T=a$ correspond bijectively to finite $B=(T-a)\setminus\{0\}$. ∎

(Lean: `factorial_mul_S`, `factorial_add_eq` in `E404Halving.lean`; `normal_form`, `good_iff_fact` in `E404Behaviour.lean`.)

*Credit.* This normalisation is not new. For $p=2$ it is Kitamura's $W_J(a)=1+\sum_{j\in J}P_j(a)$ with $g(a,2)=f(a,2)-v_2(a!)$ (`KitaKen1/erdos-404-p2-landscape`, `determining_exact_values.md` §3, July 2026), and the same division by $a!$ appears in the earlier AI write-ups cited under Proposition 1.2. What we add is the viewpoint of $g_p$ as a function on $\mathbb Z_p$.

### 1.3 Compactness

**Proposition 1.2 [proved].** Let $x\in\mathbb Z_p$. Then $g_p(x)=\infty$ iff there is a finite or infinite $B$ with $1+\sum_{b\in B}\pi_b(x)=0$ in $\mathbb Z_p$. For natural $a$, $f(a,p)=\infty$ iff there is an infinite $A\subseteq[a,\infty)$ with $\min A=a$ and $\sum_{n\in A}n!=0$ in $\mathbb Z_p$. Consequently **Q3 has a positive answer iff $f(a,p)=\infty$ for some $(a,p)$.**

*Proof.* Among any $p$ consecutive elements $x+1,\dots$ of $\mathbb Z_p$ one is divisible by $p$, so $v_p(\pi_b(x))\ge\lfloor b/p\rfloor$. Hence infinite sums converge.

(⇐) Truncate.

(⇒) For each $G$ let $X_G$ be the set of $B\subseteq[1,pG)$ with $p^G\mid S_B(x)$. It is finite and nonempty: take a witness for $g\ge G$ and delete the terms $b\ge pG$, which vanish mod $p^G$. Moreover $B\mapsto B\cap[1,pG)$ maps $X_{G+1}\to X_G$. König's lemma gives a compatible infinite $B$, and $S_B(x)=0$.

For natural $a$, use Lemma 1.1. The set $A$ must be infinite because a positive integer is not $0$.

For Q3: given $f(a,p)=\infty$ with set $A$, list $A$ increasingly. The partial sums satisfy $v_p(\sum_{i\le k}a_i!)=v_p(\text{tail}_k)\ge v_p(a_{k+1}!)\to\infty$. Conversely, a Q3 sequence gives $f(a_1,p)=\infty$. ∎

Define the closed **infinity set** $K_p:=\{x\in\mathbb Z_p:g_p(x)=\infty\}$. Then

$$\boxed{\;f(a,p)=\infty\iff a\in K_p,\qquad \text{Q3}\iff K_p\cap\mathbb Z_{\ge1}\ne\emptyset\text{ for some }p.\;}$$

(Track A named this set $\mathcal Z_p$ and track D named it $E_p$.)

*Credit.* The equivalence "$f(a,p)=\infty$ iff an infinite cancelling sequence starts at $a$, so Q3 holds iff some $f(a,p)=\infty$" is not new. It is sketched in `neelsomani/gpt-erdos` (`data/solutions/404/candidate_solution.md`, 2026-01-17), proved by a diagonal/compactness argument in `erichou1/erdos-open-problems` (`solutions/open/solution_404.md`, 2026-06-10, "exact $p$-adic reformulation"), and proved by an explicit König-type argument in `AItoBit/Erdosproblems-llm-hunter` (`GPT_6_Astra_Ultra/404.tex`, 2026-09-25). These are unrefereed AI-generated write-ups. Only the packaging of $K_p$ as a closed subset of $\mathbb Z_p$ is ours.

### 1.4 Tao's predicate, blocks, carries

Following Tao (forum, 29 Sep 2025), let $P(a,p,N)$ be the assertion that $p^{v_p(N!)}\mid\sum_{n\in T}n!$ for some finite $T\subseteq[a,N)$ with $\min T=a$.

**Lemma 1.3 [proved].**
- (i) For $N>a$: $f(a,p)\ge v_p(N!)\iff P(a,p,N)$.
- (ii) $P(a,p,N')\Rightarrow P(a,p,N)$ for $a<N\le N'$.
- (iii) *(Tao's block lemma)* Suppose $P(a,p,N)$ holds and the $2^H$ subset sums of $\{n!/p^{v_p(N!)}:N\le n<N+H\}$ cover $\mathbb Z/p^{v_p((N+H)!/N!)}$. Then $P(a,p,N+H)$ holds.
- (iv) If $p\nmid N$ then $P(a,p,N-1)\Rightarrow P(a,p,N)$.
- (v) *(Partial coverage.)* Suppose $P(a,p,N)$ holds, $N<M$, and the subset sums of $\{n!/p^{v_p(N!)}:N\le n<M\}$ cover $\mathbb Z/p^L$ for some $L\le v_p(M!)-v_p(N!)$. Then $f(a,p)\ge v_p(N!)+L$.

Parts (iii) and (iv) are stated in Tao's comment; (v) is the obvious variant of (iii) and is used in Theorem 3.9(c) and §4.4.

*Proof.*
- (i) and (ii): restrict a witness to $[a,N)$. The deleted terms are divisible by $p^{v_p(N!)}$.
- (iii): if $\sigma\equiv0 \pmod{p^{v(N!)}}$, choose a block subset whose normalised sum is $\equiv-\sigma/p^{v(N!)}$.
- (iv): $v_p(N!)=v_p((N-1)!)$.
- (v): as in (iii), choose a block subset whose normalised sum is $\equiv-\sigma/p^{v(N!)} \pmod{p^L}$. The total sum is then divisible by $p^{v(N!)+L}$. ∎

(Lean, `E404Block.lean`: `block_lift`, `first_failure`, `all_below`.)

So $f(a,p)=\infty$ iff $P(a,p,N)$ holds for all $N>a$. Let $N^*(a)$ be the **first failure**, the least $N>a$ with $\neg P(a,p,N)$. Then $p\mid N^*$, and $v_p((N^*-1)!)\le f(a,p)<v_p(N^*!)$.

*Carries.* Put $S_N=\sum_{n\in A,n<N}n!$ and $\gamma_N=S_N/N!$. Then $\gamma_{N+1}=(\gamma_N+e_N)/(N+1)$ with $e_N=\mathbf 1_{N\in A}$. Also $P(a,p,N)$ holds iff some admissible $0/1$ path has $\gamma_N\in\mathbb Z_p$.

### 1.5 Achievement sets

For $x\in\mathbb Z_p$ let $A_x=\{\sum_{j\ge0}e_j\pi_j(x):e\in\{0,1\}^{\mathbb N}\}$. This is compact. Note that $\{S_B(x)\}$ is the part of $A_x$ with $e_0=1$, and that $A_x \bmod p^k$ depends only on $x \bmod p^k$.

For natural $N$, $N!\,A_N=E_N:=\{\sum_{n\in B}n!:B\subseteq[N,\infty)\}\subseteq p^{v_p(N!)}\mathbb Z_p$. This is the "tail set" of track F.

Call $x$ **full** if $A_x=\mathbb Z_p$, and put $\mathcal G_p=\{x:A_x=\mathbb Z_p\}$, a closed set.

**Lemma 1.4 [proved].**
- (a) If $A_N=\mathbb Z_p$ and $P(a,p,N)$ holds ($a<N$), then $f(a,p)=\infty$.
- (b) If $A_N=\mathbb Z_p$, then $f(a,p)\in[v_p(a!),v_p(N!))\cup\{\infty\}$ for every $a<N$.
- (c) If $A_N=\mathbb Z_p$ and $p\nmid N$, then $f(N-1,p)=\infty$.

*Proof.*
- (a) Take a finite $F\subseteq[a,N)$ with $\min F=a$ and $\sigma_F=\sum_F n!\equiv0 \pmod{p^{v(N!)}}$. Then $-\sigma_F\in p^{v(N!)}\mathbb Z_p=E_N$, so $-\sigma_F=\sum_{n\in B}n!$ for some $B\subseteq[N,\infty)$. Now apply Proposition 1.2.
- (b) Combine (a) with Lemma 1.3(i).
- (c) We need $\sum_{n\ge N}e_nn!/N!=-(N-1)!/N!=-1/N\in\mathbb Z_p$. ∎

### 1.6 A correction to the commonly quoted grouping identity

Write $n=pm+r$ with $0\le r<p$. Then
$$n!=p^m\,m!\,W_m\prod_{j=1}^r(pm+j),$$
where $W_m=(pm)!/(p^mm!)=\prod_{i\le pm,\,p\nmid i}i$ is a $p$-adic unit with $W_m\equiv(-1)^m \pmod p$. Some informal accounts omit the unit $W_m$. **[proved]**: separate the multiples of $p$, and use $(p-1)!\equiv-1$.

---

## 2. State of the art before this note (with credit)

- **Erdős–Graham [ErGr80, p. 79]** posed the problem, together with #403.
- **S. Lin** (Bell Labs internal memorandum, 1960; cited on erdosproblems.com as [Li76]; unpublished and not online) showed that $2^{254}$ is the largest power of 2 dividing a sum of distinct factorials containing $2!$. That is, $f(2,2)=254$; the #404 page records $f(2,2)\le254$. Lin also found the five solutions of $3^m=\sum$ distinct factorials (#403). Frankl independently solved #403.
- **V. Kovač** (forum, 13 Aug 2025) corrected the statement and recorded $f(1,2)=0$, $f(2,2)=254$, $f(3,2)=1$, $f(4,2)=6$ and $f(5,2)=3$. Kovač noted that $\lim_a f(a,p)=\infty$ ("clearly").
- **T. Tao** (forum, two comments of 29 Sep 2025):
  - Tao suggested that $f(1,5)$ is "extremely large, and possibly even infinite", with examples such as $1!+4!+10!+11!$.
  - Tao stated the block lemma (Lemma 1.3(iii)) and its special case $P(a,p,N)\Rightarrow P(a,p,N+1)$ for $p\nmid N+1$ (Lemma 1.3(iv)).
  - Tao suggested checking computationally that the $2^p$ subset sums of $0!,\dots,(p-1)!$ cover $\mathbb Z/p$, which gives the step over a block of length $p$ ending at a multiple of $p$ exactly once (compare Theorem 3.9(a)).
  - Tao observed that, more generally, the step across a multiple of exactly $p^j$ should reduce to one fixed finite computation for each $j$ (calling the case $N=0$ "key"), and that doing this for all $j\le J$ would give $f(a,p)\ge v_p((p^{J+1}-1)!)$. Theorems 3.9(b) and 3.12(a) below make this position-independence precise; the $\mathrm{Cov}$/$\mathrm{UC}$ framework of §3.7 carries out Tao's programme.
- **K. Kitamura** (Jul 2026, AI-assisted; repositories `KitaKen1/erdos-404-p2-landscape` and `KitaKen1/erdos-404-odd-prime-landscape`):
  - Exact $f(a,2)$ for $1\le a\le256$, including $f(34,2)=18444$, and deeper exact rows $f(1102,2)=12633$, $f(3456,2)=8275$ and $f(8190,2)=16396$. Each is certified from both sides.
  - A two-sided Lean check of $f(2,2)=254$. The parity argument that odd $a$ give $f(a,2)=v_2(a!)$, with a Lean certificate for $f(5,2)=3$.
  - *Structural facts at $p=2$* (`README.md`, `determining_exact_values.md` §§3–5, `witness_gallery.md` §§3, 7, 8):
    - the normalisation $W_J(a)$, $g(a,2)=f(a,2)-v_2(a!)$ (our Lemma 1.1);
    - the *determinacy* lemma: whether $g(a,2)\ge G$ depends only on $a \bmod 2^G$ (our Theorem 3.1(a) at $p=2$);
    - the cube identity $a!+(a+1)!+(a+3)!=a!(a+2)^3$, so $g\ge3$ for every even $a$;
    - a certified classification of all even classes with $g\le24$ (174,640 residue classes). From it: $g$ never takes the values $1,2,4,5$, $g=3$ exactly on $a\equiv4 \pmod 8$, and the attained values up to 24 are exactly $\{3\}\cup[6,24]$. These are computer-certified statements, not merely empirical ones. The classification also gives $f(a,2)<\infty$ on a set of density $1-\delta_{25}(2)=0.8734$;
    - the *shadow family* $a=2^t-2$, with $g\ge3t$ from the cube identity and exact values for $t\le13$ (for example $g(8190,2)=8218$);
    - the *sibling-pairing theorem*, $g(a+2^{g(a)},2)=g(a,2)$, so $g$ is constant on $a \bmod 2^{g(a)}$. It is stated without a shipped proof. Kitamura also reports certified "dead balls", for example $g\equiv648$ on $254+2^{638}\mathbb Z_2$.
  - **[Round 2; credit added after the round-2 novelty referee]** A branching-process picture at $p=2$. In `witness_gallery.md` §6 Kitamura calls the deep spikes "the predictable thin tail of a critical branching process", and reports a measured survival probability to depth $G$ of about $11.5/G$ (also `determining_exact_values.md` §5 and `README.md`), so that the census determines $f(a,2)$ for most integers. This is the empirical precursor of the heuristic H1 (§5) and of the weak form of Conjecture 5.1, which Theorem 10.1 proves. Kitamura's fit $\approx11.5/G$ and the fit $\delta_G(2)\approx0.7/\sqrt G$ of §5 differ. We have not reconciled them, and the normalisations may differ.
  - The lower bound $f(594,2)\ge66126$, for which no witness is shipped.
  - Exact odd-prime rows: $f(3,3)=3$, $f(39,3)=25$, $f(700,3)=363$, $f(110,5)=30$, $f(236,5)=61$, $f(42,7)=7$, $f(113,11)=11$ and $f(163,13)=13$. Lean checks of $f(3,3)=3$, $f(4,7)=0$ and $f(6,7)=0$.
  - Witnesses $f(1,3),f(1,5),f(1,7)\ge20000$ and $f(1,11),f(1,13)\ge5000$.
  - Two odd-prime "residue patterns to audit further": $g(a,3)=1$ for $a\equiv6 \pmod 9$ and $g(a,5)=2$ for $a\equiv-5 \pmod{125}$. Theorem 3.2 proves both.
- **Earlier AI write-ups** (unrefereed, public on GitHub):
  - `neelsomani/gpt-erdos` (2026-01-17): the $a\equiv-1$ family and a sketch of the compactness equivalence;
  - `erichou1/erdos-open-problems`, `solutions/open/solution_404.md` (2026-06-10): the normal form, an "exact $p$-adic reformulation" with a compactness proof, and a first-digit obstruction;
  - `AItoBit/Erdosproblems-llm-hunter`, `GPT_6_Astra_Ultra/404.tex` (2026-09-25): a finite residue test for each threshold, an explicit König-type proof of the equivalence, the $a\equiv-1$ family, and $f(a,p)\ge v_p(a!)+v_p(a+2)$.

  Other AI-generated notes on #404 exist (for example in `przchojecki/agentic-erdos` and `ryantuck/erdos-ai`). We have not audited all of them.
- **Trivial family.** If $a\equiv-1 \pmod p$ then $f(a,p)=v_p(a!)$, because every later factorial is divisible by $(a+1)!$.
- **Formalisation.** google-deepmind/formal-conjectures PR #6936 (AItoBit, opened 2026-10-08) states parts (i)–(iii) with `sorry`. It proves only API lemmas and the eventual lower bound.
- **Status** (checked 2026-10-08):
  - erdosproblems.com/404 is open, last edited 29 Sep 2025, with 0 proof claims; commenting is suspended.
  - teorth/erdosproblems lists it as open and unformalised.
  - No refereed paper treats $p$-adic valuations of sums of distinct factorials.
  - No relevant MathOverflow thread exists; MO 476702, on $v_p(1!+\dots+n!)$, is related but different.
  - A Zenodo preprint (10.5281/zenodo.23144232, v2, 2026-10-04) contains "theorems" about $f(a,p)$. One of its claims would imply $f(2,2)=\infty$, contradicting Lin's bound; we do not regard it as progress.
- **Adjacent literature (no direct implication):**
  - Kurepa's left-factorial conjecture, verified to $2^{40}$ by Andrejić–Bostan–Tatarevic, IPL 167 (2021). Note that $!p \bmod p$ is the residue of the full first block.
  - Distribution of $n! \bmod p$ (Garaev–Luca–Shparlinski; Klurman–Munsch). These are mod-$p$ results only.
  - Morita's $p$-adic Gamma function.
  - Real achievement sets (Guthrie–Nymann; the survey arXiv 2512.17285). No $p$-adic analogue was found.

---

## 3. Rigorous results

The results below were obtained in a single AI-assisted session of six parallel investigations, labelled A–F in §7. The track labels record provenance only; they are not novelty claims. A novelty referee (§9) found that some statements in this section were already public. Each such case is credited where it occurs (Theorem 3.1(a), Corollary 3.7.1, Proposition 3.4, and the Tao programme behind Theorems 3.9 and 3.12), and §0 lists what we regard as new. Searches covered the arXiv API, OpenAlex, GitHub, MathOverflow and erdosproblems.com (2026-10-08). We cannot exclude overlap with other unpublished or AI-generated work.

### 3.1 Locality and densities

**Theorem 3.1 [proved+Lean (a)].**
- (a) If $x\equiv y \pmod{p^G}$ then $g_p(x)\ge G\iff g_p(y)\ge G$. Equivalently, $g_p(x)\ge\min(g_p(y),v_p(x-y))$.
- (b) $\{g_p\ge G\}$ is a union of classes mod $p^G$. $K_p=\bigcap_G\{g_p\ge G\}$ is closed. If $g_p(a)=G<\infty$, then $g_p\equiv G$ on $a+p^{G+1}\mathbb Z_p$, so $f(b,p)=v_p(b!)+G$ for every natural $b\equiv a \pmod{p^{G+1}}$.
- (c) The natural density of $\{a\ge1:f(a,p)\ge v_p(a!)+G\}$ exists and equals $\delta_G(p):=p^{-G}\#\{c \bmod p^G:g_p(c)\ge G\}$. It is non-increasing in $G$ with limit $\mu(K_p)$ (Haar measure). The upper density of $\{a:f(a,p)=\infty\}$ is at most $\mu(K_p)$.

*Proof.*
- (a) $S_B\in\mathbb Z[x]$, so $S_B(x)\equiv S_B(y) \pmod{p^G}$ for each $B$.
- (b) This follows from (a). For the exact value: $g(b)\ge G$, and $g(b)\ge G+1$ would force $g(a)\ge\min(g(b),v(a-b))\ge G+1$.
- (c) A set periodic mod $p^G$ has density equal to its class count. The sets $\{g\ge G\}$ are clopen and decreasing. ∎

(Lean: `residue_lemma` in `E404Halving.lean`; `locality` in `E404Behaviour.lean`.)

*Credit.* Part (a) at $p=2$ is Kitamura's determinacy lemma (`determining_exact_values.md` §3), with the observation that every computed row is therefore a residue-class theorem. The proof for general $p$ is the same. Part (c) follows at once from (a).

### 3.2 Exact values on explicit residue classes ("shadows of negative integers")

For $m\ge1$ put $\gamma_p(m):=g_p(-m)$. Since $\pi_b(-m)=0$ for $b\ge m$,
$$\gamma_p(m)=\max_{B\subseteq[1,m-1]}v_p\big(S_B(-m)\big),\qquad S_B(-m)=1+\sum_{b\in B}\prod_{l=1}^{b}(l-m).$$

**Theorem 3.2 [proved+Lean (a)].** (Tracks A, C, D and E.)
- (a) $S_B(-m)\ne0$ for all $B$ when $m\ne2$, while $S_{\{1\}}(-2)=0$. Hence $K_p\cap\mathbb Z_{<0}=\{-2\}$ for every $p$, and $\gamma_p(m)<\infty$ for $m\ne2$.
- (b) $|S_B(-m)|\le\lfloor e\,(m-1)!\rfloor$, so $\gamma_p(m)\le\log_p\lfloor e(m-1)!\rfloor$.
- (c) For every $m\ne2$ and every $a\ge1$ with $a\equiv-m \pmod{p^{\gamma_p(m)+1}}$:
$$f(a,p)=v_p(a!)+\gamma_p(m).$$

*Proof.*
- (a) For $b\ge1$, the product $\prod_{l=1}^b(l-m)$ contains the factor $1-m$. So $S_B(-m)\equiv1 \pmod{m-1}$, which is nonzero when $m\ge3$. For $m=1$, $S_B=1$. For $m=2$, $1+(1-2)=0$.
- (b) $\sum_{b=0}^{m-1}(m-1)!/(m-1-b)!=\lfloor e(m-1)!\rfloor$.
- (c) Locality (Theorem 3.1(a)) with $y=-m$: we get $g(a)\ge\min(\gamma,v(a+m))\ge\gamma$. If $g(a)\ge\gamma+1$, then $\gamma=g(-m)\ge\min(g(a),v(a+m))\ge\gamma+1$, which is absurd. ∎

(Lean: `sigma_ne_zero` in `E404Structure.lean` and `NS_ne_zero` in `NoCancel.lean`, the non-vanishing in two equivalent forms; `frozen_m1`, `frozen_m3`, `frozen_m4` and `frozen_f` in `E404Frozen.lean` for $m=1,3,4$ at every prime, stated directly for factorial sums.)

*Values.* Computed by exhaustive enumeration, and re-verified in `indep_checks.py` for $m\le14$, $p\le13$:
- $\gamma_2(m)$ for $m=4,6,8,10,12,14,18,24,26,30,34$: $3,6,8,10,3,15,22,26,29,30,39$; $\gamma_2(m)=0$ for odd $m$.
- $\gamma_3(m)$ for $m=3,5,6,8,9,11$: $1,3,4,7,5,7$.
- $\gamma_5(m)$ for $m=4,5,7,17$: $1,2,4,7$.
- $\gamma_7(4)=1$ and $\gamma_{13}(13)=3$.

*Examples.*
- $f(a,3)=v_3(a!)+1$ for all $a\equiv6 \pmod 9$. This proves the first of Kitamura's two "residue patterns to audit further".
- $f(a,5)=v_5(a!)+2$ for all $a\equiv-5 \pmod{125}$, since $\gamma_5(5)=2$. This proves the second.
- $f(a,3)=v_3(a!)+3$ for $a\equiv-5 \pmod{81}$.
- $f(a,2)=v_2(a!)+15$ for $a\equiv-14 \pmod{2^{16}}$.
- $f(a,5)=v_5(a!)+7$ for $a\equiv-17 \pmod{5^8}$.

The values $\gamma_2(4)=3$ and $\gamma_2(12)=3$ also give $g=3$ on $a\equiv4,12 \pmod{16}$.

**Corollary 3.3 (frozen classes; exact density of $f=v_p(a!)$) [proved].** For $a\ge1$ let $r=a \bmod p$ and $m=p-r\in[1,p]$. Then
$$f(a,p)=v_p(a!)\iff\gamma_p(m)=0\iff r\in\Phi_p:=\{r: p\nmid S_B(r-p)\ \forall B\subseteq[1,p-r-1]\}.$$
Consequences:
- The natural density of $\{a:f(a,p)=v_p(a!)\}$ is exactly $|\Phi_p|/p$.
- $p-1\in\Phi_p$ always (this is the classical family). $p-2\notin\Phi_p$.
- $p-3\in\Phi_p$ for all $p\ge5$, since $S_B(-3)\in\{1,-1,3\}$.
- $p-1-j\in\Phi_p$ whenever $j\ne1$ and $p>\lfloor e\,j!\rfloor$. Hence $|\Phi_p|\ge\#\{m\in\{1\}\cup[3,p]:\lfloor e(m-1)!\rfloor<p\}\gg\log p/\log\log p$.
- Examples: $\Phi_3=\{2\}$, $\Phi_5=\{2,4\}$, $\Phi_7=\{4,6\}$, $\Phi_{11}=\{7,8,10\}$, $\Phi_{13}=\{9,10,12\}$, $\Phi_{17}=\{12,13,14,16\}$, $\Phi_{19}=\{14,15,16,18\}$ and $\Phi_{23}=\{19,20,22\}$. These were re-verified by an independent oracle.

*Proof.* $a\equiv-m \pmod p$. By locality at level $1$, $g(a)\ge1\iff\gamma_p(m)\ge1$. The rest follows from Theorem 3.2. ∎

Numerically, $|\Phi_p|$ averages $\approx\log_2p-1$ for $p<30000$ **[heuristic]**. The prior state of knowledge was the single class $r=p-1$. (This is Theorem 2 of track E; track A has the special case $p>M_t$ and track C the "$p>e(K-1)!$" form.)

**Proposition 3.4 (finite values of $g_p$ are unbounded; the point $-2$) [proved].**
- (a) $S_{\{1,3\}}(x)=(x+2)^3$, hence $g_p(x)\ge3v_p(x+2)$ for all $x$. (This is Kitamura's cube identity.)
- (b) $-2$ is the only rational root of any $S_B$. Its multiplicity is at most $3$, with equality only for $B=\{1,3\}$.
- (c) For every $k\ge1$: $3k\le\gamma_p(p^k+2)<\infty$. Hence for every $k$ there is an explicit residue class, namely $a\equiv-(p^k+2) \pmod{p^{\gamma+1}}$, on which $f(a,p)-v_p(a!)$ is **finite and at least $3k$**.

  In particular: *there is no constant $C_p$ such that every $a$ has $g_p(a)\le C_p$ or $g_p(a)=\infty$.* (This disproves an internal working conjecture of track F, suggested by gap tables for $a\le300$. No published source proposed it.)
- (d) $\liminf_a g_p(a)=0$ and $\limsup_a g_p(a)=\infty$ over natural $a$.

*Proof.*
- (a) Direct expansion.
- (b) $S_B$ is monic in $\mathbb Z[x]$, so rational roots are integers. $S_B(n)\ge1$ for $n\ge0$, $S_B(-1)=1$, and $S_B(-m)\neq0$ for $m\ge3$ by Theorem 3.2(a). For the multiplicity, put $y=x+2$.
  - If $1\notin B$, then $S_B(-2)=1$.
  - If $1\in B$, then $S_B=y\,[1+(y-1)T(y)]$ with $T(y)=\sum_{b\in B,b\ge2}\pi_{b-2}(y)$. So $y^2\mid S_B$ iff $T(0)=\sum(b-2)!=1$, iff $B\cap[2,\infty)\in\{\{2\},\{3\}\}$. These give $y^2$ and $y^3$ respectively.
- (c) $m=p^k+2\ge3$, so $\gamma_p(m)<\infty$ by Theorem 3.2. Also $-m+2=-p^k$, so (a) gives $\gamma_p(m)\ge3k$.
- (d) The class $a\equiv-1$ gives $g=0$. For the limsup take $a=p^k-2$ in (a). ∎

*Credit.* At $p=2$, the points $a=2^t-2$ are Kitamura's shadow family: Kitamura notes $g\ge3t$ and computes exact finite values for $t\le13$ (`witness_gallery.md` §7). So (d) at $p=2$, and finite values of $g_2$ up to $8218$, were known. The term "shadow" in §3.2 is also Kitamura's. What we believe is new is (b), and (c) at every prime: finite values that are provably unbounded, located on explicit classes via the negative points $-(p^k+2)$.

Spot checks: $\gamma_2(2^k+2)=3,6,10,22,39$ for $k=1,\dots,5$, each $\ge3k$; $\gamma_3(5)=3$ and $\gamma_3(11)=7$.

### 3.3 Hensel dichotomy and the impossibility of finite-depth certificates

**Theorem 3.5 (dichotomy mod $p$) [proved].** For each residue $r\notin\Phi_p$ there are an explicit finite $T$ and a simple root $\alpha_r\in\mathbb Z_p$ of $S_T$ with $\alpha_r\equiv r \pmod p$. Hence $\alpha_r\in K_p$ and $g_p(a)\ge v_p(a-\alpha_r)$. So on each class mod $p$, $g_p$ is either identically $0$ (when $r\in\Phi_p$) or unbounded. No $\alpha_r$ is a natural number, by Proposition 3.4(b).

*Proof.* Let $k^*\ge1$ be least with $p\mid r+k^*$. Terms $\pi_b(r)$ with $b\ge k^*$ vanish mod $p$, so some $T_0\subseteq[1,k^*)$ has $p\mid S_{T_0}(r)$. Modulo $p$, $\pi_{k^*}'(r)\equiv\prod_{l<k^*}(r+l)\not\equiv0$, because every other term of the product rule contains the factor $r+k^*$. Therefore one of $S_{T_0}$ and $S_{T_0\cup\{k^*\}}$ has value $\equiv0$ and derivative $\not\equiv0$ mod $p$, and Hensel's lemma applies. ∎ (Track E.)

**Theorem 3.6 (no finite-depth certificate) [proved].** Both $K_p$ and $\mathcal G_p$ have empty interior in $\mathbb Z_p$.
- (a) Every class $r \bmod p^{k_0}$ contains infinitely many natural $a$ with $f(a,p)<\infty$, with explicit values from Theorem 3.2.
- (b) If $p^K>2^L$, then $A_N\ne\mathbb Z_p$ for every $N\equiv-L \pmod{p^K}$.

Consequently no property of $a$ depending only on $a \bmod p^{k_0}$ can imply $f(a,p)=\infty$. In particular "Tao covering holds on a whole residue class of $N$" is impossible: any certificate of $f(a,p)=\infty$ must inspect unboundedly many $p$-adic digits of $a$.

*Proof.*
- (a) Choose $m\ge3$ with $-m\equiv r \pmod{p^{k_0}}$, and use $a\equiv-m \pmod{p^{\max(k_0,\gamma_p(m)+1)}}$.
- (b) $A_N \bmod p^K=A_{-L} \bmod p^K$, and $\pi_j(-L)=0$ for $j\ge L$, so $|A_{-L}|\le2^L$. ∎

(Track A. Example: every lift of $0 \bmod 25$ lies in the computed $\mathcal G_8$ for $p=5$, yet $N\equiv-25 \pmod{5^{11}}$ is not full.)

### 3.4 The prime 2

**Theorem 3.7 (halving lemmas) [proved+Lean].** (Tracks D and E.) We found no earlier statement or proof of the halving lemmas themselves.
- (a) For $G\ge2$ and all $x\in\mathbb Z$: $g_2(x)\ge G\iff g_2(x+2^{G-1})\ge G$.
- (b) For $G\ge6$ and $x\equiv2 \pmod 4$: $g_2(x)\ge G\iff g_2(x+2^{G-3})\ge G$.

*Proof of (a).*
- If $x$ is odd, every $S_B(x)$ is odd, so both sides are false.
- If $2^{G-1}\mid x+2$, then $S_{\{1,2\}}(y)=(y+2)^2$ gives $\ge2(G-1)\ge G$ on both sides.
- Otherwise $t=v_2(x+2)\le G-2$. Let $2^G\mid S_B(x)$.
  - For $b\ge4$, $\pi_b(x)$ contains $(x+2)(x+4)$, so it has valuation $\ge t+1$.
  - Hence $S_B(x)\equiv1+e_1(x+1)+e_2(x+1)(x+2)+e_3(x+1)(x+2)(x+3) \pmod{2^{t+1}}$. If $e_1=0$, this is odd.
  - So $e_1=1$, and $S_B\equiv(x+2)[1+e_2(x+1)+e_3(x+1)(x+3)]$. The bracket is $\equiv1+e_2+e_3 \pmod 2$, so $|B\cap\{1,2,3\}|=2$.
- For even $x$: $\pi_1'=1$; $\pi_2'(x)\equiv1$; $\pi_3'(x)\equiv1$; and $\pi_b'(x)$ is even for $b\ge4$, since every term of the product rule keeps an even factor. Hence $S_B'(x)$ is even.
- Taylor: $S_B(x+h)\equiv S_B(x)+hS_B'(x) \pmod{h^2}$ with $h=2^{G-1}$, so $2^G\mid S_B(x+h)$.
- The converse follows by applying the forward direction at $x+h$, since $x+2h\equiv x \pmod{2^G}$. ∎

*Proof of (b) (sketch; complete in Lean).*
- If $2^{G-3}\mid x+2$, the cube $(x+2)^3$ settles it.
- Otherwise $t=v_2(x+2)\in[2,G-4]$.
- Work modulo $2^{t+2}$. For $b\ge6$, $v_2(\pi_b(x))\ge t+3$, and $\pi_4,\pi_5$ have valuation exactly $t+1$. So every witness has $1\in B$, exactly one of $2,3\in B$, and $4\in B\iff5\in B$.
- For $x\equiv2 \pmod 4$: $\pi_b'(x)\equiv1,7,7,6,2 \pmod 8$ for $b=1,\dots,5$, and $\equiv0$ for $b\ge6$. So $S_B'(x)\equiv0 \pmod 8$.
- The Taylor terms of order $\ge2$ in $h=2^{G-3}$ vanish mod $2^G$ when $G\ge6$.
- The converse uses 7 more forward steps. ∎

(Lean: `E404.halving`, `E404.halving2` in `E404Halving.lean`; `E404.sibling`, `E404.constancy`, `E404.constancy_f` in `E404Behaviour.lean`. The last of these is stated directly for factorial sums with $v_2$ given by `Nat.factorization`.)

**Corollary 3.7.1 [proved+Lean / computer-assisted (iii)].**
- (i) If $g_2(a)=G\ge1$, then $g_2\equiv G$ on $a+2^G\mathbb Z$. For instance $f(a,2)=v_2(a!)+253$ for all $a\equiv2 \pmod{2^{253}}$. This proves Kitamura's "sibling-pairing theorem" $g(a+2^{g(a)},2)=g(a,2)$ (`witness_gallery.md` §8), which Kitamura states without a shipped proof. The Lean name `E404.sibling` follows Kitamura's terminology. (The hypothesis $G\ge1$ is needed: at $G=0$ the statement would say that $g_2$ vanishes identically.)
- (ii) In the 2-adic tree of classes $\{g\ge G\}$, every surviving class has $0$ or $2$ surviving children.
- (iii) $g_2(a)\in\{0,3\}\cup[6,\infty]$. Moreover $g_2(a)=0\iff a$ is odd, and $g_2(a)=3\iff a\equiv4 \pmod 8$.
  - The direction ⇐ of the last statement is Lean `E404.g_eq_three`.
  - The rest follows from the class counts $|\{g\ge k\} \bmod 2^k|=1,2,4,6,12,24$ for $k=1,\dots,6$, a 64-class computation re-run in `indep_checks.py`. Locality (Theorem 3.1(a)) alone suffices to turn these counts into the statement; the halving lemma gives a second route.
  - *Credit.* All of (iii) was already stated by Kitamura, as a consequence of the determinacy lemma and the certified classification of the classes with $g\le24$ (§2). We include it only as an independent confirmation.
- (iv) The analogue of (i) **fails** for odd $p$: $g_3(3)=2$ but $g_3(12)\ge30$. (The value "$g_3(12)=10$" in some summaries is only a lower bound.) For odd $p$ the correct statement is constancy mod $p^{g+1}$, from Theorem 3.1(b).

**Theorem 3.8 (Tao's covering method is impossible at $p=2$) [proved+Lean].** For every $r \bmod 16$, the subset sums of $\{\pi_j(r):0\le j\le15\}$ miss some residue mod 16. Hence $A_x\ne\mathbb Z_2$ for every $x\in\mathbb Z_2$.

Consequently, if $N<M$ and $v_2(M!/N!)\ge4$, the block $\{n!/N!:N\le n<M\}$ never covers $\mathbb Z/2^{v_2(M!/N!)}$. Since covering blocks compose (Lemma 1.3(iii)), any chain of covering blocks starting from $P(a,2,N)$ certifies at most $f(a,2)\ge v_2(N!)+3$.

*Proof.* The finite check is Lean `two_adic_never_full` (`E404Structure.lean`, by `decide`). Terms with $j\ge16$ contain 16 consecutive factors and vanish mod 16. Covering by a block would make $A_N \bmod 16$ full. ∎ (Track A. The independent oracle reproduces the check.)

### 3.5 Gate structure for odd $p$; the series $e^{-1}$

Write $e_m=v_p((pm)!)=m+v_p(m!)$. Block $m$ is $\{pm,\dots,pm+p-1\}$, and its jump is $e_{m+1}-e_m=1+v_p(m+1)$. Call block $m$ a *gate of level $j$* if $v_p(m+1)=j$.

**Theorem 3.9 [proved; Lean for (b)].** Let $p$ be odd. (Tracks B and C.) Part (a) is the non-gate step that Tao proposed to check computationally (§2); Cauchy–Davenport makes it unconditional. Part (b) is the position-independence that Tao anticipated ("the $N=0$ case being key").
- (a) *(Non-gates.)* If $p\,\|\,N$ and $N-p+1>a$, then $P(a,p,N-p+1)\Rightarrow P(a,p,N)$.
- (b) *(Gate congruence.)* If $p^j\mid m+1$, then for $0\le r<p$,
$$P_m(r):=\prod_{i=1}^r(pm+i)\equiv\prod_{i=1}^r(i-p)=(p-1)!\,\frac{(-1)^{u}}{u!}\pmod{p^{j+1}},\qquad u=p-1-r.$$
  So modulo $p^{j+1}$, the normalised subset sums of a level-$\ge j$ gate block are a unit times the subset sums $\Sigma(E_p)$ of
$$E_p=\Big\{\tfrac{(-1)^u}{u!}:0\le u<p\Big\}\subset\mathbb Z_p,$$
  the truncated series for $e^{-1}$. This holds independently of the position of the gate.
- (c) Let $L_p=\max\{L:\Sigma(E_p) \bmod p^L=\mathbb Z/p^L\}$, so $L_p\ge1$ by Cauchy–Davenport. Every gate of level $\le L_p-1$ is crossed by its own block from any carry, and
$$f(1,p)\ \ge\ p+p^2+\dots+p^{L_p}.$$
- (d) *(Gap theorem.)* Write $a=pm_0+(p-k)$ with $1\le k\le p$, and let $\tau=\gamma_p(k)$, where $\gamma_p(1)=0$ and $\gamma_p(2)=\infty$.
  - If $\tau\le v_p(m_0+1)$, then $g_p(a)=\tau$.
  - Otherwise $g_p(a)\ge L_p+1$.

  Hence $g_p(a)\in\{\gamma_p(p-(a \bmod p))\}\cup[L_p+1,\infty]$, writing $p-0$ as $p$ when $p\mid a$. In particular $a\equiv-2 \pmod p$ forces $g_p(a)\ge L_p+1$.

*Proof.*
- (a) The $p-1$ elements $n!/p^{v((N-p+1)!)}$, $N-p+1\le n<N$, all have valuation $0$, and the jump is $1$. Cauchy–Davenport gives $|\{0,x_1\}+\dots+\{0,x_k\}|\ge\min(p,k+1)$ for nonzero $x_i$. (Mathlib's `ZMod.cauchy_davenport`; our `SubsetSumsCD.lean`.)
- (b) $pm+i=(i-p)+p(m+1)$ and $p^{j+1}\mid p(m+1)$. Also $\prod_{i\le r}(i-p)=(-1)^r(p-1)!/(p-1-r)!$, and $(-1)^r=(-1)^u$ for odd $p$. (Lean: `gate_factor`, `gate_prod` in `NoCancel.lean`.)
- (c) At a block of level $j\le L_p-1$ (including $j=0$, the non-gates) the jump is $j+1\le L_p$, and by (b) the block sums cover $\mathbb Z/p^{j+1}$.
  - For $a=1$: $P(1,p,p)$ holds via $1!+(p-1)!\equiv0 \pmod p$ (Wilson).
  - Inducting over blocks gives $P(1,p,pm^*)$ for $m^*=p^{L_p}-1$, the first gate of level $\ge L_p$.
  - Its block covers $\mathbb Z/p^{L_p}$ by (b) with $j=L_p-1$, so $f(1,p)\ge e_{m^*}+L_p$ by the partial-coverage form, Lemma 1.3(v).
  - Legendre's formula gives $e_{m^*}+L_p=(p^{L_p}-1)+(p^{L_p}-1)/(p-1)=p+\dots+p^{L_p}$.
- (d) Here $a\equiv-k \pmod p$ and $v_p(a+k)=1+v_p(m_0+1)$.
  - If $\tau\le v_p(m_0+1)$, Theorem 3.2(c) applies.
  - Otherwise locality gives $g(a)\ge\min(\tau,v(a+k))=v(a+k)$. So $P(a,p,p(m_0+1))$ holds, and we continue as in (c) up to the first gate $m^*>m_0$ of level $\ge L_p$. This reaches $e_{m^*}+L_p\ge e_{m_0+1}+L_p\ge v_p(a!)+1+L_p$. ∎

Values of $L_p$ [computer-assisted]:
- exact, re-run today (R8): $L_p=1$ for $p=3,5$; $2$ for $7,11,13$; $3$ for $17,19$; $4$ for $23$; $5$ for $29,31$;
- lower bounds: $L_p\ge6$ for $37\le p\le53$ and $L_p\ge5$ for $59\le p\le97$. These rest on the archived logs `archive/C/ecover_big.out` and `ecover_table.out`, which we did not re-run. Both referees re-verified $37\le p\le53$ with their own code, and the computational referee also re-verified $59\le p\le97$ (§9).

**Theorem 3.10 (barrier lemma: shallow information cannot cross deep gates) [proved].** Let $W=[pM_0,pM_1)$ be a run of full blocks whose last block is a gate of level $j$. Normalise by $p^{e_{M_0}}$. The elements $x_n=n!/p^{e_{M_0}}$ have weights $w_n=v(n!)-e_{M_0}\le w_{\max}$, and the demand is $D(W)=w_{\max}+j+1$. Fix $c\ge1$, and let $y_n=p^{w_n}\rho_n$, where $\rho_n\in[1,p^c)$ is the unit part of $x_n$ reduced mod $p^c$, so that $y_n\equiv x_n \pmod{p^{w_n+c}}$.

If $j\ge c+1$, the subset sums of $(y_n)$ do **not** cover $\mathbb Z/p^{D(W)}$.

So any proof that windows cross gates of unbounded level — in particular any proof of Q3 by Tao's lemma — must use unboundedly many $p$-adic digits of the unit parts of factorials (equivalently, of Morita's $\Gamma_p$).

*Proof.* Each block has $p$ elements of one weight, and distinct blocks have distinct weights. So every subset sum is an integer in $[0,X]$ with
$$X\le(p^c-1)\,p\,(p^{w_{\max}+1}-1)/(p-1)<p^{w_{\max}+c+2}/(p-1).$$
- For $p\ge3$ these integers occupy at most about half of the residues mod $p^{w_{\max}+c+2}$.
- For $p=2$, $X<2^{w_{\max}+c+2}-1$, so $-1$ is missed.

Since $D(W)\ge w_{\max}+c+2$, covering mod $p^{D(W)}$ would imply covering mod $p^{w_{\max}+c+2}$. ∎ (Track C.)

### 3.6 An obstruction specific to $p=3$

**Theorem 3.11 (small-twist lemma) [proved].** Let $N=p^Jc$ and $1\le t<p^J$. Then $(N+t)!=N!\,t!\,\kappa(t)$ with $\kappa(t)=\prod_{i\le t}(1+N/i)\in1+p^{J-\lfloor\log_pt\rfloor}\mathbb Z_p$.

For $p=3$ and $v_3(N)\ge4$:
$$A_N \bmod 81=\{\textstyle\sum_{t\le8}e_tt!\} \bmod 81=\mathbb Z/81\setminus\{68,77\}.$$
Hence $E_N$ misses exactly the classes $N!\cdot\{68,77\}$ modulo $3^{v_3(N!)+4}$, and $A_N\ne\mathbb Z_3$ whenever $81\mid N$.

*Proof.*
- $v(N/i)=v(N)-v(i)\ge J-\lfloor\log_pt\rfloor$ for $i\le t$.
- For $p=3$ and $J\ge4$: terms with $t\ge9$ have valuation $\ge v(9!)=4$, because $v(N+i)=v(i)$ for $i<3^J$.
- For $t\le8$ we have $v(t!)+J-\lfloor\log_3t\rfloor\ge4$, so $t!\kappa(t)\equiv t! \pmod{81}$.
- The enumeration of the $2^9$ sums mod 81 is re-run in `indep_checks.py`. ∎ (Track F. Track B found the same two missing residues; track D found the equivalent "node-level" failure at $N\equiv0 \pmod{81}$, carries $\equiv4,13 \pmod{81}$.)

Tracks A and F show computationally that full tails at $p=3$ can only occur at $N\equiv27,54 \pmod{81}$.

### 3.7 First-failure dichotomy and the Theorem-A reduction

**Definition.** For $1\le H\le p^t$ let $c=v_p((H-1)!)$. Say $\mathrm{Cov}(p,t,H)$ holds if, for every unit $K' \bmod p^c$, the subset sums of
$$y_i(K')=\prod_{s=1}^{i}\big(p^tK'-(H-s)\big),\qquad 0\le i<H,$$
cover $\mathbb Z/p^{t+c}$.

**Theorem 3.12 [proved; Lean for the logic].** (Track B.) This formalises the programme in Tao's comment (§2): a fixed finite computation at each depth $t$, independent of the position.
- (a) Suppose $N^*=p^tK''$ with $p\nmid K''$ and $N^*-H>a$. Then:
  - $v_p(N^*!)-v_p((N^*-H)!)=t+c$;
  - the normalised block $\{n!/p^{v((N^*-H)!)}:N^*-H\le n<N^*\}$ equals $U\cdot\{y_i(K'')\}$ with $U$ a unit;
  - $y_i(K'') \bmod p^{t+c}$ depends only on $K'' \bmod p^c$.

  Hence $\mathrm{Cov}(p,t,H)$ implies $P(a,p,N^*-H)\Rightarrow P(a,p,N^*)$.
- (b) Suppose $\mathrm{Cov}(p,t,H_t)$ holds for $t=1,\dots,T$, and let $H^*=\max H_t$. Then for every $a$ the first failure $N^*(a)$ satisfies $N^*\le a+H^*$ or $p^{T+1}\mid N^*$.

  Hence, for every $a<p^{T+1}-H^*$, either $f(a,p)<v_p((a+H^*)!)$ or $f(a,p)\ge v_p((p^{T+1}-1)!)$. A finite dynamic programme decides which.
- (c) *(Uniform covering implies infinity.)* Suppose $\mathrm{UC}(p)$ holds: for every $t\ge1$ there is $H_t$ with $H_t+1<p^t$ and $\mathrm{Cov}(p,t,H_t)$. Then, for every $a$, either $f(a,p)=\infty$ or the first failure satisfies $N^*\le a+H_{v_p(N^*)}$. Moreover $f(1,p)=\infty$, so Q3 holds.

*Proof.*
- (a) For $0<x<p^t$ we have $v(N^*-x)=v(x)$, which gives the jump. Next, $n!/(N^*-H)!=\prod_{s\le i}(N^*-H+s)$.
  - Expand $\prod_s(X-(H-s))$ as an integer polynomial in $X=p^tK''$.
  - Modulo $p^{t+c}$, the term $X^k$ depends on $K'' \bmod p^{t+c-tk}$, and $p^{t+c-tk}\mid p^c$.
  - Then apply Lemma 1.3(iii).
- (b) Use Lemma 1.3(iv) at non-multiples of $p$, and (a) at depths $1\le t\le T$.
- (c) The first statement is (a) applied at the depth $t=v_p(N^*)$. For $a=1$: a first failure $N^*$ with $t=v_p(N^*)\ge1$ has $N^*\ge p^t>1+H_t$, so $N^*-H_t>1=a$, and (a) gives $P(1,p,N^*)$, a contradiction. No base case is needed.

  (Consistency with Theorem 3.6: the infinitely many finite $a$ in each class fail within $H_t$ of $a$.) ∎

(Lean: `E404.block_lift`, `E404.first_failure`, `E404.all_below` in `E404Block.lean`. Only the abstract lifting logic is formalised; the class reduction in (a) is a paper proof.)

**Proposition 3.13 (tail fullness; Fourier criterion; purity) [proved].** Track F.
- (a) Lemma 1.4 (one full tail $E_N=p^{v(N!)}\mathbb Z_p$ plus one finite check $P(a,p,N)$ gives $f(a,p)=\infty$).
- (b) *Relaxed gate criterion.* Let disjoint windows carry independent probability measures on their subsets, and let $\nu$ be the law of the normalised sum. If $\sum_{0\ne\xi\in p^{-K}\mathbb Z_p/\mathbb Z_p}|\hat\nu(\xi)|<1$, then every class mod $p^{v(N!)+K}$ is a finite subset sum, by Fourier inversion. The fraction of classes missed is $\le\sum_{\xi\ne0}|\hat\nu(\xi)|^2$, by Parseval. Tao's lemma is the case where each $\hat\nu$ vanishes on its band.
- (c) For i.i.d. fair coins $\varepsilon_n$, the law $\mu$ of $X=\sum_{n\ge N}\varepsilon_nn!$ has support $E_N$, is atomless, and is of pure type: either absolutely continuous or singular with respect to Haar measure $\lambda$ on $\mathbb Z_p$. This is a $p$-adic Jessen–Wintner law.

*Proof of (c).* Write $\mathbb P$ for the product measure on $\Omega=\{0,1\}^{[N,\infty)}$. The map $\varepsilon\mapsto X(\varepsilon)$ is continuous, because $v_p(n!)\to\infty$.
- *Support.* $\mathbb P$ charges every cylinder, and $X$ is continuous, so the support of $\mu$ is the closure of $X(\Omega)$. This is $E_N$, which is compact.
- *Atomless.* Suppose $\mu(\{x\})>0$, and let $A=\{X=x\}$. By Lévy's 0–1 law, $\mathbb P(A\mid\mathcal F_m)\to\mathbf 1_A$ almost surely, where $\mathcal F_m$ is generated by the coordinates below $m$. So some cylinder $C$ fixing the coordinates in $[N,m)$ has $\mathbb P(A\cap C)>\tfrac12\mathbb P(C)$. Fix $n\ge m$ and let $\tau$ flip coordinate $n$. Then $\tau$ preserves $\mathbb P$ and maps $C$ onto $C$, so $A\cap C$ and $\tau(A\cap C)$ both have measure more than half of $\mathbb P(C)$ and therefore meet. This gives $\varepsilon\in A$ with $\tau\varepsilon\in A$. Then $x=X(\tau\varepsilon)=X(\varepsilon)\pm n!=x\pm n!$, which is impossible because $n!\ne0$.
- *Pure type.* Let $\Gamma\subset\mathbb Z_p$ be the countable group generated by $\{n!:n\ge N\}$. If two sequences differ in finitely many coordinates, their values of $X$ differ by an element of $\Gamma$. So for every $\Gamma$-invariant Borel set $S$, the event $\{X\in S\}$ does not depend on any finite set of coordinates; it is a tail event, and by Kolmogorov's 0–1 law $\mu(S)\in\{0,1\}$. Now suppose $\mu$ is not absolutely continuous. Then $\mu(S_0)>0$ for some Borel set $S_0$ with $\lambda(S_0)=0$. The set $S=\Gamma+S_0$ is a countable union of translates of $S_0$, so it is Borel, $\Gamma$-invariant and $\lambda$-null. Since $\mu(S)\ge\mu(S_0)>0$, we get $\mu(S)=1$, so $\mu$ is singular. ∎

**Proposition 3.14 (unit parts) [proved].** Track A. Let $U(n)=n!/p^{v(n!)}$ and $P(n)=\prod_{j\le n,p\nmid j}j=(-1)^{n+1}\Gamma_p(n+1)$. Then:
- $U(n)=P(n)\,U(\lfloor n/p\rfloor)$.
- $P(n+p^k)\equiv\varepsilon P(n) \pmod{p^k}$, with $\varepsilon=-1$ for $p$ odd or $p^k=4$, and $+1$ for $p=2$, $k\ge3$ (Gauss's generalised Wilson theorem). The exact period of $P \bmod p^k$ is $2p^k$ for odd $p$.
- $U \bmod p^k$ is $p$-automatic.
- $U \bmod p^k$ is **not** determined by finitely many digits: $U(p^j)\equiv(-1)^j \pmod p$ for odd $p$.

These facts are the "structured" side of the barrier lemma: deep gates see the full Morita $\Gamma_p$, which is automatic but not locally constant in the digits.

---

## 4. Computations

All computations are exact integer or residue computations; no floating point is used except in the heuristic Fourier diagnostics of §5. Programs are in `code/`. §7 lists the re-runs performed on 2026-10-08 with their outputs.

### 4.1 Known values, re-verified

An independent residue-set oracle (`code/indep/indep_checks.py`, written for this note) confirms that exponent $K$ is reachable and $K+1$ is not for each value below.
- $f(1,2)=0$, $f(2,2)=254$, $f(3,2)=1$, $f(4,2)=6$, $f(5,2)=3$, $f(6,2)=133$, $f(14,2)=1533$.
- $f(3,3)=3$, $f(39,3)=25$, $f(700,3)=363$.
- $f(110,5)=30$, $f(236,5)=61$.
- $f(42,7)=7$, $f(4,7)=f(6,7)=0$.
- $f(113,11)=11$, $f(163,13)=13$.
- $g_2(0)=254$.

A separate multi-limb C program (track D, `sumform_big.c`; re-run today) confirms $f(34,2)=18444$ in both directions (18444 reachable, 18445 not), as well as $f(38,2)=828$ and $f(14,2)=1533$. This independently confirms Kitamura's deepest row.

Further exact values from track D: $g_2(16)=533$ and $g_2(254)=648$. The values $g_2(2^k)$ for $k=3,\dots,13$ are $6,533,6,198,14,204,13,13,14,93,14$.

By Corollary 3.7.1(i), each exact value gives an infinite class. For example:
- $f(a,2)=v_2(a!)+254$ for all $a\equiv0 \pmod{2^{254}}$;
- $f(a,2)=v_2(a!)+18412$ for all $a\equiv34 \pmod{2^{18412}}$.

### 4.2 Certified uniform covering and the bounds of Theorem A [computer-assisted]

Track B certified $\mathrm{Cov}(p,t,H)$ exhaustively over all classes $K' \bmod p^c$ for the pairs below. Each pair was checked by `cov.c` and again by an independent checker (`cov_check.py`, or `cov_check2.c` for the two largest).

| $p$ | certified $(t,H)$ | $T$ | $H^*$ |
|---|---|---|---|
| 5 | (1,3) (2,10) (3,20) (4,25) | 4 | 25 |
| 7 | (1,4) (2,7) (3,19) (4,26) (5,28) (6,35) | 6 | 35 |
| 11 | (1,5) (2,10) (3,18) (4,22) (5,30) (6,33) | 6 | 33 |
| 13 | (1,6) (2,10) (3,19) (4,24) (5,32) (6,35) (7,39) | 7 | 39 |

All 23 positive certificates were **re-run today** with `cov.c`, and $(7,6,35)$ and $(13,7,39)$ were re-run with `cov_check2.c`; all hold. The independent oracle also re-checked $(5,2,10)$, $(5,3,20)$, $(7,3,19)$, $(11,3,18)$ and $(13,3,19)$ at actual factorial positions over all classes, and $(5,4,25)$ over 120 of its 500 classes.

**Consequences** (Theorem 3.12(b)). Every certified $H_t$ satisfies $H_t+1<p^t$, so the argument of Theorem 3.12(c) excludes a first failure at any depth $t\le T$ for $a=1$, with no base case needed. This gives
$$f(1,13)\ge v_{13}((13^8-1)!)=67\,977\,552 .$$
In addition, for $p\in\{5,7,11,13\}$ and $a<p^{T+1}-H^*$, either $f(a,p)<v_p((a+H^*)!)$ or $f(a,p)\ge v_p((p^{T+1}-1)!)$. The landscapes of §4.6 decide which alternative holds for each $a\le1000$.

**Depth-7 positions for $p=7$ and $p=11$ (found during refereeing; re-checked here).** Theorem 3.12(a) applies at a single position $N^*=p^tK''$ as well as uniformly in $K''$. For a first failure of depth $7$ below $p^8$ there are only $p-1$ positions, $N^*=p^7K''$ with $1\le K''\le p-1$. The computational referee (§9) checked them with blocks of length $H=40$, and we re-checked them with a separate program (`code/B/src/cov_pos.c`, which shares no code with the referee's checker):
- $p=11$, $t=7$, $H=40$, $c=v_{11}(39!)=3$: for each $K''=1,\dots,10$ the block covers $\mathbb Z/11^{10}$ (log `pub_covpos_p11_t7_H40.log`). For comparison, $H=39$ leaves $1\,389\,738$ residues uncovered at $K''=1$; both programs report this same number.
- $p=7$, $t=7$, $H=40$, $c=v_7(39!)=5$: for each $K''=1,\dots,6$ the block covers $\mathbb Z/7^{12}$ (log `pub_covpos_p7_t7_H40.log`).

Combined with the certificates for $t\le6$, this excludes every first failure below $p^8$ for $a=1$, and for every $a\le1000$ that has no first failure within $H^*$ of $a$. Hence
$$f(1,11)\ge v_{11}((11^8-1)!)=21\,435\,880,\qquad f(a,7)\ge v_7((7^8-1)!)=960\,792\ \text{ for } a=2,3,5.$$
The first bound improves the previous $f(1,11)\ge v_{11}((11^7-1)!)=1\,948\,710$ by a factor of about $11$. For $a=1$ at $p=7$ the explicit witness of §4.3 is stronger ($10^6$).

Combined with the landscapes of §4.6:

> every $a\le1000$ satisfies
> - either $f(a,13)-v_{13}(a!)\in\{0,1\}$ (an exact value) or $f(a,13)\ge67\,977\,552$;
> - either $f(a,11)-v_{11}(a!)\in\{0,1\}$ (exact) or $f(a,11)\ge21\,435\,880$;
> - either $f(a,7)-v_7(a!)\le3$ (exact) or $f(a,7)\ge960\,792$.

*Status.* The $\mathrm{Cov}$ certificates were re-run today (R6), and the depth-7 checks were done by two programs (R19). The landscapes of §4.6 were **not** re-run by us; they rest on archived logs (`archive/B/landscape_p*.csv`), and the computational referee reproduced them with an independent dynamic programme (§9).

> **[Round 2]** All bounds of this subsection are superseded by §10.2. There, two new programs certify, for example:
> - $\mathrm{Cov}(13,7,39)$ again, over all 156 classes;
> - the 12 depth-8 positions $13^8K''$ with $H=47$, giving $f(1,13)\ge883\,708\,272$;
> - all 110 depth-7 positions below $11^9$ and the 10 depth-8 positions, giving $f(1,11)\ge235\,794\,760$.
>
> They also show that $\mathrm{Cov}(11,7,40)$ is **false** (class $K'\equiv37$), and that the minimal $H_6$ at $p=7$ is $34$, not $35$.

*Negative certificates.* At these depths no $H$ in the stated range works. For each $H$, one explicit failing class $K'$ refutes $\mathrm{Cov}(p,t,H)$.
- $p=3$, $t=2$, $H\le9$: the class $N^*\equiv9 \pmod{81}$ fails. This is the same $\{68,77\}$ obstruction as Theorem 3.11. (Re-run, R7.)
- $p=3$, $t=3$: every $H\le27$ fails. (Re-run, R7.)
- $p=5$, $t=5$: every $H\le38$ fails (R20).
  - For $H\le34$ and $H=36,37$, the class $K'=1$ fails.
  - For $H=35$ and $H=38$, the class $K'=1$ is covered, but $K'=21001$ (among others) is not: $4$ residues mod $5^{12}$, respectively $8$ residues mod $5^{13}$, are missed.
  - Our `cov_pos.c` and the referee's `rcover.c` report identical numbers of missed residues for $H=31,\dots,38$.
  - A sample of 391 of the 312,500 classes for $H=39$ found no failure. That is not a certificate; the full check for $H=39$ needs about 24 core-hours.
- $p=2$, $t=2$: every $H\le4$ fails. This is a special case of Theorem 3.8.

These failures are realised: $f(949,3)=488$ with first failure $N^*=981\equiv9 \pmod{81}$, and $f(700,3)=363$ with $N^*=729$.

### 4.3 Explicit witnesses [computer-assisted]

Each witness is a strictly increasing list starting at $1$ whose factorial sum is $\equiv0 \pmod{p^K}$. All are checked by verifiers that share no code with the builders. The three largest were also checked by the computational referee's own verifier (§9). The column "exact $v_p$" gives the exact valuation of the witness sum where it was determined.

| bound | terms | max element | exact $v_p$ of the sum | builder / verifier | re-run today |
|---|---|---|---|---|---|
| $f(1,3)\ge2\,000\,001$ | 1 625 856 | 4 000 017 | $2\,000\,001$ | B `search.c` / `verify_bin.c` | archived witness re-verified at $K=2\,000\,000$ (R5), $2\,000\,001$ (holds) and $2\,000\,002$ (fails) (R21) |
| $f(1,5)\ge1\,000\,000$ | 1 414 615 | 4 000 002 | $1\,000\,000$ | B | **regenerated from scratch and verified**; fails at $K+1$ |
| $f(1,7)\ge1\,000\,000$ | 1 630 651 | 6 000 023 | $1\,000\,000$ (referee) | B | archived witness re-verified |
| $f(1,11)\ge177\,152$ | 372 930 | 1 771 555 | $177\,152$ | C `build_witness4.py` / `verify_witness.py` | re-verified |
| $f(1,13)\ge30\,938$ | 64 043 | 371 289 | | C | re-verified by the independent oracle |
| $f(1,13)\ge20\,000$ | 41 421 | 240 006 | | B | re-verified by the independent oracle |
| $f(1,17)\ge5\,219$ | 13 972 | 83 517 | | C | re-verified by the independent oracle |

The $f(1,3)$ witness was built for $K=2\,000\,000$; its sum happens to be divisible by one more power of $3$. The computational referee noticed this, and our `verify_bin` confirms it. The witnesses for $p=3,5,7$ ship gzipped in `archive/witnesses/` (the $p=5$ one is the file regenerated today by R4).

The bounds $f(1,11)\ge21\,435\,880$ and $f(1,13)\ge67\,977\,552$ of §4.2 are much larger than the witnesses for those primes, but they come from coverage certificates; no explicit witness list of that length was built.

Prior published witnesses: $20000$ for $p=3,5,7$ and $5000$ for $p=11,13$ (Kitamura). The builder `search.c` never needed to backtrack. The maximum search effort grows by about $2$–$5\times$ per unit of gate depth.

### 4.4 Lower bounds from Theorem 3.9 and two-block windows [computer-assisted]

*Two-block windows (track C).* At a gate with $m+1=p^jt$, the window $[p(m-1),p(m+1))$ has demand $j+2$, and its data mod $p^{j+2}$ depends only on $(j,t \bmod p)$. Certifying the $p-1$ classes therefore crosses **every** level-$j$ gate.

Certified window levels:
- $p=11,13$: $j=2,3$;
- $p=17,19$: $j=3,4,5$;
- $p=23$: $j=4,5$;
- $p=29,31$: $j=5$.

The levels for $p=17$–$31$ were re-run today with `win2_fast`, every class FULL (R9 in §7.2). The levels for $p=11,13$ rest on archived logs (`archive/C/`). Both referees re-checked windows with their own code: the logic referee for $p=11,13$ ($j=2,3$) and $p=17,19$ ($j=3,4$), and the computational referee for every level listed above.

The table combines Theorem 3.9(c) (with the start $\{1,p-1\}$) with the certified windows, and with the partial-coverage Lemma 1.3(v) at the first gate that is not crossed. For $37\le p\le97$ no windows are used: the bound is $p+\dots+p^{L}$ from Theorem 3.9(c) with the certified lower bound $L\le L_p$.

| $p$ | $L_p$ | method | $f(1,p)\ge$ |
|---|---|---|---|
| 17 | 3 | windows $j=3,4,5$ + Thm 3.9(c) | 25 646 163 |
| 19 | 3 | windows $j=3,4,5$ + Thm 3.9(c) | 49 659 537 |
| 23 | 4 | windows $j=4,5$ + Thm 3.9(c) | 154 764 790 |
| 29 | 5 | window $j=5$ + Thm 3.9(c) | 616 067 009 |
| 31 | 5 | window $j=5$ + Thm 3.9(c) | 917 087 135 |
| 37, 41, 43, 47, 53 | $\ge6$ | Thm 3.9(c) only | $p+\dots+p^6$ (e.g. $2.64\cdot10^9$ for 37, $2.26\cdot10^{10}$ for 53) |
| $59\le p\le97$ | $\ge5$ | Thm 3.9(c) only | $p+\dots+p^5$ |

The values $L_p\ge6$ ($37\le p\le53$) and $L_p\ge5$ ($59\le p\le97$) come from archived logs, not today's re-runs, and were re-verified independently by the referees (§3.5, §9).

The windows fail at $p=11$, $j=4$ (all $t$ partial) and at $p=17,19$, $j=6$.

> **[Round 2]** The rows $p=17,19,23$ are superseded by the covering certificates of §10.2: $f(1,17)\ge7\,411\,742\,272$, $f(1,19)\ge943\,531\,272$ and $f(1,23)\ge3\,559\,590\,232$. The rows $p\ge29$ are unchanged.

### 4.5 Tail-coverage frontiers [computer-assisted]

Track F's driver pushes a frontier $R$ such that every class of $p^{v(N_0!)}\mathbb Z/p^{v(R!)}$ is a sum of distinct $n!$, $N_0\le n<R$. Each new gate $G$ is crossed by an exactly checked window $[A,G)$ with $A\le R$. Windows ending at $v_p(G)=1$ are covered by Cauchy–Davenport.

| $p$, $N_0$ | frontier depth | consequence |
|---|---|---|
| 5, 5 | $5^{117499}$ (crossing $5^7c$, $c\le6$, and $5^8$) | $f(a,5)\ge117\,499$ for $a\in\{1,3\}$ |
| 7, 7 | $7^{283331}$ (crossing $7^7$, $2\cdot7^7$) | $f(a,7)\ge283\,331$ for $a\in\{1,2,3,5\}$; superseded by §4.2 ($\ge960\,792$) |
| 11, 11 | $11^{14997}$ (**re-run today**) | $f(a,11)\ge14\,997$ for $a\in\{1,\dots,6,9\}$; superseded by §4.2 |
| 13, 13 | $13^{12498}$ (**re-run today**) | $f(a,13)\ge12\,498$ for $a\in\{1,\dots,8,11\}$; superseded by §4.2 |
| 3, 27 | $3^{50}$ | $f(a,3)\ge50$ for 11 small $a$; stalls at $G=108$ |

These are coverage certificates produced by code. Validation:
- the window checkers were validated against brute force on about 25 small windows;
- the p=5 and p=7 runs involved manually launched split checks at the deepest gates, recorded in the archived logs;
- we did not re-run the $p=5$, $p=7$ and $p=3$ frontiers today; their logs are in `archive/F/`.

*Status of the rows.* The $p=11$ and $p=13$ rows were re-run today. They are now superseded by §4.2: every $a$ listed there is in the "deep" class of the §4.6 landscapes, so $f(a,11)\ge21\,435\,880$ and $f(a,13)\ge67\,977\,552$ for those $a$. The $p=7$ row is likewise implied and strengthened by the depth-7 checks of §4.2, which two programs confirm. The $p=5$ row (for $a=3$; for $a=1$ the witness of §4.3 is stronger) and the $p=3$ row rest **only** on the archived output of a single implementation. The computational referee could not reproduce them by a different route within its memory limits; it did not refute them either. Treat these two rows as single-implementation results.

### 4.6 Complete small-$a$ landscapes [computer-assisted]

Track B classified every $a\le2000$ for $p=3$ and every $a\le1000$ for $p=5,7,11,13$ into three classes:
- *blocked* ($a\equiv-1$);
- *exact* (exhaustive DP);
- *$g\ge10^4$* (verified witness).

No $a$ is left open. The counts (blocked / exact / $\ge10^4$) are:
- $p=3$: 667 / 600 / 733;
- $p=5$: 200 / 275 / 525;
- $p=7$: 143 / 227 / 630;
- $p=11$: 91 / 206 / 703;
- $p=13$: 77 / 164 / 759.

The maximal exact $g$ values are 18, 5, 3, 1 and 1 respectively. All 3200 of Kitamura's odd-prime rows agree, and the "ignited candidates" there are now proved to have $g\ge10^4$.

*Status.* We did not re-run the landscapes today; the data are in `archive/B/landscape_p*.csv`. The computational referee reproduced them with an independent exact dynamic programme: the same counts for $p=3$ ($a\le2000$, maximal exact $g=18$) and for $p=5,7,11,13$, where at $p=11$ and $p=13$ the $297$ and $241$ values of $a$ with a small exact $g$ are precisely the blocked and exact ones above.

The apparent gap between small and $\ge10^4$ values is a small-$a$ phenomenon. By Proposition 3.4, arbitrarily large finite values occur, starting at larger $a$: for example $g_5=7$ on $a\equiv-17 \pmod{5^8}$.

### 4.7 Exact class census; rigorous densities [computer-assisted]

The quantity $\delta_G(p)=\mu\{g_p\ge G\}$ was computed exactly by lifting classes level by level. Each class is decided exactly, which is valid by Theorem 3.1.

For $p=2$ there are four implementations:
- track E `tree.c`, to $G=29$;
- track D `gclass.c` (BFS), to $28$;
- track D `gdfs.c` (DFS), to $32$ (archived, `archive/D/dfs32_c*.log`; not re-run today);
- the computational referee's `census.c`, to $32$. It tests every child with an exact dynamic programme and does not use the halving lemma.

They agree wherever they overlap. Today's re-runs reproduced $G\le24$ (tree) and $G\le22$ (BFS), and the independent oracle reproduced $G\le14$. The odd-prime trees beyond the levels re-run today (R13) are archived in `archive/E/`; the computational referee reproduced every odd-prime value in the table below.

| $p$ | $\delta_G(p)$ |
|---|---|
| 2 | $G=4$: .3750, 8: .2422, 12: .1958, 16: .1517, 20: .1417, 24: .1292, 28: .1164, 29: .1134, 32: .1016 |
| 3 | $G=1$: .6667, 4: .4568, 8: .3937, 12: .3704, 14: .3663, 17: .36329 |
| 5 | $G=1$: .6, 4: .5392, 7: .5224, 10: .52162 |
| 7 | $G=1$: .7143, 2: .6327, 8: .62394 |
| 11 | 6: .69976 |
| 13 | 5: .75454 |
| 17, 19, 23 | $G=4$: .75692, .77792; $G=3$: .85617 |

**Rigorous corollaries.**
- $f(a,2)\le v_2(a!)+28<\infty$ for a set of $a$ of natural density $1-\delta_{29}(2)=0.886587$. Level 29 was computed by `tree.c`, by `gdfs.c` and by the referee's `census.c` ($60\,888\,286$ surviving classes mod $2^{29}$ in each), and `gclass.c` agrees up to level 28.
- $f(a,2)\le v_2(a!)+31<\infty$ on density $1-\delta_{32}(2)=0.898364$. Level 32 was computed by `gdfs.c` (archived) and reproduced exactly by the referee's `census.c` ($436\,523\,876$ surviving classes mod $2^{32}$).
- *Comparison with prior work.* Kitamura's certified classification of the classes with $g\le24$ already gives $f(a,2)<\infty$ on density $1-\delta_{25}(2)=0.873385$. Our census agrees with Kitamura's count: summing the dying classes through level 25 in `archive/E/tree_p2.txt` gives $2\times87\,320=174\,640$ classes, Kitamura's number. What is new for $p=2$ is the extension from level 25 to level 32.
- $f(a,3)<\infty$ on density $\ge0.6367$.
- For $p=5,7,11,13$ the densities are $\ge0.4784$, $0.3761$, $0.3002$ and $0.2455$. For odd $p$, these are the first rigorous densities beyond the class $a\equiv-1 \pmod p$ (density $1/p$).
- Forbidden values: $g_2\notin\{1,2,4,5\}$ (Corollary 3.7.1), and $g_7(a)\ne2$ for all $a$, since $\delta_2(7)=\delta_3(7)=31/49$.
- **[Round 2]** $\delta_G(2)\to0$, so $\mu(K_2)=0$ (Theorem 10.1). The table's $p=2$ row is therefore a decreasing sequence with limit $0$; Theorem 10.1 gives no rate.

### 4.8 Odd-prime "uniformity" data

For odd $p$ almost every surviving class keeps all $p$ children. For example:
- $p=17$, level 4: 3715 of 3719 parents keep all 17 children;
- $p=3$ is much less uniform: at level 17, 9766 parents have 0 surviving children, 5410 have 1 and 618 have 2.

Kitamura's "ignited" fractions (36.7%, 53.7%, 63.3%, 71%, 76% for $p=3,5,7,11,13$) match $\delta_G(p)$.

---

## 5. Conjectures and heuristics (clearly not proved)

**H1 (criticality) [heuristic].**
- *Tao's count.* There are about $(p-1)k$ factorials with $v_p(n!)<k$, against $p^k$ residues. This is supercritical ($2^{p-1}>p$) for $p\ge3$ and exactly critical for $p=2$.
- *Mean-field count.* Track D's count of valid sums at stage $N$ for $p=2$ is $2^{s_2(N)-s_2(a)-1}$, which is $\le1/2$ at every power of $2$.
- *Branching model.* The carry recursion of §1.4 is a branching process in a random environment. Its quenched mean log-offspring per block is $p\log2-\tfrac{p}{p-1}\log p$: zero at $p=2$ and positive for $p\ge3$. Offspring are correlated, so this is not a proof.
- **[Round 2] Credit.** At $p=2$ the critical-branching picture, and the observation that the surviving fraction decays to $0$, are already in Kitamura's July 2026 repository (§2). Round 1 did not credit this.

**Conjecture 5.1 (Q1 at $p=2$).** $f(a,2)<\infty$ for every $a$, i.e. $K_2\cap\mathbb Z=\{-2\}$. A weaker form is $\mu(K_2)=0$, i.e. $\delta_G(2)\to0$. Kitamura's measured decay of the surviving fraction (§2) is empirical evidence for the weaker form.

> **[Round 2]** The weaker form is now **proved** (Theorem 10.1; AI-refereed, not human-refereed). The strong form remains a conjecture.

*Evidence:*
- exact $\delta_G(2)$ falls steadily, with $\delta_G\sqrt G\in[0.60,0.74]$ for $8\le G\le29$;
- Monte Carlo with $4\cdot10^6$ samples and 256-bit exact arithmetic gives $\delta_{64}=0.0644$, $\delta_{128}=0.0379$ and $\delta_{254}=0.0208$, with local decay exponent rising from 0.58 to 0.88;
- first-moment experiments are consistent with $\mu(K_2)\le0.0103$.

The case $a=594$ (Kitamura's $f(594,2)\ge66126$) remains a live test.

**Conjecture 5.2 (positive measure for odd $p$).** $\mu(K_p)>0$ for every odd $p$. Numerically $\mu(K_3)\approx0.36$ (exact $\delta_{17}=0.36329$, still slowly decreasing; Monte Carlo plateau $0.3586\pm0.0034$ at $G\le38$). The other values are $\mu(K_5)\approx0.5216$, $\mu(K_7)\approx0.6239$, $\mu(K_{11})\approx0.6998$ and $\mu(K_{13})\approx0.7545$.

Even a proof of $\mu(K_p)>0$ would **not** by itself place a natural number in $K_p$: $K_p$ is nowhere dense (Theorem 3.6).

**Conjecture 5.3 ($\mathrm{UC}(p)$, track B).** For $p\ge7$, and possibly $p\ge5$, $\mathrm{Cov}(p,t,H_t)$ holds for every $t$ with some $H_t<p^t-1$. By Theorem 3.12(c) this implies $f(1,p)=\infty$, and hence **Q3 = YES**.

*Evidence:*
- certified for $t\le6$ ($p=7,11$) and $t\le7$ ($p=13$); at $t=7$ also certified at the individual positions $7^7K''$ and $11^7K''$ below $p^8$ (§4.2);
- the minimal $H_t$ grows roughly like $5$–$6t$, close to the counting threshold $H\gtrsim t/(\log_p2-1/(p-1))$;
- coverage switches on sharply once $2^H/p^{t+c}\gtrsim40$.

*Against:*
- subset sums here are far from random (e.g. $p=3$, $t=3$, $H=27$ has counting ratio 84 yet misses 2.5%);
- $\mathrm{UC}$ is false for $p=2$ (Theorem 3.8) and $p=3$ (§4.2);
- at $p=5$, $t=5$ every $H\le38$ fails (§4.2), so $H_5\ge39$ would be needed; whether some larger $H$ works is unresolved.

> **[Round 2] Further evidence (§10.2, §10.5):**
> - certified for $t\le7$ at $p=17$;
> - certified at every position below $p^9$ for $p=7,11,13,17$, and below $p^8$ for $p=19,23$;
> - a counting law (Conjecture 10.24) whose registered predictions were confirmed. Three of these predictions were genuinely out of sample and test its thresholds; see §10.5 for the exact count.
>
> Theorem 10.16 reduces $\mathrm{UC}(p)$, for $p\ge7$, to an explicit random-model Fourier bound. Still unproved.

**Conjecture 5.4 ($\mathrm{ML}_p$, track C).** For some $\lambda=\lambda(p)$, every window of $\lceil\lambda j\rceil$ blocks ending at a level-$j$ gate covers its demand. This is a block-structured form of 5.3.

**Conjecture 5.5 (full tails, track F).** $E_p=p\mathbb Z_p$ for every $p\ge5$. By Lemma 1.4 this would give $f(1,5)=f(3,5)=\infty$, among others.

For $p=3$ the two tracks disagree, and **both questions are open**:
- Track F conjectures $E_{27}=3^{13}\mathbb Z_3$. It is verified to depth $3^{50}$.
- Track A conjectures $A_N\ne\mathbb Z_3$ for every $N$. The density of the depth-14 full set is $0.008$ and falling.

**H2 (Fourier) [heuristic; floating point].** For the uniform product measure from $N_0=p$, the Fourier $L^1$ mass $\sum_{\xi\ne0}|\hat\nu(\xi)|$ over the computed depths is:
- $0.31$ for $p=7$ ($s\le8$), $0.067$ for $p=11$ ($s\le6$) and $0.009$ for $p=13$ ($s\le5$);
- $1.16$ for $p=5$ ($s\le10$, so the plain criterion fails);
- $16.8$ and growing for $p=3$;
- divergent for $p=2$.

So for $p\ge7$, Proposition 3.13(b) with the plain uniform measure *would* prove fullness if the $L^1$ bound persisted at all depths.

> **[Round 2]** These sums are now certified for the shells $k\le7$ ($p=13$) and $k\le8$ ($p=11$) (§10.4.1). Monte Carlo estimates of deep shells are in Conjecture 10.22. Corollary 10.20 explains why supremum-type transfer bounds cannot prove the persistence.

---

## 6. The most promising route to Q3, and exactly what remains

**What a covering-type proof of Q3 must do.** The constraints below are proved in §3, but items 1, 2 and 4 apply only to proofs that go through Tao-type covering of blocks or windows. They do not exclude a proof of a different kind, for example a non-constructive proof that some $f(a,2)=\infty$. That possibility is exactly the negation of Conjecture 5.1, and it remains open.
1. A covering-type proof must work at an odd prime: Tao-type covering is impossible at $p=2$ (Theorem 3.8). For $p=3$, node-level covering fails at every $N\equiv0 \pmod{81}$ (Theorem 3.11), so only a population-level argument could work there.
2. A proof that crosses gates of unbounded level by covering windows must use unboundedly many $p$-adic digits of the unit parts $U(n)$, i.e. of Morita's $\Gamma_p$ (Theorem 3.10). Mod-$p$ additive combinatorics alone (Cauchy–Davenport, Olson, Erdős–Heilbronn) cannot suffice for that.
3. No proof can use a residue-class criterion on $a$ (Theorem 3.6). This item holds for every kind of proof.
4. It must avoid "worst case over all incoming carries plus all higher digits" arguments. Track B shows such arguments give a transfer-operator constant $\ge1$; this is a statement about that proof schema, not a theorem about all proofs.

> **[Round 2]** For the updated list of what remains, see §10.6. Two round-2 results add to the constraints below:
> - Corollary 10.13: fullness information alone cannot carry a single gate block, or a window entered with fullness mod $p^D$ where $e(H-1)!\le p^D\le p^{t-1}$. Whether it can carry a whole gate-to-gate stretch is open.
> - Corollary 10.20: supremum-type Fourier transfer bounds cannot give decay.

**Recommended target: $\mathrm{UC}(13)$** (or $\mathrm{UC}(p)$ for one $p\ge7$, or for all large $p$). By Theorem 3.12(c), Q3 follows from:

> **Missing Lemma (ML).** For every $t\ge8$ there is $H$ with $H+1<13^t$ such that, for every unit $K' \bmod 13^{c}$ ($c=v_{13}((H-1)!)$), the subset sums of $y_i(K')=\prod_{s=1}^{i}(13^tK'-(H-s))$, $0\le i<H$, cover $\mathbb Z/13^{t+c}$.

The corresponding statement is already certified for $t\le7$ (§4.2). So ML would give $f(1,13)=\infty$ by Theorem 3.12(c).

**Structure available for attacking ML.** Expanding in $X=p^tK'$ gives an exact identity in $\mathbb Z[X]$:
$$y_i(K')=\sum_{k=0}^{i}X^k\,(-1)^{i-k}e_{i-k}(H-1,H-2,\dots,H-i)=\sigma_i+X\tau_i+X^2(\cdots),$$
$$\sigma_i=(-1)^i\frac{(H-1)!}{(H-1-i)!},\qquad\tau_i=(-1)^{i-1}e_{i-1}(H-1,\dots,H-i)\in\mathbb Z.$$
This is the reflected form of track C's window expansion
$$(N-1-u)!=(N-1)!\,\frac{(-1)^u}{u!}\sum_kN^kh_k(1,\tfrac12,\dots,\tfrac1u).$$
So ML is a statement about the joint behaviour of the integer vectors $(\sigma_i,\tau_i,\dots)$:
- the leading part $\sigma_i$ does not depend on $K'$, and controls the low digits;
- $K'$ enters only from digit $t$ onwards, through $p^tK'\tau_i$ and the higher terms.

ML asks that, for every unit $K'$, the twisted subset sums $\sum\varepsilon_i(\sigma_i+p^tK'\tau_i+\dots)$ fill all of $\mathbb Z/p^{t+c}$. This is an equidistribution statement, uniform in $K'$, for the subset sums of these vectors.

Proposition 3.13(b) reduces it to an exponential-sum bound
$$\sum_{\xi\ne0}\prod_i|\cos(\pi\xi y_i)|<1,$$
uniformly in $K'$. Numerically this is far from tight for $p=13$ (§5, H2). It must be proved *without* taking a supremum over phases: track B shows the sup-over-phase bound has constant $\ge1$.

**Alternative targets.**
- **(T2)** Prove that one tail is full, e.g. $E_{13}=13\mathbb Z_{13}$ or $E_{11}=11\mathbb Z_{11}$, via a self-similar induction. This must carry multiplicity or Fourier information, because "lead-only" covering information provably cannot propagate (track F; Theorem 3.10).
- **(T3)** A renormalisation lemma (track C): if the carries reachable at a level-$(j-1)$ gate fill a residue class mod $p^j$, then those at a level-$j$ gate fill one mod $p^{j+1}$. By Theorem 3.10 the step must use the first-order term $N\sum_{u\in S}(-1)^uH_u/u!$.
  - **[Round 2]** Apply Theorem 10.12 with $D=j$, $D'=j+1$ and $\delta$ the valuation gained across the stretch. It says that the fullness-only version of T3 holds for a given stretch iff the stretch's subset sums mod $p^{\delta+j+1}$ contain a complete coset of $p^j$. This is **not** decided here for the gate-to-gate stretches that T3 uses. What is proved (Corollary 10.13) is weaker. Fullness alone cannot carry a single level-$j$ gate block once $D_p\le D\le j$, where $D_p=\lceil\log_p(e(p-1)!)\rceil$. Nor can it carry a window of length $H$ entered with fullness mod $p^D$ where $e(H-1)!\le p^D\le p^{t-1}$. So an inductive proof of T3 must either use stretches long enough to avoid these cases, or carry distributional information (Theorem 10.16).
- **(T4, for Q1)** Prove $\mu(K_2)=0$ by a quenched first-moment bound. Heuristic picture (track E): grouping steps in pairs, $\log_2$ of the expected population is a zero-drift walk $\sum(2-d_k)$ with $d_k=v_2(\alpha+2k)$. The missing input is equidistribution of the unit parts of $(\alpha+1)_k \bmod 2^d$ conditional on the valuation pattern, for which the 2-adic Morita/odometer structure is the natural tool. This would give "$f(a,2)<\infty$ for almost all $a$". It would not settle Q3.
  - **[Round 2] Done:** Theorem 10.1 (AI-refereed, not human-refereed). The proof needs no equidistribution input. Conditioning on $x\bmod2^{V_n}$ makes the first moment an exact martingale once paths are weighted by frozen-state weights.

**Computational next steps** (feasible extensions of the supplied code):
- $\mathrm{Cov}(5,5,39)$ and $\mathrm{Cov}(5,5,40)$: $312\,500$ classes of $5^{13}$-bit sets each, about 24 core-hours per $H$ with `cov.c`; every $H\le38$ is already refuted;
- $\mathrm{Cov}(11,7,40)$ over all $1210$ classes $K' \bmod 11^3$ (about 2.5 core-hours and 6.5 GB with `cov.c`). This would give the dichotomy of Theorem 3.12(b) at $p=11$ with $T=7$, for all $a<11^8-40$. **[Round 2: this fails: the class $K'\equiv37$ misses 2 residues (§10.2). Use $H\ge41$.]**;
- three-block windows for $p=17$–$31$;
- the $p=7$ tail frontier (§4.5) through $7^8$;
- explicit witnesses for the frontier bounds;
- re-running the $p=5,7$ frontiers with fully automated logs.

---

## 7. Reproduction

### 7.1 Layout

> **[Round 2]** The paths `code/`, `archive/` and `review/` in §§1–9 refer to the round-1 material, which is unchanged. Round-2 code is under `code/round2/`, and round-2 track logs, re-run outputs and referee outputs are under `data/round2/`; see §10.7.

All code is under `code/`. It was copied from the six working directories of this session, which are listed below. Run `sh code/build.sh` first: it compiles every C program with `clang -O3` (or `$CC`) into the paths the run scripts expect. The Python scripts need Python 3; `numpy` and `sympy` are used only in a few sanity scripts. Lean files compile against a Lean 4 v4.34.1 + Mathlib project (`lake env lean FILE`).

Besides `code/`, the repository contains `archive/` (selected logs from the original track directories, which the "not re-run" items below rest on, and the gzipped witnesses for $p=3,7$) and `review/` (the referees' own programs and outputs, §9).

| dir | origin | key programs |
|---|---|---|
| `code/indep/` | written for this note | `indep_checks.py`: an independent oracle for $g_p$ that re-checks known values, shadows, $\Phi_p$, the $\{68,77\}$ obstruction, the mod-16 obstruction, $L_p\le23$, the gate congruence, halving numerics, class counts, Cov spot checks and witnesses |
| `code/lean/` | A, B, C, D, E, F | 7 Lean files; `run_lean.sh` |
| `code/A/` | A (structure) | `s1`–`s10` scripts, `zdens.c`, `dens2.c`, `gdens.c` |
| `code/B/` | B (computation) | `src/search.c`, `verify_bin.c`, `cov.c`, `cov_check2.c`, `cov_check.py`, `exact_f.py`, `exact_g.c`, `landscape.py`; `run_B_witness.sh`, `run_B_cov.sh`. Added during publication: `src/cov_pos.c` (position-specific coverage) and `src/cov_inputs.py` (input generator for the referee's `rcover.c`) |
| `code/C/` | C (large $p$) | `ecover_fast.c`, `win2_fast.c`, `win2g.c`, `tau.c`, `core.py`, `check_*.py`, `build_witness*.py`, `verify_witness.py`, `witnesses/`; `run_C.sh` |
| `code/D/` | D ($p=2$) | `gclass.c`, `gdfs.c`, `gdfsp.c`, `sumform_big.c`, `halving_check.c`, `gref.py`, `sumdp_check.py`, `gneg.py`, Monte Carlo `gsample*.c` |
| `code/E/` | E (behaviour) | `tree.c`, `frozen.c`, `shadow.py`, `e404lib.py`, `checks_misc.py` |
| `code/F/` | F (coverage) | `frontier.py`, `wincheck.c`, `wincheck2.c`, `cover.c`, `gap.py`, `fourier.c` |
| `code/outputs/` | re-runs of 2026-10-08 | all logs cited in 7.2; files named `pub_*` come from the publication re-checks R19–R21 |

### 7.2 Commands and re-run results (2026-10-08, at most 3 cores)

Unless a `cd` is shown, commands are run from `code/`; the bundled scripts resolve paths relative to their own directories. Outputs are in `code/outputs/`.

| # | what | command | result today | wall time |
|---|---|---|---|---|
| R1 | all Lean files | `sh lean/run_lean.sh /path/to/formal` | 7/7 files compile (exit 0); every `#print axioms` shows only `propext, Classical.choice, Quot.sound`; no `sorry` / `native_decide` (`lean.log`) | 1.3 min |
| R2 | independent oracle | `python3 -I indep/indep_checks.py C/witnesses/w3_p13_J3.txt 13 30938 C/witnesses/w_p17_L3.txt 17 5219 B/data/t13_20000.txt 13 20000` | `ALL_OK=True` (`indep_checks.out`) | 14 s |
| R3 | extra spot checks | `python3 -I indep/extra_checks.py` | all OK: $f(949,3)=488$, $g_5(5^8-17)=7$, $g_2(2^{16}-14)=15$, $3k\le\gamma_p(p^k+2)$, $g_7\ne2$, $g_2(0)=254$ (`indep_extra_checks.out`) | 1 min |
| R4 | $f(1,5)\ge10^6$ witness, regenerated | `sh B/run_B_witness.sh DIR` (DIR = directory of the unzipped archived witnesses, or `none`) (binaries from `sh build.sh`; `search5` is `src/search.c` compiled with `-DPP=5`) | rebuilt in 4.3 min: 1 414 615 terms, max 4 000 002; `verify_bin`: VERIFIED mod $5^{10^6}$, FAILED mod $5^{10^6+1}$ (`B_search5_1e6.log`, `B_verify5_*.log`) | 11 min |
| R5 | archived witnesses $f(1,3)\ge2\cdot10^6$, $f(1,7)\ge10^6$ | (same script) | both VERIFIED (`B_verify3_2e6.log`, `B_verify7_1e6.log`) | 11 min |
| R6 | Theorem A certificates | `sh B/run_B_cov.sh` | 23/23 `Cov HOLDS` with `cov.c` ($(13,7,39)$: 156 classes, 380 s); `cov_check2.c` exhaustive: $(7,6,35)$ 2058/2058 classes covered, $(13,7,39)$ 156/156 classes covered (`B_cov.log`) | 35 min |
| R7 | negative coverage scans | `B/bin/cov 3 2 2 9 34 0; B/bin/cov 3 3 3 27 34 0; B/bin/cov 2 2 1 4 34 0` | every $H$ fails, either by the counting bound $2^H<p^M$ or by computation (`B_cov_negative_scan.log`) | 40 s |
| R8 | $L_p$ table | `for p in 3 5 7 11 13 17 19 23 29 31; do C/bin/ecover_fast $p 6 4000000000; done` | $L_p$ exactly as stated in §3.5 for $p\le31$ (`C_ecover.out`) | 1 min |
| R9 | two-block windows | `C/bin/win2_fast p j t` for all $t=1..p-1$ | $p=17$, $j=3,4,5$: 48/48 FULL; $p=19$, $j=3,4,5$: 54/54; $p=23$, $j=4,5$: 44/44; $p=29$, $j=5$: 28/28; $p=31$, $j=5$: 30/30 (`C_win2_p*.out`) | 10 min |
| R10 | track C structure checks | `cd C; python3 check_structure.py; python3 check_window_e.py; python3 check_hk_expansion.py; python3 check_finiteness_general.py` | grouping identity and gate lemma (35 963 cases) True; window expansion 1364/0 failures; $h_k$ expansion 2832/0; Theorem F: 0 consistency violations, 43 DP checks 0 mismatches | 3 s |
| R11 | $f(1,11)\ge177152$ witness | `cd C; python3 verify_witness.py 11 177152 witnesses/w4_p11_J4.txt` | exact $v_{11}$ of the sum $=177152$ | 3 min |
| R12 | tail frontiers | `python3 F/frontier.py 11 11 150000 22 7 200 LOG` and `... 13 13 150000 26 7 220 LOG` | $E_{11}$ covers $11\mathbb Z/11^{14997}$; $E_{13}$ covers $13\mathbb Z/13^{12498}$ (`F_frontier_p1*.log`) | 10 s |
| R13 | class trees | `E/tree 2 24 1 PREFIX`, `E/tree 3 12 1 …`, `E/tree 5 7 1 …`, `E/tree 7 6 1 …` | survivor counts identical to the archived runs (e.g. $p=2$: 2 167 108 at $G=24$) | 6 s |
| R14 | independent BFS census, $p=2$ | `D/gclass 22 40` | identical counts to R13 and to the archived DFS | 1.5 s |
| R15 | halving lemma numerics | `D/halving_check 16` | 917 506 tests, 0 violations | <1 s |
| R16 | deep exact $p=2$ values | `D/sumform_big a K` for $(a,K)$ = (2,254/255), (14,1533/1534), (38,828/829), (34,18444/18445) | reachable / not reachable exactly as stated | ~1 min |
| R17 | $\gamma_p(m)$, $\Phi_p$, Hensel construction | `cd E; python3 shadow.py 16; python3 checks_misc.py` (after `E/frozen 30000 > data/frozen_upto30000.txt`); `cd D; python3 gneg.py` | tables reproduced; 20 704 frozen-class lower-bound checks and 161 Hensel constructions, 0 failures; maximal multiplicity of $-2$ is 3, at $B=\{1,3\}$ | 40 s |
| R18 | track A cross-checks | `cd A; clang -O3 -o zdens zdens.c; clang -O3 -o gdens gdens.c; python3 s7_crosscheck.py; python3 s8_near_minus1.py` | ALL OK; near-$(-1)$ formula 72/72 agree | <1 s |

Publication re-checks (2026-10-08, after the referee reports; commands run from `code/` after `sh build.sh`):

| # | what | command | result | wall time |
|---|---|---|---|---|
| R19 | depth-7 positions (§4.2) | `B/bin/cov_pos 11 7 40 1 2 3 4 5 6 7 8 9 10`; `B/bin/cov_pos 7 7 40 1 2 3 4 5 6`; for comparison `B/bin/cov_pos 11 7 39 1` and `B/bin/cov_pos 7 7 39 1 2` | all 10 positions at $p=11$ and all 6 at $p=7$ COVERED. $H=39$ misses $1\,389\,738$ residues at $p=11$, $K''=1$, the same count as the referee's checker. The referee's `rcover.c`, fed by `B/src/cov_inputs.py`, also gives full coverage at $p=7$ (`pub_covpos_*.log`, `pub_rcover_p7_t7_H40.log`) | 1.5 min; 6.5 GB RAM at $p=11$ |
| R20 | $\mathrm{Cov}(5,5,H)$ fails for $H\le38$ | `B/bin/cov_pos 5 5 H 1 2 3 4` for each $H\le38$, plus the classes $21001,\dots$ for $H=35,38$; `B/bin/cov 5 5 35 35 34 1 1000 1` and `B/bin/cov 5 5 38 39 34 0 1000 1` (samples of the classes $K'\equiv1 \pmod{1000}$) | a failing class for every $H\le38$. Samples: $5/79$ classes fail at $H=35$, $21/391$ at $H=38$, $0/391$ at $H=39$ (`pub_cov_p5_t5_*.log`) | 4 min |
| R21 | exact valuation of the $f(1,3)$ witness | `B/bin/verify_bin 3 1 K archive/witnesses/f1_3_K2000000.txt` (after `gunzip`) for $K=2\,000\,001$ and $2\,000\,002$ | VERIFIED at $2\,000\,001$, FAILED at $2\,000\,002$ (`pub_verify3_*.log`) | 10 min |

The scripts `code/run_DEFA.sh` (R12–R18), `code/C/run_C.sh` (R8–R11), `code/B/run_B_*.sh` (R4–R6) and `code/lean/run_lean.sh` (R1) bundle these commands. They expect the binaries built by `code/build.sh`; `run_B_witness.sh` expects the witnesses for $p=3,7$ in a directory given as its argument (unzip them from `archive/witnesses/`).

### 7.3 What was *not* re-run today

The following rest on archived logs from the same session. The relevant logs are copied into `archive/`. The last column says whether a referee reproduced the item with independent code (§9).

| item | archived log | independently reproduced? |
|---|---|---|
| $p=2$ census beyond $G=24$ ($G\le29$ by `tree.c`; $G\le32$ by `gdfs.c`) | `archive/E/tree_p2.txt`, `archive/D/dfs32_c*.log`, `archive/D/run_gclass29.log` | yes, to $G=32$ (computational referee, `review/computation/census_p2_32.out`) |
| class trees for $p=3$ ($G=13$–$17$), $5$ ($G=8$–$10$), $7$ ($G=7,8$), and $11$–$23$ | `archive/E/tree_*.txt` | yes, at every level quoted in §4.7 |
| $L_p\ge6$ for $37\le p\le53$ and $L_p\ge5$ for $59\le p\le97$ | `archive/C/ecover_big.out`, `archive/C/ecover_table.out` | yes (logic referee for $37$–$53$; computational referee for $37$–$97$) |
| two-block windows for $p=11,13$, and the failing levels | `archive/C/win2*.out` | yes, except the failing level $p=19$, $j=6$ |
| landscapes of §4.6 | `archive/B/landscape_p*.{csv,log}` | yes (counts and maximal exact values) |
| $p=5$ ($a=3$) and $p=3$ tail frontiers (§4.5) | `archive/F/frontier_p5_*`, `archive/F/frontier_p3_*` | **no** (single implementation) |
| $p=7$ tail frontier (§4.5) | `archive/F/frontier_p7_*` | superseded by §4.2 |
| Monte Carlo runs of §5 (heuristic only) | `archive/D/mc*.txt` | no |

All are reproducible with the supplied code. The commands are in the headers of the archived logs and in the track scripts.

---

## 8. AI-assistance disclosure and acknowledgements

This note was composed by **Nathan Durfee**, who set the problem, prompted and directed the work, and is the human point of contact. **Nathan Durfee has not personally verified the mathematics.**

The mathematical content, proofs, programs, computations and text were generated by **Claude (Anthropic), model Claude Opus 5.5**, running as a multi-agent workflow in Claude Code. The workflow had four stages:
- two literature and community "gate" agents;
- six parallel research tracks: A structure, B computation, C large $p$, D $p=2$, E behaviour, F literature and coverage;
- a lead-author agent that cross-checked the tracks, wrote an independent verification oracle, re-ran the computations and wrote the first version of this note;
- three separate referee agents (logic, computation, novelty), whose reports are summarised in §9, followed by a revision that applied every correction they asked for and re-checked the new computations (R19–R21).

Machine checks are limited to what §3 and §7 state. The Lean files check specific lemmas, not the full chain of reasoning. The referees are AI instances too. **No part of this note has been reviewed by a human referee.** Readers should treat every claim as unrefereed and check what they intend to rely on. Corrections are welcome.

**[Round 2]** Revision 2 (§10) came from a second session on 2026-10-11/12, again run with Claude Opus 5.5 in Claude Code and prompted by the author:
- a status check by the workflow lead;
- five parallel tracks (R1a, R1b, R2a, R2b, R3);
- a lead-author instance that checked the proofs, re-ran the computations (§10.7) and wrote §10;
- three separate referee agents (logic, computation, novelty), each writing its own code, followed by a revision that applied their corrections (§10.8).

Throughout §10, "the lead" and "the lead author" mean this lead-author AI instance, not the human author. The proof of Theorem 10.1 has been checked line by line by the lead-author instance and by the round-2 logic referee. Both are AI systems of the same kind that produced the proof. Before anyone relies on it, it should be checked independently, ideally by a human.

We thank the contributors whose public work this builds on: S. Lin, V. Kovač, T. Tao, K. Kitamura, T. Bloom (erdosproblems.com), AItoBit (formal-conjectures PR #6936 and the llm-hunter write-ups), and the authors of the earlier AI write-ups cited in §2.

---

## 9. Verification

After the first version of this note was written, three Claude instances refereed it independently, each through a different lens. Each wrote its own code, sharing none with `code/`. Their programs and outputs are in `review/`.

**Logic referee.** It checked every proof in §§1–3 line by line, re-ran all seven Lean files (all compile; only the axioms `propext`, `Classical.choice` and `Quot.sound`), and reproduced many of the numbers from scratch: the $\gamma_p$ and $\Phi_p$ tables, the $\{68,77\}$ obstruction, the $p=2$ class counts, the densities for small $G$, the exact $L_p$ for $p\le31$, $L_p\ge6$ for $37\le p\le53$, several $\mathrm{Cov}$ certificates and windows, and the gap theorem on small $a$. It found **no fatal or serious error**. Its minor findings, all now fixed:
- §6 said that *any* proof of Q3 must work at an odd prime and must use unboundedly many digits. §3 proves this only for covering-type proofs; the wording is now restricted (§6).
- The summary attributed $f(1,53)\ge2.26\cdot10^{10}$ (and $37\le p\le53$) to two-block windows; it comes from $L_p\ge6$ via Theorem 3.9(c) alone (§0, §4.4).
- Several "re-run today" labels were wrong: $L_p$ for $p\ge37$, and the landscapes behind the $a\le1000$ dichotomy, rest on archived logs. They are now labelled as such (§3.5, §4.2, §4.4, §7.3).
- Proposition 3.13(c) was only sketched; a proof is now given.
- The density headline $0.898364$ used a level computed by a single implementation; see the computational referee below.
- The summary dropped the hypotheses $G\ge2$ (halving) and $g\ge1$ (constancy), and Theorem 3.9(c) used an unstated partial-coverage form of Tao's lemma. Both are now stated (§0, Corollary 3.7.1, Lemma 1.3(v)).

**Computational referee.** It re-implemented and re-ran nearly every computation: exact values (including $f(34,2)=18444$), the $\gamma_p$ and $\Phi_p$ tables, the $p=2$ census to $G=32$ and the odd-prime censuses, all 23 $\mathrm{Cov}$ certificates including the two largest, the negative scans, the $L_p$ table (including $59\le p\le97$), the two-block windows, all seven witnesses, and the $a\le1000$ landscapes. Everything agreed. Its minor findings:
- The same mis-attribution of the $37\le p\le53$ bounds (fixed).
- The $f(1,3)$ witness is divisible by $3^{2\,000\,001}$, not just $3^{2\,000\,000}$. We confirmed this with `verify_bin` and checked that $3^{2\,000\,002}$ does not divide (R21). The bound is now $f(1,3)\ge2\,000\,001$ (§4.3).
- The $p=5$ ($a=3$) and $p=3$ tail-frontier rows of §4.5 could not be reproduced by a different route within its memory limits. They are not refuted, and are now flagged as single-implementation (§4.5, §7.3).

It also offered three new computations; we re-checked each with our own code before including it:
- $f(1,11)\ge21\,435\,880$, by checking the ten depth-7 positions $11^7K''$ with blocks of length 40. Confirmed by our `cov_pos.c` (R19), which reproduces even the referee's count of $1\,389\,738$ missed residues at $H=39$.
- $f(a,7)\ge960\,792$ for the deep $a\le1000$, from the six depth-7 positions $7^7K''$. Confirmed by `cov_pos.c` and, since the referee's log for this run was not saved, by the referee's `rcover.c` run by us (R19).
- "$\mathrm{Cov}(5,5,35)$ may hold". A sample of 79 classes **refutes** it: 5 of them fail, for example $K'=21001$, which misses 4 residues. We extended this to "every $H\le38$ fails" (R20; §4.2).

Its census to $G=32$ reproduced the archived $\delta_{32}(2)$ exactly ($436\,523\,876$ classes), so the density $0.898364$ now rests on two implementations.

**Novelty referee.** It compared every "new" claim with the public record: Kitamura's two repositories, the earlier AI write-ups (neelsomani, erichou1, przchojecki, AItoBit llm-hunter), the erdosproblems.com page and forum thread, teorth/erdosproblems, formal-conjectures PR #6936, the Zenodo preprint, arXiv and GitHub. It agreed that the mathematics stands and that Q1–Q3 remain open, but found that the first version **overstated novelty and under-credited Kitamura**. These findings were rated serious, and all are now addressed:
- The normal form and the compactness equivalence (Lemma 1.1, Proposition 1.2) were already public (Kitamura; neelsomani, erichou1, AItoBit). They are now credited and are no longer listed as new (§0, §1.2–1.3, §2).
- Locality (Theorem 3.1(a)) is Kitamura's determinacy lemma at $p=2$ (credited, §3.1).
- The $p=2$ value set, "$g=0$ iff $a$ odd" and "$g=3$ iff $a\equiv4 \pmod 8$" were stated by Kitamura as consequences of a certified classification, not as empirical observations. Constancy mod $2^g$ is Kitamura's "sibling-pairing theorem" (stated without a shipped proof). Our halving lemma supplies a proof; the rest is credited (§2, Corollary 3.7.1).
- The claim that rigorous densities were "previously known only on $a\equiv-1$" was false at $p=2$: Kitamura's census of $g\le24$ already gives density $0.8734$. The referee checked that our archived census reproduces Kitamura's class count ($174\,640$). The summary is corrected (§0, §4.7).

Its minor findings, also addressed:
- Kitamura's shadow family $a=2^t-2$ and the term "shadow" are now credited, and the phrase "refutes the natural conjecture" is dropped (Proposition 3.4).
- Two examples of Theorem 3.2 settle residue patterns that Kitamura had listed for audit; this is now said (§0, §3.2).
- Tao's comment already anticipated the position independence of Theorems 3.9(b) and 3.12(a); the $\mathrm{Cov}$/$\mathrm{UC}$ framework is now described as carrying out Tao's programme (§2, §3.5, §3.7).

**What the referees did not cover.** The Monte Carlo and Fourier heuristics of §5 were not re-done. No referee was human. **The round-1 referees did not see anything in §10.** A separate round of three AI referees checked §10; see §10.8.

---

## 10. Round 2, 2026-10-11/12

> **Everything in this section is new in revision 2. No human has refereed it.** The round-1 referee reports of §9 do not cover it. It was checked in two stages:
> - the lead-author AI instance checked the proofs line by line and re-ran the computations listed in §10.7;
> - three round-2 AI referees (logic, computation, novelty) then checked it independently, each writing its own code (§10.8).
>
> The referees found no fatal or serious mathematical error. They found two serious problems of credit and attribution and several minor errors; all are corrected in this version.
>
> In this section, "the lead" means the lead-author AI instance (Claude), not the human author.

### 10.0 Provenance, status check, headline

*Provenance.* Round 2 ran on 2026-10-11/12 as five parallel tracks, each a Claude Opus 5.5 instance in the same workflow as round 1 (§8):
- R1a and R1b: the prime $2$ (Q1; target T4 of §6);
- R2a: the Fourier route to Q3;
- R2b: the renormalisation route to Q3;
- R3: the certified-covering frontier (Theorem 3.12).

A lead-author instance (also Claude) wrote this section from the track reports, after checking each proof given as a theorem below and re-running the computations (§10.7). Track labels record provenance only.

*Status check (2026-10-11).* The workflow lead found no new results on #404 by anyone since 2026-10-08:
- erdosproblems.com/404 is unchanged: open, last edited 29 Sep 2025, 0 proof claims. Tracks R1b, R2a and R2b each re-fetched the page that day and saw the same.
- Kitamura's two repositories are unchanged.
- teorth/erdosproblems lists #404 as open.
- formal-conjectures PR #6936 still only formalises the statement.

Track R1b also ran a web search for an almost-all or measure-zero result at $p=2$ and found none.

*Novelty check by the round-2 novelty referee (2026-10-12).* The referee re-checked the public record:
- erdosproblems.com/404 is unchanged (last edited 29 Sep 2025, 0 proof claims; the newest comment is Kitamura's of 8 Jul 2026).
- Kitamura's repositories were last pushed on 7–8 Jul 2026.
- teorth/erdosproblems lists #404 as open.
- formal-conjectures PR #6936 is open and formalises only the statement.
- arXiv and GitHub searches found nothing new.

It found no prior proof or claim of $\mu(K_2)=0$, of the round-2 lower bounds, of the failure of $\mathrm{Cov}(11,7,40)$, or of the structural results of §§10.3–10.4. It did find that Kitamura's July 2026 repository already describes $p=2$ as a critical branching process, with a measured surviving fraction of about $11.5/G$. Round 1 had not credited this; it is now credited in §§0, 2 and 5 and in §10.8. We cannot exclude overlap with unpublished or AI-generated work.

*Headline.*
1. **$\mu(K_2)=0$ [proved; AI-refereed] (Theorem 10.1).** So $f(a,2)<\infty$ for all $a$ outside a set of natural density $0$. This proves the weak form of Conjecture 5.1, which Kitamura's data had anticipated empirically, and settles target T4 of §6. It does **not** decide whether any particular natural number has $f(a,2)=\infty$.
2. **Larger certified lower bounds [computer-assisted] (§10.2):**
   - $f(1,13)\ge883\,708\,272$ and $f(1,17)\ge7\,411\,742\,272$;
   - $f(1,19)\ge943\,531\,272$ and $f(1,23)\ge3\,559\,590\,232$;
   - $f(1,11)\ge235\,794\,760$ and $f(1,7)\ge6\,725\,592$.

   Each bound is certified by at least two programs, re-run on 2026-10-12. For $f(1,17)\ge7\,411\,742\,272$ these are programs A and C; program B's half of that bound rests on track logs and was not re-run. See §10.2 for which programs are independent of which.
3. **Structural theorems that constrain or reformulate the attack on Q3 [proved] (§§10.3–10.4):**
   - which carry-set information can propagate through a gate block or a short window;
   - monotonicity of $\mathrm{Cov}$ in $H$, and a layer obstruction;
   - a Fourier reduction that leaves only deep-gate frequencies (a sufficient condition for Q3);
   - an exact renormalisation identity for the Fourier shell sums;
   - an explicit conditional theorem: a stated random-model Fourier bound would imply Q3 (a sufficient condition, not an equivalence).
4. **Q3 remains OPEN.** Nothing in this note proves $f(a,p)=\infty$ for any pair $(a,p)$.

### 10.1 The prime 2: $K_2$ is Haar-null

This is track R1b's proof (`code/round2/R1b/muK2_proof.tex`). The lead has rewritten it here with additional detail where a step was terse; such steps are marked "(detail added)". Track R1a found a different argument for the same theorem (§10.1.4), which we have not checked to the same standard.

*Notation for §10.1 only.*
- $v=v_2$, $s(\cdot)$ is the binary digit sum, and $\mu$ is Haar probability measure on $\mathbb Z_2$.
- For $x\in\mathbb Z_2$ and $j\ge0$:
$$\pi_j(x)=\prod_{i=1}^{j}(x+i),\qquad V_n(x)=v(\pi_n(x)),\qquad W_n(x)=n-V_n(x),\qquad M_n(x)=\max_{1\le i\le n}v(x+i).$$
- For a polynomial or power series $F$, write $F^{[i]}=F^{(i)}/i!$.
- A *path of length $n$* is a word $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$. Put $S_e(X)=\sum_{j<n}e_j\pi_j(X)\in\mathbb Z[X]$. This is $S_B$ of §1.2 with $B=\{j\ge1:e_j=1\}$.
- The path $e$ is *alive at $n$* (for $x$) if $v(S_e(x))\ge V_n(x)$. Its *target* is then $\tau_n(e,x):=-S_e(x)/\pi_n(x)\in\mathbb Z_2$, and $\tau_{n+1}=(\tau_n-e_n)/(x+n+1)$. Its *slope* is $\lambda_e(x):=v(S_e'(x))$.
- For an infinite word $e$ with $e_0=1$, $F_e(x)=\sum_{j\ge0}e_j\pi_j(x)$.

*Basic facts.*
- By Proposition 1.2, $x\in K_2$ iff $F_e(x)=0$ for some infinite $e$. A finite $B$ is the word with trailing zeros.
- If $x$ is odd, every $S_e(x)$ is odd, so $K_2\subseteq2\mathbb Z_2$.
- *Backward integrality.* If $e'=(e,f)$ is alive at $N>n$, then $e$ is alive at $n$, because $S_e=S_{e'}-\sum_{n\le j<N}f_j\pi_j$ and $2^{V_n}\mid\pi_j$ for $j\ge n$.

**Theorem 10.1 ($\mu(K_2)=0$) [proved; checked line by line by the round-2 AI logic referee; not human-refereed].** $K_2=\{x\in\mathbb Z_2:g_2(x)=\infty\}$ has Haar measure $0$. Consequently:
- $\delta_G(2)\downarrow0$ as $G\to\infty$;
- the set $\{a\ge1:f(a,2)=\infty\}$ has natural density $0$;
- for every $\varepsilon>0$ there is $G(\varepsilon)$ with $f(a,2)\le v_2(a!)+G(\varepsilon)$ for all $a$ outside a set of natural density at most $\varepsilon$.

The consequences follow from Theorem 3.1(c): $\{a:f(a,2)=\infty\}\subseteq\{a:g_2(a)\ge G\}$, whose natural density $\delta_G(2)=\mu\{g_2\ge G\}$ decreases to $\mu(K_2)$.

**Lemma 10.2 (valuations).** Let $x\in2\mathbb Z_2$ not be a negative integer.
- (a) $V_n\ge v(n!)=n-s(n)$, so $W_n\le s(n)\le\log_2n+1$.
- (b) $V_n\le n+M_n$.
- (c) $V_j-V_n\ge\lfloor(j-n)/2\rfloor$ for $j\ge n$.
- (d) For $K\ge1$ let $N_K=\min\{N\ge1:2^K\mid x+N\}$. Then $W_{N_K}\le1-s(x\bmod2^K)$.
- (e) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$ for $i\ge0$, $j\ge1$.
- (f) For $S\in\mathbb Z_2[X]$ and $y,h\in\mathbb Z_2$: $S(y+h)=\sum_iS^{[i]}(y)h^i$, with every $S^{[i]}(y)\in\mathbb Z_2$.

*Proof.*
- (a) Among $n$ consecutive elements of $\mathbb Z_2$, at least $\lfloor n/2^\ell\rfloor$ are divisible by $2^\ell$; sum over $\ell\ge1$.
- (b) At most $\lceil n/2^\ell\rceil\le n/2^\ell+1$ are divisible by $2^\ell$, and none by $2^{M_n+1}$. So $V_n\le\sum_{\ell=1}^{M_n}(n/2^\ell+1)<n+M_n$.
- (c) $x+i$ is even for even $i$.
- (d) Let $r=x\bmod2^K\in[0,2^K)$. Then $N_K=2^K-r$ (or $2^K$ if $r=0$).
  - For $1\le i<N_K$ we have $r+i\in(r,2^K)$ and $v(x+i)=v(r+i)<K$. Hence $\sum_{i<N_K}v(x+i)=v((2^K-1)!)-v(r!)=(2^K-1-K)-(r-s(r))$.
  - Also $v(x+N_K)\ge K$. So $V_{N_K}\ge N_K-1+s(r)$.
- (e) $\pi_j^{[i]}(x)=\pi_j(x)\,e_i\big(\tfrac1{x+1},\dots,\tfrac1{x+j}\big)$, with $e_i$ the elementary symmetric function.
- (f) Taylor's formula; $S^{[i]}$ has coefficients in $\mathbb Z_2$. ∎

*The good set.* Let $\Omega$ be the set of $x\in2\mathbb Z_2$ such that:
- (G1) $x$ has infinitely many binary digits equal to $1$;
- (G2) there is $t_0$ with $M_n(x)\le2\log_2n$ for all $n\ge2^{t_0}$.

Then $\mu(2\mathbb Z_2\setminus\Omega)=0$. (G1) is clear. For (G2), the events $A_t=\{\exists\,i\le2^{t+1}:v(x+i)\ge2t\}$ have $\mu(A_t)\le2^{1-t}$. By Borel–Cantelli, almost every $x$ lies in only finitely many $A_t$. If $x\notin A_t$, then $M_n<2t\le2\log_2n$ for $n\in[2^t,2^{t+1})$. (G2) excludes the negative integers. So it suffices to show $\mu(K_2\cap\Omega)=0$.

**Lemma 10.3 (Taylor expansion; finite multiplicity).** Let $x\in\Omega$ and let $e$ be an infinite word.
- For every $i$ the series $F_e^{[i]}(x):=\sum_je_j\pi_j^{[i]}(x)$ converges, and
$$v\big(F_e^{[i]}(x)-S_{e|_n}^{[i]}(x)\big)\ge\inf_{j\ge n}(V_j-iM_j)\xrightarrow[n\to\infty]{}\infty.$$
- $F_e(x+h)=\sum_{i\ge0}F_e^{[i]}(x)h^i$ for all $h\in2\mathbb Z_2$.
- Not all $F_e^{[i]}(x)$ vanish. Hence if $F_e(x)=0$, there is a least $k\ge1$, the *multiplicity*, with $F_e^{[k]}(x)\ne0$.

*Proof.*
- By Lemma 10.2(a),(e) and (G2), $V_j-iM_j\ge j-(2i+1)\log_2j-1\to\infty$. This gives convergence and the tail bound.
- For $h\in2\mathbb Z_2$, the family $\{e_j\pi_j^{[i]}(x)h^i\}_{0\le i\le j}$ is summable. Its terms have valuation $\ge i+\max(0,V_j-iM_j)$, so for each $B$ only finitely many have valuation $<B$.
  - Summing first over $i$ gives $\sum_je_j\pi_j(x+h)=F_e(x+h)$, by Lemma 10.2(f).
  - Summing first over $j$ gives $\sum_iF_e^{[i]}(x)h^i$.
- Take $h=-4-x\in2\mathbb Z_2$. Since $\pi_j(-4)=0$ for $j\ge4$, $F_e(-4)=1-3e_1+6e_2-6e_3\equiv1\pmod3$. So $F_e(-4)\ne0$, and not all coefficients vanish. ∎

**Definition (populations).** For $L\ge0$ and $n\ge1$:
- $P^{1,L}_n(x)=\{e\text{ alive at }n:\lambda_e(x)\le L\}$.
- For $k\ge2$, with $\theta_n=\theta^{(k)}_n:=n-(2k+1)\log_2n$:
$$P^{k,L}_n(x)=\{e\text{ alive at }n:\ v(S_e^{[i]}(x))\ge\theta_n\ (1\le i\le k-1),\ v(kS_e^{[k]}(x))\le L\}.$$

**Lemma 10.4 (zeros produce populations).** Let $x\in K_2\cap\Omega$ with $F_e(x)=0$ of multiplicity $k$, and let $L\ge\kappa:=v(kF_e^{[k]}(x))$. Then $e|_n\in P^{k,L}_n(x)$ for all large $n$.

*Proof.*
- $e|_n$ is alive at $n$, because $S_{e|_n}(x)=-\sum_{j\ge n}e_j\pi_j(x)$.
- By Lemma 10.3, $v(kS^{[k]}_{e|_n}(x))=\kappa$ for large $n$.
- For $1\le i<k$, $F_e^{[i]}(x)=0$, so $v(S^{[i]}_{e|_n}(x))\ge\inf_{j\ge n}(j-(2k-1)\log_2j-1)\ge\theta_n$ for large $n$. ∎

**Lemma 10.5 (linearisation).** Let $x\in2\mathbb Z_2$ not be a negative integer, $n<N$, $m:=V_n(x)$ and $D:=V_N(x)-m$, and assume $M_N(x)<m$. Let $C=x+2^m\mathbb Z_2$, with normalised Haar measure. Write $x'=x_0+2^mw\in C$ with $x_0\in[0,2^m)$ and $w\in\mathbb Z_2$. For $f\in\{0,1\}^{N-n}$ put $Q_f(X):=\sum_{j=n}^{N-1}f_j\pi_j(X)/\pi_n(X)\in\mathbb Z[X]$.
- (a) $V_n$, $V_N$ and $M_N$ are constant on $C$. For every path $e$ of length $n$, aliveness at $n$ is constant on $C$, and so are $S_e^{[i]}(x')\bmod2^m$ and $Q_f(x')\bmod2^m$.
- (b) If $e$ is alive at $n$, then
$$\tau_n(e,x')\equiv\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)\,w\pmod{2^{m-M_n}},\qquad\text{where }\omega=\pi_n(x_0)/2^m\in\mathbb Z_2^\times.$$
- (c) $(e,f)$ is alive at $N$ iff $e$ is alive at $n$ and $\tau_n(e,x')\equiv Q_f(x')\pmod{2^D}$. In that case $\tau_N((e,f),x')=(\tau_n(e,x')-Q_f(x'))\,\pi_n(x')/\pi_N(x')$.

*Proof.*
- (a) $v(x'+i)=v(x+i)$ for $i\le N$, because $v(x+i)\le M_N<m$. The rest is reduction of integer polynomials mod $2^m$.
- (b) Put $h=2^mw$. By Lemma 10.2(f), $S_e(x')=S_e(x_0)+hS_e'(x_0)+h^2R$ with $R\in\mathbb Z_2$. Also $\pi_n(x')=\pi_n(x_0)(1+E)$ with $1+E=\prod_{i\le n}(1+h/(x_0+i))$ and $v(E)\ge m-M_n\ge1$. Hence
$$\tau_n(e,x')=\big[\tau_n(e,x_0)-\omega^{-1}wS_e'(x_0)-\omega^{-1}2^mw^2R\big](1+E)^{-1},$$
  and the bracket is in $\mathbb Z_2$.
- (c) Use backward integrality, $S_{(e,f)}=\pi_n\,(Q_f-\tau_n(e,\cdot))$ and $V_N=V_n+D$. ∎

*Frozen-state weights.* For $\lambda\ge0$ and $n$ define
$$a_n^{(\lambda)}(t):=\mathbb P_{f\in\{0,1\}^{2\lambda}}\Big(\sum_{i<2\lambda}f_i\,\frac{\pi_{n+i}(x)}{\pi_n(x)}\equiv t\pmod{2^\lambda}\Big),\qquad\rho_n(e):=2^{\lambda_e}\,a_n^{(\lambda_e)}\big(\tau_n(e,x)\big).$$
- $a_n^{(\lambda)}$ depends only on $n$, $\lambda$ and $x\bmod2^\lambda$, and $\sum_{t\bmod2^\lambda}a_n^{(\lambda)}(t)=1$.
- $a_n^{(\lambda)}\in2^{-2\lambda}\mathbb Z$, so $\rho_n(e)>0$ implies $\rho_n(e)\ge2^{-\lambda_e}$.
- By Lemma 10.2(c), the terms with $j\ge n+2\lambda$ of any $Q_f$ vanish mod $2^\lambda$. So if $N-n\ge2\lambda$, then $a_n^{(\lambda)}(t)=\mathbb P_{f\in\{0,1\}^{N-n}}(Q_f(x)\equiv t\bmod2^\lambda)$.
- For $\lambda\le1$, $\rho\equiv1$. In general $\rho$ is not constant: for $\lambda=3$ and $x+n\equiv7\pmod8$ it is $(4,4,0,0,0,0,0,0)$ (`code/round2/R1b/rho_table.py`).

**Proposition 10.6 (one-window identity, slope $\le L$).** In the setting of Lemma 10.5, let $L\ge0$ and assume
$$\text{(W1) }N-n\ge2L+2,\qquad\text{(W2) }D+L\le m-M_n,\qquad\text{(W3) }L<m-M_N.$$
Let $e\in P^{1,L}_n(x)$ (by Lemma 10.5(a) and $L<m$ this is a property of $C$), and $\lambda=\lambda_e$. Then:
- (i) every child $(e,f)$ alive at $N$ at any $x'\in C$ has slope $\lambda$, and every $e''\in P^{1,L}_N(x')$ has $e''|_n\in P^{1,L}_n(x)$;
- (ii) $s_e:=\tau_n(e,x')\bmod2^\lambda$ is constant on $C$;
- (iii) for every $s\in\mathbb Z/2^\lambda$,
$$\mathbb E_{x'\in C}\,\#\{f:(e,f)\text{ alive at }N,\ \tau_N((e,f),x')\equiv s\ (2^\lambda)\}=2^{W_N-W_n}\,a_n^{(\lambda)}(s_e).$$

*Proof.* By Lemma 10.2(c) and (W1), $D\ge\lfloor(N-n)/2\rfloor\ge L+1>\lambda$.
- (i) $S'_{(e,f)}=S'_e+\sum_{n\le j<N}f_j\pi'_j$. By Lemma 10.2(e) and (W3), $v(\pi'_j(x'))\ge V_j-M_j\ge m-M_N>L$. So a child of a slope-$\lambda$ parent has slope $\lambda$, and a parent of slope $>L$ has only children of slope $>L$. With backward integrality, and since slope $\le L<m$ is constant on $C$, this gives (i).
- (ii) $v(S_e'(x_0))=\lambda$, because $S'_e(x_0)\equiv S'_e(x)\pmod{2^m}$ and $\lambda<m$. Also $\lambda\le m-M_n$. Apply Lemma 10.5(b).
- (iii) By Lemma 10.5(b) and (W2), $t(w):=\tau_n(e,x_0+2^mw)\bmod2^{D+\lambda}$ equals $(\tau_0-2^\lambda\beta w)\bmod2^{D+\lambda}$. Here $\tau_0=\tau_n(e,x_0)$ and $\beta=\omega^{-1}S_e'(x_0)/2^\lambda\in\mathbb Z_2^\times$.
  - So $t$ depends only on $w\bmod2^D$, and $w\bmod2^D\mapsto t$ is a bijection onto the coset $\tau_0+2^\lambda\mathbb Z/2^{D+\lambda}$.
  - Since $D+\lambda\le m$, two quantities are constant on $C$: $q_f:=Q_f(x')\bmod2^{D+\lambda}$, and the unit $u:=\pi_N(x')/(2^D\pi_n(x'))\bmod2^\lambda$.
  - Fix $f$. By Lemma 10.5(c), the child $(e,f)$ is alive iff $t\equiv q_f\pmod{2^D}$ (detail added).
  - If $q_f\not\equiv\tau_0\pmod{2^\lambda}$, no $t$ in the coset satisfies this, as $D\ge\lambda$.
  - If $q_f\equiv\tau_0\pmod{2^\lambda}$, the admissible $t$ are exactly $t=q_f+2^Dz$ with $z\in\mathbb Z/2^\lambda$. All of them lie in the coset. By Lemma 10.5(c) the child then has $\tau_N\equiv zu^{-1}\pmod{2^\lambda}$, a bijection $z\leftrightarrow s$.
  - So for each $s$, exactly one class $w\bmod2^D$ (probability $2^{-D}$) produces a child in state $s$.
  - Summing over $f$, the expectation is $2^{-D}\#\{f:Q_f(x)\equiv s_e\ (2^\lambda)\}=2^{N-n-D}a_n^{(\lambda)}(s_e)$, using $N-n\ge2\lambda$. Finally $N-n-D=W_N-W_n$. ∎

**Proposition 10.7 (window bound, multiplicity $k\ge2$).** In the setting of Lemma 10.5, let $k\ge2$, $L\ge0$ and $\theta=\theta^{(k)}$. Assume $\theta$ is nondecreasing on $[n,N]$ and
$$\text{(V1) }D\le\min(\theta_n,m-M_n),\quad\text{(V2) }\theta_N\le2m-kM_N,\quad\text{(V3) }\theta_n\le m-(k-1)M_N,\quad\text{(V4) }L<m-kM_N.$$
Then every $e''\in P^{k,L}_N(x')$ ($x'\in C$) has $e''|_n\in P^{k,L}_n(x)$. Moreover, for $e\in P^{k,L}_n(x)$ and $r=\lfloor(N-n-1)/2\rfloor$,
$$\mathbb E_{x'\in C}\,\#\{f:(e,f)\in P^{k,L}_N(x')\}\le2^{\,N-n-r+L+m-\theta_N}.$$

*Proof.*

*Closure.* Let $e''=(e,f)\in P^{k,L}_N(x')$. Then $e$ is alive at $n$.
- For $1\le i\le k$ and $n\le j<N$: $v(\pi^{[i]}_j(x'))\ge V_j-iM_j\ge m-iM_N$. By (V3) this is $\ge\theta_n$ for $i\le k-1$, and by (V4) it is $>L$ for $i=k$.
- Hence $v(S^{[i]}_e)\ge\min(\theta_N,\theta_n)=\theta_n$ for $i<k$, and $v(kS^{[k]}_e)=v(kS^{[k]}_{e''})\le L$.
- These conditions are constant on $C$: they live mod $2^m$, because $\theta_n\le n-\log_2n-1\le v(n!)\le m$ and $L<m$.

*Count.* Let $e\in P^{k,L}_n(x)$.
- Since $k\ge2$, $v(S_e'(x_0))\ge\min(\theta_n,m)\ge D$. By Lemma 10.5(b) and (V1), $\tau_n(e,x')\equiv\tau_0\pmod{2^D}$ on $C$. So the set $F_0=\{f:(e,f)\text{ alive at }N\}=\{f:Q_f(x_0)\equiv\tau_0\ (2^D)\}$ is constant on $C$.
- *Bound on $|F_0|$.* The valuations $\ell_j=V_j-V_n$ ($n\le j<N$) of the coefficients of $Q_f$ start at $0$. They increase strictly at each $j$ with $x+j+1$ even. Only the last value can equal $D$. So they take at least $r$ distinct values $<D$.
  - Choose one index for each such value. The corresponding subset sums are pairwise distinct mod $2^D$, because the lowest-valuation term of a difference dominates.
  - Hence every residue mod $2^D$ is hit by at most $2^{N-n-r}$ words $f$, and $|F_0|\le2^{N-n-r}$.
- *Probability for each $f\in F_0$.* Membership of $(e,f)$ in $P^{k,L}_N(x')$ requires $v(S^{[k-1]}_{(e,f)}(x'))\ge\theta_N$. Expanding at $x_0$ with $h=2^mw$ (Lemma 10.2(f); $(S^{[k-1]})'=kS^{[k]}$):
$$S^{[k-1]}_{(e,f)}(x')=A_f+h\,kS^{[k]}_e(x_0)+h\textstyle\sum_jf_j\,k\pi^{[k]}_j(x_0)+(\text{terms of valuation}\ge2m).$$
  - $A_f\in\mathbb Z_2$ does not depend on $w$.
  - The third term has valuation $\ge2m-kM_N\ge\theta_N$, by Lemma 10.2(e) and (V2).
  - Let $\gamma=kS^{[k]}_e(x_0)$. Then $v(\gamma)=v(kS^{[k]}_e(x))\le L$, as $L<m$.
  - The set of $w\in\mathbb Z_2$ with $v(A_f+2^m\gamma w)\ge\theta_N$ is empty or a single coset of $2^{\lceil\theta_N\rceil-m-v(\gamma)}\mathbb Z_2$. Its measure is at most $2^{m+L-\theta_N}$ (trivially so if $\theta_N\le m+v(\gamma)$).
- Summing over $f\in F_0$ gives the bound. ∎

*Proof of Theorem 10.1.* By Lemmas 10.3 and 10.4, $K_2\cap\Omega\subseteq\bigcup_{k\ge1,L\ge0}K^{k,L}$. Here $K^{k,L}$ is the set of $x\in\Omega$ that have an infinite $e$ with $F_e(x)=0$ of multiplicity $k$ and $v(kF^{[k]}_e(x))\le L$. For such $x$, $e|_n\in P^{k,L}_n(x)$ for all large $n$. We show $\mu(K^{k,L})=0$.

*Digit filtration.* The window times $(n_\ell)_{\ell\ge0}$ below start at a fixed $n_0\ge4$. Each $n_{\ell+1}$ is a function of the numbers $\min(v(x+i),M_{n_\ell}+1)$ for $i\le\lfloor5n_\ell/4\rfloor$, hence of $x\bmod2^{M_{n_\ell}+1}$ (detail added). Put $m_\ell=V_{n_\ell}(x)$ and $A_\ell(x)=x+2^{m_\ell(x)}\mathbb Z_2$.
- Since $x$ is even and $n_\ell\ge4$, at least two of $x+1,\dots,x+n_\ell$ are even, so $m_\ell\ge M_{n_\ell}+1$.
- Hence every $y\in A_\ell(x)$ has $v(y+i)=v(x+i)$ for $i\le n_\ell$. So $n_0,\dots,n_{\ell+1}$ and $m_\ell$ are the same for $y$ as for $x$, and $\{A_\ell(x)\}$ is a partition of $2\mathbb Z_2$ into cylinders.
- $m_{\ell+1}\ge m_\ell$, so $A_{\ell+1}(x)\subseteq A_\ell(x)$.
- Let $\mathcal C_\ell$ be the hypotheses of the relevant window proposition for the window $[n_\ell,n_{\ell+1})$, together with $M_{n_{\ell+1}}<m_\ell$. By Lemma 10.5(a), the truth of $\mathcal C_\ell$ is constant on $A_\ell(x)$. Note that $M_{n_{\ell+1}}<m_\ell$ is itself a condition on $x\bmod2^{m_\ell}$.
- For each $j$, let $(\mathcal G^{(j)}_\ell)_{\ell\ge j}$ be the $\sigma$-algebras with atoms $A_\ell(x)$, frozen ($A_{\ell+1}:=A_\ell$) from the first $\ell\ge j$ at which $\mathcal C_\ell$ fails. This is a filtration.
- Conditional expectation given $\mathcal G^{(j)}_\ell$ is the average over the atom. The conditional law of the digits of $x$ above position $m_\ell$ is Haar; this is the only randomness used.

*Case $k=1$ (critical: a quenched martingale).* Fix $L$ and $n_0\ge8L+16$.
- Let $\nu_\ell=\min\{N>n_\ell:v(x+N)>M_{n_\ell}\}$ (the next record) and
$$n_{\ell+1}=\min\big(\max(\nu_\ell,\,n_\ell+2L+2),\ \lfloor5n_\ell/4\rfloor\big).$$
  Then (W1) holds automatically. Let $\mathcal C_\ell$ consist of (W2), (W3) and $M_{n_{\ell+1}}<m_\ell$.
- For $j\ge0$ and $\ell\ge j$ let
$$M^{\rm mart}_\ell=2^{-W_{n_\ell}}\sum_{e\in P^{1,L}_{n_\ell}}\rho^{(\ell)}(e),\qquad\rho^{(\ell)}(e)=2^{\lambda_e}a^{(\lambda_e)}_{n_\ell}(\tau_{n_\ell}(e,x)).$$
  Freeze it after the first failure $\sigma_j=\min\{\ell\ge j:\mathcal C_\ell\text{ fails}\}$: set $M^{\rm mart}_\ell:=M^{\rm mart}_{\sigma_j}$ for $\ell\ge\sigma_j$, and $M^{\rm mart}_\ell:=0$ for all $\ell\ge j$ on the $\mathcal G_j$-measurable event $\{\sigma_j=j\}$.
- $M^{\rm mart}_\ell$ is $\mathcal G_\ell$-measurable. This uses Lemma 10.5(a), and Lemma 10.5(b) at time $n_\ell$, which applies because $\lambda_e\le L\le m_\ell-M_{n_\ell}$: for $\ell=j$ by (W2), and for $\ell>j$ by (W3) of the previous window, since $L<m_{\ell-1}-M_{n_\ell}\le m_\ell-M_{n_\ell}$.

*Martingale property.* On $\{\sigma_j>\ell\}$, Proposition 10.6(i) shows that $P^{1,L}_{n_{\ell+1}}$ is the disjoint union, over $e\in P^{1,L}_{n_\ell}$, of the alive children of $e$, each of slope $\lambda_e$. A child in state $s$ has weight $2^{\lambda_e}a^{(\lambda_e)}_{n_{\ell+1}}(s)$, which is constant on the atom. By Proposition 10.6(iii) and $\sum_sa_{n_{\ell+1}}(s)=1$,
$$\mathbb E[M^{\rm mart}_{\ell+1}\mid\mathcal G_\ell]=2^{-W_{n_{\ell+1}}}\sum_e\sum_s2^{W_{n_{\ell+1}}-W_{n_\ell}}a^{(\lambda_e)}_{n_\ell}(s_e)\,2^{\lambda_e}a^{(\lambda_e)}_{n_{\ell+1}}(s)=M^{\rm mart}_\ell.$$
So $(M^{\rm mart}_\ell)_{\ell\ge j}$ is a nonnegative martingale. In transfer-operator language: on frozen residue states the window operator has rank one, and $\rho=2^\lambda a$ is its harmonic weight.

*Lower bound on survival.* On $\{\sigma_j>\ell\}$, suppose $P^{1,L}_{n_{\ell+1}}\neq\emptyset$. Then some $e\in P^{1,L}_{n_\ell}$ has a child, which forces $a^{(\lambda_e)}_{n_\ell}(s_e)>0$, so $\rho^{(\ell)}(e)\ge2^{-L}$. Hence $M^{\rm mart}_\ell\ge2^{-W_{n_\ell}-L}$.

*The environment walk is unbounded below.* Let $x\in\Omega$, take $K$ with $N_K>n_j$, and let $\ell$ be the last index with $n_\ell<N_K$.
- All $v(x+i)$ with $i\le n_\ell$ are $<K\le v(x+N_K)$. So $\nu_\ell\le N_K$, and $N_K\le n_{\ell+1}\le N_K+2L+2$.
- Since $W_{N+\delta}\le W_N+\delta$, Lemma 10.2(d) gives $W_{n_{\ell+1}}\le3+2L-s(x\bmod2^K)$.
- By (G1), this tends to $-\infty$ as $K\to\infty$.

*Conclusion for $k=1$.*
- Let $E_j=\{\sigma_j=\infty\}\cap\{P^{1,L}_{n_\ell}\ne\emptyset\ \forall\ell\ge j\}\cap\Omega$. On $E_j$, the last two paragraphs give $\sup_\ell M^{\rm mart}_\ell=\infty$.
- On each atom $A$ of $\mathcal G_j$ (a cylinder with normalised Haar measure $\mu_A$), $(M^{\rm mart}_\ell)_{\ell\ge j}$ is a nonnegative martingale with a finite constant initial value. Doob's maximal inequality gives $\mu_A(\sup_\ell M^{\rm mart}_\ell\ge t)\le M^{\rm mart}_j(A)/t$, so $\mu_A(\sup=\infty)=0$ and $\mu(E_j)=0$.
- On $\Omega$ all hypotheses hold for large $\ell$. With $M_n\le2\log_2n$, Lemma 10.2(a),(b) give $m_\ell\ge n_\ell-\log_2n_\ell-1$ and $D_\ell\le n_\ell/4+3\log_2n_\ell+2$. So (W2), (W3) and $M_{n_{\ell+1}}<m_\ell$ hold once $n_\ell$ is large.
- With Lemma 10.4, every $x\in K^{1,L}$ lies in $E_j$ for all large $j$. Hence $\mu(K^{1,L})\le\sum_j\mu(E_j)=0$.

*Case $k\ge2$ (subcritical).* Fix $k$ and $L$, take a large $n_0$, and set $n_{\ell+1}=\lfloor5n_\ell/4\rfloor$.
- Let $\mathcal C_\ell$ consist of (V1)–(V4), monotonicity of $\theta$ on $[n_\ell,n_{\ell+1}]$, $M_{n_{\ell+1}}<m_\ell$, and $\eta_\ell:=n_{\ell+1}-n_\ell-r_\ell+L+m_\ell-\theta_{n_{\ell+1}}\le-n_\ell/16$.
- Let $Z_\ell=|P^{k,L}_{n_\ell}|$, which is constant on atoms. Put $\tilde Z_\ell=Z_\ell\mathbf 1\{\mathcal C_j,\dots,\mathcal C_{\ell-1}\}$ (detail added).
- By Proposition 10.7, $\mathbb E[\tilde Z_{\ell+1}\mid\mathcal G_\ell]\le2^{-n_\ell/16}\tilde Z_\ell$. Hence $\mu(\tilde Z_\ell\ge1\mid\mathcal G_j)\le Z_j\prod_{j\le i<\ell}2^{-n_i/16}\to0$. So
$$\mu\big(Z_\ell\ge1\text{ and }\mathcal C_\ell\text{ for all }\ell\ge j\big)=0.$$
- On $\Omega$, use $m\le n+M_n$, $r\ge(N-n)/2-1$ and $\theta_N=N-(2k+1)\log_2N$. This gives $\eta_\ell\le-(N-n)/2+1+L+M_n+(2k+1)\log_2N\le-n/16$ for large $n=n_\ell$, since $N-n\ge n/4-1$.
- (V1)–(V4) also hold for large $n$:
  - (V1): $D\le n/4+3\log_2n+2\le\theta_n$;
  - (V2): $\theta_N\le N\le5n/4\le2(n-\log_2n-1)-2k\log_2(2n)$;
  - (V3): $m-(k-1)M_N\ge n-\log_2n-1-2(k-1)\log_2(2n)\ge\theta_n$;
  - (V4) is similar.
- By Lemma 10.4, every $x\in K^{k,L}$ lies in one of these null events, so $\mu(K^{k,L})=0$.

Thus $\mu(K_2\cap\Omega)=0$, hence $\mu(K_2)=0$. ∎

**Remarks 10.8.**
1. *Where the randomness comes from.* The "environment" of a window $[n,N)$ is the list of valuations $v(x+i)$, which depends on only $O(\log n)$ low digits of $x$. The targets $\tau_n$ are moved affinely, with slope $2^\lambda$, by the digits of $x$ at positions $V_n,\dots,V_n+D-1$, i.e. around position $n$. Conditioning on $x\bmod2^{V_n}$, rather than on $O(\log n)$ low digits, turns the heuristic branching process in a random environment of §5 (H1) and §6 (T4) into an exact quenched martingale. No equidistribution of unit parts is needed, contrary to what §6 (T4) anticipated.
2. *The critical walk* is $W_n=n-V_n$. For natural $x$, $W_n=s(n)-c(x,n)$, where $c(x,n)$ is the number of carries in the binary addition $x+n$. It is bounded above by $\log_2n+1$, and it tends to $-\infty$ along record times. This mirrors the classical mechanism by which a critical branching process in a random environment dies out. The quenched first moment is controlled by the associated random walk, and extinction follows once that walk has $\liminf=-\infty$. Almost-sure extinction in this setting goes back to Smith–Wilkinson (1969) and Athreya–Karlin (1971). The criterion in terms of the associated walk is stated in modern form by Afanasyev–Geiger–Kersting–Vatutin (2005), while Kozlov (1976) gives the asymptotics of the survival probability, not the extinction itself. We credit the general strategy (martingale plus an environment walk unbounded below) to this theory, but the proof above is self-contained and uses none of these results. *(Round 2: attribution corrected after the novelty referee; the previous version called this a "Kozlov-type" mechanism.)*
3. *Halving lemmas.* The slope $\lambda_e$ counts the frozen low bits of $\tau_n$. The proofs of Theorem 3.7(a),(b) show $\lambda_e\ge1$ (respectively $\ge3$ for $x\equiv2\pmod4$) for alive paths, when $v(x+2)$ is small compared with $V_n$. The halving lemmas are not used in the proof.
4. *No rate.* The argument is qualitative: it gives $\delta_G(2)\to0$ but no explicit rate. Numerically $\delta_G(2)\approx0.7/\sqrt G$ (§5). Kitamura reports a measured decay of about $11.5/G$ (§2); we have not reconciled the two fits.
5. *What it does not say.* $K_2$ is closed and Haar-null, so it is nowhere dense, which was already known (Theorem 3.6). Theorem 10.1 does not show $K_2\cap\mathbb N=\emptyset$, since a countable set is Haar-null anyway. **The strong form of Conjecture 5.1, "$f(a,2)<\infty$ for every $a$", remains open**, and so does Kitamura's test case $a=594$.

#### 10.1.1 Numerical corroboration of the window identity [computer-assisted; not needed for the proof]

The proof does not depend on any computation. As a check on Propositions 10.6 and 10.7, the following exact-arithmetic tests were re-run by the lead (§10.7, rows S1–S5):
- `mart_check2.py` (track R1b). For random even $x$ with 300 random bits, and each parent path $e$ with $\lambda_e\le D$, it averages $\sum_{\text{children}}\rho_N$ exactly over all $w\bmod2^D$ and compares the result with $2^{W_N-W_n}\rho_n(e)$ in exact rationals. It also checks slope inheritance, constancy of the parent set and of $\tau_n\bmod2^\lambda$ on the cylinder, and the frozen-state equidistribution.
- `brute_window.py` (track R1b; shares no code with `mart_check2.py`). It finds the children by testing $2^{V_N}\mid S_{(e,f)}(x_w)$ for every $f$ and every $w$.
- `negctrl.py`. Replacing $\rho$ by $1$ breaks the identity for most parents with $\lambda\ge2$, so the test is not vacuous. The script's second "control", which shifts each child's state by $1$, never fails. This is what Proposition 10.6(iii) predicts: the expected child counts are the same for every state $s$, so a shift does not change the weighted sum. It is therefore not a control.
- `lemmaB_check.py`. For parents with $\lambda_e\ge D$, the set of alive children is constant on the cylinder, and the distinct-level bound of Proposition 10.7 holds.
- `lead_window_check.py` (written by the lead; shares no code with R1b). It tests Proposition 10.6(iii) **state by state**, under exactly the hypotheses (W1)–(W3), with aliveness decided by direct evaluation of $v(S_{(e,f)}(x_w))$.

The results are in §10.7 (rows S1–S5, S12). All tests passed.

#### 10.1.2 Observed slopes [heuristic]

Over about $22\,000$ alive paths from $700$ random $x$ with a nonempty population at $n\in\{40,80\}$, the slopes $\lambda_e$ took the values $1,3,4,5,\dots$ (up to about $35$), and **$\lambda=2$ never occurred** (`lam_stats.py`; archived logs `data/round2/logs_original/R1b/lam_stats_n*.out`). This would be a "third halving" phenomenon. It is numerical only and is not used.

#### 10.1.3 Odd primes [heuristic remark]

Track R1b remarks that Proposition 10.6 should carry over to odd $p$, with truncation at $p\lambda$ terms and weights $p^\lambda a$. That would give an exact martingale $2^{-n}p^{V_n}\sum\rho$. Its mean is constant, but the normaliser $2^{-n}p^{V_n}\approx(p^{1/(p-1)}/2)^n$ decays exponentially for $p\ge3$. So the expected unnormalised weighted population $\mathbb E\sum\rho$ grows exponentially (supercriticality). *(Round 2: wording corrected after the logic referee; the previous version said the martingale's mean grows.)* An $L^2$ bound for it would give $\mu(K_p)>0$ (Conjecture 5.2). The transfer is only sketched, and the $L^2$ step was not attempted. **Not a result.**

#### 10.1.4 A second route and an explicit-rate claim (track R1a) [sketch only; not verified by the lead]

Track R1a independently found a different argument for $\mu(K_2)=0$. Its main points:
- *Stability balls and conserved weight.* Each valid carry path carries the weight $\mu(\text{ball})\cdot2^{P_n-n}$, where $P_n=v_2(\pi_n(x))$. Once the path reaches a "stability ball" (a ball of radius $2^{-(P_n-\kappa)}$, where $\kappa=v_2(B_n)$ is a derivative offset and $B_n=\sum_i\gamma_i\pi_{i-1}$), this weight is exactly conserved. The reason is that the carry map is a scaled isometry on that ball (its lemmas $S_m$, $T_1$, $T_m$).
- *Deep gates.* A deep gate $v(x+r)=t\ge D$ multiplies a survivor's weight by $2^{t-1-s_2(r-1)}$.
- *Conclusion for simple zeros.* A Cauchy–Schwarz argument gives measure $\le\sqrt{2I(3/4)^D}$ for points carried by simple zeros.
- *Multiple zeros.* These are handled by an order-$m$ hierarchy of Taylor coefficients, along which the weight halves at every even step.

This is consistent with, but different from, §10.1. Its write-up is a proof outline. The lead has **not** checked the lemmas $S_m$, $T_1$, $T_m$ or the stopping argument to the standard of §10.1, so we do not count the route as a second proof.

R1a also claims the following explicit bound. If true, it would give a rate on the three classes it treats, but not for $\delta_G(2)$ itself (see item 4 below). We record it as a claim only.

> **Claim 10.9 (R1a) [unverified].** Let $C_0=8\mathbb Z_2$, $C_2=2+8\mathbb Z_2$ and $C_6=6+16\mathbb Z_2$. For $D\ge7$,
> $$\mu\{x\in C_0\cup C_2\cup C_6:\ g_2(x)\ge2^{D+1}\}\le(2\cdot3^{-3/2}+1/9)(3/4)^{D/2}+2^{D-2^D}.$$
> Hence, for $G\ge256$, $\delta_G(2)\le1/16+0.662\,G^{-0.2075}+G\,2^{-G/4}$; for example $\delta_{2^{40}}(2)\le0.0646$. The term $1/16$ is the measure of the untreated class $14\bmod16$.
>
> *(Round 2 correction.)* The constant is $(2\cdot3^{-3/2}+1/9)\cdot\tfrac43=0.66135$, from the worst case $D=\lfloor\log_2G\rfloor-1\ge\log_2G-2$. The previous version rounded it down to $0.661$. With $0.661$ the $G$-form does not follow from the $D$-form: at $G=511$ ($D=7$) the $D$-form term is $0.1812199$, which exceeds $0.661\cdot511^{-0.2075}=0.1812192$. Both round-2 referees found this slip. With $0.662$, the $D$-form is below the $G$-form for every $256\le G<2^{22}$ (checked numerically).

*Why it is not counted as a result.*
1. It rests on R1a's conservation lemmas, which the lead has not verified.
2. It rests on finite computations: uniform $\kappa=1,3,3$ on the three classes, every path stable by $n_0=8,12,10$, and initial weights $1/16,1/8,1/8$. The lead re-ran `class_check.py` and `I8.py` (§10.7, rows S6–S7) and reproduced these numbers. But `class_check.py` averages over $\eta\bmod2^R$ with random higher digits. Its exactness depends on a locality argument (aliveness through $n_0$ depends only on $x\bmod2^{P_{n_0}}$, and $P_{n_0}\le s+R$ in every case run) that is plausible but not written out.
3. R1a's own Monte Carlo of the *unconditional* expected stopped weight is not bounded: it grows from about $4$ to $15$ as $D$ goes from $3$ to $10$. This comes from late-stabilising paths near $-2$, which is why the claim excludes the class $14\bmod16$.
4. *Even if true, it is weak.* Because of the floor $1/16$, it never gives $\delta_G(2)\to0$. It is also weaker than the existing rigorous census bound $\delta_G(2)\le\delta_{32}(2)=0.1016$ (§4.7; $\delta_G$ is nonincreasing) for every $G$ below about $8\cdot10^5$. For example, it gives $0.272$ at $G=256$ and $0.0998$ at $G=2^{20}$. *(Added after the round-2 novelty referee.)*

For comparison, the Monte Carlo values of §5 are $\delta_{64}\approx0.064$ and $\delta_{254}\approx0.021$, so Claim 10.9 is weak but consistent.

R1a's numerical checks of its lemmas are archived in `data/round2/logs_original/R1a/`:
- Lemma $T_1$: about $1000+1512$ tests, 0 failures;
- exact weight conservation by adaptive refinement: ratio exactly $1$ in $32$ instances;
- synthetic $m=2,3$ tests: 0 failures;
- Monte Carlo on $C_0$: $\mathbb E[\text{stopped weight}\mid C_0]=0.508,0.500,0.491,0.499$ for $D=4,6,8,10$, against the predicted $1/2$.

### 10.2 Odd primes: the certified covering frontier (track R3)

The method is the one of §3.7 and §4.2, with **position certificates** at every first-failure candidate of the next depth. What is new is two programs written from scratch, larger moduli (up to $13^{11}\approx1.8\cdot10^{12}$ and $17^{10}\approx2.0\cdot10^{12}$), and a script that checks every step of the first-failure argument.

**Proposition 10.10 (chain criterion) [proved].** This is a restatement of Lemma 1.3 and Theorem 3.12(a) in the form used. Let $D\ge2$. Suppose that for each depth $1\le t<D$ one of the following holds:
- *(uniform)* $\mathrm{Cov}(p,t,H_t)$ holds with $H_t+1<p^t$; or
- *(positions)* for every $K''<p^{D-t}$ with $p\nmid K''$, there is $H=H_{t,K''}$ with $p^tK''-H>1$ such that the subset sums of $\{y_i(K'')\}_{i<H}$ cover $\mathbb Z/p^{t+c}$, where $c=v_p((H-1)!)$.

Then $f(1,p)\ge v_p((p^D-1)!)$. More generally, for $a<p^D$, the first failure $N^*(a)$ satisfies either $N^*(a)\le a+\max H$ or $N^*(a)\ge p^D$.

*Proof.* Let $N^*$ be the first failure for $a=1$, and suppose $N^*<p^D$. Then $p\mid N^*$; write $N^*=p^tK''$ with $t<D$, $p\nmid K''$ and $K''<p^{D-t}$. In either case some block of length $H$ ending at $N^*$, with $N^*-H>1$, covers the demand. Theorem 3.12(a) and Lemma 1.3(iii) then give $P(1,p,N^*-H)\Rightarrow P(1,p,N^*)$. The hypothesis $P(1,p,N^*-H)$ holds by minimality of $N^*$, which is a contradiction. Hence $P(1,p,p^D-1)$ holds, and Lemma 1.3(i) gives the bound. The case of general $a$ is identical, with the condition $N^*-H>a$. ∎

**The certificates.** Each certificate below was checked by two programs that share no code with each other or with round 1's `cov.c`, `cov_pos.c` and `cov_check2.c`. Both were written by the same track instance (R3) from the same specification, so they are independent implementations but not independent in authorship.
- *Program A* (`code/round2/R3/src/fibcov.c`) splits by the low $k$ digits into fibres and uses meet-in-the-middle enumeration.
- *Program B* (`code/round2/R3/src/fibcov2.c`) builds the block from actual factorial ratios $n!/N_1!$ at the true position, with $M$ from Legendre's formula. It uses a layer split, Gray-code enumeration, and different shift kernels.
- *Program C* (`code/round2/review/computation/covchk.c`) was written from scratch by the round-2 computational referee. It builds the block from the actual integers, splits residues by their low $k$ digits, and applies the high elements by a cyclic shift-OR. It was validated against a numpy brute force on 2047 comparisons (1312 of them failing cases with exact miss counts), with 0 mismatches. It re-certified every entry of the table below, using lifted class representatives $K'+2p^c$ and $K'+3p^c$, which also exercises the class invariance of Theorem 3.12(a) (§10.8).

`code/round2/R3/src/chain.py` parses the logs of both programs, requires both for every certificate, and checks the hypotheses of Proposition 10.10. Both programs and the brute-force reference `brute.py` (actual factorials, numpy) agree on 7 500 comparisons per configuration over 25 small cases, including 158 failing cases with exact miss counts (`validate.py`; re-run, §10.7).

| $p$ | uniform $\mathrm{Cov}(p,t,H_t)$, $t=1,2,\dots$ | positions | new bound $f(1,p)\ge$ | previous (§4) |
|---|---|---|---|---|
| 7 | $H_t=4,7,19,26,28,34$ ($t\le6$) | depth 7: $K''<49$, $H=40$ (42 positions); depth 8: $K''\le6$, $H=47$ | $v_7((7^9-1)!)=6\,725\,592$ | $10^6$ (witness) |
| 11 | $5,10,18,22,30,33$ ($t\le6$) | depth 7: all $110$ positions $K''<121$, $H=40$, except $K''=37$ ($H=41$); depth 8: $K''\le10$, $H=44$ | $v_{11}((11^9-1)!)=235\,794\,760$ | $21\,435\,880$ |
| 13 | $6,10,19,24,32,35,39$ ($t\le7$) | depth 8: $K''\le12$, $H=47$ | $v_{13}((13^9-1)!)=883\,708\,272$ | $67\,977\,552$ |
| 17 | $5,11,16,25,30,34,43$ ($t\le7$; $t=7$ over all $272$ classes) | depth 8: $K''\le16$, $H=47$ | $v_{17}((17^9-1)!)=7\,411\,742\,272$ | $25\,646\,163$ |
| 19 | $5,12,17,27,31,35$ ($t\le6$) | depth 7: $K''\le18$, $H=45$ | $v_{19}((19^8-1)!)=943\,531\,272$ | $49\,659\,537$ |
| 23 | $7,12,18,23,33,37$ ($t\le6$) | depth 7: $K''\le22$, $H=43$ | $v_{23}((23^8-1)!)=3\,559\,590\,232$ | $154\,764\,790$ |

At $p=17$ there is also an intermediate bound, $f(1,17)\ge v_{17}((17^8-1)!)=435\,984\,832$. It needs only $t\le6$ uniform and the 16 depth-7 positions with $H=43$.

*Re-run status.* The table above records track R3's two-program certificates of 2026-10-11 (`data/round2/logs_original/R3/`, chain output `CHAIN_ALL_final.txt`). The lead re-ran on 2026-10-12, with both programs, every certificate behind the bounds for $p=7,11,13,19,23$ and the intermediate bound $f(1,17)\ge435\,984\,832$. The chain check passes on the re-run logs alone (§10.7, rows C1–C6). For $f(1,17)\ge7\,411\,742\,272$, the lead re-ran only program A: uniform $t=7$ over all 272 classes, and the 16 depth-8 positions. Program B's half of that certificate rests on R3's logs of 2026-10-11. The round-2 computational referee then re-certified these two components with program C: uniform $\mathrm{Cov}(17,7,43)$ over all 272 classes, and all 16 depth-8 positions with $H=47$. Its own chain script, run on program C's logs alone, gives CHAIN OK for all six bounds of the table. So $f(1,17)\ge7\,411\,742\,272$ now rests on two programs that were both re-run (A and C), plus B's original logs.

*Re-verification of round 1.* Both new programs cover all $156$ classes of the round-1 headline certificate $\mathrm{Cov}(13,7,39)$. Program B used the lift $K'+169$. Both reproduce the count $1\,389\,738$ of missed residues at $(11,7,39,K''=1)$. So four independently written programs (`cov_pos.c`, the round-1 referee's `rcover.c`, A and B) agree on that number.

*General $a$.* Proposition 10.10 also gives a dichotomy: for every $a<p^D-H^*$, where $H^*$ is the largest $H$ used, either $f(a,p)<v_p((a+H^*)!)$ or $f(a,p)\ge v_p((p^D-1)!)$. Combined with the landscapes of §4.6, every $a\le1000$ in the "$g\ge10^4$" class has:
- $f(a,13)\ge883\,708\,272$;
- $f(a,11)\ge235\,794\,760$;
- $f(a,7)\ge6\,725\,592$, including $a=2,3,5$.

The landscapes are archived and were not re-run in either round, though the round-1 computational referee reproduced them. Since $v_p((a+47)!)-v_p(a!)\le47<10^4$, the "deep" class of §4.6 is in the second alternative.

**Lemma 10.11 (layer obstruction) [proved].** (Track R3.) Let $1\le H\le p^t$, $c=v_p((H-1)!)$ and $y_i(K')=\prod_{s\le i}(p^tK'-(H-s))$. Then:
- (a) for $k\le t$, $y_i(K')\equiv\pi_i(-H)\pmod{p^k}$, independently of $K'$;
- (b) $v_p(y_i)=v_p\big((H-1)!/(H-1-i)!\big)$;
- (c) if, for some $k\le t$, the subset sums of $\{y_i:v_p(y_i)<k\}$ miss a residue mod $p^k$, then $\mathrm{Cov}(p,t,H)$ fails, and so does every position certificate of length $H$ at depth $t$;
- (d) the $p$-adic units among the $y_i$ are exactly $y_0,\dots,y_\rho$ with $\rho=(H-1)\bmod p$, and $y_i\equiv(-1)^\rho\rho!\cdot(-1)^u/u!\pmod p$ with $u=\rho-i$.

Hence $\mathrm{Cov}(p,t,H)$ requires $\rho\ge\rho_0(p)$, where $\rho_0(p)$ is the least $\rho$ such that the subset sums of $\{(-1)^u/u!:u\le\rho\}$ cover $\mathbb Z/p$. Also $\mathrm{Cov}(p,1,H)$ holds iff $H\ge\rho_0(p)+1$, so the minimal $H_1(p)$ equals $\rho_0(p)+1$.

*Proof.*
- (a) $p^tK'\equiv0\pmod{p^k}$, and $\prod_{s\le i}(s-H)=\pi_i(-H)$.
- (b) $v_p(p^tK'-(H-s))=v_p(H-s)$, because $0<H-s<p^t$.
- (c) Elements of valuation $\ge k$ vanish mod $p^k$. Covering $\mathbb Z/p^{t+c}$ implies covering $\mathbb Z/p^k$.
- (d) By (b), $y_i$ is a unit iff none of $H-1,\dots,H-i$ is divisible by $p$, iff $i\le\rho$. Since $H\equiv\rho+1\pmod p$, $\prod_{s\le i}(s-H)\equiv(-1)^i\rho!/(\rho-i)!$, and $(-1)^i=(-1)^\rho(-1)^u$.
- For $t=1$ and $H\le p$, every element is a unit and $c=0$. Adding elements can only enlarge the set of subset sums. ∎

$\rho_0(p)=1,2,3,4,5,4,4,6,6,6$ for $p=3,5,7,11,13,17,19,23,29,31$ (recomputed by the lead with `lead_checks.py`, §10.7). This matches the $H_1$ values of §4.2. The case $k\ge2$ of (c) explains the $p=5$ failures at $H=33,34$, where the multiple $25$ causes a double jump in valuation.

**Negative certificates [computer-assisted].**
- **$\mathrm{Cov}(11,7,40)$ is false.** The class $K'\equiv37\pmod{11^3}$ misses exactly $2$ residues mod $11^{10}$. Four programs agree on the count: A and B, the round-2 computational referee's program C, and the round-2 logic referee's fibre/bitset checker `covmiss.c`. The last of these lists the two missed residues as $18\,038\,488\,330$ and $23\,022\,655\,245$. So the "computational next step" of §6, running $\mathrm{Cov}(11,7,40)$ over all classes, would have failed. $H=41$ covers this class (A, B, C and `covmiss.c`).
- **Programs A and C** (B was not run on these failing cases):
  - $\mathrm{Cov}(13,8,46)$ fails at $K''=1$, missing $26$ residues out of $1.8\cdot10^{12}$;
  - $(13,8,45)$ fails at $K''=1$;
  - $\mathrm{Cov}(17,7,42)$ fails at $K'=6$. Program C finds $2$ missed residues; it found that $K'=6$ is the only failure among the classes $1,\dots,8$;
  - the block $(19,7,44)$ fails at exactly $7$ of the $18$ positions, $K''=1,5,9,11,12,14,16$.

**Minimal uniform $H_t$ [computer-assisted; minimality from exhaustive $H$-scans by program A, independently re-scanned by program C].** The least $H$ with $\mathrm{Cov}(p,t,H)$ is:

| $p$ | $t=1$ | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 7 | 4 | 7 | 19 | 26 | 28 | **34** | |
| 11 | 5 | 10 | 18 | 22 | 30 | 33 | |
| 13 | 6 | 10 | 19 | 24 | 32 | 35 | 39 |
| 17 | 5 | 11 | 16 | 25 | 30 | 34 | 43 |
| 19 | 5 | 12 | 17 | 27 | 31 | 35 | |
| 23 | 7 | 12 | 18 | 23 | 33 | 37 | |

- Every "holds" entry is certified by programs A and B, and again by program C.
- The failures of smaller $H$ come from exhaustive scans by program A (`data/round2/logs_original/R3/scan_p*.log`). Each was refuted either by the counting bound $2^H<p^{t+c}$ or by an exhaustive computation that found a missed residue.
- The round-2 computational referee re-scanned every entry with program C, testing every smaller $H$. It found the same minimal $H_t$ in all 38 cases. The round-2 novelty referee's own checker confirms the new value $H_6(7)=34$ separately: $\mathrm{Cov}(7,6,33)$ fails at $K'=5$ (2 residues mod $7^{10}$ missed), and $(7,6,34)$ covers that class. The round-2 logic referee's own checker confirms that $(7,6,34)$ holds over all 2058 classes and that $(7,6,33)$ fails at $K'=5$.
- At $p=13$ the values of §4.2 are exactly minimal. At $p=7$, §4.2's $H_6=35$ is not minimal.
- Coverage is **not monotone in $H$**. For example, at $p=13$, $t=2$, the lengths $H=10,\dots,13$ hold, $H=14,\dots,18$ fail and $H=19$ holds. The reason is that the target modulus $p^{t+c}$ jumps when $H-1$ passes a multiple of $p$, and Lemma 10.11(d) applies.
- Above the minimum, every failing $H$ in the scans has $(H-1)\bmod p<\rho_0(p)$.

### 10.3 The covering and renormalisation route: what fullness can and cannot propagate (track R2b)

**Theorem 10.12 (worst-case propagation) [proved; abstract core in Lean].** Let $D,D'\ge0$, $\delta\ge1$, and $\pi\in p^\delta\mathbb Z_p^\times$. Let $\Sigma\subset\mathbb Z_p$ be a finite set (the subset sums of a block or window). For $R\subseteq\mathbb Z_p$ put
$$T(R)=\{(x+s)/\pi:\ x\in R,\ s\in\Sigma,\ \pi\mid x+s\}.$$
Assume $D\le\delta+D'$. The following are equivalent:
- (i) $T(R)$ is full mod $p^{D'}$ (meets every class) for **every** $R$ that is full mod $p^D$;
- (ii) $\Sigma\bmod p^{\delta+D'}$ contains a complete coset $c+p^D\mathbb Z/p^{\delta+D'}\mathbb Z$.

*Proof.*
- (ii)⇒(i). Given a target $w$, choose $x\in R$ with $x\equiv\pi w-c\pmod{p^D}$. Then $\pi w-x\in c+p^D\mathbb Z$, so some $s\in\Sigma$ has $x+s\equiv\pi w\pmod{p^{\delta+D'}}$. Then $(x+s)/\pi\equiv w\pmod{p^{D'}}$.
- (i)⇒(ii). Suppose no coset $c+p^D\mathbb Z$ is contained in $\Sigma\bmod p^{\delta+D'}$. Take the target $w=0$.
  - For each class $\varrho\bmod p^D$, the class $-\varrho+p^D\mathbb Z$ is not contained in $\Sigma$. So there is a lift $x_\varrho\equiv\varrho\pmod{p^D}$ with $-x_\varrho\notin\Sigma\pmod{p^{\delta+D'}}$.
  - $R=\{x_\varrho\}$ is full mod $p^D$.
  - $0\in T(R)\bmod p^{D'}$ would require $x_\varrho+s\equiv0\pmod{p^{\delta+D'}}$ for some $\varrho$ and some $s\in\Sigma$, which is impossible. ∎

The abstract core is machine-checked: `worst_case_iff` in `code/round2/R2b/lean/Renorm.lean` (copied to `formal/Formal/E404R2b/Renorm.lean`). It says that for a subgroup $K$ of an abelian group $G$, a set $B$ and a nonempty target $T$, "$T\subseteq A+B$ for every $A$ meeting all $K$-cosets" holds iff $B$ contains a coset $c+K$. It uses only the standard axioms, with no `sorry`; this was re-compiled by the lead (§10.7).

**Corollary 10.13 (gate and window transparency) [proved].**
- (a) *Gates.* Let $D_p=\min\{D:p^D\ge e\,(p-1)!\}$; for example $D_{13}=9$. At a level-$j$ gate block, for every $D$ with $D_p\le D\le j$, there is a carry set that is full mod $p^D$ from which the gate block cannot cross.
- (b) *Windows.* For a window of length $H$ ending at $N^*=p^tK'$, and every $D$ with $e\,(H-1)!\le p^D$ and $D\le t-1$, there is a carry set at $N^*-H$ that is full mod $p^D$ from which the window cannot cross $N^*$.

*Proof.*
- (a) By the gate congruence (Theorem 3.9(b)), $\Sigma\equiv U\cdot\Sigma(E_p)\pmod{p^{j+1}}$ with $U$ a unit.
  - The values $V_S=(p-1)!\sum_{u\in S}(-1)^u/u!$ are integers in an interval of length $<e\,(p-1)!\le p^D$. So two of them congruent mod $p^D$ are equal.
  - Hence each class mod $p^D$ contains at most one residue of $\Sigma\bmod p^{j+1}$.
  - A full coset $c+p^D\mathbb Z/p^{\delta+D'}$, with $\delta=j+1$, would project to a full coset mod $p^{j+1}$, which needs $p^{j+1-D}\ge p$ residues in one class.
  - Apply Theorem 10.12 with $D'=0$: "full mod $p^0$" means nonempty.
- (b) Write $y_i\equiv\sigma_i\pmod{p^t}$ with $\sigma_i=(-1)^i(H-1)!/(H-1-i)!$ (§6). The integers $A_S=\sum_{i\in S}\sigma_i$ lie in an interval of length $<e\,(H-1)!\le p^D$.
  - So window sums in one class mod $p^D$ have the same $A_S$, and differ only by $X\,Q_S(X)$ with $X=p^tK'$ and $Q_S\in\mathbb Z[X]$. That leaves at most $p^c$ residues mod $p^{t+c}$.
  - A full coset needs $p^{t+c-D}>p^c$ residues, because $D<t$. ∎

*Consequence, and its limits.* Corollary 10.13 is about two kinds of block only. Part (a) concerns a single level-$j$ gate block entered with fullness mod $p^D$, $D_p\le D\le j$. Part (b) concerns a window of length $H$ entered with fullness mod $p^D$, $e(H-1)!\le p^D\le p^{t-1}$. For these, fullness information alone does not guarantee crossing, however much multiplicity is available in $\mathbb Z_p$. An inductive argument that works block by block, or with such windows, must therefore carry distributional (multiplicity or Fourier) information.

This does **not** refute the fullness-only form of the renormalisation lemma T3 of §6. T3 runs from a level-$(j-1)$ gate to the next level-$j$ gate, a stretch of about $p^j$ elements entered with fullness mod $p^j$. Its first block is a level-$(j-1)$ gate entered with $D=j>j-1$, so part (a) does not apply. Part (b) would need $e(H-1)!\le p^{t-1}$ with $H$ of order $p^j$, which is impossible. By Theorem 10.12, fullness-only T3 holds for a stretch iff the stretch's subset sums contain a complete coset of $p^j$ at the relevant modulus. Nothing in this note decides that. *(Round 2: the previous version said that fullness-only T3 "is false beyond level about $D_p$". Both the logic and the novelty referee pointed out that Corollary 10.13 does not prove this. The claim is withdrawn.)*

**Proposition 10.14 (monotonicity of $\mathrm{Cov}$ in $H$) [proved; recursion in Lean].** Write $y^{(H)}_i(X)=\prod_{s=1}^i(X-(H-s))$. Then $y^{(H+1)}_0=1$ and $y^{(H+1)}_{i+1}=(X-H)\,y^{(H)}_i$. Hence $\Sigma_{H+1}=\{0,1\}+(X-H)\Sigma_H$.
- (a) If $p\nmid H$, then $\mathrm{Cov}(p,t,H)\Rightarrow\mathrm{Cov}(p,t,H+1)$ (for $H+1\le p^t$). This is the $\mathrm{Cov}$-level form of Tao's step $P(a,p,N-1)\Rightarrow P(a,p,N)$ for $p\nmid N$ (Lemma 1.3(iv)), and we credit it to Tao.
- (b) If $1\le v_p(H)\le L_p$ and $H+p<p^t$, then $\mathrm{Cov}(p,t,H)\Rightarrow\mathrm{Cov}(p,t,H+p)$.

*Proof.*
- The recursion is direct. In Lean it is `window_succ`, together with `cover_extend`: if the subset sums of $L$ cover a ring and $u$ is a unit, then the subset sums of $1::uL$ cover it.
- (a) $c(H+1)=v_p(H!)=c(H)$, so the classes $K'$ are the same. $X-H$ is a unit, so $\Sigma_{H+1}\supseteq(X-H)\Sigma_H$, which is everything.
- (b) Iterating $p$ times gives $y^{(H+p)}_{i+p}=\Pi\,y^{(H)}_i$, with $\Pi=\prod_{h=H}^{H+p-1}(X-h)$. So $\Sigma_{H+p}=B+\Pi\,\Sigma_H$, where $B$ is the set of subset sums of $y^{(H+p)}_0,\dots,y^{(H+p)}_{p-1}$.
  - Since $H+p-1<p^t$, the only multiple of $p$ among $H,\dots,H+p-1$ is $H$. So $v_p(\Pi)=v_p(H)$ and $c(H+p)=c(H)+v_p(H)$.
  - The elements of $B$ are units, and modulo $p^{v_p(H)}$ (where $X\equiv H\equiv0$) they are $\prod_{s\le i}(s-p)=(p-1)!(-1)^u/u!$. So $B\equiv(p-1)!\,\Sigma(E_p)\pmod{p^{v_p(H)}}$, which covers $\mathbb Z/p^{v_p(H)}$ because $v_p(H)\le L_p$.
  - Given a target $T$, pick $b\in B$ with $b\equiv T\pmod{p^{v_p(H)}}$. By $\mathrm{Cov}(p,t,H)$, applied to $K'\bmod p^{c(H)}$ (still a unit), pick $\sigma\in\Sigma_H$ with $\sigma\equiv(T-b)/\Pi\pmod{p^{t+c(H)}}$. Then $b+\Pi\sigma\equiv T\pmod{p^{t+c(H+p)}}$. ∎

*Example.* The certified $\mathrm{Cov}(7,3,19)$ gives $\mathrm{Cov}(7,3,H)$ for $H=19,20,21$, and then for every $H=21+7k\le336$, including $H=49$.

*Remark (UC′).* The proof of Theorem 3.12(c) only needs, for each first-failure candidate $N^*=p^tK''$, **some** covering window length $H<p^t-1$, which may depend on $K''$. This is formally weaker than $\mathrm{UC}(p)$, and it is the form used in Proposition 10.10.

**Proposition 10.15 (windows of length $p^D$) [proved].**
- (i) For $H=p^D$ with $D<t$ and $X=p^tK'$: $v_p(y_i(X))=v_p(i!)$ for all $i<H$. So the window $[N^*-p^D,N^*)$ has exactly the valuation profile of $0!,\dots,(p^D-1)!$.
- (ii) *Block identity.* For $H=pH'$:
$$y^{(pH')}_{pq+r}(X)=p^q\,y^{(H')}_q(X/p)\,U_q(X)\prod_{s=pq+1}^{pq+r}(X-pH'+s),$$
  where $U_q(X)=\prod_{s\le pq,\,p\nmid s}(X-pH'+s)$ is a unit and $U_q(X)\equiv U_q(0)\pmod{p^t}$.
- (iii) *Twist-free criterion.* Write $y_i\equiv\sigma_i+X\tau_i\pmod{X^2}$ with $\sigma_i,\tau_i\in\mathbb Z$, and suppose $t\ge c$. If every $T\in\mathbb Z/p^{t+c}$ is congruent to $\sum_S\sigma_i$ for some $S$ with $\sum_S\tau_i\equiv0\pmod{p^c}$, then the window covers for **every** $K'$, unit or not.

*Proof.*
- (i) For $s\le i<p^D<p^t$, $v_p(X-(p^D-s))=v_p(p^D-s)=v_p(s)$.
- (ii) Among the factors $s=1,\dots,pq$, separate the multiples $s=ps'$: their product is $p^q\prod_{s'\le q}(X/p-(H'-s'))$. The other factors are $\equiv s\not\equiv0\pmod p$.
- (iii) The terms of order $X^2$ vanish mod $p^{2t}$, and $p^{t+c}\mid p^{2t}$. Then $\sum_Sy_i\equiv T+X\cdot p^c(\cdots)\equiv T\pmod{p^{t+c}}$. ∎

Track R2b's 2D tester `twofree.c` reproduces the known results $\mathrm{Cov}(5,2,10)$, $(5,3,20)$, $(7,3,19)$ and $(7,2,7)$ with `cov.c`. At those $H$ the stronger criterion (iii) fails: numerically it needs $H$ about twice as large. So (iii) gives no new certificates.

**Theorem 10.16 (conditional reduction of Q3 to a random-model Fourier bound) [proved; the hypothesis is unproved].**

*Definitions.*
- $U_d=\min\{i:v_p(i!)\ge d\}$, and $n_d(H)=\#\{i<H:v_p(i!)<d\}$.
- The random-model budget:
$$\Lambda_p=\sum_{d\ge1}(p^d-p^{d-1})(2/\pi)^{U_d},\qquad\tau_p(t)=p^{t+c}(2/\pi)^{p^{t-1}},\quad c=v_p((p^{t-1}-1)!).$$
- *Hypothesis $\mathrm{RMF}(p,C)$:* for every $t\ge3$ and every unit $K'\bmod p^c$, the window of length $H=p^{t-1}$ ending at $p^tK'$ satisfies
$$\sum_{\xi\ne0}\prod_{i<H}|\cos(\pi\xi y_i)|\ \le\ C\sum_d(p^d-p^{d-1})(2/\pi)^{n_d(H)}.$$

*Statement.* If $C\,(\Lambda_p+\tau_p(3))<1$, and $\mathrm{Cov}(p,1,\cdot)$ and $\mathrm{Cov}(p,2,\cdot)$ hold with $H_t+1<p^t$, then $\mathrm{UC}(p)$ holds. Consequently $f(1,p)=\infty$, and **Q3 has a positive answer**.

*Proof.*
- By Proposition 10.15(i), $v_p(y_i)=v_p(i!)$. So at a frequency $\xi$ of exact order $p^d$, only the $n_d(H)$ elements with $v_p(i!)<d$ give factors $\ne1$.
- The right-hand side is at most $\Lambda_p+\tau_p(t)$:
  - for $d\le c$, $n_d=U_d$;
  - for $c<d\le t+c$, $n_d=H$, and $\sum_{d=c+1}^{t+c}(p^d-p^{d-1})\le p^{t+c}$.
- $\tau_p(t+1)/\tau_p(t)=\big(p(2/\pi)^{p-1}\big)^{p^{t-1}}<1$ for $p\ge5$. Indeed $c(t+1)-c(t)=p^{t-1}-1$, so $\tau_p(t)\le\tau_p(3)$ for $t\ge3$.
- So the left side is $<1$, and Fourier inversion (Proposition 3.13(b)) gives that every class mod $p^{t+c}$ is a subset sum, i.e. $\mathrm{Cov}(p,t,p^{t-1})$.
- Since $p^{t-1}+1<p^t$, Theorem 3.12(c) applies. ∎

*Constants.* Recomputed by the lead with `lambda_p.py` and `rmf_budget.py` (§10.7, row S10):

| $p$ | 5 | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|---|
| $\Lambda_p$ | 1.2436 | 0.3632 | 0.07538 | 0.03514 | 0.007473 | 0.003393 | 0.000679 |

So the hypothesis with $C<2.68$ suffices at $p=7$ (where $\tau_7(3)\approx0.0099$). The allowed $C$ is about $13$ at $p=11$ and about $28$ at $p=13$, and it grows like $(\pi/2)^{p-1}/p$. Since $\Lambda_5>1$, this $L^1$ route cannot work at $p=5$ even if the true sums behave exactly like the random model.

Theorem 10.16 is a quantitative form of Proposition 3.13(b) and of the heuristic H2. Its content is the explicit budget. **RMF itself is unproved at every unbounded family of depths** (§10.5).

### 10.4 The Fourier route (track R2a)

Let $N_0=p$ and $x'_n=n!/p^{e_0}$ with $e_0=v_p(N_0!)$. The uniform-coin tail measure has Fourier shell sums
$$T_p(k)=\sum_{u\in(\mathbb Z/p^k)^\times}\ \prod_{n\ge p}\big|\cos\big(\pi u\,x'_n/p^{k}\big)\big|,$$
the $L^1$ mass at frequencies of exact order $p^k$. Only factors with $v_p(x'_n)<k$ differ from $1$.

**10.4.1 Certified shell sums [computer-assisted; floating point with outward margins, plus interval arithmetic for the dominant shells].**

| | $k=1$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | $\sum$ |
|---|---|---|---|---|---|---|---|---|---|
| $T_{13}(k)\le$ | 7.7953e-3 | 1.4998e-3 | 3.7507e-6 | 1.0363e-7 | 8.8918e-9 | 1.1655e-9 | 6.0008e-12 | | 9.2988e-3 ($k\le7$) |
| $T_{11}(k)\le$ | 6.0370e-2 | 6.1829e-3 | 2.6997e-4 | 2.2438e-5 | 9.9521e-6 | 1.2004e-7 | 3.3200e-8 | 3.2387e-9 | 6.6855e-2 ($k\le8$) |

*Method.*
- Track R2a's `fl1.c` enumerates every unit frequency by depth-first search over $p$-adic digits, with exact 128-bit residues and no pruning. Each factor is replaced by $\min(1,\cos+10^{-13})$, and the total is multiplied by $1+10^{-9}$.
- The lead wrote an independent implementation, `fl1_lead.c`. It uses full residues $x'_n\bmod p^k$, `__cospi`, balanced tree summation, a margin of $10^{-12}$ per factor and a final factor $1+10^{-10}$.
- The lead also evaluated the dominant shells ($k\le4$ at $p=13$, $k\le5$ at $p=11$) in outward-rounded interval arithmetic (`iv_shells.py`, mpmath `iv`).

The three agree to at least 7 significant digits (§10.7, row S8). Each entry is the largest of the upper bounds, rounded up in the last digit. Shells $k\ge5$ (respectively $k\ge6$) rest on floating point with margins, not interval arithmetic. Their total is below $1.1\cdot10^{-8}$ (respectively $2\cdot10^{-7}$), far from any threshold.

**Corollary 10.17 (quantitative equidistribution) [computer-assisted].** For $K\le7$ ($p=13$) and $K\le8$ ($p=11$), every class $y\in p\mathbb Z/p^{K+1}$ is hit by exactly $2^{pK}p^{-K}(1+\theta_y)$ subsets $B\subseteq[p,p(K+1))$ with $\sum_{n\in B}n!\equiv y$. Here $|\theta_y|\le0.0093$ for $p=13$ and $|\theta_y|\le0.0669$ for $p=11$.

*Proof.* Fourier inversion on $p\mathbb Z/p^{K+1}\cong\mathbb Z/p^K$ gives $|\theta_y|\le\sum_{k\le K}T_p(k)$. Elements $n\ge p(K+1)$ have $v_p(n!)\ge K+1$ and contribute factor $1$. ∎

**Theorem 10.18 (hybrid exact-vanishing reduction at $p=13$) [proved, given the certificates of §4.2].** (Track R2a.)

*Construction.*
- At each multiple $N^*\ge26$ of $13$, with $t=v_{13}(N^*)$, put a window $W(N^*)=[N^*-H_t,N^*)$. Use $H_t=6,10,19,24,32,35,39$ for $t\le7$ (the certified $\mathrm{Cov}(13,t,H_t)$), and $H_t=13$ for $t\ge8$.
- Drop the windows at $N^*-13$ and $N^*-26$ whenever they would overlap a window with $t\ge3$.
- The kept windows are disjoint. The levels a kept window owns, $[v((N^*-H)!)-1,\ v(N^*!)-1)$, partition $\mathbb Z_{\ge0}$.
- Give each window with $t\le7$ a probability measure on its subsets whose normalised sum is exactly uniform mod $13^{t+c}$. Such a measure exists by $\mathrm{Cov}(13,t,H_t)$: pick one covering subset for each residue.
- Give every other element $n\ge13$ an independent fair coin.

*Statement.* Then $\hat\nu(\xi)=0$ at every frequency $\xi$ of order $13^k$ whose level $k-1$ is owned by a window with $t\le7$; in particular this holds for every $k\le67\,977\,551$. Consequently, if
$$\sum_{N^*:\,v_{13}(N^*)\ge8}\ \ \sum_{k-1\in\mathrm{Own}(N^*)}\ \ \sum_{\mathrm{ord}(\xi)=13^k}|\hat\nu(\xi)|<1,$$
then $E_{13}=13\mathbb Z_{13}$. Hence $f(1,13)=\infty$, and Q3 has a positive answer.

*Proof.*
- *Ownership tiling.* Between consecutive kept window ends $N_1<N_2$, every multiple of $13$ lies in $(N_2-H,N_2)$. Hence $v((N_2-H)!)=v(N_1!)$. This was checked case by case for $H_t\in\{6,10,19,24,32,35,39,13\}$. The dropped windows end at points of valuation $1$. The first window, at $26$, owns level $0$.
- *Vanishing.* Suppose $W$ owns level $k-1$, and let $V_W=v((N^*-H)!)-1$. The window contributes $13^{V_W}U\cdot Z_W$, with $U$ a unit and $Z_W$ uniform mod $13^{D_W}$, where $D_W=t+c$.
  - The frequency it sees, $\xi\,13^{V_W}U$, has order $13^{k-V_W}$ with $1\le k-V_W\le D_W$.
  - So $\mathbb E\,e(\xi13^{V_W}UZ_W)=0$, and the full Fourier coefficient, a product over independent components, vanishes.
- *The first uncertified window.* It ends at $N^*=13^8$ and owns the levels $[v((13^8-13)!)-1,\ v(13^8!)-1)=[67\,977\,551,\ 67\,977\,559)$.
- *Conclusion.* Fourier inversion (Proposition 3.13(b)) applied mod every $13^K$, together with compactness, gives $E_{13}=13\mathbb Z_{13}$. Then $1!+12!\equiv0\pmod{13}$ and Lemma 1.4(a) give $f(1,13)=\infty$. ∎

This is a reformulation, not progress on the deep problem. It replaces node-level $\mathrm{UC}(13)$ at depths $t\ge8$ by a population-level Fourier condition on deep-gate shells only.

**Proposition 10.19 (renormalisation identity) [proved].** (Track R2a.)

*Set-up.*
- Let $N_W$ be the first $n$ with $v(n!)-v(N_0!)\ge W$. **Assume that $W$ is attained**, i.e. $v(N_W!/N_0!)=W$ exactly, and write $N_W!/N_0!=p^Wa$ with $a$ a $p$-adic unit.
- Let $G(\theta)=\prod_{N_0\le n<N_W}|\cos(\pi\theta x'_n)|$, where here $x'_n=n!/N_0!$.
- Let $H_W(\theta)=\sum_{s\bmod p^W}G(\theta+s/p^W)$, which has period $p^{-W}$.

The hypothesis matters. Valuations jump by more than $1$ at multiples of $p^2$, so some $W$ are skipped. For example, with $N_0=p$ and $W=p-1$ one gets $N_W=p^2$ and $v(N_W!/N_0!)=p$. Then $a$ is not a unit, $a^{-1}$ does not exist mod $p^{k-W}$, and the top frequencies $wa/p^{k-W}$ have order $p^{k-W-1}$, so the identity below fails as written. The cases checked numerically ($N_0=p$, $W=1,2$) are attained. *(Round 2: hypothesis added after the logic referee; the previous version omitted it.)*

*Statement.* For $k>W$, with $W$ attained,
$$T_{N_0}(k)=\sum_{w\in(\mathbb Z/p^{k-W})^\times}\big|\hat\nu_{N_W}(w/p^{k-W})\big|\cdot H_W\!\Big(\frac{(wa^{-1}\bmod p^{k-W})}{p^k}\Big),$$
where $\hat\nu_{N_W}$ is the Fourier transform of the tail measure from $N_W$ normalised by $N_W!$. Consequently
$$(\min H_W)\,T_{N_W}(k-W)\le T_{N_0}(k)\le(\max H_W)\,T_{N_W}(k-W).$$
In addition:
- $H_W(0)=1+(\text{the }L^1\text{ mass of the bottom }W\text{ levels})\ge1$;
- the mean of $H_W$ over a period is $p^W\int_0^1G$.
- *[Heuristic, not part of the proposition]* That mean should be close to $(p(2/\pi)^p)^W$, as it would be if the factors of $G$ were independent.

*Proof.*
- Write $u=w+p^{k-W}s$, with $w\bmod p^{k-W}$ and $s\bmod p^W$; $u$ is a unit iff $w$ is.
- For $n\ge N_W$, $x'_n=p^Wa\cdot n!/N_W!$. So $s$ drops out of the top factors, which become $|\hat\nu_{N_W}(wa/p^{k-W})|$.
- Summing the bottom factors over $s$ gives $H_W(w/p^k)$.
- Reindex $w\mapsto wa^{-1}$; this uses that $a$ is a unit, i.e. that $W$ is attained. The argument of $H_W$ is well defined modulo its period $p^{-W}$. ∎

Track R2a checked the identity to a relative error $\le6\cdot10^{-14}$ with exact integer residues (`renorm_check.py`: $p=13$, $W=1$, $k=3,4$ and $W=2$, $k=4$; $p=11$, $W=1$, $k=4$ and $W=2$, $k=4,5$). The lead re-ran it (§10.7, row S9). At $p=13$, $W=1$, $H_1(0)=1.007795=1+T_{13}(1)$. The exact period mean is $13\int_0^1G=0.0366754$, against the heuristic $13(2/\pi)^{13}=0.0366763$. It was computed by the round-2 computational referee with a factorial-digit transfer recursion, and reproduced by the lead (converged on grids of $2^{14}$ to $2^{20}$ points). *(Round 2 correction: the previous version quoted "mean $0.03678$". That number is the average over the finite sample grid printed by `renorm_check.py`, not the period mean.)*

**Corollary 10.20 (limits of sup-type renormalisation) [proved].** For every attained $W$ (Proposition 10.19), $\sup_wH_W(w/p^k)\ge H_W(1/p^k)\to H_W(0)\ge1$ as $k\to\infty$, by continuity of $G$. Hence a bound of the form $T_{N_0}(k)\le(\sup H_W)\,T_{N_W}(k-W)$, iterated, cannot give geometric decay of $T(k)$. *[Heuristic, not part of the corollary:]* the true average gain per level should be about $p(2/\pi)^p$, about $1/27$ at $p=13$.

The obstruction is archimedean: $G$ has resonances at real frequencies near $0$, and near $1/(n!/N_0!)$, where $H_W\approx0.98$ numerically. So any proof of $\sum_kT(k)<1$ along these lines must show that the top-level Fourier weights *decorrelate* from the bottom profile $H_W$. This makes precise the remark in §6 that track B's sup-over-phase constant is $\ge1$. We do not claim that every conceivable method fails, only bounds that take a supremum over the bottom profile.

**Proposition 10.21 (factorial-base digit formula) [proved].** (Track R2a.) Write $\theta=u/p^k=\sum_{n>N_0}d_n\,N_0!/n!$ with $0\le d_n\le n-1$. This expansion terminates, because $u/p^k$ has denominator dividing $N!/N_0!$ for large $N$. Then
$$|\hat\nu(u/p^k)|=\prod_{m\ge N_0}|\cos(\pi\tau_m)|,\qquad\tau_m=\sum_{n>m}d_n\,\frac{m!}{n!}\in\Big[\frac{d_{m+1}}{m+1},\frac{d_{m+1}+1}{m+1}\Big),\qquad\tau_m=\frac{d_{m+1}+\tau_{m+1}}{m+1}.$$

*Proof.* $\theta\,m!/N_0!=(\text{integer})+\sum_{n>m}d_nm!/n!$, and the tail is $<1$ by telescoping. ∎

So a Fourier coefficient is large only if most factorial-base digits of the $p$-adic rational $u/p^k$ are extreme, near $0$ or near $m$. The $L^1$ criterion is thus an averaged digit-distribution statement for rationals with $p$-power denominators in the factorial number system. Nothing currently controls the middle digits.

### 10.5 Conjectures and heuristics from round 2 (none of this is proved)

**Conjecture 10.22 (missing inequality MI-13) [conjecture].**
$$\sum_{k\ge8}T_{13}(k)<1-0.0092988=0.99070.$$
By §10.4.1 and Proposition 3.13(b), MI-13 would give $E_{13}=13\mathbb Z_{13}$. Hence $f(1,13)=\infty$ (and $f(a,13)=\infty$ for every $a<13$ with $P(a,13,13)$), and **Q3 = YES**. By Theorem 10.18, it would suffice to bound only the deep-gate shells, all of which have $k\ge67\,977\,552$. The $p=11$ analogue is $\sum_{k\ge9}T_{11}(k)<0.93314$.

*Evidence [heuristic; Monte Carlo].* Track R2a used Knuth's unbiased tree estimator with importance sampling (`knuth.c`, `knuth_big.py`, validated against the exact values for $k\le7$). It found:
- *Decay.* $T_{13}(k)$ decays by about $10^{-1.39}$ per shell. The median $\log_{10}T_{13}(k)$ is about $-28$ at $k=20$, $-112$ at $k=80$, and about $-250$ at the level-2 gate shells $k=181,182$. At $p=11$ the decay is about $10^{-1.02}$ per shell.
- *Gate shells.* The mean jumps by a factor of $10$–$150$ at the gate shells ($k=13,27,41,181,182$ for $p=13$).
- *Estimated tails.* The tail sums are about $3\cdot10^{-13}$ ($p=13$) and $4\cdot10^{-10}$ ($p=11$).

At $k\ge120$ the estimator is heavy-tailed, so only orders of magnitude mean anything. These are estimates, not certificates. The structural obstruction is Corollary 10.20: decorrelation between the archimedean bottom levels and the $p$-adic top levels.

**Conjecture 10.23 ($\mathrm{RMF}$ with a bounded constant) [conjecture].** $\mathrm{RMF}(p,C)$ of Theorem 10.16 holds for $p=7,11,13$ with $C\approx1.3$. By Theorem 10.16 this would give $f(1,p)=\infty$ for these $p$, and hence Q3 = YES.

*Evidence [heuristic; double-precision diagnostics of track R2b, `fwin2.c`; not certificates].*
- *Range of tests.* 31 runs ($p=5,7,11,13,17$): windows $H=2p,\dots,4p$ at depths $t\le5$; full stretches $H=p^{t-1}$ at $(7,3)$ and $(5,3)$; and single gate blocks up to level $9$.
- *Aggregate ratio.* $L^1/(\text{random-model budget})$ lies in $[0.40,1.30]$ in every run.
- *Single gate blocks.* The per-level ratio settles at about $1.17$ for every $p$ tested, with no visible growth in depth.
- *Full stretch $(7,3,49)$.* $L^1\approx0.29$–$0.30$ for $K'=1,2,17$, against the budget $0.371$.

*Caveat.* The windows needed by Theorem 10.16 grow with $t$. Equidistribution of a *fixed* finite set of rationals (single gate blocks) does not cover them. RMF at unbounded depth needs control of deep $p$-adic digits of factorial unit parts, i.e. of Morita's $\Gamma_p$, as the barrier lemma (Theorem 3.10) already indicates. Even level $d=1$ of RMF, taken uniformly in $p$, is a non-concentration statement for $\{r!\bmod p\}$ that we did not find in the literature. (Garaev–Luca–Shparlinski and Klurman–Munsch treat related questions; this is a limited search, to be checked by a specialist.)

**Conjecture 10.24 (bottleneck threshold law) [heuristic; fitted to data].** (Track R3.) Let $m_k(r)$ be the number of subsets of the elements of valuation $<k$ whose sum is $\equiv r\pmod{p^k}$. This is exact and $K'$-independent for $k\le t$. Define
$$R^*=\min_{k\le\min(c,t)}\Big[\min_rm_k(r)\Big]\cdot2^{\#\{\text{elements of valuation}\ge k\}}/p^{M-k},\qquad\nu=R^*/\ln(n\,p^M),$$
where $n$ is the number of classes or positions tested.

*Conjecture.* $\mathrm{Cov}$ holds on the tested set when $\nu\gtrsim1.5$, and fails when $\nu\lesssim1.17$.

*Evidence.*
- *Observations.* Over 351 observations ($p=5$–$23$, $t=3$–$8$): all 115 cases with $\nu<1.17$ fail, all 228 with $\nu>1.47$ hold, and the 8 cases in between are mixed.
- *Registered predictions.* The registration file is `data/round2/logs_original/R3/PREDICTIONS_registered.txt`; its internal timestamp is 2026-10-11 22:45:31 and its file time 22:55:47. Six outcomes were confirmed, but they do not all count as out-of-sample tests:
  - **Genuine out-of-sample tests of the thresholds (3):** $(17,7,42)$ fails ($\nu=1.03$), $(19,7,44)$ fails ($\nu=1.10$) and $(23,7,43)$ holds ($\nu=3.99$). Each was registered, and each was run only after registration.
  - **Registered and confirmed, but not a test of the thresholds (1):** $(7,8,46)$ holds. Its $\nu=1.287$ lies inside the law's own mixed band $[1.17,1.47]$.
  - **Registered, but partly known in advance (1):** uniform $(17,7,43)$ holds ($\nu=2.22$). The uniform 272-class run came after registration. But the depth-7 position results at the same $H$ had already been logged, at 22:35 (program A) and 22:41 (program B).
  - **Not registered (1):** $(17,8,47)$ holds. The registration file has no $p=17$, $t=8$ row.

  *(Round 2 correction after the novelty referee: the previous version said that six predictions were registered before the runs.)*
- *The $p=5$ anomaly.* The law explains it: $R^*$ drops to about $27$ at levels 3–5.

*Predictions.*
- At $p=13$, $H_t=47,51,58,62,71$ for $t=8,\dots,12$.
- Uniform $\mathrm{Cov}(13,8,47)$ and $\mathrm{Cov}(5,5,39)$ hold. Only $104$ of the $312\,500$ classes of $(5,5,39)$ were checked, all covered.

**Conjecture 10.25 (hardest carries) [heuristic].** (Track R3.) A residue $x$ is missed with probability about $C\exp(-\gamma R_1(x\bmod p))$, with $\gamma\approx0.76$–$0.81$, where $R_1(r)=m_1(r)2^{|U_1|}/p^{M-1}$.

*Evidence.* The missed residues concentrate in $\arg\min_rm_1(r)$:
- 26/26 at $(13,8,46,1)$, 2/2 at $(11,7,40,37)$ and 16/16 at $(11,5,29)$;
- 1880/1890 at $(7,6,33)$.

Fits of $\log(\text{misses})$ against $R_1$ have correlation $-0.997$ (`logs_original/miss_vs_m1_fit.txt`).

**Conjecture 10.26 (growth of $H_t$; design rule) [heuristic].** (Track R3.)
- $H^{\min}_t=s_p\,t+O(\log t)$ with $s_p=\log_2p/(1-\log_2p/(p-1))\approx5.3$–$5.6$ for $p\ge5$; the observed slopes are $5.6$–$6$ for $t\le8$.
- Block lengths with $H\equiv0\pmod p$ avoid the digit-0 bottleneck of Lemma 10.11.
- $\mathrm{UC}(p)$ should hold for every $p\ge7$, and plausibly for $p=5$ with $H_5=39$.

This strengthens the evidence for Conjecture 5.3, but it is only a counting heuristic.

### 10.6 Status of Q1–Q3 after round 2, and what remains

**Status line (2026-10-12).**
- **Q1 (for which $a,p$ is $f(a,p)$ finite?)** Still open in general.
  - *New at $p=2$:* $f(a,2)<\infty$ for a set of $a$ of natural density $1$ (Theorem 10.1; AI-refereed, not human-refereed). Kitamura's data had anticipated this empirically (§2). Whether $f(a,2)<\infty$ for *every* $a$ is open; $a=594$ remains a live test case.
  - *Odd $p$:* finiteness is known only on explicit residue classes (§§3.2, 4.7). No $a$ is known with $f(a,p)=\infty$ for any $p$.
- **Q2 (behaviour):** partial results only.
  - New certified lower bounds: $f(1,p)\ge883\,708\,272$ at $p=13$ and $\ge7.4\cdot10^9$ at $p=17$, among others (§10.2). The $p=17$ bound rests on programs A and C, both re-run, and on program B's original logs.
  - The density-one finiteness at $p=2$.
  - Structural facts (§§3, 10.3–10.4).
- **Q3 (is there $p$ and an infinite sequence with $v_p$ of the partial sums $\to\infty$?)** **OPEN.** Each of the following would suffice. None is proved, and none is known to be necessary:
  - $\mathrm{UC}(p)$ (Theorem 3.12(c));
  - a random-model Fourier bound (Theorem 10.16);
  - a deep-gate Fourier $L^1$ bound (Theorem 10.18, Conjecture 10.22).

**What remains, precisely.**
1. *For Q3 (covering route):* prove Missing Lemma ML of §6, for all $t\ge8$ at $p=13$. At $t=8$ it is now certified at the 12 positions below $13^9$, but not uniformly in $K'$. By the Remark (UC′) after Proposition 10.14, per-position covering at every depth would also suffice. Corollary 10.13 shows that fullness information alone cannot carry a single gate block or a short window. Whether it can carry a whole gate-to-gate stretch is the full-coset question of Theorem 10.12, which is open. The most concrete open sub-problem is RMF at deep levels for windows of length $p^{t-1}$ (Theorem 10.16). A first, insufficient step would be a rigorous version for single gate blocks, by Weyl–Kronecker equidistribution plus a finite check.
2. *For Q3 (Fourier route):* bound the deep-gate shells of Theorem 10.18. Equivalently, show that the top-level Fourier weights decorrelate from the bottom profile $H_W$ (Corollary 10.20). A cheaper intermediate target is the $L^2$ analogue, which would give positive Haar measure of the tail set.
3. *For Q1 at $p=2$:* a rate for $\delta_G(2)$. Theorem 10.1 is qualitative. Claim 10.9 is unverified, and even if true it gives no rate for $\delta_G(2)$ itself, because of its $1/16$ floor. Deciding whether $K_2\cap\mathbb N=\emptyset$ needs a different idea: measure-theoretic arguments cannot see a countable set.
4. *Odd $p$, measure:* an $L^2$ bound for the odd-$p$ analogue of the martingale of §10.1 would give $\mu(K_p)>0$ (Conjecture 5.2). It was not attempted.
5. *Computation (feasible):*
   - uniform $\mathrm{Cov}(13,8,47)$, about $170$ core-hours per program, predicted to hold;
   - $\mathrm{Cov}(5,5,39)$;
   - depth-7 positions at $p=29,31$;
   - $p=19$ depth 8;
   - an interval-arithmetic re-run of all certified shell sums.

### 10.7 Reproduction (round 2)

*Layout.* In the repository, round-2 code is under `code/round2/` and round-2 logs and data are under `data/round2/`:

| dir | origin | contents |
|---|---|---|
| `code/round2/R1b/` | track R1b | `muK2_proof.tex` (the track's write-up of Theorem 10.1); `mart_check2.py`, `brute_window.py`, `negctrl.py`, `lemmaB_check.py`, `rho_table.py`, `lam_stats.py`, `sim_mart.py` |
| `code/round2/R1a/` | track R1a | `code/` (`class_check.py`, `I8.py`, conservation and $T_m$ tests, `pop.c`), `explore/` |
| `code/round2/R2a/` | track R2a, plus the lead | `fl1.c`, `knuth.c`, `knuth_big.py`, `renorm_check.py`, `rho.c` (R2a); `fl1_lead.c` and `iv_shells.py` (the lead's independent checks) |
| `code/round2/R2b/` | track R2b | `src/` (`fwin2.c`, `twofree.c`, `lambda_p.py`, `rmf_budget.py`, …), `lean/Renorm.lean` |
| `code/round2/R3/` | track R3 | `src/fibcov.c` (program A), `src/fibcov2.c` (program B), `brute.py`, `validate.py`, `chain.py`, scans and law scripts; `specs/`; `data/` (position lists and job lists) |
| `code/round2/` | the lead | `lead_checks.py`, `lead_window_check.py`, `lead_hmean.py` (period mean of $H_1$, added in the referee revision), `run_lead_batch.sh` |
| `code/round2/review/` | round-2 referees | `logic/` (`covmiss.c`, `p2_window.py`, `lam_probe.py`, …), `computation/` (program C `covchk.c`, `shells.c`, `chain_c.py`, `p2_window.py`, `equidist_dp.py`, `thm1012_brute.py`, …), `novelty/` (`covchk.c`, `brute.py`) |
| `data/round2/logs_original/` | tracks, 2026-10-11 | the original logs of each track (`R1a/`, `R1b/`, `R2a/`, `R2b/`, `R3/`), including both programs' certificates and `PREDICTIONS_registered.txt` |
| `data/round2/R1a_explore/` | track R1a | data files written by `code/round2/R1a/explore/` |
| `data/round2/outputs/` | the lead, 2026-10-12 | every re-run log cited below (rows S1–S13, C1–C6) |
| `data/round2/review/` | round-2 referees, 2026-10-12 | the referees' logs; one large log is gzipped |

In the working session the same material lived under `code_r2/`. The scripts still use that relative layout, so their fresh outputs go to `code/round2/outputs/`. Path-only edit: absolute local paths in `data/round2/outputs/lead_batch_times.log` were replaced by `<code_r2>` and `<FORMAL_DIR>`.

*Build* (from `code/round2/`).
- `clang -O3 -march=native -o R3/bin/fibcov R3/src/fibcov.c`
- `clang -O3 -march=native -o R3/bin/fibcov2 R3/src/fibcov2.c`
- `clang -O3 -o R2a/bin/fl1 R2a/fl1.c -lm -lpthread`
- `clang -O3 -o R2a/bin/fl1_lead R2a/fl1_lead.c -lm`

The source hashes of `fibcov.c` and `fibcov2.c` equal those recorded by track R3 (`data/round2/logs_original/R3/binary_hashes.txt`). Python 3.9 with `mpmath` 1.3.0; Lean 4 v4.34.1 + Mathlib.

*Commands.*
- Rows S1–S13 are run by `sh code/round2/run_lead_batch.sh FORMAL_DIR` (one core).
- Rows C1–C6 use the job list `data/round2/outputs/R3/rerun_jobs_list.txt`. Copy it to `code/round2/R3/data/rerun_jobs.txt`, create `code/round2/outputs/R3/`, and start two or three workers with `sh src/rerun_worker.sh wN` from `code/round2/R3`.
- Then run `R3_LOGS=../outputs/R3 python3 src/chain.py specs/pXX.txt` from `code/round2/R3`. To check the archived logs instead, point `R3_LOGS` at `data/round2/outputs/R3`.

All re-runs were done on 2026-10-12 with at most 3 cores; no single run exceeded 50 minutes.

| # | what | result (2026-10-12) | wall |
|---|---|---|---|
| S1 | window identity, Prop. 10.6 (`mart_check2.py`; windows $(30,36)$, $(50,58)$, $(70,77)$; new seeds) | $257/257$, $70/70$, $187/187$ parents exact (514 in total); slope inheritance, constancy on the cylinder and state equidistribution all hold; slopes seen $1,3,4,5,7$ | 1.5 min |
| S2 | brute-force window identity (`brute_window.py`) | $(24,30)$: $109/109$ exact. $(32,39)$: $90/90$ exact (run with $D\le6$; a first attempt with $D\le8$ was stopped after 21 min while it was still inside its second instance, by which point it had $1/1$ exact; its partial log is kept as `S2_brute_32_39_killed_DMAX8.log`) | 10 s + 21 min (stopped) |
| S3 | negative control (`negctrl.py`) | 162 parents with $\lambda\ge2$; with $\rho:=1$ the identity fails on 133 | 10 min |
| S4 | deterministic part of Prop. 10.7 (`lemmaB_check.py`) | 30 instances, 360 $w$-samples: 0 changes of the child set, 0 violations of the level bound | 4 s |
| S5 | frozen-state weights (`rho_table.py`) | as stated in §10.1; e.g. $\lambda=3$, $x+n\equiv7\pmod8$: $(4,4,0,\dots,0)$ | <1 s |
| S6 | R1a class check behind Claim 10.9 (`class_check.py`, $R=10,12$) | $\kappa\in\{1\},\{3\},\{3\}$, no unstable path; $I=0.0625,0.125,0.125$ (reproduces R1a; see the caveat in §10.1.4) | 4 s |
| S7 | R1a initial weight `I8.py` | $I_8(C_0)=0.0625$ at $R=6,9$ | 1 s |
| S8 | certified shell sums (§10.4.1) | `fl1` reproduces R2a's table digit for digit. `fl1_lead` (independent) agrees to $\ge7$ digits: $\sum_{k\le7}T_{13}\le9.2987858\cdot10^{-3}$, $\sum_{k\le8}T_{11}\le6.6854497\cdot10^{-2}$. Interval arithmetic (`iv_shells.py`): $\sum_{k\le4}T_{13}\le9.2987757\cdot10^{-3}$ and $\sum_{k\le5}T_{11}\le6.6854340\cdot10^{-2}$, with interval widths below $10^{-12}$ | 4 min |
| S9 | renormalisation identity (`renorm_check.py`, 6 cases) | relative difference $\le5.9\cdot10^{-14}$ in all cases; $H_1(0)=1.007795$ at $p=13$. The script also prints a "mean(grid)" of $0.03678$; this is a finite-grid average, not the period mean (see S14) | 35 s |
| S10 | $\Lambda_p$, $\tau_p(3)$ (`lambda_p.py`, `rmf_budget.py`, `lead_checks.py`) | the table of Theorem 10.16; $1/(\Lambda_p+\tau_p(3))=2.68,13.27,28.45$ for $p=7,11,13$ | <1 s |
| S11 | Lean `Renorm.lean` (`lake env lean`) | compiles; `worst_case_iff` and `window_succ` use `propext, Classical.choice, Quot.sound`, and `cover_extend` uses `propext, Quot.sound`; no `sorry` | 2 min |
| S12 | the lead's own test of Prop. 10.6(iii), state by state (`lead_window_check.py`; shares no code with R1b) | $(30,36)$: 262/262 parents exact in all states (1028 parent-state identities); $(40,48)$: 213/213 (1742 identities); slopes seen $1,3,4$ | 16 s |
| S13 | R3 cross-validation (`validate.py`: A, B and brute force on 25 small cases) | 7 500 comparisons (all fibre levels of A; B with several sparse settings), **0 mismatches**; 158 failing (case, $K$) pairs with exact miss counts among the references. This is the same seeded test suite as track R3's, reproduced | 46 s |
| S14 | exact period mean of $H_1$ at $p=13$ (`lead_hmean.py`, added in the referee revision; factorial-digit transfer recursion) | $13\int_0^1G=0.03667545$ on grids of $2^{14},\dots,2^{20}$ points (agreeing to 10 digits), against the heuristic $13(2/\pi)^{13}=0.03667625$; reproduces the computational referee's $0.0366754$ (`lead_hmean.out`) | <1 min |
| — | `lead_checks.py` | $\rho_0(p)$ table as in Lemma 10.11; ownership tiling of Theorem 10.18: 938 consecutive window pairs around 64 centres of valuation up to $10$, 0 failures; first uncertified window owns levels $[67\,977\,551,67\,977\,559)$; $D_{13}=9$; all Legendre values of §10.2 | <1 s |
| C1 | all uniform certificates of §10.2 ($p=7,11,13,17,19,23$, $t\le6$, and $(13,7,39)$), programs A and B | 37 certificates $\times$ 2 programs: all ALL_COVERED / ALL_OK | 8 min |
| C2 | $p=13$, depth 8, $K''=1..12$, $H=47$ | A: 12/12 covered (about 250 s each); B: 12/12 OK (about 280 s each). Chain on the re-run logs alone: **CHAIN OK, $f(1,13)\ge883\,708\,272$** | A 50 min, B 56 min (CPU) |
| C3 | $p=11$: depth 7 (109 positions with $H=40$; $K''=37$ with $H=41$), depth 8 ($H=44$) | A and B: all 109 depth-7 positions with $H=40$ and $K''=37$ with $H=41$ covered; 10/10 depth-8 positions covered. $(11,7,40,K''=37)$: **both programs find exactly 2 missed residues**. Chain on the re-run logs alone: **CHAIN OK, $f(1,11)\ge235\,794\,760$** | A 12 min, B 23 min (CPU) |
| C4 | $p=7$: depth 7 (42 positions, $H=40$), depth 8 ($H=47$) | A and B: 42/42 depth-7 positions and 6/6 depth-8 positions covered. Chain on the re-run logs alone: **CHAIN OK, $f(1,7)\ge6\,725\,592$** | A 6 min, B 13 min (CPU) |
| C5 | $p=19$, depth 7, $H=45$; $p=23$, depth 7, $H=43$ | A and B: $p=19$, 18/18 positions; $p=23$, 22/22 positions covered. Chains on the re-run logs alone: **CHAIN OK, $f(1,19)\ge943\,531\,272$ and $f(1,23)\ge3\,559\,590\,232$** | $p=19$: A 9 min, B 19 min; $p=23$: A 4 min, B 5 min (CPU) |
| C6 | $p=17$: depth-7 positions ($H=43$, A and B); uniform $\mathrm{Cov}(17,7,43)$ and depth-8 positions ($H=47$), **program A only** | Depth 7, A and B: 16/16 positions covered; chain on the re-run logs alone: **CHAIN OK, $f(1,17)\ge435\,984\,832$**. Program A: uniform $\mathrm{Cov}(17,7,43)$, 272/272 classes covered, and 16/16 depth-8 positions covered. Chain with A from the re-run and B from R3's original logs (`data/round2/outputs/R3_p17_programB_original/`): **CHAIN OK, $f(1,17)\ge7\,411\,742\,272$** (`data/round2/outputs/CHAIN_p17_D9_Arerun_Boriginal.txt`). Program B's half of this bound was not re-run | depth 7: A 3 min, B 8 min; A uniform $t=7$: 54 min (two jobs of 27 min); A depth 8: 60 min (four jobs) (CPU) |

*Not re-run by the lead* (they rest on track logs of 2026-10-11 in `data/round2/logs_original/`):
- program B's uniform $\mathrm{Cov}(17,7,43)$ (about 2 core-hours) and its $p=17$ depth-8 positions (about 3 core-hours). Program C, run by the round-2 computational referee, has since certified both independently;
- R3's program-A negative results at $(13,8,45)$, $(13,8,46)$, $(17,7,42)$ and $(19,7,44)$, and the $H$-scans behind the minimality table. All of these were since reproduced by program C;
- the Fourier diagnostics `fwin2.c` and `kscan.sh` (heuristic, Conjecture 10.23);
- the Knuth estimators (heuristic, Conjecture 10.22);
- R1a's Monte Carlo and conservation tests;
- `lam_stats.py` (§10.1.2). The two round-2 referees' own slope probes are consistent with it (§10.8).

*Referee re-runs (2026-10-12).* The round-2 referees' programs are in `code/round2/review/` and their logs in `data/round2/review/`. Section 10.8 summarises their results. The main ones:
- program C's certificates for every bound of §10.2, with its own chain script: CHAIN OK for all six (`data/round2/review/computation/chain_c.out`);
- its minimality re-scans (`scans.out`) and negative certificates (`logs/N*.log`, `logs/n11_*.log`);
- certified shell sums with `shells.c`, and an exact Parseval cross-check (`equidist_dp.py`);
- exact tests of Proposition 10.6(iii) (`p2_window.py`, by both the logic and the computational referee);
- a brute-force test of Theorem 10.12 (`thm1012_brute.py`);
- the logic referee's `covmiss.c` for $(11,7,40,37)$, $(11,7,39,1)$ and $(11,7,41,37)$.

### 10.8 Verification and credit (round 2)

*What the lead-author AI instance checked* (before the referees). Here "lead author" means this Claude instance, not the human author, who has not verified the mathematics.
- **Theorem 10.1.** Every step of R1b's proof was checked line by line and rewritten in §10.1. Details were added where the original was terse:
  - measurability of the window times;
  - the stopped process $\tilde Z_\ell$;
  - the child-alive criterion in Proposition 10.6(iii).

  No error was found.
- **Propositions 10.10 and 10.14–10.15, Lemma 10.11, Theorems 10.12, 10.16 and 10.18, Corollaries 10.13 and 10.20, and Propositions 10.19 and 10.21.** All were checked. For Theorem 10.18 the ownership tiling was also checked by a script around multiples of $13$ of every valuation $t\le10$ (`lead_checks.py`). The lead missed the unit hypothesis of Proposition 10.19 and the over-reading of Corollary 10.13; the referees found both (below).
- **Lean.** `Renorm.lean` was re-compiled (§10.7).
- **Not checked to theorem standard.** R1a's route and Claim 10.9 (§10.1.4). The heuristics of §10.5 are labelled as such.

*Round-2 referees.* Three Claude instances then refereed §10 independently (2026-10-12), each from a different angle. Each wrote its own code, sharing none with the tracks or the lead; the code and logs are in `code/round2/review/` and `data/round2/review/`. **None of them is human.** All three found **no fatal or serious mathematical error**. The novelty referee found two serious problems of credit and attribution. All the findings, serious and minor, are corrected in this version, as listed below.

**Logic referee.** It read §§0–6 and all of §10 and checked every round-2 proof.
- *Theorem 10.1, line by line.* It checked:
  - Lemma 10.2(a)–(f), including the carry count in (d);
  - the good set $\Omega$ and the Borel–Cantelli bound;
  - Lemma 10.3, including summability, the Taylor identity, and non-vanishing via $F_e(-4)\equiv1\pmod3$;
  - Lemmas 10.4 and 10.5, including the $(1+E)^{-1}$ bookkeeping;
  - Proposition 10.6(i)–(iii), including the affine bijection $w\bmod2^D\leftrightarrow$ coset and $N-n-D=W_N-W_n$;
  - Proposition 10.7, including closure, the distinct-valuation bound on $|F_0|$ and the coset-measure bound;
  - the digit filtration, the martingale identity and measurability, the survival lower bound, and the environment walk;
  - the Doob argument, the asymptotic validity of (W1)–(W3) and (V1)–(V4) on $\Omega$, and the $k\ge2$ supermartingale bound.

  It found **no gap**. Its own exact-arithmetic test of Proposition 10.6(iii), state by state (`p2_window.py`, 600-bit representatives), passed on 1227/1227 parents over 3 seeds, with slopes $1,3,4$. Its slope probe saw no $\lambda=2$, consistent with §10.1.2.
- *Other proofs.* It checked Proposition 10.10 (and read `chain.py`), Lemma 10.11, Theorem 10.12 (the Lean statements match the abstract core and the recursion), Corollary 10.13 as stated, Propositions 10.14, 10.15 and 10.21, Theorem 10.16 (conditional), Theorem 10.18 and Proposition 10.19.
- *Independent recomputations.* It recomputed every Legendre value, $\rho_0$, $D_{13}$, $\Lambda_p$ and $\tau_7(3)$, and the minimal $H_t$ for $t\le3$ at $p=7,\dots,23$. Its fibre/bitset checker `covmiss.c` (validated against numpy brute force on 24 cases) gives exactly 2 misses at $(11,7,40,K'=37)$, 0 at $(11,7,41,37)$, and $1\,389\,738$ at $(11,7,39,1)$. It confirms uniform $\mathrm{Cov}(7,6,34)$ and the failure of $\mathrm{Cov}(7,6,33)$ at $K'=5$.
- *Minor findings, all fixed:*
  1. Proposition 10.19 and Corollary 10.20 tacitly needed $v_p(N_W!/N_0!)=W$ exactly. They are false as written for skipped $W$, e.g. $N_0=p$, $W=p-1$. The hypothesis "$W$ attained" is now stated. Two heuristic "close to" statements inside these proved items are now labelled heuristic.
  2. §0 item 15, the T3 bullet of §6 and the "Consequence" paragraph after Corollary 10.13 claimed that fullness-only T3 is false beyond level $D_p$. Corollary 10.13 proves this only for single gate blocks and short windows. The claim is withdrawn and the text reworded (§0, §6, §10.3, §10.6).
  3. The constant of Claim 10.9 was rounded down ($0.661$ instead of $0.66135$); it is now $0.662$.
  4. Remark 10.1.3 called the mean of a martingale "growing"; this is reworded.

**Computational referee.** It re-implemented and re-ran every computational claim of §10 with at most 3 cores and no run over 50 minutes.
- *Program C* (`covchk.c`, written from scratch) was validated against a numpy brute force on 2047 comparisons, 1312 of them failing cases with exact miss counts, with 0 mismatches. It re-ran:
  - all 37 uniform certificates of §10.2 (the 36 with $t\le6$, plus $(13,7,39)$), using lifted class representatives;
  - uniform $\mathrm{Cov}(17,7,43)$ over all 272 classes, and all 16 depth-8 positions at $p=17$, i.e. the half that the lead had not re-run with program B;
  - every depth-7 and depth-8 position behind the bounds for $p=7,11,13,19,23$.

  All of these are covered, except $(11,7,40,K''=37)$, which misses exactly 2 residues. Its own chain script, on program C's logs alone, gives CHAIN OK for all six bounds of §10.2.
- *Negative certificates.* It reproduced:
  - $(11,7,39,1)$: $1\,389\,738$ misses;
  - $(13,8,46,1)$: 26 misses, and $(13,8,45,1)$ fails;
  - $\mathrm{Cov}(17,7,42)$ fails only at $K'=6$ among the classes $1,\dots,8$;
  - $(19,7,44)$ fails at exactly the positions $K''=1,5,9,11,12,14,16$.
- *Minimality.* It re-scanned every entry of the minimality table, including $H_6(7)=34$, and found every minimal $H_t$ exactly as stated. Every failing $H$ above the minimum has $(H-1)\bmod p<\rho_0$. It also confirmed the example of Proposition 10.14(b): $\mathrm{Cov}(7,3,H)$ holds for $H=19,20,21,28,35,42$, and for $H=49$ over all $100\,842$ classes.
- *Other recomputations.* It reproduced:
  - $\Lambda_p$, $\tau_7(3)$, $\rho_0$, $L_p$, $D_{13}$ and all Legendre values;
  - the shell sums $T_{13}(1..7)$ and $T_{11}(1..8)$ to every printed digit (`shells.c`), with an exact Parseval cross-check;
  - Corollary 10.17 directly from the exact subset-sum distribution for $K\le7$ (max $|\theta|=7.994\cdot10^{-3}$ at $p=13$, $0.05657$ at $p=11$). The case $p=11$, $K=8$ was checked only through the shell sums;
  - the ownership tiling of Theorem 10.18 (0 failures);
  - a brute-force test of the "iff" of Theorem 10.12 on 3600 random small instances (0 disagreements);
  - an exact test of Proposition 10.6(iii) on 155 parents (all exact).
- *Minor findings, both fixed:* the constant of Claim 10.9 ($0.662$, as above); and the figure "mean $0.03678$" under Proposition 10.19, which was a finite-grid average. The true period mean is $0.0366754$, matching the heuristic $0.0366763$. The lead reproduced this value (§10.7, row S14).
- *Not covered by this referee:* the logic of Theorem 10.1, the Lean files, the archived round-1 landscapes (behind "every deep $a\le1000$"), and the heuristic Conjectures 10.22–10.26.

**Novelty referee.** It re-checked the public record on 2026-10-12: the problem page and forum, Kitamura's repositories, teorth/erdosproblems, formal-conjectures PR #6936, arXiv, GitHub, and the earlier AI write-ups. It found **no prior proof or claim** of $\mu(K_2)=0$, of the round-2 bounds, of the failure of $\mathrm{Cov}(11,7,40)$, or of the structural results 10.11–10.21. Q1–Q3 remain open, and the status line does not overstate them. Its own checker confirms that $\mathrm{Cov}(7,6,33)$ fails at $K'=5$ and that $(7,6,34)$ covers that class.
- *Serious finding 1: Kitamura under-credited.* Kitamura's July 2026 repository already calls $p=2$ a critical branching process and reports a measured surviving fraction of about $11.5/G$, so that the census determines $f(a,2)$ for "MOST integers". We had credited the branching picture to our round 1. This repeats the main finding of the round-1 novelty referee. *Fixed:* Kitamura is now credited in §0, §2, §5 (H1 and Conjecture 5.1), §10.0, Remark 10.8.4 and below. The lead re-read the three files to confirm the statements.
- *Serious finding 2: verification attributed to a human.* "The lead author checked every proof" could be read as the named human author, who has verified nothing. *Fixed:* §0, §8, the start of §10 and this section now say "lead-author AI instance", and "the lead" is defined.
- *Minor findings, all fixed:*
  1. The summaries overstated Corollary 10.13 (as above).
  2. Of the six "registered predictions" of Conjecture 10.24, one was not in the registration file and one was partly known beforehand; a third lies in the law's mixed band. §10.5 now gives the exact count: three genuine out-of-sample tests.
  3. Claim 10.9 cannot give a rate for $\delta_G(2)$, because of its $1/16$ floor. It is also weaker than the census bound $\delta_{32}(2)=0.1016$ for $G\lesssim8\cdot10^5$. This is now said.
  4. "Two exact reformulations of Q3" now reads "two sufficient conditions", and the hypotheses $\mathrm{Cov}(p,1,\cdot)$ and $\mathrm{Cov}(p,2,\cdot)$ of Theorem 10.16 are restored in §0.
  5. The $f(1,17)$ headline needed the caveat that program B's half was not re-run, and "independent" needed qualifying; both are now done (and program C now covers that half).
  6. Credit details: extinction for critical branching processes in random environments is due to Smith–Wilkinson and Athreya–Karlin, with the modern criterion in Afanasyev–Geiger–Kersting–Vatutin; Kozlov gives survival asymptotics. Remark 10.8.2 is corrected. Proposition 10.14(a) is credited to Tao.

*What remains unverified.*
- **No human** has checked any part of §10.
- The archived round-1 landscapes behind "every deep $a\le1000$" were not re-run in round 2; the round-1 computational referee reproduced them.
- R1a's route and Claim 10.9 remain unverified (§10.1.4).
- The Monte Carlo and Fourier diagnostics behind Conjectures 10.22–10.26 were not re-run by anyone.

*Credit.*
- The critical-branching picture at $p=2$ and the empirical decay of the surviving fraction are Kitamura's (July 2026; §2). Round 1 formulated H1 and target T4 (§5, §6) without crediting them.
- The martingale-plus-environment-walk strategy is classical for branching processes in random environments (Smith–Wilkinson 1969; Athreya–Karlin 1971; Afanasyev–Geiger–Kersting–Vatutin 2005).
- The covering framework is Tao's programme (§2), carried out in §3.7. Proposition 10.14(a) is the $\mathrm{Cov}$-level form of Tao's step.
- The values $f(2,2)=254$ (Lin) and $f(a,2)$ for small $a$ (Kovač, Kitamura), Kitamura's census and determinacy lemma, and the earlier AI write-ups are credited as in §2.
- Apart from the additions above, round 2 does not change any attribution made in revision 1.

---

## References

- [ErGr80] P. Erdős, R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, Monographies de L'Enseignement Mathématique 28 (1980), p. 79.
- [Li76] S. Lin, *On two problems of Erdős concerning sums of distinct factorials*, Bell Laboratories internal memorandum (1960; cited as [Li76] on erdosproblems.com). Unpublished.
- T. F. Bloom, *Erdős Problem #404*, https://www.erdosproblems.com/404, and the forum thread https://www.erdosproblems.com/forum/thread/404 (comments by V. Kovač, 13 Aug 2025; T. Tao, 29 Sep 2025; K. Kitamura, 7–8 Jul 2026). Accessed 2026-10-08.
- K. Kitamura, `github.com/KitaKen1/erdos-404-p2-landscape` (`README.md`, `determining_exact_values.md`, `witness_gallery.md`) and `github.com/KitaKen1/erdos-404-odd-prime-landscape` (`README.md`), July 2026 (data status 2026-07-06).
- T. Tao, comments of 29 Sep 2025 in the forum thread for Problem #404 (the block lemma and the depth-$j$ programme).
- Earlier AI-generated write-ups (unrefereed): `github.com/neelsomani/gpt-erdos`, `data/solutions/404/candidate_solution.md` (2026-01-17); `github.com/erichou1/erdos-open-problems`, `solutions/open/solution_404.md` (2026-06-10); `github.com/AItoBit/Erdosproblems-llm-hunter`, `GPT_6_Astra_Ultra/404.tex` (2026-09-25).
- google-deepmind/formal-conjectures, PR #6936 (2026-10-08) and issue #713.
- M. Andrejić, A. Bostan, M. Tatarevic, *Improved algorithms for left factorial residues*, Inform. Process. Lett. 167 (2021) 106078, arXiv:1904.09196.
- M. Andrejić, M. Tatarevic, *Searching for a counterexample to Kurepa's conjecture*, Math. Comp. 85 (2016), arXiv:1409.0800.
- M. Z. Garaev, F. Luca, I. E. Shparlinski, *Character sums and congruences with n!*, J. reine angew. Math. 584 (2005), arXiv:math/0403424.
- O. Klurman, M. Munsch, *Distribution of factorials modulo p*, J. Théor. Nombres Bordeaux 29 (2017), arXiv:1505.01198.
- Y. Morita, *A p-adic analogue of the Γ-function*, J. Fac. Sci. Univ. Tokyo 22 (1975); A. M. Robert, *A Course in p-adic Analysis*, GTM 198, Ch. 7.
- J. A. Guthrie, J. E. Nymann, *The topological structure of the set of subsums of an infinite series*, Colloq. Math. 55 (1988); survey: arXiv:2512.17285.
- Mathlib: `ZMod.cauchy_davenport` (Cauchy–Davenport theorem).
- [Round 2, background only; not used in any proof]
  - W. L. Smith, W. E. Wilkinson, *On branching processes in random environments*, Ann. Math. Statist. 40 (1969). Almost-sure extinction in the critical case.
  - K. B. Athreya, S. Karlin, *On branching processes with random environments I, II*, Ann. Math. Statist. 42 (1971).
  - V. I. Afanasyev, J. Geiger, G. Kersting, V. A. Vatutin, *Criticality for branching processes in random environment*, Ann. Probab. 33 (2005). The criterion in terms of the associated random walk.
  - M. V. Kozlov, *On the asymptotic behavior of the probability of non-extinction for critical branching processes in a random environment*, Theory Probab. Appl. 21 (1976). Survival asymptotics.
- [Round 2] K. Kitamura, `KitaKen1/erdos-404-p2-landscape`: `witness_gallery.md` §6 and `determining_exact_values.md` §5 (critical branching process; measured surviving fraction $\approx11.5/G$). Repository last pushed 2026-07-07; re-read 2026-10-12.
