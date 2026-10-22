/* Independent exact class census delta_G(p) = p^{-G} #{c mod p^G : g_p(c) >= G}.
 *
 * Written from the definitions in note.md 1.2 / 3.1 only (no code reused from
 * archive/E or code/round4/M4D).  Used to re-derive the census inputs of
 * Corollary P1 (track M4D).
 *
 * g_p(x) >= G  iff  there is a finite B subset of {1,2,...} with
 *   1 + sum_{b in B} pi_b(x) == 0 mod p^G,   pi_b(x) = (x+1)...(x+b).
 * Decision procedure (exact): process b = 0,1,2,... with a "target"
 *   tau_n = -S_n / pi_n  mod p^{m_n},  m_n = G - V_n,  V_n = v(pi_n(x)),
 * where S_n is the partial sum over digits e_0..e_{n-1} (e_0 = 1 forced).
 * Step n -> n+1 with digit e_n in {0,1} (only 1 at n = 0):
 *   w = tau_n - e_n ;  d = v(x+n+1) ;
 *   if d >= m_n : success iff w == 0 mod p^{m_n} ;
 *   else need w == 0 mod p^d, and tau_{n+1} = (w/p^d) * u^{-1} mod p^{m_n - d},
 *        u = (x+n+1)/p^d.
 * This is a finite DFS (m_n strictly decreases at every multiple of p) with a
 * memo of dead states (n, tau).
 * Census by lifting: {g >= k} is a union of classes mod p^k and
 * {g >= k} subset {g >= k-1}, so only the p children of survivors at level k-1
 * need to be tested at level k.
 *
 * usage: census p Gmax            prints survivors per level
 *        census p G check         prints, for every class c mod p^G, 1/0 (for the brute-force validator)
 *        census p Gmax pmass n0   also tallies, at each level k, the survivors c (g(c) >= k) with
 *                                 V_{n0}(c) = k, which gives the exact Haar mass
 *                                 mu{P(x,n0)} = sum_k mu{V_{n0} = k, g >= k}  (truncated at k <= Gmax).
 *                                 On a class c mod p^k: if no c+i (i <= n0) is 0 mod p^k, V_{n0} is
 *                                 constant on the class; if exactly one is, V_{n0} = k exactly on the
 *                                 fraction (1-1/p) of the class iff all other v(c+j) = 0; if two or more
 *                                 are, V_{n0} >= 2k > k.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef int64_t i64;
typedef uint64_t u64;

static i64 P, PG, G;
static i64 pw[64];
static int NMAX;
static int dn[4096];        /* d_n = v(x+n+1), capped at G   (index n) */
static i64 uinv[4096];      /* inverse of (x+n+1)/p^{d_n} mod p^G      */

/* hash set of dead states, generation-stamped */
#define HBITS 22
#define HSIZE (1u << HBITS)
static u64 *hkey;
static uint32_t *hgen;
static uint32_t gen = 0;

static inline u64 hmix(u64 k) {
  k ^= k >> 33; k *= 0xff51afd7ed558ccdULL; k ^= k >> 33; k *= 0xc4ceb9fe1a85ec53ULL; k ^= k >> 33;
  return k;
}
static int hfind(u64 k) {
  u64 h = hmix(k) & (HSIZE - 1);
  while (hgen[h] == gen) {
    if (hkey[h] == k) return 1;
    h = (h + 1) & (HSIZE - 1);
  }
  return 0;
}
static long hcount;
static void hins(u64 k) {
  u64 h = hmix(k) & (HSIZE - 1);
  while (hgen[h] == gen) {
    if (hkey[h] == k) return;
    h = (h + 1) & (HSIZE - 1);
  }
  hgen[h] = gen; hkey[h] = k; hcount++;
  if (hcount > (long)(HSIZE * 0.7)) { fprintf(stderr, "hash table too full\n"); exit(2); }
}

static i64 modinv(i64 a, i64 m) { /* a unit mod m */
  i64 t = 0, nt = 1, r = m, nr = ((a % m) + m) % m;
  while (nr) {
    i64 q = r / nr, tmp;
    tmp = t - q * nt; t = nt; nt = tmp;
    tmp = r - q * nr; r = nr; nr = tmp;
  }
  if (r != 1) { fprintf(stderr, "not invertible\n"); exit(3); }
  return ((t % m) + m) % m;
}

static long nodes;

