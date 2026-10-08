/* dens2.c -- word-level (fast) version of zdens.c / gdens.c.
 * mode Z: U_k = { r mod p^k : 0 in B_r mod p^k },  B_x = {1 + sum_{j>=1} e_j prod_{l=1}^{j}(x+l)}
 *         (for natural a: g(a,p) = f(a,p)-v_p(a!) >= k  iff  a mod p^k in U_k)
 * mode G: G_k = { r mod p^k : A_r mod p^k = Z/p^k },  A_x = {sum_{j>=0} e_j prod_{l=1}^{j}(x+l)}
 *         (A_N = Z_p iff N mod p^k in G_k for all k)
 * Survivors at level k+1 are lifts of survivors at level k (both properties are inherited by reduction).
 * Usage: ./dens2 Z|G p kmax [print_upto]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint64_t *A, *T1, *T2;
static long MOD, W;
static uint64_t LASTMASK;

static void shl(uint64_t *d, const uint64_t *s, long sh) { /* d = s << sh, truncated to MOD bits */
    long q = sh >> 6; int r = sh & 63;
    for (long w = W - 1; w >= 0; w--) {
        uint64_t v = 0;
        long a = w - q;
        if (a >= 0) { v = s[a] << r; if (r && a - 1 >= 0) v |= s[a - 1] >> (64 - r); }
        d[w] = v;
    }
    d[W - 1] &= LASTMASK;
}
static void shr(uint64_t *d, const uint64_t *s, long sh) { /* d = s >> sh */
    long q = sh >> 6; int r = sh & 63;
    for (long w = 0; w < W; w++) {
        uint64_t v = 0;
        long a = w + q;
        if (a < W) { v = s[a] >> r; if (r && a + 1 < W) v |= s[a + 1] << (64 - r); }
        d[w] = v;
    }
}
static void rot_or(long c) { /* A |= rotate_left(A, c) on Z/MOD */
    shl(T1, A, c); shr(T2, A, MOD - c);
    for (long w = 0; w < W; w++) A[w] |= T1[w] | T2[w];
}
static long popc(void) { long s = 0; for (long w = 0; w < W; w++) s += __builtin_popcountll(A[w]); return s; }

int main(int argc, char **argv) {
    char mode = argv[1][0];
    int p = atoi(argv[2]), kmax = atoi(argv[3]);
    int pr = argc > 4 ? atoi(argv[4]) : 0;
    long cap = 1; for (int i = 0; i < kmax; i++) cap *= p;
    long Wc = (cap >> 6) + 2;
    A = calloc(Wc, 8); T1 = calloc(Wc, 8); T2 = calloc(Wc, 8);
    long *surv = malloc(sizeof(long)), nsurv = 1; surv[0] = 0;
    long pk = 1;
    for (int k = 1; k <= kmax; k++) {
        long prev = pk; pk *= p; MOD = pk; W = (MOD + 63) >> 6;
        LASTMASK = (MOD & 63) ? ((1ULL << (MOD & 63)) - 1) : ~0ULL;
        long *ns = malloc(sizeof(long) * nsurv * p); long nn = 0;
        for (long t = 0; t < nsurv; t++) for (int d = 0; d < p; d++) {
            long r = surv[t] + d * prev;
            memset(A, 0, W * 8);
            int ok = 0;
            long c = 1 % MOD;
            if (mode == 'Z') { A[0] = (MOD > 1) ? 2ULL : 1ULL; }       /* {1} */
            else { A[0] = 1ULL; if (c) rot_or(c); }                    /* {0} then add element 1 */
            for (long j = 1; ; j++) {
                if (mode == 'Z' && (A[0] & 1ULL)) { ok = 1; break; }
                if (mode == 'G' && popc() >= MOD) { ok = 1; break; }
                c = (long)((__int128)c * ((r + j) % MOD) % MOD);
                if (c == 0) break;
                rot_or(c);
            }
            if (!ok) {
                if (mode == 'Z' && (A[0] & 1ULL)) ok = 1;
                if (mode == 'G' && popc() >= MOD) ok = 1;
            }
            if (ok) ns[nn++] = r;
        }
        free(surv); surv = ns; nsurv = nn;
        printf("%c p=%d k=%d  count=%ld  density=%.6f\n", mode, p, k, nsurv, (double)nsurv / pk);
        if (nsurv <= pr) { printf("   set = {"); for (long t = 0; t < nsurv; t++) printf("%ld%s", surv[t], t + 1 < nsurv ? "," : ""); printf("}\n"); }
        fflush(stdout);
        if (nsurv == 0) break;
    }
    return 0;
}
