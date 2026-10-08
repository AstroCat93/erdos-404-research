/* cover.c -- exact coverage of the tail achievement set E_N modulo p^{e(N)+k}.
 *   E_N = { sum_{n in B} n! : B subset [N, inf) }  (closed subset of p^{e(N)} Z_p)
 * Prints, for k = 1..K, the fraction of residues of p^{e(N)}Z / p^{e(N)+k}Z that are
 * finite subset sums of { n!/p^{e(N)} : n >= N } mod p^k   (exact, byte-array DP).
 * usage: cover p K N1 [N2 ...]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;

int main(int argc, char **argv) {
  int p = atoi(argv[1]), K = atoi(argv[2]);
  uint64_t M = 1; for (int i = 0; i < K; i++) M *= p;
  unsigned char *S = malloc(M), *T = malloc(M);
  if (!S || !T) { fprintf(stderr, "alloc\n"); return 1; }
  for (int a = 3; a < argc; a++) {
    int N = atoi(argv[a]);
    uint64_t U = 1 % M; int e = 0;
    for (int k = 1; k <= N; k++) { int m = k; while (m % p == 0) { m /= p; e++; } U = (uint64_t)(((u128)U * (uint64_t)m) % M); }
    memset(S, 0, M); S[0] = 1;
    uint64_t cur = U; int vr = 0, n = N, cnt = 0;
    while (vr < K) {
      uint64_t pw = 1; for (int i = 0; i < vr; i++) pw *= p;
      uint64_t w = (uint64_t)(((u128)cur * pw) % M);
      memcpy(T, S, M);
      /* S[(i+w) mod M] |= T[i] */
      uint64_t i = 0, j = w;
      for (; j < M; i++, j++) S[j] |= T[i];
      for (j = 0; i < M; i++, j++) S[j] |= T[i];
      cnt++;
      n++; int m = n; while (m % p == 0) { m /= p; vr++; }
      cur = (uint64_t)(((u128)cur * (uint64_t)m) % M);
    }
    printf("p=%d N=%d e(N)=%d elements=%d :", p, N, e, cnt);
    /* projections */
    for (int k = 1; k <= K; k++) {
      uint64_t mk = 1; for (int i = 0; i < k; i++) mk *= p;
      uint64_t hit = 0;
      if (k == K) { for (uint64_t r = 0; r < M; r++) hit += S[r] != 0; }
      else {
        memset(T, 0, mk);
        for (uint64_t r = 0; r < M; r++) if (S[r]) T[r % mk] = 1;
        for (uint64_t r = 0; r < mk; r++) hit += T[r];
      }
      printf(" k%d:%.6f", k, (double)hit / (double)mk);
    }
    printf("\n"); fflush(stdout);
  }
  return 0;
}
