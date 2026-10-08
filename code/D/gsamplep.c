// General-p residue-class survival counts: |S_k| = #{a mod p^k : g(a,p) >= k}, k <= K.
// g(a,p) = f(a,p) - v_p(a!).  Uses c-recursion c_{N+1} = (c_N + eps)/(N+1) mod p^r.
// Usage: gdfsp p K CAP k0 chunk nchunks [maxpop]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;

static u64 P; static u64 PW[64]; static int MAXE;
static u64 *bufA, *bufB; static long BUFSZ;
#define HBITS 22
#define HSZ (1UL << HBITS)
static u64 hkeys[HSZ]; static uint32_t hstamp[HSZ]; static uint32_t curstamp = 0;
static inline int hinsert(u64 k) {
    u64 h = (k * 0x9E3779B97F4A7C15ULL) >> (64 - HBITS);
    while (1) {
        if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (hkeys[h] == k) return 0;
        h = (h + 1) & (HSZ - 1);
    }
}
static inline u64 mulmod(u64 a, u64 b, u64 m) { return (u64)(((u128)a * b) % m); }
static u64 invmod(u64 a, u64 m) { // a coprime to m
    __int128 t = 0, nt = 1, r = m, nr = a % m;
    while (nr) { __int128 q = r / nr, tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
    if (t < 0) t += m; return (u64)t;
}
static inline int vp(u64 x, u64 *rest) { int t = 0; while (x % P == 0) { x /= P; t++; } *rest = x; return t; }
static long maxpop_seen = 0; static long POPLIM;

// returns exact g(a) if < M, else M; returns -1 on population overflow
static int g_capped(u64 a, int M) {
    int r = M; long np = 1; bufA[0] = 0; u64 N = a; int vacc = 0;
    while (1) {
        u64 u; int t = vp(N + 1, &u); int first = (N == a);
        u64 modr = PW[r];
        if (t >= r) {
            for (long i = 0; i < np; i++) { u64 c = bufA[i];
                if ((c + 1) % modr == 0) return M;
                if (!first && c % modr == 0) return M; }
            goto death;
        }
        {
            int rn = r - t; u64 modn = PW[rn]; u64 iv = invmod(u % modn, modn); u64 pt = PW[t];
            long nn = 0; curstamp++;
            for (long i = 0; i < np; i++) { u64 c = bufA[i];
                for (int e = first ? 1 : 0; e <= 1; e++) {
                    u64 x = (c + e) % modr;
                    if (x % pt) continue;
                    u64 nc = mulmod((x / pt) % modn, iv, modn);
                    if (hinsert(nc)) { if (nn >= POPLIM) return -1; bufB[nn++] = nc; }
                } }
            if (nn == 0) goto death;
            if (nn > maxpop_seen) maxpop_seen = nn;
            u64 *tmp = bufA; bufA = bufB; bufB = tmp; np = nn; r = rn; vacc += t; N++;
            continue;
        }
    death:;
        { u64 modr = PW[r]; int best = -1;
          for (long i = 0; i < np; i++) { u64 c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { u64 x = (c + e) % modr; u64 rr; int v = x ? vp(x, &rr) : r; if (v > best) best = v; } }
          return vacc + best; }
    }
}

// Monte Carlo for general p: sample a uniform in [1, p^CAP], compute g(a,p) capped at CAP.
// "g >= k" depends only on a mod p^k, so this estimates d_k(p) for all k <= CAP simultaneously.
// Usage: gsamplep p nsamples seed CAP [poplim]
static u64 rs[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 nxt(void) { const u64 result = rotl(rs[1] * 5, 7) * 9; const u64 t = rs[1] << 17;
    rs[2] ^= rs[0]; rs[3] ^= rs[1]; rs[1] ^= rs[2]; rs[0] ^= rs[3]; rs[2] ^= t; rs[3] = rotl(rs[3], 45); return result; }
int main(int argc, char **argv) {
    P = atoll(argv[1]); long ns = atol(argv[2]); u64 seed = strtoull(argv[3], 0, 10); int CAP = atoi(argv[4]);
    POPLIM = argc > 5 ? atol(argv[5]) : (1L << 22);
    PW[0] = 1; MAXE = 0; while (MAXE < 63 && PW[MAXE] <= (~0ULL) / P / 2) { PW[MAXE + 1] = PW[MAXE] * P; MAXE++; }
    if (CAP > MAXE - 1) { fprintf(stderr, "CAP too large (max %d)\n", MAXE - 1); return 1; }
    bufA = malloc(sizeof(u64) * POPLIM); bufB = malloc(sizeof(u64) * POPLIM);
    rs[0] = seed * 0x9E3779B97F4A7C15ULL + 1; rs[1] = seed ^ 0xDEADBEEFULL; rs[2] = 12345 + seed; rs[3] = 0xABCDEF ^ (seed << 7);
    for (int i = 0; i < 20; i++) nxt();
    long long hist[70]; memset(hist, 0, sizeof(hist)); long ovf = 0;
    for (long i = 0; i < ns; i++) {
        u64 a = (u64)(((u128)nxt() * PW[CAP]) >> 64) + 1;
        int g = g_capped(a, CAP);
        if (g < 0) { ovf++; continue; }
        hist[g]++;
    }
    long long cum = 0; long nv = ns - ovf;
    for (int k = CAP; k >= 0; k--) { cum += hist[k]; hist[k] = cum; }
    for (int k = 0; k <= CAP; k++) printf("k=%d surv=%lld frac=%.6f\n", k, hist[k], (double)hist[k] / nv);
    printf("maxpop=%ld overflow=%ld\n", maxpop_seen, ovf);
    return 0;
}
