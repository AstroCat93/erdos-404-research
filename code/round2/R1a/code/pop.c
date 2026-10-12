// pop.c -- population of valid carry paths for the p=2 problem (Erdos #404), with derivative offsets.
// EXPLORATION / CHECKING TOOL.  For x in Z_2 (W*64-bit precision), runs gamma_n = (gamma_{n-1}+e_{n-1})/(x+n),
// gamma_0 = 0, e_0 = 1, keeping only valid paths (gamma_n in Z_2).  For each path it also tracks
// B_n = sum_{i<=n} gamma_i(x) pi_{i-1}(x) mod 2^64, so kappa_n = v2(B_n) (capped at 64).
// Modes:
//   pop rand  W nmax nsamp seed [w]   : random even x (or x = -2 + 2^w*odd if w>0); report checkpoints
//   pop deep  W D nsamp seed          : run to the first deep gate r_D(x) and report population etc.
// Paths with identical (gamma mod current precision, B mod 2^64) are merged with multiplicity.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
#define MAXW 64
static int W;
static u64 s4[4];
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rng(void) { const u64 r = rotl(s4[1] * 5, 7) * 9; const u64 t = s4[1] << 17;
  s4[2] ^= s4[0]; s4[3] ^= s4[1]; s4[1] ^= s4[2]; s4[0] ^= s4[3]; s4[2] ^= t; s4[3] = rotl(s4[3], 45); return r; }
static void seedrng(u64 s) { s4[0] = s * 0x9E3779B97F4A7C15ULL + 1; s4[1] = s ^ 0xDEADBEEFULL; s4[2] = 12345 + s; s4[3] = 0xABCDEF ^ (s << 7); for (int i = 0; i < 30; i++) rng(); }
typedef struct { u64 a[MAXW]; } big;
static void bset(big *r, u64 v) { memset(r->a, 0, sizeof(u64) * W); r->a[0] = v; }
static void badd_small(big *r, const big *x, int64_t v) { // r = x + v mod 2^(64W), v may be negative
  u64 carry; if (v >= 0) { carry = (u64)v; for (int i = 0; i < W; i++) { u128 s = (u128)x->a[i] + carry; r->a[i] = (u64)s; carry = (u64)(s >> 64); } }
  else { u64 borrow = (u64)(-v); for (int i = 0; i < W; i++) { u64 xi = x->a[i]; r->a[i] = xi - borrow; borrow = (xi < borrow) ? 1 : 0; } } }
static void bmul(big *r, const big *x, const big *y) { // truncated product mod 2^(64W)
  u64 t[MAXW]; memset(t, 0, sizeof(u64) * W);
  for (int i = 0; i < W; i++) { u64 carry = 0; if (!x->a[i]) continue;
    for (int j = 0; i + j < W; j++) { u128 p = (u128)x->a[i] * y->a[j] + t[i + j] + carry; t[i + j] = (u64)p; carry = (u64)(p >> 64); } }
  memcpy(r->a, t, sizeof(u64) * W); }
static int bctz(const big *x) { for (int i = 0; i < W; i++) if (x->a[i]) return 64 * i + __builtin_ctzll(x->a[i]); return 64 * W; }
static void bshr(big *r, const big *x, int d) { int q = d / 64, s = d % 64; u64 t[MAXW];
  for (int i = 0; i < W; i++) { u64 lo = (i + q < W) ? x->a[i + q] : 0; u64 hi = (i + q + 1 < W) ? x->a[i + q + 1] : 0;
    t[i] = s ? ((lo >> s) | (hi << (64 - s))) : lo; } memcpy(r->a, t, sizeof(u64) * W); }
static void binv(big *r, const big *u) { // inverse of odd u mod 2^(64W)
  big y, t, two; bset(&y, u->a[0]); // correct mod 8
  for (int k = 0; k < 14; k++) { bmul(&t, u, &y); // t = u*y ; y = y*(2 - t)
    big n; for (int i = 0; i < W; i++) n.a[i] = ~t.a[i]; badd_small(&n, &n, 3); // 2 - t = ~t + 3
    bmul(&y, &y, &n); }
  *r = y; (void)two; }
static void bmask(big *x, int bits) { if (bits >= 64 * W) return; if (bits < 0) bits = 0; int q = bits / 64, s = bits % 64;
  if (q < W) { if (s) x->a[q] &= ((u64)1 << s) - 1; else x->a[q] = 0; for (int i = q + 1; i < W; i++) x->a[i] = 0; } }
