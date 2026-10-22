# Round 3, final editorial pass: consistency and cross-references (2026-10-13)

Lens: (1) identical round-3 numbers everywhere; (2) every reference inside §11 and the [Round 3] passages points to something that exists and says what is claimed; (3) stale statements in note.md / README.md that round 3 supersedes and that still read as current.

Read-only pass. No file other than this report was written; no git command was run. Every "current text" below is an exact substring of the named file (each checked with `grep -cF` to occur exactly once). Line numbers refer to the files as of this pass.

## Summary

- **Numbers (1): consistent.** 90394, 89804, 221465, 203812, 32768, $2^{1/80}G^{-1/80}$ with $G\ge2^{3072}$, 0.10051 at $G\ge2^{37}$, 17 865 943 312, the "about 29 times" comparison with 616 067 009, $\sup\rho_d\le1.3203/1.1760/1.8377/1.2064$ and $\Lambda'_7=2.0496$ agree across the header and status lines (l.14), §0 items 19–23, §11.0, §11.1–11.6 and §11.8, Remark 10.8.4, and README (status bullets and the "New in round 3" table). Arithmetic checks: $v_2(594!)=590$, $v_2(17662!)=17653$, $v_{29}((29^8-1)!)=17\,865\,943\,312$, $v_{31}((31^7-1)!)=917\,087\,130$, the four shadow excesses, and $1/16+0.02854=0.09104$ (Theorem 11.9 against Corollary 11.8 at $2^{40}$) are all correct. **Two track reports still carry superseded values** (R3Q.md: 0.1005 and other rounded-down bounds; R3F.md: $\Lambda'_7=2.0509$). See M17 and N30.
- **References (2): all targets exist.** One target does not say what is claimed: Theorem 3.11 is cited for "the tail set [from 3] ... never being full" (M9). Four citations are loose (N18, N19, N22, N23).
- **Stale statements (3): 8 must-fix in note.md, 7 in README.md** (M1–M8, M10–M16). Of the README items, three are round-3 referee fixes that were applied in the note but not in the README (novelty F3, F11(b); logic F1).
- Totals: **17 must-fix, 32 nice-to-fix.**

---

## Must-fix

### M1. note.md l.71 (§0 item 9): $f(1,29)\ge616\,067\,009$ still reads as current
Current:
```text
are superseded by item 14 below and §10.2.
```
Replacement:
```text
are superseded by item 14 below and §10.2. **[Round 3]** The bound $f(1,29)\ge616\,067\,009$ is superseded by item 23 ($f(1,29)\ge17\,865\,943\,312$, §11.5).
```
Why: l.68 lists $f(1,29)\ge616\,067\,009$, and the only pointer (Round 2) names other primes.

### M2. note.md l.29 (§0 status labels): "floating point" exception for the shell sums
Current:
```text
only the dominant shells were also computed in interval arithmetic. They are labelled accordingly.
```
Replacement:
```text
only the dominant shells were also computed in interval arithmetic. They are labelled accordingly. **[Round 3]** This exception no longer applies: every shell of §10.4.1 is now certified in interval arithmetic (§11.4(e)).
```

### M3. note.md l.75 (§0 item 10): "because Theorem 10.1 gives no rate"
Current:
```text
The census values remain the best *explicit* bounds, e.g. $f(a,2)\le v_2(a!)+31$ on density $0.8984$, because Theorem 10.1 gives no rate.
```
Replacement:
```text
The census values remain the best *explicit* bounds, e.g. $f(a,2)\le v_2(a!)+31$ on density $0.8984$, because Theorem 10.1 gives no rate. **[Round 3]** Theorem 11.7 now gives an explicit, very weak rate ($\delta_G(2)\le2^{1/80}G^{-1/80}$ for $G\ge2^{3072}$), and Corollary 11.8 gives $\delta_G(2)\le0.10051$ for $G\ge2^{37}$. At every evaluated $G\le2^{36}$ the census value remains the best explicit bound (§11.2).
```

