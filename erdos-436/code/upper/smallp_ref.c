/* smallp_ref.c -- check of (H3) in paper/note.md: r(8,2,p) for every prime 3 <= p <= P, by three methods.
   For every prime 3 <= p <= P:
     d = gcd(8, p-1); method A: n is an 8th-power residue iff p does not divide n and
       n^((p-1)/d) = 1 (mod p)   [the 8th powers are the d-th powers, note Lemma 2.2];
     method B: index model of note Lemma 2.1 with k = d: least primitive root g, R(q) = ind_g q mod d
       (discrete log in mu_d), f(n) = sum v_q(n) R(q) mod d, residue iff f(n) = 0;
     method C: brute force, the set {x^8 mod p : 1 <= x < p} (only for p < 20000).
   The three must agree for every n that is scanned.  r = least n with n, n+1 residues
   (p not dividing n(n+1)); n runs over 1..p-2 (beyond that the pattern repeats mod p).
   Usage: smallp_ref P                                                                  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static uint64_t mpow(uint64_t b, uint64_t e, uint64_t p) { uint64_t r = 1 % p; b %= p;
    while (e) { if (e & 1) r = r * b % p; b = b * b % p; e >>= 1; } return r; }
int main(int argc, char **argv) {
    uint64_t P = strtoull(argv[1], 0, 10);
    uint32_t *spf = calloc(P + 2, 4);
    for (uint64_t i = 2; i <= P + 1; i++) if (!spf[i]) for (uint64_t j = i; j <= P + 1; j += i) if (!spf[j]) spf[j] = i;
    int8_t *Rq = malloc(P + 2); uint8_t *br = malloc(20000);
    uint64_t maxr = 0, argmax = 0, nprimes = 0, disagree = 0, hist[4] = {0};
    uint64_t maxr1 = 0, argmax1 = 0;                 /* restricted to p = 1 mod 8 */
    printf("exceptional primes (no pair):");
    for (uint64_t p = 3; p <= P; p++) {
        if (spf[p] != p) continue;
        nprimes++;
        uint64_t d = ((p - 1) % 8 == 0) ? 8 : ((p - 1) % 4 == 0 ? 4 : 2);
        uint64_t e = (p - 1) / d;
        /* primitive root */
        uint64_t ell[32]; int ne = 0; uint64_t r = p - 1;
        while (r > 1) { uint64_t q = spf[r]; ell[ne++] = q; while (r % q == 0) r /= q; }
        uint64_t g = 1; int ok; do { g++; ok = 1; for (int i = 0; i < ne; i++) if (mpow(g, (p - 1) / ell[i], p) == 1) { ok = 0; break; } } while (!ok);
        uint64_t w = mpow(g, e, p), pw[8]; pw[0] = 1; for (uint64_t j = 1; j < d; j++) pw[j] = pw[j - 1] * w % p;
        if (p < 20000) { memset(br, 0, p); for (uint64_t x = 1; x < p; x++) br[mpow(x, 8, p)] = 1; }
        uint64_t found = 0; int prev = 0; uint64_t maxq = 1;
        for (uint64_t n = 1; n + 1 <= p - 1; n++) {
            uint64_t m = n + 1;            /* evaluate residue status of m; prev holds status of n */
            if (n == 1) {                  /* status of 1 */
                prev = 1;
            }
            int A = (mpow(m, e, p) == 1);
            /* B: index model */
            uint64_t y = m; uint64_t s = 0;
            while (y > 1) { uint64_t q = spf[y]; int a = 0; while (y % q == 0) { y /= q; a++; }
                if (q > maxq) { for (uint64_t qq = maxq + 1; qq <= q; qq++) if (spf[qq] == qq) {
                        uint64_t c = mpow(qq, e, p); int jj = -1; for (uint64_t j = 0; j < d; j++) if (pw[j] == c) jj = (int)j;
                        if (jj < 0) { printf("\nDLOG FAIL p=%llu q=%llu\n", (unsigned long long)p, (unsigned long long)qq); return 1; }
                        Rq[qq] = (int8_t)jj; }
                    maxq = q; }
                s += (uint64_t)a * Rq[q]; }
            int B = (s % d == 0);
            int C = (p < 20000) ? br[m] : A;
            if (A != B || A != C) disagree++;
            if (prev && A) { found = n; break; }
            prev = A;
        }
        if (!found) { printf(" %llu", (unsigned long long)p); continue; }
        hist[d == 8 ? 3 : (d == 4 ? 2 : 1)]++;
        if (found > maxr) { maxr = found; argmax = p; }
        if (d == 8 && found > maxr1) { maxr1 = found; argmax1 = p; }
    }
    printf("\nprimes 3..%llu: %llu (d=2: %llu, d=4: %llu, d=8: %llu non-exceptional)\n", (unsigned long long)P,
           (unsigned long long)nprimes, (unsigned long long)hist[1], (unsigned long long)hist[2], (unsigned long long)hist[3]);
    printf("max r(8,2,p) over non-exceptional p: %llu at p=%llu;  over p=1 mod 8: %llu at p=%llu\n",
           (unsigned long long)maxr, (unsigned long long)argmax, (unsigned long long)maxr1, (unsigned long long)argmax1);
    printf("method disagreements (Euler vs index model vs brute force): %llu\n", (unsigned long long)disagree);
    return disagree ? 1 : 0;
}
