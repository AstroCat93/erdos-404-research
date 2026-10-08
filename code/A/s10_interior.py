# s10_interior.py -- look for residue classes r mod p^k0 all of whose lifts stay in G_k up to kmax
# (candidates for interior points of the closed set Gcal_p = {x in Z_p : A_x = Z_p}).
# Input: output of ./dens2 G p kmax BIG (prints the sets).  Usage: python3 s10_interior.py file p
import sys, re
from collections import Counter
fn, p = sys.argv[1], int(sys.argv[2])
sets = {}; k = None
for line in open(fn):
    m = re.match(r"G p=\d+ k=(\d+)", line)
    if m: k = int(m.group(1)); continue
    if "set = {" in line:
        body = line.split("{")[1].split("}")[0]
        sets[k] = set(int(x) for x in body.split(",") if x)
kmax = max(sets)
print(f"p={p}: levels 1..{kmax}, |G_kmax|={len(sets[kmax])}")
for k0 in range(1, kmax):
    cnt = Counter(x % p ** k0 for x in sets[kmax])
    n_l = p ** (kmax - k0)
    full = sorted(r for r in sets[k0] if cnt[r] == n_l)
    best = max(sets[k0], key=lambda r: cnt[r])
    print(f"  k0={k0}: classes mod p^{k0} with ALL {n_l} lifts in G_{kmax}: count {len(full)} {full[:12]}"
          f"{'...' if len(full) > 12 else ''}; best fraction {cnt[best]/n_l:.4f} (r={best})")
