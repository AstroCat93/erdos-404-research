"""Round-3 logic referee: cross-check of Lemma S0.1 against the note's walk W_n = n - V_n.

For random 2-adic y (300 random bits; the event that a carry or a valuation reaches the
top bits has probability < 2^-250 and is detected), compute
  W_k(y) = k - sum_{i<=k} v_2(y+i)          (note Remark 10.8.2, Theorem 10.1)
  D(y,k) = s_2(k) - c(y,k)                  (S0 report, Sec. 5; carries counted directly)
check W_k = D(y,k) for all k <= nmax, and estimate P(E_n) = P(W_k >= 0 for all k <= n).
Usage: python3 -I s0_walk_mc.py SEED SAMPLES NMAX
"""
import random
import sys


def v2(z):
    return (z & -z).bit_length() - 1


def carries(y, k, bits):
    """Number of carries in the binary addition y + k, counted bit by bit."""
    c = 0
    carry = 0
    for i in range(bits):
        a = (y >> i) & 1
        b = (k >> i) & 1
        s = a + b + carry
        carry = 1 if s >= 2 else 0
        c += carry
        if carry == 0 and (k >> (i + 1)) == 0:
            break
    else:
        raise RuntimeError("carry reached the top of the window")
    return c


def main():
    seed, samples, nmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    bits = 300
    checkpoints = [2 ** e for e in range(0, nmax.bit_length()) if 2 ** e <= nmax]
    surv = {n: 0 for n in checkpoints}
    mismatches = 0
    for _ in range(samples):
        y = rng.getrandbits(bits)
        W = 0
        alive = True
        for k in range(1, nmax + 1):
            W += 1 - v2(y + k)
            D = bin(k).count("1") - carries(y, k, bits)
            if D != W:
                mismatches += 1
            if W < 0:
                alive = False
            if k in surv and alive:
                surv[k] += 1
    print(f"# seed={seed} samples={samples} nmax={nmax}")
    print(f"# W_k == D(y,k) mismatches: {mismatches}")
    for n in checkpoints:
        m = n.bit_length() - 1
        exact = (2 * m + 3) / 2 ** (m + 2)
        est = surv[n] / samples
        se = (est * (1 - est) / samples) ** 0.5
        print(f"n={n} m={m} MC P(E_n)={est:.5f} +- {se:.5f}  exact (2m+3)/2^(m+2)={exact:.5f}  "
              f"bounds [{(m + 2) / 2 ** (m + 2):.5f}, {(m + 2) / 2 ** (m + 1):.5f}]")


if __name__ == "__main__":
    main()
