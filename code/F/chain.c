/* chain.c -- rigorous (exact integer) verification of Tao's gate-covering chains.
 *
 * Blocks: block m = { pm, pm+1, ..., pm+p-1 } (all have v_p(n!) = e_m := v_p((pm)!)).
 * A window = blocks m, m+1, ..., m'-1, i.e. the integers [pm, pm').  Its jump is
 * J = e_{m'} - e_m.  The window COVERS if the 2^{p(m'-m)} subset sums of
 * { n!/p^{e_m} : pm <= n < pm' } hit every residue class mod p^J.
 * Tao's lemma: if [N0, pm) is reachable (sums over [N0,pm) cover p^{e(N0)}Z/p^{e_m}) and the
 * window [pm, pm') covers, then [N0, pm') is reachable.  We compute reach[] by DP
 * (shortest covering window first), starting from reach[M0] = true.
 *
 * Output: for each m' the window used (or failure), and the summary.  Everything is exact
 * modular integer arithmetic (bitset over Z/p^J), so a "reached" G = pm' is a proof that
 * every element of p^{e(N0)} Z_p is congruent mod p^{e(G)} to a sum of distinct n!, N0 <= n < G.
 *
 * usage: chain p M0 Mmax JMAX LMAX [verbose]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned __int128 u128;

static uint64_t *S, *T; static uint64_t NWORDS, MBITS;

static void shl(const uint64_t *in, uint64_t *out, uint64_t sh) { /* out = in << sh (truncated to NWORDS words) */
  uint64_t q = sh >> 6, r = sh & 63;
  for (uint64_t i = 0; i < NWORDS; i++) {
    uint64_t v = 0;
    if (i >= q) { v = in[i - q] << r; if (r && i >= q + 1) v |= in[i - q - 1] >> (64 - r); }
    out[i] = v;
  }
}
static void shr(const uint64_t *in, uint64_t *out, uint64_t sh) { /* out = in >> sh */
  uint64_t q = sh >> 6, r = sh & 63;
  for (uint64_t i = 0; i < NWORDS; i++) {
    uint64_t v = 0;
    if (i + q < NWORDS) { v = in[i + q] >> r; if (r && i + q + 1 < NWORDS) v |= in[i + q + 1] << (64 - r); }
    out[i] = v;
  }
}
static uint64_t *TMP;
static void addshift(uint64_t w) { /* S |= rot(S, w) over MBITS bits */
  if (w == 0) return;
  shl(S, T, w);                 /* bits i -> i+w (those >= MBITS must be cleared) */
  /* clear bits >= MBITS in T */
  uint64_t lastbits = MBITS & 63;
  if (lastbits) T[NWORDS - 1] &= ((uint64_t)1 << lastbits) - 1;
  shr(S, TMP, MBITS - w);       /* bits i >= MBITS-w -> i-(MBITS-w) */
  for (uint64_t i = 0; i < NWORDS; i++) S[i] |= T[i] | TMP[i];
}
static int full(void) {
  uint64_t c = 0; for (uint64_t i = 0; i < NWORDS; i++) c += __builtin_popcountll(S[i]);
  return c == MBITS;
}

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: chain p M0 Mmax JMAX LMAX [verbose]\n"); return 1; }
  int p = atoi(argv[1]); long M0 = atol(argv[2]), Mmax = atol(argv[3]); int JMAX = atoi(argv[4]), LMAX = atoi(argv[5]);
  int verbose = argc > 6 ? atoi(argv[6]) : 0;
  uint64_t PJ = 1; for (int i = 0; i < JMAX; i++) PJ *= p;
  long Nmax = p * Mmax + p;
  /* U[n] = unit part of n! mod p^JMAX, V[n] = v_p(n!) */
  uint64_t *U = malloc(sizeof(uint64_t) * (Nmax + 1)); long *V = malloc(sizeof(long) * (Nmax + 1));
  U[0] = 1 % PJ; V[0] = 0;
  for (long n = 1; n <= Nmax; n++) { long m = n; long v = 0; while (m % p == 0) { m /= p; v++; } V[n] = V[n - 1] + v; U[n] = (uint64_t)(((u128)U[n - 1] * (uint64_t)(m % PJ)) % PJ); }
  uint64_t maxbits = PJ; uint64_t maxwords = (maxbits + 63) / 64 + 2;
  S = malloc(8 * maxwords); T = malloc(8 * maxwords); TMP = malloc(8 * maxwords);
  char *reach = calloc(Mmax + 2, 1); reach[M0] = 1;
  long firstfail = -1, lastreach = M0; long nfail = 0;
  double lp = log((double)p), l2 = log(2.0);
  for (long mp = M0 + 1; mp <= Mmax; mp++) {
    int ok = 0; long used = -1; long usedJ = -1; int toolarge = 0;
    for (int L = 1; L <= LMAX; L++) {
      long m = mp - L; if (m < M0) break;
      long J = V[p * mp] - V[p * m];
      if (J > JMAX) { toolarge = 1; break; }
      if (!reach[m]) continue;
      if ((double)(p * L) * l2 < (double)J * lp) continue; /* counting: cannot cover */
      uint64_t PM = 1; for (int i = 0; i < J; i++) PM *= p;
      MBITS = PM; NWORDS = (PM + 63) / 64;
      memset(S, 0, 8 * NWORDS); S[0] = 1;
      for (long n = p * m; n < p * mp; n++) {
        long rel = V[n] - V[p * m];
        uint64_t w = U[n] % PM; for (long i = 0; i < rel; i++) w = (uint64_t)(((u128)w * p) % PM);
        addshift(w);
      }
      if (full()) { ok = 1; used = m; usedJ = J; break; }
    }
    reach[mp] = ok;
    if (ok) { lastreach = mp; if (verbose) printf("reach m'=%ld (G=%ld, e=%ld) via window from m=%ld (L=%ld blocks, J=%ld)\n", mp, p * mp, V[p * mp], used, mp - used, usedJ); }
    else { nfail++; if (firstfail < 0) firstfail = mp; printf("FAIL m'=%ld (G=%ld, v_p(G)=%d, e=%ld)%s\n", mp, p * mp, (int)(V[p*mp]-V[p*mp-1]), V[p * mp], toolarge ? " [hit JMAX]" : ""); fflush(stdout); if (nfail > 20) break; }
  }
  printf("SUMMARY p=%d N0=%ld e(N0)=%ld : first unreachable G=%ld ; last reachable G=%ld with e(G)=%ld\n", p, p * M0, V[p * M0], firstfail >= 0 ? p * firstfail : -1, p * lastreach, V[p * lastreach]);
  return 0;
}
