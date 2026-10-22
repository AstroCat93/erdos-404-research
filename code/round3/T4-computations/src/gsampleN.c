// gsampleN.c -- exact decision of g_2(x) >= CAP (and exact g_2(x) when < CAP) for 2-adic x given mod 2^CAP,
// with fixed-width NL*64-bit arithmetic (compile with -DNL=4,9,17,...).  Generalises code/D/gsample256.c
// (track D, round 1): the set of reachable carries gamma_N = (sum_{n in T, n<N} n!)/N!  (mod 2^r) is carried
// forward exactly; gamma_{N+1} = (gamma_N + e_N)/(N+1).  Success when some gamma + e == 0 mod 2^r.
// Modes:
//   gsampleN ns seed CAP [nthreads]      Monte Carlo: ns uniform samples x mod 2^CAP; prints survival counts for k<=CAP.
//   gsampleN 0 0 CAP a1 a2 ...           exact capped g_2(a) for the listed integers.
// Population cap POPLIM; if exceeded the program aborts (reported, never silently truncated).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#ifndef NL
#define NL 4
#endif
typedef uint64_t u64; typedef unsigned __int128 u128;
typedef struct { u64 w[NL]; } U;
#define BITS (64*NL)

static inline U uz(void) { U x; memset(&x, 0, sizeof x); return x; }
static inline U addsmall(U x, u64 e) { for (int i = 0; i < NL && e; i++) { u64 o = x.w[i]; x.w[i] += e; e = (x.w[i] < o); } return x; }
static inline U mask(U x, int r) { for (int i = 0; i < NL; i++) { int lo = 64 * i; if (r <= lo) x.w[i] = 0; else if (r < lo + 64) x.w[i] &= ((1ULL << (r - lo)) - 1); } return x; }
static inline int iszero(U x) { u64 o = 0; for (int i = 0; i < NL; i++) o |= x.w[i]; return !o; }
static inline int ctz(U x) { for (int i = 0; i < NL; i++) if (x.w[i]) return 64 * i + __builtin_ctzll(x.w[i]); return BITS; }
static inline U shr(U x, int t) { U y = uz(); int q = t / 64, s = t % 64;
    for (int i = 0; i + q < NL; i++) { u64 lo = x.w[i + q] >> s; u64 hi = (s && i + q + 1 < NL) ? (x.w[i + q + 1] << (64 - s)) : 0; y.w[i] = lo | hi; } return y; }
// truncated product mod 2^BITS, only limbs below LIM needed
static inline U mul_lim(U a, U b, int lim) { U r = uz(); for (int i = 0; i < lim; i++) { if (!a.w[i]) continue; u128 carry = 0;
        for (int j = 0; i + j < lim; j++) { u128 cur = (u128)a.w[i] * b.w[j] + r.w[i + j] + carry; r.w[i + j] = (u64)cur; carry = cur >> 64; } } return r; }
static inline U sub(U a, U b) { U r; u64 br = 0; for (int i = 0; i < NL; i++) { u64 t = a.w[i] - b.w[i] - br; br = (a.w[i] < b.w[i]) || (a.w[i] - b.w[i] < br); r.w[i] = t; } return r; }
static inline U two(void) { U x = uz(); x.w[0] = 2; return x; }
// inverse of odd u mod 2^(64*lim) by Newton iteration (x <- x(2 - u x)); start x = u (correct mod 8); precision doubles each step
static U inv_lim(U u, int lim) { U x = u; int prec = 3; while (prec < 64 * lim) { x = mul_lim(x, sub(two(), mul_lim(u, x, lim)), lim); prec *= 2; } return x; }
static inline int eq(U a, U b) { for (int i = 0; i < NL; i++) if (a.w[i] != b.w[i]) return 0; return 1; }

#define HBITS 21
#define HSZ (1UL << HBITS)
typedef struct { U *hkeys; uint32_t *hstamp; uint32_t curstamp; U *bufA, *bufB; long maxpop; } ctx_t;
static long POPLIM = 1L << 20;

