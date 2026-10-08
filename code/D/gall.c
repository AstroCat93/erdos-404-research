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

// gall K CAP: exact g(a) (capped) for all a in [1,2^K]; per-shell (v_2(a+2)=j) min g and histogram
int main(int argc, char **argv) {
    int K = atoi(argv[1]), CAP = atoi(argv[2]);
    bufA = malloc(sizeof(u64) << 20); bufB = malloc(sizeof(u64) << 20);
    int ming[70]; long cnt[70]; for (int j = 0; j < 70; j++) { ming[j] = 1000; cnt[j] = 0; }
    long hist[70] = {0};
    for (u64 a = 1; a <= (1ULL << K); a++) {
        int g = g_capped(a, CAP);
        u64 x = (a + 2) & ((1ULL << K) - 1); int j = x ? ctz64(x) : K;
        if (g < ming[j]) ming[j] = g; cnt[j]++;
        hist[g < 69 ? g : 69]++;
    }
    for (int j = 0; j <= K; j++) if (cnt[j]) printf("shell v2(a+2)=%d  n=%ld  min_g=%d\n", j, cnt[j], ming[j]);
    for (int g = 0; g < 70; g++) if (hist[g]) printf("g=%d count=%ld\n", g, hist[g]);
    return 0;
}
