/* Independent checker for the uniform covering certificates Cov(p,t,H)
 * (note.md 3.7 Definition; used by track M4D's Theorem P).
 *
 * Cov(p,t,H): for every unit K' mod p^c, c = v_p((H-1)!), the 2^H subset sums of
 *     y_i(K') = prod_{s=1}^{i} (p^t K' - (H-s)),   0 <= i < H   (y_0 = 1)
 * cover Z/p^{t+c}.
 *
 * Written from the definition only; shares no code with round-1/2 programs or
 * code/round4/M4D.  Method: the first E elements are enumerated explicitly
 * (2^E sums), the rest are applied by cyclic shift-OR on a bitset of p^{t+c} bits.
 *
 * usage: covchk p t H [mode] [arg]
 *   mode "all"          : every unit K' in [1,p^c)            (default)
 *   mode "one" K        : the single representative K (any integer, need not be < p^c)
 *   mode "lift" j       : every unit K' in [1,p^c), using the representative K' + j*p^c
 *   mode "dump" K       : print the missed residues for representative K (small cases)
 * prints one line per class and a summary line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef int64_t i64;
typedef unsigned __int128 u128;

static u64 Q;          /* modulus p^{t+c} */
static size_t NW;      /* words */
static u64 *S, *T;
static u64 lastmask;

static void set_bit(u64 *a, u64 i) { a[i >> 6] |= (1ULL << (i & 63)); }

/* dst |= src shifted towards higher positions by k bits (linear, bits >= Q dropped) */
static void or_shl(u64 *dst, const u64 *src, u64 k) {
  size_t w = k >> 6; unsigned b = k & 63;
  if (w >= NW) return;
  if (b == 0) {
    for (size_t i = NW; i-- > w;) dst[i] |= src[i - w];
  } else {
    for (size_t i = NW - 1; i > w; i--) dst[i] |= (src[i - w] << b) | (src[i - w - 1] >> (64 - b));
    dst[w] |= src[0] << b;
  }
  dst[NW - 1] &= lastmask;
}
/* dst |= src shifted towards lower positions by k bits (linear) */
static void or_shr(u64 *dst, const u64 *src, u64 k) {
  size_t w = k >> 6; unsigned b = k & 63;
  if (w >= NW) return;
  if (b == 0) {
    for (size_t i = 0; i + w < NW; i++) dst[i] |= src[i + w];
  } else {
    size_t i;
    for (i = 0; i + w + 1 < NW; i++) dst[i] |= (src[i + w] >> b) | (src[i + w + 1] << (64 - b));
    dst[i] |= src[i + w] >> b;     /* i + w == NW-1 */
  }
}
/* S <- S | rot(S, r)  (cyclic on Z/Q) */
static void rot_or(u64 r) {
  r %= Q;
  if (r == 0) return;
  memcpy(T, S, NW * sizeof(u64));
  or_shl(S, T, r);           /* j -> j + r for j + r < Q */
  or_shr(S, T, Q - r);       /* j -> j - (Q - r) for j >= Q - r */
}

static u64 count_missing(void) {
  u64 cnt = 0;
  for (size_t i = 0; i < NW; i++) cnt += __builtin_popcountll(S[i]);
  return Q - cnt;
}

static int vp(u64 n, u64 p) { int v = 0; while (n && n % p == 0) { n /= p; v++; } return v; }

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: covchk p t H [all|one K|lift j|dump K]\n"); return 1; }
  u64 p = strtoull(argv[1], 0, 10); int t = atoi(argv[2]); int H = atoi(argv[3]);
  const char *mode = argc > 4 ? argv[4] : "all";
  i64 arg = argc > 5 ? strtoll(argv[5], 0, 10) : 0;
  int c = 0; for (int s = 1; s <= H - 1; s++) c += vp(s, p);
  int M = t + c;
  u64 pc = 1; for (int i = 0; i < c; i++) pc *= p;
  u64 pt = 1; for (int i = 0; i < t; i++) pt *= p;
  Q = 1; for (int i = 0; i < M; i++) Q *= p;
  NW = (Q + 63) / 64;
  lastmask = (Q % 64) ? ((1ULL << (Q % 64)) - 1) : ~0ULL;
  S = malloc(NW * sizeof(u64)); T = malloc(NW * sizeof(u64));
  if (!S || !T) { fprintf(stderr, "alloc failed\n"); return 2; }
  int E = H < 22 ? H : 22;
  while (E > 1 && (1ULL << E) > Q / 4 + 1) E--;
  printf("# covchk p=%llu t=%d H=%d c=%d M=t+c=%d Q=p^M=%llu explicit=%d mode=%s\n",
         (unsigned long long)p, t, H, c, M, (unsigned long long)Q, E, mode);
  u64 *sums = malloc(sizeof(u64) << E);
  u64 y[256];
  long nclass = 0, nbad = 0; u64 worst = 0;
  clock_t t0 = clock();
  u64 Klo = 1, Khi = pc;   /* units K' in [1, p^c) ; for c = 0 the single class K'=1 */
  if (pc == 1) { Klo = 1; Khi = 2; }
  int single = (!strcmp(mode, "one") || !strcmp(mode, "dump"));
  if (single) { Klo = 0; Khi = 1; }
  for (u64 Kc = Klo; Kc < Khi; Kc++) {
    u64 K;
    if (single) K = (u64)arg;
    else {
      if (pc > 1 && Kc % p == 0) continue;
      K = Kc;
      if (!strcmp(mode, "lift")) K = Kc + (u64)arg * pc;
    }
    /* y_i(K) mod Q, X = p^t K mod Q */
    u64 X = (u64)(((u128)(pt % Q) * (K % Q)) % Q);
    y[0] = 1 % Q;
    for (int i = 1; i < H; i++) {
      u64 f = (X + Q - (u64)((H - i) % Q)) % Q;   /* p^t K - (H - s), s = i */
      y[i] = (u64)(((u128)y[i - 1] * f) % Q);
    }
    /* explicit sums of y[0..E-1] */
    sums[0] = 0;
    for (int i = 0; i < E; i++) {
      u64 n = 1ULL << i;
      for (u64 j = 0; j < n; j++) { u64 s = sums[j] + y[i]; if (s >= Q) s -= Q; sums[n + j] = s; }
    }
    memset(S, 0, NW * sizeof(u64));
    for (u64 j = 0; j < (1ULL << E); j++) set_bit(S, sums[j]);
    for (int i = E; i < H; i++) rot_or(y[i]);
    u64 miss = count_missing();
    nclass++;
    if (miss) nbad++;
    if (miss > worst) worst = miss;
    printf("K=%llu Kmodpc=%llu missing=%llu %s\n", (unsigned long long)K, (unsigned long long)(pc > 1 ? K % pc : 0),
           (unsigned long long)miss, miss ? "NOT_COVERED" : "covered");
    if (!strcmp(mode, "dump") && miss && miss < 1000) {
      for (u64 r = 0; r < Q; r++) if (!((S[r >> 6] >> (r & 63)) & 1)) printf("  missed %llu\n", (unsigned long long)r);
    }
    fflush(stdout);
  }
  printf("SUMMARY p=%llu t=%d H=%d c=%d classes=%ld not_covered=%ld worst_missing=%llu %s cpu=%.1fs\n",
         (unsigned long long)p, t, H, c, nclass, nbad, (unsigned long long)worst,
         nbad ? "COV_FAILS" : "ALL_COVERED", (double)(clock() - t0) / CLOCKS_PER_SEC);
  return 0;
}
