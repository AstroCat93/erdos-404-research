/* jrel.c -- rigorous enclosure of the gate-block limit constant
 *
 *   J_p = (pi/2)^p * \int_0^1 prod_{u=0}^{p-1} |cos(pi theta (p-1)!/u!)| d theta
 *       = sum_{k in Z^p : sum_u k_u (p-1)!/u! = 0}  prod_u b_{k_u},     b_k = (-1)^{k+1}/(4k^2-1)
 *
 * (round 3, track R3F; see the report, section (a)/(d)).  The constraint is resolved by the carry
 * recursion (Fourier dual of the factorial-base transfer operator): with P_u = (p-1)!/u!,
 *   start s = 0 ("carry"), for m = p-1, p-2, ..., 2:  choose k_m = s - m s'  (any s' in Z), s <- s';
 *   finally k_1 + k_0 = s, whose weight is (b*b)(s) = pi^2/8 (s=0), pi^2/16 (s=+-1), 0 otherwise.
 * Forward vectors: v_{p-1} = delta_0,  v_{m-1}(s') = sum_s v_m(s) b_{s - m s'};  J = sum_s v_1(s) (b*b)(s).
 *
 * Truncation |s| <= C at every step.  The neglected paths are those whose carry first leaves [-C,C] at
 * some step m; their total contribution is bounded by
 *   E_trunc <= sum_m beta_{m-1} * ||v_m^T||_1 * (2/3) / (m (m-1) C),
 * where beta_1 = pi^2/8, beta_m = kappa_m beta_{m-1}, kappa_m = 2 - (pi/2m) cot(pi/2m) = max over residue
 * classes r mod m of sum_{k = r mod m} |b_k|, and for |s|<=C: sum_{|s'|>C} |b_{s - m s'}| <= (2/3)/(m(m-1)C).
 * (beta_{m} bounds sup_s |completion weight from carry s before processing m|; see report.)
 *
 * Arithmetic: mid-radius.  For each new entry, mid = fl(sum v_mid * b_mid) in round-to-nearest;
 * radius (computed in FE_UPWARD) = sum (|v_mid| |b - b_mid| + v_rad (|b_mid| + |b-b_mid|)) + gamma_{n} sum|v_mid b_mid|,
 * gamma_n = n u/(1-n u), u = 2^-53, with |b - b_mid| <= 2u |b_mid|.  The constants pi^2/8 etc. are enclosed
 * with PI_LO < pi < PI_HI.  kappa_m is bounded above by its series definition evaluated in upward mode
 * (we use kappa_m <= 1 + 2 sum_{i>=1} 1/(4 m^2 i^2 - 1) <= 1 + 2/(4m^2-1) + 1/(2 m^2) ... see code).
 *
 * usage: jrel p C
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fenv.h>
#include <string.h>
#include <stdint.h>

static double PI_LO, PI_HI;

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: jrel p C\n"); return 1; }
  int p = atoi(argv[1]); long C = atol(argv[2]);
  { uint64_t a = 0x400921FB54442D18ULL, b = 0x400921FB54442D19ULL; memcpy(&PI_LO, &a, 8); memcpy(&PI_HI, &b, 8); }
  long W = 2 * C + 1;
  double *vm = calloc(W, sizeof(double)), *vr = calloc(W, sizeof(double));
  double *nm = calloc(W, sizeof(double)), *nr = calloc(W, sizeof(double));
  if (!vm || !vr || !nm || !nr) return 1;
  vm[C] = 1.0; vr[C] = 0.0;           /* v_{p-1} = delta_0 */
  const double u = 1.0 / 9007199254740992.0;   /* 2^-53 */
  double Etr = 0.0;                    /* truncation error bound (upward) */
  /* beta_{m-1} bound needs kappa's: beta_1 = pi^2/8; beta_j = kappa_j beta_{j-1} */
  double beta[256]; fesetround(FE_UPWARD);
  beta[1] = PI_HI * PI_HI / 8.0;
  for (int j = 2; j < p && j < 255; j++) {
    /* kappa_j = 1 + 2 sum_{i>=1} 1/(4 j^2 i^2 - 1) <= 1 + 2/(4j^2-1) + 2 int_1^inf dx/(3 j^2 x^2)
       = 1 + 2/(4j^2-1) + 2/(3j^2)   (4j^2x^2-1 >= 3j^2x^2 for x>=1).  Class 0 is the largest class. */
    double a = 4.0 * j * j;
    double k = 1.0 + 2.0 / (a - 1.0) + 2.0 / (3.0 * j * j);
    beta[j] = k * beta[j - 1];
  }
  fesetround(FE_TONEAREST);
  for (int m = p - 1; m >= 2; m--) {
    /* ||v_m^T||_1 upper bound */
    fesetround(FE_UPWARD);
    double l1 = 0; for (long i = 0; i < W; i++) l1 += fabs(vm[i]) + vr[i];
    Etr += beta[m - 1] * l1 * (2.0 / 3.0) / ((double)m * (double)(m - 1) * (double)C);
    fesetround(FE_TONEAREST);
    for (long j = 0; j < W; j++) {
      long sp = j - C;   /* s' */
      double S = 0.0;
      for (long i = 0; i < W; i++) {
        if (vm[i] == 0.0 && vr[i] == 0.0) continue;
        long s = i - C; long k = s - (long)m * sp;
        double den = 4.0 * (double)k * (double)k - 1.0;      /* exact (< 2^53) */
        double b = ((k & 1) ? 1.0 : -1.0) / den;               /* (-1)^{k+1}/(4k^2-1), one rounding */
        S += vm[i] * b;
      }
      nm[j] = S;
    }
    fesetround(FE_UPWARD);
    for (long j = 0; j < W; j++) {
      long sp = j - C; double A = 0.0, R = 0.0; long n = 0;
      for (long i = 0; i < W; i++) {
        if (vm[i] == 0.0 && vr[i] == 0.0) continue;
        long s = i - C; long k = s - (long)m * sp;
        double den = 4.0 * (double)k * (double)k - 1.0;
        double ab = 1.0 / fabs(den);        /* >= |b_mid| (upward); den = -1 when k = 0 */
        double br = 2.0 * u * ab;           /* >= |b - b_mid| */
        A += fabs(vm[i]) * ab;
        R += fabs(vm[i]) * br + vr[i] * (ab + br);
        n++;
      }
      double nu = (double)(n + 1) * u; double gam = nu / (1.0 - nu);
      nr[j] = R + gam * A;
    }
    fesetround(FE_TONEAREST);
    double *t; t = vm; vm = nm; nm = t; t = vr; vr = nr; nr = t;
  }
  /* J = (pi^2/8) v(0) + (pi^2/16)(v(1) + v(-1)) */
  double c0 = vm[C], r0 = vr[C], c1 = vm[C + 1] + vm[C - 1];
  fesetround(FE_UPWARD);
  double r1 = vr[C + 1] + vr[C - 1] + 2 * u * (fabs(vm[C + 1]) + fabs(vm[C - 1]));
  double pi2h = PI_HI * PI_HI, pi2l = -((-PI_LO) * PI_LO);
  /* enclosure of J_T = pi^2/8 * c0 + pi^2/16 * c1 with c0 in [c0-r0, c0+r0], c1 in [c1-r1,c1+r1] */
  double c0l = -((-c0) + r0), c0h = c0 + r0, c1l = -((-c1) + r1), c1h = c1 + r1;
  /* interval product [pl,ph]*[x,y] with 0 < pl <= ph, rounded outward (we are in FE_UPWARD) */
  #define IVMUL_LO(pl, ph, x) ((x) >= 0 ? -((-(pl)) * (x)) : -((-(ph)) * (x)))
  #define IVMUL_HI(pl, ph, y) ((y) >= 0 ? (ph) * (y) : (pl) * (y))
  double q8l = -((-pi2l) / 8.0), q8h = pi2h / 8.0, q16l = -((-pi2l) / 16.0), q16h = pi2h / 16.0;
  double a1 = IVMUL_LO(q8l, q8h, c0l), a2 = IVMUL_LO(q16l, q16h, c1l);
  double b1 = IVMUL_HI(q8l, q8h, c0h), b2 = IVMUL_HI(q16l, q16h, c1h);
  double Jl = -((-a1) + (-a2)), Jh = b1 + b2;
  printf("# v1(0) = %.15f +- %.2e ; v1(1)+v1(-1) = %.15f +- %.2e\n", c0, r0, c1, r1);
  double JlT = -((-Jl) + Etr), JhT = Jh + Etr;
  printf("p=%d C=%ld  J_trunc in [%.12f, %.12f]  trunc_err<=%.3e  =>  J_p in [%.10f, %.10f]   (2/pi)^p*J_p upper=%.6e\n",
         p, C, Jl, Jh, Etr, JlT, JhT, JhT * pow(2.0 / PI_LO, p));
  return 0;
}
