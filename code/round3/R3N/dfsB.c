// dfsB.c -- program B of track R3N (round 3).  Written independently of bfsA.c / dfsW.c
// (no shared code; GMP for all full-precision arithmetic).
// Decides "f(a,2) >= K ?" for even a; on failure prints the exact value f(a,2).
//
// Shifted normal form (single steps).  For a path A (min A = a) put S_n = sum_{m in A, m<n} m!.
// The path is alive at n iff 2^{v(n!)} | S_n; then T_n := S_n / 2^{v(n!)} mod 2^{K - v(n!)}.
// Step n -> n+1 with e = [n in A] (e = 1 forced at n = a):
//     x = T_n + e * U_n,  U_n = odd part of n!  (mod 2^K);  alive at n+1 iff 2^{v(n+1)} | x;
//     T_{n+1} = x / 2^{v(n+1)}.
// If the path dies at n+1, every extension has v(sum) = v(n!) + v(x) (later terms are
// multiples of (n+1)!); at the final step (v((n+1)!) >= K) success iff x == 0 mod 2^{K-v(n!)}.
//
// Windows: a full state T (mpz) is held at the window start nw; inside the window only the
// low 128 bits of T_n are tracked (unsigned __int128).  After the window consumed c bits, the
// low 128-c bits are exact.  A window ends at the first n with v(n!) - v(nw!) >= 64 (each test
// needs at most v(n+1) <= 18 valid bits), or runs to the final gate if K - v(nw!) <= 128.
// A survivor at the window end is rebuilt from scratch at full precision:
//     T_end = ((T_nw + sum_{n in window, e_n = 1} n!/2^{v(nw!)}) mod 2^{K-v(nw!)}) >> (v(end!)-v(nw!)),
// with a consistency check against the 128-bit window value.
// No deduplication: every alive path is enumerated.
//
// Usage: dfsB a K [witnessfile]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <gmp.h>

typedef unsigned __int128 u128;
static long a_, K_, nfin;               // nfin: the final step n (least n with v((n+1)!) >= K)
static long *vf;                        // vf[n] = v_2(n!) for n <= nfin+1
static u128 *Ulo;                       // Ulo[n] = odd part of n! mod 2^128
static long bestv = -1;
static unsigned long long cnt_steps = 0, cnt_surv = 0;
static char *path;                      // path[n] = e_n on the current DFS branch
static const char *wout = NULL;
static double tstart;

static double clk(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }

typedef struct {
    long nw, nend;      // window start; steps n = nw .. nend-1 (for the final window nend = nfin+1)
    long Rw;            // K - v(nw!)
    int fin;
    mpz_t *G;           // G[n - nw] = n!/2^{v(nw!)} mod 2^{Rw}
    mpz_t Tn;           // scratch for the rebuilt state
    char *ech;          // e choices inside the window (current branch)
    u128 *lowst;        // low-128 stack
    unsigned char *nexte;
} Win;
static Win **wins = NULL; static int nwins = 0, capw = 0;
static mpz_t Urun; static long Urun_n;   // running odd part of n! mod 2^K, at n = Urun_n

static Win *window_at(int j, long nw) {
    if (j < nwins) return wins[j];
    if (nwins == capw) { capw = capw ? 2 * capw : 512; wins = realloc(wins, capw * sizeof(Win *)); }
    Win *w = calloc(1, sizeof(Win));
    w->nw = nw; w->Rw = K_ - vf[nw];
    if (w->Rw <= 128) { w->fin = 1; w->nend = nfin + 1; }
    else { long n = nw; while (vf[n] - vf[nw] < 64) n++; w->nend = n; w->fin = 0; }
    long len = w->nend - nw;
    w->G = malloc(len * sizeof(mpz_t));
    // advance Urun to nw
    if (Urun_n > nw) { fprintf(stderr, "window order violated\n"); exit(1); }
    while (Urun_n < nw) { Urun_n++; long m = Urun_n; while (!(m & 1)) m >>= 1; mpz_mul_ui(Urun, Urun, (unsigned long)m); mpz_fdiv_r_2exp(Urun, Urun, K_); }
    mpz_t U; mpz_init_set(U, Urun);
    for (long i = 0; i < len; i++) {
        long n = nw + i;
        if (i > 0) { long m = n; while (!(m & 1)) m >>= 1; mpz_mul_ui(U, U, (unsigned long)m); mpz_fdiv_r_2exp(U, U, K_); }
        mpz_init(w->G[i]);
        mpz_mul_2exp(w->G[i], U, vf[n] - vf[nw]);
        mpz_fdiv_r_2exp(w->G[i], w->G[i], w->Rw);
        // check the 128-bit table against U
        u128 lo = (u128)mpz_getlimbn(U, 0) | ((u128)mpz_getlimbn(U, 1) << 64);
        if (mpz_size(U) < 2) lo = (u128)mpz_getlimbn(U, 0);
        if (K_ >= 128 && lo != Ulo[n]) { fprintf(stderr, "Ulo mismatch at n=%ld\n", n); exit(1); }
    }
    mpz_clear(U);
    mpz_init(w->Tn);
    w->ech = calloc(len + 1, 1); w->lowst = malloc((len + 1) * sizeof(u128)); w->nexte = calloc(len + 1, 1);
    wins[nwins++] = w;
    return w;
}

static u128 low128(const mpz_t x) {
    size_t s = mpz_size(x);
    u128 r = 0;
    if (s >= 1) r = mpz_getlimbn(x, 0);
    if (s >= 2) r |= (u128)mpz_getlimbn(x, 1) << 64;
    return r;
}
static int ctz128(u128 x) { uint64_t l = (uint64_t)x; if (l) return __builtin_ctzll(l); return 64 + __builtin_ctzll((uint64_t)(x >> 64)); }

