# Erdős Problem #404: structure, finiteness families and certified lower bounds

This repository is a research note on [Erdős Problem #404](https://www.erdosproblems.com/404) (sums of distinct factorials divisible by high prime powers), with the code, logs and data behind it.

**Problem #404 is not solved.** Status after round 3 (2026-10-21):
- **Q3 is open.** Nothing here proves that $f(a,p)=\infty$ for any pair $(a,p)$.
- **Q1 is open in general.** *New in round 2:* at $p=2$, $f(a,2)<\infty$ for all $a$ outside a set of natural density $0$ (note.md Theorem 10.1). This is a complete proof, checked by AI referees and not by a human. *New in round 3:* an explicit rate off the class $a\equiv14\pmod{16}$ (note.md Corollary 11.30). Whether $f(a,2)<\infty$ for *every* $a$ is still open. For odd $p$, positive measure of the infinity set is reduced to an unproved hypothesis.
- **Q2 has partial results.** These are structural theorems (in round 3: the infinity set $K_p$ is uncountable, with Hausdorff dimension at least 0.853 at $p=2$ and at least 0.9247 at $p=3$), exact values on residue classes, much larger certified lower bounds than were previously published, and precise sufficient conditions for a positive answer to Q3.

**Status check, 2026-10-12.** There are no new results on #404 by others since this note was first written (8 Oct). The following show no change: the problem page (last edited 29 Sep 2025, 0 proof claims), Kitamura's repositories (last pushed 7–8 Jul 2026), the teorth/erdosproblems database (status `open`) and arXiv. A Lean formalization of the *statement* of #404 is under review in google-deepmind/formal-conjectures (PR #6936, still open). The workflow lead checked on 11 Oct, and the round-2 novelty referee re-checked on 12 Oct.

**Status check, 2026-10-21.** The round-3 gate (12 Oct) and the round-3 novelty referee (21 Oct) again found no prior or concurrent work by others overlapping the new results: the problem page is unchanged, Kitamura's #404 repositories have not been pushed since July, PR #6936 is still open, and arXiv and MathOverflow show nothing relevant. Google Scholar and zbMATH were not queried directly (note.md §11.0, §11.9).

The full write-up is [`note.md`](note.md). **The mathematics, code and text were produced by AI** (see [AI disclosure](#ai-disclosure-and-authorship)). No human has verified the mathematics. Three rounds of AI referees have checked it: three referees (logic, computation, novelty) per round, plus sixteen targeted refutation attempts in round 3. See note.md §9 for round 1, §10.8 for round 2 and §11.9 for round 3.

## Interim update (2026-10-21)

*Superseded by round 3 (below): this bound is now note.md Theorem 11.50. The round-3 referees checked its arithmetic and position counts, but did not re-run the coverage certificates.*

**New bound: $f(1,19)\ge v_{19}((19^9-1)!)=17\,927\,094\,312$.** If it holds up, it supersedes the round-2 bound $943\,531\,272$ (note.md §10.2).
- It follows from Proposition 10.10. The new certificates are at depth 7 (all 342 classes, $H=45$) and depth 8 (all 18 positions, $H=49$).
- **Status:** computer-assisted. Every certificate was checked by two independently written programs.
- It was produced by Claude (Anthropic) AI instances. **It is not yet refereed** by the round-3 referees, and **it has not been verified by a human.**
- Details, caveats and reproduction: [`interim/2026-10-21-f1-19/README.md`](interim/2026-10-21-f1-19/README.md).

## The problem

For a prime $p$ and an integer $a\ge1$, let $f(a,p)$ be the largest $k$ such that $p^k$ divides $a_1!+a_2!+\dots+a_n!$ for some $a=a_1<a_2<\dots<a_n$ (or $\infty$ if there is no largest). Erdős and Graham (1980) asked:

- **(Q1)** For which $a$ and $p$ is $f(a,p)$ finite?
- **(Q2)** How does $f(a,p)$ behave?
- **(Q3)** Is there a prime $p$ and an infinite sequence $a_1<a_2<\cdots$ such that the exact power of $p$ dividing $\sum_{i\le k}a_i!$ tends to infinity?

Known before this note: $f(2,2)=254$ (S. Lin), the trivial family $a\equiv-1 \pmod p$ (where $f(a,p)=v_p(a!)$), Tao's block lemma, and K. Kitamura's extensive computations (exact values of $f(a,2)$ for $a\le256$ and deeper rows, a certified classification of all $p=2$ classes with excess $\le24$, and witnesses $f(1,p)\ge20000$ for $p=3,5,7$ and $\ge5000$ for $p=11,13$).

Write $f(a,p)=v_p(a!)+g_p(a)$. The excess $g_p$ extends to a function on the $p$-adic integers (this normal form is Kitamura's; see below).

## What is new (round 1, 2026-10-08)

Each item survived three AI referee reports (logic, computation, novelty), after the corrections listed in note.md §9. Status labels: **proved** = complete proof in the note; **Lean** = a stated core is machine-checked in Lean 4 + Mathlib (standard axioms only, no `sorry`, no `native_decide`); **computer-assisted** = depends on a finite exact computation, run by at least two independent programs unless stated otherwise.

| | Statement | Status |
|---|---|---|
| Thm 3.1 | $g_p$ is a function on $\mathbb Z_p$; the infinity set $K_p=\{g_p=\infty\}$ is closed; the density of $\{a: f(a,p)\ge v_p(a!)+G\}$ exists and is an explicit class count $\delta_G(p)$ | proved (locality part: Lean) |
| Thm 3.2, Cor 3.3 | **Exact values on explicit residue classes**: $f(a,p)=v_p(a!)+\gamma_p(m)$ whenever $a\equiv-m \pmod{p^{\gamma_p(m)+1}}$, where $\gamma_p(m)$ is a finite computation, finite for every $m\ne2$. Every residue class mod every $p^k$ contains infinitely many $a$ with $f(a,p)<\infty$. The set where $f(a,p)=v_p(a!)$ is an explicit union of classes mod $p$. This settles two residue patterns Kitamura listed for audit | proved (non-vanishing: Lean) |
| Prop 3.4 | Finite values of $g_p$ are unbounded at every prime: $3k\le\gamma_p(p^k+2)<\infty$ | proved |
| Thm 3.5–3.6 | Hensel dichotomy: on each class mod $p$, $g_p$ is $\equiv0$ or unbounded. $K_p$ is nowhere dense, so no criterion on finitely many digits of $a$ can certify $f(a,p)=\infty$ | proved |
| Thm 3.7 | $p=2$ halving lemmas; they prove Kitamura's "sibling-pairing" statement ($g_2$ is constant on $a \bmod 2^{g_2(a)}$ when $g_2(a)\ge1$) | proved + Lean |
| Thm 3.8 | Tao-type covering can never work at $p=2$: any chain of covering blocks gains at most 3 | proved + Lean |
| Thm 3.9–3.10 | Gate structure for odd $p$ via the truncated series of $e^{-1}$; a gap theorem; a barrier lemma (covering arguments that see only $c$ digits of factorial unit parts cannot cross gates of level $>c$) | proved (gate congruence: Lean) |
| Thm 3.11 | At $p=3$, for $81\mid N$, the tail sums $\sum_{n\in B}n!$ ($B\subseteq[N,\infty)$) miss exactly the classes $N!\cdot\{68,77\}$ modulo $3^{v_3(N!)+4}$ | proved |
| Thm 3.12 | The $\mathrm{Cov}$/$\mathrm{UC}$ framework, which carries out Tao's suggested programme: a uniform covering statement $\mathrm{UC}(p)$ for one prime would answer Q3 | proved (logic: Lean) |

## New in round 2 (2026-10-11/12; note.md §10)

Round 2 was produced by a second AI-assisted session:
- five research tracks;
- a lead-author AI instance that checked the proofs and re-ran the computations;
- three new AI referees (logic, computation, novelty), each writing its own code.

The referees found **no fatal or serious mathematical error**. They found two serious problems of credit and attribution, and several minor errors. All are corrected; see the list below and note.md §10.8. Only items that survived this review are listed here.

| | Statement | Status |
|---|---|---|
| Thm 10.1 | **$\mu(K_2)=0$.** The set of 2-adic $x$ with $g_2(x)=\infty$ has Haar measure $0$. Hence $\delta_G(2)\to0$, and $f(a,2)<\infty$ for all $a$ outside a set of natural density $0$. The proof is an exact quenched martingale for the carry branching process, plus an environment walk that is unbounded below. It says nothing about any particular $a$; $a=594$ is still a live test case. Kitamura had observed the decay of the surviving density empirically; we know of no earlier proof | proved; checked line by line by the AI logic referee; its core window identity was tested exactly by three separate programs |
| §10.2 | **Larger certified lower bounds** (table below), and the same deep alternative for every "deep" $a\le1000$ at $p=7,11,13$ | computer-assisted (programs A, B, C) |
| §10.2 | **$\mathrm{Cov}(11,7,40)$ is false.** The class $K'\equiv37$ misses exactly 2 residues mod $11^{10}$; $H=41$ is needed there | computer-assisted (four programs) |
| Lemma 10.11, §10.2 | Layer obstruction: $\mathrm{Cov}(p,t,H)$ needs $(H-1)\bmod p\ge\rho_0(p)$. The minimal uniform $H_t$ are tabulated for $p=7,\dots,23$, $t\le6$ or $7$ (e.g. $H_6(7)=34$) | proved; table computer-assisted (minimality scanned by programs A and C) |
| Thm 10.12, Cor 10.13 | An exact criterion for when "the incoming carries meet every class mod $p^D$" guarantees crossing a block. Fullness alone cannot carry a single level-$j$ gate block (for $D_p\le D\le j$), or a window of length $H$ with $e(H-1)!\le p^D\le p^{t-1}$. Whether it can carry a whole gate-to-gate stretch is open | proved; abstract core in Lean |
| Prop 10.14 | Monotonicity of $\mathrm{Cov}$ in $H$. Part (a) is the $\mathrm{Cov}$-level form of Tao's step | proved; recursion in Lean |
| Thm 10.16, Thm 10.18 | Two **sufficient conditions** for Q3, neither proved. (i) A random-model Fourier bound $\mathrm{RMF}(p,C)$ with $C(\Lambda_p+\tau_p(3))<1$, where $\Lambda_7=0.363$ and $\Lambda_{13}=0.0351$; since $\Lambda_5>1$, this route cannot work at $p=5$. (ii) At $p=13$, an $L^1$ bound on the deep-gate Fourier shells alone; all frequencies of order $\le13^{67\,977\,551}$ vanish exactly | proved (the conditions are unproved) |
| §10.4 | Certified Fourier shell sums $\sum_{k\le7}T_{13}(k)\le0.0093$ and $\sum_{k\le8}T_{11}(k)\le0.0669$, giving quantitative equidistribution (Cor 10.17). An exact renormalisation identity (Prop 10.19, at exactly attained levels $W$) shows that supremum-type transfer bounds cannot give decay (Cor 10.20). A factorial-base digit formula (Prop 10.21) | proved; shell sums in floating point with outward margins by three implementations, dominant shells also in interval arithmetic |

| $p$ | 7 | 11 | 13 | 17 | 19 | 23 |
|---|---|---|---|---|---|---|
| $f(1,p)\ge$ (round 2) | $6\,725\,592$ | $235\,794\,760$ | $883\,708\,272$ | $7\,411\,742\,272$ | $943\,531\,272$ | $3\,559\,590\,232$ |
| previous best | $10^6$ | $21\,435\,880$ | $67\,977\,552$ | $25\,646\,163$ | $49\,659\,537$ | $154\,764\,790$ |

Each bound is $v_p((p^D-1)!)$, obtained from uniform covering certificates for small depths and position certificates for the remaining depths (Proposition 10.10). Three programs were used:
- Programs A and B were written by one round-2 track. The lead-author instance re-ran both on 12 Oct.
- Program C was written independently by the round-2 computational referee. It re-certified every bound, and its own chain check passes for all six.
- For $p=17$, program B's half was not re-run; programs A and C were.

The "deep $a\le1000$" statements also rely on the archived round-1 landscapes.

**Not counted as results** (note.md §10.1.4, §10.5):
- the R1a track's second route to $\mu(K_2)=0$;
- its explicit bound, Claim 10.9. This is unverified, and it has a $1/16$ floor, so it gives no rate for $\delta_G(2)$;
- the heuristic Conjectures 10.22–10.26. Of the counting law's registered predictions (Conj 10.24), three were genuine out-of-sample tests, and all three were confirmed.

**Corrections made after the round-2 referees** (note.md §10.8):
- **Credit.** K. Kitamura is now credited with describing $p=2$ as a critical branching process and with reporting a measured decay of the surviving fraction. Our round 1 had attributed that picture to itself.
- **Verification wording.** "The lead author checked every proof" now says that the lead-author *AI instance* did this. The human author has not verified the mathematics.
- **Corollary 10.13.** It no longer claims to refute a fullness-only renormalisation lemma (T3).
- **Proposition 10.19 and Corollary 10.20.** These now require the level $W$ to be exactly attained.
- **Smaller fixes.**
  - The constant in Claim 10.9 is now $0.662$ (was $0.661$).
  - A grid average ($0.03678$) is replaced by the exact period mean $0.0366754$.
  - A misworded martingale remark is fixed.
  - The prediction count of Conj 10.24 is corrected.
  - "Exact reformulations" now reads "sufficient conditions".
  - The credits for branching processes in random environments (Smith–Wilkinson; Athreya–Karlin; Afanasyev–Geiger–Kersting–Vatutin) are corrected, and Proposition 10.14(a) is credited to Tao.

## New in round 3 (2026-10-12 and 2026-10-20/21; note.md §11)

Round 3 was produced by a third AI-assisted session:
- two literature and status "gate" agents and seven research tracks (T1a, T1b, T2, T3a, T3b, T4, plus two finishing instances). The gates and track T4 ran on 2026-10-12; after a budget interruption, the other tracks ran on 2026-10-20 and 2026-10-21;
- a lead-author AI instance that checked the proofs, re-ran a selection of the computations and wrote note.md §11;
- three new AI referees (logic, computation, novelty) and sixteen targeted AI refutation attempts, two for each of eight results (one hunting for a gap, one for a counterexample), all on 2026-10-21, each writing its own code;
- a revision that applied every correction, and an AI re-check of the revised text.

The referees found **no fatal error**. They found **two serious errors**, both corrected:
1. The reduction "H′(p) ⇒ $\mu(K_p)>0$" was overstated. Theorem 11.7 also needs an atom with large normalised weight and small freezing probability. H′(p) (Conjecture 11.10) now includes that condition.
2. A "Consequence [proved]" after Theorem 11.45 was false. It has been withdrawn.

They also found 12 minor errors, mostly constants rounded the wrong way, and all are corrected (note.md §11.9). The re-check found six further wording issues, which are also applied. No proof of a result labelled [proved] was refuted. Only items that survived this review are listed here.

| | Statement | Status |
|---|---|---|
| Thms 11.11, 11.14, 11.15 | **$K_p$ is uncountable, with a perfect kernel**, for every prime $p$. The closure of the simple zeros of the series $F_e=\sum_je_j\pi_j$ is a perfect subset of $K_p$, nonempty exactly in the classes $r\notin\Phi_p$. Whether $K_p$ itself is perfect is open | proved |
| Thm 11.17, Cors 11.19–11.20 | **Hausdorff dimension of $K_p$.** $\dim_HK_2\ge0.8530$ (although $\mu(K_2)=0$), $\dim_HK_3\ge0.9247$, $\dim_HK_5\ge0.9691$, $\dim_HK_7\ge0.9921$, $\dim_HK_{13}\ge0.9996$. Consequently $\delta_G(2)\ge2^{-(0.147+o(1))G}$. None of this places a natural number in $K_p$ | proved; the constants are exact computations reproduced by four independently written programs |
| Thm 11.29, Cor 11.30 | **An explicit rate at $p=2$ off one class.** The density of $\{a\not\equiv14\ (\mathrm{mod}\ 16):f(a,2)\ge v_2(a!)+G\}$ is at most $2.0\cdot10^5\,G^{-0.227}$. This beats the trivial bound only for astronomically large $G$, and it gives no rate for $\delta_G(2)$ itself | proved |
| Thms 11.3, 11.4, 11.7 | **Odd $p$:** the quenched martingale of §10.1 transfers, and $\mu(K_p)>0$ (Conjecture 5.2) follows from hypothesis H′(p): a uniform variance bound together with one atom with large normalised weight and small freezing probability | proved; **H′(p) is unproved for every $p$** |
| Thms 11.36, 11.38, Cor 11.39 | **The $L^2$ form of the Fourier route.** The $L^2$ mass $C_k$ factorises into a positive carry cocycle, and unconditionally $C_k\le p^{\theta_pk+O(\log^2k)}$, with $\theta_2=\log_23/4$, $\theta_3\le0.229401$, $\theta_{13}\le9.08\cdot10^{-4}$. This gives dimension bounds for the tail sets and $T_p(k)\le p^{(1+\theta_p)k/2+o(k)}$: a square-root saving, **not** decay. Two obstructions (Props 11.40, 11.41) | proved |
| Thms 11.45, 11.46, 11.48 | **The covering route:** an exact lifting criterion at the final gate, and negative results (fullness of the carry fibres never suffices; the second-moment covering criterion is useless at depth). These are reformulations, not progress on $\mathrm{UC}(p)$ | proved |
| Thm 11.50 | **$f(1,19)\ge v_{19}((19^9-1)!)=17\,927\,094\,312$**, up from $943\,531\,272$ (this is the interim result of 2026-10-21) | computer-assisted; every certificate by two independently written programs (A′, C′). The referees checked the arithmetic and position counts but did not re-run the certificates |
| Prop 11.53, Comp 11.55 | The annealed second moment satisfies $\mathbb EZ_G^2\ge p^G/4$ at every prime. Exact annealed moments to $G=28,17,11,9$ for $p=2,3,5,7$, giving $f(a,p)<\infty$ on density $\ge0.4783977$ ($p=5$) and $\ge0.3760812$ ($p=7$) | proved; computer-assisted (the two new densities rest on one program, corroborated by an independent Monte Carlo) |
| §11.6 | New exact value $f(2210,2)=8467$, by two independently written programs; three of Kitamura's deep records reproduced independently | computer-assisted |

**Status of Q1–Q3 after round 3** (note.md §11.7):
- **Q1 is open in general.** At $p=2$ there is now an explicit rate off the class $14\bmod16$. Whether $f(a,2)<\infty$ for every $a$ is open ($a=594$ is still a live test case). For odd $p$, $\mu(K_p)>0$ is reduced to the unproved H′(p).
- **Q2 has partial results:** the new bound for $p=19$, the exact value $f(2210,2)=8467$, the two exact densities, and the structure of $K_p$.
- **Q3 is OPEN.** Round 3 adds no new sufficient condition for Q3 beyond reformulations, and nothing proves $f(a,p)=\infty$ for any $(a,p)$.

**Not counted as results** (note.md §11.1, §11.3, §11.4, §11.6):
- H′(p) itself (Conjecture 11.10). Its variance part has numerical support at shallow depths only.
- Conjectures 11.22 ($\dim_HK_2=1$), 11.34 ($\delta_G(2)\sim c_2/G$ with $c_2\approx5.5$–$6$) and 11.44 ($C_\infty<\infty$ for odd $p$), and Heuristic 11.33.
- The Monte Carlo evidence for $\delta_G(2)\approx5.5/G$. Our reading of Kitamura's "$\approx11.5/G$" as $2\delta_G(2)$, the fraction among even $a$, is a heuristic. The earlier fit $0.7/\sqrt G$ of §5 was a small-$G$ transient.
- The statement that the untruncated annealed second-moment route to $\mu(K_p)>0$ is hopeless. It rests on numerics for the first moments, and truncated moments are not ruled out.
- The two further confirmed out-of-sample predictions of the covering counting law (Computation 11.51); the law itself is heuristic.

**Corrections made after the round-3 referees** (note.md §11.9):
- **S1.** H′(p) now contains the atom condition; the four summaries that said the variance bound alone suffices are corrected.
- **S2.** The Consequence after Theorem 11.45 is withdrawn. The lead-author instance reproduced the counterexamples at $p=3,5,7$.
- **Constants.** $\theta_3\le0.22940$ was truncated; it is now $\le0.229401$ ($\theta_3=0.2294000283$). The $p=13$ dimension bound $0.99966$ is now $0.999656$. **The round-1 odd-prime density bounds $0.4784$, $0.3761$, $0.2455$ ($p=5,7,13$) had been rounded up**; they are now $0.4783$, $0.3760$, $0.2454$ (the table below is corrected).
- **Wording and credit.** "The annealed route is closed" is now labelled heuristic. Theorem 11.48(b) is stated with $\le$. G. Kersting (2020) is credited as the closest classical analogue of Theorems 11.4 and 11.7, and classical sources are credited for several standard steps. Two bibliographic entries are fixed. Statistical fits on nested Monte Carlo samples are now labelled descriptive.
- **The lead's own check missed both serious errors and the wrongly rounded constants.** The note records this.

## What is computed in round 1 (computer-assisted)

| Result | How | Checked by |
|---|---|---|
| $f(1,3)\ge2\,000\,001$, $f(1,5)\ge10^6$, $f(1,7)\ge10^6$ | explicit witness lists (1.4–1.6 million terms; `archive/witnesses/`) | two independent verifiers each |
| $f(1,13)\ge67\,977\,552$ *(superseded in round 2)* | $\mathrm{Cov}$ certificates for all depths $t\le7$ | `cov.c` + an independent checker; also the computational referee |
| $f(1,11)\ge21\,435\,880$ *(superseded in round 2)* | $\mathrm{Cov}$ certificates for $t\le6$ plus the ten depth-7 positions $11^7K''$ (found during refereeing) | the referee's `rcover.c` and our `cov_pos.c` |
| $f(a,7)\ge960\,792$ for $a=2,3,5$ *(superseded in round 2)* | as above, with the six depth-7 positions $7^7K''$ | `cov_pos.c` and `rcover.c` |
| every $a\le1000$: either $f(a,13)-v_{13}(a!)\in\{0,1\}$ or $f(a,13)\ge67\,977\,552$; similarly $\{0,1\}$ / $21\,435\,880$ at $p=11$ and $\le3$ / $960\,792$ at $p=7$ *(deep alternatives superseded in round 2)* | certificates + exact small-$a$ landscapes | landscapes: archived run + the computational referee's independent DP |
| $f(1,p)\ge25\,646\,163$ ($p=17$), $49\,659\,537$ (19), $154\,764\,790$ (23), $616\,067\,009$ (29), $917\,087\,135$ (31) *($p=17,19,23$ superseded in round 2)* | Theorem 3.9(c) + certified two-block windows | re-run; windows re-checked by both referees |
| $f(1,p)\ge p+\dots+p^6$ for $37\le p\le53$ (e.g. $2.26\cdot10^{10}$ at $p=53$); $\ge p+\dots+p^5$ for $59\le p\le97$ | Theorem 3.9(c) alone (covering depth of $\{(-1)^u/u!\}$) | archived run; re-checked by the computational referee (and by the logic referee for $p\le53$) |
| $f(a,2)<\infty$ on density $\ge0.8866$ ($G=29$; three programs) and $\ge0.8984$ ($G=32$; two programs). Kitamura's census already gave $0.8734$ | exact class census | see note.md §4.7 |
| $f(a,p)<\infty$ on density $\ge0.6367$ ($p=3$), $0.4783$ (5), $0.3760$ (7), $0.3002$ (11), $0.2454$ (13): the first such densities at odd primes beyond $a\equiv-1$. *Corrected in round 3: rounds 1–2 printed $0.4784$, $0.3761$, $0.2455$, which round these lower bounds up. Round 3 improves $p=5,7$ to $0.4783977$ and $0.3760812$* | exact class census | archived/re-run + the computational referee |
| $\mathrm{Cov}(5,5,H)$ fails for every $H\le38$ | explicit failing class for each $H$ | `cov_pos.c` / `cov.c` and `rcover.c` |

Two frontier results in note.md §4.5 ($f(3,5)\ge117\,499$ and $f(a,3)\ge50$ for 11 small $a$) rest on a single implementation and are flagged there.

## What is conjectural

These are **not** proved; see note.md §5–6.
- $f(a,2)<\infty$ for every $a$ (Conjecture 5.1). *The weaker form $\mu(K_2)=0$ is now proved (Theorem 10.1).* Evidence for the strong form: exact densities to $G=32$ and Monte Carlo to $G=254$; but a measure-theoretic argument cannot see a countable set.
- $\mu(K_p)>0$ for every odd $p$ (Conjecture 5.2); numerically $\mu(K_3)\approx0.36$, $\mu(K_5)\approx0.52$, $\mu(K_7)\approx0.62$.
- $\mathrm{UC}(p)$ for $p\ge7$ (Conjecture 5.3), which would give $f(1,p)=\infty$ and answer Q3 positively. Certified for depths $t\le7$ at $p=13$; the "missing lemma" for $t\ge8$ is stated precisely in §6.
- The Fourier and branching-process heuristics of §5.
- *Round 2* (note.md §10.5):
  - the deep-shell Fourier inequality MI-13 (Conj 10.22), which would give $f(1,13)=\infty$;
  - RMF with a bounded constant for $p=7,11,13$ (Conj 10.23);
  - the bottleneck counting law for covering (Conj 10.24) and its predicted $H_t$.
- *Round 3* (note.md §11):
  - H′(p) (Conj 11.10), which would give $\mu(K_p)>0$ for odd $p$;
  - $\dim_HK_2=1$ (Conj 11.22);
  - $\delta_G(2)\sim c_2/G$ with $c_2\approx5.5$–$6$ (Conj 11.34);
  - the $L^2$ dichotomy $C_\infty<\infty$ for odd $p$ (Conj 11.44).

## Prior work and credit

- **P. Erdős and R. L. Graham** posed the problem (1980).
- **S. Lin** proved $f(2,2)=254$ (Bell Labs memorandum, cited on erdosproblems.com).
- **V. Kovač** corrected the problem statement on the forum (13 Aug 2025).
- **T. Tao** (forum, 29 Sep 2025) stated the block lemma and proposed the programme of position-independent finite computations at each depth. Theorems 3.9 and 3.12 carry that programme out.
- **K. Kitamura** ([`KitaKen1/erdos-404-p2-landscape`](https://github.com/KitaKen1/erdos-404-p2-landscape), [`KitaKen1/erdos-404-odd-prime-landscape`](https://github.com/KitaKen1/erdos-404-odd-prime-landscape), July 2026) introduced the normal form $g=f-v_p(a!)$ at $p=2$ and proved its determinacy (our Theorem 3.1(a) at $p=2$). Kitamura also found the cube identity and the shadow family $2^t-2$, computed the exact values ($f(34,2)=18444$ and others), and gave the certified classification of $p=2$ classes with $g\le24$. From that classification come the $p=2$ value set ($g\ne1,2,4,5$; $g=3$ iff $a\equiv4 \pmod 8$) and the density $0.8734$. Kitamura stated the sibling-pairing theorem and built the first large odd-prime witnesses. Kitamura also described $p=2$ as a critical branching process and reported a measured decay of the surviving fraction (about $11.5/G$). This anticipates empirically the density statement that Theorem 10.1 proves; credit for it was added in round 2. This note re-derives several of these statements and credits them throughout.
- **Earlier AI write-ups** already contained the compactness equivalence "Q3 iff some $f(a,p)=\infty$": `neelsomani/gpt-erdos` (2026-01-17), `erichou1/erdos-open-problems` (2026-06-10) and `AItoBit/Erdosproblems-llm-hunter` (2026-09-25).
- **AItoBit** opened google-deepmind/formal-conjectures PR #6936 (statement only).
- **Branching processes in random environments** (Smith–Wilkinson 1969; Athreya–Karlin 1971; Afanasyev–Geiger–Kersting–Vatutin 2005) supply the general strategy behind Theorem 10.1, whose proof is self-contained.
- **Branching processes, round 3.** The second-moment and size-biasing strategy (Kesten–Stigum 1966; Lyons–Pemantle–Peres 1995; Tanny 1988; Kersting–Vatutin 2017) is the template of note.md §11.1. Closest to Theorems 11.4 and 11.7 is G. Kersting (2020), on square integrability of the normalised martingale in a varying environment. Classical tools (Hensel's lemma, Strassmann's theorem, the mass distribution principle, the $L^2$/energy method for Bernoulli convolutions) are credited in note.md §11.9.
- **T. Bloom** maintains erdosproblems.com.

## Reproducing

You need a C compiler (clang or gcc) and Python 3. A few sanity scripts use `numpy` and `sympy`. Lean 4 + Mathlib (v4.34.1) is needed only for the Lean files. Everything was run on macOS (Apple silicon) using at most 3 cores.

```sh
cd code
sh build.sh                          # compile all C programs
python3 -I indep/indep_checks.py     # independent oracle: known values, gamma/Phi, obstructions, Cov spot checks (~15 s)
sh C/run_C.sh                        # L_p table, p = 17 windows, structure checks, f(1,11) witness (~10 min)
sh run_DEFA.sh                       # frontiers, class trees, p = 2 checks (~3 min)
sh B/run_B_cov.sh                    # all 23 Cov certificates, twice for the largest (~35 min, ~2.5 GB RAM)
B/bin/cov_pos 11 7 40 1 2 3 4 5 6 7 8 9 10   # the depth-7 positions behind f(1,11) >= 21 435 880 (6.5 GB RAM)
sh lean/run_lean.sh /path/to/a/Mathlib/project   # the seven Lean files
```

`note.md` §7 lists every command (R1–R21) with its expected output, log file and running time. §7.3 lists what rests on archived logs (copied into `archive/`) and whether a referee reproduced it independently.

Round 2 (`note.md` §10.7; details in [`code/round2/README.md`](code/round2/README.md)):

```sh
cd code/round2
clang -O3 -march=native -o R3/bin/fibcov  R3/src/fibcov.c     # covering program A
clang -O3 -march=native -o R3/bin/fibcov2 R3/src/fibcov2.c    # covering program B
clang -O3 -o R2a/bin/fl1 R2a/fl1.c -lm -lpthread && clang -O3 -o R2a/bin/fl1_lead R2a/fl1_lead.c -lm
sh run_lead_batch.sh /path/to/a/Mathlib/project   # rows S1-S13: window identity of Thm 10.1, shell sums, Lean, ... (tens of minutes, one core)
cd R3 && R3_LOGS=../../../data/round2/outputs/R3 python3 src/chain.py specs/p13.txt   # re-check a chain from the archived logs
```

The certificate re-runs (rows C1–C6) take a few CPU-hours in total and are driven by a job list; see `code/round2/README.md`. The round-2 referees' programs are in `code/round2/review/`, and their logs are in `data/round2/review/`.

Round 3 (`note.md` §11.8; details in [`code/round3/README.md`](code/round3/README.md)):

```sh
cd code/round3
python3 -I lead/lead_r3fix_checks.py                     # theta_3, the withdrawn Consequence's counterexamples, new densities (<2 s)
(cd T1b-Kp-structure && clang -O2 -o wdim wdim.c -lm && ./wdim 3 5 13)   # one dimension constant of Corollary 11.19
(cd T3a-q3-fourier && python3 verify_l2_r3.py)           # 111 exact L^2 masses
(cd T3b-q3-covering && L=../../../data/round2 && python3 src/chain_r3.py 19 9 "$L/outputs/R3:$L/logs_original/R3:$L/review/computation/logs:../../../data/round3/T3b-q3-covering/logs" specs_p19_D9_r3.txt 2)   # chain behind f(1,19) >= 17927094312
```

The round-3 referees' reports, programs and logs are together in `data/round3/review/`.

## Repository layout

```
README.md            this file
note.md              the research note (statements, proofs, computations, verification summary)
code/                programs of the six research tracks (A-F), the independent oracle, Lean files, build/run scripts
code/outputs/        logs of the 2026-10-08 re-runs (pub_* = publication re-checks R19-R21)
archive/             archived logs that the "not re-run" items rest on; gzipped witnesses for p = 3, 5, 7
review/              the round-1 referees' own programs and outputs
code/round2/         round-2 programs (tracks R1a, R1b, R2a, R2b, R3; the lead's checks; the round-2 referees' programs in review/)
data/round2/         round-2 logs: original track logs, the 2026-10-12 re-runs, the round-2 referees' logs
code/round3/         round-3 programs (tracks T1a, T1b, T2, T3a, T3b, T4; the lead's checks)
data/round3/         round-3 track reports, logs and data; the round-3 referees' reports, programs and logs in review/
interim/             the interim update of 2026-10-21 (f(1,19)), now note.md Theorem 11.50
LICENSE              MIT (code)
LICENSE-docs.md      CC BY 4.0 (documents)
CITATION.cff
```

## AI disclosure and authorship

- **Author:** Nathan Durfee, as composer and prompter. Nathan Durfee chose the problem and directed the work, and has **not** personally verified the mathematics.
- **Mathematics, code and text:** produced by Claude (Anthropic, model Claude Opus 5.5), running as a multi-agent workflow in Claude Code. The workflow had five stages:
  1. literature and community "gate" agents;
  2. six parallel research tracks;
  3. a lead-author agent that cross-checked the tracks, wrote an independent oracle and re-ran the computations;
  4. three separate referee agents (logic, computation, novelty);
  5. a revision that applied every referee correction and re-checked the new computations.
- **Referee outcome (round 1):** no fatal or serious mathematical error was found. The novelty referee found that the first draft overstated novelty and under-credited Kitamura and earlier AI write-ups; this is corrected. The computational referee contributed the depth-7 improvements, which we re-checked with separate code. Details are in note.md §9.
- **Round 2 (2026-10-11/12):** the same model and the same kind of workflow, with:
  - five research tracks;
  - a lead-author AI instance that checked the proofs, re-ran the computations and wrote note.md §10;
  - three new referee agents (logic, computation, novelty), each writing its own code;
  - a revision that applied all their corrections.

  Wherever the note says "the lead" or "the lead author" in round 2, it means that AI instance, not the human author.
- **Referee outcome (round 2):** no fatal or serious mathematical error. The logic referee checked the proof of Theorem 10.1 line by line and found no gap. The computational referee re-certified every new bound with its own program. The novelty referee found two serious problems of credit and attribution: Kitamura's critical-branching observation was uncredited, and the verification wording could be read as referring to the human author. It also found several minor overstatements. All are corrected. Details are in note.md §10.8.
- **Round 3 (2026-10-12 and 2026-10-20/21):** the round-3 gate and track instances ran on **Claude Fable 5.1** (Anthropic), according to the workflow configuration; rounds 1 and 2 ran on Claude Opus 5.5. The gates and track T4 ran on 2026-10-12; after a budget interruption the other tracks ran on 2026-10-20 and 2026-10-21. The lead-author instance that compiled note.md §11 reports its own model as Claude Opus 5.5 (note.md §11.0). The workflow had seven research tracks, a lead-author AI instance, three referee agents, sixteen targeted refutation agents, a revision and an AI re-check of the revision. Wherever the note says "the lead" in round 3, it means that AI instance, not the human author.
- **Referee outcome (round 3):** no fatal error. Two serious errors (an overstated reduction to H′(p), and a false Consequence after Theorem 11.45) and 12 minor ones, mostly constants rounded the wrong way. All are corrected or withdrawn. No proof of a result labelled [proved] was refuted. The lead-author instance's own check had missed both serious errors. Details are in note.md §11.9.
- **No human referee** has checked any part of this. Treat it as an unrefereed preprint, and check whatever you intend to rely on. Corrections are welcome (open an issue).

## License

- Code (`code/`, including `code/round2/` and `code/round3/`, and `review/`, and the referee programs in `data/round3/review/`): [MIT](LICENSE).
- Documents (`README.md`, `note.md`, `archive/README.md`, `review/README.md`, `code/round2/README.md`, `data/round2/README.md`, `code/round3/README.md`, `data/round3/README.md`) and logs and data (`code/outputs/`, `archive/`, `data/`): [CC BY 4.0](LICENSE-docs.md).

Both are copyright © 2026 Nathan Durfee. The problem statement is from erdosproblems.com (T. F. Bloom) and Erdős–Graham (1980).
