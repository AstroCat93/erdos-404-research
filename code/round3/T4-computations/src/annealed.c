// annealed.c -- exact annealed moments for Erdos #404 (round 3, track T4).
//
// For prime p and level G let M_G = max{ b : v_p(b!) < G }  (so v_p(b!) >= G for all b > M_G,
// and pi_b(x) = (x+1)...(x+b) is divisible by b!, hence by p^G, for every x in Z_p and b > M_G;
// conversely pi_b(0) = b!, so M_G is the least cutoff that works for all x).
// For each class x mod p^G compute exactly
//     N_G(x) = #{ B subset [1, M_G] : 1 + sum_{b in B} pi_b(x) == 0 (mod p^G) }
// by a dynamic programme over residues.  Pruning: once all remaining terms are divisible by p^L,
// only partial sums divisible by p^L can still reach 0, so we keep only those and divide by p^L
// (array of size p^{G-L}).  Sparse (sorted pairs) while small, dense count array afterwards.
// Z_G(x) = p^G 2^{-M_G} N_G(x).  Reports E Z, E Z^2, E Z^2/(E Z)^2, delta_G = P(N > 0),
// E[Z | Z>0], max N, and the histogram of N over classes (optionally per-class dump).
//
// usage: annealed p G nthreads [dumpfile]
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

typedef uint64_t u64; typedef unsigned __int128 u128;

typedef struct { u64 *r; u64 *c; u64 *r2; u64 *c2; size_t cap; u64 *dense; u64 *dense2; size_t dcap; } ws_t;

static void ws_ensure(ws_t *W, size_t n) {
    if (n <= W->cap) return;
    size_t c = W->cap ? W->cap : 1024; while (c < n) c *= 2;
    W->r = realloc(W->r, c * 8); W->c = realloc(W->c, c * 8); W->r2 = realloc(W->r2, c * 8); W->c2 = realloc(W->c2, c * 8);
    if (!W->r || !W->c || !W->r2 || !W->c2) { fprintf(stderr, "oom\n"); exit(1); }
    W->cap = c;
}
static void ws_densure(ws_t *W, size_t n) {
    if (n <= W->dcap) return;
    size_t c = W->dcap ? W->dcap : 1024; while (c < n) c *= 2;
    W->dense = realloc(W->dense, c * 8); W->dense2 = realloc(W->dense2, c * 8);
    if (!W->dense || !W->dense2) { fprintf(stderr, "oom\n"); exit(1); }
    W->dcap = c;
}

// exact count N_G(x) for x given mod p^G (M = p^G), M_G = Mcut.
static __thread int FREE, MAXV; // free terms (== 0 mod p^G) among b <= M_G; max_{i<=M_G} v_p(x+i); set by countN
static u64 countN(u64 p, u64 x, int G, u64 M, u64 Mcut, ws_t *W) {
    // state: sparse sorted (r[i], c[i]) with residues in [0, Mc), Mc = p^{G-L}, or dense array of size Mc.
    u64 Mc = M; int L = 0;
    int dense = 0;
    ws_ensure(W, 4);
    u64 *R = W->r, *C = W->c; size_t n = 1; R[0] = 1 % M; C[0] = 1;   // B = empty: S = 1
    u64 u = 1; int v = 0;  // u = unit part of pi_b(x) mod M, v = v_p(pi_b(x))
    FREE = 0; MAXV = 0;
    for (u64 i = 1; i <= Mcut; i++) { u64 y = x + i; int w = 0; while (y % p == 0) { y /= p; w++; } if (w > MAXV) MAXV = w; }
    for (u64 b = 1; b <= Mcut; b++) {
        u64 y = x + b; int w = 0;
        while (y % p == 0) { y /= p; w++; }
        v += w;
        if (v >= G) { FREE = (int)(Mcut - b + 1); break; }  // terms b..M_G vanish mod p^G: each doubles the count
        u = (u64)(((u128)u * (u128)(y % M)) % M);
        if (v > L) {
            u64 d = 1; for (int i = 0; i < v - L; i++) d *= p;
            if (!dense) {
                size_t m = 0;
                for (size_t i = 0; i < n; i++) if (R[i] % d == 0) { R[m] = R[i] / d; C[m] = C[i]; m++; }
                n = m;
            } else {
                u64 *D = W->dense; u64 Mn = Mc / d; size_t m = 0;
                for (u64 i = 0; i < Mn; i++) D[i] = D[i * d];
                (void)m;
            }
            Mc /= d; L = v;
            if (!dense && n == 0) return 0;
        }
        u64 t = u % Mc;  // normalised term pi_b(x)/p^L mod p^{G-L}
        if (!dense && 2 * n >= Mc) {
            // switch to dense
            ws_densure(W, Mc);
            u64 *D = W->dense; memset(D, 0, Mc * 8);
            for (size_t i = 0; i < n; i++) D[R[i]] += C[i];
            dense = 1;
        }
        if (dense) {
            u64 *D = W->dense, *E = W->dense2;
            // E[r] = D[r] + D[r - t]
            for (u64 r = 0; r < Mc; r++) { u64 s = r >= t ? r - t : r + Mc - t; E[r] = D[r] + D[s]; }
            W->dense = E; W->dense2 = D;
        } else {
            ws_ensure(W, 2 * n + 4);
            R = W->r; C = W->c; u64 *R2 = W->r2, *C2 = W->c2;
            // shifted copy: residues R[i]+t mod Mc; sorted order starts at first index with R[i] >= Mc - t
            size_t wrap; { size_t lo = 0, hi = n; while (lo < hi) { size_t mid = (lo + hi) / 2; if (R[mid] >= Mc - t) hi = mid; else lo = mid + 1; } wrap = lo; }
            size_t i = 0, j = 0, m = 0;
            while (i < n || j < n) {
                u64 sv = 0, sc = 0; int have = (j < n);
                if (have) { size_t idx = (j < n - wrap) ? (wrap + j) : (j - (n - wrap)); sv = (j < n - wrap) ? (R[idx] + t - Mc) : (R[idx] + t); sc = C[idx]; }
                if (i < n && (!have || R[i] < sv)) { R2[m] = R[i]; C2[m] = C[i]; m++; i++; }
                else if (i < n && have && R[i] == sv) { R2[m] = R[i]; C2[m] = C[i] + sc; m++; i++; j++; }
                else { R2[m] = sv; C2[m] = sc; m++; j++; }
            }
            W->r = R2; W->c = C2; W->r2 = R; W->c2 = C; R = R2; C = C2; n = m;
        }
    }
    u64 res = 0;
    if (dense) res = W->dense[0];
    else for (size_t i = 0; i < n; i++) if (R[i] == 0) { res = C[i]; break; }
    return res;
}

