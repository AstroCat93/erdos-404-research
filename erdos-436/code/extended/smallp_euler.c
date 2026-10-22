/* smallp_euler.c -- separately written check of (H3) in paper/note.md: r(8,2,p) for every prime 3 <= p <= PMAX
 * by Euler's criterion.
 * n (p does not divide n) is an 8th-power residue iff n^((p-1)/d) == 1 mod p, d = gcd(8,p-1).
 * r = least n >= 1 with p not dividing n(n+1) and n, n+1 both residues; scanning n = 1..p-2 suffices
 * (residue status is periodic mod p and n == 0, -1 are excluded). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static uint64_t pw(uint64_t b, uint64_t e, uint64_t m) { uint64_t r = 1; b %= m; while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; } return r; }
int main(int argc, char **argv) {
    long P = atol(argv[1]);
    char *c = calloc(P + 1, 1);
    for (long i = 2; i * i <= P; i++) if (!c[i]) for (long j = i * i; j <= P; j += i) c[j] = 1;
    long maxr = 0, argmax = 0, nmax = 0, cnt = 0, hist[4] = {0};
    long maxr_by_class[8] = {0};
    printf("exceptional:");
    for (long p = 3; p <= P; p++) {
        if (c[p]) continue;
        cnt++;
        long d = (p - 1) % 8 == 0 ? 8 : ((p - 1) % 4 == 0 ? 4 : 2);
        uint64_t e = (p - 1) / d;
        long r = -1;
        int prev = 0; /* residue status of n */
        prev = (pw(1, e, p) == 1);
        for (long n = 1; n <= p - 2; n++) {
            int nx = (pw(n + 1, e, p) == 1);
            if (prev && nx) { r = n; break; }
            prev = nx;
        }
        if (r < 0) { printf(" %ld", p); continue; }
        if (r > maxr_by_class[p % 8]) maxr_by_class[p % 8] = r;
        if (r > maxr) { maxr = r; argmax = p; nmax = 1; } else if (r == maxr) nmax++;
    }
    printf("\nprimes checked (3..%ld): %ld\nmax r over non-exceptional: %ld at p=%ld (count with this max: %ld)\n", P, cnt, maxr, argmax, nmax);
    printf("max r by p mod 8: 1:%ld 3:%ld 5:%ld 7:%ld\n", maxr_by_class[1], maxr_by_class[3], maxr_by_class[5], maxr_by_class[7]);
    return 0;
}
