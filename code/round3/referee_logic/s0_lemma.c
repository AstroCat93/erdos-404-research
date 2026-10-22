/*
 * Round-3 logic referee: exact test of Lemma S0.1 (data/round3/reports/S0.md, Sec. 5).
 *
 * For y Haar-random in Z_2 and k >= 1, D(y,k) = s_2(k) - c(y,k), where c(y,k) is the
 * number of carries in the binary addition y + k.  E_n = {D(y,k) >= 0 for 1 <= k <= n}.
 * Lemma S0.1 claims, with m = floor(log2 n):
 *     (m+2)/2^(m+2) <= P(E_n) <= (m+2)/2^(m+1).
 *
 * Exact method (no sampling).  Write y = Y + 2^L H with 0 <= Y < 2^L, L > log2(nmax).
 * For k < 2^L the integer sum Z = Y + k determines all carries inside the window; if
 * Z >= 2^L a carry enters bit L and then runs through the t >= 0 trailing ones of H.
 * Hence D(y,k) = s(Z) - s(Y) - t*[Z >= 2^L], where t is the SAME for every k, and
 * P(t >= r) = 2^-r.  Given Y, E_n holds iff every "certain" k (Z < 2^L) has
 * s(Z) - s(Y) >= 0 and t <= d_n := min over "uncertain" k <= n of s(Z) - s(Y).
 * So P(E_n | Y) is 0, 1, or 1 - 2^-(d_n+1), and P(E_n) is an exact dyadic rational.
 *
 * Output: for every n <= nmax, the exact P(E_n) as num / 2^(L+DS), and checks of both
 * bounds; also the conjectured closed form (2m+3)/2^(m+2) at n = 2^m.
 *
 * Usage: s0_lemma LOG2NMAX      (e.g. 18)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 u128;

int main(int argc, char **argv) {
    int lg = argc > 1 ? atoi(argv[1]) : 16;
    if (lg < 1 || lg > 24) { fprintf(stderr, "LOG2NMAX in [1,24]\n"); return 1; }
    long nmax = 1L << lg;
    int L = lg + 2;                 /* window bits; k <= nmax < 2^L */
    int DS = L + 2;                 /* d <= L+1, so 2^(d+1) <= 2^DS */
    long NY = 1L << L;
    /* contribution of each Y, as a function of n, is piecewise constant:
       state -2 = dead (0), state -1 = certain alive (weight 2^DS),
       state d >= 0 : weight 2^DS - 2^(DS-d-1).  Accumulate via a difference array. */
    int64_t *diff = calloc(nmax + 2, sizeof(int64_t));
    if (!diff) { fprintf(stderr, "alloc\n"); return 1; }
    const int64_t FULL = (int64_t)1 << DS;
    for (long Y = 0; Y < NY; Y++) {
        int sY = __builtin_popcountl((unsigned long)Y);
        int64_t w = FULL;           /* current weight, valid from n = start */
        long start = 1;
        int d = 1 << 30;            /* min over uncertain k */
        for (long k = 1; k <= nmax; k++) {
            unsigned long Z = (unsigned long)Y + (unsigned long)k;
            int Dw = __builtin_popcountl(Z) - sY;
            int64_t nw = w;
            if (Z < (unsigned long)NY) {
                if (Dw < 0) nw = 0;
            } else {
                if (Dw < 0) nw = 0;
                else if (Dw < d) { d = Dw; nw = FULL - ((int64_t)1 << (DS - d - 1)); }
            }
            if (nw != w) {
                /* weight w on n in [start, k-1], new weight from n = k */
                diff[start] += w; diff[k] -= w;
                w = nw; start = k;
                if (w == 0) break;
            }
        }
        if (w != 0) { diff[start] += w; diff[nmax + 1] -= w; }
    }
    /* prefix sums: num[n] = sum_Y weight_Y(n);  P(E_n) = num / 2^(L+DS) */
    int64_t acc = 0;
    long viol_lo = 0, viol_hi = 0, nchecked = 0;
    double minratio_lo = 1e9, maxratio_hi = 0;
    printf("# s0_lemma: exact P(E_n) for 1<=n<=%ld, window L=%d bits, scale 2^%d\n", nmax, L, L + DS);
    printf("# n  m  P(E_n)  lower=(m+2)/2^(m+2)  upper=(m+2)/2^(m+1)  [at n=2^m also (2m+3)/2^(m+2)]\n");
    for (long n = 1; n <= nmax; n++) {
        acc += diff[n];
        int m = 63 - __builtin_clzl((unsigned long)n);
        /* compare acc/2^(L+DS) with (m+2)/2^(m+2) and (m+2)/2^(m+1), exactly */
        u128 lhs = (u128)acc << (m + 2);                 /* P * 2^(L+DS) * 2^(m+2) */
        u128 rlo = (u128)(m + 2) << (L + DS);            /* lower * 2^(L+DS) * 2^(m+2) */
        u128 rhi = (u128)(m + 2) << (L + DS + 1);        /* upper * ... */
        nchecked++;
        if (lhs < rlo) viol_lo++;
        if (lhs > rhi) viol_hi++;
        double P = (double)acc / (double)((u128)1 << (L + DS));
        double lo = (double)(m + 2) / (double)(1UL << (m + 2));
        double hi = 2 * lo;
        if (P / lo < minratio_lo) minratio_lo = P / lo;
        if (P / hi > maxratio_hi) maxratio_hi = P / hi;
        int pow2 = (n & (n - 1)) == 0;
        if (pow2 || n <= 16 || n == nmax) {
            int conj = 0;
            if (pow2) { u128 rc = (u128)(2 * m + 3) << (L + DS); conj = (lhs == rc); }
            printf("%ld %d %.10f %.10f %.10f%s\n", n, m, P, lo, hi,
                   pow2 ? (conj ? "  conj(2m+3)/2^(m+2): EXACT" : "  conj(2m+3)/2^(m+2): differs") : "");
        }
    }
    printf("# checked %ld values of n; lower-bound violations %ld; upper-bound violations %ld\n",
           nchecked, viol_lo, viol_hi);
    printf("# min P/lower = %.6f ; max P/upper = %.6f\n", minratio_lo, maxratio_hi);
    free(diff);
    return 0;
}
