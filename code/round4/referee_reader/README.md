# Round-4 fresh-reader referee: code

- `qs_check.py`: recomputes the block constants $q_1(p)$, $q_2(p)$ of note.md §12.1 exactly (integer DP over residues, weights 2,1,1 for the lazy signed digit). Written from the definition in §12.1; shares no code with the tracks.
  Run: `nice -n 10 python3 -I qs_check.py 7 11 13 17 19 23` (under 1 minute).

The other re-runs in the report (`fe_verify.py` at p = 7, `assemble.py` at p = 11, 13, 41) used the tracks' own code read-only, from the scratch directory `/tmp/r4_ref_reader/`.
