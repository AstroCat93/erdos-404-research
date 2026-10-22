/* l2mc.c -- Monte Carlo for the odd-p quenched martingale (track T1a, round 3; writeup.md Sec. 6).
 *
 *   M_n(x) = 2^{-n} p^{V_n(x)} sum_{e alive at n, lambda_e <= L} rho_n(e),
 *   rho_n(e) = p^{lambda} a_n^{(lambda)}(tau_n(e) mod p^lambda),
 *   a_n^{(lambda)}(t) = P_{f in {0,1}^{p lambda}}( sum_{i < p lambda} f_i pi_{n+i}/pi_n == t  (mod p^lambda) ).
 *
 * The atom A = x0 + p^{m0} Z_p, m0 = V_{n0}(x0), is fixed by the seed; x is sampled uniformly in A
 * (digits m0..P-1 uniform).  For window times n_0 < n_1 < ... (n_{l+1} = floor(ratio * n_l)) we record
 *   E[M_l], E[M_l^2], E[(M_l - M_{l-1})^2], P(M_l = 0), P(population empty), E|P_{n_l}|, E[2^{-n} p^{V_n}],
 * and the fraction of samples violating the window hypotheses (W2) D+L <= m - M_n, (W3) L < m - M_N, M_N < m.
 * All exact integer arithmetic mod p^P (p^P < 2^64; 128-bit products); M in double.
 *
 * Usage: l2mc seed p L P n0 nwin ratio samples [maxpop]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 rng_s[2];
static u64 rng(void){ u64 s1=rng_s[0], s0=rng_s[1]; rng_s[0]=s0; s1^=s1<<23; rng_s[1]=s1^s0^(s1>>17)^(s0>>26); return rng_s[1]+s0; }

static u64 mulmod(u64 a, u64 b, u64 m){ return (u64)(((u128)a*b)%m); }
static u64 powmod(u64 a, u64 e, u64 m){ u64 r=1%m; a%=m; while(e){ if(e&1) r=mulmod(r,a,m); a=mulmod(a,a,m); e>>=1;} return r; }
/* inverse of unit u mod p^k via Newton iteration (u odd prime power modulus) */
static u64 invmod_pk(u64 u, u64 m, u64 p){
    /* phi(p^k) = p^k - p^{k-1}; use pow(u, phi-1) */
    u64 phi = m - m/p;
    return powmod(u, phi-1, m);
}
static int vp_u64(u64 a, u64 p, int cap){ if(a==0) return cap; int k=0; while(a%p==0){ a/=p; k++; if(k>=cap) return cap;} return k; }

typedef struct { u64 tau; uint8_t sp; } path_t;   /* tau mod p^prec ; sp = S'_e mod p^{L+1} */