### M4. note.md l.662 (§4.4): "The rows $p\ge29$ are unchanged."
Current:
```text
The rows $p\ge29$ are unchanged.
```
Replacement:
```text
The rows $p\ge29$ are unchanged in round 2.
>
> **[Round 3]** The row $p=29$ is superseded by Theorem 11.25: $f(1,29)\ge17\,865\,943\,312$ (§11.5). At $p=31$ the round-3 uniform certificates give only $917\,087\,130$, so the row $p=31$ stands.
```
Why: §11.5 cites "§4.4" for the previous bound, and the §4.4 table (l.653) still shows 616 067 009 as current.

### M5. note.md l.732 (§4.7): "Theorem 10.1 gives no rate"
Current:
```text
The table's $p=2$ row is therefore a decreasing sequence with limit $0$; Theorem 10.1 gives no rate.
```
Replacement:
```text
The table's $p=2$ row is therefore a decreasing sequence with limit $0$; Theorem 10.1 gives no rate. **[Round 3]** Theorem 11.7 gives an explicit (very weak) rate, and Corollary 11.8 improves on $\delta_{32}(2)=0.1016$ only for $G\ge2^{37}$ (§11.2).
```

### M6. note.md l.1503 (§10.4.1): shells $k\ge5$/$k\ge6$ "not interval arithmetic"
Current:
```text
Shells $k\ge5$ (respectively $k\ge6$) rest on floating point with margins, not interval arithmetic. Their total is below $1.1\cdot10^{-8}$ (respectively $2\cdot10^{-7}$), far from any threshold.
```
Replacement:
```text
Shells $k\ge5$ (respectively $k\ge6$) rest on floating point with margins, not interval arithmetic. Their total is below $1.1\cdot10^{-8}$ (respectively $2\cdot10^{-7}$), far from any threshold. **[Round 3]** Every shell of this table, including these, is now certified in interval arithmetic by two implementations plus the checker's third (§11.4(e)): $\sum_{k\le7}T_{13}(k)\le9.29878581108\cdot10^{-3}$ and $\sum_{k\le8}T_{11}(k)\le6.68544967911\cdot10^{-2}$.
```
Why: §10.6 l.1655 has its "[Round 3: done]" pointer, but §10.4.1, where the caveat is stated, has none. See also N11 (the heading label).

### M7. note.md l.1634 (§10.6): "$a=594$ remains a live test case."
Current:
```text
$a=594$ remains a live test case.
```
Replacement:
```text
$a=594$ remains a live test case. **[Round 3: resolved, $f(594,2)=90394$ (Theorem 11.2).]**
```
Why: the section-level note at l.1630 ("Superseded in part") does not say which part. This sentence is now false.

### M8. note.md l.1648 (§10.6 item 3): "a rate for $\delta_G(2)$" still listed as open
Current:
```text
3. *For Q1 at $p=2$:* a rate for $\delta_G(2)$. Theorem 10.1 is qualitative.
```
Replacement:
```text
3. *For Q1 at $p=2$:* a rate for $\delta_G(2)$. **[Round 3: an explicit, very weak rate is now Theorem 11.7; see §11.6 item 3.]** Theorem 10.1 is qualitative.
```

### M9. note.md §11.4(b), l.2060: Theorem 3.11 cited for something it does not prove
Current:
```text
This is numerical evidence [heuristic] that the tail set has positive Haar measure while never being full (Theorem 3.11).
```
Replacement:
```text
This is numerical evidence [heuristic] that the tail set from 3 has positive Haar measure, although the tails $E_N$ with $81\mid N$ are never full (Theorem 3.11).
```
Why: Theorem 3.11 proves non-fullness only for $E_N$ with $81\mid N$. Whether $E_3$ (or $E_{27}$) is full is open (§5, the discussion after Conjecture 5.5: track F conjectures $E_{27}=3^{13}\mathbb Z_3$). R3F.md (l.256, l.540) has the correct form.

