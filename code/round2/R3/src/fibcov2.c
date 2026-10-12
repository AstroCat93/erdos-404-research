/*
 * fibcov2.c -- PROGRAM B (R3-frontier, 2026-10-11).  Independent of fibcov.c (program A) and of
 * the note's cov.c / cov_pos.c / cov_check2.c: different element computation, different
 * decomposition parameter, different enumeration, different shift kernel, different final test.
 *
 * For an ACTUAL position N* = p^t * K (K not divisible by p) and block length H, with N1 = N* - H,
 * the normalised block is { n!/N1! : N1 <= n < N* } (times a unit, irrelevant for coverage), and
 *     e_i := (N1+1)(N1+2)...(N1+i) mod p^M,     M := v_p(N*!) - v_p(N1!)   (Legendre).
 * We decide whether the subset sums of e_0..e_{H-1} cover Z/p^M.
 *
 * Decomposition: choose a level kb.  Elements with v_p(e_i) >= kb are "high"; they are divided by
 * p^kb and act inside each class x == r (mod p^kb).  The low elements' subset sums (all 2^nlow
 * of them, enumerated in Gray-code order) are distributed into the p^kb classes by counting sort.
 * In class r we start with S_r = {(s - r)/p^kb : s low subset sum, s == r} subset Z/p^(M-kb),
 * optionally expand it as an explicit list by the first `sparse` high elements, then turn it into
 * a bitset and do S <- S u (S + h) for the remaining high elements, with an in-place
 * "copy + shift-left-or + shift-right-or" kernel.  Coverage <=> popcount(S_r) = p^(M-kb) for all r.
 *
 * usage:  fibcov2 p t H kb sparse K1 [K2 ...]
 *         fibcov2 p t H kb sparse all LIFT      (all unit classes K' mod p^c, using K = K' + LIFT*p^c)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 U128;
static unsigned long long prime, Qm, pkb, fib;
static size_t nwords;
static uint64_t *S, *Tm;

static int legendre(unsigned long long n, unsigned long long p) { int e = 0; while (n) { n /= p; e += (int)n; } return e; }
static double wall(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + ts.tv_nsec * 1e-9; }

/* S |= (Tm << s) on [s, fib), and S |= (Tm >> (fib-s)) on [0, s): i.e. S |= Tm + s (cyclic mod fib) */
static void shift_or_left(uint64_t *dst, const uint64_t *src, unsigned long long s) {
    /* bits x of src with x + s < fib go to x + s */
    size_t ws = s >> 6; unsigned bs = s & 63;
    if (bs == 0) { for (size_t i = nwords; i-- > ws;) dst[i] |= src[i - ws]; }
    else {
        for (size_t i = nwords - 1; i > ws; i--) dst[i] |= (src[i - ws] << bs) | (src[i - ws - 1] >> (64 - bs));
        dst[ws] |= src[0] << bs;
    }
}
static void shift_or_right(uint64_t *dst, const uint64_t *src, unsigned long long s) {
    /* bits x of src with x >= s go to x - s */
    size_t ws = s >> 6; unsigned bs = s & 63;
    if (bs == 0) { for (size_t i = 0; i + ws < nwords; i++) dst[i] |= src[i + ws]; }
    else {
        for (size_t i = 0; i + ws + 1 < nwords; i++) dst[i] |= (src[i + ws] >> bs) | (src[i + ws + 1] << (64 - bs));
        dst[nwords - 1 - ws] |= src[nwords - 1] >> bs;
    }
}
static void clear_tail(uint64_t *X) { unsigned r = (unsigned)(fib & 63); if (r) X[nwords - 1] &= (1ULL << r) - 1; }

static void add_elem(unsigned long long h) {
    if (h == 0) return;
    /* tail bits beyond fib are zero in S (invariant) so the left shift drops correctly after clear_tail */
    memcpy(Tm, S, nwords * 8);
    shift_or_left(S, Tm, h);          /* x -> x+h for x < fib-h */
    shift_or_right(S, Tm, fib - h);   /* x -> x+h-fib for x >= fib-h */
    clear_tail(S);
}

static int cmpu(const void *a, const void *b) { unsigned long long x = *(const unsigned long long *)a, y = *(const unsigned long long *)b; return x < y ? -1 : x > y; }

