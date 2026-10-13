/*
 * covfast.c -- PROGRAM D (round 3, track R3C, 2026-10-13).
 * Written from scratch in round 3.  It shares no code with fibcov.c (program A), fibcov2.c (B),
 * covchk.c (C) or the round-1 programs cov.c / cov_pos.c / cov_check2.c.
 *
 * Question (note.md Theorem 3.12(a), Proposition 10.10).  For a position N* = p^t K (p not | K)
 * and a block length H, put N1 = N* - H and
 *     y_i = (N1+1)(N1+2)...(N1+i) = (N1+i)!/N1!,   0 <= i < H   (y_0 = 1),
 *     M   = v_p(N*!) - v_p(N1!)   (Legendre; equals t + v_p((H-1)!) when H <= p^t).
 * Do the 2^H subset sums of the y_i cover Z/p^M?  The program prints the EXACT number of residues
 * mod p^M that are not subset sums.
 *
 * Method.
 *  1. Elements: exact GMP products (N1+1)...(N1+i), reduced mod Q = p^M.  The exact p-adic
 *     valuation of each product (mpz_remove) is checked against Legendre's formula.
 *  2. Fibres by the low k digits.  L = {i : v(y_i) < k}, U = {i : v(y_i) >= k}.  A subset sum lies in
 *     the class r mod p^k iff its L-part does; inside that class (identified with Z/F, F = p^(M-k),
 *     via x = r + p^k z) the reachable set is  B_r + Sigma(U/p^k)  with
 *     B_r = {(s - r)/p^k : s in Sigma(L), s == r mod p^k}.  Sigma(L) is enumerated completely
 *     (doubling) and counting-sorted by residue mod p^k.
 *  3. Each fibre is completed in three exact phases, the elements w = y_u/p^k mod F taken in order:
 *     (a) list phase:  explicit list X <- X ++ (X + w mod F) while it has at most LISTMAX entries
 *         (duplicates allowed: the list represents the set of its entries);
 *     (b) bitset phase: X <- X | rot(X, w) on F bits, rot(X,w)[x] = X[(x - w) mod F]; double buffer,
 *         constant-offset word kernel with a 128-bit cyclic pad; popcount fused.  As soon as X is
 *         full the fibre is covered (adding elements to a full set keeps it full);
 *     (c) complement phase: once at most ZMAX residues are missing, keep the sorted list Z of missing
 *         residues and update Z <- Z intersect (Z + w): x is missed after adding w iff x and x - w
 *         were both missed before.
 *     The missing count of the fibre is exact in every phase; the total is the sum over fibres.
 *
 * usage:
 *   covfast p t H k pos K1 [K2 ...]              positions N* = p^t K
 *   covfast p t H k cls LIFT [nsplit split]      all unit classes K' mod p^c, K = K' + LIFT*p^c
 * env: COVFAST_LISTMAX (default 2^24), COVFAST_ZMAX (default 2^22), COVFAST_DUMP=n (print up to n
 *      missed residues per K), COVFAST_STOP=1 (stop at the first K that is not covered).
 * build: cc -O3 -march=native -o covfast covfast.c -lgmp
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <gmp.h>

typedef uint64_t u64;

static u64 P, Q, PK, F;
static int T, H, C, M, KF;
static size_t NW;                  /* words holding F bits */
static u64 *bx, *by;               /* bitsets, NW + 3 words each (3 pad words) */
static u64 *lst;                   /* list phase buffer */
static size_t LISTMAX;
static u64 ZMAX;
static u64 *za, *zb, *zc;          /* complement phase buffers */
static size_t ZCAP;
static long dump_left;

static double wall(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }

static u64 powu(u64 b, int e) {
    u64 r = 1;
    for (int i = 0; i < e; i++) {
        if (r > (UINT64_MAX >> 2) / b) { fprintf(stderr, "covfast: p^%d too large\n", e); exit(2); }
        r *= b;
    }
    return r;
}
static int legendre_mpz(const mpz_t n) {     /* v_p(n!) for an mpz n >= 0 */
    mpz_t q; mpz_init_set(q, n); int e = 0;
    while (mpz_sgn(q) > 0) { mpz_fdiv_q_ui(q, q, P); e += (int)mpz_get_ui(q); }
    mpz_clear(q); return e;
}
static int legendre_u(u64 n) { int e = 0; while (n) { n /= P; e += (int)n; } return e; }

