#!/usr/bin/env python3
"""Two-sided re-check of K. Kitamura's published table of f(a,2), 1 <= a <= 256.

Input : Kitamura's CSV (data/p2_exact_table_1_256.csv of github.com/KitaKen1/erdos-404-p2-landscape,
        commit 32697193; a copy is in data/round3/S0/kitamura_excerpts/).
Engine: the round-1 track-D program code/D/sumform_big.c (C, multi-limb, "sum form" DP),
        which shares no code with Kitamura's Python scripts.  For every row (a, f) it decides
        "2^f | some sum of distinct factorials with minimum a"   (must be: reachable)
        "2^(f+1) | ..."                                          (must be: not reachable)
Odd a are also compared against the closed form f(a,2) = v_2(a!) = a - s_2(a).

Usage: python3 -I check_kitamura_table.py CSV SUMFORM_BIG_BINARY [--skip a1,a2,...]
Exit status 0 iff every decision agrees with the table.
"""
import csv
import subprocess
import sys
import time


def v2_fact(n):
    return n - bin(n).count("1")


def run(binary, a, k):
    out = subprocess.run([binary, str(a), str(k)], capture_output=True, text=True, timeout=3600).stdout.strip()
    if out.startswith("trivially reachable"):
        return True, out
    if "reachable=1" in out:
        return True, out
    if "reachable=0" in out:
        return False, out
    raise RuntimeError(f"inconclusive output for a={a} K={k}: {out!r}")


def main():
    csv_path, binary = sys.argv[1], sys.argv[2]
    skip = set()
    if "--skip" in sys.argv:
        skip = {int(x) for x in sys.argv[sys.argv.index("--skip") + 1].split(",") if x}
    rows = list(csv.DictReader(open(csv_path)))
    assert [int(r["a"]) for r in rows] == list(range(1, 257)), "table must list a = 1..256"
    bad = 0
    t_all = time.time()
    for r in rows:
        a, f = int(r["a"]), int(r["value"])
        assert r["p"] == "2" and r["status"] == "exact"
        if a % 2 == 1 and f != v2_fact(a):
            print(f"MISMATCH odd a={a}: table {f} vs v2(a!)={v2_fact(a)}")
            bad += 1
        if a in skip:
            print(f"a={a} f={f}: skipped (--skip)")
            continue
        t0 = time.time()
        lo, out_lo = run(binary, a, f)
        hi, out_hi = run(binary, a, f + 1)
        dt = time.time() - t0
        ok = lo and not hi
        bad += 0 if ok else 1
        print(f"a={a} f={f} g={f - v2_fact(a)} method={r['method']}: K=f {'reachable' if lo else 'NOT reachable'}; "
              f"K=f+1 {'reachable' if hi else 'not reachable'} -> {'OK' if ok else 'MISMATCH'} ({dt:.2f} s)")
        sys.stdout.flush()
    print(f"rows checked: {len(rows)}, mismatches: {bad}, wall {time.time() - t_all:.1f} s")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
