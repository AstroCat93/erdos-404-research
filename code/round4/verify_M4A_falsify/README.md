# verify_M4A_falsify: numerical falsification of round-4 track M4A (Theorem M, p = 7; Corollary M', p = 11..23)

The code here was written from the statements in `data/round4/reports/M4A.md` and shares none with `code/round4/M4A/`. The only input taken from M4A is the atom data file `data/round4/M4A/atom_p{7,11,13}.txt`; its content is re-verified from scratch. The report is `data/round4/checks/M4A_falsify.md`, and the logs are in `data/round4/verify_M4A_falsify/`.

| file | purpose |
|---|---|
| `vf_lib.py` | Library: valuations; exact constants q_s and P_0; a CRT-exact signed-process DP (int64 residues modulo primes near 2^60, reconstructed and range-checked); the Lemma Q bound and four stronger control variants; Props D and E, both per-c via Lemma Q and in block form (exact gmpy2 rationals); the Prop E' closed form |
| `t0_validate.py` | Constants checked against the report; DP checked against brute-force enumeration |
| `t1_lemmaQ.py` | Lemma Q, exact, for these u types: random, near small negative integers, integers, a residue scan, near double roots of signed polynomials, and runs of depth-1 gates (`d1run`, `d1first`) |
| `t2a_lemmaH.py` | Lemma H on random and adversarial polynomials (squares, cubes, near-double roots, signed carry polynomials) |
| `t2b_chain.py` | On windows and balls: the Theorem 1 identity, Lemma F, Prop D (pointwise and chi^2 versions), Prop E, the two code paths, and E' >= E |
| `t3_atom_fe.py` | Independent recomputation of the whole FE certificate (phases 0-4, with an analytic tail), plus Pi_A, delta_A and the Paley-Zygmund bound |
| `t4_eprime.py` | E' >= E on random and adversarial windows at p = 3, 5, 7, 11 |
| `t5_atom_lowscale.py` | Prop D at the real geometry of the p = 7 atom, at the exactly computable scales j <= 6 |
| `t6_deep_algebra.py` | The algebra of Lemma Q's proof (Steps 0(a), 3 and 4) at levels up to about 220 |
| `run.sh`, `batch_t1.sh`, `batch_t2.sh` | Logged runs (`nice -n 10`, wall-time limit; the command is the first line of each log) |

## Second check: Corollary M' (p = 11, 13, 17, 19, 23)

The files `cm_*.py` are a second, separate implementation, written for the check of Corollary M'. They share no code with `code/round4/M4A/` and none with `vf_lib.py`. Where possible they use different algorithms:
- q_s by an int64 residue DP, cross-checked by enumeration (p <= 13) and by an FFT of the characteristic function;
- P_0 by exact meet-in-the-middle;
- V_N on the atom by Legendre's formula.

| file | purpose |
|---|---|
| `cm_lib.py` | Library: constants q_s and P_0; the Lemma Q right-hand side (with controls); Props D/E in block form and literally per c; Prop E' constants and closed form; a CRT-exact joint signed DP |
| `cm1_consts.py` | q_s, P_0, rho_1, gamma, kappa and the phase-4 rate at p = 3..23, by two or three methods, against M4A's printed constants |
| `cm2_cert.py` | Independent recomputation of the FE certificate for one atom file: atom and path at x_A and at random points of A, all five phases, the analytic phase-4 tail, Pi_A, delta_A and the Paley-Zygmund bound |
| `cm3_lemmaQ.py` | Lemma Q, exact, at p = 7..23, at points near -1, -2, ..., small integers, runs of depth-1 gates and near double roots; controls |
| `cm4_atomlow.py` | Prop D at the real geometry of the p = 11..23 atoms, at exactly computable scales |
| `cm5_eprime.py` | Prop E' >= Prop E (with M4A's S = 8 or 4) on random and deep-gate windows; block form == literal form |
| `cm6_thm1.py` | Theorem 1 (exact identity), Lemma F, Props D and E on balls, at p = 7, 11, 13 |
| `cm7_lemmaH.py` | Lemma H on adversarial polynomials at p = 7..23 |
| `cm8_propD_window.py` | Prop D, the eps form and the chi^2 form pointwise at the largest exact levels, at p = 7..23 |
| `batch_cm3.sh`, `batch_cm4.sh` | Logged runs (logs `data/round4/verify_M4A_falsify/cm*.log`) |
