/* shells.c -- referee's independent computation of the Fourier shell sums of §10.4.1.
 *   T_p(k)  = sum_{u unit mod p^k} prod_{n>=p, v(n!/p)<k} |cos(pi u x_n / p^k)|,  x_n = n!/p mod p^k
 *   T2_p(k) = same with cos^2 (for an exact Parseval cross-check).
 * Brute force over u (u and p^k-u give the same value, so only u < p^k/2 are summed, doubled).
 * Rigour: each factor is replaced by min(1, |cos|+1e-14) (cos computed in long double from an
 * exactly reduced phase in [0, 1/2]); the shell total is summed in long double and multiplied by
 * (1+1e-9).  Also prints a plain (no margin) value.
 * usage: shells p k [nthreads]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <pthread.h>

typedef unsigned __int128 u128;
static uint64_t p, Q; static int k, nf; static uint64_t xs[4096];
static int nth = 1;
typedef struct { int id; long double up, plain, sq; } job;

static void *work(void *arg){
    job *J = arg; long double up=0, pl=0, sq=0;
    uint64_t half = Q/2;
    for(uint64_t u = 1 + J->id; u <= half; u += nth){
        if(u % p == 0) continue;
        long double a=1, b=1, s=1;
        for(int i=0;i<nf;i++){
            uint64_t r = (uint64_t)(((u128)u * xs[i]) % Q);
            if(r > Q - r) r = Q - r;               /* |cos(pi r/Q)| symmetric; phase in [0,1/2] */
            long double cv = cosl(3.14159265358979323846264338327950288L * (long double)r / (long double)Q);
            long double cu = cv + 1e-14L; if(cu>1) cu=1;
            a *= cu; b *= cv; s *= cv*cv;
        }
        up += a; pl += b; sq += s;
    }
    J->up = 2*up; J->plain = 2*pl; J->sq = 2*sq;  /* u and Q-u */
    return NULL;
}
int main(int argc, char **argv){
    p = strtoull(argv[1],0,10); k = atoi(argv[2]); if(argc>3) nth = atoi(argv[3]);
    Q = 1; for(int i=0;i<k;i++) Q *= p;
    /* x_n = n!/p mod p^k for n >= p, while v(n!) - 1 < k.  Compute n!/p with the factor p removed
       exactly: maintain the p-free part and the valuation separately. */
    uint64_t unit = 1; int val = 0;  /* n! = p^val * unit (unit mod Q) */
    nf = 0;
    for(uint64_t n=1;;n++){
        uint64_t m = n; while(m % p == 0){ m/=p; val++; }
        unit = (uint64_t)(((u128)unit * (m % Q)) % Q);
        if(n < p) continue;
        int e = val - 1;                   /* valuation of n!/p */
        if(e >= k) break;
        uint64_t pe = 1; for(int i=0;i<e;i++) pe *= p;
        xs[nf++] = (uint64_t)(((u128)unit * pe) % Q);
    }
    pthread_t th[64]; job J[64];
    for(int i=0;i<nth;i++){ J[i].id=i; pthread_create(&th[i],0,work,&J[i]); }
    long double up=0, pl=0, sq=0;
    for(int i=0;i<nth;i++){ pthread_join(th[i],0); up+=J[i].up; pl+=J[i].plain; sq+=J[i].sq; }
    if(Q==2) { /* not used */ }
    printf("p=%llu k=%d factors=%d  T_plain=%.10Le  T_upper=%.10Le  T2_plain=%.12Le\n",
           (unsigned long long)p, k, nf, pl, up*(1+1e-9L), sq);
    return 0;
}