/* all 2^n subset sums of el[0..n) mod Q, by Gray code */
static unsigned long long *gray_all(const unsigned long long *el, int n, unsigned long long Q) {
    size_t N = (size_t)1 << n; unsigned long long *out = malloc(8 * N), cur = 0; out[0] = 0;
    for (size_t g = 1; g < N; g++) {
        int bit = __builtin_ctzll((unsigned long long)g);
        if ((g ^ (g >> 1)) & ((size_t)1 << bit)) { cur += el[bit]; if (cur >= Q) cur -= Q; }
        else { cur += Q - el[bit]; if (cur >= Q) cur -= Q; }
        out[g] = cur;
    }
    return out;
}
/* finish one class: starting list lst[0..m) (values in Z/fib), sparse doubling, bitset DP, count */
static unsigned long long finish_class(unsigned long long **plst, size_t *plcap, size_t m, const unsigned long long *hi, int nhi, int sparse) {
    int nsp = sparse < nhi ? sparse : nhi;
    while (nsp > 0 && (m << nsp) > ((size_t)1 << 26)) nsp--;
    size_t need = (m << nsp) + 1;
    if (need > *plcap) { *plcap = need; *plst = realloc(*plst, 8 * need); }
    unsigned long long *lst = *plst; size_t len = m;
    for (int j = 0; j < nsp; j++) {
        unsigned long long h = hi[j] % fib;
        for (size_t q = 0; q < len; q++) { unsigned long long z = lst[q] + h; if (z >= fib) z -= fib; lst[len + q] = z; }
        len *= 2;
    }
    memset(S, 0, nwords * 8);
    for (size_t q = 0; q < len; q++) S[lst[q] >> 6] |= 1ULL << (lst[q] & 63);
    for (int j = nsp; j < nhi; j++) add_elem(hi[j] % fib);
    unsigned long long pc = 0; for (size_t w = 0; w < nwords; w++) pc += (unsigned long long)__builtin_popcountll(S[w]);
    return fib - pc;
}
/* low elements split by layer: G1 = {v < kb-1}, G2 = {v == kb-1} (all of G2 divisible by p^(kb-1)).
   A low subset sum in class r (mod p^kb) is a1 + a2 with a1 in Sigma(G1), a1 == r (mod p^(kb-1)),
   and a2 in Sigma(G2) whose digit kb-1 equals ((r - a1) mod p^kb) / p^(kb-1). */
static unsigned long long run_layer_split(const unsigned long long *lo, const int *vlo, int nlo,
                                          const unsigned long long *hi, int nhi, int kb, int sparse, unsigned long long Q) {
    unsigned long long pk1 = pkb / prime;
    unsigned long long *g1 = malloc(8 * (nlo + 1)), *g2 = malloc(8 * (nlo + 1)); int n1 = 0, n2 = 0;
    for (int i = 0; i < nlo; i++) { if (vlo[i] == kb - 1) g2[n2++] = lo[i]; else g1[n1++] = lo[i]; }
    if (n1 > 30 || n2 > 30) { fprintf(stderr, "layer split too large (%d,%d)\n", n1, n2); exit(5); }
    unsigned long long *s1 = gray_all(g1, n1, Q), *s2 = gray_all(g2, n2, Q);
    size_t N1 = (size_t)1 << n1, N2 = (size_t)1 << n2;
    /* bucket s1 by residue mod pk1 */
    size_t *b1 = calloc(pk1 + 1, sizeof(size_t)); unsigned long long *t1 = malloc(8 * N1);
    for (size_t q = 0; q < N1; q++) b1[s1[q] % pk1 + 1]++;
    for (unsigned long long r = 0; r < pk1; r++) b1[r + 1] += b1[r];
    { size_t *f = malloc(sizeof(size_t) * pk1); memcpy(f, b1, sizeof(size_t) * pk1);
      for (size_t q = 0; q < N1; q++) t1[f[s1[q] % pk1]++] = s1[q]; free(f); }
    /* bucket s2 by digit kb-1 */
    size_t *b2 = calloc(prime + 1, sizeof(size_t)); unsigned long long *t2 = malloc(8 * N2);
    for (size_t q = 0; q < N2; q++) { if (s2[q] % pk1) { fprintf(stderr, "G2 not divisible\n"); exit(5); } b2[(s2[q] / pk1) % prime + 1]++; }
    for (unsigned long long d = 0; d < prime; d++) b2[d + 1] += b2[d];
    { size_t *f = malloc(sizeof(size_t) * prime); memcpy(f, b2, sizeof(size_t) * prime);
      for (size_t q = 0; q < N2; q++) t2[f[(s2[q] / pk1) % prime]++] = s2[q]; free(f); }
    free(s1); free(s2);
    unsigned long long notcov = 0, *lst = NULL; size_t lcap = 0;
    for (unsigned long long r = 0; r < pkb; r++) {
        unsigned long long q1 = r % pk1;
        size_t m = 0;
        for (size_t u = b1[q1]; u < b1[q1 + 1]; u++) m += 0;   /* size computed below */
        /* count */
        for (size_t u = b1[q1]; u < b1[q1 + 1]; u++) {
            unsigned long long a1 = t1[u], d = (((r + pkb - a1 % pkb) % pkb) / pk1) % prime;
            m += b2[d + 1] - b2[d];
        }
        if (m + 1 > lcap) { lcap = m + 1; lst = realloc(lst, 8 * lcap); }
        size_t w = 0;
        for (size_t u = b1[q1]; u < b1[q1 + 1]; u++) {
            unsigned long long a1 = t1[u], d = (((r + pkb - a1 % pkb) % pkb) / pk1) % prime;
            for (size_t v = b2[d]; v < b2[d + 1]; v++) {
                unsigned long long sm = a1 + t2[v]; if (sm >= Q) sm -= Q;
                if (sm % pkb != r) { fprintf(stderr, "class error\n"); exit(5); }
                lst[w++] = (sm - r) / pkb;
            }
        }
        notcov += finish_class(&lst, &lcap, m, hi, nhi, sparse);
    }
    free(lst); free(b1); free(t1); free(b2); free(t2); free(g1); free(g2);
    return notcov;
}

