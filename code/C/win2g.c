/* win2g.c -- certify 2-block Tao-window coverage at a level-j gate by "greedy shifted covers".
 *
 * Window [p(m-1), p(m+1)), m+1 = p^j t0, normalized by (p(m-1))!:
 *   block m-1 : x_r = P_{m-1}(r) = prod_{k<=r} (p(m-1)+k)
 *   block m   : p * rho * P_m(r),   rho = P_{m-1}(p-1) * m
 * Demand Z/p^{j+2}.  Let B = Sigma({rho * P_m(r)}) mod p^{j+1} (exact bitmap DP).
 * For a subset R of block m-1 with x = sum_R x_r (mod p^{j+2}), write x = rho0 + p*xi (0<=rho0<p).
 * Then every target tau = rho0 + p*sigma with sigma in xi + B is attained.  For each rho0 we OR
 * shifted copies xi + B over random R with x == rho0 (mod p) until all of Z/p^{j+1} is covered.
 * Success is an exact certificate (each shift is an explicit subset); failure only means "not certified".
 *
 * usage: win2g p j t0 [maxshifts]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static inline int getbit(const u64 *S, u64 i) { return (S[i >> 6] >> (i & 63)) & 1; }
static inline u64 read64(const u64 *S, u64 q) { u64 w = q >> 6, o = q & 63; if (!o) return S[w]; return (S[w] >> o) | (S[w + 1] << (64 - o)); }
/* T = S | rot(S,x) */
static void step(const u64 *S, u64 *T, u64 M, u64 x, u64 nw) {
    for (u64 w = 0; w < nw; w++) {
        u64 i0 = w * 64, val = 0;
        if (i0 >= x && i0 + 64 <= M) val = read64(S, i0 - x);
        else for (int b = 0; b < 64; b++) { u64 i = i0 + b; if (i >= M) break; u64 src = (i >= x) ? i - x : i + M - x; if (getbit(S, src)) val |= (u64)1 << b; }
        T[w] = S[w] | val;
    }
    u64 rem = M & 63; if (rem) T[nw - 1] &= (((u64)1 << rem) - 1);
}
/* C |= rot(B, x): C[i] |= B[(i - x) mod M] for i < M.  Fast path: tight vectorizable loop on
   words fully inside [x, M) (source i-x has no wrap); edges handled bit by bit. */
