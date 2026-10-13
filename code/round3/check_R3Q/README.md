# check_R3Q: adversarial check of track R3Q (round 3, 2026-10-13)

Report: `data/round3/checks/R3Q.md`. Logs: `data/round3/check_R3Q/`. All programs are pure Python 3 (standard library only),
were written from the statements in `data/round3/reports/R3Q.md`, and share no code with `code/round3/R3Q/`.
Run with `nice -n 10 python3 -I`, one core.

| file | what it checks | log | wall |
|---|---|---|---|
| `cert3.py` | Lemma 3 finite checks (a)-(e), by dual numbers and subset-sum tables; repeated with 1 and 2 extra bits of x; valuation facts of the reduction by brute force mod 2^20 | `cert3.log` | 0.6 s |
| `lemma_tests.py 1` | random exact tests (mod 2^600) of Lemmas 1, 2(c), 3, 4, 5 (one-step identity, recomputed from scratch at every x' = x + 2^m w, with a rho := 1 negative control), 6(a)(b)(c), 8, 9 (a)-(d) incl. the Taylor congruence and kappa <= j | `lemma_tests.log` | 853 s |
| `bounds_check.py table` | exact re-evaluation of every row of the report's Corollary D and Theorem A tables from the logged parameters, with all hypotheses re-checked; own dyadic tail bound for the failure sums | `table.log` | 8 s |
| `bounds_check.py ruleA 1024 1536 2048 4096` | exact values under the Theorem A' rule | `ruleA.log` | <1 s |
| `bounds_check.py closed 4000000` | closed-form inequalities of Theorems A' and C (terms as written in the report's proofs) on [1024, 4e6] and [2400, 4e6], plus the integer side conditions of both rules | `closed_and_ruleC.log` | 19 s |
| `bounds_check.py ruleC 3072 3264 1` | exact bound under the rule R(K) of Theorem C, every K in [3072, 3264] | `closed_and_ruleC.log` | 24 s |
| `run_ruleC_blocks.sh` | exact bound under R(K) at K = 3584, 4096, 8192, 16384 and at K = 64M+63 (worst K of each M-block) for M = 48..400 | `ruleC_blocks.log` | 75 s |
