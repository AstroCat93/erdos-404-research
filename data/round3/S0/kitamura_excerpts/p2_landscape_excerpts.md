# Excerpts from K. Kitamura, github.com/KitaKen1/erdos-404-p2-landscape
# (Names of AI tools in the original AI-usage disclosures are redacted in this copy, per project policy; see the original source.)
# Commit 32697193c8a3259ef090ba1c1a6b5fb135184223 (2026-07-08 07:50:20 +0900), branch main; cloned 2026-10-13 ~05:55 UTC.
# Licensed Apache-2.0 by the repository owner; reproduced verbatim (excerpts) for citation. Line numbers refer to that commit.

## witness_gallery.md, lines 195-213 (section 9: a = 594)

## 9. The champion without an exact value: a = 594

The deepest-surviving plain integer currently known.  Certified by an
increasing ladder of probes (selected rows; each row is an independently
verified finite decision; state as of 2026-07-06):

```text
g(594,2) >= 8192      55 s
g(594,2) >= 16384     10 min
g(594,2) >= 32768     61 min
g(594,2) >= 65536     3.5 h      =>  f(594,2) >= 66126
```

That is 3.5 times the depth of the a = 34 record — and still no death.
Either a deeper probe eventually fails, and 594 becomes the largest exact
value ever computed, or it never does.  The second possibility is exactly
the open core of Erdos #404 at p = 2: a positive even integer with
`f(a,2) = infinity` could never be certified by finite computation, only
by a new idea.

## determining_exact_values.md, lines 196-237 (end of section 4 and section 5)

`n!/34!` modulo `2^18412` and checks the sum, sharing no code with the
search.  House rule for every published exact value:

```text
lower side:  explicit witness file, re-verified from the definition;
upper side:  the no-witness decision, re-run in a second, independently
             written DP implementation.
```

The same pipeline produced `f(1102,2) = 12633`, `f(3456,2) = 8275`, and
`f(8190,2) = 16396`, whose witness files (except 8190) ship in `data/`.

## 5. Why this terminates — and the one thing it cannot do

For each fixed `G` the decision `g(a,2) >= G` is finite.  So IF `f(a,2)`
is finite, running `G = 1, 2, 3, ...` eventually hits the first failure
and the procedure halts with a two-sided certificate.  Every even
`a <= 256` has halted, and so have the deeper spikes 1102, 3456, and
8190 — but see the champion below for one that has not halted yet.  In this precise
sense f(a,2) is exactly determined at every a where it is finite — and
the complete classification of all even classes with `g <= 24` (a finite
certified computation over 174,640 residue classes) determines it
simultaneously for MOST integers: the surviving fraction decays like
`~ 11.5/G`.

What the procedure can never do is certify `f(a,2) = infinity`.  A
witness only ever proves a lower bound; "no death at depth G" only says
`g >= G`.  The open core of Problem #404 at p = 2 is exactly:

```text
Is f(a,2) finite for every positive even a?
```

The current champion illustrates the asymmetry: `a = 594` is certified

```text
f(594,2) >= 66126        (g(594,2) >= 65536, verified 2026-07-06)
```

with deeper probes still running.  Either some probe finally fails — and
594 joins the exact table with the largest value ever computed — or it
never does, and no amount of computation will tell us.

## README.md, lines 30-60 (Main contribution 1)

## Main contribution 1: exact values of f(a,2), 1 ≤ a ≤ 256

`f(a,2)` is exactly computed — an explicit lower witness AND a proof that
no list reaches one exponent higher — for every `1 <= a <= 256`.  A
sampled walk across the range (full table:
[data/p2_exact_table_1_256.csv](data/p2_exact_table_1_256.csv)):

| a      | 1 | 2   | 3 | 4 | 5 | 6   | 7 | 8  | 9 | 10 | 11 | 12 | 13 | 14   | 15 | 16  |
|--------|--:|----:|--:|--:|--:|----:|--:|---:|--:|---:|---:|---:|---:|-----:|---:|----:|
| f(a,2) | 0 | 254 | 1 | 6 | 3 | 133 | 4 | 13 | 7 | 14 |  8 | 13 | 10 | 1533 | 11 | 548 |

| a      | ... | 30  | 31 | 32 | 33 | 34    | 35 | 36 | ... | 62  | 63 | 64  | ... |
|--------|:---:|----:|---:|---:|---:|------:|---:|---:|:---:|----:|---:|----:|:---:|
| f(a,2) | ... | 126 | 26 | 37 | 31 | 18444 | 32 | 37 | ... | 254 | 57 | 261 | ... |

| a      | ... | 126 | 127 | 128 | ... | 150 | ... | 158 | ... | 254 | 255 | 256 |
|--------|:---:|----:|----:|----:|:---:|----:|:---:|----:|:---:|----:|----:|----:|
| f(a,2) | ... | 276 | 120 | 141 | ... | 157 | ... | 316 | ... | 895 | 247 | 459 |

Every row of the full table is clickable in the
[GitHub Pages viewer][github-pages]: the witness list opens next to the
table and can be re-verified in the browser.  A handful of deeper rows —
up to the record `f(34,2) = 18444` —
are also exactly determined; those are collected in the observations
appendix.

