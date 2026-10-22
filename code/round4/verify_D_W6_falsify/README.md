# verify_D_W6_falsify (round 4): numerical falsification of M4D's Lemmas W1–W3, Prop W4, Cor W5, Thm W6

Report: `data/round4/checks/M4D_falsify_W6.md`. Logs: `data/round4/verify_D_W6_falsify/`.
Each run starts with its command line and start time and ends with its exit code and wall time (`run.sh`).
All runs use `nice -n 10`, a 30-minute timeout and a 3 GB address-space limit, one job at a time.

The code was written from the definitions in `data/round4/reports/M4D.md` §3 and `data/round3/reports/R3M.md` §1–§5.
It shares no code with `code/round4/M4D/`, `code/round4/verify_M4D_logic/` or the interrupted
`code/round4/verify_M4D_falsify/`.

Every x is a natural number, i.e. a genuine point of Z_p that is not a negative integer.

| file | purpose |
|---|---|
| `wf_core.py` | Core library. Valuations; π_j, π_j′ modulo p^R by exact integer recursion; all alive paths at n by pruned BFS on exact residues (checked against exhaustive enumeration of all 2^(n−1) paths); window sums Q_f(x); weights as integer vectors; exact μ^q_k, χ²_q, ε̃^q, ε^{q,q′} (composite law ν), m(W;D′), q*. Class `Cyl`: for a cylinder C = x + p^m Z_p it evaluates S_e, S_{(e,f)}, S_{(e,f,f′)} and their derivatives **directly** at every point x′ = x0 + p^m w, w mod p^Ken, and records the alive slope-0 children, grandchildren and child targets. It also runs the structural checks of W1(a) (slopes of children and grandchildren of every parent), Lemma 2(a) (parents' aliveness/slope constant on C; BFS at sampled x′ gives the same alive set) and locality (a second lift of w gives the same alive structure). |
| `t_cyl.py` | Cylinder tests of W1(b), W1 step 1 per sub-cylinder C′, W2 (pointwise weighted child mass; exact Parseval form of the identity; literal complex form in float; bound; single-parent equality), W3 (a) exact, (b) summed over ξ exact, (b) per ξ in float64 with FFT, all k ≤ k3), W4 (adapted form with q′ varying with C′, including the per-C′ variance-maximising point masses; sharp form for q′ constant on C; single-parent equality), W5 (m = 0 iff complete class; (a) over named, all point-mass, random, perturbed and gradient-descent weights; (b) exact equality at q*; (c) M_N′ constant on every C′). Samplers: random x, gates of depth 2–4 in the history or inside the windows, x near −2, tight case D + D′ = m − M_N′, D = 0, D′ = 0. Weights: parents ones / random / single / one β-class / zero; q uniform / random / sparse / point / q* / uniform over residues / one class; q′ uniform / random / point / residue-uniform / varying random / varying point / varying variance-maximising. Negative controls NC1–NC4 (failures expected). |
| `t_chain.py` | Theorem W6 at finite horizon: enumerates every G_ℓ-atom below an admissible atom A (levels 0..L), with adapted or predictable weight schedules (U, R, RP, S = q*, P = point masses, M = mixtures) and ε̄ = ∞ / median / lower quartile / 0. Checks the weighted martingale on every atom, the first-window bound with χ²_{q_0}, the per-atom two-window inequality with ε̃ (and with the sharp ε for predictable schedules), the recursion a_{ℓ+1} − a_ℓ ≤ ε̄_ℓ a_{ℓ−1}, the product bound, the finite-horizon Paley–Zygmund conclusion μ_A(Y_L > 0) ≥ (1 − √(Πδ))²/Π, Remark 2 (ε̃ = m under q*; M_{ℓ+1} = M_ℓ when m = 0), single-path equality cases, and measurability (populations, regime, q* and ε̃ recomputed at a second representative of sampled atoms; survival via independent BFS). |
| `t_adv.py` | Hill-climbing search (exact rational objective) for parent weights and window weights that push Var/(M²χ²), LHS/(ε̃M²), LHS/(εM²) or m/ε̃ above 1, starting from 2–3 weighted parents. |
| `batch.sh`, `batch3.sh`, `batch2.sh`, `batch4.sh` | the logged runs, in that order (batch3/batch4 are reruns after resource limits; see the report §7) |
| `aggregate.py` | sums the check tables of all completed runs in the logs |
| `run.sh` | logging wrapper |

Reproduce, for example:
```
./run.sh LOG python3 t_cyl.py 5 20 5 5 201 30 rand,gate_hist,gate_win,near2,tight - 1
./run.sh LOG python3 t_chain.py 3 24 5 3 401 5 U,R,RP,S,P,M inf,med,q1 - rand,gate_hist
./run.sh LOG python3 t_adv.py 3 20 5 4 701 6 300
```
