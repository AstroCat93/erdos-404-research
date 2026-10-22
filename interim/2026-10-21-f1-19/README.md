# Interim update (2026-10-21): f(1,19) >= 17,927,094,312

> **Status**
> - **Computer-assisted.** The bound rests on finite exact computations plus Proposition 10.10 of [`note.md`](../../note.md).
> - Every certificate it uses was checked by **two independently written programs** (three where stated below).
> - Produced by Claude (Anthropic) AI instances. **Not yet refereed by the round-3 referees.**
> - **The human author, Nathan Durfee, has not verified the mathematics.**
> - If it holds up, it supersedes the round-2 bound $f(1,19)\ge 943\,531\,272$ (note.md §10.2).
> - The full round-3 note (§11 of note.md) will follow; this page is released early and may be corrected.

## Statement

$$f(1,19)\ \ge\ v_{19}\big((19^9-1)!\big) \;=\; \frac{19^9-1-9\cdot 18}{18} \;=\; 17\,927\,094\,312 .$$

The previous bound was $v_{19}((19^8-1)!)=943\,531\,272$, so the new one is about 19 times larger.

**Dichotomy for general $a$.** Proposition 10.10 gives the same conclusion for every starting point, with largest window $H^*=49$. For every $a<19^9-49$, either
$$f(a,19)<v_{19}\big((a+49)!\big)\qquad\text{or}\qquad f(a,19)\ge 17\,927\,094\,312 .$$

## How it follows from Proposition 10.10

Notation is that of note.md §3.7. Write $c=v_{19}((H-1)!)$ and $y_i(K)=\prod_{s=1}^{i}(19^tK-(H-s))$. Theorem 3.12(a) says this: if the $2^H$ subset sums of $\{y_i(K'')\}_{i<H}$ cover $\mathbb Z/19^{t+c}$, the block of $H$ factorials ending at $N^*=19^tK''$ lifts $P(1,19,N^*-H)$ to $P(1,19,N^*)$. Proposition 10.10 (chain criterion) with $D=9$ excludes a first failure below $19^9$. It needs a certificate at every depth $1\le t\le 8$:

| depth $t$ | what is needed | window | certified by | source |
|---|---|---|---|---|
| 1–6 | uniform $\mathrm{Cov}(19,t,H_t)$, $H_t+1<19^t$ | $H_t=5,12,17,27,31,35$ | **A, B, C** (three programs) | round 2 (note §10.2) |
| 7 | positions $K''\le 18$ | $H=45$ ($c=2$, $M=9$) | **A, B, C** (three programs) | round 2 (note §10.2) |
| 7 | the 324 classes $K''=20,\dots,360$ with $19\nmid K''$ | $H=45$ | **A′ and C′** (new) | `logs/U19_t7_H45_{A,C}_chunk*.log` |
| 8 | all 18 positions $K''=1,\dots,18$ | $H=49$ ($c=2$, $M=10$) | **A′ and C′** (new) | `logs/P19_t8_H49_K*_{A,C}.log` |

At depth 7 the first-failure candidates below $19^9$ are $19^7K''$ with $K''<19^2$ and $19\nmid K''$. These are exactly the 342 unit classes mod $19^c=19^2$. At depth 8 they are $19^8K''$ with $K''\le18$. Every window satisfies $19^tK''-H>1$.

All 342 depth-7 classes and all 18 depth-8 positions are reported `COVERED` with 0 misses, by both programs, in every job log. The chain-check script `code/chain_r3.py` gives the following on the full set of round-2 and round-3 logs:
- with 2 programs required per certificate: `CHAIN OK (2 program(s) per certificate): no first failure below 19^9; f(1,19) >= v_19((19^9-1)!) = 17927094312`;
- with 3 required: `CHAIN INCOMPLETE`. This is expected, because the new certificates have exactly two programs.

The output is in `logs/chain_r3_final.log`. A separately written parser re-checked the logs and agrees, and so did the independent audit below.

## Registered out-of-sample predictions (Conjecture 10.24)

