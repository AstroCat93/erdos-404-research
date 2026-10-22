// dfsD.c -- check_R3N (round 3): own exhaustive solver for "is f(a,2) >= K ?" (even a),
// printing the exact f(a,2) when the answer is no.  Written from scratch for the adversarial
// check of track R3N; it shares no code with that track's programs B (dfsB.c) or C (dfsW.c).
//
// Mathematics (re-derived here).  For A finite with min A = a, let S_n = sum_{m in A, m < n} m!
// (stage n > a).  S_{a+1} = a! (a is forced into A).  Step n -> n+1 adds e_n * n!, e_n in {0,1}.
// Write vf(n) = v_2(n!) = n - s_2(n) (Legendre).  Let N_K = min{n : vf(n) >= K}.
//   * If v_2(S) >= K for some A, then deleting the terms >= N_K keeps v_2 >= K, and the truncated
//     set has v_2(S_n) >= vf(n) for every a < n < N_K (S_{N_K} - S_n is a multiple of n! and
//     vf(n) < K).  So it suffices to enumerate the prefixes that are "alive", v_2(S_n) >= vf(n),
//     at every stage n < N_K, and to test S_{N_K} == 0 mod 2^K at the last step.
//   * A set whose first non-alive stage is d < N_K has v_2(sum) = v_2(S_d) < vf(d) (later terms
//     are multiples of d!).  Hence, if no prefix reaches S_{N_K} == 0 mod 2^K, then
//     f(a,2) = max of v_2 over all first-death values S_d (d <= N_K), all of which are < K.
//
// Implementation.  The state is S_n mod 2^K (unshifted).  Stages are cut into windows
// [s, t]: lo = vf(s), and t is the largest stage with vf(t) - lo <= 128 (or t = N_K when
// K - lo <= 128).  In a window, every term m! (m >= s) and the alive state S_s are multiples of
// 2^lo, so bits [lo, lo+128) of S_n are exactly the 128-bit sum of the corresponding bits of
// S_s and of the chosen m!; every test needs only bits below vf(n) <= lo+128 (or K at N_K).
// A prefix alive at the window end t is materialised mod 2^K (GMP mpn limbs) by adding or
// subtracting m! only at the positions where its choice vector differs from the previously
// materialised one, then checked against the 128-bit window value, and the search recurses.
// No deduplication, no pruning other than aliveness.  Counters: steps (candidate evaluations),
// alive_even = number of (alive prefix, even stage N) with a+2 <= N <= N_K-2.
//
// Usage: dfsD a K [witnessfile]
//        dfsD a K -p L START END TLIMIT
//            partitioned run: the subtrees rooted at the survivors that reach window L are numbered
//            in DFS order 0,1,2,...; this job expands those with START <= number < END, and stops
//            (before opening a new subtree) once TLIMIT seconds have passed (TLIMIT <= 0: no limit),
//            printing the first unprocessed number NEXT.  Windows < L are always expanded.  A chain
//            of jobs [0,N1), [N1,N2), ..., [Nm, inf) covers the full search; the deep counters add up,
//            and the job that runs to the end also has the complete shallow counters.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <gmp.h>

typedef unsigned __int128 u128;
typedef mp_limb_t limb;

static long Aa, KK, NK;          // a, K, N_K
static long LK;                  // limbs for mod 2^K
static limb TOPM;                // mask of the top limb
static long best = -1;           // max first-death valuation
static unsigned long long steps = 0, surv = 0, alive_even = 0, upd = 0;
static const char *wpath = NULL;
static double T0;
static long nfaccheck = 0;
static long PL = -1; static double PT = 0;                // partition (-p L START END TLIMIT)
static unsigned long long PS = 0, PE = ~0ULL, pnext = 0;
static unsigned long long pcount = 0, deep_steps = 0, deep_alive = 0, deep_surv = 0, deep_trees = 0;

static double wall(void) { struct timespec q; clock_gettime(CLOCK_MONOTONIC, &q); return q.tv_sec + 1e-9 * q.tv_nsec; }
static long vf(long n) { return n - __builtin_popcountl((unsigned long)n); }
static int ctz128(u128 y) { uint64_t l = (uint64_t)y; return l ? __builtin_ctzll(l) : 64 + __builtin_ctzll((uint64_t)(y >> 64)); }
static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); fflush(stdout); exit(9); }

