/* Independent re-implementation (referee): gate-block law of Lemma 11.37.
   e_u = (-1)^u (p-1)!/u!, u=0..p-1.  W = sum eta_u e_u, eta in {-1,0,1} with
   weights 1/4,1/2,1/4.  Prints weighted counts  sum_{eta: p^j | W} 2^{#zeros}
   (= 4^p P(p^j|W)) for j=0..JMAX, and the count for W==0 exactly.
   Usage: gblock p  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define JMAX 24
static int p; static int64_t e[32];
static unsigned __int128 hist[JMAX+2]; /* hist[j] = weight with v_p(W)==j (j<=JMAX), hist[JMAX+1]= v>JMAX but W!=0 */
static unsigned __int128 wzero;
static void rec(int u, int64_t W, int zeros){
  if(u==p){
    uint64_t w=(uint64_t)1<<zeros;
    if(W==0){ wzero+=w; return; }
    int64_t a = W<0?-W:W; int v=0; while(a%p==0){a/=p;v++; if(v>JMAX) break;}
    if(v>JMAX) hist[JMAX+1]+=w; else hist[v]+=w; return;
  }
  rec(u+1,W,zeros+1); rec(u+1,W+e[u],zeros); rec(u+1,W-e[u],zeros);
}
static void pr128(unsigned __int128 x){ char b[64]; int i=63; b[i]=0; if(x==0){printf("0");return;} while(x){b[--i]='0'+(int)(x%10); x/=10;} printf("%s",b+i);}
int main(int argc,char**argv){
  p=atoi(argv[1]);
  int64_t f=1; for(int i=1;i<p;i++) f*=i; /* (p-1)! */
  int64_t uf=1;
  for(int u=0;u<p;u++){ if(u>0) uf*=u; e[u]=(u%2?-1:1)*(f/uf); }
  rec(0,0,0);
  /* cumulative: weight with p^j | W  = wzero + sum_{v>=j} hist[v] */
  printf("p=%d W==0 weight=",p); pr128(wzero); printf(" (4^p=2^%d)\n",2*p);
  for(int j=0;j<=JMAX;j++){
    unsigned __int128 c=wzero; for(int v=j;v<=JMAX+1;v++) c+=hist[v];
    printf("j=%d cnt=",j); pr128(c); printf("\n");
  }
  return 0;
}
