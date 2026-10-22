/* Referee brute force of annealed moments (Computation 11.55) for small (p,G):
   N(x) = #{B subset [1,M_G] : p^G | 1 + sum_{b in B} pi_b(x)}, for every class x mod p^G,
   by a subset-count DP over Z/p^G.  M_G = max{b : v_p(b!) < G}.  Prints survivors (N>0), sumN, sumN2, maxN,
   and N(-2 mod p^G) vs 2^{M_G-1} (Prop. 11.53).   Usage: annref p G  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static void pr(u128 x){ char b[64]; int i=63; b[i]=0; if(!x){printf("0");return;} while(x){b[--i]='0'+(int)(x%10); x/=10;} printf("%s",b+i);}
int main(int c,char**v){ int p=atoi(v[1]), G=atoi(v[2]); u64 m=1; for(int i=0;i<G;i++) m*=p;
  int MG=0; { for(int b=1;;b++){ int s=0; int n=b; while(n){n/=p; s+=n;} if(s<G) MG=b; else if(s>=G && b>p*G) break; } }
  u64 *A=malloc(m*8), *B=malloc(m*8); u64 surv=0, maxN=0; u128 sN=0, sN2=0; u64 Nm2=0;
  for(u64 x=0;x<m;x++){
    memset(A,0,m*8); A[0]=1; u64 pib=1;
    for(int b=1;b<=MG;b++){ pib=(u64)(((u128)pib*((x+b)%m))%m);
      for(u64 r=0;r<pib;r++) B[r]=A[r]+A[r+m-pib]; for(u64 r=pib;r<m;r++) B[r]=A[r]+A[r-pib]; u64*T=A;A=B;B=T; }
    u64 N=A[(m-1)%m]; /* sum = -1 */
    if(N){surv++;} sN+=N; sN2+=(u128)N*N; if(N>maxN) maxN=N; if(x==(m-2)%m) Nm2=N; }
  printf("p=%d G=%d M_G=%d classes=%llu surviving=%llu sumN=",p,G,MG,(unsigned long long)m,(unsigned long long)surv); pr(sN); printf(" sumN2="); pr(sN2);
  printf(" maxN=%llu  N(-2)=%llu  2^(M_G-1)=%llu\n",(unsigned long long)maxN,(unsigned long long)Nm2,(unsigned long long)(1ULL<<(MG-1))); return 0; }
