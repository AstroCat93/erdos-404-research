#!/usr/bin/env python3
"""Round-3 computational referee: re-check rows of the R3N survey CSVs in both directions.

For each selected row (a, f):
  1. rsolve a f W     -> must report reachable=1; the witness W is then verified exactly by
                         verify_witness_bsplit.v2_sum_factorials (binary splitting, CPython ints):
                         min W = a, strictly increasing, v_2(sum) == f.
  2. rsolve a f+1     -> must report reachable=0 and best (max valuation over all P) == f.
  3. (rows with small excess) an independent breadth-first oracle written here in pure Python
     (states = partial sums mod 2^K, deduplicated) must give reachable(f)=1, reachable(f+1)=0.

Usage: python3 -I check_survey.py RSOLVE_BIN SCRATCH SEED NSAMPLE ORACLE_GMAX EXTRA_A[,..] CSV...
"""
import sys, os, csv, random, subprocess, time, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_witness_bsplit import v2_sum_factorials, read_witness  # noqa: E402


def V(n):
    return n - bin(n).count("1")


def run_rsolve(binp, a, K, wfile=None):
    cmd = ["nice", "-n", "10", binp, str(a), str(K)] + ([wfile] if wfile else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    line = [l for l in out.splitlines() if l.startswith("RESULT")][0]
    kv = dict(t.split("=", 1) for t in line.split()[1:])
    return kv


def oracle_reachable(a, K):
    """Pure-Python BFS: is there P subset [a, N_K), a in P, with 2^K | sum P n! ?"""
    NK = a
    while V(NK) < K:
        NK += 1
    mod = 1 << K
    fact = math.factorial(a) % mod
    m0 = (1 << min(V(a + 1), K)) - 1
    states = {fact} if fact & m0 == 0 else set()   # prefix sums at stage a+1 (a included)
    if not states:
        return False
    N = a + 1
    while N < NK:
        fact = fact * N % mod                # fact = N! mod 2^K
        need = min(V(N + 1), K)
        mask = (1 << need) - 1
        new = set()
        for s in states:
            if s & mask == 0:
                new.add(s)
            t = (s + fact) % mod
            if t & mask == 0:
                new.add(t)
        states = new
        if not states:
            return False
        N += 1
    return 0 in states


def main():
    binp, scratch, seed, nsample, gmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    extra = [int(x) for x in sys.argv[6].split(",") if x]
    files = sys.argv[7:]
    rows = {}
    for fn in files:
        with open(fn) as fh:
            for r in csv.DictReader(fh):
                if r["status"] != "exact":
                    continue
                a, f = int(r["a"]), int(r["f"])
                if int(r["v2(a!)"]) != V(a):
                    print("CSV v2(a!) mismatch at a=%d" % a)
                if int(r["g"]) != f - V(a):
                    print("CSV g mismatch at a=%d" % a)
                if a in rows and rows[a] != f:
                    print("CSV CONFLICT a=%d: %d vs %d" % (a, rows[a], f))
                rows[a] = f
    print("exact rows (distinct a):", len(rows), " min a", min(rows), " max a", max(rows))
    rng = random.Random(seed)
    pool = sorted(a for a in rows if a not in extra)
    sample = sorted(rng.sample(pool, nsample))
    todo = sample + extra
    print("sample (seed %d, n=%d):" % (seed, nsample), " ".join(map(str, sample)))
    nfail = 0
    t_all = time.time()
    noracle = 0
    for a in todo:
        f = rows[a]
        t0 = time.time()
        w = os.path.join(scratch, "w_%d.txt" % a)
        r1 = run_rsolve(binp, a, f, w)
        ok1 = r1["reachable"] == "1"
        vw = None
        if ok1:
            _, A = read_witness(w)
            okw = A[0] == a and all(A[i] < A[i + 1] for i in range(len(A) - 1))
            vw = v2_sum_factorials(A)
            ok1 = ok1 and okw and vw == f
            os.remove(w)
        r2 = run_rsolve(binp, a, f + 1)
        ok2 = r2["reachable"] == "0" and int(r2["best"]) == f
        orc = ""
        if f - V(a) <= gmax:
            o1, o2 = oracle_reachable(a, f), oracle_reachable(a, f + 1)
            orc = " oracle=(%d,%d)" % (o1, o2)
            ok2 = ok2 and o1 and not o2
            noracle += 1
        ok = ok1 and ok2
        nfail += not ok
        print("a=%d f=%d g=%d  K=f: reachable=%s witness_v2=%s |  K=f+1: reachable=%s best=%s nodes=%s%s  %s  %.1fs"
              % (a, f, f - V(a), r1["reachable"], vw, r2["reachable"], r2["best"], r2["nodes"], orc,
                 "OK" if ok else "FAIL", time.time() - t0), flush=True)
    print("SUMMARY rows=%d (random %d + extra %d) failures=%d oracle_rows=%d total %.1fs"
          % (len(todo), len(sample), len(extra), nfail, noracle, time.time() - t_all))


if __name__ == "__main__":
    main()
