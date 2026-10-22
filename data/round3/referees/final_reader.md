# Round-3 final editorial pass: fresh-reader lens

*Reviewer:* an AI instance doing a read-only editorial pass. No human has checked this report.  
*Date:* 2026-10-13.  
*Read in full:* README.md; note.md header, §0 (including "Round 3 additions"), §11.0–§11.8 and the References. Notation was traced back to §1.5, §3.5, §3.7, §10.1, §10.2, §10.4 and §10.5, and definitions were taken from the track reports R3M, R3F, R3N, R3Q and S0 and from the computational referee report. No file other than this report was written, and git was not run.

## Verdict

There are 11 must-fix and 35 nice-to-fix findings. None changes a mathematical statement. The must-fix items fall into four groups:

- **Overstated verification.** The README says six tracks were checked; only five were, and S0 was not. §11.8 says the computational referee reproduced "every decisive computation", but one of its runs did not finish.
- **Overstated status.** The README calls FE "of barrier type" without "heuristically". Three summaries say single gate blocks satisfy "the random-model Fourier bound", which reads as RMF; the R3F check corrected this wording. The README row for the bottleneck law gives no heuristic label.
- **Undefined notation in stated results.** $\chi^2_W$, $M$ and $M_\ell$ (Proposition 11.12) are undefined, and $M_\ell$ clashes with $M_n$. Theorem 11.14 uses the undefined $j$, $\chi^2_j$, $\varepsilon_\ell(x)$ and $\mu_A$. Theorem 11.22 uses the undefined $n_d$ and $\tau'_p$.
- **Contradiction.** The README says "everything was run on macOS", but note.md §11.7 says round 3 ran on Linux x86_64.

**Checked and fine:**
- Q3 is stated as open everywhere.
- Q1 is stated as open in general everywhere, and every finiteness claim at $p=2$ is labelled computer-assisted or proved, apart from the README rate sentence (nice-to-fix 1).
- No round-3 text names an AI model or version: round-3 passages say only "Claude (Anthropic)". The "Claude Opus 5.5" mentions are in round-1 and round-2 text (note.md lines 5, 938, 946, 1017; README line 216).
- No gendered pronouns.
- The `$` signs balance on every line of README.md, note.md §0 and note.md §11, and every table there has consistent column counts.
- The paths cited in the README's round-3 reproduction block exist.

Every *current text* below occurs exactly once in its file, which was checked by exact string search; line numbers refer to the files as of this pass.

## Must-fix

### 1. README.md:33

**Current text:**

```text
Round 3 was produced by a third AI-assisted session. Each of six tracks was checked by a separate AI instance that wrote its own code.
```

**Replacement:**

```text
Round 3 was produced by a third AI-assisted session: a status gate (S0) and five research tracks. Each research track was checked by a separate AI instance that wrote its own code; S0 was not checked, except for its Lemma S0.1.
```

**Why:** Overstates verification and contradicts note.md (header line 11, §11 preamble, §11.0, §11.8 "What remains unverified") and the README's own AI-disclosure bullet, which all say five research tracks were checked and the status gate S0 was not.

### 2. README.md:40

**Current text:**

```text
proved (FE unproved; of barrier type; numerically plausible
```

**Replacement:**

```text
proved (FE unproved; heuristically of barrier type; numerically plausible
```

**Why:** States as fact what the note labels heuristic. The round-3 logic referee required "FE is of barrier type" to be labelled heuristic (§11.8), and note.md §0 item 21, §11.0 and §11.3 all say "heuristically"; R3M's own report says the mechanism is "not a proved claim".

### 3. README.md:41

**Current text:**

```text
Single gate blocks satisfy the random-model Fourier bound at every level: $\sup_d\rho_d\le1.3203,1.1760,1.8377,1.2064$ ($p=5,7,11,13$).
```

**Replacement:**

```text
Single gate blocks (windows of length $p$) satisfy an RMF-type per-level Fourier bound at every level, though not RMF itself: the ratio $\rho_d$ of the level-$d$ $L^1$ Fourier shell to its random-model value satisfies $\sup_d\rho_d\le1.3203,1.1760,1.8377,1.2064$ ($p=5,7,11,13$).
```

