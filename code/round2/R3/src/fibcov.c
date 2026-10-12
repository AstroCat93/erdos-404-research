/*
 * fibcov.c -- PROGRAM A (R3-frontier, 2026-10-11).  Written from scratch; shares no code with
 * publish-erdos404/code (cov.c, cov_pos.c, cov_check2.c) or with fibcov2.c (program B).
 *
 * Decides whether the 2^H subset sums of
 *      y_i = prod_{s=1}^{i} (p^t K - (H-s)),   0 <= i < H        (y_0 = 1)
 * cover Z/p^M, M = t + c, c = v_p((H-1)!)   [note.md, Theorem 3.12(a)].
 *
 * Method ("fibres by the low k digits").  Let L = {i : v_p(y_i) < k}, U = {i : v_p(y_i) >= k}.
 * Every element of U is divisible by p^k.  For a residue r mod p^k write the fibre
 *      F_r = { r + p^k z : z in Z/p^(M-k) }.
 * A subset sum a + b (a from L, b from U) lies in F_r iff a == r (mod p^k), and then equals
 *      r + p^k ( (a - r)/p^k + b/p^k ).
 * Hence  Sigma(L u U) covers Z/p^M  iff  for every r:
 *      { (a-r)/p^k : a in Sigma(L), a == r mod p^k }  +  Sigma({ y_u / p^k : u in U })  =  Z/p^(M-k).
 * For each fibre we build the left set as a bitset of p^(M-k) bits (meet-in-the-middle enumeration
 * of Sigma(L)), then apply x -> x  OR  x + w  (cyclic in Z/p^(M-k)) for each w = y_u/p^k, and test
 * that the bitset is full.  Memory: two bitsets of p^(M-k) bits.
 *
 * usage:
 *   fibcov p t H k pos K1 [K2 ...]      positions N* = p^t K (K not divisible by p)
 *   fibcov p t H k all [nsplit split]   every unit class K mod p^c (K = 1..p^c-1, p not | K)
 *   fibcov p t H k list FILE            K values read from FILE
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
static size_t NW;                 /* words per fibre bitset */
static uint64_t *A, *Bf;          /* double buffer */
static uint64_t lastmask;

static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
static int vfact(uint64_t n, uint64_t p) { int s = 0; while (n) { n /= p; s += (int)n; } return s; }
static uint64_t ipow(uint64_t b, int e) { uint64_t r = 1; while (e--) { if (r > UINT64_MAX / b) { fprintf(stderr, "overflow\n"); exit(2); } r *= b; } return r; }
static uint64_t mulmod(uint64_t a, uint64_t b, uint64_t m) { return (uint64_t)(((u128)a * b) % m); }

/* 64 bits of bitset X starting at bit position pos, cyclically modulo F */
static inline uint64_t grab(const uint64_t *X, uint64_t pos) {
    if (pos + 64 <= F) {
        uint64_t w = pos >> 6, o = pos & 63;
        if (!o) return X[w];
        return (X[w] >> o) | (X[w + 1] << (64 - o));
    }
    uint64_t r = 0;
    for (int b = 0; b < 64; b++) {
        uint64_t q = pos + b; while (q >= F) q -= F;
        r |= ((X[q >> 6] >> (q & 63)) & 1ULL) << b;
    }
    return r;
}

/* out = in | (in shifted cyclically by +w in Z/F) : out bit x = in bit x OR in bit (x-w mod F) */
/* contiguous segment: out[j] = in[j] | 64 source bits starting at bit position pos0 + 64*(j-j0),
   for j in [j0, j1), all source windows lying inside [0, F). Constant bit offset -> vectorisable. */
static void seg_or(uint64_t *restrict out, const uint64_t *restrict in, size_t j0, size_t j1, uint64_t pos0) {
    const uint64_t *src = in + (pos0 >> 6);
    unsigned o = (unsigned)(pos0 & 63);
    size_t n = j1 - j0;
    uint64_t *restrict d = out + j0; const uint64_t *restrict s0 = in + j0;
    if (o == 0) { for (size_t q = 0; q < n; q++) d[q] = s0[q] | src[q]; }
    else { unsigned oo = 64 - o; for (size_t q = 0; q < n; q++) d[q] = s0[q] | (src[q] >> o) | (src[q + 1] << oo); }
}
static void rot_or(uint64_t *restrict out, const uint64_t *restrict in, uint64_t w) {
    uint64_t pos = (F - w) % F;     /* source bit position for output bit 0 */
    size_t j = 0;
    while (j < NW) {
        /* how many whole words can be taken without the source window crossing F? */
        uint64_t room = (F - pos) / 64;          /* windows [pos+64q, pos+64q+64) inside [0,F) for q < room */
        size_t n = (size_t)room; if (n > NW - j) n = NW - j;
        if (n > 0) {
            seg_or(out, in, j, j + n, pos);
            j += n; pos += 64 * (uint64_t)n; if (pos >= F) pos -= F;
        }
        if (j < NW) {                             /* one window crossing the wrap point: slow path */
            out[j] = in[j] | grab(in, pos);
            j++; pos += 64; while (pos >= F) pos -= F;
        }
    }
    out[NW - 1] &= lastmask;
}

