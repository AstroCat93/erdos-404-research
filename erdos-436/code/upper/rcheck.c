/* rcheck.c -- third checker for the "pairtree-cert 1" format, written from certificate/FORMAT.md only.
 * Reads the decompressed stream on stdin. Usage: rcheck [expected_k expected_L expected_R2list]
 * e.g.  xz -dc k8_L1508324.cert.xz | rcheck 8 1508324 0,2,4,6
 * Prints header, verdict and statistics. Exit 0 iff the stream is a valid proof (no U lines)
 * and (if given) the header equals the expected one.
 * Validation is strict: 7-bit ASCII, LF line ends, no CR/tab/empty lines/extra spaces,
 * canonical decimals, nothing after "end\n".
 * Factorisation: smallest-prime-factor sieve to L+1 (independent of any listed data). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static char line[256];
static long lineno = 0;

static void die(const char *msg) {
    printf("INVALID at line %ld: %s\n", lineno, msg);
    exit(2);
}

/* read one line, strict; returns length (without LF); -1 on clean EOF (no bytes) */
static int rd(void) {
    int n = 0, c;
    lineno++;
    for (;;) {
        c = getchar();
        if (c == EOF) {
            if (n == 0) return -1;
            die("missing final LF");
        }
        if (c == '\n') break;
        if (c < 0x20 || c > 0x7e) die("non-printable or non-ASCII byte");
        if (n >= 250) die("line too long");
        line[n++] = (char)c;
    }
    line[n] = 0;
    if (n == 0) die("empty line");
    if (line[0] == ' ' || line[n - 1] == ' ') die("leading/trailing space");
    if (strstr(line, "  ")) die("double space");
    return n;
}

/* parse canonical decimal from s; sets *end; returns -1 if not canonical */
static long long pdec(const char *s, const char **end) {
    const char *p = s;
    long long v = 0;
    if (*p < '0' || *p > '9') return -1;
    if (*p == '0' && p[1] >= '0' && p[1] <= '9') return -1; /* leading zero */
    while (*p >= '0' && *p <= '9') {
        v = v * 10 + (*p - '0');
        if (v > 4000000000000LL) return -1;
        p++;
    }
    *end = p;
    return v;
}

