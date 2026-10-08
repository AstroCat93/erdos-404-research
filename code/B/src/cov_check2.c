/*
 * cov_check2.c -- second, independently written coverage checker (for large moduli where the
 * Python big-int checker would need too much memory).  Differences from cov.c:
 *   - uses an ACTUAL position N* = p^t K'' (K'' == K' mod p^c, random lift), computes
 *     M = v_p(N*!) - v_p((N*-H)!) by Legendre and elements (N1+i)!/N1! mod p^M directly;
 *   - "pull" formulation of the rotation: new[j] = old[j] | bits(old, j*64 - s mod Q .. +63),
 *     with an explicit wrap-around slow path.
 * usage: cov_check2 p t H nsample seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t Q; static size_t NW;
static int vfact_ll(unsigned long long n, unsigned long long p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }
static inline int getbit(const uint64_t *B, uint64_t i) { return (B[i >> 6] >> (i & 63)) & 1; }
/* 64 bits of B starting at bit position pos (0 <= pos < Q), cyclic mod Q */
static inline uint64_t bits_at(const uint64_t *B, uint64_t pos) {
    if (pos + 64 <= Q) {
        size_t w = pos >> 6; unsigned o = pos & 63;
        uint64_t lo = B[w] >> o;
        uint64_t hi = (o && w + 1 < NW) ? (B[w + 1] << (64 - o)) : 0;
        return lo | hi;
    }
    uint64_t r = 0;
    for (int k = 0; k < 64; k++) { uint64_t q = pos + k; if (q >= Q) q -= Q; r |= (uint64_t)getbit(B, q) << k; }
    return r;
}
static uint64_t rng = 88172645463325252ULL;
static uint64_t xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

int main(int argc, char **argv) {
    unsigned long long p = atoll(argv[1]); int t = atoi(argv[2]); int H = atoi(argv[3]);
    int nsample = atoi(argv[4]); rng ^= (uint64_t)atoll(argv[5]) * 0x9E3779B97F4A7C15ULL;
    int c = vfact_ll(H - 1, p);
    unsigned long long pc = 1; for (int i = 0; i < c; i++) pc *= p;
    unsigned long long pt = 1; for (int i = 0; i < t; i++) pt *= p;
    uint64_t *B = NULL, *Nn = NULL;
    int allok = 1;
    int exhaustive = (nsample == 0);
    if (exhaustive) nsample = (c == 0) ? 1 : (int)(pc - pc / p);
    unsigned long long nextK = 1;
    int quiet = exhaustive;
    for (int smp = 0; smp < nsample; smp++) {
        unsigned long long Kc;
        if (exhaustive) { while (c > 0 && nextK % p == 0) nextK++; Kc = nextK++; }
        else do { Kc = (c == 0) ? 1 : 1 + xr() % (pc - 1); } while (c > 0 && Kc % p == 0);
        unsigned long long Kpp = Kc + pc * (1 + xr() % 1000);
        if (Kpp % p == 0) Kpp += pc;
        unsigned long long Ns = pt * Kpp, N1 = Ns - H;
        int M = vfact_ll(Ns, p) - vfact_ll(N1, p);
        Q = 1; for (int i = 0; i < M; i++) Q *= p;
        NW = (Q + 63) / 64;
        B = realloc(B, NW * 8); Nn = realloc(Nn, NW * 8);
        memset(B, 0, NW * 8); B[0] = 1;
        uint64_t y = 1 % Q;
        for (int i = 0; i < H; i++) {
            if (i > 0) y = (uint64_t)(((unsigned __int128)y * ((N1 + i) % Q)) % Q);
            uint64_t s = y;
            if (s == 0) continue;
            uint64_t start = (Q - s) % Q;   /* bit j of shifted set = bit (j - s) mod Q of old */
            for (size_t w = 0; w < NW; w++) {
                uint64_t pos = (uint64_t)w * 64 + start; if (pos >= Q) pos -= Q;
                Nn[w] = B[w] | bits_at(B, pos);
            }
            if (Q % 64) Nn[NW - 1] &= (((uint64_t)1 << (Q % 64)) - 1);
            uint64_t *tmp = B; B = Nn; Nn = tmp;
        }
        uint64_t cnt = 0; for (size_t w = 0; w < NW; w++) cnt += __builtin_popcountll(B[w]);
        int ok = (cnt == Q);
        if (!ok) allok = 0;
        if (!quiet || !ok) printf("  p=%llu t=%d H=%d class K'=%llu (N*=%llu) M=%d covered=%llu/%llu %s\n", p, t, H, Kc, Ns, M,
               (unsigned long long)cnt, (unsigned long long)Q, ok ? "OK" : "NOT COVERED");
        fflush(stdout);
    }
    printf("cov_check2 p=%llu t=%d H=%d %s=%d -> %s\n", p, t, H, exhaustive ? "classes(all)" : "samples", nsample, allok ? "ALL COVERED" : "FAILURES");
    return 0;
}
