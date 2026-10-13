// dfsW.c -- program C of track R3N (round 3): windowed depth-first search.
// Decides "f(a,2) >= K ?" for even a; on failure prints the exact f(a,2) (the maximal valuation
// over all finite sets A with min A = a); on success writes an explicit witness set.
//
// Notation: S_N = sum_{n in A, n < N} n!.  A path is alive at N iff v_2(S_N) >= v_2(N!).
// Pair step N -> N+2 (N even): S_{N+2} = S_N + d, d in {0, N!, (N+1)!, N!+(N+1)!}.
//
// Two-level scheme.  Boundaries M_0 = a+2 < M_1 < ... (even).  Window j covers the pair steps
// N = M_j, M_j+2, ..., M_{j+1}-2 and the bit range [lo_j, lo_j + 64*WL), lo_j = v_2(M_j!), where
// M_{j+1} is the largest even M with v_2(M!) - lo_j <= 64*WL (or the final gate if it fits).
// Inside a window only the window bits of S_N are tracked (WL limbs): every operand vanishes
// below bit lo_j, so these bits evolve exactly, and every aliveness test and every death
// valuation inside the window reads only bits < v_2(M_{j+1}!) <= lo_j + 64*WL.
// A survivor at M_{j+1} is then materialised at full precision (mod 2^K) by adding/subtracting
// the factorials along the difference between consecutive survivor paths (DFS order gives
// lexicographic order, so this is a prefix-tree walk), and the search recurses.
// Every alive path is enumerated (no deduplication), so correctness does not depend on hashing.
//
// Usage: dfsWp a K [witnessfile] [profilefile]
// dfsWp = dfsW plus a population profile: the number of alive paths at every window boundary
// M_j, and the deepest stage N at which some path is alive.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#ifndef WL
#define WL 4
#endif
typedef uint64_t u64;
typedef unsigned __int128 u128;

static long a; static int K, LK; static u64 topmask;
static long Nfin;                  // least even N with v2(N!) >= K
static long best = -1;             // max death valuation
static long long nodes = 0, survivors = 0, fulladds = 0, deaths = 0;
static int maxlevel = 0;
static double t0, tlast;
static const char *wfile = NULL;
static int init_e1 = 0;
static const char *pfile = NULL;
static long long *survat = NULL; static int capsurv = 0;
static long maxstage = 0;

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static long v2fact(long n) { long v = 0; while (n) { n >>= 1; v += n; } return v; }

typedef struct {
    long M, Mp; int ns; long lo; int base; int Lf; int final;
    u64 *full;          // 2*ns entries, each Lf limbs: (M+k)! mod 2^K, limbs [base, LK)
    u64 *win;           // ns*4*WL : window values of the 4 options of pair step i
    int *tgt;           // ns : relative target bit count
    u64 *Xw;            // LK limbs
    unsigned char *inc, *chosen, *onext;
    u64 *ys;            // (ns+1)*WL
} Level;
static Level **lev = NULL; static int nlev = 0, caplev = 0;
static u64 *tmpfull;

static void mul1(u64 *x, int n0, u64 m) { // x[n0..LK) *= m mod 2^K (limbs below n0 assumed zero)
    u64 c = 0;
    for (int i = n0; i < LK; i++) { u128 s = (u128)x[i] * m + c; x[i] = (u64)s; c = (u64)(s >> 64); }
    x[LK - 1] &= topmask;
}
static void getwin(const u64 *x /*full LK*/, long lo, u64 *out) {
    int q = (int)(lo / 64), r = (int)(lo % 64);
    for (int k = 0; k < WL; k++) {
        u64 lo_ = (q + k < LK) ? x[q + k] : 0, hi_ = (q + k + 1 < LK) ? x[q + k + 1] : 0;
        out[k] = r ? ((lo_ >> r) | (hi_ << (64 - r))) : lo_;
    }
}
static inline void addW(u64 *c, const u64 *x, const u64 *y) {
    u64 cy = 0; for (int k = 0; k < WL; k++) { u128 s = (u128)x[k] + y[k] + cy; c[k] = (u64)s; cy = (u64)(s >> 64); }
}
static inline int lowzero(const u64 *c, int t) { // bits [0,t) zero, t <= 64*WL
    int k = 0;
    while (t >= 64) { if (c[k]) return 0; k++; t -= 64; }
    if (t == 0) return 1;
    return (c[k] & ((1ULL << t) - 1)) == 0;
}
static inline int ctzW(const u64 *c) { for (int k = 0; k < WL; k++) if (c[k]) return 64 * k + __builtin_ctzll(c[k]); return 64 * WL; }
static void addfull(u64 *X, const u64 *f, int base) { // X[base..LK) += f[0..LK-base)
    u64 c = 0; int L = LK - base; u64 *x = X + base;
    for (int i = 0; i < L; i++) { u128 s = (u128)x[i] + f[i] + c; x[i] = (u64)s; c = (u64)(s >> 64); }
    X[LK - 1] &= topmask; fulladds++;
}
static void subfull(u64 *X, const u64 *f, int base) {
    u64 br = 0; int L = LK - base; u64 *x = X + base;
    for (int i = 0; i < L; i++) { u128 s = (u128)x[i] - f[i] - br; x[i] = (u64)s; br = (u64)(s >> 64) & 1; }
    X[LK - 1] &= topmask; fulladds++;
}

