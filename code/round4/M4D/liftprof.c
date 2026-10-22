/* liftprof.c -- subset-sum support of a list of residues modulo M = p^K as a bitset (rotate-or), and the
 * per-class lift counts  L[r] = #{ t in [0, p^(K-D)) : r + p^D t is a subset sum mod M },  r in [0, p^D).
 * Used by lift_scan.py (track M4D, round 4) for windows beyond numpy's comfortable range.
 * Input (stdin, whitespace separated): p K D H y_0 ... y_{H-1}   (y_i already reduced mod p^K)
 * Output (stdout): one line "LIFT n_sums_bits" then p^D integers L[0..p^D-1].
 * Memory: 2 * M/8 bytes.  Build: gcc -O2 -o liftprof liftprof.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t M, NW;

static inline uint64_t get64(const uint64_t *src, uint64_t off) {
    uint64_t w = off >> 6, b = off & 63;
    if (!b) return src[w];
    return (src[w] >> b) | (src[w + 1] << (64 - b));
}

/* dst bits [doff, doff+len) |= src bits [soff, soff+len) ; src padded with zero words */
static void or_range(uint64_t *dst, uint64_t doff, const uint64_t *src, uint64_t soff, uint64_t len) {
    if (!len) return;
    uint64_t end = doff + len;
    uint64_t dw0 = doff >> 6, dw1 = (end - 1) >> 6;
    for (uint64_t dw = dw0; dw <= dw1; dw++) {
        uint64_t lo = dw << 6, hi = lo + 64;
        uint64_t a = lo < doff ? doff : lo, z = hi > end ? end : hi;  /* bits [a,z) of this word */
        uint64_t val;
        /* source bit for destination bit d is d - doff + soff; read 64 bits starting at lo - doff + soff
           but lo - doff may be negative for the first word: handle by reading from a and shifting */
        uint64_t sstart = a - doff + soff;
        val = get64(src, sstart);           /* bit k of val = source bit for destination bit a+k */
        uint64_t nb = z - a;
        if (nb < 64) val &= ((uint64_t)1 << nb) - 1;
        dst[dw] |= val << (a - lo);
    }
}

int main(void) {
    long p, K, D, H;
    if (scanf("%ld %ld %ld %ld", &p, &K, &D, &H) != 4) return 1;
    M = 1; for (long i = 0; i < K; i++) M *= (uint64_t)p;
    uint64_t pD = 1; for (long i = 0; i < D; i++) pD *= (uint64_t)p;
    NW = (M + 63) / 64 + 2;
    uint64_t *S = calloc(NW, 8), *T = calloc(NW, 8);
    if (!S || !T) { fprintf(stderr, "alloc failed\n"); return 2; }
    S[0] = 1;                                     /* empty sum 0 */
    for (long h = 0; h < H; h++) {
        unsigned long long yy; if (scanf("%llu", &yy) != 1) return 3;
        uint64_t y = (uint64_t)yy % M;
        if (!y) continue;
        memcpy(T, S, NW * 8);
        or_range(T, y, S, 0, M - y);              /* s -> s + y for s < M - y */
        or_range(T, 0, S, M - y, y);              /* s -> s + y - M for s >= M - y */
        uint64_t *tmp = S; S = T; T = tmp;
        /* clear padding bits beyond M */
        if (M & 63) S[M >> 6] &= ((uint64_t)1 << (M & 63)) - 1;
        for (uint64_t w = (M >> 6) + 1; w < NW; w++) S[w] = 0;
    }
    uint64_t *L = calloc(pD, 8);
    uint64_t cnt = 0;
    for (uint64_t w = 0; w < (M + 63) / 64; w++) {
        uint64_t x = S[w];
        if (!x) continue;
        uint64_t base = (w << 6) % pD;
        while (x) {
            int b = __builtin_ctzll(x);
            x &= x - 1;
            uint64_t r = base + (uint64_t)b;
            while (r >= pD) r -= pD;
            L[r]++;
            cnt++;
        }
    }
    printf("LIFT %llu\n", (unsigned long long)cnt);
    for (uint64_t r = 0; r < pD; r++) printf("%llu\n", (unsigned long long)L[r]);
    return 0;
}