// bits [off, off+128) of the little-endian limb array x[0..n), zero-extended
static u128 bits128(const limb *x, long n, long off) {
    long q = off / 64; int r = (int)(off % 64);
    limb l0 = q < n ? x[q] : 0, l1 = q + 1 < n ? x[q + 1] : 0, l2 = q + 2 < n ? x[q + 2] : 0;
    u128 lo = ((u128)l1 << 64) | l0;
    if (r == 0) return lo;
    return (lo >> r) | ((u128)l2 << (128 - r));
}

typedef struct {
    long s, t, lo; int fin;
    long base, len;              // limbs [base, LK) are stored, len = LK - base
    long n;                      // number of steps = t - s
    limb *F;                     // F[i*len ..] = (s+i)! mod 2^K, limbs [base, LK)
    u128 *w, *mask;              // window bits of (s+i)!, test mask for stage s+i+1
    u128 *x;                     // x[d] = window bits of S_{s+d} on the current branch
    unsigned char *e, *inc, *nx; // current choices, choices in W, next choice to try
    limb *W;                     // full LK limbs: S_s + sum_{i: inc[i]} (s+i)!  mod 2^K
} Win;

static Win **wins = NULL; static long nw = 0, capw = 0;
static limb *RF;                 // running factorial (LK limbs), = s! of the next window to build
static long RFn;

static void check_fac(long n) {  // RF == n! mod 2^K, recomputed by mpz_fac_ui
    mpz_t f; mpz_init(f); mpz_fac_ui(f, (unsigned long)n); mpz_fdiv_r_2exp(f, f, (mp_bitcnt_t)KK);
    long sz = (long)mpz_size(f);
    for (long i = 0; i < LK; i++) { limb g = i < sz ? mpz_getlimbn(f, i) : 0; if (g != RF[i]) die("running factorial != mpz_fac_ui"); }
    mpz_clear(f); nfaccheck++;
}

static Win *get_win(long j) {
    if (j < nw) return wins[j];
    if (j != nw) die("window order");
    Win *P = j ? wins[j - 1] : NULL;
    Win *w = calloc(1, sizeof(Win));
    w->s = P ? P->t : Aa + 1;
    w->lo = vf(w->s);
    if (KK - w->lo <= 128) { w->fin = 1; w->t = NK; }
    else { long t = w->s + 1; while (vf(t + 1) - w->lo <= 128) t++; w->t = t; if (vf(t) >= KK) die("window end"); }
    w->n = w->t - w->s;
    if (w->n < 1) die("empty window");
    w->base = w->lo / 64; w->len = LK - w->base;
    w->F = malloc(sizeof(limb) * (size_t)w->n * (size_t)w->len);
    w->w = malloc(sizeof(u128) * w->n); w->mask = malloc(sizeof(u128) * w->n);
    w->x = malloc(sizeof(u128) * (w->n + 1));
    w->e = calloc(w->n + 1, 1); w->inc = calloc(w->n + 1, 1); w->nx = calloc(w->n + 1, 1);
    w->W = calloc(LK, sizeof(limb));
    if (!w->F || !w->W) die("out of memory");
    if (RFn != w->s) die("running factorial position");
    if (j % 8 == 0) check_fac(w->s);
    for (long i = 0; i < w->n; i++) {
        long m = w->s + i;
        for (long k = 0; k < w->base; k++) if (RF[k]) die("factorial: low limb not zero");
        memcpy(w->F + (size_t)i * w->len, RF + w->base, sizeof(limb) * w->len);
        w->w[i] = bits128(RF + w->base, w->len, w->lo - 64 * w->base);
        long need = (m + 1 == NK) ? KK - w->lo : vf(m + 1) - w->lo;
        if (m + 1 == NK && !(w->fin && i == w->n - 1)) die("final gate misplaced");
        if (m + 1 < NK && vf(m + 1) >= KK) die("N_K wrong");
        if (need < 1 || need > 128) die("test width");
        w->mask[i] = need == 128 ? ~(u128)0 : (((u128)1 << need) - 1);
        // RF <- (m+1)!  (mod 2^K); limbs below base stay zero
        mpn_mul_1(RF + w->base, RF + w->base, w->len, (limb)(m + 1));
        RF[LK - 1] &= TOPM;
    }
    RFn = w->t;
    if (nw == capw) { capw = capw ? 2 * capw : 1024; wins = realloc(wins, sizeof(Win *) * capw); }
    wins[nw++] = w;
    return w;
}

