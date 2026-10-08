// Exhaustive residue-class computation of g(a,2) = f(a,2) - v_2(a!) for p = 2.
// Key lemma: "g(a) >= G" depends only on a mod 2^G (a >= 1).
// We build S_k = { a mod 2^k : g(a) >= k } for k = 1..K by lifting, with
// representatives in [1, 2^k].  For every representative we compute g exactly
// (capped at CAP <= 63) with the c-recursion c_{N+1} = (c_N + eps)/(N+1) mod 2^r.
//
// Usage: gclass K CAP [outfile]
// Output: for each k: |S_k|, density |S_k|/2^k, and the histogram of exact g values found.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;

static inline u64 inv64(u64 u) { u64 x = u; for (int i = 0; i < 6; i++) x *= 2 - u * x; return x; }
static inline int ctz64(u64 x) { return __builtin_ctzll(x); }

#define HSZ (1 << 22)
static u64 *bufA, *bufB;
static u64 hkeys[HSZ];
static uint32_t hstamp[HSZ];
static uint32_t curstamp = 0;
static long maxpop = 0;

static inline int hinsert(u64 k) {
    u64 h = (k * 0x9E3779B97F4A7C15ULL) >> 42; // 22 bits
    while (1) {
        if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (hkeys[h] == k) return 0;
        h = (h + 1) & (HSZ - 1);
    }
}

// returns exact g(a) if < M, else M.
static int g_capped(u64 a, int M) {
    int r = M;
    long np = 1; bufA[0] = 0;
    u64 N = a;
    int vacc = 0;
    while (1) {
        u64 n1 = N + 1;
        int t = ctz64(n1);
        u64 u = n1 >> t;
        int first = (N == a);
        u64 maskr = (r >= 64) ? ~0ULL : ((1ULL << r) - 1);
        if (t >= r) {
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                if (((c + 1) & maskr) == 0) return M;
                if (!first && (c & maskr) == 0) return M;
            }
            goto death;
        }
        {
            int rn = r - t;
            u64 maskn = (rn >= 64) ? ~0ULL : ((1ULL << rn) - 1);
            u64 iv = inv64(u);
            u64 pt = (t == 0) ? 0 : ((1ULL << t) - 1);
            long nn = 0;
            curstamp++;
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                for (int e = first ? 1 : 0; e <= 1; e++) {
                    u64 x = (c + e) & maskr;
                    if ((x & pt) != 0) continue;
                    u64 nc = ((x >> t) * iv) & maskn;
                    if (hinsert(nc)) { bufB[nn++] = nc; }
                }
            }
            if (nn == 0) goto death;
            if (nn > maxpop) maxpop = nn;
            if (nn > (1L << 21)) { fprintf(stderr, "population overflow a=%llu\n", (unsigned long long)a); exit(1); }
            u64 *tmp = bufA; bufA = bufB; bufB = tmp; np = nn;
            r = rn; vacc += t; N++;
            continue;
        }
    death:;
        {
            u64 maskr2 = (r >= 64) ? ~0ULL : ((1ULL << r) - 1);
            int best = -1;
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                for (int e = first ? 1 : 0; e <= 1; e++) {
                    u64 x = (c + e) & maskr2;
                    int v = x ? ctz64(x) : r;
                    if (v > best) best = v;
                }
            }
            return vacc + best;
        }
    }
}

int main(int argc, char **argv) {
    int K = atoi(argv[1]);
    int CAP = atoi(argv[2]);
    const char *outf = argc > 3 ? argv[3] : NULL;
    bufA = malloc(sizeof(u64) << 22); bufB = malloc(sizeof(u64) << 22);
    // S_k arrays: rep and g
    long cap = 1L << 20; long ns = 0;
    u64 *rep = malloc(sizeof(u64) * cap); int *gv = malloc(sizeof(int) * cap);
    // k = 1: classes mod 2: reps 1, 2
    long hist[70]; memset(hist, 0, sizeof(hist));
    // level-0: S_0 = {rep 1 (class 0 mod 1)}
    rep[0] = 1; gv[0] = g_capped(1, CAP); ns = 1;
    hist[gv[0] < CAP ? gv[0] : 69]++;
    for (int k = 0; k < K; k++) {
        // lift S_k -> S_{k+1}
        long cap2 = 2 * ns + 16;
        u64 *rep2 = malloc(sizeof(u64) * cap2); int *gv2 = malloc(sizeof(int) * cap2);
        long n2 = 0;
        u64 step = 1ULL << k;
        for (long i = 0; i < ns; i++) {
            u64 r0 = rep[i]; int g0 = gv[i];
            if (g0 >= k + 1) { rep2[n2] = r0; gv2[n2] = g0; n2++; }
            u64 r1 = r0 + step;
            int g1 = g_capped(r1, CAP);
            hist[g1 < CAP ? g1 : 69]++;
            if (g1 >= k + 1) { rep2[n2] = r1; gv2[n2] = g1; n2++; }
        }
        free(rep); free(gv); rep = rep2; gv = gv2; ns = n2;
        printf("k=%d |S_k|=%ld density=%.6f  maxpop=%ld\n", k + 1, ns, (double)ns / (double)(1ULL << (k + 1)), maxpop);
        fflush(stdout);
    }
    // exact distribution: mu(g = j) for j < K computed from classes: we recompute from final reps? use hist of computed reps is biased.
    if (outf) {
        FILE *f = fopen(outf, "w");
        for (long i = 0; i < ns; i++) fprintf(f, "%llu %d\n", (unsigned long long)rep[i], gv[i]);
        fclose(f);
    }
    return 0;
}
