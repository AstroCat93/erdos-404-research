#!/usr/bin/env python3
"""check_R3N: validation of verify_w.py.
(1) brute force: 300 random sets A (min a <= 60, max <= 400) -- method H and method M against
    v_2 of sum(math.factorial(n)) computed directly (Python ints, by counting trailing zeros);
(2) negative tests on the shipped 594 witness: wrong K (90393, 90395), wrong a, a duplicated
    line, a dropped line -- each must be rejected.
Usage: python3 -I test_verifier.py VERIFY_W_PATH WITNESS_594_GZ SCRATCHDIR"""
import gzip, importlib.util, math, random, subprocess, sys
vw_path, wit, tmp = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("vw", vw_path); vw = importlib.util.module_from_spec(spec); spec.loader.exec_module(vw)
rng = random.Random(404)
bad = 0
for it in range(300):
    a = rng.randint(1, 60); top = rng.randint(a, 400)
    A = sorted({a} | {n for n in range(a + 1, top + 1) if rng.random() < 0.4})
    S = sum(math.factorial(n) for n in A)
    v = 0
    while S % 2 == 0:
        S //= 2; v += 1
    vH, _ = vw.method_H(A); vM = vw.method_M(A, v + 64)
    if vH != v or vM != v:
        bad += 1; print("MISMATCH", A[:5], v, vH, vM)
print(f"brute force: 300 random sets, mismatches {bad}")
lines = [l for l in gzip.open(wit, 'rt').read().splitlines() if l and not l.startswith('#')]
def run(content, a, K):
    p = f"{tmp}/neg.txt"; open(p, 'w').write("\n".join(content) + "\n")
    return subprocess.run([sys.executable, '-I', vw_path, p, str(a), str(K)], capture_output=True, text=True).returncode
cases = [("K=90393", lines, 594, 90393), ("K=90395", lines, 594, 90395), ("a=592", lines, 592, 90394),
         ("duplicated line", lines[:100] + [lines[99]] + lines[100:], 594, 90394),
         ("dropped line", lines[:100] + lines[101:], 594, 90394), ("control (unchanged)", lines, 594, 90394)]
for name, c, a, K in cases:
    rc = run(c, a, K)
    exp = 0 if name.startswith("control") else 1
    print(f"negative test {name}: exit {rc} ({'as expected' if rc == exp else 'UNEXPECTED'})")
    bad += rc != exp
print("ALL_OK" if bad == 0 else "FAILURES")
