"""Analyse the arrays written by chebo.c (empirical check of paper/note.md Theorem 5.4 / Remark 5.5).
Usage: python -I chebo_analyse.py k m prefix seed
  prefix.least : counts of R_{p,g} (g = least primitive root) on the first m primes
  prefix.real  : for each vector v, number of p for which SOME primitive root realises v exactly
Prediction (note Theorem 5.4 + Remark 5.5 + Chebotarev for M_N/Q):
  k = 8: R(2) is never odd; every v with R(2) even is realised; P(R_p in orbit O) = |O| / (4*8^(m-1)).
  k = 9: every v is realised; P(R_p in orbit O) = |O| / 9^m.
"""
import sys, math
import numpy as np

k, m, prefix, seed = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
units = [u for u in range(1, k) if math.gcd(u, k) == 1]
least = np.fromfile(prefix + ".least", dtype=np.uint32).astype(np.int64)
real = np.fromfile(prefix + ".real", dtype=np.uint32).astype(np.int64)
assert least.size == k ** m and real.size == k ** m
n = int(least.sum())
print(f"k={k} m={m} primes p=1 mod {k} used: {n}")

def digits(codes, mm):
    return [(codes // k ** i) % k for i in range(mm)]

def mulcode(codes, u, mm):
    d = digits(codes, mm)
    return sum(((u * d[i]) % k) * k ** i for i in range(mm))

def orbit_tools(mm):
    codes = np.arange(k ** mm, dtype=np.int64)
    imgs = [mulcode(codes, u, mm) for u in units]
    stab = sum((img == codes).astype(np.int64) for img in imgs)
    orbsize = len(units) // stab
    rep = np.minimum.reduce(imgs)
    return codes, imgs, stab, orbsize, rep

def allowed_mask(codes, mm):
    return (digits(codes, mm)[0] % 2 == 0) if k == 8 else np.ones(codes.size, bool)

# 1. R(2) parity
d0 = digits(np.arange(k ** m, dtype=np.int64), m)[0]
if k == 8:
    print(f"[parity] p with R(2) odd (least g): {int(least[d0 % 2 == 1].sum())};  "
          f"vectors with R(2) odd realised by some primitive root: {int((real[d0 % 2 == 1] > 0).sum())}  (predicted 0, 0)")

# 2. note Remark 5.5 (orbit formula) vs the literal per-primitive-root count
codes, imgs, stab, orbsize, rep = orbit_tools(m)
orbit_sum = sum(least[img] for img in imgs) // stab
print(f"[Remark 5.5] literal 'realised by some g' count == sum of least-g counts over the unit orbit: "
      f"{bool(np.array_equal(orbit_sum, real))}")

# 3. exhaustive coverage at each level mm <= m, and orbit frequencies vs Chebotarev
rng = np.random.default_rng(seed)
for mm in range(1, m + 1):
    lm = least.reshape((k,) * m, order='F').sum(axis=tuple(range(mm, m))).reshape(-1, order='F')
    c, im, st, osz, rp = orbit_tools(mm)
    realm = sum(lm[x] for x in im) // st
    allow = allowed_mask(c, mm)
    cells = int(allow.sum())
    expected = n * osz / cells
    miss = int(((realm == 0) & allow).sum())
    outside = int(((realm > 0) & ~allow).sum())
    # orbit frequencies
    reps = np.unique(rp[allow])
    obs = np.bincount(rp, weights=lm, minlength=k ** mm)[reps]
    exp_ = n * osz[reps] / cells
    chi2 = float(((obs - exp_) ** 2 / exp_).sum()); dof = reps.size - 1
    z = (obs - exp_) / np.sqrt(exp_)
    # multinomial reference: same n, same probabilities
    nsim = int(max(5, min(200, 5e7 // reps.size)))
    sim = rng.multinomial(n, exp_ / exp_.sum(), size=nsim)
    chi2_sim = ((sim - exp_) ** 2 / exp_).sum(axis=1)
    print(f"[m={mm}] cells={cells} orbits={reps.size}: allowed vectors never realised={miss} (Poisson expectation {float(np.exp(-expected[allow]).sum()):.1f}); "
          f"realised vectors outside the predicted set={outside}; min realisations={int(realm[allow].min())} "
          f"(expected for that orbit size {expected[allow][np.argmin(realm[allow])]:.1f}); "
          f"orbit chi2={chi2:.1f} dof={dof} (multinomial reference, {nsim} sims: {chi2_sim.mean():.1f}+-{chi2_sim.std():.1f}); "
          f"max|z|={np.abs(z).max():.2f}; obs/exp in [{(obs/exp_).min():.3f},{(obs/exp_).max():.3f}]")

# 4. orbit-invariant marginals with binomial z-scores
dg = digits(np.arange(k ** m, dtype=np.int64), m)
def frac(mask, p0, label):
    c = int(least[mask].sum()); z = (c - n * p0) / math.sqrt(n * p0 * (1 - p0))
    print(f"  {label}: {c}/{n} = {c/n:.5f}  predicted {p0:.5f}  z={z:+.2f}")
print("[marginals]")
if k == 8:
    frac(dg[0] == 0, 1/4, "R(2)=0 (2 an 8th-power residue)")
    frac(dg[0] == 4, 1/4, "R(2)=4")
    frac((dg[0] == 2) | (dg[0] == 6), 1/2, "R(2) in {2,6} (2 not a quartic residue)")
    for i, q in enumerate([2, 3, 5, 7, 11, 13, 17, 19][:m]):
        if i == 0: continue
        frac(dg[i] == 0, 1/8, f"R({q})=0")
        frac(dg[i] % 2 == 1, 1/2, f"R({q}) odd")
    # joint: R(2)/2 mod 2 against R(3) mod 2 (a would-be extra Kummer relation 2^a 3^b)
    for a, b in [(0, 1), (1, 1)]:
        frac(((dg[0] // 2) * a + dg[1] * b) % 2 == 0, 1/2, f"(R(2)/2)*{a}+R(3)*{b} even")
else:
    frac(dg[1] == 0, 1/9, "R(3)=0 (3 a 9th-power residue)")
    frac(dg[1] % 3 == 0, 1/3, "R(3)=0 mod 3 (3 a cubic residue)")
    frac(dg[0] == 0, 1/9, "R(2)=0")
    for i, q in enumerate([2, 3, 5, 7, 11, 13, 17][:m]):
        frac(dg[i] % 3 == 0, 1/3, f"R({q})=0 mod 3")
    frac((dg[0] + dg[1]) % 9 == 0, 1/9, "R(2)+R(3)=0 (6 a 9th power residue)")
    frac((3 * dg[1]) % 9 == 0, 1/3, "3R(3)=0 (27 a 9th power residue)")

# 5. random assignments at the full level m, using the literal 'realised' array
allow = allowed_mask(codes, m); cells = int(allow.sum())
for label, mask in ([("R(2) even", allow), ("R(2) odd", ~allow)] if k == 8 else [("any", allow)]):
    pool = np.nonzero(mask)[0]
    pick = rng.choice(pool, size=2000, replace=False)
    hits = real[pick]
    lam = n * orbsize[pick] / cells
    if label == "R(2) odd":
        print(f"[random m={m}] 2000 random R with {label}: max realisations={int(hits.max())} (predicted 0)")
    else:
        zero_pred = float(np.exp(-lam).sum())
        print(f"[random m={m}] 2000 random R with {label}: total realisations={int(hits.sum())} "
              f"expected={lam.sum():.0f}; never realised={int((hits == 0).sum())} (Poisson expectation {zero_pred:.2f}); "
              f"mean hits/expected={float((hits/lam).mean()):.4f}")
