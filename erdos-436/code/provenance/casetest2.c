/*
 * casetest2.c -- lookahead variant of the BLL (1964, Section 4) case test (exploratory).
 * At a zero pair, for each prime factor q of n(n+1) (largest first) that is not fixed and each value w,
 * compute the next first zero pair; apply the (q,w) that pushes it furthest (ties: larger q).
 * Primes listed in the start file with value 0 and the prime 2 are fixed; nothing else is ever fixed.
 * (Original header follows for the shared parts.)
 *
 * Start: R from an exceptions file (q v), R = 1 for all other primes; primes in the file are FIXED
 * unless their value is 2 (then "special").  Loop: find the first zero pair (n, n+1) with n <= L.
 * Take the largest prime factor q of n(n+1) that is not fixed:  R(q)=1 -> 2 (special);
 * R(q)=2 (special) -> 0 (fixed).  If every factor is fixed: impasse, stop.  Prime 2 is always fixed.
 * After each change f is updated on multiples of q only; the scan resumes at min(previous pair, q-1).
 * Usage: casetest -k K -x EXC -L L [-maxit M] [-o OUTEXC]
 * Output: final first zero pair (<= L or "none <= L"), the list of non-default values.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

int main(int argc, char **argv) {
    int k = 0; long L = 0, maxit = 100000; const char *xf = 0, *of = 0;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-k")) k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-x")) xf = argv[++i];
        else if (!strcmp(argv[i], "-L")) L = atol(argv[++i]);
        else if (!strcmp(argv[i], "-maxit")) maxit = atol(argv[++i]);
        else if (!strcmp(argv[i], "-o")) of = argv[++i];
    }
    clock_t c0 = clock();
    long N = L + 1;
    uint32_t *lp = calloc(N + 1, 4); long np = 0; uint32_t *pr = malloc((N / 2 + 10) * 4);
    for (long i = 2; i <= N; i++) { if (!lp[i]) { lp[i] = i; pr[np++] = i; }
        for (long j = 0; j < np && pr[j] <= lp[i] && (long)pr[j] * i <= N; j++) lp[pr[j] * i] = pr[j]; }
    int8_t *R = malloc(N + 1); uint8_t *st = calloc(N + 1, 1); /* 0 default, 1 special, 2 fixed */
    for (long i = 0; i <= N; i++) R[i] = 1 % k;
    FILE *F = fopen(xf, "r"); long q; int v; char line[128];
    while (fgets(line, sizeof line, F)) { if (line[0] == '#') continue; if (sscanf(line, "%ld %d", &q, &v) == 2 && q <= N) { R[q] = ((v % k) + k) % k; st[q] = (R[q] == 0) ? 2 : 1; } }
    fclose(F);
    st[2] = 2;
    uint8_t *f = malloc(N + 2); f[1] = 0;
    for (long n = 2; n <= N; n++) { int x = f[n / lp[n]] + R[lp[n]]; f[n] = x % k; }
    long start = 1, it = 0, n = 0;
    for (;;) {
        for (n = start; n <= L; n++) if (!f[n] && !f[n + 1]) break;
        if (n > L) { printf("no zero pair with n <= %ld after %ld changes\n", L, it); break; }
        if (it >= maxit) { printf("maxit reached; current first pair %ld\n", n); break; }
        long fs[64]; int nf = 0;
        for (long t = n; t <= n + 1; t++) { long m = t; while (m > 1) { long p = lp[m]; fs[nf++] = p; while (m % p == 0) m /= p; } }
        long bq = 0; int bw = -1; long bpos = n;
        for (int i = 0; i < nf; i++) {
            long qq = fs[i]; if (st[qq] == 2) continue;
            for (int w = 0; w < k; w++) { if (w == R[qq]) continue;
                int d = ((w - R[qq]) % k + k) % k;
                for (long m = qq; m <= N; m += qq) { long x = m; int e = 0; while (x % qq == 0) { x /= qq; e++; } f[m] = (f[m] + e * d) % k; }
                long s0 = qq - 1 < n ? (qq - 1 > 1 ? qq - 1 : 1) : n, t;
                for (t = s0; t <= L; t++) if (!f[t] && !f[t + 1]) break;
                if (t > bpos || (t == bpos && t > n && qq > bq)) { bpos = t; bq = qq; bw = w; }
                int dd = (k - d) % k;
                for (long m = qq; m <= N; m += qq) { long x = m; int e = 0; while (x % qq == 0) { x /= qq; e++; } f[m] = (f[m] + e * dd) % k; }
            }
        }
        if (!bq) { printf("STUCK at pair %ld, %ld: no single change moves it, after %ld changes\n", n, n + 1, it); break; }
        long best = bq; int old = R[best], nw = bw;
        int d = ((nw - old) % k + k) % k;
        for (long m = best; m <= N; m += best) { long x = m; int e = 0; while (x % best == 0) { x /= best; e++; } f[m] = (f[m] + e * d) % k; }
        R[best] = nw; it++;
        if (of) { FILE *O = fopen(of, "w"); fprintf(O, "# after %ld changes, next pair >= %ld\n", it, bpos); for (long j = 0; j < np; j++) if (R[pr[j]] != 1 % k) fprintf(O, "%u %d\n", pr[j], R[pr[j]]); fclose(O); }
        if (1) fprintf(stderr, "it=%ld pair=%ld -> %ld via q=%ld:=%d\n", it, n, bpos, best, nw);
        start = bpos; if (bpos > L) { n = bpos; printf("no zero pair with n <= %ld after %ld changes\n", L, it); break; }
        continue;
        start = (best - 1 < n) ? (best - 1 > 1 ? best - 1 : 1) : n;
    }
    long ne = 0; for (long j = 0; j < np; j++) if (R[pr[j]] != 1 % k) ne++;
    printf("first zero pair: %ld  (limit L=%ld)  non-default entries: %ld  cpu %.1fs\n", n <= L ? n : -1, L, ne, (double)(clock() - c0) / CLOCKS_PER_SEC);
    if (of) { FILE *O = fopen(of, "w"); for (long j = 0; j < np; j++) if (R[pr[j]] != 1 % k) fprintf(O, "%u %d\n", pr[j], R[pr[j]]); fclose(O); }
    return 0;
}
