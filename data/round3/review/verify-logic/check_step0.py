# Thm 11.15 Step 0(b): for each k, every residue mod k is f(u)=u+v_p(u!) for some u with p|u (search up to p^E)
def vfact(u, p):
    s = 0; q = p
    while q <= u: s += u // q; q *= p
    return s
for p, E in ((2, 22), (3, 14), (5, 9), (7, 8)):
    bad = []
    for k in range(1, 61):
        hit = set(); u = 0
        while u < p ** E and len(hit) < k:
            hit.add((u + vfact(u, p)) % k); u += p
        if len(hit) < k: bad.append(k)
    print(p, "k<=60 with some residue not hit (u<p^%d):" % E, bad)
