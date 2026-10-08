// 256-bit version of gsample128.c: Monte Carlo estimate of d_k = mu{g(alpha,2) >= k}, k <= 254.
// Usage: gsample256 nsamples seed CAP
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
typedef struct { u64 w[4]; } U;

static inline U uz(void) { U x = {{0, 0, 0, 0}}; return x; }
static inline U addsmall(U x, u64 e) { for (int i = 0; i < 4 && e; i++) { u64 o = x.w[i]; x.w[i] += e; e = (x.w[i] < o); } return x; }
static inline U mask(U x, int r) { for (int i = 0; i < 4; i++) { int lo = 64 * i; if (r <= lo) x.w[i] = 0; else if (r < lo + 64) x.w[i] &= ((1ULL << (r - lo)) - 1); } return x; }
static inline int iszero(U x) { return !(x.w[0] | x.w[1] | x.w[2] | x.w[3]); }
static inline int ctz(U x) { for (int i = 0; i < 4; i++) if (x.w[i]) return 64 * i + __builtin_ctzll(x.w[i]); return 256; }
static inline U shr(U x, int t) { U y = uz(); int q = t / 64, s = t % 64;
    for (int i = 0; i + q < 4; i++) { u64 lo = x.w[i + q] >> s; u64 hi = (s && i + q + 1 < 4) ? (x.w[i + q + 1] << (64 - s)) : 0; y.w[i] = lo | hi; } return y; }
static inline U mul(U a, U b) { U r = uz(); for (int i = 0; i < 4; i++) { u128 carry = 0;
        for (int j = 0; i + j < 4; j++) { u128 cur = (u128)a.w[i] * b.w[j] + r.w[i + j] + carry; r.w[i + j] = (u64)cur; carry = cur >> 64; } } return r; }
static inline U sub(U a, U b) { U r; u64 br = 0; for (int i = 0; i < 4; i++) { u64 t = a.w[i] - b.w[i] - br; br = (a.w[i] < b.w[i]) || (a.w[i] - b.w[i] < br); r.w[i] = t; } return r; }
static inline U two(void) { U x = uz(); x.w[0] = 2; return x; }
static U inv(U u) { U x = u; for (int i = 0; i < 9; i++) x = mul(x, sub(two(), mul(u, x))); return x; }
static inline int eq(U a, U b) { return a.w[0] == b.w[0] && a.w[1] == b.w[1] && a.w[2] == b.w[2] && a.w[3] == b.w[3]; }

#define HBITS 20
#define HSZ (1UL << HBITS)
static U hkeys[HSZ]; static uint32_t hstamp[HSZ]; static uint32_t curstamp = 0;
static inline int hinsert(U k) {
    u64 h = (k.w[0] ^ (k.w[1] * 31) ^ (k.w[2] * 131) ^ (k.w[3] * 1031)) * 0x9E3779B97F4A7C15ULL; h >>= (64 - HBITS);
    while (1) { if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (eq(hkeys[h], k)) return 0; h = (h + 1) & (HSZ - 1); }
}
static U *bufA, *bufB; static long POPLIM = 1L << 19; static long maxpop = 0;

static int g_capped(U a, int M) {
    int r = M; long np = 1; bufA[0] = uz(); U N = a; int vacc = 0;
    while (1) {
        U n1 = addsmall(N, 1); int t = ctz(n1); U u = shr(n1, t); int first = eq(N, a);
        if (t >= r) {
            for (long i = 0; i < np; i++) { U c = bufA[i];
                if (iszero(mask(addsmall(c, 1), r))) return M;
                if (!first && iszero(mask(c, r))) return M; }
            goto death;
        }
        { int rn = r - t; U iv = inv(u); long nn = 0; curstamp++;
          for (long i = 0; i < np; i++) { U c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) {
                U x = mask(addsmall(c, e), r); if (t && ctz(x) < t) continue;
                U nc = mask(mul(shr(x, t), iv), rn);
                if (hinsert(nc)) { if (nn >= POPLIM) { fprintf(stderr, "overflow\n"); exit(1); } bufB[nn++] = nc; }
            } }
          if (nn == 0) goto death;
          if (nn > maxpop) maxpop = nn;
          U *tmp = bufA; bufA = bufB; bufB = tmp; np = nn; r = rn; vacc += t; N = addsmall(N, 1); continue; }
    death:;
        { int best = -1;
          for (long i = 0; i < np; i++) { U c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { U x = mask(addsmall(c, e), r); int v = iszero(x) ? r : ctz(x); if (v > best) best = v; } }
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
    bufA = malloc(sizeof(U) * POPLIM); bufB = malloc(sizeof(U) * POPLIM);
    long long hist[260]; memset(hist, 0, sizeof(hist));
    if (ns == 0) { for (int j = 4; j < argc; j++) { U a = uz(); a.w[0] = strtoull(argv[j], 0, 10);
            printf("a=%s g=%d\n", argv[j], g_capped(a, CAP)); } return 0; }
    for (long i = 0; i < ns; i++) {
        U a; for (int j = 0; j < 4; j++) a.w[j] = next();
        a = mask(a, 254); if (iszero(a)) a.w[3] = 1ULL << 62;
        int g = g_capped(a, CAP); hist[g]++;
    }
    long long cum = 0;
    for (int k = CAP; k >= 0; k--) { cum += hist[k]; hist[k] = cum; }
    for (int k = 0; k <= CAP; k++) printf("k=%d surv=%lld frac=%.6f\n", k, hist[k], (double)hist[k] / ns);
    fprintf(stderr, "maxpop=%ld\n", maxpop);
    return 0;
}
