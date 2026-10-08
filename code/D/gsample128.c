// Monte Carlo estimate of d_k = mu{alpha in Z_2 : g(alpha) >= k} for k <= 126 (p = 2).
// Since "g(a) >= k" depends only on a mod 2^k, a uniform random integer a in [1, 2^126]
// gives, for every k <= 126 simultaneously, an unbiased sample of the class a mod 2^k.
// Exact g(a) (capped at CAP <= 126) via the c-recursion mod 2^r using 128-bit arithmetic.
// Usage: gsample128 nsamples seed CAP
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;

static inline u128 inv128(u128 u) { u128 x = u; for (int i = 0; i < 7; i++) x *= (u128)2 - u * x; return x; }
static inline int ctz128(u128 x) { u64 lo = (u64)x; if (lo) return __builtin_ctzll(lo); return 64 + __builtin_ctzll((u64)(x >> 64)); }
static inline u128 maskof(int r) { return r >= 128 ? ~(u128)0 : (((u128)1 << r) - 1); }

#define HBITS 20
#define HSZ (1UL << HBITS)
static u128 hkeys[HSZ]; static uint32_t hstamp[HSZ]; static uint32_t curstamp = 0;
static inline int hinsert(u128 k) {
    u64 h = ((u64)k ^ (u64)(k >> 64)) * 0x9E3779B97F4A7C15ULL; h >>= (64 - HBITS);
    while (1) {
        if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (hkeys[h] == k) return 0;
        h = (h + 1) & (HSZ - 1);
    }
}
static u128 *bufA, *bufB; static long POPLIM = 1L << 19; static long maxpop = 0;

static int g_capped(u128 a, int M) {
    int r = M; long np = 1; bufA[0] = 0; u128 N = a; int vacc = 0;
    while (1) {
        u128 n1 = N + 1; int t = ctz128(n1); u128 u = n1 >> t; int first = (N == a);
        u128 mr = maskof(r);
        if (t >= r) {
            for (long i = 0; i < np; i++) { u128 c = bufA[i];
                if (((c + 1) & mr) == 0) return M;
                if (!first && (c & mr) == 0) return M; }
            goto death;
        }
        { int rn = r - t; u128 mn = maskof(rn); u128 iv = inv128(u); u128 pt = maskof(t);
          long nn = 0; curstamp++;
          for (long i = 0; i < np; i++) { u128 c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) {
                u128 x = (c + e) & mr; if (x & pt) continue;
                u128 nc = ((x >> t) * iv) & mn;
                if (hinsert(nc)) { if (nn >= POPLIM) { fprintf(stderr, "overflow\n"); exit(1); } bufB[nn++] = nc; }
            } }
          if (nn == 0) goto death;
          if (nn > maxpop) maxpop = nn;
          u128 *tmp = bufA; bufA = bufB; bufB = tmp; np = nn; r = rn; vacc += t; N++; continue; }
    death:;
        { u128 mr2 = maskof(r); int best = -1;
          for (long i = 0; i < np; i++) { u128 c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { u128 x = (c + e) & mr2; int v = x ? ctz128(x) : r; if (v > best) best = v; } }
          return vacc + best; }
    }
}

static u64 s[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 next(void) { const u64 result = rotl(s[1] * 5, 7) * 9; const u64 t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return result; }

int main(int argc, char **argv) {
    long ns = atol(argv[1]); u64 seed = strtoull(argv[2], 0, 10); int CAP = atoi(argv[3]);
    s[0] = seed * 0x9E3779B97F4A7C15ULL + 1; s[1] = seed ^ 0xDEADBEEFULL; s[2] = 12345 + seed; s[3] = 0xABCDEF ^ (seed << 7);
    for (int i = 0; i < 20; i++) next();
    bufA = malloc(sizeof(u128) * POPLIM); bufB = malloc(sizeof(u128) * POPLIM);
    long long hist[130]; memset(hist, 0, sizeof(hist));
    for (long i = 0; i < ns; i++) {
        u128 a = (((u128)next() << 64) | next()) & maskof(126);
        if (a == 0) a = (u128)1 << 126;
        int g = g_capped(a, CAP);
        hist[g]++;
    }
    // print survival counts: number of samples with g >= k
    long long cum = 0;
    for (int k = CAP; k >= 0; k--) { cum += hist[k]; hist[k] = cum; }
    for (int k = 0; k <= CAP; k++) printf("k=%d surv=%lld frac=%.6f\n", k, hist[k], (double)hist[k] / ns);
    fprintf(stderr, "maxpop=%ld\n", maxpop);
    return 0;
}
