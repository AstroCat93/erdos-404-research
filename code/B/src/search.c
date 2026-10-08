/*
 * search.c -- witness builder for  f(a,p) >= K  (Erdos #404).
 *
 * Builds an explicit finite set A, min A = a, with  sum_{n in A} n! == 0 (mod p^K).
 * The output witness is checked afterwards by an INDEPENDENT verifier (verify_bin.c / verify.py);
 * nothing produced here is trusted on its own.
 *
 * Arithmetic: numbers mod p^(WD*L) stored as little-endian limbs in base BASE = p^WD < 2^32,
 * so p-adic digits can be read directly.  S = running sum, F = running factorial n!.
 *
 * Block structure: block m = {pm, ..., pm+p-1}.  v(n) := v_p(n!) is constant on a block.
 * After block m the partial sum must be == 0 mod p^{min(K, v(p(m+1)))}  (exact necessary condition:
 * every later factorial is divisible by that power).
 *
 * Planner: from block m0 (V0 = v(p m0)), work with W-digit windows  x = n!/p^V0 mod p^W  and
 * c = S/p^V0 mod p^W  (exact integers mod p^W).  DFS over subsets R of each block, using
 * precomputed "digit chunks" so that only valid R are visited, until a horizon of H blocks.
 * Commit the first C blocks at full precision, re-plan.  Checkpoints allow backtracking.
 *
 * Compile: clang -O3 -DPP=3 -o search3 search.c
 * Usage:   ./search3 a K outfile [Hmax] [C] [WLuse]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#ifndef PP
#error "define PP"
#endif
#define P PP
#if P == 2
#define WD 31
#define BASE 2147483648ULL
#elif P == 3
#define WD 20
#define BASE 3486784401ULL
#elif P == 5
#define WD 13
#define BASE 1220703125ULL
#elif P == 7
#define WD 11
#define BASE 1977326743ULL
#elif P == 11
#define WD 9
#define BASE 2357947691ULL
#elif P == 13
#define WD 8
#define BASE 815730721ULL
#else
#error "unsupported P"
#endif

#define WL 8              /* max window limbs */
#define W (WL * WD)       /* window digits (max) */
#define HMAXCAP 160
#define NSUB (1u << P)

typedef struct { uint32_t d[WL]; } win;

static uint64_t pw[64];   /* p^k, k < 40 or so (fits) */
static int K, L;          /* target exponent, limbs */
static long long a_start;
static int WLU = WL;      /* window limbs actually used */

static int vfact(long long n) { int s = 0; while (n) { n /= P; s += (int)n; } return s; }

/* ---------------- full precision ---------------- */
static void full_mul(uint32_t *X, int lo, uint64_t t) {
    uint64_t carry = 0;
    for (int i = lo; i < L; i++) {
        uint64_t cur = (uint64_t)X[i] * t + carry;
        X[i] = (uint32_t)(cur % BASE);
        carry = cur / BASE;
    }
}
static void full_add(uint32_t *X, const uint32_t *Y, int lo) {
    uint64_t carry = 0;
    for (int i = lo; i < L; i++) {
        uint64_t cur = (uint64_t)X[i] + Y[i] + carry;
        if (cur >= BASE) { X[i] = (uint32_t)(cur - BASE); carry = 1; }
        else { X[i] = (uint32_t)cur; carry = 0; }
    }
}
/* digit extraction helpers */
static uint32_t full_digitword(const uint32_t *X, int q) { return (q >= 0 && q < L) ? X[q] : 0; }
static win full_extract(const uint32_t *X, int pos) {
    win w; int q = pos / WD, r = pos % WD;
    uint64_t lowdiv = pw[r], hip = pw[WD - r];
    for (int i = 0; i < WL; i++) {
        uint64_t lo = full_digitword(X, q + i) / lowdiv;
        uint64_t hi = (r == 0) ? 0 : (full_digitword(X, q + i + 1) % lowdiv) * hip;
        w.d[i] = (uint32_t)(lo + hi);   /* < p^(WD-r) + (p^r-1) p^(WD-r) = p^WD */
    }
    return w;
}
/* check digits [lo, hi) of X are all zero */
static int full_zero_digits(const uint32_t *X, int lo, int hi) {
    for (int pos = lo; pos < hi; ) {
        int q = pos / WD, r = pos % WD;
        int take = WD - r; if (pos + take > hi) take = hi - pos;
        uint64_t v = (uint64_t)X[q] / pw[r] % pw[take];
        if (v) return 0;
        pos += take;
    }
    return 1;
}

