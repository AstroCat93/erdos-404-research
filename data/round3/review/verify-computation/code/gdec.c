/* Referee decision procedure for g_p (independent of T4's annealed.c/gsampleN.c/p2add.c, T2's gcap.py).
   gval(x,cap) = min(g_p(x), cap) for x in Z_p given mod p^cap (p^cap < 2^126), by the
   normalised-state recursion: for a path alive at length n (p^{V_n} | S), sigma = S/pi_n mod p^{cap-V_n};
   children sigma+b (b=0,1); alive at n+1 iff v(sigma+b) >= j = v(x+n+1); then sigma' = (sigma+b)/(x+n+1).
   g = max over all alive (path,n), b of V_n + v(sigma+b); returns cap as soon as some value reaches cap.
   Modes:
     census p Gmax nthreads      : exact counts of classes mod p^G with g>=G, all G<=Gmax (digit-tree DFS)
     mc p cap nsamp seed nthreads: Monte Carlo histogram of min(g,cap) for Haar-random x
   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static int p; static u128 pw[130];
static int vcap(u128 z, int cap){ if(z==0) return cap; int v=0; while(z%p==0){ z/=p; v++; if(v>=cap) return cap;} return v; }
static u128 mulmod(u128 a,u128 b,u128 m){ /* a,b < m < 2^126 : do via double-and-add if needed */
  if((a>>63)==0 && (b>>63)==0) return (a*b)%m;
  u128 r=0; a%=m; while(b){ if(b&1){ r+=a; if(r>=m) r-=m; } a<<=1; if(a>=m) a-=m; b>>=1; } return r; }
static u128 invmod(u128 u,u128 m){ /* u unit mod m=p^k ; extended Euclid on signed 128 */
  __int128 t=0,nt=1; __int128 r=(__int128)m, nr=(__int128)(u%m);
  while(nr){ __int128 q=r/nr, tmp; tmp=t-q*nt; t=nt; nt=tmp; tmp=r-q*nr; r=nr; nr=tmp; }
  if(t<0) t+=(__int128)m; return (u128)t; }
typedef struct { u128 *a; u64 n, cap; u128 *tab; u64 tcap; } pset;
static void ps_init(pset*s){ s->cap=1024; s->a=malloc(s->cap*16); s->n=0; s->tcap=4096; s->tab=malloc(s->tcap*16); }
static u128 EMPTY=~(u128)0;
static void ps_clear(pset*s,u64 want){ s->n=0; u64 need=4; while(need<2*want+8) need<<=1; if(need>s->tcap){ free(s->tab); s->tcap=need; s->tab=malloc(need*16);} for(u64 i=0;i<s->tcap;i++) s->tab[i]=EMPTY; }
static void ps_add(pset*s,u128 v){ u64 h=(u64)(v*0x9E3779B97F4A7C15ULL ^ (v>>64)); h^=h>>29; u64 msk=s->tcap-1; u64 i=h&msk;
  while(s->tab[i]!=EMPTY){ if(s->tab[i]==v) return; i=(i+1)&msk; }
  s->tab[i]=v; if(s->n==s->cap){ s->cap*=2; s->a=realloc(s->a,s->cap*16);} s->a[s->n++]=v; }
typedef struct { pset A,B; } ws_t;
static int gval(ws_t*W, u128 x, int cap){
  u128 M=pw[cap];
  /* length 0: S=0 (empty), sigma=0 at V_0=0; first step must take e_0=1 */
  pset *cur=&W->A, *nxt=&W->B; ps_clear(cur,1); ps_add(cur,0);
  int V=0, best=0; int first=1;
  for(long n=0;;n++){
    u128 xn=(x+(u128)(n+1))%M; int j=vcap(xn,cap);
    u128 mod=pw[cap-V];
    u128 uinv=0; int haveinv=0;
    ps_clear(nxt,2*cur->n);
    for(u64 i=0;i<cur->n;i++){
      for(int b=(first?1:0); b<=1; b++){
        u128 t=(cur->a[i]+b)%mod;
        int vt = (t==0)? (cap-V) : vcap(t,cap-V);
        if(V+vt>=cap) return cap;
        if(V+vt>best) best=V+vt;
        if(vt>=j){
          if(V+j>=cap) return cap;
          u128 mod2=pw[cap-V-j];
          if(!haveinv){ u128 u=xn/pw[j]; uinv=invmod(u%mod2,mod2); haveinv=1; }
          u128 s2=mulmod((t/pw[j])%mod2, uinv, mod2);
          ps_add(nxt,s2);
        }
      }
    }
    first=0;
    if(nxt->n==0) return best;
    V+=j; pset*T=cur; cur=nxt; nxt=T;
  }
}
/* ---------------- census by DFS on digits ---------------- */
static int Gmax;
typedef struct { u128 r0, r1; u64 cnt[130]; ws_t W; } job_t; /* cnt[G] = #classes mod p^Gmax with g>=G (weighted) */
static void addval(u64*cnt,int c,u128 weight){ for(int G=0;G<=c && G<=Gmax;G++) cnt[G]+=(u64)weight; }
static void dfs(ws_t*W,u64*cnt,u128 r,int k,int c){
  /* class r mod p^k, c = min(g(r),Gmax) with c >= k (so class has g>=k). */
  if(k==Gmax){ addval(cnt,Gmax,1); return; }
  for(int d=0; d<p; d++){
    u128 r2 = r + (u128)d*pw[k];
    int c2 = (d==0)? c : gval(W,r2,Gmax);
    if(c2>=k+1) dfs(W,cnt,r2,k+1,c2);
    else { /* g = c2 on r2 + p^{c2+1} Z_p, which contains the class r2 mod p^{k+1} since c2+1<=k+1 */
      addval(cnt,c2,pw[Gmax-(k+1)]); }
  }
}
static int Lcut;
static void *censusjob(void*a){ job_t*J=a; ps_init(&J->W.A); ps_init(&J->W.B);
  for(u128 r=J->r0;r<J->r1;r++){ int c=gval(&J->W,r,Gmax);
    if(c>=Lcut) dfs(&J->W,J->cnt,r,Lcut,c); else addval(J->cnt,c,pw[Gmax-Lcut]); }
  return NULL; }
