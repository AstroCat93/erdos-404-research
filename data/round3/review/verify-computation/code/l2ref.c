/* Referee re-implementation of the exact L^2 masses C_k (Computation 11.43), from the definition
   C_k = p^k P(sum_n eta_n x_n = 0 mod p^k) = p^k sum_r N(r)^2 / 4^M,
   x_n = n!/p^{v(N0!)}, n >= N0, only elements with v(x_n) < kmax kept (M of them);
   N(r) = #subsets with sum = r mod p^kmax (exact uint32 counts, DP with two arrays);
   lower levels by folding.  T3a's l2dp.c not read.
   Usage: l2ref p N0 kmax     prints: k M S_k  (S_k = sum_r Nk(r)^2, Nk folded counts)  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
#ifdef DBL
typedef double cnt_t;
#elif defined(WIDE)
typedef uint64_t cnt_t;
#else
typedef uint32_t cnt_t;
#endif
static void pr(u128 x){ char b[64]; int i=63; b[i]=0; if(!x){printf("0");return;} while(x){b[--i]='0'+(int)(x%10); x/=10;} printf("%s",b+i);}
int main(int argc,char**argv){
  int p=atoi(argv[1]); long N0=atol(argv[2]); int kmax=atoi(argv[3]);
  u64 m=1; for(int i=0;i<kmax;i++) m*=p;
  /* v(N0!) */
  int e0=0; { long n=N0; while(n){ n/=p; e0+=n; } }
  /* elements */
  u64 xs[4096]; int M=0; int vlist[4096];
  /* unit part of n! mod m and valuation, iteratively from n=1 */
  u64 u=1; int v=0;
  for(long n=1; ; n++){
    long t=n; int vn=0; while(t%p==0){t/=p; vn++;}
    v+=vn; u=(u64)(((u128)u*(u64)(t%(long)m))%m);
    if(n<N0) continue;
    int rel=v-e0; if(rel>=kmax) break;
    u64 pw=1; for(int i=0;i<rel;i++) pw*=p;
    xs[M]=(u64)(((u128)u*pw)%m); vlist[M]=rel; M++;
  }
  fprintf(stderr,"p=%d N0=%ld kmax=%d e0=%d M=%d m=%llu\n",p,N0,kmax,e0,M,(unsigned long long)m);
  cnt_t *A=calloc(m,sizeof(cnt_t)), *B=calloc(m,sizeof(cnt_t));
  if(sizeof(cnt_t)==4 && M>31 && 0){fprintf(stderr,"M>31 needs -DWIDE\n");return 1;}
  if(!A||!B){fprintf(stderr,"alloc fail\n");return 1;}
  A[0]=1;
  for(int i=0;i<M;i++){
    u64 x=xs[i];
    /* B[r] = A[r] + A[r-x mod m] */
    #ifdef DBL
    for(u64 r=0;r<x;r++) B[r]=0.5*(A[r]+A[r+m-x]);
    for(u64 r=x;r<m;r++) B[r]=0.5*(A[r]+A[r-x]);
#else
    for(u64 r=0;r<x;r++) B[r]=A[r]+A[r+m-x];
    for(u64 r=x;r<m;r++) B[r]=A[r]+A[r-x];
#endif
    cnt_t*T=A;A=B;B=T;
  }
  free(B);
  /* levels: fold */
  for(int k=kmax;k>=1;k--){
    u64 mk=1; for(int i=0;i<k;i++) mk*=p;
#ifdef DBL
    { long double Sd=0; if(k==kmax){ for(u64 r=0;r<m;r++) Sd+=(long double)A[r]*A[r]; }
      else { double *Fd=calloc(mk,8); for(u64 r=0;r<m;r++) Fd[r%mk]+=A[r]; for(u64 r=0;r<mk;r++) Sd+=(long double)Fd[r]*Fd[r]; free(Fd);} 
      printf("k=%d M=%d C_k-1=%.10Le (double DP)\n",k,M,(long double)mk*Sd-1.0L); continue; }
#endif
    u128 S=0;
    if(k==kmax){ for(u64 r=0;r<m;r++) S+=(u128)A[r]*A[r]; }
    else {
      u64 *F=calloc(mk,8);
      for(u64 r=0;r<m;r++) F[r%mk]+=A[r];
      for(u64 r=0;r<mk;r++) S+=(u128)F[r]*F[r];
      free(F);
    }
    printf("k=%d M=%d S=",k,M); pr(S); printf("\n");
  }
  return 0;
}
