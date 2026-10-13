/* shellchk.c -- independent check (round 3, check of track R3F).
 *
 * Computes enclosures of the L^1 and L^2 Fourier shells
 *     S1 = sum_{u in (Z/M)^x} prod_i |cos(pi u x_i / M)|,   S2 = sum_u prod_i cos^2(pi u x_i / M)
 * for M = p^d and a list of residues x_i mod M.
 *
 * Method (shares no code with the R3F programs ivshell.c, gate_d.c, shells_mpfr.py):
 *  - cos(pi r / M) for 0 <= r < M is evaluated from FOUR precomputed tables via the addition formula
 *        r = hi*B + lo,  cos(pi r/M) = Ch[hi]*Cl[lo] - Sh[hi]*Sl[lo],
 *    with Ch[h] = cos(pi h B/M), Sh[h] = sin(pi h B/M), Cl[l] = cos(pi l/M), Sl[l] = sin(pi l/M).
 *    The tables are produced by gen_tables.py with arb ball arithmetic (python-flint); the generator
 *    certifies a bound e_t on |table double - true value| and an absolute bound eps on the error of the
 *    evaluated cosine (eps >= 4 e_t + 2.0001 u + rounding of the final +-eps step; see gen_tables.py).
 *  - Each factor is replaced by a_i = min(1, |c~| + eps) (upper) and b_i = max(0, |c~| - eps) (lower).
 *  - Default rounding (round to nearest), no FMA contraction (-ffp-contract=off).  The products, squares and
 *    block sums are computed in double; block sums (L = 4096 terms) are accumulated in long double.
 *    The driver (shells.py) multiplies the printed upper sums by (1-u)^{-(2n-1)} / (1-gamma_{L-1}) /
 *    (1 - nblocks 2^-64) (1 + 1e-19) and the lower sums by the reciprocal-type factor, u = 2^-53
 *    (product roundings, recursive summation in double within a block, long-double accumulation, decimal print).
 *  - u runs over 1..(M-1)/2 (M odd); u and M-u give equal products, so the totals are 2x the half sums.
 *    Residues r_i = u x_i mod M are updated incrementally; non-units (p | u) are skipped.
 *    Optional range [ulo, uhi] for chunked runs (default: the whole half range).
 *
 * usage: shellchk TABLEFILE ELEMFILE p [ulo uhi]
 *   TABLEFILE: binary  uint64 M, uint64 B, uint64 nhi, double eps, then double Ch[nhi], Sh[nhi], Cl[B], Sl[B]
 *   ELEMFILE : text    n  then n residues mod M
 * output: one line "M n ulo uhi units_half S1_up_half S1_lo_half S2_up_half S2_lo_half" (%.17Lg)
 * build: gcc -O2 -ffp-contract=off -fno-fast-math -o shellchk shellchk.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: shellchk TABLE ELEM p [ulo uhi]\n"); return 1; }
  FILE *ft = fopen(argv[1], "rb"); if (!ft) { perror("table"); return 1; }
  uint64_t M, B, nhi; double eps;
  if (fread(&M, 8, 1, ft) != 1 || fread(&B, 8, 1, ft) != 1 || fread(&nhi, 8, 1, ft) != 1 || fread(&eps, 8, 1, ft) != 1) return 1;
  int logB = 0; while ((1ULL << logB) < B) logB++;
  if ((1ULL << logB) != B) { fprintf(stderr, "B not a power of two\n"); return 1; }
  if (nhi * B < M) { fprintf(stderr, "table too short\n"); return 1; }
  double *Ch = malloc(8 * nhi), *Sh = malloc(8 * nhi), *Cl = malloc(8 * B), *Sl = malloc(8 * B);
  if (fread(Ch, 8, nhi, ft) != nhi || fread(Sh, 8, nhi, ft) != nhi || fread(Cl, 8, B, ft) != B || fread(Sl, 8, B, ft) != B) { fprintf(stderr, "short table\n"); return 1; }
  fclose(ft);
  FILE *fe = fopen(argv[2], "r"); if (!fe) { perror("elem"); return 1; }
  int n; if (fscanf(fe, "%d", &n) != 1 || n < 1 || n > 200) return 1;
  uint64_t x[200], r[200];
  for (int i = 0; i < n; i++) { unsigned long long v; if (fscanf(fe, "%llu", &v) != 1) return 1; x[i] = v % M; }
  fclose(fe);
  uint64_t p = strtoull(argv[3], 0, 10);
  uint64_t half = (M - 1) / 2, ulo = 1, uhi = half;
  if (argc >= 6) { ulo = strtoull(argv[4], 0, 10); uhi = strtoull(argv[5], 0, 10); if (uhi > half) uhi = half; }
  /* initial residues r_i = (ulo - 1) x_i mod M */
  for (int i = 0; i < n; i++) r[i] = (uint64_t)(((unsigned __int128)(ulo - 1) * x[i]) % M);
  uint64_t mask = B - 1, cnt = (ulo - 1) % p, units = 0;
  long double A1u = 0, A1l = 0, A2u = 0, A2l = 0;
  double b1u = 0, b1l = 0, b2u = 0, b2l = 0; uint32_t inblk = 0;
  for (uint64_t u = ulo; u <= uhi; u++) {
    for (int i = 0; i < n; i++) { uint64_t t = r[i] + x[i]; r[i] = (t >= M) ? t - M : t; }
    cnt++; if (cnt == p) { cnt = 0; continue; }
    double pu = 1.0, pl = 1.0;
    for (int i = 0; i < n; i++) {
      uint64_t rr = r[i], hi = rr >> logB, lo = rr & mask;
      double c = Ch[hi] * Cl[lo] - Sh[hi] * Sl[lo];
      double a = fabs(c);
      double au = a + eps; if (au > 1.0) au = 1.0;
      double al = a - eps; if (al < 0.0) al = 0.0;
      pu *= au; pl *= al;
    }
    b1u += pu; b1l += pl; b2u += pu * pu; b2l += pl * pl; units++;
    if (++inblk == 4096) { A1u += b1u; A1l += b1l; A2u += b2u; A2l += b2l; b1u = b1l = b2u = b2l = 0; inblk = 0; }
  }
  A1u += b1u; A1l += b1l; A2u += b2u; A2l += b2l;
  printf("%llu %d %llu %llu %llu %.21Lg %.21Lg %.21Lg %.21Lg\n", (unsigned long long)M, n, (unsigned long long)ulo,
         (unsigned long long)uhi, (unsigned long long)units, A1u, A1l, A2u, A2l);
  return 0;
}
