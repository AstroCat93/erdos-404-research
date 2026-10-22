# Round 4 referee report: NOVELTY AND CREDIT (note.md §12 and the [Round 4] edits), 2026-10-14

**Scope.** This report covers novelty, priority, credit and verification wording for revision 4 of note.md. That means §12 in full and the "[Round 4]" edits in the header and status lines, §0 (items 24–25), §5 (Conjecture 5.2), §11 (lines 1875, 2029, 2147) and README.md (lines 11, 34–41, 246).

**Sources read.**
- note.md: the header, §§0, 2, 4.6–4.8, 5, 8, 11.3, 11.6, 11.8, 12 and the References.
- README.md.
- `data/round4/BRIEF.md`.
- The track reports `data/round4/reports/M4{A,B,C,D}.md`.
- The verifier reports `data/round4/checks/*.md`, with most care on M4A_obstruction, M4C_logic, M4C_falsify, M4C_obstruction and M4D_P.
- `data/round3/reports/R3M.md` (§§5, 10) and `data/round3/checks/R3M.md`.
- The round-3 novelty report `data/round3/referees/novelty.md`, which gives the baseline for the public-record check.

Everything fetched from outside the repository was treated as data. No script from an outside repository was executed.

This report was written by an AI referee instance. It is not a human review.

**Files written.** This report, plus code in `code/round4/referee_novelty/`:
- `arxiv_batch.py`: an arXiv API batch query helper. Its query lists are `queries.txt`, `queries_rerun.txt` and `queries_extra.txt`.
- `qconst_small.py`: exact $q_1(p)$ and $q_2(p)$ for $3\le p\le23$, plus subset-sum counts used for an OEIS look-up.
- `kitamura_check.py`: the arithmetic behind N1. It reads, and never executes, a clone of Kitamura's odd-prime repository.

Scratch and logs are in `/tmp/r4_ref_novelty/`. **Compute:** under 3 core-minutes. Everything ran under `nice -n 10`, and the longest job took under 1 s of CPU. Nothing in the repository was edited, and git was used only on read-only clones of public repositories in `/tmp/r4_ref_novelty/`.

## Verdict

**There is no fatal finding. There is one serious credit finding and twelve minor findings.**

**Public record.** As of 2026-10-14 04:36 UTC, nothing new on #404 has appeared since round 3 (§1).
- The problem page, the forum, Kitamura's two repositories, teorth/erdosproblems and formal-conjectures PR #6936 are unchanged.
- The arXiv index (complete to 13 Oct 2026) and GitHub have nothing new.

**No precursor found** in the public record (§2) for any of the following:
- positive Haar measure of the cancellation set of a random $p$-adic series, or of the set where $0$ is a subsum of $\{\pi_j(x)\}$;
- anti-concentration of signed subset sums of $\{r!\bmod p\}$ or of $(r!,r!H_r)\bmod p$;
- the constants $q_s(p)$ (the corresponding counts are not in OEIS);
- a reduction of a fine-scale $L^2$ mass to high-slope signed paths.

So Theorem 12.1, and the two mechanisms of §12.1 as applied here, are new relative to the public record that I could search.

**The serious finding (N1).** Theorem 12.1 is presented as proving Conjecture 5.2. The note nowhere credits the public precursor of that conjecture at odd primes. Kitamura's odd-prime repository (commit `ef0881bb`, 8 Jul 2026) contains three relevant items:
- it describes odd primes as supercritical ("ignite into the supercritical saturation regime");
- it states the **same per-block branching margin** as the note's heuristic H1, $p\log_p2-p/(p-1)$, with "+0.39 for p=3, +0.90 for p=5". This is H1's $p\log2-\tfrac{p}{p-1}\log p$ divided by $\log p$; I checked the identity to four decimals;
- it publishes "ignited" fractions (36.7%, 53.7%, 63.3%, 71%, 76% at $p=3,5,7,11,13$) that track the note's numerical $\mu(K_p)$ to within 0.02.