static Level *make_level(int j) {
    Level *P = (j > 0) ? lev[j - 1] : NULL;
    Level *Lv = calloc(1, sizeof(Level));
    Lv->M = (j == 0) ? a + 2 : P->Mp;
    Lv->lo = v2fact(Lv->M);
    long lim = Lv->lo + 64 * WL;
    if (K <= lim) { Lv->Mp = Nfin; Lv->final = 1; }
    else { long M = Lv->M; while (v2fact(M + 2) <= lim) M += 2; Lv->Mp = M; Lv->final = 0; }
    if (Lv->Mp <= Lv->M) { fprintf(stderr, "window too small at M=%ld\n", Lv->M); exit(1); }
    Lv->ns = (int)((Lv->Mp - Lv->M) / 2);
    Lv->base = (int)(Lv->lo / 64); Lv->Lf = LK - Lv->base;
    Lv->full = malloc((size_t)2 * Lv->ns * Lv->Lf * 8);
    Lv->win = malloc((size_t)Lv->ns * 4 * WL * 8);
    Lv->tgt = malloc(sizeof(int) * Lv->ns);
    if (!Lv->full || !Lv->win) { fprintf(stderr, "out of memory making level %d\n", j); exit(3); }
    // tmpfull = M! mod 2^K (full LK array)
    if (j == 0) {
        memset(tmpfull, 0, (size_t)LK * 8); tmpfull[0] = 1;
        for (long n = 2; n <= Lv->M; n++) mul1(tmpfull, 0, (u64)n);
    } else {
        memset(tmpfull, 0, (size_t)LK * 8);
        memcpy(tmpfull + P->base, P->full + (size_t)(2 * P->ns - 1) * P->Lf, (size_t)P->Lf * 8);
        mul1(tmpfull, P->base, (u64)Lv->M);
    }
    for (int k = 0; k < 2 * Lv->ns; k++) {
        if (k > 0) mul1(tmpfull, Lv->base, (u64)(Lv->M + k));
        // sanity: limbs below base are zero
        for (int i = 0; i < Lv->base; i++) if (tmpfull[i]) { fprintf(stderr, "nonzero low limb\n"); exit(1); }
        memcpy(Lv->full + (size_t)k * Lv->Lf, tmpfull + Lv->base, (size_t)Lv->Lf * 8);
    }
    for (int i = 0; i < Lv->ns; i++) {
        long N = Lv->M + 2 * i;
        u64 *w = Lv->win + (size_t)i * 4 * WL;
        memset(w, 0, WL * 8);
        // option 1: N!, option 2: (N+1)!, option 3: sum
        memset(tmpfull, 0, (size_t)LK * 8); memcpy(tmpfull + Lv->base, Lv->full + (size_t)(2 * i) * Lv->Lf, (size_t)Lv->Lf * 8);
        getwin(tmpfull, Lv->lo, w + WL);
        memset(tmpfull, 0, (size_t)LK * 8); memcpy(tmpfull + Lv->base, Lv->full + (size_t)(2 * i + 1) * Lv->Lf, (size_t)Lv->Lf * 8);
        getwin(tmpfull, Lv->lo, w + 2 * WL);
        addW(w + 3 * WL, w + WL, w + 2 * WL);
        long vt = v2fact(N + 2);
        if (vt >= K) { if (i != Lv->ns - 1 || !Lv->final) { fprintf(stderr, "final gate misplaced\n"); exit(1); } vt = K; }
        Lv->tgt[i] = (int)(vt - Lv->lo);
        if (Lv->tgt[i] > 64 * WL || Lv->tgt[i] <= 0) { fprintf(stderr, "bad target\n"); exit(1); }
    }
    Lv->Xw = malloc((size_t)LK * 8);
    Lv->inc = calloc(Lv->ns + 1, 1); Lv->chosen = calloc(Lv->ns + 1, 1); Lv->onext = calloc(Lv->ns + 1, 1);
    Lv->ys = malloc((size_t)(Lv->ns + 1) * WL * 8);
    return Lv;
}
static Level *get_level(int j) {
    if (j < nlev) return lev[j];
    if (j != nlev) { fprintf(stderr, "level gap\n"); exit(1); }
    if (nlev >= caplev) { caplev = caplev ? 2 * caplev : 256; lev = realloc(lev, sizeof(Level *) * caplev); }
    lev[nlev] = make_level(j); nlev++;
    return lev[j];
}
static void add_option(u64 *X, Level *Lv, int i, int o, int sign) {
    if (o & 1) { const u64 *f = Lv->full + (size_t)(2 * i) * Lv->Lf; if (sign > 0) addfull(X, f, Lv->base); else subfull(X, f, Lv->base); }
    if (o & 2) { const u64 *f = Lv->full + (size_t)(2 * i + 1) * Lv->Lf; if (sign > 0) addfull(X, f, Lv->base); else subfull(X, f, Lv->base); }
}

