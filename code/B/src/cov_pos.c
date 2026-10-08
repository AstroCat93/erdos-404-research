/*
 * cov_pos.c -- position-specific version of cov.c (same bitset core, written for the
 * publication check of 2026-10-08; it shares no code with the referee's rcover.c).
 *
 * For N* = p^t K'' (p not dividing K'') the normalised block {n!/p^{v((N*-H)!)} : N*-H <= n < N*}
 * is U * {y_i(K'')}, 0 <= i < H, with U a p-adic unit and
 *      y_i(K'') = prod_{s=1}^{i} (p^t K'' - (H-s))                (note.md, Theorem 3.12(a)),
 * and the block raises the valuation by t + c, c = v_p((H-1)!).
 * This program checks, for each K'' given on the command line, whether the 2^H subset sums of
 * y_0..y_{H-1} cover Z/p^{t+c}.  (Unlike cov.c it does NOT range over all unit classes K' mod p^c;
 * it certifies the block only at the listed positions N* = p^t K''.)
 *
 * usage: cov_pos p t H K1 [K2 ...]
 * memory: two bitsets of p^{t+c} bits each.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static uint64_t Q;
static size_t NW;
static uint64_t *Bs, *Tmp;

static void mask_top(uint64_t *b) {
    uint64_t r = Q % 64;
    if (r) b[NW - 1] &= ((uint64_t)1 << r) - 1;
}
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
static uint64_t popc(const uint64_t *b) { uint64_t s = 0; for (size_t i = 0; i < NW; i++) s += __builtin_popcountll(b[i]); return s; }

/* number of residues mod Q NOT reached by subset sums of y[0..n) (empty sum included) */
static uint64_t missing(const uint64_t *y, int n) {
    memset(Bs, 0, NW * 8); Bs[0] = 1;
    for (int i = 0; i < n; i++) {
        uint64_t s = y[i] % Q;
        if (s == 0) continue;
        memcpy(Tmp, Bs, NW * 8);
        shl_or(Bs, Tmp, s);       /* x -> x + s, for x + s < Q      */
        shr_or(Bs, Tmp, Q - s);   /* x -> x + s - Q, for x + s >= Q */
        mask_top(Bs);
    }
    return Q - popc(Bs);
}
static int vp_fact(long long n, long long p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s p t H K1 [K2 ...]\n", argv[0]); return 1; }
    long long p = atoll(argv[1]); int t = atoi(argv[2]); int H = atoi(argv[3]);
    int c = vp_fact(H - 1, p), M = t + c;
    uint64_t q = 1;
    for (int i = 0; i < M; i++) { if (q > UINT64_MAX / (uint64_t)p) { fprintf(stderr, "modulus too large\n"); return 1; } q *= (uint64_t)p; }
    Q = q; NW = (Q + 63) / 64;
    Bs = malloc(NW * 8); Tmp = malloc(NW * 8);
    if (!Bs || !Tmp) { fprintf(stderr, "alloc failed (%zu bytes x 2)\n", NW * 8); return 2; }
    uint64_t ptQ = 1; for (int i = 0; i < t; i++) ptQ = (uint64_t)(((unsigned __int128)ptQ * (uint64_t)p) % Q);
    uint64_t *y = malloc((size_t)H * 8);
    int allok = 1;
    for (int k = 4; k < argc; k++) {
        long long K = atoll(argv[k]);
        if (K % p == 0) { printf("K''=%lld is divisible by p; skipped\n", K); continue; }
        clock_t t0 = clock();
        uint64_t base = (uint64_t)(((unsigned __int128)ptQ * (uint64_t)K) % Q);   /* p^t K'' mod Q */
        y[0] = 1 % Q;
        for (int i = 1; i < H; i++) {
            uint64_t f = (base + Q - ((uint64_t)(H - i) % Q)) % Q;                 /* p^t K'' - (H-i) */
            y[i] = (uint64_t)(((unsigned __int128)y[i - 1] * f) % Q);
        }
        uint64_t m = missing(y, H);
        if (m) allok = 0;
        printf("p=%lld t=%d H=%d c=%d mod p^%d  K''=%lld  missing=%llu  %s  [%.1fs]\n", p, t, H, c, M, K,
               (unsigned long long)m, m ? "NOT COVERED" : "COVERED", (double)(clock() - t0) / CLOCKS_PER_SEC);
        fflush(stdout);
    }
    printf("%s\n", allok ? "ALL LISTED POSITIONS COVERED" : "SOME POSITION NOT COVERED");
    return allok ? 0 : 3;
}
