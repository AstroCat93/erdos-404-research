// bfsA.c -- program A of track R3N (round 3).
// Exact decision of "f(a,2) >= K ?" for even a, with exact value on death, and optional witness.
//
// Representation (unshifted sum form): state X = S_N mod 2^K, where S_N = sum_{n in A, n<N} n!,
// A = a witness set with min A = a.  A path is alive at N iff v_2(S_N) >= v_2(N!).  Two alive
// paths with equal X at the same N have identical futures, so the population is the SET of
// distinct X (deduplicated by hashing).  Only limbs [floor(v(N!)/64), ceil(K/64)) are stored:
// the limbs below are zero for every alive state.
//
// Steps: from N=a+1 (S=a!) one single step to N=a+2, then "pair steps" N -> N+2 for even N:
// candidates X + d, d in {0, N!, (N+1)!, N!+(N+1)!}, survivor iff v(X+d) >= v((N+2)!).
// The survivor test reads only the two limbs around bit v(N!) (no carry enters from below
// because every operand vanishes below bit v(N!)).
//
// Final gate: at the first step whose end N' has v(N'!) >= K, success iff some candidate is
// 0 mod 2^K.  If the population dies at a step N -> N', the exact value is
//   f(a,2) = max over states X and options d of v(X+d)        (all < v(N'!) <= K-1 or so)
// since paths that died earlier have smaller valuation (see report).
//
// Witness: with -w FILE, every child records (parent index, option) in a binary log;
// on success the path is reconstructed and written as the list of n with e_n = 1.
//
// Usage: bfsA a K [-w witnessfile] [-l logdir] [-p printevery] [-t threads(ignored)]
// Plain C, no GMP; 64-bit limbs; unsigned __int128 for carries.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

static int K, LK;                 // modulus 2^K, LK limbs
static u64 topmask;               // mask of the top limb

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static long v2fact(long n) { long v = 0; while (n) { n >>= 1; v += n; } return v; }
static int ctzl_(long n) { return __builtin_ctzl((unsigned long)n); }

// x (full LK limbs) *= m mod 2^K
static void mul1(u64 *x, u64 m) {
    u64 c = 0;
    for (int i = 0; i < LK; i++) { u128 s = (u128)x[i] * m + c; x[i] = (u64)s; c = (u64)(s >> 64); }
    x[LK - 1] &= topmask;
}
// dst[b..LK) = x[b..LK) + y[b..LK) mod 2^K ; arrays indexed from b (dst,x relative), y absolute
static inline void addrange(u64 *dst, const u64 *x, const u64 *yabs, int b) {
    u64 c = 0; int L = LK - b; const u64 *y = yabs + b;
    for (int i = 0; i < L; i++) {
        u128 s = (u128)x[i] + y[i] + c; dst[i] = (u64)s; c = (u64)(s >> 64);
    }
    dst[L - 1] &= topmask;
}
// valuation of (x + y) restricted to [b..LK) limbs (x relative, y absolute); returns K if zero mod 2^K
static int val_sum(const u64 *x, const u64 *yabs, int b) {
    u64 c = 0; int L = LK - b; const u64 *y = yabs + b;
    for (int i = 0; i < L; i++) {
        u128 s = (u128)x[i] + y[i] + c; u64 w = (u64)s; c = (u64)(s >> 64);
        if (i == L - 1) w &= topmask;
        if (w) { int v = 64 * (b + i) + __builtin_ctzll(w); return v < K ? v : K; }
    }
    return K;
}
// quick test: is v(x + y) >= vt, given both vanish below bit vlo (vlo <= vt < vlo + 64 guaranteed small gap)?
// x relative to limb b = vlo/64.  Reads limbs b, b+1 (if present).
static inline int quick_ok(const u64 *x, const u64 *yabs, int b, int vt) {
    // bits [64b, vt) of the sum must be zero
    int need = vt - 64 * b;          // number of low bits (relative to limb b) that must vanish
    const u64 *y = yabs + b;
    u128 s0 = (u128)x[0] + y[0];
    u64 w0 = (u64)s0;
    if (b == LK - 1) w0 &= topmask;
    if (need <= 64) {
        u64 m = (need == 64) ? ~0ULL : ((1ULL << need) - 1);
        return (w0 & m) == 0;
    }
    if (w0) return 0;
    if (b + 1 >= LK) return 1;
    u64 w1 = x[1] + y[1] + (u64)(s0 >> 64);
    if (b + 1 == LK - 1) w1 &= topmask;
    int need1 = need - 64;
    u64 m1 = (need1 >= 64) ? ~0ULL : ((1ULL << need1) - 1);
    if (need1 > 64) { // very rare (t > 64): fall back to exact valuation
        return 0; // handled by caller via val_sum
    }
    return (w1 & m1) == 0;
}

