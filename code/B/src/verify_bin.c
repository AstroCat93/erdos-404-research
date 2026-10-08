/*
 * verify_bin.c -- independent verifier for witnesses of  f(a,p) >= K.
 *
 * Shares NO code with search.c: arithmetic is ordinary binary multiprecision modulo M = p^K
 * (64-bit limbs, Knuth-D single-digit reduction with a normalized modulus), not base-p^w digits.
 *
 * Reads a witness file (one integer per line, '#' comments ignored), checks
 *   - strictly increasing, first element == a,
 *   - S := sum_{n in list} n!  ==  0  (mod p^K),
 * by streaming n = 0,1,2,...,max: X = n! mod M (scaled), S += X when n is listed.
 *
 * usage: verify_bin p a K file
 * exit code 0 iff VERIFIED.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
static int nl;                 /* limbs of M */
static uint64_t *Mn;           /* normalized modulus M << s */

/* y (nl+1 limbs) := y mod Mn, given y < Mn * 2^64 and y[nl] < Mn[nl-1] */
static void reduce1(uint64_t *y) {
    uint64_t top = y[nl], nxt = y[nl - 1];
    u128 num = ((u128)top << 64) | nxt;
    uint64_t qh = (uint64_t)(num / Mn[nl - 1]);
    if (qh == 0) return;  /* then y < Mn already? not necessarily; handled below by compare loop */
    /* y -= qh * Mn */
    uint64_t carry = 0, borrow = 0;
    for (int i = 0; i < nl; i++) {
        u128 pr = (u128)qh * Mn[i] + carry;
        uint64_t lo = (uint64_t)pr; carry = (uint64_t)(pr >> 64);
        uint64_t yi = y[i];
        uint64_t d = yi - lo - borrow;
        borrow = (yi < lo) || (yi - lo < borrow);
        y[i] = d;
    }
    uint64_t yt = y[nl] - carry - borrow;   /* top limb, 0 or 0xFFFF.. (negative) */
    y[nl] = yt;
    while ((int64_t)y[nl] < 0) {  /* add back */
        uint64_t c = 0;
        for (int i = 0; i < nl; i++) {
            u128 s = (u128)y[i] + Mn[i] + c;
            y[i] = (uint64_t)s; c = (uint64_t)(s >> 64);
        }
        y[nl] += c;
    }
}
static int geq_M(const uint64_t *y) {  /* y has nl+1 limbs */
    if (y[nl]) return 1;
    for (int i = nl - 1; i >= 0; i--) { if (y[i] != Mn[i]) return y[i] > Mn[i]; }
    return 1;
}
static void sub_M(uint64_t *y) {
    uint64_t borrow = 0;
    for (int i = 0; i < nl; i++) {
        uint64_t yi = y[i], m = Mn[i];
        uint64_t d = yi - m - borrow;
        borrow = (yi < m) || (yi - m < borrow);
        y[i] = d;
    }
    y[nl] -= borrow;
}
static void normalize(uint64_t *y) { while (geq_M(y)) { if (y[nl] || 1) { reduce1(y); if (!geq_M(y)) break; sub_M(y); } } }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s p a K file\n", argv[0]); return 2; }
    long long p = atoll(argv[1]), a = atoll(argv[2]); long long K = atoll(argv[3]);
    FILE *f = fopen(argv[4], "r"); if (!f) { perror("open"); return 2; }
    long long cap = 1 << 20, cnt = 0; long long *xs = malloc(cap * sizeof(long long));
    char line[256];
    while (fgets(line, sizeof line, f)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        if (cnt == cap) { cap *= 2; xs = realloc(xs, cap * sizeof(long long)); }
        xs[cnt++] = atoll(line);
    }
    fclose(f);
    if (cnt == 0) { printf("EMPTY\n"); return 1; }
    if (xs[0] != a) { printf("FIRST ELEMENT %lld != a=%lld\n", xs[0], a); return 1; }
    for (long long i = 1; i < cnt; i++) if (xs[i] <= xs[i - 1]) { printf("NOT INCREASING at %lld\n", i); return 1; }
    /* M = p^K in binary */
    int maxl = (int)(K * 4 / 64) + 4;  /* log2(13) < 4 */
    uint64_t *M = calloc(maxl, 8); M[0] = 1; int ml = 1;
    long long rem = K;
    uint64_t chunk = 1; int ck = 0; while (chunk <= (UINT64_MAX / p) / p && ck < 30) { chunk *= p; ck++; }
    while (rem > 0) {
        uint64_t mul = 1; int k = 0; while (k < ck && k < rem) { mul *= p; k++; }
        rem -= k;
        uint64_t c = 0;
        for (int i = 0; i < ml; i++) { u128 pr = (u128)M[i] * mul + c; M[i] = (uint64_t)pr; c = (uint64_t)(pr >> 64); }
        if (c) M[ml++] = c;
    }
    nl = ml;
    int s = __builtin_clzll(M[nl - 1]);
    Mn = calloc(nl + 1, 8);
    for (int i = nl - 1; i >= 0; i--) {
        Mn[i] = (M[i] << s) | ((s && i > 0) ? (M[i - 1] >> (64 - s)) : 0);
    }
    /* X = 1 * 2^s (scaled), S = 0 */
    uint64_t *X = calloc(nl + 1, 8), *S = calloc(nl + 1, 8);
    X[0] = (uint64_t)1 << s; if (s == 0) X[0] = 1;
    if (K == 0) { printf("VERIFIED trivially (K=0)\n"); return 0; }
    long long last = xs[cnt - 1], j = 0;
    clock_t t0 = clock();
    for (long long n = 0; n <= last; n++) {
        if (n > 0) {
            /* X := X * n mod Mn */
            uint64_t c = 0;
            for (int i = 0; i < nl; i++) { u128 pr = (u128)X[i] * (uint64_t)n + c; X[i] = (uint64_t)pr; c = (uint64_t)(pr >> 64); }
            X[nl] = c;
            reduce1(X);
            while (geq_M(X)) sub_M(X);
        }
        if (xs[j] == n) {
            uint64_t c = 0;
            for (int i = 0; i < nl; i++) { u128 sm = (u128)S[i] + X[i] + c; S[i] = (uint64_t)sm; c = (uint64_t)(sm >> 64); }
            S[nl] += c;
            while (geq_M(S)) sub_M(S);
            j++;
            if (j == cnt) break;
        }
    }
    int zero = 1; for (int i = 0; i <= nl; i++) if (S[i]) { zero = 0; break; }
    printf("p=%lld a=%lld K=%lld terms=%lld max=%lld  sum mod p^K %s  -> %s  (%.1fs)\n", p, a, K, cnt, last,
           zero ? "== 0" : "!= 0", zero ? "VERIFIED" : "FAILED", (double)(clock() - t0) / CLOCKS_PER_SEC);
    (void)normalize;
    return zero ? 0 : 1;
}