static inline int hinsert(ctx_t *C, U k) {
    u64 h = 0; for (int i = 0; i < NL; i++) h ^= k.w[i] * (0x9E3779B97F4A7C15ULL + 2 * (u64)i); h *= 0x9E3779B97F4A7C15ULL; h >>= (64 - HBITS);
    while (1) { if (C->hstamp[h] != C->curstamp) { C->hstamp[h] = C->curstamp; C->hkeys[h] = k; return 1; }
        if (eq(C->hkeys[h], k)) return 0; h = (h + 1) & (HSZ - 1); }
}
static void ctx_init(ctx_t *C) { C->hkeys = malloc(sizeof(U) * HSZ); C->hstamp = calloc(HSZ, 4); C->curstamp = 0; C->bufA = malloc(sizeof(U) * POPLIM); C->bufB = malloc(sizeof(U) * POPLIM); C->maxpop = 0;
    if (!C->hkeys || !C->hstamp || !C->bufA || !C->bufB) { fprintf(stderr, "oom\n"); exit(1); } }

// returns min(g_2(a), M) exactly
static int g_capped(ctx_t *C, U a, int M) {
    int r = M; long np = 1; C->bufA[0] = uz(); U N = a; int vacc = 0;
    while (1) {
        U n1 = addsmall(N, 1); int t = ctz(n1); U u = shr(n1, t); int first = eq(N, a);
        if (t >= r) {
            for (long i = 0; i < np; i++) { U c = C->bufA[i];
                if (iszero(mask(addsmall(c, 1), r))) return M;
                if (!first && iszero(mask(c, r))) return M; }
            goto death;
        }
        { int rn = r - t; int lim = (rn + 63) / 64; U iv = inv_lim(u, lim); long nn = 0; C->curstamp++;
          if (C->curstamp == 0) { memset(C->hstamp, 0, HSZ * 4); C->curstamp = 1; }
          for (long i = 0; i < np; i++) { U c = C->bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) {
                U x = mask(addsmall(c, e), r); if (t && ctz(x) < t) continue;
                U nc = mask(mul_lim(shr(x, t), iv, lim), rn);
                if (hinsert(C, nc)) { if (nn >= POPLIM) { fprintf(stderr, "population overflow (POPLIM=%ld) at N+1=%llu r=%d\n", POPLIM, (unsigned long long)N.w[0] + 1, r); return -1; } C->bufB[nn++] = nc; }
            } }
          if (nn == 0) goto death;
          if (nn > C->maxpop) C->maxpop = nn;
          U *tmp = C->bufA; C->bufA = C->bufB; C->bufB = tmp; np = nn; r = rn; vacc += t; N = addsmall(N, 1); continue; }
    death:;
        { int best = -1;
          for (long i = 0; i < np; i++) { U c = C->bufA[i];
            for (int e = first ? 1 : 0; e <= 1; e++) { U x = mask(addsmall(c, e), r); int v = iszero(x) ? r : ctz(x); if (v > best) best = v; } }
          return vacc + best; }
    }
}

