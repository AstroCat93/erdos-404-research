# verify_M4B_falsify (round 4): numerical falsification of M4B Theorem B1 / B1'

Report: `data/round4/checks/M4B_falsify.md`. Logs: `data/round4/verify_M4B_falsify/` (each log starts with
`### command:`; wrapper `run.sh` runs under `nice -n 10` with a 30-minute limit).
All code here is new and shares nothing with `code/round4/M4B/` or `code/round3/`.
Exact arithmetic: Python integers, `fractions.Fraction`, numpy int64 counts (bounded by 2^60);
float only in the Fourier cross-check of eps (`eps_fourier`) and in square roots of the final
Paley-Zygmund comparisons.

| file | what it tests |
|---|---|
| `fz_lib.py` | library: valuations, slope-0 population counts by DP over (S mod p^{V_T}, S' mod p), explicit path enumeration, descendants of one parent, window laws, chi^2, eps (collisions and Fourier fibres), adaptive rules `lin`, `ladder`, `hash`, `det` |
| `t0_validate.py` | DP counts vs brute force over all 2^{n-1} paths; eps collisions vs Fourier fibres |
| `t1_partition.py` | Lemma B1a (partition, constancy of n_0..n_{l+1}, m_l on A_l, refinement), G_{l-1}-measurability of B_l and of eps_l, deep lifts; negative control (one-step rule) |
| `t1b_n0_small.py` | sensitivity of Lemma B1a to n_0 >= 2p |
| `t2_martingale.py` | Cor A' with adaptive n_{l+1} (exact mean identity on atoms of G_l), Prop A(i) at slope 0, rule constancy; negative control (peeking rule) |
| `t3_twowindow.py` | Prop C2 and Prop B on atoms of G_{l-1} with adaptive n_{l+1}: full populations, single explicit parents (exact equality), parent subsets; negative control (one-step-predictable n_{l+1}, two adversaries) |
| `t4_obsG_ladder.py` | Observation G (path level), the M_j bound in the proof of B1', the ladder rule of M4B section 2 |
| `t4b_Mj_probe.py` | probe: growth of max M_n at deep gates (bears on "M_j is bounded" in the proof of B1') |
| `t5_global.py` | exact finite-horizon B1' over all of Z_p (exhaustive atoms of G_0), and B1 per atom at j = 0 |
| `t6_atom_j.py` | exact finite-horizon B1 per atom at random starting times j = 1, 2 |
| `batch_t5.sh`, `batch_t6.sh`, `run.sh` | drivers |

## Part II: M4B Lemma B2a + Corollary B2' (deep gate at distance d)

Report: `data/round4/checks/M4B_falsify.md`, Part II. Logs: `data/round4/verify_M4B_falsify/b2_*.log`.
New code, independent of `fz_lib.py`, of `code/round4/M4B/` and of `code/round3/`.

| file | what it tests |
|---|---|
| `b2_lib.py` | library: valuations on cylinders x + p^400 Z_p, window elements, exact signed laws by meet in the middle (deep gates, K up to ~70), numpy int64 laws, R3M subset-sum collision definition, forced gates |
| `b2_t1_lemmaB2a.py` | Lemma B2a exhaustively for d <= 24 (both forms); sharpness of p^s > e(d-1)! |
| `b2_t2_propB2.py` | Prop B2 (B2.1)-(B2.5) at every split point, all r; eps three ways; negative control |
| `b2_t3_corB2p.py` | Cor B2' (a),(b),(c), band [1/2,3/2]; families rand, negk (x ~ -k, n = 0..k-1), two (second deep gate), end, short |
| `b2_t4_controls.py` | controls: hypothesis violated; d = 1 with the d >= 2 formula; wrong Delta argument; gate in the second window; double-root algebra |
| `b2_t5_r3m_compare.py` | comparison with data/round3/R3M/eps_gate_depth.log; kappa reading |
| `b2_t6_exhaustive.py` | Cor B2' over all units w mod p^R; direct decomposition of eps by pre-digits |
| `b2_t7_large_d.py` | Cor B2' at d = 10..16 |
