"""Compare Arevalo's unsettled vectors at L=1508323 with the 432 unresolved leaves (capped tree), up to units of Z/8."""
import sys
ar, ours = sys.argv[1], sys.argv[2]
A = []
for line in open(ar):
    if line.startswith('UNSETTLED:'):
        kv = [t.split('=') for t in line.split()[1:]]
        qs = [int(a) for a, b in kv]; vs = tuple(int(b) for a, b in kv)
        A.append(vs)
O = [tuple(int(x) for x in l.split()) for l in open(ours) if l.strip()]
print("arevalo vectors:", len(A), "distinct:", len(set(A)), "lengths:", set(map(len, A)), "primes:", qs[:3], '...', qs[-3:])
print("our unresolved:", len(O), "distinct:", len(set(O)), "lengths:", set(map(len, O)))
U = (1, 3, 5, 7)
canon = lambda v: min(tuple((u * x) % 8 for x in v) for u in U)
CA = {canon(v) for v in A}; CO = {canon(v) for v in O}
print("orbits: arevalo", len(CA), "ours", len(CO), "equal:", CA == CO)
# each of our leaves: orbit sizes
from collections import Counter
c = Counter(canon(v) for v in O)
print("our leaves per orbit:", Counter(c.values()))
print("all 4 unit multiples of each arevalo vector present in ours:", all(tuple((u*x)%8 for x in v) in set(O) for v in A for u in U))
print("R(2) values ours:", Counter(v[0] for v in O), "arevalo:", Counter(v[0] for v in A))
