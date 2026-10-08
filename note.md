# Erdős Problem #404 (sums of distinct factorials divisible by high prime powers): structure, finiteness families, certified lower bounds, and what remains

**Author:** Nathan Durfee (composer and prompter; he has not personally verified the mathematics)

**AI assistance:** The mathematics, code, computations and text in this note were produced by Claude (Anthropic), model Claude Opus 5.5. It ran as a multi-agent workflow inside Claude Code, prompted and composed by the author. See §8 for the full disclosure.

**Date:** 2026-10-08. **Revision:** this version incorporates the corrections from three AI referee reports (logic, computation, novelty); see §9.

**Status:** Unrefereed research note. No human referee has checked it. **All three questions of Problem #404 remain OPEN.** Nothing here proves that $f(a,p)=\infty$ for any pair $(a,p)$.

---

## 0. Summary

Throughout, $p$ is a prime and $v=v_p$ is the $p$-adic valuation. For $a\ge1$, $f(a,p)$ is the supremum of the $k$ such that $p^k\mid a_1!+\dots+a_n!$ for some $a=a_1<a_2<\dots<a_n$.

Status labels used throughout:
- **[proved]** — a complete proof is given here.
- **[proved+Lean]** — in addition, a stated core was machine-checked in Lean 4 + Mathlib. Only the standard axioms are used, with no `sorry` and no `native_decide`.
- **[computer-assisted]** — the proof relies on a finite exact computation. The programs are supplied and were re-run, either today or as recorded in §7.
- **[heuristic]** and **[conjecture]** — not proofs.

### What was already known, and is only re-derived or repackaged here

A novelty referee (§9) found that several statements of an earlier draft were already public. We credit them here and in §2.
- **Normal form.** Writing $f(a,p)=v_p(a!)+g$, with $g$ the valuation of $1+\sum_{b\in B}(a+1)\cdots(a+b)$, is Kitamura's normalisation $W_J(a)$, $g(a,2)=f(a,2)-v_2(a!)$ (July 2026, `determining_exact_values.md` §3).
- **Compactness.** "$f(a,p)=\infty$ iff some infinite set $A\ni a$ has $\sum_{n\in A}n!=0$ in $\mathbb Z_p$, so Q3 holds iff some $f(a,p)=\infty$" appears in earlier public AI write-ups: neelsomani/gpt-erdos (2026-01-17, sketch), erichou1/erdos-open-problems (2026-06-10, with proof) and AItoBit/Erdosproblems-llm-hunter (2026-09-25, an explicit König-type proof).
- **Locality.** "$g\ge G$ depends only on $a \bmod p^G$" is Kitamura's *determinacy* lemma for $p=2$. The proof for general $p$ is the same one-line argument.
- **The $p=2$ value set.** Kitamura states that $g(a,2)=0$ for odd $a$ (a parity argument, with a Lean certificate for $a=5$), that $g\ge3$ for even $a$ (cube identity), that $g$ never takes the values $1,2,4,5$, and that $g=3$ exactly on $a\equiv4 \pmod 8$. These follow from his determinacy lemma and his certified classification of all even classes with $g\le24$ (174,640 residue classes). He also states the "sibling-pairing theorem" ($g$ is constant on $a \bmod 2^{g(a)}$), without a shipped proof, and the shadow family $a=2^t-2$ with $g\ge3t$.
- **Tao's programme.** Tao (forum, 29 Sep 2025) stated the block lemma and the step $P(a,p,N)\Rightarrow P(a,p,N+1)$ for $p\nmid N+1$. He also observed that each depth-$j$ step should reduce to one fixed finite computation, giving lower bounds of the shape $v_p((p^{J+1}-1)!)$. Our gate congruence (Theorem 3.9) and the $\mathrm{Cov}$/$\mathrm{UC}$ framework (Theorem 3.12) carry out this programme.

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
10. **Densities beyond Kitamura's census [computer-assisted]** (§4.7). For $p=2$, Kitamura's classification of $g\le24$ already gives $f(a,2)<\infty$ on a set of density $1-\delta_{25}(2)=0.8734$. We extend this:
    - $f(a,2)\le v_2(a!)+28$ on density $1-\delta_{29}(2)=0.8866$ (three independent implementations), and $f(a,2)\le v_2(a!)+31$ on density $1-\delta_{32}(2)=0.8984$ (two implementations);
    - at odd primes, the first densities beyond the class $a\equiv-1 \pmod p$: $f(a,p)<\infty$ on density $\ge0.6367$ for $p=3$, $\ge0.4784$ for $p=5$, $\ge0.3761$ for $p=7$, $\ge0.3002$ for $p=11$ and $\ge0.2455$ for $p=13$.
