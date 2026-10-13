/* ivshell.c -- rigorous interval enclosures of Fourier shell sums (round 3, track R3F).
 *
 * For a finite list of elements x_i = p^{l_i} U_i (U_i an integer residue, l_i >= 0) put, for k >= 1,
 *   T1(k) = sum_{u in (Z/p^k)^x} prod_{i: l_i < k} |cos(pi u x_i / p^k)|      (L^1 shell)
 *   T2(k) = sum_{u in (Z/p^k)^x} prod_{i: l_i < k}  cos^2(pi u x_i / p^k)     (L^2 shell)
 * (elements with l_i >= k contribute the factor 1).  The program prints, for each k, an enclosure
 * [lo, hi] of T1(k) and of T2(k), and the cumulative enclosures.
 *
 * Element sources:
 *   mode "fact" p N0 kmax :  x_n = n!/p^{e0}, n >= N0, e0 = v_p(N0!)   (the tail measure of note §10.4)
 *   mode "file" p kmax FILE: lines "U l" (U a nonnegative integer < 2^63, l >= 0)
 *
 * Rigour.  The program runs entirely in the FE_UPWARD rounding mode (checked at start-up by a
 * self-test).  Downward-rounded operations are written as negations of upward ones:
 * dn(a*b) = -up((-a)*b), dn(a/b) = -up((-a)/b), dn(a+b) = -up((-a)+(-b)).
 * For 0 <= r <= M/2 (M = p^k < 2^53, so r and M are exact doubles):
 *   q_lo <= r/M <= q_hi,  x_lo = dn(q_lo*PI_LO) <= pi r/M <= x_hi = up(q_hi*PI_HI),
 * where PI_LO = 0x400921FB54442D18 < pi < PI_HI = 0x400921FB54442D19.
 * cos is decreasing on [0, pi/2]; on 0 <= x <= 1.58 the terms t_j = x^{2j}/(2j)! decrease for j >= 1,
 * so by the alternating-series bound  S_{10}(x) >= cos x >= S_{11}(x), S_J = sum_{j<=J} (-1)^j t_j.
 * Upper bound: S_10(x_lo) with even terms rounded up and odd terms rounded down (then subtracted
 * in upward mode).  Lower bound: S_11(x_hi) with even terms rounded down and odd terms rounded up,
 * accumulated in downward mode.  Then hi = min(1, .), lo = max(0, .).
 * Products of nonnegative upper (lower) bounds are rounded up (down); sums likewise.
 * |cos| is even, so u and -u give the same product: only u with lowest digit in [1,(p-1)/2] are
 * enumerated and the totals are doubled (exact).
 * Enumeration: depth-first over the p-adic digits of u (lowest first); an element of level l is
 * evaluated at depth k-l, where its phase u U_i / p^{k-l} depends on u mod p^{k-l} only.  No pruning.
 *
 * usage:  ivshell fact p N0 kmax      |   ivshell file p kmax FILE [kmin t0lo t0hi]
 *         (optional: only shells kmin..kmax and only lowest digits u_0 in [t0lo,t0hi]; the partial sums of
 *          the chunks t0 = 1..(p-1)/2 add up to the full shell)
 * build:  gcc -O2 -frounding-math -fno-fast-math -o ivshell ivshell.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <fenv.h>

typedef unsigned __int128 u128;
#define MAXE 20000
#define MAXK 40

static int P, KMAX;
static int KMIN = 1, T0LO = 1, T0HI = 1 << 30;   /* optional restriction (file mode): shells KMIN..KMAX, lowest digit in [T0LO,T0HI] */
static uint64_t UE[MAXE]; static int LE[MAXE]; static int NE;
static uint64_t PW[MAXK + 2];
static int K;
static int lvstart[MAXK + 2], lvcnt[MAXK + 2];
static uint64_t LIST[MAXE];

static double PI_LO, PI_HI;
static double CUP[16], CDN[16];   /* upper / lower bounds of 1/((2j-1)(2j)) */

/* all arithmetic below assumes FE_UPWARD */
static inline double dn_mul(double a, double b) { return -((-a) * b); }
static inline double dn_add(double a, double b) { return -((-a) + (-b)); }