static unsigned long long run_position(int t, int H, int kb, int sparse, unsigned long long K, int *Mout) {
    unsigned long long pt = 1; for (int i = 0; i < t; i++) pt *= prime;
    unsigned long long Nstar = pt * K, N1 = Nstar - (unsigned long long)H;
    int M = legendre(Nstar, prime) - legendre(N1, prime);
    *Mout = M;
    unsigned long long Q = 1; for (int i = 0; i < M; i++) Q *= prime;
    if (Q != Qm) { fprintf(stderr, "M mismatch (M=%d)\n", M); exit(4); }
    unsigned long long *e = malloc(sizeof(unsigned long long) * H);
    e[0] = 1 % Q;
    for (int i = 1; i < H; i++) e[i] = (unsigned long long)(((U128)e[i - 1] * ((N1 + (unsigned long long)i) % Q)) % Q);
    /* split */
    unsigned long long *lo = malloc(8 * H), *hi = malloc(8 * H); int nlo = 0, nhi = 0;
    int *vlo = malloc(sizeof(int) * H);
    for (int i = 0; i < H; i++) {
        unsigned long long z = e[i]; int v = 0;
        if (!z) { fprintf(stderr, "zero element\n"); exit(4); }
        while (z % prime == 0) { z /= prime; v++; }
        if (v >= kb) hi[nhi++] = e[i] / pkb; else { vlo[nlo] = v; lo[nlo++] = e[i]; }
    }
    int use_layer = (nlo > 24) || (getenv("FIBCOV2_LAYER") != NULL);
    if (use_layer && kb >= 1) {
        unsigned long long nc = run_layer_split(lo, vlo, nlo, hi, nhi, kb, sparse, Q);
        free(e); free(lo); free(hi); free(vlo);
        return nc;
    }
    /* low subset sums via Gray code, processed in batches of classes [r0, r1) to bound memory:
       for each batch the 2^nlo sums are enumerated twice (count, then fill). */
    size_t nsum = (size_t)1 << nlo;
    unsigned long long batch = pkb;
    { double per = (double)nsum / (double)pkb * 8.0;             /* bytes per class */
      unsigned long long cap = (unsigned long long)(1.5e9 / (per > 1 ? per : 1));
      if (cap < 1) cap = 1; if (cap < batch) batch = cap;
      if (getenv("FIBCOV2_NBATCH")) { unsigned long long nbt = strtoull(getenv("FIBCOV2_NBATCH"), 0, 10); unsigned long long fb = nbt ? (pkb + nbt - 1) / nbt : pkb; if (fb >= 1 && fb < batch) batch = fb; } }
    unsigned long long notcov = 0;
    unsigned long long *lst = NULL; size_t lcap = 0;
    size_t *cnt = malloc(sizeof(size_t) * (batch + 1));
    size_t *pos = malloc(sizeof(size_t) * batch);
    unsigned long long *byc = NULL; size_t bycap = 0;
    for (unsigned long long r0 = 0; r0 < pkb; r0 += batch) {
        unsigned long long r1 = r0 + batch < pkb ? r0 + batch : pkb, nb = r1 - r0;
        for (int pass = 0; pass < 2; pass++) {
            if (pass == 0) memset(cnt, 0, sizeof(size_t) * (nb + 1));
            unsigned long long cur = 0;
            for (size_t g = 0; g < nsum; g++) {
                if (g) {
                    int bit = __builtin_ctzll((unsigned long long)g);
                    size_t gray = g ^ (g >> 1);
                    if (gray & ((size_t)1 << bit)) { cur += lo[bit]; if (cur >= Q) cur -= Q; }
                    else { cur += Q - lo[bit]; if (cur >= Q) cur -= Q; }
                }
                unsigned long long r = cur % pkb;
                if (r < r0 || r >= r1) continue;
                if (pass == 0) cnt[r - r0 + 1]++;
                else byc[pos[r - r0]++] = (cur - r) / pkb;
            }
            if (pass == 0) {
                for (unsigned long long q = 0; q < nb; q++) cnt[q + 1] += cnt[q];
                if (cnt[nb] > bycap) { bycap = cnt[nb]; byc = realloc(byc, 8 * bycap); }
                memcpy(pos, cnt, sizeof(size_t) * nb);
            }
        }
        for (unsigned long long r = r0; r < r1; r++) {
            size_t base = cnt[r - r0], m = cnt[r - r0 + 1] - cnt[r - r0];
            int nsp = sparse < nhi ? sparse : nhi;
            while (nsp > 0 && (m << nsp) > ((size_t)1 << 26)) nsp--;     /* cap explicit list at 2^26 */
            size_t need = (m << nsp) + 1;
            if (need > lcap) { lcap = need; lst = realloc(lst, 8 * lcap); }
            memcpy(lst, byc + base, 8 * m);
            size_t len = m;
            for (int j = 0; j < nsp; j++) {
                unsigned long long h = hi[j] % fib;
                for (size_t q = 0; q < len; q++) { unsigned long long z = lst[q] + h; if (z >= fib) z -= fib; lst[len + q] = z; }
                len *= 2;
            }
            memset(S, 0, nwords * 8);
            for (size_t q = 0; q < len; q++) S[lst[q] >> 6] |= 1ULL << (lst[q] & 63);
            for (int j = nsp; j < nhi; j++) add_elem(hi[j] % fib);
            unsigned long long pc = 0; for (size_t w = 0; w < nwords; w++) pc += (unsigned long long)__builtin_popcountll(S[w]);
            notcov += fib - pc;
        }
    }
    free(pos); free(byc);
    free(lst); free(cnt); free(e); free(lo); free(hi); free(vlo);
    return notcov;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: %s p t H kb sparse K... | all LIFT\n", argv[0]); return 1; }
    prime = strtoull(argv[1], 0, 10); int t = atoi(argv[2]), H = atoi(argv[3]), kb = atoi(argv[4]), sparse = atoi(argv[5]);
    int c = legendre((unsigned long long)H - 1, prime), M = t + c;
    Qm = 1; for (int i = 0; i < M; i++) Qm *= prime;
    pkb = 1; for (int i = 0; i < kb; i++) pkb *= prime;
    fib = Qm / pkb; nwords = (fib + 63) / 64;
    S = malloc(nwords * 8); Tm = malloc(nwords * 8);
    if (!S || !Tm) { fprintf(stderr, "alloc\n"); return 2; }
    printf("# fibcov2(B) p=%llu t=%d H=%d c=%d M=%d kb=%d sparse=%d fibre=%llu bits\n", prime, t, H, c, M, kb, sparse, fib);
    fflush(stdout);
    unsigned long long *Kl = NULL; size_t nK = 0;
    if (!strcmp(argv[6], "all")) {
        unsigned long long lift = argc > 7 ? strtoull(argv[7], 0, 10) : 0;
        unsigned long long pc = 1; for (int i = 0; i < c; i++) pc *= prime;
        Kl = malloc(8 * (pc + 1));
        if (c == 0) Kl[nK++] = 1 + lift * prime;   /* any K not divisible by p */
        else for (unsigned long long K = 1; K < pc; K++) if (K % prime) Kl[nK++] = K + lift * pc;
        for (size_t q = 0; q < nK; q++) if (Kl[q] % prime == 0) Kl[q] += pc;  /* cannot happen for c>0 */
    } else { Kl = malloc(8 * argc); for (int a = 6; a < argc; a++) Kl[nK++] = strtoull(argv[a], 0, 10); }
    size_t bad = 0; unsigned long long worst = 0; double t0 = wall();
    for (size_t q = 0; q < nK; q++) {
        if (Kl[q] % prime == 0) { printf("K=%llu divisible by p, skipped\n", Kl[q]); continue; }
        double t1 = wall(); int Mx;
        unsigned long long nc = run_position(t, H, kb, sparse, Kl[q], &Mx);
        printf("B p=%llu t=%d H=%d M=%d K=%llu notcovered=%llu %s [%.2fs]\n", prime, t, H, Mx, Kl[q], nc, nc ? "FAIL" : "OK", wall() - t1);
        fflush(stdout);
        if (nc) { bad++; if (nc > worst) worst = nc; }
    }
    printf("SUMMARY B p=%llu t=%d H=%d c=%d M=%d kb=%d n=%zu fail=%zu worst=%llu %s total=%.1fs\n", prime, t, H, c, M, kb, nK, bad, worst,
           bad ? "SOME_FAIL" : "ALL_OK", wall() - t0);
    (void)cmpu;
    return bad ? 3 : 0;
}