static inline int bit(const u64 *X, u64 i) { return (int)((X[i >> 6] >> (i & 63)) & 1ULL); }
static inline void setb(u64 *X, u64 i) { X[i >> 6] |= 1ULL << (i & 63); }

/* clear the bits >= F of the last word and the pad words, then write the cyclic pad:
   bit F + i := bit (i mod F) for 0 <= i < 128 */
static void make_pad(u64 *X) {
    unsigned f = (unsigned)(F & 63);
    if (f) X[NW - 1] &= (1ULL << f) - 1;
    X[NW] = X[NW + 1] = X[NW + 2] = 0;
    for (u64 i = 0; i < 128; i++) if (bit(X, i % F)) setb(X, F + i);
}

/* out[j] = in[j] | (64 source bits starting at bit s0 + 64 (j - j0)), j in [j0, j1); returns popcount */
static u64 run_or(u64 *restrict out, const u64 *restrict in, u64 j0, u64 j1, u64 s0) {
    u64 cnt = 0, q = s0 >> 6; unsigned o = (unsigned)(s0 & 63);
    const u64 *src = in + q;
    if (o == 0) {
        for (u64 j = j0; j < j1; j++) { u64 v = in[j] | src[j - j0]; out[j] = v; cnt += (u64)__builtin_popcountll(v); }
    } else {
        unsigned oo = 64 - o;
        for (u64 j = j0; j < j1; j++) {
            u64 v = in[j] | (src[j - j0] >> o) | (src[j - j0 + 1] << oo);
            out[j] = v; cnt += (u64)__builtin_popcountll(v);
        }
    }
    return cnt;
}
/* out = in | rot(in, w), 0 < w < F; in must carry a valid pad; returns popcount of out over [0,F) */
static u64 or_rot(u64 *out, const u64 *in, u64 w) {
    u64 j1 = (w + 63) >> 6; if (j1 > NW) j1 = NW;
    u64 cnt = 0;
    cnt += run_or(out, in, 0, j1, F - w);            /* 64 j < w: source starts at 64 j - w + F */
    if (j1 < NW) cnt += run_or(out, in, j1, NW, 64 * j1 - w);
    unsigned f = (unsigned)(F & 63);
    if (f) { cnt -= (u64)__builtin_popcountll(out[NW - 1]); out[NW - 1] &= (1ULL << f) - 1; cnt += (u64)__builtin_popcountll(out[NW - 1]); }
    make_pad(out);
    return cnt;
}

/* complement step: Z (sorted, n entries) -> Z intersect (Z + w mod F); returns new size (result in za) */
static size_t z_step(size_t n, u64 w) {
    /* zb = sorted (Z + w) mod F : entries z >= F - w wrap and come first */
    size_t a = 0, lo = 0, hi = n;
    while (lo < hi) { size_t mid = (lo + hi) / 2; if (za[mid] >= F - w) hi = mid; else lo = mid + 1; }
    a = lo;
    size_t m = 0;
    for (size_t i = a; i < n; i++) zb[m++] = za[i] + w - F;
    for (size_t i = 0; i < a; i++) zb[m++] = za[i] + w;
    size_t i = 0, j = 0, r = 0;
    while (i < n && j < n) {
        if (za[i] < zb[j]) i++;
        else if (za[i] > zb[j]) j++;
        else { zc[r++] = za[i]; i++; j++; }
    }
    memcpy(za, zc, r * sizeof(u64));
    return r;
}