static int bcmp_(const big *x, const big *y) { return memcmp(x->a, y->a, sizeof(u64) * W); }
typedef struct { big g; u64 B; long long cnt; } part;
#define MAXP 200000
static part P0[MAXP], P1[MAXP];
static int cmpp(const void *a, const void *b) { const part *p = a, *q = b; int c = bcmp_(&p->g, &q->g); if (c) return c; return (p->B < q->B) ? -1 : (p->B > q->B); }
static inline int v64(u64 b) { return b ? __builtin_ctzll(b) : 64; }
// run from n=1 to nend (inclusive) ; returns final population count (sum of cnt), fills stats
typedef struct { long long pop; int maxkap; long long flat, unstable; int vpi; int M; } stats;
static big X;
static int run(int nend, stats *st, int *outn, int stop_deep) {
  int prec = 64 * W; int np = 0; u64 pi_prev = 1; int vpi = 0, Menv = 0;
  // n = 1 : gamma_1 = 1/(x+1)
  big t; badd_small(&t, &X, 1); int d = bctz(&t); if (d) { st->pop = 0; *outn = 1; return 0; }
  binv(&P0[0].g, &t); P0[0].B = P0[0].g.a[0]; P0[0].cnt = 1; np = 1; pi_prev = t.a[0];
  int n;
  for (n = 2; n <= nend; n++) {
    badd_small(&t, &X, n); d = bctz(&t); vpi += d; if (d > Menv) Menv = d;
    if (d >= prec - 8) { fprintf(stderr, "precision exhausted at n=%d\n", n); break; }
    big u, ui; bshr(&u, &t, d); binv(&ui, &u); int nprec = prec - d;
    int nn = 0;
    for (int i = 0; i < np; i++) for (int e = 0; e < 2; e++) {
      big y; badd_small(&y, &P0[i].g, e); bmask(&y, prec);
      if (d && bctz(&y) < d) continue;
      if (nn >= MAXP) { fprintf(stderr, "MAXP\n"); exit(1); }
      bshr(&y, &y, d); bmul(&P1[nn].g, &y, &ui); bmask(&P1[nn].g, nprec);
      P1[nn].B = P0[i].B + P1[nn].g.a[0] * pi_prev; P1[nn].cnt = P0[i].cnt; nn++; }
    // merge
    qsort(P1, nn, sizeof(part), cmpp);
    np = 0; for (int i = 0; i < nn; i++) { if (np && !bcmp_(&P0[np - 1].g, &P1[i].g) && P0[np - 1].B == P1[i].B) P0[np - 1].cnt += P1[i].cnt; else P0[np++] = P1[i]; }
    prec = nprec; pi_prev *= t.a[0];
    if (np == 0) break;
    if (stop_deep && d >= stop_deep) { n++; break; }
  }
  st->pop = 0; st->maxkap = -1; st->flat = 0; st->unstable = 0; st->vpi = vpi; st->M = Menv;
  for (int i = 0; i < np; i++) { int k = v64(P0[i].B); st->pop += P0[i].cnt; if (k > st->maxkap) st->maxkap = k;
    if (k >= vpi) st->flat += P0[i].cnt; if (vpi < 2 * k + Menv + 1) st->unstable += P0[i].cnt; }
  *outn = n - 1; return np;
}
int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  W = atoi(argv[2]); if (W > MAXW) return 1;
  if (!strcmp(argv[1], "rand")) {
    int nmax = atoi(argv[3]); long ns = atol(argv[4]); seedrng(strtoull(argv[5], 0, 10)); int w = argc > 6 ? atoi(argv[6]) : 0;
    int cps[] = {8, 16, 32, 64, 128, 256, 512, 1024, 2048}; int ncp = 9;
    for (long it = 0; it < ns; it++) {
      for (int i = 0; i < W; i++) X.a[i] = rng();
      if (w > 0) { big o; for (int i = 0; i < W; i++) o.a[i] = X.a[i]; o.a[0] |= 1; // X = -2 + 2^w * o
        big sh; memset(sh.a, 0, sizeof(sh.a)); int q = w / 64, s = w % 64; for (int i = W - 1; i >= 0; i--) { u64 lo = (i - q >= 0) ? o.a[i - q] : 0; u64 lo2 = (i - q - 1 >= 0) ? o.a[i - q - 1] : 0; sh.a[i] = s ? ((lo << s) | (lo2 >> (64 - s))) : lo; }
        badd_small(&X, &sh, -2); }
      else X.a[0] &= ~(u64)1;
      printf("sample %ld x0=%llu", it, (unsigned long long)(X.a[0] & 0xffff));
      for (int c = 0; c < ncp && cps[c] <= nmax; c++) { stats st; int on; run(cps[c], &st, &on, 0);
        printf(" | n=%d pop=%lld maxk=%d flat=%lld unst=%lld P=%d M=%d", cps[c], st.pop, st.maxkap, st.flat, st.unstable, st.vpi, st.M);
        if (st.pop == 0) break; }
      printf("\n"); fflush(stdout); }

  } else if (!strcmp(argv[1], "fixed")) {
    long long xv = atoll(argv[3]); int n1 = atoi(argv[4]), n2 = atoi(argv[5]);
    bset(&X, 0); badd_small(&X, &X, xv);
    for (int n = n1; n <= n2; n++) { stats st; int on; run(n, &st, &on, 0); printf("x=%lld n=%d pop=%lld P=%d maxk=%d\n", xv, n, st.pop, st.vpi, st.maxkap); }
  } else if (!strcmp(argv[1], "deep")) {
    int D = atoi(argv[3]); long ns = atol(argv[4]); seedrng(strtoull(argv[5], 0, 10));
    u64 cmask = argc > 7 ? strtoull(argv[6], 0, 10) : 1, cres = argc > 7 ? strtoull(argv[7], 0, 10) : 0;
    double sumN = 0, sumW = 0, sumW2 = 0; long surv = 0;
    for (long it = 0; it < ns; it++) {
      for (int i = 0; i < W; i++) X.a[i] = rng(); X.a[0] = (X.a[0] & ~cmask) | cres;
      stats st; int on; run(1 << (D + 1), &st, &on, D);
      // weight at stopping time: N * 2^{P - n}
      double wgt = st.pop ? ldexp((double)st.pop, st.vpi - on) : 0;
      sumN += st.pop; sumW += wgt; sumW2 += wgt * wgt; surv += st.pop > 0;
    }
    double mw = sumW / ns, se = sqrt((sumW2 / ns - mw * mw) / ns);
    printf("D=%d samples=%ld E[N_tau]=%.5f P(N_tau>0)=%.5f E[N_tau 2^{P-tau}]=%.4f (se %.4f)\n", D, ns, sumN / ns, (double)surv / ns, mw, se);
  }
  return 0;
}
