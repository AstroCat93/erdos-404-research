/* pairtree.c -- exhaustive depth-first case tree for pairs of consecutive k-th power
 * residues, emitting a preorder certificate stream (see certificate/FORMAT.md).
 *
 * Model.  R assigns a value in Z/k to each prime q <= L+1; f_R(m) = sum_q v_q(m) R(q) mod k.
 * Primes are branched on in increasing order p_0=2, p_1=3, ...; at the prime 2 the values
 * of the --r2 list are used, at every other prime all values 0..k-1, always in increasing
 * order.  No unit normalisation.  A node at depth d (R fixed on p_0..p_{d-1}) is a leaf
 * "L n" as soon as some n <= L has every prime factor of n(n+1) among p_0..p_{d-1} and
 * f_R(n) = f_R(n+1) = 0; n is the least such.  A node that is not closed at depth T (the
 * depth cap) is written "U" (unresolved).  With T = pi(L+1) (the default) a "U" is a full
 * assignment with no closing pair at all.
 *
 * Since the parent of a depth-d node was not closed, a closing pair of a depth-d node has
 * largest prime exactly p_{d-1}.  Pairs are therefore grouped by the index of the largest
 * prime of n(n+1), and only the group of the newly assigned prime is examined.
 *
 * Usage: pairtree k L [--r2 v,v,...|all|even] [--maxdepth T] [--out FILE|-]
 *                    [--stop-at-first-U] [--witness-out FILE] [--maxnodes N] [--order v,v,...]
 *                    [--unres-out FILE]   (one line per unresolved leaf: its values R(p_0) .. R(p_{T-1}))
 * --order permutes the values tried at primes other than 2.  It is meant only for the search
 * of witnesses (--stop-at-first-U); it cannot be combined with --out, because the certificate
 * format fixes the increasing order.
 * Output: the certificate (if --out), statistics on stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int K; static long L, N;
static int32_t *spf, *pidx;          /* pidx[p] = index of prime p, -1 otherwise */
static int32_t *primes; static int NP;
/* pair storage, grouped by g = index of the largest prime dividing n(n+1) */
static int64_t *gstart;              /* pairs of group g: gstart[g] .. gstart[g+1]-1 */
static int32_t *pn;                  /* n */
static uint8_t *pe;                  /* exponent (mod K) of the group prime in n(n+1) */
static int64_t *fstart;              /* other factors of pair i: fstart[i] .. fstart[i+1]-1 */
static int32_t *fidx; static uint8_t *fco, *fsame;   /* prime index, exponent mod K, same side as group prime? */

static int allow0[32], nallow0, allowx[32], nallowx;
static int T;                        /* depth cap */
static int32_t *Rv;                  /* current assignment by prime index */
static int32_t *closeN;              /* closeN[d*K+v]: least closing n for value v at prime d, 0 if none */
static int32_t *cpos;                /* next child position at branching level d */

static FILE *out = NULL; static char *obuf; static size_t olen = 0; static const size_t OCAP = 1 << 22;
static void oflush(void) { if (out && olen) { if (fwrite(obuf, 1, olen, out) != olen) { perror("write"); exit(2); } } olen = 0; }
static inline void oput(const char *s, int n) { if (!out) return; if (olen + n + 32 > OCAP) oflush(); memcpy(obuf + olen, s, n); olen += n; }
static inline void oleaf(long n) {
    if (!out) return;
    char t[32]; int i = 31; t[i--] = '\n'; do { t[i--] = '0' + n % 10; n /= 10; } while (n);
    t[i--] = ' '; t[i] = 'L'; oput(t + i, 32 - i);
}