**Why:** The README's Thm 10.16 row calls RMF "a random-model Fourier bound", so "the random-model Fourier bound" reads as RMF, a sufficient condition for Q3. The R3F check corrected exactly this ("an RMF-type per-level bound for single gate blocks", not RMF; note.md §11.4 check list and "What (a) does not imply"). $\rho_d$ is also undefined in the README.

### 4. note.md:126

**Current text:**

```text
Single gate blocks satisfy the random-model Fourier bound at every level, with certified constants $\sup_d
```

**Replacement:**

```text
Single gate blocks (windows of length $p$) satisfy an RMF-type per-level Fourier bound at every level (not RMF itself; §11.4(a)), with certified constants $\sup_d
```

**Why:** Same overstatement as the README row: in the summary, "the random-model Fourier bound" reads as RMF (item 17 introduces RMF as "a random-model Fourier bound"), which §11.4 and the R3F check say (a) does not give.

### 5. note.md:1860

**Current text:**

```text
Single gate blocks satisfy the random-model Fourier bound at every level, with certified constants. This explains
```

**Replacement:**

```text
Single gate blocks (windows of length $p$) satisfy an RMF-type per-level Fourier bound at every level, with certified constants; this is not RMF itself, which concerns windows of length $p^{t-1}$. This explains
```

**Why:** Same overstatement in the §11.0 headline; it contradicts "What (a) does not imply" in §11.4 and the wording fix the R3F check required.

### 6. README.md:44

**Current text:**

```text
| computer-assisted; lemma proved |
```

**Replacement:**

```text
| computer-assisted; lemma proved; the bottleneck law itself is heuristic (Conj 10.24) |
```

**Why:** The row also reports "63 of 64 registered predictions of the bottleneck law confirmed", but the status column gives only "computer-assisted; lemma proved". A reader can take the law as computer-assisted. note.md labels it "[heuristic law; outcomes computer-assisted]".

### 7. note.md:2181

**Current text:**

```text
With its own code, it reproduced every decisive computation of §§11.1–11.4 and Proposition 11.11, exactly or to all printed digits:
```

**Replacement:**

```text
With its own code, it re-ran the decisive computations of §§11.1–11.4 and Proposition 11.11 listed below; every run that finished agreed exactly or to all printed digits (one run did not finish; see the paragraph after the list):
```

**Why:** Overstates the check and contradicts the next paragraph and "What remains unverified": the referee's own upper-bound run for $f(17662,2)\le221465$ hit its time limit. Its report also checks $\rho_d$ only at small $d$ for $p=7,13$ and does not re-run the interval sums of §11.4(e), so "every decisive computation" claims too much.

### 8. note.md:2002

**Current text:**

```text
Every window with $D\ge1$ has $\chi_W^2\ge(p-1)4^{-p}$. This comes from the mod-$p$ shell alone, whatever the window length or the gates. The bound $\operatorname{Var}\le M^2\chi_W^2$ is attained, for example for a single parent. So $\prod_\ell(1+\chi^2_{W_\ell})=\infty$ for every window sequence, and no recursion of the form $\mathbb E[M_{\ell+1}^2]\le(1+\chi^2_\ell)\mathbb E[M_\ell^2]$ can prove $L^2$-boundedness.
```

**Replacement:**

```text
Every window with $D\ge1$ has $\chi_W^2\ge(p-1)4^{-p}$. Here $\mu_W=2^{-(N-n)}m_W$ is the law of a uniformly random subset sum of the window modulo $p^D$ (Proposition 11.11), and $\chi_W^2:=p^D\sum_r\mu_W(r)^2-1=\sum_{\xi\ne0}|\hat\mu_W(\xi)|^2$ is its $\chi^2$-distance from the uniform law. The bound comes from the mod-$p$ shell alone, whatever the window length or the gates. The Cauchy–Schwarz bound $\operatorname{Var}(c_NY)\le M^2\chi_W^2$ for Proposition 11.11, with $M=c_n|P|$, is attained, for example for a single parent. So $\prod_\ell(1+\chi^2_{W_\ell})=\infty$ for every window sequence, and no recursion of the form $\mathbb E[M_{\ell+1}^2]\le(1+\chi^2_\ell)\mathbb E[M_\ell^2]$, where $M_\ell:=c_{n_\ell}Z^0_{n_\ell}$ is the slope-0 martingale at the window times (not the maximal valuation $M_n$ of §10.1), can prove $L^2$-boundedness.
```

