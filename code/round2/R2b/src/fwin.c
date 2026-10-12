/*
 * fwin.c -- Fourier L^1 / L^2 diagnostics for the gate windows of note.md Thm 3.12.
 *
 * Window y_i = prod_{s=1}^{i} (X - (H-s)), 0 <= i < H, X = p^t K (mod p^M), M = t + c + k.
 * For each nonzero frequency xi in Z/p^M computes  F(xi) = prod_i |cos(pi xi y_i / p^M)|
 * (= |Fourier coefficient| of the uniform measure on the 2^H subset sums) and reports
 *   L1 = sum_{xi != 0} F(xi),  L2 = sum_{xi != 0} F(xi)^2,
 *   the random-phase prediction R1 = (p^M - 1) (2/pi)^H, R2 = (p^M - 1) (1/2)^H... (E cos^2 = 1/2),
 *   and the largest F(xi) with its xi and p-adic valuation of xi.
 * Floating point: diagnostic only (not a certificate).
 * L1 < 1 would certify coverage (Prop 3.13(b) of note.md); missing-residue fraction <= L2.
 *
 * usage: fwin p t H K [k=0] [nsplit=1 split=0]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

static int vpf(long long n,long long p){ int s=0; while(n){ n/=p; s+=(int)n; } return s; }

int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage: %s p t H K [k] [nsplit split]\n",argv[0]); return 1; }
  long long p=atoll(argv[1]); int t=atoi(argv[2]); int H=atoi(argv[3]); long long K=atoll(argv[4]);
  int k=argc>5?atoi(argv[5]):0; int nsplit=argc>6?atoi(argv[6]):1, split=argc>7?atoi(argv[7]):0;
  int c=vpf(H-1,p), M=t+c+k; uint64_t Q=1; for(int i=0;i<M;i++) Q*=(uint64_t)p;
  uint64_t X=1; for(int i=0;i<t;i++) X=(X*(uint64_t)p)%Q;
  long long Km=K%(long long)Q; if(Km<0) Km+=(long long)Q; X=(uint64_t)(((unsigned __int128)X*(uint64_t)Km)%Q);
  uint64_t *y=malloc(H*8); uint64_t yy=1;
  for(int i=0;i<H;i++){ if(i>0){ uint64_t f=(X+Q-((uint64_t)(H-i)%Q))%Q; yy=(uint64_t)(((unsigned __int128)yy*f)%Q);} y[i]=yy; }
  double L1=0,L2=0,mx=0; uint64_t argmx=0;
  double invQ=1.0/(double)Q;
  /* frequencies xi = 1..Q-1, split by xi % nsplit */
  uint64_t *th=malloc(H*8);
  uint64_t start=(uint64_t)split; if(start==0) start=nsplit; /* skip xi=0 */
  for(int i=0;i<H;i++) th[i]=(uint64_t)(((unsigned __int128)y[i]*start)%Q);
  uint64_t *step=malloc(H*8); for(int i=0;i<H;i++) step[i]=(uint64_t)(((unsigned __int128)y[i]*(uint64_t)nsplit)%Q);
  for(uint64_t xi=start; xi<Q; xi+=nsplit){
    double pr=1.0;
    for(int i=0;i<H;i++){
      double a=(double)th[i]*invQ; /* in [0,1) */
      pr*=fabs(cos(M_PI*a));
      th[i]+=step[i]; if(th[i]>=Q) th[i]-=Q;
    }
    L1+=pr; L2+=pr*pr; if(pr>mx){ mx=pr; argmx=xi; }
  }
  int vx=0; { uint64_t z=argmx; while(z && z%p==0){ z/=p; vx++; } }
  double R1=((double)Q-1)*pow(2.0/M_PI,H), R2=((double)Q-1)*pow(0.5,H);
  printf("p=%lld t=%d H=%d K=%lld c=%d k=%d M=%d split=%d/%d  L1=%.6g L2=%.6g  R1=%.6g R2=%.6g  maxF=%.6g at xi=%llu (v=%d)\n",
         p,t,H,K,c,k,M,split,nsplit,L1,L2,R1,R2,mx,(unsigned long long)argmx,vx);
  return 0;
}
