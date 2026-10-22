/*
 * pairs.c -- first pair of consecutive k-th power "residues" for a character-exponent vector.
 *
 * Model: p = km+1 prime, g a primitive root, R(q) = ind_g(q) mod k for primes q.
 * f(n) = sum over q^e || n of e*R(q)  (mod k)  is completely additive, and
 * n is a k-th power residue mod p (p > n) iff f(n) == 0.
 * r(k,2,p) = least n >= 1 with f(n) == f(n+1) == 0.
 *
 * Algorithm (deliberately different from the prime-power additive sieve in pairs_np.py):
 * linear (Euler) sieve for the least prime factor lp[n], then f(n) = f(n/lp[n]) + R(lp[n]).
 *
 * Usage:
 *   pairs -k K -v VECFILE -N N [-d DEFAULT|none] [-u UNIT] [-B COVER] [-o FDUMP] [-x XFILE] [-q]
 *     -N N        compute f on [1, N]; search pairs (n, n+1) with n+1 <= N
 *     -d DEFAULT  value used for primes <= N absent from VECFILE (default: none = such primes are an error)
 *     -u UNIT     multiply every R value by UNIT mod k before use
 *     -B COVER    require VECFILE to list every prime <= COVER (default: N if -d none, else 0)
 *     -o FDUMP    write f(1..N) as N raw bytes
 *     -x XFILE    extra "q v" overrides applied after VECFILE (may list primes > max of VECFILE)
 *     -q          quiet: no per-pair listing
 * Vector file: lines "q v" (q prime, v integer). Lines starting with '#' are ignored.
 * Validation: q must be prime, no duplicates, values reduced mod k.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int k = 0;
static long N = 0;

static void die(const char *m) { fprintf(stderr, "ERROR: %s\n", m); exit(2); }

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + 1e-9 * t.tv_nsec; }

/* read "q v" lines; returns count. arrays grown dynamically */
static long readvec(const char *fn, long **qs, long **vs) {
    FILE *F = fopen(fn, "r"); if (!F) die("cannot open vector file");
    long cap = 1 << 16, n = 0; *qs = malloc(cap * sizeof(long)); *vs = malloc(cap * sizeof(long));
    char line[256];
    while (fgets(line, sizeof line, F)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        long q, v; if (sscanf(line, "%ld %ld", &q, &v) != 2) die("bad line in vector file");
        if (n == cap) { cap *= 2; *qs = realloc(*qs, cap * sizeof(long)); *vs = realloc(*vs, cap * sizeof(long)); }
        (*qs)[n] = q; (*vs)[n] = v; n++;
    }
    fclose(F); return n;
}