/* statistics */
static long long nB = 0, nL = 0, nU = 0; static long maxleafn = 0; static long long nmaxleaf = 0;
static long long *Bdepth, *Ldepth; static int maxdep = 0;
static int32_t *U0, *U0n; static int lcp = -1, lcpn = -1;   /* first unresolved vector (raw, unit-normalised) and LCPs */
static long long nUnorm_first = 0;                          /* unresolved leaves whose normalised vector equals the first one */
static FILE *unresf = NULL;
static int *inv; static int stopU = 0; static const char *witfile = NULL; static long long maxnodes = -1;

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static void build(void) {
    N = L + 1;
    spf = calloc(N + 1, sizeof(int32_t)); pidx = malloc((N + 1) * sizeof(int32_t));
    for (long i = 0; i <= N; i++) pidx[i] = -1;
    for (long i = 2; i <= N; i++) if (!spf[i]) { for (long j = i; j <= N; j += i) if (!spf[j]) spf[j] = (int32_t)i; }
    NP = 0; for (long i = 2; i <= N; i++) if (spf[i] == i) NP++;
    primes = malloc(NP * sizeof(int32_t)); NP = 0;
    for (long i = 2; i <= N; i++) if (spf[i] == i) { pidx[i] = NP; primes[NP++] = (int32_t)i; }
    /* pass 1: group and factor count of each n */
    int32_t *grp = malloc((L + 1) * sizeof(int32_t)); uint8_t *nfac = malloc(L + 1);
    gstart = calloc(NP + 2, sizeof(int64_t));
    for (long n = 1; n <= L; n++) {
        int g = -1, c = 0;
        for (int s = 0; s < 2; s++) { long m = n + s; while (m > 1) { int p = spf[m]; while (m % p == 0) m /= p; if (pidx[p] > g) g = pidx[p]; c++; } }
        grp[n] = g; nfac[n] = (uint8_t)(c - 1); gstart[g + 1]++;
    }
    for (int g = 0; g < NP; g++) gstart[g + 1] += gstart[g];
    long npairs = gstart[NP];
    pn = malloc(npairs * sizeof(int32_t)); pe = malloc(npairs); fstart = malloc((npairs + 1) * sizeof(int64_t));
    int64_t *pos = malloc((NP + 1) * sizeof(int64_t)); memcpy(pos, gstart, (NP + 1) * sizeof(int64_t));
    int64_t *slot = malloc((L + 1) * sizeof(int64_t));
    for (long n = 1; n <= L; n++) slot[n] = pos[grp[n]]++;
    /* fstart: prefix sums of factor counts in slot order */
    uint8_t *cnt = malloc(npairs);
    for (long n = 1; n <= L; n++) cnt[slot[n]] = nfac[n];
    fstart[0] = 0; for (long i = 0; i < npairs; i++) fstart[i + 1] = fstart[i] + cnt[i];
    long nf = fstart[npairs];
    fidx = malloc(nf * sizeof(int32_t)); fco = malloc(nf); fsame = malloc(nf);
    for (long n = 1; n <= L; n++) {
        long i = slot[n]; int g = grp[n]; int gs = -1; int ge = 0;
        /* locate the side of the group prime */
        for (int s = 0; s < 2; s++) { long m = n + s; if (m % primes[g] == 0) { gs = s; while (m % primes[g] == 0) { m /= primes[g]; ge++; } } }
        pn[i] = (int32_t)n; pe[i] = (uint8_t)(ge % K);
        long j = fstart[i];
        for (int s = 0; s < 2; s++) { long m = n + s; while (m > 1) { int p = spf[m]; int e = 0; while (m % p == 0) { m /= p; e++; }
                if (pidx[p] == g) continue; fidx[j] = pidx[p]; fco[j] = (uint8_t)(e % K); fsame[j] = (uint8_t)(s == gs); j++; } }
        if (j != fstart[i + 1]) { fprintf(stderr, "internal factor count error at n=%ld\n", n); exit(3); }
    }
    free(grp); free(nfac); free(pos); free(slot); free(cnt);
    fprintf(stderr, "k=%d L=%ld primes<=L+1: %d  pairs: %ld  factor entries: %ld\n", K, L, NP, npairs, nf);
}

/* compute closeN for branching level d under the current assignment Rv[0..d-1] */
static void level(int d) {
    int32_t *c = closeN + (long)d * K; for (int v = 0; v < K; v++) c[v] = 0;
    const int *al = d ? allowx : allow0; int na = d ? nallowx : nallow0; int left = na;
    for (int64_t i = gstart[d]; i < gstart[d + 1] && left; i++) {
        int A = 0, B = 0;
        for (int64_t j = fstart[i]; j < fstart[i + 1]; j++) { int t = fco[j] * Rv[fidx[j]]; if (fsame[j]) A += t; else B += t; }
        if (B % K) continue;
        int e = pe[i];
        for (int a = 0; a < na; a++) { int v = al[a]; if (!c[v] && (A + e * v) % K == 0) { c[v] = pn[i]; left--; } }
    }
}

