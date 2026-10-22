# verify_M4D_logic (round 4): logic check of M4D Lemma L, Theorem F, Corollary F1

Report: `data/round4/checks/M4D_logic.md`. Logs: `data/round4/verify_M4D_logic/` (each run is preceded by its command line and start time, and followed by its exit code and wall time; written by `runlog.sh`). Everything was run through `batch.sh`, one job at a time, under `nice -n 10`.

This code was written from scratch for the check. It shares no code with `code/round4/M4D/`.

Every test point $x$ is a nonnegative integer, which is a genuine point of $\mathbb Z_p$ and never a negative integer. So all valuations, products and targets are exact.

| file | purpose |
|---|---|
| `vF.py` | library: exact valuations and products, brute-force and DFS alive paths, exact targets, the single-step carry recursion for alive-target sets (Python and numpy versions), window sums, lift counts and lift sets, window unit |
| `t2_recursion.py` | validates the two target routes: brute force over all $2^{n-1}$ paths vs DFS (prefix pruning = the (F2) converse), and the target sets vs the carry recursion (both versions); also checks $V_n\ge v(n!)$ |
| `t1_lemmaL.py` | Lemma L and (F2) by brute force over all digit strings $f$, per alive parent: aliveness, target formula, set equality with $\lambda(\mathrm{Lift}(r))$, sizes, bijectivity on the whole coset, "full iff cover". Supports forced gates. NEG control: unit $2u$ |
| `t3_thmF_chain.py` | Theorem F in its strong quantitative form ($\lvert T_\ell\rvert\ge\theta_\ell p^{D_\ell}$) over finite chains. $\theta$ schedules: optimal backward, constants, Tao, random. Also the unconditional per-step bound, the exact union identity, and the controls NEG1 ((I) alone) and NEG2 ((II) with $\ge$) |
| `t4_corF1_exhaustive.py` | Corollary F1 (finite horizon) exhaustively over cylinders, in exact Fractions; the pointwise implication; local constancy re-checked at random far points of the cylinders |
| `batch.sh`, `runlog.sh` | the logged batch |

## Part II: logic check of M4D section 3 (Lemmas W1-W3, Prop W4, Cor W5, Thm W6)

Report: `data/round4/checks/M4D_logic_W6.md` (summarised at the end of `data/round4/checks/M4D_logic.md`). Logs: `data/round4/verify_M4D_logic/w1_abstract.log`, `w2_concrete.log`, `w3_chain.log`, `w4_cw5_adv.log`. Run through `wbatch.sh` (stage 1) and `wbatch2.sh` (stage 1b and stages 2-4, after a hand-stopped first attempt), one job at a time, `nice -n 10`, single-threaded numpy. Written from scratch from the statements in M4D.md section 3 and R3M.md sections 1-5; shares no code with `code/round4/M4D/` or with the Part I files.

| file | purpose |
|---|---|
| `wlib.py` | library: exact valuations/products, DFS alive paths with direct valuations, window elements and unit, weighted laws, collision forms of the fine masses (adapted and composite), direct and FFT fibre masses F^q, Corollary W5's m and q* |
| `w1_abstract.py` | the W1-W5 algebra in the linearised model with arbitrary residue multisets: W1 means, W2 identity (float) and bound, W3(a) per parent (exact) and W3(b) (float), W4 adapted/sharp (exact), single-parent equality in the sharp form, W5(a)(b)(c); controls NEG1 (q' sees the fresh digit), NEG2 (uniform q, m=0), NEG3 (unit 2u); FFT vs direct F |
| `w2_concrete.py` | the same on real windows with direct valuations at every point of the cylinder, plus the bridge to the linearised model (child counts = mu^q_D(tau0 - beta w)), slope inheritance, and (optionally) the full slope-0 population at N from scratch |
| `w3_chain.py` | Theorem W6 over three windows, exhaustively on admissible atoms: measurability of the regime event, eps_2, q*_1 and the functionals; stopped martingale; first-window bound; conditional increments; W5(c) in the chain; the a_l recursion; finite-horizon Paley-Zygmund; schedules U (uniform = Thm 11.14), R (adapted random), S (q*), P (predictable random); control NEGM |
| `w4_cw5_adv.py` | Corollary W5: PSD of the quadratic form, exact KKT certificate of global optimality of q*, projected-gradient attack, "m=0 iff complete", and the scope probe (sharp eps^{q,q'} = 0 with m > 0 when W' covers its jump) |
| `wbatch.sh`, `wbatch2.sh` | the logged batches |
