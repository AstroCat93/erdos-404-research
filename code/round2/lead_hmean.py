import numpy as np, math
# exact period mean of H_1 at p=13: 13 * int_0^1 prod_{n=13}^{25} |cos(pi theta n!/13!)| dtheta
# forward weight recursion omega_{n+1}(u) = (1/(n+1)) sum_d omega_n((d+u)/(n+1)) |cos(pi (d+u)/(n+1))|
def run(M, p=13, N0=13, N1=26):
    u = (np.arange(M)+0.5)/M          # midpoints
    om = np.ones(M)
    xs = np.concatenate([u-1, u, u+1])  # periodic extension helper
    for n in range(N0, N1-1):          # build omega_{n+1} for n=13..24
        q = n+1
        new = np.zeros(M)
        for d in range(q):
            t = (d+u)/q
            vals = np.interp(t, (np.arange(M)+0.5)/M, om, period=1.0)
            new += vals*np.abs(np.cos(np.pi*t))
        om = new/q
    # last factor at n=25
    return p*np.mean(om*np.abs(np.cos(np.pi*u)))
for e in (14,16,18,20):
    print(e, repr(run(2**e)))
print('heuristic 13(2/pi)^13 =', 13*(2/math.pi)**13)
