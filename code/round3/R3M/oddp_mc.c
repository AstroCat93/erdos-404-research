/* oddp_mc.c -- Monte Carlo of the carry population at an odd prime p (track R3M, round 3).
 *
 * For Haar-random x in Z_p (K random base-p digits) it follows every path e = (e_0=1,e_1,...)
 * alive at time n, i.e. tau_n(e,x) = -S_e(x)/pi_n(x) in Z_p, via the carry recursion
 *     tau_{j+1} = (tau_j - e_j)/(x+j+1),        tau_0 = 0,
 * with tau_j stored mod p^(K - V_j) (exact precision bookkeeping), and the slope
 * lam_e = v_p(S_e'(x)) from S_e'(x) mod p^KD (S' updated by S'_{j+1} = S'_j + e_j pi_j'(x)).
 * Output, for each n <= NMAX, aggregated over the NX samples:
 *   P(Z_n>0), E Z_n, E Z_n^2, E Z_n^2/(E Z_n)^2 for Z_n = #alive paths (all slopes) and Z0_n = #slope-0
 *   alive paths, and the quenched normalised slope-0 population M0_n = 2^-n p^{V_n(x)} Z0_n:
 *   E M0_n, E M0_n^2.
 * A sample whose population exceeds CAP, or whose valuations exceed the precision, is
 * reported (and excluded from the moments from that time on; counted in 'censored').
 * usage: oddp_mc p SEED NX NMAX K KD CAP [NVERB]
 * NVERB > 0 prints "SAMPLE x n Z Z0" for the first NVERB samples at n = NMAX (for cross-checks).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 rng_s[2];
static u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rnd(void) { u64 s0 = rng_s[0], s1 = rng_s[1], r = s0 + s1; s1 ^= s0;
  rng_s[0] = rotl(s0, 55) ^ s1 ^ (s1 << 14); rng_s[1] = rotl(s1, 36); return r; }

static u64 pw[64];
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 invmod(u64 a, u64 m) { /* a unit mod m, m = p^k */
  __int128 t = 0, nt = 1, r = m, nr = a % m;
  while (nr) { __int128 q = r / nr, tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
  if (t < 0) t += m; return (u64)t; }

