/* ecover.c -- exact subset-sum coverage of E_p = { (-1)^u / u! : 0<=u<=p-1 } in Z/p^L.
 *
 * Usage: ecover p Lmax [maxbits]
 * For L = 1..Lmax (stopping at first failure or when p^L > maxbits), computes the
 * full set Sigma(E_p) mod p^L by the bitmap recursion S <- S | (S + x) (cyclic),
 * and prints the number of residues covered.  Exact: no sampling, no hashing.
 *
 * Also prints the a=1 start condition: exists R subset {2..p-1} with 1 + sum r! == 0 mod p.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1 % m; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
/* inverse of unit a mod m = p^L via extended Euclid */
static u64 invmod(u64 a, u64 m) {
    __int128 t = 0, nt = 1, r = m, nr = a % m;
    while (nr) { __int128 q = r / nr, tmp; tmp = t - q * nt; t = nt; nt = tmp; tmp = r - q * nr; r = nr; nr = tmp; }
    if (r != 1) { fprintf(stderr, "not invertible\n"); exit(1); }
    if (t < 0) t += m;
    return (u64)t;
}

static inline int getbit(const u64 *S, u64 i) { return (S[i >> 6] >> (i & 63)) & 1; }

/* read 64 bits of S starting at bit position q (no wrap: q+64 <= nbits_padded) */
static inline u64 read64(const u64 *S, u64 q) {
    u64 w = q >> 6, o = q & 63;
    if (o == 0) return S[w];
    return (S[w] >> o) | (S[w + 1] << (64 - o));
}

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
    if (argc < 3) { fprintf(stderr, "usage: ecover p Lmax [maxbits]\n"); return 1; }
    u64 p = strtoull(argv[1], 0, 10);
    int Lmax = atoi(argv[2]);
    double maxbits = argc > 3 ? atof(argv[3]) : 4.5e9;

    /* start condition for a = 1 (mod p): 1 + subset sums of {r! : 2<=r<=p-1} hits 0 */
    {
        char *R = calloc(p, 1), *R2 = calloc(p, 1);
        R[1 % p] = 1;
        u64 f = 1;
        for (u64 r = 2; r < p; r++) {
            f = f * r % p;
            memcpy(R2, R, p);
            for (u64 s = 0; s < p; s++) if (R[s]) R2[(s + f) % p] = 1;
            memcpy(R, R2, p);
        }
        printf("p=%llu start(a=1): %s\n", (unsigned long long)p, R[0] ? "OK" : "FAILS");
        free(R); free(R2);
    }

    for (int L = 1; L <= Lmax; L++) {
        double Md = 1; for (int i = 0; i < L; i++) Md *= (double)p;
        if (Md > maxbits) { printf("p=%llu L=%d skipped (p^L=%.3g > maxbits)\n", (unsigned long long)p, L, Md); break; }
        u64 M = 1; for (int i = 0; i < L; i++) M *= p;
        u64 nw = (M + 63) / 64 + 1;
        u64 *S = calloc(nw, 8), *T = calloc(nw, 8);
        if (!S || !T) { printf("alloc fail\n"); return 1; }
        S[0] = 1; /* empty sum */
        u64 fact = 1;
        for (u64 u = 0; u < p; u++) {
            if (u > 0) fact = mulmod(fact, u, M);
            u64 x = invmod(fact, M);
            if (u & 1) x = (M - x) % M;
            step(S, T, M, x, nw - 1);
            T[nw - 1] = 0;
            u64 *tmp = S; S = T; T = tmp;
        }
        u64 cnt = 0;
        for (u64 w = 0; w + 1 < nw; w++) cnt += __builtin_popcountll(S[w]);
        printf("p=%llu L=%d p^L=%llu covered=%llu %s frac=%.6f\n", (unsigned long long)p, L,
               (unsigned long long)M, (unsigned long long)cnt, cnt == M ? "FULL" : "partial", (double)cnt / (double)M);
        fflush(stdout);
        free(S); free(T);
        if (cnt != M) break;
    }
    return 0;
}
