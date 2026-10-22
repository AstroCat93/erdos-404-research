/* l2dp.c -- exact second moment of subset sums of factorials modulo p^E.
 *
 * Track T3a (round 3), Erdos #404.  Written 2026-10-20.
 *
 * Elements: n = N0, N0+1, ..., while v_p(n!) < E  (n! with v_p(n!) >= E is 0 mod p^E
 * and only doubles every count; it is left out).  M = number of elements.
 * N(r) = #{ B subset of the elements : sum_{n in B} n! == r (mod p^E) }.
 * For every E' <= E we output  S(E') = sum_{r mod p^{E'}} N_{E'}(r)^2  where
 * N_{E'}(r) = sum_{r' == r mod p^{E'}} N(r')  (folded counts; the elements with
 * E' <= v(n!) < E double each folded count, which is harmless because we always
 * report M together with S).  Then
 *     P(p^{E'} | sum_n eta_n n!) = S(E') / 4^M,   eta_n iid in {-1,0,1} w.p. 1/4,1/2,1/4,
 * and the L^2 Fourier mass of the tail measure from N0 (elements n!/p^{v(N0!)}, fair
 * coins) over all frequencies of p^{-k}Z/Z, k = E' - v(N0!), equals p^k S(E')/4^M.
 *
 * Exactness: counts are held in uint64 when M <= 64 (N(r) <= 2^M < 2^64 then), and in
 * unsigned __int128 when 64 < M <= 120.  S(E') can exceed 2^128, so it is accumulated
 * modulo 2^128 (printed as hi,lo) AND modulo q = 2^61-1; the caller reconstructs the
 * exact value by CRT (valid while S < 2^189, i.e. 2M <= 189).  A long double value is
 * printed as a plausibility check only.
 *
 * Memory: 1.5 arrays of p^E entries (in place with a save buffer; the two-array original
 * is kept as l2dp_twoarray.c for cross-checks).  Usage: l2dp p E N0
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
static const uint64_t Q = 2305843009213693951ULL; /* 2^61-1 */

static uint64_t mulmodq(uint64_t a, uint64_t b){ return (uint64_t)(((u128)a*b) % Q); }

static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }

