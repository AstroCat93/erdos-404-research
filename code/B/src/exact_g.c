/*
 * exact_g.c -- exact value of g(a,p) := f(a,p) - v_p(a!) when it is small, by exhaustive residue DP.
 *
 *   sum_{n in A} n! = a! * (1 + sum_{j>=1} eps_j P_j),   P_j = (a+1)(a+2)...(a+j),
 * so g(a,p) = sup over finite 0/1 eps of v_p(1 + sum eps_j P_j).
 * Test "g >= G": residues mod p^G; after deciding eps_j, every later term is divisible by
 * p^{v_p(P_{j+1})}, so states not == 0 mod p^{min(G, v_p(P_{j+1}))} can be dropped (exact pruning).
 * When v_p(P_j) >= G all remaining terms vanish mod p^G.
 *
 * usage: exact_g p a Gcap cap
 * output: "p a v_p(a!) STATUS value maxstates"
 *    STATUS = EXACT  value = g        (g >= value proven by DP reaching 0, g >= value+1 refuted)
 *           = EXPLODED value = G      (DP for g >= G exceeded the state cap; g >= G-1 proven)
 *           = CAPPED   value = Gcap   (g >= Gcap proven)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int cmpu(const void *x, const void *y) { uint64_t a = *(const uint64_t *)x, b = *(const uint64_t *)y; return (a > b) - (a < b); }
static int vp(long long n, long long p) { int v = 0; while (n % p == 0) { n /= p; v++; } return v; }
static int vfact(long long n, long long p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }

static uint64_t *st, *nx; static size_t cap;

/* returns 1 if g>=G, 0 if not, -1 if exploded */
static int test(long long p, long long a, int G, size_t *maxst) {
    uint64_t Q = 1; for (int i = 0; i < G; i++) Q *= (uint64_t)p;
    size_t n = 1; st[0] = 1 % Q;
    int vnext = vp(a + 1, p);
    uint64_t pr = 1;
    /* initial prune */
    { int e = vnext < G ? vnext : G; uint64_t m = 1; for (int i = 0; i < e; i++) m *= p;
      size_t k = 0; for (size_t i = 0; i < n; i++) if (st[i] % m == 0) st[k++] = st[i]; n = k; }
    if (!n) return 0;
    int vP = 0;
    for (long long j = 1;; j++) {
        pr = (uint64_t)(((unsigned __int128)pr * (uint64_t)((a + j) % (long long)Q)) % Q);
        vP += vp(a + j, p);
        if (vP >= G) break;
        size_t m2 = 0;
        for (size_t i = 0; i < n; i++) { nx[m2++] = st[i]; uint64_t s = st[i] + pr; if (s >= Q) s -= Q; nx[m2++] = s; }
        int vn = vP + vp(a + j + 1, p); int e = vn < G ? vn : G;
        uint64_t md = 1; for (int i = 0; i < e; i++) md *= p;
        size_t k = 0; for (size_t i = 0; i < m2; i++) if (nx[i] % md == 0) nx[k++] = nx[i];
        qsort(nx, k, 8, cmpu);
        size_t u = 0; for (size_t i = 0; i < k; i++) if (u == 0 || nx[i] != nx[u - 1]) nx[u++] = nx[i];
        uint64_t *tmp = st; st = nx; nx = tmp; n = u;
        if (n > *maxst) *maxst = n;
        if (!n) return 0;
        if (n * 2 > cap) return -1;
    }
    for (size_t i = 0; i < n; i++) if (st[i] == 0) return 1;
    return n ? 1 : 0;  /* after final prune every state is 0 mod Q */
}

int main(int argc, char **argv) {
    long long p = atoll(argv[1]), a = atoll(argv[2]); int Gcap = atoi(argv[3]); cap = (size_t)atoll(argv[4]) * 2 + 4;
    st = malloc(cap * 8); nx = malloc(cap * 8);
    /* max G with p^G < 2^63 */
    int Gmax = 0; { unsigned __int128 q = 1; while (q * p < ((unsigned __int128)1 << 63)) { q *= p; Gmax++; } }
    if (Gcap > Gmax) Gcap = Gmax;
    size_t maxst = 1;
    for (int G = 1; G <= Gcap; G++) {
        int r = test(p, a, G, &maxst);
        if (r == 0) { printf("%lld %lld %d EXACT %d %zu\n", p, a, vfact(a, p), G - 1, maxst); return 0; }
        if (r < 0) { printf("%lld %lld %d EXPLODED %d %zu\n", p, a, vfact(a, p), G, maxst); return 0; }
    }
    printf("%lld %lld %d CAPPED %d %zu\n", p, a, vfact(a, p), Gcap, maxst);
    return 0;
}
