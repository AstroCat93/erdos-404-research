// gatesum.c -- single-gate-block Fourier L^1 sums (Erdos #404, round 3, track T4, item 4).
//
// e_u = (-1)^u (p-1)!/u!  (u = 0..p-1; r = p-1-u), the gate-block elements of note.md Thm 3.9(b).
// For i >= 1 computes (double precision, pairwise-summed per thread):
//   Lunit(p,i)  = sum over units xi mod p^i          of prod_u |cos(pi xi e_u / p^i)|
//   Lall(p,i)   = sum over all xi != 0 mod p^i       of the same product
//   maxterm, argmax
// and (with flag) the integral  I_p = int_0^1 prod_u |cos(pi e_u theta)| dtheta,
// computed exactly-in-structure: with Theta = (p-1)! theta the integrand is prod_u |cos(pi Theta/u!)|,
// whose only kinks (for u >= 2) lie at integers Theta (since u!/2 is an integer), and for u = 0,1 the factor is
// cos^2(pi Theta), smooth.  So I_p = (1/(p-1)!) sum_{k=0}^{(p-1)!-1} int_0^1 F(k+t) dt with F smooth on each
// unit interval; each piece by NGL-point Gauss-Legendre.  Convergence is checked by varying NGL.
// usage: gatesum p imax nthreads [ngl]     (ngl > 0 also computes I_p with that many nodes; 0 skips)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <pthread.h>
typedef uint64_t u64; typedef __int128 i128; typedef unsigned __int128 u128;

static int P, NT; static long long E[64]; static u64 Q; static int NGL;
static double GLx[64], GLw[64];

// Gauss-Legendre nodes on [0,1] via Newton iteration on Legendre polynomials
static void gauss_legendre(int n) {
    for (int i = 0; i < n; i++) {
        double x = cos(M_PI * (i + 0.75) / (n + 0.5));
        for (int it = 0; it < 100; it++) {
            double p0 = 1, p1 = x;
            for (int k = 2; k <= n; k++) { double p2 = ((2 * k - 1) * x * p1 - (k - 1) * p0) / k; p0 = p1; p1 = p2; }
            double dp = n * (x * p1 - p0) / (x * x - 1);
            double dx = p1 / dp; x -= dx; if (fabs(dx) < 1e-16) {
                double pp0 = 1, pp1 = x; for (int k = 2; k <= n; k++) { double p2 = ((2 * k - 1) * x * pp1 - (k - 1) * pp0) / k; pp0 = pp1; pp1 = p2; }
                dp = n * (x * pp1 - pp0) / (x * x - 1); GLw[i] = 1.0 / ((1 - x * x) * dp * dp); GLx[i] = 0.5 * (x + 1); break; }
        }
    }
}

typedef struct { int id; double Lunit, Lall, mx; u64 argmx; double I; } job_t;

static void *sumworker(void *arg) {
    job_t *J = arg; double Lu = 0, La = 0, mx = 0; u64 am = 0;
    // thread-local Kahan-ish: accumulate in long double
    long double LLu = 0, LLa = 0;
    u64 start = 1 + (u64)J->id;   // xi = 1.. Q-1, strided by NT
    for (u64 xi = start; xi < Q; xi += NT) {
        double pr = 1.0;
        for (int u = 0; u < P; u++) {
            i128 v = (i128)xi * (i128)E[u]; long long m = (long long)(v % (i128)Q); if (m < 0) m += Q;
            pr *= fabs(cos(M_PI * ((double)m / (double)Q)));
            if (pr == 0) break;
        }
        LLa += pr; if (xi % P) LLu += pr;
        if (pr > mx) { mx = pr; am = xi; }
    }
    Lu = (double)LLu; La = (double)LLa; J->Lunit = Lu; J->Lall = La; J->mx = mx; J->argmx = am; return 0;
}

static u64 FACT; // (p-1)!
static void *intworker(void *arg) {
    job_t *J = arg; long double acc = 0;
    double fact[64]; fact[0] = 1; for (int u = 1; u < P; u++) fact[u] = fact[u - 1] * u;
    for (u64 k = (u64)J->id; k < FACT; k += NT) {
        double s = 0;
        for (int g = 0; g < NGL; g++) {
            double t = GLx[g], c0 = cos(M_PI * t), pr = c0 * c0;
            double Th = (double)k + t;
            for (int u = 2; u < P; u++) pr *= fabs(cos(M_PI * (Th / fact[u])));
            s += GLw[g] * pr;
        }
        acc += s;
    }
    J->I = (double)acc; return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: gatesum p imax nthreads [ngl]\n"); return 1; }
    P = atoi(argv[1]); int imax = atoi(argv[2]); NT = atoi(argv[3]); NGL = argc > 4 ? atoi(argv[4]) : 0;
    long long f = 1; for (int j = 1; j < P; j++) f *= j; FACT = (u64)f;
    for (int u = 0; u < P; u++) { long long uf = 1; for (int j = 1; j <= u; j++) uf *= j; E[u] = (u % 2 ? -1 : 1) * (f / uf); }
    printf("# p=%d  e_u = (-1)^u (p-1)!/u!:", P); for (int u = 0; u < P; u++) printf(" %lld", E[u]); printf("\n");
    pthread_t th[64]; job_t J[64];
    for (int i = 1; i <= imax; i++) {
        Q = 1; for (int j = 0; j < i; j++) Q *= P;
        for (int t = 0; t < NT; t++) { J[t].id = t; pthread_create(&th[t], 0, sumworker, &J[t]); }
        double Lu = 0, La = 0, mx = 0; u64 am = 0;
        for (int t = 0; t < NT; t++) { pthread_join(th[t], 0); Lu += J[t].Lunit; La += J[t].Lall; if (J[t].mx > mx) { mx = J[t].mx; am = J[t].argmx; } }
        double units = (double)Q * (1.0 - 1.0 / P);
        printf("p=%d i=%d p^i=%llu Lunit=%.10g Lall=%.10g Lunit/units=%.10g Lall/p^i=%.10g maxterm=%.6g argmax=%llu randomphase_budget=%.10g\n",
               P, i, (unsigned long long)Q, Lu, La, Lu / units, La / (double)Q, mx, (unsigned long long)am, units * pow(2.0 / M_PI, P));
        fflush(stdout);
    }
    if (NGL > 0) {
        gauss_legendre(NGL);
        for (int t = 0; t < NT; t++) { J[t].id = t; pthread_create(&th[t], 0, intworker, &J[t]); }
        long double I = 0; for (int t = 0; t < NT; t++) { pthread_join(th[t], 0); I += J[t].I; }
        I /= (long double)FACT;
        printf("p=%d integral I_p=%.12Lg (ngl=%d, %llu unit pieces)  (2/pi)^p=%.12g  (2/pi)^(p-2)/2=%.12g\n", P, I, NGL, (unsigned long long)FACT, pow(2.0 / M_PI, P), 0.5 * pow(2.0 / M_PI, P - 2));
    }
    return 0;
}
