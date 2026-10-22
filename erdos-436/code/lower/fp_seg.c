/* fp_seg.c -- re-check of "least zero pair" claims for an exponent vector (paper/note.md (H2), section 7).
   Algorithm (different from the additive prime-power sieve of code/lower/pairs_np.py and from the
   smallest-prime-factor recursions of code/lower/pairs.c and code/lower/check_vector.py): a SEGMENTED
   DIVIDE-OUT sieve.
   In each segment, rem[m] = m; for each prime q <= sqrt(hi) and each multiple m of q, divide q
   out of rem[m] completely, adding R(q) to f[m] once per division; a cofactor rem[m] > 1 is then a
   prime and contributes R(rem[m]).  The scan stops at the first n >= 1 with f(n) = f(n+1) = 0.
   Every prime actually used must have a value (listed, or the default if default >= 0).
   Usage: fp_seg k Nmax vecfile default      (default -1: every prime used must be listed)   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: fp_seg k Nmax vecfile default\n"); return 2; }
    int k = atoi(argv[1]); uint64_t Nmax = strtoull(argv[2], 0, 10); int def = atoi(argv[4]);
    uint64_t T = Nmax + 2;
    uint8_t *isc = calloc(T + 1, 1);                 /* composite flags, for validating the file */
    isc[0] = isc[1] = 1;
    for (uint64_t i = 2; i * i <= T; i++) if (!isc[i]) for (uint64_t j = i * i; j <= T; j += i) isc[j] = 1;
    int8_t *R = malloc(T + 1); memset(R, -1, T + 1);
    FILE *fp = fopen(argv[3], "r"); if (!fp) { perror(argv[3]); return 2; }
    char line[512]; uint64_t listed = 0, above = 0, lines = 0;
    while (fgets(line, sizeof line, fp)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        long long q, r; if (sscanf(line, "%lld %lld", &q, &r) != 2) { fprintf(stderr, "bad line %s", line); return 2; }
        lines++;
        if (q < 2) { fprintf(stderr, "bad q %lld\n", q); return 2; }
        if ((uint64_t)q > T) { above++; continue; }
        if (isc[q]) { fprintf(stderr, "listed q=%lld is not prime\n", q); return 2; }
        if (r < 0 || r >= k) { fprintf(stderr, "value %lld out of range [0,k) at q=%lld\n", r, q); return 2; }
        if (R[q] != -1) { fprintf(stderr, "duplicate q=%lld\n", q); return 2; }
        R[q] = (int8_t)r; listed++;
    }
    fclose(fp);
    uint64_t sq = 1; while ((sq + 1) * (sq + 1) <= T) sq++;
    uint64_t *sp = malloc(sizeof(uint64_t) * (sq + 1)); uint64_t nsp = 0;
    for (uint64_t i = 2; i <= sq; i++) if (!isc[i]) sp[nsp++] = i;
    const uint64_t S = 1 << 20;
    uint32_t *rem = malloc(4 * S); uint8_t *f = malloc(S);
    int prevzero = 0; uint64_t zeros = 0, missing = 0;
#define VAL(q) (R[q] >= 0 ? R[q] : (def >= 0 ? def % k : (missing++, 0)))
    for (uint64_t lo = 1; lo <= Nmax + 1; lo += S) {
        uint64_t hi = lo + S; if (hi > Nmax + 2) hi = Nmax + 2;          /* segment [lo, hi) */
        for (uint64_t x = lo; x < hi; x++) { rem[x - lo] = (uint32_t)x; f[x - lo] = 0; }
        for (uint64_t i = 0; i < nsp && sp[i] * sp[i] < hi; i++) {
            uint64_t q = sp[i]; int rq = -2;
            uint64_t st = ((lo + q - 1) / q) * q;
            for (uint64_t x = st; x < hi; x += q) {
                if (rq == -2) rq = VAL(q);
                uint32_t v = rem[x - lo]; int a = 0;
                while (v % q == 0) { v /= q; a++; }
                rem[x - lo] = v; f[x - lo] = (uint8_t)((f[x - lo] + a * rq) % k);
            }
        }
        for (uint64_t x = lo; x < hi; x++) {
            uint32_t v = rem[x - lo];
            if (v > 1) f[x - lo] = (uint8_t)((f[x - lo] + VAL(v)) % k);
            if (missing) { fprintf(stderr, "prime factor of %llu has no value (default -1)\n", (unsigned long long)x); return 3; }
            int z = (f[x - lo] == 0);
            if (z) zeros++;
            if (z && prevzero && x >= 2) {
                uint64_t n = x - 1;
                printf("k=%d vec=%s default=%d listed<=Nmax+2:%llu above:%llu R(2)=%d\n", k, argv[3], def,
                       (unsigned long long)listed, (unsigned long long)above, R[2] >= 0 ? R[2] : def);
                printf("LEAST_ZERO_PAIR %llu %llu   (zeros of f in [1,n+1]: %llu)\n",
                       (unsigned long long)n, (unsigned long long)x, (unsigned long long)zeros);
                for (uint64_t t = n; t <= n + 1; t++) {
                    uint64_t y = t; int s = 0; printf("  %llu =", (unsigned long long)t);
                    for (uint64_t q = 2; q * q <= y; q++) if (y % q == 0) { int e = 0; while (y % q == 0) { y /= q; e++; }
                        int r = R[q] >= 0 ? R[q] : def; printf(" %llu^%d[R=%d]", (unsigned long long)q, e, r); s += e * r; }
                    if (y > 1) { int r = R[y] >= 0 ? R[y] : def; printf(" %llu[R=%d]", (unsigned long long)y, r); s += r; }
                    printf("  -> sum mod %d = %d\n", k, s % k);
                }
                /* how many primes <= n+1 exist, and how many are listed */
                uint64_t np = 0, nl = 0; for (uint64_t q = 2; q <= n + 1; q++) if (!isc[q]) { np++; if (R[q] >= 0) nl++; }
                printf("  primes <= n+1: %llu, of which listed: %llu\n", (unsigned long long)np, (unsigned long long)nl);
                return 0;
            }
            prevzero = z;
        }
    }
    printf("k=%d vec=%s: NO zero pair with n+1 <= %llu\n", k, argv[3], (unsigned long long)(Nmax + 1));
    return 1;
}
