/* rho.c -- per-block "sup over cosets" constants.
 * For block m (n = pm..pm+p-1) and order p^j:
 *   rho(m,j) = max_{a mod p^{j-1}} sum_{t mod p} prod_{n in block} |cos(pi ((a+t p^{j-1}) U_n mod p^j)/p^j)|
 * where for j=1 the coset is all of Z/p minus 0 (a=0, t != 0).
 * Also prints the mean coset sum (= p * average |phi|) for comparison.
 * usage: rho p m_lo m_hi jmax
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef unsigned __int128 u128;
int main(int argc, char **argv) {
  int p = atoi(argv[1]), mlo = atoi(argv[2]), mhi = atoi(argv[3]), jmax = atoi(argv[4]);
  uint64_t BIG = 1; for (int i = 0; i < jmax; i++) BIG *= p;
  /* unit part of (p*mlo)! mod BIG */
  uint64_t cur = 1; int n;
  for (n = 1; n <= p * mlo; n++) { int m = n; while (m % p == 0) m /= p; cur = (uint64_t)(((u128)cur * m) % BIG); }
  for (int m = mlo; m <= mhi; m++) {
    uint64_t U[64];
    U[0] = cur;
    for (int r = 1; r < p; r++) { int nn = p * m + r; int q = nn; while (q % p == 0) q /= p; U[r] = (uint64_t)(((u128)U[r - 1] * q) % BIG); }
    /* advance cur to unit part of (p(m+1))! */
    { int nn = p * (m + 1); int q = nn; while (q % p == 0) q /= p; cur = (uint64_t)(((u128)U[p - 1] * q) % BIG); }
    printf("m=%d:", m);
    uint64_t M = 1;
    for (int j = 1; j <= jmax; j++) {
      M *= p; uint64_t Mp = M / p;
      double best = 0, mean = 0; uint64_t cnt = 0;
      uint64_t alo = (j == 1) ? 0 : 1;
      for (uint64_t a = alo; a < (j == 1 ? 1 : Mp); a++) {
        if (j > 1 && a % p == 0) continue;   /* need exact order p^j: a unit */
        double s = 0;
        for (int t = 0; t < p; t++) {
          uint64_t v = a + (uint64_t)t * Mp;
          if (v == 0) continue;
          double pr = 1;
          for (int r = 0; r < p; r++) {
            uint64_t x = (uint64_t)(((u128)v * (U[r] % M)) % M);
            pr *= fabs(cos(M_PI * (double)x / (double)M));
          }
          s += pr;
        }
        if (s > best) best = s;
        mean += s; cnt++;
      }
      printf("  j=%d rho=%.4f mean=%.2e", j, best, mean / cnt);
    }
    printf("\n"); fflush(stdout);
  }
  return 0;
}