/* enclosure of cos(pi r / M), 0 <= r <= M/2 */
static inline void cospi_enc(uint64_t r, uint64_t M, double *lo, double *hi) {
  if (r == 0) { *lo = 1.0; *hi = 1.0; return; }
  volatile double rd = (double)r, Md = (double)M;
  double q_hi = rd / Md;
  double q_lo = -((-rd) / Md);
  double x_hi = q_hi * PI_HI;
  double x_lo = dn_mul(q_lo, PI_LO);
  /* upper bound of cos(x_lo): S_10, even terms up, odd terms down */
  {
    double yu = x_lo * x_lo, yd = dn_mul(x_lo, x_lo);
    double tu = 1.0, td = 1.0, s = 1.0;
    for (int j = 1; j <= 10; j++) {
      tu = (tu * yu) * CUP[j];
      td = dn_mul(dn_mul(td, yd), CDN[j]);
      if (j & 1) s = s + (-td); else s = s + tu;
    }
    *hi = s > 1.0 ? 1.0 : s;
  }
  /* lower bound of cos(x_hi): S_11, even terms down, odd terms up, downward accumulation */
  {
    double yu = x_hi * x_hi, yd = dn_mul(x_hi, x_hi);
    double tu = 1.0, td = 1.0, s = 1.0;
    for (int j = 1; j <= 11; j++) {
      tu = (tu * yu) * CUP[j];
      td = dn_mul(dn_mul(td, yd), CDN[j]);
      if (j & 1) s = dn_add(s, -tu); else s = dn_add(s, td);
    }
    *lo = s < 0.0 ? 0.0 : s;
  }
}

typedef struct { double s1lo, s1hi, s2lo, s2hi; uint64_t leaves; } acc_t;
static acc_t ACC;

static void dfs(int d, uint64_t u, double a_lo, double a_hi, double b_lo, double b_hi) {
  /* u known mod p^d (d >= 1); choose digit of position d */
  uint64_t M = PW[d + 1];
  int s = lvstart[d + 1], c = lvcnt[d + 1];
  for (int t = 0; t < P; t++) {
    uint64_t v = u + (uint64_t)t * PW[d];
    double al = a_lo, ah = a_hi, bl = b_lo, bh = b_hi;
    for (int i = 0; i < c; i++) {
      uint64_t r = (uint64_t)(((u128)v * LIST[s + i]) % M);
      if (r > M - r) r = M - r;
      double lo, hi; cospi_enc(r, M, &lo, &hi);
      al = dn_mul(al, lo); ah = ah * hi;
      bl = dn_mul(bl, dn_mul(lo, lo)); bh = bh * (hi * hi);
    }
    if (d + 1 == K) {
      ACC.s1lo = dn_add(ACC.s1lo, al); ACC.s1hi = ACC.s1hi + ah;
      ACC.s2lo = dn_add(ACC.s2lo, bl); ACC.s2hi = ACC.s2hi + bh;
      ACC.leaves++;
    } else dfs(d + 1, v, al, ah, bl, bh);
  }
}