/* ---------------- window arithmetic (mod p^(WD*WLU)) ---------------- */
static inline void win_mul(win *x, uint64_t t) {
    uint64_t carry = 0;
    for (int i = 0; i < WLU; i++) {
        uint64_t cur = (uint64_t)x->d[i] * t + carry;
        x->d[i] = (uint32_t)(cur % BASE);
        carry = cur / BASE;
    }
}
static inline void win_add(win *x, const win *y) {
    uint64_t carry = 0;
    for (int i = 0; i < WLU; i++) {
        uint64_t cur = (uint64_t)x->d[i] + y->d[i] + carry;
        if (cur >= BASE) { x->d[i] = (uint32_t)(cur - BASE); carry = 1; }
        else { x->d[i] = (uint32_t)cur; carry = 0; }
    }
}
/* floor(x / p^pos) mod p^e, requires e <= 30-ish and p^e < 2^63 */
static inline uint64_t win_chunk(const win *x, int pos, int e) {
    uint64_t mod = pw[e];
    unsigned __int128 res = 0, mult = 1;
    int q = pos / WD, r = pos % WD;
    int got = 0;  /* digits gathered */
    /* first partial limb */
    uint64_t v = x->d[q] / pw[r];
    int avail = WD - r;
    res = v % mod; mult = pw[avail < e ? avail : e]; got = avail;
    q++;
    while (got < e && q < WLU) {
        int take = (e - got) < WD ? (e - got) : WD;
        uint64_t part = x->d[q] % pw[take];
        res = (res + (unsigned __int128)part * mult) % mod;
        got += WD;
        if (got < e) mult = (mult * pw[WD]) % mod;
        q++;
    }
    return (uint64_t)(res % mod);
}

/* ---------------- planner ---------------- */
typedef struct {
    long long m;
    int pos, e;
    uint64_t mod;           /* p^e */
    int lo_r, must_r;       /* allowed r >= lo_r ; must include must_r (or -1) */
    win x[P];               /* element windows */
    uint64_t chunk[P];
    /* candidates sorted by d */
    int ncand;
    uint64_t *d;            /* NSUB */
    uint32_t *mask;         /* NSUB */
} blockinfo;
#define CR 512
typedef struct { long long m; int ncand; uint64_t chunkcheck[P]; uint64_t *d; uint32_t *mask; } candcache;
static candcache CC[CR];

static blockinfo BI[HMAXCAP];
static long long mstart, mend;      /* first block, end block (exclusive) */
static long long dfs_nodes;
static long long total_nodes = 0;

