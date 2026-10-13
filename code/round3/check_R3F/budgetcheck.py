"""budgetcheck.py -- independent evaluation of the random-model budgets of R3F B2 / D4 and note Thm 10.16.
  Lambda_p(q) = sum_{d>=1} (p^d - p^{d-1}) q^{U_d},  U_d = min{i : v_p(i!) >= d}
  q = 2/pi (L^1, Thm 10.16), q = 2^{-1/2} (Lambda'_p, B5), q = 1/2 (Lambda2_p, L^2 mass), q = 32/(15 pi) (D4 lower bound).
Summed exactly (mpmath interval arithmetic) for d <= D, plus the rigorous tail bound from U_d >= (p-1)d + 1:
  sum_{d>D} N_d q^{U_d} <= q * r^{D+1}/(1-r),  r = p q^{p-1}  (valid when r < 1).
Also tau'_p(3) = p^{3+c_3} 2^{-p^2/2}, c_3 = v_p((p^2-1)!), and the C thresholds of B5 / Thm 10.16.
usage: python3 -I budgetcheck.py
"""
from mpmath import iv
import mpmath

iv.dps = 30


def vp_fact(n, p):
    s, q = 0, p
    while q <= n:
        s += n // q
        q *= p
    return s


def U_list(p, D):
    out, i = [], 0
    for d in range(1, D + 1):
        while vp_fact(i, p) < d:
            i += 1
        out.append(i)
    return out


def budget(p, q, D=400):
    r = p * q ** (p - 1)
    Us = U_list(p, D)
    s = iv.mpf(0)
    for d, U in enumerate(Us, start=1):
        s += (iv.mpf(p) ** d - iv.mpf(p) ** (d - 1)) * q ** U
    if r.b < 1:
        tail = q * r ** (D + 1) / (1 - r)
        return iv.mpf([s.a, (s + tail).b]), r
    return None, r     # divergent (r > 1) or undecided


def main():
    qs = {'Lambda (2/pi)': iv.mpf(2) / iv.pi, "Lambda' (2^-1/2)": 1 / iv.sqrt(2), 'Lambda2 (1/2)': iv.mpf(1) / 2,
          'D4 (32/(15pi))': iv.mpf(32) / (15 * iv.pi)}
    for name, q in qs.items():
        row = []
        for p in (3, 5, 7, 11, 13, 17, 19, 23):
            val, r = budget(p, q)
            row.append(f'p={p}: ' + (f'[{mpmath.nstr(val.a, 6)}, {mpmath.nstr(val.b, 6)}]' if val is not None
                                     else f'diverges? r={mpmath.nstr(r.a, 5)}>1'))
        print(f'{name:18s} ' + '  '.join(row), flush=True)
    print('# partial sums for the divergent cases (first 60 levels), to show growth:')
    for p, q in ((3, iv.mpf(2) / iv.pi), (3, 1 / iv.sqrt(2)), (5, 1 / iv.sqrt(2)), (5, iv.mpf(32) / (15 * iv.pi))):
        Us = U_list(p, 60)
        s = iv.mpf(0); marks = []
        for d, U in enumerate(Us, start=1):
            s += (iv.mpf(p) ** d - iv.mpf(p) ** (d - 1)) * q ** U
            if d in (10, 20, 40, 60):
                marks.append(f'D={d}: {mpmath.nstr(s.a, 5)}')
        print(f'  p={p} q={mpmath.nstr(q.mid, 6)}: ' + ', '.join(marks))
    print("# B2 bound: Lambda'_p <= 2^-1/2 r/(1-r), r = p 2^{-(p-1)/2}")
    for p in (7, 11, 13):
        r = iv.mpf(p) * iv.mpf(2) ** (-(iv.mpf(p) - 1) / 2)
        print(f'  p={p}: r={mpmath.nstr(r.mid, 6)}  bound={mpmath.nstr((r / (1 - r) / iv.sqrt(2)).b, 6)}')
    print("# tau'_p(3) = p^{3+c3} 2^{-p^2/2} and C thresholds 1/(Lambda'+tau')^2 (B5), 1/(Lambda+tau) (Thm 10.16)")
    for p in (7, 11, 13):
        c3 = vp_fact(p * p - 1, p)
        taup = iv.mpf(p) ** (3 + c3) * iv.mpf(2) ** (-iv.mpf(p * p) / 2)
        tau = iv.mpf(p) ** (3 + c3) * (iv.mpf(2) / iv.pi) ** (p * p)
        Lp, _ = budget(p, 1 / iv.sqrt(2)); L1, _ = budget(p, iv.mpf(2) / iv.pi)
        print(f'  p={p}: c3={c3} tau\'={mpmath.nstr(taup.b, 4)} tau={mpmath.nstr(tau.b, 4)}  '
              f'B5: C < {mpmath.nstr((1 / (Lp + taup) ** 2).a, 5)}   Thm10.16: C < {mpmath.nstr((1 / (L1 + tau)).a, 5)}')


if __name__ == '__main__':
    main()
