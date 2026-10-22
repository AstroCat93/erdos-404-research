/* smallp.c -- direct computation of r(k,2,p) for all primes 3 <= p <= PMAX.
 * r(k,2,p) = least n >= 1 with n and n+1 both nonzero k-th power residues mod p
 * (n+1 <= p-1), or "none".  n is a k-th power residue iff n^((p-1)/d) = 1 mod p,
 * d = gcd(k, p-1) (Euler's criterion in the cyclic group (Z/p)^*).
 * Usage: smallp k PMAX BOUND   -- lists the primes with no pair, and those with r > BOUND.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint64_t pw(uint64_t b, uint64_t e, uint64_t m) { uint64_t r = 1; b %= m; while (e) { if (e & 1) r = r * b % m; b = b * b % m; e >>= 1; } return r; }
static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }

int main(int argc, char **argv) {
    int k = atoi(argv[1]); long PMAX = atol(argv[2]); long BOUND = atol(argv[3]);
    char *comp = calloc(PMAX + 1, 1);
    for (long i = 2; i * i <= PMAX; i++) if (!comp[i]) for (long j = i * i; j <= PMAX; j += i) comp[j] = 1;
    long nprimes = 0, nnone = 0, nbig = 0, rmax = 0, prmax = 0;
    printf("k=%d primes 3..%ld; primes with no pair of consecutive nonzero k-th power residues:", k, PMAX);
    for (long p = 3; p <= PMAX; p++) {
        if (comp[p]) continue;
        nprimes++;
        long d = gcdl(k, p - 1), e = (p - 1) / d, r = -1;
        int prev = 1;                      /* n = 1 is a residue */
        for (long n = 2; n <= p - 1; n++) {
            int cur = pw(n, e, p) == 1;
            if (prev && cur) { r = n - 1; break; }
            prev = cur;
        }
        if (r < 0) { nnone++; printf(" %ld(d=%ld)", p, d); continue; }
        if (r > BOUND) { nbig++; fprintf(stderr, "r(%d,2,%ld) = %ld > %ld\n", k, p, r, BOUND); }
        if (r > rmax) { rmax = r; prmax = p; }
    }
    printf("\nprimes examined: %ld; with no pair: %ld; with r > %ld: %ld; largest finite r = %ld at p = %ld\n",
           nprimes, nnone, BOUND, nbig, rmax, prmax);
    return 0;
}
