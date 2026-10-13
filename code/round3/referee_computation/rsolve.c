/*
 * rsolve.c -- round-3 computational referee: an exact exhaustive solver for f(a,2).
 * Written from scratch; shares no code with the R3N track (programs A, B, C) or its checker (D).
 *
 * Decides R(a,K): is there a finite P with min P = a and 2^K | sum_{n in P} n! ?
 * Then f(a,2) = f  iff  R(a,f) and not R(a,f+1).
 *
 * Reduction.  Let N_K = min{N : v(N!) >= K}.  Terms n >= N_K are 0 mod 2^K, so
 * R(a,K) iff some P subset [a,N_K) with a in P has 2^K | S_P.  Deciding P stage by
 * stage, the prefix sum S_N (elements < N) must satisfy 2^{V(N)} | S_N for N < N_K
 * (all later terms are multiples of 2^{V(N)} and K > V(N)), and 2^K | S_{N_K}.
 *
 * State.  t_N = S_N / 2^{V(N)} modulo 2^{L_N}, L_N = K - V(N).  With the odd part
 * U_N = N!/2^{V(N)}:  t_{N+1} = (t_N + x U_N) / 2^{v(N+1)}, x in {0,1}.
 *
 * Fast part: 128-bit window.  r_N = t_N mod 2^{vb_N}; vb drops by v(N+1) per step.
 * Window bases B_0 = a < B_1 < ... are a fixed schedule: a stage N becomes a new base
 * when vb_N is smaller than the number of bits the next test needs.
 *
 * Exact part (only for nodes alive at a base): per window level i an exact
 * accumulator X_i = t_{B_i} + sum_{s in window, chosen} 2^{V(s)-V(B_i)} U_s
 * (mod 2^{L_{B_i}}), updated by signed shifted adds for the stages where the current
 * path differs from the cached one; then t_{B_{i+1}} = X_i >> (V(B_{i+1})-V(B_i)).
 * Two consistency assertions per rebase: the low bits shifted out are zero, and the
 * window value agrees with the exact value on its valid bits.
 *
 * Output: reachable=0/1, node count, best = max v_2(S_P) over all P subset [a,N_K)
 * that die before N_K or fail at N_K (so best = f when K = f+1 is unreachable),
 * and for reachable=1 a witness P written to a file.
 *
 * Build: gcc -O3 -march=native -o rsolve rsolve.c
 * Usage: rsolve a K [witness_file]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef uint64_t limb;

static int64_t V2fact(int64_t n) { return n - __builtin_popcountll((unsigned long long)n); }

static int ctz128(u128 y) { limb lo = (limb)y; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((limb)(y >> 64)); }

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }

/* X (nx limbs, value mod 2^Lbits) += sign * (U (nu limbs) << e) */
static void addsub_shifted(limb *X, int64_t nx, int64_t Lbits, const limb *U, int64_t nu, int64_t e, int neg)
{
    int64_t q = e >> 6; int sh = (int)(e & 63);
    limb carry = 0; /* carry for add, borrow for sub */
    int64_t k;
    for (k = 0; q + k < nx; k++) {
        limb w;
        if (k < nu) {
            w = U[k] << sh;
            if (sh && k > 0) w |= U[k - 1] >> (64 - sh);
        } else if (k == nu) {
            w = (sh && nu > 0) ? (U[nu - 1] >> (64 - sh)) : 0;
        } else {
            w = 0;
            if (carry == 0) break;
        }
        limb *d = &X[q + k];
        if (!neg) {
            u128 s = (u128)*d + w + carry;
            *d = (limb)s; carry = (limb)(s >> 64);
        } else {
            u128 s = (u128)*d - w - carry;
            *d = (limb)s; carry = (limb)((s >> 64) ? 1 : 0);
        }
    }
    int tb = (int)(Lbits & 63);
    if (tb) X[nx - 1] &= (((limb)1) << tb) - 1;
}

