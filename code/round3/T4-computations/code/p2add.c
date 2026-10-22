// p2add.c -- exact min(g_2(a), CAP) for a natural number a, by the carry recursion with additions only.
// State after processing terms b < n (e_0 = 1 forced): c = S_n / 2^{V_n} mod 2^{r}, r = CAP - V_n,
// where S_n = sum_{b<n} e_b pi_b(a), V_n = v_2(pi_n(a)); omega = pi_n(a)/2^{V_n} mod 2^r (odd).
// Step (term b = n): t = v_2(a+n+1).  If t >= r: g >= CAP iff some c + e*omega == 0 mod 2^r; else g = V_n + max v_2(c+e*omega).
// Else children y = c + e*omega mod 2^r with v_2(y) >= t -> nc = y >> t (mod 2^{r-t}); omega <- omega * ((a+n+1)>>t) mod 2^{r-t}.
// No children -> g = V_n + max_{c,e} v_2(y) (exact, see writeup).  Distinct carries are deduplicated (lossless for the decision).
// Usage: p2add CAP a [POPLIM_log2]      prints: a g_capped maxpop steps seconds
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
static int HB=23; static uint32_t *hidx; static uint32_t *hstamp; static uint32_t cur=0;
static inline u64 hashk(const u64*k,int nl){ u64 h=0x9E3779B97F4A7C15ULL; for(int i=0;i<nl;i++){ h^=k[i]; h*=0xBF58476D1CE4E5B9ULL; h^=h>>29; } return h; }
static inline int ctzml(const u64*a,int nl){ for(int i=0;i<nl;i++) if(a[i]) return 64*i+__builtin_ctzll(a[i]); return 64*nl; }
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: p2add CAP a [poplim_log2]\n"); return 1; }
    int CAP=atoi(argv[1]); u64 a=strtoull(argv[2],0,10); long POPLIM = 1L<<(argc>3?atoi(argv[3]):21);
    clock_t t0=clock();
    hidx=malloc(sizeof(uint32_t)<<HB); hstamp=calloc(1<<HB,sizeof(uint32_t));
    int r=CAP; int nl=(r+63)/64; u64 *buf=calloc(nl,8); long np=1; // c=0
    u64 *om=calloc(nl,8); om[0]=1; u64 *y=malloc(8*nl);
    long maxpop=1; long n=0; int first=1; long V=0;
    while(1){
        u64 m=a+n+1; int t=__builtin_ctzll(m);
        int lastlimb=(r-1)/64; u64 topmask=(r%64)? ((1ULL<<(r%64))-1) : ~0ULL;
        if(t>=r){ int best=-1;
            for(long i=0;i<np;i++){ u64*c=buf+i*nl;
                for(int e=first;e<=1;e++){ u64 cy=0; for(int j=0;j<nl;j++){ u128 s=(u128)c[j]+(e?om[j]:0)+cy; y[j]=(u64)s; cy=(u64)(s>>64);} y[lastlimb]&=topmask;
                    int v=ctzml(y,nl); if(v>=r){ printf("%llu %d %ld %ld %.1f\n",(unsigned long long)a,CAP,maxpop,n,(double)(clock()-t0)/CLOCKS_PER_SEC); return 0; }
                    if(v>best) best=v; } }
            printf("%llu %ld %ld %ld %.1f\n",(unsigned long long)a,V+best,maxpop,n,(double)(clock()-t0)/CLOCKS_PER_SEC); return 0; }
        int rn=r-t; int nln=(rn+63)/64; int lastn=(rn-1)/64; u64 topn=(rn%64)?((1ULL<<(rn%64))-1):~0ULL;
        long cap2=2*np; u64 *nb=malloc((size_t)cap2*nln*8); if(!nb){ fprintf(stderr,"oom\n"); return 2; }
        long nn=0; cur++; if(cur==0){ memset(hstamp,0,sizeof(uint32_t)<<HB); cur=1; }
        int best=-1;
        for(long i=0;i<np;i++){ u64*c=buf+i*nl;
            for(int e=first;e<=1;e++){ u64 cy=0; for(int j=0;j<nl;j++){ u128 s=(u128)c[j]+(e?om[j]:0)+cy; y[j]=(u64)s; cy=(u64)(s>>64);} y[lastlimb]&=topmask;
                int v=ctzml(y,nl); if(v<t){ if(v>best) best=v; continue; }
                // nc = y >> t, nln limbs
                u64 *nc=nb+nn*nln; int q=t/64, s=t%64;
                for(int j=0;j<nln;j++){ u64 lo=(j+q<nl)? (y[j+q]>>s):0; u64 hi=(s && j+q+1<nl)? (y[j+q+1]<<(64-s)):0; nc[j]=lo|hi; }
                nc[lastn]&=topn;
                u64 h=hashk(nc,nln)>>(64-HB);
                while(1){ if(hstamp[h]!=cur){ hstamp[h]=cur; hidx[h]=(uint32_t)nn; nn++; break; }
                    if(!memcmp(nb+(size_t)hidx[h]*nln,nc,8*nln)) break; h=(h+1)&((1UL<<HB)-1); }
                if(nn>=POPLIM){ fprintf(stderr,"population overflow at n=%ld (POPLIM=%ld)\n",n,POPLIM); printf("%llu -1 %ld %ld\n",(unsigned long long)a,maxpop,n); return 3; }
            } }
        if(nn==0){ printf("%llu %ld %ld %ld %.1f\n",(unsigned long long)a,V+best,maxpop,n,(double)(clock()-t0)/CLOCKS_PER_SEC); return 0; }
        if(nn>maxpop) maxpop=nn;
        // omega <- omega * u mod 2^rn
        { u64 u=m>>t; u64 cy=0; for(int j=0;j<nln;j++){ u128 s=(u128)om[j]*u+cy; om[j]=(u64)s; cy=(u64)(s>>64);} om[lastn]&=topn; }
        free(buf); buf=nb; np=nn; r=rn; nl=nln; V+=t; n++; first=0;
    }
}
