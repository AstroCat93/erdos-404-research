// independent: does subset-sum set of {(-1)^u/u! : u<p} cover Z/p^L ? byte-per-residue would be too big; use bits.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static u64 inv(u64 a,u64 m){__int128 t=0,nt=1,r=m,nr=a%m;while(nr){__int128 q=r/nr,x;x=t-q*nt;t=nt;nt=x;x=r-q*nr;r=nr;nr=x;}if(t<0)t+=m;return (u64)t;}
static inline int gb(const u64*S,u64 i){return (S[i>>6]>>(i&63))&1;}
int main(int c,char**v){u64 p=atoll(v[1]);int L=atoi(v[2]);u64 M=1;for(int i=0;i<L;i++)M*=p;
 u64 nw=(M+63)/64; u64*S=calloc(nw,8),*T=calloc(nw,8); S[0]=1; u64 fact=1;
 for(u64 u=0;u<p;u++){ if(u>0) fact=(u64)((u128)fact*u%M);
   u64 x=inv(fact,M); if(u&1) x=(M-x)%M; if(x==0) continue;
   // T = S | rot(S,x): T[i] |= S[(i-x) mod M]
   memcpy(T,S,nw*8);
   // generic: for target i, source i-x. Process by 64-bit words using a read of 64 bits at arbitrary src position with wrap.
   for(u64 w=0;w<nw;w++){ u64 i0=w*64; u64 val=0;
     u64 src=(i0>=x)?i0-x:i0+M-x;
     if(src+64<=M){ u64 q=src>>6,o=src&63; u64 lo=S[q]>>o; u64 hi=(o&&q+1<nw)?(S[q+1]<<(64-o)):0; val=lo|hi; }
     else { for(int b=0;b<64;b++){u64 i=i0+b; if(i>=M)break; u64 s=(i>=x)?i-x:i+M-x; if(gb(S,s)) val|=(u64)1<<b;} }
     T[w]|=val; }
   u64 rem=M&63; if(rem) T[nw-1]&=(((u64)1<<rem)-1);
   u64*tmp=S;S=T;T=tmp; }
 u64 cnt=0; for(u64 w=0;w<nw;w++) cnt+=__builtin_popcountll(S[w]);
 printf("p=%llu L=%d M=%llu covered=%llu %s\n",p,L,M,cnt,cnt==M?"FULL":"partial"); return 0;}
