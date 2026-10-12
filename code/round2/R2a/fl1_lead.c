/* fl1_lead.c -- lead author's independent re-implementation (2026-10-12) of the Fourier L1
 * shell sums of note_v2.md Section 10.4:
 *
 *   T_p(k) = sum_{u in (Z/p^k)^x} prod_{n >= N0} |cos(pi u n! / (p^{e0} p^k))|,  e0 = v_p(N0!).
 *
 * Shares no code with fl1.c.  Differences: (i) elements are x_n = n!/p^{e0} reduced mod p^k
 * directly (not unit parts), (ii) frequencies are enumerated by full p-adic odometer recursion
 * on the LEAST significant digit first but with every factor evaluated only at the leaf (no
 * prefix products), (iii) the cosine is evaluated with __cospi (macOS libm), (iv) summation is
 * a balanced tree (per-digit subtotals), whose relative rounding error is <= K*p*2^-52.
 * Outward margin: each factor is replaced by min(1, __cospi(q) + 1e-12); the final sum is
 * multiplied by (1 + 1e-10).  This is floating point with explicit margins, not interval
 * arithmetic.
 *
 * usage: fl1_lead p N0 kmax
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

extern double __cospi(double);
typedef unsigned __int128 u128;

static int P, N0, KMAX, K;
static uint64_t MOD;            /* p^K */
static uint64_t X[4096];        /* x_n mod p^KMAX for n with l_n < K */
static int LV[4096], NX;

static double leaf(uint64_t u) {
  double prod = 1.0;
  for (int i = 0; i < NX; i++) {
    if (LV[i] >= K) continue;
    uint64_t r = (uint64_t)(((u128)u * (X[i] % MOD)) % MOD);   /* u x_n mod p^K */
    uint64_t rr = r > MOD - r ? MOD - r : r;                  /* distance to 0 mod p^K */
    double q = (double)rr / (double)MOD;                      /* in [0, 1/2] */
    double c = __cospi(q) + 1e-12;
    if (c > 1.0) c = 1.0;
    prod *= c;
  }
  return prod;
}

/* sum over u = u0 + p^d * (digits d..K-1), u0 fixed mod p^d; returns tree-summed subtotal */
static double rec(int d, uint64_t u0, uint64_t pd) {
  if (d == K) return leaf(u0);
  double s = 0.0;
  for (int t = (d == 0 ? 1 : 0); t < P; t++) s += rec(d + 1, u0 + (uint64_t)t * pd, pd * P);
  return s;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: fl1_lead p N0 kmax\n"); return 1; }
  P = atoi(argv[1]); N0 = atoi(argv[2]); KMAX = atoi(argv[3]);
  uint64_t BIG = 1; for (int i = 0; i < KMAX; i++) BIG *= (uint64_t)P;
  /* x_n = n!/p^{e0} mod p^KMAX, l_n = v(n!) - e0, for n >= N0 while l_n < KMAX */
  int e0 = 0; for (int k = 1; k <= N0; k++) { int m = k; while (m % P == 0) { m /= P; e0++; } }
  /* compute n!/p^{v(n!)} * p^{v(n!)-e0} incrementally: keep unit part and level */
  uint64_t unit = 1; int lev = 0;
  for (int k = 1; k <= N0; k++) { int m = k; while (m % P == 0) m /= P; unit = (uint64_t)(((u128)unit * (uint64_t)m) % BIG); }
  NX = 0;
  for (int n = N0; lev < KMAX; ) {
    uint64_t pw = 1; for (int i = 0; i < lev; i++) pw *= (uint64_t)P;
    X[NX] = (uint64_t)(((u128)unit * pw) % BIG); LV[NX] = lev; NX++;
    n++; int m = n; while (m % P == 0) { m /= P; lev++; }
    unit = (uint64_t)(((u128)unit * (uint64_t)m) % BIG);
  }
  printf("# fl1_lead p=%d N0=%d e0=%d elements=%d margin=1e-12 per factor, x(1+1e-10)\n", P, N0, e0, NX);
  double cum = 0.0;
  for (K = 1; K <= KMAX; K++) {
    MOD = 1; for (int i = 0; i < K; i++) MOD *= (uint64_t)P;
    double T = rec(0, 0, 1) * (1.0 + 1e-10);
    cum += T;
    printf("k=%2d T_upper=%.7e cum_upper=%.7e\n", K, T, cum);
    fflush(stdout);
  }
  return 0;
}
