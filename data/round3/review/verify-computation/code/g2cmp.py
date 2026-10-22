# compare capped g_2 table with Kitamura's exact table (data file read as data) and compute N(4096,G)
import csv, sys
g={}
for l in open("out/g2_range_cap1024.txt"):
    a,v=map(int,l.split()); g[a]=v
cap=1024
def vf(a): return a-bin(a).count("1")
mis=0; n=0
for row in csv.DictReader(open("../T4-computations/kitamura/p2_exact_table_1_256.csv")):
    a=int(row['a']); 
    if row['status']!='exact': print("non-exact row",row); continue
    f=int(row['value']); gk=f-vf(a); n+=1
    if min(gk,cap)!=g[a]: mis+=1; print("MISMATCH",a,gk,g[a])
print(f"Kitamura rows compared: {n}, mismatches (after f->g and cap {cap}): {mis}")
for G in [8,16,32,64,128,256,512,1024]:
    print(f"N(4096,{G}) = {sum(1 for a in g if a<=4096 and g[a]>=G)}")
print("a<=4096 with g>=1024:", [a for a in sorted(g) if g[a]>=1024])
