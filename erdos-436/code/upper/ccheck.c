/* Second, independent checker for 'pairtree-cert 1' certificates (C99).
 * Written from certificate/FORMAT.md only.
 *
 * Differences from pcheck.py on purpose:
 *  - leaf condition 2 is checked by TRIAL DIVISION of n and n+1 by the
 *    assigned primes p_0..p_{d-1} only (no factor sieve): the cofactor must be 1;
 *  - the tree is consumed with a per-depth "children remaining" counter array.
 *
 * Usage: ccheck K L S2 [WALKFILE OUTFILE] < raw_stream
 *   K, L, S2 (comma list) = target statement C(K, L, S2); the header must match.
 *   WALKFILE (optional): lines "id v_0 v_1 ... v_{T-1}" = assignment R(p_i)=v_i.
 *   For each, the leaf reached by walking the tree is written to OUTFILE as
 *   "id depth n" (n = -1 for U, -2 if the vector was too short).
 * Exit 0 = valid proof of the target with no U; 1 = reject; 2 = usage error.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static void die(long long lineno, const char *msg, const char *line) {
    printf("VERDICT REJECT line %lld: %s%s%.40s%s\n", lineno, msg,
           line ? " [" : "", line ? line : "", line ? "]" : "");
    exit(1);
}

/* parse canonical decimal from s[0..len); returns -1 if not canonical */
static long long canon(const char *s, size_t len) {
    if (len == 0 || len > 18) return -1;
    if (len > 1 && s[0] == '0') return -1;
    long long v = 0;
    for (size_t i = 0; i < len; i++) {
        if (s[i] < '0' || s[i] > '9') return -1;
        v = v * 10 + (s[i] - '0');
    }
    return v;
}

static char *buf = NULL; static size_t cap = 0;
static long long lineno = 0;
/* read one line; returns length without LF, -1 at clean EOF; dies if no final LF / non-ASCII */
static long getl(void) {
    ssize_t r = getline(&buf, &cap, stdin);
    if (r < 0) return -1;
    lineno++;
    if (buf[r - 1] != '\n') die(lineno, "last line lacks LF", NULL);
    for (ssize_t i = 0; i < r; i++)
        if ((unsigned char)buf[i] > 0x7f || buf[i] == 0) die(lineno, "non-ASCII or NUL byte", NULL);
    buf[r - 1] = 0;
    return (long)(r - 1);
}

