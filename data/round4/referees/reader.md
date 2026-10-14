# Round-4 referee report: fresh reader and consistency

Date: 2026-10-14. Role: FRESH READER AND CONSISTENCY. Classification: Internal (research working file).
Code: `code/round4/referee_reader/` (`qs_check.py`). Scratch: `/tmp/r4_ref_reader/`. Budget used: under 2 core-minutes.

**Read as a newcomer.** README.md in full. note.md: the header and §0 (with items 21, 24 and 25), §5 (H1 and Conjecture 5.2), §8's [Round 4] paragraph, §9's closing paragraph, §10.6 item 4, §11.0 item 3, §11.3 (for the definitions §12 relies on), the [Round 4] blockquote after Theorem 11.14, §11.6, and §12 in full.
**Cross-checked against:** `data/round4/reports/M4{A,B,C,D}.md`, `data/round4/checks/*.md`, and the logs `data/round4/M4A/fe_verify_final.log`, `data/round4/M4D/plateau_bounds.log`, `data/round4/verify_D_P_recompute/bounds.log`.
**Not repeated:** the novelty referee's credit findings. The placeholder in §12.7 is not flagged.

## Verdict

**No fatal finding. One serious finding, 22 minor ones.**

- **Headline numbers.** They are identical wherever they appear (README, header, §0 items 24–25, §5, §11, §12) and agree with the logs: 7, 97, $1.843\cdot10^{-26}$, $7^{51}$, $1.46\cdot10^{-69}$, the 21 values of $c_p$, 0.69, the five constants of Corollary 12.3, and $q_1(7)=8309/8192$, $q_2(7)=4557/4096$.
- **References.** Every theorem and section reference in §12 points to something that exists, with one exception (finding 12).
- **No overstatement of the main result.** Q3 is said to be untouched everywhere. Theorem 12.1 is labelled computer-assisted, as resting on Theorem 11.14, and as AI-verified and not human-refereed, everywhere it is stated.
- **Math syntax.** Every `$` is paired and every brace balanced in the parts read.

**The serious finding.** Theorem 12.11 prints the certified plateau bound $\delta_G(11)\ge0.6896$. This is rounded *up*. The certified value is $0.689545$.

**The minor findings fall into seven groups:**
- a garbled description of M4A's phases (finding 2);
- a verification count that overstates the checking of Theorem 12.11 (finding 3);
- six statements outside §12 that are now stale and have no [Round 4] pointer (findings 4–8 and 23);
- missing notation for the newcomer (findings 9–11, 15, 16);
- one wrong pointer and two imprecise sentences in §12.0–12.1 (findings 12–14);
- README and reproduction gaps (findings 17–20);
- a phrasing that a verifier fix should have removed, and an incomplete "unverified" list (findings 21, 22).

## What I checked, and how

