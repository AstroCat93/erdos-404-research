/* fl1.c -- certified upper bounds for Fourier L1 shell sums of the uniform
 * factorial Bernoulli convolution (Erdos #404, tail fullness).
 *
 * X = sum_{n>=N0} eps_n n!/p^{e0},  e0=v_p(N0!), eps_n iid fair coins.
 * For xi = u/p^k (u unit mod p^k):  |nu^(xi)| = prod_{n: l_n<k} |cos(pi u x_n / p^k)|,
 * x_n = p^{l_n} U_n, l_n = v(n!)-e0.  Shell sum T(k) = sum_{u unit mod p^k} |nu^(u/p^k)|.
 *
 * DFS over p-adic digits u_0,u_1,... ; after d digits, all n with k-l_n = d are evaluated
 * (they depend on u mod p^d only).  Pruning: a node with partial product P at depth d
 * contributes at most P * p^(k-d) * (#units fraction) -- we use p^(k-d) (rigorous, factors<=1).
 * Outward rounding: each factor is replaced by min(1, fl(cos)+DELTA), DELTA=1e-13 >> libm error
 * (<=1ulp) + argument error (~1e-15); product/sum roundings are dominated (see notes).
 * Final upper bound multiplied by (1+1e-9).
 * Symmetry u -> -u halves the work (cos even); u_0 in [1,(p-1)/2], result doubled.
 *
 * usage: fl1 p N0 kmin kmax tau [nthreads]
 *   prints, per shell k: exact-part sum (upper), pruned mass bound, total upper bound,
 *   number of evaluated leaves; and the cumulative sum.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <pthread.h>

typedef unsigned __int128 u128;
#define MAXN 8192
#define MAXK 40
static int P, N0, KMIN, KMAX, NTH = 3;
static double TAU;
static uint64_t UB[MAXN]; static int LB[MAXN]; static int CNT;
static const double DELTA = 1e-13;

/* per-shell structures */
static int K;                         /* current shell */
static uint64_t PW[MAXK + 1];         /* p^i */
static double PWD[MAXK + 1];
static int lvstart[MAXK + 2], lvcnt[MAXK + 2]; /* n's evaluated at depth d: indices into LIST */
static uint64_t LIST[MAXN];           /* U_n mod p^d for the n evaluated at depth d */

typedef struct { int t0, t1; double sum, pruned; uint64_t leaves; } job_t;

static inline double fac(uint64_t r, uint64_t M) {
  uint64_t rr = (r > M - r) ? M - r : r;           /* |cos(pi r/M)| = cos(pi min(r,M-r)/M) */
  double q = (double)rr / (double)M;
  double c = cos(M_PI * q) + DELTA;
  return c > 1.0 ? 1.0 : c;
}

static void dfs(int d, uint64_t u, double part, job_t *J) {
  /* u = u mod p^d known; choose digit t for position d */
  uint64_t M = PW[d + 1];
  int s = lvstart[d + 1], c = lvcnt[d + 1];
  for (int t = 0; t < P; t++) {
    uint64_t v = u + (uint64_t)t * PW[d];
    double pr = part;
    for (int i = 0; i < c; i++) {
      uint64_t r = (uint64_t)(((u128)v * LIST[s + i]) % M);
      pr *= fac(r, M);
    }
    if (d + 1 == K) { J->sum += pr; J->leaves++; continue; }
    double bound = pr * PWD[K - d - 1];
    if (bound < TAU) { J->pruned += bound; continue; }
    dfs(d + 1, v, pr, J);
  }
}

static void *work(void *arg) {
  job_t *J = (job_t *)arg;
  int s = lvstart[1], c = lvcnt[1];
  for (int t = J->t0; t < J->t1; t++) {
    double pr = 1.0;
    for (int i = 0; i < c; i++) pr *= fac((uint64_t)(((u128)t * LIST[s + i]) % PW[1]), PW[1]);
    if (K == 1) { J->sum += pr; J->leaves++; continue; }
    double bound = pr * PWD[K - 1];
    if (bound < TAU) { J->pruned += bound; continue; }
    dfs(1, (uint64_t)t, pr, J);
  }
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: fl1 p N0 kmin kmax tau [threads]\n"); return 1; }
  P = atoi(argv[1]); N0 = atoi(argv[2]); KMIN = atoi(argv[3]); KMAX = atoi(argv[4]); TAU = atof(argv[5]);
  if (argc > 6) NTH = atoi(argv[6]);
  PW[0] = 1; PWD[0] = 1;
  for (int i = 1; i <= KMAX; i++) { PW[i] = PW[i - 1] * (uint64_t)P; PWD[i] = PWD[i - 1] * P; }
  if ((double)PW[KMAX] > 9.0e18 || (double)PW[KMAX] * (double)P > 1.8e19) { fprintf(stderr, "p^kmax too large\n"); return 1; }
  uint64_t BIG = PW[KMAX];
  /* unit part of N0! and e0 */
  int e0 = 0; for (int k = 1; k <= N0; k++) { int m = k; while (m % P == 0) { m /= P; e0++; } }
  /* elements n >= N0 with l_n < KMAX: U_n mod BIG (unit part of n!; common unit factor irrelevant) */
  uint64_t cur = 1; for (int k = 1; k <= N0; k++) { int m = k; while (m % P == 0) m /= P; cur = (uint64_t)(((u128)cur * (uint64_t)m) % BIG); }
  int l = 0, n = N0; CNT = 0;
  while (l < KMAX) {
    UB[CNT] = cur; LB[CNT] = l; CNT++;
    n++; int m = n; while (m % P == 0) { m /= P; l++; }
    cur = (uint64_t)(((u128)cur * (uint64_t)m) % BIG);
    if (CNT >= MAXN) { fprintf(stderr, "too many\n"); return 1; }
  }
  printf("# fl1 p=%d N0=%d e0=%d elements(l<%d)=%d tau=%.3g DELTA=%.1e\n", P, N0, e0, KMAX, CNT, TAU, DELTA);
  printf("# k  sum_evaluated(upper)  pruned_bound  T_upper  leaves  cum_T_upper  T/T_prev\n");
  double cum = 0, prev = 0;
  for (K = KMIN; K <= KMAX; K++) {
    /* build per-depth lists: depth d = K - l */
    int pos = 0;
    for (int d = 1; d <= K; d++) {
      lvstart[d] = pos; lvcnt[d] = 0;
      for (int i = 0; i < CNT; i++) if (LB[i] == K - d) { LIST[pos++] = UB[i] % PW[d]; lvcnt[d]++; }
    }
    int half = (P - 1) / 2;
    pthread_t th[16]; job_t jb[16];
    int nth = NTH > half ? half : NTH;
    for (int t = 0; t < nth; t++) {
      jb[t].t0 = 1 + (t * half) / nth; jb[t].t1 = 1 + ((t + 1) * half) / nth;
      jb[t].sum = jb[t].pruned = 0; jb[t].leaves = 0;
      pthread_create(&th[t], NULL, work, &jb[t]);
    }
    double S = 0, Pr = 0; uint64_t lv = 0;
    for (int t = 0; t < nth; t++) { pthread_join(th[t], NULL); S += jb[t].sum; Pr += jb[t].pruned; lv += jb[t].leaves; }
    S *= 2; Pr *= 2;               /* symmetry u <-> -u */
    double T = (S + Pr) * (1 + 1e-9);
    cum += T;
    printf("%2d %.6e %.3e %.6e %llu %.6e %.4f\n", K, S, Pr, T, (unsigned long long)lv, cum, prev > 0 ? T / prev : 0.0);
    fflush(stdout); prev = T;
  }
  return 0;
}
