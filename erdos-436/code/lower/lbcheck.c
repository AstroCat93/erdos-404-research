/* lbcheck.c -- lower-bound vector check, written from the definitions in paper/note.md, sections 2 and 4.
 * Usage: lbcheck k NMAX vecfile default [reset]
 *   vecfile: lines "q v" (q prime), '#' comment lines ignored. Unlisted primes get `default`
 *   (default = -1 means every prime <= NMAX+1 must be listed).
 *   f(m) = sum_q v_q(m) R(q) mod k, computed as f(m) = f(m / spf(m)) + R(spf(m)).
 *   Prints the least n <= NMAX with f(n) = f(n+1) = 0, and its factorisations.
 *   With "reset": for each listed prime q, also reports the least zero pair when R(q) is set to 1.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint32_t *spf;
static long T;

static long firstpair(const uint8_t *Rv, int k, uint8_t *f) {
    f[1] = 0;
    for (long m = 2; m <= T; m++) {
        uint32_t q = spf[m];
        int v = f[m / q] + Rv[q];
        f[m] = (uint8_t)(v >= k ? v - k : v);
    }
    for (long n = 1; n < T; n++) if (f[n] == 0 && f[n + 1] == 0) return n;
    return -1;
}

static void factor(long m, const uint8_t *Rv) {
    int first = 1;
    while (m > 1) {
        uint32_t q = spf[m]; int e = 0;
        while (m % q == 0) { m /= q; e++; }
        printf(first ? "%u^%d[R=%d]" : " * %u^%d[R=%d]", q, e, Rv[q]);
        first = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage\n"); return 1; }
    int k = atoi(argv[1]);
    long N = atol(argv[2]);
    int def = atoi(argv[4]);
    int reset = argc > 5 && !strcmp(argv[5], "reset");
    T = N + 1;
    spf = calloc(T + 1, sizeof(uint32_t));
    long nprimes = 0;
    for (long i = 2; i <= T; i++) if (!spf[i]) {
        spf[i] = (uint32_t)i; nprimes++;
        if ((long long)i * i <= T) for (long j = i * i; j <= T; j += i) if (!spf[j]) spf[j] = (uint32_t)i;
    }
    uint8_t *Rv = malloc(T + 1);
    uint8_t *listed = calloc(T + 1, 1);
    memset(Rv, def < 0 ? 255 : def % k, T + 1);
    FILE *fp = fopen(argv[3], "r");
    char buf[512]; long nl = 0, above = 0;
    long *lq = malloc(sizeof(long) * 200000); int nlq = 0;
    while (fgets(buf, sizeof buf, fp)) {
        if (buf[0] == '#' || buf[0] == '\n') continue;
        long q; int v;
        if (sscanf(buf, "%ld %d", &q, &v) != 2) { printf("bad line %s", buf); return 1; }
        if (q > T) { above++; continue; }
        if (q < 2 || spf[q] != q) { printf("listed non-prime %ld\n", q); return 1; }
        if (listed[q]) { printf("duplicate %ld\n", q); return 1; }
        listed[q] = 1; Rv[q] = (uint8_t)(((v % k) + k) % k); nl++;
        if (nlq < 200000) lq[nlq++] = q;
    }
    fclose(fp);
    if (def < 0) for (long i = 2; i <= T; i++) if (spf[i] == i && !listed[i]) { printf("prime %ld not listed\n", i); return 1; }
    printf("k=%d NMAX=%ld primes<=NMAX+1=%ld listed=%ld listed_above=%ld default=%d R(2)=%d\n", k, N, nprimes, nl, above, def, Rv[2]);
    uint8_t *f = malloc(T + 1);
    long n = firstpair(Rv, k, f);
    if (n < 0) { printf("NO zero pair with n+1 <= %ld\n", T); }
    else {
        long z = 0; for (long m = 1; m <= n + 1; m++) z += f[m] == 0;
        printf("LEAST_ZERO_PAIR %ld %ld  (zeros of f in [1,n+1]: %ld)\n  %ld = ", n, n + 1, z, n);
        factor(n, Rv); printf("  f=%d\n  %ld = ", f[n], n + 1); factor(n + 1, Rv); printf("  f=%d\n", f[n + 1]);
    }
    if (reset) {
        int allearlier = 1;
        for (int i = 0; i < nlq; i++) {
            long q = lq[i]; uint8_t old = Rv[q];
            if (old == 1 % k) { printf("reset %ld: already 1\n", q); continue; }
            Rv[q] = 1;
            long m = firstpair(Rv, k, f);
            printf("reset q=%ld (R %d->1): least zero pair %ld%s\n", q, old, m, (m >= 0 && m < n) ? "  EARLIER" : "  not earlier");
            if (!(m >= 0 && m < n) && q != 2) allearlier = 0;
            Rv[q] = old;
        }
        printf("every listed prime other than 2 individually necessary: %s\n", allearlier ? "YES" : "NO");
    }
    return 0;
}