### M10. README.md l.33: "Each of six tracks was checked"
Current:
```text
Each of six tracks was checked by a separate AI instance that wrote its own code.
```
Replacement:
```text
Each of the five research tracks (R3N, R3Q, R3M, R3F, R3C) was checked by a separate AI instance that wrote its own code; the status gate S0 was not, except that its Lemma S0.1 was checked by the round-3 logic referee.
```
Why: this is novelty-referee F3. It was applied in the note (l.11, l.1819, l.1838, §8) but not here. As written, the sentence contradicts note §11.8 ("The status gate S0 was not checked") and README l.231.

### M11. README.md l.37 (round-3 table, row 1): "largest excess known"
Current:
```text
the largest excess $g_2=203812$ known
```
Replacement:
```text
the largest exactly computed value of $g_2$ at a natural number in the public record ($g_2=203812$)
```
Why: this is novelty-referee F11(b). It was applied in note item 19 and §11.0 but not here. Finite values of $g_2$ are unbounded (Proposition 3.4).

### M12. README.md l.37 (row 1, status column): "verified exactly by three verifiers"
Current:
```text
plus an explicit witness verified exactly by three verifiers
```
Replacement:
```text
plus an explicit witness verified exactly (by three verifiers for 594 and 17662; for every other row, by the track's GMP verifier and by the checker's own verifier)
```
Why: in note Theorem 11.2, three verifiers are used only for 594 and 17662. Theorem 11.4 has, for the other 16382 rows, C's witness checked by GMP and D's witness checked by D's own verifier. Note item 19 avoids a count.

### M13. README.md l.40 (row 4): "of barrier type" unlabelled
Current:
```text
proved (FE unproved; of barrier type; numerically plausible at $p\ge5$, doubtful at $p=3$)
```
Replacement:
```text
proved (FE unproved; heuristically of barrier type; numerically plausible at $p\ge5$, doubtful at $p=3$)
```
Why: this is logic-referee F1. It was applied in note item 21, §11.0 item 3 and §11.3, but not here.

### M14. README.md l.73 (round-2 table, Thm 10.1): "$a=594$ is still a live test case"
Current:
```text
It says nothing about any particular $a$; $a=594$ is still a live test case.
```
Replacement:
```text
It says nothing about any particular $a$. *(Round 3: Kitamura's live test case $a=594$ is now resolved, $f(594,2)=90394$; note.md Thm 11.2.)*
```
Why: this sentence is now false. It is also logic-referee F16, which was only partly applied.

### M15. README.md l.80 (round-2 table, §10.4 status): "shell sums in floating point"
Current:
```text
proved; shell sums in floating point with outward margins by three implementations, dominant shells also in interval arithmetic
```
Replacement:
```text
proved; shell sums in floating point with outward margins by three implementations, dominant shells also in interval arithmetic *(round 3: all shells now certified in interval arithmetic, note.md §11.4(e))*
```

### M16. README.md l.121 (round-1 table): $f(1,29)\ge616\,067\,009$
Current:
```text
*($p=17,19,23$ superseded in round 2)*
```
Replacement:
```text
*($p=17,19,23$ superseded in round 2; $p=29$ superseded in round 3: $f(1,29)\ge17\,865\,943\,312$)*
```

### M17. data/round3/reports/R3Q.md: rounded-down upper bounds (check F1 not applied)
Current (title line):
```text
# Track R3Q (round 3, 2026-10-13, restarted): an explicit rate for $\delta_G(2)\to0$
```
Replacement:
```text
# Track R3Q (round 3, 2026-10-13, restarted): an explicit rate for $\delta_G(2)\to0$

*Edited by the lead after the check (`data/round3/checks/R3Q.md`, F1): the prose bounds $0.1005$, $0.0910$/$0.091$, $4.9\cdot10^{-6}$ and $0.0285$ below are rounded to nearest and lie slightly below the exact bounds $0.1005059$, $0.0910330$, $4.9359\cdot10^{-6}$ and $0.028533$. The rounded-up values $0.10051$, $0.09104$, $4.94\cdot10^{-6}$ and $0.02854$ are those of note.md Corollary 11.8 and Theorem 11.9. The tables round to nearest.*
```
Why: the R3Q check's F1 rates this "must fix". The report still says "$\delta_G(2)\le0.1005$ for $G\ge2^{37}$" (l.16, l.348, l.393, l.402, l.411), which is slightly false as a proved bound and contradicts note and README (0.10051). Note §11.8 states that the checks' rounding corrections "are applied in §11 and in the marked edits of the track reports". The report itself carries only the referee's 0.912 edit. An alternative is to reword §11.8 (N31).