This is the odd-prime twin of the omission that the round-2 novelty referee rated serious at $p=2$ (Kitamura's critical-branching picture).

**The minor findings** (§3, N2–N13) fall into five groups:
- **Overstated independence and novelty wording** (N2, N3). One example is "two new lemmas found independently by two tracks". The track's own account, the shared brief, the file timestamps and the classical background (Hensel/Igusa root counts, the $p$-adic Kac–Rice formula, Littlewood–Offord) all call for more careful wording.
- **The literature status of AC($p$)** (N4). Here the logic of "even equidistribution … is open" runs the wrong way, and a caveat present in the sources was dropped.
- **A conflated citation** (N5): Garaev–Luca–Shparlinski.
- **Verification-extent and arithmetic-type wording** (N6–N9).
- **Gaps in the §12.7 credit list, the missing round-4 status check, the missing §8 disclosure paragraph, and one older credit omission** (N10–N13).

**Human verification.** No wording reads as human verification (§6).

---

## 1. Public-record check (all times UTC, 2026-10-14)

| source | how | time | result |
|---|---|---|---|
| https://www.erdosproblems.com/404 | curl | 04:14:41 | **Unchanged.** "This page was last edited 29 September 2025." Comments (7), proof claims (0), "No proof expositions yet". Reactions unchanged: likes Woett, Sky-Yang, Alfaiz; "Open to collaboration Woett"; "Currently working on Sky-Yang" (undated). |
| https://www.erdosproblems.com/forum/thread/404 | curl | 04:14:42 | **Unchanged:** 7 comments, in order Kovač ×2 and Bloom (13 Aug 2025), Tao ×2 (29 Sep 2025), Kitamura (7 Jul 2026 23:11 and 8 Jul 2026 01:58). "The ability to post new comments has been suspended." Tao's first comment says of $f(1,5)$ that "there is a combinatorial explosion of possible cases" (used in N1). |
| github.com/KitaKen1/erdos-404-p2-landscape | `git ls-remote` | 04:14:57 | HEAD `32697193`, unchanged since round 3. |
| github.com/KitaKen1/erdos-404-odd-prime-landscape | `git ls-remote`; full clone (2 commits); WebFetch of issue #1 | 04:14:57; ≈04:31; ≈04:16 | HEAD `ef0881bb` (2026-07-08 10:54 +0900), unchanged. Issue #1 (opened by AstroCat93, 12 Oct, signed by the human author of this project) has no reply visible to a logged-out reader. The README "Ignition layer" table and the docstrings of `scripts/p_general_dp.py` and `scripts/ignition_scan.py` are the source of N1 and N13 (sha256 `3cbf0067…` and `3c92c734…`, the latter equal to S0's recorded hash). |
| github.com/teorth/erdosproblems | `git ls-remote` | 04:14:57 | HEAD `86c3dc3e`, the same commit as the round-3 check, so #404 is still `state: "open"` and unformalised. |
| google-deepmind/formal-conjectures PR #6936 | `git ls-remote refs/pull/6936/*`; WebFetch of the PR page | 04:14:58; ≈04:15 | Head still `205ea70`. Open and not merged. Its 2 commits and its reviews (bocowgill approved 9 and 11 Oct; Paul-Lez commented 10 Oct) are unchanged. `main` is still `e47a327f`, with no `404.lean`. |
| plasma-ai/erdos (wiki) | `git ls-remote`; blobless shallow clone | 04:15:49 | HEAD `2fccbe67` (2026-10-13 19:42 −0600). The #404 pages changed only editorially after `4e4895c8`: `42103d16` adds "S. Lin" as author of the Lin claim page, and `2092633f` renames "the site". The status is still open, with no new claim. |
| grandchallenge/MATH-PROGRAMME issue #1674 | WebFetch | ≈04:16 | Unchanged since round 3: one comment (fyremael, 13 Oct) with trivial arithmetic. Its instructions to automated workers were not acted on. |
| arXiv API | `arxiv_batch.py` (logs `arxiv_batch_run{1,2,3}.log`) | 04:16–04:36 | The index is complete to submissions of **2026-10-13** (`cat:math.NT`, newest 2610.18503). There is nothing on #404, on $v_p$ of sums of distinct factorials, or on positive measure of $p$-adic subsum or zero sets. The full queries and counts are in §7. Relevant hits are listed in §2. |
| GitHub search | GitHub MCP | ≈04:16–04:30 | Repositories `erdos 404 pushed:>=2026-10-13`: **0**. `erdos factorials pushed:>=2026-10-13`: 0. All `erdos 404` repositories: 6, none with an update date after 2026-10-12 in the search metadata. They are this project's AstroCat93/erdos-404-research (updated 12 Oct), Kitamura's two repositories, two vibemathing templates and one unrelated (JSP-404/Erdős 504) repository. Code `"distinct factorials" "Haar measure"`: 0. Code `"distinct factorials" supercritical`: 0. Code `"sums of distinct factorials" p-adic`: 4 hits, all on Problem 1108. |
| Earlier AI write-ups | curl / sparse clone | 04:30–04:32 | erichou1 `solution_404.md`, neelsomani `candidate_solution.md`, and AItoBit's three `404.tex` files (now under `attacks/open_problems/…`, HEAD `2e1c8307`) contain no measure or supercriticality statement. AItoBit's "finite branching" is König's lemma. |
| OEIS | JSON search | 04:27:05–04:27:17 | No entry for the subset-sum counts $N_0(p)$ (3, 5, 16, 177, 630, 7712, 27603, 364750), for $\sum_zN_z^2$ (22, 212, 2374, 381848, …), or for the numerators of $q_1(p)$ (8309, 525041, 33555171). |
| Web search | WebSearch | 04:16–04:36 | "Erdős problem 404" 2026: nothing beyond erdosproblems.com. The searches on the topics of §2 are listed there. |

**Conclusion.** No prior or concurrent public work proves or claims positive measure of $K_p$, and none states the round-4 lemmas. The only ongoing activity visible is the undated "Currently working on: Sky-Yang" reaction on the problem page (N11).

---

## 2. Prior and concurrent work on the requested topics

### 2.1 Positive Haar measure of the zero or cancellation set of random $p$-adic series, or of subset sums of factorials
- **Nothing found.** The nearest work is on zeros of random $p$-adic polynomials with Haar-random coefficients:
  - S. N. Evans, *The expected number of zeros of a random system of p-adic polynomials*, Electron. Commun. Probab. 11 (2006), arXiv:math/0602478. This is the $p$-adic co-area or Kac–Rice formula.
  - X. Caruso, *Where are the zeroes of a random p-adic polynomial?*, arXiv:2110.03942.
  - Bhargava–Cremona–Fisher–Gajović, arXiv:2101.09590.
  - arXiv:2608.06576 (2026).

  In all of these the randomness is in the coefficients. Here the coefficients $\pi_j(x)$ are fixed polynomials and $x$ is random, so none of them implies or anticipates Theorem 12.1.
- **Achievement sets.** The literature on real achievement sets (Guthrie–Nymann; arXiv:2512.17285, already cited; Marchwicki–Vlasák arXiv:1802.10535; Nowakowski arXiv:2512.17761) has no $p$-adic analogue.
- **arXiv.** `abs:"random p-adic" AND abs:series` gives 0 hits; `abs:"p-adic" AND abs:"Cantor set" AND abs:"positive measure"` gives 0.

### 2.2 Survival of supercritical BPRE with dependent offspring via second moments
- **Nothing found on survival via second moments with offspring dependence of the kind in Proposition 11.11**, where all offspring counts are functions of one uniform digit.
- **The classical templates.**
  - Lyons, Comm. Math. Phys. 125 (1989): quasi-independent percolation.
  - Lyons, Ann. Probab. 18 (1990) and 20 (1992): already cited.
  - Mathieu–Temmel, arXiv:1103.1291: already cited.
  - Pemantle, *Sharpness of second moment criteria for branching and tree-indexed processes*, arXiv:math/0404090. This covers second-moment survival criteria in varying environments, with Agresti (1975) as the precursor.
- **Recent BPRE work** found by arXiv `abs:"branching process" AND abs:"random environment" AND abs:"dependent"` (18 hits) concerns joint environments or immigration, not this setting. Examples are arXiv:2606.08115 and arXiv:2601.14655.
- §11's existing citations are adequate. Pemantle's paper is optional background.

### 2.3 Anti-concentration or equidistribution of signed subset sums of $r!\bmod p$ or of $(r!,r!H_r)\bmod p$ (the constants $q_s(p)$)
- **Nothing on subset sums, signed or unsigned, of $\{r!\}_{r<p}$ modulo $p$ or $p^2$.** Nothing on the pair $(r!,r!H_r)=(r!,|s(r+1,2)|)$ either.
- **What is known about $\{n!\bmod p\}$ is very little:**
  - **Garaev–Luca–Shparlinski, *Exponential sums and congruences with factorials*,** J. reine angew. Math. 584 (2005) 29–44, arXiv:math/0403424. I extracted the text of the arXiv PDF (`/tmp/r4_ref_novelty/gls/gls.txt`). Its introduction says: "Very little seems to be known, or even conjectured, about the distribution of n! modulo p." On the single sums $S_a(L,N)=\sum e(an!)$ it says: "Although we have not been able to obtain 'individual' bounds for these sums, we obtain various bounds 'on average'."
  - Garaev–Luca–Shparlinski, *Character sums and congruences with n!*, Trans. Amer. Math. Soc. 356 (2004) 5089–5102, arXiv:math/0403422. This covers multiplicative characters. The note's reference list conflates these two papers (N5).
  - **Erdős Problem #478** ([ErGr80, p. 96]; erdosproblems.com/478, fetched 04:33:27, last edited 12 Apr 2026) asks whether $|A_p|\sim(1-1/e)p$ for $A_p=\{k!\bmod p\}$. It records the best lower bound $(\sqrt2-o(1))\sqrt p$ (Grebennikov–Sagdeev–Semchankau–Vasilevskii, Rev. Mat. Iberoam. 2024, arXiv:2204.01153). It also records Klurman–Munsch, the socialist-prime problem (Rokowska–Schinzel; Trudgian; Andrejić–Tatarevic) and Guy F11.
  - **New since the note's sources.** X. Hu, arXiv:2608.01781 (3 Aug 2026, unrefereed), claims $|A_p|\gg p^{8/15}$, and arXiv:2609.05652 (4 Sep 2026) generalises it. This supersedes M4C §9.3's "the known lower bounds for the number of distinct values are of order $\sqrt p$" (N4).
  - V. M. Abramov, arXiv:2604.26429 (v7, Sep 2026, unrefereed) claims there are no socialist primes $p>5$. This is tangential.
- **Sums of factorials modulo $p$, with repetitions allowed.**
  - Garaev–Luca–Shparlinski, *Waring problem with factorials*, Bull. Austral. Math. Soc. (2005).
  - The Crelle paper above: every residue is $m!n!+n_1!+\dots+n_{47\text{ or }49}!$.
  - Garaev–Pardo, arXiv:2508.12127 (2025).

  None concerns *distinct* factorials or anti-concentration.
- **Conclusion.** AC($p$) (M4C §9.2) and the constants $q_s(p)$ are not in the literature I found. AC($p$) is *implied by* equidistribution of the dilates of $\{r!\bmod p\}$, but it is much weaker (N4). The note's statement "even equidistribution of $\{r!\bmod p\}$ is open" is true, and is supported by the GLS sentence quoted above. But it is no evidence that AC($p$) is out of reach.
- **Independent arithmetic.** `qconst_small.py` (exact rationals; log `qconst_small.log`) reproduces every value quoted in §12.1:
  - $q_1(7)=8309/8192$ and $q_2(7)=4557/4096$;
  - $q_1-1=2.202\cdot10^{-5}$ and $q_2-1=8.124\cdot10^{-3}$ at $p=13$;
  - $q_1-1=5.423\cdot10^{-9}$ and $q_2-1=2.263\cdot10^{-6}$ at $p=23$;
  - $q_2(11)=1165593/1048576$, which equals the M4C falsification verifier's exact value.

  It also checks the identity $q_1(p)=p\sum_zN_z^2/4^p$.

### 2.4 Hensel-ball arguments for densities of polynomial images
- **The count behind M4A's Lemma H, M4C's Lemma H2 and M4B's Lemma B3 (note Lemma 12.8) is classical.** Near a simple root $\rho$ of $F$ with $v(F'(\rho))=\lambda$, $\{v(F)\ge k\}$ is the ball $\rho+p^{k-\lambda}\mathbb Z_p$, so $p^k\mu\{\cdots\}=p^\lambda$ is independent of $k>2\lambda$.
  - This is the stabilisation of root counts modulo $p^k$ that underlies Igusa's Poincaré series in one variable (J.-I. Igusa, *An introduction to the theory of local zeta functions*, AMS/IP 2000; for the algorithmic univariate case, Dwivedi–Saxena, arXiv:2006.08926).
  - It is also the $p$-adic co-area or Kac–Rice computation of Evans (2006) and Caruso (2021).
