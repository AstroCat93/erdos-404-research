# Erdős Problem #404 (sums of distinct factorials divisible by high prime powers): structure, finiteness families, certified lower bounds, and what remains

**Author:** Nathan Durfee (composer and prompter; has not personally verified the mathematics)

**AI assistance:** The mathematics, code, computations and text in this note were produced by Claude (Anthropic), model Claude Opus 5.5. It ran as a multi-agent workflow inside Claude Code, prompted and composed by the author. See §8 for the full disclosure.

**Date:** 2026-10-08. **Revision 2:** 2026-10-12. **Revision 3:** 2026-10-21 (round-3 work 2026-10-12 and 2026-10-20/21; referee corrections applied 2026-10-21).
- Revision 1 incorporates the corrections from three AI referee reports (logic, computation, novelty); see §9.
- **Revision 2 adds the round-2 results of 2026-10-11/12 in §10.** It also updates the summary (§0), the tables of §4 and the conjectures of §5 accordingly, marking each change "[Round 2]".
- §10 was then checked by a second set of three AI referee reports (logic, computation, novelty; 2026-10-12). They found no fatal or serious mathematical error. They did find two serious problems of credit and attribution, and several minor errors. All of these are corrected in this version; the reports are summarised in §10.8. **No human has refereed any part of §10.**
- **[Round 3] Revision 3 (draft compiled 2026-10-21) adds the round-3 results in §11**, a summary block at the end of §0 and a pointer in §10.6; the text of revisions 1–2 is otherwise unchanged, except for three density bounds of §0 and §4.7 that were rounded up and are now corrected (marked "[Round 3 correction]"). The round-3 tracks were run with Claude Fable 5.1 (Anthropic), not Claude Opus 5.5 (see §11.0). §11 was then checked by three AI referee reports (logic, computation, novelty) and by sixteen targeted AI refutation attempts on eight results (2026-10-21). They found no fatal error. They found two serious errors, both corrected here: an overstated reduction of $\mu(K_p)>0$ to hypothesis H′(p), and a false "Consequence" after Theorem 11.45. They also found a number of minor errors, mostly constants rounded the wrong way. All corrections are listed in §11.9. **No human has refereed any part of §11.**

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
    - at odd primes, the first densities beyond the class $a\equiv-1 \pmod p$: $f(a,p)<\infty$ on density $\ge0.6367$ for $p=3$, $\ge0.4783$ for $p=5$, $\ge0.3760$ for $p=7$, $\ge0.3002$ for $p=11$ and $\ge0.2454$ for $p=13$. *[Round 3 correction: revisions 1–2 printed $0.4784$, $0.3761$, $0.2455$, which round these lower bounds up; the exact values are $1-\delta_{10}(5)=0.4783837$, $1-\delta_8(7)=0.3760622$, $1-\delta_5(13)\approx0.24546$. Round 3 improves the first two to $0.4783977$ and $0.3760812$ (Computation 11.55).]*
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

### Round 3 additions (2026-10-12 and 2026-10-20/21; §11; AI-refereed, not human-refereed)

These were produced in a third AI-assisted session, with the round-3 tracks run on Claude Fable 5.1 (Anthropic). The gate agents and track T4 ran on 2026-10-12; after a budget interruption the other tracks ran on 2026-10-20 and 2026-10-21 (§11.0). The lead-author AI instance (not the human author) checked every proof given as [proved] and re-ran a selection of the computations (§11.8). Three AI referees (logic, computation, novelty) and sixteen targeted AI refutation attempts then checked §11 on 2026-10-21 (§11.9).
- They found **no fatal error**.
- They found **two serious errors**, both corrected below. (1) The reduction "H′(p) ⇒ $\mu(K_p)>0$" was overstated: Theorem 11.7 also needs an atom with large normalised weight and small freezing probability, and H′(p) is now stated with that condition (item 22). (2) A "Consequence [proved]" after Theorem 11.45 was false and has been withdrawn.
- They found **minor errors**, all corrected: two constants rounded the wrong way ($\theta_3$, and the $p=13$ dimension in item 23), three odd-prime density bounds of revisions 1–2 rounded up (item 10), an overstated "route closed" (item 26), and wording and credit fixes.

**No human has checked any of it.**

