# Round-2 logs and data (note.md §10)

| dir | what |
|---|---|
| `logs_original/R1a/`, `R1b/`, `R2a/`, `R2b/`, `R3/` | Original logs of the five round-2 tracks (2026-10-11). `R3/` includes both programs' covering certificates, the chain outputs (`CHAIN_*.txt`), the minimality scans (`scan_p*.log`), and `PREDICTIONS_registered.txt` (see Conjecture 10.24 for which predictions count as out of sample). |
| `R1a_explore/` | Data files written by the R1a exploration scripts. |
| `outputs/` | The lead-author instance's re-runs of 2026-10-12 (rows S1–S14 and C1–C6 of note.md §10.7). `outputs/R3/` holds the certificate re-runs; `outputs/R3_p17_programB_original/` holds program B's original p = 17 logs, which were not re-run. |
| `review/logic/`, `review/computation/`, `review/novelty/` | Logs of the three round-2 AI referees (2026-10-12). `review/computation/logs/U7_t3_H49_full.log.gz` is gzipped; it is about 6 MB uncompressed. |

Notes:
- File modification times are not preserved by git. The timestamps quoted in note.md §10.5 (Conjecture 10.24) come from the working directory, and from the registration file's own header.
- One path-only edit was made. In `outputs/lead_batch_times.log`, absolute local paths were replaced by `<code_r2>` and `<FORMAL_DIR>`.
- The novelty referee also read third-party files (Kitamura's repositories, earlier AI write-ups). None of them is redistributed here; see note.md §2 and the References for links.