**Why:** $\chi^2_W$, $M$ and $M_\ell$ are never defined in note.md. Worse, $M_n$ already means the maximal valuation (§10.1), and it is used in that sense two lines later (Proposition 11.13). Definitions are from R3M.md §3 (Proposition B) and §5 ("Setting for the theorem"). $\chi^2$ also drives Theorem 11.14.

### 9. note.md:2008

**Current text:**

```text
Fix deterministic window times $2p\le n_0<n_1<\cdots$, a summable sequence $(\bar\varepsilon_\ell)$, and an admissible atom $A$, i.e. a cylinder with a nonempty slope-0 population and valid window conditions. Let $\tau$ be the first window at which the linear-regime conditions fail or $\varepsilon_\ell(x)>\bar\varepsilon_\ell$, and put $\Pi_A=(1+\chi^2_j)\prod_\ell(1+\bar\varepsilon_\ell)$.
```

**Replacement:**

```text
Fix deterministic window times $2p\le n_0<n_1<\cdots$, with windows $W_\ell=[n_\ell,n_{\ell+1})$, $\chi^2_\ell:=\chi^2_{W_\ell}$ (Proposition 11.12) and fine-scale masses $\varepsilon_\ell(x):=\varepsilon(W_{\ell-1},W_\ell)$ (Proposition 11.13). Fix also an index $j$, a summable sequence $(\bar\varepsilon_\ell)_{\ell>j}$, and an admissible atom $A$ at time $n_j$, i.e. a cylinder $x+p^{V_{n_j}(x)}\mathbb Z_p$ with a nonempty slope-0 population and valid window conditions; $\mu_A$ is normalised Haar measure on $A$. Let $\tau$ be the first window $\ell>j$ at which the linear-regime conditions (the hypotheses of Proposition 11.13 for $(W_{\ell-1},W_\ell)$) fail or $\varepsilon_\ell(x)>\bar\varepsilon_\ell$, and put $\Pi_A=(1+\chi^2_j)\prod_{\ell>j}(1+\bar\varepsilon_\ell)$.
```

**Why:** This is the headline conditional theorem, but as written its hypothesis FE cannot be read: $j$, $\chi^2_j$, $\varepsilon_\ell(x)$, "linear-regime conditions" and $\mu_A$ are all undefined in note.md. The definitions are from R3M.md §5 (Theorem C3 and its setting). The later "for $n_j$ large enough" also relies on $j$.

### 10. note.md:2064

**Current text:**

```text
and every window of length $p^{t-1}$ ($t\ge3$, every $K'$) has $Q_d\le C\,N_d2^{-n_d}$ at every level, with $\sqrt C(\Lambda'_p+\tau'_p(3))<1$.
```

**Replacement:**

```text
and every window of length $p^{t-1}$ ($t\ge3$, every unit $K'\bmod p^{c_t}$, $c_t=v_p((p^{t-1}-1)!)$) has $Q_d\le C\,N_d2^{-n_d}$ for $1\le d\le t+c_t$, where $n_d=\#\{i<p^{t-1}:v_p(i!)<d\}$. Suppose also that $\sqrt C(\Lambda'_p+\tau'_p(3))<1$, where $\tau'_p(t):=p^{t+c_t}2^{-p^{t-1}/2}$ (the $L^2$ analogue of $\tau_p(t)$ in Theorem 10.16).
```

**Why:** This states a sufficient condition for Q3 in terms of the undefined $n_d$ (easily confused with $N_d$ and $U_d$) and the undefined $\tau'_p(3)$. "Every $K'$" and "at every level" are also looser than the theorem actually proved. The text is from R3F.md, Theorem B5 (H2), (H3).

### 11. README.md:155

**Current text:**

```text
Everything was run on macOS (Apple silicon) using at most 3 cores.
```

**Replacement:**

```text
Rounds 1 and 2 were run on macOS (Apple silicon) using at most 3 cores. Round 3 ran on Linux x86_64 with 4 shared cores, and also needs GMP and the Python packages `mpmath`, `gmpy2` and `python-flint` (note.md §11.7).
```