static void orshift(const u64 *B, u64 *C, u64 M, u64 x, u64 nw) {
    u64 wlo = (x + 63) / 64;            /* first word with i0 >= x */
    u64 whi = M / 64;                   /* words [wlo, whi) have i0+64 <= M */
    u64 q = x >> 6, o = x & 63;
    /* for word w in [wlo, whi): bits i0..i0+63 <- B bits (i0 - x)..; i0 - x = 64(w - q) - o */
    if (whi > wlo) {
        if (o == 0) {
            for (u64 w = wlo; w < whi; w++) C[w] |= B[w - q];
        } else {
            for (u64 w = wlo; w < whi; w++) C[w] |= (B[w - q - 1] >> (64 - o)) | (B[w - q] << o);
        }
    }
    /* wrap region: words w with i0+63 < x (i.e. w < x/64): source i + (M - x), no wrap */
    u64 wwrap = x / 64;                 /* words [0, wwrap) satisfy i0 + 64 <= x */
    {
        u64 off = M - x, q2 = off >> 6, o2 = off & 63;
        if (o2 == 0) { for (u64 w = 0; w < wwrap; w++) C[w] |= B[w + q2]; }
        else { for (u64 w = 0; w < wwrap; w++) C[w] |= (B[w + q2] >> o2) | (B[w + q2 + 1] << (64 - o2)); }
    }
    for (u64 w = wwrap; w < nw; w++) {
        if (w >= wlo && w < whi) { w = whi - 1; continue; }
        u64 i0 = w * 64, val = 0;
        for (int b = 0; b < 64; b++) { u64 i = i0 + b; if (i >= M) break; u64 src = (i >= x) ? i - x : i + M - x; if (getbit(B, src)) val |= (u64)1 << b; }
        C[w] |= val;
    }
    u64 rem = M & 63; if (rem) C[nw - 1] &= (((u64)1 << rem) - 1);
}
static u64 rng = 88172645463325252ULL;
static u64 xs64(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

int main(int argc, char **argv) {
    u64 p = strtoull(argv[1], 0, 10); int j = atoi(argv[2]); u64 t0 = strtoull(argv[3], 0, 10);
    int maxshifts = argc > 4 ? atoi(argv[4]) : 400;
    rng ^= p * 1000003ULL + j * 7919ULL + t0;
    u64 M2 = 1; for (int i = 0; i < j + 2; i++) M2 *= p;   /* p^{j+2} */
    u64 M1 = M2 / p;                                         /* p^{j+1} */
    u64 pj = 1; for (int i = 0; i < j; i++) pj *= p;
    u64 m = pj * t0 - 1;
    u64 base1 = mulmod(p, (m - 1) % M2, M2), base2 = mulmod(p, m % M2, M2);
    u64 *x = malloc(8 * p), *yv = malloc(8 * p);
    u64 P = 1 % M2;
    for (u64 r = 0; r < p; r++) { if (r) P = mulmod(P, (base1 + r) % M2, M2); x[r] = P; }
    u64 rho = mulmod(x[p - 1], m % M2, M2);
    u64 Q = 1 % M2;
    for (u64 r = 0; r < p; r++) { if (r) Q = mulmod(Q, (base2 + r) % M2, M2); yv[r] = mulmod(rho, Q, M2) % M1; }
    u64 nw = (M1 + 63) / 64 + 1;
    u64 *B = calloc(nw, 8), *T = calloc(nw, 8), *C = calloc(nw, 8);
    if (!B || !T || !C) { printf("alloc fail\n"); return 1; }
    B[0] = 1;
    for (u64 r = 0; r < p; r++) { step(B, T, M1, yv[r], nw - 1); T[nw - 1] = 0; u64 *tmp = B; B = T; T = tmp; }
    u64 bc = 0; for (u64 w = 0; w + 1 < nw; w++) bc += __builtin_popcountll(B[w]);
    int worst = 0; int ok = 1;
    for (u64 rho0 = 0; rho0 < p && ok; rho0++) {
        memset(C, 0, nw * 8);
        int shifts = 0; u64 cnt = 0;
        while (shifts < maxshifts) {
            /* random subset of block m-1 with sum == rho0 mod p */
            u64 s;
            do {
                u64 mask = xs64();
                s = 0;
                u64 mask2 = xs64();
                for (u64 r = 0; r < p; r++) { int bit = r < 64 ? (int)((mask >> r) & 1) : (int)((mask2 >> (r - 64)) & 1); if (bit) s = (s + x[r]) % M2; }
            } while (s % p != rho0);
            u64 xi = (s - rho0) / p;     /* in [0, p^{j+1}) */
            orshift(B, C, M1, xi % M1, nw - 1);
            shifts++;
            if ((shifts >= 16 && shifts % 8 == 0) || shifts >= maxshifts) {
                cnt = 0; for (u64 w = 0; w + 1 < nw; w++) cnt += __builtin_popcountll(C[w]);
                if (cnt == M1) break;
            }
        }
        if (cnt != M1) ok = 0;
        if (shifts > worst) worst = shifts;
    }
    printf("p=%llu j=%d t0=%llu D=%d |B|=%llu/%llu  %s (max shifts used %d)\n", (unsigned long long)p, j, (unsigned long long)t0, j + 2,
           (unsigned long long)bc, (unsigned long long)M1, ok ? "FULL" : "NOT-CERTIFIED", worst);
    return 0;
}
