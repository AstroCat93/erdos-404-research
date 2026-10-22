/* wdim.c -- exact computation of the window-code dimension bound D_p(w,K)
   of Theorem 3.1 (writeup.md, track T1b, round 3).

   For each y mod p^(K-1), tau = p*y in Z/p^K:
     q_s = prod_{t=1}^{s} (tau+t) mod p^K, 0<=s<P=w*p
     G   = min(K, sum_{t=1}^{P} min(v(tau+t),K))   (v(0):=K)
     N   = #{ sum_{s in S} q_s mod p^G : S subset [0,P) }
   D = (p-1)/(w p) * mean_y log_p N.
   N is computed exactly, by subset-sum DP on a byte array of size p^G
   (cost P*p^G) or by Gray-code enumeration of the 2^P subsets with a stamp
   array (cost 2^P), whichever is cheaper.
   Usage: wdim p w K      Output: one summary line + per-G table.          */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

static int vp(u64 a, u64 p, int K){ if(a==0) return K; int c=0; while(a%p==0){a/=p;c++; if(c>=K) return K;} return c; }

int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: wdim p w K\n");return 1;}
  u64 p=strtoull(argv[1],0,10); int w=atoi(argv[2]); int K=atoi(argv[3]);
  int P=w*(int)p;
  u64 pK=1; for(int i=0;i<K;i++) pK*=p;
  u64 ntypes=pK/p;
  u64 *pw=malloc(sizeof(u64)*(K+1)); pw[0]=1; for(int i=1;i<=K;i++) pw[i]=pw[i-1]*p;
  unsigned char *A=NULL,*B=NULL; u64 Acap=0;
  uint32_t *stamp=NULL; u64 stampcap=0; uint32_t stampid=0;
  u64 *q=malloc(sizeof(u64)*P);
  double sumlog=0; double sumG=0;
  double *sumlogG=calloc(K+1,sizeof(double)); u64 *cntG=calloc(K+1,sizeof(u64));
  double *minlogG=malloc(sizeof(double)*(K+1)); for(int i=0;i<=K;i++) minlogG[i]=1e9;
  for(u64 y=0;y<ntypes;y++){
    u64 tau=(p*y)%pK;
    int Gs=0;
    for(int t=1;t<=P;t++){ Gs+=vp((tau+t)%pK,p,K); if(Gs>K){Gs=K;} }
    int G=Gs<K?Gs:K;
    u64 m=pw[G];
    u64 cur=1%pK;
    for(int s=0;s<P;s++){ if(s>0) cur=(u64)(((u128)cur*((tau+s)%pK))%pK); q[s]=cur%m; }
    u64 N;
    double costDP=(double)P*(double)m, costEN=ldexp(1.0,P);
    if(costDP<=costEN){
      if(m>Acap){free(A);free(B);A=malloc(m);B=malloc(m);Acap=m;}
      memset(A,0,m); A[0]=1;
      for(int s=0;s<P;s++){
        u64 qs=q[s]; if(qs==0) continue;
        memcpy(B,A,m);
        for(u64 r=0;r<m;r++) if(B[r]){ u64 r2=r+qs; if(r2>=m) r2-=m; A[r2]=1; }
      }
      N=0; for(u64 r=0;r<m;r++) N+=A[r];
    } else {
      if(m>stampcap){free(stamp);stamp=calloc(m,sizeof(uint32_t));stampcap=m;stampid=0;}
      stampid++; if(stampid==0){memset(stamp,0,sizeof(uint32_t)*stampcap);stampid=1;}
      u64 sum=0; N=0; stamp[0]=stampid; N=1;
      u64 total=1ULL<<P;
      for(u64 g=1; g<total; g++){
        int b=__builtin_ctzll(g);
        /* Gray code: element b toggles */
        u64 gray=g^(g>>1);
        if(gray>>b & 1){ sum+=q[b]; if(sum>=m) sum-=m; }
        else { sum+= m-q[b]; if(sum>=m) sum-=m; }
        if(stamp[sum]!=stampid){stamp[sum]=stampid;N++;}
      }
    }
    double l=log((double)N)/log((double)p);
    sumlog+=l; sumG+=Gs; sumlogG[G]+=l; cntG[G]++; if(l<minlogG[G]) minlogG[G]=l;
  }
  double meanlog=sumlog/(double)ntypes;
  double D=(double)(p-1)/((double)w*(double)p)*meanlog;
  printf("p=%llu w=%d K=%d P=%d types=%llu mean_log_p_N=%.10f mean_G_capped=%.6f D=%.10f\n",
         p,w,K,P,ntypes,meanlog,sumG/(double)ntypes,D);
  for(int g=0;g<=K;g++) if(cntG[g]) printf("  G=%d frac=%.8f mean_logN=%.6f min_logN=%.6f\n",g,(double)cntG[g]/ntypes,sumlogG[g]/cntG[g],minlogG[g]);
  return 0;
}