static void dump_witness(void) {
    if (!wout) return;
    FILE *f = fopen(wout, "w"); long c = 0;
    for (long n = a_; n <= nfin; n++) c += path[n];
    fprintf(f, "# witness (program B) for f(%ld,2) >= %ld; %ld terms\n", a_, K_, c);
    for (long n = a_; n <= nfin; n++) if (path[n]) fprintf(f, "%ld\n", n);
    fclose(f);
}

// T: full state at w->nw (mod 2^{Rw}); returns 1 on success
static int search(int j, const mpz_t T) {
    Win *w = window_at(j, j == 0 ? a_ : wins[j - 1]->nend);
    long nw = w->nw, len = w->nend - nw;
    int k = 0; w->lowst[0] = low128(T); w->nexte[0] = 0;
    while (k >= 0) {
        long n = nw + k;
        if (k == len) {
            // survivor at the window end: rebuild at full precision
            cnt_surv++;
            mpz_set(w->Tn, T);
            for (long i = 0; i < len; i++) if (w->ech[i]) mpz_add(w->Tn, w->Tn, w->G[i]);
            mpz_fdiv_r_2exp(w->Tn, w->Tn, w->Rw);
            long D = vf[w->nend] - vf[nw];
            if (mpz_sgn(w->Tn) != 0 && (long)mpz_scan1(w->Tn, 0) < D) { fprintf(stderr, "rebuild: low bits not zero\n"); exit(1); }
            mpz_fdiv_q_2exp(w->Tn, w->Tn, D);
            u128 chk = low128(w->Tn), wv = w->lowst[len];
            int valid = 128 - (int)D;
            u128 m = (valid >= 128) ? ~(u128)0 : (((u128)1 << valid) - 1);
            if ((chk & m) != (wv & m)) { fprintf(stderr, "rebuild mismatch at n=%ld\n", n); exit(1); }
            if ((cnt_surv & 0xffff) == 0) { fprintf(stdout, "[%.0fs] window %d n=%ld steps=%llu surv=%llu best=%ld\n", clk() - tstart, j, n, cnt_steps, cnt_surv, bestv); fflush(stdout); }
            // the next window works on its own copy
            mpz_t Tc; mpz_init_set(Tc, w->Tn);
            int r = search(j + 1, Tc);
            mpz_clear(Tc);
            if (r) return 1;
            k--; continue;
        }
        int e = w->nexte[k];
        int emin = (n == a_) ? 1 : 0;
        if (e < emin) e = emin;
        if (e > 1) { path[n] = 0; k--; continue; }
        w->nexte[k] = (unsigned char)(e + 1);
        cnt_steps++;
        u128 x = w->lowst[k] + (e ? Ulo[n] : 0);
        long t = vf[n + 1] - vf[n];
        if (n == nfin) {
            long need = K_ - vf[n];
            u128 mk = (need >= 128) ? ~(u128)0 : (((u128)1 << need) - 1);
            if ((x & mk) == 0) { path[n] = (char)e; w->ech[k] = (char)e; printf("SUCCESS at final step n=%ld\n", n); dump_witness(); return 1; }
            long v = vf[n] + ctz128(x); if (v > bestv) bestv = v;
            continue;
        }
        u128 mt = ((u128)1 << t) - 1;
        if ((x & mt) == 0) {
            path[n] = (char)e; w->ech[k] = (char)e;
            w->lowst[k + 1] = x >> t; w->nexte[k + 1] = 0; k++;
        } else {
            long v = vf[n] + ctz128(x); if (v > bestv) bestv = v;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: dfsB a K [witnessfile]\n"); return 2; }
    a_ = atol(argv[1]); K_ = atol(argv[2]); if (argc > 3) wout = argv[3];
    printf("dfsB a=%ld K=%ld\n", a_, K_); fflush(stdout);
    if (a_ % 2) { printf("odd a: f = v2(a!)\n"); return 0; }
    tstart = clk();
    // v2 table
    long cap = a_ + 4; vf = malloc(cap * sizeof(long)); vf[0] = 0;
    long n = 0;
    while (1) {
        if (n + 2 >= cap) { cap *= 2; vf = realloc(vf, cap * sizeof(long)); }
        long m = n + 1, t = 0; while (!(m & 1)) { m >>= 1; t++; }
        vf[n + 1] = vf[n] + t; n++;
        if (n > a_ && vf[n] >= K_) break;
    }
    if (vf[a_] >= K_) { printf("RESULT reachable=1 (trivial)\n"); return 0; }
    nfin = n - 1;                        // v((nfin+1)!) >= K, v(nfin!) < K
    Ulo = malloc((nfin + 2) * sizeof(u128)); Ulo[0] = 1;
    for (long i = 1; i <= nfin + 1; i++) { long m = i; while (!(m & 1)) m >>= 1; Ulo[i] = Ulo[i - 1] * (u128)m; }
    path = calloc(nfin + 2, 1);
    mpz_init_set_ui(Urun, 1); Urun_n = 0;
    mpz_t T0; mpz_init_set_ui(T0, 0);
    int r = search(0, T0);
    printf("RESULT a=%ld K=%ld reachable=%d steps=%llu surv=%llu windows=%d time=%.1fs\n", a_, K_, r, cnt_steps, cnt_surv, nwins, clk() - tstart);
    if (!r) { long va = vf[a_]; printf("EXACT a=%ld f=%ld g=%ld\n", a_, bestv, bestv - va); }
    return 0;
}