The predictions were registered in `logs/PREDICTIONS_registered_r3.txt`. Its header gives **2026-10-12 14:36:09 CDT (unix 1791833769)**, before any of the runs below. The first validation run started at 14:41:51, and the first depth-8 run at 14:49:50.

| case | $\nu$ | prediction | outcome |
|---|---|---|---|
| $(19,8,47)$ at $K''=1$ | 0.527 | FAIL | **fails**, with exactly **2,739,774** missed residues mod $19^{10}$ in **both** A′ and C′ |
| $(19,8,49)$ at all 18 positions | 2.660 | HOLD | **holds**: all 18 positions covered by both A′ and C′ |

The other rows of the registration file were not run: $(19,8,48)$, $(19,8,50)$ and the $p=13$, $t=9$ rows. The C′ replication of the 324 depth-7 classes was registered separately in `logs/PREDICTIONS_registered_r3_cont2.txt` (2026-10-21 12:00:42 CDT), predicting 324/324 covered. That prediction was confirmed. It is a replication, not a test of the conjecture. The timestamps come from the files' own headers and the working directory. They are not externally attested.

## Independent audit (2026-10-21)

Before release, a separate AI instance audited the bound adversarially, without using `chain_r3.py` or the track's parsers. Its files are in `audit/`.
- **Requirements re-derived** from Proposition 10.10 and Theorem 3.12(a) alone: 417 certificates (depths 1–3: one class each; depths 4–6: 18 classes each; depth 7: 342 classes; depth 8: 18 positions). Every window satisfies $H+1<19^t$ or $19^tK''-H>1$ as needed. It also checked that both programs build the window ending exactly at $19^tK''$ and reduce modulo $19^{t+c}$ with $c$ from Legendre's formula.
- **Fresh log parser** (`audit/audit_parse.py`, output `audit/parse_out.txt`). It counts only completed runs, using each program's own final line and excluding interrupted logs. Result: all 417 requirements are met by at least two program families, with **0 gaps** and **0 conflicts**. The $(19,8,47)$ failure count is 2,739,774 in both programs.
- **Spot re-runs** from freshly built binaries on 6 randomly chosen depth-7 classes ($K''=29,34,111,145,155,328$): all covered by A′ and C′, and by the original round-2 program C on $K''=145,155,328$. A lifted representative ($K=390\equiv29$) is also covered. Logs: `audit/logs/`.
- **Own brute force** (`audit/mini_brute.py`, actual factorials): 218 comparisons against A′, C′ and C on small cases, 42 of them failing cases with exact miss counts, **0 mismatches**.
- **Legendre's formula** recomputed with separate code: $17\,927\,094\,312$.
- The audit did **not** re-run depth 8 (about 3 GB per run).
- Verdict: **confirmed, with caveats.** The caveats it found are minor and listed below; none affects the bound.

## Caveats

- **A′ and C′ are not new from scratch.** They are memory-reduced modifications, made in round 3, of round-2 program A (track R3) and program C (round-2 computational referee). The in-place shift-OR kernels were written separately for each. Both were validated:
  - on **1,325 brute-force comparisons**: 817 failing cases with exact miss counts, 0 mismatches (`logs/validate_ip.log`, re-run for this page with the same result);
  - on archived depth-7 results (`logs/VAL_*.log`), including the published $(19,7,44)$ failure pattern: misses $4,8,4,4,4,4,4$ at $K''=1,5,9,11,12,14,16$.
