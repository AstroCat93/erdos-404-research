// verify_witness_gmp.c -- second independent exact verifier for p=2 witness files (track R3N).
// Computes the exact integer S = sum_{n in A} n! with GMP (mpz_fac_ui for the first term,
// then a running product), and prints v_2(S) = mpz_scan1(S, 0).  No modular reduction.
// Usage: verify_witness_gmp FILE a [K]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: verify_witness_gmp FILE a [K]\n"); return 2; }
    FILE *f = fopen(argv[1], "r"); if (!f) { perror("open"); return 2; }
    long a = atol(argv[2]); long K = argc > 3 ? atol(argv[3]) : -1;
    long cap = 1 << 16, n = 0; long *A = malloc(cap * sizeof(long));
    char line[256];
    while (fgets(line, sizeof line, f)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        if (n == cap) { cap *= 2; A = realloc(A, cap * sizeof(long)); }
        A[n++] = atol(line);
    }
    fclose(f);
    int ok = 1;
    if (n == 0 || A[0] != a) { printf("FAIL: min != a\n"); ok = 0; }
    for (long i = 1; i < n; i++) if (A[i] <= A[i - 1]) { printf("FAIL: not increasing at %ld\n", i); ok = 0; break; }
    mpz_t P, S; mpz_init(P); mpz_init(S);
    mpz_fac_ui(P, (unsigned long)A[0]);   // P = A[0]!
    mpz_set(S, P);
    long cur = A[0];
    for (long i = 1; i < n; i++) {
        while (cur < A[i]) { cur++; mpz_mul_ui(P, P, (unsigned long)cur); }
        mpz_add(S, S, P);
    }
    // cross-check the running product against mpz_fac_ui at the end
    mpz_t Q; mpz_init(Q); mpz_fac_ui(Q, (unsigned long)cur);
    if (mpz_cmp(P, Q)) { printf("FAIL: running product mismatch\n"); ok = 0; }
    unsigned long v = mpz_scan1(S, 0);
    long va = 0; for (long m = a; m; m /= 2) va += m / 2;
    printf("terms=%ld min=%ld max=%ld v2(sum)=%lu bits=%zu v2(a!)=%ld g>=%ld\n", n, A[0], A[n - 1], v, mpz_sizeinbase(S, 2), va, (long)v - va);
    if (K >= 0) { printf("check v2(sum) >= %ld: %s\n", K, (long)v >= K ? "True" : "False"); if ((long)v < K) ok = 0; }
    printf(ok ? "VERIFIED\n" : "NOT VERIFIED\n");
    return ok ? 0 : 1;
}