- No paper applies it to an $L^2$ band mass of subset-sum laws.
- arXiv: `abs:"Hensel" AND abs:"Haar measure" AND abs:polynomial` gives 0; `abs:"image of a polynomial" AND abs:"p-adic" AND abs:density` gives 0; `abs:"Igusa" AND abs:"Poincare series" AND abs:"Hensel"` gives 0.
- **Conclusion.** The *mechanism* is classical and should be cited (N3). Its *use*, reducing $\mathbb E_B[\varepsilon]$ to the high-slope signed mass on frozen-gate balls, has no precursor that I found.

### 2.5 Value–derivative anti-concentration
- Controlling near-double roots through the joint law of $(P(x),P'(x))$, together with Littlewood–Offord-type bounds, is the strategy of:
  - Peled–Sen–Zeitouni, *Double roots of random Littlewood polynomials*, Israel J. Math. (2016), arXiv:1409.2034;
  - Feldheim–Sen, Electron. J. Probab. 22 (2017).

  Both work over $\mathbb Z$ and $\mathbb C$, with Sárközy–Szemerédi-type bounds, not modulo $p^k$.
- Lemma Q's block structure (a depth-1 gate converting the derivative digit into a second-digit constraint on the previous block) has no precursor that I found. Background credit is optional (N3).

### 2.6 Kitamura's odd-prime repository (July 2026)
**What it contains.** Commit `ef0881bb`, 2026-07-08. The excerpts below are verbatim; `kitamura_check.py` prints them with line numbers.
- `scripts/p_general_dp.py` l.17–21: "Tao's base-5 comments predict exactly this mechanism for p=5; the branching heuristic (p log_p 2 - p/(p-1) extra digits per block: +0.39 for p=3, +0.90 for p=5) predicts sigma(K) grows linearly …".
- `scripts/ignition_scan.py` l.10–23: "active starts either die at TINY normalized depth (ignition failure, g <= ~7 in all known cases) or ignite into the supercritical saturation regime (g >= 1000 by explicit witness) … A bounded B(p) would make the sharpened Tao conjecture decidable-in-principle for each a: g(a,p) <= B(p) or g(a,p) = infinity."
- `README.md` l.238–248 ("Ignition layer"). The "ignited candidates" counts are 733 of $a\le2000$ ($p=3$) and 161, 190, 213, 229 of $a\le300$ ($p=5,7,11,13$), "It is not a proof that `f(a,p)` is infinite".

**What the note credits.**
- §4.6 (l.712) and §4.8 (l.755) mention the ignited fractions.
- The note **never** credits the supercritical heuristic or the margin formula.
- It never links either to Conjecture 5.2.

**Arithmetic** (`kitamura_check.log`):

| $p$ | Kitamura's margin | H1 / $\log p$ | ignited / scanned | note's $\mu(K_p)$ |
|---|---|---|---|---|
| 3 | +0.3928 | +0.3928 | 733/2000 = 0.3665 | 0.36 |
| 5 | +0.9034 | +0.9034 | 161/300 = 0.5367 | 0.5216 |
| 7 | +1.3268 | +1.3268 | 190/300 = 0.6333 | 0.6239 |
| 11 | +2.0797 | +2.0797 | 213/300 = 0.7100 | 0.6998 |
| 13 | +2.4298 | +2.4298 | 229/300 = 0.7633 | 0.7545 |

### 2.7 Timeline of tracks M4A and M4C (for N2)
These are file modification times in the shared workspace (`ls --time-style=full-iso`), together with M4C's logged start times.

**M4A, 13 Oct:**
- `lemma_q_check.py` 23:17:36; `lemma_q_check.log` 23:19:26;
- `hensel_identity.log` 23:13:25;
- `fe_verify_final.log` 23:40:44;
- last log 23:46:37.

**M4C:**
- `test_H2.py` 23:46:54 on 13 Oct;
- `test_Q.py` **00:00:28** on 14 Oct;
- the first `test_Q.log` run started **00:24:27** on 14 Oct;
- `assemble.log` 00:48 on 14 Oct.

**M4B:** the report `M4B.md` 23:26 on 13 Oct. Its Lemma B3 (note Lemma 12.8) is a third Hensel-ball conservation statement.

**What the timestamps show.** M4A's Lemma Q and Hensel identity were tested and logged in the shared workspace before M4C's Lemma Q test code existed. This neither confirms nor refutes M4C's statement that it saw "only [M4A's] headline, after our Lemmas H2, Q and P were written and tested" (M4C §14).

---

## 3. Findings

### N1 [serious] (missing credit): the public precursor of Conjecture 5.2 at odd primes is uncredited where the conjecture is stated and where Theorem 12.1 claims to prove it

**Where.**
- §5, H1 (l.764): "- *Branching model.* The carry recursion of §1.4 is a branching process in a random environment. Its quenched mean log-offspring per block is $p\log2-\tfrac{p}{p-1}\log p$: zero at $p=2$ and positive for $p\ge3$. Offspring are correlated, so this is not a proof."
- §5, H1 credit (l.765): "- **[Round 2] Credit.** At $p=2$ the critical-branching picture, and the observation that the surviving fraction decays to $0$, are already in Kitamura's July 2026 repository (§2). Round 1 did not credit this."
- §5, Conjecture 5.2 (l.780) and its [Round 4] line (l.784): "> **[Round 4]** Proved for every prime $7\le p\le97$ (Theorem 12.1; computer-assisted; AI-verified, not human-refereed). Still open at $p=3,5$ and for $p>97$."
- §12.0 (l.2266): "This proves the cases $7\le p\le97$ of Conjecture 5.2 (computer-assisted, AI-verified, not human-refereed). The conjecture remains open at $p=3,5$ and for $p>97$."
- §12.7 *Credit* (l.2419–2426): Kitamura is not named.
- README l.11: "This proves Conjecture 5.2 for these primes. It is a measure statement and says nothing about Q3."

**Problem.** §2.6 shows that, in July 2026, Kitamura's odd-prime repository publicly contained three things:
- (i) the supercritical branching heuristic at odd primes, with **exactly** H1's per-block margin (in base $p$);
- (ii) the description of surviving starts as entering "the supercritical saturation regime";
- (iii) measured surviving ("ignited") fractions that agree with the note's $\mu(K_p)$ to within 0.02.

Conjecture 5.2 is the Haar-measure form of that picture. The note's only credit is that the ignited fractions "match $\delta_G(p)$" (§4.8). Tao's forum remark on $f(1,5)$ ("a combinatorial explosion of possible cases") is the informal origin, and §5 already labels the count "Tao's count".

Round 2's novelty referee rated the same omission at $p=2$ (Kitamura's critical branching) as serious. Round 4 now advertises a proof of the odd-prime conjecture in the header, §0, §12 and the README, so the precursor must be credited there. The formulation as a Haar-measure statement, the numerics, and of course the proof remain the note's.

**Fix.**
1. §5, insert after l.765:
   "- **[Round 4] Credit (odd $p$).** The supercritical side of this picture is also already public. Kitamura's odd-prime repository (`KitaKen1/erdos-404-odd-prime-landscape`, commit `ef0881bb`, 8 Jul 2026) states 'the branching heuristic (p log_p 2 - p/(p-1) extra digits per block: +0.39 for p=3, +0.90 for p=5)' (`scripts/p_general_dp.py`). This is the quenched mean log-offspring above, divided by $\log p$. The repository describes surviving starts as igniting 'into the supercritical saturation regime' (`scripts/ignition_scan.py`). Its README's 'ignited candidates' (733 of $a\le2000$ at $p=3$; 161, 190, 213 and 229 of $a\le300$ at $p=5,7,11,13$) are the surviving fractions of §4.8. Round 1 did not credit this."