- **No third program at depth 8**, and no brute force at that size: a fibre there is $19^8$ bits, about 2 GB.
- **Proposition 10.10 has been refereed by AI only** (note §10.8). The class reduction in Theorem 3.12(a) is a paper proof, and only the abstract lifting logic is in Lean.
- **Round 3 has not been refereed.** The round-3 referees have not yet reviewed this computation or this page.
- **The `exit=` field is not the program's exit status.** In the `# END` lines of the job logs, `exit=` is always 0 because of how `code/run_job.sh` builds that line. Completeness is shown instead by each program's own final line (`SUMMARY A'` / `END C'`), which is present in all 65 job logs.
- **`chain_r3.py` is lenient.** It does not require a completed run and it counts the 13 classes in the interrupted log listed below. It also silently skips a missing log directory (the track's own command named `data/round2/logs_lead/R3`, which does not exist; the command below uses `outputs/R3`). Neither affects the result: the audit's stricter parser excludes the interrupted log and still finds every certificate.
- **Note §10.2 wording.** For the $p=19$, depth-7, $H=45$ entry, program C's round-2 logs use the positions $K''=1,\dots,18$ themselves, not the lifted representatives that note §10.2 mentions. That is valid for positions, but the note's wording is inaccurate for this entry.
- **Excluded logs.** Three runs were killed by a session cut-off on 2026-10-12 and were later re-run in full. Their logs are not used and not included:
  - `P19_t8_H49_K3_A_INTERRUPTED_20261012.log`
  - `P19_t8_H49_K5_C_INTERRUPTED_20261012.log`
  - `U19_t7_H45_A_chunk3_INTERRUPTED_20261012.log`
- **Resources.** Depth-8 runs took up to 2,593 s and up to $3.241\cdot10^9$ bytes maximum RSS. Depth-7 classes took 30–82 s each at about 0.24 GB.

## Reproduction

Run from this directory (`interim/2026-10-21-f1-19/`). The round-2 logs are in `../../data/round2/`.

```sh
mkdir -p bin
clang -O2 -o bin/fibcov_ip code/fibcov_ip.c -lm      # program A'
clang -O2 -o bin/covchk_ip code/covchk_ip.c -lm      # program C'

# chain check, seconds (N = programs required per certificate: 1, 2 or 3)
L=../../data/round2
python3 code/chain_r3.py 19 9 "$L/outputs/R3:$L/logs_original/R3:$L/review/computation/logs:logs" code/specs_p19_D9_r3.txt 2

# brute-force validation (needs numpy; about 30 s; uses ../../code/round2/R3/src/brute.py)
python3 code/validate_ip.py

# one depth-7 class (about 1 min, 0.24 GB each) and the failing depth-8 case (11-45 min, about 3.2 GB)
bin/fibcov_ip 19 7 45 2 pos 20 ; bin/covchk_ip 19 7 45 2 pos 20
bin/covchk_ip 19 8 47 2 pos 1       # expect miss=2739774 UNCOVERED
bin/covchk_ip 19 8 49 2 pos 1       # expect miss=0 COVERED (repeat for K'' = 2..18)
```

`code/results_table.py` regenerates `logs/results_table_final.md` from `logs/`. The batch scripts are `run_job.sh`, `worker_*.sh` and `val_big.sh`. They expect `T3B_WORKDIR` to point to a directory that contains `src/` (these scripts), `bin/`, `logs/`, `locks/` and the queue files.

**Changes made for publication.** Program logic is unchanged.
- In the seven shell scripts, the hard-coded absolute working directory `W=...` became `W="${T3B_WORKDIR:?...}"`.
- In `validate_ip.py`, the absolute path to the round-2 `brute.py` became `$ERDOS404_R3_SRC`, which defaults to `../../../code/round2/R3/src` relative to the script.
- In the logs, the machine hostname was replaced by `host=<host>` (65 lines).

Everything else is byte-identical to the working copies. `code/specs_p19_D9.txt` is the superseded 2026-10-12 spec, which listed only 18 depth-7 positions. Use `code/specs_p19_D9_r3.txt`.

## Credit

- **The method is Tao's programme.** It uses Tao's block lemma and the suggestion that each depth reduces to one finite computation (forum, 29 Sep 2025), as carried out in note.md §3.7.
- **Earlier work by others.** K. Kitamura's computations and bounds came first (note §2). The round-1 and round-2 bounds at $p=19$ are in note §4.2 and §10.2.
- **Programs.** Round-2 track R3 wrote programs A and B, `brute.py`, `chain.py` and Conjecture 10.24 with `bottleneck.py`. The round-2 computational referee wrote program C. Round-3 track T3b wrote A′, C′, `chain_r3.py` and the runs reported here.
