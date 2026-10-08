// Depth-first version of gclass.c: counts |S_k| = #{a mod 2^k : g(a,2) >= k} for k <= K
// without storing the classes.  Work is split into NCH chunks (by index of the classes of S_k0).
// Also records, for classes in S_K, the distribution of v_2(rep+2) (distance to -2).
// Usage: gdfs K CAP k0 chunk nchunks
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static inline u64 inv64(u64 u) { u64 x = u; for (int i = 0; i < 6; i++) x *= 2 - u * x; return x; }
static inline int ctz64(u64 x) { return __builtin_ctzll(x); }

#define HSZ (1 << 20)
static u64 *bufA, *bufB;
static u64 hkeys[HSZ];
static uint32_t hstamp[HSZ];
static uint32_t curstamp = 0;

static inline int hinsert(u64 k) {
    u64 h = (k * 0x9E3779B97F4A7C15ULL) >> 44;
    while (1) {
        if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (hkeys[h] == k) return 0;
        h = (h + 1) & (HSZ - 1);
    }
}

static int g_capped(u64 a, int M) {
    int r = M; long np = 1; bufA[0] = 0; u64 N = a; int vacc = 0;
    while (1) {
        u64 n1 = N + 1; int t = ctz64(n1); u64 u = n1 >> t; int first = (N == a);
        u64 maskr = (r >= 64) ? ~0ULL : ((1ULL << r) - 1);
        if (t >= r) {
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                if (((c + 1) & maskr) == 0) return M;
                if (!first && (c & maskr) == 0) return M;
            }
            goto death;
        }
        {
            int rn = r - t; u64 maskn = (rn >= 64) ? ~0ULL : ((1ULL << rn) - 1);
            u64 iv = inv64(u); u64 pt = (t == 0) ? 0 : ((1ULL << t) - 1);
            long nn = 0; curstamp++;
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                for (int e = first ? 1 : 0; e <= 1; e++) {
                    u64 x = (c + e) & maskr;
                    if ((x & pt) != 0) continue;
                    u64 nc = ((x >> t) * iv) & maskn;
                    if (hinsert(nc)) bufB[nn++] = nc;
                }
            }
            if (nn == 0) goto death;
            if (nn > (1L << 19)) { fprintf(stderr, "population overflow\n"); exit(1); }
            u64 *tmp = bufA; bufA = bufB; bufB = tmp; np = nn; r = rn; vacc += t; N++;
            continue;
        }
    death:;
        { u64 m2 = (r >= 64) ? ~0ULL : ((1ULL << r) - 1); int best = -1;
          for (long i = 0; i < np; i++) { u64 c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { u64 x = (c + e) & m2; int v = x ? ctz64(x) : r; if (v > best) best = v; } }
          return vacc + best; }
    }
}

// For each shell j = v_2(a+2) and shift exponent s: count G and a with
// [g(a)>=G] != [g(a+2^{G-s})>=G], where a, a+2^{G-s} in [1,2^K], G-s > j (so both in same shell).
int main(int argc, char **argv) {
    int K = atoi(argv[1]); u64 n = 1ULL << K;
    bufA = malloc(sizeof(u64) << 20); bufB = malloc(sizeof(u64) << 20);
    unsigned char *g = malloc(n + 1);
    for (u64 a = 1; a <= n; a++) g[a] = (unsigned char)g_capped(a, 63);
    for (int j = 1; j <= 6; j++) {
        printf("shell j=%d:", j);
        for (int s = 1; s <= 8; s++) {
            long bad = 0, tests = 0; int firstG = -1;
            for (int G = s + j + 1; G <= K; G++) {
                u64 h = 1ULL << (G - s);
                for (u64 a = 1; a + h <= n; a++) {
                    u64 x = a + 2; if (__builtin_ctzll(x) != j) continue;
                    tests++;
                    if ((g[a] >= G) != (g[a + h] >= G)) { bad++; if (firstG < 0) firstG = G; }
                }
            }
            printf("  s=%d:%ld/%ld", s, bad, tests);
        }
        printf("\n");
    }
    return 0;
}
