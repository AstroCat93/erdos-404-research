// Residue-class tree for Erdos #404:  for each level G, the set
//   S_G = { c mod p^G : g(a,p) >= G for a == c mod p^G }
// (well defined by the Locality Lemma).  S_{G+1} consists of children of S_G.
// decide(p,a,G) is the exact pruned residue DP (independent re-implementation of e404lib.ge).
//
// usage: tree p Gmax nthreads outprefix [G0]
//   writes per-level counts to stdout; writes survivors of level G0 with the depth
//   their subtree reaches (<= Gmax) to outprefix_subtree_G0.txt
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

typedef struct { u64 *a, *b; size_t cap; } buf_t;

static void ensure(buf_t *B, size_t n) {
    if (n <= B->cap) return;
    size_t c = B->cap ? B->cap : 1024;
    while (c < n) c *= 2;
    B->a = realloc(B->a, c * sizeof(u64));
    B->b = realloc(B->b, c * sizeof(u64));
    if (!B->a || !B->b) { fprintf(stderr, "oom\n"); exit(1); }
    B->cap = c;
}

// returns 1 iff exists finite T subset {1,2,...}: 1 + sum_{k in T} (a+1)...(a+k) == 0 mod p^G
static int decide(u64 p, u64 a, int G, buf_t *B) {
    if (G <= 0) return 1;
    u64 M = 1; for (int i = 0; i < G; i++) M *= p;
    u64 Mc = M; int L = 0;
    ensure(B, 4);
    u64 *R = B->a; size_t n = 1; R[0] = 1 % M;
    if (R[0] == 0) return 1;
    u64 u = 1; int v = 0;
    for (u64 k = 1;; k++) {
        u64 x = a + k; int w = 0;
        while (x % p == 0) { x /= p; w++; }
        v += w;
        if (v >= G) return 0;            // all remaining terms vanish mod p^G; 0 not reached
        u = (u64)(((u128)u * (u128)(x % M)) % M);
        if (v > L) {
            u64 d = 1; for (int i = 0; i < v - L; i++) d *= p;
            size_t m = 0;
            for (size_t i = 0; i < n; i++) if (R[i] % d == 0) R[m++] = R[i] / d;
            n = m; Mc /= d; L = v;
            if (n == 0) return 0;
        }
        u64 t = u % Mc;
        ensure(B, 2 * n + 4);
        R = B->a; u64 *S = B->b;
        // R sorted ascending, values in [0,Mc).  R+t mod Mc sorted: split at wrap index.
        size_t wrap = n; // first index with R[i] + t >= Mc
        {
            size_t lo = 0, hi = n;
            while (lo < hi) { size_t mid = (lo + hi) / 2; if (R[mid] >= Mc - t) hi = mid; else lo = mid + 1; }
            wrap = lo;
        }
        // shifted sequence: R[wrap..n-1]+t-Mc (small), then R[0..wrap-1]+t
        size_t i = 0, j = 0, m = 0, ns = n;
        // merge R (i) with shifted (j over 0..ns-1)
        while (i < n || j < ns) {
            u64 sv = 0; int have = (j < ns);
            if (have) { size_t idx = (j < n - wrap) ? (wrap + j) : (j - (n - wrap));
                        sv = (j < n - wrap) ? (R[idx] + t - Mc) : (R[idx] + t); }
            u64 rv = (i < n) ? R[i] : 0;
            u64 val;
            if (i < n && (!have || rv <= sv)) { val = rv; i++; if (have && rv == sv) j++; }
            else { val = sv; j++; }
            if (m == 0 || S[m - 1] != val) S[m++] = val;
        }
        B->a = S; B->b = R; R = S; n = m;
        if (R[0] == 0) return 1;
        if (n == Mc) return 1;
    }
}

// ---------------- tree driver -----------------
static u64 P; static int GLEV; static u64 *par; static size_t npar; static unsigned char *res;
static int NT;
static void *worker(void *arg) {
    long id = (long)arg; buf_t B = {0, 0, 0};
    u64 Mprev = 1; for (int i = 0; i < GLEV - 1; i++) Mprev *= P;
    u64 Mnew = Mprev * P;
    for (size_t i = id; i < npar; i += NT) {
        for (u64 c = 0; c < P; c++) {
            u64 cl = par[i] + c * Mprev;
            u64 rep = cl ? cl : Mnew;
            res[i * P + c] = (unsigned char)decide(P, rep, GLEV, &B);
        }
    }
    free(B.a); free(B.b);
    return NULL;
}