---

## Nice-to-fix

### N1. note.md l.11: list of updated sections
Current: `and updates the summary (§0), §2, §5 and §10 where they are superseded`
Replacement: `and updates the summary (§0), §2, §4, §5, §8 and §10 where they are superseded`
Why: §8 already carries a [Round 3] block (l.954), and §4 will after M4/M5.

### N2. note.md l.16: "conditional and structural results only"
Current: `Round 3 adds conditional and structural results only (§11.3–11.5).`
Replacement: `Round 3 adds conditional, structural and computational results only (§11.3–11.5).`
Why: §11.5 is a certified lower bound ($f(1,29)$), which is neither conditional nor structural.

### N3. note.md l.14: theorem cited for 594
Current: `including Kitamura's test case $f(594,2)=90394$ (Theorem 11.4, computer-assisted)`
Replacement: `including Kitamura's test case $f(594,2)=90394$ (Theorems 11.2 and 11.4, computer-assisted)`
Why: the value and its certification table are in Theorem 11.2. Theorem 11.4 only refers to it.

### N4. README.md l.9: same
Current: `and $f(17662,2)=221465$ (note.md Theorem 11.4; computer-assisted)`
Replacement: `and $f(17662,2)=221465$ (note.md Theorems 11.2 and 11.4; computer-assisted)`

### N5. note.md l.51 (§0 item 3): shadow values "up to $t=13$"
Current: `(At $p=2$, Kitamura's shadow family $a=2^t-2$ already has $g\ge3t$, with exact finite values up to $t=13$.)`
Replacement: append ` **[Round 3]** Exact values now reach $t=17$, and the largest exactly computed finite value is $g_2(17662)=203812$ (§11.1).`

### N6. note.md l.82 (§0 heuristics)
Current: `**[Round 2: "almost all" is now Theorem 10.1. "All" remains open.]**`
Replacement: `**[Round 2: "almost all" is now Theorem 10.1. "All" remains open.] [Round 3: verified for every $a\le32768$, Theorem 11.4.]**`

### N7. note.md l.784 (§5, Conjecture 5.3 evidence)
Current: `whose registered predictions were confirmed. Three of these predictions were genuinely out of sample and test its thresholds; see §10.5 for the exact count.`
Replacement: append ` **[Round 3]** At $p=29,31$, 63 of 64 genuine registered predictions were confirmed and 1 was falsified (§11.5); at $p=29$ covering is certified at every position below $29^8$ (Theorem 11.25).`

### N8. note.md l.804 (§5, H2)
Current: `Corollary 10.20 explains why supremum-type transfer bounds cannot prove the persistence.`
Replacement: append ` **[Round 3]** All of these certified shells are now in interval arithmetic (§11.4(e)), and single gate blocks satisfy a certified per-level bound at every level (Theorem 11.19).`

### N9. note.md l.816 (§6)
Current: `> **[Round 2]** For the updated list of what remains, see §10.6.`
Replacement: `> **[Round 2]** For the updated list of what remains, see §10.6. **[Round 3]** See also §11.6.`

### N10. note.md l.1001 (§9)
Current: `A separate round of three AI referees checked §10; see §10.8.`
Replacement: `A separate round of three AI referees checked §10; see §10.8. **[Round 3]** A third round checked §11; see §11.8.`

### N11. note.md l.1491: §10.4.1 heading label
Current: `**10.4.1 Certified shell sums [computer-assisted; floating point with outward margins, plus interval arithmetic for the dominant shells].**`
Replacement: `**10.4.1 Certified shell sums [computer-assisted; floating point with outward margins, plus interval arithmetic for the dominant shells; Round 3: all shells in interval arithmetic, §11.4(e)].**`

