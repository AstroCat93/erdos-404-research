/* smc2.c -- sequential Monte Carlo for the L^2 mass C_k(2,N0) at p = 2  [HEURISTIC NUMERICS; track T3a round 3].
 * Same algorithm as smc_l2.py (exact carry recursion of Theorem 1, particle filter with systematic resampling),
 * specialised to p = 2 with fixed-width multiprecision carries (W 64-bit words, so K <= 64W - 16).
 * Elements x_n = n!/2^{v(N0!)}, n >= N0; level a = v(n!) - v(N0!); unit U(n) = n!/2^{v(n!)} mod 2^{64W}.
 * Carry c (meaningful in bits [0, K-a)) survives the level group iff c + y == 0 mod 2^J (J = next level - a),
 * y = sum_{group} eta_n U(n), eta in {-1,0,1} with weights 1,2,1; then c <- (c+y) >> J.
 * Output: "lvl a' C_est D_est J" per group, final line "# final".  Usage: smc2 N0 K P seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define W 16
typedef struct { uint64_t w[W]; } big;
static uint64_t rs[4];
static inline uint64_t rotl(const uint64_t x, int k){ return (x<<k)|(x>>(64-k)); }
static uint64_t nxt(void){ const uint64_t r=rotl(rs[1]*5,7)*9, t=rs[1]<<17; rs[2]^=rs[0]; rs[3]^=rs[1]; rs[1]^=rs[2]; rs[0]^=rs[3]; rs[2]^=t; rs[3]=rotl(rs[3],45); return r; }
static double urand(void){ return (nxt()>>11)*0x1.0p-53; }
static void add(big*r,const big*a,const big*b){ unsigned __int128 c=0; for(int i=0;i<W;i++){ c+=(unsigned __int128)a->w[i]+b->w[i]; r->w[i]=(uint64_t)c; c>>=64; } }
static void neg(big*r,const big*a){ big t; for(int i=0;i<W;i++) t.w[i]=~a->w[i]; big one; memset(&one,0,sizeof one); one.w[0]=1; add(r,&t,&one); }
static void shr(big*r,int J){ /* J < 64 */ for(int i=0;i<W;i++){ uint64_t hi = (i+1<W)? r->w[i+1] : 0; r->w[i] = (r->w[i]>>J) | (J? (hi<<(64-J)) : 0); } }
static void mulsmall(big*r,uint64_t m){ unsigned __int128 c=0; for(int i=0;i<W;i++){ c+=(unsigned __int128)r->w[i]*m; r->w[i]=(uint64_t)c; c>>=64; } }
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage: smc2 N0 K P seed\n");return 1;}
  long N0=atol(argv[1]); int K=atoi(argv[2]); long P=atol(argv[3]); uint64_t seed=strtoull(argv[4],0,10);
  if(K>64*W-16){fprintf(stderr,"K too large\n");return 1;}
  rs[0]=seed*0x9E3779B97F4A7C15ULL+1; rs[1]=seed^0xD1B54A32D192ED03ULL; rs[2]=0x8CB92BA72F3D8DD7ULL+seed; rs[3]=0xABCDEF1234567ULL^(seed<<7); for(int i=0;i<20;i++) nxt();
  /* elements */
  int cap=4*K+64, ng=0; int *glev=malloc(cap*sizeof(int)); int *gsz=malloc(cap*sizeof(int)); big *gu=malloc(2*cap*sizeof(big));
  big U; memset(&U,0,sizeof U); U.w[0]=1; long v=0, e0=-1;
  for(long n=1;;n++){
    long m=n; while(!(m&1)){ m>>=1; v++; } mulsmall(&U,(uint64_t)m);
    if(n<N0) continue;
    if(e0<0) e0=v;
    long a=v-e0; if(a>=K) break;
    if(ng>0 && glev[ng-1]==a){ if(gsz[ng-1]>=2){fprintf(stderr,"group >2\n");return 1;} gu[2*(ng-1)+gsz[ng-1]]=U; gsz[ng-1]++; }
    else { glev[ng]=(int)a; gsz[ng]=1; gu[2*ng]=U; ng++; if(ng>=cap){fprintf(stderr,"cap\n");return 1;} }
  }
  big *C=calloc(P,sizeof(big)), *Cn=malloc(P*sizeof(big)); double *f=malloc(P*sizeof(double));
  if(!C||!Cn||!f){fprintf(stderr,"alloc\n");return 1;}
  double logZ=0;
  printf("# p=2 N0=%ld K=%d P=%ld seed=%llu groups=%d\n",N0,K,P,(unsigned long long)seed,ng);
  for(int g=0; g<ng; g++){
    int a=glev[g], b=(g+1<ng)?glev[g+1]:K, J=b-a; if(J>=64){fprintf(stderr,"J>=64\n");return 1;}
    uint64_t mask = (J==64)?~0ULL:((1ULL<<J)-1);
    /* configs */
    int nc=1; big y[9]; int wt[9]; memset(&y[0],0,sizeof(big)); wt[0]=1;
    for(int i=0;i<gsz[g];i++){
      big u=gu[2*g+i], mu; neg(&mu,&u);
      int nn=0; big yy[9]; int ww[9];
      for(int c=0;c<nc;c++){ yy[nn]=y[c]; ww[nn]=2*wt[c]; nn++; add(&yy[nn],&y[c],&u); ww[nn]=wt[c]; nn++; add(&yy[nn],&y[c],&mu); ww[nn]=wt[c]; nn++; }
      nc=nn; memcpy(y,yy,sizeof(big)*nn); memcpy(wt,ww,sizeof(int)*nn);
    }
    int tot=1; for(int i=0;i<gsz[g];i++) tot*=4;
    double sf=0;
    for(long i=0;i<P;i++){
      uint64_t low=C[i].w[0]&mask; int cw=0; int ok[9]; int no=0;
      for(int c=0;c<nc;c++) if(((low+(y[c].w[0]&mask))&mask)==0){ ok[no++]=c; cw+=wt[c]; }
      f[i]=(double)cw/tot; sf+=f[i];
      if(cw){ double r=urand()*cw; int s=0, acc=wt[ok[0]]; while(acc<=r && s<no-1){ s++; acc+=wt[ok[s]]; }
        add(&Cn[i],&C[i],&y[ok[s]]); shr(&Cn[i],J); }
      else memset(&Cn[i],0,sizeof(big));
    }
    if(sf==0){ printf("EXTINCT at group %d\n",g); return 0; }
    double mf=sf/P; logZ+=log(mf);
    /* systematic resampling */
    double step=sf/P, u0=urand()*step, cum=0; long k=0;
    for(long i=0;i<P && k<P;i++){ cum+=f[i]; while(k<P && u0+k*step<cum){ C[k]=Cn[i]; k++; } }
    while(k<P){ C[k]=C[k-1]; k++; }
    printf("lvl %d %.10g %.6e %d\n", b, exp(b*log(2.0)+logZ), ldexp(mf,J)-1, J);
  }
  printf("# final C_%d estimate %.10g (log %.6f)\n", K, exp(K*log(2.0)+logZ), K*log(2.0)+logZ);
  return 0;
}
