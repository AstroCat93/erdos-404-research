/* Independent computation of D_p(w,K) (note_v3 §11.2, "Window data").
   Written from the definition only, not from wdim.c.
   D_p(w,K) = (p-1)/(wp) * p^{-(K-1)} * sum_{y mod p^{K-1}} log_p N_{w,K}(p y)
   N = #distinct subset sums of {q_s(tau)}_{0<=s<P} mod p^{G_K(tau)},
   q_s = prod_{t=1}^{s} (tau+t), G_K = min(K, sum_{t=1}^{P} min(v(tau+t),K)).
   Strategy: group tau by G.  For G<K, tau's with G_K(tau)=G are exactly those
   whose class mod p^{G+1} has sum_t min(v(tau+t),G+1) == G (then all v<=G are exact),
   each such class has p^{K-G-1} lifts among y mod p^{K-1}.  For G=K enumerate mod p^K.
   Usage: mydim p w K [sample_count seed]   (sample>0: Monte Carlo over y instead) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

static int p;
static long long ipow(int b,int e){long long r=1;while(e--)r*=b;return r;}
static int vcap(long long x,long long mod,int cap){ /* v_p(x mod mod), capped */
  x%=mod; if(x<0)x+=mod; if(x==0) return cap; int v=0; while(x%p==0&&v<cap){x/=p;v++;} return v;}

static unsigned char *buf1,*buf2;
static uint64_t *b64a,*b64b;
static long long count_sums_bits(long long *q,int P,long long M){ /* p=2, M=2^G>=64 */
  long long W=M/64; memset(b64a,0,W*8); b64a[0]=1;
  for(int s=0;s<P;s++){
    long long a=((q[s]%M)+M)%M; long long ws=a>>6; int bs=a&63;
    for(long long j=0;j<W;j++){
      long long i0=(j-ws)%W; if(i0<0)i0+=W; long long i1=i0-1; if(i1<0)i1+=W;
      uint64_t x = bs? ((b64a[i0]<<bs)|(b64a[i1]>>(64-bs))) : b64a[i0];
      b64b[j]=b64a[j]|x; }
    uint64_t*t=b64a;b64a=b64b;b64b=t;
  }
  long long c=0; for(long long j=0;j<W;j++) c+=__builtin_popcountll(b64a[j]); return c;
}
static long long count_sums(long long *q,int P,long long M){
  if(p==2 && M>=64) return count_sums_bits(q,P,M);
  memset(buf1,0,M); buf1[0]=1;
  for(int s=0;s<P;s++){
    long long a=((q[s]%M)+M)%M;
    memcpy(buf2,buf1,M);
    for(long long r=0;r<M;r++) if(buf1[r]){ long long u=r+a; if(u>=M)u-=M; buf2[u]=1; }
    unsigned char*t=buf1;buf1=buf2;buf2=t;
  }
  long long c=0; for(long long r=0;r<M;r++) c+=buf1[r]; return c;
}
static double logN_of_tau(long long tau,int P,int G){ /* tau mod p^G suffices */
  long long M=ipow(p,G); long long q[256]; long long cur=1%M;
  for(int s=0;s<P;s++){ if(s>0){ cur=(__int128)cur*((tau+s)%M)%M; } q[s]=cur; }
  long long N=count_sums(q,P,M); return log((double)N)/log((double)p);
}
static int Gof(long long tau,int P,int K){ long long MK=ipow(p,K); long long S=0;
  for(int t=1;t<=P;t++) S+=vcap(tau+t,MK,K); return S<K?(int)S:K; }

int main(int argc,char**argv){
  p=atoi(argv[1]); int w=atoi(argv[2]); int K=atoi(argv[3]); int P=w*p;
  long long samples= argc>4? atoll(argv[4]):0; unsigned seed= argc>5? atoi(argv[5]):1;
  long long MK=ipow(p,K); buf1=malloc(MK); buf2=malloc(MK); b64a=malloc(MK/8+8); b64b=malloc(MK/8+8);
  long long Y=ipow(p,K-1);
  if(samples>0){ srand(seed); double s=0,s2=0;
    for(long long i=0;i<samples;i++){ long long y=0; for(int d=0;d<K-1;d++) y=y*p+arc4random_uniform(p);
      long long tau=p*y; int G=Gof(tau,P,K); double l=logN_of_tau(tau,P,G); s+=l; s2+=l*l; }
    double m=s/samples, var=s2/samples-m*m; double f=(p-1.0)/(w*p);
    printf("MC p=%d w=%d K=%d n=%lld D~=%.6f se=%.6f\n",p,w,K,samples,f*m,f*sqrt(var/samples)); return 0; }
  double tot=0; long long wsum=0;
  for(int G=0;G<=K;G++){
    long long M = (G<K)? ipow(p,G+1): MK; long long lifts = Y/(M/p); long long cnt=0;
    for(long long tau=0;tau<M;tau+=p){
      long long S=0; int cap=(G<K)?G+1:K;
      for(int t=1;t<=P;t++){ S+=vcap(tau+t,M,cap); if(G<K && S>G) break; }
      if(G<K){ if(S!=G) continue; } else { if(S<K) continue; }
      double l = (G==0)?0.0: logN_of_tau(tau,P,G);
      tot += lifts*l; wsum+=lifts; cnt++;
    }
    fprintf(stderr,"G=%d classes=%lld\n",G,cnt);
  }
  double D=(p-1.0)/(w*p)*tot/Y;
  printf("p=%d w=%d K=%d weightcheck=%lld/%lld D=%.10f\n",p,w,K,wsum,Y,D);
  return 0;
}
