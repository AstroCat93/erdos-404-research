"""Check the claims of paper/note.md section 4 about the vectors: note table vs file, 74 count,
agreement with BLL Table V, SAT vs tree-witness differences, unit multiples, R* vs SAT on listed primes.
Usage: python3 -I vecfacts.py REPO_ROOT"""
import re, sys
B = sys.argv[1]
def load(p):
    d = {}
    for l in open(p):
        l = l.strip()
        if not l or l.startswith('#'): continue
        q, v = map(int, l.split()[:2]); assert q not in d; d[q] = v % 8
    return d
C = load(B + '/vectors/vec8_compact.txt')
S = load(B + '/vectors/vec8_L1508323.txt')
W = load(B + '/vectors/k8_L1508323_witness.txt')
BLL = load(B + '/vectors/bll_k8_tableV.txt')
note = open(B + '/paper/note.md').read()
tab = {}
for m in re.finditer(r'^\| \$(\d)\$ \| ([\d, ]+) \|$', note, re.M):
    v = int(m.group(1))
    for q in m.group(2).split(','):
        q = int(q); assert q not in tab; tab[q] = v
print("note table entries:", len(tab), " file entries:", len(C), " identical:", tab == C)
from collections import Counter
print("value counts in file:", sorted(Counter(C.values()).items()))
# R* vs SAT at listed primes
print("R* listed values equal SAT values at those primes:", all(S[q] == v for q, v in C.items()))
print("primes where SAT != 1 but R* = 1 (reset by greedy):", sum(1 for q in S if S[q] != 1 and q not in C))
print("SAT entries:", len(S), "witness entries:", len(W), "same keys:", set(S) == set(W))
for u in (1, 3, 5, 7):
    diff = sum(1 for q in S if (u * S[q]) % 8 != W[q])
    print(f"  #primes where {u}*SAT != witness: {diff}")
for u in (1, 3, 5, 7):
    diff = sum(1 for q in S if (u * S[q]) % 8 != (C.get(q, 1)))
    print(f"  #primes where {u}*SAT != R*: {diff}")
agree = [q for q in BLL if C.get(q, 1) == BLL[q]]
print("BLL Table V listed:", len(BLL), " R* agrees at", len(agree), "of them; disagrees at", sorted(set(BLL) - set(agree)))
print("R*(2), R*(3) =", C[2], C[3], " BLL(2),BLL(3) =", BLL[2], BLL[3])
print("R*(5) =", C.get(5, 1), "-> stabiliser of R* in (Z/8)^*:", [u for u in (1,3,5,7) if all((u*v)%8 == v for v in list(C.values()) + [1])])
print("W(2), W(5):", W[2], W[5], " stabiliser of SAT:", [u for u in (1,3,5,7) if all((u*v)%8==v for v in S.values())])
