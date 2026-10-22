// annealed.c -- exact per-class subset counts N_G(x) = #{B subset [1,M_G] : p^G | 1 + sum_{b in B} pi_b(x)},
// for every class x mod p^G, by a carry DP over residues (count arrays).
// M_G = min{M : v_p((M+1)!) >= G}  (= min M such that pi_b == 0 mod p^G for all x and all b > M).
// Usage: annealed p G chunk nchunks     (classes x with x % nchunks == chunk)
// Output: one line  p G M_G nclasses survivors sumN sumN2 maxN sumN3(ld) sumN4(ld)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static u64 pw[64]; static int p, G, MG;
static u64 *cntA, *cntB;

static int vp_fact(u64 b){ int v=0; u64 q=b; while(q){ q/=p; v+=q; } return v; }

static u64 count_class(u64 x){
    int r=G; int n=0; u64 om=1; int first=1;
    memset(cntA,0,sizeof(u64)*pw[G]); cntA[0]=1;
    while(1){
        u64 m=x+n+1; int t=0; u64 pr=pw[r];
        if(m%pr==0) t=r; else { while(m%p==0){ m/=p; t++; } }
        if(t>=r){
            u128 N=0;
            for(u64 c=0;c<pr;c++){ u64 k=cntA[c]; if(!k) continue;
                for(int e=first;e<=1;e++){ u64 y=c+(e?om:0); if(y>=pr) y-=pr; if(y==0) N+=k; } }
            // free terms b in [n+1, MG]: MG-n of them
            if(N==0) return 0;
            int fr=MG-n; if(fr<0){ fprintf(stderr,"bug fr<0\n"); exit(1); }
            u128 res=N<<fr; if(res>>64){ fprintf(stderr,"overflow N\n"); exit(1);} return (u64)res;
        }
        int rn=r-t; u64 prn=pw[rn]; u64 pt=pw[t];
        memset(cntB,0,sizeof(u64)*prn);
        int any=0;
        for(u64 c=0;c<pr;c++){ u64 k=cntA[c]; if(!k) continue;
            for(int e=first;e<=1;e++){ u64 y=c+(e?om:0); if(y>=pr) y-=pr; if(y%pt) continue; cntB[y/pt]+=k; any=1; } }
        if(!any) return 0;
        u64 u=((x+n+1)/pt)%prn; om=(u128)om*u%prn;
        u64 *tmp=cntA; cntA=cntB; cntB=tmp; r=rn; n++; first=0;
    }
}
int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: annealed p G chunk nchunks\n"); return 1; }
    p=atoi(argv[1]); G=atoi(argv[2]); int chunk=atoi(argv[3]), nch=atoi(argv[4]);
    pw[0]=1; for(int i=1;i<64;i++){ pw[i]=pw[i-1]*p; if(pw[i]<pw[i-1]) break; }
    MG=0; while(vp_fact(MG+1)<G) MG++;
    cntA=malloc(sizeof(u64)*pw[G]); cntB=malloc(sizeof(u64)*pw[G]);
    u128 sN=0,sN2=0; long double sN3=0,sN4=0; u64 maxN=0; u64 surv=0,ncl=0;
    for(u64 x=chunk;x<pw[G];x+=nch){ u64 N=count_class(x); ncl++;
        if(N){ surv++; sN+=N; sN2+=(u128)N*N; long double d=(long double)N; sN3+=d*d*d; sN4+=d*d*d*d; if(N>maxN) maxN=N; } }
    char b1[64],b2[64]; 
    { u128 v=sN; int i=63; b1[i]=0; if(!v) b1[--i]='0'; while(v){ b1[--i]='0'+(int)(v%10); v/=10; } memmove(b1,b1+i,64-i); }
    { u128 v=sN2; int i=63; b2[i]=0; if(!v) b2[--i]='0'; while(v){ b2[--i]='0'+(int)(v%10); v/=10; } memmove(b2,b2+i,64-i); }
    printf("%d %d %d %llu %llu %s %s %llu %.6Le %.6Le\n",p,G,MG,(unsigned long long)ncl,(unsigned long long)surv,b1,b2,(unsigned long long)maxN,sN3,sN4);
    return 0;
}
