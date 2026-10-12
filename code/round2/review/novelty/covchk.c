/* independent referee check: subset sums of y_i=prod_{s<=i}(p^t K - (H-s)) mod p^M, M=t+v_p((H-1)!).
   byte-array dynamic programme; prints number of missed residues. usage: covchk p t H K */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int main(int argc,char**argv){
  long p=atol(argv[1]),t=atol(argv[2]),H=atol(argv[3]),K=atol(argv[4]);
  long c=0; for(long i=1;i<=H-1;i++){long x=i; while(x%p==0){c++;x/=p;}}
  long M=t+c; unsigned long long N=1; for(int i=0;i<M;i++) N*=p;
  unsigned long long X=1; for(int i=0;i<t;i++) X*=p; X=(X*(unsigned long long)K)%N;
  unsigned char *S=calloc(N,1),*T=malloc(N); S[0]=1;
  unsigned __int128 y=1;
  for(long i=0;i<H;i++){
    if(i>0){ unsigned long long f=(X+N-(unsigned long long)((H-i)%N))%N; y=(y*f)%N; }
    unsigned long long s=(unsigned long long)y;
    if(s==0) continue;
    /* T[x]=S[x] | S[x-s mod N] */
    memcpy(T,S,N);
    for(unsigned long long x=0;x<N-s;x++) T[x+s]|=S[x];
    for(unsigned long long x=N-s;x<N;x++) T[x+s-N]|=S[x];
    unsigned char*tmp=S;S=T;T=tmp;
  }
  unsigned long long miss=0,first=0; for(unsigned long long x=0;x<N;x++) if(!S[x]){ if(!miss) first=x; miss++;}
  printf("p=%ld t=%ld H=%ld K=%ld M=%ld N=%llu missed=%llu first=%llu\n",p,t,H,K,M,N,miss,first);
  return 0;}