| item | result | how |
|---|---|---|
| $1.843\cdot10^{-26}$, $\Pi_A\le10^{25.7344}$, $\delta_A\le1.0006\cdot10^{-45}$, $\Pi_A\delta_A\le10^{-19.265}$ ($p=7$) | consistent in §12.0, Theorem 12.2 and the log | re-ran `code/round4/M4A/fe_verify.py data/round4/M4A/atom_p7.txt 8 60000` (read-only, 1.3 s): `log10 Pi_A <= 25.7344`, `delta_A <= 1.000520e-45`, `log10(Pi_A delta_A) <= -19.2654`, ratio `>= 1.8434e-26` |
| $1.46\cdot10^{-69}$ | correct | $1.843\cdot10^{-26}\cdot7^{-51}=1.4639\cdot10^{-69}$ (exact rational); also $(1-\sqrt{10^{-19.265}})^2/10^{25.7344}=1.8433\cdot10^{-26}$ |
| Corollary 12.3: $1.05\cdot10^{-4}$, $4.89\cdot10^{-2}$, $3.48\cdot10^{-3}$, $1.09\cdot10^{-1}$, $2.06\cdot10^{-1}$; margins $10^{16.6}$ to $10^{21.9}$ | all rounded down from the log ($1.0587\cdot10^{-4}$, $4.8954\cdot10^{-2}$, $3.4825\cdot10^{-3}$, $1.0909\cdot10^{-1}$, $2.0671\cdot10^{-1}$); margins $-16.63$ to $-21.92$ | `fe_verify_final.log` |
| $c_p$ table (21 primes), $c_p\ge0.69$ for $17\le p\le97$ | identical to M4C §7.3; the minimum is $0.691999$ at $p=41$ | re-ran `code/round4/M4C/assemble.py p 0.05 3000 1.6` for $p=11,13,41$ (read-only, about 6 s each): $c_{11}\ge1.25\cdot10^{-4}$ with $\Pi_A\le10.6182$; $c_{13}\ge0.572777$; $c_{41}\ge0.691999$ |
| $\mu(K_{13})\ge2.6\cdot10^{-4}$ (§12.0) | correct | $0.572/13^3=2.60\cdot10^{-4}$; `assemble.py` prints $2.607\cdot10^{-4}$ |
| $q_1,q_2$ examples in §12.1 | all correct | own code `qs_check.py`, written from the definition in §12.1. $p=7$: $8309/8192$, $4557/4096$. $p=13$: $q_1-1=2.20\cdot10^{-5}$, $q_2-1=8.12\cdot10^{-3}$. $p=23$: $q_1-1=5.42\cdot10^{-9}$, $q_2-1=2.26\cdot10^{-6}$ |
| plateau bounds (Theorem 12.11, §0 item 25, README) | $\delta_G(7)\ge0.6119$, $\delta_G(13)\ge0.7431$ and $\delta_G(13)\ge0.6531$ are correct. **$\delta_G(11)\ge0.6896$ is not** (finding 1) | `verify_D_P_recompute/bounds.log` |
| $2.47\cdot10^{-94}$, $4\cdot10^{42}$, $1.45\cdot10^{-9}$, rate survey $7\le p\le211$, $10^{-2.6\cdot10^{58}}$, 99.6%, $1.5\cdot10^6$ cases, level 219, 4118 trials, 37 of 38 certificates | each matches its source | M4A §6; `M4A_obstruction.md` (§3, row R); `M4C_logic.md` §8; `M4C_obstruction.md` §2.3; `M4A_falsify.md` (the Lemma Q row, 1,525,715 cases); `M4C_falsify.md` (the H2 row); `M4D_P.md` |
| "298 windows" (Theorem 12.2) | wrong count, inconsistent phase labels (finding 2) | `fe_verify_final.log`: phase 2 is $\ell=9..16$ and phase 3 is $\ell=17..306$ |
| references in §12 | all exist, except the location given for "Remark C6" (finding 12) | grep for every theorem, proposition, lemma and section number cited |
| §12.6 file paths | all exist; one command lacks its required arguments (finding 17) | `ls`; the usage string of `fe_verify.py` |

## Findings

### 1. [serious] Theorem 12.11 prints a certified plateau bound rounded up (note.md §12.4)

Current text (occurs once):
> `\delta_G(11)\ge0.6896\ (G\le19488)`

Fix:
> `\delta_G(11)\ge0.6895\ (G\le19488)`

**Why.** The bound is $B_{11}-(N-n_0)11^{-7}$, evaluated at the largest $N$ with $v_{11}(N!)=19488$ ($N=194904$, loss $0.0100000$).
- With M4D's $B_{11}=0.6995451$, this is $0.689545$ (`data/round4/verify_D_P_recompute/bounds.log`, row `11 | 0.01 | 194904 | ... | 19488 | 0.689545`).
- Even with the exact census value, $B_{11}=0.6995525$, the bound is $0.68955<0.6896$. The smallest $N$ with the same $G$, which is $N=194898$, gives $0.68955$ too.
- The printed $0.6896$ is $0.68955$ rounded half-up. Neither the M4D report nor its verifier prints it; only the lead's summary does.

So "$\delta_G(11)\ge0.6896$" is not certified. This is the same kind of defect as the three constants of Corollary 12.3 that the verifiers required to be rounded down (§12.7 (iv)). After the fix, the sentence "The verifier ... reproduced every number" is true. The other three plateau bounds are correctly rounded down ($0.6119076$, $0.7431645$, $0.6531645$).

### 2. [minor] Theorem 12.2's certificate structure: wrong window count, a misattributed proposition, and phase labels that clash with §12.0 and §12.6 (note.md §12.2)

