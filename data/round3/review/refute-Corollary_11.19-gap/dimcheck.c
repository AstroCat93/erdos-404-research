/* Independent re-implementation of D_p(w,K) from note_v3 §11.2 (window data).
   tau = p*y, y mod p^{K-1}; G = min(K, sum_{t=1}^{P} min(v(tau+t),K)); q_s=prod_{t=1}^{s}(tau+t) mod p^G, s<P;
   N = #distinct subset sums mod p^G (Gray-code enumeration, bitmap). D = (p-1)/(wp) * avg log_p N. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>
static int vp(int64_t x,int p,int K,int64_t pK){ x%=pK; if(x<0)x+=pK; if(x==0) return K; int v=0; while(x%p==0){x/=p;v++;} return v;}
int main(int argc,char**argv){
  int p=atoi(argv[1]), w=atoi(argv[2]), K=atoi(argv[3]); int P=w*p;
  int64_t pK=1; for(int i=0;i<K;i++) pK*=p; int64_t pK1=pK/p;
  uint8_t *mark=calloc(pK,1); int64_t *list=malloc(sizeof(int64_t)*((size_t)1<<P));
  double acc=0; long double accl=0; int64_t minN=-1;
  for(int64_t y=0;y<pK1;y++){
    int64_t tau=p*y; int Gs=0; for(int t=1;t<=P;t++){ Gs+=vp(tau+t,p,K,pK); if(Gs>=K) break;} int G=Gs<K?Gs:K;
    int64_t m=1; for(int i=0;i<G;i++) m*=p;
    int64_t q[64]; int64_t c=1%m; for(int s=0;s<P;s++){ if(s>0) c=(c*((tau+s)%m))%m; q[s]=c; }
    /* gray code */
    int64_t cur=0; int64_t n=0; uint64_t used=0; mark[0]=1; list[n++]=0;
    for(uint64_t i=1;i<((uint64_t)1<<P);i++){ int b=__builtin_ctzll(i); if(used>>b&1){cur-=q[b]; if(cur<0)cur+=m;} else {cur+=q[b]; if(cur>=m)cur-=m;} used^=1ULL<<b;
      if(!mark[cur]){mark[cur]=1; list[n++]=cur;} }
    for(int64_t i=0;i<n;i++) mark[list[i]]=0;
    accl += logl((long double)n)/logl((long double)p);
    if(minN<0||n<minN) minN=n;
  }
  long double D=(long double)(p-1)/(w*p)*accl/(long double)pK1;
  printf("p=%d w=%d K=%d D=%.12Lf minN=%lld\n",p,w,K,D,(long long)minN);
  return 0;}