static void write_witness(int jlast) {
    if (!wfile) return;
    FILE *wf = fopen(wfile, "w");
    long cnt = 1 + init_e1;
    for (int j = 0; j <= jlast; j++) for (int i = 0; i < lev[j]->ns; i++) cnt += __builtin_popcount(lev[j]->chosen[i]);
    fprintf(wf, "# witness for f(%ld,2) >= %d : the set A (one n per line), |A| = %ld\n", a, K, cnt);
    fprintf(wf, "%ld\n", a);
    if (init_e1) fprintf(wf, "%ld\n", a + 1);
    for (int j = 0; j <= jlast; j++) { Level *Lv = lev[j];
        for (int i = 0; i < Lv->ns; i++) { long N = Lv->M + 2 * i; int o = Lv->chosen[i];
            if (o & 1) fprintf(wf, "%ld\n", N);
            if (o & 2) fprintf(wf, "%ld\n", N + 1); } }
    fclose(wf);
    printf("witness written: %s (%ld terms)\n", wfile, cnt);
}


static void progress(int j) {
    double t = now();
    if (t - tlast > 60) {
        tlast = t;
        printf("[%.0fs] level=%d M=%ld nlev=%d maxlevel=%d nodes=%lld surv=%lld fulladds=%lld best=%ld\n", t - t0, j, lev[j]->M, nlev, maxlevel, nodes, survivors, fulladds, best);
        fflush(stdout);
    }
}