Current text (occurs once):
```
*Structure of the certificate* (M4A report §6). The windows are handled in four phases:
- (i) the first 8 windows get pointwise thresholds;
- (ii) later windows use Markov's inequality with $\bar\varepsilon_\ell=2^{-(\ell-8)}$ and explicit averaged bounds (Propositions D, E and E′);
- (iii) 298 windows up to $4\cdot10^{42}$ are handled with exact $D$, $K$;
- (iv) beyond that, random deep gates are truncated by an event of measure $\le2.47\cdot10^{-94}$, and a closed-form tail argument covers the rest.

The evaluation uses interval arithmetic (mpmath, 200 bits). A second, exact-rational code path reproduces phases (i)–(ii).
```
Fix:
```
*Structure of the certificate* (M4A report §6; phases numbered as there). Phase 0 bounds $\chi^2_0$ by Proposition D. Then:
- phase 1: the first 8 windows get pointwise thresholds $\bar\varepsilon_\ell$ from Proposition D;
- phase 2: windows $9\le\ell\le16$ get $\bar\varepsilon_\ell=2^{-(\ell-8)}$, Markov's inequality and the averaged bound of Proposition E;
- phase 3: the next 290 windows ($17\le\ell\le306$, up to time $\approx4\cdot10^{42}$) are handled the same way, with Proposition E′ and exact $D$, $K$;
- phase 4: beyond that, random deep gates are truncated by an event of measure $\le2.47\cdot10^{-94}$, and a closed-form tail argument covers the rest.

The evaluation uses interval arithmetic (mpmath, 200 bits). A second, exact-rational code path reproduces phases 0–2.
```
**Why.**
- *The count.* The log (`fe_verify_final.log`) labels $\ell=9..16$ as phase 2 and $\ell=17..306$ as phase 3. So phase 3 has 290 windows. The figure 298 is phases 2 and 3 together, which overlaps item (ii).
- *Proposition D* gives the pointwise thresholds of phases 0–1, not the Markov phase.
- *Labels.* §12.0 says the verifiers recomputed "phases 3–4", and §12.6 says `fe_crosscheck.py` covers "phases 0–2". Both use M4A's numbering, which a reader cannot match to (i)–(iv). The fix uses M4A's numbering throughout.

### 3. [minor] The section header overstates how Theorem 12.11 was verified (note.md §12, opening blockquote)

Current text (occurs once):
> `> - every main claim of every track (Theorems 12.2, 12.4, 12.5 and 12.9–12.11, Corollary 12.3 and Proposition 12.6) was adversarially verified by two or three separate AI instances, each using a different lens and writing its own code (`data/round4/checks/`); Propositions 12.7 and 12.12 and Lemma 12.8 were checked only by their tracks;`

Fix:
> `> - every main claim of every track (Theorems 12.2, 12.4, 12.5, 12.9 and 12.10, Corollary 12.3 and Proposition 12.6) was adversarially verified by two or three separate AI instances, each using a different lens and writing its own code (`data/round4/checks/`); Theorem 12.11 was checked by one such instance, under the logic and independent-recomputation lenses (`checks/M4D_P.md`); Propositions 12.7 and 12.12 and Lemma 12.8 were checked only by their tracks;`

**Why.** Theorem 12.11 (M4D Theorem P and Corollary P1) has exactly one verifier report, `checks/M4D_P.md`, written by the single track `verify_D_P_recompute`. Every other listed claim has two or three. §12.7 already describes the check correctly ("logic and independent recomputation"). The header line "Every main claim was adversarially verified by two or three separate AI instances", §8's "two or three adversarial verifiers per main claim", and README lines 36 and 248 are acceptable only if Theorem 12.11 is not counted as a main claim. The blockquote counts it explicitly.

### 4. [minor] Stale: README "What is conjectural" still describes Conjecture 5.2 as reduced to an unproved FE

Current text (README.md, occurs once):
> `Round 3 reduces it to an unproved fine-scale equidistribution hypothesis FE (Theorem 11.14).`

Fix:
> `Round 3 reduces it to an unproved fine-scale equidistribution hypothesis FE (Theorem 11.14). *Round 4 proves it for every prime $7\le p\le97$ (Theorem 12.1; computer-assisted; rests on Theorem 11.14); it remains open at $p=3,5$ and for $p>97$.*`

**Why.** This is the most visible stale statement. The neighbouring bullet, Conjecture 5.1, carries its update ("The weaker form ... is now proved"). This bullet has none.

### 5. [minor] Stale: the README round-3 table still says "FE unproved"

