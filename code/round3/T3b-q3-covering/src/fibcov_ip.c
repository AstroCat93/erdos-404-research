/*
 * fibcov_ip.c -- PROGRAM A' (track T3b, round 3, 2026-10-12).
 * Derived from program A (publish-erdos404/code/round2/R3/src/fibcov.c, track R3, 2026-10-11).
 * Same element computation, same fibre decomposition, same meet-in-the-middle enumeration of the low
 * subset sums.  CHANGED: the shift-OR kernel is IN PLACE (one fibre bitset of p^(M-k) bits plus a
 * save buffer of at most p^(M-k)/2 bits, instead of two full bitsets), and the last high element is
 * applied by a read-only counting pass.  Purpose: depth-8 positions at p = 19 (p^8 bits = 2.0 GB per
 * bitset) within a 4 GB budget.
 *
 * Question decided (note.md Theorem 3.12(a)): do the 2^H subset sums of
 *      y_i = prod_{s=1}^{i} (p^t K - (H-s)),   0 <= i < H        (y_0 = 1)
 * cover Z/p^M, M = t + c, c = v_p((H-1)!) ?
 *
 * usage:
 *   fibcov_ip p t H k pos K1 [K2 ...]      positions N* = p^t K (K not divisible by p)
 *   fibcov_ip p t H k all [nsplit split]   every unit class K mod p^c
 *   fibcov_ip p t H k list FILE            K values read from FILE
 * flags (env): FIBCOV_DUMP=n  print up to n missing residues per failing K (as x mod p^M)
 *              FIBCOV_STOP=1  stop at the first failing K
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;

static uint64_t P, Q, PK, F;      /* p, p^M, p^k, p^(M-k) */
static int T, Hh, C, M, KL;
static size_t NW;                 /* words per fibre bitset (plus 2 pad words allocated, kept zero) */
static uint64_t *A, *SV;          /* the fibre bitset; the save buffer (ceil(F/2/64)+2 words) */
static size_t NSV;
static uint64_t lastmask;

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static int vfact(uint64_t n, uint64_t p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }
static uint64_t ipow(uint64_t b, int e) { uint64_t r = 1; while (e--) { if (r > UINT64_MAX / b) { fprintf(stderr, "overflow\n"); exit(2); } r *= b; } return r; }
static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m) { return (uint64_t)(((u128)a * b) % m); }

/* 64 bits of X starting at LINEAR bit position pos (pos < 64*NW; pad words are zero) */
static inline uint64_t lin64(const uint64_t *X, uint64_t pos) {
    uint64_t w = pos >> 6, o = pos & 63;
    if (!o) return X[w];
    return (X[w] >> o) | (X[w + 1] << (64 - o));
}
/* 64 bits of X starting at bit position pos, CYCLICALLY modulo F (slow path only when crossing F) */
static inline uint64_t cyc64(const uint64_t *X, uint64_t pos) {
    if (pos + 64 <= F) return lin64(X, pos);
    uint64_t r = 0;
    for (int b = 0; b < 64; b++) {
        uint64_t q = pos + b; if (q >= F) q -= F;
        r |= ((X[q >> 6] >> (q & 63)) & 1ULL) << b;
    }
    return r;
}
/* DST bits [0,n) := X bits [start, start+n)  (linear; start+n <= F) */
static void copy_bits(uint64_t *DST, const uint64_t *X, uint64_t start, uint64_t n) {
    uint64_t nw = (n + 63) / 64;
    for (uint64_t q = 0; q < nw; q++) DST[q] = lin64(X, start + 64 * q);
    if (n & 63) DST[nw - 1] &= (1ULL << (n & 63)) - 1ULL;
    DST[nw] = 0;
}
/* X bits [pos, pos+n) |= SRC bits [0, n)   (linear; pos+n <= F; SRC has a zero pad word) */
static void or_bits_at(uint64_t *X, uint64_t pos, const uint64_t *SRC, uint64_t n) {
    uint64_t nw = (n + 63) / 64;
    unsigned o = (unsigned)(pos & 63);
    uint64_t w0 = pos >> 6;
    for (uint64_t q = 0; q < nw; q++) {
        uint64_t v = SRC[q];
        if (q == nw - 1 && (n & 63)) v &= (1ULL << (n & 63)) - 1ULL;
        if (o == 0) X[w0 + q] |= v;
        else { X[w0 + q] |= v << o; X[w0 + q + 1] |= v >> (64 - o); }
    }
}