static u64 hashst(const u64 *x, int L) {
    u64 h = 0x9E3779B97F4A7C15ULL ^ (u64)L;
    if (L <= 8) { for (int i = 0; i < L; i++) { h ^= x[i]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 33; } return h; }
    int idx[6] = {1, 2, L / 2, L - 3, L - 2, L - 1};
    for (int j = 0; j < 6; j++) { h ^= x[idx[j]]; h *= 0xff51afd7ed558ccdULL; h ^= h >> 33; }
    return h;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: bfsA a K [-w witnessfile] [-l logdir] [-p every]\n"); return 1; }
    long a = atol(argv[1]); K = atoi(argv[2]);
    const char *wfile = NULL, *logdir = "/tmp/r3_R3N"; long every = 1000;
    for (int i = 3; i + 1 < argc; i += 2) {
        if (!strcmp(argv[i], "-w")) wfile = argv[i + 1];
        else if (!strcmp(argv[i], "-l")) logdir = argv[i + 1];
        else if (!strcmp(argv[i], "-p")) every = atol(argv[i + 1]);
    }
    printf("bfsA a=%ld K=%d witness=%s\n", a, K, wfile ? wfile : "(none)"); fflush(stdout);
    if (a < 2 || (a & 1)) { printf("only even a >= 2 supported (odd a: f = v2(a!))\n"); return 1; }
    long va = v2fact(a);
    if (va >= K) { printf("RESULT a=%ld K=%d reachable=1 (trivial: v2(a!)=%ld >= K)\n", a, K, va); return 0; }
    LK = (K + 63) / 64; topmask = (K % 64) ? ((1ULL << (K % 64)) - 1) : ~0ULL;
    double t0 = now();

    // F = N! mod 2^K for running N
    u64 *F = calloc(LK, 8); F[0] = 1;
    for (long n = 2; n <= a; n++) mul1(F, (u64)n);
    // options buffers
    u64 *D1 = calloc(LK, 8), *D2 = calloc(LK, 8), *D3 = calloc(LK, 8), *Z = calloc(LK, 8);

    // witness log
    int wfd = -1; long *stepoff = NULL; long *stepN = NULL; long nsteps_cap = 0, nsteps = 0; long logpos = 0;
    char logpath[512];
    if (wfile) {
        snprintf(logpath, sizeof logpath, "%s/bfsA_%ld_%d.plog", logdir, a, K);
        wfd = open(logpath, O_RDWR | O_CREAT | O_TRUNC, 0644);
        if (wfd < 0) { perror("open log"); return 1; }
    }

    // population: N = a+1, X = a! mod 2^K
    long N = a + 1;
    long vN = va;                       // v2(N!) = v2((a+1)!) = v2(a!) since a+1 odd
    int b = (int)(vN / 64);
    int L = LK - b;
    size_t capCur = 1024, capNew = 2048;
    u64 *cur = malloc(capCur * L * 8), *nw = NULL;
    memcpy(cur, F + b, (size_t)L * 8);  // X = a!
    long np = 1;
    // F currently a!; we need F = N! = (a+1)!
    mul1(F, (u64)(a + 1));
    // hash table
    long HS = 1L << 12; u64 *hv = malloc(HS * 8); uint32_t *hi = malloc(HS * 4); uint32_t *hs = calloc(HS, 4); uint32_t stamp = 0;
    uint32_t *plog = NULL; size_t plogcap = 0;
    long maxpop = 1, maxpopN = N; double work = 0; long long totchildren = 0, totdup = 0;
    long lastprint = N;

    while (1) {
        // one step from N to N2 = N+s; s = 1 if N odd (only at start), else 2
        int s = (N & 1) ? 1 : 2;
        long N2 = N + s;
        long vN2 = v2fact(N2);
        int nopt;
        const u64 *opt[4];
        // option values (absolute limb arrays): Z = 0, D1 = N!, D2 = (N+1)!, D3 = N!+(N+1)!
        memcpy(D1, F, (size_t)LK * 8);
        if (s == 1) { opt[0] = Z; opt[1] = D1; nopt = 2; }
        else {
            memcpy(D2, F, (size_t)LK * 8); mul1(D2, (u64)(N + 1));
            { u64 c = 0; for (int i = 0; i < LK; i++) { u128 x = (u128)D1[i] + D2[i] + c; D3[i] = (u64)x; c = (u64)(x >> 64); } D3[LK - 1] &= topmask; }
            opt[0] = Z; opt[1] = D1; opt[2] = D2; opt[3] = D3; nopt = 4;
        }
        if (vN2 >= K) {
            // final gate
            int bestv = -1; long bi = -1; int bo = -1;
            for (long i = 0; i < np; i++) for (int o = 0; o < nopt; o++) {
                int v = val_sum(cur + (size_t)i * L, opt[o], b);
                if (v > bestv) { bestv = v; bi = i; bo = o; }
            }
            int ok = (bestv >= K);
            printf("RESULT a=%ld K=%d reachable=%d (final gate N=%ld->%ld, best=%d, maxpop=%ld at N=%ld, work=%.3e limbops, children=%lld dups=%lld, time=%.1fs)\n",
                   a, K, ok, N, N2, bestv, maxpop, maxpopN, work, totchildren, totdup, now() - t0);
            if (!ok) printf("EXACT a=%ld f=%d g=%ld (final gate failed; best valuation over all paths)\n", a, bestv, bestv - va);
            if (ok && wfd >= 0) {
                // reconstruct: option bo at step from N; then walk back through the log
                // choices: record e_n for n in [a, N2)
                long nn = N2 - a; char *e = calloc(nn, 1); e[0] = 1;
                long idx = bi; int o = bo; long Ncur = N; int scur = s;
                long st = nsteps; // steps logged: 0..nsteps-1; step k transitions stepN[k] -> next
                while (1) {
                    if (scur == 1) { if (o == 1) e[Ncur - a] = 1; }
                    else { if (o == 1 || o == 3) e[Ncur - a] = 1; if (o == 2 || o == 3) e[Ncur + 1 - a] = 1; }
                    if (st == 0) break;
                    st--;
                    uint32_t rec; if (pread(wfd, &rec, 4, (stepoff[st] + idx) * 4) != 4) { perror("pread"); return 1; }
                    idx = rec >> 2; o = rec & 3; Ncur = stepN[st]; scur = (Ncur & 1) ? 1 : 2;
                }
                FILE *wf = fopen(wfile, "w");
                long cnt = 0; for (long j = 0; j < nn; j++) if (e[j]) cnt++;
                fprintf(wf, "# witness for f(%ld,2) >= %d : the set A (one n per line), |A| = %ld; check v2(sum n!) >= %d\n", a, K, cnt, K);
                for (long j = 0; j < nn; j++) if (e[j]) fprintf(wf, "%ld\n", a + j);
                fclose(wf);
                printf("witness written: %s (%ld terms)\n", wfile, cnt);
            }
            return 0;
        }
        int bn = (int)(vN2 / 64); int Ln = LK - bn;
        // capacity
        size_t need = (size_t)np * (nopt == 2 ? 2 : 2) + 16; // at most 2 survivors per parent (see report) -- checked below
        if (need > capNew) { capNew = need + need / 4; }
        free(nw); nw = malloc(capNew * (size_t)Ln * 8);
        if (!nw) { printf("out of memory (np=%ld, Ln=%d)\n", np, Ln); return 3; }
        while (HS < 2 * (long)need) { HS <<= 1; free(hv); free(hi); free(hs); hv = malloc(HS * 8); hi = malloc(HS * 4); hs = calloc(HS, 4); stamp = 0; }
        stamp++; if (stamp == 0) { memset(hs, 0, HS * 4); stamp = 1; }
        if (wfd >= 0 && plogcap < need) { plogcap = need + need / 4; plog = realloc(plog, plogcap * 4); }
        long nn = 0;
        int bestv = -1;
        u64 *tmp = malloc((size_t)L * 8);
        for (long i = 0; i < np; i++) {
            const u64 *x = cur + (size_t)i * L;
            int nchild = 0;
            for (int o = 0; o < nopt; o++) {
                int ok;
                int need_bits = (int)(vN2 - 64 * b);
                if (need_bits <= 128) ok = quick_ok(x, opt[o], b, (int)vN2);
                else ok = (val_sum(x, opt[o], b) >= vN2);
                if (need_bits > 128 && ok) {}
                if (!ok) continue;
                // child = x + opt mod 2^K, stored from limb bn
                addrange(tmp, x, opt[o], b);
                // verify low limbs between b and bn are zero (they must be, as v >= vN2 >= 64*bn)
                const u64 *c = tmp + (bn - b);
                nchild++;
                totchildren++;
                u64 h = hashst(c, Ln); long pos = h & (HS - 1); int dup = 0;
                while (hs[pos] == stamp) {
                    if (hv[pos] == h && !memcmp(nw + (size_t)hi[pos] * Ln, c, (size_t)Ln * 8)) { dup = 1; break; }
                    pos = (pos + 1) & (HS - 1);
                }
                if (dup) { totdup++; continue; }
                if ((size_t)nn >= capNew) { printf("capacity exceeded\n"); return 4; }
                memcpy(nw + (size_t)nn * Ln, c, (size_t)Ln * 8);
                hs[pos] = stamp; hv[pos] = h; hi[pos] = (uint32_t)nn;
                if (wfd >= 0) plog[nn] = (uint32_t)((i << 2) | o);
                nn++;
            }
            if (nchild > 2) { printf("unexpected: %d children\n", nchild); return 5; }
        }
        free(tmp);
        work += (double)np * L;
        if (nn == 0) {
            // death: exact value
            for (long i = 0; i < np; i++) for (int o = 0; o < nopt; o++) {
                int v = val_sum(cur + (size_t)i * L, opt[o], b); if (v > bestv) bestv = v;
            }
            printf("EXACT a=%ld f=%d g=%ld (population died)\n", a, bestv, bestv - va);
            printf("RESULT a=%ld K=%d reachable=0 DIED at step N=%ld->%ld (v2(N!)=%ld, v2(N2!)=%ld); exact f(a,2)=%d g=%d; maxpop=%ld at N=%ld, work=%.3e, children=%lld dups=%lld, time=%.1fs\n",
                   a, K, N, N2, vN, vN2, bestv, bestv - (int)va, maxpop, maxpopN, work, totchildren, totdup, now() - t0);
            return 0;
        }
        if (wfd >= 0) {
            if (nsteps >= nsteps_cap) { nsteps_cap = nsteps_cap ? 2 * nsteps_cap : 1 << 16; stepoff = realloc(stepoff, nsteps_cap * 8); stepN = realloc(stepN, nsteps_cap * 8); }
            stepoff[nsteps] = logpos; stepN[nsteps] = N; nsteps++;
            if (write(wfd, plog, (size_t)nn * 4) != (ssize_t)(nn * 4)) { perror("write log"); return 1; }
            logpos += nn;
        }
        // advance
        u64 *t = cur; cur = nw; nw = t; { size_t tc = capCur; capCur = capNew; capNew = tc; }
        np = nn; L = Ln; b = bn; vN = vN2;
        // F <- N2!
        for (long n = N + 1; n <= N2; n++) mul1(F, (u64)n);
        N = N2;
        if (np > maxpop) { maxpop = np; maxpopN = N; }
        if (N - lastprint >= every) {
            lastprint = N;
            printf("N=%ld R=%ld pop=%ld L=%d maxpop=%ld work=%.3e children=%lld dups=%lld t=%.1fs\n", N, K - vN, np, L, maxpop, work, totchildren, totdup, now() - t0);
            fflush(stdout);
        }
    }
}