int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage: l2dp p E N0\n");return 1;}
  uint64_t p=strtoull(argv[1],0,10); int E=atoi(argv[2]); uint64_t N0=strtoull(argv[3],0,10);
  u128 mod=1; for(int i=0;i<E;i++) mod*=p;
  if(mod > ((u128)1<<40)){fprintf(stderr,"modulus too large\n");return 1;}
  uint64_t Mod=(uint64_t)mod;
  /* list elements: n! mod p^E for n>=N0 while v_p(n!)<E */
  int cap=4096; uint64_t *res=malloc(cap*8); int *vals=malloc(cap*sizeof(int)); int M=0;
  { /* compute n! mod p^E iteratively together with v_p(n!) */
    u128 f=1; int v=0;
    for(uint64_t n=1;;n++){
      uint64_t m=n; while(m%p==0){m/=p;v++;}
      f=(f*(m%Mod))%Mod; /* f = unit part of n! mod p^E */
      if(v>=E) break;
      if(n>=N0){ /* residue of n! = p^v * f mod p^E */
        u128 pv=1; for(int i=0;i<v;i++) pv*=p;
        res[M]=(uint64_t)((pv*f)%Mod); vals[M]=v; M++;
        if(M>=cap){fprintf(stderr,"too many elements\n");return 1;}
      }
    }
  }
  int wide = (M>64);
  if(M>120){fprintf(stderr,"M=%d too large\n",M);return 1;}
  fprintf(stderr,"p=%llu E=%d N0=%llu modulus=%llu M=%d wide=%d\n",(unsigned long long)p,E,(unsigned long long)N0,(unsigned long long)Mod,M,wide);
  double t0=now();
  size_t esz = wide?16:8;
  /* In-place DP with a save buffer of at most Mod/2 entries.  Replacing an element a by
   * Mod-a translates the count function (N'(r)=N(r+a)); every statistic we report is
   * translation invariant, so we may use a' = min(a, Mod-a) <= Mod/2.
   * Case a <= Mod/2 ("add"):  new[r] = old[r] + old[r-a]  (r>=a), old[r-a+Mod] (r<a):
   *   save old[Mod-a..Mod), downward pass r=Mod-1..a (reads unmodified lower entries),
   *   then r<a from the buffer.
   * Case a' = Mod-a < Mod/2 ("sub"): new[r] = old[r] + old[r+a'] (r<Mod-a'), old[r+a'-Mod] (r>=Mod-a'):
   *   save old[0..a'), upward pass r=0..Mod-a'-1 (reads unmodified higher entries), rest from buffer. */
  void *A=calloc(Mod,esz); void *B=malloc((Mod/2+1)*esz);
  if(!A||!B){fprintf(stderr,"alloc failed\n");return 1;}
  if(wide) ((u128*)A)[0]=1; else ((uint64_t*)A)[0]=1;
  for(int i=0;i<M;i++){
    uint64_t a=res[i];
    if(a<=Mod/2){
      if(wide){ u128*X=A,*S=B; memcpy(S,X+(Mod-a),a*16); for(uint64_t r=Mod;r-->a;) X[r]+=X[r-a]; for(uint64_t r=0;r<a;r++) X[r]+=S[r]; }
      else { uint64_t*X=A,*S=B; memcpy(S,X+(Mod-a),a*8); for(uint64_t r=Mod;r-->a;) X[r]+=X[r-a]; for(uint64_t r=0;r<a;r++) X[r]+=S[r]; }
    } else {
      uint64_t ap=Mod-a;
      if(wide){ u128*X=A,*S=B; memcpy(S,X,ap*16); for(uint64_t r=0;r<Mod-ap;r++) X[r]+=X[r+ap]; for(uint64_t r=Mod-ap;r<Mod;r++) X[r]+=S[r+ap-Mod]; }
      else { uint64_t*X=A,*S=B; memcpy(S,X,ap*8); for(uint64_t r=0;r<Mod-ap;r++) X[r]+=X[r+ap]; for(uint64_t r=Mod-ap;r<Mod;r++) X[r]+=S[r+ap-Mod]; }
    }
    if((i&7)==7) fprintf(stderr,"  element %d/%d (n!=%llu mod, v=%d) t=%.1fs\n",i+1,M,(unsigned long long)a,vals[i],now()-t0);
  }
  free(B); B=malloc((Mod/p+1)*esz); if(!B){fprintf(stderr,"alloc failed\n");return 1;}
  /* Now A holds N(r) mod p^E.  Fold level by level, computing S(E'). */
  printf("# p=%llu E=%d N0=%llu M=%d\n",(unsigned long long)p,E,(unsigned long long)N0,M);
  printf("# columns: Eprime  Mprime(=#elements with v<Eprime)  S_hi  S_lo  S_modq  S_longdouble  maxcount(as long double)  hit(=#residues with N>0)\n");
  uint64_t cur=Mod;
  for(int Ep=E;Ep>=1;Ep--){
    u128 S=0; uint64_t Sq=0; long double Sd=0, mx=0; uint64_t hit=0; int Mp=0; for(int i=0;i<M;i++) if(vals[i]<Ep) Mp++;
    if(wide){ u128*X=A; for(uint64_t r=0;r<cur;r++){ u128 x=X[r]; if(x) hit++; S+=x*x; uint64_t xq=(uint64_t)(x%Q); Sq=(Sq+mulmodq(xq,xq))%Q; long double xd=(long double)x; Sd+=xd*xd; if(xd>mx)mx=xd; } }
    else { uint64_t*X=A; for(uint64_t r=0;r<cur;r++){ u128 x=X[r]; if(x) hit++; S+=x*x; uint64_t xq=X[r]%Q; Sq=(Sq+mulmodq(xq,xq))%Q; long double xd=(long double)X[r]; Sd+=xd*xd; if(xd>mx)mx=xd; } }
    printf("%d %d %llu %llu %llu %.6Le %.6Le %llu\n",Ep,Mp,(unsigned long long)(S>>64),(unsigned long long)(uint64_t)S,(unsigned long long)Sq,Sd,mx,(unsigned long long)hit);
    fflush(stdout);
    if(Ep==1) break;
    /* fold: new array of size cur/p : F[r'] = sum_{j} X[r' + j*cur/p] */
    uint64_t nxt=cur/p;
    if(wide){ u128*X=A,*Y=B; for(uint64_t r=0;r<nxt;r++){ u128 s=0; for(uint64_t j=0;j<p;j++) s+=X[r+j*nxt]; Y[r]=s; } }
    else { uint64_t*X=A,*Y=B; for(uint64_t r=0;r<nxt;r++){ u128 s=0; for(uint64_t j=0;j<p;j++) s+=X[r+j*nxt]; if(s>>64){fprintf(stderr,"fold overflow\n");return 2;} Y[r]=(uint64_t)s; } }
    void*t=A;A=B;B=t; cur=nxt;
  }
  fprintf(stderr,"done in %.1fs\n",now()-t0);
  return 0;
}