**Why:** This is now false and contradicts note.md §11.7 ("Machine: Linux x86_64, 4 shared cores ..."). A reader reproducing round 3 also needs the extra dependencies that §11.7 lists.

## Nice-to-fix

### 1. README.md:9

**Current text:**

```text
(note.md Theorem 11.4; computer-assisted). There is also an explicit, very weak rate: $\delta_G(2)\le2^{1/80}G^{-1/80}$ for $G\ge2^{3072}$ (Theorem 11.7).
```

**Replacement:**

```text
(note.md Theorems 11.2 and 11.4; computer-assisted). There is also an explicit, very weak rate: $\delta_G(2)\le2^{1/80}G^{-1/80}$ for $G\ge2^{3072}$ (Theorem 11.7; computer-assisted).
```

**Why:** The Q1 status bullet gives the rate without its status label, although Theorem 11.7 is computer-assisted. The two named values are Theorem 11.2; Theorem 11.4 is the table.

### 2. README.md:37

**Current text:**

```text
computer-assisted: at least two independently written exhaustive programs (three for 594), plus an explicit witness verified exactly by three verifiers
```

**Replacement:**

```text
computer-assisted: at least two independently written exhaustive programs (three for 594), plus an explicit witness verified exactly (by three verifiers for 594 and 17662, by two for the other rows)
```

**Why:** In note.md §11.1, three verifiers check only the 594 and 17662 witnesses. Each of the other 16382 rows has a witness checked by GMP and one checked by the checker's verifier, so "three verifiers" overstates for the table rows.

### 3. README.md:42

**Current text:**

```text
A collision-count ($L^2$) version of Theorem 10.16 (budget $<1$ exactly for $p\ge11$)
```

**Replacement:**

```text
A collision-count ($L^2$) version of Theorem 10.16 (budget $<1$ if and only if $p\ge11$)
```

**Why:** Here "exactly" can be read as "exactly computed". The meaning is "precisely when": $\Lambda'_p=\infty$ at $p=3,5$, $\Lambda'_7=2.0496$, and $\Lambda'_p\le0.371$ for $p\ge11$.

### 4. note.md:11

**Current text:**

```text
updates the summary (§0), §2, §5 and §10 where they are superseded
```

**Replacement:**

```text
updates the summary (§0), §2, §5, §8 and §10 where they are superseded
```

**Why:** §8 also has a "[Round 3]" paragraph (the round-3 AI disclosure), so the list of updated sections is incomplete.

### 5. note.md:120

**Current text:**

```text
Each item was produced by one round-3 track and checked by a separate AI instance with its own code (§11.0, §11.8). **No human has checked any of it.**
```

**Replacement:**

```text
Each item was produced by one round-3 research track and checked by a separate AI instance with its own code (§11.0, §11.8); the remarks credited to the status gate S0 (such as the re-fit in item 19) were not checked, except its Lemma S0.1. **No human has checked any of it.**
```

**Why:** Item 19 includes S0's re-fit of the Haar values, and S0 was not checked (header line 11, §11.8), so "each item ... checked" slightly overstates.

### 6. note.md:1876

**Current text:**

```text
- (iii) Fix $K>v(a!)$ and let $N_K$ be the least $N$ with $v(N!)\ge K$. If no "final candidate" at $N_K$ is $\equiv0\pmod{2^K}$, then $f(a,2)$ equals the largest valuation of a death candidate at a stage $\le N_K$, and this is $<K$.
```

**Replacement:**

```text
- (iii) For even $N$ and a prefix $P\subseteq[a,N)$ alive at $N$, the four *candidates* at stage $N+2$ are $\sum_{n\in P}n!+d$ with $d\in\{0,N!,(N+1)!,N!+(N+1)!\}$, the possible partial sums below $N+2$ (at the first stage, the *initial candidates* $a!$ and $a!+(a+1)!$). A candidate of valuation $<v((N+2)!)$ is a *death candidate*. Fix $K>v(a!)$ and let $N_K$ be the least $N$ with $v(N!)\ge K$; the *final candidates* are the candidates at stage $N_K$. If no final candidate is $\equiv0\pmod{2^K}$, then $f(a,2)$ equals the largest valuation of a death candidate at a stage $\le N_K$, and this is $<K$.
```