Current text (README.md, occurs once):
> `| proved (FE unproved; heuristically of barrier type; numerically plausible at $p\ge5$, doubtful at $p=3$) |`

Fix:
> `| proved (FE unproved in general; heuristically of barrier type; numerically plausible at $p\ge5$, doubtful at $p=3$). *Round 4: FE verified on explicit atoms for every prime $7\le p\le97$ (Thm 12.1)* |`

### 6. [minor] Stale: note.md §0 item 21 still says "FE unproved"

Current text (occurs once):
> `[proved; FE unproved, heuristically of barrier type, numerically plausible at $p\ge5$ and doubtful at $p=3$].`

Fix:
> `[proved; FE unproved, heuristically of barrier type, numerically plausible at $p\ge5$ and doubtful at $p=3$]. **[Round 4]** FE is now verified on explicit atoms for every prime $7\le p\le97$, so $\mu(K_p)>0$ for these $p$ (Theorem 12.1, item 24).`

### 7. [minor] Stale: note.md §0 lists odd-prime supercriticality under "none of it is proved", without a pointer

Current text (occurs once):
> `- Every odd $p$ is "supercritical", with $\mu(K_p)\approx0.363$ for $p=3$, $0.522$ for $p=5$, $0.624$ for $p=7$ and $0.700$ for $p=11$.`

Fix:
> `- Every odd $p$ is "supercritical", with $\mu(K_p)\approx0.363$ for $p=3$, $0.522$ for $p=5$, $0.624$ for $p=7$ and $0.700$ for $p=11$. **[Round 4: $\mu(K_p)>0$ is now proved for every prime $7\le p\le97$, Theorem 12.1; the numerical values remain heuristic.]**`

**Why.** The bullet just above it, on $p=2$, carries [Round 2] and [Round 3] pointers. This one does not, so §0 says that nothing in the supercritical picture is proved, which contradicts item 24 fifty lines later.

### 8. [minor] Stale: note.md §10.6 item 4 ends at round 3

Current text (occurs once):
> `$\mu(K_p)>0$ is reduced to the unproved hypothesis FE (Theorem 11.14).]**`

Fix:
> `$\mu(K_p)>0$ is reduced to the unproved hypothesis FE (Theorem 11.14).] [Round 4: FE is verified on explicit atoms for every prime $7\le p\le97$, so $\mu(K_p)>0$ for these $p$ (Theorem 12.1).]**`

### 9. [minor] §12 never defines or points to its basic notation

The terms are gate depth, gate pattern ("frozen gate pattern"), the jumps $D$ and $K$, "atom" and "admissible", $\Pi_A$, $\delta_A$ and $V_n$. Also, $q_2(p)$ is used in §12.1 before it is defined.

Current text (note.md §12.0, occurs once):
> `The problem page lists an undated 'Currently working on' reaction (Sky-Yang).`

Fix (append a paragraph):
```
The problem page lists an undated 'Currently working on' reaction (Sky-Yang).

*Notation (from §§1.2, 10.1, 11.3).* For $x\in\mathbb Z_p$: $\pi_c(x)=(x+1)\cdots(x+c)$, $V_n(x)=v(\pi_n(x))$ and $M_n(x)=\max_{i\le n}v(x+i)$. A *gate* of $x$ is a position $i\ge1$ with $p\mid x+i$, and its *depth* is $v(x+i)$. A window's *gate pattern* is the list of the depths of its gates; on a ball where this list is constant, the gate pattern is *frozen*. A window $W=[n,N)$ has *jump* $D=V_N-V_n$, and a composite window $[n,N')$ has $K=V_{N'}-V_n$. The *slope* of a path $e$ is $v(S_e')$. The following are those of Theorem 11.14: the *fine-scale masses* $\varepsilon_\ell$ (Proposition 11.13); an *admissible atom* $A$ (a cylinder $x+p^{V_{n_j}(x)}\mathbb Z_p$ with a nonempty slope-0 population and valid window conditions); $\Pi_A$; $\delta_A$; and the hypothesis FE, $\Pi_A\delta_A<1$. Under FE, $\mu(K_p\cap A)/\mu(A)\ge(1-\sqrt{\Pi_A\delta_A})^2/\Pi_A$. The block constants $q_s(p)$ are defined in §12.1.
```
**Why.** A newcomer meets "depth-1 gate", "frozen gate pattern", "deep gates", "$\delta_A$", "admissible atom" and "exact $D$, $K$" in §§12.1–12.3 with no definition and no pointer.
- *Gate depth.* The only definition of "gate" in the note is §3.5's "gate of level $j$", a property of blocks at natural numbers. It is not the same notion. The definition used in §12 is in the track reports (M4A §1), not in the note.
- *$\Pi_A$, $\delta_A$, atoms, $V_n$.* These are defined in Theorem 11.14 and §10.1, but §12 never says so.
- *Order.* §12.1 uses "$q_2(p)/p^2$" four lines before it defines $q_s(p)$.

