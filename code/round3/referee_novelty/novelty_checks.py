#!/usr/bin/env python3
"""Round-3 novelty referee: two small arithmetic checks behind the report.

1. Kitamura's "~11.5/G": compare G * (fraction surviving to depth G) for
   (a) the class census (published delta_G(2) values, note.md S4.7/S5, all of
       Z_2 and doubled for even classes) and
   (b) Kitamura's own exact table of f(a,2), a <= 256 (even a only),
   to see which data set the figure 11.5 could come from.
2. Mod-p step for "every residue mod p^k is a sum of distinct factorials":
   do the subset sums of {0!, 1!, ..., (p-1)!} cover Z/p?  (Combined with the
   round-1 tail frontiers of note.md S4.5 this gives all residues mod
   p^{v_p(R!)}.)

Usage: python3 -I novelty_checks.py PATH/TO/p2_exact_table_1_256.csv
No network, no side effects.
"""
import csv
import math
import sys


def v2_fact(a):
    return a - bin(a).count("1")


def kitamura_table(path):
    rows = list(csv.DictReader(open(path)))
    gs = [(int(r["a"]), int(r["value"]) - v2_fact(int(r["a"])))
          for r in rows if int(r["a"]) % 2 == 0]
    assert len(gs) == 128
    print("(b) Kitamura's table, even a <= 256 (128 values): G * #{g >= G} / 128")
    for G in [8, 16, 24, 25, 32, 64, 128, 256, 512]:
        c = sum(1 for _, g in gs if g >= G)
        print("   G=%4d  count=%3d  G*frac_even=%6.2f" % (G, c, G * c / 128))


def census():
    # published delta_G(2) (fraction of Z_2), note.md S4.7 (exact) and S5 (Monte Carlo)
    pub = {8: .2422, 12: .1958, 16: .1517, 20: .1417, 24: .1292,
           25: 1 - 0.8734, 28: .1164, 29: .1134, 32: .1016,
           64: .0644, 128: .0379, 254: .0208}
    print("(a) class census / Haar values: G*delta_G (all Z_2) and G*2*delta_G (even classes)")
    for G, d in sorted(pub.items()):
        tag = "exact" if G <= 32 else "Monte Carlo"
        print("   G=%4d  delta=%.4f  G*delta=%5.2f  G*2delta=%5.2f  (%s)"
              % (G, d, G * d, 2 * G * d, tag))
    print("   11.5/G at G=25 would be %.3f (even) vs census 2*delta_25 = %.3f"
          % (11.5 / 25, 2 * (1 - 0.8734)))


def modp_cover():
    print("Mod-p covering by subset sums of {0!,...,(p-1)!}:")
    for p in [3, 5, 7, 11, 13, 17, 19, 23]:
        sums = {0}
        for u in range(p):
            f = math.factorial(u) % p
            sums |= {(s + f) % p for s in sums}
        print("   p=%2d  residues reached %d/%d  %s"
              % (p, len(sums), p, "FULL" if len(sums) == p else "NOT FULL"))


if __name__ == "__main__":
    census()
    kitamura_table(sys.argv[1])
    modp_cover()