### N12. note.md §10.1.4: Claim 10.9 pointer
Current: `If true, it would give a rate on the three classes it treats, but not for $\delta_G(2)$ itself (see item 4 below). We record it as a claim only.`
Replacement: append ` **[Round 3]** Theorem 11.9 proves a computer-assisted analogue on $8\mathbb Z_2$, $2+16\mathbb Z_2$ and $6+16\mathbb Z_2$, and Theorem 11.7 gives a rate for $\delta_G(2)$ itself (§11.2).`

### N13. note.md l.1611 (§10.5, Conjecture 10.24 predictions)
Current: `Only $104$ of the $312\,500$ classes of $(5,5,39)$ were checked, all covered.`
Replacement: append ` **[Round 3]** 64 further genuine registered predictions at $p=29,31$: 63 confirmed, 1 falsified (uniform $\mathrm{Cov}(29,5,36)$ holds, which Lemma 11.26 explains); 48 more classes of $(5,5,39)$ were covered (§11.5).`

### N14. note.md l.1646 (§10.6 item 1)
Current: `A first, insufficient step would be a rigorous version for single gate blocks, by Weyl–Kronecker equidistribution plus a finite check.`
Replacement: append ` **[Round 3: done by a different route (the Poisson/carry formula), Theorems 11.18–11.19.]**`

### N15. note.md l.1647 (§10.6 item 2)
Current: `A cheaper intermediate target is the $L^2$ analogue, which would give positive Haar measure of the tail set.`
Replacement: append ` **[Round 3: see Proposition 11.20 and Theorem 11.22; the $L^2$ hypothesis is unproved.]**`

### N16. note.md l.1649 (§10.6 item 4)
Current: `would give $\mu(K_p)>0$ (Conjecture 5.2). It was not attempted.`
Replacement: `would give $\mu(K_p)>0$ (Conjecture 5.2). It was not attempted in round 2. **[Round 3: the odd-$p$ martingale is Proposition 11.10; the per-window $L^2$ route is closed (Proposition 11.12); $\mu(K_p)>0$ is reduced to the unproved hypothesis FE (Theorem 11.14).]**`

### N17. note.md l.1653 (§10.6 item 5)
Current: `   - depth-7 positions at $p=29,31$;`
Replacement: `   - depth-7 positions at $p=29,31$ **[Round 3: done at $p=29$, Theorem 11.25; not run at $p=31$]**;`

### N18. note.md §11.3 l.2022: Theorem 3.6 cited for "would not put a natural number in $K_p$"
Current: `Even an unconditional $\mu(K_p)>0$ would not put a natural number in $K_p$ (Theorem 3.6).`
Replacement: `Even an unconditional $\mu(K_p)>0$ would not put a natural number in $K_p$: $\mathbb N$ is countable, hence Haar-null (compare Remark 10.8.5); $K_p$ is also nowhere dense (Theorem 3.6).`
Why: Theorem 3.6 states only that $K_p$ has empty interior. The operative reason is countability, as Remark 10.8.5 says. (§5 l.767 has the same pre-existing phrasing.)

### N19. note.md §11.3 l.2018: Proposition 3.4 part
Current: `because of the double root of $S_{\{1,2\}}=(x+2)^2$ at $-2$ (Proposition 3.4).`
Replacement: `because of the double root of $S_{\{1,2\}}=(x+2)^2$ at $-2$ (Proposition 3.4(b) and its proof).`
Why: 3.4(a) is the cube $S_{\{1,3\}}$. The square appears only in the proof of (b).