static void write_witness(long jlast) {
    if (!wpath) return;
    FILE *f = fopen(wpath, "w"); if (!f) die("witness file");
    long cnt = 1;
    for (long j = 0; j <= jlast; j++) for (long i = 0; i < wins[j]->n; i++) cnt += wins[j]->e[i];
    fprintf(f, "# dfsD witness: min A = %ld, 2^%ld | sum, %ld terms\n%ld\n", Aa, KK, cnt, Aa);
    for (long j = 0; j <= jlast; j++) for (long i = 0; i < wins[j]->n; i++) if (wins[j]->e[i]) fprintf(f, "%ld\n", wins[j]->s + i);
    fclose(f);
    printf("witness: %s (%ld terms)\n", wpath, cnt);
}

static int search(long j, const limb *S) {
    Win *w = get_win(j);
    long n = w->n;
    memcpy(w->W, S, sizeof(limb) * LK);
    for (long k = 0; k < w->base; k++) if (S[k]) die("start state has nonzero low limb");
    memset(w->inc, 0, n);
    w->x[0] = bits128(S + w->base, w->len, w->lo - 64 * w->base);
    long d = 0; w->nx[0] = 0;
    while (d >= 0) {
        if (d == n) {            // alive at the (non-final) window end t
            surv++;
            long i = 0; while (i < n && w->inc[i] == w->e[i]) i++;
            for (; i < n; i++) {
                if (w->inc[i] != w->e[i]) {
                    limb *p = w->W + w->base, *q = w->F + (size_t)i * w->len;
                    if (w->e[i]) mpn_add_n(p, p, q, w->len); else mpn_sub_n(p, p, q, w->len);
                    w->W[LK - 1] &= TOPM; upd++;
                    w->inc[i] = w->e[i];
                }
            }
            if (bits128(w->W + w->base, w->len, w->lo - 64 * w->base) != w->x[n]) die("materialised state != window value");
            long vt = vf(w->t);  // full-precision aliveness: low vt bits of W vanish
            for (long k = 0; k < vt / 64; k++) if (w->W[k]) die("materialised state not alive");
            if (vt % 64 && (w->W[vt / 64] & (((limb)1 << (vt % 64)) - 1))) die("materialised state not alive");
            if ((surv & 0xfffff) == 0) { printf("[%.0fs] win=%ld s=%ld steps=%llu surv=%llu best=%ld\n", wall() - T0, j, w->s, steps, surv, best); fflush(stdout); }
            if (PL >= 0 && j + 1 == PL) {
                unsigned long long idx = pcount++;
                if (idx < PS || idx >= PE) { d--; continue; }
                if (PT > 0 && wall() - T0 > PT) { pnext = idx; return 2; }
                unsigned long long s0 = steps, a0 = alive_even, v0 = surv;
                int rr = search(j + 1, w->W);
                deep_steps += steps - s0; deep_alive += alive_even - a0; deep_surv += surv - v0; deep_trees++;
                if (rr) return rr;
                d--; continue;
            }
            { int rr = search(j + 1, w->W); if (rr) return rr; }
            d--; continue;
        }
        int e = w->nx[d];
        if (e == 2) { d--; continue; }
        w->nx[d] = (unsigned char)(e + 1);
        steps++;
        u128 y = w->x[d] + (e ? w->w[d] : 0);
        if ((y & w->mask[d]) == 0) {
            w->e[d] = (unsigned char)e;
            if (w->fin && d == n - 1) { printf("SUCCESS: S_{N_K} == 0 mod 2^%ld at N_K=%ld\n", KK, NK); write_witness(j); return 1; }
            w->x[d + 1] = y; d++; w->nx[d] = 0;
            long st = w->s + d;
            if (!(st & 1) && st <= NK - 2) alive_even++;
        } else {
            long v = w->lo + ctz128(y);
            if (v > best) best = v;
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: dfsD a K [witnessfile]\n"); return 2; }
    Aa = atol(argv[1]); KK = atol(argv[2]);
    if (argc > 3 && !strcmp(argv[3], "-p")) {
        if (argc < 8) { fprintf(stderr, "usage: dfsD a K -p L START END TLIMIT\n"); return 2; }
        PL = atol(argv[4]); PS = strtoull(argv[5], NULL, 10);
        PE = strcmp(argv[6], "inf") ? strtoull(argv[6], NULL, 10) : ~0ULL; PT = atof(argv[7]);
        if (PL < 1 || PE < PS) { fprintf(stderr, "bad partition\n"); return 2; }
    } else if (argc > 3) wpath = argv[3];
    printf("dfsD a=%ld K=%ld\n", Aa, KK); fflush(stdout);
    if (Aa < 2 || (Aa & 1)) { printf("even a >= 2 only\n"); return 2; }
    T0 = wall();
    if (vf(Aa) >= KK) { printf("RESULT a=%ld K=%ld reachable=1 trivial ({a} alone)\n", Aa, KK); return 0; }
    NK = Aa + 1; while (vf(NK) < KK) NK++;
    if (NK & 1) die("N_K odd");
    LK = (KK + 63) / 64; TOPM = (KK % 64) ? (((limb)1 << (KK % 64)) - 1) : ~(limb)0;
    // memory estimate of the factorial tables: sum_{m=a+1}^{N_K-1} (LK - vf(m)/64) limbs
    double mem = 0; for (long m = Aa + 1; m < NK; m++) mem += 8.0 * (LK - vf(m) / 64);
    printf("N_K=%ld tables~%.2f GB\n", NK, mem / 1e9); fflush(stdout);
    if (mem > 6e9) die("tables too large for this check");
    RF = calloc(LK, sizeof(limb));
    { mpz_t f; mpz_init(f); mpz_fac_ui(f, (unsigned long)Aa); mpz_fdiv_r_2exp(f, f, (mp_bitcnt_t)KK);
      for (long i = 0; i < (long)mpz_size(f); i++) RF[i] = mpz_getlimbn(f, i);
      mpz_clear(f); }
    limb *S0 = calloc(LK, sizeof(limb)); memcpy(S0, RF, sizeof(limb) * LK);   // S_{a+1} = a!
    mpn_mul_1(RF, RF, LK, (limb)(Aa + 1)); RF[LK - 1] &= TOPM; RFn = Aa + 1;   // RF = (a+1)!
    int r = search(0, S0);
    if (PL < 0 && r == 2) die("unexpected stop");
    double tt = wall() - T0;
    printf("RESULT a=%ld K=%ld reachable=%d steps=%llu alive_even=%llu surv=%llu updates=%llu windows=%ld faccheck=%ld time=%.1fs\n",
           Aa, KK, r, steps, alive_even, surv, upd, nw, nfaccheck, tt);
    if (PL >= 0) {
        printf("PARTITION L=%ld range=[%llu,%s) processed=[%llu,%llu) stopped=%d complete_shallow=%d subtrees_seen=%llu deep_trees=%llu "
               "shallow_steps=%llu shallow_alive_even=%llu deep_steps=%llu deep_alive_even=%llu deep_surv=%llu best=%ld\n",
               PL, PS, PE == ~0ULL ? "inf" : argv[6], PS, r == 2 ? pnext : (pcount < PE ? pcount : PE), r == 2, r == 0,
               pcount, deep_trees, steps - deep_steps, alive_even - deep_alive, deep_steps, deep_alive, deep_surv, best);
        if (r == 2) printf("STOPPED by time limit: NEXT=%llu (start the next job there)\n", pnext);
        if (r == 0) printf("PART DONE: no success in subtrees [%llu,%llu); max death valuation seen = %ld\n", PS, pcount < PE ? pcount : PE, best);
    } else if (!r) printf("EXACT a=%ld f=%ld g=%ld\n", Aa, best, best - vf(Aa));
    return 0;
}