11. **A negative coverage result [computer-assisted]** (§4.2). $\mathrm{Cov}(5,5,H)$ fails for every $H\le38$. So a uniform-covering proof at $p=5$ needs blocks of length at least $39$ at depth $5$.
12. **A precise target for Q3 (§6).**
    - Prove a uniform covering statement $\mathrm{UC}(p)$ for one prime $p\ge7$. It is already certified for all depths $t\le7$ at $p=13$.
    - Equivalently, prove a joint equidistribution statement for subset sums of the universal vectors $\big((-1)^u/u!,\,(-1)^uH_u/u!,\dots\big)$.

The heuristics (§5) point in a definite direction, but none of it is proved:
- $p=2$ is "critical", and $f(a,2)<\infty$ probably holds for almost all, perhaps all, $a$.
- Every odd $p$ is "supercritical", with $\mu(K_p)\approx0.363$ for $p=3$, $0.522$ for $p=5$, $0.624$ for $p=7$ and $0.700$ for $p=11$.

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
- **V. Kovač** (forum, 13 Aug 2025) corrected the statement and recorded $f(1,2)=0$, $f(2,2)=254$, $f(3,2)=1$, $f(4,2)=6$ and $f(5,2)=3$. He noted that $\lim_a f(a,p)=\infty$ ("clearly").
- **T. Tao** (forum, two comments of 29 Sep 2025):
  - He suggested that $f(1,5)$ is "extremely large, and possibly even infinite", with examples such as $1!+4!+10!+11!$.
  - He stated the block lemma (Lemma 1.3(iii)) and its special case $P(a,p,N)\Rightarrow P(a,p,N+1)$ for $p\nmid N+1$ (Lemma 1.3(iv)).
  - He suggested checking computationally that the $2^p$ subset sums of $0!,\dots,(p-1)!$ cover $\mathbb Z/p$, which gives the step over a block of length $p$ ending at a multiple of $p$ exactly once (compare Theorem 3.9(a)).
  - He observed that, more generally, the step across a multiple of exactly $p^j$ should reduce to one fixed finite computation for each $j$ (he called the case $N=0$ "key"), and that doing this for all $j\le J$ would give $f(a,p)\ge v_p((p^{J+1}-1)!)$. Theorems 3.9(b) and 3.12(a) below make this position-independence precise; the $\mathrm{Cov}$/$\mathrm{UC}$ framework of §3.7 carries out his programme.
- **K. Kitamura** (Jul 2026, AI-assisted; repositories `KitaKen1/erdos-404-p2-landscape` and `KitaKen1/erdos-404-odd-prime-landscape`):
  - Exact $f(a,2)$ for $1\le a\le256$, including $f(34,2)=18444$, and deeper exact rows $f(1102,2)=12633$, $f(3456,2)=8275$ and $f(8190,2)=16396$. Each is certified from both sides.
  - A two-sided Lean check of $f(2,2)=254$. The parity argument that odd $a$ give $f(a,2)=v_2(a!)$, with a Lean certificate for $f(5,2)=3$.
  - *Structural facts at $p=2$* (`README.md`, `determining_exact_values.md` §§3–5, `witness_gallery.md` §§3, 7, 8):
    - the normalisation $W_J(a)$, $g(a,2)=f(a,2)-v_2(a!)$ (our Lemma 1.1);
    - the *determinacy* lemma: whether $g(a,2)\ge G$ depends only on $a \bmod 2^G$ (our Theorem 3.1(a) at $p=2$);
    - the cube identity $a!+(a+1)!+(a+3)!=a!(a+2)^3$, so $g\ge3$ for every even $a$;
    - a certified classification of all even classes with $g\le24$ (174,640 residue classes). From it: $g$ never takes the values $1,2,4,5$, $g=3$ exactly on $a\equiv4 \pmod 8$, and the attained values up to 24 are exactly $\{3\}\cup[6,24]$. These are computer-certified statements, not merely empirical ones. The classification also gives $f(a,2)<\infty$ on a set of density $1-\delta_{25}(2)=0.8734$;
    - the *shadow family* $a=2^t-2$, with $g\ge3t$ from the cube identity and exact values for $t\le13$ (for example $g(8190,2)=8218$);
    - the *sibling-pairing theorem*, $g(a+2^{g(a)},2)=g(a,2)$, so $g$ is constant on $a \bmod 2^{g(a)}$. It is stated without a shipped proof. He also reports certified "dead balls", for example $g\equiv648$ on $254+2^{638}\mathbb Z_2$.
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

