#!/usr/bin/env python3
"""Round-4 novelty referee: arithmetic behind finding N1 (Kitamura's odd-prime precursor).

Usage: python3 -I kitamura_check.py PATH_TO_CLONE_OF_KitaKen1/erdos-404-odd-prime-landscape

Reads (never executes) the clone's README.md and scripts/*.py, prints the lines that
state the branching heuristic and the ignition-layer table, and compares:
  * Kitamura's per-block margin  p*log_p(2) - p/(p-1)   ("extra digits per block")
  * note.md H1's quenched mean log-offspring per block  p*log(2) - p/(p-1)*log(p),
    divided by log(p)  (they should coincide);
  * Kitamura's "ignited candidates" fractions with the note's numerical mu(K_p)
    (note.md section 5 / section 4.7 values, typed in below).
"""
import math
import os
import re
import sys


def main():
    root = sys.argv[1]
    readme = open(os.path.join(root, "README.md"), encoding="utf-8").read().splitlines()
    for name in ("p_general_dp.py", "ignition_scan.py"):
        txt = open(os.path.join(root, "scripts", name), encoding="utf-8").read().splitlines()
        for i, ln in enumerate(txt, 1):
            if re.search(r"branching|supercritical|margin|sharpened Tao|B\(p\)", ln):
                print("scripts/%s:%d: %s" % (name, i, ln.rstrip()))
    rows = {}
    for i, ln in enumerate(readme, 1):
        m = re.match(r"\|\s*(\d+)\s*\|\s*`1\.\.(\d+)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", ln)
        if m:
            p, n, blk, fin, ign, mx = map(int, m.groups())
            rows[p] = (n, ign)
            print("README.md:%d: %s" % (i, ln.rstrip()))
    print()
    print(" p   Kitamura margin   H1/log p    ignited/scanned    note mu(K_p) numerics")
    note_mu = {3: 0.36, 5: 0.5216, 7: 0.6239, 11: 0.6998, 13: 0.7545}
    for p in (3, 5, 7, 11, 13):
        kit = p * math.log(2) / math.log(p) - p / (p - 1)
        h1 = (p * math.log(2) - p / (p - 1) * math.log(p)) / math.log(p)
        n, ign = rows.get(p, (0, 0))
        frac = ign / n if n else float("nan")
        print("%2d   %+.4f           %+.4f     %4d/%-4d = %.4f   %.4f" % (p, kit, h1, ign, n, frac, note_mu[p]))


if __name__ == "__main__":
    main()