static u64 P, M, MCUT; static int GG, NT;
typedef struct { u64 cnt, surv, maxN; u128 S1, S2; } acc_t;
static acc_t ACC[64][64];   // [thread][maxv]
static void *worker(void *arg) {
    long id = (long)arg; ws_t W; memset(&W, 0, sizeof W);
    for (u64 x = id; x < M; x += NT) {
        u64 n = countN(P, x, GG, M, MCUT, &W);
        u128 N = (u128)n << FREE;            // task's N_G(x) = N' * 2^{free}
        acc_t *A = &ACC[id][MAXV];
        A->cnt++; if (n) A->surv++;
        A->S1 += N; A->S2 += N * N;
        if (N > A->maxN) A->maxN = (u64)N;
        if (A->S2 >> 124) { fprintf(stderr, "S2 overflow risk\n"); exit(2); }
    }
    return 0;
}
static void pr128(u128 v, char *buf) { char t[64]; int i = 0; if (!v) { strcpy(buf, "0"); return; } while (v) { t[i++] = '0' + (int)(v % 10); v /= 10; } for (int j = 0; j < i; j++) buf[j] = t[i - 1 - j]; buf[i] = 0; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: annealed p G nthreads\n"); return 1; }
    P = strtoull(argv[1], 0, 10); GG = atoi(argv[2]); NT = atoi(argv[3]);
    M = 1; for (int i = 0; i < GG; i++) M *= P;
    { u64 b = 0; int v = 0; for (;;) { u64 y = b + 1; int w = 0; while (y % P == 0) { y /= P; w++; } if (v + w >= GG) break; v += w; b++; } MCUT = b; }
    if (MCUT >= 63) { fprintf(stderr, "N' may overflow u64 (M_G=%llu)\n", (unsigned long long)MCUT); return 3; }
    memset(ACC, 0, sizeof ACC);
    pthread_t th[64];
    for (long i = 0; i < NT; i++) pthread_create(&th[i], 0, worker, (void *)i);
    for (long i = 0; i < NT; i++) pthread_join(th[i], 0);
    acc_t tot[64]; memset(tot, 0, sizeof tot);
    for (int t = 0; t < NT; t++) for (int v = 0; v < 64; v++) { acc_t *A = &ACC[t][v]; tot[v].cnt += A->cnt; tot[v].surv += A->surv; tot[v].S1 += A->S1; tot[v].S2 += A->S2; if (A->maxN > tot[v].maxN) tot[v].maxN = A->maxN; }
    long double two = 1.0L; for (u64 i = 0; i < MCUT; i++) two *= 2;
    char b1[64], b2[64];
    printf("# p=%llu G=%d M_G=%llu p^G=%llu  (Z = p^G N / 2^{M_G}; rows: maxv = max_{1<=i<=M_G} v_p(x+i))\n", (unsigned long long)P, GG, (unsigned long long)MCUT, (unsigned long long)M);
    printf("# maxv classes surviving sumN sumN2 maxN\n");
    acc_t all; memset(&all, 0, sizeof all);
    for (int v = 0; v < 64; v++) if (tot[v].cnt) {
        pr128(tot[v].S1, b1); pr128(tot[v].S2, b2);
        printf("row %d %llu %llu %s %s %llu\n", v, (unsigned long long)tot[v].cnt, (unsigned long long)tot[v].surv, b1, b2, (unsigned long long)tot[v].maxN);
        all.cnt += tot[v].cnt; all.surv += tot[v].surv; all.S1 += tot[v].S1; all.S2 += tot[v].S2; if (tot[v].maxN > all.maxN) all.maxN = tot[v].maxN;
    }
    pr128(all.S1, b1); pr128(all.S2, b2);
    long double EZ = (long double)all.S1 / two, EZ2 = (long double)M * (long double)all.S2 / (two * two);
    printf("total classes=%llu surviving=%llu sumN=%s sumN2=%s maxN=%llu\n", (unsigned long long)all.cnt, (unsigned long long)all.surv, b1, b2, (unsigned long long)all.maxN);
    printf("EZ=%.10Lg EZ2=%.10Lg ratio=%.10Lg delta=%.10Lg\n", EZ, EZ2, EZ2 / (EZ * EZ), (long double)all.surv / (long double)M);
    return 0;
}
