/* Independent re-implementation (refute-Corollary_11.19 track) of N_{w,K}(tau) and D_p(w,K)
   from note_v3 §11.2 "Window data".  Written from the definition only; not derived from wdim.c.
   Usage: ./mydim p w K [ystart yend]
   Output: exact histogram "N count" lines (N = number of distinct subset sums), so D can be
   recomputed in high precision by mydim_sum.py.  Also prints a double-precision D. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>

static uint64_t ipow(uint64_t p, int e){uint64_t r=1;while(e--)r*=p;return r;}
static int vp(uint64_t x, uint64_t p, int K){ if(x==0) return K; int v=0; while(x%p==0){x/=p;v++;} return v<K?v:K; }

int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 1;}
  uint64_t p=atoll(argv[1]); int w=atoi(argv[2]); int K=atoi(argv[3]);
  int P=w*(int)p; uint64_t pK=ipow(p,K), nY=ipow(p,K-1);
  uint64_t y0=0,y1=nY; if(argc>=6){y0=atoll(argv[4]);y1=atoll(argv[5]);}
  uint64_t *hist=calloc(pK+1,sizeof(uint64_t));
  uint8_t *A=malloc(pK), *Bt=malloc(pK);
  uint64_t *WA=malloc((pK/64+2)*8), *WB=malloc((pK/64+2)*8);
  uint64_t q[4096];
  for(uint64_t y=y0;y<y1;y++){
    uint64_t tau=(p*y)%pK;
    int S=0; for(int t=1;t<=P;t++){ S+=vp((tau+t)%pK,p,K); if(S>=K)break; }
    int G=S<K?S:K; uint64_t M=ipow(p,G);
    /* q_s = prod_{t<=s}(tau+t) mod M, s=0..P-1 */
    uint64_t cur=1%M; for(int s=0;s<P;s++){ if(s>0) cur=(cur*((tau+s)%M))%M; q[s]=cur; }
    uint64_t N;
    if(p==2 && M>=64){
      uint64_t W=M/64; memset(WA,0,W*8); WA[0]=1;
      for(int s=0;s<P;s++){ uint64_t qq=q[s]; if(qq==0) continue; uint64_t a=qq/64; int b=qq%64;
        for(uint64_t j=0;j<W;j++){ uint64_t i1=(j+W-a)%W; uint64_t o=WA[i1]<<b; if(b){uint64_t i2=(j+W-a-1)%W; o|=WA[i2]>>(64-b);} WB[j]=WA[j]|o; }
        uint64_t*t=WA;WA=WB;WB=t; }
      N=0; for(uint64_t j=0;j<W;j++) N+=__builtin_popcountll(WA[j]);
    } else {
      memset(A,0,M); A[0]=1;
      for(int s=0;s<P;s++){ uint64_t qq=q[s]; if(qq==0) continue;
        /* B[i] = A[i] | A[(i-qq) mod M] */
        for(uint64_t i=0;i<qq;i++) Bt[i]=A[i]|A[i+M-qq];
        for(uint64_t i=qq;i<M;i++) Bt[i]=A[i]|A[i-qq];
        uint8_t*t=A;A=Bt;Bt=t; }
      N=0; for(uint64_t i=0;i<M;i++) N+=A[i];
    }
    hist[N]++;
  }
  double sum=0; for(uint64_t n=1;n<=pK;n++) if(hist[n]){ printf("N %llu %llu\n",(unsigned long long)n,(unsigned long long)hist[n]); sum+=hist[n]*(log((double)n)/log((double)p)); }
  if(y0==0&&y1==nY) printf("D_double p=%llu w=%d K=%d %.12f\n",(unsigned long long)p,w,K,(double)(p-1)/(double)(w*p)*sum/(double)nY);
  return 0;
}