int main(int argc, char **argv) {
    if (argc != 4 && argc != 6) { fprintf(stderr, "usage\n"); return 2; }
    clock_t t0 = clock();
    int tk = atoi(argv[1]); long long tL = atoll(argv[2]);
    int tS2[64], ts = 0;
    { char *s = strdup(argv[3]), *tok = strtok(s, ","); while (tok) { tS2[ts++] = atoi(tok); tok = strtok(NULL, ","); } }

    long n;
    /* header */
    if ((n = getl()) < 0 || strcmp(buf, "pairtree-cert 1")) die(lineno, "bad magic", buf);
    if ((n = getl()) < 0 || strncmp(buf, "k ", 2)) die(lineno, "bad k line", buf);
    long long k = canon(buf + 2, n - 2); if (k < 2) die(lineno, "bad k", buf);
    if ((n = getl()) < 0 || strncmp(buf, "L ", 2)) die(lineno, "bad L line", buf);
    long long L = canon(buf + 2, n - 2); if (L < 1) die(lineno, "bad L", buf);
    if ((n = getl()) < 0 || strncmp(buf, "R2 ", 3)) die(lineno, "bad R2 line", buf);
    int S2[64], s = 0;
    {
        char *p = buf + 3, *e = buf + n;
        while (1) {
            char *q = memchr(p, ' ', e - p); if (!q) q = e;
            long long v = canon(p, q - p);
            if (v < 0 || v > k - 1) die(lineno, "bad R2 value", buf);
            if (s > 0 && v <= S2[s - 1]) die(lineno, "R2 not strictly increasing", buf);
            if (s >= 64) die(lineno, "too many R2 values", buf);
            S2[s++] = (int)v;
            if (q == e) break;
            p = q + 1;
        }
    }
    if ((n = getl()) < 0 || strcmp(buf, "begin")) die(lineno, "missing begin", buf);
    /* target match */
    int match = (k == tk && L == tL && s == ts);
    for (int i = 0; match && i < s; i++) if (S2[i] != tS2[i]) match = 0;

    /* primes <= L+1 */
    long long N = L + 1;
    char *comp = calloc(N + 1, 1);
    long long M = 0;
    for (long long i = 2; i <= N; i++) if (!comp[i]) { M++; for (long long j = i * i; j <= N; j += i) comp[j] = 1; }
    long long *P = malloc(sizeof(long long) * (M + 1));
    { long long c = 0; for (long long i = 2; i <= N; i++) if (!comp[i]) P[c++] = i; }
    free(comp);

    /* walk vectors */
    int nt = 0, T = 0; int **vec = NULL; long long *wid = NULL; FILE *wout = NULL;
    int **alive = NULL; int *nalive = NULL;
    if (argc == 6) {
        FILE *wf = fopen(argv[4], "r"); if (!wf) { perror("walkfile"); return 2; }
        char *lb = NULL; size_t lc = 0; int capv = 0;
        while (getline(&lb, &lc, wf) > 0) {
            if (nt == capv) { capv = capv ? 2 * capv : 64; vec = realloc(vec, sizeof(int*) * capv); wid = realloc(wid, sizeof(long long) * capv); }
            char *p = lb; wid[nt] = strtoll(p, &p, 10);
            int c = 0, cv = 64; int *v = malloc(sizeof(int) * cv);
            while (1) { char *q; long x = strtol(p, &q, 10); if (q == p) break; if (c == cv) { cv *= 2; v = realloc(v, sizeof(int) * cv); } v[c++] = (int)x; p = q; }
            if (nt == 0) T = c; else if (c != T) { fprintf(stderr, "ragged walkfile\n"); return 2; }
            vec[nt++] = v;
        }
        fclose(wf);
        wout = fopen(argv[5], "w");
        alive = calloc(M + 1, sizeof(int*)); nalive = calloc(M + 1, sizeof(int));
        alive[0] = malloc(sizeof(int) * (nt ? nt : 1));
        for (int i = 0; i < nt; i++) alive[0][i] = i;
        nalive[0] = nt;
    }

    int *R = malloc(sizeof(int) * (M + 1));
    int *left = malloc(sizeof(int) * (M + 1));   /* children still to read at open B of depth d (incl. current) */
    int *cur = malloc(sizeof(int) * (M + 1));    /* index of current child of open B at depth d */
    long long depth = 0, top = -1;              /* top = depth of deepest open B, -1 if none */
    long long nB = 0, nL = 0, nU = 0, maxd = 0, maxn = 0, maxncnt = 0;
    int root_done = 0;
#define VAL(d, j) ((d) == 0 ? S2[(j)] : (j))
#define NCH(d) ((d) == 0 ? s : (int)k)
#define FILTER(d) do { if (alive) { long long d1 = (d) + 1; if (!alive[d1]) alive[d1] = malloc(sizeof(int) * (nt ? nt : 1)); int c = 0; \
        for (int a = 0; a < nalive[d]; a++) { int t = alive[d][a]; if ((d) >= T) { fprintf(wout, "%lld %lld -2\n", wid[t], (long long)(d)); } else if (vec[t][d] == R[d]) alive[d1][c++] = t; } \
        nalive[d1] = c; } } while (0)

    while (!root_done) {
        n = getl();
        if (n < 0) die(lineno, "stream ended inside the tree", NULL);
        if (n == 1 && buf[0] == 'B') {
            if (depth >= M) die(lineno, "B at depth >= M", buf);
            nB++;
            top = depth; cur[depth] = 0; left[depth] = NCH(depth); R[depth] = VAL(depth, 0);
            FILTER(depth);
            depth++;
            if (depth > maxd) maxd = depth;
            continue;
        }
        if (n == 1 && buf[0] == 'U') {
            nU++;
            if (alive) for (int a = 0; a < nalive[depth]; a++) fprintf(wout, "%lld %lld -1\n", wid[alive[depth][a]], depth);
        } else if (n >= 3 && buf[0] == 'L' && buf[1] == ' ') {
            long long v = canon(buf + 2, n - 2);
            if (v < 0) die(lineno, "leaf value not canonical", buf);
            if (v < 1 || v > L) die(lineno, "leaf n outside [1, L]", buf);
            for (int w = 0; w < 2; w++) {
                unsigned long long m = (unsigned long long)v + w; long long sum = 0;
                for (long long i = 0; i < depth && m > 1; i++) {
                    unsigned long long p = (unsigned long long)P[i];
                    while (m % p == 0) { m /= p; sum += R[i]; }
                }
                if (m != 1) die(lineno, w ? "n+1 has an unassigned prime factor" : "n has an unassigned prime factor", buf);
                if (sum % k) die(lineno, w ? "f(n+1) != 0 mod k" : "f(n) != 0 mod k", buf);
            }
            nL++;
            if (v > maxn) { maxn = v; maxncnt = 1; } else if (v == maxn) maxncnt++;
            if (alive) for (int a = 0; a < nalive[depth]; a++) fprintf(wout, "%lld %lld %lld\n", wid[alive[depth][a]], depth, v);
        } else die(lineno, "unrecognised node line", buf);
        /* advance */
        while (1) {
            if (top < 0) { root_done = 1; break; }
            if (--left[top] > 0) {
                cur[top]++; R[top] = VAL(top, cur[top]); FILTER(top); depth = top + 1; break;
            }
            /* B at depth top finished: find the next open B above it */
            long long d = top - 1;
            while (d >= 0 && left[d] <= 0) d--;   /* should not happen: parents always have left>=1 */
            top = d;
        }
    }
    n = getl();
    if (n < 0 || strcmp(buf, "end")) die(lineno, "expected end", n < 0 ? NULL : buf);
    if (getl() >= 0) die(lineno, "data after end", buf);
    if (wout) fclose(wout);
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("k=%lld L=%lld S2=", k, L); for (int i = 0; i < s; i++) printf("%s%d", i ? "," : "", S2[i]);
    printf(" M=%lld B=%lld L_leaves=%lld U=%lld nodes=%lld max_depth=%lld max_leaf_n=%lld (x%lld) lines=%lld cpu_s=%.2f\n",
           M, nB, nL, nU, nB + nL + nU, maxd, maxn, maxncnt, lineno, secs);
    if (!match) { printf("VERDICT REJECT valid tree but header (k,L,S2) differs from target\n"); return 1; }
    if (nU) { printf("VERDICT REJECT well-formed partial tree with %lld U leaves\n", nU); return 1; }
    printf("VERDICT PROOF of C(%lld, %lld, S2)\n", k, L);
    return 0;
}
