/* wincheck2.c -- exact check of COVER(A,B) for long windows via one split A < M < B and
 * bitset intersections (handles dense hole sets near deep gates).
 *
 * COVER(A,B): subset sums of {n! : A <= n < B} hit every class of p^{e(A)}Z / p^{e(B)}Z.
 * Let j1 = e(M)-e(A), D = e(B)-e(M).  HB = holes of the W2=[M,B) sums (normalized by p^{e(M)})
 * in Z/p^D (exact bitset DP).  A class y = r + p^{j1} z (r mod p^{j1}, z mod p^D) is hit iff some
 * subset sum a = r + p^{j1} l of W1 = [A,M) (normalized by p^{e(A)}, taken mod p^{j1+D}) has
 * z - l not in HB.  So COVER(A,B) holds iff for every r: (i) class r is hit by W1 mod p^{j1} and
 * (ii) the intersection over all lifts l of (l + HB) is empty.  Lifts are capped at CAP per class;
 * if a class still has candidates after CAP lifts we report INCONCLUSIVE (never a false HOLDS).
 * All integer arithmetic exact.
 *
 * usage: wincheck2 p A M B UA [CAP]    (UA = unit part of A! mod p^{e(B)-e(A)}, decimal)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int P;
static u128 mulmod(u128 a, u128 b, u128 m) { u128 r = 0; a %= m; while (b) { if (b & 1) { r += a; if (r >= m) r -= m; } a <<= 1; if (a >= m) a -= m; b >>= 1; } return r; }
static u128 powp(int k) { u128 r = 1; for (int i = 0; i < k; i++) r *= P; return r; }

int main(int argc, char **argv) {
  if (argc < 6) { fprintf(stderr, "usage: wincheck2 p A M B UA [CAP]\n"); return 1; }
  P = atoi(argv[1]); long A = atol(argv[2]), M = atol(argv[3]), B = atol(argv[4]);
  int CAP = argc > 6 ? atoi(argv[6]) : 96;
  long *V = malloc(sizeof(long) * (B + 2)); V[0] = 0;
  for (long n = 1; n <= B + 1; n++) { long m = n, v = 0; while (m % P == 0) { m /= P; v++; } V[n] = V[n - 1] + v; }
  long Etot = V[B] - V[A], j1 = V[M] - V[A], D = V[B] - V[M];
  u128 MODBIG = powp((int)Etot);
  u128 ua = 0; for (const char *c = argv[5]; *c; c++) ua = ua * 10 + (u128)(*c - '0'); ua %= MODBIG;
  long nW = B - A; u128 *UN = malloc(sizeof(u128) * (nW + 1)); UN[0] = ua;
  for (long i = 1; i <= nW; i++) { long m = A + i; while (m % P == 0) m /= P; UN[i] = mulmod(UN[i - 1], (u128)m, MODBIG); }
  /* element n (A<=n<B) normalized by p^{e(base)} mod mod */
  #define ELEM(n, base, mod) ({ u128 _x = UN[(n) - A] % (mod); for (long _i = 0; _i < V[n] - V[base]; _i++) _x = mulmod(_x, (u128)P, (mod)); _x; })
  u64 PD = (u64)powp((int)D), PJ = (u64)powp((int)j1);
  u128 PJD = (u128)PJ * PD;
  if (PJD >= ((u128)1 << 63)) { fprintf(stderr, "p^(j1+D) too large\n"); return 1; }
  printf("# p=%d A=%ld M=%ld B=%ld  e(A)=%ld e(M)=%ld e(B)=%ld  j1=%ld D=%ld |W1|=%ld |W2|=%ld\n", P, A, M, B, V[A], V[M], V[B], j1, D, M - A, B - M);
  /* ---- W2 sums: bitset over Z/p^D ---- */
  u64 NWd = (PD + 63) / 64;
  u64 *S = calloc(NWd + 2, 8), *T = calloc(NWd + 2, 8), *U2 = calloc(NWd + 2, 8);
  S[0] = 1;
  for (long n = M; n < B; n++) {
    u64 w = (u64)ELEM(n, M, (u128)PD); if (w == 0) continue;
    /* T = S << w (mod PD bits), cyclic */
    u64 q = w >> 6, r = w & 63;
    for (u64 i = 0; i < NWd; i++) { u64 v = 0; if (i >= q) { v = S[i - q] << r; if (r && i >= q + 1) v |= S[i - q - 1] >> (64 - r); } T[i] = v; }
    if (PD & 63) T[NWd - 1] &= (((u64)1) << (PD & 63)) - 1;
    u64 sh = PD - w; q = sh >> 6; r = sh & 63;
    for (u64 i = 0; i < NWd; i++) { u64 v = 0; if (i + q < NWd) { v = S[i + q] >> r; if (r && i + q + 1 < NWd) v |= S[i + q + 1] << (64 - r); } U2[i] = v; }
    for (u64 i = 0; i < NWd; i++) S[i] |= T[i] | U2[i];
  }
  /* HB = complement; build doubled array HB2 (2*PD bits) for rotation reads */
  u64 nholes = 0;
  u64 *HB = calloc(NWd + 2, 8);
  for (u64 i = 0; i < NWd; i++) HB[i] = ~S[i];
  if (PD & 63) HB[NWd - 1] &= (((u64)1) << (PD & 63)) - 1;
  for (u64 i = 0; i < NWd; i++) nholes += __builtin_popcountll(HB[i]);
  printf("W2 sums: holes %llu of %llu (%.4f)\n", (unsigned long long)nholes, (unsigned long long)PD, (double)nholes / PD);
  free(T); free(U2);
  if (nholes == 0) {
    /* then COVER(A,B) holds iff W1 covers mod p^{j1} */
  }
  u64 NW2 = (2 * PD + 63) / 64 + 2;
  u64 *HB2 = calloc(NW2, 8);
  for (u64 b = 0; b < 2 * PD; b++) { u64 src = b % PD; if (HB[src >> 6] >> (src & 63) & 1) HB2[b >> 6] |= (u64)1 << (b & 63); }
  free(S);
  /* ---- W1 subset sums, bucket lifts per class ---- */
  long n1 = M - A; if (n1 > 36) { fprintf(stderr, "W1 too long\n"); return 1; }
  u64 *elo = malloc(8 * n1), *ehi = malloc(8 * n1);
  for (long i = 0; i < n1; i++) { u128 x = ELEM(A + i, A, PJD); elo[i] = (u64)(x % PJ); ehi[i] = (u64)(x / PJ); }
  u64 *lifts = malloc(sizeof(u64) * PJ * (u64)CAP); uint32_t *cnt = calloc(PJ, 4); unsigned char *over = calloc(PJ, 1);
  u64 lo = 0, hi = 0;
  for (u64 g = 0; g < ((u64)1 << n1); g++) {
    if (g) { int b = __builtin_ctzll(g); u64 gray = g ^ (g >> 1);
      if (gray >> b & 1) { lo += elo[b]; u64 c = 0; if (lo >= PJ) { lo -= PJ; c = 1; } hi += ehi[b] + c; if (hi >= PD) hi -= PD; if (hi >= PD) hi -= PD; }
      else { u64 bor = 0; if (lo >= elo[b]) lo -= elo[b]; else { lo = lo + PJ - elo[b]; bor = 1; } u64 sub = ehi[b] + bor; hi = (hi >= sub) ? hi - sub : hi + PD - sub; if (hi >= PD) hi -= PD; } }
    if (cnt[lo] < (uint32_t)CAP) {
      /* skip duplicate lifts */
      int dup = 0; for (uint32_t i = 0; i < cnt[lo]; i++) if (lifts[lo * CAP + i] == hi) { dup = 1; break; }
      if (!dup) lifts[lo * CAP + cnt[lo]++] = hi;
    } else over[lo] = 1;
  }
  u64 unseen = 0; for (u64 r = 0; r < PJ; r++) if (!cnt[r]) unseen++;
  if (unseen) { printf("W1 misses %llu classes mod p^%ld -> RESULT: COVER(%ld,%ld) FAILS (whole cosets)\n", (unsigned long long)unseen, j1, A, B); return 0; }
  if (nholes == 0) { printf("RESULT: COVER(%ld,%ld) HOLDS\n", A, B); return 0; }
  /* ---- sparse mode: difference set of holes (exact) ---- */
  if (!getenv("DENSE") && (getenv("SPARSE") || nholes <= 60000)) {
    u64 nh = nholes; u64 *hl = malloc(8 * nh); u64 c0 = 0;
    for (u64 i = 0; i < NWd; i++) { u64 w = HB[i]; while (w) { int b = __builtin_ctzll(w); hl[c0++] = i * 64 + b; w &= w - 1; } }
    u64 *DL = calloc(NWd + 2, 8);
    for (u64 a = 0; a < nh; a++) for (u64 b = 0; b < nh; b++) { u64 d = hl[b] >= hl[a] ? hl[b] - hl[a] : hl[b] + PD - hl[a]; DL[d >> 6] |= (u64)1 << (d & 63); }
    u64 dcount = 0; for (u64 i = 0; i < NWd; i++) dcount += __builtin_popcountll(DL[i]);
    printf("difference set density %.4f\n", (double)dcount / PD);
    u64 bad = 0, inc = 0, holes_found = 0, slow = 0;
    for (u64 r = 0; r < PJ; r++) {
      uint32_t k = cnt[r]; int covered = 0;
      for (uint32_t i = 0; i < k && !covered; i++) for (uint32_t j = i + 1; j < k; j++) {
        u64 a = lifts[r * CAP + i], b = lifts[r * CAP + j]; u64 d = b >= a ? b - a : b + PD - a;
        if (!(DL[d >> 6] >> (d & 63) & 1)) { covered = 1; break; } }
      if (covered) continue;
      slow++;
      /* explicit candidates z = l0 + h, keep if z - l_i in HB for all i */
      u64 l0 = lifts[r * CAP]; u64 nc = 0;
      for (u64 t = 0; t < nh; t++) {
        u64 z = l0 + hl[t]; if (z >= PD) z -= PD; int ok = 1;
        for (uint32_t i = 1; i < k; i++) { u64 l = lifts[r * CAP + i]; u64 y = z >= l ? z - l : z + PD - l; if (!(HB[y >> 6] >> (y & 63) & 1)) { ok = 0; break; } }
        if (ok) nc++;
      }
      if (nc) { if (over[r]) inc++; else { bad++; holes_found += nc; } }
    }
    printf("sparse mode: classes %llu, slow-path classes %llu, classes with holes %llu (holes %llu), inconclusive %llu\n", (unsigned long long)PJ, (unsigned long long)slow, (unsigned long long)bad, (unsigned long long)holes_found, (unsigned long long)inc);
    if (bad) printf("RESULT: COVER(%ld,%ld) FAILS: %llu holes\n", A, B, (unsigned long long)holes_found);
    else if (inc) printf("RESULT: INCONCLUSIVE (raise CAP)\n");
    else printf("RESULT: COVER(%ld,%ld) HOLDS\n", A, B);
    return 0;
  }
  /* ---- per class intersection (dense bitset phase, then sparse list phase) ---- */
  u64 *C = malloc(8 * (NWd + 2));
  u64 *lst = malloc(8 * (NWd + 64)); /* sparse candidates (switch when popcount < NWd) */
  u64 badcls = 0, inconc = 0, totalcand = 0; u64 maxused = 0;
  for (u64 r = 0; r < PJ; r++) {
    uint32_t k = cnt[r]; int empty = 0; u64 used = 0; int sparse = 0; u64 nl = 0;
    for (uint32_t t = 0; t < k; t++) {
      u64 l = lifts[r * CAP + t];
      used = t + 1;
      if (sparse) {
        u64 w2 = 0;
        for (u64 i = 0; i < nl; i++) { u64 z = lst[i]; u64 y = z >= l ? z - l : z + PD - l; if (HB[y >> 6] >> (y & 63) & 1) lst[w2++] = z; }
        nl = w2; if (!nl) { empty = 1; break; }
        continue;
      }
      /* bit y of rot = HB[(y - l) mod PD] = HB2[y - l + PD] ; start offset s0 = PD - l */
      u64 s0 = PD - l; if (s0 == PD) s0 = 0;
      u64 q = s0 >> 6, rr = s0 & 63;
      for (u64 i = 0; i < NWd; i++) {
        u64 w = HB2[q + i] >> rr; if (rr) w |= HB2[q + i + 1] << (64 - rr);
        if (t == 0) C[i] = w; else C[i] &= w;
      }
      if (PD & 63) { C[NWd - 1] &= (((u64)1) << (PD & 63)) - 1; }
      if (t > 0) {
        u64 pc = 0; for (u64 i = 0; i < NWd; i++) pc += __builtin_popcountll(C[i]);
        if (!pc) { empty = 1; break; }
        if (pc < NWd) { /* switch to sparse */
          nl = 0; for (u64 i = 0; i < NWd; i++) { u64 w = C[i]; while (w) { int b = __builtin_ctzll(w); lst[nl++] = i * 64 + b; w &= w - 1; } }
          sparse = 1;
        }
      }
    }
    if (used > maxused) maxused = used;
    if (!empty) {
      u64 c = 0;
      if (sparse) c = nl; else for (u64 i = 0; i < NWd; i++) c += __builtin_popcountll(C[i]);
      if (c == 0) continue;
      if (over[r]) inconc++; else { badcls++; totalcand += c;
        if (getenv("PRINTHOLES") && c <= 1000000) {
          if (sparse) { for (u64 i = 0; i < nl; i++) printf("HOLE r=%llu z=%llu\n", (unsigned long long)r, (unsigned long long)lst[i]); }
          else { for (u64 i = 0; i < NWd; i++) { u64 w = C[i]; while (w) { int b = __builtin_ctzll(w); printf("HOLE r=%llu z=%llu\n", (unsigned long long)r, (unsigned long long)(i * 64 + b)); w &= w - 1; } } }
        } }
    }
  }
  printf("classes: %llu, max lifts used %llu, classes with holes %llu (holes %llu), inconclusive %llu\n", (unsigned long long)PJ, (unsigned long long)maxused, (unsigned long long)badcls, (unsigned long long)totalcand, (unsigned long long)inconc);
  if (badcls) printf("RESULT: COVER(%ld,%ld) FAILS: %llu holes\n", A, B, (unsigned long long)totalcand);
  else if (inconc) printf("RESULT: INCONCLUSIVE (raise CAP)\n");
  else printf("RESULT: COVER(%ld,%ld) HOLDS\n", A, B);
  return 0;
}