**Why:** The lemma that makes Theorem 11.4 an exact computation uses "final candidate", "death candidate" and "stage" without defining them. The definitions are from R3N.md (Pair steps and candidates, Lemma 2).

### 7. note.md:1871

**Current text:**

```text
**Method [proved correct; performance computer-assisted].**
```

**Replacement:**

```text
**Method [proved; the runs that apply it are computer-assisted].**
```

**Why:** "proved correct; performance computer-assisted" does not use the note's status vocabulary, and "performance" suggests speed rather than results.

### 8. note.md:1880

**Current text:**

```text
The new ingredient is a **windowed depth-first search** (program C, `code/round3/R3N/dfsW.c`):
```

**Replacement:**

```text
The new ingredient is a **windowed depth-first search** (program C, `code/round3/R3N/dfsW.c`). The other programs of this subsection are A (`bfsA.c`, the track's breadth-first search, after the design of round-1 track D, which is unrelated to program D), B (`dfsB.c`, a second depth-first search using GMP) and D (`check_R3N/dfsD.c`, written by the checker). Program letters are local to each subsection of §11. Program C works as follows:
```

**Why:** Program C is introduced first. B and D appear only in the table, and A appears only in the Credit paragraph next to "round-1 track D". The letters A–D also mean different programs in §11.3 and §11.5, so a fresh reader cannot tell which program is which.

### 9. note.md:1883

**Current text:**

```text
- There is no deduplication. In every breadth-first run, deduplication merged at most 2 states.
```

**Replacement:**

```text
- It does not merge equal states (no deduplication). Little is lost: in every run of the breadth-first program A, which does deduplicate, deduplication merged at most 2 states in total.
```

**Why:** As written, the two sentences look contradictory ("no deduplication", then deduplication merged states).

### 10. note.md:1892

**Current text:**

```text
$dfsW4$ (program C with checkpoints; interrupted once and resumed) and D (split into 20000 subtrees). Identical tree size $5\,927\,905\,821=\mathrm{nodes}_{dfsW4}/4$
```

**Replacement:**

```text
`dfsW4` (program C with checkpoints; interrupted once and resumed) and D (split into 20000 subtrees). Identical tree size $5\,927\,905\,821=\mathrm{nodes}_{\mathrm{dfsW4}}/4$
```

**Why:** In math mode, a program name renders as the italic product $d\,f\,s\,W\,4$. Elsewhere (§11.8) it is written `dfsW4`.

### 11. note.md:1894

**Current text:**

```text
For $a=17662$: $dfsW4$ needs about 1.5 h
```

**Replacement:**

```text
For $a=17662$: `dfsW4` needs about 1.5 h
```

**Why:** Same math-mode program name as in the table.

### 12. note.md:1912

**Current text:**

```text
Q1 at $p=2$ (Conjecture 5.1) is thereby verified up to $2^{15}$. Kitamura's complete exact table reached 256, with isolated rows up to 8190.
```

**Replacement:**

```text
Q1 at $p=2$ (Conjecture 5.1) is thereby verified up to $2^{15}$.
```

**Why:** This is the third statement of the same fact in §11 (see also §11.0 headline 1, "Kitamura's complete exact table covered $a\le256$, plus isolated rows up to 8190", and the Credit paragraph), plus §0 item 19.

### 13. note.md:1928

**Current text:**

```text
Under a $c/G$ law, survivors to depth $G$ occur among about $G$ even integers.
```

**Replacement:**

```text
Under a $c/G$ law, roughly one even integer in every $G/c$ survives to depth $G$.
```

**Why:** As written, "occur among about $G$ even integers" is unclear: it could mean that $G$ integers survive, or that one survives among $G$.

### 14. note.md:1926

**Current text:**

```text
the probability $P(E_n)$ that the digit-sum environment walk of the 2-adic odometer stays $\ge0$ up to time $n$ satisfies
```

**Replacement:**

```text
the probability $P(E_n)$ that the environment walk $W_k=k-V_k(x)$ of §10.1 (Remark 10.8.2; $W_k=s(x+k)-s(x)$ for natural $x$), driven by the 2-adic odometer $x\mapsto x+1$, stays $\ge0$ for $1\le k\le n$ satisfies
```

**Why:** The walk is not defined where Lemma S0.1 is stated. Its formula first appears in §11.6 item 4. The definition is S0.md §5 ($D(y,k)=s_2(k)-c(y,k)$, identified there with $W_n$ of Remark 10.8.2).

