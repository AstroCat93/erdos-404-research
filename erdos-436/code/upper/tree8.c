// tree8.c -- separately written case-vector DFS for the Lambda(k,2) upper bound (written separately from code/generator/pairtree.c).
// Assign R(p_0..p_{T-1}) in Z/k in order; a branch closes when some pair (n,n+1), n<=L, both p_{T-1}-smooth,
// all of whose primes are assigned, has f(n)=f(n+1)=0. No unit normalization; for k=8 R(2) restricted to even values.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { int nf; unsigned char idx[16]; unsigned char e[16]; unsigned char side[16]; } Pair; // side 0 -> n, 1 -> n+1
int k,T; long L; int *pr; Pair **byd; int *cnt; int R[512];
long long nodes=0, closed=0, unresolved=0; int maxd=0;
static int test(int d){ // check pairs whose max prime index is d
  for(int i=0;i<cnt[d];i++){ Pair*P=&byd[d][i]; int a=0,b=0;
    for(int j=0;j<P->nf;j++){ int c=P->e[j]*R[P->idx[j]]; if(P->side[j]) b+=c; else a+=c; }
    if(a%k==0 && b%k==0) return 1; }
  return 0; }
long long unres_report=0;
static void dfs(int d){
  nodes++;
  if(d==T){ unresolved++; if(unres_report<3){ printf("unresolved leaf:"); for(int i=0;i<T && i<30;i++) printf(" %d",R[i]); printf(" ...\n"); unres_report++;} return; }
  for(int v=0; v<k; v++){
    if(d==0 && k%8==0 && (v%2)) continue; // R(2) even for 8|k
    R[d]=v;
    if(test(d)) { closed++; continue; }
    dfs(d+1);
  }
}
int main(int argc,char**argv){
  k=atoi(argv[1]); L=atol(argv[2]); T=atoi(argv[3]);
  long N=L+1; int *spf=calloc(N+1,sizeof(int));
  for(long i=2;i<=N;i++) if(!spf[i]) for(long j=i;j<=N;j+=i) if(!spf[j]) spf[j]=i;
  pr=malloc(sizeof(int)*T); int np=0; int *pidx=calloc(N+1,sizeof(int));
  for(long i=2;i<=N && np<T;i++) if(spf[i]==i){ pr[np]=i; pidx[i]=np+1; np++; }
  int P=pr[T-1];
  cnt=calloc(T,sizeof(int)); int *cap=calloc(T,sizeof(int)); byd=calloc(T,sizeof(Pair*));
  long npairs=0;
  for(long n=1;n<=L;n++){
    Pair Q; Q.nf=0; int ok=1, md=-1;
    for(int s=0;s<2 && ok;s++){ long m=n+s; while(m>1){ int p=spf[m]; if(p>P){ok=0;break;} int e=0; while(m%p==0){m/=p;e++;} int id=pidx[p]-1; Q.idx[Q.nf]=id; Q.e[Q.nf]=e; Q.side[Q.nf]=s; Q.nf++; if(id>md) md=id; } }
    if(!ok) continue;
    if(md<0) md=0; // n=1: f(1)=0 and f(2) involves prime 2 -> md=0 anyway
    if(cnt[md]==cap[md]){ cap[md]=cap[md]?2*cap[md]:64; byd[md]=realloc(byd[md],sizeof(Pair)*cap[md]); }
    byd[md][cnt[md]++]=Q; npairs++;
  }
  fprintf(stderr,"k=%d L=%ld T=%d (p_T=%d) smooth pairs=%ld\n",k,L,T,P,npairs);
  dfs(0);
  printf("k=%d L=%ld T=%d p_T=%d nodes=%lld closed=%lld unresolved=%lld\n",k,L,T,P,nodes,closed,unresolved);
  return 0;
}
