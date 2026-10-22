## depth-8 positions, p=19 (one log per (K,program))
| log | prog | p,t,H | K'' | misses | outcome | wall (s) | max RSS (GB) | start | end | complete |
|---|---|---|---|---|---|---|---|---|---|---|
| P19_t8_H47_K1_A | A' | 19,8,47 | 1 | 2739774 | NOT_COVERED | 2593 | 2.88 | 2026-10-12 14:49:50 CDT | 2026-10-12 15:33:03 CDT | True |
| P19_t8_H49_K1_A | A' | 19,8,49 | 1 | 0 | COVERED | 2236 | 2.86 | 2026-10-12 15:33:18 CDT | 2026-10-12 16:10:35 CDT | True |
| P19_t8_H49_K1_C | C' | 19,8,49 | 1 | 0 | COVERED | 2186 | 2.86 | 2026-10-12 15:01:05 CDT | 2026-10-12 15:37:31 CDT | True |
| P19_t8_H49_K2_A | A' | 19,8,49 | 2 | 0 | COVERED | 2452 | 2.97 | 2026-10-12 16:10:35 CDT | 2026-10-12 16:51:27 CDT | True |
| P19_t8_H49_K2_C | C' | 19,8,49 | 2 | 0 | COVERED | 1386 | 2.96 | 2026-10-12 15:37:31 CDT | 2026-10-12 16:00:37 CDT | True |
| P19_t8_H49_K3_A | | | | | (no result line) | | | 2026-10-20 17:27:25 CDT | None | False |
| P19_t8_H49_K3_A_INTERRUPTED_20261012 | | | | | (no result line) | | | 2026-10-12 16:51:27 CDT | None | False |
| P19_t8_H49_K3_C | C' | 19,8,49 | 3 | 0 | COVERED | 1557 | 2.97 | 2026-10-12 16:00:37 CDT | 2026-10-12 16:26:34 CDT | True |
| P19_t8_H49_K4_C | C' | 19,8,49 | 4 | 0 | COVERED | 1435 | 2.97 | 2026-10-12 16:26:34 CDT | 2026-10-12 16:50:30 CDT | True |
| P19_t8_H49_K5_C | | | | | (no result line) | | | 2026-10-20 17:27:23 CDT | None | False |
| P19_t8_H49_K5_C_INTERRUPTED_20261012 | | | | | (no result line) | | | 2026-10-12 16:50:30 CDT | None | False |

## depth-7 classes K'' mod 19^2 at H=45 (program A', chunks)
| log | classes | covered | failed | total wall (s) | start | end | complete |
|---|---|---|---|---|---|---|---|
| U19_t7_H45_A_chunk1 | 36 (20..56) | 36 | 0  | 2921 | 2026-10-12 15:21:41 CDT | 2026-10-12 16:10:22 CDT | True |
| U19_t7_H45_A_chunk2 | 36 (58..94) | 36 | 0  | 2621 | 2026-10-12 16:10:22 CDT | 2026-10-12 16:54:03 CDT | True |
| U19_t7_H45_A_chunk3 | 10 (96..105) | 10 | 0  | None | 2026-10-20 17:27:27 CDT | None | False |
| U19_t7_H45_A_chunk3_INTERRUPTED_20261012 | 13 (96..108) | 13 | 0  | None | 2026-10-12 16:54:03 CDT | None | False |

classes 19<K''<361 certified by A' (complete logs only): 82/324; failures: []; missing: [106, 107, 108, 109, 110, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126]...
