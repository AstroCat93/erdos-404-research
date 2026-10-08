/* fourier.c -- Fourier diagnostics for the p-adic "factorial Bernoulli convolution".
 *
 * nu_N = law of X = sum_{n>=N} eps_n * n!/p^{e(N)}  in Z_p,  eps_n iid Bernoulli(1/2),
 * e(N) = v_p(N!).  For a frequency xi = u/p^s (u a unit mod p^s, "depth" s >= 1):
 *     |hat nu_N(xi)| = prod_{n>=N, v_p(n!)-e(N) < s} |cos(pi * u * w_n / p^s)|,
 *     w_n = n!/p^{e(N)} mod p^s.
 * For each depth s we print
 *     T_s = sum_{u unit mod p^s} |hat nu(u/p^s)|        (L^1 mass at depth s)
 *     Q_s = sum_{u unit mod p^s} |hat nu(u/p^s)|^2      (L^2 mass at depth s)
 *     Mx_s = max_u |hat nu(u/p^s)|
 * Criterion (rigorous, see notes): if sum_{s=1}^K T_s < 1 then the subset sums of
 * {n! : n >= N} cover all of p^{e(N)} Z / p^{e(N)+K} Z.
 * Floating point with a 2^16-entry interpolated cosine table: DIAGNOSTIC ONLY.
 *
 * usage: fourier p N Smax [threads]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <pthread.h>

typedef unsigned __int128 u128;
static int P, NN, SMAX, NTH = 3;
static uint64_t W[4096]; static int NW;
static uint64_t MOD;
#define TB 65536
static double CT[TB + 2];

typedef struct { uint64_t u0, u1; double T, Q, Mx; } job_t;

static void *work(void *arg) {
  job_t *j = (job_t *)arg;
  uint64_t r[4096];
  for (int i = 0; i < NW; i++) r[i] = (uint64_t)(((u128)j->u0 * W[i]) % MOD);
  double T = 0, Q = 0, Mx = 0;
  const double sc = (double)TB / (double)MOD;
  for (uint64_t u = j->u0; u < j->u1; u++) {
    if (u % P) {
      double pr = 1.0;
      for (int i = 0; i < NW; i++) {
        double x = (double)r[i] * sc;
        int k = (int)x; double f = x - k;
        pr *= CT[k] + f * (CT[k + 1] - CT[k]);
      }
      T += pr; Q += pr * pr; if (pr > Mx) Mx = pr;
    }
    for (int i = 0; i < NW; i++) { uint64_t t = r[i] + W[i]; if (t >= MOD) t -= MOD; r[i] = t; }
  }
  j->T = T; j->Q = Q; j->Mx = Mx;
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: fourier p N Smax [threads]\n"); return 1; }
  P = atoi(argv[1]); NN = atoi(argv[2]); SMAX = atoi(argv[3]); if (argc > 4) NTH = atoi(argv[4]);
  for (int k = 0; k <= TB + 1; k++) CT[k] = fabs(cos(M_PI * (double)k / TB));
  /* big modulus p^SMAX */
  uint64_t BIG = 1; for (int i = 0; i < SMAX; i++) BIG *= P;
  /* unit part of N! mod BIG and e(N) */
  uint64_t U = 1 % BIG; int e = 0;
  for (int k = 1; k <= NN; k++) { int m = k; while (m % P == 0) { m /= P; e++; } U = (uint64_t)(((u128)U * (uint64_t)m) % BIG); }
  /* list n >= N with relative valuation < SMAX, store (n!/p^{e(N)}) mod BIG and relative valuation */
  static uint64_t WB[4096]; static int VR[4096]; int cnt = 0;
  { uint64_t cur = U; int vr = 0; int n = NN;
    while (vr < SMAX) {
      uint64_t pw = 1; for (int i = 0; i < vr; i++) pw *= P;
      WB[cnt] = (uint64_t)(((u128)cur * pw) % BIG); VR[cnt] = vr; cnt++;
      n++; int m = n; while (m % P == 0) { m /= P; vr++; }
      cur = (uint64_t)(((u128)cur * (uint64_t)m) % BIG);
    }
  }
  printf("# p=%d N=%d e(N)=%d elements_with_relval<%d: %d\n", P, NN, e, SMAX, cnt);
  printf("# s  #nontriv  T_s  Q_s  Mx_s  cumT  cumQ  T_s/T_{s-1}\n");
  double cumT = 0, cumQ = 0, prevT = 0;
  for (int s = 1; s <= SMAX; s++) {
    MOD = 1; for (int i = 0; i < s; i++) MOD *= P;
    NW = 0; for (int i = 0; i < cnt; i++) if (VR[i] < s) W[NW++] = WB[i] % MOD;
    /* by symmetry u <-> MOD-u, sum over u in [1, MOD/2] and double (MOD odd for odd p; p=2 handle separately) */
    uint64_t lo = 1, hi = (P == 2) ? MOD : (MOD / 2 + 1);
    pthread_t th[16]; job_t jb[16];
    uint64_t span = hi - lo, step = (span + NTH - 1) / NTH;
    for (int t = 0; t < NTH; t++) { jb[t].u0 = lo + t * step; jb[t].u1 = lo + (t + 1) * step; if (jb[t].u1 > hi) jb[t].u1 = hi; if (jb[t].u0 > hi) jb[t].u0 = hi; pthread_create(&th[t], NULL, work, &jb[t]); }
    double T = 0, Q = 0, Mx = 0;
    for (int t = 0; t < NTH; t++) { pthread_join(th[t], NULL); T += jb[t].T; Q += jb[t].Q; if (jb[t].Mx > Mx) Mx = jb[t].Mx; }
    if (P != 2) { T *= 2; Q *= 2; }
    cumT += T; cumQ += Q;
    printf("%2d %4d %.6e %.6e %.6e %.6f %.6f %.4f\n", s, NW, T, Q, Mx, cumT, cumQ, prevT > 0 ? T / prevT : 0.0);
    fflush(stdout); prevT = T;
  }
  return 0;
}