### 10. [minor] In Proposition P1, $n_1,n_2$ are undefined and clash with the window times $n_\ell$ (note.md §12.3)

Current text (occurs once):
> `and $\varepsilon_\ell\le q_1^{n_1}q_2^{n_2}-1$ pointwise.`

Fix:
> `and $\varepsilon_\ell\le q_1^{g_1}q_2^{g_2}-1$ pointwise, where $g_1$ and $g_2$ count the gates of depth 1 and 2 in the composite window (before time $p^3$ every gate on $A$ has depth 1 or 2; M4C writes $n_1,n_2$).`

### 11. [minor] In Lemmas T and T′, $G_\ell$ is undefined and clashes with Theorem 12.9's $G_\ell$ (note.md §12.3)

Current text (occurs once):
> `- **Lemmas T and T′ (tail).** Explicit bounds for $\mathbb E_A[\varepsilon_\ell\mathbf 1_{G_\ell}]$ and $\mu_A(G_\ell^c)$ for all later windows`

Fix:
> `- **Lemmas T and T′ (tail).** Here $G_\ell\subseteq A$ is the deep-gate truncation event: no gate up to time $n_{\ell+1}$ has depth $>s_\ell$, for an explicit cap $s_\ell\ge3$, so that $\mu_A(G_\ell^c)\le\lfloor n_{\ell+1}/p^3\rfloor p^{-(s_\ell-2)}$ (M4C Lemma L). Explicit bounds for $\mathbb E_A[\varepsilon_\ell\mathbf 1_{G_\ell}]$ and $\mu_A(G_\ell^c)$ for all later windows`

**Why.**
- In M4C, $n_\ell=b_\ell p$ and Lemma L(a) reads $\lfloor b_{\ell+1}/p^2\rfloor p^{-(s-2)}$, which is the same as the fix.
- Theorem 12.9 (§12.4) uses $G_\ell$ for "the sets ... of well-lifting residues", a different object. Consider renaming one of them, for example $\mathcal L_\ell$ in Theorem 12.9.

### 12. [minor] "Remark C6 (§11.3, §12.0)" points to two places that do not mention Remark C6 (note.md §12.1)

Current text (occurs once):
> `which pointed both at round 3's Remark C6 (§11.3, §12.0).`

Fix:
> `which pointed both at round 3's Remark C6 (R3M's report, `data/round3/reports/R3M.md`; summarised in §11.6 item 2).`

**Why.** A grep finds "Remark C6" in note.md only in §11.6 item 2 and in §12 itself. Neither §11.3 nor §12.0 names it, so a reader following the reference cannot learn what it says.

### 13. [minor] The census comparison in §12.0 is valid only at $11\le p\le23$ but is placed after a claim about $17\le p\le97$

Current text (occurs once):
> `For comparison, the round-1 census values (which are upper bounds for $\mu(K_p)$) give an average density of at most 0.96–0.99 on the residue classes where $g_p$ is not identically $0$, the class of $p^3\mathbb Z_p$ among them.`

Fix:
> `For comparison, at $11\le p\le23$ (the primes where round 1 ran the census) the census values, which are upper bounds for $\mu(K_p)$, give an average density of at most 0.96–0.99 on the residue classes where $g_p$ is not identically $0$, the class of $p^3\mathbb Z_p$ among them (`checks/M4C_obstruction.md`, row T3).`

**Why.** The source (`M4C_obstruction.md` §2.3) gives $0.962$, $0.981$, $0.990$, $0.985$ and $0.985$ at $p=11,13,17,19,23$ only. Round 1 has no census at $p\ge29$. The sentence before is about $17\le p\le97$, so the reader would assume the range carries over.

### 14. [minor] §12.0 gives the wrong reason why a measure statement cannot reach Q3

