# Erdős Problem #404: structure, finiteness families and certified lower bounds

This repository is a research note on [Erdős Problem #404](https://www.erdosproblems.com/404) (sums of distinct factorials divisible by high prime powers), with the code, logs and data behind it.

**All three questions of Problem #404 remain open.** Nothing here proves that $f(a,p)=\infty$ for any pair $(a,p)$, or that $f(a,p)<\infty$ for every $a$. The note proves some structural results, certifies much larger lower bounds than were previously published, and isolates a precise statement that would settle question (Q3).

The full write-up is [`note.md`](note.md). **The mathematics, code and text were produced by AI** (see [AI disclosure](#ai-disclosure-and-authorship)). No human has verified the mathematics; three AI referees have checked it (note.md §9).

## The problem

For a prime $p$ and an integer $a\ge1$, let $f(a,p)$ be the largest $k$ such that $p^k$ divides $a_1!+a_2!+\dots+a_n!$ for some $a=a_1<a_2<\dots<a_n$ (or $\infty$ if there is no largest). Erdős and Graham (1980) asked:

- **(Q1)** For which $a$ and $p$ is $f(a,p)$ finite?
- **(Q2)** How does $f(a,p)$ behave?
- **(Q3)** Is there a prime $p$ and an infinite sequence $a_1<a_2<\cdots$ such that the exact power of $p$ dividing $\sum_{i\le k}a_i!$ tends to infinity?

Known before this note: $f(2,2)=254$ (S. Lin), the trivial family $a\equiv-1 \pmod p$ (where $f(a,p)=v_p(a!)$), Tao's block lemma, and K. Kitamura's extensive computations (exact values of $f(a,2)$ for $a\le256$ and deeper rows, a certified classification of all $p=2$ classes with excess $\le24$, and witnesses $f(1,p)\ge20000$ for $p=3,5,7$ and $\ge5000$ for $p=11,13$).

Write $f(a,p)=v_p(a!)+g_p(a)$. The excess $g_p$ extends to a function on the $p$-adic integers (this normal form is Kitamura's; see below).

## What is new

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

## What is computed (computer-assisted)

| Result | How | Checked by |
|---|---|---|
| $f(1,3)\ge2\,000\,001$, $f(1,5)\ge10^6$, $f(1,7)\ge10^6$ | explicit witness lists (1.4–1.6 million terms; `archive/witnesses/`) | two independent verifiers each |
| $f(1,13)\ge67\,977\,552$ | $\mathrm{Cov}$ certificates for all depths $t\le7$ | `cov.c` + an independent checker; also the computational referee |
| $f(1,11)\ge21\,435\,880$ | $\mathrm{Cov}$ certificates for $t\le6$ plus the ten depth-7 positions $11^7K''$ (found during refereeing) | the referee's `rcover.c` and our `cov_pos.c` |
| $f(a,7)\ge960\,792$ for $a=2,3,5$ | as above, with the six depth-7 positions $7^7K''$ | `cov_pos.c` and `rcover.c` |
| every $a\le1000$: either $f(a,13)-v_{13}(a!)\in\{0,1\}$ or $f(a,13)\ge67\,977\,552$; similarly $\{0,1\}$ / $21\,435\,880$ at $p=11$ and $\le3$ / $960\,792$ at $p=7$ | certificates + exact small-$a$ landscapes | landscapes: archived run + the computational referee's independent DP |
| $f(1,p)\ge25\,646\,163$ ($p=17$), $49\,659\,537$ (19), $154\,764\,790$ (23), $616\,067\,009$ (29), $917\,087\,135$ (31) | Theorem 3.9(c) + certified two-block windows | re-run; windows re-checked by both referees |
| $f(1,p)\ge p+\dots+p^6$ for $37\le p\le53$ (e.g. $2.26\cdot10^{10}$ at $p=53$); $\ge p+\dots+p^5$ for $59\le p\le97$ | Theorem 3.9(c) alone (covering depth of $\{(-1)^u/u!\}$) | archived run; re-checked by the computational referee (and by the logic referee for $p\le53$) |
| $f(a,2)<\infty$ on density $\ge0.8866$ ($G=29$; three programs) and $\ge0.8984$ ($G=32$; two programs). Kitamura's census already gave $0.8734$ | exact class census | see note.md §4.7 |
| $f(a,p)<\infty$ on density $\ge0.6367$ ($p=3$), $0.4784$ (5), $0.3761$ (7), $0.3002$ (11), $0.2455$ (13): the first such densities at odd primes beyond $a\equiv-1$ | exact class census | archived/re-run + the computational referee |
| $\mathrm{Cov}(5,5,H)$ fails for every $H\le38$ | explicit failing class for each $H$ | `cov_pos.c` / `cov.c` and `rcover.c` |

Two frontier results in note.md §4.5 ($f(3,5)\ge117\,499$ and $f(a,3)\ge50$ for 11 small $a$) rest on a single implementation and are flagged there.

## What is conjectural

These are **not** proved; see note.md §5–6.
- $f(a,2)<\infty$ for every $a$ (Conjecture 5.1); the weaker $\mu(K_2)=0$. Evidence: exact densities to $G=32$ and Monte Carlo to $G=254$.
- $\mu(K_p)>0$ for every odd $p$ (Conjecture 5.2); numerically $\mu(K_3)\approx0.36$, $\mu(K_5)\approx0.52$, $\mu(K_7)\approx0.62$.
- $\mathrm{UC}(p)$ for $p\ge7$ (Conjecture 5.3), which would give $f(1,p)=\infty$ and answer Q3 positively. Certified for depths $t\le7$ at $p=13$; the "missing lemma" for $t\ge8$ is stated precisely in §6.
- The Fourier and branching-process heuristics of §5.

## Prior work and credit

- **P. Erdős and R. L. Graham** posed the problem (1980).
- **S. Lin** proved $f(2,2)=254$ (Bell Labs memorandum, cited on erdosproblems.com).
- **V. Kovač** corrected the problem statement on the forum (13 Aug 2025).
- **T. Tao** (forum, 29 Sep 2025) stated the block lemma and proposed the programme of position-independent finite computations at each depth. Theorems 3.9 and 3.12 carry that programme out.
- **K. Kitamura** ([`KitaKen1/erdos-404-p2-landscape`](https://github.com/KitaKen1/erdos-404-p2-landscape), [`KitaKen1/erdos-404-odd-prime-landscape`](https://github.com/KitaKen1/erdos-404-odd-prime-landscape), July 2026) introduced the normal form $g=f-v_p(a!)$ at $p=2$ and proved its determinacy (our Theorem 3.1(a) at $p=2$). He also found the cube identity and the shadow family $2^t-2$, computed the exact values ($f(34,2)=18444$ and others), and gave the certified classification of $p=2$ classes with $g\le24$. From that classification come the $p=2$ value set ($g\ne1,2,4,5$; $g=3$ iff $a\equiv4 \pmod 8$) and the density $0.8734$. He stated the sibling-pairing theorem and built the first large odd-prime witnesses. This note re-derives several of his statements and credits them throughout.
- **Earlier AI write-ups** already contained the compactness equivalence "Q3 iff some $f(a,p)=\infty$": `neelsomani/gpt-erdos` (2026-01-17), `erichou1/erdos-open-problems` (2026-06-10) and `AItoBit/Erdosproblems-llm-hunter` (2026-09-25).
- **AItoBit** opened google-deepmind/formal-conjectures PR #6936 (statement only).
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

## Repository layout

```
README.md            this file
note.md              the research note (statements, proofs, computations, verification summary)
code/                programs of the six research tracks (A-F), the independent oracle, Lean files, build/run scripts
code/outputs/        logs of the 2026-10-08 re-runs (pub_* = publication re-checks R19-R21)
archive/             archived logs that the "not re-run" items rest on; gzipped witnesses for p = 3, 5, 7
review/              the referees' own programs and outputs
LICENSE              MIT (code)
LICENSE-docs.md      CC BY 4.0 (documents)
CITATION.cff
```

## AI disclosure and authorship

- **Author:** Nathan Durfee, as composer and prompter. He chose the problem and directed the work. He has **not** personally verified the mathematics.
- **Mathematics, code and text:** produced by Claude (Anthropic, model Claude Opus 5.5), running as a multi-agent workflow in Claude Code. The workflow had five stages:
  1. literature and community "gate" agents;
  2. six parallel research tracks;
  3. a lead-author agent that cross-checked the tracks, wrote an independent oracle and re-ran the computations;
  4. three separate referee agents (logic, computation, novelty);
  5. a revision that applied every referee correction and re-checked the new computations.
- **Referee outcome:** no fatal or serious mathematical error was found. The novelty referee found that the first draft overstated novelty and under-credited Kitamura and earlier AI write-ups; this is corrected. The computational referee contributed the depth-7 improvements, which we re-checked with separate code. Details are in note.md §9.
- **No human referee** has checked any part of this. Treat it as an unrefereed preprint, and check whatever you intend to rely on. Corrections are welcome (open an issue).

## License

- Code (`code/`, `review/`): [MIT](LICENSE).
- Documents (`README.md`, `note.md`, `archive/README.md`, `review/README.md`) and logs and data (`code/outputs/`, `archive/`): [CC BY 4.0](LICENSE-docs.md).

Both are copyright © 2026 Nathan Durfee. The problem statement is from erdosproblems.com (T. F. Bloom) and Erdős–Graham (1980).
