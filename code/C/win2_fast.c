/* win2.c -- Tao-window coverage for a level-j gate using the 2-block window [p(m-1), p(m+1)).
 *
 * Gate block m with m+1 = p^j t (p does not divide t).  Window elements, normalized by (p(m-1))!:
 *   block m-1 :  x_r = prod_{k=1}^r (p(m-1)+k)                       (r = 0..p-1)
 *   block m   :  y_r = p * rho * prod_{k=1}^r (pm+k),  rho = P_{m-1}(p-1) * m
 *               (since (pm)! = (p(m-1))! * P_{m-1}(p-1) * p*m and p does not divide m)
 * Demand D = v_p((p(m+1))!/(p(m-1))!) = 1 + (j+1) = j+2.
 * If the 2^{2p} subset sums cover Z/p^D, Tao's lemma gives P(p(m-1)) => P(p(m+1)).
 * The data mod p^D depends only on (j, t mod p)  [see notes], so t = t0 in 1..p-1 covers all t == t0.
 *
 * usage: win2 p j t0      prints covered count and FULL/partial.  Exact bitmap DP.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static inline int getbit(const u64 *S, u64 i) { return (S[i >> 6] >> (i & 63)) & 1; }
static inline u64 read64(const u64 *S, u64 q) { u64 w = q >> 6, o = q & 63; if (!o) return S[w]; return (S[w] >> o) | (S[w + 1] << (64 - o)); }
/* T = S | rot(S, x) where rot(S,x)[i] = S[(i - x) mod M]  (fast paths; edges bit by bit) */
static void step(const u64 *S, u64 *T, u64 M, u64 x, u64 nw) {
    memcpy(T, S, nw * 8);
    u64 wlo = (x + 63) / 64, whi = M / 64, q = x >> 6, o = x & 63;
    if (whi > wlo) {
        if (o == 0) { for (u64 w = wlo; w < whi; w++) T[w] |= S[w - q]; }
        else { for (u64 w = wlo; w < whi; w++) T[w] |= (S[w - q - 1] >> (64 - o)) | (S[w - q] << o); }
    }
    u64 wwrap = x / 64;
    { u64 off = M - x, q2 = off >> 6, o2 = off & 63;
      if (o2 == 0) { for (u64 w = 0; w < wwrap; w++) T[w] |= S[w + q2]; }
      else { for (u64 w = 0; w < wwrap; w++) T[w] |= (S[w + q2] >> o2) | (S[w + q2 + 1] << (64 - o2)); } }
    for (u64 w = wwrap; w < nw; w++) {
        if (w >= wlo && w < whi) { w = whi - 1; continue; }
        u64 i0 = w * 64, val = 0;
        for (int b = 0; b < 64; b++) { u64 i = i0 + b; if (i >= M) break; u64 src = (i >= x) ? i - x : i + M - x; if (getbit(S, src)) val |= (u64)1 << b; }
        T[w] |= val;
    }
    u64 rem = M & 63; if (rem) T[nw - 1] &= (((u64)1 << rem) - 1);
}

int main(int argc, char **argv) {
    u64 p = strtoull(argv[1], 0, 10); int j = atoi(argv[2]); u64 t0 = strtoull(argv[3], 0, 10);
    int D = j + 2;
    u64 M = 1; for (int i = 0; i < D; i++) M *= p;
    /* m = p^j t0 - 1, work with residues mod M (m itself may be huge only through p^j t0, fine in u64 for our ranges) */
    u64 pj = 1; for (int i = 0; i < j; i++) pj *= p;
    u64 m = pj * t0 - 1;            /* fits: p^j t0 < M */
    u64 base1 = mulmod(p % M, (m - 1) % M, M);   /* p(m-1) mod M */
    u64 base2 = mulmod(p % M, m % M, M);         /* pm mod M */
    u64 *el = malloc(sizeof(u64) * 2 * p);
    u64 P = 1 % M;
    for (u64 r = 0; r < p; r++) { if (r) P = mulmod(P, (base1 + r) % M, M); el[r] = P; }
    u64 Pfull = mulmod(P, (base1 + p - 1 + 0) % M, M); /* placeholder, recomputed below */
    /* P_{m-1}(p-1) = prod_{k=1}^{p-1} (p(m-1)+k) = el[p-1] */
    Pfull = el[p - 1];
    u64 rho = mulmod(Pfull, m % M, M);
    u64 Q = 1 % M;
    for (u64 r = 0; r < p; r++) { if (r) Q = mulmod(Q, (base2 + r) % M, M); el[p + r] = mulmod(mulmod(p % M, rho, M), Q, M); }
    u64 nw = (M + 63) / 64 + 1;
    u64 *S = calloc(nw, 8), *T = calloc(nw, 8);
    if (!S || !T) { printf("alloc fail\n"); return 1; }
    S[0] = 1;
    for (u64 i = 0; i < 2 * p; i++) { step(S, T, M, el[i] % M, nw - 1); T[nw - 1] = 0; u64 *tmp = S; S = T; T = tmp; }
    u64 cnt = 0; for (u64 w = 0; w + 1 < nw; w++) cnt += __builtin_popcountll(S[w]);
    printf("p=%llu j=%d t0=%llu D=%d p^D=%llu covered=%llu %s\n", (unsigned long long)p, j, (unsigned long long)t0, D,
           (unsigned long long)M, (unsigned long long)cnt, cnt == M ? "FULL" : "partial");
    return 0;
}