### 15. note.md:1926

**Current text:**

```text
the survival probability of a critical BPRE is of the same order (Kozlov 1976; Geiger–Kersting 2000; AGKV 2005, Thm 1.1)
```

**Replacement:**

```text
the survival probability of a critical branching process in a random environment (BPRE) is of the same order (Kozlov 1976; Geiger–Kersting 2000; Afanasyev–Geiger–Kersting–Vatutin [AGKV] 2005, Thm 1.1)
```

**Why:** The abbreviations BPRE and AGKV are never expanded in note.md, and AGKV is used again in §11.6 item 3.

### 16. note.md:1948

**Current text:**

```text
- Bounds on the frozen-state weights: $2^{-\lfloor\log_22\lambda\rfloor}\le\rho\le2^{\min(\lambda-1,\lfloor(\lambda+\tilde M)/2\rfloor-1)}$, the lower bound on paths that survive $2\lambda$ steps.
```

**Replacement:**

```text
- Bounds on the frozen-state weights: $2^{-\lfloor\log_22\lambda\rfloor}\le\rho\le2^{\min(\lambda-1,\lfloor(\lambda+\tilde M)/2\rfloor-1)}$, where $\tilde M=\max_{1\le i\le2\lambda}\min(v(x+n+i),\lambda)$; the lower bound holds on paths that survive $2\lambda$ steps.
```

**Why:** $\tilde M$ is undefined in note.md. The definition is from R3Q.md Lemma 6(b).

### 17. note.md:1971

**Current text:**

```text
The total over the three classes is $\le0.02854$ at $G=2^{40}$.
```

**Replacement:**

```text
By exact evaluation (as in Corollary 11.8), the total over the three classes is $\le0.02854$ already at $G=2^{40}$, far below the range $K\ge1024$ of the closed form.
```

**Why:** Right after a theorem stated only for $K\ge1024$, a value at $K=40$ looks contradictory. The value comes from the exact evaluation in R3Q.md (Theorem A table), not from the $2^{-K/7}$ bound.

### 18. note.md:2000

**Current text:**

```text
So $\operatorname{Var}(c_N Y)$ equals the Fourier overlap
```

**Replacement:**

```text
So, writing $Y$ for the total number of children of a set $P$ of slope-0 parents, $\operatorname{Var}(c_N Y)$ equals the Fourier overlap
```

**Why:** $Y$ (and the parent set $P$ used in Proposition 11.12) is undefined in note.md. The definition is from R3M.md Proposition B(ii).

### 19. note.md:2006

**Current text:**

```text
Here $\varepsilon(W,W')=p^{D+D'}\mathrm{Coll}_{D+D'}-p^D\mathrm{Coll}_D$ is the $L^2$ mass of the *composite* window law in the band $(p^D,p^{D+D'}]$.
```

**Replacement:**

```text
Here $\varepsilon(W,W')=p^{D+D'}\mathrm{Coll}_{D+D'}-p^D\mathrm{Coll}_D$, where $\mathrm{Coll}_K$ is the probability that two independent uniformly random subset sums of the *composite* window $\{\pi_j(x)/\pi_n(x):n\le j<N'\}$ agree modulo $p^K$. Equivalently, $\varepsilon(W,W')$ is the $L^2$ mass of the composite window law in the band $(p^D,p^{D+D'}]$.
```

