// Exact decision "is 2^K | sum of distinct factorials with minimum a ?" (p = 2), sum form,
// multi-limb.  Independent of the c-recursion code: only additions, shifts and multiplication
// of the odd part of N! by small integers.
// State at stage N: T = S_N / 2^{v_2(N!)} mod 2^R, R = K - v_2(N!), S_N = sum_{n in A, n<N} n!.
// Usage: sumform_big a K
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static int W;           // limbs
static long PMAX = 1L << 17;

static void add_mod(u64 *dst, const u64 *x, const u64 *y, int R) { // dst = x + y mod 2^R
    int L = (R + 63) / 64; u64 c = 0;
    for (int i = 0; i < L; i++) { u64 s1 = x[i] + y[i]; u64 c1 = (s1 < x[i]); u64 s2 = s1 + c; u64 c2 = (s2 < s1); dst[i] = s2; c = c1 | c2; }
    if (R % 64) dst[L - 1] &= ((1ULL << (R % 64)) - 1);
    for (int i = L; i < W; i++) dst[i] = 0;
}
static int low_zero(const u64 *x, int t) { // low t bits zero?
    int q = t / 64, r = t % 64;
    for (int i = 0; i < q; i++) if (x[i]) return 0;
    if (r && (x[q] & ((1ULL << r) - 1))) return 0;
    return 1;
}
static void shr(u64 *x, int t, int R) { // x >>= t (x < 2^R)
    int q = t / 64, r = t % 64; int L = (R + 63) / 64;
    for (int i = 0; i < L; i++) {
        u64 lo = (i + q < W) ? x[i + q] >> r : 0;
        u64 hi = (r && i + q + 1 < W) ? x[i + q + 1] << (64 - r) : 0;
        x[i] = lo | hi;
    }
    for (int i = L; i < W; i++) x[i] = 0;
}
static void mul_small(u64 *x, u64 m, int R) { int L = (R + 63) / 64; u64 c = 0;
    for (int i = 0; i < L; i++) { u128 s = (u128)x[i] * m + c; x[i] = (u64)s; c = (u64)(s >> 64); }
    if (R % 64) x[L - 1] &= ((1ULL << (R % 64)) - 1);
}
static u64 hashv(const u64 *x, int L) { u64 h = 1469598103934665603ULL; for (int i = 0; i < L; i++) { h ^= x[i]; h *= 1099511628211ULL; h ^= h >> 29; } return h; }

int main(int argc, char **argv) {
    long a = atol(argv[1]); int K = atoi(argv[2]);
    W = (K + 63) / 64 + 1;
    // F = odd part of a! mod 2^K ; v = v_2(a!)
    u64 *F = calloc(W, 8); F[0] = 1; int v = 0;
    for (long n = 2; n <= a; n++) { long m = n; while (!(m & 1)) { m >>= 1; v++; } mul_small(F, (u64)m, K); }
    int R = K - v;
    if (R <= 0) { printf("trivially reachable\n"); return 0; }
    u64 *pop = calloc((size_t)PMAX * W, 8), *nw = calloc((size_t)PMAX * W, 8);
    long HS = 1L << 19; long *hidx = malloc(sizeof(long) * HS); u64 *hval = malloc(sizeof(u64) * HS);
    long np = 1; memset(pop, 0, (size_t)W * 8); // T = 0
    long N = a; long maxp = 1;
    u64 *cand = calloc(W, 8);
    while (1) {
        long n1 = N + 1; int t = __builtin_ctzl(n1); long u = n1 >> t;
        // candidates T (if N != a) and T + F
        long nn = 0; for (long i = 0; i < HS; i++) hidx[i] = -1;
        int Rn = R - t;
        for (long i = 0; i < np; i++) {
            for (int e = (N == a) ? 1 : 0; e <= 1; e++) {
                if (e) add_mod(cand, pop + i * W, F, R); else memcpy(cand, pop + i * W, (size_t)W * 8);
                if (Rn <= 0) { // final: need cand == 0 mod 2^R
                    if (low_zero(cand, R)) { printf("a=%ld K=%d reachable=1 (final stage N=%ld, maxpop=%ld)\n", a, K, N, maxp); return 0; }
                    continue;
                }
                if (!low_zero(cand, t)) continue;
                shr(cand, t, R);
                int L = (Rn + 63) / 64; u64 h = hashv(cand, L); long pos = h & (HS - 1); int dup = 0;
                while (hidx[pos] >= 0) { if (hval[pos] == h && !memcmp(nw + hidx[pos] * W, cand, (size_t)L * 8)) { dup = 1; break; } pos = (pos + 1) & (HS - 1); }
                if (dup) continue;
                if (nn >= PMAX) { printf("population overflow at N=%ld\n", N); return 2; }
                memcpy(nw + nn * W, cand, (size_t)W * 8); hidx[pos] = nn; hval[pos] = h; nn++;
            }
        }
        if (Rn <= 0) { printf("a=%ld K=%d reachable=0 (died at final gate N+1=%ld, maxpop=%ld)\n", a, K, n1, maxp); return 0; }
        if (nn == 0) { printf("a=%ld K=%d reachable=0 (population died at N+1=%ld, maxpop=%ld)\n", a, K, n1, maxp); return 0; }
        if (nn > maxp) maxp = nn;
        u64 *tmp = pop; pop = nw; nw = tmp; np = nn; R = Rn;
        // F <- F * u  (odd part of (N+1)!)
        mul_small(F, (u64)u, K);
        N++;
    }
}
