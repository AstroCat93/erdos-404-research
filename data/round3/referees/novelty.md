# Round 3 referee report: NOVELTY (note.md §11 and the [Round 3] edits), 2026-10-13

Scope: novelty, priority and credit for revision 3 of note.md (§11 except the placeholder §11.5, and the "[Round 3]" edits in §0, §2, §5, §8, Remarks 10.8, §10.5, §10.6), plus the round-3 rows of README.md. Sources read: README.md; note.md §§0, 2, 5, 8, 10.5–10.6, Remarks 10.8, §11 in full; the track reports `data/round3/reports/{S0,R3N,R3Q,R3M,R3F}.md`; the checks `data/round3/checks/{R3N,R3Q,R3M,R3F}.md`; S0's saved excerpts of Kitamura's repositories. Everything outside the repository was treated as data.

This report was written by an AI referee instance. It is not a human review.

Files written: this report; `code/round3/referee_novelty/arxiv_query.py` (arXiv API query helper) and `code/round3/referee_novelty/novelty_checks.py` (two small arithmetic checks, §2.3 and F6 below). Scratch: `/tmp/r3_ref_novelty/` (clones, logs). Compute used: well under one core-minute; nothing heavy was run.

## Verdict

**No fatal or serious novelty or credit problem.** As of 2026-10-13 19:28 UTC, the public record has no exact value of $f(a,2)$ for any $a>256$ other than Kitamura's rows 510, 1022, 1102, 2046, 3456, 4094 and 8190. In particular, nothing public gives $f(594,2)$, $f(17662,2)$, the table to $2^{15}$, the shadows $t=14$–$17$, an explicit rate for $\delta_G(2)$, a survival rate for a critical branching process in an odometer environment, a positive-measure theorem for $K_p$, or the gate-block constants $J_p$. Nothing new on #404 by others has appeared since round 2: the problem page, the forum, Kitamura's repositories, teorth/erdosproblems, PR #6936, arXiv and GitHub were all re-checked today. The credits to Kitamura, Tao, Smith–Wilkinson, Athreya–Karlin, Kozlov, Afanasyev–Geiger–Kersting–Vatutin, Morita and the round-2 tracks are essentially correct.

There are **12 minor findings** (§3). Most are wording fixes:
- one statement about Kitamura's "≈11.5/G" that the data contradict (F1);
- one self-referential "first improvement" (F2);
- an overstatement of how much of round 3 was adversarially checked (F3);
- an S0 correction to Remark 10.8.2 that was not applied, and is now contradicted by a citation in §11.6 (F4);
- integer data used as evidence about Haar measure (F5);
- a "by-product" already implied by round 1 (F6);
- several small credit and citation gaps (F7–F12).

---

## 1. Public-record check (all times UTC, 2026-10-13)