/* one fibre r: B list in lst[0..m); U elements uw[0..nu).  Returns exact number of missed z in Z/F. */
static u64 fibre(u64 r, size_t m, const u64 *uw, int nu, int *phase_out) {
    int u = 0;
    /* (a) list phase */
    while (u < nu && 2 * m <= LISTMAX) {
        u64 w = uw[u++];
        for (size_t i = 0; i < m; i++) { u64 z = lst[i] + w; if (z >= F) z -= F; lst[m + i] = z; }
        m *= 2;
    }
    /* (b) bitset phase */
    memset(bx, 0, (NW + 3) * sizeof(u64));
    for (size_t i = 0; i < m; i++) setb(bx, lst[i]);          /* entries are < F: no bit >= F is set */
    u64 cnt = 0; for (size_t j = 0; j < NW; j++) cnt += (u64)__builtin_popcountll(bx[j]);   /* count before padding */
    make_pad(bx);
    u64 *cur = bx, *nxt = by;
    int phase = 1;
    while (u < nu && cnt < F && F - cnt > ZMAX) {
        u64 w = uw[u++];
        if (w == 0) continue;
        cnt = or_rot(nxt, cur, w);
        u64 *tmp = cur; cur = nxt; nxt = tmp;
    }
    u64 missing = F - cnt;
    if (missing > 0 && (u < nu || dump_left > 0) && missing <= ZCAP) {
        /* (c) complement phase */
        phase = 2;
        size_t n = 0;
        for (u64 j = 0; j < NW; j++) {
            u64 v = ~cur[j];
            while (v) { u64 x = 64 * j + (u64)__builtin_ctzll(v); v &= v - 1; if (x < F) za[n++] = x; }
        }
        if (n != missing) { fprintf(stderr, "covfast: complement extraction mismatch %zu vs %llu\n", n, (unsigned long long)missing); exit(4); }
        while (u < nu && n > 0) { u64 w = uw[u++]; if (w) n = z_step(n, w); }
        missing = n;
        for (size_t i = 0; i < n && dump_left > 0; i++, dump_left--)
            printf("    MISS x=%llu (fibre r=%llu z=%llu)\n", (unsigned long long)(r + PK * za[i]), (unsigned long long)r, (unsigned long long)za[i]);
    } else if (missing > 0 && u < nu) {
        fprintf(stderr, "covfast: complement buffer too small\n"); exit(4);
    }
    if (cur != bx) { u64 *tmp = bx; bx = by; by = tmp; }
    *phase_out = phase;
    return missing;
}