2. §5, after the [Round 4] line under Conjecture 5.2 (l.784), add:
   "*Credit.* The heuristic behind this conjecture (supercriticality at odd $p$; H1) and its empirical support at the integers (the 'ignited' fractions, §4.8) are Kitamura's (July 2026). Tao's remark of 29 Sep 2025 that for $f(1,5)$ 'there is a combinatorial explosion of possible cases' is the informal starting point. The formulation as a statement about Haar measure, and the numerical values of $\mu(K_p)$ above, are round 1's."
3. §12.0 l.2266: replace "This proves the cases $7\le p\le97$ of Conjecture 5.2 (computer-assisted, AI-verified, not human-refereed)." with
   "This proves the cases $7\le p\le97$ of Conjecture 5.2 (computer-assisted, AI-verified, not human-refereed), round 1's Haar-measure form of the supercritical picture that Kitamura described and measured at odd primes in July 2026 (§5, H1)."
4. §12.7 *Credit*, add as the first bullet:
   "- Kitamura (July 2026, `KitaKen1/erdos-404-odd-prime-landscape`): the supercritical branching heuristic at odd primes, with the per-block margin $p\log_p2-p/(p-1)$ of H1, and the measured 'ignited' fractions. Conjecture 5.2, proved here for $7\le p\le97$, is the Haar-measure form of that picture. Tao (forum, 29 Sep 2025): the 'combinatorial explosion' remark on $f(1,5)$."
5. README l.11: after "This proves Conjecture 5.2 for these primes." insert
   "Conjecture 5.2 is the Haar-measure form of the supercritical picture already described and measured at odd primes in K. Kitamura's odd-prime repository (July 2026)."
6. References, add:
   "- [Round 4] K. Kitamura, `github.com/KitaKen1/erdos-404-odd-prime-landscape`: `README.md` ('Ignition layer'), `scripts/p_general_dp.py` and `scripts/ignition_scan.py` (branching heuristic; supercritical 'ignition'), commit `ef0881bb` (2026-07-08); re-read 2026-10-14."
7. Optional, §4.8 l.755: append "They are the empirical precursor of Conjecture 5.2 (§5)."

### N2 [minor] (overstated independence; priority): "found independently by two tracks"

**Where.**
- §12.1 (l.2274): "M4A and M4C found the same two new ingredients independently: the tracks ran in parallel, and M4C, which finished later, states that it neither read nor compared M4A's proofs."
- §0 item 24 (l.136): "The proofs verify the hypothesis FE of Theorem 11.14 using two new lemmas found independently by two tracks: …"
- §12.7 (l.2421): "- The Hensel reduction and the value–derivative anti-concentration lemma were found independently by tracks M4A and M4C."
- README l.39: "| §12.1 | Two new lemmas, each found independently by two tracks: …"

**Problem.** The note's paraphrase drops part of M4C's own account. M4C §14 says: "We saw only its headline, after our Lemmas H2, Q and P were written and tested, and we have not compared the proofs in detail." M4A's headline states both ingredients, including the factor $q_2/p^2$. In addition:
- **Common brief.** Both tracks worked from one brief, which pointed both at round 3's Remark C6, (S) and a deep-gate truncation.
- **Shared workspace.** Both tracks worked in one workspace, and M4A's Lemma Q and Hensel-identity tests were logged there before M4C's Lemma Q test file existed (§2.7).
- **Third track.** The Hensel-ball mechanism also appears in a third track: M4B's Lemma B3, note Lemma 12.8.

The "independence" is a self-report by an instance of the same system working from the same brief. It is reasonable to call it *separate* work. But "found independently" in the headline and README invites a stronger reading, and the priority within the project (M4A first) is not recorded.

**Fix.**
- **§12.1, replace the sentence with:** "M4A and M4C reached the same two ingredients by separate work from the same brief, which pointed both at round 3's Remark C6 (§11.3, §12.0). M4C states that it saw only M4A's headline, after its own Lemmas H2, P and Q were written and tested, and that it did not read or compare M4A's proofs. The tracks shared a workspace, and M4A's logged tests of its Lemma Q and Hensel identity (13 Oct, 23:13–23:19 UTC) precede M4C's Lemma Q code (14 Oct, 00:00 UTC). This separateness therefore rests on M4C's own account. The Hensel-ball mechanism also appears in track M4B (Lemma 12.8)."
- **§0 item 24:** replace "using two new lemmas found independently by two tracks:" with "using two lemmas, new in this setting, that two tracks reached separately from a common brief (§12.1):".
- **§12.7:** replace the bullet with: "- The Hensel reduction and the value–derivative anti-concentration lemma are due to track M4A and, separately, track M4C (§12.1 records the extent of the separation; M4A's versions were logged first). Track M4B's Lemma 12.8 is a third Hensel-ball statement."
- **README l.39:** replace "Two new lemmas, each found independently by two tracks:" with "Two lemmas, new in this setting, reached separately by two tracks from a common brief:".

### N3 [minor] (novelty wording; classical and internal background): "two new ingredients"

**Where.**
- §12.1 l.2274 ("the same two new ingredients").
- §12.1 l.2276: "The reason is that Hensel balls of a polynomial are scaled isometries: low-slope roots contribute exactly the same mass at every finer resolution, so only high-slope (near-multiple-root) paths contribute to $\varepsilon$."
- §12.1 l.2280: "**Quenched value–derivative anti-concentration [proved] (M4A Lemma Q; M4C Lemmas P and Q).**"
- §0 item 24 and README l.39 ("two new lemmas").