/* IN PLACE: X <- X | rot(X, w), i.e. bit x |= bit (x - w mod F), for all x < F.  0 < w < F. */
static void rot_or_inplace(uint64_t *X, uint64_t w) {
    if (w == 0) return;
    if (2 * w <= F) {
        /* targets x in [w,F) read sources x-w in [0,F-w): process words in DESCENDING order, so every
           source bit is read before it is overwritten (sources lie below the target word, or in the
           target word itself, which is read before being written).  Targets x in [0,w) read the
           original bits [F-w,F): saved first. */
        copy_bits(SV, X, F - w, w);
        uint64_t j0 = w >> 6;                       /* word containing bit w */
        for (uint64_t j = NW - 1; j > j0; j--) X[j] |= lin64(X, 64 * j - w);
        /* partial word j0: bits x in [w, 64*j0+64) have sources x-w in [0, 64*j0+64-w) (word 0 only) */
        { unsigned sh = (unsigned)(w - 64 * j0); X[j0] |= X[0] << sh; }   /* sh in [0,63]; sh=0 -> whole word 0 */
        X[NW - 1] &= lastmask;
        or_bits_at(X, 0, SV, w);                    /* wrap: x in [0,w) |= original bit x-w+F */
    } else {
        uint64_t u = F - w;                         /* 0 < u < F/2;  x - w == x + u (mod F) */
        /* targets x in [0,F-u) read sources x+u in [u,F): ASCENDING order (sources lie above the target
           word, or in it).  Targets x in [F-u,F) read original bits [0,u): saved first. */
        copy_bits(SV, X, 0, u);
        uint64_t lim = F - u;                       /* targets below lim */
        uint64_t j1 = lim >> 6;                     /* word containing bit lim (partial), full words j < j1 */
        for (uint64_t j = 0; j < j1; j++) X[j] |= lin64(X, 64 * j + u);
        if (lim & 63) {                             /* partial word j1: target bits [64*j1, lim) */
            uint64_t v = lin64(X, 64 * j1 + u);     /* sources [64*j1+u, 64*j1+u+64) subset of [lim+? ..) fine: pad is zero */
            v &= (1ULL << (lim & 63)) - 1ULL;
            X[j1] |= v;
        }
        X[NW - 1] &= lastmask;
        or_bits_at(X, lim, SV, u);                  /* wrap: x in [F-u,F) |= original bit x-(F-u) */
    }
}
/* READ-ONLY: number of x < F with (X bit x) == 0 and (X bit (x-w mod F)) == 0. */
static uint64_t rot_or_count_missing(const uint64_t *X, uint64_t w) {
    uint64_t miss = 0;
    for (uint64_t j = 0; j < NW; j++) {
        uint64_t pos = 64 * j + F - w; if (pos >= F) pos -= F;     /* source position of target bit 64j */
        uint64_t v = X[j] | (w ? cyc64(X, pos) : 0);
        if (j == NW - 1) v |= ~lastmask;
        miss += (uint64_t)__builtin_popcountll(~v);
    }
    return miss;
}
static uint64_t count_missing(const uint64_t *X) {
    uint64_t miss = 0;
    for (uint64_t j = 0; j < NW; j++) { uint64_t v = X[j]; if (j == NW - 1) v |= ~lastmask; miss += (uint64_t)__builtin_popcountll(~v); }
    return miss;
}

