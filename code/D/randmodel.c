// "Random-bits" branching model for p = 2 (HEURISTIC, not a proof).
// For a random 2-adic alpha, the environment is t_b = v_2(alpha + b + 1).  In the c-recursion each
// particle has: 2 children if t_b = 0; exactly 1 child if t_b = 1; and, if t_b >= 2, one child with
// probability 2^{1-t_b} (this is the model assumption: the low bits of c are uniformly random).
// First step (b = 0): forced eps = 1 -> exactly 1 child (alpha even).  Final partial gate with
// r remaining bits: survive with probability 2^{1-r}.
// Computes the model prediction of d_k = P(g >= k) averaged over random alpha, for k <= KMAX.
// Usage: randmodel nsamples seed KMAX
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 s[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 next(void) { const u64 result = rotl(s[1] * 5, 7) * 9; const u64 t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return result; }
static inline int ctz128(u128 x) { u64 lo = (u64)x; if (lo) return __builtin_ctzll(lo); return 64 + __builtin_ctzll((u64)(x >> 64)); }

int main(int argc, char **argv) {
    long ns = atol(argv[1]); u64 seed = strtoull(argv[2], 0, 10); int KMAX = atoi(argv[3]);
    s[0] = seed * 0x9E3779B97F4A7C15ULL + 1; s[1] = seed ^ 0xDEADBEEFULL; s[2] = 12345 + seed; s[3] = 0xABCDEF ^ (seed << 7);
    for (int i = 0; i < 20; i++) next();
    double *acc = calloc(KMAX + 2, sizeof(double));
    int tb[4096];
    for (long it = 0; it < ns; it++) {
        u128 a = (((u128)next() << 64) | next()) & ((((u128)1) << 126) - 1);
        if (a & 1) { acc[0] += 1.0; continue; } // odd alpha: g = 0
        // environment
        int L = 0; int V = 0;
        while (V < KMAX + 1 && L < 4000) { int t = ctz128(a + (u128)L + 1); tb[L++] = t; V += t; }
        // for each k in 1..KMAX: find b* = first stage with V_{b*} + t_{b*} >= k
        acc[0] += 1.0;
        int Vb = 0, b = 0;
        for (int k = 1; k <= KMAX; k++) {
            while (Vb + tb[b] < k) { Vb += tb[b]; b++; }
            int r = k - Vb; // remaining bits at final gate b (t_b >= r >= 1)
            // extinction prob: compose f_0 o f_1 o ... o f_{b-1} o f_final (0)
            double qf = (r >= 1) ? ldexp(1.0, 1 - r) : 1.0; if (qf > 1) qf = 1;
            double sv = 1.0 - qf;               // P(extinct) for one particle at final gate
            if (b == 0) { // final gate is the very first step: forced eps=1, c+1 = 1 odd -> dies (alpha even so t_0=0, cannot happen)
                acc[k] += 0.0; continue; }
            for (int i = b - 1; i >= 0; i--) {
                int t = tb[i];
                if (i == 0) { /* forced single child */ }
                else if (t == 0) sv = sv * sv;
                else if (t == 1) { }
                else { double q = ldexp(1.0, 1 - t); sv = 1.0 - q + q * sv; }
            }
            acc[k] += 1.0 - sv;
        }
    }
    for (int k = 0; k <= KMAX; k++) printf("k=%d model_d=%.6f\n", k, acc[k] / ns);
    return 0;
}