| source | how | time | result |
|---|---|---|---|
| https://www.erdosproblems.com/404 | WebFetch | ≈19:15 | Unchanged. "This page was last edited 29 September 2025." Proof claims (0), proof expositions (0), Comments (7). No status label is printed. The only numerical remark is "Lin [Li76] has shown that $f(2,2)\le254$". Reactions: "Currently working on: Sky-Yang"; "Open to collaboration: Woett"; likes Woett, Sky-Yang, Alfaiz. |
| https://www.erdosproblems.com/forum/thread/404 | WebFetch | ≈19:15 | Unchanged: 7 comments (Kovač ×2 and Bloom, 13 Aug 2025; Tao ×2, 29 Sep 2025; Kitamura, 7 Jul 2026 23:11 and 8 Jul 2026 01:58). "The ability to post new comments has been suspended." No 594, 66126, 90394 or 17662. |
| https://www.erdosproblems.com/bibs/Li76 | curl | 19:15:11 | "[Li76] Lin, S., On two problems of Erdős concerning sums of distinct factorials. Bell Laboratories internal memorandum (1960)." |
| github.com/KitaKen1/erdos-404-p2-landscape | `git ls-remote`; shallow clone | 19:14:19; ≈19:20 | HEAD `32697193` (2026-07-08 07:50 +0900), unchanged. Issues: 0 (WebFetch of the issues page, ≈19:22). |
| github.com/KitaKen1/erdos-404-odd-prime-landscape | `git ls-remote`; WebFetch of issue #1 | 19:14:21; ≈19:22 | HEAD `ef0881bb`, unchanged. Issue #1 (by AstroCat93, 2026-10-12) has no reply visible to a logged-out reader. |
| github.com/teorth/erdosproblems | `git ls-remote`; shallow clone | 19:14:26; 19:15:35 | HEAD `86c3dc3e` (2026-10-13 17:13 UTC). The `data/problems.yaml` entry for #404 still reads `state: "open"` (last_update 2025-08-31), `formal_status: unformalized`, `oeis: ["N/A"]`. |
| google-deepmind/formal-conjectures PR #6936 | `git ls-remote refs/pull/6936/*`; WebFetch of the PR page; shallow clone of `main` | 19:14:25–19:14:38 | Head still `205ea70`. Open, not merged. Reviews: bocowgill approved (9 Oct), Paul-Lez left comments (10 Oct), bocowgill approved again (11 Oct). `main` at `e47a327f` (2026-10-13 16:06 UTC) has `ErdosProblems/403.lean` and `405.lean` but **no `404.lean`**. |
| plasma-ai/erdos | blobless clone | 19:16:34 | The #404 pages' only change today is commit `4e4895c8` (2026-10-13 06:00 −0600), which rewords the site labels into the past tense. Status open, claim none. Claim pages: Lin (dated 1976), Kitamura p = 2, Kitamura odd p. The E0403 page asserts that the [ErGr80] bibliography reads "[Lin (76)]" and that erdosproblems.com's 1960 is a misprint. |
| grandchallenge/MATH-PROGRAMME issue #1674 | WebFetch | ≈19:25 | Open. **New since S0:** one comment by fyremael, 2026-10-13, with trivial arithmetic ($1!+4!=25=5^2$; some residues $k!/5\bmod5$) and a proposed task. No new result. Its instructions to automated workers were not acted on. |
| arXiv API | `code/round3/referee_novelty/arxiv_query.py` | 19:17:30, 19:18:04, 19:27:28 | Nothing on #404 or on $v_p$ of sums of distinct factorials; the newest submissions in the index date from 2026-10-09. Queries: `all:"distinct factorials"` (only 2610.01899, square products); `abs:"sums of factorials"`; `all:Erdos AND abs:factorials`; `abs:adic AND abs:factorials AND abs:valuation`; `abs:"erdosproblems"` (0); Morita/Γ/equidistribution (0); BPRE with odometer or stationary-ergodic or dynamical environments (0); `abs:"random p-adic" AND abs:series` (0); p-adic subset sums (1, unrelated); subset sums with factorials (2, unrelated); the Cusick conjecture (8, background, F12); `abs:"branching process" AND abs:"random environment"`, newest 6 (none on odometer environments). |
| GitHub search (code and repositories) | GitHub MCP search | 19:16–19:27 | Code `"f(594,2)"` returns only Kitamura's three p2 documents. Code `"g(594"` returns only Kitamura. Code `"distinct factorials" "594"` has no hit with content on #404; the erichou1 problem card matches only through hashes, checked 19:27:09. Repositories `erdos 404 pushed:>=2026-10-12` return only AstroCat93/erdos-404-research (last push 2026-10-12; round 3 is not pushed). Of the broad Erdős repositories updated today (plasma-ai/erdos, SamPetkov/Erdos, wcook04/plectis-erdos, leandrejack-afk/erdos-computations, wangkant/corroborate, siso-os), none has #404 factorial content beyond plasma-ai's wiki. |
| OEIS | JSON search | 19:15:41–19:16:00 | No entry for $f(a,2)$ ("0,254,1,6,3,133", "254,1,6,3,133,4,13,7,14,8,13,10,1533"), for the shadow sequence ("254,133,1533,126,254,276,895"), for $g_2$ ("253,3,130,6"), or for 594/17662 together. The hits for 89804, 90394, 221465 and 203812 alone are unrelated. teorth's entry also has `oeis: N/A`. |
| Web search (general) | WebSearch | ≈19:26 | "Erdős problem 404" 2026: nothing beyond erdosproblems.com and the MATH-PROGRAMME issue. |

## 2. Prior and concurrent work on the specific topics

### 2.1 Exact $f(a,2)$ beyond $a\le256$; $f(594,2)$; $f(17662,2)$
- **Nothing public.**
  - Kitamura's published exact rows beyond 256 are 1102, 3456 and 8190, plus the shadows 510, 1022, 2046 and 4094.
  - For 594, Kitamura publishes only $f(594,2)\ge66126$, "verified 2026-07-06, with deeper probes still running" (`determining_exact_values.md` §5).
  - No source mentions 17662.
- **Possible unpublished concurrent work.** Kitamura reported deeper probes of 594 still running in July. The erdosproblems page also lists "Currently working on: Sky-Yang" (undated). See F11.

