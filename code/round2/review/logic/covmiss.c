/* Referee's independent coverage counter (third implementation, shares no code with fibcov/fibcov2/cov.c).
   Usage: covmiss p t H K   -> counts residues mod p^(t+c) NOT hit by subset sums of
          y_i = prod_{s=1..i} (p^t K - (H-s)), 0<=i<H, c = v_p((H-1)!).
   Method: units U (v=0) and non-units (all divisible by p). Bitset S' over Z/p^(M-1) of subset sums of
   the non-units divided by p (cyclic shift-or DP); then for each first digit t0 the fibre is the union of
   translates S' + (a-t0)/p over unit subset sums a == t0 (mod p).  Prints missing count and up to 10 misses. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 Lbits, Nw;

static inline u64 get64(const u64 *a, long long pos) { /* bits pos..pos+63 of a (zero outside [0,Lbits)) */
  u64 r = 0;
  if (pos >= (long long)Lbits || pos <= -64) return 0;
  if (pos < 0) { u64 w0 = a[0]; r = w0 << (-pos); }
  else {
    u64 wi = (u64)pos >> 6, sh = (u64)pos & 63;
    r = a[wi] >> sh;
    if (sh && wi + 1 < Nw) r |= a[wi + 1] << (64 - sh);
  }
  return r;
}
/* dst |= rot(src, z): dst[x] |= src[(x - z) mod L] */
static void or_rot(u64 *dst, const u64 *src, u64 z) {
  z %= Lbits;
  for (u64 w = 0; w < Nw; w++) {
    long long x0 = (long long)(w << 6);
    /* part 1: x >= z  -> src bit x - z */
    u64 v1 = get64(src, x0 - (long long)z);
    /* part 2: x < z -> src bit x - z + L */
    u64 v2 = 0;
    if ((u64)x0 < z) v2 = get64(src, x0 - (long long)z + (long long)Lbits);
    /* mask: v1 valid for x>=z, v2 valid for x<z */
    u64 m1;
    if ((u64)x0 >= z) m1 = ~0ULL;
    else if ((u64)x0 + 64 <= z) m1 = 0;
    else m1 = ~0ULL << (z - (u64)x0);
    dst[w] |= (v1 & m1) | (v2 & ~m1);
  }
  /* clear padding beyond L */
  if (Lbits & 63) dst[Nw - 1] &= (~0ULL) >> (64 - (Lbits & 63));
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
  u64 p = strtoull(argv[1], 0, 10), t = strtoull(argv[2], 0, 10), H = strtoull(argv[3], 0, 10), K = strtoull(argv[4], 0, 10);
  u64 c = 0; for (u64 q = p; q <= H - 1; q *= p) c += (H - 1) / q;
  u64 M = t + c; u128 mod = 1; for (u64 i = 0; i < M; i++) mod *= p;
  u128 X = 1; for (u64 i = 0; i < t; i++) X *= p; X = (X * K) % mod;
  u128 *y = malloc(sizeof(u128) * H); y[0] = 1;
  for (u64 i = 1; i < H; i++) { u128 f = (X + mod - (u128)(H - i)) % mod; y[i] = (y[i - 1] * f) % mod; }
  u128 modp = mod / p; Lbits = (u64)modp; Nw = (Lbits + 63) / 64;
  fprintf(stderr, "p=%llu t=%llu H=%llu K=%llu c=%llu M=%llu L=%llu words=%llu\n", (unsigned long long)p, (unsigned long long)t,
          (unsigned long long)H, (unsigned long long)K, (unsigned long long)c, (unsigned long long)M, (unsigned long long)Lbits, (unsigned long long)Nw);
  u64 *S = calloc(Nw, 8), *T = calloc(Nw, 8);
  S[0] = 1;
  u128 units[64]; int nu = 0;
  for (u64 i = 0; i < H; i++) {
    if (y[i] % p) { units[nu++] = y[i]; continue; }
    u64 z = (u64)((y[i] / p) % modp);
    memcpy(T, S, Nw * 8); or_rot(T, S, z); u64 *tmp = S; S = T; T = tmp;
  }
  fprintf(stderr, "units: %d\n", nu);
  /* unit subset sums mod p^M */
  int ns = 1 << nu; u128 *A = malloc(sizeof(u128) * ns);
  for (int m = 0; m < ns; m++) { u128 s = 0; for (int j = 0; j < nu; j++) if (m >> j & 1) s = (s + units[j]) % mod; A[m] = s; }
  u64 missing = 0; int shown = 0;
  for (u64 t0 = 0; t0 < p; t0++) {
    memset(T, 0, Nw * 8);
    int any = 0;
    for (int m = 0; m < ns; m++) if ((u64)(A[m] % p) == t0) { u64 al = (u64)(((A[m] + mod - t0) % mod) / p); or_rot(T, S, al); any = 1; }
    u64 pc = 0;
    if (any) for (u64 w = 0; w < Nw; w++) pc += __builtin_popcountll(T[w]);
    u64 miss = Lbits - pc; missing += miss;
    if (miss && shown < 10) {
      for (u64 x = 0; x < Lbits && shown < 10; x++) if (!(T[x >> 6] >> (x & 63) & 1)) {
        u128 r = (u128)t0 + (u128)p * x; printf("missed residue %llu\n", (unsigned long long)r); shown++; }
    }
  }
  printf("p=%llu t=%llu H=%llu K=%llu c=%llu missing=%llu\n", (unsigned long long)p, (unsigned long long)t, (unsigned long long)H,
         (unsigned long long)K, (unsigned long long)c, (unsigned long long)missing);
  return 0;
}