static void unresolved(int d) {   /* node at depth d == T, assignment Rv[0..d-1] */
    nU++;
    /* unit normalisation for the report only: multiply by the inverse of the first unit value */
    int u = 1; for (int i = 0; i < d; i++) if (gcd(Rv[i], K) == 1) { u = inv[Rv[i]]; break; }
    if (nU == 1) { for (int i = 0; i < d; i++) { U0[i] = Rv[i]; U0n[i] = (Rv[i] * u) % K; } lcp = d; lcpn = d; nUnorm_first = 1; }
    else {
        int i = 0; while (i < lcp && Rv[i] == U0[i]) i++; lcp = i;
        i = 0; while (i < d && (Rv[i] * u) % K == U0n[i]) i++; if (i < lcpn) lcpn = i; if (i == d) nUnorm_first++;
    }
    oput("U\n", 2);
    if (unresf) { for (int i = 0; i < d; i++) fprintf(unresf, i ? " %d" : "%d", Rv[i]); fputc('\n', unresf); }
    if (stopU) {
        if (witfile) { FILE *w = fopen(witfile, "w"); for (int i = 0; i < d; i++) fprintf(w, "%d %d\n", primes[i], Rv[i]); fclose(w); }
        fprintf(stderr, "first unresolved node at depth %d (prime p_%d = %d) after %lld nodes\n", d, d - 1, primes[d - 1], nB + nL + nU);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: pairtree k L [--r2 v,..|all|even] [--maxdepth T] [--out FILE|-] [--stop-at-first-U] [--witness-out FILE] [--maxnodes N]\n"); return 1; }
    K = atoi(argv[1]); L = atol(argv[2]);
    if (K < 2 || K > 16 || L < 1 || L > 1000000000L) { fprintf(stderr, "bad k or L\n"); return 1; }
    const char *r2 = "all", *outf = NULL, *order = NULL; long Tcap = -1;
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--r2")) r2 = argv[++i];
        else if (!strcmp(argv[i], "--maxdepth")) Tcap = atol(argv[++i]);
        else if (!strcmp(argv[i], "--out")) outf = argv[++i];
        else if (!strcmp(argv[i], "--stop-at-first-U")) stopU = 1;
        else if (!strcmp(argv[i], "--witness-out")) witfile = argv[++i];
        else if (!strcmp(argv[i], "--maxnodes")) maxnodes = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--order")) order = argv[++i];
        else if (!strcmp(argv[i], "--unres-out")) { unresf = fopen(argv[++i], "w"); if (!unresf) { perror(argv[i]); return 1; } }
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 1; }
    }
    nallowx = K; for (int v = 0; v < K; v++) allowx[v] = v;
    if (order) {
        if (outf) { fprintf(stderr, "--order cannot be combined with --out\n"); return 1; }
        int seen = 0, n = 0; char buf[256]; strncpy(buf, order, 255); buf[255] = 0;
        for (char *t = strtok(buf, ","); t; t = strtok(NULL, ",")) { int v = atoi(t); if (v < 0 || v >= K || ((seen >> v) & 1) || n >= K) { fprintf(stderr, "bad --order\n"); return 1; } seen |= 1 << v; allowx[n++] = v; }
        if (n != K) { fprintf(stderr, "--order must be a permutation of 0..k-1\n"); return 1; }
    }
    if (!strcmp(r2, "all")) { nallow0 = K; for (int v = 0; v < K; v++) allow0[v] = v; }
    else if (!strcmp(r2, "even")) { nallow0 = 0; for (int v = 0; v < K; v += 2) allow0[nallow0++] = v; }
    else { nallow0 = 0; char buf[256]; strncpy(buf, r2, 255); buf[255] = 0; for (char *t = strtok(buf, ","); t; t = strtok(NULL, ",")) { int v = atoi(t); if (v < 0 || v >= K || (nallow0 && v <= allow0[nallow0 - 1])) { fprintf(stderr, "--r2 must be strictly increasing values in [0,k)\n"); return 1; } allow0[nallow0++] = v; } }
    inv = calloc(K, sizeof(int)); for (int a = 1; a < K; a++) for (int b = 1; b < K; b++) if (a * b % K == 1) inv[a] = b;
    clock_t t0 = clock();
    build();
    T = (Tcap < 0 || Tcap > NP) ? NP : (int)Tcap;
    double tb = (double)(clock() - t0) / CLOCKS_PER_SEC;
    Rv = calloc(NP + 1, sizeof(int32_t)); closeN = malloc(((long)T + 1) * K * sizeof(int32_t)); cpos = calloc(T + 1, sizeof(int32_t));
    Bdepth = calloc(T + 2, sizeof(long long)); Ldepth = calloc(T + 2, sizeof(long long));
    U0 = malloc((T + 1) * sizeof(int32_t)); U0n = malloc((T + 1) * sizeof(int32_t));
    if (outf) { out = strcmp(outf, "-") ? fopen(outf, "w") : stdout; if (!out) { perror(outf); return 1; } obuf = malloc(OCAP); }
    if (out) { char h[512]; int n = snprintf(h, sizeof h, "pairtree-cert 1\nk %d\nL %ld\nR2", K, L); oput(h, n);
        for (int a = 0; a < nallow0; a++) { n = snprintf(h, sizeof h, " %d", allow0[a]); oput(h, n); } oput("\nbegin\n", 7); }
    int aborted = 0, stopped = 0;
    /* root: depth 0 is never closed (no prime assigned); T >= 1 always since 2 <= L+1 */
    oput("B\n", 2); nB++; Bdepth[0]++; level(0); cpos[0] = 0; int d = 0;
    while (d >= 0) {
        const int *al = d ? allowx : allow0; int na = d ? nallowx : nallow0;
        if (cpos[d] == na) { d--; continue; }
        int v = al[cpos[d]++];
        int32_t cn = closeN[(long)d * K + v];
        if (cn) { oleaf(cn); nL++; Ldepth[d + 1]++; if (cn > maxleafn) { maxleafn = cn; nmaxleaf = 0; } if (cn == maxleafn) nmaxleaf++; if (d + 1 > maxdep) maxdep = d + 1; continue; }
        Rv[d] = v;
        if (d + 1 == T) { if (d + 1 > maxdep) maxdep = d + 1; unresolved(d + 1); if (stopU) { stopped = 1; break; } continue; }
        if (maxnodes >= 0 && nB + nL + nU >= maxnodes) { aborted = 1; break; }
        oput("B\n", 2); nB++; Bdepth[d + 1]++; level(d + 1); cpos[d + 1] = 0; d++;
    }
    if (out) { if (!aborted && !stopped) oput("end\n", 4); oflush(); if (out != stdout) fclose(out); }
    if (unresf) fclose(unresf);
    double tt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    if (order) fprintf(stderr, "value order at primes > 2: %s\n", order);
    fprintf(stderr, "RESULT k=%d L=%ld R2=%s T=%d (p_T=%d)%s%s: internal(B)=%lld leaves(L)=%lld unresolved(U)=%lld total=%lld maxdepth=%d max_leaf_n=%ld (x%lld) build=%.2fs total=%.2fs\n",
            K, L, r2, T, primes[T - 1], aborted ? " [ABORTED at maxnodes]" : "", stopped ? " [STOPPED at first U]" : "",
            nB, nL, nU, nB + nL + nU, maxdep, maxleafn, nmaxleaf, tb, tt);
    fprintf(stderr, "B per depth:"); for (int i = 0; i <= T; i++) if (Bdepth[i]) fprintf(stderr, " %d:%lld", i, Bdepth[i]); fprintf(stderr, "\n");
    fprintf(stderr, "L per depth:"); for (int i = 0; i <= T; i++) if (Ldepth[i]) fprintf(stderr, " %d:%lld", i, Ldepth[i]); fprintf(stderr, "\n");
    if (nU) {
        fprintf(stderr, "unresolved: literal common prefix length %d:", lcp); for (int i = 0; i < lcp; i++) fprintf(stderr, " %d", U0[i]); fprintf(stderr, "\n");
        fprintf(stderr, "unresolved: unit-normalised common prefix length %d (primes up to %d):", lcpn, lcpn ? primes[lcpn - 1] : 0);
        for (int i = 0; i < lcpn; i++) fprintf(stderr, " %d", U0n[i]); fprintf(stderr, "\n");
        fprintf(stderr, "unresolved: leaves whose normalised vector equals the first one: %lld\n", nUnorm_first);
        int show = T < 100 ? T : 100;
        fprintf(stderr, "first unresolved vector (first %d of %d values, raw):", show, T); for (int i = 0; i < show; i++) fprintf(stderr, " %d", U0[i]); fprintf(stderr, "\n");
    }
    return 0;
}