static int is_full(const uint64_t *X) {
    for (size_t j = 0; j + 1 < NW; j++) if (X[j] != ~0ULL) return 0;
    return (X[NW - 1] & lastmask) == lastmask;
}
static uint64_t popcnt(const uint64_t *X) { uint64_t s = 0; for (size_t j = 0; j < NW; j++) s += (uint64_t)__builtin_popcountll(X[j]); return s; }

/* checks one K; returns number of missing residues mod Q (0 = covered) */
static uint64_t check_K(uint64_t K, int dump) {
    uint64_t ptK = mulmod(ipow(P, T) % Q, K % Q, Q);
    uint64_t *y = malloc(sizeof(uint64_t) * Hh);
    int *vv = malloc(sizeof(int) * Hh);
    y[0] = 1 % Q;
    for (int i = 1; i < Hh; i++) {
        uint64_t f = (ptK + Q - ((uint64_t)(Hh - i) % Q)) % Q;
        y[i] = mulmod(y[i - 1], f, Q);
    }
    /* valuations; sanity: must equal v_p((H-1)!/(H-1-i)!) */
    int nL = 0, nU = 0;
    uint64_t *Lv = malloc(sizeof(uint64_t) * Hh), *Uw = malloc(sizeof(uint64_t) * Hh);
    for (int i = 0; i < Hh; i++) {
        uint64_t z = y[i]; int v = 0;
        if (z == 0) { fprintf(stderr, "y_%d == 0 mod Q\n", i); exit(3); }
        while (z % P == 0) { z /= P; v++; }
        int vexp = vfact(Hh - 1, P) - vfact(Hh - 1 - i, P);
        if (v != vexp) { fprintf(stderr, "valuation mismatch i=%d v=%d exp=%d\n", i, v, vexp); exit(3); }
        vv[i] = v;
        if (v < KL) Lv[nL++] = y[i]; else Uw[nU++] = y[i] / PK;   /* exact: PK | y[i] as integer in [0,Q) */
    }
    /* meet in the middle on L: S1 = sums of first n1, S2 = sums of last n2, S2 bucketed by residue mod PK */
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

    uint64_t missing = 0; int dumped = 0;
    for (uint64_t r = 0; r < PK; r++) {
        memset(A, 0, NW * 8);
        for (size_t q1 = 0; q1 < s1n; q1++) {
            uint64_t s1 = S1[q1];
            uint64_t b = (r + PK - s1 % PK) % PK;
            for (size_t q2 = bst[b]; q2 < bst[b + 1]; q2++) {
                uint64_t a = s1 + S2[q2]; if (a >= Q) a -= Q;
                uint64_t z = (a - r) / PK;              /* a == r mod PK, a >= r */
                A[z >> 6] |= 1ULL << (z & 63);
            }
        }
        uint64_t *cur = A, *nxt = Bf;
        for (int u = 0; u < nU; u++) {
            uint64_t w = Uw[u] % F;
            if (w == 0) continue;
            rot_or(nxt, cur, w);
            uint64_t *tmp = cur; cur = nxt; nxt = tmp;
        }
        if (!is_full(cur)) {
            uint64_t pc = popcnt(cur);
            missing += F - pc;
            if (dumped < dump) {
                for (uint64_t z = 0; z < F && dumped < dump; z++)
                    if (!((cur[z >> 6] >> (z & 63)) & 1)) { printf("    MISS K=%llu x=%llu (x mod p^k=%llu)\n", (unsigned long long)K, (unsigned long long)(r + PK * z), (unsigned long long)r); dumped++; }
            }
            if (getenv("FIBCOV_FIBRESTOP")) break;
        }
        if (cur != A) { uint64_t *tmp = A; A = Bf; Bf = tmp; }   /* keep A/Bf as the two buffers */
    }
    free(S1); free(S2); free(bst); free(y); free(vv); free(Lv); free(Uw);
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
    A = aligned_alloc(64, ((NW * 8 + 63) / 64) * 64); Bf = aligned_alloc(64, ((NW * 8 + 63) / 64) * 64);
    if (!A || !Bf) { fprintf(stderr, "alloc failed\n"); return 2; }
    int dump = getenv("FIBCOV_DUMP") ? atoi(getenv("FIBCOV_DUMP")) : 0;
    int stop = getenv("FIBCOV_STOP") ? atoi(getenv("FIBCOV_STOP")) : 0;
    printf("# fibcov(A) p=%llu t=%d H=%d c=%d M=%d k=%d  Q=%llu fibre=%llu bits (%zu MB x2)\n",
           (unsigned long long)P, T, Hh, C, M, KL, (unsigned long long)Q, (unsigned long long)F, NW * 8 >> 20);
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
    printf("SUMMARY A p=%llu t=%d H=%d c=%d M=%d k=%d mode=%s nK=%zu fail=%zu worst_missing=%llu %s total=%.1fs\n",
           (unsigned long long)P, T, Hh, C, M, KL, mode, nK, nfail, (unsigned long long)worst,
           nfail ? "SOME_NOT_COVERED" : "ALL_COVERED", now() - t0);
    return nfail ? 3 : 0;
}
