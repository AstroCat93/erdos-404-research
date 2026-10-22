#!/usr/bin/env python3
"""check_R3N: consistency checks of track R3N's survey CSVs against the claims of its report
(§4.1 table and value-set claims, §6 survival table, Kitamura cross-checks, profile sum).
Pure parsing and arithmetic; no search.
Usage: python3 -I check_csv.py R3N_DATA_DIR KITAMURA_TABLE
"""
import csv
import os
import sys


def v2f(n):
    return n - bin(n).count('1')


def main():
    d, ktab = sys.argv[1], sys.argv[2]
    files = ['survey_2_4096.csv', 'survey_4098_16384.csv', 'survey_16386_32768_merged.csv']
    rows = {}
    problems = []
    for fn in files:
        for r in csv.DictReader(open(os.path.join(d, fn))):
            a = int(r['a'])
            if a in rows:
                problems.append(f"duplicate a={a} in {fn}")
            rows[a] = r
    evens = set(range(2, 32769, 2))
    print(f"rows: {len(rows)}; all even a in [2,32768] present exactly once: {set(rows) == evens}")
    if set(rows) != evens:
        problems.append("coverage")
    exact = {}
    for a, r in rows.items():
        if int(r['v2(a!)']) != v2f(a):
            problems.append(f"v2(a!) wrong at a={a}")
        if r['status'] == 'exact':
            f, g = int(r['f']), int(r['g'])
            if g != f - v2f(a):
                problems.append(f"g != f - v2 at a={a}")
            if r['certB'] != '1':
                problems.append(f"certB != 1 at a={a}")
            if int(r['witness_v2']) != f:
                problems.append(f"witness_v2 != f at a={a}")
            exact[a] = g
    lower = sorted(a for a, r in rows.items() if r['status'] != 'exact')
    print(f"exact rows {len(exact)}, capped rows {lower} -> {[(a, rows[a]['g']) for a in lower]}")
    # value set and g = 3 iff a = 4 mod 8
    forb = [a for a, g in exact.items() if g in (1, 2, 4, 5)]
    g3 = all((g == 3) == (a % 8 == 4) for a, g in exact.items())
    print(f"rows with g in {{1,2,4,5}}: {len(forb)}; g=3 iff a=4 mod 8 on all exact rows: {g3}")
    # Kitamura table, a <= 256
    kit = {int(r['a']): int(r['value']) for r in csv.DictReader(open(ktab))}
    mism = [(a, int(rows[a]['f']), kit[a]) for a in range(2, 257, 2) if int(rows[a]['f']) != kit[a]]
    print(f"a<=256 even: survey f vs Kitamura table mismatches: {mism}")
    for a, fk in [(1102, 12633), (3456, 8275), (8190, 16396), (34, 18444), (14, 1533), (2, 254)]:
        print(f"  Kitamura row a={a}: f={fk}; survey f={rows[a]['f']} {'OK' if int(rows[a]['f']) == fk else 'MISMATCH'}")
    # shadow family
    for t in (14, 15):
        a = 2 ** t - 2
        print(f"  shadow t={t} a={a}: survey f={rows[a]['f']} g={rows[a]['g']}")
    sh = {int(r['a']): r for r in csv.DictReader(open(os.path.join(d, 'shadow_t15_17.csv')))}
    for a, r in sorted(sh.items()):
        ok = r['status'] == 'exact' and r['certB'] == '1' and int(r['witness_v2']) == int(r['f']) and int(r['g']) == int(r['f']) - v2f(a)
        print(f"  shadow csv a={a} f={r['f']} g={r['g']} consistent={ok}" + (f" (survey row: f={rows[a]['f']})" if a in rows else ""))
    # top g table (with 594 = 89804 and 17662 >= 131072 from the report)
    allg = dict(exact)
    allg[594] = 89804
    top = sorted(allg.items(), key=lambda kv: -kv[1])[:18]
    print("top exact g (with g(594)=89804): " + ", ".join(f"{a}:{g}" for a, g in top))
    top4096 = sorted(((a, g) for a, g in allg.items() if a <= 4096), key=lambda kv: -kv[1])[:10]
    print("top g, a<=4096: " + ", ".join(f"{a}:{g}" for a, g in top4096))
    top16384 = max(((g, a) for a, g in allg.items() if a <= 16384))
    print(f"largest g for a<=16384: a={top16384[1]} g={top16384[0]}")
    # §6 survival table: c(G) over the 16384 even a <= 32768, g(17662) >= 131072
    print("G, c(G), G*c(G)/16384:")
    for k in range(6, 18):
        G = 2 ** k
        c = sum(1 for g in allg.values() if g >= G) + 1  # + a = 17662 (g >= 131072 >= G)
        print(f"  {G} {c} {G * c / 16384:.1f}")
    # survey overlap claim (first 16386..32768 process vs second)
    s1 = {int(r['a']): r for r in csv.DictReader(open(os.path.join(d, 'survey_16386_32768.csv')))}
    s2 = {int(r['a']): r for r in csv.DictReader(open(os.path.join(d, 'survey_24578_32768.csv')))}
    ov = sorted(set(s1) & set(s2))
    same = all(s1[a] == s2[a] for a in ov)
    print(f"overlap of the two 16386..32768 processes: {len(ov)} rows ({ov[0] if ov else '-'}..{ov[-1] if ov else '-'}), identical: {same}; "
          f"first process max a = {max(s1)}")
    # profile: sum of boundary populations
    prof = os.path.join(d, 'profile_594.txt')
    tot, nb, peak = 0, 0, (0, 0)
    for line in open(prof):
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split()
        try:
            M, cnt = int(parts[1]), int(parts[3])   # columns: j, M_j, v2(M_j!), alive paths
        except (ValueError, IndexError):
            continue
        tot += cnt
        nb += 1
        peak = max(peak, (cnt, M))
    print(f"profile_594: {nb} boundaries, sum of populations {tot}, peak {peak[0]} at M={peak[1]}")
    print("problems:", problems if problems else "none")


if __name__ == '__main__':
    main()
