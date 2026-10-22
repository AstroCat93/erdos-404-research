/* chebo.c -- empirical test of the realizability theorem (Theorem 5.4 of paper/note.md; Remark 6.1).
   Written separately from an earlier, simpler test that is not included here.

   For every prime p = 1 (mod k), Q[m-1] < p <= X:
     * factor p-1, find the least primitive root g (genuine primitive root, checked
       against every prime factor of p-1);
     * for EACH unit u of Z/k pick t = u, u+k, u+2k, ... with gcd(t, p-1) = 1, put
       g_u = g^t, RE-CHECK that g_u is a primitive root, and compute the vector
       R_u(q) = ind_{g_u}(q) mod k for the first m primes q by a discrete log in mu_k:
       q^((p-1)/k) = (g_u^((p-1)/k))^j  <=>  j = ind_{g_u}(q) mod k;
     * count_least[code(R for the least g)]++  and, for every DISTINCT vector among the
       R_u, realized[code]++ (so realized[v] = number of primes p for which SOME primitive
       root realizes v exactly; no orbit formula is used).
   Also checks the premise of note Lemma 2.1 directly: q^((p-1)/k) is always a k-th root of unity
   that is a power of g_u^((p-1)/k).
   Output: binary arrays (uint32) <out>.least and <out>.real of length k^m, and a summary.
   Usage: chebo k m X out                                                          */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t mpow(uint64_t b, uint64_t e, uint64_t p) {
    uint64_t r = 1 % p; b %= p;
    while (e) { if (e & 1) r = r * b % p; b = b * b % p; e >>= 1; }
    return r;
}
static uint64_t gcd(uint64_t a, uint64_t b) { while (b) { uint64_t t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: chebo k m X out\n"); return 2; }
    int k = atoi(argv[1]), m = atoi(argv[2]); uint64_t X = strtoull(argv[3], 0, 10);
    if (X >= (1ULL << 31)) { fprintf(stderr, "X too large for 64-bit mulmod\n"); return 2; }
    uint8_t *comp = calloc(X + 1, 1);
    for (uint64_t i = 2; i * i <= X; i++) if (!comp[i]) for (uint64_t j = i * i; j <= X; j += i) comp[j] = 1;
    /* small primes for factoring and the first m primes Q */
    uint64_t sp[20000]; int nsp = 0;
    for (uint64_t i = 2; i * i <= X + 1 && nsp < 20000; i++) if (!comp[i]) sp[nsp++] = i;
    for (uint64_t i = sp[nsp - 1] + 1; nsp < 20000 && i <= X; i++) if (!comp[i]) { sp[nsp++] = i; if (i * i > X) break; }
    uint64_t Q[16]; for (int i = 0; i < m; i++) Q[i] = sp[i];
    int units[16], nu = 0; for (int u = 1; u < k; u++) if (gcd(u, k) == 1) units[nu++] = u;
    size_t ncodes = 1; for (int i = 0; i < m; i++) ncodes *= k;
    uint32_t *least = calloc(ncodes, 4), *real = calloc(ncodes, 4);
    uint64_t np = 0, bad = 0, nonprim = 0;
    for (uint64_t p = Q[m - 1] + 1; p <= X; p++) {
        if (comp[p] || p % k != 1) continue;
        /* factor p-1 */
        uint64_t ell[32]; int ne = 0, x = 0; uint64_t r = p - 1;
        for (int i = 0; i < nsp && sp[i] * sp[i] <= r; i++) if (r % sp[i] == 0) { ell[ne++] = sp[i]; while (r % sp[i] == 0) r /= sp[i]; }
        if (r > 1) ell[ne++] = r;
        uint64_t g = 1; int ok;
        do { g++; ok = 1; for (int i = 0; i < ne; i++) if (mpow(g, (p - 1) / ell[i], p) == 1) { ok = 0; break; } } while (!ok);
        uint64_t e = (p - 1) / k, cq[16];
        for (int i = 0; i < m; i++) cq[i] = mpow(Q[i], e, p);
        size_t codes[16]; int ncod = 0;
        for (int a = 0; a < nu; a++) {
            uint64_t t = units[a];
            while (gcd(t, p - 1) != 1) t += k;
            uint64_t gu = mpow(g, t, p);
            for (int i = 0; i < ne; i++) if (mpow(gu, (p - 1) / ell[i], p) == 1) { nonprim++; break; }
            uint64_t w = mpow(gu, e, p), pw[16]; pw[0] = 1;
            for (int j = 1; j < k; j++) pw[j] = pw[j - 1] * w % p;
            if (pw[k - 1] * w % p != 1) bad++;
            for (int j = 1; j < k; j++) if (pw[j] == 1) bad++;      /* w must have exact order k */
            size_t code = 0, mul = 1;
            for (int i = 0; i < m; i++) {
                int jj = -1; for (int j = 0; j < k; j++) if (pw[j] == cq[i]) { jj = j; break; }
                if (jj < 0) { bad++; jj = 0; }
                code += mul * jj; mul *= k;
            }
            if (a == 0) least[code]++;          /* u = 1, t = 1: the least primitive root itself */
            int dup = 0; for (int c = 0; c < ncod; c++) if (codes[c] == code) dup = 1;
            if (!dup) { codes[ncod++] = code; real[code]++; }
        }
        np++;
    }
    char fn[1024];
    snprintf(fn, sizeof fn, "%s.least", argv[4]); FILE *f = fopen(fn, "wb"); fwrite(least, 4, ncodes, f); fclose(f);
    snprintf(fn, sizeof fn, "%s.real", argv[4]); f = fopen(fn, "wb"); fwrite(real, 4, ncodes, f); fclose(f);
    printf("k=%d m=%d X=%llu Q=", k, m, (unsigned long long)X);
    for (int i = 0; i < m; i++) printf("%llu%s", (unsigned long long)Q[i], i + 1 < m ? "," : "");
    printf(" primes_used=%llu discrete_log_failures=%llu non_primitive_g_u=%llu\n",
           (unsigned long long)np, (unsigned long long)bad, (unsigned long long)nonprim);
    return (bad || nonprim) ? 1 : 0;
}