static u64 check(u64 K) {
    /* exact elements */
    mpz_t Ns, N1, prod, tmp, qz; mpz_inits(Ns, N1, prod, tmp, qz, NULL);
    mpz_ui_pow_ui(Ns, P, (unsigned long)T); mpz_mul_ui(Ns, Ns, K);
    mpz_sub_ui(N1, Ns, (unsigned long)H);
    if (mpz_sgn(N1) < 0) { fprintf(stderr, "covfast: N* < H\n"); exit(2); }
    int Mpos = legendre_mpz(Ns) - legendre_mpz(N1);
    if (Mpos != M) { fprintf(stderr, "covfast: M mismatch (Legendre at the position %d vs t+c %d)\n", Mpos, M); exit(3); }
    mpz_set_ui(qz, Q);
    u64 *y = malloc(sizeof(u64) * H); int *v = malloc(sizeof(int) * H);
    mpz_set_ui(prod, 1);
    for (int i = 0; i < H; i++) {
        if (i > 0) { mpz_add_ui(tmp, N1, (unsigned long)i); mpz_mul(prod, prod, tmp); }
        mpz_set(tmp, prod);
        mpz_t pp; mpz_init_set_ui(pp, P);
        int e = (int)mpz_remove(tmp, tmp, pp);
        mpz_clear(pp);
        int expect = legendre_u((u64)(H - 1)) - legendre_u((u64)(H - 1 - i));
        if (e != expect) { fprintf(stderr, "covfast: valuation mismatch i=%d %d vs %d\n", i, e, expect); exit(3); }
        if (e >= M) { fprintf(stderr, "covfast: element vanishes mod Q\n"); exit(3); }
        mpz_mod(tmp, prod, qz);
        y[i] = mpz_get_ui(tmp); v[i] = e;
    }
    mpz_clears(Ns, N1, prod, tmp, qz, NULL);
    /* split */
    u64 *lo = malloc(sizeof(u64) * H), *uw = malloc(sizeof(u64) * H);
    int nl = 0, nu = 0;
    for (int i = 0; i < H; i++) {
        if (v[i] < KF) lo[nl++] = y[i];
        else { if (y[i] % PK) { fprintf(stderr, "covfast: U element not divisible by p^k\n"); exit(3); } uw[nu++] = (y[i] / PK) % F; }
    }
    if (nl > 26) { fprintf(stderr, "covfast: |L| = %d > 26; raise k\n", nl); exit(2); }
    /* all subset sums of L, counting-sorted by residue mod p^k */
    size_t NS = (size_t)1 << nl;
    u64 *sums = malloc(sizeof(u64) * NS), *srt = malloc(sizeof(u64) * NS);
    if (!sums || !srt) { fprintf(stderr, "covfast: alloc sums\n"); exit(2); }
    sums[0] = 0;
    for (int j = 0; j < nl; j++) {
        size_t h = (size_t)1 << j;
        for (size_t a = 0; a < h; a++) { u64 s = sums[a] + lo[j]; if (s >= Q) s -= Q; sums[h + a] = s; }
    }
    size_t *start = calloc(PK + 1, sizeof(size_t));
    for (size_t a = 0; a < NS; a++) start[sums[a] % PK + 1]++;
    for (u64 r = 0; r < PK; r++) start[r + 1] += start[r];
    {
        size_t *fill = malloc(sizeof(size_t) * PK); memcpy(fill, start, sizeof(size_t) * PK);
        for (size_t a = 0; a < NS; a++) srt[fill[sums[a] % PK]++] = sums[a];
        free(fill);
    }
    free(sums);
    u64 total = 0; long nbit = 0, ncomp = 0;
    for (u64 r = 0; r < PK; r++) {
        size_t m = start[r + 1] - start[r];
        if (m == 0) { total += F; continue; }          /* empty fibre: every residue of it is missed */
        if (m > LISTMAX) {
            /* initial list too large for the buffer: grow the buffer */
            free(lst); LISTMAX = m; lst = malloc(sizeof(u64) * 2 * LISTMAX);
            if (!lst) { fprintf(stderr, "covfast: alloc list\n"); exit(2); }
        }
        for (size_t a = 0; a < m; a++) lst[a] = (srt[start[r] + a] - r) / PK;
        int ph;
        total += fibre(r, m, uw, nu, &ph);
        if (ph == 1) nbit++; else ncomp++;
    }
    free(srt); free(start); free(lo); free(uw); free(y); free(v);
    if (getenv("COVFAST_VERBOSE")) printf("    (fibres ending in bitset phase %ld, complement phase %ld)\n", nbit, ncomp);
    return total;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: covfast p t H k pos K... | cls LIFT [nsplit split]\n"); return 1; }
    P = strtoull(argv[1], 0, 10); T = atoi(argv[2]); H = atoi(argv[3]); KF = atoi(argv[4]);
    const char *mode = argv[5];
    if (P < 2 || T < 1 || H < 1) { fprintf(stderr, "bad arguments\n"); return 1; }
    C = legendre_u((u64)(H - 1)); M = T + C;
    if (KF < 0 || KF > M) { fprintf(stderr, "bad k\n"); return 1; }
    Q = powu(P, M); PK = powu(P, KF); F = Q / PK;
    if ((u64)H > powu(P, T)) { fprintf(stderr, "H > p^t\n"); return 1; }
    if (PK > ((u64)1 << 28)) { fprintf(stderr, "p^k too large\n"); return 1; }
    NW = (size_t)((F + 63) / 64);
    LISTMAX = getenv("COVFAST_LISTMAX") ? (size_t)strtoull(getenv("COVFAST_LISTMAX"), 0, 10) : ((size_t)1 << 24);
    if (LISTMAX < 1) LISTMAX = 1;
    ZMAX = getenv("COVFAST_ZMAX") ? strtoull(getenv("COVFAST_ZMAX"), 0, 10) : ((u64)1 << 22);
    ZCAP = (size_t)(ZMAX < F ? ZMAX : F);
    dump_left = 0;
    long dump = getenv("COVFAST_DUMP") ? atol(getenv("COVFAST_DUMP")) : 0;
    if (dump > 0 && (size_t)F > ZCAP) ZCAP = ZCAP < ((size_t)1 << 22) ? ((size_t)1 << 22) : ZCAP;
    if (ZCAP > F) ZCAP = (size_t)F;
    int stop = getenv("COVFAST_STOP") != NULL;
    bx = aligned_alloc(64, ((NW + 3) * 8 + 63) / 64 * 64);
    by = aligned_alloc(64, ((NW + 3) * 8 + 63) / 64 * 64);
    lst = malloc(sizeof(u64) * 2 * LISTMAX);
    za = malloc(sizeof(u64) * (ZCAP + 1)); zb = malloc(sizeof(u64) * (ZCAP + 1)); zc = malloc(sizeof(u64) * (ZCAP + 1));
    if (!bx || !by || !lst || !za || !zb || !zc) { fprintf(stderr, "covfast: alloc failed\n"); return 2; }
    printf("# covfast(D) p=%llu t=%d H=%d c=%d M=%d k=%d Q=%llu F=%llu bits (%zu MB x2) LISTMAX=%zu ZMAX=%llu\n",
           (unsigned long long)P, T, H, C, M, KF, (unsigned long long)Q, (unsigned long long)F, (NW * 8) >> 20,
           LISTMAX, (unsigned long long)ZMAX);
    fflush(stdout);
    u64 *Ks = NULL; size_t nK = 0, cap = 0;
#define ADDK(x) do { if (nK == cap) { cap = cap ? 2 * cap : 256; Ks = realloc(Ks, cap * sizeof(u64)); } Ks[nK++] = (x); } while (0)
    if (!strcmp(mode, "pos")) {
        for (int a = 6; a < argc; a++) ADDK(strtoull(argv[a], 0, 10));
    } else if (!strcmp(mode, "cls")) {
        if (argc < 7) { fprintf(stderr, "cls needs LIFT\n"); return 1; }
        u64 lift = strtoull(argv[6], 0, 10);
        int nsplit = argc > 7 ? atoi(argv[7]) : 1, split = argc > 8 ? atoi(argv[8]) : 0;
        u64 pc = powu(P, C); size_t idx = 0;
        if (C == 0) { if (split == 0) ADDK(1 + lift); }
        else for (u64 Kp = 1; Kp < pc; Kp++) { if (Kp % P == 0) continue; if ((int)(idx++ % nsplit) == split) ADDK(Kp + lift * pc); }
    } else { fprintf(stderr, "bad mode\n"); return 1; }
    size_t nbad = 0; u64 worst = 0; double t0 = wall();
    for (size_t q = 0; q < nK; q++) {
        u64 K = Ks[q];
        if (K % P == 0) { printf("D skip K=%llu (divisible by p)\n", (unsigned long long)K); continue; }
        double t1 = wall();
        dump_left = dump;
        u64 miss = check(K);
        printf("D p=%llu t=%d H=%d c=%d M=%d k=%d K=%llu Kmodpc=%llu missing=%llu %s [%.2fs]\n", (unsigned long long)P, T, H, C, M, KF,
               (unsigned long long)K, (unsigned long long)(C ? K % powu(P, C) : 0), (unsigned long long)miss,
               miss ? "NOT_COVERED" : "COVERED", wall() - t1);
        fflush(stdout);
        if (miss) { nbad++; if (miss > worst) worst = miss; if (stop) break; }
    }
    printf("SUMMARY D p=%llu t=%d H=%d c=%d M=%d k=%d mode=%s nK=%zu fail=%zu worst_missing=%llu %s total=%.1fs\n",
           (unsigned long long)P, T, H, C, M, KF, mode, nK, nbad, (unsigned long long)worst,
           nbad ? "SOME_NOT_COVERED" : "ALL_COVERED", wall() - t0);
    return 0;
}
