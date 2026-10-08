/* tau.c -- tau(k,p) = max{ v_p(Q_S) : k-1 in S subset {0..k-1} },  Q_S = sum_{u in S} (-1)^u/u!
 * computed exactly mod p^L for L = 1..Lmax by the bitmap recursion over u.
 * tau(k,p) >= L  iff  -(-1)^{k-1}/(k-1)!  lies in Sigma({(-1)^u/u! : u <= k-2}) mod p^L.
 * Output: for each k in 1..p, tau(k,p) (">=Lmax" if still hit at Lmax).  k=2 is the exact-zero class.
 * usage: tau p Lmax
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 invmod(u64 a, u64 m) {
    __int128 t = 0, nt = 1, r = m, nr = a % m;
    while (nr) { __int128 q = r / nr, tmp; tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
    if (t < 0) t += m; return (u64)t;
}
static inline int getbit(const u64 *S, u64 i) { return (S[i >> 6] >> (i & 63)) & 1; }
static inline u64 read64(const u64 *S, u64 q) { u64 w = q >> 6, o = q & 63; if (!o) return S[w]; return (S[w] >> o) | (S[w + 1] << (64 - o)); }
static void step(const u64 *S, u64 *T, u64 M, u64 x, u64 nw) {
    for (u64 w = 0; w < nw; w++) {
        u64 i0 = w * 64, val = 0;
        if (i0 >= x && i0 + 64 <= M) val = read64(S, i0 - x);
        else for (int b = 0; b < 64; b++) { u64 i = i0 + b; if (i >= M) break; u64 src = (i >= x) ? i - x : i + M - x; if (getbit(S, src)) val |= (u64)1 << b; }
        T[w] = S[w] | val;
    }
    u64 rem = M & 63; if (rem) T[nw - 1] &= (((u64)1 << rem) - 1);
}
int main(int argc, char **argv) {
    u64 p = strtoull(argv[1], 0, 10); int Lmax = atoi(argv[2]);
    int *tau = calloc(p + 2, sizeof(int));
    for (u64 k = 1; k <= p; k++) tau[k] = 0;
    for (int L = 1; L <= Lmax; L++) {
        u64 M = 1; for (int i = 0; i < L; i++) M *= p;
        u64 nw = (M + 63) / 64 + 1;
        u64 *S = calloc(nw, 8), *T = calloc(nw, 8);
        S[0] = 1;
        u64 fact = 1;
        for (u64 k = 1; k <= p; k++) {
            /* S currently = Sigma({e_u : u <= k-2}); element e_{k-1} */
            u64 u = k - 1;
            if (u > 0) fact = mulmod(fact, u, M);
            u64 x = invmod(fact, M); if (u & 1) x = (M - x) % M;   /* e_u */
            u64 target = (M - x) % M;                                 /* need s + e_u == 0 */
            if (getbit(S, target) && tau[k] == L - 1) tau[k] = L;
            step(S, T, M, x, nw - 1); T[nw - 1] = 0; u64 *tmp = S; S = T; T = tmp;
        }
        free(S); free(T);
    }
    printf("p=%llu tau:", (unsigned long long)p);
    double dens = 0, pw;
    for (u64 k = 1; k <= p; k++) {
        if (k == 2) { printf(" *"); continue; }
        printf(" %d%s", tau[k], tau[k] == Lmax ? "+" : "");
        pw = 1; for (int i = 0; i <= tau[k]; i++) pw *= (double)p;
        dens += 1.0 / pw;
    }
    printf("  | density_lb=%.6f\n", dens);
    return 0;
}
