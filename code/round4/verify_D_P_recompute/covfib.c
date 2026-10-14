/* Fibred checker for Cov(p,t,H) (same definition as covchk.c), for moduli too
 * large for a single bitset (used for Cov(13,7,39), modulus 13^9).
 *
 * Split level k: "low" elements y_i with v_p(y_i) < k, "high" ones with v_p >= k.
 * For each residue rho mod p^k the fibre {s == rho mod p^k} of Z/p^M is identified
 * with Z/p^{M-k} via s -> (s - rho)/p^k.  The subset sums are
 *     (low sums) + (high sums),  high sums in p^k Z,
 * so the fibre rho is covered iff  F_rho + Sigma(high/p^k) = Z/p^{M-k},  where
 * F_rho = {(a - rho)/p^k : a a low subset sum, a == rho mod p^k}.
 * F_rho is built by a two-pass counting sort of all 2^{#low} low sums, then the
 * high elements are applied by cyclic shift-OR on a bitset of p^{M-k} bits.
 * Missing count = sum over fibres.  Validated against covchk.c (cov_fib_validate.log).
 *
 * usage: covfib p t H k [all|one K|range K0 K1]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64; typedef unsigned __int128 u128;

static u64 Q;  static size_t NW; static u64 *S, *T; static u64 lastmask;
static void or_shl(u64 *dst, const u64 *src, u64 k) {
  size_t w = k >> 6; unsigned b = k & 63; if (w >= NW) return;
  if (b == 0) { for (size_t i = NW; i-- > w;) dst[i] |= src[i - w]; }
  else { for (size_t i = NW - 1; i > w; i--) dst[i] |= (src[i - w] << b) | (src[i - w - 1] >> (64 - b)); dst[w] |= src[0] << b; }
  dst[NW - 1] &= lastmask;
}
static void or_shr(u64 *dst, const u64 *src, u64 k) {
  size_t w = k >> 6; unsigned b = k & 63; if (w >= NW) return;
  if (b == 0) { for (size_t i = 0; i + w < NW; i++) dst[i] |= src[i + w]; }
  else { size_t i; for (i = 0; i + w + 1 < NW; i++) dst[i] |= (src[i + w] >> b) | (src[i + w + 1] << (64 - b)); dst[i] |= src[i + w] >> b; }
}
static void rot_or(u64 r) { r %= Q; if (!r) return; memcpy(T, S, NW * 8); or_shl(S, T, r); or_shr(S, T, Q - r); }
static int vp(u64 n, u64 p) { int v = 0; if (!n) return 99; while (n % p == 0) { n /= p; v++; } return v; }

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: covfib p t H k [all|one K|range K0 K1]\n"); return 1; }
  u64 p = strtoull(argv[1], 0, 10); int t = atoi(argv[2]), H = atoi(argv[3]), k = atoi(argv[4]);
  const char *mode = argc > 5 ? argv[5] : "all";
  int c = 0; for (int s = 1; s < H; s++) c += vp(s, p);
  int M = t + c;
  u64 pc = 1, pt = 1, PM = 1, pk = 1;
  for (int i = 0; i < c; i++) pc *= p; for (int i = 0; i < t; i++) pt *= p;
  for (int i = 0; i < M; i++) PM *= p; for (int i = 0; i < k; i++) pk *= p;
  Q = PM / pk; NW = (Q + 63) / 64; lastmask = (Q % 64) ? ((1ULL << (Q % 64)) - 1) : ~0ULL;
  S = malloc(NW * 8); T = malloc(NW * 8);
  printf("# covfib p=%llu t=%d H=%d c=%d M=%d fibre level k=%d fibres=%llu fibre size=%llu mode=%s\n",
         (unsigned long long)p, t, H, c, M, k, (unsigned long long)pk, (unsigned long long)Q, mode);
  u64 K0 = 1, K1 = (pc > 1 ? pc : 2);
  if (!strcmp(mode, "one")) { K0 = strtoull(argv[6], 0, 10); K1 = K0 + 1; }
  if (!strcmp(mode, "range")) { K0 = strtoull(argv[6], 0, 10); K1 = strtoull(argv[7], 0, 10); }
  long ncl = 0, nbad = 0; u64 worst = 0; clock_t t0 = clock();
  uint32_t *buck = NULL; u64 *cnt = calloc(pk + 1, 8), *pos = calloc(pk + 1, 8);
  for (u64 K = K0; K < K1; K++) {
    if (pc > 1 && K % p == 0 && strcmp(mode, "one")) continue;
    u64 X = (u64)(((u128)(pt % PM) * (K % PM)) % PM);
    u64 y[256]; y[0] = 1 % PM;
    for (int i = 1; i < H; i++) y[i] = (u64)(((u128)y[i - 1] * ((X + PM - (u64)(H - i) % PM) % PM)) % PM);
    u64 lo[64], hi[256]; int nlo = 0, nhi = 0;
    for (int i = 0; i < H; i++) { if (vp(y[i], p) < k) lo[nlo++] = y[i]; else if (y[i]) hi[nhi++] = (y[i] / pk) % Q; }
    if (nlo > 30) { fprintf(stderr, "too many low elements (%d)\n", nlo); return 2; }
    u64 nsum = 1ULL << nlo;
    if (!buck) buck = malloc(sizeof(uint32_t) * nsum);
    /* pass 1: count low sums per residue mod p^k (Gray-code enumeration) */
    memset(cnt, 0, (pk + 1) * 8);
    u64 s = 0; cnt[0]++;
    for (u64 g = 1; g < nsum; g++) {
      int b = __builtin_ctzll(g);
      if ((g ^ (g >> 1)) >> b & 1) { s += lo[b]; if (s >= PM) s -= PM; } else { s += PM - lo[b]; if (s >= PM) s -= PM; }
      cnt[s % pk]++;
    }
    pos[0] = 0; for (u64 r = 0; r < pk; r++) pos[r + 1] = pos[r] + cnt[r];
    u64 *fill = malloc(pk * 8); memcpy(fill, pos, pk * 8);
    s = 0; buck[fill[0]++] = 0;
    for (u64 g = 1; g < nsum; g++) {
      int b = __builtin_ctzll(g);
      if ((g ^ (g >> 1)) >> b & 1) { s += lo[b]; if (s >= PM) s -= PM; } else { s += PM - lo[b]; if (s >= PM) s -= PM; }
      u64 r = s % pk; buck[fill[r]++] = (uint32_t)((s - r) / pk);
    }
    free(fill);
    u64 miss = 0;
    for (u64 r = 0; r < pk; r++) {
      memset(S, 0, NW * 8);
      for (u64 j = pos[r]; j < pos[r + 1]; j++) { u64 v = buck[j]; S[v >> 6] |= 1ULL << (v & 63); }
      for (int i = 0; i < nhi; i++) rot_or(hi[i]);
      u64 cntb = 0; for (size_t i = 0; i < NW; i++) cntb += __builtin_popcountll(S[i]);
      miss += Q - cntb;
      if (getenv("COVFIB_FIBRES") && cntb != Q) printf("  fibre r=%llu missing=%llu\n", (unsigned long long)r, (unsigned long long)(Q - cntb));
    }
    ncl++; if (miss) nbad++; if (miss > worst) worst = miss;
    printf("K=%llu Kmodpc=%llu low=%d high=%d missing=%llu %s\n", (unsigned long long)K, (unsigned long long)(pc > 1 ? K % pc : 0),
           nlo, nhi, (unsigned long long)miss, miss ? "NOT_COVERED" : "covered");
    fflush(stdout);
  }
  printf("SUMMARY p=%llu t=%d H=%d c=%d k=%d classes=%ld not_covered=%ld worst_missing=%llu %s cpu=%.1fs\n",
         (unsigned long long)p, t, H, c, k, ncl, nbad, (unsigned long long)worst, nbad ? "COV_FAILS" : "ALL_COVERED",
         (double)(clock() - t0) / CLOCKS_PER_SEC);
  return 0;
}