19. **$K_p$ is uncountable, with a perfect kernel [proved] (Theorems 11.11, 11.14, 11.15).** For every $p$ and every word $e$, $F_e=\sum_je_j\pi_j$ is a restricted power series on each residue disc, so it has finitely many zeros, each of finite multiplicity. Far single flips give Hensel children at exact distances. Hence the closure of the simple zeros is a perfect subset of $K_p$, nonempty exactly in the classes $r\notin\Phi_p$, and $|K_p|=2^{\aleph_0}$. Whether $K_p$ itself is perfect is open.
20. **Hausdorff dimension of $K_p$ [proved; values computer-assisted] (Theorem 11.17, Corollaries 11.19–11.20).** Near every simple zero, $\dim_HK_p\ge\sup_{w,K}D_p(w,K)\ge D_p(1,L_p+1)\ge1-p^{-L_p}$, where $D_p(w,K)$ ($p\nmid w$, $K\ge1$) is an explicit average of logarithms of numbers of distinct window subset sums. (The last inequality holds for $(w,K)=(1,L_p+1)$, not for every $(w,K)$.) Computed: $\dim_HK_2\ge0.8530$ (although $\mu(K_2)=0$), $\dim_HK_3\ge0.9247$, $\dim_HK_5\ge0.9691$, $\dim_HK_7\ge0.9921$, $\dim_HK_{13}\ge0.9996$. Consequently $\delta_G(2)\ge2^{-(0.147+o(1))G}$. None of this places a natural number in $K_p$.
21. **$p=2$: an explicit rate off the class $14\bmod16$ [proved] (Theorem 11.29, Corollary 11.30).** The natural density of $\{a\not\equiv14\ (\mathrm{mod}\ 16):f(a,2)\ge v_2(a!)+G\}$ is at most $2.0\cdot10^5\,G^{-0.227}$. This is the first explicit rate on a set of positive density, but it beats the trivial bound only for astronomically large $G$. It gives **no** rate for $\delta_G(2)$ itself: the excluded class carries about $64\%$ of the survivors at $G=512$ [Monte Carlo], and there $S_{\{1,3\}}=(x+2)^3$ is a triple root (Proposition 11.32).
22. **Odd $p$: a quenched martingale and an $L^2$ criterion [proved; the criterion's hypothesis is unproved] (Theorems 11.3, 11.4, 11.7).** The exact martingale of §10.1 transfers to every odd $p$. Hypothesis H′(p) (Conjecture 11.10) has two parts. The first is a uniform bound $K$ on a parent-correlation ratio times a single-parent relative variance. The second is an atom $A$ with $M_j(A)>0$ and freezing probability $\mu_A(\sigma_j<\infty)<1/\Lambda$, where $\Lambda=1+p^LKS_j/M_j(A)$. Together they give $\mu(K_p)>0$ (Conjecture 5.2). *[Corrected after the round-3 referees: the bound alone does not give $\mu(K_p)>0$. The atom condition amounts to a weighted population $\gg n_j^4$ on an atom that rarely freezes [heuristic], and its existence is not proved.]* The bound part has numerical support at shallow depths [heuristic]; no part of H′(p) is proved for any $p$.
23. **The $L^2$ form of the Fourier route [proved] (Theorems 11.36, 11.38).** The $L^2$ mass $C_k$ of the uniform tail measure factorises exactly into a positive carry cocycle. Unconditionally $C_k\le p^{\theta_pk+O(\log^2k)}$, with $\theta_2=\log_23/4$, $\theta_3\le0.229401$ and $\theta_{13}\le9.08\cdot10^{-4}$. Hence collision probabilities are $\le p^{-(1-\theta_p)k+o(k)}$, $\dim_HE_N\ge1-\theta^{\rm set}_p$ ($\ge0.999656$ at $p=13$; corrected from a wrongly rounded $0.99966$), and $T_p(k)\le p^{(1+\theta_p)k/2+o(k)}$: a square-root saving, **not** decay. Two obstructions show that supremum-type transfer bounds cannot prove $C_\infty<\infty$ (Propositions 11.40, 11.41).
24. **The covering route: an exact lifting criterion and negative results [proved] (Theorems 11.45, 11.46, 11.48, Corollary 11.47).** $\mathrm{Cov}(p,t,pH')$ holds iff every carry fibre $B_T$ satisfies $B_T+uV_p=\mathbb Z/p^t$ at the final, universal gate. Fullness of the fibres never suffices, and the second-moment (Chebyshev) covering criterion is dominated by the $L^1$ criterion and useless at depth. These are reformulations and negative results, not progress on $\mathrm{UC}(p)$.
25. **$f(1,19)\ge v_{19}((19^9-1)!)=17\,927\,094\,312$ [computer-assisted; every certificate by two independently written programs] (Theorem 11.50)**, up from $943\,531\,272$. Two more registered out-of-sample predictions of Conjecture 10.24 were confirmed at depth 8 (Computation 11.51).
26. **Computations (§11.6).**
    - The annealed second moment satisfies $\mathbb EZ_G^2\ge p^G/4$ at every prime [proved] (Proposition 11.53; this is the shadow of $-2$). Since the exact first moments grow only linearly in $G$ [computer-assisted, $G\le28,17,11,9$; not proved for all $G$], the untruncated subset-counting second moment cannot prove $\mu(K_p)>0$ [heuristic as a statement about all $G$]. Truncated moments are not ruled out.
    - Exact annealed moments to $G=28,17,11,9$ for $p=2,3,5,7$, with the new exact densities $\delta_{11}(5)=0.5216023$ and $\delta_9(7)=0.6239187$ (rounded to nearest) [computer-assisted; for these two values, one program, corroborated by an independent Monte Carlo within $5\cdot10^{-4}$]. They give $f(a,p)<\infty$ on density $\ge0.4783977$ ($p=5$) and $\ge0.3760812$ ($p=7$).
    - New exact value $f(2210,2)=8467$, by two independently written programs; three of Kitamura's deep records were reproduced by programs independent of Kitamura's [computer-assisted].
    - Monte Carlo suggests $\delta_G(2)\approx5.5/G$ [heuristic]. Kitamura's "$\approx11.5/G$" is $2\delta_G(2)$, the fraction among even $a$ [heuristic reading], and the earlier fit $0.7/\sqrt G$ of §5 was a small-$G$ transient [heuristic].

**Q1–Q3 after round 3:** Q1 is still open, both in general and at $p=2$ for individual $a$; Q2 has partial results only; **Q3 is OPEN**. Nothing proves $f(a,p)=\infty$ for any $(a,p)$.

What is not new in round 3, and is credited (§11.9):
- the quenched martingale and frozen-state weights (round-2 track R1b, §10.1);
- the class split at $p=2$ with $14\bmod16$ left over (round-2 track R1a's unverified Claim 10.9);
- the covering framework (Tao's programme, §3.7);
- the second-moment strategy for branching processes (Kesten–Stigum; Lyons–Pemantle–Peres; Tanny), and, closest to Theorems 11.4 and 11.7, Kersting's (2020) square-integrability criterion for the normalised martingale of a branching process in a varying environment;
- Hensel's lemma, Strassmann's theorem, Cauchy–Davenport and the mass distribution principle (classical); the binomial congruence of Theorem 11.45(a), the Chebyshev and Cauchy–Schwarz facts of Theorem 11.48(a,b), and the $L^2$ (energy) method for Bernoulli convolutions, of which Corollary 11.39 is a $p$-adic analogue (classical);
- the compactness reformulation restated in Proposition 11.21 (earlier AI write-ups, §2);
- Kitamura's normal form, determinacy lemma, data, cube identity and shadow family (§2); Proposition 11.53 is the shadow of $-2$.

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
- For $p=5,7,11,13$ the densities are $\ge0.4783$, $0.3760$, $0.3002$ and $0.2454$ *[Round 3 correction: previously printed as $0.4784$, $0.3761$, $0.2455$, which rounds lower bounds up; the exact values are $0.4783837$, $0.3760622$ and $\approx0.24546$. Round 3 improves the first two to $0.4783977$ and $0.3760812$, Computation 11.55]*. For odd $p$, these are the first rigorous densities beyond the class $a\equiv-1 \pmod p$ (density $1/p$).
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

**[Round 3]** Revision 3 (§11) came from a third session (2026-10-12, then 2026-10-20/21 after a budget interruption), with the round-3 gate and track instances running on Claude Fable 5.1 (Anthropic) and prompted by the author; provenance, the lead-author instance's checks and the round-3 AI referee reports (three referees and sixteen targeted refutation attempts, run by Claude instances on 2026-10-21) are described in §11.0, §11.8 and §11.9.

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

> **[Round 3]** For the status after round 3 and an updated list of what remains, see §11.7.

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

## 11. Round 3, 2026-10-12 and 2026-10-20/21

> **Everything in this section is new in revision 3. No human has refereed it.** Each proof labelled [proved] below was rewritten by the lead-author AI instance from the track reports and checked step by step; where the lead could not check a step, the item is labelled [sketch]. A selection of the computations was re-run by the lead (§11.8). Three AI referees and sixteen targeted AI refutation attempts then checked this section (2026-10-21). Their findings and every correction made in response are listed in §11.9; corrected passages are marked *[Corrected, round-3 referee]*.
>
> In this section, "the lead" means the lead-author AI instance, not the human author, who has not verified any mathematics. Labels: [proved], [computer-assisted], [heuristic], [conjecture], [sketch].

### 11.0 Provenance, status check, headline

*Provenance.* Round 3 ran as one workflow with two literature/status "gate" agents, seven research tracks and a lead-author instance:
- *gate-status* and *gate-literature* (2026-10-12): the public record on #404 and a verified reference list (`data/round3/gate-status/`, `data/round3/gate-literature/`).
- *T1a* (odd $p$: the quenched martingale and an $L^2$ criterion for $\mu(K_p)>0$), §11.1;
- *T1b* (fine structure of $K_p$: perfect kernel, Hausdorff dimension), §11.2;
- *T2* ($p=2$: an explicit rate), §11.3;
- *T3a* (Q3, Fourier route: the $L^2$ collision mass), §11.4;
- *T3b* and its finishing instance *T3b-finish* (Q3, covering route, and the $p=19$ computations), §11.5;
- *T4* and its finishing instance *T4b-finish* (computations), §11.6.

Track labels record provenance only. According to the workflow configuration, the round-3 track and gate instances ran on **Claude Fable 5.1 (Anthropic)**; rounds 1 and 2 ran on Claude Opus 5.5. The lead-author instance that compiled this section reports its own model as Claude Opus 5.5.

*Dates.* The gate agents and track T4 ran on **2026-10-12** (T4 launched all its runs that day; they finished the same afternoon). A budget limit then interrupted the workflow on 2026-10-12. **The other tracks ran after that interruption, on 2026-10-20, and continued into 2026-10-21**; the finishing instances T3b-finish and T4b-finish ran on 2026-10-20/21. In detail (from file timestamps and logs):
- T3b: a first instance on 2026-10-12 wrote the programs A′, C′, validated them, registered its predictions (2026-10-12 14:36:09 CDT) and started the depth-8 runs; a continuation ran the job queue on 2026-10-20 (17:27–21:36 CDT); a third instance ran the replication on 2026-10-21 (12:00–13:22 CDT); T3b-finish collected the logs on 2026-10-21 (18:39–18:45 CDT).
- T1a: a first instance on 2026-10-12 left exact-arithmetic window checks; the reported work is from 2026-10-21.
- T1b and T2: 2026-10-21 (T2's work directory was empty at the start, so everything was derived afresh).
- T3a: a previous instance (2026-10-20/21) wrote the exact $L^2$ programs; the reported work is from 2026-10-21.
- T4: runs 2026-10-12; report rewritten 2026-10-20; T4b-finish 2026-10-20 and re-verification 2026-10-21.

The lead compiled this section on 2026-10-21 (times in §11 are CDT unless marked UTC).

*Status check (gate-status, 2026-10-12 14:21–14:24 CDT; read-only).* Nothing new on #404 by anyone outside this project since 2026-10-08:
- erdosproblems.com/404: open, last edited 29 Sep 2025, 0 proof claims, comments suspended; 7 forum posts, the newest Kitamura's of 8 Jul 2026.
- Kitamura's two #404 repositories were last pushed on 2026-07-07/08 (0 stars, 0 forks). Kitamura has been active on other problems since, but not on #404.
- The only new #404 activity is this project's own: the repository AstroCat93/erdos-404-research (created and pushed 2026-10-12; AstroCat93 is this workspace's GitHub account, i.e. Nathan Durfee's own repository) and an issue opened from that account on KitaKen1/erdos-404-odd-prime-landscape (#1, 2026-10-12 12:12 UTC). About 7 hours after posting, the issue had 0 comments and 0 reactions.
- teorth/erdosproblems lists #404 as open and not formalised. Other AI catalogues (plasma-ai/erdos, rjwalters/lean-genius, neelsomani/gpt-erdos, daedalus/alphaproof-nexus) record it as open with no new claims. vibemathing/problem-um-ep-404-… (pushed 2026-09-06) is a harness template with no result; grandchallenge/MATH-PROGRAMME issue #1674 (2026-10-09) is a source-audit task packet with no mathematics.
- arXiv (all 266 math.NT listings of October 2026, and API queries): nothing on sums of distinct factorials or their $p$-adic valuations. Adjacent but unrelated: Yudin, arXiv:2610.01899 (square products of factorials, #374); Abramov, arXiv:2604.26429 (distinct residues of factorials mod $p$); Hughes, arXiv:2609.10902 (sums of distinct divisors of $n!$). MathOverflow (StackExchange API): nothing relevant.
- Gaps of the check: Google Scholar and zbMATH were not queried, and Kitamura's older forum posts were not paged.

*Citation corrections found by gate-literature (2026-10-12).* These concern the reference list of revisions 1–2, which is left unchanged; corrected entries are added at the end of the references.
1. The entry "Garaev–Luca–Shparlinski, *Character sums and congruences with n!*, J. reine angew. Math. 584 (2005), arXiv:math/0403424" conflates two papers: *Character sums and congruences with $n!$*, Trans. Amer. Math. Soc. 356 (2004) 5089–5102, arXiv:math/0403422; and *Exponential sums and congruences with factorials*, J. reine angew. Math. 584 (2005) 29–44, arXiv:math/0403424.
2. Kozlov's paper appeared in Russian in Teor. Veroyatnost. i Primenen. 21:4 (1976) 813–825 and in English in Theory Probab. Appl. 21:4 (1977) 791–804. It gives $\mathbb P(T>n)\asymp n^{-1/2}$, with an exact asymptotic only for linear-fractional offspring; the general i.i.d. case is Geiger–Kersting (2001).
3. The Zenodo record 10.5281/zenodo.23144232 is "Version 1" in its metadata, not "v2" as §2 says.
4. Lin's memorandum is cited on erdosproblems.com under the key [Li76], while the year printed there is 1960; a third-party catalogue (plasma-ai/erdos) flags this as a misprint. We have not seen the memorandum and cannot resolve the year.
5. The $p$-adic Jessen–Wintner purity law of Proposition 3.13(c) (proved there directly) appears, according to its abstract, to be covered by P. Hartman, Trans. Amer. Math. Soc. 214 (1975) 215–231, on pure laws of infinite convolutions on locally compact abelian groups; the gate did not read the full text, so this should be checked before it is cited as the source.

*Headline.*
1. **$K_p$ is uncountable, with a perfect kernel, and has large Hausdorff dimension [proved + exact computation] (§11.2).** In particular $\dim_HK_2\ge0.8530$ although $\mu(K_2)=0$, and $\dim_HK_{13}\ge0.9996$. Consequently $\delta_G(2)\ge2^{-(0.147+o(1))G}$.
2. **An explicit rate at $p=2$ off the class $14\bmod16$ [proved] (§11.3):** the natural density of $\{a\not\equiv14\ (16):f(a,2)\ge v_2(a!)+G\}$ is at most $2.0\cdot10^5\,G^{-0.227}$. No rate for $\delta_G(2)$ itself.
3. **Odd $p$: the quenched martingale of §10.1 transfers, and $\mu(K_p)>0$ is reduced to an explicit $L^2$ hypothesis H′(p) [proved; hypothesis unproved] (§11.1).** H′(p) consists of a uniform variance bound *together with* the existence of one atom with large normalised weight and small freezing probability. *[Corrected, round-3 referee: an earlier text claimed that the variance bound alone suffices.]*
4. **The $L^2$ form of the Fourier route [proved] (§11.4):** an exact positive carry cocycle, the first unconditional exponent bound $C_k\le p^{\theta_pk+o(k)}$, dimension bounds for the tail sets, and two obstructions.
5. **The covering route [proved; reformulations and negative results] (§11.5)**, and the new bound **$f(1,19)\ge17\,927\,094\,312$ [computer-assisted; two programs per certificate]**.
6. **Computations (§11.6):** the annealed second moment satisfies $\mathbb EZ_G^2\ge p^G/4$ at every prime [proved]. With the linear growth of the exact first moments [computer-assisted, small $G$ only], this makes the untruncated annealed second-moment route to $\mu(K_p)>0$ hopeless [heuristic]; truncated moments are not ruled out. Also: exact moments, new exact values and densities; Monte Carlo evidence for $\delta_G(2)\approx5.5/G$ and a reconciliation of Kitamura's "$\approx11.5/G$" with it [heuristic].
7. **Q3 remains OPEN.** Nothing in this note proves $f(a,p)=\infty$ for any pair $(a,p)$.

*Common notation for §11.* $p$ is a prime and $v=v_p$; $\mu$ is Haar probability measure on $\mathbb Z_p$; $\pi_j(x)=\prod_{i=1}^j(x+i)$, $V_n(x)=v(\pi_n(x))$, $M_n(x)=\max_{1\le i\le n}v(x+i)$; $F^{[i]}=F^{(i)}/i!$. A *path of length $n$* is $e=(e_0,\dots,e_{n-1})\in\{0,1\}^n$ with $e_0=1$, and $S_e=\sum_{j<n}e_j\pi_j$. It is *alive at $n$* (for $x$) if $v(S_e(x))\ge V_n(x)$; then its *target* is $\tau_n(e,x)=-S_e(x)/\pi_n(x)\in\mathbb Z_p$ and its *slope* is $\lambda_e(x)=v(S_e'(x))$. For an infinite word $e$ with $e_0=1$, $F_e=\sum_je_j\pi_j$. *Backward integrality*: if $(e,f)$ is alive at $N>n$ then $e$ is alive at $n$, since $p^{V_n}\mid\pi_j$ for $j\ge n$. These agree with §10.1 at $p=2$.

### 11.1 Odd primes: the quenched martingale and an $L^2$ criterion for $\mu(K_p)>0$ (track T1a)

Target: Conjecture 5.2 ($\mu(K_p)>0$ for odd $p$) by the route anticipated in §10.1.3. Lemma 11.1 to Theorem 11.3 transcribe §10.1 (track R1b's proof, as rewritten by the round-2 lead) with $2$ replaced by $p$; Theorems 11.4–11.7 (the $L^2$ half) are new. Throughout, $p$ is odd and $x\in\mathbb Z_p$ is not a negative integer. If $x\equiv-1\pmod p$ then $p\mid\pi_j(x)$ for all $j\ge1$, so $S_e(x)\equiv1$ and no path of length $\ge1$ is alive; such $x$ play no role.

**Lemma 11.1 (valuations; linearisation) [proved].**
- (a) $V_n\ge v(n!)=(n-s_p(n))/(p-1)\ge n/(p-1)-\log_pn-1$.
- (b) For $n<N$: $V_N-V_n<(N-n)/(p-1)+M_N$.
- (c) $V_j-V_n\ge\lfloor(j-n)/p\rfloor$ for $j\ge n$.
- (d) $v(\pi_j^{[i]}(x))\ge V_j-iM_j$.
- (e) For $S\in\mathbb Z_p[X]$ and $y,h\in\mathbb Z_p$: $S(y+h)=\sum_iS^{[i]}(y)h^i$ with $S^{[i]}(y)\in\mathbb Z_p$.
- (f) If $n\ge2p$ then $M_n<V_n$.
- (g) *(Linearisation.)* Let $n<N$, $m=V_n(x)$, $D=V_N(x)-m$, and assume $M_N(x)<m$. Let $C=x+p^m\mathbb Z_p$ with normalised Haar measure, fix $x_0\in C$ and write $x'=x_0+p^mw$. Put $Q_f=\sum_{j=n}^{N-1}f_j\pi_j/\pi_n\in\mathbb Z[X]$ for $f\in\{0,1\}^{N-n}$. Then (i) $v(x'+i)=v(x+i)$ for $i\le N$, so $V_n,V_N,M_n,M_N$ are constant on $C$, and so are aliveness at $n$, $S_e^{[i]}\bmod p^m$, $Q_f\bmod p^m$ and the unit parts $(x'+i)/p^{v(x+i)}\bmod p^{m-M_N}$; (ii) if $e$ is alive at $n$, then with $\omega=\pi_n(x_0)/p^m\in\mathbb Z_p^\times$,
$$\tau_n(e,x')\equiv\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)\,w\pmod{p^{m-M_n}};$$
(iii) $(e,f)$ is alive at $N$ iff $e$ is alive at $n$ and $\tau_n(e,x')\equiv Q_f(x')\pmod{p^D}$, and then $\tau_N((e,f),x')=(\tau_n(e,x')-Q_f(x'))\,\pi_n(x')/\pi_N(x')$.

*Proof.* (a) At least $\lfloor n/p^k\rfloor$ of $n$ consecutive elements of $\mathbb Z_p$ are divisible by $p^k$; sum over $k$ (Legendre), and $s_p(n)\le(p-1)(\log_pn+1)$. (b) Among $x+n+1,\dots,x+N$ at most $(N-n)/p^k+1$ are divisible by $p^k$, and none by $p^{M_N+1}$; sum over $k\le M_N$. (c) One of any $p$ consecutive elements is divisible by $p$. (d) $\pi_j^{[i]}=\pi_j\,e_i(1/(x+1),\dots,1/(x+j))$, and every monomial of the elementary symmetric polynomial $e_i$ has valuation $\ge-iM_j$. (e) Taylor's formula; $S^{[i]}$ has coefficients in $\mathbb Z_p$. (f) Two of $x+1,\dots,x+n$ are divisible by $p$; $V_n$ is the sum of all the valuations, $M_n$ the largest. (g)(i) $v(x'-x)\ge m>M_N\ge v(x+i)$; the rest is reduction of integer polynomials mod $p^m$. (ii) With $h=p^mw$: $S_e(x')=S_e(x_0)+hS_e'(x_0)+h^2R$, $R\in\mathbb Z_p$, and $\pi_n(x')=\pi_n(x_0)(1+E)$ with $v(E)\ge m-M_n\ge1$. As $p^m\mid S_e(x_0)$, $\tau_n(e,x')=[\tau_n(e,x_0)-\omega^{-1}S_e'(x_0)w-\omega^{-1}p^mw^2R](1+E)^{-1}$ with the bracket in $\mathbb Z_p$. (iii) $S_{(e,f)}=\pi_n\,(Q_f-\tau_n(e,\cdot))$ (using backward integrality for "only if") and $V_N=m+D$. ∎

*Frozen-state weights.* For $\lambda\ge0$ and $t\in\mathbb Z/p^\lambda$ put
$$a_n^{(\lambda)}(t)=\mathbb P_{f\in\{0,1\}^{p\lambda}}\Big(\sum_{i<p\lambda}f_i\frac{\pi_{n+i}(x)}{\pi_n(x)}\equiv t\ (p^\lambda)\Big),\qquad\rho_n(e)=p^{\lambda_e}a_n^{(\lambda_e)}\big(\tau_n(e,x)\bmod p^{\lambda_e}\big).$$
$a_n^{(\lambda)}$ depends only on $n,\lambda$ and $x\bmod p^\lambda$, sums to $1$ over $t$, and takes values in $2^{-p\lambda}\mathbb Z$. By Lemma 11.1(c) the terms with $i\ge p\lambda$ vanish mod $p^\lambda$, so for $N-n\ge p\lambda$
$$a_n^{(\lambda)}(t)=\mathbb P_{f\in\{0,1\}^{N-n}}\big(Q_f(x)\equiv t\ (p^\lambda)\big).\tag{$*$}$$
For $\lambda=0$, $\rho\equiv1$; in general $\rho$ is not constant (e.g. $p=3$, $\lambda=1$, $x+n\equiv0\pmod3$: $a=(\tfrac12,\tfrac14,\tfrac14)$).

**Proposition 11.2 (one-window identity at odd $p$; affine profile) [proved].** In the setting of Lemma 11.1(g), let $L\ge0$ and assume
$$\text{(W1) }N-n\ge p(L+1),\qquad\text{(W2) }D+L\le m-M_n,\qquad\text{(W3) }L<m-M_N.$$
Let $P^L_n=\{e\text{ alive at }n:\lambda_e\le L\}$, $e\in P^L_n(x)$, $\lambda=\lambda_e$. Then:
- (i) membership in $P^L_n$ is constant on $C$; every child $(e,f)$ alive at $N$ at any $x'\in C$ has slope $\lambda$; every $e''\in P^L_N(x')$ has $e''|_n\in P^L_n(x)$;
- (ii) $s_e:=\tau_n(e,x')\bmod p^\lambda$ is constant on $C$;
- (iii) write $\tau_n(e,x_0)\bmod p^{D+\lambda}=s_e+p^\lambda\theta_e$ ($\theta_e\in\mathbb Z/p^D$), $\beta_e=\omega^{-1}S'_e(x_0)/p^\lambda\in(\mathbb Z/p^D)^\times$, $q_f=Q_f(x_0)\bmod p^{D+\lambda}$, $u=\pi_N(x_0)/(p^D\pi_n(x_0))\bmod p^\lambda$, and for $y\in\mathbb Z/p^D$
$$\Phi_{\lambda,s}(y)=\sum_{f}\mathbf 1\big[q_f\equiv s+p^\lambda y\ (p^D)\big]\;p^\lambda a_N^{(\lambda)}\Big(u^{-1}\tfrac{s+p^\lambda y-q_f}{p^D}\bmod p^\lambda\Big).$$
Then for every digit block $w\in\mathbb Z/p^D$, the weighted child sum $X_e(w):=\sum_{f:(e,f)\text{ alive at }N}\rho_N((e,f))$ at $x'=x_0+p^mw$ equals $\Phi_{\lambda,s_e}(\theta_e-\beta_ew)$;
- (iv) $\mathbb E_wX_e=2^{N-n}p^{-D}\rho_n(e)$, and for each state $s\in\mathbb Z/p^\lambda$, $\mathbb E_{x'\in C}\#\{f:(e,f)\text{ alive at }N,\ \tau_N\equiv s\ (p^\lambda)\}=2^{N-n}p^{-D}a_n^{(\lambda)}(s_e)$.

*Proof.* By (W1) and Lemma 11.1(c), $D\ge L+1>\lambda$. (i) $S'_{(e,f)}=S'_e+\sum_{n\le j<N}f_j\pi'_j$, and $v(\pi_j'(x'))\ge V_j-M_j\ge m-M_N>L$ by Lemma 11.1(d) and (W3); so a child of a slope-$\lambda$ parent ($\lambda\le L$) has slope $\lambda$, and a parent of slope $>L$ has children of slope $>L$ only. "Slope $\le L$" is constant on $C$ because $S_e'\bmod p^m$ is and $L<m$; with backward integrality this gives (i). (ii) $\lambda\le L\le m-M_n$ by (W2); apply Lemma 11.1(g)(ii) mod $p^\lambda$. (iii) By (W2), $D+\lambda\le m-M_n$, so $t(w):=\tau_n(e,x')\bmod p^{D+\lambda}=s_e+p^\lambda(\theta_e-\beta_ew)$. $q_f$ is constant on $C$ since $D+\lambda\le m$; $u$ is constant since $\lambda<m-M_N$ (Lemma 11.1(g)(i)). By Lemma 11.1(g)(iii) the child $(e,f)$ is alive iff $t(w)\equiv q_f\pmod{p^D}$, and then $\tau_N\equiv u^{-1}(t(w)-q_f)/p^D\pmod{p^\lambda}$; its weight is $p^\lambda a_N^{(\lambda)}(\tau_N\bmod p^\lambda)$, where $a_N^{(\lambda)}$ is constant on $C$. Summing over $f$ gives the formula. (iv) $w\mapsto\theta_e-\beta_ew$ is a bijection of $\mathbb Z/p^D$, so $\mathbb E_wX_e=p^{-D}\sum_y\Phi_{\lambda,s_e}(y)$. Fix $f$. If $q_f\not\equiv s_e\pmod{p^\lambda}$ no $y$ contributes (as $D\ge\lambda$). Otherwise the congruence fixes $y\bmod p^{D-\lambda}$, leaving $p^\lambda$ values of $y$, for which $(s_e+p^\lambda y-q_f)/p^D$ runs once through $\mathbb Z/p^\lambda$; so $f$ contributes $p^\lambda\sum_ta_N^{(\lambda)}(t)=p^\lambda$. By $(*)$ (valid as $N-n\ge p\lambda$) the number of such $f$ is $2^{N-n}a_n^{(\lambda)}(s_e)$. The state-by-state statement is the same count with the weight replaced by the indicator of the state. ∎

*Window scheme and filtration.* Fix $L\ge0$, $1<r<2$ and $n_0\ge2p$, and put $n_{\ell+1}=\max(\lfloor rn_\ell\rfloor,\ n_\ell+p(L+1))$, so (W1) holds for every window $[n_\ell,n_{\ell+1})$. Let $m_\ell=V_{n_\ell}(x)$, $A_\ell(x)=x+p^{m_\ell}\mathbb Z_p$, $D_\ell=m_{\ell+1}-m_\ell$, and let $\mathcal G_\ell$ be generated by the sets $A_\ell(x)$. The *window hypotheses* are
$$\mathcal C_\ell:\quad\text{(W2) }D_\ell+L\le m_\ell-M_{n_\ell},\qquad\text{(W3) }L<m_\ell-M_{n_{\ell+1}},\qquad\text{(ENV) }M_{n_{\ell+1}}<m_\ell .$$
For $j\ge0$ let $\sigma_j=\min\{\ell\ge j:\mathcal C_\ell\text{ fails}\}$ and
$$M_\ell=2^{-n_\ell}p^{m_\ell}\sum_{e\in P^L_{n_\ell}(x)}\rho_{n_\ell}(e)\ (j\le\ell\le\sigma_j),\qquad M_\ell=M_{\sigma_j}\ (\ell\ge\sigma_j),\qquad M_\ell\equiv0\ (\ell\ge j)\text{ on }\{\sigma_j=j\}.$$

**Theorem 11.3 (quenched martingale at odd $p$) [proved].**
- (a) *(Atoms.)* The sets $A_\ell(x)$ partition $\mathbb Z_p$ minus the negative integers, $A_{\ell+1}(x)\subseteq A_\ell(x)$, and $m_\ell$ is constant on $A_\ell(x)$; so $(\mathcal G_\ell)$ is a filtration. Each $\mathcal C_\ell$ is $\mathcal G_\ell$-measurable.
- (b) $(M_\ell)_{\ell\ge j}$ is a nonnegative $(\mathcal G_\ell)$-martingale, and $M_\ell=0$ implies $M_{\ell+1}=0$.
- (c) If $\sigma_j(x)=\infty$ and $M_\ell(x)>0$ for all $\ell\ge j$, then $x\in K_p$.
- (d) For $\mu$-a.e. $x$, $\mathcal C_\ell(x)$ holds for all large $\ell$, and in fact $M_{n_\ell}(x)<3\log_pn_\ell$ for all large $\ell$. Hence $\mu(\sigma_j<\infty)\downarrow0$ as $j\to\infty$, and for every $\varepsilon>0$ the atoms $A$ of $\mathcal G_j$ with $\mu_A(\sigma_j<\infty)\ge\varepsilon$ have total measure at most $\mu(\sigma_j<\infty)/\varepsilon$.

*Proof.* (a) By Lemma 11.1(f), $M_{n_\ell}<m_\ell$, so $v(y+i)=v(x+i)$ for $y\in A_\ell(x)$, $i\le n_\ell$; hence $m_\ell(y)=m_\ell(x)$ and $A_\ell(y)=A_\ell(x)$. Nesting follows from $m_{\ell+1}\ge m_\ell$. For (ENV): if $v(x+i)<m_\ell$ then $v(y+i)=v(x+i)$, and if $v(x+i)\ge m_\ell$ then $v(y+i)\ge m_\ell$; so (ENV) is constant on the atom, and under (ENV) all $v(y+i)$, $i\le n_{\ell+1}$, hence $D_\ell$ and $M_{n_{\ell+1}}$, are constant. (b) *Measurability on $\{\sigma_j\ge\ell\}$.* Aliveness at $n_\ell$ is constant on $A_\ell$ (Lemma 11.1(g)(i)); "$\lambda_e\le L$" is constant since $L<m_\ell$; $\tau_{n_\ell}(e)\bmod p^{\lambda_e}$ is constant by Lemma 11.1(g)(ii) provided $\lambda_e\le m_\ell-M_{n_\ell}$, which is (W2) of window $j$ if $\ell=j$, and follows from (W3) of window $\ell-1$ if $\ell>j$ ($L<m_{\ell-1}-M_{n_\ell}\le m_\ell-M_{n_\ell}$); finally $a^{(\lambda)}_{n_\ell}$ depends on $x\bmod p^\lambda$ with $\lambda<m_\ell$. After $\sigma_j$ the process is frozen. *Martingale property.* On $\{\sigma_j>\ell\}$, Proposition 11.2 applies on $A_\ell(x)$ with $(n,N,m,D)=(n_\ell,n_{\ell+1},m_\ell,D_\ell)$. By 11.2(i), $P^L_{n_{\ell+1}}(x')$ is the disjoint union over $e\in P^L_{n_\ell}$ of the alive children of $e$, so $M_{\ell+1}=2^{-N}p^{m+D}\sum_eX_e(w)$, where $w$, the digit block of $x'$ at positions $m,\dots,m+D-1$, is uniform on $\mathbb Z/p^D$ under $\mu_{A_\ell(x)}$. By 11.2(iv), $\mathbb E[M_{\ell+1}\mid\mathcal G_\ell]=2^{-N}p^{m+D}\sum_e2^{N-n}p^{-D}\rho_n(e)=M_\ell$. *Zero is absorbing.* If $M_\ell=0$ on $\{\sigma_j>\ell\}$, every parent has $a_{n}^{(\lambda_e)}(s_e)=0$, i.e. no $f$ with $q_f\equiv s_e\pmod{p^{\lambda_e}}$; a child needs $q_f\equiv t(w)\equiv s_e$, so there is none and $M_{\ell+1}=0$. (c) Then $P^L_{n_\ell}(x)\ne\emptyset$ for all $\ell\ge j$, so (backward integrality) alive paths exist at every length. The alive finite paths form a finitely branching tree with nodes at every level; König's lemma gives an infinite branch $e$, and $v(S_{e|_n}(x))\ge V_n(x)\to\infty$ (Lemma 11.1(a)), so $F_e(x)=0$ and $x\in K_p$ by Proposition 1.2. (d) $\mu\{\exists i\le n:v(x+i)\ge K\}\le np^{-K}$. With $K_\ell=\lceil3\log_pn_\ell\rceil$ this is $\le n_\ell^{-2}$, summable as $n_\ell\ge n_0+\ell p(L+1)$. By Borel–Cantelli, a.e. $x$ has $M_{n_\ell}\le K_\ell-1<3\log_pn_\ell$ for all large $\ell$ (detail added: $M<\lceil c\rceil$ for an integer $M$ gives $M<c$). For such $\ell$, Lemma 11.1(a),(b) give $m_\ell\ge n_\ell/(p-1)-\log_pn_\ell-1$ and $D_\ell<(r-1)n_\ell/(p-1)+O(\log n_\ell)$ (for large $\ell$, $n_{\ell+1}=\lfloor rn_\ell\rfloor$); since $r-1<1$, (W2), (W3) and (ENV) hold once $n_\ell$ is large. The events $\{\sigma_j<\infty\}$ decrease in $j$ to a null set; the last claim is Markov's inequality applied to $\mu(\sigma_j<\infty)=\sum_A\mu(A)\mu_A(\sigma_j<\infty)$. ∎

*Remark (what differs from $p=2$).* Nothing in the martingale half. The normaliser $2^{-n}p^{V_n}\approx(p^{1/(p-1)}/2)^n$ decays because $p^{1/(p-1)}<2$ for $p\ge3$: the expected weighted population grows exponentially (supercritical), and the extinction argument of §10.1 is unavailable. The question is whether $M_\ell$ has a nonzero limit with positive probability.

**Theorem 11.4 ($L^2$ criterion) [proved].** Let $A$ be an atom of $\mathcal G_j$ with $M_j(A)>0$ (so $\mathcal C_j$ holds on $A$). Suppose that for some $\Lambda\ge1$
$$\text{(E1) }\sup_{\ell\ge j}\mathbb E_A[M_\ell^2]\le\Lambda M_j(A)^2,\qquad\text{(E2) }\mu_A(\sigma_j<\infty)<1/\Lambda .$$
Then $\mu(K_p\cap A)\ge\mu(A)\,\big(1/\Lambda-\mu_A(\sigma_j<\infty)\big)>0$.

*Proof.* On $(A,\mu_A)$, $(M_\ell)$ is an $L^2$-bounded martingale, so it converges a.s. and in $L^2$ to $M_\infty\ge0$ with $\mathbb E_AM_\infty=M_j(A)$ and $\mathbb E_AM_\infty^2\le\Lambda M_j(A)^2$. By Cauchy–Schwarz, $\mathbb E_AM_\infty\le(\mathbb E_AM_\infty^2)^{1/2}\mu_A(M_\infty>0)^{1/2}$, so $\mu_A(M_\infty>0)\ge1/\Lambda$. On $\{M_\infty>0\}$, $M_\ell>0$ for all $\ell$ (zero is absorbing), so on $\{M_\infty>0,\ \sigma_j=\infty\}$ Theorem 11.3(c) gives $x\in K_p$. ∎

By Theorem 11.3(d), for each *fixed* $\Lambda$, (E2) holds on all but a vanishing proportion (in measure) of the atoms of $\mathcal G_j$ as $j\to\infty$. The content is (E1) with a $\Lambda$ that does not grow with the atom. Whether an atom exists with $M_j(A)>0$, (E1) and (E2) together is the open question (see the Remark after Theorem 11.7).

*Window relative variance.* For an atom $A'$ of $\mathcal G_\ell$ with $\mathcal C_\ell$ and $M_\ell(A')>0$ put $\Sigma(w)=\sum_{e\in P^L_{n_\ell}}X_e(w)$ and $R_\ell(A')=\mathrm{Var}_w\Sigma/(\mathbb E_w\Sigma)^2$ (and $R_\ell=0$ if $M_\ell=0$). Since $M_{\ell+1}=2^{-N}p^{m+D}\Sigma(w)$ and $M_\ell=2^{-N}p^{m+D}\mathbb E_w\Sigma$,
$$\mathbb E[M_{\ell+1}^2\mid\mathcal G_\ell]=M_\ell^2(1+R_\ell)\qquad\text{on }\{\sigma_j>\ell\}.\tag{11.1}$$

**Corollary 11.5 (summable relative variances) [proved].** Let $A$ be an atom of $\mathcal G_j$ with $M_j(A)>0$, and let $\bar R_\ell$ be the supremum of $R_\ell(A')$ over atoms $A'\subseteq A$ of $\mathcal G_\ell$ on which $\mathcal C_j,\dots,\mathcal C_\ell$ hold. If $\sum_\ell\bar R_\ell<\infty$, then (E1) holds with $\Lambda=\prod_{\ell\ge j}(1+\bar R_\ell)$. Hence *Hypothesis H(p)* — there are $L,r,n_0,j$, an atom $A$ with $M_j(A)>0$, and summable $c_\ell\ge\bar R_\ell$ with $\mu_A(\sigma_j<\infty)<\prod(1+c_\ell)^{-1}$ — implies $\mu(K_p)>0$.

*Proof.* By (11.1), $\mathbb E_A[M_{\ell+1}^2]=\mathbb E_A[M_\ell^2(1+R_\ell\mathbf 1_{\sigma_j>\ell})]\le(1+\bar R_\ell)\mathbb E_A[M_\ell^2]$; induct from $\mathbb E_A[M_j^2]=M_j(A)^2$ and apply Theorem 11.4. ∎

**Theorem 11.6 (exact one-window second moment: Fourier × Weyl structure) [proved].** On an atom satisfying the window hypotheses, write $\Phi_e=\Phi_{\lambda_e,s_e}$, $\widehat F(\zeta)=\sum_{y\in\mathbb Z/p^D}F(y)e(-\zeta y/p^D)$ with $e(t)=e^{2\pi it}$, and $y^*_e=\theta_e\beta_e^{-1}$ (the *phase point* of $e$). Then
$$\mathrm{Var}_w\Sigma=p^{-2D}\sum_{0\ne\eta\in\mathbb Z/p^D}\Big|\sum_ee\big(-\eta y^*_e/p^D\big)\,\widehat\Phi_e(-\eta\beta_e^{-1})\Big|^2 .$$
Grouping the parents into classes $c$ with equal $(\lambda,s,\beta\bmod p^D)$, with weights $\pi_c=\rho_c|c|/\sum_e\rho_e$, normalised profiles $\hat\varphi_c=\widehat\Phi_c/\widehat\Phi_c(0)$ and class Weyl sums $w_c(\eta)=|c|^{-1}\sum_{e\in c}e(-\eta y^*_e/p^D)$,
$$R=\sum_{\eta\ne0}\Big|\sum_c\pi_c\,\hat\varphi_c(-\eta/\beta_c)\,w_c(\eta)\Big|^2\le\sum_c\pi_c\sum_{\zeta\ne0}|\hat\varphi_c(\zeta)|^2\,|w_c(-\beta_c\zeta)|^2 .$$

*Proof.* Substituting $y=\theta_e-\beta_ew$ (a bijection) gives $\widehat{X_e}(\eta)=e(-\eta\beta_e^{-1}\theta_e/p^D)\,\widehat\Phi_e(-\eta\beta_e^{-1})$; sum over $e$ and use Parseval on $\mathbb Z/p^D$ ($\mathrm{Var}=p^{-2D}\sum_{\eta\ne0}|\widehat\Sigma(\eta)|^2$). For the class form, $\rho_e$ depends only on $(\lambda_e,s_e)$, $\widehat\Phi_c(0)=\sum_y\Phi_c(y)=2^{N-n}\rho_c$ (proof of 11.2(iv)) and $\mathbb E_w\Sigma=2^{N-n}p^{-D}\sum_e\rho_e$; the inequality is Jensen's ($\sum_c\pi_c=1$). Classes with $\rho_c=0$ have $X_e\equiv0$ and are omitted. ∎

So the correlation between parents is exactly "window Fourier coefficients times Weyl sums of the parents' phase points". The quantity measured below is the *aggregate correlation ratio* $\kappa=\mathrm{Var}_w\Sigma/\sum_e\mathrm{Var}_wX_e$ together with the single-parent relative variances $r_e=\mathrm{Var}_wX_e/\mu_e^2$, $\mu_e=\mathbb E_wX_e$, and $r^{\max}=\max_{\mu_e>0}r_e$. (For $\lambda_e=0$, $r_e=\sum_{\zeta\ne0}|\hat h_D(\zeta)|^2$ with $\hat h_D(\zeta)=\prod_{n\le j<N}\tfrac12(1+e(-\zeta\pi_j(x_0)/(\pi_n(x_0)p^D)))$: the $L^2$ Fourier mass of the window map.)

**Theorem 11.7 (a cleaner sufficient condition, H′(p)) [proved].** Run the martingale with $\mathcal C'_\ell=\mathcal C_\ell\wedge\{M_{n_\ell}\le3\log_pn_\ell\}$ in place of $\mathcal C_\ell$ (still $\mathcal G_\ell$-measurable, and still true for all large $\ell$ for a.e. $x$ by Theorem 11.3(d)). Let $A$ be an atom of $\mathcal G_j$ with $M_j(A)>0$, and suppose $\kappa_\ell(A')\,r^{\max}_\ell(A')\le K$ for all $\ell\ge j$ and all atoms $A'\subseteq A$ of $\mathcal G_\ell$ on which $\mathcal C'_j,\dots,\mathcal C'_\ell$ hold. Then
$$\sup_{\ell\ge j}\mathbb E_A[M_\ell^2]\le M_j(A)^2+p^LK\,M_j(A)\,S_j,\qquad S_j=\sum_{\ell\ge j}\Big(\frac{p^{1/(p-1)}}2\Big)^{n_\ell}n_\ell^3<\infty,$$
so (E1) holds with $\Lambda=1+p^LKS_j/M_j(A)$, and $\mu(K_p\cap A)>0$ whenever $\mu_A(\sigma_j<\infty)<1/\Lambda$.

*Proof.* On an unfrozen atom, with $n=n_\ell$, $N=n_{\ell+1}$, $m=m_\ell$: $M_\ell^2R_\ell=(2^{-N}p^{V_N})^2\mathrm{Var}_w\Sigma\le(2^{-N}p^{V_N})^2\kappa\,r^{\max}\sum_e\mu_e^2$ (parents with $\mu_e=0$ have $X_e\equiv0$). Now $\sum_e\mu_e^2\le\max_e\mu_e\sum_e\mu_e$, $\max_e\mu_e=2^{N-n}p^{-D}\max_e\rho_e\le2^{N-n}p^{-D}p^L$ (as $\rho_e\le p^{\lambda_e}$), and $\sum_e\mu_e=\mathbb E_w\Sigma=2^Np^{-V_N}M_\ell$. Multiplying out, $M_\ell^2R_\ell\le p^LK\,2^{-n}p^mM_\ell$. By Lemma 11.1(b) and $\mathcal C'_\ell$, $p^m<p^{n/(p-1)}p^{M_n}\le p^{n/(p-1)}n^3$. By (11.1), $\mathbb E_A[M^2_{\ell+1}]-\mathbb E_A[M^2_\ell]=\mathbb E_A[M_\ell^2R_\ell\mathbf 1_{\sigma_j>\ell}]\le p^LK(p^{1/(p-1)}/2)^{n_\ell}n_\ell^3\,\mathbb E_A[M_\ell]$, and $\mathbb E_A[M_\ell]=M_j(A)$. Sum over $\ell$; $S_j<\infty$ because $p^{1/(p-1)}<2$ for $p\ge3$ and $n_\ell$ grows at least linearly. ∎

Since $S_j\to0$, under a uniform $K$ the constant $\Lambda$ tends to $1$ on atoms with $M_j(A)$ bounded below; the martingale limit would then be positive on essentially the whole survival set.

*Remark (what Theorem 11.7 does not give) [observations; no impossibility is claimed; the size estimate is heuristic].* *[Corrected, round-3 referee.]* Theorem 11.7 is a statement about one given atom $A$, and it needs both $M_j(A)>0$ and $\mu_A(\sigma_j<\infty)<1/\Lambda(A)$ with $\Lambda(A)=1+p^LKS_j/M_j(A)$. A uniform bound on $\kappa\,r^{\max}$ does not by itself produce such an atom. Three natural shortcuts fail.
- Theorem 11.3(d) bounds only the total measure of atoms with large freezing probability, by about $\mu(\sigma_j<\infty)/\varepsilon$.
- Summing Theorem 11.7 over all atoms gives only $\mu(K_p)\ge\sum_A\mu(A)\big(M_j(A)/(M_j(A)+p^LKS_j)-\mu_A(\sigma_j<\infty)\big)$. The only proved lower bound on $\mu(M_j>0)$ is exponentially small (Corollary 11.20).
- Shrinking atoms around a point of $K_p$ needs that point to satisfy $\mathcal C'_\ell$ eventually, which is not known.

Size of the condition [heuristic]: $2^{-n}p^m\approx(p^{1/(p-1)}/2)^n$ up to factors polynomial in $n$, so $S_j/M_j(A)\approx\mathrm{poly}(n_j)/\sum_{e\in P^L_{n_j}}\rho(e)$, of order $n_j^4$ divided by the weighted population. The atom must therefore carry a weighted population $\gg p^LKn_j^4$ and freeze with probability below about $1/\Lambda$. $M_j(A)$ is a finite computation, and $\mu_A(\sigma_j<\infty)$ can be bounded above by the explicit union bound in the proof of Theorem 11.3(d). So for a given $K$, the condition could in principle be certified on a single atom. The data of track T1a ($|P^L|\le89\,168$ at $n\le86$ for $p=3$) are far from this range.

**Proposition 11.8 (the children's phase points) [sketch; main identity checked by the lead, hypothesis bookkeeping not re-verified].** Strengthen (W2), (W3) to $D+D'+L\le m-M_n$ and $D'+L<m-M_N$, where $D'$ is the depth of the next window. For a parent $e$ of slope $\lambda$ let $t^+_e(w)=\tau_n(e,x_0)-p^\lambda\beta_ew\in\mathbb Z/p^{D+D'+\lambda}$ and $u'=\pi_N(x_0)/(p^D\pi_n(x_0))\bmod p^{D'+\lambda}$. Then the child $(e,f)$ has $\beta_{(e,f)}\equiv\beta_eu'^{-1}$ and phase point $y^*_{(e,f)}=(\zeta-u's')/(p^\lambda\beta_e)\bmod p^{D'}$, where $\zeta=(t^+_e(w)-q_f)/p^D$ and $s'=u'^{-1}\zeta\bmod p^\lambda$. Consequently the $\rho$-weighted Weyl sum of the children of $e$ at order $p^d$ ($d\le D'$) is
$$W_e(\xi,d;w)=p^{-K}\sum_{\chi\in\mathbb Z/p^K}\hat g_e(\chi\bmod p^{\lambda+d})\,e\big(\chi t^+_e(w)/p^K\big)\,\widehat S(\chi),\qquad K=D+\lambda+d,$$
with $\widehat S(\chi)=\prod_{n\le j<N}\big(1+e(-\chi\pi_j(x_0)/(\pi_n(x_0)p^K))\big)$ the window's subset-sum transform at precision $p^K$ and $g_e$ an explicit function on $\mathbb Z/p^{\lambda+d}$. (The identity is Fourier inversion of $G_e(z)=\mathbf 1[p^D\mid z]\,g_e(z/p^D)$ on $\mathbb Z/p^K$, summed over $f$; the lead checked this computation and the formula for $y^*$. The constancy statements at the higher precision are claimed to follow from the strengthened hypotheses exactly as in Proposition 11.2; the lead did not re-check them in detail.)

**Remark 11.9 (why supremum bounds cannot close an induction on Weyl sums) [proved facts; the interpretation is heuristic].** Proposition 11.8 suggests an induction on "(weighted population, Weyl sums of targets)", with normalised contraction factor $p^D\max_\chi|\widehat S(\chi)|/2^{N-n}$. A complete block of $p$ elements following a multiple of $p$ contributes a factor $\prod_{r<p}|\cos(\pi\chi'r!/p^k)|$ at some scale $k\ge1$. At $k=1$ its supremum over units $\chi'$ is $c_p$ ($=1/8$, $0.1324$, $0.0824$, $0.0267$, $0.0033$ for $p=3,5,7,11,13$; computed in §11.6), and for the worst incomplete block (the two units $(p-2)!,(p-1)!\equiv-(p-2)!$) it is $\cos^2(\pi/p)$. At scale $k\ge2$, taking $\chi'=1$ makes every phase $r!/p^k$ small, so the supremum tends to $1$ as $k\to\infty$. Hence block-by-block supremum bounds give no contraction at deep scales — the same obstruction as Corollary 10.20 and the barrier lemma (Theorem 3.10). *[heuristic]* With square-root cancellation in the lifted-frequency sum the factor would be $\approx p^{D/2+\lambda}2^{-(N-n)/2}<1$ for long windows at every $p\ge3$; without that cancellation it would be $\approx p^{D+\lambda}2^{-(N-n)/2}$, which needs $2^{p-1}>p^2$, i.e. $p\ge7$. The needed input is cancellation driven by the deep $p$-adic digits of the unit parts of $\pi_j(x_0)/\pi_n(x_0)$ — the same missing input as RMF (Theorem 10.16).

*The route "$\mu\{x:-1\in A'_x\}>0$".* By Proposition 11.21 below, $-1\in A'_x$ iff $x\in K_p$, so this is a restatement. Its natural moment method is the annealed second moment of §11.6. That moment satisfies $\mathbb EZ_G^2\ge p^G/4$ at every prime (Proposition 11.53, [proved]). Together with first moments that grow only linearly in $G$ (Computation 11.55; [computer-assisted], small $G$ only), this makes the untruncated annealed second moment useless for $\mu(K_p)>0$ [heuristic], which is one reason why the criterion above is quenched. Truncated moments are not ruled out. *[Qualified after the round-3 re-check, as in §11.6.]*

**Conjecture 11.10 (H′(p)) [conjecture].** *[Corrected, round-3 referee: the atom condition (b) was missing.]* For every odd $p$ there are $L,r,n_0,j$, a constant $K$ and an atom $A$ of $\mathcal G_j$ such that:
- (a) $\kappa_\ell(A')\,r^{\max}_\ell(A')\le K$ for all $\ell\ge j$ and all atoms $A'\subseteq A$ of $\mathcal G_\ell$ on which $\mathcal C'_j,\dots,\mathcal C'_\ell$ hold;
- (b) $M_j(A)>0$ and $\mu_A(\sigma_j<\infty)<1/\Lambda$, with $\Lambda=1+p^LKS_j/M_j(A)$ (as in Theorem 11.7, $\sigma_j$ refers to the conditions $\mathcal C'_\ell$).

By Theorem 11.7, H′(p) gives $\mu(K_p\cap A)>0$, hence $\mu(K_p)>0$ (Conjecture 5.2). Part (a) alone, even with $K$ uniform over all atoms of all levels, is not known to imply $\mu(K_p)>0$ (Remark after Theorem 11.7). The evidence below concerns (a) only.

*Evidence [computer-assisted statistics; the reading is heuristic].* Track T1a's program `winvar.c` keeps exact residues mod $p^P<2^{126}$ for every alive path and computes, on each window, the exact affine profiles, $\mathbb E_w\Sigma$ (checked against $2^{N-n}p^{-D}\sum\rho$: no discrepancy above $10^{-6}$ relative occurred), $\mathrm{Var}_w\Sigma$ by enumerating all $p^D$ digit blocks, $\kappa$, and the $\rho$-weighted Weyl sums of the phase points. It agrees to all printed digits with the independent exact-rational Python brute force `window_exact2.py` on four windows ($p=3,5,7$). Over the windows on which the hypotheses hold:

| $p$ | windows | $\lvert P^L\rvert$ | $R$ | $R\,\lvert P^L\rvert$ (median) | $\kappa$ | $W_1\sqrt{\lvert P^L\rvert}$ (median) |
|---|---|---|---|---|---|---|
| 3 | 24 | 10–89 168 | $4\cdot10^{-6}$–$1.2\cdot10^{-2}$ | 0.04–4.3 (0.22) | 0.10–2.1 | 0.19–3.6 (0.90) |
| 5 | 26 | 68–528 488 | $2.4\cdot10^{-7}$–$3.7\cdot10^{-3}$ | 0.0007–7.6 (0.20) | 0.02–6.3 | 0.25–2.6 (1.16) |
| 7 | 16 | 96–201 780 | $9\cdot10^{-7}$–$7.6\cdot10^{-3}$ | 0.01–1.2 (0.43) | 0.04–9.7 | 0.24–2.8 (1.00) |

($W_1$ is the normalised $\rho$-weighted Weyl sum of all parents' phase points at order $p$.) So $R$ decays geometrically along trajectories with $R|P^L|=O(1)$, $\kappa$ stays in $[0.02,10]$, and the Weyl sums show square-root cancellation. An atom Monte Carlo (150–200 samples of the digits above an atom; 19 atoms) finds $\mathbb E[M_\ell]$ constant within error and $\mathbb E[M_\ell^2]$ flat with geometrically decaying increments (e.g. $p=3$: $3.134,3.104,3.110,3.112$, increments $1.0\cdot10^{-2},1.6\cdot10^{-3},2.4\cdot10^{-4}$). *Limits:* $n\le86$ ($p=3$), $\le50$ ($p=5$), $\le37$ ($p=7$), $M_n\le5$; no deep gates were reached, and the supremum in H′(p) runs over deep-gate atoms too. At $p=7$ the accessible windows are too shallow for (W2) with $L=1$ except on all-slope-0 atoms. (The appendix tables of the track report mislabel two columns — the first column is $p$, not $L$ — a presentational slip in its `summarize.py`; the logs are unaffected.)

### 11.2 The fine structure of $K_p$: a perfect kernel and Hausdorff dimension (track T1b)

Here $p$ is any prime, a *word* is $e\in\{0,1\}^{\mathbb Z_{\ge0}}$ with $e_0=1$, and $Z(F)$ is the zero set in $\mathbb Z_p$. By Proposition 1.2, $K_p=\bigcup_eZ(F_e)$.

**Theorem 11.11 (each $F_e$ is a restricted power series on every residue disc; finitely many zeros) [proved].**
- (a) For $0\le i\le j$ and all $x\in\mathbb Z_p$: $\pi_j^{[i]}(x)=\sum_{I\subseteq[1,j],|I|=j-i}\prod_{l\in I}(x+l)$, and $v(\pi_j^{[i]}(x))\ge\lfloor j/p\rfloor-i$. If $x\notin\{-1,\dots,-j\}$ then $v(\pi_j^{[i]}(x))\ge v(\pi_j(x))-iM_j(x)$.
- (b) For every word $e$ and $i\ge0$ the series $F_e^{[i]}=\sum_je_j\pi_j^{[i]}$ converges uniformly on $\mathbb Z_p$, and $F_e(x+h)=\sum_{i\ge0}F_e^{[i]}(x)h^i$ for all $x\in\mathbb Z_p$, $h\in p\mathbb Z_p$. So $u\mapsto F_e(x+pu)$ lies in $\mathbb Z_p\langle u\rangle$, $F_e$ is locally analytic, and $F_e'=F_e^{[1]}$.
- (c) $Z(F_e)$ is finite, and at each $x\in Z(F_e)$ some $F_e^{[k]}(x)\ne0$; the least such $k\ge1$ is the *multiplicity*. The set $\{(x,e):F_e(x)=0\}$ is compact and $K_p$ is its projection.

This extends Lemma 10.3 (which needed $p=2$ and $x\in\Omega$) to all $p$ and all $x$.

*Proof.* (a) Expand $\prod_l((x+l)+h)$ and read off the coefficient of $h^i$. Among $x+1,\dots,x+j$ at least $\lfloor j/p\rfloor$ are divisible by $p$, and deleting $i$ factors leaves at least $\lfloor j/p\rfloor-i$ of them. The last bound is Lemma 11.1(d). (b) The terms of $F^{[i]}_e$ have valuation $\ge\lfloor j/p\rfloor-i\to\infty$ uniformly in $x$. For $h\in p\mathbb Z_p$ the double family $\{e_j\pi_j^{[i]}(x)h^i\}_{0\le i\le j}$ has valuations $\ge\max(\lfloor j/p\rfloor,i)$, so it is summable in any order: summing over $i$ first gives $\sum_je_j\pi_j(x+h)=F_e(x+h)$, over $j$ first gives $\sum_iF_e^{[i]}(x)h^i$, whose coefficients times $p^i$ tend to $0$. Then $|F_e(x+h)-F_e(x)-F_e^{[1]}(x)h|\le|h|^2$. (c) Fix $r$ and $\Phi(u)=F_e(r+pu)\in\mathbb Z_p\langle u\rangle$. If $\Phi\equiv0$, then $F_e$ vanishes at every negative integer $-m\equiv r\pmod p$ with $m\ge3$; but $\pi_j(-m)=0$ for $j\ge m$, so $F_e(-m)=S_B(-m)$ with $B=\{1\le j<m:e_j=1\}$, which is $\equiv1\pmod{m-1}$ and nonzero (Theorem 3.2(a)). So $\Phi\ne0$ and, by Strassmann's theorem (a nonzero element of $\mathbb Z_p\langle u\rangle$ has finitely many zeros in $\mathbb Z_p$), $Z(F_e)\cap(r+p\mathbb Z_p)$ is finite. If all $F_e^{[i]}(x)$ vanished, (b) would give $F_e\equiv0$ on $x+p\mathbb Z_p$, excluded. Compactness: $(x,e)\mapsto F_e(x)$ is continuous (uniform convergence; partial sums depend on finitely many coordinates). ∎

**Lemma 11.12 (Hensel for power series; distance formula) [proved; standard].**
- (a) Let $G(h)=\sum_ic_ih^i$ with $c_i\in\mathbb Z_p$, $\lambda=v(c_1)<\infty$ and $V=v(c_0)>2\lambda$. Then $G$ has exactly one zero $h^*$ with $v(h^*)>\lambda$; $v(G'(h^*))=\lambda$; and if $c_0\ne0$ then $v(h^*)=V-\lambda$.
- (b) Let $z\in Z(F_e)$ with $\lambda=v(F_e'(z))<\infty$, and $\tilde z\in Z(F_{\tilde e})$ with $v(\tilde z-z)>\lambda$. Then $v(\tilde z-z)=v\big((F_{\tilde e}-F_e)(\tilde z)\big)-\lambda$.

*Proof.* (a) On $D=p^{V-\lambda}\mathbb Z_p$ let $T(h)=-(c_0+\sum_{i\ge2}c_ih^i)/c_1$. For $h\in D$ and $i\ge2$, $v(c_ih^i)\ge2(V-\lambda)>V$, so $T(D)\subseteq D$; and $v(T(h)-T(h'))\ge v(h-h')+(V-\lambda)-\lambda\ge v(h-h')+1$, using $h^i-h'^i=(h-h')\sum_{a+b=i-1}h^ah'^b$. The fixed point $h^*$ of this contraction is a zero of $G$. If $G(h_1)=G(h_2)=0$ with $v(h_k)>\lambda$, then $0=(h_1-h_2)[c_1+\sum_{i\ge2}c_i\sum_{a+b=i-1}h_1^ah_2^b]$ and the bracket has valuation exactly $\lambda$, so $h_1=h_2$. $G'(h^*)=c_1+\sum_{i\ge2}ic_ih^{*i-1}$, and the sum has valuation $\ge V-\lambda>\lambda$. If $c_0\ne0$, $c_1h^*=-c_0-\sum_{i\ge2}c_ih^{*i}$ has valuation $V$. (b) $d=\tilde z-z\in p\mathbb Z_p$, and by Theorem 11.11(b) $F_e(\tilde z)=F_e'(z)d+\sum_{i\ge2}F_e^{[i]}(z)d^i$ with the sum of valuation $\ge2v(d)>\lambda+v(d)$; so $v(F_e(\tilde z))=\lambda+v(d)$, and $F_e(\tilde z)=-(F_{\tilde e}-F_e)(\tilde z)$. ∎

Call $x$ a *simple zero* if $F_e(x)=0\ne F_e'(x)$ for some $e$, with *slope* $\lambda=v(F_e'(x))$; let $\mathcal S_p$ be the set of simple zeros. For $J\subseteq\mathbb Z_{\ge1}$ let $e^J$ be $e$ with the coordinates in $J$ flipped, so $F_{e^J}=F_e+\Delta_J$ with $\Delta_J=\sum_{j\in J}(1-2e_j)\pi_j$.

**Proposition 11.13 (Hensel children; simple zeros accumulating at $-2$) [proved].**
- (a) Let $\alpha$ be a simple zero of $F_e$ with slope $\lambda$, and $J\subseteq[p(2\lambda+2),\infty)$ (finite or infinite). Then $F_{e^J}$ has exactly one zero $\alpha_J$ with $v(\alpha_J-\alpha)>\lambda$; it is simple with slope $\lambda$, and $v(\alpha_J-\alpha)=v(\Delta_J(\alpha))-\lambda$. If $\alpha$ is not a negative integer, a single flip $J=\{j\}$ gives $\alpha_j\ne\alpha$ with $v(\alpha_j-\alpha)=v(\pi_j(\alpha))-\lambda$ exactly.
- (b) For every $p$ and $c\ge2p$, the word with $e_0=e_1=e_2=e_{c+2}=1$ (all other $e_j=0$) has a simple zero $x_c$ with $v(x_c+2)=v(c!)$. Hence $-2$ is a limit of simple zeros different from $-2$.

*Proof.* (a) Apply Lemma 11.12(a) to $G(h)=F_{e^J}(\alpha+h)$: $c_0=\Delta_J(\alpha)$ has valuation $\ge\min_{j\in J}\lfloor j/p\rfloor\ge2\lambda+2$, and $c_1=F_e'(\alpha)+\Delta_J'(\alpha)$ with $v(\Delta_J'(\alpha))\ge2\lambda+1>\lambda$ (Theorem 11.11(a)), so $v(c_1)=\lambda$. For a single flip, $\pi_j(\alpha)\ne0$. (b) With $y=x+2$: $\pi_1=y-1$, $\pi_2=(y-1)y$, $\pi_{c+2}(x)=(y-1)y\pi_c(y)$, so $F_e=y\,H(y)$ with $H(y)=y+(y-1)\pi_c(y)$. Then $H(0)=-c!$ and $H'(0)=1+c!-\sum_{i\le c}c!/i\equiv1\pmod p$, because $p\mid c!$ and each $c!/i$ contains at least $\lfloor c/p\rfloor-1\ge1$ multiples of $p$. Lemma 11.12(a) with $\lambda=0$ gives $H(y_c)=0$ with $v(y_c)=v(c!)$; then $x_c=y_c-2$ is a zero of $F_e$ and $F_e'(x_c)=H(y_c)+y_cH'(y_c)=y_cH'(y_c)\ne0$. ∎

**Theorem 11.14 (a perfect kernel in $K_p$) [proved].** For every prime $p$:
- (i) $\overline{\mathcal S}_p\subseteq K_p$ and $\overline{\mathcal S}_p$ is perfect;
- (ii) $\overline{\mathcal S}_p$ meets the class $r+p\mathbb Z_p$ iff $K_p$ does, iff $r\notin\Phi_p$;
- (iii) $K_p$ has the cardinality of the continuum, and contains a nonempty perfect set in every class $r\notin\Phi_p$;
- (iv) the simple zeros of words of finite support are dense in $\overline{\mathcal S}_p$.

*Proof.* (i) $K_p$ is closed (Theorem 3.1). A simple zero $\alpha\ne-2$ is not a negative integer, since $K_p\cap\mathbb Z_{<0}=\{-2\}$ (Theorem 3.2(a)); by Proposition 11.13(a) it is a limit of simple zeros $\alpha_j\ne\alpha$. The point $-2$ is a simple zero of $x+2=S_{\{1\}}$ and is such a limit by 11.13(b). So $\mathcal S_p$ has no isolated points, and its closure is perfect. (ii) If $r\in\Phi_p$, $g_p\equiv0$ on the natural numbers of the class (Corollary 3.3), hence on all of $r+p\mathbb Z_p$ by locality at level 1 (Theorem 3.1(a)) *(citation added after a round-3 referee)*; otherwise Theorem 3.5 gives a simple zero there. (iii) A nonempty perfect subset of $\mathbb Z_p$ has cardinality $2^{\aleph_0}$. (iv) If $F_e(x)=0$ with slope $\lambda$, then $e|_n=e^J$ with $J=\{j\ge n:e_j=1\}$, and for $n\ge p(2\lambda+2)$ Proposition 11.13(a) gives a simple zero of the finite word $e|_n$ within $p^{-(\lfloor n/p\rfloor-\lambda)}$ of $x$. ∎

Previously known: $K_p$ is closed, nowhere dense and nonempty in every class $r\notin\Phi_p$ (Theorems 3.1, 3.5, 3.6). Uncountability and the perfect kernel are new here as far as we know.

*Runs and levels.* For $x\in\mathbb Z_p\setminus\mathbb Z_{<0}$ let $l_0\ge1$ be least with $p\mid x+l_0$, $l_i=l_0+pi$, and $L_i(x)=v(\pi_{l_i}(x))$. Run $i$ is the set of positions $l_i,\dots,l_i+p-1$; its elements are $\pi_{l_i+r}=\pi_{l_i}q_r$ with $q_r=\prod_{t\le r}(x+l_i+t)\equiv r!\pmod p$, all of valuation $L_i$. Writing $x+l_0=py$, the jump is $J_i=L_{i+1}-L_i=v(x+l_{i+1})=1+v(y+i+1)$.

**Theorem 11.15 (accumulation at multiple zeros) [proved].** Let $x\in K_p$ be a zero of multiplicity $k$ of some word $e$, and suppose $2v_p(k)+1\le p$. Then $x$ is a limit of simple zeros different from $x$; in particular $x\in\overline{\mathcal S}_p$ and $x$ is not isolated in $K_p$. (So: every zero of multiplicity prime to $p$; for $p=3$ every multiplicity with $9\nmid k$; for $p\ge5$ every multiplicity with $v_p(k)\le(p-1)/2$.)

*Proof.* If $x=-2$ use Proposition 11.13(b); so let $x\notin\mathbb Z_{<0}$. Put $\kappa=v(k)$, $w=2\kappa+1\le p$, $c_k=F_e^{[k]}(x)\ne0$, $\gamma=v(c_k)$, and $f(u)=u+v(u!)=\sum_{s\le u}(1+v(s))$.

*Step 0 (residues of levels).* (a) If $p^B\mid y+i_0$ then $L_{i_0+u}-L_{i_0}=f(u)$ for $0\le u<p^B$, because $v(y+i_0+s)=v(s)$ for $1\le s<p^B$. (b) For every $\ell\in\mathbb Z/k$ there are $B$ and $u<p^B$ with $p\mid u$ and $f(u)\equiv\ell\pmod k$. Indeed, for $u=\sum_id_ip^i$ Legendre gives $f(u)=\sum_id_iR_{i+1}$ with $R_n=(p^n-1)/(p-1)$. Write $k=p^ak'$ with $p\nmid k'$. For $n\ge a$, $R_n\equiv R_a\pmod{p^a}$; and $R_n\bmod k'$ is purely periodic ($R\mapsto pR+1$ is invertible mod $k'$) with $R_1=1$, so $R_n\equiv1\pmod{k'}$ for infinitely many $n$. Hence infinitely many $n\ge a+2$ have $R_n\equiv\varrho\pmod k$, where $\varrho\equiv(R_a\bmod p^a,\ 1\bmod k')$ is a unit mod $k$. Take $0\le c<k$ with $c\varrho\equiv\ell$, choose $c$ such $n$, and set $d_{n-1}=1$ there and all other digits $0$; then $d_0=0$ and $f(u)\equiv c\varrho\equiv\ell$.

*Step 1 (choice of runs).* There are infinitely many runs $i^*$ with (a) $J_{i^*}=\dots=J_{i^*+w-2}=1$, (b) $L_{i^*}\equiv\gamma\pmod k$, and (c) $L_{i^*}\ge k(M+\gamma+w)+\gamma$, where $M=M_{l_{i^*}+wp}(x)$. Take $B$ as in Step 0 for all residues mod $k$ and with $p^B>u+w$ for the $u$ used. In any stretch of $p^B$ consecutive runs there is an *aligned window* $i_0,\dots,i_0+p^B-1$ with $p^B\mid y+i_0$; choose $u$ with $p\mid u$ and $f(u)\equiv\gamma-L_{i_0}\pmod k$ and set $i^*=i_0+u$. Then (b) holds by Step 0(a), and (a) holds because $J_{i_0+u+t}=1+v(u+t+1)=1$ for $0\le t\le p-2$ (as $u+t+1\equiv t+1\not\equiv0$). For (c): $L_{i^*}\ge v(l_{i^*}!)$ grows linearly in $l_{i^*}$. If $n\mapsto M_n(x)$ is bounded, any far aligned window works. Otherwise let $l^\star_m$ be the record positions of $M_n(x)$, with values $M^\star_m$; since $v(l^\star_{m+1}-l^\star_m)\ge M^\star_m$, consecutive records are at least $p^{M^\star_m}$ apart, and $M_n=M^\star_m$ on $[l^\star_m,l^\star_{m+1})$. For large $m$ this interval contains an aligned window beyond position $(p-1)[k(M^\star_m+\gamma+w)+\gamma]+O(\log)$ and before $l^\star_{m+1}-wp$, because its length beats any linear function of $M^\star_m$; there (c) holds.

*Step 2 (the perturbation).* Fix such $i^*$, put $V=L_{i^*}$, $s=(V-\gamma)/k\in\mathbb Z$, and $\theta=c_kp^{ks}/p^V\in\mathbb Z_p^\times$. The runs $i^*+t$, $0\le t<w$, have levels $V+t$ by (a), and their elements are $p^{V+t}$ times units $\equiv\pm\omega_tr!\not\equiv0\pmod p$ (with the sign $1-2e_j$ of the flip). By Cauchy–Davenport the subset sums of these $p$ nonzero residues cover $\mathbb Z/p$. So, choosing subsets $R_0,R_1,\dots,R_{w-1}$ of the runs in turn to fix the digits $V,V+1,\dots,V+w-1$, we get a flip set $J$ with $\delta:=\Delta_J(x)\equiv-\theta p^V\pmod{p^{V+w}}$. Put $e'=e^J$.

*Step 3 (Hensel in a rescaled variable).* $F_{e'}(x+h)=\sum_ia_ih^i$ with $a_0=\delta$, $a_i=F_e^{[i]}(x)+\Delta_J^{[i]}(x)$, and $F_e^{[i]}(x)=0$ for $1\le i<k$. Every $j\in J$ has $v(\pi_j(x))\ge V$ and $j<l_{i^*}+wp$, so $v(\Delta_J^{[i]}(x))\ge V-iM$ by Theorem 11.11(a). Put $H(u)=p^{-V}F_{e'}(x+p^su)=\sum_ib_iu^i$, $b_i=a_ip^{is-V}$. Using $s\ge M+\gamma+w$ (from (c)): for $1\le i<k$, $v(b_i)\ge i(s-M)\ge w$; for $i=k$, $c_kp^{ks-V}=\theta$ and $v(\Delta_J^{[k]}p^{ks-V})\ge k(s-M)\ge w$, so $b_k\equiv\theta\pmod{p^w}$; for $i>k$, $v(b_i)\ge is-V=(i-k)s-\gamma\ge w$ and $v(b_i)\to\infty$. Also $b_0\equiv-\theta\pmod{p^w}$. So $H\in\mathbb Z_p\langle u\rangle$, $H(1)\equiv0\pmod{p^w}$, and $H'(1)=kb_k+\sum_{i\ne k}ib_i$ has valuation exactly $\kappa$ (the sum has valuation $\ge w>\kappa$). Lemma 11.12(a) applied to $t\mapsto H(1+t)$ (with $v(H(1))\ge w>2\kappa$) gives a zero $u^*$ with $v(u^*-1)\ge1$ and $v(H'(u^*))=\kappa$. Then $x+p^su^*$ is a zero of $F_{e'}$ at distance exactly $p^{-s}$ from $x$, with $F_{e'}'(x+p^su^*)=p^{V-s}H'(u^*)\ne0$. As $i^*\to\infty$, $s\to\infty$. ∎

**Proposition 11.16 ($p=2$, $v_2(k)=1$) [computer-assisted; a finite enumeration of 64 configurations, re-read by the lead].** At $p=2$, every zero of multiplicity $k$ with $v_2(k)=1$ of any word is a limit of simple zeros.

*Proof (outline; the enumeration is `code/round3/T1b-Kp-structure/p2k2.py`).* As in Theorem 11.15 with $w=3$, except Step 2: use two consecutive runs $u,u+1$ in an aligned window with $u\equiv2\pmod4$, so that $J_u=1$ and $J_{u+1}=1+v(u+2)\ge3$; run $u$ has level $V$, run $u+1$ level $V+1$, and every later run level $\ge V+4$. The four normalised elements mod $8$ depend only on $X=x+l_u+2\bmod16$, with $X\equiv6\pmod8$. The script checks, for both admissible classes $X\bmod16$ and all $16$ sign patterns, that their subset sums reach every odd residue mod $8$ (it also shows that runs with $J_{u+1}=2$ fail for some signs, which is why they are avoided). The residues of the levels mod $k$ are handled as in Step 0, with $f(u)=3+\sum_{i\ge2}d_iR_{i+1}$ for $u=2+\sum_{i\ge2}d_i2^i$. Step 3 is unchanged ($w=3>2\kappa=2$). ∎

*Open.* Whether $K_p$ is perfect, i.e. $K_p=\overline{\mathcal S}_p$, and whether $K_p$ contains any multiple zero other than $-2$. By Theorem 11.15 and Proposition 11.16, a point of $K_p\setminus\overline{\mathcal S}_p$ would have only representing words of multiplicity $k$ with $v_2(k)\ge2$ ($p=2$), $v_3(k)\ge2$ ($p=3$), or $v_p(k)>(p-1)/2$ ($p\ge5$).

*Window data.* Fix $w\ge1$ with $p\nmid w$, $K\ge1$, and $P=wp$. For $\tau\in p\mathbb Z/p^K$ (with $v(0):=K$) let $q_s(\tau)=\prod_{t\le s}(\tau+t)$ for $0\le s<P$, $G_K(\tau)=\min\big(K,\sum_{t=1}^P\min(v(\tau+t),K)\big)$, $N_{w,K}(\tau)$ the number of distinct subset sums of $\{q_s(\tau)\}_{s<P}$ mod $p^{G_K(\tau)}$, and
$$D_p(w,K)=\frac{p-1}{wp}\cdot\frac1{p^{K-1}}\sum_{y\bmod p^{K-1}}\log_pN_{w,K}(py).$$
$N_{w,K}(\tau)\ge p$ by Cauchy–Davenport, since $q_s\equiv s!\not\equiv0\pmod p$ for $s<p$.

**Theorem 11.17 (window-code lower bound for the Hausdorff dimension) [proved].** Let $\alpha\ne-2$ be a simple zero of a word $e$ of finite support. Then for every $w\ge1$ with $p\nmid w$, every $K\ge1$ and every $\rho>0$, $\dim_H(K_p\cap B(\alpha,\rho))\ge D_p(w,K)$. By Theorem 11.14(iv) and Proposition 11.13(b) the same holds near every point of $\overline{\mathcal S}_p$, hence in every class $r\notin\Phi_p$, and near every multiple zero covered by Theorem 11.15 or Proposition 11.16.

*Proof.* Let $\lambda$ be the slope and use the runs of $\alpha$. Fix $i_0$ with $l_{i_0}\ge p(2\lambda+2)$, $l_{i_0}$ beyond the support of $e$, and $P_0:=L_{i_0}(\alpha)-\lambda\ge\max(K+1,v(\alpha+2)+1)$; note $P_0>\lambda$ since $L_{i_0}\ge\lfloor l_{i_0}/p\rfloor\ge2\lambda+2$. Window $k$ is the set of positions $a_k+[0,P)$, $a_k=l_{i_0+kw}$; its *type* is $\tau_k=(\alpha+a_k)\bmod p^K\in p\mathbb Z/p^K$; write $N_k=N_{w,K}(\tau_k)$, $G_k=G_K(\tau_k)$.

*Codes.* Fix families $\mathcal F_k$ of $N_k$ subsets of $[0,P)$ with pairwise distinct sums $\sum_{s\in S}q_s(\tau_k)\bmod p^{G_k}$. For $c=(S_k)_k\in\Omega=\prod_k\mathcal F_k$ let $J(c)=\bigcup_k(a_k+S_k)$ and let $z(c)$ be the zero $\alpha_{J(c)}$ of Proposition 11.13(a) (here $e^{J(c)}=e+\mathbf 1_{J(c)}$). It is simple with slope $\lambda$, and $v(z(c)-\alpha)\ge P_0$, because every flipped $j\ge l_{i_0}$ has $v(\pi_j(\alpha))\ge L_{i_0}(\alpha)$. Hence $z\equiv\alpha\pmod{p^{P_0}}$, so $(z+a_k)\bmod p^K=\tau_k$, $\min(v(z+n),K)=\min(v(\alpha+n),K)$ for all $n$, and $v(z+2)=v(\alpha+2)<\infty$; so $z\ne-2$, $z$ is not a negative integer, and $\mathcal L_k(z):=v(\pi_{a_k}(z))<\infty$.

*Distances.* Let $c\ne c'$ first differ in window $k$, $z=z(c)$, $z'=z(c')$; then $v(z-z')\ge P_0>\lambda$, and Lemma 11.12(b) (with base zero $z'$) gives $v(z-z')=v(H(z))-\lambda$ for $H=F_{e^{J(c)}}-F_{e^{J(c')}}$. Now
$$H(z)=\pi_{a_k}(z)\Big[\sum_{s\in S_k}q^z_s-\sum_{s\in S'_k}q^z_s\Big]+\sum_{n\ge a_{k+1}}(\pm)\pi_n(z),\qquad q^z_s=\prod_{t\le s}(z+a_k+t)\equiv q_s(\tau_k)\ (p^K).$$
The bracket has valuation $d<G_k\le K$ by the choice of $\mathcal F_k$; the tail has valuation $\ge\mathcal L_{k+1}(z)=\mathcal L_k(z)+g_k(z)$ with $g_k(z)=\sum_{t=1}^Pv(z+a_k+t)\ge G_k$. Hence
$$v(z(c)-z(c'))=\mathcal L_k(z)-\lambda+d,\qquad0\le d<G_k.\tag{11.2}$$
Put $\rho_k(z)=\mathcal L_k(z)+G_k-\lambda$. By (11.2), $c'$ agrees with $c$ on windows $0,\dots,k$ iff $v(z(c')-z(c))\ge\rho_k(z(c))$: a first difference at $m\le k$ gives $v\le\mathcal L_m+G_m-1-\lambda\le\rho_k-1$ (as $\mathcal L_m+G_m\le\mathcal L_{m+1}\le\mathcal L_k$ for $m<k$), and one at $m>k$ gives $v\ge\mathcal L_{k+1}-\lambda\ge\rho_k$. So $c\mapsto z(c)$ is injective and continuous, $Z=z(\Omega)\subseteq K_p\cap B(\alpha,p^{-P_0})$ is compact, and the depth-$(k+1)$ cylinder of $z$ is $Z\cap\bar B(z,p^{-\rho_k(z)})$. *(Detail added.)* $\rho_k$ is constant on a cylinder: for $n\le a_k$, $v(z+n)\le\mathcal L_k(z)-\lfloor a_k/p\rfloor+1\le\mathcal L_k(z)-2\lambda-1<\rho_k(z)$, so $v(z'+n)=v(z+n)$ for $z'$ in the ball, and $\mathcal L_k(z')=\mathcal L_k(z)$. Hence balls of distinct depth-$(k+1)$ cylinders are disjoint.

*Measure.* Let $\nu$ be the product of the uniform measures on the $\mathcal F_k$ and $\mu_Z=z_*\nu$. Then $\mu_Z(\bar B(z,p^{-\rho_k(z)}))=\prod_{m\le k}N_m^{-1}\le p^{-(k+1)}$, and for $p^{-\rho_{k+1}(z)}<r\le p^{-\rho_k(z)}$,
$$\frac{\log\mu_Z(\bar B(z,r))}{\log r}\ \ge\ \frac{\sum_{m\le k}\log_pN_m}{\rho_{k+1}(z)}.\tag{11.3}$$
*Numerator:* $\tau_m/p\equiv y+i_0+mw\pmod{p^{K-1}}$ with $\alpha+l_0=py$; as $p\nmid w$, this runs through all residues once in every $p^{K-1}$ consecutive $m$, so $\frac1k\sum_{m<k}\log_pN_m\to\frac{wp}{p-1}D_p(w,K)$. *Denominator:* $\rho_{k+1}\le\mathcal L_{k+1}+K$ and $\mathcal L_{k+1}(z)=\mathcal L_0(z)+\sum_{a_0<n\le a_{k+1}}v(z+n)\le\mathcal L_0(z)+(k+1)P/(p-1)+\mathfrak M_{k+1}(z)$, with $\mathfrak M_k(z)=\max_{a_0<n\le a_k}v(z+n)$ (at most $T/p^\ell+1$ of $T$ consecutive integers are divisible by $p^\ell$). So the right side of (11.3) has $\liminf\ge D_p(w,K)$ wherever $\mathfrak M_k(z)=o(k)$, which holds $\mu_Z$-a.e. by Lemma 11.18. The local mass distribution principle (if $\liminf_{r\to0}\log\mu_Z(\bar B(z,r))/\log r\ge s_0$ for $\mu_Z$-a.e. $z$, then $\dim_HZ\ge s_0$; standard, e.g. Falconer, *Techniques in Fractal Geometry*, Prop. 2.3 (proposition number supplied by a round-3 referee, not checked by the lead against the book); it is also proved in two lines in the track report via ultrametric covers) gives $\dim_HZ\ge D_p(w,K)$. ∎

**Lemma 11.18 (no deep traps) [proved].** In the setting of the proof above, $\mathfrak M_k(z)=o(k)$ for $\mu_Z$-a.e. $z$.

*Proof.* Here $W_k$ denotes the $P$ positions $n=a_k+1,\dots,a_k+P$ that enter $g_k$ (window $k$ of the proof of Theorem 11.17, shifted by one). *[Corrected, round-3 referees: the text had $a_k+[0,P)$. Each $W_k$ is still $P$ fixed integers, so every bound below is unchanged. Renamed from "window $k$" after the round-3 re-check, so that "window $k$" keeps its meaning $a_k+[0,P)$ from Theorem 11.17.]* (F1) If $\rho_{m-1}(z)\le R$ then $\mu_Z(\bar B(z,p^{-R}))\le\prod_{i<m}N_i^{-1}\le p^{-m}$. (F2) Among $P$ consecutive integers at most one has $v(z+n)>\beta:=\lfloor\log_pP\rfloor$, so $g_k(z)\le(P-1)\beta+\max_{n\in W_k}v(z+n)$.
*Step A.* Let $A_k=\{z\in Z:v(z+n)\ge\rho_k(z)\text{ for some }n\in W_k\}$. Then $-n\in\bar B(z,p^{-\rho_k(z)})$; distinct depth-$(k+1)$ cylinder balls are disjoint, so at most $P$ cylinders meet $A_k$ and $\mu_Z(A_k)\le Pp^{-(k+1)}$. By Borel–Cantelli a.e. $z$ is in finitely many $A_k$; for the other $k$, (F2) and $\rho_k\le\mathcal L_k+K$ give $\mathcal L_{k+1}\le2\mathcal L_k+C_0$, so $\mathcal L_k(z)\le C(z)2^k$.
*Step B.* For $C,k_1$ let $\mathrm{Good}=\{\mathcal L_k\le C2^k\ \forall k\ge k_1\}$ and $E_k=\{z\in\mathrm{Good}:\max_{n\in W_k}v(z+n)\ge k^2\}$. If $v(z+n)\ge k^2$ then $\bar B(z,p^{-k^2})=\bar B(-n,p^{-k^2})$, and by (F1) with $\rho_{m-1}\le C2^{m-1}+K$ its measure is $\le p^{-\log_2((k^2-K)/C)}\le C'k^{-2}$ for large $k$. So $\mu_Z(E_k)\le PC'k^{-2}$ is summable, and (union over $C,k_1$) a.e. $z$ has $\max_{n\in W_k}v(z+n)<k^2$ eventually; then $\mathcal L_k(z)=O(k^3)$.
*Step C.* Repeat with $\mathrm{Good}'=\{\mathcal L_k\le Ck^3\ \forall k\ge k_1\}$ and threshold $\varepsilon k$: now the ball measure is $\le p^{-((\varepsilon k-K)/C)^{1/3}+1}$, summable in $k$. So a.e. $z$ has $\max_{n\in W_k}v(z+n)<\varepsilon k$ eventually, i.e. $\mathfrak M_k\le\varepsilon k+O_z(1)$; intersect over $\varepsilon=1/j$. ∎

**Corollary 11.19 (closed form; computed values) [proved; values computer-assisted].**
- (a) Let $L_p$ be the covering depth of Theorem 3.9 for odd $p$, and $L_2=1$. Then near every point of $\overline{\mathcal S}_p$, $\dim_HK_p\ge D_p(1,L_p+1)\ge1-p^{-L_p}$.
- (b) Exact counts give the following lower bounds for $\dim_H(K_p\cap U)$, $U$ any neighbourhood of any point of $\overline{\mathcal S}_p$ (rounded down; table below).

*Proof of (a).* For $w=1$ only $t=p$ has $p\mid\tau+t$, so $G_K(\tau)=\min(K,v(\tau+p))=:J$, and mod $p^J$, $\tau\equiv-p$, so $q_s\equiv\prod_{t\le s}(t-p)=(p-1)!(-1)^u/u!$ ($u=p-1-s$; for $p=2$ the set is $\{1,-1\}$). Hence $N_{1,K}(\tau)\ge p^{\min(J,L_p)}$. With $\tau=py$, $y$ uniform mod $p^{K-1}$ and $K\ge L_p+1$: $J=\min(K,1+v(y+1))$ and $\mathbb E\min(J,L_p)=\sum_{s<L_p}p^{-s}=(1-p^{-L_p})\frac p{p-1}$. ∎

| $p$ | best $(w,K)$ | $D_p(w,K)$, rounded down | $1-p^{-L_p}$ |
|---|---|---|---|
| 2 | $(9,22)$; also $(1,2)$: 0.6462, $(3,16)$: 0.7543, $(5,16)$: 0.8054, $(7,22)$: 0.8333 | **0.8530** | 0.5 |
| 3 | $(5,13)$; also $(1,8)$: 0.8068, $(2,10)$: 0.8591, $(4,12)$: 0.9111 | **0.9247** | 0.6667 |
| 5 | $(3,8)$; also $(1,7)$: 0.9236, $(2,8)$: 0.9548 | **0.9691** | 0.8 |
| 7 | $(2,6)$; also $(1,5)$: 0.9855 | **0.9921** | 0.9796 |
| 11 | $(1,5)$ | **0.9982** | 0.9917 |
| 13 | $(1,5)$ | **0.9996** | 0.9940 |
| 17, 19, 23 | $(1,4)$ | 0.99996, 0.99999, 0.99999 | $1-p^{-3},1-p^{-3},1-p^{-4}$ |

*Status of the values.* `wdim.c` (T1b) computes every $N_{w,K}(\tau)$ exactly and combines them in double precision (relative error $<10^{-12}$; not interval-certified). The track's independent brute force `wdim_check.py` agrees to 10 digits on five cases, and the lead's own re-implementation of the definition (`code/round3/lead/lead_checks_r3.py`) agrees on $(2,3,7)$, $(3,2,5)$, $(5,1,4)$, $(7,1,3)$. The lead re-ran `wdim` for eleven cases including $(2,9,22)$ (809 s) and $(3,5,13)$: identical to the track's log. For $p=2$, predictions for $w=7,9$ were registered before the runs (`PREDICTIONS_registered_T1b.txt`, 2026-10-21 22:18:27 UTC) and confirmed. Values for $37\le p\le97$ via (a) use the archived lower bounds for $L_p$ (§3.5); these lower bounds were not re-checked in round 3. (In the last table row, $(1,4)$ is $K=L_p+1$ for $p=17,19$ and $K=L_p$ for $p=23$, where $D_{23}(1,4)=1-23^{-4}$ exactly.) *Round-3 referees:* four independently written programs reproduced every table value to every printed digit, including $(2,9,22)=0.8530453$ and $(3,5,13)=0.9247357$; every rounding-down margin is $\ge1.3\cdot10^{-5}$ (§11.9). A cross-check with §11.4: for $w=1$ and large $K$, $D_p(1,K)$ coincides to 9–10 digits with $1-\theta^{\rm set}_p$ of Theorem 11.38, computed by a different program in another track (Computation 11.59).

**Corollary 11.20 (box dimension; an exponential lower bound for $\delta_G$) [proved; constants computer-assisted].** For every $p$, $\underline{\dim}_BK_p\ge\dim_HK_p\ge D:=\sup_{w,K}D_p(w,K)$ (over $p\nmid w$, $K\ge1$; attainment is not claimed), and for every $\varepsilon>0$, $\delta_G(p)\ge p^{-(1-D+\varepsilon)G}$ for all large $G$. At $p=2$: $\delta_G(2)\ge2^{-(0.147+o(1))G}$.

*Proof.* $\dim_H\le\underline{\dim}_B$ for compact sets. So the number of classes mod $p^G$ meeting $K_p$ is $\ge p^{(D-\varepsilon)G}$ for large $G$, and each such class lies in $\{g_p\ge G\}$ by locality (Theorem 3.1(a)). ∎

This beats the explicit bound $\delta_G(p)\ge p^{-\lceil G/3\rceil}$ coming from Kitamura's cube identity ($\{g_p\ge G\}\supseteq-2+p^{\lceil G/3\rceil}\mathbb Z_p$; shadow family). A *polynomial* lower bound for $\delta_G(2)$ remains open; note that it would concern the approximating sets $\{g_2\ge G\}$ and would not by itself determine $\dim_BK_2$ (a class can survive to level $G$ and die later).

**Proposition 11.21 ($K_p=\{x:-1\in A'_x\}$) [proved].** Let $A'_x=\{\sum_{j\ge1}e_j\pi_j(x):e\in\{0,1\}^{\mathbb Z_{\ge1}}\}$. Then $A'_x$ is compact with the finite sums dense; $g_p(x)=-\log_p\mathrm{dist}(-1,A'_x)$ (with $-\log_p0=\infty$), so $K_p=\{x:-1\in A'_x\}$; and $d_H(A'_x,A'_y)\le|x-y|_p$, which re-proves locality (Theorem 3.1(a)). *(Credit: this restates the compactness reformulation of §1.3, which is due to earlier public AI write-ups credited in §2: neelsomani, erichou1, AItoBit. Only the Hausdorff-distance form is added here.)*

*Proof.* $e\mapsto\sum_je_j\pi_j(x)$ is continuous on a compact space and truncations are dense. $g_p(x)\ge G$ iff some finite sum $s$ has $v(1+s)\ge G$, iff $\mathrm{dist}(-1,A'_x)\le p^{-G}$ by density. Finally $\pi_j(x)-\pi_j(y)\in(x-y)\mathbb Z_p$ termwise. ∎

**Conjecture 11.22 [conjecture].** $\dim_HK_2=1$ although $\mu(K_2)=0$, and $\sup_KD_2(w,K)\to1$ as $w\to\infty$; for odd $p$, $\dim_HK_p=1$ (this would follow from $\mu(K_p)>0$). *Evidence [heuristic]:* the deficits $1-D_2$ are $0.354,0.246,0.195,0.167,0.147$ for $w=1,3,5,7,9$, roughly $0.45\,w^{-1/2}$ (a fit to five numbers). A proof would need a quenched lower bound $\mathbb E_\tau\log_2N_w(\tau)\ge2w-o(w)$; annealed collision counts cannot give it, because rare shadow types near $-2$ dominate them (as in §11.6).

### 11.3 The prime 2: an explicit rate off the class $14\bmod16$ (track T2)

Theorem 10.1 gives $\delta_G(2)\to0$ with no rate. Here $p=2$, $v=v_2$, $s(\cdot)$ is the binary digit sum, $W_n=n-V_n$, $P_n(x)$ is the set of paths alive at $n$, and $Z_n=2^{-W_n}|P_n|$. Odd $x$ have $g_2=0$; on $4+8\mathbb Z_2$, $g_2=3$ (Corollary 3.7.1(iii)). The rest of $R:=\mathbb Z_2\setminus(14+16\mathbb Z_2)$ is covered by
$$C_0=8\mathbb Z_2,\qquad C_2=2+8\mathbb Z_2,\qquad C_6=6+16\mathbb Z_2 .$$
The class split and the expectation that $14\bmod16$ is the hard case are round-2 track R1a's (unverified Claim 10.9); the proof below is independent of R1a's lemmas.

**Lemma 11.23 (valuation facts) [proved].** Let $x\in2\mathbb Z_2$ not be a negative integer. In addition to Lemma 10.2(a)–(f):
- (a) For $K\ge1$, $r=x\bmod2^K$ and $N_K=\min\{N\ge1:2^K\mid x+N\}$: $W_{N_K+\delta}=W_{N_K}+s(\delta)$ for $0\le\delta<2^K$.
- (b) $V_n\ge M_n+1$ for $n\ge4$.
- (c) $D:=V_N-V_n\le(N-n)+M_N$ for $N>n$.
- (d) If $g_2(x)\ge G$ then $P_n(x)\ne\emptyset$ for every $n$ with $V_n(x)\le G$.
- (e) For $n\ge4$ the cylinders $C_n(x)=x+2^{V_n(x)}\mathbb Z_2$ partition $2\mathbb Z_2$ (minus the negative integers), refine as $n$ grows, and $v(\cdot+i)$ ($i\le n$), $P_n$ and $W_n$ are constant on each. Let $\mathcal F_n$ be the generated $\sigma$-algebra.

*Proof.* (a) $x+N_K=2^Ku$ and $v(2^Ku+i)=v(i)$ for $1\le i<2^K$, so $V_{N_K+\delta}-V_{N_K}=v(\delta!)=\delta-s(\delta)$. (b) $x+2,x+4$ are even; the largest valuation is $M_n$ and the other even term adds $\ge1$. (c) $D=\sum_{\ell\ge1}\#\{i\in(n,N]:2^\ell\mid x+i\}\le\sum_{\ell\le M_N}(\lfloor(N-n)/2^\ell\rfloor+1)\le(N-n)+M_N$. (d) Take $B$ with $v(S_B(x))\ge G$ and $e$ its word; $S_{e|_n}=S_B-\sum_{j\ge n}e_j\pi_j$ has valuation $\ge\min(G,V_n)=V_n$. (e) By (b), $v(y-x)\ge V_n(x)>M_n(x)$ for $y\in C_n(x)$, so $v(y+i)=v(x+i)$ for $i\le n$; aliveness is a congruence mod $2^{V_n}$ of integer polynomials. ∎

**Lemma 11.24 (Taylor inequality; renormalisation near $-2$) [proved].**
- (a) If $\Phi(y+h)=\sum_i\varphi_ih^i$ converges with all $\varphi_i\in\mathbb Z_2$, then $\min_i(v(\varphi_i)+iv(h))\le v(\Phi(y+h))$.
- (b) Let $x\equiv2\pmod4$, $y=x+2$, $t=v(y)\ge2$. If $v(S_e(x))\ge t+1$ then $e_1=1$ and $e_2+e_3=1$.
- (c) For every path with $e_1=1$, $S_e(x)=y(y-1)\Phi_e(y)$ with $\Phi_e(y)=e_2-\frac1{1-y}+\sum_{k\ge1}e_{k+2}\pi_k(y)$; for $y,h\in2\mathbb Z_2$, $\Phi_e(y+h)=\sum_i\Phi_e^{[i]}(y)h^i$ with all coefficients in $\mathbb Z_2$; and if $v(\Phi_e(y))>t+v(\Phi_e'(y))$ then $\lambda_e(x)=t+v(\Phi_e'(y))$.

*Proof.* (a) If every term had valuation $>v(\Phi(y+h))$, so would the sum. (b) For $b\ge4$, $\pi_b(x)$ contains $(x+2)(x+4)$, so modulo $2^{t+1}$, $S_e(x)\equiv1+e_1(x+1)+e_2(x+1)(x+2)+e_3(x+1)(x+2)(x+3)$; this is odd if $e_1=0$, and if $e_1=1$ it is $y[1+e_2(x+1)+e_3(x+1)(x+3)]$ with bracket $\equiv1+e_2+e_3\pmod2$ (the halving-lemma argument, Theorem 3.7). (c) $\pi_1(x)=y-1$ and $\pi_j(x)=(y-1)y\pi_{j-2}(y)$ for $j\ge2$, so $S_e=y+y(y-1)[e_2+\sum_{k\ge1}e_{k+2}\pi_k(y)]$ and $y=y(y-1)\cdot(-\frac1{1-y})$. The expansion: the polynomial part is exact Taylor; $-\frac1{1-y-h}=-\sum_ih^i(1-y)^{-i-1}$ with $1-y$ a unit. Finally $S_e'(x)=(2y-1)\Phi_e(y)+y(y-1)\Phi_e'(y)$, whose two terms have valuations $v(\Phi_e)$ and $t+v(\Phi_e')$. ∎

**Proposition 11.25 (slope certificates) [proved; the finite cases checked twice].** Let $e$ be alive at $n$ (at $x$).
- (a) If $x\in C_0$ and $V_n(x)\ge4$, then $\lambda_e(x)\le1$.
- (b) If $x\in C_2$ and $V_n(x)\ge7$, then $\lambda_e(x)\le3$.
- (c) If $x\in C_6$ and $V_n(x)\ge11$, then $\lambda_e(x)\le6$.

*Proof.* The idea is to evaluate at a negative integer, where only finitely many path entries matter, and to read the result as a bound on a Taylor coefficient at $x$.
- (a) Take $h=-4-x$, $v(h)=2$. As $\pi_j(-4)=0$ for $j\ge4$, $S_e(-4)=1-3e_1+6e_2-6e_3\in\{1,-5,7,1,-2,-8,4,-2\}$, of valuation $\le3$. By Lemma 11.24(a), some $i$ has $v(S_e^{[i]}(x))+2i\le3$. Not $i=0$ ($v(S_e(x))\ge V_n\ge4$), not $i\ge2$; so $v(S_e'(x))\le1$.
- (b) $t=2$, $y\equiv4\pmod8$, $h=-4-y$ with $v(h)\ge3$; by Lemma 11.24(b), $e_1=1$, $e_2+e_3=1$. Using $\pi_k(-4)=-3,6,-6,0$ ($k=1,2,3,\ge4$): if $e_2=1,e_3=0$, $\Phi_e(-4)=\frac45+6e_4-6e_5\in\{\frac45,\frac{34}5,-\frac{26}5\}$ has valuation $\le2$; since $v(h)\ge3$ this forces $v(\Phi_e(y))\le2$, so $v(S_e(x))\le t+2=4<7$, impossible. If $e_2=0,e_3=1$, $\Phi_e(-4)=-\frac15-3+6e_4-6e_5\in\{-\frac{16}5,\frac{14}5,-\frac{46}5\}$ has valuation $\le4$; $i=0$ would give $v(S_e(x))\le6<7$, and $i\ge2$ gives $\ge6>4$; so $v(\Phi_e'(y))\le1$, and as $v(\Phi_e(y))\ge V_n-t\ge5>t+1$, $\lambda_e=t+v(\Phi_e')\le3$.
- (c) $t=3$, $y\equiv8\pmod{16}$. If $e_2=1,e_3=0$, take $h=-4-y$ ($v(h)=2$): $v(\Phi_e(-4))\le2$; $i=0$ gives $v(S_e(x))\le5<11$, $i\ge2$ gives $\ge4$; so $v(\Phi_e'(y))=0$ and $\lambda_e=3$ (as $v(\Phi_e)\ge8$). If $e_2=0,e_3=1$, take $h=-8-y$ ($v(h)\ge4$): $\Phi_e(-8)=-\frac19+\sum_{k=1}^7e_{k+2}\pi_k(-8)$ depends on $(e_4,\dots,e_9)$, and over all 64 cases it is nonzero with valuation $\le7$ (histogram $\{1{:}32,3{:}16,4{:}8,5{:}3,6{:}4,7{:}1\}$). $i=0$ gives $v(S_e(x))\le10<11$, $i\ge2$ gives $\ge8>7$; so $v(\Phi_e'(y))\le3$ and $\lambda_e=3+v(\Phi_e')\le6$ (as $v(\Phi_e)\ge8>6$). ∎

The finite values were computed by T2's `certs.py` and independently by the lead (`lead_t2_certs.py`, which evaluates the integers $S_e(-m-2)=(-m)(-m-1)\Phi_e(-m)$ directly and also checks the identity of Lemma 11.24(c) on 2000 random cases): identical. On 20 000 random points per class (depth $\le64$), the largest slopes seen were $1,3,3$.

**Proposition 11.26 (Hensel first-moment bound) [proved].** Let $C=r_0+2^k\mathbb Z_2\subseteq2\mathbb Z_2$, $L\ge0$, $n\ge6$, and let $\Gamma$ be a set on which $V_n\ge\max(2L+1,L+k)$ and $V_n-L>M_n$. Suppose every $e\in P_n(x)$ has $\lambda_e(x)\le L$ for every $x\in C\cap\Gamma$. Then $\int_{C\cap\Gamma}Z_n\,d\mu\le2^{L-1+\max(0,L+1-k)}$. In particular, with $\Gamma_*(n)$ the event $\{V_n\ge\max(V_{\rm cert},2L+1,L+k),\ V_n-L>M_n\}$ and $(k,L,V_{\rm cert})=(3,1,4),(3,3,7),(4,6,11)$ for $C_0,C_2,C_6$: $\int_{C_0\cap\Gamma_*}Z_n\le1$, $\int_{C_2\cap\Gamma_*}Z_n\le8$, $\int_{C_6\cap\Gamma_*}Z_n\le256$.

*Proof.* Two standard facts for nonzero $f\in\mathbb Z_2[X]$: *(strong Hensel)* if $v(f(x))>2\lambda$ with $\lambda=v(f'(x))$, there is a root $r$ with $v(r-x)=v(f(x))-\lambda$ and $v(f'(r))=\lambda$ (Newton iteration; or Lemma 11.12(a)); *(root separation)* distinct roots $r_1,r_2$ satisfy $v(f'(r_1))\ge v(r_1-r_2)$, because $f'(r_1)=-h\sum_{i\ge2}f^{[i]}(r_1)h^{i-2}$ with $h=r_2-r_1$. Write $\int_{C\cap\Gamma}Z_n=\sum_e\int_{A_e\cap C\cap\Gamma}2^{V_n-n}$, $A_e=\{x:e\in P_n(x)\}$, over the $2^{n-1}$ paths $e$ ($S_e\ne0$ since $S_e(0)\ge1$). Fix $e$ and $x$ in the domain, $\lambda=\lambda_e(x)\le L$. As $v(S_e(x))\ge V_n\ge2L+1>2\lambda$, there is a root $r$ of $S_e$ with $v(r-x)\ge V_n-\lambda\ge V_n-L>M_n(x)$ and $v(S_e'(r))=\lambda$; so $V_n(r)=V_n(x)$, $M_n(r)=M_n(x)$, and $r\in C$ (as $V_n-L\ge k$). Thus $r\in R_e=\{r\in C:S_e(r)=0,\ \lambda_r:=v(S_e'(r))\le L,\ V_n(r)-\lambda_r>M_n(r)\}$ and $x\in B_r=r+2^{V_n(r)-\lambda_r}\mathbb Z_2$, on which $V_n\equiv V_n(r)$. Hence the integral over $A_e$ is $\le\sum_{r\in R_e}2^{V_n(r)-n}\mu(B_r)=\sum_{r\in R_e}2^{\lambda_r-n}\le|R_e|2^{L-n}$. By root separation distinct $r_1,r_2\in R_e$ have $k\le v(r_1-r_2)\le L$; so $|R_e|\le1$ if $k>L$, and otherwise $|R_e|\le2^{L+1-k}$. Sum over $e$. ∎

Numerically $\mathbb E[Z_n\mid C]\approx0.52,0.97,2.0$ and flat in $n$, so the constants are crude.

*Window identity.* Fix $L$, put $\ell_0=2L+2$, $N=n+\ell_0$, $m=V_n(x)$, and let $\Gamma_L(n)$ be the event $2M_N(x)+3L+3\le V_n(x)$ (decided by $x\bmod2^m$). On $\Gamma_L(n)$: $M_N<m$; $D\le\ell_0+M_N$ (Lemma 11.23(c)), so $D+L\le m-M_n$; $L<m-M_N$; and $D\ge L+1$. These are (W1)–(W3) of Proposition 10.6, whose conclusions therefore hold. Summing Proposition 10.6(iii) over the $2^\lambda$ states $s$ (its right side does not depend on $s$) and also weighting by $\rho_N=2^\lambda a_N^{(\lambda)}(s)$ (constant on $C$, $\sum_sa_N=1$) gives, for every $e\in P_n(x)$ of slope $\lambda\le L$:
$$\mathbb E_{x'\in C}\#\{f:(e,f)\in P_N(x')\}=2^{W_N-W_n}\rho_n(e),\qquad\mathbb E_{x'\in C}\sum_{f:(e,f)\in P_N(x')}\rho_N((e,f))=2^{W_N-W_n}\rho_n(e).\tag{11.4}$$
The first (unweighted) identity is the one new ingredient here.

Fix one of the classes $C\in\{C_0,C_2,C_6\}$, $n_0\ge19$ (so $V_{n_0}\ge13\ge\max(V_{\rm cert},2L+1,L+k)$ and $C\in\mathcal F_{n_0}$), $n_\ell=n_0+\ell\ell_0$, $\mathcal F_\ell=\mathcal F_{n_\ell}$, $\Gamma_\ell=\Gamma_L(n_\ell)$, and
$$M_\ell=2^{-W_{n_\ell}}\sum_{e\in P_{n_\ell}}\rho_{n_\ell}(e),\qquad Y_\ell=M_\ell\mathbf 1_{\Gamma_0\cap\dots\cap\Gamma_\ell}.$$

**Lemma 11.27 [proved].** On $C$: (a) $Y_\ell$ is $\mathcal F_\ell$-measurable; (b) on $C\cap\Gamma_\ell$, $\mathbb E[M_{\ell+1}\mid\mathcal F_\ell]=M_\ell$, $\mathbb E[|P_{n_{\ell+1}}|\mid\mathcal F_\ell]=2^{W_{n_{\ell+1}}}M_\ell$, and $W_{n_{\ell+1}}$ is $\mathcal F_\ell$-measurable; (c) $(Y_\ell\mathbf 1_C)$ is a nonnegative supermartingale.

*Proof.* (a) On $C\cap\Gamma_\ell$ every $e\in P_{n_\ell}$ has $\lambda_e\le L$ (Proposition 11.25, as $V_{n_\ell}\ge V_{\rm cert}$), so $\rho_{n_\ell}(e)$ is constant on the atom (Proposition 10.6(ii)); $P_{n_\ell}$, $W_{n_\ell}$ and $\Gamma_0,\dots,\Gamma_\ell$ are $\mathcal F_\ell$-measurable. (b) By backward integrality $P_{n_{\ell+1}}$ is the disjoint union over $e\in P_{n_\ell}$ of the alive children; $W_{n_{\ell+1}}$ is constant on the atom (Lemma 10.5(a)); sum (11.4). (c) $\mathbb E[Y_{\ell+1}\mid\mathcal F_\ell]=\mathbf 1_{\Gamma_0\cap\dots\cap\Gamma_\ell}\mathbb E[M_{\ell+1}\mathbf 1_{\Gamma_{\ell+1}}\mid\mathcal F_\ell]\le Y_\ell$. ∎

**Proposition 11.28 (predictable-barrier bound) [proved].** For $c\in\mathbb R$ and $\ell^*\ge0$ let $A_\ell=\Gamma_0\cap\dots\cap\Gamma_\ell\cap\{W_{n_{\ell+1}}\le-c\}\in\mathcal F_\ell$ and $\mathrm{Hit}=\bigcup_{\ell\le\ell^*}A_\ell$. Then
$$\mu\big(C\cap\mathrm{Hit}\cap\{P_{n_{\ell+1}}\ne\emptyset\ \forall\ell\le\ell^*\}\big)\le2^{-c}\,\mathbb E[Y_0\mathbf 1_C].$$

*Proof.* $\sigma=\min\{\ell\le\ell^*:x\in A_\ell\}$ is a stopping time. On $\{\sigma=\ell\}$, $Y_\ell=M_\ell$ and $2^{W_{n_{\ell+1}}}\le2^{-c}$, so by Lemma 11.27(b) the measure is at most $\sum_{\ell\le\ell^*}\mathbb E[\mathbf 1_C\mathbf 1_{\sigma=\ell}|P_{n_{\ell+1}}|]=\sum_\ell\mathbb E[\mathbf 1_C\mathbf 1_{\sigma=\ell}2^{W_{n_{\ell+1}}}M_\ell]\le2^{-c}\mathbb E[\mathbf 1_CY_{\sigma\wedge(\ell^*+1)}]\le2^{-c}\mathbb E[\mathbf 1_CY_0]$, by optional stopping for the bounded stopping time and the nonnegative supermartingale of Lemma 11.27(c). ∎

Because the barrier event is predictable, this costs $2^{-c}$, without the factor $2^L$ that the survival lower bound of §10.1 would cost.

**Theorem 11.29 (explicit bound) [proved].** For each class, with data

| class | $k$ | $r_0$ | $L$ | $\ell_0$ | $s_L=\max_{\delta<\ell_0}s(\delta)$ | $E_C$ |
|---|---|---|---|---|---|---|
| $C_0$ | 3 | 0 | 1 | 4 | 2 | 1 |
| $C_2$ | 3 | 2 | 3 | 8 | 3 | $2^3\cdot8=64$ |
| $C_6$ | 4 | 6 | 6 | 14 | 3 | $2^6\cdot256=16384$ |

and all integers $G$, $n_0\ge19$, $c$ with $T:=\lfloor G/2\rfloor\ge n_0+\ell_0$, $K:=\lfloor\log_2(T-\ell_0+1)\rfloor$, $2^K\ge\ell_0$ and $K>k$:
$$\mu(C\cap\{g_2\ge G\})\le B_L(n_0)+n_02^{-K}+2^{-c}E_C+2^{-k}\,\mathbb P\big(\mathrm{Bin}(K-k,\tfrac12)\le c+s_L-s(r_0)\big),$$
where $h_L(n)=\frac12(n-\log_2n-3L-4)$ and $B_L(n_0)=\sum_{i\ge1}2^{-\lfloor h_L(\max(n_0,i-\ell_0))\rfloor-1}$.

*Proof.* Let $\ell^*=\max\{\ell:n_{\ell+1}\le T\}$ and $E_{\rm good}=\Gamma_0\cap\dots\cap\Gamma_{\ell^*}$. Then $\mu(C\cap\{g\ge G\})\le\mu(E^c_{\rm good})+\mu(C\cap\{g\ge G\}\cap E_{\rm good}\cap\mathrm{Hit})+\mu(C\cap E_{\rm good}\setminus\mathrm{Hit})$.
*Bad windows.* $\neg\Gamma_\ell$ gives $2M_{n_\ell+\ell_0}>V_{n_\ell}-3L-3\ge n_\ell-\log_2n_\ell-3L-4$, so some $i\le n_\ell+\ell_0$ has $v(x+i)>h_L(n_\ell)\ge h_L(\max(n_0,i-\ell_0))$ ($h_L$ is nondecreasing for $n\ge2$). Since $\mu\{v(x+i)>h\}=2^{-\lfloor h\rfloor-1}$, a union bound over $i$ gives $\mu(E_{\rm good}^c)\le B_L(n_0)$.
*Barrier term.* On $\Gamma_\ell$, $M_N<V_n/2\le V_N/2$ with $N=n_{\ell+1}$, so $V_N<N+M_N$ (Lemma 10.2(b)) gives $V_N<2N\le2T\le G$. On $\{g\ge G\}\cap E_{\rm good}$, Lemma 11.23(d) gives $P_{n_{\ell+1}}\ne\emptyset$ for all $\ell\le\ell^*$, and Proposition 11.28 bounds the term by $2^{-c}\mathbb E[Y_0\mathbf 1_C]$. Since $Y_0\le2^LZ_{n_0}\mathbf 1_{\Gamma_0}$ (and $Y_0=Z_{n_0}\mathbf 1_{\Gamma_0}$ when $L=1$, as $\rho\equiv1$ for $\lambda\le1$) and $\Gamma_0\subseteq\Gamma_*(n_0)$, Proposition 11.26 gives $\mathbb E[Y_0\mathbf 1_C]\le E_C$.
*Walk term.* If $N_K>n_0$, take $\ell$ with $n_\ell<N_K\le n_{\ell+1}$. Then $\delta=n_{\ell+1}-N_K<\ell_0\le2^K$ and $n_{\ell+1}\le2^K+\ell_0-1\le T$, so $\ell\le\ell^*$, and by Lemma 10.2(d) and 11.23(a), $W_{n_{\ell+1}}=W_{N_K}+s(\delta)\le1-s(x\bmod2^K)+s_L$. Off $\mathrm{Hit}$ and on $E_{\rm good}$ this is $>-c$, so $s(x\bmod2^K)\le c+s_L$ ($c$ an integer). Finally $\mu\{N_K\le n_0\}\le n_02^{-K}$, and on $C$ the digits of $x$ in positions $k,\dots,K-1$ are i.i.d. fair bits with $s(x\bmod2^K)=s(r_0)+$(their sum). ∎

**Corollary 11.30 (power law; main result) [proved; constants evaluated by T2 and independently by the lead].** With $\alpha=0.227$, $n_0=\lceil4\log_2G\rceil+3L+40$ and $c=\lfloor\alpha(K-k)\rfloor-s_L+s(r_0)$, for all $G\ge2$:
$$\mu(C_0\cap\{g_2\ge G\})\le29\,G^{-0.227},\quad\mu(C_2\cap\{g_2\ge G\})\le1325\,G^{-0.227},\quad\mu(C_6\cap\{g_2\ge G\})\le1.98\cdot10^5\,G^{-0.227}.$$
Hence, with $R=\mathbb Z_2\setminus(14+16\mathbb Z_2)$, $\mu\{x\in R:g_2(x)\ge G\}\le2.0\cdot10^5\,G^{-0.227}$ for $G\ge4$, and by Theorem 3.1(c) the natural density of $\{a\ge1:\ a\not\equiv14\ (\mathrm{mod}\ 16),\ f(a,2)\ge v_2(a!)+G\}$ is at most $2.0\cdot10^5\,G^{-0.227}$.

*Proof.* $\alpha^*=0.22709\ldots$ is the root of $\alpha=1-H_2(\alpha)$, and $1-H_2(0.227)=0.22726>0.227$. Chernoff gives $\mathbb P(\mathrm{Bin}(N,\frac12)\le\alpha N)\le2^{-N(1-H_2(\alpha))}\le2^{-\alpha N}$, and $2^{-c}\le2^{1+s_L-s(r_0)}2^{-\alpha(K-k)}$. For $G\ge4\ell_0$, $2^K>(T-\ell_0+1)/2\ge G/8$. So the two main terms of Theorem 11.29 total at most $(2^{1+s_L-s(r_0)}E_C+2^{-k})2^{\alpha k}(8/G)^\alpha$, i.e. $20.88$, $1316.4$ and $1.9716\cdot10^5$ times $G^{-\alpha}$, for every $G\ge2^{10}$ (where all hypotheses of Theorem 11.29 hold). The side terms $(B_L(n_0)+n_02^{-K})G^\alpha$ depend on $G$ only through $(n_0,K)$, so they are constant on explicit integer intervals and their supremum is attained at interval ends. The lead's script `lead_t2_constants.py` enumerates every such interval for $2^{10}\le G\le2^{400}$ in exact integer arithmetic (with a rigorous bound for the tail of the series $B_L$) and finds $\sup(B_L(n_0)+n_02^{-K})G^\alpha=1.585$, $1.701$, $1.876$ for $C_0,C_2,C_6$; for $G>2^{400}$ these terms are below $10^{-50}$ since they decay like $G^{\alpha-1}\log G$. So the constants $22.47$, $1318.1$, $1.97162\cdot10^5$ suffice for $G\ge2^{10}$. For $G\le2^{10}$, $\mu(C)\le\frac18\le0.61\,G^{-\alpha}$. Summing over the three classes ($R$ also contains the odd and $4\bmod8$ classes, where $g_2\le3$) gives the last statement. ∎

*(Lead's note.)* The track derived the constants $29,1325,1.98\cdot10^5$ from evaluations at $G=2^j$ plus an interpolation step ("at most twice the neighbouring values") whose factor is not quite right as stated (a direct estimate gives $2^\alpha+2^{1-\alpha}\approx2.9$); the lead's exact piecewise evaluation above replaces that step and confirms the stated constants with room to spare. The supremum of the full bound $\min(\mu(C),\mathrm{RHS})\,G^{0.227}$ over $2^{10}\le G\le2^{400}$, with the exact binomial tail, is $17.53$, $1121$ and $1.680\cdot10^5$ (track's dense-grid check: $17.8$, $1120$, $1.68\cdot10^5$). Three round-3 referees recomputed these constants with their own code. They got side terms $1.584/1.701/1.875$ and main-plus-side constants $22.469/1318.07/197161$. For the supremum of the full bound they got $17.52$–$17.53$, $1119.8$–$1121$ and $1.657$–$1.680\cdot10^5$, depending on grid and range ($G\le2^{120}$ to $2^{400}$). All are below the stated $29$, $1325$, $1.98\cdot10^5$. The bound beats the trivial bound $\mu(C)$ only from $G\approx2^{18}$ ($C_0$), $2^{29}$ ($C_2$), $2^{44}$ ($C_6$) (track, optimised $c$); for all practical $G$ the census bound $\delta_G(2)\le\delta_{32}(2)=0.1016$ (§4.7) is far better. The content is the existence of an explicit polynomial rate.

**Proposition 11.31 (a conditional improvement) [proved, conditional on the stated hypothesis].** With $n_0$ as in Corollary 11.30 (so that $x\bmod2^K$ is $\mathcal F_0$-measurable), suppose (H$_{\rm dec}$): $\mathbb E[Y_0\mathbf 1_C2^{-s(x\bmod2^K)}]\le A\,2^{-k}(3/4)^{K-k}$ for all large $G$. Then $\mu(C\cap\{g_2\ge G\})\le A'G^{-\log_2(4/3)}+O(G^{-1}\log G)$, exponent $0.415$.

*Proof.* Run Proposition 11.28 with the $\mathcal F_0$-measurable level $c(x)=s(x\bmod2^K)-1-s_L$ (the proof is unchanged, since $\{\sigma=\ell\}\in\mathcal F_\ell$ still). On $\{N_K>n_0\}\cap E_{\rm good}$ the walk argument of Theorem 11.29 shows that $\mathrm{Hit}$ occurs. So $\mu(C\cap\{g\ge G\})\le B_L(n_0)+n_02^{-K}+2^{1+s_L}\mathbb E[2^{-s(x\bmod2^K)}Y_0\mathbf 1_C]$; apply H$_{\rm dec}$ and $2^{-K}\le8/G$. ∎

*Why $0.227$ and not $0.415$ unconditionally [sketch].* The martingale reads the same low digits that determine the walk minimum, so $\mathbb E[M\mid x\bmod2^K]$ is not the initial value. If the only information used is $\mathbb EM\le C$ and the law of $s(x\bmod2^K)\sim\mathrm{Bin}(K,\frac12)$, an adversarial coupling ($M=2^{s-c}$ on $\{s\le\alpha^*K\}$) shows that $2^{-\alpha^*K}$ cannot be beaten.

**Proposition 11.32 (the triple root at $-2$) [proved].** $S_{\{1,3\}}(x)=(x+2)^3$; hence $\gamma_2(m)\ge3v(m-2)$ for $m\ge3$, and for $x$ with $v(x+2)=t$ and any integer $m\ne2$ with $v(m-2)<t$, the Taylor inequality for $S_{\{1,3\}}$ at $-m$ has its minimum at $i=3$, not $i=1$. So no single integer point can certify a bounded slope for the paths extending $\{1,3\}$.

*Proof.* Expand. $S_{\{1,3\}}(-m)=(2-m)^3$. At $-m$ with $v(x+m)=v(m-2)=:j<t$ the $i=3$ term has valuation $3j$ while the $i=1$ term $3(x+2)^2(-m-x)$ has valuation $2t+j>3j$. ∎

On $14+16\mathbb Z_2=\{v(x+2)\ge4\}$ the paths with $e_2=1,e_3=0$ ("family A") have slope exactly $t=v(x+2)$ (same proof as Proposition 11.25(c)); a rate for them is only sketched by the track. The paths with $e_2=0,e_3=1$ ("family B") have unbounded slopes: measured maximal slopes are exactly $2t+1$ for odd $t=5,\dots,11$, with tails up to $\approx5.5t$ for even $t$ [computer-assisted, 300 samples per $t$]. In 60 000 exact samples to cap 512 (an independent Python reimplementation of the carry recursion, `gcap.py`; its $2\delta_{512}=0.0213$ agrees with T4's $0.02136$), the class $14\bmod16$ carries $41.5\%,58.2\%,61.6\%,63.1\%,64.2\%$ of the survivors among even $x$ at $G=16,64,128,256,512$ [computer-assisted, Monte Carlo]. So Corollary 11.30 controls only about a third of the survivors, and **no rate for $\delta_G(2)$ itself was obtained, not even $C/\log G$.**

**Heuristic 11.33 (a varying-environment predictor; Kitamura's fit) [heuristic].** Conditioning on the environment $(v(x+i))_i$, the population is approximately a branching process in a varying environment: deterministic doubling at steps with $x+n+1$ odd, and at most one child, with mean $2^{1-D}$, otherwise. The classical survival estimate for such processes (Agresti 1975; Kersting 2020; cited by the track from memory, with bibliographic records verified by the round-3 novelty referee; only the heuristic shape is used here) suggests
$$\mathbb P(g_2(x)\ge G\mid x)\approx\min\big(1,\kappa/A_G(x)\big),\qquad A_G(x)=\sum_{k<n_G(x),\ x+k+1\text{ odd}}2^{-W_{k+1}(x)},$$
with one constant $\kappa\approx2.6$ fitted to T4's Monte Carlo. Using $\sum_{j<2^K}2^{-s(j)}=(3/2)^K$ one gets $\mathbb E[1/A_G]\approx(3/4)^K(2/3)^K=2^{-K}\approx1/G$: the exponent $1$ splits as $\log_2\frac43$ (drift of the walk; the most a first-moment argument can give) plus $\log_2\frac32$ (variance at doubling steps). Tests: $G\,\mathbb E[1/(2A_G)]=2.09$–$2.12$ for $G=16,\dots,16384$; predicted/observed $\delta_G(2)$ ratios $0.96$–$1.06$ for $256\le G\le2048$ (but $2.05$ at $G=16$); $N(A,G)$ for $A=256,1024,4096$ and $256\le G\le4094$ within $2$ Poisson standard deviations. For natural $a$ the walk is bounded below by $1-s(a)$, and the predictor gives $\mathbb P(g_2(a)\ge G)\asymp2^{-s(a)}G^{-0.585}$ for $G\gg a$.

*Reconciliation of the two fits of §2 and §10.1 Remark 4 [heuristic reading of T4's data].* (1) Kitamura's "$\approx11.5/G$" matches $2\delta_G(2)$, the surviving fraction among even $a$: $2\delta_GG=10.5$–$11.6$ for $256\le G\le2046$ (§11.6). Kitamura's repository gives no definition of the fit; this identification is an inference. (2) The note's $\delta_G(2)\approx0.7/\sqrt G$ was fitted on $8\le G\le254$, where the local exponent is still $0.5$–$0.85$; the predictor reproduces this transient. (3) Natural $a$ behave like Haar points for $G\lesssim a$. So the two fits are one curve seen in two windows, plus a factor $2$.

**Conjecture 11.34 [conjecture].** (a) $G\,\delta_G(2)\to c_2\in(0,\infty)$, with $c_2\approx5.5$–$6$. (b) For each $\lambda>0$, $\#\{a\le X:g_2(a)\ge\lambda a\}\sim q(\lambda)\log_2X$ with $q(\lambda)\asymp\lambda^{-\log_2(3/2)}$ as $\lambda\to\infty$. *Evidence:* T4's Monte Carlo (§11.6) for (a); for (b), the counts $27,15,6,3,3,2,1$ of even $16\le a\le4094/\lambda$ with $g_2(a)\ge\lambda a$ ($\lambda=1,2,\dots,64$) against predicted $33.6,16.4,8.1,4.0,2.0,0.9,0.4$ — small counts, not decisive.

### 11.4 Q3, Fourier route: the $L^2$ (collision) mass of the tail measure (track T3a)

No decay of the $L^1$ shell sums $T_p(k)$ of §10.4 was obtained; RMF, MI-13 and Q3 remain open. The work moved to the $L^2$ version, the "cheaper intermediate target" of §10.6 item 2.

*Set-up.* Fix $p$ and $N_0\ge1$, $e_0=v_p(N_0!)$, $x_n=n!/p^{e_0}$ ($n\ge N_0$). Let $\nu$ be the law of $X=\sum_{n\ge N_0}\varepsilon_nx_n$ for i.i.d. fair coins; its support is $p^{-e_0}E_{N_0}$ (Proposition 3.13(c)). With $\eta_n=\varepsilon_n-\varepsilon_n'$ (law $\frac14,\frac12,\frac14$ on $-1,0,1$; $\mathbb Ee(\xi\eta_nx)=\cos^2(\pi\xi x)$), define
$$C_k=\sum_{\xi\in p^{-k}\mathbb Z_p/\mathbb Z_p}|\hat\nu(\xi)|^2=p^k\,\mathbb P\Big(\sum_n\eta_nx_n\equiv0\ (p^k)\Big),\qquad C_\infty=\lim_kC_k\in[1,\infty],$$
the second equality by Parseval. *Level groups* are $G_a=\{n:v(x_n)=a\}$; for an attained level $a$, $J$ is the jump to the next attained level. For $N_0=pm_0$ the groups are the blocks $\{pm,\dots,pm+p-1\}$, with level $e_m-e_0$ and jump $J_m=1+v_p(m+1)$.

**Lemma 11.35 [proved].** (a) If $C_\infty<\infty$ then $\nu$ has an $L^2$ density $f$ with $\|f\|_2^2=C_\infty$, and $\lambda(E_{N_0})/\lambda(p^{e_0}\mathbb Z_p)\ge1/C_\infty$. (b) For every $k$ the proportion of classes of $p^{e_0}\mathbb Z_p/p^{e_0+k}$ that meet $E_{N_0}$ is $\ge1/C_k$. (c) $C_k-C_{k-1}\le T(k):=\sum_{\mathrm{ord}\xi=p^k}|\hat\nu(\xi)|$ and $T(k)\le(p^k(1-\frac1p)(C_k-C_{k-1}))^{1/2}\le(p^kC_k)^{1/2}$.

*Proof.* (a) $f_k(x)=p^k\nu(x+p^k\mathbb Z_p)$ is a Haar martingale with $\|f_k\|_2^2=C_k$; an $L^2$-bounded martingale converges in $L^2$ to a density $f$ of $\nu$; and $1=\int_Sf\le\|f\|_2\lambda(S)^{1/2}$ for the compact support $S$. (b) The same Cauchy–Schwarz at level $k$. (c) $\cos^2\le|\cos|$, and Cauchy–Schwarz over the $p^k(1-1/p)$ frequencies of exact order $p^k$. ∎

So $C_\infty<\infty$ would give positive Haar measure of a tail set; it follows from any of the $L^1$ hypotheses of §10 and is strictly weaker than the full coverage $E_{N_0}=p^{e_0}\mathbb Z_p$ that Q3 needs (Lemma 1.4).

**Theorem 11.36 (exact carry cocycle) [proved].** Let $a$ be an attained level with jump $J$. Put $Z_{<a}=\sum_{v(x_n)<a}\eta_nx_n$, $Y_a=\sum_{n\in G_a}\eta_nx_n/p^a$, and on $\{p^a\mid Z_{<a}\}$ the carry $c_a=Z_{<a}/p^a$. Let $\hat\kappa_a(\xi)=\mathbb E[e(\xi Z_{<a}/p^a)\mathbf 1\{p^a\mid Z_{<a}\}]$ and $\varphi_a(\xi)=\prod_{n\in G_a}\cos^2(\pi\xi x_n/p^a)$ for $\xi\in\mathbb Q_p/\mathbb Z_p$.
- (i) $\hat\kappa_a(\xi)=p^{-a}\sum_{t\in\mathbb Z/p^a}\prod_{v(x_n)<a}\cos^2(\pi\frac{\xi+t}{p^a}x_n)\ge0$ and $\hat\kappa_a(0)=p^{-a}C_a$; so $\hat\rho_a=\hat\kappa_a/\hat\kappa_a(0)\in[0,1]$ is the characteristic function of the conditional law of $c_a$.
- (ii) For $1\le j\le J$: $C_{a+j}=C_a(1+D_a^{(j)})$ with $1+D_a^{(j)}=\sum_{\xi\in p^{-j}\mathbb Z/\mathbb Z}\hat\rho_a(\xi)\varphi_a(\xi)=p^j\,\mathbb P(c_a+Y_a\equiv0\ (p^j)\mid p^a\mid Z_{<a})$.
- (iii) $\hat\kappa_{a+J}(\xi)=p^{-J}\sum_{\zeta:\ p^J\zeta=\xi}\hat\kappa_a(\zeta)\varphi_a(\zeta)$: a positive transfer operator on functions on $\mathbb Q_p/\mathbb Z_p$.
- (iv) $0\le D_a^{(j)}\le\Gamma_{G_a}(j):=\sum_{0\ne\xi\in p^{-j}\mathbb Z/\mathbb Z}\varphi_a(\xi)=p^j\mathbb P(Y_a\equiv0\ (p^j))-1$; among all carries independent of $Y_a$, $p^j\mathbb P(c+Y_a\equiv0)$ is maximised by $c\equiv0$.

*Proof.* (i) Use $\mathbf 1\{p^a\mid z\}=p^{-a}\sum_te(tz/p^a)$, independence, and $\mathbb Ee(\theta\eta x)=\cos^2(\pi\theta x)$; at $\xi=0$ the sum is $p^{-a}\sum_{\zeta\in p^{-a}\mathbb Z/\mathbb Z}|\hat\nu_{<a}(\zeta)|^2=p^{-a}C_a$, since elements of level $\ge a$ contribute factors $1$ there. (ii) No level lies strictly between $a$ and $a+J$, so $Z_{<a+j}=Z_{<a}+p^aY_a$ and $C_{a+j}=p^{a+j}\mathbb E[\mathbf 1\{p^a\mid Z_{<a}\}\mathbf 1\{p^j\mid c_a+Y_a\}]=p^a\sum_{\xi\in p^{-j}\mathbb Z/\mathbb Z}\hat\kappa_a(\xi)\varphi_a(\xi)$, by independence of $Y_a$ and $Z_{<a}$; divide by $C_a=p^a\hat\kappa_a(0)$. (iii) Expand $\mathbf 1\{p^J\mid c_a+Y_a\}$ in the same way. (iv) $\hat\rho_a\in[0,1]$, $\varphi_a\ge0$, $\hat\rho_a(0)=\varphi_a(0)=1$; for any independent carry $c$, $\sum_\xi\mathbb Ee(\xi c)\varphi_a(\xi)\le\sum_\xi\varphi_a(\xi)$. ∎

In $L^2$ the kernel $\cos^2$ is a trigonometric polynomial, which is why this exact probabilistic representation exists; there is no analogue in $L^1$. (The factorisation (ii) was first found, in code, by an earlier instance of this track; the proof and the transfer form are the reporting instance's.)

**Lemma 11.37 (the gate-block law) [proved; table computer-assisted].** Let $e_u=(-1)^u(p-1)!/u!$ ($0\le u<p$), $W=\sum_u\eta_ue_u$, $\Gamma_p(j)=p^j\mathbb P(W\equiv0\ (p^j))-1$, and $\mathrm{dist}_p(j)$ the number of distinct subset sums of $(e_u)$ mod $p^j$.
- (a) For $N_0=pm_0$, $m\ge m_0$, block $m$ at level $a$: $x_{pm+r}/p^a=U_mP_m(r)$ with $U_m=(pm)!/p^{e_m}$ a unit and $P_m(r)=\prod_{i\le r}(pm+i)\equiv\epsilon_pe_{p-1-r}\pmod{p^{J_m}}$ ($\epsilon_p=1$ for odd $p$, $\epsilon_2=-1$). Hence for $j\le J_m$ the block has $\Gamma_{\rm block}(j)=\Gamma_p(j)$ and exactly $\mathrm{dist}_p(j)$ distinct subset sums mod $p^j$.
- (b) $W=0$ iff $\eta_0=\eta_1$ and $\eta_u=0$ for all $u\ge2$; so $\mathbb P(W=0)=3/2^{p+1}$, and the subset sums of $(e_u)$ take exactly $3\cdot2^{p-2}$ distinct integer values.
- (c) Let $J_0(p)$ be the least $j$ with $\mathbb P(W\equiv0\ (p^j))=\mathbb P(W=0)$. For $j\ge J_0(p)$, $\Gamma_p(j)=\frac32p^j2^{-p}-1$; $\Gamma_p$ is nondecreasing in $j$.
- (d) $\Gamma_p(1)>0$ for odd $p$; $\Gamma_2(1)=0$.

*Proof.* (a) For odd $p$ this is Theorem 3.9(b). For $p=2$: $P_m(0)=1=-e_1$ and $P_m(1)=2(m+1)-1\equiv-1=-e_0\pmod{2^{J_m}}$. Multiplication by the unit $\epsilon_pU_m$ permutes $p^{-j}\mathbb Z/\mathbb Z$. (b) $e_0=-e_1=(p-1)!$; for $u\ge2$, $\sum_{v>u}|e_v|<|e_u|/u$ (superincreasing), and $\sum_{u\ge2}|e_u|<(e-2)(p-1)!<(p-1)!$. If $W=0$ then $|\eta_0-\eta_1|(p-1)!<(p-1)!$, so $\eta_0=\eta_1$, and then superincreasing forces $\eta_u=0$ for $u\ge2$. $\mathbb P(\eta_0=\eta_1)=\frac38$ and $\mathbb P(\eta_u=0\ \forall u\ge2)=2^{2-p}$. Subset sums are $s+\sum_{u\ge2}\epsilon_ue_u$ with $s\in\{0,\pm(p-1)!\}$, pairwise distinct by the same estimates. (c) $\{W=0\}\subseteq\{p^j\mid W\}$ and every sign vector has positive probability, so equality of probabilities forces equality of events, which persists for larger $j$. $\Gamma_p(j)$ is a sum of nonnegative terms over a growing set. (d) For odd $p$, $\xi e_u\notin\frac12+\mathbb Z$ for $\xi=t/p$, so every term is positive; for $p=2$, $\varphi_2(1/2)=0$. ∎

Exhaustive enumeration over the $3^p$ sign vectors (`gamma_enum.c`, $p\le19$; agreeing with an earlier independent Python DP for $p\le13$, and with the lead's own brute force for $p\le11$, which reproduces every weight count $4^p\mathbb P(p^J\mid W)$, $J\le8$) gives:

| $p$ | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 |
|---|---|---|---|---|---|---|---|---|
| $\Gamma_p(1)$ | $0$ | $1/32$ | $9/256$ | $117/8192$ | $753/2^{19}$ | $739/2^{25}$ | $2617/2^{32}$ | $13507/2^{37}$ |
| $J_0(p)$ | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 7 |
| $\max\{j:\mathrm{dist}_p(j)=p^j\}$ | 1 | 1 | 1 | 2 | 2 | 2 | 3 | 3 |

The last row reproduces the covering depths $L_p$ of §3.5.

For $j\ge0$ put $f_p(j)=\log_p(1+\Gamma_p(j+1))\in[0,j+1]$, $\theta_p=\frac{p-1}p\sum_{j\ge0}(1-\frac1p)p^{-j}f_p(j)$, and $\theta^{\rm set}_p=\frac{p-1}p\sum_{j\ge0}(1-\frac1p)p^{-j}\log_p\big(p^{j+1}/\mathrm{dist}_p(j+1)\big)$; by Lemma 11.37(c) the summands are affine in $j$ from $j+1=J_0(p)$ on, so both series are summed in closed form.

**Theorem 11.38 (an unconditional exponent bound) [proved; constants computer-assisted in interval arithmetic].** For every prime $p$ and every $N_0\ge1$, $\log_pC_k\le\theta_pk+A_p\log_p^2k+B_{p,N_0}$ for $k\ge2$. Upper bounds for $\theta_p$ (mpmath interval arithmetic on the exact rationals above, `theta.py`):

| $p$ | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 |
|---|---|---|---|---|---|---|---|---|
| $\theta_p\le$ | $\log_23/4\le0.396241$ | 0.229401 | 0.11014 | 0.026608 | $6.2357\cdot10^{-3}$ | $9.0768\cdot10^{-4}$ | $8.4107\cdot10^{-5}$ | $3.4067\cdot10^{-5}$ |
| $1-\theta^{\rm set}_p\ge$ | 0.64624 | 0.80687 | 0.92369 | 0.98555 | 0.99826 | 0.999656 | 0.999965 | 0.999993 |

*Proof.* Let $m_0=\lceil N_0/p\rceil$. If $p\nmid N_0$ the first group is a partial block at level $0$, whose factor is trivially at most $p^{1+v_p(m_0)}$; all later groups are full blocks. Given $k$, let $M$ be the largest $m$ with $a_m<k$. Apply Theorem 11.36(ii),(iv) block by block, with $j=J_m$ for $m<M$ and $j=k-a_M\le J_M$ for $m=M$; by Lemma 11.37(a),(c), each factor is at most $1+\Gamma_p(J_m)$. So $\log_pC_k\le B+\sum_{i=1}^{M+1}f_p(v_p(i))$. Since $\#\{i\le X:v_p(i)=j\}\le X(1-\frac1p)p^{-j}+1$ and vanishes for $j>\log_pX$, and $f_p(j)\le j+1$, the sum is $\le XF_p+\frac12(\log_pX+2)^2$ with $F_p=\sum_j(1-\frac1p)p^{-j}f_p(j)$. Finally $e_M=(pM-s_p(M))/(p-1)<k+e_0$ gives $X=M+1\le\frac{p-1}p(k+e_0+\log_pk+O(1))$. ∎

The lead checked $\theta_2=\log_23/4$ by hand ($f_2(0)=0$, $f_2(j)=j-2+\log_23$ for $j\ge1$) and re-ran `theta.py` (identical output).

*[Corrected, round-3 referees.]* The table previously printed $\theta_3\le0.22940$. That is false by $2.8\cdot10^{-8}$, because the decimal was truncated rather than rounded up, and the excess $2.8\cdot10^{-8}k$ is not absorbed by the $O(\log^2k)$ term. From $\Gamma_3(1)=1/32$, $J_0(3)=2$ and $\Gamma_3(j)=\frac3{16}3^j-1$ for $j\ge2$, the closed form is $\theta_3=\frac49\big[\log_3\frac{33}{32}+\frac74-2\log_32\big]=0.2294000283$. This value was found by four referees and re-derived by the lead from the definition (`code/round3/lead/lead_r3fix_checks.py`: closed form and a direct 400-term sum agree), so the correct bound is $\theta_3\le0.229401$. Likewise $\log_23/4=0.39624063$ is now printed as an upper bound. All other entries of both rows were confirmed by the referees as rounded in the safe direction. (The T3a track report's $\theta_5\le0.11013$ was also too small; the note's $0.11014$ is correct.) *Constants:* the form $A_p\log_p^2k+B_{p,N_0}$ uses $\log_pX\le\log_pk+\log_p(1+e_0)+O(1)$ for the quantity $X\le\frac{p-1}p\,(k+e_0+\log_pk+O(1))$ of the proof, and hence $(\log_pX+2)^2\le2\log_p^2k+2(\log_p(1+e_0)+O(1))^2$ for $k\ge2$; so $A_p$ does not depend on $N_0$. *[Wording corrected after the round-3 re-check; the conclusion is unchanged.]*

**Corollary 11.39 [proved].** For every $p$, $N_0$ and $\varepsilon>0$:
- (a) $\mathbb P\big(\sum_n\eta_nn!/p^{v(N_0!)}\equiv0\ (p^k)\big)\le C_\varepsilon p^{-(1-\theta_p-\varepsilon)k}$;
- (b) every Borel set charged by $\nu$ has Hausdorff dimension $\ge1-\theta_p$; in particular so does $E_{N_0}$, since $\nu$ is carried by $p^{-e_0}E_{N_0}$ and scaling by $p^{e_0}$ preserves dimension. Moreover $\dim_HE_{N_0}\ge1-\theta^{\rm set}_p$ (e.g. $\ge0.999656$ at $p=13$; *[corrected, round-3 referees: previously printed $\ge0.99966$, which rounds the lower bound $0.99965675$ up]*);
- (c) for $N_0=p$, $T_p(k)\le p^{(1+\theta_p)k/2+O(\log^2k)}$ — a square-root saving over the trivial $p^k$, **not decay**.

*Proof.* (a) is $C_kp^{-k}$. (b) $\int\nu(x+p^k\mathbb Z_p)\,d\nu(x)=C_kp^{-k}$; by Markov and Borel–Cantelli, for $s<1-\theta_p$, $\nu$-a.e. $x$ has $\nu(x+p^k\mathbb Z_p)\le p^{-sk}$ for large $k$; the ultrametric mass distribution principle gives $\mathcal H^s>0$ on any set of positive $\nu$-measure. For $\theta^{\rm set}$, replace the coins on block $m$ by the uniform law on one subset per distinct residue mod $p^{J_m}$ (still supported in $E_{N_0}$); by Theorem 11.36 for general independent group laws (replace $\varphi_a$ by $|\hat\mu_a|^2$), the block factor is $p^{J_m}/\mathrm{dist}_p(J_m)$; repeat the proofs. (c) Lemma 11.35(c) and Theorem 11.38. ∎

**Proposition 11.40 (the $L^2$ analogue of Corollary 10.20) [proved].** Let $p$ be odd, $N_0=pm_0$, and let a *window* $\mathcal W$ be a run of consecutive full blocks $m_1\le m<m_2$, with $J_{\mathcal W}=a_{m_2}-a_{m_1}$, $Y_{\mathcal W}=\sum_{n\in\mathcal W}\eta_nx_n/p^{a_{m_1}}$ and $\Gamma_{\mathcal W}=p^{J_{\mathcal W}}\mathbb P(Y_{\mathcal W}\equiv0\ (p^{J_{\mathcal W}}))-1$. Then (a) $C_{a_{m_2}}=C_{a_{m_1}}\cdot p^{J_{\mathcal W}}\mathbb P(c+Y_{\mathcal W}\equiv0\mid\cdot)$ with $c$ the carry, and for every carry independent of $Y_{\mathcal W}$ this factor is $\le1+\Gamma_{\mathcal W}$, with equality for $c\equiv0$; (b) $\Gamma_{\mathcal W}\ge\Gamma_p(1)>0$; (c) hence chaining supremum bounds over $r$ windows gives at best $(1+\Gamma_p(1))^r$, and a proof of $C_\infty<\infty$ must use the actual carry law at all but finitely many window boundaries.

*Proof.* (a) As Theorem 11.36(ii),(iv), with the window in place of a group. (b) At the frequencies $t/p$ every element of relative level $\ge1$ contributes $\cos^2(\pi\cdot\text{integer})=1$, so $\varphi_{\mathcal W}(t/p)=\varphi_p(U_{m_1}t/p)$ by Lemma 11.37(a); summing over $t$ gives $\Gamma_p(1)$, and the other terms are $\ge0$. (c) Multiply. ∎

The maximising law $c\equiv0$ is a genuine carry law (the event "all $\eta_n=0$ so far" has positive probability). At $p=2$, (b) fails ($\Gamma_2(1)=0$); only windows containing a gate pay.

**Proposition 11.41 (no uniform spectral gap at depth; the deep-gate law) [proved].**
- (a) For $y_1,\dots,y_s\in\mathbb Z_p$ and $d\ge s+1$ there is $\xi\ne0$ in $p^{-d}\mathbb Z/\mathbb Z$ with $\prod_{i\le s}\cos^2(\pi\xi y_i)\ge\cos^{2s}(\pi p^{-\lfloor(d-1)/s\rfloor})\ge1-s\pi^2p^{-2\lfloor(d-1)/s\rfloor}$.
- (b) If $J_m\ge J_0(p)$, then conditional on $p^{J_m}\mid Y_m$ the quotient $Y_m/p^{J_m}$ has law $\frac23\delta_0+\frac16(\delta_{U'}+\delta_{-U'})$ with $U'=U_mP_m(p-2)(m+1)p^{-v_p(m+1)}\in\mathbb Z_p^\times$; its characteristic function at $U'^{-1}p^{-d}$ is $\frac23+\frac13\cos(2\pi p^{-d})\to1$.
- (c) The analogous pigeonhole bound holds for any conditional law with $K$ atoms: some $\xi\ne0$ of order $\le p^d$ ($d\ge K+1$) has $\mathrm{Re}\,\psi(\xi)\ge\cos(2\pi p^{-\lfloor(d-1)/K\rfloor})$.

*Proof.* (a) With $M=p^{\lfloor(d-1)/s\rfloor}$ ($M^s<p^d$, $M\ge2$), two distinct $t,t'\in\mathbb Z/p^d$ have the points $((ty_i\bmod p^d)/p^d)_i$ in the same cube of side $1/M$; $\xi=(t-t')/p^d$ works since $\|\xi y_i\|<1/M\le\frac12$. The last form follows from $\cos x\ge1-x^2/2$ and Bernoulli. (b) By Lemma 11.37(a),(c), $\{p^{J_m}\mid Y_m\}=\{W=0\}$, on which only $u=0,1$ (i.e. $r=p-1,p-2$) carry a common sign $\eta$, with conditional weights $4:1:1$ for $\eta=0,\pm1$, and $Y_m=\eta U_m(P_m(p-1)+P_m(p-2))=\eta U_mP_m(p-2)\,p(m+1)$. (c) As (a), applied to the atoms. ∎

*Interpretation [heuristic].* A supremum-norm spectral-gap bound at depth $d$ needs windows of $\gtrsim d/\log d$ elements, hence (Theorem 3.12(a), Proposition 3.14) unboundedly many $p$-adic digits of the unit parts — a Fourier-side companion of the barrier lemma, not an impossibility theorem for all methods.

**Proposition 11.42 (a criterion for $C_\infty<\infty$) [proved].** For odd $p$, $N_0=pm_0$ and blocks $m\ge m_0$, let $\Delta_m=p^{J_m}\mathbb P(c_{a_m}\equiv0\ (p^{J_m})\mid p^{a_m}\mid Z_{<a_m})-1=\sum_{0\ne\xi\in p^{-J_m}\mathbb Z/\mathbb Z}\hat\rho_{a_m}(\xi)\ge0$. Then $D_m\le\Delta_m$, and for non-gate blocks ($J_m=1$) $D_m\ge\varphi_{\min}\Delta_m$ with $\varphi_{\min}=\min_{p\nmid t}\varphi_p(t/p)>0$. Hence $\sum_m\Delta_m<\infty\Rightarrow C_\infty<\infty\Rightarrow\sum_{m:J_m=1}\Delta_m<\infty$.

*Proof.* $D_m=\sum_{\xi\ne0}\hat\rho\varphi$ with $\hat\rho,\varphi\ge0$ and $\varphi\le1$ (Theorem 11.36(ii)); and $C_\infty=C_{a_{m_0}}\prod_m(1+D_m)$. ∎

**Computation 11.43 (exact $L^2$ masses) [computer-assisted].** $C_k$ is computed as the exact rational $p^kS/4^M$, $S=\sum_rN(r)^2$, by two in-memory layouts of one program (`l2dp.c`, `l2dp_twoarray.c`; exact 128-bit and CRT arithmetic). Independent checks: `verify_l2_r3.py` recomputes 111 cases with $p^k\le4\cdot10^6$ exactly (0 mismatches; Fourier formula to $1.3\cdot10^{-15}$), `verify_wide_r3.py` checks 11 deeper cases modulo $\approx2^{95}$; the lead re-ran `verify_l2_r3.py` (identical). The last 1–4 levels of each deep run rest on one author's program. Theorem 11.36(iv) ($0\le D\le\Gamma$) holds on all 12 data sets. *[Clarified after the round-3 referees.]* The archived checker output `data/round3/T3a-q3-fourier/data/l2_summary.txt` prints `viol=1` for $(p,N_0)=(3,1)$. That flag is an artefact of the checker, not a violation. It compares the partial first group $\{1!,2!\}$ (ratio $1.125$) with the full-block bound $1+\Gamma_3(1)=1.03125$. The correct bound for that group is its own $1+\Gamma_{G_0}(1)=1+1/8$, which holds with equality. Two referees reached this conclusion independently. Independent recomputation by the computational referee (`l2ref.c`) matches every exact level ($p=2$, $k\le27$; $p=3$, $k\le16$; $p=5$, $k\le11$; $p=7$, $k\le9$), and the double-precision values match at $p=11,13$.

| $p$, $N_0$ | depth $k$ | $C_k-1$ | product bound of Theorem 11.38 |
|---|---|---|---|
| 2, 1 | 28 | 3.47616 | 410.06 |
| 3, 1 | 17 | 0.310525 | 33.95 |
| 5, 1 | 12 | 0.0790030 | 5.124 |
| 7, 1 | 10 | 0.0193292 | 1.2515 |
| 11, 1 | 7 | $2.06856\cdot10^{-3}$ | 1.01073 |
| 13, 1 | 7 | $2.86586\cdot10^{-5}$ | 1.000161 |
| 13, 13 | 6 | $2.25377\cdot10^{-5}$ | 1.000132 |

Per-block ratios $D/\Gamma$ collapse at odd $p$ (at $p=13$, $N_0=13$: $1,\ 2.3\cdot10^{-2},\ 2.0\cdot10^{-8},\dots,4.2\cdot10^{-15}$) and decay slowly at $p=2$ (gates only).

**Conjecture 11.44 ($L^2$ dichotomy) [conjecture].** For odd $p$ and $N_0\in\{1,p\}$ (plausibly every $N_0$), $C_\infty(p,N_0)<\infty$, so $E_{N_0}$ has positive Haar measure, with relative measure $\ge1/C_\infty$; estimates $C_\infty(3,1)\approx1.31$, $C_\infty(5,1)\approx1.079$, $C_\infty(7,1)\approx1.0193$, $C_\infty(13,1)\approx1.0000287$. For $p=2$, $C_k\asymp k^\alpha$ with $\alpha\approx0.6$–$0.75$, so there is no $L^2$ density.

*Evidence [heuristic; sequential Monte Carlo on the exact carry recursion with the true factorials].* Compared with exact values: at $p=3$, $k=17$ the SMC gives $1.2989$ against the exact $1.3105$, so $C$ agrees to about $1\%$ but the excess $C-1$ is $3.7\%$ low; at $p=2$, $k=16$, $3.0634\pm0.0014$ against $3.0623$. *[Reworded after the round-3 computational referee; previously "validated".]* So $C_\infty(3,1)\approx1.31$ is an extrapolation of the exact data, and the SMC does not sharpen it. At $p=2$ ($P=8\cdot10^6$ particles, 2 runs): $C_k\approx5.35,8.96,13.9,21.8,34.9,51.2$ at $k=32,64,128,256,512,1000$ (random model: $5.06,\dots,37.4$, exponent $\log_2\frac32$). At $p=3,5,7$ the pooled per-block defects beyond level 20 are $0$ within $\approx10^{-5}$ (non-gates) and $10^{-4}$ (level-1 gates), up to depth 2000/1000/400. At $p=3$, slow growth of $\log C$ (below $\approx0.1$ per decade) is not excluded. Positive measure of $E_{N_0}$ would not by itself settle Q3.

### 11.5 Q3, covering route: self-similarity, the lifting criterion, a negative $L^2$ result, and $f(1,19)$ (tracks T3b, T3b-finish)

Notation of §3.7: $y_i(K')=\prod_{s=1}^i(p^tK'-(H-s))$, $c=v((H-1)!)$, $M=t+c$, $\rho=(H-1)\bmod p$, $E_p=\{(-1)^u/u!\}_{u<p}$, $V_p=(p-1)!\,\Sigma(E_p)$ (the subset sums), $D_p=\lceil\log_p(e(p-1)!)\rceil$, $\ell(i)=\lfloor\log_pi\rfloor$ ($\ell(0)=0$).

**Theorem 11.45 (exact self-similarity for windows of length $p^D$) [proved].** Let $1\le D<t$, $H=p^D$, $X=p^tK'$ with $K'\in\mathbb Z_p$. For $0\le i<H$,
$$y_i(K')=i!\,A_i\,B_i(K'),\qquad A_i=(-1)^i\binom{p^D-1}{i}=\prod_{s\le i}\Big(1-\frac{p^D}s\Big),\qquad B_i(K')=\prod_{s\le i}\Big(1+\frac{p^tK'}{s-p^D}\Big),$$
and (a) $A_i\equiv1\pmod{p^{D-\ell(i)}}$; (b) $B_i\equiv1\pmod{p^{t+v(K')-\ell(i)}}$; (c) $A_i\equiv1-p^DH_i\pmod{p^{2(D-\ell(i))}}$ with $H_i=\sum_{s\le i}1/s$; (d) $v(y_i-i!A_i)\ge t+v(K')+v(i!)-\ell(i)$. Each of the four bounds is attained for some $i$ (exact check on 10 parameter sets, `selfsim_check.py`, re-run by the lead); they are not attained for every $i$ (see below). *(Credit: (a) is the classical congruence $(-1)^i\binom{p^D-1}i\equiv1\pmod{p^{D-\lfloor\log_pi\rfloor}}$.)*

*Proof.* $X-(p^D-s)=(s-p^D)(1+X/(s-p^D))$ and $\prod_{s\le i}(s-p^D)=(-1)^i(p^D-1)!/(p^D-1-i)!=i!\prod_{s\le i}(1-p^D/s)$. (a) For $s\le i<p^D$, $v(s)\le\ell(i)<D$, so each factor lies in the group $1+p^{D-\ell(i)}\mathbb Z_p$. (b) $v(p^tK'/(s-p^D))=t+v(K')-v(s)$. (c) Expanding $\prod(1-a_s)$ with $v(a_s)\ge D-\ell(i)$, terms with $\ge2$ factors have valuation $\ge2(D-\ell(i))$. (d) $y_i-i!A_i=i!A_i(B_i-1)$. ∎

So for the family $H=p^{t-1}$ of Theorem 10.16 the position $K'$ enters $y_i$ only from digit $t+v(i!)-\ell(i)$ on, *at the earliest*: (a)–(d) are lower bounds on valuations.

*[Withdrawn, round-3 logic referee.]* An earlier text stated a "Consequence [proved]": that no element of this window is congruent to its factorial at the top digit $t+c$ of the demand, and hence that $\mathrm{Cov}(p,t,p^{t-1})$ is not implied by any covering statement about the factorials $i!$ through congruences. **That statement is false.** The argument only showed that the lower bound (d) does not reach digit $t+c$, and (d) is not sharp near $i=p^D-1$, where the terms $1/(s-p^D)$ with $v(s)=\ell(i)$ cancel in pairs.

Counterexample [computer-assisted, exact integers; found by the referee and re-derived by the lead in `code/round3/lead/lead_r3fix_checks.py`]: take $p=3$, $t=3$, $H=9$, $c=v_3(8!)=2$, demand $3^5$. For each unit $K'\in\{1,2,4,5\}$, $v_3(y_8-8!)=5=t+c$, so $y_8\equiv8!\pmod{3^5}$; the same holds for $i=6$. Further cases with $y_i\equiv i!\pmod{p^{t+c}}$:
- $p=5$, $t=3$: $i=20,24$;
- $p=7$, $t=3$: $i=42,48$;
- $p=3$, $t=4$: $i=20,25$;
- $p=3$, $t=5$: $i=76$.

No claim about congruence-based covering arguments survives. The weaker statement, that such arguments would have to use the specific digits of the $y_i$ beyond those controlled by (a)–(d), is only a heuristic restatement of the barrier lemma (Theorem 3.10). Theorem 11.45(a)–(d) themselves are unaffected and were re-checked by two referees (92 000 congruence cases).

**Theorem 11.46 (mini-blocks; the exact lifting criterion at the final gate) [proved].** Let $H=pH'\le p^t$, $X=p^tK'$, $i=pq+r$ ($0\le r<p$, $0\le q<H'$), $m_q=H'-q$.
- (a) $y_{pq+r}(X)=p^q\,y'_q\,U_q(X)\,w_{q,r}(X)$, where $y'_q=\prod_{s'\le q}(X/p-(H'-s'))$ is the depth-$(t-1)$ window element of length $H'$, $U_q(X)=\prod_{s\le pq,\,p\nmid s}(X-pH'+s)$ is a unit with $U_q(X)\equiv U_q(0)\pmod{p^t}$, and $w_{q,r}(X)=\prod_{j\le r}(X-pm_q+j)\equiv\prod_{j\le r}(j-pm_q)\pmod{p^t}$. Block $q$ has valuation $e_q$ with $e_{q+1}-e_q=1+v(H'-1-q)$; the last block ($q=H'-1$) has $e_{H'-1}=c$ and is a level-$(t-1)$ gate whose normalised subset sums are $V_p$ mod $p^t$.
- (b) Let $R$ be the set of subset sums of the first $p(H'-1)$ elements, $u=y_{p(H'-1)}/p^c$ (a unit), and for $T\in\mathbb Z/p^c$ let $B_T=\{(r-T)/p^c\bmod p^t:r\in R,\ r\equiv T\ (p^c)\}$. Then the window covers $\mathbb Z/p^M$ iff $B_T+uV_p=\mathbb Z/p^t$ for every $T\in\mathbb Z/p^c$.

*Proof.* (a) This is Proposition 10.15(ii) with bookkeeping. Among the factors $X-pH'+s$, $s\le pq$, the multiples $s=ps'$ give $p^qy'_q$, the others are units $\equiv s$; the factors $s=pq+j$, $j\le r$, give $w_{q,r}$, a unit $\equiv r!$. $v(y'_{q+1}/y'_q)=v(H'-1-q)$ because $0<H'-1-q<p^{t-1}$. The last block has $v(y_{p(H'-1)})=v((pH'-1)!/(p-1)!)=c$ and $m_{H'-1}=1$, so $w\equiv\prod_{j\le r}(j-p)=(p-1)!(-1)^u/u!$ ($u=p-1-r$). (b) $\Sigma_H=R+y_{p(H'-1)}\{w_{H'-1,S}\}_S$ with $y_{p(H'-1)}w_{H'-1,S}\equiv p^cu\,\omega_S\pmod{p^M}$, $\omega_S\in V_p$. A target $z\equiv T\pmod{p^c}$ is reached iff $r+p^cu\omega_S\equiv z$ for some $r\equiv T$, i.e. iff $(z-T)/p^c\in B_T+uV_p$ mod $p^t$; and $(z-T)/p^c$ runs over $\mathbb Z/p^t$. ∎

This is the fibre decomposition that programs A, B, C (§10.2) and A′, C′ below implement. An independent exact check (`s3_check.py`; 18 configurations with $p\le13$, $t\le4$, all 466 unit classes, 107 of them not covered) confirms that the direct miss count equals the sum of the fibre miss counts on every class; the lead re-ran it.

**Corollary 11.47 (what an induction must carry; Fourier lifting) [proved].**
- (a) Only the fibres $(B_T)_T$ enter $\mathrm{Cov}(p,t,pH')$.
- (b) *Fullness never suffices:* for $D_p\le d<t$ there are sets $B_T$ meeting every class mod $p^d$ with $B_T+uV_p\ne\mathbb Z/p^t$.
- (c) If $|B_T|>p^t-|uV_p\bmod p^t|$ for every $T$, the window covers.
- (d) *(Fourier form.)* Let $\mu_T$ be any probability measure supported in $B_T$ and $\hat E_p(\theta)=\prod_{u<p}|\cos(\pi\theta(p-1)!(-1)^u/u!)|$ (universal: it depends on $p$ only). If $\sum_{0\ne\eta\in\mathbb Z/p^t}|\hat\mu_T(\eta)|\,\hat E_p(u\eta/p^t)<1$ then $B_T+uV_p=\mathbb Z/p^t$.

*Proof.* (a) and (c) are immediate from Theorem 11.46(b) (for (c), the complement of $B_T$ is too small to contain a translate of $-uV_p$). (b) By the abstract core of Theorem 10.12 (Lean `worst_case_iff`) with $G=\mathbb Z/p^t$, $K=p^d\mathbb Z/p^t$, $B=uV_p$, the conclusion would hold for all such $B_T$ iff $uV_p$ contains a coset of $p^d$. The elements of $V_p$ are integers in an interval of length $<e(p-1)!\le p^{D_p}\le p^d$, hence pairwise incongruent mod $p^d$ (and multiplication by the unit $u$ preserves this), while a coset of $p^d$ in $\mathbb Z/p^t$ has $p^{t-d}\ge p$ elements congruent mod $p^d$. (d) $\mu_T*\lambda$, with $\lambda$ uniform on the multiset $\{u\omega_S\}$ ($|\hat\lambda(\eta)|=\hat E_p(u\eta/p^t)$), is supported on $B_T+uV_p$ and, by Fourier inversion, is $\ge p^{-t}(1-\sum_{\eta\ne0}|\hat\mu_T||\hat\lambda|)>0$ everywhere. ∎

So the depth dependence of $\mathrm{Cov}(p,t,pH')$ sits entirely in the Fourier profile of the carry fibre, weighted by a fixed function of $p$. The gate's own $L^1$ mass on the order-$p^d$ shells grows like $(p^d-p^{d-1})(2/\pi)^p$ (floating point, diagnostic: $G_{13}(d)=0.0078,0.50,5.8,90,1132$ for $d=1,\dots,5$), and its shell maxima tend to $1$ (the archimedean resonance of Corollary 10.20). Corollary 11.47(d) is a reformulation, like Theorem 10.18, not progress.

**Theorem 11.48 (second-moment covering criteria) [proved].** Let $Y=(y_1,\dots,y_n)$ in $\mathbb Z/p^m$, $N(r)$ the number of subsets with sum $\equiv r$, $\bar N=2^n/p^m$, $\hat\nu(\xi)=\prod_i\frac{1+e(\xi y_i/p^m)}2$, $L^1(Y)=\sum_{\xi\ne0}|\hat\nu(\xi)|$ and $L^2(Y)=p^m\sum_{\xi\ne0}|\hat\nu(\xi)|^2=\sum_r(N(r)/\bar N-1)^2$.
- (a) *(Chebyshev)* $\#\{r:N(r)=0\}\le L^2(Y)$; so $L^2(Y)<1$ implies covering.
- (b) $L^1(Y)\le\sqrt{L^2(Y)}$, with strict inequality when $L^2(Y)>0$ *[corrected, round-3 referee: previously "$<$" without qualification, which fails when $L^2(Y)=0$, e.g. $Y=\{1\}$ in $\mathbb Z/2$]*; so $L^2<1\Rightarrow L^1<1$: the second-moment criterion never has more room than the $L^1$ criterion of Proposition 3.13(b).

(Credit: (a) and (b) are the standard Chebyshev and Cauchy–Schwarz facts for Fourier coefficients; only their application to covering windows is specific to this note.)
- (c) For a window $y_i(K')$, $i<H$, of $\mathrm{Cov}(p,t,H)$ ($p$ odd), $L^2(Y)\ge c_1(p,\rho)\,p^M$ with $c_1(p,\rho)=\sum_{\xi'=1}^{p-1}\prod_{u=0}^\rho\cos^2\big(\pi\xi'(-1)^\rho\rho!(-1)^u/(u!\,p)\big)>0$, independent of $t$, $c$, $K'$. Hence the Chebyshev criterion certifies $\mathrm{Cov}(p,t,H)$ only if $p^{t+c}<1/c_1(p,\rho)$; e.g. at $p=13$, $c_1\ge2.2\cdot10^{-5}$ for every $\rho$, so nothing with $M\ge5$.
- (d) *(Fibre form.)* With the low/high split at level $k$, fibre sets $B_T\subseteq\mathbb Z/F$ ($F=p^{m-k}$) and $\nu_U$ the uniform subset-sum measure of the high elements divided by $p^k$: the number of residues missed in fibre $T$ is at most $\mathrm{Cheb}_T=F\sum_{\eta\ne0}|\hat B_T(\eta)|^2|\hat\nu_U(\eta)|^2\le F(F/|B_T|-1)\sup_{\eta\ne0}|\hat\nu_U(\eta)|^2$.

*Proof.* (a) Chebyshev with $\sum_r(N(r)-\bar N)^2=\bar N^2L^2(Y)$. (b) Cauchy–Schwarz over the $p^m-1$ nonzero frequencies gives $L^1\le\sqrt{(1-p^{-m})L^2}$. (c) Keep only the frequencies of exact order $p$: elements with $v(y_i)\ge1$ contribute $1$, and by Lemma 10.11(d) the units are $y_0,\dots,y_\rho$ with $y_i\equiv(-1)^\rho\rho!(-1)^u/u!\pmod p$; no factor vanishes for odd $p$. (d) In fibre $T$ the representation count is $N_T(z)=\bar N_T\sum_\eta\hat B_T(\eta)\hat\nu_U(\eta)e(-\eta z/F)$; apply Chebyshev and Parseval, and $\sum_{\eta\ne0}|\hat B_T|^2=F/|B_T|-1$. ∎

*Corrections recorded by the track (2026-10-20).* An earlier text of the track (i) used the quantity $(F/|B_T|-1)\sum_{\eta\ne0}|\hat\nu_U|^2$ as if it bounded $\mathrm{Cheb}_T$; it does not (it is the expectation of $\mathrm{Cheb}_T$ for a random set $B_T$ of the same size [heuristic]), and certified windows exist where it is smaller than $\mathrm{Cheb}_T$ in every fibre; (ii) overstated the reach of Proposition 10.14 (Remark 11.49). On certified minimal windows, $L^1\in[3.7,30]$, $L^2\in[9\cdot10^2,8\cdot10^5]$ and $\max_T\mathrm{Cheb}_T\in[20,4.8\cdot10^3]$, while the windows cover with minimal multiplicity as low as $2$ [computer-assisted, floating point]: covering at these lengths is a large-deviation phenomenon in the multiplicities that neither $L^1$ nor $L^2$ sees.

**Remark 11.49 (the reach of Proposition 10.14) [proved].** Step (a) of Proposition 10.14 needs $p\nmid H$; so from a certified $H_0$ the chain reaches $H_0,H_0+1,\dots$ up to the first multiple $pm_0\ge H_0$ of $p$, and then only the multiples $pm$, $m_0\le m\le p^{L_p}$. Lengths in between can fail: exact DP shows $\mathrm{Cov}(13,3,H)$ holds for $H=19,\dots,26$, fails for $H=27,\dots,31$ and holds at $32$ (`chain_monotone_check.py`). From the certified $\mathrm{Cov}(13,7,39)$: $\mathrm{Cov}(13,7,13m)$ for $3\le m\le169$, including $H=13^2,13^3$; similarly at $p=7$ (from $\mathrm{Cov}(7,6,34)$: $H=34,35$ and $7m$, $5\le m\le49$) and $p=11$ (from $\mathrm{Cov}(11,6,33)$: $11m$, $3\le m\le121$).

**Theorem 11.50 ($f(1,19)\ge17\,927\,094\,312$) [computer-assisted; every certificate checked by two independently written programs].**
$$f(1,19)\ \ge\ v_{19}((19^9-1)!)=17\,927\,094\,312,$$
up from $v_{19}((19^8-1)!)=943\,531\,272$ (§10.2). More generally, for every $a<19^9-49$, either $f(a,19)<v_{19}((a+49)!)$ or $f(a,19)\ge17\,927\,094\,312$.

*Proof.* Proposition 10.10 with $D=9$. Its hypotheses: (i) uniform $\mathrm{Cov}(19,t,H_t)$ for $t\le6$, $H_t=5,12,17,27,31,35$, with $H_t+1<19^t$ — certified in round 2 by programs A, B, C (§10.2); (ii) at depth $7$, for every $K''<19^2$ with $19\nmid K''$ (342 positions), the window $H=45$ ($c=v_{19}(44!)=2$, $19^7K''-45>1$) covers $\mathbb Z/19^9$ — the 18 positions $K''\le18$ by A, B, C (round 2) and the 324 positions $19<K''<361$ by the new programs A′ and C′ (all COVERED, 0 failures); (iii) at depth $8$, for every $K''\le18$, the window $H=49$ ($c=v_{19}(48!)=2$, $M=10$) covers $\mathbb Z/19^{10}$ — by A′ and C′ (36 runs, all COVERED). The chain script `chain_r3.py` reports `CHAIN OK (2 program(s) per certificate)`, and an independently written parser (`collect_t3b.py`, T3b-finish; it counts only logs with an END line and exit status 0, and excludes three logs of runs killed by the 2026-10-12 interruption) confirms: depth 7 — 342/342 positions by the A family and 342/342 by the C family (three program families on 18 positions, two on 324); depth 8 — 18/18 by A′ and by C′; no failure logged. The Legendre value $(19^9-1-162)/18$ was computed by two independent scripts and by the lead. The lead re-ran both chain checks on the archived logs (identical output). ∎

*Programs and their independence.* A′ (`fibcov_ip.c`) and C′ (`covchk_ip.c`) are memory-reduced modifications, by track T3b, of program A (track R3) and program C (the round-2 computational referee), with separately written in-place shift-OR kernels (3.0 GiB instead of 4.1 GB per run). They inherit the independence of A and C in authorship of the core. Validation: 1 325 comparisons against the brute force `brute.py` on 29 small cases at every fibre level (817 failing cases with exact miss counts; 0 mismatches), and the archived depth-7 results ($(11,7,40,K''=37)$: 2 misses; $(17,7,42,K'=6)$: 2 misses; the $(19,7,44)$ failure pattern at $K''=1,5,9,11,12,14,16$ with $4,8,4,4,4,4,4$ misses, reproduced exactly by both). A′ and C′ never disagree. There is no third program and no brute force at the $19^8$-bit fibre size. Proposition 10.10 is AI-refereed only (§10.8). Every run stayed below 45 min and $3.241\cdot10^9$ bytes maximum RSS.

**Computation 11.51 (two further out-of-sample tests of Conjecture 10.24) [computer-assisted; the law remains heuristic].** Registered before any run (`PREDICTIONS_registered_r3.txt`, 2026-10-12 14:36:09 CDT; $R^*$, $\nu$ from the published `bottleneck.py`, re-derived on 2026-10-20):
- $(19,8,47)$ at $K''=1$, $\nu=0.527$, predicted FAIL: **fails, with exactly $2\,739\,774$ missed residues out of $19^{10}$, by both A′ and C′**;
- $(19,8,49)$, $\nu=2.661$, predicted HOLD at all 18 positions: **covered at all 18, by both**.

Not run: $(19,8,48)$ (mixed band), $(19,8,50)$, and the three $p=13$, $t=9$ rows (memory: $13^{10}$-bit fibres). The C′ replication of the 324 depth-7 classes was also registered before launch (`PREDICTIONS_registered_r3_cont2.txt`, 2026-10-21 12:00:42 CDT) and confirmed; it is a replication, not a test of the law. The depth-7 agreement $\nu=2.00$ over 342 classes is not an out-of-sample test (two A′ chunks had run before $\nu$ was computed for $n=342$). With the three genuine tests of §10.5 this makes five.

### 11.6 Computations (tracks T4, T4b-finish) and cross-track consistency

All runs of T4 were launched on 2026-10-12 and finished that afternoon; T4b-finish (2026-10-20/21) checked that every run completed (file contents, not only logs), re-ran every post-processor (byte-identical outputs), and re-derived every headline number with two newly written parsers. One run ($p=7$, $G=9$, annealed) took 65.5 min on 4 threads, over the 45-min guideline; it was kept because it passed the internal consistency checks. Items below are exact integer computations unless marked floating point or Monte Carlo.

*Annealed moments.* For $x\bmod p^G$ let $N_G(x)$ be the number of $B\subseteq[1,M_G]$ with $p^G\mid S_B(x)$ and $Z_G(x)=p^G2^{-M_G}N_G(x)$; $\mathbb E$ is the average over the $p^G$ classes (Haar measure). In a random model $\mathbb EZ_G=1$.

**Lemma 11.52 (cutoff; prefix reduction; exact decision) [proved].**
- (a) $b!\mid\pi_b(x)$ in $\mathbb Z_p$ for all $x$, with equality of valuations at $x=0$; so $M_G:=\max\{b:v_p(b!)<G\}$ is the least $M$ with $p^G\mid\pi_b(x)$ for all $x$ and all $b>M$, and $M_G\le pG-1$. $Z_G$ does not change if $M_G$ is replaced by any larger cutoff.
- (b) With $n_0=\min\{n:V_n(x)\ge G\}$ (valuations capped at $G$): $N_G(x)=2^{M_G+1-n_0}\#\{e\in\{0,1\}^{n_0}:e_0=1,\ p^G\mid S_{n_0}\}$, and every prefix of such an $e$ is alive.
- (c) The carry recursion on the set of normalised states $S_n/p^{V_n}\bmod p^{G-V_n}$ decides $g_p(x)\ge G$, and when every branch dies at step $n$ it returns $g_p(x)$ exactly as $V_n+\max v(y)$ over the last candidates $y$.

*Proof.* (a) $\pi_b(x)/b!=\binom{x+b}b$ is integer-valued on $\mathbb N$, hence on $\mathbb Z_p$ by density; $\pi_b(0)=b!$; and $b\mapsto v_p(b!)$ is nondecreasing with $v_p((pG)!)\ge G$. Raising the cutoff to $M$ multiplies $N_G$ by $2^{M-M_G}$, which $2^{-M}$ compensates. (b) Terms $b\ge n_0$ are divisible by $\pi_{n_0}$, hence by $p^G$, so they are free; for $n<n_0$, $S_n=S_{n_0}-\sum_{n\le j<n_0}e_j\pi_j$ with $p^{V_n}\mid\pi_j$ and $V_n<G$. (c) Merging words with equal states is lossless. If all branches die at step $n$, any $B$ containing an element $>n$ has $v(S_B)<V_{n+1}$ (otherwise all its prefixes would be alive), so $S_B\equiv S_{B\cap[0,n]}\pmod{p^{V_{n+1}}}$; and a set whose first dead prefix is at stage $m\le n$ has $v(S_B)=v(S_m)<V_m\le V_n$. ∎

**Proposition 11.53 (the annealed second moment diverges at every prime) [proved].** For every prime $p$ and $G\ge1$, $\mathbb EZ_G^2\ge p^G/4$.

*Proof.* On the class $x\equiv-2\pmod{p^G}$, $S_{\{1\}}(x)=x+2\equiv0$ and $\pi_b(x)\equiv0$ for $b\ge2$ (factor $x+2$); so $p^G\mid S_B(x)$ iff $1\in B$, $N_G=2^{M_G-1}$ and $Z_G=p^G/2$. This class has weight $p^{-G}$. ∎

(The lead checked $N_G(-2)=2^{M_G-1}$ by brute force for $(p,G)=(2,6),(3,3),(5,2),(7,2)$; the round-3 referees checked it in 5 and 8 further cases.) *Credit:* the class $-2+p^G\mathbb Z_p$ is the shadow of $-2$, from Kitamura's cube identity and shadow family (§2). Only the moment bound is added here.

*Reading [heuristic; corrected after the round-3 referees, who found the earlier wording overstated].* The proposition proves only the lower bound $\mathbb EZ_G^2\ge p^G/4$. To conclude that $\mathbb EZ_G^2/(\mathbb EZ_G)^2\to\infty$ one also needs $\mathbb EZ_G=o(p^{G/2})$. That is supported only by the exact first moments of Computation 11.55, which grow roughly linearly up to $G=28,17,11,9$ for $p=2,3,5,7$; it is not proved for all $G$. Granting this, the *untruncated* subset-counting (annealed) second moment cannot prove $\mu(K_p)>0$ at any prime. Moments truncated away from the shadows are **not** ruled out: Computation 11.55 discusses them only heuristically. This is why §11.1 works with the quenched, frozen-state-weighted martingale. (An earlier text said the annealed route is "closed"; that is withdrawn.)

**Lemma 11.54 [proved].** For odd $p$, the geometric mean over $\xi\in(\mathbb Z/p)^\times$ of $\prod_{r<p}|\cos(\pi\xi r!/p)|$ is exactly $2^{-p}$.

*Proof.* Each $r!$ ($r<p$) is a unit, so $\xi\mapsto\xi r!$ permutes the units and $\prod_\xi|\cos(\pi\xi r!/p)|=\prod_{k=1}^{p-1}|\cos(k\pi/p)|=2^{1-p}$ (classical, for odd $p$: $\prod_{k=1}^{p-1}|2\cos(k\pi/p)|=|\Phi(-1)|=1$ with $\Phi(X)=(X^p-1)/(X-1)$). Multiply over the $p$ values of $r$ and take the $(p-1)$-th root. ∎

**Computation 11.55 (exact annealed moments; new exact densities) [computer-assisted; readings heuristic].** Two programs sharing no code (`annealed.c`, sparse/dense pruned states; `xcheck_annealed.c`, dense normalised states) agree on survivors, $\sum N$, $\sum N^2$ and $\max N$ in every one of 10 overlapping cases and with brute force on 6 small cases; survivor counts reproduce every $\delta_G(p)$ of §4.7 with $G\le28,17,11,9$ for $p=2,3,5,7$ (the $p=2$ rows $G=29,32$ of §4.7 lie beyond these runs). *[Clarified, round-3 computational referee.]* The 10 overlapping cases are $p=2$, $G\le18$; $p=3$, $G\le11$; $p=5$, $G\le7$; $p=7$, $G\le6$ (`T4-computations/logs/xcheck_annealed.log`). So the deepest rows of the table, including the two **new** values $\delta_{11}(5)$ and $\delta_9(7)$, rest on **one** program (`annealed.c`). The referee's independent Monte Carlo agrees with them: $p=5$, $2\cdot10^6$ samples, $0.52108\pm0.00035$ ($z=-1.5$); $p=7$, $2.4\cdot10^5$ samples, $0.62256\pm0.00099$ ($z=-1.4$). Monte Carlo cannot resolve the $\approx2\cdot10^{-5}$ gain over §4.7, and an exact independent census was beyond the referee's budget. The $p=2$, $G=28$ survivor count was reproduced exactly by the referee's own census.

| $p$ | $G$ | $\delta_G(p)$ | $\mathbb EZ_G$ | $\mathbb EZ_G^2/(p^G/4)$ |
|---|---|---|---|---|
| 2 | 28 | $31\,246\,552/2^{28}=0.1164025$ | 23.616 | 1.9869 |
| 3 | 17 | $46\,915\,750/3^{17}=0.3632933$ | 8.377 | 1.4707 |
| 5 | 11 | $25\,468\,861/5^{11}=\mathbf{0.5216023}$ | 4.959 | 1.2317 |
| 7 | 9 | $25\,177\,371/7^9=\mathbf{0.6239187}$ | 4.041 | 1.1227 |

The values $\delta_{11}(5)=0.52160227\ldots$ and $\delta_9(7)=0.62391872\ldots$ are new (one level beyond §4.7 at each prime). They give $f(a,5)<\infty$ on a set of density $\ge0.4783977$ and $f(a,7)<\infty$ on density $\ge0.3760812$ (rounded down). These are small improvements on the exact previous levels $1-\delta_{10}(5)=0.4783837$ and $1-\delta_8(7)=0.3760622$. *[Corrected, round-3 novelty referee: §4.7 and §0 of revisions 1–2 printed those as $0.4784$ and $0.3761$, i.e. rounded up, which made the "improvement" look negative. Those lines are now corrected to $0.4783$ and $0.3760$. The table entry $0.5216022$ is also corrected to $0.5216023$.]* *Readings [heuristic]:* $\mathbb EZ_G$ grows linearly (slopes $\approx1.2,0.52,0.41,0.39$), as a sum of $O(1)$ contributions from the $O(G)$ "shadow" buckets $\max_{i\le M_G}v(x+i)=v$; at $p=2$, $G=28$ each bucket $v=16,\dots,21$ contributes $1.0000$ to $\mathbb EZ$ to four or five digits, which suggests an unproved identity. $\mathbb EZ_G^2/(p^G/4)$ is constant to four digits over the last levels: the shadow of $-2$ and its neighbours carry essentially the whole second moment. Truncated to $\{\max_iv(x+i)\le K\}$, the moments are stable in $G$ for odd $p$ but still grow at $p=2$; even so, the truncated ratio grows like $p^K$, so a Paley–Zygmund bound from these moments gives at best $\delta_G\gtrsim(\log G)^2/G$.

**Computation 11.56 (natural $a$ at $p=2$; deep exact values) [computer-assisted].** Exact $\min(g_2(a),\mathrm{cap})$ for every $a\le4096$ at caps $32,254,1022,2046,4094$ (`gsampleN.c`; caps mutually consistent; no population overflow), with **0 mismatches** against Kitamura's certified exact table for $a\le256$ (the table's `value` column is $f(a,2)=v_2(a!)+g_2(a)$; T4b-finish's newer parser `t4b_indep_check.py` prints a list of "mismatches" because it compares $f$ with $g$ without the conversion — a labelling slip in that diagnostic line, noted by T4b-finish; the lead's own comparison with the conversion finds 0 mismatches). $N(A,G)=\#\{a\le A:g_2(a)\ge G\}$: $N(4096,G)=992,622,411,263,167,85,40,20,13,10,5$ at $G=8,16,32,64,128,256,512,1024,2048,3072,4094$; $N(4096,G)\,G/4096$ stays in $[4.8,7.5]$ for $G\ge128$ while $N\sqrt G/4096$ falls from $0.69$ to $0.08$ [heuristic reading: natural numbers follow the Haar law $\approx5.5/G$ in this range]. Five $a\le4096$ have $g_2(a)\ge4094$: $34,594,1102,2210,3456$. Deep values:
- $g_2(3456)=4823$, $g_2(1102)=11536$, $g_2(34)=18412$, i.e. Kitamura's records $f(3456,2)=8275$, $f(1102,2)=12633$, $f(34,2)=18444$, reproduced by T4's add-only carry program `p2add.c` (a formulation independent of Kitamura's code and of `gsampleN.c`) and again by T2's Python carry recursion `gcap.py`, run by the lead. ($f(34,2)=18444$ was already confirmed in round 1, §4.1.)
- **New:** $g_2(2210)=6261$, i.e. $f(2210,2)=v_2(2210!)+6261=2206+6261=8467$. Computed by `p2add.c` (T4) and, independently, by track T2's Python carry recursion `gcap.py`, run by the lead (`lead_deep_gcap.py`, 10 s). Two independently written programs, by different track instances.
- $g_2(594)\ge16382$ (survived cap $16382$); Kitamura reports $f(594,2)\ge66126$, which we did not reach.

**Computation 11.57 ($\delta_G(2)$ by Monte Carlo) [computer-assisted estimates; the rate reading is heuristic].** Exact decision per sample (Lemma 11.52(c)); $4\cdot10^7,2\cdot10^7,2\cdot10^6,10^6,2\cdot10^5$ samples at caps $126,256,512,1024,2046$; no overflow; consistent with the exact census at every $G\le32$ (largest $|z|=2.26$). Estimates (binomial standard errors in the last digit):

| $G$ | 64 | 128 | 256 | 512 | 768 | 1024 | 1536 | 2046 |
|---|---|---|---|---|---|---|---|---|
| $\delta_G(2)$ | 0.06416(4) | 0.03770(4) | 0.02052(3) | 0.01068(7) | 0.00758(9) | 0.00562(7) | 0.00370(14) | 0.00266(12) |
| $G\,\delta_G(2)$ | 4.11 | 4.83 | 5.25 | 5.47 | 5.82 | 5.76 | 5.69 | 5.44 |

*Descriptive fits.* A weighted power-law fit on $[64,2046]$ gives exponent $0.813$ ($\chi^2/\mathrm{dof}=4593/9$). On $[512,2046]$ it gives exponent $0.939$ ($\chi^2/\mathrm{dof}=14.1/3$), and local exponents are within two nominal standard errors of $1$ for $G\ge384$. *[Corrected, round-3 computational referee.]* The estimates at different $G$ come from the same nested Monte Carlo samples, so they are positively correlated. The $\chi^2$ values and the nominal exponent errors (the track report quotes $\pm0.001$) are therefore **not** valid test statistics, and they are descriptive only. The statement "a single power law is rejected" is withdrawn as a formal test, though the drift of the local exponent is visible in the table. The referee's refit of T4's data reproduces the exponents $0.813$, $0.886$, $0.930$, $0.939$. *Reading [heuristic]:* $\delta_G(2)\sim c_2/G$ with $c_2\approx5.5$–$6$ (Conjecture 11.34(a)); $2\delta_GG=10.5$–$11.6$ for $256\le G\le2046$ matches Kitamura's "$\approx11.5/G$" read as the fraction among even $a$; the $0.7/\sqrt G$ fit of §5 reflects the pre-asymptotic range $G\le254$.

**Computation 11.58 (gate constants) [computer-assisted; floating point].** $c_p=\max_{\xi}\prod_{r<p}|\cos(\pi\xi r!/p)|$ for $p\le53$ (mpmath, 30 digits): $c_3=1/8$, $c_5=0.1323771$, $c_7=0.0823662$, $c_{11}=0.0266813$, $c_{13}=3.29992\cdot10^{-3}$, …, $c_{53}=4.02552\cdot10^{-14}$; $c_p/(2/\pi)^p$ is erratic ($0.015$ at $p=41$, $175$ at $p=43$). Single-gate-block $L^1$ sums $L(p,i)=\sum_{\xi\in(\mathbb Z/p^i)^\times}\prod_u|\cos(\pi\xi e_u/p^i)|$ ($e_u=(-1)^u(p-1)!/u!$) for $p=5,7,11,13$, $i\le8$, converge to the random-model budget $p^i(1-\frac1p)I_p$, $I_p=\int_0^1\prod_u|\cos(\pi e_u\theta)|\,d\theta$, with relative error $<5\cdot10^{-8}$ at $i=8$; $I_p/(2/\pi)^p=1.1670,1.1704,1.1725,1.1729$ for $p=5,7,11,13$. This identifies the "per-level ratio $\approx1.17$" measured by round-2 track R2b (§10.5) as $I_p/(2/\pi)^p$. ($I_p$ by Gauss–Legendre on the $(p-1)!$ unit intervals on which the integrand is analytic, at two node counts agreeing to $4\cdot10^{-10}$; no interval arithmetic.)

**Computation 11.59 (cross-track consistency) [computer-assisted].** For $w=1$ and $K$ large, the window-code dimension $D_p(1,K)$ of Theorem 11.17 (T1b's `wdim.c`) and $1-\theta^{\rm set}_p$ of Theorem 11.38 (T3a's `gamma_enum.c` + `theta.py`) are the same quantity, $\frac{p-1}p\,\mathbb E\log_p\mathrm{dist}_p(1+v(y+1))$, computed by different programs written by different instances. They agree: $0.6462406$ ($p=2$), $0.8068732786$ vs $0.806873278571$ ($p=3$), $0.9236947455$ vs $0.923694745532$ ($p=5$), $0.9855568255$ vs $0.985556825536$ ($p=7$), $0.9982683160$ vs $0.998268316014$ ($p=11$), $0.9996567499$ vs $0.999656751178$ ($p=13$; the first value is capped at $K=5$, hence the $10^{-9}$ difference).

### 11.7 Status of Q1–Q3 after round 3, and what remains

**Status line (2026-10-21).**
- **Q1** (for which $a,p$ is $f(a,p)$ finite?) **Open in general.** New at $p=2$: an explicit rate, density $O(G^{-0.227})$ of $\{a\not\equiv14\ (16):f(a,2)\ge v_2(a!)+G\}$ (Corollary 11.30). Whether $f(a,2)<\infty$ for every $a$ is open; $a=594$ remains a live test case. $K_2$ is Haar-null but has Hausdorff dimension $\ge0.853$ (Corollary 11.19), so measure arguments alone cannot decide whether it meets $\mathbb N$. Odd $p$: $\mu(K_p)>0$ (Conjecture 5.2) is reduced to the hypothesis H′(p) (Conjecture 11.10, via Theorem 11.7), unproved. H′(p) consists of a uniform variance bound *and* the existence of one atom with large normalised weight and small freezing probability. *[Corrected, round-3 referees: an earlier text reduced $\mu(K_p)>0$ to the variance bound alone, which Theorem 11.7 does not support.]*
- **Q2** (behaviour) **Partial.** New: $f(1,19)\ge17\,927\,094\,312$ (Theorem 11.50); the exact value $f(2210,2)=8467$; exact densities $\delta_{11}(5)$, $\delta_9(7)$; structure of $K_p$ (§11.2); the dichotomy for $a<19^9-49$ at $p=19$.
- **Q3** **OPEN.** Nothing proves $f(a,p)=\infty$ for any $(a,p)$. Round 3 adds no new sufficient condition for Q3 beyond reformulations (Corollary 11.47(d)); its positive-measure statements (Theorem 11.7, Conjecture 11.44) would not by themselves place a natural number in $K_p$. The round-3 referees agree that Q3 is correctly stated as open.

**What remains, precisely.**
1. *Q3, covering route:* prove $\mathrm{UC}(p)$ or $\mathrm{UC}'$ for one $p\ge7$; by Corollary 11.47 an induction must carry the Fourier profile of the carry fibre at the final gate on all shells, and by Theorem 11.48 the second-moment version is useless. The concrete open step is an RMF-type bound for the fibre measure of windows of length $p^{t-1}$ at a single deep gate, using the explicit digit structure of Theorem 11.45 and the automaticity of the unit parts (Proposition 3.14).
2. *Q3 and positive measure, Fourier route:* prove $C_\infty<\infty$ for one odd $p$ (Conjecture 11.44); by Propositions 11.40–11.42 this needs control of the conditional carry at all but finitely many window boundaries. A first rigorous target: $C_\infty<\infty$ almost surely in a random-unit model that keeps the valuations, the gate congruence and the shadow windows.
3. *Odd $p$, measure:* prove H′(p) (Conjecture 11.10) for one $p$. For part (a), start with gate-free windows (single-parent bound from the $L^2$ mass of the window map; second-moment bound for the children's Weyl sums, Proposition 11.8), then bounded gates. For part (b), exhibit, or prove the existence of, one atom whose weighted population is $\gg n_j^4$ and whose freezing probability is small. Alternatively, find an argument that removes the need for (b), for instance a lower bound on $\mu\{M_j\ge c\,S_j\}$ that exceeds $(1+p^LK/c)\,\mu(\sigma_j<\infty)$. (Summing Theorem 11.7 over the atoms in $\{M_j\ge cS_j\}$ gives $\mu(K_p)\ge\mu\{M_j\ge cS_j\}/(1+p^LK/c)-\mu(\sigma_j<\infty)$, and $\mu(\sigma_j<\infty)$ is only polynomially small, about $n_j^{-2}$ [heuristic size].) *[Corrected after the round-3 re-check: this sentence previously asked for $\mu\{M_j\ge c\,n_j^4S_j\}$ "not exponentially small". The $n_j^4$ belongs to the population form of the condition (Remark after Theorem 11.7), and "not exponentially small" is not sufficient.]*
4. *$p=2$:* a rate for $\delta_G(2)$ itself, by treating $14+16\mathbb Z_2$ (the triple root of Proposition 11.32; the track's sketch renormalises at $-2$ to a problem of the same type at the odd point $x+3$); or exponent $0.415$ under the decorrelation hypothesis of Proposition 11.31; the conjectured exponent is $1$ (Conjecture 11.34).
5. *Structure of $K_p$:* is $K_p$ perfect? Are there multiple zeros other than $-2$? Is $\dim_HK_2=1$ (Conjecture 11.22)?
6. *Computation (feasible):* $g_2(594)$ beyond cap $16382$; $\delta_G(2)$ at $G=4096$; the registered $(19,8,48)$, $(19,8,50)$ rows; an odd-$p$ SMC with multiprecision carries at $p=3$; and, carried over from §10.6, uniform $\mathrm{Cov}(13,8,47)$ and $\mathrm{Cov}(5,5,39)$.

### 11.8 Reproduction (round 3)

*Layout.* Round-3 code is under `code/round3/<track>/` and round-3 logs, data and the track reports under `data/round3/<track>/`, for the tracks `T1a-oddp-quenched`, `T1b-Kp-structure`, `T2-p2-rate`, `T3a-q3-fourier`, `T3b-q3-covering`, `T3b-finish`, `T4-computations` (and `T4b-finish`, a copy of the T4 addendum), the gate outputs `gate-status/`, `gate-literature/`, and the lead's own checks `code/round3/lead/`, `data/round3/lead/`. Compiled binaries are not included. *Path-only edit:* in ten copied scripts (T3b workers and job wrappers, `validate_ip.py`, T4's `run_annealed.sh` and `run_queue.sh`) the absolute path of the working session was replaced by `<WORKSPACE>`; in the public repository, the logs are unedited except that the machine's hostname was replaced by `<host>` (T3b's covering logs) and three absolute local paths by `<scratchpad>/`, `<python-site-packages>/` or a repository-relative path (two referee run scripts, one referee log). Kitamura's files fetched by T4 are not redistributed (fetch `p2_exact_table_1_256.csv` from `KitaKen1/erdos-404-p2-landscape`); only our derived count `data/round3/T4-computations/kitamura_derived/kitamura_N256.txt` is included. Scripts that compare with round-1/2 data were run with this repository checked out as `publish-erdos404/` beside the track directories (T4's `t4b_indep_check.py` reads `review/computation/census_p2_32.out`; T3b's chain check reads `data/round2/`). Tools: clang, Python 3.9 with numpy 2.0.2 and mpmath 1.3.0.

*Track commands* (run inside the track's directory; each track report gives full details and timings).
- **T1a.** `clang -O2 -o winvar winvar.c -lm`; trajectories `./winvar 1 101 3 4 79 24 4 1.25 14 8000000 256` (and seeds 202, 303, 404, 505, 606 with the parameters of the report, 23 s in all); atom Monte Carlo `./winvar 2 SEED p L P n0 nwin 1.25 NSAMP 8000000` (`run_batch_r3.sh`, `run_batch_r3b.sh`); exact cross-checks `python3 window_exact2.py 3 1 1 22 28 40 1 x=9931185549497379070` and the three other windows of §6.1 of the report; `python3 summarize.py`; `python3 cp_const.py 3 5 7 11 13`. Each run $<1$ GB, $<1$ min.
- **T1b.** `clang -O2 -o wdim wdim.c -lm`; `./wdim p w K` for the cases of Corollary 11.19 (`run_batch.sh`; the longest, `./wdim 2 9 22`, 801–809 s, 32 MB); `python3 wdim_check.py 2,3,7 3,2,5 5,1,4 2,5,6 7,1,3`; `python3 hensel_check.py`; `python3 p2k2.py`. Predictions: `data/round3/T1b-Kp-structure/PREDICTIONS_registered_T1b.txt`.
- **T2.** `python3 certs.py`; `python3 check_cert.py 2 64 20000`; `python3 slope_depth.py 3 300 90`; `python3 gcap.py 5 60000 512` (116 s); `python3 agresti.py haar 4000`; `python3 agresti2.py`; `python3 agresti3.py`; `python3 lambda_test.py <T4>/data/surv_cap4094.txt`; `python3 constants.py`, `constants2.py`, `constants_opt.py`. All single-core, $<4$ min.
- **T3a.** `python3 verify_l2_r3.py` (111 cases); `python3 verify_wide_r3.py p N0 k`; `clang -O2 -o l2dp l2dp.c` and `l2dp 13 7 13`, `l2dp 3 17 1`; `python3 summary_r3.py`; `clang -O2 -o gamma_enum gamma_enum.c` and `gamma_enum p 16` ($p\le19$); `python3 gamma_table.py`; `python3 theta.py`; SMC: `run_smc.sh`, `clang -O2 -o smc2 smc2.c -lm` and `run_smc2.sh "N0 K P seed"`, then `smc_table.py`, `smc_dstats.py`. Each run $\le2.2$ GB except the inherited exact runs ($\le3.7$ GB).
- **T3b.** `clang -O2 -o bin/fibcov_ip src/fibcov_ip.c` (A′), `clang -O2 -o bin/covchk_ip src/covchk_ip.c` (C′); validation `python3 src/validate_ip.py`; jobs through `src/run_job.sh NAME BINARY p t H c pos K''...` (e.g. `bin/covchk_ip 19 7 45 2 pos 20 21 …`, `bin/fibcov_ip 19 8 49 2 pos 1`), queued by `src/worker_queue.sh` / `src/worker_queue_c7.sh` with `queue_r3cont.txt` / `queue_r3c7.txt` (three workers, $\le3.241\cdot10^9$ bytes and $\le45$ min per job); `python3 src/results_table.py`; `python3 src/chain_r3.py 19 9 "$L/outputs/R3:$L/logs_original/R3:$L/review/computation/logs:$M/logs" specs_p19_D9_r3.txt N` with `L=../../../data/round2`, `M=../../../data/round3/T3b-q3-covering`, $N=1,2,3$ (paths as in this repository; re-checked in this layout on 2026-10-21: `CHAIN OK` for $N=1,2$); `python3 src/selfsim_check.py` (2 min); `python3 src/s3_check.py` (11 s); `python3 src/chain_monotone_check.py`; `python3 src/l2_study.py`, `src/l2_hybrid_fix.py`, `src/l2_lower_gate_shells.py`. T3b-finish: `python3 src/collect_t3b.py <T3b dir> <publish-erdos404/data/round2>`.
- **T4.** `clang -O3 -march=native -o src/annealed src/annealed.c -lpthread`, `src/annealed p G 4`; `clang -O3 -march=native -DNL=N -o src/gsample_nlN src/gsampleN.c -lpthread` ($N=2,4,5,9,17,33,65$), range mode `src/gsample_nlN -1 0 CAP 4096 4`, Monte Carlo `src/gsample_nl2 40000000 20261012 126 4`, `gsample_nl5 20000000 20261013 256 4`, `gsample_nl9 2000000 20261014 512 4`, `gsample_nl17 1000000 20261015 1024 4`, `gsample_nl33 200000 20261016 2046 4`; `clang -O3 -march=native -o src/gatesum src/gatesum.c -lpthread -lm`, `src/gatesum 13 8 4 12` etc.; `clang -O3 -march=native -o code/xcheck_annealed code/xcheck_annealed.c`, `sh code/run_xcheck.sh`; `clang -O3 -march=native -o code/p2add code/p2add.c`, `code/p2add CAP a 22`; post-processing `src/annealed_post.py`, `src/surv_post.py`, `src/mc_post.py`, `src/assemble_results.py`, `code/post_extra.py`, `code/assemble_retry.py`, `code/t4b_final.py`, `code/t4b_indep_check.py`. (The batch scripts `run_annealed.sh`, `run_queue.sh` reproduce the 2026-10-12 runs, 4 threads each.)

*Lead re-runs (2026-10-21 CDT, at most 2 cores; outputs in `data/round3/lead/`).*

| # | what | command | result | wall |
|---|---|---|---|---|
| L1 | finite cases of Proposition 11.25, by a different route | `python3 -I code/round3/lead/lead_t2_certs.py` | identical valuations and histograms to T2's `certs.py`; identity of Lemma 11.24(c): 0 failures in 2000 cases; $S_{\{1,3\}}=(x+2)^3$ | <1 s |
| L2 | constants of Corollary 11.30, exact piecewise | `python3 -I code/round3/lead/lead_t2_constants.py 400` | main $+$ side constants $22.47$, $1318.1$, $1.97162\cdot10^5$ ($\le29$, $1325$, $1.98\cdot10^5$); sup of the full bound $\times G^{0.227}$: $17.53$, $1121$, $1.680\cdot10^5$ | 1.3 s |
| L3 | independent spot checks | `T4DIR=… python3 -I code/round3/lead/lead_checks_r3.py` | $D_p(w,K)$ for 4 cases (own code) as T1b; gate-block law, $J_0$, $\Gamma_p(1)$ and all counts $4^p\mathbb P(p^J\mid W)$, $p\le11$, as T3a; $\theta_2=\log_23/4$; $v_{19}((19^9-1)!)=17\,927\,094\,312$; Proposition 11.13(b) roots for six $(p,c)$; Lemma 11.54 to 12 digits for $p\le17$; Proposition 11.53 by brute force; Kitamura's table vs T4: 0 mismatches | 0.6 s |
| L4 | T1b dimension values | `wdim` for 11 cases incl. `2 9 22`, `3 5 13`, `2 7 22`; `wdim_check.py` | identical to `logs/batch1.log` | 809 s + 65 s |
| L5 | T3a | `theta.py`, `verify_l2_r3.py`, `gamma_enum p 8` ($p=3,\dots,13$) | identical; 111/111 exact | 2 s |
| L6 | T3b | `chain_r3.py` ($N=1,2,3$), `collect_t3b.py`, `selfsim_check.py`, `s3_check.py` | `CHAIN OK` for $N=1,2$, `INCOMPLETE` for $N=3$; parser as in Theorem 11.50; all identity checks pass | 2.3 min |
| L7 | T4 | `t4b_indep_check.py` | byte-identical to the archived output | <1 s |
| L8 | T1a | `winvar 1 101 3 4 79 24 4 1.25 14 8000000 256`; `window_exact2.py` ($p=3$ window) | 130/130 window lines identical to the archived log; 180/180 exact first-moment identities | 17 s + 2 s |
| L9 | deep $g_2$ values with T2's `gcap.py` (independent of T4's `p2add.c`) | `python3 -I code/round3/lead/lead_deep_gcap.py <T2 code dir>` | $g_2(3456)=4823$, $g_2(2210)=6261$, $g_2(1102)=11536$, $g_2(34)=18412$ (all died below the cap, so exact) | 3 min |
| L10 | round-3 referee fixes (after the reports) | `python3 code/round3/lead/lead_r3fix_checks.py`; `python3 code/round3/lead/lead_t2_constants.py 400` | $\theta_3=0.2294000283$ (closed form = direct sum); $\Gamma_3(1..4)=1/32,11/16,65/16,227/16$; counterexamples to the withdrawn Consequence of Theorem 11.45 at $p=3,5,7$; $1-\delta_{11}(5)=0.47839773$, $1-\delta_9(7)=0.37608128$; Corollary 11.30 $C_6$ supremum $1.680\cdot10^5$ attained near $G=2^{354}$ | <2 s |

Not re-run by the lead: the 2026-10-12/20/21 coverage runs of T3b (about 25 core-hours in all; the lead re-ran only the chain checks on their logs), T4's annealed and Monte Carlo runs, T3a's deep exact runs and SMC, T2's Monte Carlo and predictor scripts, T1a's atom Monte Carlo, and T1b's `hensel_check.py`, `p2k2.py`.

*Referee material.* The round-3 referees' reports, code and logs are archived in `data/round3/review/`, unedited apart from the path replacements listed under *Layout* (`verify-logic/`, `verify-computation/`, `verify-novelty/` and the sixteen `refute-*` directories); four compiled binaries were removed. Their commands and timings are in each directory's writeup or `COMMANDS.log`. The referees report runs of at most 3 cores and at most 45 min each; the computational referee stopped one $g_2(34)$ run at that limit. Section 11.9 summarises the findings. The round-3 re-check of the corrected note (2026-10-21) is in `data/round3/review/recheck/`; its six minor findings are applied in this version (§11.9).

### 11.9 Verification and credit (round 3)

> **§11 has been checked by AI referees (Claude instances), not by any human.** Their reports were written on 2026-10-21 and are archived, with their code and logs, in `data/round3/review/`. Every correction made in response is listed below, and the corrected passages in §0 and §11 are marked. The human author has not verified any of the mathematics.

*Who refereed.* There were two layers, each using its own code written from the note's definitions. None of it was shared with the tracks or the lead, except one unchanged re-run of `p2k2.py` by the logic referee.
- *Three referees, one per lens:*
  - logic (`verify-logic/`, line by line, with brute-force checks);
  - computation (`verify-computation/`, at most 3 cores and runs under 45 min);
  - novelty (`verify-novelty/`, read-only searches on 2026-10-21).
- *Sixteen targeted refutation attempts, two per result:* one hunted for a gap in the proof and one for a counterexample. They covered Theorems 11.14, 11.17, 11.29 and 11.38 and Corollaries 11.19, 11.20, 11.30 and 11.39 (`refute-<result>-gap/`, `refute-<result>-counterexample/`).

*Counts.*

| report | fatal | serious | minor | notes |
|---|---|---|---|---|
| logic referee | 0 | 2 | 5 | the reduction to H′(p) (S1); the Consequence after Theorem 11.45 (S2) |
| computation referee | 0 | 0 | 6 | every number it could re-run agrees with the note |
| novelty referee | 0 | 1 | 7 | S1 again; no overlapping prior or concurrent work found |
| 16 refutation attempts | 0 | 0 | 4 refuted (minor) | 12 not refuted. The 4 refutations (Theorem 11.38 ×2, Corollary 11.39 ×2) concern only the two wrongly rounded constants M1, M2. No counterexample to any theorem's mathematics was found. |

After merging duplicates there are **2 serious and 12 minor distinct findings**, plus presentational points. All were acted on. No result labelled [proved] had its proof refuted. The two serious findings concern a *claimed consequence* stated outside a theorem (S1) and a *Consequence paragraph* (S2).

**Serious findings.**
- **S1. The reduction "H′(p) ⇒ $\mu(K_p)>0$" was overstated.** Raised by the logic and novelty referees. Theorem 11.7 is correct as displayed, and both referees confirmed this. But it concerns a given atom $A$ with $M_j(A)>0$ and $\mu_A(\sigma_j<\infty)<1/\Lambda(A)$. §0 item 22, §11.0 headline 3, Conjecture 11.10 and §11.7 claimed that the variance bound alone gives $\mu(K_p)>0$.
  - *Lead's re-derivation.* The lead agrees with both referees. Theorem 11.3(d) controls only the total measure of badly freezing atoms. Summing Theorem 11.7 over atoms gives $\sum_A\mu(A)\big(M_j(A)/(M_j(A)+p^LKS_j)-\mu_A(\sigma_j<\infty)\big)$. Since $S_j/M_j(A)$ is of order $n_j^4$ divided by the weighted population [heuristic size estimate], this is useful only on atoms with population $\gg n_j^4$, and no lower bound on the measure of such atoms is proved; the only proved bound is exponentially small (Corollary 11.20).
  - *Action:* H′(p) is restated with the atom condition as part (b) (Conjecture 11.10). A Remark after Theorem 11.7 explains the gap and its size. The four summaries are corrected, and §11.7 item 3 now lists part (b) as an open step. The status of Theorem 11.7 is unchanged ([proved]).
- **S2. The "Consequence [proved]" after Theorem 11.45 is false.** Raised by the logic referee. Counterexample: $p=3$, $t=3$, $K'=1$, where $v_3(y_8-8!)=5=t+c$. Further cases occur at $p=5,7$ ($t=3$) and $p=3$ ($t=4,5$).
  - *Lead's re-derivation:* the lead recomputed these cases exactly with its own script (`code/round3/lead/lead_r3fix_checks.py`, log `data/round3/lead/lead_r3fix_checks.log`) and found them all.
  - *Action:* the Consequence and its conclusion about covering statements are **withdrawn**. Only a heuristic restatement of the barrier lemma remains. Theorem 11.45(a)–(d) stand as lower bounds, and the wording "all four bounds are attained" is made precise.

**Minor findings (all corrected).**
- **M1.** The bound $\theta_3\le0.22940$ was truncated; the true value is $\theta_3=0.2294000283$. Found by the logic and computation referees and four refutation attempts. Now $\theta_3\le0.229401$ (Theorem 11.38), re-derived by the lead in closed form and by direct summation. $\log_23/4$ is now printed as $\le0.396241$.
- **M2.** "$\dim_HE_{N_0}\ge0.99966$ at $p=13$" rounded the lower bound $1-\theta^{\rm set}_{13}=0.99965675$ up. Found by all three referees and two refutation attempts. Now $\ge0.999656$ (Corollary 11.39(b), §0 item 23).
- **M3.** The odd-prime density bounds of revisions 1–2 were rounded up: $0.4784$, $0.3761$, $0.2455$ for $p=5,7,13$. This made the round-3 "improvements" look negative. Found by the novelty referee. Now $0.4783$, $0.3760$, $0.2454$ in §0 and §4.7, the improved bounds $0.4783977$ and $0.3760812$ are stated explicitly, and $\delta_{11}(5)$ is printed as $0.5216023$ (Computation 11.55).
- **M4.** "The annealed route is closed" (Proposition 11.53, §0 item 26, §11.0 headline 6) needs $\mathbb EZ_G=o(p^{G/2})$, which rests only on numerics, and says nothing about truncated moments. Found by the logic and novelty referees. Now labelled [heuristic] and qualified; the proposition itself is unchanged.
- **M5.** Theorem 11.48(b) said $L^1<\sqrt{L^2}$; this fails when $L^2=0$. Now $\le$, with strict inequality when $L^2>0$ (the proof gives $L^1\le\sqrt{(1-p^{-m})L^2}$).
- **M6.** §0 item 20 claimed $D_p(w,K)\ge1-p^{-L_p}$ for every $(w,K)$; it holds for $(1,L_p+1)$. Now stated as a chain through $\sup_{w,K}$.
- **M7.** The archived `viol=1` in T3a's `l2_summary.txt` is a checker artefact: a partial first group was compared with the full-block bound. Explained in Computation 11.43.
- **M8.** The two new exact densities rest on one program; the two-program cross-check covers only smaller $G$. Stated in Computation 11.55, with the referee's agreeing Monte Carlo ($z=-1.5$, $-1.4$).
- **M9.** The $\chi^2$ statistics of Computation 11.57 ignore the correlation between nested Monte Carlo samples. They are now labelled descriptive, and "a single power law is rejected" is withdrawn as a formal test.
- **M10.** "Validated" overstated the SMC agreement at $p=3$, where the excess $C-1$ is $3.7\%$ low. Reworded in Conjecture 11.44.
- **M11. Credit and bibliography** (novelty referee).
  - arXiv:2509.20181 is Balka–Héra–Kiss, *Signed null sequences and Hausdorff dimension*; it was misdescribed as being on "real achievement sets".
  - Abram–Lagarias appeared in J. Fractal Geom. 1 (2014) 45–81.
  - The Agresti (1975) and Kersting (2020) records were verified, and Kersting (2020) is now credited as the closest classical analogue of Theorems 11.4 and 11.7.
  - Classical or earlier sources are now credited for Theorem 11.45(a) (binomial congruence), Theorem 11.48(a,b) (Chebyshev, Cauchy–Schwarz), Proposition 11.21 (the compactness reformulation of §2), Proposition 11.53 (Kitamura's shadow of $-2$) and Corollary 11.39 (the $L^2$/energy method for Bernoulli convolutions).
- **M12.** The round-3 headers carried only the date 2026-10-12, and the header said "AI-refereed" while the reports were pending. Dates and status are now corrected in the front matter, §0, §8 and the §11 heading.

*Presentational points from the refutation attempts (adopted):*
- Theorem 11.14(ii) now cites locality (Theorem 3.1(a)) to pass from natural $a$ to the whole class.
- Theorem 11.17 states "for every $w$ with $p\nmid w$ and every $K\ge1$".
- Lemma 11.18's "window $k$" is now the positions $a_k+1,\dots,a_k+P$ that enter $g_k$; it said $a_k+[0,P)$, and no bound changes. After the round-3 re-check it is renamed $W_k$, so that "window $k$" has one meaning.
- A precise citation is given for the local mass distribution principle (proposition number as given by a referee).
- Corollary 11.20 uses $\sup$ for $\max$.
- Corollary 11.39(b) now says that $\nu$ lives on a scaled copy of $E_{N_0}$.
- The independence of $A_p$ from $N_0$ in Theorem 11.38 is made explicit.
- The $p=23$ entry of the Corollary 11.19 table has $K=L_p$.

Points raised and judged to need no change:
- "$V_{n_0}\ge13$" in Theorem 11.29 understates a true $\ge16$; it is still a valid bound.
- §0 item 20 omits $p=11$.

*Re-check of the corrected text (AI, 2026-10-21; `data/round3/review/recheck/`).* A further Claude instance re-read the corrected §0 and §11 against all referee findings and recomputed $\theta_3$, the exact densities and the counterexamples to the withdrawn Consequence with its own scripts. It confirmed that S1, S2 and M1–M12 are addressed, that every corrected constant is a valid bound, and that the revision introduced no new mathematical error and affects no [proved] statement. It found six minor wording issues, all applied in this version:
- R1: the alternative to H′(p)(b) in §11.7 item 3 now asks for $\mu\{M_j\ge cS_j\}>(1+p^LK/c)\,\mu(\sigma_j<\infty)$ (it had $c\,n_j^4S_j$ and "not exponentially small");
- R2: the sentence on the annealed second moment before Conjecture 11.10 is qualified as in §11.6;
- R3: one date convention (CDT) for the lead's work;
- R4: the constants sentence after Theorem 11.38 bounds $\log_pX$ correctly;
- R5: Lemma 11.18 uses $W_k$ instead of a second meaning of "window $k$";
- R6: Computation 11.55's reproduction claim is restricted to $G\le28,17,11,9$.

*Where referees differed, and the lead's verdict.*
1. *$\theta_3$ fix:* $0.22941$ against $0.229401$. Both are valid upper bounds; the note uses $0.229401$.
2. *$p=13$ dimension fix:* $0.99965$ against $0.999656$. Both are valid; the note uses $0.999656$, consistent with the table.
3. *Corollary 11.30, supremum of the full $C_6$ bound:* the lead and the computational referee found $1.680\cdot10^5$; two refutation attempts found $1.657\cdot10^5$ and $1.6776\cdot10^5$. The lead re-ran `lead_t2_constants.py`. The supremum is attained near $G=2^{354}$, beyond those two referees' ranges ($G\le2^{190}$ and $G\le2^{120}$), so $1.680\cdot10^5$ is right and the smaller values are truncation effects. All values lie below the stated $1.98\cdot10^5$, so nothing changes.
4. *Registration time of `PREDICTIONS_registered_T1b.txt`:* one refutation attempt read the file times as UTC−7 and concluded that the label "2026-10-21T22:18:27Z" was wrong. The lead checked the original file: its creation time is 17:18:27 CDT (UTC−5), which is 22:18:27 UTC. **The label is correct**, and registration preceded the first run (22:18:57Z) by 30 s. The file was later appended with outcomes, below a line marking the append. Its modification time (22:37:02Z) is after the runs, so the claim that nothing above that line was edited rests on the file's own statement.

*What the referees re-ran and confirmed* (details in their reports):
- **Dimension constants.** All 19 constants $D_p(w,K)$, by four independent programs; every rounding margin is $\ge1.3\cdot10^{-5}$.
- **Hensel and code machinery.** The constructions of Theorems 11.14 and 11.17, including the distance formula (11.2), the cylinder–ball correspondence and the slopes: tens of thousands of exact $p$-adic tests with 0 failures.
- **$p=2$ certificates and identities.** The certificates of Proposition 11.25 (the 64-case histogram, by four programs) and the window identity (11.4), exactly, both weighted and unweighted.
- **Constants of Corollary 11.30.** Recomputed by four referees.
- **Gate law and $L^2$ masses.** The gate law, $J_0$, $L_p$, $\theta_p$ and $\theta^{\rm set}_p$ for $p\le17$ by exhaustive $3^p$ enumeration; every exact $C_k$ level.
- **Exact census.** The census at $p=2$, $G=28$ ($31\,246\,552$ survivors).
- **Comparisons with Kitamura and deep values.** Kitamura's table for $a\le4096$ (0 mismatches) and $N(4096,G)$; the new $f(2210,2)=8467$ by a third program; $g_2(3456)$ and $g_2(1102)$.
- **Gate constants.** $c_p$, Lemma 11.54 and $c_1(13)\ge2.2\cdot10^{-5}$.
- **Covering pattern and Theorem 11.45.** The Cov$(13,3,H)$ pattern of Remark 11.49, and the congruences of Theorem 11.45 (92 000 cases).

*Not re-run by any referee:* the coverage certificates behind $f(1,19)\ge17\,927\,094\,312$ (only the arithmetic and position counts were checked), the T1a window statistics and atom Monte Carlo, the deepest exact $C_k$ levels, the SMC, an exact census at $(5,11)$ and $(7,9)$, and $g_2(34)$ at cap 19 000 (stopped at the 45-min limit).

*What the lead-author AI instance checked before the referees (2026-10-21).*
- *Proofs rewritten and checked step by step:*
  - T1a: Lemma 11.1, Proposition 11.2, Theorems 11.3, 11.4, 11.6, 11.7, Corollary 11.5.
  - T1b: Theorem 11.11, Lemma 11.12, Proposition 11.13, Theorems 11.14, 11.15, 11.17, Lemma 11.18, Corollaries 11.19(a), 11.20, Proposition 11.21. Details were added in Theorem 11.17 on the constancy of $\rho_k$ on cylinders.
  - T2: Lemmas 11.23, 11.24, 11.27, Propositions 11.25, 11.26, 11.28, 11.31, 11.32, Theorem 11.29, Corollary 11.30, with the constants re-derived independently (L2).
  - T3a: Lemmas 11.35, 11.37, Theorems 11.36, 11.38, Corollary 11.39, Propositions 11.40–11.42.
  - T3b: Theorems 11.45, 11.46, 11.48, Corollary 11.47, Remark 11.49.
  - T4: Lemmas 11.52, 11.54, Proposition 11.53.
- *Errors the lead missed:* the lead found no mathematical error, but the referees later found the two serious errors S1 and S2 and the wrongly rounded constants M1–M3. **The lead's check alone was not sufficient.**
- *Downgraded:* Proposition 11.8 is labelled [sketch], because the lead did not re-check its constancy statements at the higher precision.
- *Corrections made by the lead before refereeing:*
  - The interpolation step behind the constants of Corollary 11.30 was replaced by an exact piecewise evaluation; the stated constants survive.
  - The "mismatch" line of T4b-finish's newer parser was traced to a missing $f\to g$ conversion; there are 0 mismatches after conversion.
  - The new exact value $g_2(2210)=6261$ was re-derived with a second, independently written program.
- *Track self-corrections recorded:* T3b found and corrected two errors in its own 2026-10-12 text (Theorem 11.48 and Remark 11.49).

*Credit.*
- Problem and earlier results: Erdős–Graham; S. Lin (memorandum; see the date question in §11.0); V. Kovač (2025); T. Tao (2025; the covering programme behind §11.5); K. Kitamura (July 2026). From Kitamura: the normal form, the determinacy lemma, the exact $p=2$ table, the deep records reproduced in §11.6, the critical-branching picture and the "$\approx11.5/G$" fit analysed in §11.3, and the cube identity and shadow family used in Corollary 11.20 and behind Proposition 11.53, as in §2.
- Earlier public AI write-ups (neelsomani, erichou1, AItoBit; §2): the compactness reformulation, restated in Proposition 11.21.
- Within this project:
  - the quenched martingale and frozen-state weights are round-2 track R1b's (§10.1);
  - the class split at $p=2$ and the hard class $14\bmod16$ were first proposed in round-2 track R1a's unverified Claim 10.9;
  - programs A, B (track R3) and C (round-2 computational referee) underlie A′, C′;
  - Theorem 10.12, Corollary 10.13 and Proposition 10.15 (track R2b) are used in §11.5;
  - $T_p(k)$, RMF and Corollary 10.20 (tracks R2a, R2b) frame §11.4;
  - the exact census is round 1's (tracks D, E) and the round-2 computational referee's.
- Classical tools: Hensel's lemma, Strassmann's theorem, Cauchy–Davenport, the mass distribution principle, $L^2$ martingale convergence, Paley–Zygmund-type second-moment arguments (Kahane), Chernoff bounds, Parseval, the binomial congruence $(-1)^i\binom{p^D-1}i\equiv1\pmod{p^{D-\lfloor\log_pi\rfloor}}$ (Theorem 11.45(a)), and the Chebyshev and Cauchy–Schwarz facts of Theorem 11.48(a,b).
- Corollary 11.39 is a $p$-adic analogue of the classical $L^2$ (energy) method for Bernoulli convolutions.
- The second-moment and size-biasing strategy for branching processes (Kesten–Stigum 1966; Lyons–Pemantle–Peres 1995; for random environments Tanny 1988 and Kersting–Vatutin 2017) is the template of §11.1. Closest to Theorems 11.4 and 11.7 is G. Kersting (2020), which treats square integrability of the normalised martingale of a branching process in a varying environment. No theorem of these works is used: the frozen-state weights and the window identity are specific to this problem.
- The varying-environment survival estimate behind Heuristic 11.33 is Agresti (1975) and Kersting (2020). Their bibliographic records were verified by the round-3 novelty referee.
- Sequential Monte Carlo (Del Moral 2004) is used heuristically in §11.4.
- *Novelty.*
  - The gate (2026-10-12) and the round-3 novelty referee (2026-10-21) found no prior or concurrent public work overlapping any §11 result. The referee searched erdosproblems.com/404 (still open, last edited 29 Sep 2025, 7 comments, 0 proof claims), GitHub (only this project's repository, Kitamura's two repositories, a template repository and `przchojecki/agentic-erdos`, with no structural overlap; formal-conjectures PR #6936 still open; issue #1 on Kitamura's odd-prime repository unanswered), arXiv and MathOverflow.
  - The checked results are: the perfect kernel, uncountability and Hausdorff dimension of $K_p$; the explicit $p=2$ rate; the odd-$p$ martingale and $L^2$ criterion; the $L^2$ carry cocycle and $\theta_p$; $f(1,19)\ge17\,927\,094\,312$; and $f(2210,2)=8467$. In Kitamura's repositories, $a=2210$ appears only inside witness index lists.
  - Kitamura's "$\approx11.5/G$" is undefined in the source, and our reading of it as $2\delta_G(2)$ remains a heuristic.
  - Related but different: Abram–Lagarias on $p$-adic path-set fractals, and Balka–Héra–Kiss on signed null sequences and the Hausdorff dimension of the associated sets of sign sequences.
  - Gaps: Google Scholar and zbMATH were not queried directly, and Kitamura's older forum posts were not paged. We cannot exclude overlap with unpublished or AI-generated work.

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
- [Round 3; bibliographic records verified by the round-3 literature gate on 2026-10-12 at publisher, Project Euclid, arXiv, Numdam, Mathnet or IMPAN pages; contents from abstracts only unless stated]
  - *Corrected entries for references above (§11.0).* M. Z. Garaev, F. Luca, I. E. Shparlinski, *Character sums and congruences with $n!$*, Trans. Amer. Math. Soc. 356 (2004) 5089–5102, arXiv:math/0403422; and *Exponential sums and congruences with factorials*, J. reine angew. Math. 584 (2005) 29–44, arXiv:math/0403424. M. V. Kozlov, Teor. Veroyatnost. i Primenen. 21:4 (1976) 813–825; English translation Theory Probab. Appl. 21:4 (1977) 791–804. Zenodo 10.5281/zenodo.23144232 is "Version 1".
  - J. Geiger, G. Kersting, *The survival probability of a critical branching process in a random environment*, Theory Probab. Appl. 45 (2001) 517–525, doi:10.4213/tvp491.
  - H. Kesten, B. P. Stigum, *A limit theorem for multidimensional Galton–Watson processes*, Ann. Math. Statist. 37 (1966) 1211–1223, doi:10.1214/aoms/1177699266.
  - R. Lyons, R. Pemantle, Y. Peres, *Conceptual proofs of $L\log L$ criteria for mean behavior of branching processes*, Ann. Probab. 23 (1995) 1125–1138, arXiv:math/0404083.
  - D. Tanny, *A necessary and sufficient condition for a branching process in a random environment to grow like the product of its means*, Stoch. Proc. Appl. 28 (1988) 123–139.
  - J. Coffey, D. Tanny, *A necessary and sufficient condition for noncertain extinction of a branching process in a random environment (BPRE)*, Stoch. Proc. Appl. 16 (1984) 189–197.
  - G. Kersting, V. Vatutin, *Discrete Time Branching Processes in Random Environment*, ISTE/Wiley, 2017.
  - J.-P. Kahane, *Some Random Series of Functions*, 2nd ed., Cambridge Univ. Press, 1985 (Paley–Zygmund inequality).
  - B. Jessen, A. Wintner, *Distribution functions and the Riemann zeta function*, Trans. Amer. Math. Soc. 38 (1935) 48–88; P. Hartman, *Infinite convolutions on locally compact Abelian groups and additive functions*, Trans. Amer. Math. Soc. 214 (1975) 215–231 (pure laws on LCA groups; full text not read).
  - C. Cobeli, M. Vâjâitu, A. Zaharescu, *The sequence $n!\pmod p$*, J. Ramanujan Math. Soc. 15 (2000) 135–154 (page range confirmed by the round-3 novelty referee). Cited by T1b only to say that residues of $r!\bmod p$ are not needed.
  - Ž. Mijajlović, *Fifty years of Kurepa's $!n$ hypothesis*, Bull. Cl. Sci. Math. Nat. Sci. Math. 46 (2021) (Kurepa's conjecture still open).
  - Yudin, arXiv:2610.01899; V. Abramov, arXiv:2604.26429; S. D. Hughes, arXiv:2609.10902 — adjacent recent preprints with no bearing on #404 (§11.0).
- [Round 3; cited by the tracks; bibliographic records verified by the round-3 novelty referee on 2026-10-21, contents from abstracts and records only]
  - A. Agresti, *On the extinction times of varying and random environment branching processes*, J. Appl. Probab. 12(1) (1975) 39–46 (Heuristic 11.33).
  - G. Kersting, *A unifying approach to branching processes in a varying environment*, J. Appl. Probab. 57(1) (2020) 196–220, doi:10.1017/jpr.2019.84. Treats square integrability of the normalised martingale in varying environments; the closest classical analogue of Theorems 11.4 and 11.7 (§11.9), and the source of the survival estimate behind Heuristic 11.33.
  - S. Abram, J. C. Lagarias, *p-adic path set fractals*, J. Fractal Geom. 1 (2014) 45–81, arXiv:1210.2478 — related but different (T1b).
  - Balka, Héra, Kiss, *Signed null sequences and Hausdorff dimension*, arXiv:2509.20181 (2025) — dimension of sets of sign sequences; related but different. *[Corrected: earlier described here as a paper on "real achievement sets".]*
- [Round 3; cited by the tracks but **not** verified by the gate or the referees]
  - Strassmann's theorem: J. W. S. Cassels, *Local Fields*, LMS Student Texts 3, Cambridge Univ. Press, 1986; N. Koblitz, *p-adic Numbers, p-adic Analysis, and Zeta-Functions*, GTM 58. Mass distribution principle: K. Falconer, *Techniques in Fractal Geometry*, Wiley, 1997 (local version: Prop. 2.3, as cited by a round-3 referee; not checked by the lead).
  - P. Del Moral, *Feynman–Kac Formulae*, Springer, 2004 (sequential Monte Carlo; T3a).
- [Round 3] This project's own public repository: `github.com/AstroCat93/erdos-404-research` (created 2026-10-12), and the issue opened from it at `KitaKen1/erdos-404-odd-prime-landscape` #1 (2026-10-12).
