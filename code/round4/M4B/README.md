# Track M4B (round 4): adaptive windows (strategy B)

Report: `data/round4/reports/M4B.md`. Logs: `data/round4/M4B/` (each run: `### command:`, `### start:`, filtered output,
`### exit:`, `### wall:`; wrapper `runlog.sh` runs under `nice -n 10` with a 30-minute limit).

| file | role | status of what it checks |
|---|---|---|
| `m4b_lib.py` | exact p-adic helpers: valuations, window elements, exact subset-sum / signed laws (numpy int64 or Python ints), eps | library |
| `b2_gate_split_check.py` | Prop B2 (gate splitting identity and its bounds), exact rationals; `NEG=1` negative control | exact test |
| `b3_ball_check.py` | Lemma B3 (conservation of the unweighted signed mass on Hensel balls), exact; fine-cylinder control; `nohypH` control | exact test |
| `n4_infinite_mean_check.py` | mechanism of Prop N4 (eps = (p^s/2) eps_fact for a deep gate at distance 1), exact | exact test |
| `eps_factorial.py` | fine-scale masses of factorial windows (position-independent part), exact numbers | exact numbers |
| `r3m_kappa_compare.py` | Corollary B2' predictions vs the round-3 deep-gate log | exact numbers |
| `ladder_vs_fixed.py` | eps at fixed vs ladder starts (Monte Carlo over x, exact eps per sample) | heuristic |
| `slope_profile.py` | slope profile / Hensel-failure mass of the signed process (Monte Carlo, float64 DP) | heuristic |
| `sb_probe.py` | first probe of (S_B) (Monte Carlo, float64 DP); superseded by `slope_profile.py`, not used in the report | heuristic |