Current text (occurs once):
> `Theorem 12.1 does **not** bear on Q3. $K_p$ is a closed, nowhere dense set (Theorem 3.6), and a statement about its measure cannot place a natural number in it.`

Fix:
> `Theorem 12.1 does **not** bear on Q3. $\mathbb N$ is countable, hence Haar-null, so a statement about the measure of $K_p$ cannot place a natural number in it; $K_p$ is moreover closed and nowhere dense (Theorem 3.6).`

**Why.** Nowhere density is not the reason. A nowhere dense set of positive measure can contain integers. The reason is that $\mathbb N$ is Haar-null, as §11.3 and M4A's headline say.

### 15. [minor] Proposition 12.6 cites a "round 3 heuristic" whose symbols are not in the note (note.md §12.4)

Current text (occurs once):
> `This proves round 3's heuristic $\kappa\approx p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}$ up to that factor.`

Fix:
> `Here $\varepsilon_{\rm post}=\varepsilon([n+d,N),[N,N'))$ is the fine-scale mass of the composite window restarted at the gate. This proves, up to that factor, the heuristic $\kappa\approx(c_{n+d}/c_n)\,\varepsilon_{\rm post}$ for the cost of a deep gate, which R3M's report (`data/round3/reports/R3M.md`) writes as $p^{v_{\rm pre}}2^{-d}\varepsilon^{\rm post}$; it is not stated in §11.3.`

**Why.**
- $\kappa$, $v_{\rm pre}$ and $\varepsilon^{\rm post}$ do not appear earlier in the note.
- The sentence before writes $\varepsilon_{\rm post}$ (subscript), and this one writes $\varepsilon^{\rm post}$ (superscript).
- M4B §1 defines $\varepsilon^{\rm post}$ as in the fix.

### 16. [minor] $T(p)$ in Theorem 12.11 is undefined (note.md §12.4)

Current text (occurs once):
> `The round-2 uniform covering certificates localise death at gates deeper than $T(p)$.`

Fix:
> `The round-2 uniform covering certificates localise death, after time $n_0=\max_tH_t$, at gates deeper than $T(p)$, where $T(7)=T(11)=T(19)=T(23)=6$ and $T(13)=T(17)=7$ (M4D Theorem P).`

### 17. [minor] The §12.6 command for Theorem 12.2 omits its required arguments

Current text (note.md, occurs once):
> `` - §12.2: `python3 code/round4/M4A/fe_verify.py` (interval arithmetic) and `fe_crosscheck.py` (exact rationals, phases 0–2); the atoms are in `data/round4/M4A/atom_p*.txt`. ``

Fix:
> `` - §12.2: `python3 code/round4/M4A/fe_verify.py data/round4/M4A/atom_p7.txt 8 60000` (interval arithmetic, about 2 s; `atom_pP.txt 6 60000` for $p=11,\dots,23$) and `fe_crosscheck.py data/round4/M4A/atom_pP.txt LMAX L1` (exact rationals, phases 0–2); the atoms are in `data/round4/M4A/atom_p*.txt`. ``

**Why.** The usage of `fe_verify.py` is `ATOMFILE L1 NBLOCK`, and the command as printed does not run. I ran the fixed command; it reproduces Theorem 12.2 in 1.3 s.

### 18. [minor] README's "Reproducing" section has round-3 commands but none for round 4

Current text (README.md, occurs once):
> `` Every round-3 log in `data/round3/` begins with its command line. The track reports are in `data/round3/reports/`, the adversarial checks in `data/round3/checks/`, and the referee reports in `data/round3/referees/`. ``

Fix (append):
````
Every round-3 log in `data/round3/` begins with its command line. The track reports are in `data/round3/reports/`, the adversarial checks in `data/round3/checks/`, and the referee reports in `data/round3/referees/`.

Round 4 (`note.md` §12.6):

```sh
python3 code/round4/M4A/fe_verify.py data/round4/M4A/atom_p7.txt 8 60000   # Theorem 12.2: FE at p = 7 (about 2 s)
python3 code/round4/M4C/assemble.py 41 0.05 3000 1.6                       # Theorem 12.4 at one prime 11 <= p <= 97 (seconds)
```

The track reports are in `data/round4/reports/`, the verifier reports in `data/round4/checks/`, and the referee reports in `data/round4/referees/`.
````

