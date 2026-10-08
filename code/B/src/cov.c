/*
 * cov.c -- exhaustive certificates for the Tao-type block lemma, uniform in the position.
 *
 * Setting.  P(a,p,N): exists T subset [a,N), min T = a, with p^{v(N)} | sum_{n in T} n!,  v(N)=v_p(N!).
 * Block lemma: if N1 > a and the subset sums of { n!/p^{v(N1)} : N1 <= n < N2 } cover Z/p^{v(N2)-v(N1)},
 * then P(a,p,N1) => P(a,p,N2).
 *
 * Here: N2 = N* = p^t K' with p not dividing K', and N1 = N* - H with 1 <= H <= p^t.
 *   v(N*) - v(N*-H) = t + c,  c := v_p((H-1)!)      (since v_p(N*-x) = v_p(x) for 0<x<p^t)
 *   n!/p^{v(N1)} = U(N1) * y_i,   y_i := prod_{s=1}^{i} (p^t K' - (H-s)),  i = n - N1 in [0,H)
 *   (U(N1) a p-adic unit; multiplying all elements by a unit does not change coverage.)
 *   y_i mod p^{t+c} depends only on K' mod p^c.
 * Cov(p,t,H): for EVERY unit class K' mod p^c, subset sums of {y_0..y_{H-1}} cover Z/p^{t+c}.
 * If Cov(p,t,H) holds then for every a and every N* with v_p(N*) = t and N* - H > a:
 *      P(a,p,N*-H) => P(a,p,N*).
 *
 * usage: cov p t Hmin Hmax [maxbits_log2=33] [stop_at_first=1]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static uint64_t Q;  /* modulus p^M */
static size_t NW;   /* words */
static uint64_t *Bs, *Tmp;

static void mask_top(uint64_t *b) {
    uint64_t r = Q % 64;
    if (r) b[NW - 1] &= ((uint64_t)1 << r) - 1;
}
/* dst |= src << s  (bits >= Q dropped) */
static void shl_or(uint64_t *dst, const uint64_t *src, uint64_t s) {
    size_t ws = s / 64; unsigned bs = s % 64;
    if (ws >= NW) return;
    if (bs == 0) {
        for (size_t i = NW; i-- > ws;) dst[i] |= src[i - ws];
    } else {
        for (size_t i = NW - 1; i > ws; i--) dst[i] |= (src[i - ws] << bs) | (src[i - ws - 1] >> (64 - bs));
        dst[ws] |= src[0] << bs;
    }
}
/* dst |= src >> s  */
static void shr_or(uint64_t *dst, const uint64_t *src, uint64_t s) {
    size_t ws = s / 64; unsigned bs = s % 64;
    if (ws >= NW) return;
    if (bs == 0) {
        for (size_t i = 0; i + ws < NW; i++) dst[i] |= src[i + ws];
    } else {
        for (size_t i = 0; i + ws + 1 < NW; i++) dst[i] |= (src[i + ws] >> bs) | (src[i + ws + 1] << (64 - bs));
        dst[NW - 1 - ws] |= src[NW - 1] >> bs;
    }
}
static int full(const uint64_t *b) {
    for (size_t i = 0; i + 1 < NW; i++) if (b[i] != ~(uint64_t)0) return 0;
    uint64_t r = Q % 64; uint64_t m = r ? (((uint64_t)1 << r) - 1) : ~(uint64_t)0;
    return (b[NW - 1] & m) == m;
}
static uint64_t popc(const uint64_t *b) { uint64_t s = 0; for (size_t i = 0; i < NW; i++) s += __builtin_popcountll(b[i]); return s; }

/* returns 1 if subset sums of y[0..n) cover Z/Q */
static int covers(const uint64_t *y, int n, uint64_t *missing) {
    memset(Bs, 0, NW * 8); Bs[0] = 1;
    for (int i = 0; i < n; i++) {
        uint64_t s = y[i] % Q;
        if (s == 0) continue;
        memcpy(Tmp, Bs, NW * 8);
        shl_or(Bs, Tmp, s);
        shr_or(Bs, Tmp, Q - s);
        mask_top(Bs);
    }
    int f = full(Bs);
    if (missing) *missing = Q - popc(Bs);
    return f;
}