int main(int argc, char **argv) {
    const char *vf = NULL, *dump = NULL, *xf = NULL; int dflt = -1, unit = 1, quiet = 0; long B = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-k")) k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-v")) vf = argv[++i];
        else if (!strcmp(argv[i], "-N")) N = atol(argv[++i]);
        else if (!strcmp(argv[i], "-d")) { i++; dflt = strcmp(argv[i], "none") ? atoi(argv[i]) : -1; }
        else if (!strcmp(argv[i], "-u")) unit = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-B")) B = atol(argv[++i]);
        else if (!strcmp(argv[i], "-o")) dump = argv[++i];
        else if (!strcmp(argv[i], "-x")) xf = argv[++i];
        else if (!strcmp(argv[i], "-q")) quiet = 1;
        else die("unknown option");
    }
    if (k < 2 || !vf || N < 3) die("need -k K -v FILE -N N");
    double t0 = now();
    long *qs, *vs; long nv = readvec(vf, &qs, &vs);
    long *xq = NULL, *xv = NULL; long nx = xf ? readvec(xf, &xq, &xv) : 0;
    long maxq = 0; for (long i = 0; i < nv; i++) if (qs[i] > maxq) maxq = qs[i];
    for (long i = 0; i < nx; i++) if (xq[i] > maxq) maxq = xq[i];
    long M = (maxq > N ? maxq : N);
    /* linear sieve up to M */
    uint32_t *lp = calloc(M + 1, sizeof(uint32_t)); if (!lp) die("oom lp");
    long cap = M / 8 + 1000, np = 0; uint32_t *pr = malloc(cap * sizeof(uint32_t));
    for (long i = 2; i <= M; i++) {
        if (!lp[i]) { lp[i] = (uint32_t)i; if (np == cap) { cap *= 2; pr = realloc(pr, cap * sizeof(uint32_t)); } pr[np++] = (uint32_t)i; }
        for (long j = 0; j < np && pr[j] <= lp[i] && (long)pr[j] * i <= M; j++) lp[pr[j] * i] = pr[j];
    }
    /* R table */
    int8_t *R = malloc(M + 1); memset(R, -1, M + 1);
    long nonprime = 0, dup = 0;
    for (long i = 0; i < nv; i++) {
        long q = qs[i];
        if (q < 2 || lp[q] != (uint32_t)q) { nonprime++; fprintf(stderr, "non-prime key %ld\n", q); continue; }
        if (R[q] >= 0) { dup++; fprintf(stderr, "duplicate key %ld\n", q); continue; }
        R[q] = (int8_t)((((vs[i] % k) + k) % k));
    }
    for (long i = 0; i < nx; i++) {
        long q = xq[i];
        if (q < 2 || lp[q] != (uint32_t)q) { nonprime++; fprintf(stderr, "non-prime override %ld\n", q); continue; }
        R[q] = (int8_t)((((xv[i] % k) + k) % k));
    }
    if (B < 0) B = (dflt < 0) ? N : 0;
    long missing = 0, firstmissing = 0, primes_le_B = 0, primes_le_N = 0;
    for (long j = 0; j < np; j++) {
        long q = pr[j];
        if (q <= B) { primes_le_B++; if (R[q] < 0) { if (!missing) firstmissing = q; missing++; } }
        if (q <= N) primes_le_N++;
    }
    printf("k=%d N=%ld vecfile=%s entries=%ld overrides=%ld maxkey=%ld nonprime=%ld dup=%ld\n", k, N, vf, nv, nx, maxq, nonprime, dup);
    printf("cover bound B=%ld primes<=B=%ld missing=%ld%s", B, primes_le_B, missing, missing ? "" : "\n");
    if (missing) printf(" (first missing %ld)\n", firstmissing);
    if (nonprime || dup) die("invalid vector file");
    /* primes <= N absent from file -> default */
    long defaulted = 0;
    for (long j = 0; j < np && pr[j] <= N; j++) if (R[pr[j]] < 0) {
        if (dflt < 0) die("prime <= N without value and no default");
        R[pr[j]] = (int8_t)(((dflt % k) + k) % k); defaulted++;
    }
    printf("primes<=N=%ld defaulted=%ld default=%d unit=%d R(2)=%d\n", primes_le_N, defaulted, dflt, unit, R[2]);
    if (unit != 1) for (long j = 0; j < np && pr[j] <= N; j++) R[pr[j]] = (int8_t)(((long)R[pr[j]] * unit % k + k) % k);
    /* f by least-prime-factor recursion */
    uint8_t *f = malloc(N + 2); f[0] = 255; f[1] = 0;
    for (long n = 2; n <= N; n++) { uint32_t p = lp[n]; int t = f[n / p] + R[p]; if (t >= k) t -= k; f[n] = (uint8_t)t; }
    long zeros = 0, pairs = 0, first = 0;
    for (long n = 1; n <= N; n++) if (f[n] == 0) zeros++;
    for (long n = 1; n + 1 <= N; n++) if (f[n] == 0 && f[n + 1] == 0) { pairs++; if (!first) first = n; }
    printf("zeros on [1,N]=%ld zero-pairs with n+1<=N=%ld\n", zeros, pairs);
    if (first) {
        printf("FIRST_PAIR n=%ld n+1=%ld\n", first, first + 1);
        if (!quiet) for (long t = first; t <= first + 1; t++) {
            long m = t; int s = 0; printf("  %ld =", t); int firstf = 1;
            while (m > 1) { long p = lp[m]; int e = 0; while (m % p == 0) { m /= p; e++; }
                printf("%s%ld^%d[R=%d]", firstf ? " " : " * ", p, e, R[p]); firstf = 0; s = (s + e * R[p]) % k; }
            printf("   f=%d\n", s);
        }
    } else printf("FIRST_PAIR none with n+1<=%ld\n", N);
    if (dump) { FILE *O = fopen(dump, "wb"); fwrite(f + 1, 1, N, O); fclose(O); }
    printf("time %.2fs\n", now() - t0);
    return 0;
}