int main(int argc, char **argv) {
    long long k, L;
    const char *e;
    int S2[64], s = 0;
    if (rd() < 0 || strcmp(line, "pairtree-cert 1")) die("bad magic");
    if (rd() < 0 || strncmp(line, "k ", 2)) die("bad k line");
    k = pdec(line + 2, &e);
    if (k < 2 || *e || k > 64) die("bad k");
    if (rd() < 0 || strncmp(line, "L ", 2)) die("bad L line");
    L = pdec(line + 2, &e);
    if (L < 1 || *e || L > 400000000) die("bad L");
    if (rd() < 0 || strncmp(line, "R2 ", 3)) die("bad R2 line");
    {
        const char *p = line + 3;
        for (;;) {
            long long v = pdec(p, &e);
            if (v < 0 || v >= k) die("bad R2 value");
            if (s > 0 && v <= S2[s - 1]) die("R2 not strictly increasing");
            S2[s++] = (int)v;
            if (*e == 0) break;
            if (*e != ' ') die("bad R2 separator");
            p = e + 1;
        }
    }
    if (rd() < 0 || strcmp(line, "begin")) die("bad begin");
    printf("HEADER k=%lld L=%lld R2=", k, L);
    for (int i = 0; i < s; i++) printf(i ? ",%d" : "%d", S2[i]);
    printf("\n");
    if (argc == 4) {
        char buf[512] = "";
        for (int i = 0; i < s; i++) { char t[16]; sprintf(t, i ? ",%d" : "%d", S2[i]); strcat(buf, t); }
        if (atoll(argv[1]) != k || atoll(argv[2]) != L || strcmp(argv[3], buf)) {
            printf("HEADER MISMATCH with expected k=%s L=%s R2=%s\n", argv[1], argv[2], argv[3]);
            return 3;
        }
        printf("HEADER matches expected\n");
    }
    /* sieve */
    long T = (long)L + 1;
    uint32_t *spf = calloc(T + 1, sizeof(uint32_t));
    int32_t *idx = malloc((T + 1) * sizeof(int32_t));
    long M = 0;
    for (long i = 2; i <= T; i++) {
        if (!spf[i]) {
            spf[i] = (uint32_t)i;
            idx[i] = (int32_t)M++;
            if ((long long)i * i <= T)
                for (long j = (long)i * i; j <= T; j += i) if (!spf[j]) spf[j] = (uint32_t)i;
        }
    }
    printf("M=pi(L+1)=%ld\n", M);
    int *R = malloc(sizeof(int) * (M + 1));
    long *stk_d = malloc(sizeof(long) * (M + 2));
    int *stk_j = malloc(sizeof(int) * (M + 2));
    long sp = 0, depth = 0;
    long long nB = 0, nL = 0, nU = 0, nLeqL = 0, maxn = 0, maxBdepth = -1, maxLeafDepth = 0;
    static long long leafdepth[4096];
    int first = 1;
    for (;;) {
        if (rd() < 0) die("unexpected EOF inside tree");
        if (line[0] == 'B' && line[1] == 0) {
            if (depth >= M) die("B at depth >= M");
            int nv = depth == 0 ? s : (int)k;
            (void)nv;
            stk_d[sp] = depth; stk_j[sp] = 0; sp++;
            R[depth] = depth == 0 ? S2[0] : 0;
            if (depth > maxBdepth) maxBdepth = depth;
            depth++;
            nB++;
            first = 0;
            continue;
        }
        if (first) die("root is not B (leaf root cannot be valid / or is a 1-node tree)");
        if (line[0] == 'U' && line[1] == 0) {
            nU++;
        } else if (line[0] == 'L' && line[1] == ' ') {
            long long n = pdec(line + 2, &e);
            if (n < 1 || *e) die("bad leaf integer");
            if (n > L) die("leaf n > L");
            for (int t = 0; t < 2; t++) {
                long m = (long)(n + t);
                long acc = 0;
                while (m > 1) {
                    uint32_t q = spf[m];
                    int ex = 0;
                    while (m % q == 0) { m /= q; ex++; }
                    long i = idx[q];
                    if (i >= depth) die("leaf uses unassigned prime");
                    acc += (long)ex * R[i];
                }
                if (acc % k) die("leaf sum not 0 mod k");
            }
            nL++;
            if (n == L) nLeqL++;
            if (n > maxn) maxn = n;
            if (depth < 4096) leafdepth[depth]++;
            if (depth > maxLeafDepth) maxLeafDepth = depth;
        } else die("unknown node line");
        /* advance */
        while (sp > 0) {
            long d = stk_d[sp - 1];
            int nv = d == 0 ? s : (int)k;
            if (stk_j[sp - 1] + 1 < nv) {
                stk_j[sp - 1]++;
                R[d] = d == 0 ? S2[stk_j[sp - 1]] : stk_j[sp - 1];
                depth = d + 1;
                break;
            }
            sp--;
        }
        if (sp == 0) break;
    }
    if (rd() < 0 || strcmp(line, "end")) die("missing end");
    if (getchar() != EOF) { lineno++; die("bytes after end"); }
    printf("node_lines=%lld internal(B)=%lld leaves(L)=%lld unresolved(U)=%lld\n", nB + nL + nU, nB, nL, nU);
    printf("deepest_branch_depth=%lld (prime p_%lld) max_leaf_depth=%lld max_leaf_n=%lld leaves_with_n_eq_L=%lld\n",
           maxBdepth, maxBdepth, maxLeafDepth, maxn, nLeqL);
    {   /* report prime at deepest branch depth */
        long c = 0;
        for (long i = 2; i <= T; i++) if (spf[i] == i) { if (c == maxBdepth) { printf("p_%lld=%ld\n", maxBdepth, i); break; } c++; }
    }
    printf("leaf depth histogram:");
    for (long d = 0; d <= maxLeafDepth && d < 4096; d++) if (leafdepth[d]) printf(" %ld:%lld", d, leafdepth[d]);
    printf("\n");
    if (nU) { printf("VERDICT: well-formed PARTIAL tree (%lld open cases), NOT a proof\n", nU); return 1; }
    printf("VERDICT: VALID PROOF of C(k=%lld, L=%lld, S2)\n", k, L);
    return 0;
}