int main(int argc, char **argv){
    if(argc<9){ fprintf(stderr,"usage: l2mc seed p L P n0 nwin ratio samples [maxpop]\n"); return 1; }
    u64 seed=strtoull(argv[1],0,10); int p=atoi(argv[2]); int L=atoi(argv[3]); int P=atoi(argv[4]);
    int n0=atoi(argv[5]); int nwin=atoi(argv[6]); double ratio=atof(argv[7]); long samples=atol(argv[8]);
    size_t maxpop = argc>9 ? (size_t)atol(argv[9]) : 20000000;
    rng_s[0]=seed*0x9E3779B97F4A7C15ULL+1; rng_s[1]=seed^0xD1B54A32D192ED03ULL; for(int i=0;i<20;i++) rng();

    u64 pw[64]; pw[0]=1; for(int i=1;i<=P;i++) pw[i]=pw[i-1]*(u64)p;   /* caller ensures p^P < 2^64 */
    u64 MOD=pw[P];
    int wins[64]; wins[0]=n0; for(int l=1;l<=nwin;l++) wins[l]=(int)floor(ratio*wins[l-1]);
    int nmax=wins[nwin];

    /* atom: choose x0 at random avoiding the trivial class x == -1 mod p; m0 = V_{n0}(x0) */
    u64 x0; int m0;
    for(;;){ x0 = rng()%MOD; if(x0%p==(u64)(p-1)) continue; m0=0; for(int i=1;i<=n0;i++) m0+=vp_u64((x0+i)%MOD,p,P); if(m0+L+4 < P) break; }
    u64 xfix = x0 % pw[m0];
    printf("# p=%d L=%d P=%d n0=%d nwin=%d ratio=%.3f samples=%ld  atom: x0 mod p^%d = %llu  (x0 mod p^3 = %llu)\n",
           p,L,P,n0,nwin,ratio,samples,m0,(unsigned long long)xfix,(unsigned long long)(x0%pw[3]));
    printf("# windows:"); for(int l=0;l<=nwin;l++) printf(" %d",wins[l]); printf("\n");

    path_t *A=malloc(maxpop*sizeof(path_t)), *B=malloc(maxpop*sizeof(path_t));
    if(!A||!B){ fprintf(stderr,"alloc fail\n"); return 2; }
    /* accumulators per window */
    double sM[64]={0}, sM2[64]={0}, sInc2[64]={0}, sPop[64]={0}, sNorm[64]={0}, sV[64]={0}, sMmax[64]={0};
    long zeroM[64]={0}, emptyP[64]={0}, hypfail[64]={0}, overflow=0;
    double *aTab = malloc(sizeof(double)*(size_t)(L+1)*pw[L>0?L:0]*(nwin+1)); /* a_n^{(lam)}(t) for lam<=L at window times */
    /* a_n^{(lam)} depends on x mod p^lam only: constant on the atom (lam <= L < m0). Precompute per window. */
    for(int l=0;l<=nwin;l++) for(int lam=1;lam<=L;lam++){
        u64 md=pw[lam]; int K=p*lam;
        double *cnt=calloc(md,sizeof(double)), *nw=calloc(md,sizeof(double)); cnt[0]=1;
        u64 prod=1;
        for(int i=0;i<K;i++){ u64 term=prod%md; memset(nw,0,md*sizeof(double));
            for(u64 r=0;r<md;r++){ if(cnt[r]==0) continue; nw[r]+=cnt[r]; nw[(r+term)%md]+=cnt[r]; }
            memcpy(cnt,nw,md*sizeof(double)); prod = mulmod(prod,(xfix+wins[l]+i+1)%md,md); }
        double tot=ldexp(1.0,K);
        for(u64 t=0;t<md;t++) aTab[((size_t)l*(L+1)+lam)*pw[L]+t]=cnt[t]/tot;
        free(cnt); free(nw);
    }

    for(long s=0;s<samples;s++){
        u64 x = (xfix + (u64)(rng()%(MOD/pw[m0]))*pw[m0]) % MOD;
        /* step data */
        size_t np=1; A[0].tau=0; A[0].sp=0; int prec=P; int V=0;
        u64 pi_mod=1;      /* pi_j mod p^{L+1} */
        u64 dpi_mod=0;     /* pi_j' mod p^{L+1} */
        u64 mdL=pw[L+1];
        int Mn=0; int wi=0; double Mprev=0; int ok=1;
        int Mwin[64]; int Vwin[64];
        for(int j=0;j<=nmax;j++){
            if(j==wins[wi]){
                /* evaluate martingale at time j: prec = P - V_j */
                double sum=0; size_t cntL=0;
                for(size_t i=0;i<np;i++){
                    int lam=vp_u64(A[i].sp,p,L+1); if(lam>L) continue; cntL++;
                    double rho;
                    if(lam==0) rho=1.0; else { u64 t=A[i].tau%pw[lam]; rho=pw[lam]*aTab[((size_t)wi*(L+1)+lam)*pw[L]+t]; }
                    sum+=rho;
                }
                double norm=exp(-j*log(2.0)+V*log((double)p));
                double M=norm*sum;
                sM[wi]+=M; sM2[wi]+=M*M; sPop[wi]+=(double)np; sNorm[wi]+=norm; sV[wi]+=V; if(M>sMmax[wi]) sMmax[wi]=M;
                if(M==0) zeroM[wi]++; if(np==0) emptyP[wi]++;
                if(wi>0) sInc2[wi]+=(M-Mprev)*(M-Mprev);
                Mprev=M; Mwin[wi]=Mn; Vwin[wi]=V;
                /* hypotheses for the window [wins[wi-1], wins[wi]) now checkable: need M_N (=Mn now), m=V_{n}, D */
                if(wi>0){ int m=Vwin[wi-1], D=V-m, MnPrev=Mwin[wi-1], MN=Mn;
                    if(!(D+L<=m-MnPrev && L<m-MN && MN<m)) hypfail[wi]++; }
                wi++; if(wi>nwin) break;
            }
            /* step j -> j+1 */
            u64 xj=(x+j+1)%MOD; int d=vp_u64(xj,p,P); if(d>Mn) Mn=d;
            if(prec-d<=L){ ok=0; overflow++; break; }
            u64 unit=xj/pw[d]; u64 newmod=pw[prec-d]; u64 uinv=invmod_pk(unit%newmod,newmod,p);
            u64 oldmod=pw[prec];
            size_t nb=0;
            for(size_t i=0;i<np;i++){
                u64 tau=A[i].tau;
                for(int e=(j==0?1:0); e<=1; e++){
                    u64 t=(tau+oldmod-(u64)e)%oldmod;
                    if(d && t%pw[d]) continue;
                    u64 nt=mulmod((t/pw[d])%newmod,uinv,newmod);
                    if(nb>=maxpop){ ok=0; break; }
                    B[nb].tau=nt; B[nb].sp=(uint8_t)((A[i].sp + (e? dpi_mod:0))%mdL); nb++;
                }
                if(!ok) break;
            }
            if(!ok){ overflow++; break; }
            /* update pi_j', pi_j mod p^{L+1}: pi_{j+1} = pi_j (x+j+1), pi'_{j+1} = pi'_j (x+j+1) + pi_j */
            u64 xjL=(x+j+1)%mdL; dpi_mod=(mulmod(dpi_mod,xjL,mdL)+pi_mod)%mdL; pi_mod=mulmod(pi_mod,xjL,mdL);
            path_t *T=A; A=B; B=T; np=nb; prec-=d; V+=d;
        }
        if(!ok){ s--; continue; }   /* resample (rare) */
    }
    printf("# overflow/precision resamples: %ld\n", overflow);
    printf("#  l    n   E[V_n]   E|P_n|      E[norm]     E[M]      E[M^2]     Var[M]   E[(M_l-M_{l-1})^2]  max M   P(M=0)  P(pop=0)  hypfail\n");
    for(int l=0;l<=nwin;l++){
        double EM=sM[l]/samples, EM2=sM2[l]/samples;
        printf("%3d %4d  %7.2f %10.1f  %11.4e  %8.5f  %9.5f  %9.5f  %12.5e  %7.3f  %6.4f  %6.4f   %6.4f\n",
               l,wins[l],sV[l]/samples,sPop[l]/samples,sNorm[l]/samples,EM,EM2,EM2-EM*EM,sInc2[l]/samples,sMmax[l],
               (double)zeroM[l]/samples,(double)emptyP[l]/samples,(double)hypfail[l]/samples);
    }
    free(A); free(B); free(aTab);
    return 0;
}