/* ---------------- Monte Carlo ---------------- */
static u64 rng_s[64][2];
static u64 xr(u64*s){ u64 s1=s[0]; const u64 s0=s[1]; s[0]=s0; s1^=s1<<23; s[1]=s1^s0^(s1>>17)^(s0>>26); return s[1]+s0; }
typedef struct { int id; u64 ns; int cap; u64 hist[130]; u64 h16[130][16]; ws_t W; } mjob_t;
static void *mcjob(void*a){ mjob_t*J=a; ps_init(&J->W.A); ps_init(&J->W.B);
  for(u64 i=0;i<J->ns;i++){
    u128 x=((u128)xr(rng_s[J->id])<<64)|xr(rng_s[J->id]); x%=pw[J->cap];
    int c=gval(&J->W,x,J->cap); J->hist[c]++; J->h16[c][(int)(x%16)]++; }
  return NULL; }
int main(int argc,char**argv){
  p=atoi(argv[2]); pw[0]=1; for(int i=1;i<130;i++){ pw[i]=pw[i-1]*p; if(pw[i]>((u128)1<<126)) { pw[i]=0; break; } }
  if(!strcmp(argv[1],"census")){
    Gmax=atoi(argv[3]); int NT=atoi(argv[4]);
    Lcut=1; while(pw[Lcut]<(u128)(64*NT) && Lcut<Gmax) Lcut++;
    int NJ=(int)pw[Lcut];  /* one job per top class, NT worker threads pull jobs */
    job_t*J=calloc(NJ,sizeof(job_t)); pthread_t th[64];
    for(int t=0;t<NJ;t++){ J[t].r0=t; J[t].r1=t+1; }
    int done=0;
    while(done<NJ){ int nt=0; for(;nt<NT && done+nt<NJ;nt++) pthread_create(&th[nt],0,censusjob,&J[done+nt]); for(int t=0;t<nt;t++) pthread_join(th[t],0); done+=nt; }
    u64 cnt[130]={0}; for(int t=0;t<NJ;t++) for(int G=0;G<=Gmax;G++) cnt[G]+=J[t].cnt[G];
    for(int G=0;G<=Gmax;G++){ u128 tot=pw[G]; u64 c=cnt[G]/(u64)pw[Gmax-G];
      printf("p=%d G=%d survivors_mod_p^G=%llu  delta=%.10f  (exact div check %d)\n",p,G,(unsigned long long)c,(double)c/(double)tot,(int)(cnt[G]%(u64)pw[Gmax-G]==0)); }
    return 0;
  }
  if(!strcmp(argv[1],"mc")){
    int cap=atoi(argv[3]); u64 ns=strtoull(argv[4],0,10); u64 seed=strtoull(argv[5],0,10); int NT=atoi(argv[6]);
    mjob_t*J=calloc(NT,sizeof(mjob_t)); pthread_t th[64];
    for(int t=0;t<NT;t++){ J[t].id=t; J[t].ns=ns/NT; J[t].cap=cap; rng_s[t][0]=seed*2654435761ULL+t*0x9E3779B97F4A7C15ULL+1; rng_s[t][1]=(seed^0xDEADBEEFULL)+977*t+7; for(int k=0;k<20;k++) xr(rng_s[t]); pthread_create(&th[t],0,mcjob,&J[t]); }
    u64 h[130]={0}, h16[130][16]; memset(h16,0,sizeof h16); u64 N=0;
    for(int t=0;t<NT;t++){ pthread_join(th[t],0); for(int c=0;c<=cap;c++){ h[c]+=J[t].hist[c]; for(int r=0;r<16;r++) h16[c][r]+=J[t].h16[c][r]; } N+=J[t].ns; }
    printf("# mc p=%d cap=%d N=%llu seed=%llu\n",p,cap,(unsigned long long)N,(unsigned long long)seed);
    for(int c=0;c<=cap;c++) if(h[c]){ printf("g=%d count=%llu",c,(unsigned long long)h[c]); if(p==2){ printf(" by_x_mod16:"); for(int r=0;r<16;r++) printf(" %llu",(unsigned long long)h16[c][r]); } printf("\n"); }
    return 0;
  }
  if(!strcmp(argv[1],"one")){ /* gval for a given integer x < 2^63 */
    int cap=atoi(argv[3]); u64 x=strtoull(argv[4],0,10); ws_t W; ps_init(&W.A); ps_init(&W.B);
    printf("p=%d x=%llu min(g,%d)=%d\n",p,(unsigned long long)x,cap,gval(&W,(u128)x%pw[cap],cap)); return 0; }
  return 1;
}
