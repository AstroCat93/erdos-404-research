"""t0: validate the independent library.
(1) constants q_s, P_0 at p=3,5,7,11,13 (compared with the values printed in M4A.md section 4);
(2) monotonicity q_s <= q_{s+1} <= p q_s (needed for Delta_s >= 0 in Prop E');
(3) rho_1, gamma, kappa (M4A.md section 5);
(4) the exact CRT DP against brute-force enumeration of all signed paths (small t), both for
    the Lemma Q process (dt_0=1, value+derivative) and for Coll (all digits signed).
usage: python3 t0_validate.py SEED NTEST
"""
import sys, random, itertools
from fractions import Fraction
import vf_lib as L

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
NT = int(sys.argv[2]) if len(sys.argv) > 2 else 30
random.seed(seed)

print("== (1) constants")
for p in (3, 5, 7, 11, 13):
    q = L.q_consts(p, 8)
    print(f"p={p}: " + "  ".join(f"q_{s}={q[s]} ({float(q[s]):.6f})" for s in range(1, 6)))
    mono = all(q[s] <= q[s + 1] <= p * q[s] for s in range(1, 8))
    print(f"   monotone q_s<=q_(s+1)<=p q_s for s<8: {mono}")
q7 = L.q_consts(7, 8)
print("p=7 report check: q1==8309/8192", q7[1] == Fraction(8309, 8192), " q2==4557/4096", q7[2] == Fraction(4557, 4096),
      " q3==33271/8192", q7[3] == Fraction(33271, 8192),
      " q_s==7^s*3/256 (s=4..8)", all(q7[s] == Fraction(7 ** s * 3, 256) for s in range(4, 9)))
print("p=7 P0 table:")
for g in range(1, 8):
    print(f"   g={g}: " + " ".join(str(L.P0(7, g, s)) for s in range(1, 6)))
print("   report: P0(2,s)=1/4; P0(1,.)=P0(3,.)=0; P0(4,1)=9/64; P0(5,.)=(33/256,1/64,0); P0(6,.)=(37/256,7/1024,0); P0(7,.)=(591/4096,15/1024,1/4096,0)")
ok = (all(L.P0(7, 2, s) == Fraction(1, 4) for s in range(1, 9)) and all(L.P0(7, 1, s) == 0 for s in range(1, 5))
      and all(L.P0(7, 3, s) == 0 for s in range(1, 5)) and L.P0(7, 4, 1) == Fraction(9, 64)
      and [L.P0(7, 5, s) for s in (1, 2, 3)] == [Fraction(33, 256), Fraction(1, 64), 0]
      and [L.P0(7, 6, s) for s in (1, 2, 3)] == [Fraction(37, 256), Fraction(7, 1024), 0]
      and [L.P0(7, 7, s) for s in (1, 2, 3, 4)] == [Fraction(591, 4096), Fraction(15, 1024), Fraction(1, 4096), 0])
print("   P0 table agrees with the report:", ok)

print("== (3) Prop E' constants")
for p in (3, 5, 7, 11, 13):
    C = L.eprime_consts(p)
    print(f"p={p}: rho1={float(C['rho1']):.5f} gamma={float(C['gamma']):.5f} kappa={float(C['kappa']):.5f}")

print("== (4) DP vs brute force")
bad = 0
ntest = 0
for trial in range(NT):
    p = random.choice((3, 5, 7))
    E = 30
    kind = random.choice(("rand", "neg", "int"))
    if kind == "rand":
        u = random.randrange(p ** E)
    elif kind == "neg":
        g = random.randint(1, 6)
        s = random.randint(1, 5)
        u = (-g + p ** s * random.randrange(1, p ** (E - s))) % p ** E
        if (u + g) % p ** (s + 1) == 0:
            u = (u + p ** s) % p ** E
    else:
        u = random.randint(0, 40)
    t = random.randint(2, 9)
    ka = random.randint(1, 4 if p > 3 else 6)
    kb = random.randint(0, 2 if p > 3 else 4)
    Pv, Dv = L.pi_and_deriv(u, t, p ** 40)
    # brute force over dt_1..dt_{t-1}
    cnt = {}
    for digs in itertools.product((-1, 0, 1), repeat=t - 1):
        w = 1
        for d in digs:
            w *= 2 if d == 0 else 1
        T = Pv[0] + sum(d * Pv[c + 1] for c, d in enumerate(digs))
        Tp = Dv[0] + sum(d * Dv[c + 1] for c, d in enumerate(digs))
        key = (T % p ** ka, Tp % p ** kb)
        cnt[key] = cnt.get(key, 0) + w
    dp = L.SignedDP(p, ka, kb, first_fixed=True)
    for c in range(t):
        dp.step(Pv[c], Dv[c])
    for k in range(0, ka + 1):
        for f in range(0, kb + 1):
            bf = sum(w for (a, b), w in cnt.items() if a % p ** k == 0 and b % p ** f == 0)
            x, tot = dp.count_zero(k, f)
            ntest += 1
            if x != bf or tot != 4 ** (t - 1):
                bad += 1
    # Coll check (all digits signed) on a window
    n = random.randint(0, 20)
    H = random.randint(2, 8)
    K = random.randint(1, 4 if p > 3 else 6)
    x0 = random.randrange(p ** E)
    Y, _ = L.window_elems(x0, n, H, p ** K)
    cnt2 = {}
    for digs in itertools.product((-1, 0, 1), repeat=H):
        w = 1
        for d in digs:
            w *= 2 if d == 0 else 1
        key = sum(d * Y[c] for c, d in enumerate(digs)) % p ** K
        cnt2[key] = cnt2.get(key, 0) + w
    dp2 = L.coll_counts(p, x0, n, H, K)
    for j in range(0, K + 1):
        bf = sum(w for a, w in cnt2.items() if a % p ** j == 0)
        x, tot = dp2.count_zero(j, 0)
        ntest += 1
        if x != bf or tot != 4 ** H:
            bad += 1
print(f"DP vs brute force: {ntest} comparisons, {bad} mismatches")
