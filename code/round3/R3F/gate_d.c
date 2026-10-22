/* gate_d.c -- rigorous UPPER bound for the level-d L^1 shell of a single gate block (round 3, R3F, target (a)).
 *
 *   S_d = sum_{u in (Z/p^d)^x} prod_{i<p} |cos(pi u sigma_i / p^d)|,   sigma_i = (-1)^i (p-1)!/(p-1-i)!
 *
 * Independent of ivshell.c (fresh code).  Method: u runs over 1..(M-1)/2 (M = p^d), u and M-u give equal
 * products, so the total is twice the half sum.  Residues r_i = u sigma_i mod M are updated incrementally
 * (r_i += sigma_i mod M).  sigma_{p-1} = -sigma_{p-2}, so their two factors are one factor squared.
 * Rigour: FE_UPWARD throughout; rho = min(r, M-r) <= M/2;  q_lo = dn(rho * dn(1/M)) <= rho/M,
 * x_lo = dn(q_lo * PI_LO) <= pi rho/M <= pi/2;  cos(pi rho/M) <= cos(x_lo) <= S_6(x_lo), where
 * S_6(x) = sum_{j<=6} (-1)^j x^{2j}/(2j)! (alternating series with decreasing terms for x <= 1.58, ending with a
 * + term, so S_6 >= cos).  Even terms rounded up, odd terms rounded down then subtracted (upward mode).
 * Products and sums of nonnegative upper bounds rounded up.  Non-units u (p | u) are skipped.
 * usage: gate_d p d       (prints the upper bound of S_d and of S_d / (N_d (2/pi)^p), N_d = p^d - p^{d-1})
 * build: gcc -O2 -frounding-math -fno-fast-math -o gate_d gate_d.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <fenv.h>

static inline double dn_mul(double a, double b) { return -((-a) * b); }

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: gate_d p d\n"); return 1; }
  int p = atoi(argv[1]), d = atoi(argv[2]);
  if (fesetround(FE_UPWARD) != 0) return 2;
  double PI_LO, PI_HI; { uint64_t a = 0x400921FB54442D18ULL, b = 0x400921FB54442D19ULL; memcpy(&PI_LO, &a, 8); memcpy(&PI_HI, &b, 8); }
  { volatile double o = 1.0, t = 3.0; if (!(o / t > -((-o) / t))) { fprintf(stderr, "rounding self-test failed\n"); return 2; } }
  uint64_t M = 1; for (int i = 0; i < d; i++) M *= (uint64_t)p;
  if ((double)M > 4.0e15) return 1;
  /* sigma_i mod M, i = 0..p-1 ; we use i = 0..p-2 with the last two merged (sigma_{p-1} = -sigma_{p-2}) */
  uint64_t sg[64]; int ns = p - 1;
  { unsigned __int128 f = 1; for (int j = 1; j < p; j++) f *= j;           /* (p-1)! */
    for (int i = 0; i < p; i++) {
      unsigned __int128 q = 1; for (int j = 1; j <= p - 1 - i; j++) q *= j;   /* (p-1-i)! */
      unsigned __int128 v = f / q; uint64_t r = (uint64_t)(v % M);
      if (i & 1) r = (M - r) % M;
      if (i < p) sg[i] = r;
    }
    if ((sg[p - 1] + sg[p - 2]) % M != 0) { fprintf(stderr, "sigma check failed\n"); return 3; }
  }
  volatile double Md = (double)M, one = 1.0;
  double invM_lo = -((-one) / Md);
  double c[8]; for (int j = 1; j <= 7; j++) { volatile double den = (double)((2 * j - 1) * (2 * j)); c[j] = 1.0 / den; }
  double cd[8]; for (int j = 1; j <= 7; j++) { volatile double den = (double)((2 * j - 1) * (2 * j)); cd[j] = -((-1.0) / den); }
  uint64_t r[64]; for (int i = 0; i < ns; i++) r[i] = 0;
  double S = 0.0; uint64_t cnt = 0;
  double Sblk = 0.0; uint64_t blk = 0;
  uint64_t half = (M - 1) / 2;
  for (uint64_t u = 1; u <= half; u++) {
    for (int i = 0; i < ns; i++) { r[i] += sg[i]; if (r[i] >= M) r[i] -= M; }
    if (u % (uint64_t)p == 0) continue;
    double pr = 1.0;
    for (int i = 0; i < ns; i++) {
      uint64_t rr = r[i]; if (rr > M - rr) rr = M - rr;
      double f;
      if (rr == 0) f = 1.0;
      else {
        double ql = dn_mul((double)rr, invM_lo);
        double x = dn_mul(ql, PI_LO);           /* x <= pi rr / M, exact double, x >= 0 */
        double yu = x * x, yd = dn_mul(x, x);
        double tu = 1.0, td = 1.0, s = 1.0;
        for (int j = 1; j <= 6; j++) {
          tu = (tu * yu) * c[j];
          td = dn_mul(dn_mul(td, yd), cd[j]);
          if (j & 1) s = s + (-td); else s = s + tu;
        }
        f = s > 1.0 ? 1.0 : s;
      }
      if (i == p - 2) f = f * f;              /* merged factor sigma_{p-2}, sigma_{p-1} */
      pr = pr * f;
    }
    Sblk = Sblk + pr; cnt++;
    if (++blk == 1000000) { S = S + Sblk; Sblk = 0.0; blk = 0; }
  }
  S = S + Sblk;
  double T = 2.0 * S;
  double N = (double)M - (double)(M / p);
  double rm = pow(2.0 / PI_HI, p);   /* lower bound of (2/pi)^p in upward mode? 2/PI_HI <= 2/pi; pow rounding: ratio below is informative */
  printf("p=%d d=%d M=%llu units/2=%llu  S_d_upper=%.12e  ratio S_d/(N_d (2/pi)^p) ~ %.8f\n", p, d,
         (unsigned long long)M, (unsigned long long)cnt, T, T / (N * rm));
  return 0;
}