static uint64_t rng_state;
static uint64_t splitmix(uint64_t *s) {
    uint64_t z = (*s += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

static int cmp_u64pair(const void *A, const void *Bv) {
    const uint64_t *x = A, *y = Bv;
    return (x[0] > y[0]) - (x[0] < y[0]);
}
static uint64_t pairbuf[2 * NSUB];

static uint32_t cnt_buf[(1 << 15) + 1];
static uint64_t dsum_buf[NSUB];
static void build_candidates(blockinfo *bi) {
    uint64_t mod = bi->mod;
    /* Gray-code enumeration of all subset sums of chunk[] mod p^e */
    dsum_buf[0] = 0;
    uint64_t s = 0; uint32_t g = 0;
    for (uint32_t i = 1; i < NSUB; i++) {
        int bit = __builtin_ctz(i);
        uint32_t ng = g ^ (1u << bit);
        if (ng >> bit & 1) { s += bi->chunk[bit]; if (s >= mod) s -= mod; }
        else { s = s + mod - bi->chunk[bit]; if (s >= mod) s -= mod; }
        g = ng; dsum_buf[g] = s;
    }
    int n = 0;
    if (mod <= (1u << 15)) {
        memset(cnt_buf, 0, (mod + 1) * sizeof(uint32_t));
        for (uint32_t R = 0; R < NSUB; R++) {
            if (bi->lo_r > 0 && (R & ((1u << bi->lo_r) - 1))) continue;
            if (bi->must_r >= 0 && !(R >> bi->must_r & 1)) continue;
            cnt_buf[dsum_buf[R] + 1]++; n++;
        }
        for (uint64_t i = 1; i <= mod; i++) cnt_buf[i] += cnt_buf[i - 1];
        for (uint32_t R = 0; R < NSUB; R++) {
            if (bi->lo_r > 0 && (R & ((1u << bi->lo_r) - 1))) continue;
            if (bi->must_r >= 0 && !(R >> bi->must_r & 1)) continue;
            uint32_t k = cnt_buf[dsum_buf[R]]++;
            bi->d[k] = dsum_buf[R]; bi->mask[k] = R;
        }
    } else {
        for (uint32_t R = 0; R < NSUB; R++) {
            if (bi->lo_r > 0 && (R & ((1u << bi->lo_r) - 1))) continue;
            if (bi->must_r >= 0 && !(R >> bi->must_r & 1)) continue;
            pairbuf[2 * n] = dsum_buf[R]; pairbuf[2 * n + 1] = R; n++;
        }
        qsort(pairbuf, n, 2 * sizeof(uint64_t), cmp_u64pair);
        for (int i = 0; i < n; i++) { bi->d[i] = pairbuf[2 * i]; bi->mask[i] = (uint32_t)pairbuf[2 * i + 1]; }
    }
    bi->ncand = n;
}
/* range of candidates with d == target */
static void cand_range(const blockinfo *bi, uint64_t target, int *lo, int *hi) {
    int l = 0, h = bi->ncand;
    while (l < h) { int mid = (l + h) / 2; if (bi->d[mid] < target) l = mid + 1; else h = mid; }
    int s = l; h = bi->ncand;
    while (l < h) { int mid = (l + h) / 2; if (bi->d[mid] <= target) l = mid + 1; else h = mid; }
    *lo = s; *hi = l;
}

/* DFS state */
static win cstack[HMAXCAP + 1];
static int lostack[HMAXCAP], histack[HMAXCAP], idxstack[HMAXCAP], offstack[HMAXCAP];
static uint32_t path[HMAXCAP];

/* returns 1 on success (path[0..H-1] filled), 0 on exhaustion, -1 on budget */
static int dfs(int H, const win *c0, long long budget, uint64_t seed) {
    int b = 0;
    cstack[0] = *c0;
    /* enter node 0 */
    for (;;) {
        if (b == H) return 1;
        /* compute candidate range for node b (first visit) */
        blockinfo *bi = &BI[b];
        uint64_t ch = win_chunk(&cstack[b], bi->pos, bi->e);
        uint64_t target = (bi->mod - ch) % bi->mod;
        int lo, hi; cand_range(bi, target, &lo, &hi);
        lostack[b] = lo; histack[b] = hi; idxstack[b] = 0;
        int cnt = hi - lo;
        offstack[b] = (seed && cnt > 1) ? (int)(splitmix(&rng_state) % (uint64_t)cnt) : 0;
        /* try next candidate at level b, backtracking as needed */
        for (;;) {
            if (idxstack[b] < histack[b] - lostack[b]) {
                int cntb = histack[b] - lostack[b];
                int k = lostack[b] + (idxstack[b] + offstack[b]) % cntb;
                idxstack[b]++;
                uint32_t R = BI[b].mask[k];
                path[b] = R;
                cstack[b + 1] = cstack[b];
                for (int r = 0; r < P; r++) if (R >> r & 1) win_add(&cstack[b + 1], &BI[b].x[r]);
                dfs_nodes++;
                if (dfs_nodes > budget) return -1;
                b++;
                break;   /* go initialize level b */
            } else {
                if (b == 0) return 0;
                b--;
            }
        }
    }
}

/* ---------------- main driver ---------------- */
typedef struct {
    long long m0; uint32_t *S, *F; long long witlen; int attempt;
} ckpt;

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s a K outfile [Hmax] [C] [WLuse] [budget]\n", argv[0]); return 1; }
    a_start = atoll(argv[1]); K = atoi(argv[2]); const char *out = argv[3];
    int Hmax = argc > 4 ? atoi(argv[4]) : 96;
    int Ccommit = argc > 5 ? atoi(argv[5]) : 12;
    if (argc > 6) WLU = atoi(argv[6]);
    long long budget = argc > 7 ? atoll(argv[7]) : 20000000LL;
    long long maxfail = argc > 8 ? atoll(argv[8]) : 2000LL;
    if (Hmax > HMAXCAP) Hmax = HMAXCAP;
    if (WLU > WL) WLU = WL;
    int Wuse = WLU * WD;
    pw[0] = 1; for (int i = 1; i < 64; i++) pw[i] = (pw[i - 1] != 0 && pw[i - 1] <= (uint64_t)(INT64_MAX / P)) ? pw[i - 1] * P : 0;
    for (int i = 0; i < CR; i++) { CC[i].m = -1; CC[i].d = malloc(NSUB * 8); CC[i].mask = malloc(NSUB * 4); }
    L = K / WD + 2;
    uint32_t *S = calloc(L, 4), *F = calloc(L, 4);
    mstart = a_start / P;
    mend = 0; while (vfact(P * mend) < K) mend++;   /* first block boundary with v >= K */
    /* F = (P*mstart)! */
    F[0] = 1;
    for (long long n = 2; n <= P * mstart; n++) full_mul(F, vfact(n - 1) / WD, (uint64_t)n);
    long long wcap = 1 << 20, witlen = 0;
    long long *wit = malloc(wcap * sizeof(long long));
    /* checkpoints */
    int NCK = 24; ckpt *ck = calloc(NCK, sizeof(ckpt));
    for (int i = 0; i < NCK; i++) { ck[i].S = malloc(L * 4); ck[i].F = malloc(L * 4); }
    int cktop = 0;  /* number of valid checkpoints in ring (stack semantics) */
    long long m0 = mstart;
    int attempt = 0;
    long long nplans = 0, nfail = 0, nbacktrack = 0;
    long long deep_stats[40] = {0};
    long long slack_hist[40][4]; memset(slack_hist, 0, sizeof slack_hist); /* [t][0]=#blocks with 1 valid R, [1]=2-3, [2]=4+, [3]=sum valid */
    long long maxnodes_t[40] = {0};
    clock_t t0 = clock();
    FILE *log = stderr;
    rng_state = 12345;
    while (m0 < mend) {
        /* push checkpoint */
        if (cktop == NCK) { /* drop oldest */
            ckpt tmp = ck[0]; memmove(ck, ck + 1, (NCK - 1) * sizeof(ckpt)); ck[NCK - 1] = tmp; cktop--;
        }
        ck[cktop].m0 = m0; memcpy(ck[cktop].S, S, L * 4); memcpy(ck[cktop].F, F, L * 4);
        ck[cktop].witlen = witlen; ck[cktop].attempt = attempt; cktop++;
    replan:;
        int V0 = vfact(P * m0);
        int chk_lo = V0 - 3 * WD; if (chk_lo < 0) chk_lo = 0;
        if (!full_zero_digits(S, chk_lo, V0 < K ? V0 : K)) { fprintf(stderr, "INVARIANT FAIL S at m0=%lld\n", m0); return 2; }
        win c = full_extract(S, V0), u = full_extract(F, V0);
        /* horizon */
        int H = 0;
        while (H < Hmax && m0 + H < mend) {
            int vend = vfact(P * (m0 + H + 1)); if (vend > K) vend = K;
            if (vend - V0 > Wuse) break;
            H++;
        }
        if (H == 0) { fprintf(stderr, "window too small at m0=%lld\n", m0); return 3; }
        /* element windows */
        win cur = u;
        for (int b = 0; b < H; b++) {
            blockinfo *bi = &BI[b];
            long long m = m0 + b; bi->m = m;
            int vb = vfact(P * m), ve = vfact(P * (m + 1)); if (ve > K) ve = K;
            bi->pos = vb - V0; bi->e = ve - vb; bi->mod = pw[bi->e];
            bi->lo_r = (m == mstart) ? (int)(a_start - P * mstart) : 0;
            bi->must_r = (m == mstart) ? (int)(a_start - P * mstart) : -1;
            for (int r = 0; r < P; r++) {
                long long n = P * m + r;
                if (!(b == 0 && r == 0)) win_mul(&cur, (uint64_t)n);
                bi->x[r] = cur;
                bi->chunk[r] = bi->e > 0 ? win_chunk(&cur, bi->pos, bi->e) : 0;
            }
            if (bi->e == 0) { bi->mod = 1; }
            candcache *cc = &CC[m % CR];
            if (cc->m == m && memcmp(cc->chunkcheck, bi->chunk, sizeof(bi->chunk)) == 0) {
                bi->d = cc->d; bi->mask = cc->mask; bi->ncand = cc->ncand;
            } else {
                bi->d = cc->d; bi->mask = cc->mask;
                build_candidates(bi);
                cc->m = m; cc->ncand = bi->ncand; memcpy(cc->chunkcheck, bi->chunk, sizeof(bi->chunk));
            }
        }
        dfs_nodes = 0;
        uint64_t seed = attempt ? (uint64_t)(m0 * 1000003 + attempt) : 0;
        if (seed) rng_state = seed;
        int res = dfs(H, &c, budget, seed);
        total_nodes += dfs_nodes;
        nplans++;
        { int tmax = 0; for (int b = 0; b < H; b++) if (BI[b].e - 1 > tmax) tmax = BI[b].e - 1;
          if (tmax < 40 && dfs_nodes > maxnodes_t[tmax]) maxnodes_t[tmax] = dfs_nodes; }
        if (res != 1) {
            nfail++;
            if (nfail > maxfail) { fprintf(stderr, "FAILED: fail budget exhausted at m0=%lld\n", m0);
                FILE *fo = fopen(out, "w"); fprintf(fo, "# FAILED (budget) a=%lld p=%d K=%d at m0=%lld\n", a_start, P, K, m0); fclose(fo); return 4; }
            /* backtrack: restore previous checkpoint (the one before current), bump its attempt */
            cktop--;  /* discard current */
            if (cktop == 0) { fprintf(stderr, "FAILED: no checkpoint left at m0=%lld (res=%d)\n", m0, res);
                FILE *fo = fopen(out, "w"); fprintf(fo, "# FAILED a=%lld p=%d K=%d at m0=%lld\n", a_start, P, K, m0); fclose(fo); return 4; }
            ckpt *pk = &ck[cktop - 1];
            m0 = pk->m0; memcpy(S, pk->S, L * 4); memcpy(F, pk->F, L * 4); witlen = pk->witlen;
            pk->attempt++; attempt = pk->attempt; nbacktrack++;
            if (attempt > 40) { /* give up on this checkpoint too */
                cktop--;
                if (cktop == 0) { fprintf(stderr, "FAILED deep backtrack at m0=%lld\n", m0);
                    FILE *fo = fopen(out, "w"); fprintf(fo, "# FAILED a=%lld p=%d K=%d at m0=%lld\n", a_start, P, K, m0); fclose(fo); return 4; }
                pk = &ck[cktop - 1];
                m0 = pk->m0; memcpy(S, pk->S, L * 4); memcpy(F, pk->F, L * 4); witlen = pk->witlen;
                pk->attempt++; attempt = pk->attempt;
            }
            goto replan;
        }
        /* commit */
        int C = Ccommit; if (C > H) C = H;
        if (m0 + H >= mend) C = H;   /* final stretch: commit all */
        for (int b = 0; b < C; b++) {
            uint32_t R = path[b];
            long long m = m0 + b;
            if (BI[b].e >= 2) { int t = BI[b].e - 1; if (t < 40) deep_stats[t]++;
                /* count valid R for the committed carry: recompute chunk of committed S at this block */
                int vb = vfact(P * m); win cw = full_extract(S, vb);
                uint64_t ch = win_chunk(&cw, 0, BI[b].e); uint64_t tg = (BI[b].mod - ch) % BI[b].mod;
                int lo2, hi2; cand_range(&BI[b], tg, &lo2, &hi2); int nv = hi2 - lo2;
                if (t < 40) { slack_hist[t][nv <= 1 ? 0 : (nv <= 3 ? 1 : 2)]++; slack_hist[t][3] += nv; } }
            for (int r = 0; r < P; r++) {
                long long n = P * m + r;
                int lo = vfact(n) / WD;
                if (R >> r & 1) {
                    full_add(S, F, lo);
                    if (witlen == wcap) { wcap *= 2; wit = realloc(wit, wcap * sizeof(long long)); }
                    wit[witlen++] = n;
                }
                full_mul(F, lo, (uint64_t)(n + 1));
            }
        }
        int Vn = vfact(P * (m0 + C)); if (Vn > K) Vn = K;
        if (!full_zero_digits(S, V0 < Vn ? V0 : Vn, Vn)) { fprintf(stderr, "COMMIT CHECK FAIL at m0=%lld\n", m0); return 5; }
        m0 += C; attempt = 0;
        if (nplans % 20000 == 0) {
            fprintf(log, "[p=%d] m0=%lld/%lld  v=%d/%d  wit=%lld  plans=%lld fails=%lld nodes=%lld  %.1fs\n",
                    P, m0, mend, Vn, K, witlen, nplans, nfail, total_nodes, (double)(clock() - t0) / CLOCKS_PER_SEC);
        }
    }
    /* final check */
    if (!full_zero_digits(S, 0, K)) { fprintf(stderr, "FINAL CHECK FAIL\n"); return 6; }
    FILE *fo = fopen(out, "w");
    fprintf(fo, "# witness for f(%lld,%d) >= %d ; terms=%lld ; max=%lld ; builder=search.c (internal check passed; verify independently)\n",
            a_start, P, K, witlen, witlen ? wit[witlen - 1] : -1);
    for (long long i = 0; i < witlen; i++) fprintf(fo, "%lld\n", wit[i]);
    fclose(fo);
    fprintf(log, "DONE p=%d a=%lld K=%d terms=%lld max=%lld plans=%lld fails=%lld backtracks=%lld nodes=%lld time=%.1fs\n",
            P, a_start, K, witlen, witlen ? wit[witlen - 1] : -1, nplans, nfail, nbacktrack, total_nodes,
            (double)(clock() - t0) / CLOCKS_PER_SEC);
    fprintf(log, "deep blocks committed (t = v_p(m+1) >= 1):");
    for (int t = 1; t < 40; t++) if (deep_stats[t]) fprintf(log, " t%d:%lld", t, deep_stats[t]);
    fprintf(log, "\n");
    fprintf(log, "per depth t: committed blocks | #with exactly 1 valid R | 2-3 | >=4 | mean valid R | max DFS nodes of a plan whose deepest block has this t\n");
    for (int t = 0; t < 40; t++) if (deep_stats[t] || maxnodes_t[t])
        fprintf(log, "  t=%2d  %8lld  %8lld %8lld %8lld  %7.2f  %lld\n", t, deep_stats[t], slack_hist[t][0], slack_hist[t][1], slack_hist[t][2],
                deep_stats[t] ? (double)slack_hist[t][3] / deep_stats[t] : 0.0, maxnodes_t[t]);
    return 0;
}