int main(int argc, char **argv)
{
    if (argc < 3) { fprintf(stderr, "usage: rsolve a K [witness_file]\n"); return 1; }
    int64_t a = atoll(argv[1]), K = atoll(argv[2]);
    const char *wfile = argc > 3 ? argv[3] : NULL;
    if (a < 1 || K <= V2fact(a)) die("need a>=1 and K > v2(a!)");
    clock_t t0 = clock();

    int64_t NK = a; while (V2fact(NK) < K) NK++;
    int64_t S = NK - a + 2;              /* stage index = N - a, N in [a, NK] */
    int64_t *Vt = malloc(S * sizeof(int64_t));
    int64_t *Lt = malloc(S * sizeof(int64_t));
    for (int64_t N = a; N <= NK; N++) { Vt[N - a] = V2fact(N); Lt[N - a] = K - V2fact(N); }

    /* exact odd parts U_N mod 2^{L_N}, N in [a, NK) */
    int64_t *uoff = malloc(S * sizeof(int64_t)), *unl = malloc(S * sizeof(int64_t));
    int64_t tot = 0;
    for (int64_t N = a; N < NK; N++) { unl[N - a] = (Lt[N - a] + 63) / 64; uoff[N - a] = tot; tot += unl[N - a]; }
    limb *pool = calloc((size_t)tot + 1, sizeof(limb));
    if (!pool) die("out of memory (U pool)");
    {
        int64_t n0 = unl[0], L0 = Lt[0];
        limb *u = pool + uoff[0];
        u[0] = 1;
        for (int64_t m = 2; m <= a; m++) {      /* u <- u * oddpart(m) mod 2^{L_a} */
            limb om = (limb)m; while (!(om & 1)) om >>= 1;
            limb c = 0;
            for (int64_t k = 0; k < n0; k++) { u128 p = (u128)u[k] * om + c; u[k] = (limb)p; c = (limb)(p >> 64); }
        }
        if (L0 & 63) u[n0 - 1] &= (((limb)1) << (L0 & 63)) - 1;
        for (int64_t N = a + 1; N < NK; N++) {
            limb om = (limb)N; while (!(om & 1)) om >>= 1;
            const limb *src = pool + uoff[N - 1 - a];
            limb *dst = pool + uoff[N - a];
            int64_t nd = unl[N - a]; limb c = 0;
            for (int64_t k = 0; k < nd; k++) { u128 p = (u128)src[k] * om + c; dst[k] = (limb)p; c = (limb)(p >> 64); }
            if (Lt[N - a] & 63) dst[nd - 1] &= (((limb)1) << (Lt[N - a] & 63)) - 1;
        }
    }
    u128 *u = malloc(S * sizeof(u128));
    for (int64_t N = a; N < NK; N++) {
        const limb *src = pool + uoff[N - a];
        u128 w = src[0];
        if (unl[N - a] > 1) w |= ((u128)src[1]) << 64;
        u[N - a] = w;
    }

    /* window schedule */
    int *lev = malloc(S * sizeof(int));      /* level index if stage is a base, else -1 */
    int *jv = malloc(S * sizeof(int)), *need = malloc(S * sizeof(int));
    int64_t *vbB = malloc(S * sizeof(int64_t));
    int64_t nlev = 0; int64_t *base = malloc(S * sizeof(int64_t));
    {
        int64_t B = a, vb0 = Lt[0] < 128 ? Lt[0] : 128;
        for (int64_t N = a; N < NK; N++) {
            jv[N - a] = (int)(Vt[N + 1 - a] - Vt[N - a]);
            need[N - a] = (N + 1 == NK) ? (int)Lt[N - a] : jv[N - a];
            int64_t vb = vb0 - (Vt[N - a] - Vt[B - a]);
            lev[N - a] = -1;
            if (N == a) { lev[0] = 0; base[nlev++] = a; vbB[0] = vb0; continue; }
            if (vb < need[N - a]) {
                B = N; vb0 = Lt[N - a] < 128 ? Lt[N - a] : 128;
                lev[N - a] = (int)nlev; vbB[nlev] = vb0; base[nlev++] = N;
                if (vb0 < need[N - a]) die("schedule");
            }
        }
        base[nlev] = NK;
    }
    /* per-level exact accumulators and cached decisions */
    limb **X = malloc(nlev * sizeof(limb *));
    unsigned char **cache = malloc(nlev * sizeof(unsigned char *));
    int64_t *Xn = malloc(nlev * sizeof(int64_t)), *XL = malloc(nlev * sizeof(int64_t));
    for (int64_t i = 0; i < nlev; i++) {
        XL[i] = Lt[base[i] - a]; Xn[i] = (XL[i] + 63) / 64;
        X[i] = calloc(Xn[i] + 1, sizeof(limb));
        cache[i] = calloc(base[i + 1] - base[i] + 1, 1);
    }

    u128 *r = malloc(S * sizeof(u128));
    unsigned char *nx = malloc(S), *dec = malloc(S);
    int *curlev = malloc(S * sizeof(int));     /* window level of each stage */
    { int c = 0; for (int64_t N = a; N < NK; N++) { if (lev[N - a] >= 0) c = lev[N - a]; curlev[N - a] = c; } }

    u128 lowmask[130];
    for (int j = 0; j < 128; j++) lowmask[j] = (j == 0) ? 0 : ((((u128)1) << j) - 1);
    lowmask[128] = ~(u128)0;

    uint64_t nodes = 0, rebases = 0, fulladds = 0;
    int64_t best = -1; int reachable = 0;
    int64_t N = a;
    r[0] = 0; nx[0] = 1;   /* stage a: x = 1 forced */
    memset(X[0], 0, Xn[0] * sizeof(limb));
    memset(cache[0], 0, base[1] - base[0]);

    while (1) {
        int64_t id = N - a;
        if (nx[id] > 1) { if (N == a) break; N--; continue; }
        int x = nx[id]++;
        dec[id] = (unsigned char)x;
        u128 y = r[id] + (x ? u[id] : 0);
        int nd = need[id];
        if (y & lowmask[nd]) {                      /* dies here: exact final valuation */
            int64_t vv = Vt[id] + ctz128(y);
            if (vv > best) best = vv;
            continue;
        }
        if (N + 1 == NK) { reachable = 1; break; }
        nodes++;
        int j = jv[id];
        y >>= j;
        int64_t N1 = N + 1, id1 = id + 1;
        int L1 = lev[id1];
        if (L1 >= 0) {                              /* rebase to exact */
            int i = L1 - 1;                         /* window level we are leaving */
            int64_t B = base[i];
            int64_t E = Vt[id1] - Vt[B - a];
            unsigned char *c = cache[i];
            for (int64_t s = B; s < N1; s++) {
                unsigned char d = dec[s - a];
                if (d != c[s - B]) {
                    addsub_shifted(X[i], Xn[i], XL[i], pool + uoff[s - a], unl[s - a], Vt[s - a] - Vt[B - a], d == 0);
                    c[s - B] = d; fulladds++;
                }
            }
            /* check low E bits of X[i] are zero */
            {
                int64_t q = E >> 6; int sh = (int)(E & 63);
                for (int64_t k = 0; k < q && k < Xn[i]; k++) if (X[i][k]) die("rebase: low limbs nonzero");
                if (sh && q < Xn[i] && (X[i][q] & ((((limb)1) << sh) - 1))) die("rebase: low bits nonzero");
            }
            /* X[L1] = X[i] >> E  mod 2^{XL[L1]} */
            {
                limb *dst = X[L1]; int64_t ndst = Xn[L1];
                int64_t q = E >> 6; int sh = (int)(E & 63);
                for (int64_t k = 0; k < ndst; k++) {
                    limb lo = (q + k < Xn[i]) ? X[i][q + k] : 0;
                    limb hi = (q + k + 1 < Xn[i]) ? X[i][q + k + 1] : 0;
                    dst[k] = sh ? ((lo >> sh) | (hi << (64 - sh))) : lo;
                }
                if (XL[L1] & 63) dst[ndst - 1] &= (((limb)1) << (XL[L1] & 63)) - 1;
                memset(cache[L1], 0, base[L1 + 1] - base[L1]);
                u128 full = dst[0];
                if (ndst > 1) full |= ((u128)dst[1]) << 64;
                /* window value must agree with exact value on its valid bits */
                int64_t vbw = vbB[i] - (Vt[id1] - Vt[B - a]);
                if (vbw > 0 && ((full ^ y) & lowmask[vbw > 128 ? 128 : vbw])) die("rebase: window mismatch");
                y = full;
            }
            rebases++;
        }
        r[id1] = y; nx[id1] = 0; N = N1;
    }
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("RESULT a=%lld K=%lld NK=%lld reachable=%d nodes=%llu rebases=%llu fulladds=%llu levels=%lld best=%lld time=%.1fs\n",
           (long long)a, (long long)K, (long long)NK, reachable, (unsigned long long)nodes,
           (unsigned long long)rebases, (unsigned long long)fulladds, (long long)nlev, (long long)best, secs);
    if (!reachable)
        printf("UNREACHABLE: f(%lld,2) <= %lld; max valuation over all P in [a,N_K) = %lld\n", (long long)a, (long long)(K - 1), (long long)best);
    if (reachable && wfile) {
        FILE *fh = fopen(wfile, "w");
        int64_t cnt = 0;
        for (int64_t s = a; s < NK; s++) cnt += dec[s - a];
        fprintf(fh, "# rsolve witness for f(%lld,2) >= %lld, |P| = %lld\n", (long long)a, (long long)K, (long long)cnt);
        for (int64_t s = a; s < NK; s++) if (dec[s - a]) fprintf(fh, "%lld\n", (long long)s);
        fclose(fh);
    }
    return 0;
}