typedef struct { u64 s[4]; } rng_t;
static inline u64 rotl(const u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 next(rng_t *R) { u64 *s = R->s; const u64 result = rotl(s[1] * 5, 7) * 9; const u64 t = s[1] << 17;
    s[2] ^= s[0]; s[3] ^= s[1]; s[1] ^= s[2]; s[0] ^= s[3]; s[2] ^= t; s[3] = rotl(s[3], 45); return result; }

static long NS; static u64 SEED; static int CAP, NT; static long long HIST[64][BITS + 2]; static long MAXPOP[64]; static int OVF[64];
static void *worker(void *arg) {
    long id = (long)arg; ctx_t C; ctx_init(&C); rng_t R; u64 seed = SEED + 1000003ULL * (u64)id;
    R.s[0] = seed * 0x9E3779B97F4A7C15ULL + 1; R.s[1] = seed ^ 0xDEADBEEFULL; R.s[2] = 12345 + seed; R.s[3] = 0xABCDEF ^ (seed << 7);
    for (int i = 0; i < 20; i++) next(&R);
    long n0 = (NS * id) / NT, n1 = (NS * (id + 1)) / NT;
    for (long i = n0; i < n1; i++) {
        U a; for (int j = 0; j < NL; j++) a.w[j] = next(&R);
        a = mask(a, CAP); if (iszero(a)) a.w[0] = 2;   // x = 0 excluded (prob 2^-CAP), replaced by 2
        int g = g_capped(&C, a, CAP);
        if (g < 0) { OVF[id]++; g = CAP; }   // counted as survivor (conservative upper bound); reported separately
        HIST[id][g]++;
    }
    MAXPOP[id] = C.maxpop;
    return 0;
}

typedef struct { long lo, hi; int cap; int *out; } job_t;
static void *rangeworker(void *arg) { job_t *J = arg; ctx_t C; ctx_init(&C);
    for (long a = J->lo; a <= J->hi; a++) { if (a % 2) { J->out[a] = 0; continue; } U x = uz(); x.w[0] = (u64)a; J->out[a] = g_capped(&C, x, J->cap); } return 0; }

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: gsampleN ns seed CAP [nthreads] | gsampleN 0 0 CAP a1 a2 ...\n"); return 1; }
    NS = atol(argv[1]); SEED = strtoull(argv[2], 0, 10); CAP = atoi(argv[3]);
    if (CAP > BITS - 2) { fprintf(stderr, "CAP too large for NL=%d\n", NL); return 1; }
    if (NS < 0) { // range mode: gsampleN -1 0 CAP A [nthreads]: exact capped g_2(a) for 1 <= a <= A (odd a have g=0)
        long A = atol(argv[4]); int nt = argc > 5 ? atoi(argv[5]) : 1; int *gout = malloc((A + 1) * sizeof(int));
        static job_t jobs[64]; pthread_t th[64];
        for (int i = 0; i < nt; i++) { jobs[i].lo = 1 + (A * i) / nt; jobs[i].hi = (A * (i + 1)) / nt; jobs[i].cap = CAP; jobs[i].out = gout; pthread_create(&th[i], 0, rangeworker, &jobs[i]); }
        for (int i = 0; i < nt; i++) pthread_join(th[i], 0);
        printf("# a g_capped (cap=%d, NL=%d); g=-1 means population overflow\n", CAP, NL);
        for (long a = 1; a <= A; a++) printf("%ld %d\n", a, gout[a]);
        return 0; }
    if (NS == 0) { ctx_t C; ctx_init(&C);
        for (int j = 4; j < argc; j++) { U a = uz(); a.w[0] = strtoull(argv[j], 0, 10); C.maxpop = 0;
            int g = g_capped(&C, a, CAP); printf("a=%s g_capped=%d cap=%d maxpop=%ld\n", argv[j], g, CAP, C.maxpop); fflush(stdout); }
        return 0; }
    NT = argc > 4 ? atoi(argv[4]) : 1; if (NT > 64) NT = 64;
    memset(HIST, 0, sizeof HIST); memset(OVF, 0, sizeof OVF);
    pthread_t th[64];
    for (long i = 0; i < NT; i++) pthread_create(&th[i], 0, worker, (void *)i);
    for (long i = 0; i < NT; i++) pthread_join(th[i], 0);
    long long hist[BITS + 2]; memset(hist, 0, sizeof hist); long mp = 0; int ovf = 0;
    for (int t = 0; t < NT; t++) { for (int k = 0; k <= CAP; k++) hist[k] += HIST[t][k]; if (MAXPOP[t] > mp) mp = MAXPOP[t]; ovf += OVF[t]; }
    long long cum = 0;
    for (int k = CAP; k >= 0; k--) { cum += hist[k]; hist[k] = cum; }
    printf("# gsampleN NL=%d ns=%ld seed=%llu CAP=%d threads=%d maxpop=%ld overflow_samples=%d\n", NL, NS, (unsigned long long)SEED, CAP, NT, mp, ovf);
    for (int k = 0; k <= CAP; k++) printf("k=%d surv=%lld frac=%.6f\n", k, hist[k], (double)hist[k] / NS);
    return 0;
}
