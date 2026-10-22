/* Referee re-implementation of D_p(w,K) (Theorem 11.17 / Corollary 11.19), written from the
   definition in note_v3 section 11.2 only (T1b's wdim.c not read).
   D_p(w,K) = (p-1)/(w p) * p^{-(K-1)} * sum_{y mod p^{K-1}} log_p N(p y),
   N(tau) = #distinct subset sums mod p^{G} of q_s = prod_{t=1}^{s}(tau+t), s=0..P-1, P=w p,
   G = min(K, sum_{t=1}^{P} min(v(tau+t),K)), v(0 mod p^K) := K.
   Distinct subset sums by a cyclic bitset over Z/p^G (OR with rotated copy per element).
   Usage: dimref p w K [nthreads]   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
typedef uint64_t u64;
static int p, w, K, P, NT = 1;
static u64 pK, pK1, ppow[64];
static void or_rot(u64 *dst, const u64 *src, u64 m, u64 q, u64 nw) {
  /* dst |= rot_left(src, q) on m-bit cyclic array; src clean (no bits >= m) */
  if (q == 0) { for (u64 j = 0; j < nw; j++) dst[j] |= src[j]; return; }
  u64 ws = q >> 6, bs = q & 63;
  for (u64 j = ws; j < nw; j++) {
    u64 v = src[j - ws] << bs;
    if (bs && j > ws) v |= src[j - ws - 1] >> (64 - bs);
    dst[j] |= v;
  }
  u64 r = m - q; ws = r >> 6; bs = r & 63; /* dst |= src >> r */
  for (u64 j = 0; j + ws < nw; j++) {
    u64 v = src[j + ws] >> bs;
    if (bs && j + ws + 1 < nw) v |= src[j + ws + 1] << (64 - bs);
    dst[j] |= v;
  }
  u64 rem = m & 63; if (rem) dst[nw - 1] &= (((u64)1 << rem) - 1);
}
typedef struct { u64 y0, y1; long double sumlog; u64 hist[64]; } job_t;
static void *run(void *arg) {
  job_t *J = (job_t *)arg;
  u64 maxw = (pK + 63) / 64 + 1;
  u64 *A = malloc(maxw * 8), *B = malloc(maxw * 8);
  long double lp = logl((long double)p);
  J->sumlog = 0;
  for (u64 y = J->y0; y < J->y1; y++) {
    u64 tau = (p * y) % pK;
    int G = 0;
    for (int t = 1; t <= P; t++) {
      u64 z = (tau + t) % pK; int v = 0;
      if (z == 0) v = K; else { while (z % p == 0 && v < K) { z /= p; v++; } }
      G += v;
    }
    if (G > K) G = K;
    u64 m = ppow[G], nw = (m + 63) / 64;
    memset(A, 0, nw * 8); A[0] = 1; /* empty sum */
    u64 q = 1 % m;
    for (int s = 0; s < P; s++) {
      if (s > 0) q = (u64)(((unsigned __int128)q * ((tau + s) % m)) % m);
      memcpy(B, A, nw * 8);
      or_rot(B, A, m, q, nw);
      u64 *T = A; A = B; B = T;
    }
    u64 N = 0; for (u64 j = 0; j < nw; j++) N += __builtin_popcountll(A[j]);
    J->sumlog += logl((long double)N) / lp;
    if (G < 64) J->hist[G]++;
  }
  free(A); free(B); return NULL;
}
int main(int argc, char **argv) {
  p = atoi(argv[1]); w = atoi(argv[2]); K = atoi(argv[3]); if (argc > 4) NT = atoi(argv[4]);
  P = w * p; ppow[0] = 1; for (int i = 1; i < 64; i++) ppow[i] = ppow[i - 1] * p;
  pK = ppow[K]; pK1 = ppow[K - 1];
  pthread_t th[64]; job_t jb[64]; memset(jb, 0, sizeof jb);
  for (int i = 0; i < NT; i++) { jb[i].y0 = pK1 * i / NT; jb[i].y1 = pK1 * (i + 1) / NT; pthread_create(&th[i], 0, run, &jb[i]); }
  long double tot = 0; u64 hist[64] = {0};
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0); tot += jb[i].sumlog; for (int g = 0; g < 64; g++) hist[g] += jb[i].hist[g]; }
  long double D = (long double)(p - 1) / (w * p) * tot / (long double)pK1;
  printf("p=%d w=%d K=%d D=%.12Lf  (mean log_p N = %.12Lf)\n", p, w, K, D, tot / (long double)pK1);
  printf("G histogram:"); for (int g = 0; g < 64; g++) if (hist[g]) printf(" %d:%llu", g, (unsigned long long)hist[g]); printf("\n");
  return 0;
}
