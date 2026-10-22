/*
 * simplify.c -- greedy compaction of a character-exponent vector.
 * Start from a vector R (all primes <= N=L+1) with no zero pair (n, n+1), n <= L.
 * Repeatedly try to move R(q) to a "simpler" value while keeping the invariant
 * "no n <= L with f(n) == f(n+1) == 0".  Changing R(q) only changes f on multiples of q,
 * and two consecutive integers are never both multiples of q, so a change is safe iff
 * for every multiple m <= N whose new f(m) is 0, neither neighbour (m-1 >= 1, m+1 <= N)
 * has f == 0.  Cost per trial: N/q.
 *
 * Usage: simplify -k K -v VEC -L L -t TARGET -o OUT [-order desc|asc|rand] [-seed S]
 *                 [-fix q1,q2,...] [-alt v1,v2,...]
 *   TARGET  default value we try to move every prime to (e.g. 1)
 *   -fix    primes never changed (e.g. 2, whose value must stay even for k=8)
 *   -alt    after a failed move to TARGET, try these values in order (to shrink the value set)
 * OUT gets the full simplified vector (q v for every prime <= N).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int main(int argc, char **argv) {
    int k = 0, t = 1; long L = 0; const char *vf = 0, *of = 0, *order = "desc"; unsigned seed = 1;
    char fixs[4096] = "", alts[256] = "";
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-k")) k = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-v")) vf = argv[++i];
        else if (!strcmp(argv[i], "-L")) L = atol(argv[++i]);
        else if (!strcmp(argv[i], "-t")) t = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-o")) of = argv[++i];
        else if (!strcmp(argv[i], "-order")) order = argv[++i];
        else if (!strcmp(argv[i], "-seed")) seed = (unsigned)atoi(argv[++i]);
        else if (!strcmp(argv[i], "-fix")) strncpy(fixs, argv[++i], sizeof fixs - 1);
        else if (!strcmp(argv[i], "-alt")) strncpy(alts, argv[++i], sizeof alts - 1);
    }
    long N = L + 1;
    uint32_t *lp = calloc(N + 1, 4); long np = 0; uint32_t *pr = malloc((N / 2 + 10) * 4);
    for (long i = 2; i <= N; i++) { if (!lp[i]) { lp[i] = i; pr[np++] = i; }
        for (long j = 0; j < np && pr[j] <= lp[i] && (long)pr[j] * i <= N; j++) lp[pr[j] * i] = pr[j]; }
    int8_t *R = malloc(N + 1); memset(R, -1, N + 1); uint8_t *fixed = calloc(N + 1, 1);
    FILE *F = fopen(vf, "r"); long q; int v; char line[128];
    while (fgets(line, sizeof line, F)) { if (line[0] == '#') continue; if (sscanf(line, "%ld %d", &q, &v) == 2 && q <= N) R[q] = ((v % k) + k) % k; }
    fclose(F);
    for (long j = 0; j < np; j++) if (R[pr[j]] < 0) { fprintf(stderr, "missing prime %u\n", pr[j]); return 2; }
    for (char *s = strtok(fixs, ","); s; s = strtok(0, ",")) fixed[atol(s)] = 1;
    int alt[16], nalt = 0; for (char *s = strtok(alts, ","); s; s = strtok(0, ",")) alt[nalt++] = atoi(s);
    uint8_t *f = malloc(N + 2); f[1] = 0;
    for (long n = 2; n <= N; n++) { int x = f[n / lp[n]] + R[lp[n]]; f[n] = x % k; }
    for (long n = 1; n < N; n++) if (!f[n] && !f[n + 1]) { fprintf(stderr, "input already has a zero pair at %ld\n", n); return 2; }
    /* order of primes */
    uint32_t *ord = malloc(np * 4);
    for (long j = 0; j < np; j++) ord[j] = pr[strcmp(order, "asc") ? np - 1 - j : j];
    if (!strcmp(order, "rand")) { srand(seed); for (long j = np - 1; j > 0; j--) { long r = rand() % (j + 1); uint32_t x = ord[j]; ord[j] = ord[r]; ord[r] = x; } }
    long changes = 1, pass = 0;
    while (changes) {
        changes = 0; pass++;
        for (long j = 0; j < np; j++) {
            long p = ord[j]; if (fixed[p]) continue;
            /* preference ranking: TARGET (rank 0), then alt[0], alt[1], ... ; other values rank 99.
               candidates = values strictly preferred over the current one, best first. */
            int cands[17], nc = 0, cur = 99;
            if (R[p] == t) cur = 0; else for (int b = 0; b < nalt; b++) if (alt[b] == R[p]) { cur = 1 + b; break; }
            if (cur > 0) cands[nc++] = t;
            for (int a = 0; a < nalt && 1 + a < cur; a++) if (alt[a] != t) cands[nc++] = alt[a];
            for (int c = 0; c < nc; c++) {
                int d = ((cands[c] - R[p]) % k + k) % k, ok = 1;
                for (long m = p; m <= N && ok; m += p) {
                    long x = m; int e = 0; while (x % p == 0) { x /= p; e++; }
                    int nf = (f[m] + e * d) % k;
                    if (nf == 0 && ((m - 1 >= 1 && f[m - 1] == 0) || (m + 1 <= N && f[m + 1] == 0))) ok = 0;
                }
                if (ok) {
                    for (long m = p; m <= N; m += p) { long x = m; int e = 0; while (x % p == 0) { x /= p; e++; } f[m] = (f[m] + e * d) % k; }
                    R[p] = cands[c]; changes++; break;
                }
            }
        }
        long ex = 0; for (long j = 0; j < np; j++) if (R[pr[j]] != t) ex++;
        fprintf(stderr, "pass %ld: changes=%ld exceptions(R!=%d)=%ld\n", pass, changes, t, ex);
    }
    /* final self-check */
    for (long n = 2; n <= N; n++) { int x = f[n / lp[n]] + R[lp[n]]; if ((uint8_t)(x % k) != f[n]) { fprintf(stderr, "f mismatch at %ld\n", n); return 3; } }
    for (long n = 1; n < N; n++) if (!f[n] && !f[n + 1]) { fprintf(stderr, "BUG: zero pair at %ld\n", n); return 3; }
    FILE *O = fopen(of, "w"); long cnt[32] = {0};
    for (long j = 0; j < np; j++) { fprintf(O, "%u %d\n", pr[j], R[pr[j]]); cnt[R[pr[j]]]++; }
    fclose(O);
    printf("order=%s seed=%u target=%d primes=%ld value counts:", order, seed, t, np);
    for (int a = 0; a < k; a++) printf(" %d:%ld", a, cnt[a]);
    printf("\n");
    printf("exceptions (R != %d):", t);
    long shown = 0; for (long j = 0; j < np; j++) if (R[pr[j]] != t) { if (shown < 400) printf(" %u:%d", pr[j], R[pr[j]]); shown++; }
    printf("\n#exceptions=%ld maxexception=", shown);
    for (long j = np - 1; j >= 0; j--) if (R[pr[j]] != t) { printf("%u", pr[j]); break; }
    printf("\n");
    return 0;
}