### 2.2 Explicit rates for $\mu\{g_2\ge G\}$; critical BPRE survival in odometer or deterministic environments
- **No result found for odometer, Toeplitz or deterministic-ergodic environments.**
- Survival asymptotics are known in these settings:
  - i.i.d. environments: Kozlov 1976 (order $n^{-1/2}$ under extra assumptions; $\sim cn^{-1/2}$ in the linear-fractional case); Geiger–Kersting, Theory Probab. Appl. 45 (2000) 607–615 ($\sim cn^{-1/2}$ in general); Afanasyev–Geiger–Kersting–Vatutin 2005 ($P(Z_n>0)\sim\theta P(\min S\ge0)$). The summary is Dyakonova–Vatutin–Sagitov, arXiv:1110.6139, §3.1, re-read today: "Kozlov has shown … $c_1n^{-1/2}\le P(Z_n>0)\le c_2n^{-1/2}$ … Only in 2000 Geiger and Kersting were able to demonstrate the validity of (12) for arbitrary BPREs".
  - Finite-state Markov environments: Grama–Lauvergnat–Le Page, SPA 129 (2019) 2485–2527, arXiv:1708.00233.
  - Multitype i.i.d. environments: Le Page–Peigné–Pham, AOP 2018.
- The note's position, that no BPRE result applies (§11.1 and Lemma S0.1), is correct. The citation of the $n^{-1/2}$ law is imprecise; see F8.

