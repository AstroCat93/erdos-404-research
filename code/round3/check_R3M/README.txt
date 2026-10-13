check_R3M (round 3): adversarial check of track R3M (odd primes, Haar measure of K_p).
Written independently of code/round3/R3M/ (no shared code; written from the statements in
data/round3/reports/R3M.md).  Run everything from the repository root.  Logs: data/round3/check_R3M/.

ck_lib.py           exact p-adic helpers: products pi_j, pi_j', valuations, DFS of alive paths with
                    prefix pruning (backward integrality), targets, subset-sum laws, collisions.
ck_validate_lib.py  validates the DFS against brute force over all 2^(n-1) paths (validate_lib.log).
ck_propA.py         Prop A(i)-(iii) state by state, Cor A' (weighted), (2.1), constancy on C;
                    exact Fractions; NEG=1 drops (W1)-(W3) (non-vacuity control).        propA.log
ck_propB.py         Prop B(i) pointwise, B(ii) mean, Fourier identity, Var <= M^2 chi^2;
                    Prop N bound and equality case |P|=1.                                 propB.log
ck_C1C2.py          Lemma C1(a),(b) for P and a random subset P', Prop C2 (exact),
                    eps by collisions == eps by Fourier fibres; NEG=1 drops (5.2).       C1C2.log
ck_C5_N3_C4.py      Lemma C5 (exact), Prop N3 lower bound and shell masses, Lemma C4
                    deterministic implication, G_(l-1)-measurability of eps_l.           C5_N3_C4.log
ck_mc_M.py          heuristic: independent Monte Carlo of M^0_n = c_n Z^0_n with s.e. and
                    heavy-tail indicator.                                                mc_M.log
ck_deepgate_M2.py   heuristic: importance sampling of E[(M^0_n)^2] on {v(x+i)=s}.        deepgate_M2.log
ck_run.sh           logging wrapper (command line, start time, output, exit code, wall time).
ck_batch1.sh, ck_batch2.sh   the exact batch and the heuristic batch, as run.
Re-runs of two R3M programs (unchanged): rerun_R3M_checks.log.
