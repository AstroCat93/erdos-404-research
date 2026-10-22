/* gamma_enum.c -- exact gate-block constants for the L^2 route (track T3a, round 3, 2026-10-21).
 *
 * For a prime p let e_u = (-1)^u (p-1)!/u!, u = 0..p-1 (the gate pattern of note Thm 3.9(b); for p = 2 this is {1,-1}).
 * eta_u iid in {-1,0,1} with weights 1,2,1 (probabilities 1/4,1/2,1/4); W = sum_u eta_u e_u (an exact integer).
 * Output, for J = 1..Jmax:
 *   cnt(J)  = sum of weights of eta with p^J | W          (exact integer; total weight 4^p)
 *             so Gamma_p(J) = p^J cnt(J)/4^p - 1 exactly;
 *   dist(J) = number of distinct residues mod p^J of the 2^p subset sums sum_{u in S} e_u.
 * Also Sigma_p = sum_u |e_u|, the zero-weight cnt(inf) (eta with W = 0 exactly), and the number of distinct
 * integer subset sums.  Exhaustive enumeration (3^p sign vectors, 2^p subsets); exact integer arithmetic (__int128).
 * Usage: gamma_enum p Jmax      (p <= 19)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef __int128 i128;
static int p, Jmax;
static i128 e[32];
static unsigned long long hist[128]; /* hist[v] = weight of eta with v_p(W) = v (v < 127); hist[127] = W == 0 */
static void pr128(i128 x){ char b[64]; int i=63; b[i]=0; int neg=x<0; unsigned __int128 u = neg? -(unsigned __int128)x : (unsigned __int128)x; if(!u){printf("0");return;} while(u){ b[--i]='0'+(int)(u%10); u/=10;} if(neg) printf("-"); printf("%s",b+i); }
static void dfs(int u, i128 W, unsigned long long w){
  if(u==p){
    if(W==0){ hist[127]+=w; return; }
    int v=0; i128 x=W; while(x%p==0){ x/=p; v++; } hist[v]+=w; return;
  }
  dfs(u+1, W, w*2); dfs(u+1, W+e[u], w); dfs(u+1, W-e[u], w);
}
static int cmp(const void*a,const void*b){ unsigned long long x=*(const unsigned long long*)a, y=*(const unsigned long long*)b; return x<y?-1:x>y; }
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: gamma_enum p Jmax\n");return 1;}
  p=atoi(argv[1]); Jmax=atoi(argv[2]);
  if(p>19){fprintf(stderr,"p<=19 only\n");return 1;}
  i128 f=1; for(int i=1;i<p;i++) f*=i;              /* (p-1)! */
  i128 uf=1; i128 Sig=0;
  for(int u=0;u<p;u++){ if(u) uf*=u; e[u]=((u%2)?-1:1)*(f/uf); Sig += e[u]<0?-e[u]:e[u]; }
  memset(hist,0,sizeof hist);
  dfs(0,0,1);
  printf("p=%d  e_u =",p); for(int u=0;u<p;u++){ printf(" "); pr128(e[u]); } printf("\n");
  printf("p=%d  Sigma_p=",p); pr128(Sig); printf("  total_weight=4^p=%llu  weight(W=0)=%llu\n", 1ULL<<(2*p), hist[127]);
  /* distinct subset sums */
  int S = 1<<p; i128 *ss = malloc(sizeof(i128)*S);
  for(int m=0;m<S;m++){ i128 s=0; for(int u=0;u<p;u++) if(m>>u&1) s+=e[u]; ss[m]=s; }
  { /* distinct integers */
    i128 *t = malloc(sizeof(i128)*S); memcpy(t,ss,sizeof(i128)*S);
    /* simple sort of i128 via qsort on pairs */
    for(int i=1;i<S;i++){ /* insertion is too slow for 2^19; use shell sort */ }
    int gaps[]={1391376,463792,198768,86961,33936,13776,4592,1968,861,336,112,48,21,7,3,1};
    for(int g=0; g<16; g++){ int gap=gaps[g]; for(int i=gap;i<S;i++){ i128 x=t[i]; int j=i; while(j>=gap && t[j-gap]>x){ t[j]=t[j-gap]; j-=gap;} t[j]=x; } }
    int d=1; for(int i=1;i<S;i++) if(t[i]!=t[i-1]) d++;
    printf("p=%d  distinct integer subset sums = %d  (3*2^(p-2) = %d)\n", p, d, p>=2? 3*(1<<(p-2)) : 0);
    free(t);
  }
  unsigned long long *r = malloc(sizeof(unsigned long long)*S);
  i128 pJ=1;
  for(int J=1;J<=Jmax;J++){
    pJ*=p; if(pJ > ((i128)1<<62)) break;
    unsigned long long cnt=hist[127]; for(int v=J; v<127; v++) cnt+=hist[v];
    for(int m=0;m<S;m++){ i128 x = ss[m] % pJ; if(x<0) x+=pJ; r[m]=(unsigned long long)x; }
    qsort(r,S,sizeof(unsigned long long),cmp);
    int d=1; for(int i=1;i<S;i++) if(r[i]!=r[i-1]) d++;
    printf("p=%d J=%d  p^J=", p, J); pr128(pJ); printf("  cnt=%llu  dist=%d  pJ>Sigma=%d\n", cnt, d, pJ>Sig);
  }
  free(r); free(ss);
  return 0;
}