### N20. note.md §11.4(b) l.2057: unnamed "$L^2$ budget"
Current: `- The $L^2$ budget converges at every odd $p$, including $p=3,5$, where the $L^1$ budget fails.`
Replacement: `- The $L^2$-mass budget $\sum_dN_d2^{-U_d}$ converges at every odd $p$, including $p=3,5$, where the $L^1$ budget fails (unlike the Cauchy–Schwarz budget $\Lambda'_p$ below, which is infinite at $p=3,5$).`
Why: Theorem 11.22 says "$\Lambda'_p=\infty$ for $p=3,5$". Without the name, the two statements read as contradictory (R3F B2 distinguishes $\Lambda2_p$ from $\Lambda'_p$).

### N21. note.md §11.2 l.1934: $C_2$ differs from Claim 10.9's $C_2$
Current: `Notation of §10.1. $C_r$ denotes a residue class: $C_0=8\mathbb Z_2$, $C_2=2+16\mathbb Z_2$, $C_6=6+16\mathbb Z_2$, $C_{14}=14+16\mathbb Z_2$.`
Replacement: append ` (Claim 10.9 uses the larger $C_2=2+8\mathbb Z_2$; here $10+16\mathbb Z_2$ is handled by Lemma 11.5.)`
Why: Theorem 11.9 is explicitly compared with Claim 10.9, which uses the same symbol for a different class.

### N22. note.md §11.5 l.2106: converse of Lemma 11.26
Current: `Combine the two layers. The converse is Lemma 10.11(c).`
Replacement: `Combine the two layers. The converse is the layer obstruction of Lemma 10.11 ((c) with (d): $\mathrm{Cov}(p,t,H)$ requires $(H-1)\bmod p\ge\rho_0(p)$).`
Why: (c) alone is the generic "miss mod $p^k$ implies failure". The statement used is the "Hence" after (d).

### N23. note.md §11.6 l.2127: "the items of §10.6"
Current: `1. *Q3:* the items of §10.6, plus the $L^2$ hypothesis of Theorem 11.22.`
Replacement: `1. *Q3:* items 1–2 of §10.6, plus the $L^2$ hypothesis of Theorem 11.22.`
Why: §10.6 items 3–5 are not about Q3, and some of them were done in round 3 (the rate, the $p=29$ positions, the interval shells).

### N24. note.md §11.6 l.2128: "$p\ge7$, where the fine-scale masses decay"
Current: `The most promising case is $p\ge7$, where the fine-scale masses decay numerically.`
Replacement: `The most promising case is $p\ge7$: the fine-scale masses decay numerically at $p=5$ and $7$ (not visibly at $p=3$), and the slope-0 part carries most of the surviving set at larger $p$ (§11.3).`
Why: §11.3, item 21 and the README say that FE is plausible at $p\ge5$, so the current clause implies the masses do not decay at $p=5$.

### N25. README.md l.96: Claim 10.9 "gives no rate"
Current: `This is unverified, and it has a $1/16$ floor, so it gives no rate for $\delta_G(2)$;`
Replacement: `This is unverified, and it has a $1/16$ floor, so it gives no rate for $\delta_G(2)$ (round 3 proves a rate by another route, Thm 11.7, and a computer-assisted analogue of the claim, Thm 11.9);`

### N26. README.md l.97: prediction count
Current: `three were genuine out-of-sample tests, and all three were confirmed.`
Replacement: `three were genuine out-of-sample tests, and all three were confirmed (round 3: of 64 further genuine predictions, 63 were confirmed and 1 was falsified; note.md §11.5).`

### N27. README.md l.132: evidence for Conjecture 5.1
Current: `Evidence for the strong form: exact densities to $G=32$ and Monte Carlo to $G=254$; but a measure-theoretic argument cannot see a countable set.`
Replacement: `Evidence for the strong form: exact densities to $G=32$, Monte Carlo to $G=254$, and (round 3) exact finite values for every $a\le32768$ (Theorem 11.4); but a measure-theoretic argument cannot see a countable set.`

### N28. README.md l.133: Conjecture 5.2
Current: `numerically $\mu(K_3)\approx0.36$, $\mu(K_5)\approx0.52$, $\mu(K_7)\approx0.62$.`
Replacement: append ` Round 3 reduces it to an unproved fine-scale equidistribution hypothesis FE (Theorem 11.14).`

### N29. README.md l.37: "Kitamura's exact table reached $a\le256$"
Current: `Kitamura's exact table reached $a\le256$ |`
Replacement: `Kitamura's complete exact table covered $a\le256$, plus isolated rows up to 8190 |`
Why: this is novelty-referee F11(c). It was applied in note §11.0 and §11.1 but not here.

### N30. data/round3/reports/R3F.md l.233 (and the table at l.226): $\Lambda'_7$
Current: `- Λ'_7 = 2.0509 (computed, with a rigorous geometric tail bound).`
Replacement: `- Λ'_7 = 2.0496 (2.04957; 2.0509 is the upper end of the D = 60 enclosure; corrected after the check).`
Also, in the table row `| Λ'_p = Σ N_d 2^{−U_d/2} (Cauchy–Schwarz) | ∞ | ∞ | 2.0509 |`, change `2.0509` to `2.0496`.
Why: this is R3F check B2. The note uses 2.0496 twice. As an upper bound 2.0509 is not wrong, but it disagrees with the note's stated value.

### N31. data/round3/reports/R3N.md §6: source of Kitamura's figure
Current: `(Kitamura does not state the normalisation; the figure comes from the class census)`
Replacement: `(Kitamura states neither how the figure was measured nor its normalisation; it is not a fit to the g ≤ 24 census; corrected after the round-3 novelty referee, note §11.1)`
Why: this is novelty-referee F1. The note was corrected (§11.1, §11.8), but the report still asserts the opposite.

### N32. note.md §11.8 l.2156: alternative to M17/N30/N31
Current: `and all are applied in §11 and in the marked edits of the track reports.`
Replacement (only if M17, N30 and N31 are not applied): `and all are applied in §11. The track reports keep their original wording and rounding except where an edit is marked; R3Q.md's prose bounds are rounded to nearest, and Corollary 11.8 gives the rounded-up values.`

---

## Cross-references checked and found correct (no action)

Each of these targets exists and says what the citing text claims:
- Lemma 1.3(iii); Proposition 1.2 (König).
- Theorem 3.1(a). Corollary 3.7.1(i) and (iii). Proposition 3.4(c) ("finite values unbounded").
- Theorem 3.9(b), the gate congruence (Lemma 11.16). Theorem 3.10 (Proposition 11.23; §11.4(a)). Theorem 3.12(c).
- §4.5 (frontiers $11^{14997}$, $13^{12498}$, $7^{283331}$, with re-run status as stated in §11.4(b)). §4.7 ($\delta_{32}(2)=0.1016$).
- Lemma 10.5 and Proposition 10.6 (W1–W3). §10.1.3 (sketch only). $K^{k,L}$ in the proof of Theorem 10.1 (l.1197).
- Remark 10.8.2 (now corrected for natural $x$; supports §11.6 item 4). Remark 10.8.4 (the "0.7/√G" fit and the unreconciled 11.5/G).
- Claim 10.9. Proposition 10.10 ($D=8$). Lemma 10.11 and $\rho_0$. Theorem 10.16. Theorem 10.18. Proposition 10.19. Corollary 10.20.
- Conjecture 10.23 evidence (ratio ≈1.17, with its [Round 3] pointer to Theorem 11.18). Conjecture 10.24.
- §10.4.1 and the §10.6 shell-sum item (l.1655).
- Inside §11: Theorems 11.2, 11.4, 11.7, 11.9, 11.14, 11.17–11.19, 11.22 and 11.25; Lemmas 11.5, 11.6, 11.16 and 11.26; Propositions 11.10–11.13, 11.15, 11.20, 11.21, 11.23 and 11.24; Corollary 11.8.
- Report pointers: R3N.md Lemmas 1–2 and §6; R3Q.md §§1–8 and "Provenance" (l.33); R3M.md Lemma C4, Remark C6 and §8 (computational record); R3F.md "Reproduction"; S0.md Lemma S0.1 and the $[0.607,0.693]$ table.
- Track and check counts: 16382 other rows; 68 certificate logs; 7680 comparisons; 63/1/11/20/4/21 predictions; 06:12:36 UTC; 17/4/12 referee findings.