int main(int argc, char **argv) {
    if (argc > 1 && !strcmp(argv[1], "test")) { buf_t B={0,0,0}; unsigned long long p,a; int G; while (scanf("%llu %llu %d",&p,&a,&G)==3) printf("%d\n", decide(p,a,G,&B)); return 0; }
    if (argc > 1 && !strcmp(argv[1], "gtab")) { // gtab p amin amax cap : prints a min(g(a),cap)
        buf_t B={0,0,0}; u64 p=strtoull(argv[2],0,10), a0=strtoull(argv[3],0,10), a1=strtoull(argv[4],0,10); int cap=atoi(argv[5]);
        for (u64 a=a0;a<=a1;a++){ int lo=0, hi=cap; // invariant: g>=lo, and (hi==cap or g<hi+1)
            while(lo<hi){ int mid=(lo+hi+1)/2; if(decide(p,a,mid,&B)) lo=mid; else hi=mid-1; }
            printf("%llu %d\n",(unsigned long long)a,lo); }
        return 0; }
    if (argc < 5) { fprintf(stderr, "usage: tree p Gmax nthreads outprefix [G0]\n"); return 1; }
    P = strtoull(argv[1], 0, 10); int Gmax = atoi(argv[2]); NT = atoi(argv[3]);
    const char *pre = argv[4]; int G0 = argc > 5 ? atoi(argv[5]) : -1;
    // level 0: single class 0 mod 1
    par = malloc(sizeof(u64)); par[0] = 0; npar = 1;
    // ancestor bookkeeping for G0: anc index of each current survivor
    u64 *anc = NULL; size_t nanc0 = 0; int *depth = NULL; u64 *ancval = NULL;
    u64 Mlev = 1;
    printf("# p=%llu\n# G  survivors  density  children-survival-histogram(0..p)\n", (unsigned long long)P);
    printf("%d %zu %.10f\n", 0, npar, 1.0);
    for (int G = 1; G <= Gmax; G++) {
        GLEV = G;
        res = malloc(npar * P);
        pthread_t th[64];
        for (long t = 0; t < NT; t++) pthread_create(&th[t], 0, worker, (void *)t);
        for (long t = 0; t < NT; t++) pthread_join(th[t], 0);
        u64 Mprev = Mlev; Mlev *= P;
        size_t cnt = 0; size_t hist[64] = {0};
        for (size_t i = 0; i < npar; i++) { int h = 0; for (u64 c = 0; c < P; c++) h += res[i * P + c]; hist[h]++; cnt += h; }
        u64 *np = malloc((cnt ? cnt : 1) * sizeof(u64));
        u64 *nanc = (G0 >= 0 && G > G0) ? malloc((cnt ? cnt : 1) * sizeof(u64)) : NULL;
        size_t k = 0;
        for (size_t i = 0; i < npar; i++) for (u64 c = 0; c < P; c++) if (res[i * P + c]) {
            if (nanc) nanc[k] = anc[i];
            np[k++] = par[i] + c * Mprev;
        }
        free(par); free(res); par = np; npar = cnt;
        if (G0 >= 0 && G == G0) {
            nanc0 = npar; anc = malloc((npar ? npar : 1) * sizeof(u64));
            depth = malloc((npar ? npar : 1) * sizeof(int)); ancval = malloc((npar ? npar : 1) * sizeof(u64));
            for (size_t i = 0; i < npar; i++) { anc[i] = i; depth[i] = G0; ancval[i] = par[i]; }
        } else if (nanc) {
            free(anc); anc = nanc;
            for (size_t i = 0; i < npar; i++) depth[anc[i]] = G;
        }
        double dens = (double)npar / (double)Mlev;
        printf("%d %zu %.10f", G, npar, dens);
        for (u64 h = 0; h <= P; h++) printf(" %zu", hist[h]);
        printf("\n"); fflush(stdout);
        if (npar == 0) break;
    }
    if (G0 >= 0 && depth) {
        char fn[1024]; snprintf(fn, sizeof fn, "%s_subtree_G%d.txt", pre, G0);
        FILE *f = fopen(fn, "w");
        fprintf(f, "# class_mod_p^%d  max_level_reached_by_descendants(capped at Gmax=%d)\n", G0, Gmax);
        for (size_t i = 0; i < nanc0; i++) fprintf(f, "%llu %d\n", (unsigned long long)ancval[i], depth[i]);
        fclose(f);
    }
    // dump final survivors
    char fn[1024]; snprintf(fn, sizeof fn, "%s_survivors_last.txt", pre);
    FILE *f = fopen(fn, "w");
    for (size_t i = 0; i < npar && i < 2000000; i++) fprintf(f, "%llu\n", (unsigned long long)par[i]);
    fclose(f);
    return 0;
}
