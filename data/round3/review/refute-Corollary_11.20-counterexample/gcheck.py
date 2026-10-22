# Independent brute-force check that classes z mod 2^G (z = computed zeros) satisfy g_2 >= G,
# directly from the definition g = sup_B v(1+sum_{b in B} pi_b(x)), B subset [1,2G) (terms b>=2G vanish mod 2^G).
import sys, random
sys.setrecursionlimit(10000)
exec(open(sys.argv[1]).read().split("# runs")[0].replace("sys.argv[1]","'2'").replace("int(sys.argv[2])","3").replace("int(sys.argv[3])","6").replace("int(sys.argv[4])","4"))
def g_at_least(c, G):
    M = 2**G; reach = {1 % M}
    pi = 1
    for b in range(1, 2*G):
        pi = pi*(c+b) % M
        reach |= {(r+pi) % M for r in reach}
        if 0 in reach: return True
    return 0 in reach
J = [0,1,2,6] + [16,18,19,22,25,30,33]
z, lz = newton(alpha, J)
print("zero with slope", lz)
for G in (8,12,14,16,18):
    print(G, g_at_least(z % 2**G, G), "random class:", sum(g_at_least(random.randrange(2**G), G) for _ in range(40)), "/40")