static void selftest(void) {
  volatile double one = 1.0, three = 3.0;
  double up = one / three, dn = -((-one) / three);
  if (!(up > dn)) { fprintf(stderr, "rounding self-test failed: %.17g %.17g\n", up, dn); exit(2); }
  if (fegetround() != FE_UPWARD) { fprintf(stderr, "not in FE_UPWARD\n"); exit(2); }
  /* pi enclosure */
  if (!(PI_LO < PI_HI)) { fprintf(stderr, "pi enclosure\n"); exit(2); }
  /* cos enclosure sanity at a few points vs libm (round-to-nearest value must lie inside up to 1e-15) */
  uint64_t Ms[3] = {7, 1000003, 4782969};
  for (int a = 0; a < 3; a++)
    for (uint64_t r = 0; r <= Ms[a] / 2; r += (Ms[a] / 2) / 50 + 1) {
      double lo, hi; cospi_enc(r, Ms[a], &lo, &hi);
      double ref = cos(M_PI * (double)r / (double)Ms[a]);
      if (!(lo <= ref + 1e-15 && ref - 1e-15 <= hi && hi - lo < 1e-14)) {
        fprintf(stderr, "cos enclosure test failed r=%llu M=%llu [%.17g,%.17g] ref %.17g\n",
                (unsigned long long)r, (unsigned long long)Ms[a], lo, hi, ref); exit(2);
      }
    }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: ivshell fact p N0 kmax | ivshell file p kmax FILE\n"); return 1; }
  if (fesetround(FE_UPWARD) != 0) { fprintf(stderr, "fesetround failed\n"); return 2; }
  { uint64_t a = 0x400921FB54442D18ULL, b = 0x400921FB54442D19ULL; memcpy(&PI_LO, &a, 8); memcpy(&PI_HI, &b, 8); }
  for (int j = 1; j < 16; j++) {
    volatile double den = (double)((2 * j - 1) * (2 * j));
    CUP[j] = 1.0 / den; CDN[j] = -((-1.0) / den);
  }
  selftest();
  if (!strcmp(argv[1], "test")) {   /* ivshell test M r1 r2 ... : print enclosures of cos(pi r/M) */
    uint64_t M = strtoull(argv[2], 0, 10);
    for (int a = 3; a < argc; a++) {
      uint64_t r = strtoull(argv[a], 0, 10); if (2 * r > M) { fprintf(stderr, "r > M/2\n"); return 1; }
      double lo, hi; cospi_enc(r, M, &lo, &hi);
      printf("%llu %llu %a %a\n", (unsigned long long)M, (unsigned long long)r, lo, hi);
    }
    return 0;
  }
  P = atoi(argv[2]);
  if (!strcmp(argv[1], "fact")) {
    int N0 = atoi(argv[3]); KMAX = atoi(argv[4]);
    PW[0] = 1; for (int i = 1; i <= KMAX + 1; i++) PW[i] = PW[i - 1] * (uint64_t)P;
    if ((double)PW[KMAX] >= 9.0e15) { fprintf(stderr, "p^kmax too large\n"); return 1; }
    uint64_t BIG = PW[KMAX];
    int e0 = 0; uint64_t unit = 1;
    for (int n = 1; n <= N0; n++) { int m = n; while (m % P == 0) { m /= P; e0++; } unit = (uint64_t)(((u128)unit * (uint64_t)m) % BIG); }
    int lev = 0; NE = 0;
    for (int n = N0; lev < KMAX;) {
      UE[NE] = unit; LE[NE] = lev; NE++;
      if (NE >= MAXE) { fprintf(stderr, "too many elements\n"); return 1; }
      n++; int m = n; while (m % P == 0) { m /= P; lev++; }
      unit = (uint64_t)(((u128)unit * (uint64_t)m) % BIG);
    }
    printf("# ivshell fact p=%d N0=%d e0=%d kmax=%d elements(level<kmax)=%d\n", P, N0, e0, KMAX, NE);
  } else {
    KMAX = atoi(argv[3]);
    if (argc >= 8) { KMIN = atoi(argv[5]); T0LO = atoi(argv[6]); T0HI = atoi(argv[7]); }
    PW[0] = 1; for (int i = 1; i <= KMAX + 1; i++) PW[i] = PW[i - 1] * (uint64_t)P;
    if ((double)PW[KMAX] >= 9.0e15) { fprintf(stderr, "p^kmax too large\n"); return 1; }
    FILE *f = fopen(argv[4], "r"); if (!f) { perror("open"); return 1; }
    unsigned long long U; int l; NE = 0;
    while (fscanf(f, "%llu %d", &U, &l) == 2) { UE[NE] = (uint64_t)(U % PW[KMAX]); LE[NE] = l; NE++; if (NE >= MAXE) return 1; }
    fclose(f);
    printf("# ivshell file p=%d kmax=%d elements=%d source=%s\n", P, KMAX, NE, argv[4]);
  }
  printf("# k  T1_lo  T1_hi  T2_lo  T2_hi  leaves(half)  cumT1_hi  cumT2_hi\n");
  double c1 = 0, c2 = 0;
  if (KMIN > 1 || T0LO > 1 || T0HI < (P - 1) / 2)
    printf("# PARTIAL RUN: shells %d..%d, lowest digit u_0 in [%d,%d] only (u and -u still merged; totals are 2 x partial sums)\n",
           KMIN, KMAX, T0LO, T0HI < (P - 1) / 2 ? T0HI : (P - 1) / 2);
  for (K = KMIN; K <= KMAX; K++) {
    int pos = 0;
    for (int d = 1; d <= K; d++) {
      lvstart[d] = pos; lvcnt[d] = 0;
      for (int i = 0; i < NE; i++) if (LE[i] == K - d) { LIST[pos++] = UE[i] % PW[d]; lvcnt[d]++; }
    }
    memset(&ACC, 0, sizeof ACC);
    int half = (P - 1) / 2;
    int s = lvstart[1], c = lvcnt[1];
    for (int t = (T0LO > 1 ? T0LO : 1); t <= half && t <= T0HI; t++) {
      double al = 1, ah = 1, bl = 1, bh = 1;
      for (int i = 0; i < c; i++) {
        uint64_t r = (uint64_t)(((u128)t * LIST[s + i]) % PW[1]);
        if (r > PW[1] - r) r = PW[1] - r;
        double lo, hi; cospi_enc(r, PW[1], &lo, &hi);
        al = dn_mul(al, lo); ah = ah * hi; bl = dn_mul(bl, dn_mul(lo, lo)); bh = bh * (hi * hi);
      }
      if (K == 1) {
        ACC.s1lo = dn_add(ACC.s1lo, al); ACC.s1hi = ACC.s1hi + ah;
        ACC.s2lo = dn_add(ACC.s2lo, bl); ACC.s2hi = ACC.s2hi + bh; ACC.leaves++;
      } else dfs(1, (uint64_t)t, al, ah, bl, bh);
    }
    double T1lo = 2 * ACC.s1lo, T1hi = 2 * ACC.s1hi, T2lo = 2 * ACC.s2lo, T2hi = 2 * ACC.s2hi;
    c1 = c1 + T1hi; c2 = c2 + T2hi;
    printf("%2d %.12e %.12e %.12e %.12e %llu %.12e %.12e\n", K, T1lo, T1hi, T2lo, T2hi,
           (unsigned long long)ACC.leaves, c1, c2);
    fflush(stdout);
  }
  return 0;
}