*Credit.* At $p=2$, the points $a=2^t-2$ are Kitamura's shadow family: he notes $g\ge3t$ and computes exact finite values for $t\le13$ (`witness_gallery.md` §7). So (d) at $p=2$, and finite values of $g_2$ up to $8218$, were known. The term "shadow" in §3.2 is also his. What we believe is new is (b), and (c) at every prime: finite values that are provably unbounded, located on explicit classes via the negative points $-(p^k+2)$.

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
- (i) If $g_2(a)=G\ge1$, then $g_2\equiv G$ on $a+2^G\mathbb Z$. For instance $f(a,2)=v_2(a!)+253$ for all $a\equiv2 \pmod{2^{253}}$. This proves Kitamura's "sibling-pairing theorem" $g(a+2^{g(a)},2)=g(a,2)$ (`witness_gallery.md` §8), which he states without a shipped proof. The Lean name `E404.sibling` follows his terminology. (The hypothesis $G\ge1$ is needed: at $G=0$ the statement would say that $g_2$ vanishes identically.)
- (ii) In the 2-adic tree of classes $\{g\ge G\}$, every surviving class has $0$ or $2$ surviving children.
- (iii) $g_2(a)\in\{0,3\}\cup[6,\infty]$. Moreover $g_2(a)=0\iff a$ is odd, and $g_2(a)=3\iff a\equiv4 \pmod 8$.
  - The direction ⇐ of the last statement is Lean `E404.g_eq_three`.
  - The rest follows from the class counts $|\{g\ge k\} \bmod 2^k|=1,2,4,6,12,24$ for $k=1,\dots,6$, a 64-class computation re-run in `indep_checks.py`. Locality (Theorem 3.1(a)) alone suffices to turn these counts into the statement; the halving lemma gives a second route.
  - *Credit.* All of (iii) was already stated by Kitamura, as a consequence of his determinacy lemma and his certified classification of the classes with $g\le24$ (§2). We include it only as an independent confirmation.
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

The maximal exact $g$ values are 18, 5, 3, 1 and 1 respectively. All 3200 of Kitamura's odd-prime rows agree, and his "ignited candidates" are now proved to have $g\ge10^4$.

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
- *Comparison with prior work.* Kitamura's certified classification of the classes with $g\le24$ already gives $f(a,2)<\infty$ on density $1-\delta_{25}(2)=0.873385$. Our census agrees with his count: summing the dying classes through level 25 in `archive/E/tree_p2.txt` gives $2\times87\,320=174\,640$ classes, his number. What is new for $p=2$ is the extension from level 25 to level 32.
- $f(a,3)<\infty$ on density $\ge0.6367$.
- For $p=5,7,11,13$ the densities are $\ge0.4784$, $0.3761$, $0.3002$ and $0.2455$. For odd $p$, these are the first rigorous densities beyond the class $a\equiv-1 \pmod p$ (density $1/p$).
- Forbidden values: $g_2\notin\{1,2,4,5\}$ (Corollary 3.7.1), and $g_7(a)\ne2$ for all $a$, since $\delta_2(7)=\delta_3(7)=31/49$.

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

**Conjecture 5.1 (Q1 at $p=2$).** $f(a,2)<\infty$ for every $a$, i.e. $K_2\cap\mathbb Z=\{-2\}$. A weaker form is $\mu(K_2)=0$, i.e. $\delta_G(2)\to0$.

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

---

## 6. The most promising route to Q3, and exactly what remains

