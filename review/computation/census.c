/* Referee's independent class census: counts #{c mod p^G : g_p(c) >= G} for G=1..Gmax by DFS over the
   p-adic tree, testing EVERY child with an exact carry DP (no use of halving lemmas).
   usage: census p Gmax [print_children_stats]  ; requires p^(Gmax) < 2^62 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static int P, GMAX;
static u64 pw[70];
static int vp(u64 n){int k=0; while(n%P==0){n/=P;k++;} return k;}
/* hash set of u64 */
typedef struct { u64 *t; u64 cap; u64 n; } hset;
static void hs_init(hset*h,u64 cap){ h->cap=cap; h->t=malloc(cap*8); memset(h->t,0xff,cap*8); h->n=0; }
static void hs_clear(hset*h){ memset(h->t,0xff,h->cap*8); h->n=0; }
static u64 *usedpos; static u64 nused=0;
static int hs_add(hset*h,u64 x){ u64 i=(x*0x9E3779B97F4A7C15ULL)&(h->cap-1);
  while(h->t[i]!=~0ULL){ if(h->t[i]==x) return 0; i=(i+1)&(h->cap-1);} h->t[i]=x; h->n++; usedpos[nused++]=i; return 1; }
static void hs_reset(hset*h){ for(u64 k=0;k<nused;k++) h->t[usedpos[k]]=~0ULL; nused=0; h->n=0; }
static u64 *bufA,*bufB; static hset HS;
#define MAXST (1u<<24)
/* returns 1 iff g_p(a) >= K */
static int g_ge(u64 a,int K){
  if(K<=0) return 1;
  int w=vp(a+1); if(w>0) return 0;
  u64 N=a+1; u64 mod=pw[K];
  u64 u=(N/pw[vp(N)])%mod;  /* w=0 here */
  u64 *cur=bufA,*nxt=bufB; u64 nc=1, nn; cur[0]=1%mod;
  while(w<K){
    mod=pw[K-w];
    int d=vp(N+1);
    if(w+d>=K){ /* success iff some t has v(t)>=K-w... i.e. t==0 mod p^(K-w) */
      for(u64 i=0;i<nc;i++){ u64 s=cur[i]; if(s%mod==0) return 1; if((s+u)%mod==0) return 1; }
      return 0;
    }
    u64 pd=pw[d]; u64 nmod=pw[K-w-d];
    nn=0; hs_reset(&HS);
    for(u64 i=0;i<nc;i++){
      u64 s=cur[i];
      u64 t1=s, t2=(s+u)%mod;
      if(t1%pd==0){ u64 x=(t1/pd)%nmod; if(hs_add(&HS,x)) nxt[nn++]=x; }
      if(t2%pd==0){ u64 x=(t2/pd)%nmod; if(hs_add(&HS,x)) nxt[nn++]=x; }
      if(nn>=MAXST/2){fprintf(stderr,"too many states\n"); exit(3);}
    }
    if(nn==0) return 0;
    u64*tmp=cur;cur=nxt;nxt=tmp;nc=nn;
    w+=d; N++;
    u64 m2=pw[K-w];
    u64 q=N/pw[vp(N)];
    u=(u64)(((u128)(u%m2)*(q%m2))%m2);
  }
  return nc>0;
}
static u64 cnt[70]; static u64 kids[70][70];
static void dfs(u64 c,int G){ /* c mod p^G has g>=G; count, then children */
  cnt[G]++;
  if(G==GMAX) return;
  int k=0;
  for(int i=0;i<P;i++){
    u64 ch=c+(u64)i*pw[G]; u64 a= ch? ch : pw[G+1];
    if(g_ge(a,G+1)){ k++; dfs(ch,G+1); }
  }
  kids[G][k]++;
}
int main(int argc,char**argv){
  P=atoi(argv[1]); GMAX=atoi(argv[2]);
  pw[0]=1; for(int i=1;i<70;i++) pw[i]=pw[i-1]*P;
  bufA=malloc(MAXST*8); usedpos=malloc(MAXST*8); bufB=malloc(MAXST*8); hs_init(&HS,1u<<25);
  if(argc>3 && !strcmp(argv[3],"glist")){ int amax=atoi(argv[4]);
    for(u64 a=1;a<=(u64)amax;a++){ int g=0; while(g<GMAX && g_ge(a,g+1)) g++; printf("%llu %d\n",(unsigned long long)a,g);} return 0; }
  if(argc>3 && !strcmp(argv[3],"gvals")){ /* census p Kmax gvals amax : histogram of min(g_p(a),Kmax) */
    int amax=atoi(argv[4]); u64 hist[70]={0};
    for(u64 a=1;a<=(u64)amax;a++){ int g=0; while(g<GMAX && g_ge(a,g+1)) g++; hist[g]++; }
    for(int g=0;g<=GMAX;g++) if(hist[g]) printf("g=%d%s: %llu\n",g,g==GMAX?"+":"",(unsigned long long)hist[g]);
    return 0; }
  /* level 0: the single class; g>=0 always */
  dfs(0,0);
  for(int G=1;G<=GMAX;G++){
    printf("p=%d G=%d count=%llu delta=%.6f",P,G,(unsigned long long)cnt[G],(double)cnt[G]/(double)pw[G]);
    if(argc>3 && G<GMAX){ printf("  children-dist:"); for(int k=0;k<=P;k++) if(kids[G][k]) printf(" %d:%llu",k,(unsigned long long)kids[G][k]); }
    printf("\n");
  }
  return 0;
}
