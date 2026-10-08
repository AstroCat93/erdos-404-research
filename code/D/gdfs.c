// Depth-first version of gclass.c: counts |S_k| = #{a mod 2^k : g(a,2) >= k} for k <= K
// without storing the classes.  Work is split into NCH chunks (by index of the classes of S_k0).
// Also records, for classes in S_K, the distribution of v_2(rep+2) (distance to -2).
// Usage: gdfs K CAP k0 chunk nchunks
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
static inline u64 inv64(u64 u) { u64 x = u; for (int i = 0; i < 6; i++) x *= 2 - u * x; return x; }
static inline int ctz64(u64 x) { return __builtin_ctzll(x); }

#define HSZ (1 << 20)
static u64 *bufA, *bufB;
static u64 hkeys[HSZ];
static uint32_t hstamp[HSZ];
static uint32_t curstamp = 0;

static inline int hinsert(u64 k) {
    u64 h = (k * 0x9E3779B97F4A7C15ULL) >> 44;
    while (1) {
        if (hstamp[h] != curstamp) { hstamp[h] = curstamp; hkeys[h] = k; return 1; }
        if (hkeys[h] == k) return 0;
        h = (h + 1) & (HSZ - 1);
    }
}

static int g_capped(u64 a, int M) {
    int r = M; long np = 1; bufA[0] = 0; u64 N = a; int vacc = 0;
    while (1) {
        u64 n1 = N + 1; int t = ctz64(n1); u64 u = n1 >> t; int first = (N == a);
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
            int rn = r - t; u64 maskn = (rn >= 64) ? ~0ULL : ((1ULL << rn) - 1);
            u64 iv = inv64(u); u64 pt = (t == 0) ? 0 : ((1ULL << t) - 1);
            long nn = 0; curstamp++;
            for (long i = 0; i < np; i++) {
                u64 c = bufA[i];
                for (int e = first ? 1 : 0; e <= 1; e++) {
                    u64 x = (c + e) & maskr;
                    if ((x & pt) != 0) continue;
                    u64 nc = ((x >> t) * iv) & maskn;
                    if (hinsert(nc)) bufB[nn++] = nc;
                }
            }
            if (nn == 0) goto death;
            if (nn > (1L << 19)) { fprintf(stderr, "population overflow\n"); exit(1); }
            u64 *tmp = bufA; bufA = bufB; bufB = tmp; np = nn; r = rn; vacc += t; N++;
            continue;
        }
    death:;
        { u64 m2 = (r >= 64) ? ~0ULL : ((1ULL << r) - 1); int best = -1;
          for (long i = 0; i < np; i++) { u64 c = bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { u64 x = (c + e) & m2; int v = x ? ctz64(x) : r; if (v > best) best = v; } }
          return vacc + best; }
    }
}

static int K, CAP;
static long long cnt[70];
static long long distm2[70];  // for classes in S_K: v_2(rep+2) histogram (capped at K)
static long long gexact[70];  // number of computed reps with exact g = j (diagnostic)

static void lift(u64 rep, int g, int k) {
    cnt[k]++;
    if (k == K) { u64 x = (rep + 2) & ((1ULL << K) - 1); int v = x ? ctz64(x) : K; distm2[v]++; return; }
    if (g >= k + 1) lift(rep, g, k + 1);
    u64 r1 = rep + (1ULL << k);
    int g1 = g_capped(r1, CAP);
    if (g1 >= k + 1) lift(r1, g1, k + 1);
}

int main(int argc, char **argv) {
    K = atoi(argv[1]); CAP = atoi(argv[2]); int k0 = atoi(argv[3]); int ch = atoi(argv[4]); int nch = atoi(argv[5]);
    bufA = malloc(sizeof(u64) << 20); bufB = malloc(sizeof(u64) << 20);
    // BFS to level k0
    long ns = 1; u64 *rep = malloc(sizeof(u64)); int *gv = malloc(sizeof(int));
    rep[0] = 1; gv[0] = g_capped(1, CAP);
    for (int k = 0; k < k0; k++) {
        u64 *rep2 = malloc(sizeof(u64) * (2 * ns + 2)); int *gv2 = malloc(sizeof(int) * (2 * ns + 2)); long n2 = 0;
        for (long i = 0; i < ns; i++) {
            if (gv[i] >= k + 1) { rep2[n2] = rep[i]; gv2[n2] = gv[i]; n2++; }
            u64 r1 = rep[i] + (1ULL << k); int g1 = g_capped(r1, CAP);
            if (g1 >= k + 1) { rep2[n2] = r1; gv2[n2] = g1; n2++; }
        }
        free(rep); free(gv); rep = rep2; gv = gv2; ns = n2;
    }
    for (long i = ch; i < ns; i += nch) lift(rep[i], gv[i], k0);
    for (int k = k0; k <= K; k++) printf("k=%d count=%lld\n", k, cnt[k]);
    for (int v = 0; v <= K; v++) if (distm2[v]) printf("dist_to_-2 v=%d count=%lld\n", v, distm2[v]);
    return 0;
}
