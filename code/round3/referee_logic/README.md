# Round-3 logic referee: code and logs

Report: `data/round3/referees/logic.md`. Scratch: `/tmp/r3_ref_logic/`. Everything ran on one core under `nice -n 10`.

| program | what it tests | command | log (`logs/`) | wall |
|---|---|---|---|---|
| `s0_lemma.c` | Lemma S0.1 exactly (all n <= 2^18), and the closed form P(E_{2^m}) = (2m+3)/2^(m+2) | `gcc -O2 -o /tmp/r3_ref_logic/s0_lemma s0_lemma.c && /tmp/r3_ref_logic/s0_lemma 10` and `... 18` | `s0_lemma.log` | 0.24 s |
| `s0_walk_mc.py` | the walk of Lemma S0.1 equals the note's W_n = n - V_n; Monte Carlo of P(E_n) | `python3 -I s0_walk_mc.py 20261013 4000 512` | `s0_walk_mc.log` | 5 s |
| `c2_test.py` | definition-level test of R3M Cor A' (L = 0), Prop B(ii), Prop C2 and Prop N (note Props 11.10-11.13): slope-0 populations found by DFS over all words, cylinder sampled exhaustively | `python3 -I c2_test.py p SEED NSAMPLES n H H' MAXCYL [1 = single parents only]`; the configurations are the `### command:` lines of the logs | `c2_test.log`, `c2_single.log`, `c2_single2.log` | about 17 min in total |

One run (`c2_test.py 7 32 10 21 7 7 2500`) was stopped by hand after 562 s because the DFS at p = 7, n = 21 is too large for Python; it produced no result and none is used.