int main(int argc, char **argv) {
  if (argc < 8) { fprintf(stderr, "usage: oddp_mc p SEED NX NMAX K KD CAP\n"); return 1; }
  int p = atoi(argv[1]); u64 seed = strtoull(argv[2], 0, 10); long NX = atol(argv[3]);
  int NMAX = atoi(argv[4]), K = atoi(argv[5]), KD = atoi(argv[6]); long CAP = atol(argv[7]); int NVERB = argc > 8 ? atoi(argv[8]) : 0;
  pw[0] = 1; for (int i = 1; i < 64; i++) pw[i] = pw[i - 1] * (u64)p;
  if ((long double)pw[K] * 2 > 1.8e19L) { fprintf(stderr, "K too large\n"); return 1; }
  rng_s[0] = seed * 0x9E3779B97F4A7C15ULL + 1; rng_s[1] = seed ^ 0xD1B54A32D192ED03ULL; for (int i = 0; i < 20; i++) rnd();
  u64 PK = pw[K], PKD = pw[KD];
  double *s1 = calloc(NMAX + 1, 8), *s2 = calloc(NMAX + 1, 8), *z1 = calloc(NMAX + 1, 8), *z2 = calloc(NMAX + 1, 8);
  double *m1 = calloc(NMAX + 1, 8), *m2 = calloc(NMAX + 1, 8);
  long *pos = calloc(NMAX + 1, 8), *pos0 = calloc(NMAX + 1, 8), *nval = calloc(NMAX + 1, 8);
  long censored = 0;
  u64 *tau = malloc(sizeof(u64) * CAP * 2), *ntau = malloc(sizeof(u64) * CAP * 2);
  u64 *ds = malloc(sizeof(u64) * CAP * 2), *nds = malloc(sizeof(u64) * CAP * 2);
  u64 *pij = malloc(sizeof(u64) * (NMAX + 2)), *dpij = malloc(sizeof(u64) * (NMAX + 2));
  for (long it = 0; it < NX; it++) {
    u64 x = 0; for (int i = 0; i < K; i++) x = x * p + rnd() % p;   /* x mod p^K */
    /* pi_j(x), pi_j'(x) mod p^KD */
    pij[0] = 1; dpij[0] = 0;
    for (int j = 1; j <= NMAX + 1; j++) { u64 xj = (x + j) % PKD;
      dpij[j] = (mulmod(dpij[j - 1], xj, PKD) + pij[j - 1]) % PKD; pij[j] = mulmod(pij[j - 1], xj, PKD); }
    /* time 1: path (1): tau_1 = -1/(x+1) */
    long Z = 1; int V = 0; int ok = 1;
    tau[0] = 0; ds[0] = 0;   /* tau_0 = 0, S'_0 = 0 (S_0 = 0) ; step j=0 uses e_0 = 1 forced */
    double logc = 0;  /* log2 of 2^-n p^V */
    for (int j = 0; j < NMAX && ok; j++) {
      /* step from time j to j+1 with factor z = x + j + 1 */
      u64 z = (x + (u64)j + 1) % PK; int d = 0; u64 zz = z;
      if (zz == 0) { ok = 0; break; }
      while (zz % p == 0) { zz /= p; d++; }
      int prec = K - V; if (d >= prec) { ok = 0; break; }
      u64 mod = pw[prec], nmod = pw[prec - d];
      u64 uinv = invmod(zz % nmod, nmod);
      long nZ = 0;
      for (long i = 0; i < Z; i++) {
        for (int e = (j == 0 ? 1 : 0); e <= 1; e++) {
          u64 t = (tau[i] + mod - (u64)e) % mod;
          if (d && t % pw[d]) continue;
          t /= pw[d];
          if (nZ >= CAP) { ok = 0; break; }
          ntau[nZ] = mulmod(t, uinv, nmod);
          nds[nZ] = e ? (ds[i] + dpij[j]) % PKD : ds[i];
          nZ++;
        }
        if (!ok) break;
      }
      if (!ok) break;
      V += d; Z = nZ;
      u64 *tt = tau; tau = ntau; ntau = tt; tt = ds; ds = nds; nds = tt;
      int n = j + 1;
      logc += -1.0 + d * log2((double)p);
      long Z0 = 0; for (long i = 0; i < Z; i++) if (ds[i] % p) Z0++;
      double c = exp2(logc);
      nval[n]++; s1[n] += Z; s2[n] += (double)Z * Z; z1[n] += Z0; z2[n] += (double)Z0 * Z0;
      m1[n] += c * Z0; m2[n] += c * c * (double)Z0 * Z0;
      if (Z > 0) pos[n]++; if (Z0 > 0) pos0[n]++;
      if (Z == 0) { /* extinct: record zeros for the remaining times */
        for (int nn = n + 1; nn <= NMAX; nn++) nval[nn]++;
        break; }
    }
    if (!ok) censored++;
    if (it < NVERB && ok) {
      long Z0 = 0; for (long i = 0; i < Z; i++) if (ds[i] % p) Z0++;
      printf("SAMPLE %llu %d %ld %ld\n", (unsigned long long)x, NMAX, Z, Z0);
    }
  }
  printf("# oddp_mc p=%d seed=%llu NX=%ld NMAX=%d K=%d KD=%d CAP=%ld censored=%ld\n", p, (unsigned long long)seed, NX, NMAX, K, KD, CAP, censored);
  printf("# n  nvalid  P(Z>0)  P(Z0>0)  EZ  EZ^2/(EZ)^2  EZ0  EZ0^2/(EZ0)^2  E[M0]  E[M0^2]  E[M0^2]/E[M0]^2\n");
  for (int n = 1; n <= NMAX; n++) {
    double N_ = nval[n]; if (N_ == 0) continue;
    double ez = s1[n] / N_, ez2 = s2[n] / N_, e0 = z1[n] / N_, e02 = z2[n] / N_, em = m1[n] / N_, em2 = m2[n] / N_;
    printf("TABLE %3d %8.0f %.5f %.5f %.4e %.4f %.4e %.4f %.5f %.5f %.4f\n", n, N_, pos[n] / N_, pos0[n] / N_, ez,
           ez > 0 ? ez2 / (ez * ez) : 0, e0, e0 > 0 ? e02 / (e0 * e0) : 0, em, em2, em > 0 ? em2 / (em * em) : 0);
  }
  return 0;
}