/* DFS from state (n, tau mod p^m). returns 1 if some continuation reaches valuation G */
static int dfs(int n, i64 tau, int m) {
  nodes++;
  if (n >= NMAX) { fprintf(stderr, "NMAX exceeded\n"); exit(4); }
  int d = dn[n];
  i64 pm = pw[m];
  for (int e = 1; e >= (n == 0 ? 1 : 0); e--) {
    i64 w = tau - e; if (w < 0) w += pm;
    if (d >= m) {
      if (w % pm == 0) return 1;
      continue;
    }
    if (w % pw[d] != 0) continue;
    int m2 = m - d;
    i64 pm2 = pw[m2];
    i64 t2 = (i64)(((__int128)((w / pw[d]) % pm2) * (uinv[n] % pm2)) % pm2);
    u64 key = (u64)(n + 1) * (u64)PG + (u64)t2;
    if (hfind(key)) continue;
    if (dfs(n + 1, t2, m2)) return 1;
    hins(key);
  }
  return 0;
}

/* decide g_p(x) >= G for x given mod p^G (0 <= x < p^G) */
static int decide(i64 x) {
  /* precompute d_n, uinv_n until V_n >= G */
  i64 V = 0; int n = 0;
  while (1) {
    if (n >= 4095) { fprintf(stderr, "too long\n"); exit(5); }
    i64 y = (x + n + 1) % PG;
    int d = 0;
    if (y == 0) d = (int)G;
    else { while (y % P == 0) { y /= P; d++; } }
    dn[n] = d;
    uinv[n] = (d >= G) ? 1 : modinv(y, PG);
    V += d; n++;
    if (V >= G) break;
  }
  NMAX = n + 1;
  gen++; hcount = 0;
  if (gen == 0) { memset(hgen, 0, sizeof(uint32_t) * HSIZE); gen = 1; }
  return dfs(0, 0, (int)G);
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
  P = atoll(argv[1]);
  int Gmax = atoi(argv[2]);
  int check = (argc > 3 && !strcmp(argv[3], "check"));
  int pmass = (argc > 4 && !strcmp(argv[3], "pmass")) ? atoi(argv[4]) : 0;
  double mass = 0.0; long double massl = 0.0L;
  pw[0] = 1; for (int i = 1; i < 64; i++) pw[i] = pw[i - 1] * P;
  hkey = malloc(sizeof(u64) * HSIZE); hgen = calloc(HSIZE, sizeof(uint32_t));
  if (check) {
    G = Gmax; PG = pw[G];
    for (i64 c = 0; c < PG; c++) printf("%lld %d\n", (long long)c, decide(c));
    return 0;
  }
  /* lifting census */
  i64 *cur = malloc(sizeof(i64)), *nxt;
  long ncur = 1; cur[0] = 0;
  printf("# census p=%lld levels 0..%d ; columns: G survivors density children-histogram(0..p)\n", (long long)P, Gmax);
  printf("0 1 1.0000000000\n");
  for (int k = 1; k <= Gmax; k++) {
    G = k; PG = pw[k];
    nxt = malloc(sizeof(i64) * (size_t)ncur * (size_t)P);
    long nn = 0; long hist[64] = {0}; nodes = 0; long vk = 0, vk_part = 0;
    for (long a = 0; a < ncur; a++) {
      int kept = 0;
      for (i64 j = 0; j < P; j++) {
        i64 x = cur[a] + j * pw[k - 1];
        if (decide(x)) {
          nxt[nn++] = x; kept++;
          if (pmass) {   /* mass of {V_{n0} == k} inside the class x mod p^k */
            long V = 0; int top = 0;
            for (int i = 1; i <= pmass; i++) {
              i64 y = (x + i) % PG; if (y == 0) { top++; continue; }
              while (y % P == 0) { y /= P; V++; }
            }
            if (!top && V == k) vk++;                 /* whole class */
            else if (top == 1 && V == 0) vk_part++;   /* fraction (1-1/p): v(x+i) == k exactly */
          }
        }
      }
      hist[kept]++;
    }
    printf("%d %ld %.10f", k, nn, (double)nn / (double)PG);
    for (int i = 0; i <= P; i++) printf(" %ld", hist[i]);
    printf("   [dfs nodes %ld]", nodes);
    if (pmass) { massl += ((long double)vk + (long double)vk_part * (1.0L - 1.0L / (long double)P)) / (long double)PG;
                 printf("  #{g>=k, V_%d=k}=%ld (+%ld partial)  partial mu{P(x,%d)} >= %.10Lf", pmass, vk, vk_part, pmass, massl); }
    printf("\n");
    fflush(stdout);
    free(cur); cur = nxt; ncur = nn;
  }
  return 0;
}
