# verify_M4D_falsify (round 4): numerical falsification of M4D's Lemma L, Theorem F, Corollary F1

Report: `data/round4/checks/M4D_falsify.md`. Logs: `data/round4/verify_M4D_falsify/`. Each run starts with its command line and start time and ends with its exit code and wall time; `run.sh` writes these lines. All runs used `nice -n 10`, one at a time, with a 30-minute timeout.

This code was written from the definitions (note.md §1.2–1.4, M4D.md §1–2). It shares no code with `code/round4/M4D/` or with `code/round4/verify_M4D_logic/`. Every x is a natural number, which is a genuine point of Z_p and not a negative integer. All arithmetic uses exact Python integers or `Fraction`; residues are taken only at the end. numpy is used only for boolean subset-sum bitsets, and `t5` cross-checks those against Python sets.

| file | purpose |
|---|---|
| `fz_core.py` | Core library. Valuations; π_n, π_n′ and V_n; alive paths three ways (brute force over all 2^(n−1) paths, pruned DFS on exact S_e, carry-recursion DP on targets); targets −S/π_n mod p^k; window elements, sums and lift counts |
| `t1_basics.py` | Checks: (F1) V_n ≥ v_p(n!); the deletion step P(x,n) ⇔ g_p ≥ V_n; DFS against brute force; DP against DFS; (F2), its converse and the target formula, over all parents (alive or not) and all digit words; locality of all chain data on cylinders |
| `t2_lemmaL.py` | Lemma L by brute force: the child targets mod p^{D′}, found from the definition over all 2^H words, against λ(Lift(r)); injectivity; counts; "cover ⇔ complete". Edge samplers: x near −1, near −2, near small negative integers, and gates at the start, middle or end of W or W′. Records slopes and the linear regime. Negative controls: unit 2u; divisor p^{D+1} |
| `t3_thmF.py` | Theorem F at finite horizon, exhaustive over all critical θ-sequences (which covers every θ ∈ (0,1]^L), plus a literal `Fraction` re-evaluation with random θ. Special cases: Tao's block lemma (θ = p^{−D}) and θ = 1 (fullness, R2b's Theorem 10.12 in both directions). Also Prop F2(a) and the F2(b) key step. Negative controls: (II) with ≥ in place of >; (I) dropped; index slip |
| `t4_corF1.py` | Corollary F1 at finite horizon, by exhaustive Haar enumeration of the cylinders of a base set B (B = Z_p, or a cylinder at a gate or near −2). Checks the pointwise implication on every determined cylinder and the integrated inequality in exact rationals |
| `t5_deep_highslope.py` | Lemma L for x extremely close to −m (v(x+m) = 6, 9, 12; moduli up to p^18), with windows before, straddling, and after the gate, and on the explicit high-slope cube path (1,1,0,1,0,…) at x ≡ −2 |
| `run.sh` | logging wrapper |

Reproduce, for example:
```
./run.sh LOG python3 t2_lemmaL.py 7 303 2000
./run.sh LOG python3 t3_thmF.py 7 505 400
./run.sh LOG python3 t4_corF1.py 7 7 0 0 7 8 8 8
```
