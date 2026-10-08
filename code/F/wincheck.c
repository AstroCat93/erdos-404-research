/* wincheck.c -- exact meet-in-the-middle check of Tao's window-covering condition
 *
 *   COVER(A,B):  { sum_{n in S} n! : S subset [A,B) }  hits every class of p^{e(A)} Z / p^{e(B)} Z,
 *   e(x) = v_p(x!).   (Equivalently: the tail set E_A = closure of sums over subsets of [A,inf)
 *   satisfies E_A mod p^{e(B)} = p^{e(A)}Z/p^{e(B)}Z.)
 *
 * Method ("hole propagation"): pick A = M_0 < M_1 < ... < M_t < B.  Let H_k = set of residues of
 * p^{e(M_k)}Z/p^{e(B)}Z NOT hit by sums over [M_k, B) ("holes", stored relative to p^{e(M_k)}).
 *  - H_t is computed by an exact bitset DP over Z/p^{e(B)-e(M_t)} (elements M_t <= n < B).
 *  - H_k from H_{k+1}: with W=[M_k,M_{k+1}), j=e(M_{k+1})-e(M_k), D=e(B)-e(M_{k+1}):
 *      y = r + p^j z  (r mod p^j, z mod p^D) is a hole of [M_k,B) iff for every subset sum a of W
 *      with a == r (mod p^j), writing a = r + p^j l (l mod p^D), we have z - l in H_{k+1}.
 *    We enumerate all 2^|W| subset sums (Gray code) and intersect candidate sets per class r.
 *  - COVER(A,B) holds iff H_0 is empty.
 * All arithmetic is exact (unsigned 64/128-bit integers).  No floating point.
 *
 * usage: wincheck p A B step [tailmaxexp]
 *   sub-boundaries M_k = A + k*step while e(B) - e(M_k) > tailmaxexp ... (see code)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef uint64_t u64;

static int P;
static u128 mulmod(u128 a, u128 b, u128 m) { /* (a*b) mod m, m < 2^126 */
  u128 r = 0; a %= m;
  while (b) { if (b & 1) { r += a; if (r >= m) r -= m; } a <<= 1; if (a >= m) a -= m; b >>= 1; }
  return r;
}
static u128 powp(int k) { u128 r = 1; for (int i = 0; i < k; i++) r *= P; return r; }
static long *V; /* V[n] = v_p(n!) */
static long vp_l(long n) { long v = 0; while (n % P == 0) { n /= P; v++; } return v; }

/* ---- hash set of u128 ---- */
typedef struct { u128 *key; char *used; u64 cap; u64 n; } hset;
static u64 hh(u128 x) { u64 a = (u64)x, b = (u64)(x >> 64); a ^= b * 0x9E3779B97F4A7C15ULL; a ^= a >> 29; a *= 0xBF58476D1CE4E5B9ULL; a ^= a >> 32; return a; }
static void hs_init(hset *h, u64 n) { u64 c = 16; while (c < 2 * n + 16) c <<= 1; h->cap = c; h->n = 0; h->key = malloc(sizeof(u128) * c); h->used = calloc(c, 1); }
static void hs_add(hset *h, u128 x) { u64 i = hh(x) & (h->cap - 1); while (h->used[i]) { if (h->key[i] == x) return; i = (i + 1) & (h->cap - 1); } h->used[i] = 1; h->key[i] = x; h->n++; }
static int hs_has(const hset *h, u128 x) { u64 i = hh(x) & (h->cap - 1); while (h->used[i]) { if (h->key[i] == x) return 1; i = (i + 1) & (h->cap - 1); } return 0; }
static void hs_free(hset *h) { free(h->key); free(h->used); }

/* unit part of n! modulo MODBIG (u128) for n in [0, B] */
static u128 *UN; static u128 MODBIG;