/* checks one K; returns number of missing residues mod Q (0 = covered) */
static uint64_t check_K(uint64_t K, int dump) {
    uint64_t ptK = mulmod(ipow(P, T) % Q, K % Q, Q);
    uint64_t *y = malloc(sizeof(uint64_t) * Hh);
    y[0] = 1 % Q;
    for (int i = 1; i < Hh; i++) {
        uint64_t f = (ptK + Q - ((uint64_t)(Hh - i) % Q)) % Q;
        y[i] = mulmod(y[i - 1], f, Q);
    }
    int nL = 0, nU = 0;
    uint64_t *Lv = malloc(sizeof(uint64_t) * Hh), *Uw = malloc(sizeof(uint64_t) * Hh);
    for (int i = 0; i < Hh; i++) {
        uint64_t z = y[i]; int v = 0;
        if (z == 0) { fprintf(stderr, "y_%d == 0 mod Q\n", i); exit(3); }
        while (z % P == 0) { z /= P; v++; }
        int vexp = vfact(Hh - 1, P) - vfact(Hh - 1 - i, P);
        if (v != vexp) { fprintf(stderr, "valuation mismatch i=%d v=%d exp=%d\n", i, v, vexp); exit(3); }
        if (v < KL) Lv[nL++] = y[i]; else Uw[nU++] = y[i] / PK;
    }
    int n2 = nL < 20 ? nL : 20, n1 = nL - n2;
    size_t s1n = (size_t)1 << n1, s2n = (size_t)1 << n2;
    uint64_t *S1 = malloc(8 * s1n), *S2raw = malloc(8 * s2n), *S2 = malloc(8 * s2n);
    S1[0] = 0; for (int j = 0; j < n1; j++) { size_t h = (size_t)1 << j; for (size_t q = 0; q < h; q++) { uint64_t s = S1[q] + Lv[j]; if (s >= Q) s -= Q; S1[h + q] = s; } }
    S2raw[0] = 0; for (int j = 0; j < n2; j++) { size_t h = (size_t)1 << j; for (size_t q = 0; q < h; q++) { uint64_t s = S2raw[q] + Lv[n1 + j]; if (s >= Q) s -= Q; S2raw[h + q] = s; } }
    size_t *bst = calloc(PK + 1, sizeof(size_t));
    for (size_t q = 0; q < s2n; q++) bst[S2raw[q] % PK + 1]++;
    for (uint64_t r = 0; r < PK; r++) bst[r + 1] += bst[r];
    size_t *fill = malloc(sizeof(size_t) * PK); memcpy(fill, bst, sizeof(size_t) * PK);
    for (size_t q = 0; q < s2n; q++) { uint64_t r = S2raw[q] % PK; S2[fill[r]++] = S2raw[q]; }
    free(fill); free(S2raw);

    /* reduce high elements mod F and drop zeros (a zero shift changes nothing) */
    int nUe = 0; for (int u = 0; u < nU; u++) { uint64_t w = Uw[u] % F; if (w) Uw[nUe++] = w; }

    uint64_t missing = 0; int dumped = 0;
    for (uint64_t r = 0; r < PK; r++) {
        memset(A, 0, (NW + 2) * 8);
        for (size_t q1 = 0; q1 < s1n; q1++) {
            uint64_t s1 = S1[q1];
            uint64_t b = (r + PK - s1 % PK) % PK;
            for (size_t q2 = bst[b]; q2 < bst[b + 1]; q2++) {
                uint64_t a = s1 + S2[q2]; if (a >= Q) a -= Q;
                uint64_t z = (a - r) / PK;
                A[z >> 6] |= 1ULL << (z & 63);
            }
        }
        uint64_t fm;
        if (nUe == 0) fm = count_missing(A);
        else {
            for (int u = 0; u + 1 < nUe; u++) rot_or_inplace(A, Uw[u]);
            fm = rot_or_count_missing(A, Uw[nUe - 1]);
        }
        if (fm) {
            missing += fm;
            if (dumped < dump) {
                if (nUe) rot_or_inplace(A, Uw[nUe - 1]);
                for (uint64_t z = 0; z < F && dumped < dump; z++)
                    if (!((A[z >> 6] >> (z & 63)) & 1)) { printf("    MISS K=%llu x=%llu (x mod p^k=%llu)\n", (unsigned long long)K, (unsigned long long)(r + PK * z), (unsigned long long)r); dumped++; }
            }
            if (getenv("FIBCOV_FIBRESTOP")) break;
        }
    }
    free(S1); free(S2); free(bst); free(y); free(Lv); free(Uw);
    return missing;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: %s p t H k pos K... | all [nsplit split] | list FILE\n", argv[0]); return 1; }
    P = strtoull(argv[1], 0, 10); T = atoi(argv[2]); Hh = atoi(argv[3]); KL = atoi(argv[4]);
    const char *mode = argv[5];
    C = vfact(Hh - 1, P); M = T + C;
    if (KL < 0 || KL > M) { fprintf(stderr, "bad k\n"); return 1; }
    Q = ipow(P, M); PK = ipow(P, KL); F = Q / PK;
    if ((uint64_t)Hh > ipow(P, T)) { fprintf(stderr, "H > p^t\n"); return 1; }
    NW = (F + 63) / 64;
    lastmask = (F % 64) ? ((1ULL << (F % 64)) - 1) : ~0ULL;
    NSV = (F / 2 + 63) / 64 + 2;
    A = calloc(NW + 2, 8); SV = calloc(NSV, 8);
    if (!A || !SV) { fprintf(stderr, "alloc failed\n"); return 2; }
    int dump = getenv("FIBCOV_DUMP") ? atoi(getenv("FIBCOV_DUMP")) : 0;
    int stop = getenv("FIBCOV_STOP") ? atoi(getenv("FIBCOV_STOP")) : 0;
    printf("# fibcov_ip(A') p=%llu t=%d H=%d c=%d M=%d k=%d  Q=%llu fibre=%llu bits (%zu MB + %zu MB save)\n",
           (unsigned long long)P, T, Hh, C, M, KL, (unsigned long long)Q, (unsigned long long)F, NW * 8 >> 20, NSV * 8 >> 20);
    fflush(stdout);
    uint64_t *Ks = NULL; size_t nK = 0, capK = 0;
#define PUSHK(v) do { if (nK == capK) { capK = capK ? 2 * capK : 1024; Ks = realloc(Ks, 8 * capK); } Ks[nK++] = (v); } while (0)
    if (!strcmp(mode, "pos")) { for (int a = 6; a < argc; a++) PUSHK(strtoull(argv[a], 0, 10)); }
    else if (!strcmp(mode, "all")) {
        int nsplit = argc > 6 ? atoi(argv[6]) : 1, split = argc > 7 ? atoi(argv[7]) : 0;
        uint64_t pc = ipow(P, C); size_t idx = 0;
        if (C == 0) { if (split == 0) PUSHK(1); }
        else for (uint64_t K = 1; K < pc; K++) { if (K % P == 0) continue; if ((int)(idx++ % nsplit) == split) PUSHK(K); }
    } else if (!strcmp(mode, "list")) {
        FILE *fp = fopen(argv[6], "r"); unsigned long long v; while (fp && fscanf(fp, "%llu", &v) == 1) PUSHK(v); if (fp) fclose(fp);
    } else { fprintf(stderr, "bad mode\n"); return 1; }
    size_t nfail = 0; uint64_t worst = 0; double t0 = now();
    for (size_t q = 0; q < nK; q++) {
        uint64_t K = Ks[q];
        if (K % P == 0) { printf("K=%llu divisible by p: skipped\n", (unsigned long long)K); continue; }
        double t1 = now();
        uint64_t miss = check_K(K, dump);
        printf("A p=%llu t=%d H=%d c=%d M=%d K=%llu missing=%llu %s [%.2fs]\n", (unsigned long long)P, T, Hh, C, M,
               (unsigned long long)K, (unsigned long long)miss, miss ? "NOT_COVERED" : "COVERED", now() - t1);
        fflush(stdout);
        if (miss) { nfail++; if (miss > worst) worst = miss; if (stop) break; }
    }
    printf("SUMMARY A' p=%llu t=%d H=%d c=%d M=%d k=%d mode=%s nK=%zu fail=%zu worst_missing=%llu %s total=%.1fs\n",
           (unsigned long long)P, T, Hh, C, M, KL, mode, nK, nfail, (unsigned long long)worst,
           nfail ? "SOME_NOT_COVERED" : "ALL_COVERED", now() - t0);
    return nfail ? 3 : 0;
}