And you can check the Lean certificates in your browser — lean4web, no
install needed.  Three files, one per value, each sandwiching its value
from below and above:

- **[f(5,2) = 3 — open in lean4web][lean4web-5-2]**: exact, both bounds

## README.md, lines 225-238 (open core)


```text
a:            4     12     20     28
v_2(a!):      3     10     18     25
f(a,2):       6     13     21     28        = v_2(a!) + 3, every time.
```

What remains open is exactly one statement — the open core of #404 at
`p = 2`: **is `f(a,2)` finite for EVERY even `a`?**  The measured
survival density decays like `~ 11.5/G`, and every tracked spike except
the champion 594 (observations appendix) has died — but a hypothetical infinite
survivor could never be certified by computation of this kind: witnesses
only ever prove lower bounds.


## README.md, lines 329-351 (records) and 385-418 (shadow family, exactness classes)

## Appendix: interesting observations

### The records

The largest exact values known, each certified by the two-sided pipeline
of contribution 2:

| a    | f(a,2) | lower witness                        |
|-----:|-------:|--------------------------------------|
|   34 |  18444 | 9216-term list — ships in `data/`    |
| 8190 |  16396 | `8190 = 2^13 - 2`, shadow family     |
| 1102 |  12633 | 5731-term list — ships in `data/`    |
| 3456 |   8275 | 2392-term list — ships in `data/`    |
|   14 |   1533 | `14 = 2^4 - 2`, shadow family        |
|    2 |    254 | 119-term list — proved in Lean       |

Beyond all of these sits one certified lower bound whose exact value is
still being hunted:

```text
f(594,2) >= 66126        the current champion; no death found yet
```

### The shadow family a = 2^t - 2

Here the cube identity guarantees depth `g >= 3t` — and the actual
values ignore the guarantee and follow no visible pattern:

| t           | 2   | 3   | 4    | 5   | 6   | 7   | 8   | 9    | 10   | 11   | 12   | 13    |
|-------------|----:|----:|-----:|----:|----:|----:|----:|-----:|-----:|-----:|-----:|------:|
| a = 2^t - 2 | 2   | 6   | 14   | 30  | 62  | 126 | 254 | 510  | 1022 | 2046 | 4094 | 8190  |
| f(a,2)      | 254 | 133 | 1533 | 126 | 254 | 276 | 895 | 1019 | 1195 | 2603 | 4443 | 16396 |

Two curiosities inside this one table: `f(62,2) = 254 = f(2,2)` — a pure
numerical coincidence (the two rows die at different normalized
depths) — and the `t = 13` member exploding to 16396, the second-largest
exact value known.

### Exact values no search could ever touch

Exactness is contagious upward: `g` is constant on the residue class
`a mod 2^g(a)`, so each finite row pins infinitely many integers.

```text
from f(2,2)  = 254:    every a == 2 (mod 2^253) has g(a,2) = 253
                       — exact rows at 77-digit integers;
from f(34,2) = 18444:  every a == 34 (mod 2^18412) has g(a,2) = 18412
                       — exact rows at 5543-digit integers.
```

All of the objects behind this appendix are laid out to be LOOKED AT in
the witness gallery, [witness_gallery.md](witness_gallery.md): the full
119-term list for `f(2,2)`, the anatomy of the a = 34 record, the shadow
table — at-a-glance lists and tables, every number machine-verified.
The raw witness files live in `data/`, and the
[GitHub Pages viewer][github-pages] makes every row clickable with
in-browser re-verification.

## README.md, lines 273-313 (Reproduce, AI usage)

## Reproduce

Definition-level verification of the three big witnesses (seconds):

```bash
python3 scripts/verify_witness_file.py --a 34   --g 18412 --file data/a34_g18412_witness_indices.txt
python3 scripts/verify_witness_file.py --a 1102 --g 11536 --file data/a1102_g11536_witness_indices.txt
python3 scripts/verify_witness_file.py --a 3456 --g 4823  --file data/a3456_g4823_witness_indices.txt
```

The two-sided boundary of the biggest spike (seconds each):

```bash
python3 scripts/p2_scaled_gate_search.py one --a 34 --extra-target 18412 --max-states 100000   # witness exists
python3 scripts/p2_scaled_gate_search.py one --a 34 --extra-target 18413 --max-states 100000   # no witness
```

(`extra-target` counts beyond `v_2(34!) = 32`, so these are the decisions
`f(34,2) >= 18444` and `f(34,2) >= 18445`.)

An ordinary exact row, upper decision for `f(2,2)`:

```bash
python3 scripts/p2_exact_search.py one --a 2 --p 2 --target 255      # -> no witness, so f(2,2) <= 254
python3 scripts/p2_exact_search.py exact --a 4 --p 2 --limit 20 --witness   # -> f(4,2) = 6, witness [4,5,7]
```

The Lean certificates (needs any recent Lean 4; last checked with 4.31.0):

```bash
lean lean/S404_5_2_exact.lean
lean lean/S404_4_2_exact.lean
lean lean/S404_2_2_254.lean
lean lean/S404_lean4web_2_2.lean    # f(2,2) = 254 EXACT: the kernel replays the search (~6 min)
```

## AI usage

The Lean formalizations, the search programs, and the write-ups in this
repository were prepared with assistance from
[AI tool names redacted in this copy].
