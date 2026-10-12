/* knuth.c -- HEURISTIC (Monte Carlo) estimates of the Fourier L1 shell sums T(k)
 * for the uniform factorial Bernoulli convolution from N0, via Knuth's unbiased
 * tree-size estimator with importance sampling (child chosen with prob. proportional
 * to its factor; estimator = product of the local child-sums along the path).
 * NOT a proof.  Requires p^kmax < 2^63.
 * usage: knuth p N0 kmin kmax samples seed
 * prints k, mean estimate, std error, relative std error, max single estimate.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
static uint64_t rng = 88172645463325252ULL;
static inline uint64_t xs(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static inline double unif(void) { return (xs() >> 11) * (1.0 / 9007199254740992.0); }
int main(int argc, char **argv) {
  int p = atoi(argv[1]), N0 = atoi(argv[2]), kmin = atoi(argv[3]), kmax = atoi(argv[4]);
  long S = atol(argv[5]); rng ^= (uint64_t)atol(argv[6]) * 0x9E3779B97F4A7C15ULL;
  uint64_t PW[64]; PW[0] = 1; for (int i = 1; i <= kmax; i++) PW[i] = PW[i - 1] * p;
  uint64_t BIG = PW[kmax];
  static uint64_t UB[4096]; static int LB[4096]; int cnt = 0;
  uint64_t cur = 1; for (int k = 1; k <= N0; k++) { int m = k; while (m % p == 0) m /= p; cur = (uint64_t)(((u128)cur * m) % BIG); }
  int l = 0, n = N0;
  while (l < kmax) { UB[cnt] = cur; LB[cnt] = l; cnt++; n++; int m = n; while (m % p == 0) { m /= p; l++; } cur = (uint64_t)(((u128)cur * m) % BIG); }
  printf("# knuth p=%d N0=%d samples=%ld (HEURISTIC)\n# k mean stderr rel maxest\n", p, N0, S);
  for (int K = kmin; K <= kmax; K++) {
    /* lists per depth */
    static int st[70], ct[70]; static uint64_t LI[4096]; int pos = 0;
    for (int d = 1; d <= K; d++) { st[d] = pos; ct[d] = 0; for (int i = 0; i < cnt; i++) if (LB[i] == K - d) { LI[pos++] = UB[i] % PW[d]; ct[d]++; } }
    double sum = 0, sum2 = 0, mx = 0;
    for (long s = 0; s < S; s++) {
      uint64_t u = 0; double est = 1;
      for (int d = 0; d < K; d++) {
        double w[64]; double tot = 0; uint64_t M = PW[d + 1];
        for (int t = 0; t < p; t++) {
          if (d == 0 && t == 0) { w[t] = 0; continue; }
          uint64_t v = u + (uint64_t)t * PW[d]; double pr = 1;
          for (int i = 0; i < ct[d + 1]; i++) { uint64_t r = (uint64_t)(((u128)v * LI[st[d + 1] + i]) % M); pr *= fabs(cos(M_PI * (double)r / (double)M)); }
          w[t] = pr; tot += pr;
        }
        est *= tot; if (tot <= 0) { est = 0; break; }
        double x = unif() * tot; int t = 0; while (t < p - 1 && x >= w[t]) { x -= w[t]; t++; }
        while (w[t] == 0 && t < p - 1) t++;
        u += (uint64_t)t * PW[d];
      }
      sum += est; sum2 += est * est; if (est > mx) mx = est;
    }
    double mean = sum / S, var = sum2 / S - mean * mean; double se = sqrt(var > 0 ? var / S : 0);
    printf("%2d %.4e %.2e %.3f %.3e\n", K, mean, se, mean > 0 ? se / mean : 0, mx); fflush(stdout);
  }
  return 0;
}