// returns 1 on success (2^K reachable)
static int dfs_level(int j, const u64 *Xin) {
    Level *Lv = get_level(j);
    if (j > maxlevel) maxlevel = j;
    int ns = Lv->ns;
    memcpy(Lv->Xw + Lv->base, Xin + Lv->base, (size_t)Lv->Lf * 8);
    for (int i = 0; i < Lv->base; i++) { if (Xin[i]) { fprintf(stderr, "state not alive at level %d\n", j); exit(1); } Lv->Xw[i] = 0; }
    memset(Lv->inc, 0, ns);
    getwin(Xin, Lv->lo, Lv->ys);
    int d = 0; Lv->onext[0] = 0;
    while (d >= 0) {
        if (d == ns) {
            // survivor at Mp: materialise
            survivors++;
            if (j + 1 >= capsurv) { int nc = capsurv ? 2 * capsurv : 1024; while (nc <= j + 1) nc *= 2; survat = realloc(survat, nc * sizeof(long long)); memset(survat + capsurv, 0, (nc - capsurv) * sizeof(long long)); capsurv = nc; }
            survat[j + 1]++;
            int i0 = 0; while (i0 < ns && Lv->inc[i0] == Lv->chosen[i0]) i0++;
            for (int i = i0; i < ns; i++) {
                if (Lv->inc[i]) add_option(Lv->Xw, Lv, i, Lv->inc[i], -1);
                if (Lv->chosen[i]) add_option(Lv->Xw, Lv, i, Lv->chosen[i], +1);
                Lv->inc[i] = Lv->chosen[i];
            }
            // sanity: window of Xw at lo equals ys[ns]
            u64 chk[WL]; getwin(Lv->Xw, Lv->lo, chk);
            if (memcmp(chk, Lv->ys + (size_t)ns * WL, WL * 8)) { fprintf(stderr, "materialisation mismatch at level %d\n", j); exit(1); }
            if ((survivors & 0xfff) == 0) progress(j);
            if (dfs_level(j + 1, Lv->Xw)) return 1;
            d--; continue;
        }
        int o = Lv->onext[d];
        if (o == 4) { d--; continue; }
        Lv->onext[d] = (unsigned char)(o + 1);
        nodes++;
        u64 c[WL];
        addW(c, Lv->ys + (size_t)d * WL, Lv->win + ((size_t)d * 4 + o) * WL);
        int t = Lv->tgt[d];
        if (lowzero(c, t)) {
            if (Lv->final && d == ns - 1) {
                Lv->chosen[d] = (unsigned char)o;
                printf("SUCCESS: 2^%d divides a witness sum (final gate at N=%ld)\n", K, Lv->M + 2 * d);
                write_witness(j);
                return 1;
            }
            Lv->chosen[d] = (unsigned char)o;
            if (Lv->M + 2 * d + 2 > maxstage) maxstage = Lv->M + 2 * d + 2;
            memcpy(Lv->ys + (size_t)(d + 1) * WL, c, WL * 8);
            d++; Lv->onext[d] = 0;
        } else {
            deaths++;
            long v = Lv->lo + ctzW(c);
            if (v > best) best = v;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: dfsW a K [witnessfile]\n"); return 1; }
    a = atol(argv[1]); K = atoi(argv[2]); if (argc > 3 && strcmp(argv[3], "-")) wfile = argv[3]; if (argc > 4) pfile = argv[4];
    printf("dfsW (WL=%d) a=%ld K=%d witness=%s\n", WL, a, K, wfile ? wfile : "(none)"); fflush(stdout);
    if (a < 2 || (a & 1)) { printf("only even a >= 2\n"); return 1; }
    t0 = tlast = now();
    long va = v2fact(a);
    if (va >= K) { printf("RESULT a=%ld K=%d reachable=1 (trivial)\n", a, K); return 0; }
    LK = (K + 63) / 64; topmask = (K % 64) ? ((1ULL << (K % 64)) - 1) : ~0ULL;
    Nfin = a + 2; while (v2fact(Nfin) < K) Nfin += 2;
    tmpfull = malloc((size_t)LK * 8);
    // initial: X = a! + e*(a+1)!, alive iff v(X) >= v((a+2)!)
    u64 *fa = calloc(LK, 8), *fa1 = calloc(LK, 8), *X = calloc(LK, 8);
    fa[0] = 1; for (long n = 2; n <= a; n++) mul1(fa, 0, (u64)n);
    memcpy(fa1, fa, (size_t)LK * 8); mul1(fa1, 0, (u64)(a + 1));
    long v0 = v2fact(a + 2);
    int found = 0;
    for (int e1 = 0; e1 <= 1 && !found; e1++) {
        memcpy(X, fa, (size_t)LK * 8); if (e1) addfull(X, fa1, 0);
        // valuation of X
        long vx = K; for (int i = 0; i < LK; i++) if (X[i]) { vx = 64L * i + __builtin_ctzll(X[i]); break; }
        if (vx > K) vx = K;
        if (v0 >= K) { // final gate immediately
            if (vx >= K) { init_e1 = e1; found = 1; if (wfile) { FILE *wf = fopen(wfile, "w"); fprintf(wf, "# witness for f(%ld,2) >= %d\n%ld\n", a, K, a); if (e1) fprintf(wf, "%ld\n", a + 1); fclose(wf); } }
            else if (vx > best) best = vx;
            continue;
        }
        if (vx < v0) { deaths++; if (vx > best) best = vx; continue; }
        init_e1 = e1;
        if (dfs_level(0, X)) found = 1;
    }
    double t = now() - t0;
    printf("deepest alive stage N = %ld (v2(N!) = %ld)\n", maxstage, v2fact(maxstage));
    if (pfile) {
        FILE *pf = fopen(pfile, "w");
        fprintf(pf, "# a=%ld K=%d : level j, boundary M_j, v2(M_j!), number of alive paths at M_j (j>=1)\n", a, K);
        for (int j = 1; j < nlev && j < capsurv; j++) fprintf(pf, "%d %ld %ld %lld\n", j, lev[j]->M, lev[j]->lo, survat[j]);
        fclose(pf);
    }
    if (found) printf("RESULT a=%ld K=%d reachable=1 nodes=%lld surv=%lld fulladds=%lld levels=%d time=%.1fs\n", a, K, nodes, survivors, fulladds, nlev, t);
    else {
        printf("RESULT a=%ld K=%d reachable=0 nodes=%lld surv=%lld fulladds=%lld levels=%d time=%.1fs\n", a, K, nodes, survivors, fulladds, nlev, t);
        printf("EXACT a=%ld f=%ld g=%ld (max valuation over all paths; valid since K > f)\n", a, best, best - va);
    }
    return 0;
}