static int vp_fact(long long n, long long p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s p t Hmin Hmax [maxbits_log2] [stop_first]\n", argv[0]); return 1; }
    long long p = atoll(argv[1]); int t = atoi(argv[2]); int Hmin = atoi(argv[3]), Hmax = atoi(argv[4]);
    int maxlog = argc > 5 ? atoi(argv[5]) : 33;
    int stop_first = argc > 6 ? atoi(argv[6]) : 1;
    int nsplit = argc > 7 ? atoi(argv[7]) : 1, split = argc > 8 ? atoi(argv[8]) : 0;
    long long pt = 1; for (int i = 0; i < t && pt < (1LL << 40); i++) pt *= p;
    for (int H = Hmin; H <= Hmax; H++) {
        if (H > pt) { printf("H=%d exceeds p^t\n", H); break; }
        int c = vp_fact(H - 1, p), M = t + c;
        /* Q = p^M */
        double lq = 0; uint64_t q = 1; int ok = 1;
        for (int i = 0; i < M; i++) { if (q > (UINT64_MAX / p)) { ok = 0; break; } q *= p; }
        if (!ok) { printf("H=%d M=%d: modulus too large\n", H, M); continue; }
        Q = q; lq = 0; { uint64_t z = Q; while (z > 1) { z >>= 1; lq++; } }
        if (lq > maxlog) { printf("H=%d c=%d M=%d: 2^%.0f bits exceeds limit\n", H, c, M, lq); continue; }
        /* trivial necessary condition: 2^H >= Q */
        if (H < 64 && ((uint64_t)1 << H) < Q) { printf("H=%d c=%d M=%d: 2^H < p^M, impossible\n", H, c, M); fflush(stdout); continue; }
        NW = (Q + 63) / 64;
        Bs = realloc(Bs, NW * 8); Tmp = realloc(Tmp, NW * 8);
        uint64_t pc = 1; for (int i = 0; i < c; i++) pc *= p;
        uint64_t ptQ = 1; for (int i = 0; i < t && i < M; i++) ptQ *= p;  /* p^t mod Q (t < M or t==M -> 0) */
        if (t >= M) ptQ = 0;
        uint64_t *y = malloc(H * 8);
        long long nclass = 0, nfail = 0; uint64_t worst_missing = 0;
        clock_t t0 = clock();
        long long first_fail[8]; int nff = 0;
        for (uint64_t Kc = (c == 0 ? 1 : 1); Kc < (c == 0 ? 2 : pc); Kc++) {
            if (c > 0 && Kc % p == 0) continue;
            if ((long long)(Kc % (uint64_t)nsplit) != split) continue;
            nclass++;
            uint64_t base = (uint64_t)(((unsigned __int128)ptQ * Kc) % Q);  /* p^t K' mod Q */
            y[0] = 1 % Q;
            for (int i = 1; i < H; i++) {
                uint64_t x = (uint64_t)(H - i);
                uint64_t f = (base + Q - (x % Q)) % Q;
                y[i] = (uint64_t)(((unsigned __int128)y[i - 1] * f) % Q);
            }
            uint64_t miss = 0;
            if (!covers(y, H, &miss)) {
                nfail++; if (miss > worst_missing) worst_missing = miss;
                if (nff < 8) first_fail[nff++] = (long long)Kc;
            }
        }
        if (nsplit > 1) printf("[split %d/%d] ", split, nsplit);
        printf("p=%lld t=%d H=%d c=%d M=%d Q=p^%d (2^%.0f bits) classes=%lld FAIL=%lld worst_missing=%llu  [%.1fs]",
               p, t, H, c, M, M, lq, nclass, nfail, (unsigned long long)worst_missing, (double)(clock() - t0) / CLOCKS_PER_SEC);
        if (nff) { printf("  failing K' mod p^c e.g."); for (int i = 0; i < nff; i++) printf(" %lld", first_fail[i]); }
        printf("%s\n", nfail == 0 ? "  => Cov HOLDS" : "");
        fflush(stdout);
        free(y);
        if (nfail == 0 && stop_first) break;
    }
    return 0;
}
