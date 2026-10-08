/* zdens.c -- density of U_k = { r mod p^k : 0 in B_r mod p^k },
 *   B_x = { 1 + sum_{j>=1} e_j prod_{l=1}^{j} (x+l) }  (x in Z_p),
 * so that for natural a:  g(a,p) := f(a,p) - v_p(a!) >= k  iff  (a mod p^k) in U_k.
 * U_{k+1} is contained in the lifts of U_k, so we refine survivors level by level.
 * Exact bitset subset-sum over Z/p^k.  Usage: ./zdens p kmax [print_upto]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint64_t *A, *B;
static long MOD, W;

static inline int getbit(const uint64_t *x, long i) { return (x[i >> 6] >> (i & 63)) & 1; }

/* B = A rotated left by s (bit i -> bit (i+s) mod MOD); then A |= B */
static void rot_or(long s) {
    memset(B, 0, W * 8);
    /* simple but correct: iterate words of A, place bits; use shift on 64-bit chunks */
    for (long w = 0; w < W; w++) {
        uint64_t v = A[w];
        if (!v) continue;
        long base = w * 64;
        while (v) {
            int b = __builtin_ctzll(v);
            v &= v - 1;
            long i = base + b;
            if (i >= MOD) break;
            long t = i + s; if (t >= MOD) t -= MOD;
            B[t >> 6] |= 1ULL << (t & 63);
        }
    }
    for (long w = 0; w < W; w++) A[w] |= B[w];
}

int main(int argc, char **argv) {
    int p = atoi(argv[1]), kmax = atoi(argv[2]);
    int pr = argc > 3 ? atoi(argv[3]) : 0;
    long cap = 1; for (int i = 0; i < kmax; i++) cap *= p;
    long *surv = malloc(sizeof(long) * 1), nsurv = 1; surv[0] = 0; /* level 0: everything */
    long pk = 1;
    A = malloc(((cap >> 6) + 2) * 8); B = malloc(((cap >> 6) + 2) * 8);
    for (int k = 1; k <= kmax; k++) {
        long prev = pk; pk *= p; MOD = pk; W = (MOD >> 6) + 1;
        long *ns = malloc(sizeof(long) * nsurv * p); long nn = 0;
        for (long t = 0; t < nsurv; t++) for (int d = 0; d < p; d++) {
            long r = surv[t] + d * prev;
            memset(A, 0, W * 8);
            A[0] = 1ULL << 1 % 64; if (MOD == 1) A[0] = 1; /* start set {1} */
            if (MOD > 1) { A[0] = 0; A[1 >> 6] |= 1ULL << (1 & 63); }
            long c = 1 % MOD; int ok = 0;
            for (long j = 1; ; j++) {
                c = (long)((__int128)c * ((r + j) % MOD) % MOD);
                if (c == 0) break;
                rot_or(c);
                if (getbit(A, 0)) { ok = 1; break; }
            }
            if (!ok && getbit(A, 0)) ok = 1;
            if (ok) ns[nn++] = r;
        }
        free(surv); surv = ns; nsurv = nn;
        printf("p=%d k=%d  |U_k|=%ld  density=%.6f\n", p, k, nsurv, (double)nsurv / pk);
        if (nsurv <= pr) { printf("   U_k = {"); for (long t = 0; t < nsurv; t++) printf("%ld%s", surv[t], t + 1 < nsurv ? "," : ""); printf("}\n"); }
        fflush(stdout);
        if (nsurv == 0) break;
    }
    return 0;
}
