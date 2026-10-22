/* Independent regeneration of the CANONICAL 'pairtree-cert 1' tree for (k, L, S2),
 * written from the canonical-form rule in FORMAT.md section 4 only:
 *   node at depth d >= 1 is "L n" iff some n <= L satisfies leaf conditions 1-3 there,
 *   with n the least such; otherwise "B" if d < M, "U" if d = M; the root is "B".
 * Optimisation (proved in the comment below): at a node of depth d >= 1 only pairs
 * whose largest prime has index exactly d-1 can be the least closing pair.
 *   Proof: the node's ancestors at depths 1..d-1 are B, so at its parent (depth d-1)
 *   no pair with largest-prime index <= d-2 closed; those pairs' sums use only
 *   R(p_0..p_{d-2}), which are unchanged at depth d.  Pairs with index >= d are
 *   excluded by condition 2.  (For d = 1 the parent is the root; no pair has index < 0.)
 * Usage: regen K L S2 > stream
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int K; static long long L, M; static int S2[64], s2n;
static int *spf; static int *pidx;
/* pairs bucketed by largest-prime index: for bucket b, pairs [bstart[b], bstart[b+1]) */
static long long *bstart; static int *pn;           /* pair n */
static long long *fstart; static int *fidx; static unsigned char *fexp, *fwhich; /* factor entries */
static int R[200000];
static char obuf[1 << 20]; static size_t olen = 0;
static void out(const char *s) { size_t l = strlen(s); if (olen + l > sizeof obuf) { fwrite(obuf, 1, olen, stdout); olen = 0; } memcpy(obuf + olen, s, l); olen += l; }

static void node(long long d) {
    /* d >= 1 */
    long long b = d - 1;
    for (long long q = bstart[b]; q < bstart[b + 1]; q++) {
        long long s0 = 0, s1 = 0;
        for (long long f = fstart[q]; f < fstart[q + 1]; f++) {
            long long t = (long long)fexp[f] * R[fidx[f]];
            if (fwhich[f]) s1 += t; else s0 += t;
        }
        if (s0 % K == 0 && s1 % K == 0) { char tmp[32]; sprintf(tmp, "L %d\n", pn[q]); out(tmp); return; }
    }
    if (d < M) {
        out("B\n");
        for (int v = 0; v < K; v++) { R[d] = v; node(d + 1); }
    } else out("U\n");
}

int main(int argc, char **argv) {
    K = atoi(argv[1]); L = atoll(argv[2]);
    { char *s = strdup(argv[3]), *t = strtok(s, ","); while (t) { S2[s2n++] = atoi(t); t = strtok(NULL, ","); } }
    long long N = L + 1;
    spf = calloc(N + 1, sizeof(int)); pidx = malloc(sizeof(int) * (N + 1));
    M = 0;
    for (long long i = 2; i <= N; i++) if (!spf[i]) { pidx[i] = (int)M++; for (long long j = i; j <= N; j += i) if (!spf[j]) spf[j] = (int)i; }
    if (M >= 200000) { fprintf(stderr, "M too large\n"); return 2; }
    /* bucket count */
    long long *cnt = calloc(M + 1, sizeof(long long)), *fcnt = calloc(M + 1, sizeof(long long));
    int *mx = malloc(sizeof(int) * (L + 1)); unsigned char *nf = malloc(L + 1);
    for (long long n = 1; n <= L; n++) {
        int m = -1, c = 0;
        for (int w = 0; w < 2; w++) { long long x = n + w; while (x > 1) { int p = spf[x]; if (pidx[p] > m) m = pidx[p]; c++; while (x % p == 0) x /= p; } }
        mx[n] = m; nf[n] = (unsigned char)c; cnt[m]++; fcnt[m] += c;
    }
    bstart = malloc(sizeof(long long) * (M + 2)); long long *fb = malloc(sizeof(long long) * (M + 2));
    bstart[0] = 0; fb[0] = 0;
    for (long long b = 0; b < M; b++) { bstart[b + 1] = bstart[b] + cnt[b]; fb[b + 1] = fb[b] + fcnt[b]; }
    long long NP = bstart[M], NF = fb[M];
    pn = malloc(sizeof(int) * NP); fstart = malloc(sizeof(long long) * (NP + 1));
    fidx = malloc(sizeof(int) * NF); fexp = malloc(NF); fwhich = malloc(NF);
    long long *bp = calloc(M + 1, sizeof(long long)), *bf = calloc(M + 1, sizeof(long long));
    /* fill, n increasing so each bucket is sorted by n */
    for (long long n = 1; n <= L; n++) {
        int b = mx[n]; long long q = bstart[b] + bp[b]++; long long f = fb[b] + bf[b];
        pn[q] = (int)n; fstart[q] = f;   /* temporary: fstart relative ordering fixed below */
        for (int w = 0; w < 2; w++) { long long x = n + w; while (x > 1) { int p = spf[x], e = 0; while (x % p == 0) { x /= p; e++; } fidx[f] = pidx[p]; fexp[f] = (unsigned char)e; fwhich[f] = (unsigned char)w; f++; } }
        bf[b] += nf[n];
    }
    fstart[NP] = NF;
    /* fstart[q] set per pair in bucket order; since pairs and factor blocks are laid out
       consecutively inside each bucket and buckets are consecutive, fstart is monotone */
    for (long long q = 0; q + 1 <= NP; q++) if (q + 1 < NP && fstart[q + 1] < fstart[q]) { fprintf(stderr, "layout bug\n"); return 3; }
    fprintf(stderr, "M=%lld pairs=%lld factor entries=%lld; bucket sizes b=0..9:", M, NP, NF);
    for (int b = 0; b < 10 && b < M; b++) fprintf(stderr, " %lld", cnt[b]);
    fprintf(stderr, "\n");
    printf("pairtree-cert 1\nk %d\nL %lld\nR2", K, L);
    for (int i = 0; i < s2n; i++) printf(" %d", S2[i]);
    printf("\nbegin\n");
    fflush(stdout);
    out("B\n");
    for (int i = 0; i < s2n; i++) { R[0] = S2[i]; node(1); }
    out("end\n");
    fwrite(obuf, 1, olen, stdout);
    return 0;
}
