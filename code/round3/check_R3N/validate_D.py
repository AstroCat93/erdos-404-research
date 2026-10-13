#!/usr/bin/env python3
"""check_R3N: validate the own solver dfsD (and the own verifier verify_w.py).

Part 1 (kitamura): every row of K. Kitamura's p2_exact_table_1_256.csv.
  odd a : value must equal v_2(a!) (the trivial family a = -1 mod 2).
  even a: dfsD at K = f must be reachable (witness written and checked by verify_w.py to have
          v_2 = f exactly, unless f = v_2(a!), where {a} is the witness), and dfsD at K = f+1
          must be unreachable with EXACT f.
Part 2 (survey): a seeded random sample of exact rows of the track's survey CSVs (and of the
  shadow CSV), same two-direction test (witnesses are checked only for f - v_2(a!) <= 20000 to
  keep the Python verifier cheap).
Usage: python3 -I validate_D.py kitamura TABLE.csv BIN VERIFIER
       python3 -I validate_D.py survey NSAMPLE SEED BIN VERIFIER CSV [CSV ...]
       python3 -I validate_D.py survey 0 -1 BIN VERIFIER a1,a2,... CSV [CSV ...]   (explicit rows)
       python3 -I validate_D.py full A0 A1 BIN VERIFIER CSV [CSV ...]   (every exact row in [A0, A1])
"""
import csv
import random
import subprocess
import sys
import time


def v2f(n):
    return n - bin(n).count('1')


def run_D(binary, a, K, wpath=None):
    args = [binary, str(a), str(K)] + ([wpath] if wpath else [])
    out = subprocess.run(args, capture_output=True, text=True, check=False).stdout
    reach, exact = None, None
    for l in out.splitlines():
        if l.startswith('RESULT'):
            reach = 1 if 'reachable=1' in l else 0
        elif l.startswith('EXACT'):
            exact = int(l.split(' f=')[1].split()[0])
    return reach, exact


def verify(verifier, wpath, a, K):
    r = subprocess.run([sys.executable, '-I', verifier, wpath, str(a), str(K)], capture_output=True, text=True)
    return r.returncode == 0


def check_row(binary, verifier, a, f, wpath, check_witness=True):
    va = v2f(a)
    r1, _ = run_D(binary, a, f, wpath if f > va else None)
    r0, ex = run_D(binary, a, f + 1)
    ok = (r1 == 1 and r0 == 0 and ex == f)
    wok = None
    if ok and f > va and check_witness:
        wok = verify(verifier, wpath, a, f)
        ok = ok and wok
    return ok, r1, r0, ex, wok


def main():
    mode = sys.argv[1]
    wpath = '/tmp/r3_check_R3N/val_w.txt'
    if mode == 'kitamura':
        table, binary, verifier = sys.argv[2], sys.argv[3], sys.argv[4]
        nodd = neven = nbad = nw = 0
        t0 = time.time()
        for row in csv.DictReader(open(table)):
            a, f = int(row['a']), int(row['value'])
            if row['p'] != '2' or row['status'] != 'exact':
                print(f"unexpected row {row}")
                nbad += 1
                continue
            if a % 2:
                nodd += 1
                if f != v2f(a):
                    print(f"BAD odd a={a}: table {f} != v2(a!) {v2f(a)}")
                    nbad += 1
                continue
            neven += 1
            ok, r1, r0, ex, wok = check_row(binary, verifier, a, f, wpath)
            nw += wok is True
            if not ok:
                nbad += 1
                print(f"BAD a={a} f={f}: reach(K=f)={r1} reach(K=f+1)={r0} EXACT={ex} witness_ok={wok}")
        print(f"kitamura table: odd rows {nodd} (formula), even rows {neven} (dfsD both directions), "
              f"witnesses verified {nw}, failures {nbad}, time {time.time() - t0:.1f}s")
        print("ALL_OK" if nbad == 0 else "FAILURES")
    elif mode == 'survey':
        nsample, seed, binary, verifier = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        explicit = None
        if seed < 0:  # explicit list mode: NSAMPLE ignored, a values given as "a1,a2,..." in argv[6]
            explicit = [int(x) for x in sys.argv[6].split(',')]
            del sys.argv[6]
        rows = {}
        for path in sys.argv[6:]:
            for row in csv.DictReader(open(path)):
                if row['status'] == 'exact':
                    rows[int(row['a'])] = int(row['f'])
        keys = sorted(rows)
        sample = explicit if explicit is not None else sorted(random.Random(seed).sample(keys, nsample))
        nbad = 0
        t0 = time.time()
        for a in sample:
            f = rows[a]
            t1 = time.time()
            ok, r1, r0, ex, wok = check_row(binary, verifier, a, f, wpath, check_witness=(explicit is not None or f - v2f(a) <= 20000))
            line = f"a={a} f={f} g={f - v2f(a)} ok={int(ok)} witness={wok} time={time.time() - t1:.2f}s"
            if not ok:
                nbad += 1
                line += f" BAD reach(K=f)={r1} reach(K=f+1)={r0} EXACT={ex}"
            if not ok or f - v2f(a) >= 1000:
                print(line, flush=True)
        print(f"survey sample: {len(sample)} rows (seed {seed}) from {len(keys)} exact rows, failures {nbad}, "
              f"time {time.time() - t0:.1f}s")
        print(f"sample a values: {' '.join(map(str, sample))}")
        print("ALL_OK" if nbad == 0 else "FAILURES")
    elif mode == 'full':
        # every exact row with A0 <= a <= A1: dfsD at K=f (witness) and K=f+1; witness checked
        # in-process with verify_w.method_H / method_M (v_2 = f exactly, min = a, increasing).
        A0, A1, binary, verifier = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
        import importlib.util
        spec = importlib.util.spec_from_file_location("vw", verifier)
        vw = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vw)
        rows = {}
        for path in sys.argv[6:]:
            for row in csv.DictReader(open(path)):
                if row['status'] == 'exact' and A0 <= int(row['a']) <= A1:
                    rows[int(row['a'])] = int(row['f'])
        nbad = 0
        t0 = time.time()
        for a in sorted(rows):
            f = rows[a]
            va = v2f(a)
            r1, _ = run_D(binary, a, f, wpath if f > va else None)
            r0, ex = run_D(binary, a, f + 1)
            ok = (r1 == 1 and r0 == 0 and ex == f)
            if ok and f > va:
                A, _ = vw.read_list(wpath)
                ok = (A[0] == a and all(x < y for x, y in zip(A, A[1:]))
                      and vw.method_H(A)[0] == f and vw.method_M(A, f + 64) == f)
                with open(wpath, 'w') as fh:
                    fh.write("")  # no stale witness can be re-read for the next row
            if not ok:
                nbad += 1
                print(f"BAD a={a} f={f} reach(K=f)={r1} reach(K=f+1)={r0} EXACT={ex}", flush=True)
        print(f"full re-certification of {len(rows)} exact rows with {A0} <= a <= {A1}: failures {nbad}, "
              f"time {time.time() - t0:.1f}s")
        print("ALL_OK" if nbad == 0 else "FAILURES")


if __name__ == '__main__':
    main()
