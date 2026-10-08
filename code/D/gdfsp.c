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

static int K, CAP; static long long cnt[70]; static long long overflow = 0;
static void lift(u64 rep, int g, int k) {
    cnt[k]++;
    if (k == K) return;
    if (g >= k + 1) lift(rep, g, k + 1);
    for (u64 j = 1; j < P; j++) {
        u64 r1 = rep + j * PW[k];
        int g1 = g_capped(r1, CAP);
        if (g1 < 0) { overflow++; g1 = CAP; }  // treat as survivor (conservative: upper bound on |S_k|)
        if (g1 >= k + 1) lift(r1, g1, k + 1);
    }
}

int main(int argc, char **argv) {
    P = atoll(argv[1]); K = atoi(argv[2]); CAP = atoi(argv[3]); int k0 = atoi(argv[4]); int ch = atoi(argv[5]); int nch = atoi(argv[6]);
    POPLIM = argc > 7 ? atol(argv[7]) : (1L << 21);
    PW[0] = 1; MAXE = 0; while (MAXE < 63 && PW[MAXE] <= (~0ULL) / P / 2) { PW[MAXE + 1] = PW[MAXE] * P; MAXE++; }
    if (CAP > MAXE - 1) { fprintf(stderr, "CAP too large (max %d)\n", MAXE - 1); return 1; }
    bufA = malloc(sizeof(u64) * POPLIM); bufB = malloc(sizeof(u64) * POPLIM);
    long ns = 1; u64 *rep = malloc(sizeof(u64)); int *gv = malloc(sizeof(int));
    rep[0] = 1; gv[0] = g_capped(1, CAP); if (gv[0] < 0) gv[0] = CAP;
    for (int k = 0; k < k0; k++) {
        u64 *rep2 = malloc(sizeof(u64) * (P * ns + 2)); int *gv2 = malloc(sizeof(int) * (P * ns + 2)); long n2 = 0;
        for (long i = 0; i < ns; i++) {
            if (gv[i] >= k + 1) { rep2[n2] = rep[i]; gv2[n2] = gv[i]; n2++; }
            for (u64 j = 1; j < P; j++) {
                u64 r1 = rep[i] + j * PW[k]; int g1 = g_capped(r1, CAP); if (g1 < 0) { overflow++; g1 = CAP; }
                if (g1 >= k + 1) { rep2[n2] = r1; gv2[n2] = g1; n2++; } }
        }
        free(rep); free(gv); rep = rep2; gv = gv2; ns = n2;
        if (ch == 0) { printf("k=%d count=%ld density=%.6f\n", k + 1, ns, (double)ns / (double)PW[k + 1]); fflush(stdout); }
    }
    for (long i = ch; i < ns; i += nch) lift(rep[i], gv[i], k0);
    for (int k = k0; k <= K; k++) printf("k=%d count=%lld\n", k, cnt[k]);
    printf("maxpop=%ld overflow=%lld\n", maxpop_seen, overflow);
    return 0;
}