**What a covering-type proof of Q3 must do.** The constraints below are proved in §3, but items 1, 2 and 4 apply only to proofs that go through Tao-type covering of blocks or windows. They do not exclude a proof of a different kind, for example a non-constructive proof that some $f(a,2)=\infty$. That possibility is exactly the negation of Conjecture 5.1, and it remains open.
1. A covering-type proof must work at an odd prime: Tao-type covering is impossible at $p=2$ (Theorem 3.8). For $p=3$, node-level covering fails at every $N\equiv0 \pmod{81}$ (Theorem 3.11), so only a population-level argument could work there.
2. A proof that crosses gates of unbounded level by covering windows must use unboundedly many $p$-adic digits of the unit parts $U(n)$, i.e. of Morita's $\Gamma_p$ (Theorem 3.10). Mod-$p$ additive combinatorics alone (Cauchy–Davenport, Olson, Erdős–Heilbronn) cannot suffice for that.
3. No proof can use a residue-class criterion on $a$ (Theorem 3.6). This item holds for every kind of proof.
4. It must avoid "worst case over all incoming carries plus all higher digits" arguments. Track B shows such arguments give a transfer-operator constant $\ge1$; this is a statement about that proof schema, not a theorem about all proofs.

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
- **(T4, for Q1)** Prove $\mu(K_2)=0$ by a quenched first-moment bound. Heuristic picture (track E): grouping steps in pairs, $\log_2$ of the expected population is a zero-drift walk $\sum(2-d_k)$ with $d_k=v_2(\alpha+2k)$. The missing input is equidistribution of the unit parts of $(\alpha+1)_k \bmod 2^d$ conditional on the valuation pattern, for which the 2-adic Morita/odometer structure is the natural tool. This would give "$f(a,2)<\infty$ for almost all $a$". It would not settle Q3.

**Computational next steps** (feasible extensions of the supplied code):
- $\mathrm{Cov}(5,5,39)$ and $\mathrm{Cov}(5,5,40)$: $312\,500$ classes of $5^{13}$-bit sets each, about 24 core-hours per $H$ with `cov.c`; every $H\le38$ is already refuted;
- $\mathrm{Cov}(11,7,40)$ over all $1210$ classes $K' \bmod 11^3$ (about 2.5 core-hours and 6.5 GB with `cov.c`). This would give the dichotomy of Theorem 3.12(b) at $p=11$ with $T=7$, for all $a<11^8-40$;
- three-block windows for $p=17$–$31$;
- the $p=7$ tail frontier (§4.5) through $7^8$;
- explicit witnesses for the frontier bounds;
- re-running the $p=5,7$ frontiers with fully automated logs.

---

## 7. Reproduction

### 7.1 Layout

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

This note was composed by **Nathan Durfee**, who set the problem, prompted and directed the work, and is the human point of contact. **He has not personally verified the mathematics.**

The mathematical content, proofs, programs, computations and text were generated by **Claude (Anthropic), model Claude Opus 5.5**, running as a multi-agent workflow in Claude Code. The workflow had four stages:
- two literature and community "gate" agents;
- six parallel research tracks: A structure, B computation, C large $p$, D $p=2$, E behaviour, F literature and coverage;
- a lead-author agent that cross-checked the tracks, wrote an independent verification oracle, re-ran the computations and wrote the first version of this note;
- three separate referee agents (logic, computation, novelty), whose reports are summarised in §9, followed by a revision that applied every correction they asked for and re-checked the new computations (R19–R21).

Machine checks are limited to what §3 and §7 state. The Lean files check specific lemmas, not the full chain of reasoning. The referees are AI instances too. **No part of this note has been reviewed by a human referee.** Readers should treat every claim as unrefereed and check what they intend to rely on. Corrections are welcome.

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
- The $p=2$ value set, "$g=0$ iff $a$ odd" and "$g=3$ iff $a\equiv4 \pmod 8$" were stated by Kitamura as consequences of a certified classification, not as empirical observations. Constancy mod $2^g$ is his "sibling-pairing theorem" (stated without a shipped proof). Our halving lemma supplies a proof; the rest is credited (§2, Corollary 3.7.1).
- The claim that rigorous densities were "previously known only on $a\equiv-1$" was false at $p=2$: Kitamura's census of $g\le24$ already gives density $0.8734$. The referee checked that our archived census reproduces his class count ($174\,640$). The summary is corrected (§0, §4.7).

Its minor findings, also addressed:
- Kitamura's shadow family $a=2^t-2$ and the term "shadow" are now credited, and the phrase "refutes the natural conjecture" is dropped (Proposition 3.4).
- Two examples of Theorem 3.2 settle residue patterns that Kitamura had listed for audit; this is now said (§0, §3.2).
- Tao's comment already anticipated the position independence of Theorems 3.9(b) and 3.12(a); the $\mathrm{Cov}$/$\mathrm{UC}$ framework is now described as carrying out his programme (§2, §3.5, §3.7).

**What the referees did not cover.** The Monte Carlo and Fourier heuristics of §5 were not re-done. No referee was human.

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