**Problem.**
- **(a) The Hensel count is classical.** Near a simple root, $p^k\mu\{v(F)\ge k\}$ is constant in $k>2\lambda$. This is the stabilisation of root counts modulo $p^k$ (Igusa's Poincaré series in one variable; the $p$-adic Kac–Rice formula of Evans 2006, §2.4). What is new is its use to reduce $\varepsilon$ to high-slope signed mass on frozen-gate balls.
- **(b) Lemma Q is a Littlewood–Offord-type small-ball bound.** M4A §4, Remark 3 and M4A §12 say so, but the note does not. Controlling near-double roots through the joint law of value and derivative is also the strategy of Peled–Sen–Zeitouni (§2.5).
- **(c) Internal precursors are not mentioned.** The mod-$p$ content of Lemma Q's block statistic is the pair $(r!,r!H_r)$. Up to sign and the reflection $r\mapsto p-1-r$, this is round 1's pair of "universal vectors" $((-1)^u/u!,(-1)^uH_u/u!)$ (§0 item 12; §6, T3). The identity holds by Wilson's theorem and $H_{p-1-r}\equiv H_r\pmod p$; I checked it for $p\le17$. In addition:
  - $q_1(p)-1$ is the level-1 $L^2$ shell ($\chi^2$) of a single gate block. That is the kind of quantity whose shells R3F studied as exact collision counts (Theorems 11.17–11.19; R3F A2, B3), and Proposition 11.12 bounds it below by $(p-1)4^{-p}$;
  - R3F's C2 "2D lazy walk $(\sum\delta\sigma,\sum\delta\tau)$" is the round-3 two-dimensional analogue;
  - R3Q's Lemma 8 is credited by both tracks as the 2-adic precursor of slope control.

**Fix.**
- In §12.1, after the Hensel paragraph (after "…only high-slope (near-multiple-root) paths contribute to $\varepsilon$."), add:
  "The underlying count (near a simple root $\rho$ with $v(F'(\rho))=\lambda$, $p^k\mu\{v(F)\ge k\}$ does not depend on $k$ once $k>2\lambda$) is classical. It is the stabilisation of root counts modulo $p^k$ (Igusa's Poincaré series in one variable) and the $p$-adic Kac–Rice formula of Evans (2006). What is new is its use to reduce $\varepsilon$ to high-slope signed mass on frozen-gate balls."
- After the Lemma Q paragraph, add:
  "Lemma Q is a Littlewood–Offord-type small-ball bound. Controlling near-double roots through the joint law of value and derivative is also the strategy of Peled–Sen–Zeitouni (2016) for random $\pm1$ polynomials. Modulo $p$, the block statistic involves the pair $(r!,\,r!H_r)$. Up to sign and the reflection $r\mapsto p-1-r$, this is round 1's pair of universal vectors $((-1)^u/u!,\,(-1)^uH_u/u!)$ (§0 item 12; §6). $q_1(p)-1$ is the level-1 $L^2$ shell of a gate block (R3F, §11.4; Proposition 11.12)."
- In §0 item 24 and README l.39, write "two lemmas, new in this setting," as in N2.
- Add to the References:
  - Evans, Electron. Commun. Probab. 11 (2006), arXiv:math/0602478;
  - Igusa, *An introduction to the theory of local zeta functions*, AMS/IP Stud. Adv. Math. 14 (2000);
  - P. Erdős, *On a lemma of Littlewood and Offord*, Bull. Amer. Math. Soc. 51 (1945);
  - Peled–Sen–Zeitouni, Israel J. Math. (2016), arXiv:1409.2034.

### N4 [minor] (literature status of AC($p$): the logic of "even" is reversed, the claim is uncited, and a caveat was dropped)

**Where.**
- §12.3 (l.2347): "An "all $p\ge p_0$" version reduces to a hypothesis AC($p$), uniform anti-concentration of signed subset sums of $\{r!\}$ and $\{(r!,r!H_r)\}$ modulo $p$ (and of falling factorials modulo $p^3$), which is not available: even equidistribution of $\{r!\bmod p\}$ is open."
- §12.5 (l.2375): "2. *All $p\ge7$.* The hypothesis AC($p$): uniform anti-concentration of signed factorial subset sums modulo $p$ and $p^2$, a question about the distribution of $\{r!\bmod p\}$ that is open in the literature."
- README l.41: "(needs anti-concentration of signed factorial subset sums mod $p$)".

**Problem.**
- **The direction of the logic.** AC($p$) is *implied by* equidistribution of the dilates $b\cdot\{r!\bmod p\}$, and it is much weaker. For example, $q_1(p)\le1+p^{-3}$ holds as soon as, for every $b\not\equiv0$, at least $4\log_2p$ of the residues $b\,r!$ ($r<p$) lie at distance $\ge p/4$ from $0$. Each such factor of $\prod_r\cos^2(\pi br!/p)$ is then $\le1/2$. So "even equidistribution is open" says nothing about whether AC($p$) is reachable; the word "even" suggests the opposite relation.
- **"Open in the literature" overstates.** No paper that I found poses AC($p$). The sources are more careful:
  - M4C §9.3: "We did not search the literature systematically, so this is a reported belief, not a verified claim."
  - §10.5 (l.1607): "a non-concentration statement for $\{r!\bmod p\}$ that we did not find in the literature … a limited search, to be checked by a specialist."
- **The statement is true but uncited.** The citable support is the GLS (Crelle 2005) introduction (§2.3) and Erdős Problem #478.
- **§12.5 omits $p^3$.** It drops the $p^3$ part ($q_3\le2$) of AC($p$).
- **M4C §9.3 is now out of date.** It says "the known lower bounds for the number of distinct values are of order $\sqrt p$". The best published bound is $(\sqrt2-o(1))\sqrt p$ (GSSV 2024), and an unrefereed preprint (arXiv:2608.01781, Aug 2026) claims $p^{8/15}$.

**Fix.**
- **§12.3:** replace "which is not available: even equidistribution of $\{r!\bmod p\}$ is open." with:
  "which we could not prove and did not find in the literature (searched 2026-10-14). It would follow from equidistribution of the dilates of $\{r!\bmod p\}_{r<p}$, but it is much weaker. For example, $q_1(p)\le1+p^{-3}$ holds as soon as every dilate $b\cdot\{r!\bmod p\}$, $b\not\equiv0$, has at least $4\log_2p$ elements at distance $\ge p/4$ from $0$. Little is known even so. No individual nontrivial bound for $\sum_{n<p}e(an!/p)$ is known (Garaev–Luca–Shparlinski 2005 obtain bounds only on average). Whether $|\{r!\bmod p\}|\sim(1-1/e)p$ is Erdős Problem #478, where the best published lower bound is $(\sqrt2-o(1))\sqrt p$ (Grebennikov–Sagdeev–Semchankau–Vasilevskii 2024)."
- **§12.5 item 2:** replace with:
  "2. *All $p\ge7$.* The hypothesis AC($p$): uniform anti-concentration of signed factorial subset sums modulo $p$ and $p^2$, and of falling factorials modulo $p^3$ (§12.3). We found no result that gives it. It concerns the distribution of $\{r!\bmod p\}$, about which little is known (Erdős Problem #478; Garaev–Luca–Shparlinski 2005)."
- **README l.41:** replace "(needs anti-concentration of signed factorial subset sums mod $p$)" with "(needs anti-concentration of signed factorial subset sums mod $p$, $p^2$ and $p^3$, which we did not find in the literature)".
- **M4C report §9.3, lead's note:** add "(best published lower bound $(\sqrt2-o(1))\sqrt p$, GSSV 2024; an unrefereed preprint, arXiv:2608.01781, claims $\gg p^{8/15}$)".
- **References, add:**
  - Grebennikov, Sagdeev, Semchankau, Vasilevskii, *On the sequence $n!\bmod p$*, Rev. Mat. Iberoam. (2024), arXiv:2204.01153;
  - T. F. Bloom, Erdős Problem #478, https://www.erdosproblems.com/478 (accessed 2026-10-14).

### N5 [minor] (citation): two Garaev–Luca–Shparlinski papers are conflated
- **Where.** References (l.2441): "- M. Z. Garaev, F. Luca, I. E. Shparlinski, *Character sums and congruences with n!*, J. reine angew. Math. 584 (2005), arXiv:math/0403424."
- **Problem.** These details mix two papers:
  - arXiv:math/0403424 is *Exponential sums and congruences with factorials*, J. reine angew. Math. 584 (2005) 29–44. I checked the arXiv PDF title page and the Macquarie record.
  - *Character sums and congruences with n!* is Trans. Amer. Math. Soc. 356 (2004) 5089–5102, arXiv:math/0403422.

  The error dates from round 1, but N4's fix makes the reference load-bearing for §12.
- **Fix.** Replace the entry with: "- M. Z. Garaev, F. Luca, I. E. Shparlinski, *Character sums and congruences with n!*, Trans. Amer. Math. Soc. 356 (2004) 5089–5102, arXiv:math/0403422; and *Exponential sums and congruences with factorials*, J. reine angew. Math. 584 (2005) 29–44, arXiv:math/0403424."

### N6 [minor] (verification wording): "computed exactly" and "exact arithmetic" cover floating-point recomputations
- **Where.**
  - §12.1 (l.2286–2289): "The constants were computed exactly by: … the M4C falsification verifier (a CRT dynamic program and an independent Fourier sum, plus brute force over all $3^p$ signed vectors at $p=11,13$); the M4C obstruction verifier (a Fourier positivity formula)."
  - §12.0 (l.2254): "*Verification.* Every main claim got an adversarial check from the logic lens and the numerical-falsification lens (own code, exact arithmetic)."
- **Problem.** Several of these computations were not exact:
  - The M4C obstruction verifier's $q_s$ are float64, with relative accuracy about $10^{-12}$ (`checks/M4C_obstruction.md`, S1).
  - The falsification verifier's Fourier sum is floating point ("Method 2, independent floating point").
  - The M4A verifiers recomputed phases 3–4 in mpmath at 60 digits or 320 bits, without outward rounding (`checks/M4A_falsify.md` l.140, l.256; `checks/M4A_logic.md` l.215).

  The margins make this harmless, but the wording overstates.
- **Fix.**
  - **§12.1:** replace the list with: "The constants were computed exactly (rational arithmetic) by each track (M4C by two dynamic programs, plus brute force for $p\le13$) and by the M4C falsification verifier (a CRT dynamic program, plus brute force over all $3^p$ signed vectors at $p=11,13$). They were computed in floating point (relative accuracy about $10^{-12}$) by that verifier's Fourier sum and by the M4C obstruction verifier's Fourier positivity formula. The round-4 novelty referee reproduced $q_1,q_2$ exactly for $3\le p\le23$."
  - **§12.0:** replace "(own code, exact arithmetic)" with "(own code; exact arithmetic for the lemma tests and the early phases of the certificates, and multi-precision floating point without outward rounding for some tail recomputations, whose margins are many orders of magnitude)".

### N7 [minor] (extent of verification): "every main claim of every track", "every certificate", and past-tense final referees
- **Where.**
  - §12 preamble (l.2241–2242): "> - every main claim of every track was adversarially verified by two or three separate AI instances, each using a different lens and writing its own code (`data/round4/checks/`);" and "> - a final round of AI referees checked this section (§12.7)."
  - Header l.12: "…and §12 by a final round of AI referees (§12.7)."
  - README l.34: "Every main claim was verified by two or three separate AI instances, each writing its own code and including independent recomputation of every certificate; a final round of AI referees then checked note.md §12."
  - README l.18: "Three rounds of three AI referees (logic, computation, novelty) have checked it: note.md §9 for round 1, §10.8 for round 2 and §11.8 for round 3. In round 3, each research track was also checked by a separate AI instance with its own code."
  - §12.1 (l.2297): "The shared core was checked line by line in round 3 (R3M check, round-3 logic referee) and again in round 4 (§12.7)."
- **Problem.** These statements overstate the extent of checking:
  - §12.7 itself says that Propositions 12.7 and 12.12 and Lemma 12.8 "were checked only by the track".
  - Theorem 12.11's verifier re-ran 37 of 38 certificates (`checks/M4D_P.md` l.24).
  - §12.7 still holds the placeholder `[ROUND4_REFEREE_SUMMARY]`, so the past-tense "checked" is premature (as in round 3's F3).
  - No round-4 verifier re-checked Theorem 11.14 line by line. M4A's track and M4A's logic verifier re-read C3; M4C's logic verifier "took it as given, as instructed"; M4A's falsification verifier did not re-test it. So "again in round 4 (§12.7)" is only true if the round-4 logic referee does it.
- **Fix.**
  - **l.2241:** replace with: "> - every main claim of every track (Theorems 12.2, 12.4, 12.5 and 12.9–12.11, Corollary 12.3 and Proposition 12.6) was adversarially verified by two or three separate AI instances, each using a different lens and writing its own code (`data/round4/checks/`); Propositions 12.7 and 12.12 and Lemma 12.8 were checked only by their tracks;"
  - **l.2242, header l.12 and README l.34:** keep the past tense only once the referee summary is filled and the referees' corrections are applied.
  - **README l.34:** replace "including independent recomputation of every certificate" with "including independent recomputation of every certificate of Theorem 12.1 (and of 37 of the 38 covering certificates behind Theorem 12.11)".
  - **README l.18:** replace "…and §11.8 for round 3. In round 3, each research track was also checked by a separate AI instance with its own code." with "…§11.8 for round 3 and §12.7 for round 4. In rounds 3 and 4, each research track was also checked by separate AI instances with their own code."
  - **l.2297:** replace "The shared core was checked line by line in round 3 (R3M check, round-3 logic referee) and again in round 4 (§12.7)." with "The shared core was checked line by line by AI instances in round 3 (the R3M check and the round-3 logic referee). In round 4, track M4A and the M4A logic verifier re-read the proof of Theorem 11.14, and the other verifiers took it as given." Then add one sentence on what the round-4 logic referee did (§12.7).

### N8 [minor] (accuracy and credit to the verifiers): the summary of the fixes understates them
- **Where.** §12.7 (l.2397): "No verifier found a mathematical or computational error in any main claim. All fixes concerned wording, labels, rounding direction and missing one-line justifications."
- **Problem.** The checks found more than that:
  - Both tracks' headlines claimed that no truncation was used. This was false: "uses no truncation beyond working on one atom" (M4A) and "verifies FE completely, with no truncation" (M4C).
  - M4C's far-tail remainder beyond $10^{60}$ was "asserted with an unspecified $O(\ln b)$ term" and hard-coded as $10^{-1000}$. The M4C logic verifier derived the explicit majorant (`checks/M4C_logic.md` F1, §8). That is a gap filled by a verifier, not a one-line justification.
  - A displayed inequality of M4C §4.2 "is false as written when $e_i<3$" (F2), though it is not used downstream.
  - Three constants of Corollary 12.3 had been rounded up.

  None changes a conclusion, but the sentence understates both the problems and the verifiers' contributions.
- **Fix.** Replace with: "No verifier found an error that changes a number or a conclusion of a main claim. The fixes were these: (i) both tracks' headlines said that no truncation was used, which was false, since both proofs need the deep-gate truncation (Propositions O1 and O1′); (ii) M4C's far-tail remainder beyond $10^{60}$ had been asserted without proof and hard-coded, and the M4C logic verifier supplied the explicit majorant; (iii) a displayed inequality of M4C §4.2 was false as written for $e_i<3$ (it is not used downstream), and one justification in Lemma Q was misattributed; (iv) three constants of Corollary 12.3 had been rounded up; (v) wording, labels and missing one-line justifications."

### N9 [minor] (overstated wording): "proved necessary", "unavoidable" and "provably fails"
- **Where.**
  - §12.1 (l.2293): "**Deep-gate truncation [proved necessary].** Both proofs truncate at deep gates and pay for the truncation explicitly in $\delta_A$. The verifiers proved that this is unavoidable."
  - §12.5 (l.2369): "Open at $p=3,5$, where the method provably fails, and for $p>97$, where the method plausibly works but was not run."
- **Problem.** The claims go beyond what was proved:
  - What was proved (Propositions O1 and O1′) is that on these atoms and window schedules the *untruncated* first moment is infinite. So Markov's inequality needs a truncation. The M4A obstruction verifier itself writes "some deep-gate truncation is mathematically necessary: either $G'$ or C3's own linear-regime clause". That is necessity for the first-moment step, not for every proof.
  - At $p=3,5$, M4A shows that *its closed-form rate* is negative, and M4A §10 suggests sharper treatments that might change this. "Provably fails" contradicts §12.2's own "This is a limit of the method".
- **Fix.**
  - **l.2293:** replace "**Deep-gate truncation [proved necessary].**" with "**Deep-gate truncation [proved necessary for the first-moment step].**" Replace "The verifiers proved that this is unavoidable." with "The verifiers proved that, on these atoms and schedules, Markov's inequality cannot be applied without it."
  - **l.2369:** replace "where the method provably fails" with "where M4A's averaged bound has a negative asymptotic rate and M4C's gain $q_2/p$ is too weak (§12.2; a sharper treatment of depth-2 gates might change this)".

### N10 [minor] (credit list of §12.7 incomplete)
- **Where.** §12.7 *Credit* (l.2419–2426), in particular "- The classical tools are the Paley–Zygmund inequality, Doob's $L^2$ convergence, Hensel's lemma and the second-moment method on trees (Lyons)." and "- The round-2 covering certificates (track R3, round 2) underlie Theorem 12.11."
- **Problem.** The track reports credit more than §12.7 does:
  - **Internal credits** (M4A §12, M4C §14, M4B §11, M4D §11):
    - R3M's Remark C6 and Proposition 11.15(b), which proposed the route ((S) plus a deep-gate truncation) that M4A and M4C carry out;
    - R3Q's Lemmas 8–9 (high-slope and second-derivative templates);
    - R3F's gate-block Fourier analysis and factorial measure, which motivated the constants;
    - the round-3 checker's Observation G (block-0 probabilities);
    - R2b's UC′ remark, behind Proposition 12.12;
    - the round-2 computational referee's covering program C and round 1's census (tracks D and E), both behind Theorem 12.11;
    - Tao's first-failure idea and round-1 Theorem 3.12, also behind Theorem 12.11.
  - **Classical tools used in the proofs but not credited:**
    - Littlewood–Offord-type anti-concentration (M4A credits it as the guiding idea of Lemma Q);
    - Legendre's formula;
    - Wilson's theorem and the Wilson quotient (Proposition W);
    - $H_{p-1}\equiv0\pmod p$ (Lemma Q, Step 4);
    - König's lemma (survival implies $x\in K_p$);
    - Markov's and Minkowski's inequalities.
  - **Wilson primes.** The search bound for further Wilson primes ($>2\cdot10^{13}$, M4C §13) is Costa–Gerbicz–Harvey's.
- **Fix.** Replace the *Credit* list of §12.7 with the following (keeping N1's Kitamura bullet first):
  - "- The machinery of Theorem 11.14 is round-3 track R3M's, building on round-2 track R1b's frozen-state martingale at $p=2$. R3M's Remark C6 and Proposition 11.15(b) proposed the route that M4A and M4C carry out: a high-slope first-moment bound plus a deep-gate truncation. Round-3 track R3Q's Lemmas 8–9 (high-slope control at $p=2$) are the template both tracks name. Round-3 track R3F's gate-block Fourier analysis motivated the constants $q_s(p)$. The block-0 probabilities $P_0$ use the round-3 checker's Observation G."
  - "- The Hensel reduction and the value–derivative anti-concentration lemma: see N2's wording."
  - "- Theorem 12.9: Tao's block lemma and Theorem 10.12 (round-2 track R2b) are its endpoints. Proposition 12.12 uses R2b's remark UC′. Theorem 12.11 rests on the round-2 covering certificates (track R3 and the round-2 computational referee's program C), on round 1's census (tracks D and E; §4.7), and on Tao's first-failure idea and Theorem 3.12."
  - "- The verifiers contributed Propositions O1 and O1′, the explicit far-tail majorant of Theorem 12.4, the rate survey $7\le p\le211$, and an independent reassembly of every certificate of Theorem 12.1."
  - "- Classical tools: Hensel's lemma and the stabilisation of root counts modulo $p^k$ (Igusa; Evans's $p$-adic Kac–Rice formula); Littlewood–Offord-type anti-concentration; the Paley–Zygmund, Markov and Minkowski inequalities; Doob's $L^2$ convergence; König's lemma; the second-moment method on trees (Lyons); Legendre's formula; Wilson's theorem, the Wilson quotient and $H_{p-1}\equiv0\pmod p$. The known Wilson primes are 5, 13 and 563, with none other below $2\cdot10^{13}$ (Costa–Gerbicz–Harvey, Math. Comp. 83 (2014)). Branching processes in random environments (Smith–Wilkinson; Athreya–Karlin; Afanasyev–Geiger–Kersting–Vatutin) are background only."
  - "- Morita's $p$-adic Gamma function is the object whose digits the barrier lemmas concern."
  - "- The problem is due to Erdős and Graham."

### N11 [minor] (no round-4 status check; priority caveat)
- **Where.**
  - §12.0 has no status check.
  - README l.14 still reads "**Status check, 2026-10-13 (round 3, track S0).**"
  - The README round-4 bullet (l.11) and §0 item 24 assert the result with no reference date.
- **Problem.** Rounds 2 and 3 each recorded a dated check of the public record. Round 4 has none, and Theorem 12.1 is the kind of result whose priority a reader will ask about. The problem page also shows an undated "Currently working on: Sky-Yang" reaction.
- **Fix.**
  - **In §12.0, after *Verification*, add:** "*Status check (round-4 novelty referee, 2026-10-14, 04:14–04:36 UTC; `data/round4/referees/novelty.md`).* Nothing new on #404 by others has appeared since 2026-10-13. The problem page (last edited 29 Sep 2025, 0 proof claims, 7 comments, newest Kitamura's of 8 Jul 2026), Kitamura's repositories (HEADs `32697193` and `ef0881bb`), teorth/erdosproblems (HEAD `86c3dc3e`; #404 open), formal-conjectures PR #6936 (head `205ea70`; open, not merged; no `404.lean` on `main`) and arXiv (indexed to 13 Oct 2026) are unchanged. Nothing public gives positive Haar measure for a set of this kind, or anti-concentration of signed factorial subset sums modulo $p$. The claims of §12 are relative to this record. The problem page lists an undated 'Currently working on' reaction (Sky-Yang)."
  - **README:** add a line "**Status check, 2026-10-14 (round 4, novelty referee).** Still nothing new on #404 by others (note.md §12.0)."

### N12 [minor] (AI disclosure): §8 has no [Round 4] paragraph
- **Where.** §8 ends its round list with "**[Round 3]** Revision 3 (§11) came from a third session on 2026-10-13, …" (l.971–978). There is no round-4 paragraph, although the header says "Changes elsewhere are marked "[Round 4]"". The disclosure for round 4 appears only in the §12 preamble.
- **Fix.** Add after the [Round 3] paragraph of §8:
  "**[Round 4]** Revision 4 (§12) came from a fourth session on 2026-10-13/14, run with the same AI system and the same kind of workflow as rounds 1–3, prompted by the author. It had four research tracks (M4A–M4D) on one target from a shared brief; two or three adversarial verifiers per main claim (separate AI instances writing their own code); and a final round of AI referees on §12 (§12.7). A container restart interrupted the session once (§12.0). Throughout §12, 'the lead' means the AI instance that ran the workflow and wrote §12, not the human author. **No human has checked any part of §12.**"

  (Name the system as the earlier paragraphs of §8 do.)

### N13 [minor; predates round 4, found during this search] (missing credit): the question that Proposition 3.4 answers was posed by Kitamura
- **Where.** §0 item 3 (l.52): "…and there is no bound of the form "$g_p(a)\le C_p$ or $g_p(a)=\infty$"." This is Proposition 3.4.
- **Problem.** Kitamura's `scripts/ignition_scan.py` (July 2026) asks exactly whether such a bound exists ("A bounded B(p) would make the sharpened Tao conjecture decidable-in-principle for each a: g(a,p) <= B(p) or g(a,p) = infinity"). Proposition 3.4 answers it negatively, without credit.
- **Fix.** Append to §0 item 3 and to Proposition 3.4: "This answers, negatively, the question of a bounded 'ignition bound' $B(p)$ raised in Kitamura's odd-prime repository (`scripts/ignition_scan.py`, July 2026), where it is called a sharpened form of a conjecture of Tao."

---

## 4. Credit statements checked (§12 and the [Round 4] edits)

| statement (location) | verdict |
|---|---|
| "The machinery of Theorem 11.14 is round-3 track R3M's, building on round-2 track R1b's frozen-state martingale at $p=2$" (§12.7) | **Correct** (§11.3; R3M §5; M4A §12; M4C §14). It omits R3M's Remark C6 and Proposition 11.15(b) as the route (N10). |
| "found independently by tracks M4A and M4C" (§12.1, §12.7, §0 item 24, README) | **Overstated** (N2). M4C saw M4A's headline. There was a common brief and a shared workspace, and M4A logged first. M4B has a third Hensel-ball statement. |
| "two new ingredients" / "two new lemmas" (§12.1, §0, README) | New **as applications**. The Hensel count is classical, and Lemma Q is Littlewood–Offord-type (N3). |
| "This makes round 3's Remark C6 rigorous" (§12.1) | **Correct** (R3M Remark C6; BRIEF.md). |
| "This is the loophole named in round 3" (§12.1) | **Correct** (§11.3 "Relation to the obstructions"; BRIEF.md). |
| Propositions O1 and O1′ credited to the obstruction verifiers (§12.1) | **Correct** (`checks/M4A_obstruction.md` l.99; `checks/M4C_obstruction.md` l.115). The wording "unavoidable" overstates (N9). |
| "The constants were computed exactly by … the M4C obstruction verifier" (§12.1) | **Inaccurate** for the floating-point recomputations (N6). The values themselves are reproduced (§2.3). |
| "The M4A obstruction verifier found that the rate is positive at every prime $7\le p\le211$" (§12.2) | **Correct** (`checks/M4A_obstruction.md` G3, l.301, l.503). |
| "including an explicit far-tail majorant … (completed by the M4C logic verifier)" (§12.3) | **Correct** (`checks/M4C_logic.md` F1, §8). The summary in §12.7 understates it (N8). |
| "even equidistribution of $\{r!\bmod p\}$ is open" (§12.3); "open in the literature" (§12.5) | True but uncited, and the logic of "even" is reversed. "Open in the literature" overstates (N4). |
| "the Wilson prime 563 needs a separate first block" (§12.3) | **Correct** (M4C Proposition W, §13). The search bound should be cited (N10). |
| "This proves round 3's heuristic $\kappa\approx p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}$" (§12.4) | **Correct** attribution to round 3 (R3M §7.3; BRIEF.md). |
| "Lemma 12.8 … repairs a weighting slip in round 3's Remark C6" (§12.4) | **Correct** (M4B item 6, §8.2). |
| "Minimal $\theta$ recovers Tao's block lemma; $\theta=1$ recovers Theorem 10.12" (§12.4) | **Correct** (forum, 29 Sep 2025; M4D §2 credits R2b). |
| "The verifier re-ran 37 of the 38 cited certificates" (§12.4) | **Correct** (`checks/M4D_P.md` l.24). The README's "every certificate" is inconsistent with it (N7). |
| "the obstruction verifier notes that a shorter pointwise phase already gives $1.45\cdot10^{-9}\mu(A)$" (§12.5) | **Correct** as worded ("notes"). The verifier says it is an observation with M4A's code, not re-verified independently (`checks/M4A_obstruction.md` l.211). |
| "Tao's block lemma and Theorem 10.12 (round-2 track R2b) are the endpoints of Theorem 12.9"; "The round-2 covering certificates (track R3, round 2) underlie Theorem 12.11" (§12.7) | **Correct but incomplete** (N10). |
| "Morita's $p$-adic Gamma function …"; "The problem is due to Erdős and Graham" (§12.7) | **Correct.** |
| §5 [Round 4] under Conjecture 5.2; §12.0 "This proves the cases …"; README l.11 | The proof claim is labelled correctly, but the conjecture's public precursor is uncredited (N1). |
| §11 [Round 4] edits (l.1875, l.2029, l.2147) | **Correct** internal cross-references. |
| Kitamura not mentioned anywhere in §12 or the README round-4 section | **Omission** (N1). |

## 5. Novelty claims checked

| claim | verdict |
|---|---|
| Theorem 12.1: $\mu(K_p)>0$ for $7\le p\le97$, with explicit constants | **New relative to the public record** (§1, §2.1). No prior or concurrent claim of positive measure for $K_p$ or any analogous $p$-adic cancellation set. Conjecture 5.2's heuristic precursor must be credited (N1). |
| Hensel reduction of the fine-scale mass (M4A Theorem 1; M4C Lemma H2 / Proposition H′) | **New as an application.** The underlying count is classical (§2.4; N3). |
| Quenched value–derivative anti-concentration (Lemma Q) with $q_2(p)/p^2$ | **No precursor found** for this block form. It is Littlewood–Offord-type, and Peled–Sen–Zeitouni is a distant analogue (§2.5; N3). |
| Constants $q_s(p)$ | **Not in the literature or in OEIS** (§1, §2.3). The values are reproduced exactly for $p\le23$. $q_1-1$ is round 3's level-1 $L^2$ shell (N3). |
| AC($p$) "not available" or "open" | **Not found in the literature.** But "even equidistribution … is open" reverses the logic (N4). |
| Theorem 12.5 (adaptive windows), Proposition 12.6, Proposition 12.7, Lemma 12.8 | Internal extensions of round 3. No external precursor found. Lemma B2a (finite signed factorial sums) is elementary. |
| Theorem 12.9 ($\theta$-lifting) | **New** as stated. Its endpoints are credited (Tao; R2b). |
| Theorem 12.11 (plateau lower bounds on $\delta_G(p)$) | **New** relative to the public record. Kitamura's ignited fractions are integer data at shallow depth, not lower bounds on $\delta_G$. Credit is incomplete (N10). |
| Proposition 12.12 (single-lineage obstruction) | Internal; uses R2b's UC′ (N10). |
| "c_p ≥ 0.69 … at least 69% of [$p^3\mathbb Z_p$] lies in $K_p$" (§12.0) | Internal arithmetic; not a novelty issue. |

## 6. Wording that could read as human verification

**None found.** Every round-4 statement of checking names AI instances, verifiers or referees, which the §12 preamble defines as AI instances, or says "no human":
- the header (l.12), §0 l.16 and l.134–136;
- §5 l.784;
- the §12 preamble (l.2240–2244);
- §12.0, §12.5 item 4 and §12.7 ("No human has checked any part of §12");
- README l.11, l.34 and l.246.

What is overstated is the *extent* and *arithmetic type* of the AI checking (N6–N8). Two optional additions would help a reader who jumps into the middle:
- write "by AI instances" in §12.1 l.2297 (N7);
- add a [Round 4] paragraph to §8 (N12).

## 7. Reproduction

All commands are run from the repository root. Scratch is in `/tmp/r4_ref_novelty/`.
- `nice -n 10 python3 -I code/round4/referee_novelty/arxiv_batch.py code/round4/referee_novelty/queries.txt 8` (first run, cut short by HTTP 429; log `arxiv_batch_run1.log`).
- `… arxiv_batch.py code/round4/referee_novelty/queries_rerun.txt 8 20` (log `arxiv_batch_run2.log`).
- `… arxiv_batch.py code/round4/referee_novelty/queries_extra.txt 5 20` (log `arxiv_batch_run3.log`).

  Totals:
  - `all:"distinct factorials"` 1 (2610.01899, square products);
  - `abs:"sums of factorials"` 9 (unrelated);
  - `abs:factorials AND abs:adic AND abs:valuation` 8 (unrelated);
  - `abs:erdosproblems` 0;
  - `all:Erdos AND abs:factorials` 3 (unrelated);
  - `abs:"random p-adic" AND abs:series` 0;
  - `abs:"p-adic" AND abs:"subset sums"` 1 (unrelated);
  - `abs:"random p-adic" AND abs:polynomial AND abs:roots` 4 (§2.1);
  - `abs:"p-adic" AND abs:"Kac-Rice"` 0;
  - `abs:factorials AND abs:"modulo p" AND abs:distribution` 2 (the two GLS papers);
  - `abs:"Littlewood-Offord" AND abs:"finite field"` 1 (unrelated);
  - `abs:"anti-concentration" AND abs:"subset sums" AND abs:"modulo"` 0;
  - Stirling and Wilson-quotient distribution queries 0;
  - `abs:"branching process" AND abs:"random environment" AND abs:"dependent"` 18 (§2.2);
  - `abs:"quasi-independent" AND abs:percolation AND abs:tree` 1 (unrelated);
  - the Hensel, Igusa and polynomial-image queries 0;
  - `cat:math.NT`, newest 2026-10-13;
  - `abs:factorial AND abs:residues AND abs:prime` 14 (§2.3: 2609.05652, 2609.37460).
- `nice -n 10 timeout 600 python3 -I code/round4/referee_novelty/qconst_small.py 23` (under 1 s; log `qconst_small.log`). This gives exact $q_1,q_2$ for $3\le p\le23$ and the identity $q_1=p\sum N_z^2/4^p$.
- `nice -n 10 python3 -I code/round4/referee_novelty/kitamura_check.py /tmp/r4_ref_novelty/kodd_full` (log `kitamura_check.log`; clone of `KitaKen1/erdos-404-odd-prime-landscape` at `ef0881bb`). It prints the quoted lines and the table of §2.6.
- `pdftotext` of arXiv:math/0403424 (`/tmp/r4_ref_novelty/gls/gls.txt`, lines 37–41 and 110–115) gives the GLS quotations.
- The reflection identity of N3 was checked with a one-line exact computation for $p\in\{5,7,11,13,17\}$ (`True` for all).
- The timestamps of §2.7 come from `ls -la --time-style=full-iso` on `data/round4/M4{A,C}`, `code/round4/M4{A,C}`, and the `### start:` lines of `data/round4/M4C/test_Q.log`.