### 2.3 Positive Haar measure for zero sets of random $p$-adic series
- **Nothing found** on positive measure of "0 is a subsum" or of zero sets of random $p$-adic series.
- The nearest literature counts the zeros of random $p$-adic polynomials (Evans 2006, https://www.stat.berkeley.edu/users/evans/699.pdf; Caruso, arXiv:2110.03942). It also covers $p$-adic self-similar sets (Hare–Vávra, arXiv:2307.07375; cited by S0).
- The classical template for Theorem 11.14 is the second-moment method for survival on trees: Lyons (1990, 1992); Mathieu–Temmel, SPA 122 (2012), arXiv:1103.1291, which S0 named as the closest template. The note does not cite it (F12).

### 2.4 Equidistribution of subset sums of factorials, or of the digits of Morita's $\Gamma_p$
- **Nothing beyond mod $p$:**
  - Garaev–Luca–Shparlinski 2005 and Klurman–Munsch 2017, both already cited;
  - Garaev–Pardo, *Additive congruences with factorials modulo a prime*, arXiv:2508.12127 (Aug 2025). This is mod $p$ only: sums of products $m!n!$ and non-distinct sums of factorials. It does not treat subset sums, and it does not treat $p^k$ for $k\ge2$.
- **Nothing on $\Gamma_p(n)\bmod p^k$ equidistribution.** This search was WebSearch and arXiv only, so the check is limited.

### 2.5 $L^2$ and collision-count methods for subset-sum coverage
- These are **classical**:
  - Parseval and Cauchy–Schwarz bounds on missed residues and on the measure of the support;
  - Erdős–Rényi, *Probabilistic methods in group theory*, J. Analyse Math. 14 (1965) 127–138, on random subset sums covering a finite abelian group;
  - for $L^2$ densities and absolute continuity of Bernoulli convolutions: Garsia (1962) and Solomyak, Ann. of Math. 142 (1995).
- R3F's report labels these as "standard facts" and lists the classical tools it uses. Note §11.4(b) states Proposition 11.20 as "[proved]" with no "standard" label (F12).
- The applications to factorial windows (Theorem 11.22, §11.4(c)) have no precursor that I found.

### 2.6 The environment walk $s_2(x+n)-s_2(x)$ (Lemma S0.1)
- For a fixed shift $t$, the law of $s_2(n+t)-s_2(n)$ is the subject of Cusick's conjecture. This is the same object as the Haar law of $s_2(x+t)-s_2(x)$ on $\mathbb Z_2$. The literature includes:
  - Drmota–Kauers–Spiegelhofer (SIAM J. Discrete Math. 2016);
  - Spiegelhofer–Wallner, *The binary digits of n+t*, arXiv:2005.07167 (Ann. Sc. Norm. Super. Pisa, to appear per arXiv). It proves the conjecture when $t$ has many blocks of ones and gives a Gaussian law, strengthening Emme–Hubert;
  - K. Cheng, *A first-exit proof of Cusick's sum-of-digits conjecture*, arXiv:2606.23398 (v2, Aug 2026). This is an unrefereed claim of a full proof by a stopped-random-walk method. WebFetch today confirmed that it concerns a fixed $t$ and not persistence over all $k\le n$.
- None of these gives the persistence probability $P(D(y,k)\ge0\ \forall k\le n)\asymp(\log n)/n$ of Lemma S0.1, and the note claims no novelty for it. The literature is still worth citing as context (F12).

### 2.7 Arithmetic check of Kitamura's "≈11.5/G" (for F1)
Command (output in `/tmp/r3_ref_novelty/novelty_checks.log`):
```
nice -n 10 python3 -I code/round3/referee_novelty/novelty_checks.py data/round3/S0/kitamura_excerpts/p2_exact_table_1_256.csv
```
- **Class census** (published exact $\delta_G(2)$, note §4.7). $G\cdot2\delta_G$, the even-class normalisation, is 3.88, 4.85, 6.20, 6.33 and 6.50 at $G=8,16,24,25,32$.
  - At $G=25$, the depth of Kitamura's own census of $g\le24$, it is $6.33$, against $11.5$.
  - Over all of $\mathbb Z_2$ it is half that.
  - So "11.5/G" is **not** a fit to the census in either normalisation.
- **Haar Monte Carlo** (note §5). $G\cdot2\delta_G=8.24$, 9.70 and 10.57 at $G=64,128,254$.
- **Kitamura's own table** (even $a\le256$). $G\cdot\#\{g\ge G\}/128=9.0$, 14.0 and 10.0 at $G=64,128,256$, consistent with 11.5.
- Kitamura's texts say only "measured probability `~ 11.5/G`" (`witness_gallery.md` l.135) and "the surviving fraction decays like `~ 11.5/G`" (`determining_exact_values.md` l.218–219). The second sentence sits next to the census sentence, but it does not say that the figure was computed from the census.

---

## 3. Findings

### F1 [minor] (credit accuracy): Kitamura's "≈11.5/G" is attributed to the class census, and the census data contradict this
- **Where.** note.md l.1920: "Kitamura does not state the normalisation; the figure comes from the class census." The R3N check (`checks/R3N.md` §5) proposed this wording, reading S0's report; S0 says only that the normalisation is not stated.
- **Problem.** Kitamura does not say how the figure was measured. The census cannot be its source: at the census depth $G\approx24$–$25$ the even-class fraction gives $G\cdot2\delta_G\approx6.2$–$6.3$, not 11.5 (§2.7). Kitamura's own integer table and the Haar Monte Carlo at $G\ge64$ do give values near 11.5. As written, the sentence implies that Kitamura's figure does not fit Kitamura's own census.
- **Fix.** Replace the sentence with: "Kitamura states neither how the figure was measured nor its normalisation. It is not a fit to the $g\le24$ census, which gives $G\cdot$(even-class fraction) $\approx6.3$ at $G=25$. It is consistent with the even $a$ of Kitamura's own table $a\le256$ ($G\cdot$fraction $=9$–$14$ for $G=64$–$256$) and with twice the Haar Monte Carlo values of §5 [arithmetic: `code/round3/referee_novelty/novelty_checks.py`]."

### F2 [minor] (overstated novelty): "the first improvement on the census bound 0.1016"
- **Where.** §0 item 20 (l.123), §11.0 headline 2 (l.1857), README l.38.
- **Problem.** The census bound $\delta_G(2)\le\delta_{32}(2)=0.1016$ is the note's own round-1 result. It holds for every $G\ge32$ only because $\delta_G$ is non-increasing. A census to depth 33–40, which nobody has run, would beat 0.1016 at moderate $G$ and by a wide margin. The new bound improves it by 0.0011, and only for $G\ge2^{37}$. "First improvement" is literally true but suggests a hard-won advance. §11.2 (l.1968) and README l.38 already say the bound is meaningful only at astronomically large $G$, so this is a wording issue.
- **Fix.** In all three places, replace "the first improvement on the census bound 0.1016" with: "the first proved bound below round 1's census value $\delta_{32}(2)=0.1016$ that applies at large $G$ (the census bound itself could be lowered at moderate $G$ by extending the census beyond $G=32$, which was not attempted)".

### F3 [minor] (verification wording): what was adversarially checked is overstated
- **Where.**
  - §11 preamble l.1818: "Every result below was checked in two stages".
  - §11.0 l.1838: "Every track was then checked by a separate instance."
  - §0 l.11: "Each round-3 track was checked by a separate AI instance".
  - README l.33: "Each of six tracks was checked by a separate AI instance that wrote its own code."
- **Problem.** Track S0 had no adversarial check; `data/round3/checks/` has only R3N, R3Q, R3M and R3F (R3C is pending). §11.1 itself correctly labels Lemma S0.1 "[proved by S0; not separately checked]". S0's re-checks of Kitamura's rows (S0.R1–R3) were also not checked, although R3N's programs B, C and D later re-validated the table $a\le256$.
- **Also in the README.**
  - l.17 is stale: "Two rounds of three AI referees … have checked it: note.md §9 … and §10.8".
  - l.33 says, in the past tense, that "a final round of three AI referees then checked note.md §11", while that round is still in progress and §11.8 is still `[REFEREE_PLACEHOLDER]`.
- **Fix.**
  - In the four places, write "each of the five research tracks (R3N, R3Q, R3M, R3F, R3C) was checked by a separate AI instance; the status gate S0 was not separately checked (its Lemma S0.1 is marked as such)".
  - l.1818: write "Every result below from a research track was checked …".
  - README l.17: add "and a third round on §11 (§11.8)".
  - Keep README l.33 in its final form only after §11.8 is filled.

### F4 [minor] (unapplied S0 correction, now contradicted by a citation)
- **Where.** Remark 10.8.2 (l.1250): "For natural $x$, $W_n=s(n)-c(x,n)$ … It is bounded above by $\log_2n+1$, and it tends to $-\infty$ along record times." §11.6 item 4 (l.2112) cites "(Remark 10.8.2; S0)" for the opposite: "For natural $a$ the environment walk $W_n=s(a+n)-s(a)$ is bounded below".
- **Problem.** S0 (report, item 6 and Open issue 2) found that for natural $x$, $W_n=s_2(x+n)-s_2(x)\ge1-s_2(x)$. This follows from Kummer's carry count. The divergence to $-\infty$ holds only on $\Omega$ (G1). The fix was not applied, so §11.6 now cites a remark that says the opposite of the cited statement. The proof of Theorem 10.1 is unaffected.
- **Fix.** In Remark 10.8.2, replace "It is bounded above by $\log_2n+1$, and it tends to $-\infty$ along record times." with: "It is bounded above by $\log_2n+1$. On the full-measure set $\Omega$ it tends to $-\infty$ along record times (G1). For natural $x$, Kummer gives $W_n=s(x+n)-s(x)\ge1-s(x)$, so it is bounded below. **[Round 3; S0]**"

### F5 [minor] (overstated inference): integer survival data used as evidence about the Haar density $\delta_G(2)$
- **Where.**
  - §5 l.763: "The survival data over the integers suggest $\delta_G(2)\approx c/G$ rather than $0.7/\sqrt G$".
  - §0 item 19 (l.122): "The survival data suggest $\delta_G(2)\approx c/G$".
  - §11.1 l.1924: "… that $\delta_G(2)$ decays like $c/G$ … This reconciles, heuristically, the two fits".
  - Remark 10.8.4 (l.1252).
- **Problem.** For $G>16$ the even $a\le2^{15}$ are not a sample of Haar measure mod $2^{G}$. Their digits above position 15 vanish, and their environment walk is bounded below (S0 Remark S0.2; F4). So R3N's count $G\cdot\#\{a\le2^{15}:g_2(a)\ge G\}/16384\in[8,12]$ for $256\le G\le2^{17}$ is a statement about integers, and only heuristic evidence about $\delta_G$. The Haar evidence is S0's re-fit of the published Haar values, which favours $(\log G)/G$ over $0.7/\sqrt G$ for $8\le G\le254$.
- **Fix.**
  - l.763 and item 19: "Over the integers $a\le2^{15}$, the proportion with $g_2(a)\ge G$ behaves like $c/G$ for $256\le G\le2^{17}$. A re-fit of the published Haar values favours $(\log G)/G$ over $0.7/\sqrt G$ [heuristic; §11.1]."
  - l.1924: add "For $G>16$ the integer data do not sample Haar measure (their environment walk is bounded below), so they bear on $\delta_G(2)$ only heuristically", and change "reconciles" to "suggests a reconciliation of".

### F6 [minor] (internal novelty): the "by-product" of Proposition 11.21 is already implied by round 1
- **Where.** §11.4(b), l.2063: "As a by-product, every residue class mod $7^9$, $11^7$ and $13^7$ has the form $\sum_{i\in B}i!$".
- **Problem.** Round 1's tail frontiers (§4.5) already say that every class of $p\mathbb Z/p^{v(R!)}$ is a sum of distinct $n!$ with $p\le n<R$, up to $11^{14997}$ and $13^{12498}$ (re-run in round 1), and $7^{283331}$ (archived single-implementation log). The subset sums of $\{0!,\dots,(p-1)!\}$ cover $\mathbb Z/p$; I checked this for every $p\le23$ with `novelty_checks.py`, and Tao suggested the check. Together these give every residue mod $p^{14997}$ ($p=11$) and $p^{12498}$ ($p=13$). The round-3 statement is a much weaker, though independent, Fourier confirmation.
- **Fix.** Append: "This is implied, with far larger exponents ($11^{14997}$, $13^{12498}$; and $7^{283331}$ from archived logs), by the tail frontiers of §4.5 together with the covering of $\mathbb Z/p$ by subset sums of $0!,\dots,(p-1)!$. Here it is an independent Fourier-analytic confirmation at low depth."

### F7 [minor] (missing credit): round-2 and Kitamura contributions that round 3 builds on
- **§11.8** (l.2140–2145) omits:
  - round-2 track **R1b**: the frozen-state martingale and window identity of Theorem 10.1, which Theorem 11.7, Proposition 11.10 and Theorem 11.14 extend. R3Q's credits list it;
  - round-2 track **R1a**: Claim 10.9, which Theorem 11.9 is compared with;
  - the **round-2 computational referee and lead**: the period mean and the factorial-digit transfer recursion behind §11.4(d). R3F's credits list them.
- **§11.1 table** (l.1891). Program B's "shifted normal form" is the single-step form of Kitamura's "scaled gate DP" recurrence $x'=(x+dH)/2^e$ (`scripts/p2_scaled_gate_search.py`). Program C's pair steps $\{0,1,m,1+m\}$ are Kitamura's pair gates. S0 also ran Kitamura's script unmodified as one of its two rung programs.
- **Corollary 11.3** (l.1901) and the value-set check (l.1910) use Corollary 3.7.1. That corollary proves Kitamura's sibling-pairing statement and Kitamura's value-set facts, but Kitamura is not named at either place.
- **Fix.**
  - Add to §11.8: "Round-2 track R1b: the frozen-state martingale of Theorem 10.1, extended in §§11.2–11.3. Round-2 track R1a: Claim 10.9. The round-2 computational referee and lead: the period mean and the factorial-digit transfer recursion (§11.4(d)). Kitamura: the pair-gate and scaled ('shifted') DP recurrences that programs B and C reimplement."
  - At l.1901: write "Corollary 3.7.1(i) (Kitamura's sibling-pairing statement) gives …".
  - At l.1910: write "as Kitamura's classification and Corollary 3.7.1(iii) require".

### F8 [minor] (credit precision): the $n^{-1/2}$ law
- **Where.** l.1926: "In i.i.d. environments the corresponding probability is $\asymp n^{-1/2}$ (Kozlov; Afanasyev–Geiger–Kersting–Vatutin)."
- **Problem.** "The corresponding probability" is the probability that the walk stays $\ge0$. For i.i.d. zero-mean finite-variance increments, its order $n^{-1/2}$ is classical fluctuation theory (Sparre Andersen; Spitzer; see Feller, Vol. II, §XII.7), not Kozlov's or AGKV's. Kozlov (1976) proved that the BPRE *survival* probability is of order $n^{-1/2}$ (exact asymptotics only in the linear-fractional case). Geiger–Kersting (2000) proved $\sim cn^{-1/2}$ in general, and AGKV (2005) gave the relation $P(Z_n>0)\sim\theta P(\min S\ge0)$. Geiger–Kersting is cited in S0's report but not in the note.
- **Fix.** Replace the parenthesis with: "(classical fluctuation theory for random walks, e.g. Feller II §XII.7). In i.i.d. environments the survival probability of a critical BPRE is of the same order (Kozlov 1976; Geiger–Kersting 2000; AGKV 2005, Thm 1.1)." Add to the References: "J. Geiger, G. Kersting, *The survival probability of a critical branching process in random environment*, Theory Probab. Appl. 45 (2000) 607–615."

### F9 [minor] (accuracy of a statement about Kitamura's ladder)
- **Where.** §11.0 l.1850: "It also re-checked … the first four rungs for $a=594$."
- **Problem.** The sentence follows a description of *Kitamura's* four rungs, $8192,\dots,65536$. S0 checked $G=1024,2048,4096,8192$, and says explicitly that "the rungs $G\ge16384$, and so the published bound 66126, have not been reproduced". Only 8192 is one of Kitamura's rungs. Kitamura's bound itself *was* later confirmed, by R3N's verified witness at $K=66126$. The note does not say so.
- **Fix.** Replace the clause with: "… and the rungs $g_2(594)\ge1024,2048,4096,8192$ (only the last is one of Kitamura's published rungs). Kitamura's bound $f(594,2)\ge66126$ is now independently confirmed by an explicit verified witness (R3N, `witness_594_K66126.txt.gz`)."

### F10 [minor] (citation): Lin's year
- **Where.** §2 l.235 ("Bell Labs internal memorandum, 1960") and the References at l.2152 ("(1960; cited as [Li76] …)"). §11.0 l.1848 now notes the conflict and points to §2, but §2 still states 1960 without qualification.
- **Problem.** erdosproblems.com prints 1960 under the key Li76 (re-read today). The plasma-ai wiki says that [ErGr80] cites "[Lin (76)]". Neither S0 nor I could check the monograph.
- **Fix.** At l.235 and l.2152 write: "Bell Laboratories internal memorandum; erdosproblems.com prints the year 1960 under the key [Li76], and the plasma-ai/erdos wiki reports that [ErGr80] cites it as 'Lin (76)'; we have not seen the monograph."

### F11 [minor] (priority caveats and "largest known")
- **(a) Priority caveat for 594.** §11.0 headline 1, §11.1 and README l.37 should say that the claim is relative to the public record. Kitamura reported "deeper probes still running" in July 2026 and has published nothing since. The erdosproblems page shows an undated "Currently working on: Sky-Yang" reaction.
  - Fix: add to the §11.1 *Credit* paragraph: "No exact value of $f(594,2)$ is in the public record as of 2026-10-13. Kitamura reported deeper probes still running in July 2026, so an unpublished determination cannot be excluded."
- **(b) "The largest excess known"** (l.122, l.1855 "we know", README l.37). Finite values of $g_2$ are unbounded (Proposition 3.4), but not computed.
  - Fix: write "the largest exactly computed value of $g_2$ at a natural number in the public record".
- **(c) "Kitamura's exact table reached 256"** (l.122, l.1856, l.1912, README l.37). This is correct for Kitamura's complete table.
  - Fix, for precision: write "Kitamura's complete exact table covered $a\le256$, plus isolated rows up to 8190".
- **(d)** l.1848, "with no mathematics": since 2026-10-13 the MATH-PROGRAMME issue has a comment with trivial arithmetic ($1!+4!=5^2$).
  - Fix: write "with no new mathematics".

### F12 [minor] (background references; no credit owed, but readers need them)
Add a "[Round 3]" block to the References and the corresponding in-text mentions:
- **§11.4(b), Proposition 11.20 and Theorem 11.22.** Label Proposition 11.20 "[proved; standard: Plancherel and Cauchy–Schwarz]". Note that the collision-count ($L^2$) coverage criterion is classical: Erdős–Rényi, J. Analyse Math. 14 (1965); for $L^2$ densities of Bernoulli convolutions, Garsia (1962) and Solomyak (1995).
- **Theorem 11.14.** It is the second-moment (Paley–Zygmund) method for survival on trees: Lyons (1990, 1992). For dependent percolation on trees, the closest template is Mathieu–Temmel, SPA 122 (2012), as S0 found.
- **§11.1, Lemma S0.1.** For the walk $s_2(x+t)-s_2(x)$: the Cusick-conjecture literature (Drmota–Kauers–Spiegelhofer 2016; Spiegelhofer–Wallner, arXiv:2005.07167; Cheng, arXiv:2606.23398, an unrefereed claim). For non-i.i.d. BPRE survival: Grama–Lauvergnat–Le Page, SPA 129 (2019) (finite-state Markov), the nearest non-i.i.d. setting.
- **Sources §11.0 relies on.** `plasma-ai/erdos` (wiki, commit `4e4895c8`), grandchallenge/MATH-PROGRAMME issue #1674, Kitamura `witness_gallery.md` §9 and `determining_exact_values.md` §5, and Dyakonova–Vatutin–Sagitov, arXiv:1110.6139.

---

## 4. Credit statements checked

| statement (location) | verdict |
|---|---|
| Kitamura identified 594 as the open champion, with $f(594,2)\ge66126$ (l.1850, l.1930, l.2141; §2 l.253) | **correct** (`witness_gallery.md` §9; `determining_exact_values.md` §5). See F9 for the rung wording. |
| Kitamura designed the exact-value pipeline (exhaustive DP plus witness); Lemma 11.1 is that pipeline written out (l.1878, l.1930) | **correct** (Kitamura's "house rule": a witness re-verified from the definition, plus a second no-witness DP). Kitamura's pair and scaled recurrences are not credited for programs B and C (F7). |
| Kitamura's table $a\le256$ and rows 1102, 3456, 8190, with shadows to $t=13$ (l.1909, l.1916, l.1930) | **correct** (README records table l.335–350; shadow table l.391–393). |
| Kitamura's critical-branching picture and "≈11.5/G" (l.1920, l.2141) | Picture **correct** ("the predictable thin tail of a critical branching process"). The provenance attributed to the figure is wrong (F1). |
| Tao: the block lemma and the position-independent programme (l.2142) | **correct** (forum, 29 Sep 2025). It matters for §11.5, which is not checked here. |
| Smith–Wilkinson, Athreya–Karlin: classical criteria assume conditional independence of offspring (l.2000, l.2143) | **correct** (Ann. Math. Statist. 40 (1969) 814–827; 42 (1971)). Both assume that individuals reproduce independently given the environment; the survey's §1 confirms the attribution of the BPRE start. |
| Kozlov; AGKV for $n^{-1/2}$ (l.1926) | imprecise: F8. The Remark 10.8.2 wording on Kozlov (from round 2) is correct. |
| "no result of theirs is used in a proof" (l.2143) | **correct** for §§11.2–11.3 (R3Q and R3M use only Doob, Paley–Zygmund, Minkowski, Chernoff and other classical tools). |
| Morita: the $p$-adic Gamma function, whose digits the barrier lemmas concern (l.2144; Prop 11.23) | **correct** (J. Fac. Sci. Univ. Tokyo Sect. IA 22 (1975) 255–266). |
| Earlier AI write-ups | Not used in §11 apart from Proposition 1.2 (compactness) in the proof of Theorem 11.14, which is credited in §1.3. No change needed. The README and §2 credits are unchanged and still correct. |
| Round-2 tracks R2a, R2b, R3 (l.2145) | **correct but incomplete** (F7: R1b, R1a, the round-2 computational referee and lead). |
| Round-1 track D: the BFS design behind program A (l.1930) | **correct**. |
| "Theorem 11.9 is a proved analogue of R1a's unverified Claim 10.9, with a weaker rate" (l.1973) | **correct** (R3Q §9: proved rate $G^{-1/7}$ against the claimed $G^{-0.2075}$). |
| §8 [Round 3] disclosure (l.954–960) | adequate. It names the AI system and its developer and says "No human has checked any part of §11". |
| §11.0 status bullets (l.1842–1848) | All **confirmed** today, apart from F11(d). |

## 5. Novelty claims checked

| claim | verdict |
|---|---|
| $f(594,2)=90394$, $f(17662,2)=221465$, exact $f(a,2)$ for all $a\le2^{15}$, shadows $t=14$–$17$ | **New relative to the public record** (§1, §2.1). Add the priority caveat (F11a). |
| "the largest excess known" | Correct when read as "largest exactly computed $g_2$ at a natural number". Reword (F11b). Kitamura's best was the lower bound $g_2(594)\ge65536$. |
| "Kitamura's exact table reached 256" | **Correct** for the complete table. Reword for precision (F11c). |
| "The new ingredient is a windowed depth-first search" (l.1880) | **Correct** as an implementation novelty. Kitamura's scaled gate DP (read today) is a breadth-first set DP over pair steps with shifting, and has no bounded windows. |
| Explicit rate $\delta_G(2)\le2^{1/80}G^{-1/80}$ (Theorem 11.7) | **No precursor found.** Kitamura's decay is empirical, BPRE theory does not cover odometer environments, and Theorem 10.1 is qualitative. |
| "first improvement on the census bound 0.1016" | Literally true but self-referential (F2). |
| "first beats the trivial 1/16 at $G=2^{448}$" (l.1969) | Internal statement, correct as worded. |
| Conditional $\mu(K_p)>0$ (Theorem 11.14), second-moment identity, impossibility of per-window Cauchy–Schwarz | **No precursor found** (§2.3). The method is classical and should be cited (F12). |
| Gate-block constants; "explains round 2's ratio ≈1.17" (Theorems 11.17–11.19, l.2048, l.1587, README l.41) | **Supported.** Round 2 (§10.5) observed the ratio of single gate blocks settling near 1.17 for every $p$ tested. R3F proves $\rho_d\to J_p$ with $J_5,J_7,J_{11},J_{13}=1.16698,\,1.17044,\,1.17252,\,1.17295$ (enclosures in R3F §A5), and $J_{13}$ matches round 2's diagnostic 1.173 at $d=5$–$7$. "Explains the limiting value" would be slightly more precise: at small $d$, $\rho_d$ reaches 1.84 at $p=11$. |
| Collision-count version of Theorem 10.16; $L^2$ barrier lemma; $L^2$ renormalisation | New as applications. The underlying $L^2$ tools are classical (F12). |
| Interval-arithmetic re-run (§11.4(e)) | Internal. No novelty claim. |
| "by-product: every residue mod $7^9,11^7,13^7$ is a sum of distinct factorials" | Already implied by round 1 (F6). |
| Survival law $c/G$ and the "reconciliation" (l.1918–1928) | Heuristic. Overstated as evidence about Haar measure (F5); Kitamura provenance wrong (F1). |
| Lemma S0.1 | No novelty claimed. No precursor found for the persistence probability (§2.6). |

## 6. Wording that could read as human verification

None found. §11's preamble (l.1818–1822), §0 l.11–13, §8 l.954–960 and README l.33 all say that the checks and referees are AI instances and that no human has checked §11. The "*Check*" paragraphs (l.1980, l.2030, l.2082) and the phrase "verified by three verifiers" (programs) are unambiguous in context. What is overstated is the *extent* of the AI checking (F3). Optionally, prefix each "*Check*" paragraph with "AI" ("*AI check (`data/round3/checks/…`)*"), so that a reader who jumps straight to a subsection still sees it.

## 7. Reproduction

- `python3 -I code/round3/referee_novelty/arxiv_query.py 'QUERY' N` (arXiv API; the queries are listed in §1).
- `nice -n 10 python3 -I code/round3/referee_novelty/novelty_checks.py data/round3/S0/kitamura_excerpts/p2_exact_table_1_256.csv` (§2.7, F6; under 1 s).
- Clones used in scratch (`/tmp/r3_ref_novelty/`): `kp2` (Kitamura p2, `32697193`), `te` (teorth, `86c3dc3e`), `fc` (formal-conjectures main, `e47a327f`), `pl` (plasma-ai/erdos, `94b8ab00`).
