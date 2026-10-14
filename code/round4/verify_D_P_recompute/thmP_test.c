/* End-to-end test of Theorem P (track M4D) at p = 7 (or any odd p given T, n0).
 *
 * Theorem P: if Cov(p,t,H_t) holds for t <= T (H_t + 1 < p^t), n0 >= max H_t,
 * P(x,n0) holds and v(x+i) <= T for all n0 < i <= N, then P(x,N) holds.
 *
 * P(x,n) is decided EXACTLY through the equivalence P(x,n) <=> g_p(x) >= V_n(x)
 * (M4D section 1; checked by hand in the report) and the census DFS of
 * census.c (validated against brute force), run with G = V_n(x) on x mod p^G.
 *
 * Sampling: x uniform mod p^L (L = 21 digits at p = 7), optionally with a
 * forced gate of exact depth t at a uniformly chosen position i in [ilo, ihi]
 * (x == -i mod p^t, x != -i mod p^{t+1}).  For each sample we record
 *   A = P(x,n0),  B = P(x,N),  dmax = max_{n0<j<=N} v(x+j).
 * A violation of Theorem P is: A && !B && dmax <= T.
 * Controls (expected to produce A && !B): gates of depth > T, or gates placed
 * too close to the start (the theorem's n0 >= max H_t is then not met for the
 * relevant window).
 *
 * usage: thmP_test p T n0 N L nsamples seed tlo thi ilo ihi checkfrom
 *   tlo = 0 means no forced gate.
 *   checkfrom: the "n0" used for the premise A (normally = n0; controls may use a smaller one)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef int64_t i64; typedef uint64_t u64; typedef __int128 i128;

static i64 P, PG, G;
static i64 pw[64];
static int NMAX;
static int dn[4096];
static i64 uinv[4096];

#ifndef HBITS
#define HBITS 25
#endif
#define HSIZE (1u << HBITS)
static int overflow = 0;
static u64 *hk1; static uint8_t *hk2; static uint32_t *hgen; static uint32_t gen = 0; static long hcount;
static inline u64 hmix(u64 k) { k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33; return k; }
static int hfind(u64 a, int n) {
  u64 h = hmix(a * 131 + (u64)n) & (HSIZE - 1);
  while (hgen[h] == gen) { if (hk1[h] == a && hk2[h] == n) return 1; h = (h + 1) & (HSIZE - 1); }
  return 0;
}
static void hins(u64 a, int n) {
  u64 h = hmix(a * 131 + (u64)n) & (HSIZE - 1);
  while (hgen[h] == gen) { if (hk1[h] == a && hk2[h] == n) return; h = (h + 1) & (HSIZE - 1); }
  if (hcount > (long)(HSIZE * 0.7)) { overflow = 1; return; }   /* memo budget exhausted: decision becomes "undecided" */
  hgen[h] = gen; hk1[h] = a; hk2[h] = (uint8_t)n; hcount++;
}
static i64 modinv(i64 a, i64 m) {
  i64 t = 0, nt = 1, r = m, nr = ((a % m) + m) % m;
  while (nr) { i64 q = r / nr, tmp; tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
  if (r != 1) { fprintf(stderr, "not invertible\n"); exit(3); }
  return ((t % m) + m) % m;
}
static long nodes;
static int dfs(int n, i64 tau, int m) {
  nodes++;
  if (overflow) return 0;
  if (n >= NMAX) { fprintf(stderr, "NMAX\n"); exit(4); }
  int d = dn[n]; i64 pm = pw[m];
  for (int e = 1; e >= (n == 0 ? 1 : 0); e--) {
    i64 w = tau - e; if (w < 0) w += pm;
    if (d >= m) { if (w % pm == 0) return 1; continue; }
    if (w % pw[d] != 0) continue;
    int m2 = m - d; i64 pm2 = pw[m2];
    i64 t2 = (i64)(((i128)((w / pw[d]) % pm2) * (uinv[n] % pm2)) % pm2);
    if (hfind((u64)t2, n + 1)) continue;
    if (dfs(n + 1, t2, m2)) return 1;
    hins((u64)t2, n + 1);
  }
  return 0;
}
/* decide g_p(x) >= Gv, x given mod p^Gv */
static int decide(i64 x, int Gv) {
  G = Gv; PG = pw[Gv];
  i64 V = 0; int n = 0;
  while (1) {
    i64 y = (x + n + 1) % PG; int d = 0;
    if (y == 0) d = (int)G; else { while (y % P == 0) { y /= P; d++; } }
    dn[n] = d; uinv[n] = (d >= G) ? 1 : modinv(y, PG);
    V += d; n++;
    if (V >= G) break;
  }
  NMAX = n + 1; gen++; hcount = 0; overflow = 0;
  int r = dfs(0, 0, (int)G);
  if (r) return 1;            /* a witness path was found: exact */
  return overflow ? -1 : 0;   /* 0 = exhaustively refuted; -1 = undecided */
}

static u64 rs;
static u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static i64 rmod(i64 m) { return (i64)(((unsigned __int128)rnd() * (unsigned __int128)m) >> 64); }

static int vpx(i64 x, i64 i, int L) { /* v(x+i) with x mod p^L; returns L if divisible by p^L */
  i64 y = (x + i) % pw[L]; int v = 0;
  if (y == 0) return L;
  while (y % P == 0) { y /= P; v++; }
  return v;
}

int main(int argc, char **argv) {
  if (argc < 13) { fprintf(stderr, "usage: thmP_test p T n0 N L nsamples seed tlo thi ilo ihi checkfrom\n"); return 1; }
  P = atoll(argv[1]); int T = atoi(argv[2]); int n0 = atoi(argv[3]); int N = atoi(argv[4]); int L = atoi(argv[5]);
  long ns = atol(argv[6]); rs = strtoull(argv[7], 0, 10) * 2654435761ULL + 88172645463325252ULL;
  int tlo = atoi(argv[8]), thi = atoi(argv[9]), ilo = atoi(argv[10]), ihi = atoi(argv[11]); int cf = atoi(argv[12]);
  pw[0] = 1; for (int i = 1; i < 64; i++) pw[i] = pw[i - 1] * P;
  if ((double)pw[L] > 4e18) { fprintf(stderr, "L too large\n"); return 1; }
  hk1 = malloc(sizeof(u64) * HSIZE); hk2 = malloc(HSIZE); hgen = calloc(HSIZE, sizeof(uint32_t));
  for (int i = 0; i < 20; i++) rnd();
  long undecided = 0, cntA = 0, cntAB = 0, cntAnB = 0, viol = 0, skipped = 0, cnt_deep = 0, cnt_deep_fail = 0, done = 0;
  long bydepth_A[64] = {0}, bydepth_AnB[64] = {0};
  printf("# thmP_test p=%lld T=%d n0=%d N=%d L=%d samples=%ld forced depth %d..%d at i in [%d,%d], premise P(x,%d)\n",
         (long long)P, T, n0, N, L, ns, tlo, thi, ilo, ihi, cf);
  while (done < ns) {
    i64 x; int tf = 0, ipos = 0;
    if (tlo > 0) {
      tf = tlo + (int)rmod(thi - tlo + 1); ipos = ilo + (int)rmod(ihi - ilo + 1);
      i64 u; do { u = rmod(pw[L - tf]); } while (u % P == 0);
      x = ((-(i64)ipos % pw[L]) + pw[L] + (i64)(((i128)pw[tf] * u) % pw[L])) % pw[L];
    } else x = rmod(pw[L]);
    /* valuations, exact as long as all < L */
    int bad = 0; i64 Vc = 0, VN = 0; int dmax = 0;
    for (int i = 1; i <= N; i++) {
      int v = vpx(x, i, L); if (v >= L) bad = 1;
      if (i <= cf) Vc += v;
      VN += v;
      if (i > cf && v > dmax) dmax = v;
    }
    if (bad || VN >= L) { skipped++; continue; }
    if (tlo > 0 && vpx(x, ipos, L) != tf) { fprintf(stderr, "forcing failed\n"); return 5; }
    done++;
    int A = decide(x % pw[Vc], (int)Vc);
    if (A < 0) { undecided++; continue; }
    if (!A) continue;
    cntA++;
    int B = decide(x % pw[VN], (int)VN);
    if (B < 0) { undecided++; cntA--; continue; }
    if (dmax > T) cnt_deep++;
    bydepth_A[dmax]++;
    if (B) cntAB++;
    else {
      cntAnB++; bydepth_AnB[dmax]++;
      if (dmax > T) cnt_deep_fail++;
      else { viol++; printf("%s x=", (cf < n0 || thi > T) ? "CONTROL_FAIL" : "VIOLATION"); printf("%lld (mod p^%d) dmax=%d forced t=%d at i=%d\n", (long long)x, L, dmax, tf, ipos); }
    }
  }
  printf("undecided (memo budget exhausted, neither witness nor refutation): %ld\n", undecided);
  printf("samples %ld (skipped %ld for valuation >= L); P(x,%d): %ld; of these P(x,%d): %ld, not P(x,%d): %ld\n",
         done, skipped, cf, cntA, N, cntAB, N, cntAnB);
  printf("by max depth in (%d,%d]:", cf, N);
  for (int d = 0; d < 64; d++) if (bydepth_A[d]) printf("  d=%d: %ld premise, %ld fail", d, bydepth_A[d], bydepth_AnB[d]);
  printf("\nsamples with a gate deeper than T=%d: %ld (fails among them: %ld)\n", T, cnt_deep, cnt_deep_fail);
  if (cf < n0 || thi > T) printf("RESULT (CONTROL run: hypotheses of Theorem P deliberately not met) implication failures with dmax <= T: %ld\n", viol);
  else printf("RESULT violations of Theorem P (premise, no gate > T, but not P(x,N)): %ld\n", viol);
  return 0;
}