/* element value n!/p^{e(base)} mod m  (requires V[n] >= V[base]) */
static u128 elem(long n, long base, u128 m) {
  u128 x = UN[n] % m; long rel = V[n] - V[base];
  for (long i = 0; i < rel; i++) x = mulmod(x, (u128)P, m);
  return x;
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: wincheck p A B step [tailmaxexp=16]\n"); return 1; }
  P = atoi(argv[1]); long A = atol(argv[2]), B = atol(argv[3]), step = atol(argv[4]);
  int tailmax = argc > 5 ? atoi(argv[5]) : 16;
  V = malloc(sizeof(long) * (B + 2)); V[0] = 0; for (long n = 1; n <= B + 1; n++) V[n] = V[n - 1] + vp_l(n);
  long Etot = V[B] - V[A];
  /* choose MODBIG = p^{Etot} (must be < 2^126) */
  if ((double)Etot * __builtin_log((double)P) > 125 * 0.6931) { fprintf(stderr, "Etot=%ld too large for u128\n", Etot); return 1; }
  MODBIG = powp((int)Etot);
  UN = malloc(sizeof(u128) * (B + 2)); UN[0] = 1;
  if (argc > 6) { /* unit part of A! mod p^{Etot} supplied (decimal) */
    u128 ua = 0; for (const char *c = argv[6]; *c; c++) ua = ua * 10 + (u128)(*c - '0');
    UN[A] = ua % MODBIG;
    for (long n = A + 1; n <= B; n++) { long m = n; while (m % P == 0) m /= P; UN[n] = mulmod(UN[n - 1], (u128)m, MODBIG); }
  } else {
    for (long n = 1; n <= B; n++) { long m = n; while (m % P == 0) m /= P; UN[n] = mulmod(UN[n - 1], (u128)m, MODBIG); }
  }
  /* boundaries */
  long Mk[100000]; int t = 0; Mk[0] = A;
  if (getenv("BOUNDS")) { /* explicit boundaries: comma list starting with A */
    const char *c = getenv("BOUNDS"); t = -1;
    while (*c) { long x = strtol(c, (char **)&c, 10); Mk[++t] = x; if (*c == ',') c++; }
    if (Mk[0] != A) { fprintf(stderr, "BOUNDS must start with A\n"); return 1; }
  } else
  { /* tail start Mt: smallest M = A + kp < B with e(B)-e(M) <= tailmax (largest admissible tail) */
    long Mt = A; while (Mt + P < B && V[B] - V[Mt] > tailmax) Mt += P;
    while (Mk[t] + step < Mt) { Mk[t + 1] = Mk[t] + step; t++; }
    if (Mt > Mk[t]) Mk[++t] = Mt;
  }
  /* advance M_t forward while tail exponent too big? we require e(B)-e(M_t) <= tailmax */
  if (V[B] - V[Mk[t]] > tailmax) { fprintf(stderr, "tail exponent %ld > %d; choose different step\n", V[B] - V[Mk[t]], tailmax); return 1; }
  printf("# p=%d A=%ld B=%ld e(A)=%ld e(B)=%ld jump=%ld ; boundaries:", P, A, B, V[A], V[B], Etot);
  for (int k = 0; k <= t; k++) printf(" %ld", Mk[k]); printf("\n");
  /* --- exact bitset for tail [M_t, B) --- */
  long Dt = V[B] - V[Mk[t]]; u64 MT = (u64)powp((int)Dt);
  unsigned char *S = calloc(MT, 1), *T = malloc(MT); S[0] = 1;
  for (long n = Mk[t]; n < B; n++) {
    u64 w = (u64)elem(n, Mk[t], (u128)MT);
    memcpy(T, S, MT);
    u64 i = 0, jx = w; for (; jx < MT; i++, jx++) S[jx] |= T[i]; for (jx = 0; i < MT; i++, jx++) S[jx] |= T[i];
  }
  hset H; u64 nh = 0; for (u64 r = 0; r < MT; r++) nh += !S[r];
  hs_init(&H, nh); for (u64 r = 0; r < MT; r++) if (!S[r]) hs_add(&H, (u128)r);
  printf("tail [%ld,%ld): D=%ld, holes=%llu of %llu\n", Mk[t], B, Dt, (unsigned long long)H.n, (unsigned long long)MT);
  { const char *hm = getenv("HMAX"); u64 HMAXv = hm ? strtoull(hm, NULL, 10) : 300000ULL;
    if (t > 0 && H.n > HMAXv) { printf("RESULT: INCONCLUSIVE (tail hole set %llu > HMAX)\n", (unsigned long long)H.n); return 0; } }
  free(S); free(T); fflush(stdout);
  long D = Dt;
  for (int k = t - 1; k >= 0; k--) {
    long a0 = Mk[k], a1 = Mk[k + 1];
    long j = V[a1] - V[a0]; int nW = (int)(a1 - a0);
    u64 PJc = (u64)powp((int)j); u128 PD = powp((int)D);
    if (H.n == 0) {
      /* holes of [a0,B) = classes mod p^j not hit by sums of W (each a full coset) */
      unsigned char *hit = calloc(PJc, 1);
      /* enumerate sums mod p^j */
      u64 *el = malloc(8 * nW); for (int i = 0; i < nW; i++) el[i] = (u64)elem(a0 + i, a0, (u128)PJc);
      u64 s = 0; hit[0] = 1;
      for (u64 g = 1; g < ((u64)1 << nW); g++) { int b = __builtin_ctzll(g); u64 gray = g ^ (g >> 1); if (gray >> b & 1) { s += el[b]; if (s >= PJc) s -= PJc; } else { s += PJc - el[b]; if (s >= PJc) s -= PJc; } hit[s] = 1; }
      u64 miss = 0; for (u64 r = 0; r < PJc; r++) miss += !hit[r];
      printf("step [%ld,%ld): j=%ld, no incoming holes; classes missed = %llu of %llu\n", a0, a1, j, (unsigned long long)miss, (unsigned long long)PJc);
      if (miss) {
        if (k == 0) { printf("RESULT: COVER(%ld,%ld) FAILS (whole classes missed)\n", A, B); return 0; }
        const char *hm = getenv("HMAX"); u64 HMAXv = hm ? strtoull(hm, NULL, 10) : 300000ULL;
        if ((double)miss * (double)PD > (double)HMAXv) { printf("RESULT: INCONCLUSIVE (whole cosets missed at intermediate boundary %ld)\n", a0); return 0; }
        hset H2; hs_init(&H2, (u64)(miss * (u64)PD) + 1);
        for (u64 r = 0; r < PJc; r++) if (!hit[r]) for (u128 z = 0; z < PD; z++) hs_add(&H2, (u128)r + (u128)PJc * z);
        hs_free(&H); H = H2;
        printf("   -> holes now %llu (whole cosets)\n", (unsigned long long)H.n);
      }
      free(hit); free(el);
      D += j; continue;
    }
    if (nW > 34) { fprintf(stderr, "window too long\n"); return 1; }
    if ((double)H.n * (double)PJc > 4e9) { printf("RESULT: INCONCLUSIVE (work bound: holes %llu x classes %llu)\n", (unsigned long long)H.n, (unsigned long long)PJc); return 0; }
    /* per-class state */
    u128 *l0 = malloc(sizeof(u128) * PJc); unsigned char *st = calloc(PJc, 1); /* 0 = unseen, 1 = seen once (candidates implicit l0+H), 2 = explicit list, 3 = dead */
    u128 **cand = calloc(PJc, sizeof(u128 *)); int *ncand = calloc(PJc, sizeof(int));
    /* elements split as (lo mod p^j, hi = floor(x/p^j) mod p^D) */
    u64 *elo = malloc(8 * nW); u128 *ehi = malloc(sizeof(u128) * nW);
    u128 PJD = (u128)PJc * PD;
    for (int i = 0; i < nW; i++) { u128 x = elem(a0 + i, a0, PJD); elo[i] = (u64)(x % PJc); ehi[i] = x / PJc; }
    /* collect the hole list as array for iteration */
    u128 *Hl = malloc(sizeof(u128) * H.n); { u64 c = 0; for (u64 i = 0; i < H.cap; i++) if (H.used[i]) Hl[c++] = H.key[i]; }
    u64 lo = 0; u128 hi = 0;
    for (u64 g = 0; g < ((u64)1 << nW); g++) {
      if (g) {
        int b = __builtin_ctzll(g); u64 gray = g ^ (g >> 1);
        if (gray >> b & 1) { lo += elo[b]; u128 c = 0; if (lo >= PJc) { lo -= PJc; c = 1; } hi += ehi[b] + c; while (hi >= PD) hi -= PD; }
        else { u128 bor = 0; if (lo >= elo[b]) lo -= elo[b]; else { lo = lo + PJc - elo[b]; bor = 1; } u128 sub = ehi[b] + bor; hi = (hi >= sub) ? hi - sub : hi + PD - sub; while (hi >= PD) hi -= PD; }
      }
      unsigned char s = st[lo];
      if (s == 3) continue;
      if (s == 0) { st[lo] = 1; l0[lo] = hi; continue; }
      if (s == 1) {
        /* materialize candidates z = l0 + h with z - hi in H */
        int cnt = 0, capc = 0; u128 *lst = NULL;
        for (u64 i = 0; i < H.n; i++) { u128 z = l0[lo] + Hl[i]; if (z >= PD) z -= PD; u128 d = (z >= hi) ? z - hi : z + PD - hi; if (hs_has(&H, d)) { if (cnt == capc) { capc = capc ? 2 * capc : 4; lst = realloc(lst, sizeof(u128) * capc); } lst[cnt++] = z; } }
        if (cnt == 0) { st[lo] = 3; free(lst); } else { st[lo] = 2; cand[lo] = lst; ncand[lo] = cnt; }
        continue;
      }
      /* s == 2: filter */
      { int c = ncand[lo], w = 0; u128 *lst = cand[lo];
        for (int i = 0; i < c; i++) { u128 z = lst[i]; u128 d = (z >= hi) ? z - hi : z + PD - hi; if (hs_has(&H, d)) lst[w++] = z; }
        if (w == 0) { st[lo] = 3; free(lst); cand[lo] = NULL; ncand[lo] = 0; } else ncand[lo] = w; }
    }
    /* build new hole set: relative value y = r + p^j z, modulus p^{D+j} */
    u64 newn = 0, unseen = 0, single = 0;
    for (u64 r = 0; r < PJc; r++) { if (st[r] == 0) unseen++; else if (st[r] == 1) { single++; newn += H.n; } else if (st[r] == 2) newn += ncand[r]; }
    if (unseen) {
      printf("step [%ld,%ld): j=%ld, %llu classes unseen -> whole cosets missed\n", a0, a1, j, (unsigned long long)unseen);
      if (k == 0) { printf("RESULT: COVER(%ld,%ld) FAILS\n", A, B); return 0; }
      newn += unseen * (u64)PD;
    }
    { const char *hm = getenv("HMAX"); u64 HMAXv = hm ? strtoull(hm, NULL, 10) : 300000ULL;
      if (k > 0 && newn > HMAXv) { printf("RESULT: INCONCLUSIVE (hole set %llu > HMAX at boundary %ld)\n", (unsigned long long)newn, a0); return 0; } }
    hset H2; hs_init(&H2, newn + 1);
    for (u64 r = 0; r < PJc; r++) {
      if (st[r] == 1) { for (u64 i = 0; i < H.n; i++) { u128 z = l0[r] + Hl[i]; if (z >= PD) z -= PD; hs_add(&H2, (u128)r + (u128)PJc * z); } }
      else if (st[r] == 2) { for (int i = 0; i < ncand[r]; i++) hs_add(&H2, (u128)r + (u128)PJc * cand[r][i]); free(cand[r]); }
      else if (st[r] == 0) { for (u128 z = 0; z < PD; z++) hs_add(&H2, (u128)r + (u128)PJc * z); }
    }
    printf("step [%ld,%ld): j=%ld, |W|=%d, incoming holes=%llu -> holes=%llu (classes seen once: %llu)\n", a0, a1, j, nW, (unsigned long long)H.n, (unsigned long long)H2.n, (unsigned long long)single);
    fflush(stdout);
    hs_free(&H); H = H2; free(l0); free(st); free(cand); free(ncand); free(elo); free(ehi); free(Hl);
    D += j;
  }
  if (H.n == 0) printf("RESULT: COVER(%ld,%ld) HOLDS: sums of distinct n!, %ld<=n<%ld, hit every class of p^%ld Z / p^%ld Z\n", A, B, A, B, V[A], V[B]);
  else printf("RESULT: COVER(%ld,%ld) FAILS: %llu holes in p^%ld Z / p^%ld Z\n", A, B, (unsigned long long)H.n, V[A], V[B]);
  return 0;
}