### 19. [minor] README describes Theorem 12.10 as "weighted window times"

Current text (README.md, occurs once):
> `| Thm 12.5–12.12 | Theorem 11.14 with adaptive and with weighted window times;`

Fix:
> `| Thm 12.5–12.12 | Theorem 11.14 with adaptive window times and with weighted windows;`

**Why.** Theorem 12.10 puts adapted probability weights on the window *digit strings*; the window times are unchanged (note.md §12.4; §11.3's blockquote says "weighted windows").

### 20. [minor] README's main row leaves out Corollary 12.3, which its own text relies on

Current text (README.md, occurs once):
> `| Thm 12.1, 12.2, 12.4 |`

Fix:
> `| Thm 12.1–12.4 |`

**Why.** The row says "Two tracks separately cover $11\le p\le23$". The second track's result is Corollary 12.3.

### 21. [minor] The header keeps the phrasing that §12.7 says was reworded

Current text (note.md header, Status, Q2 line; occurs once):
> `i.e. Conjecture 5.2 holds for these $p$`

Fix:
> `i.e. these cases of Conjecture 5.2 hold`

**Why.** §12.7 lists, as an applied fix, that '"Conjecture 5.2 holds for these primes" is reworded'. The M4A verifiers asked for "the cases ... of Conjecture 5.2 hold". The header still has the old phrasing. The variants "This proves Conjecture 5.2 for these primes" (§0 item 24 and README line 11) are harmless, but could be aligned in the same way.

### 22. [minor] §12.7 "What remains unverified" omits the results that only their tracks checked

Current text (note.md §12.7, occurs once):
> `- The secondary results of M4C (Theorems E/F, Lemma D1/Theorem D2, Proposition Q) and of M4D (Proposition F2, Corollary F3) were not verified.`

Fix:
> `- The secondary results of M4C (Theorems E/F, Lemma D1/Theorem D2, Proposition Q) and of M4D (Proposition F2, Corollary F3) were not verified. Propositions 12.7 and 12.12, Lemma 12.8 and M4B's reduction to ($S_B$) were checked only by their tracks.`

**Why.** The section's opening blockquote and the M4B and M4D bullets of §12.7 say that these items were checked only by their tracks. The summary list of what remains unverified should say so too.

### 23. [minor] Stale: §9 does not mention the round-4 referees

Current text (note.md §9, occurs once):
> `**[Round 3]** A third round checked §11; see §11.8.`

Fix:
> `**[Round 3]** A third round checked §11; see §11.8. **[Round 4]** A fourth round checked §12; see §12.7.`

## Checked and found consistent (no action)

- **Scope.** Q3 is said to be untouched in the README (line 11), the header (Q2 and Q3 lines), §0 item 24, §12.0, §12.5 and the credit list. Every statement of Theorem 12.1 is labelled computer-assisted. Each says that it rests on Theorem 11.14, or that it verifies Theorem 11.14's FE. Each says it was AI-verified and not human-refereed. Nothing claims a uniform-in-$p$ result: Corollary M′ is labelled heuristic in §12.3.
- **Pointers.** These stale-candidate places already carry a correct [Round 4] pointer: §5 (Conjecture 5.2), §11.0 item 3, the blockquote after Theorem 11.14, and §11.6 item 2. §10.1.3's remark ("An $L^2$ bound for it would give $\mu(K_p)>0$ ... **Not a result.**") is historical and does not claim that anything is open.
- **AC($p$).** The three descriptions agree in substance: "modulo $p$ (and of falling factorials modulo $p^3$)" in §12.3, "modulo $p$ and $p^2$, and of falling factorials modulo $p^3$" in §12.5, and "mod $p$, $p^2$ and $p^3$" in the README. This is because $q_2$'s block statistic lives modulo $p^2$.
- **The example bound on $q_1$ (§12.3).** If every dilate has $\ge4\log_2p$ elements at distance $\ge p/4$ from 0, then $q_1(p)\le1+p^{-3}$. This is correct: $q_1-1=\sum_{b\ne0}\prod_r\cos^2(\pi br!/p)\le(p-1)2^{-4\log_2p}<p^{-3}$.
- **Math syntax.** In the parts read (the header, §0, §5, §8, §9, §11.3, §11.6, §12, and README lines 1–60 and 140–150), every `$` is paired and every brace balanced. The table column counts in §12 are consistent.