**Why:** $\mathrm{Coll}$ is undefined in note.md, and $\varepsilon(W,W')$ is the quantity that FE bounds. The definition is from R3M.md Proposition C2.

### 20. note.md:2028

**Current text:**

```text
- The median fine-scale masses $\varepsilon_\ell$ decay steadily at $p=7$ and $p=5$, but **not visibly at $p=3$**. So FE is plausible at $p\ge5$ and doubtful at $p=3$.
```

**Replacement:**

```text
- The median fine-scale masses $\varepsilon_\ell$ decay steadily at $p=7$, less clearly at $p=5$ (the medians are not monotone there), and **not visibly at $p=3$**; no scan was made at $p\ge11$. So FE is plausible at $p=5,7$, most clearly at $p=7$, and doubtful at $p=3$.
```

**Why:** This overstates the data. In R3M.md §7.3 the $p=5$ medians are 0.035, 0.027, 0.025, 0.046, 0.050, 0.013, 0.0024, which the report calls "less clearly", and only $p=3,5,7$ were scanned. The current text also reads as inconsistent with §11.6 item 2 ("the most promising case is $p\ge7$"). If adopted, make the same change from "$p\ge5$" to "$p=5,7$" in §0 item 21 and in the README Thm 11.14 row.

### 21. note.md:2038

**Current text:**

```text
Notation of §10.4. $S_d$ and $Q_d$ are the $L^1$ and $L^2$ Fourier shells at level $d$ of a subset-sum law.
```

**Replacement:**

```text
Notation of §10.4; $K'$ is the unit class of §3.7 that fixes the position $p^tK'$ of a window or block. $S_d$ and $Q_d$ are the $L^1$ and $L^2$ Fourier shells at level $d$ of a subset-sum law (unrelated to the polynomials $S_e$ of §§11.2–11.3), and $\rho_d$ below is unrelated to the frozen-state weights $\rho$ of §§11.2–11.3 and to $\rho_0(p)$ of Lemma 10.11.
```

**Why:** $K'$ is used in Lemma 11.16, Theorem 11.22 and (c) without a pointer to its definition (§3.7). $S$ and $\rho$ each carry three or four unrelated meanings within §11.

### 22. note.md:2057

**Current text:**

```text
  - The $L^2$ budget converges at every odd $p$, including $p=3,5$, where the $L^1$ budget fails.
  - The Cauchy–Schwarz budget $\Lambda'_p=\sum_dN_d2^{-U_d/2}$ is $<1$ exactly for $p\ge11$:
```

**Replacement:**

```text
  - The random-model $L^2$ mass $\sum_dN_d2^{-U_d}$ is finite at every odd $p$, including $p=3,5$, where the $L^1$ budget $\Lambda_p$ fails.
  - The Cauchy–Schwarz budget $\Lambda'_p=\sum_dN_d2^{-U_d/2}$ is $<1$ if and only if $p\ge11$:
```

**Why:** As written, "the $L^2$ budget converges ... including $p=3,5$" seems to contradict Theorem 11.22's "$\Lambda'_p=\infty$ for $p=3,5$". These are two different sums (R3F.md B2: $\Lambda2_p$ versus $\Lambda'_p$). Also, "exactly for" reads as "exactly computed".

### 23. note.md:2055

**Current text:**

```text
If the $L^2$ mass of the tail measure from $N_0$ is finite, the measure is absolutely continuous, and the tail set $E_{N_0}$ has Haar measure $\ge p^{-v_p(N_0!)}/(1+L^2)$.
```

**Replacement:**

```text
If the $L^2$ mass $\mathcal L$ of the tail measure from $N_0$ is finite, the measure is absolutely continuous, and the tail set $E_{N_0}$ (§1.5) has Haar measure $\ge p^{-v_p(N_0!)}/(1+\mathcal L)$.
```

**Why:** Here "$L^2$" is used as a number inside a formula.

### 24. note.md:2060

**Current text:**

```text
Passing from the tail from 3 to every $E_N$ needs a further step, $\lambda(E_3)>0\Rightarrow\lambda(E_N)>0$, which is not done here.
```

**Replacement:**

```text
Passing from the tail from 3 to every $E_N$ needs a further step, $\mu(E_3)>0\Rightarrow\mu(E_N)>0$, which is not done here.
```

**Why:** Haar measure is $\mu$ everywhere else in the note, and $\lambda$ is the slope in §§11.2–11.3.

### 25. note.md:2061

**Current text:**

```text
equal the shells of the *factorial measure* $\mathrm{law}(\sum_{i\ge0}\varepsilon_ii!)$.
```

**Replacement:**

```text
equal the shells of the *factorial measure* $\mathrm{law}(\sum_{i\ge0}\varepsilon_ii!)$, with $\varepsilon_i\in\{0,1\}$ i.i.d. fair bits.
```

**Why:** Yet another undefined $\varepsilon$ in §11. $\varepsilon$ already denotes $\varepsilon(G)$, $\varepsilon(W,W')$, $\varepsilon_\ell(x)$ and $\bar\varepsilon_\ell$.

### 26. note.md:2074

**Current text:**

```text
**(d) The factorial-base transfer picture [D1, D4 proved; D2 a floating-point illustration].**
```

**Replacement:**

```text
**(d) The factorial-base transfer picture [proved, except the aliasing measurement marked below, which is a floating-point illustration].**
```

**Why:** D1, D2 and D4 are labels internal to R3F.md and are never defined in the note. There are only two bullets, and "D" is also a program name.

### 27. note.md:2104

**Current text:**

```text
*Lemma 11.26 [proved].* Let $p$ be odd, $2\le t\le L_p$ and $p<H\le2p$.
```

**Replacement:**

```text
*Lemma 11.26 [proved].* Let $p$ be odd, $2\le t\le L_p$ (the covering depth of Theorem 3.9) and $p<H\le2p$, and let $\rho_0(p)$ be the least $\rho$ such that the subset sums of $\{(-1)^u/u!:u\le\rho\}$ cover $\mathbb Z/p$ (Lemma 10.11).
```

**Why:** $L_p$ and $\rho_0(p)$ are defined only in §3.5 and Lemma 10.11, and §11.5's notation pointer names only §3.7 and §10.2. Restating them here makes the iff statement self-contained.

### 28. note.md:2107

**Current text:**

```text
uniform $\mathrm{Cov}(29,5,36)$ was predicted to fail ($\nu=1.112$) but holds.
```

**Replacement:**

```text
uniform $\mathrm{Cov}(29,5,36)$ was predicted to fail (bottleneck ratio $\nu=1.112$, in the notation of Conjecture 10.24) but holds.
```

**Why:** $\nu$ is undefined in §11. It is the ratio $R^*/\ln(np^M)$ of Conjecture 10.24 (§10.5).

### 29. note.md:1980

**Current text:**

```text
*Check (`data/round3/checks/R3Q.md`).* Every lemma, theorem and explicit constant was checked line by line.
```

**Replacement:**

```text
*AI check (`data/round3/checks/R3Q.md`).* The checking AI instance checked every lemma, theorem and explicit constant line by line.
```

**Why:** A reader who jumps straight to §11.2 can read the passive "was checked line by line" as checking by a human.

### 30. note.md:2030

**Current text:**

```text
*Check (`data/round3/checks/R3M.md`).* Every [proved] item was checked line by line
```

**Replacement:**

```text
*AI check (`data/round3/checks/R3M.md`).* The checking AI instance checked every [proved] item line by line
```

**Why:** Same human-verification ambiguity as in §11.2.

### 31. note.md:2082

**Current text:**

```text
*Check (`data/round3/checks/R3F.md`).* Every [proved] item was checked line by line
```

**Replacement:**

```text
*AI check (`data/round3/checks/R3F.md`).* The checking AI instance checked every [proved] item line by line
```

**Why:** Same human-verification ambiguity as in §11.2.

### 32. note.md:2173

**Current text:**

```text
Theorems 11.17 and 11.22. All are correct.
```

**Replacement:**

```text
Theorems 11.17 and 11.22, and found no error in any of them.
```

**Why:** The note states an AI referee's judgement as established fact; elsewhere it attributes such verdicts to the referee.

### 33. note.md:2157

**Current text:**

```text
An own verifier (backward Horner and odd-part methods) checks every witness.
```

**Replacement:**

```text
The checker's own verifier (backward Horner and odd-part methods) checks every witness.
```

**Why:** Typo ("An own verifier").

### 34. note.md:2213

**Current text:**

```text
Round-2 track R1a: Claim 10.9, compared with in Theorem 11.9.
```

**Replacement:**

```text
Round-2 track R1a: Claim 10.9, with which Theorem 11.9 is compared.
```

**Why:** Garbled phrase ("compared with in").

### 35. note.md:1861

**Current text:**

```text
   - A collision-count ($L^2$) version of Theorem 10.16 holds; its budget is $<1$ exactly for $p\ge11$.
```

**Replacement:**

```text
   - A collision-count ($L^2$) version of Theorem 10.16 is proved (its hypothesis is not); its budget is $<1$ if and only if $p\ge11$.
```

**Why:** In a Q3 headline, "holds" can be read as saying that the sufficient condition holds. "Exactly for" reads as "exactly computed".
