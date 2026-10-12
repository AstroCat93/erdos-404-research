/*
 * twofree.c -- twist-free ("2D") covering test for the gate windows of note.md Thm 3.12.
 *
 * Window of length H before N* = p^t K' :  y_i(X) = prod_{s=1}^{i} (X - (H-s)),  X = p^t K'.
 * As polynomials in Z[X]:  y_i(X) = sigma_i + X tau_i + X^2 (...).
 * If t >= c := v_p((H-1)!), then modulo p^{t+c} only sigma_i and tau_i matter, and
 *     y_i(X) == sigma_i + p^t K' tau_i   (mod p^{t+c}),
 * where only tau_i mod p^c matters.
 *
 * Criterion E2D(p,t,H): for every T in Z/p^{t+c} there is S subset [0,H) with
 *     sum_{i in S} sigma_i == T (mod p^{t+c})   and   sum_{i in S} tau_i == 0 (mod p^c).
 * E2D(p,t,H) implies Cov(p,t,H) (for EVERY K', unit or not), because then
 * sum_S y_i(X) == T + p^t K' * 0 == T.
 *
 * The program also reports, from the same 2D table Z = {(A_S mod p^{t+c}, B_S mod p^c)},
 * the number of unit classes K' mod p^c for which Cov fails (i.e. the projection
 * (A,B) -> A + p^t K' B is not onto), as an independent re-derivation of cov.c.
 *
 * usage: twofree p t Hmin Hmax [maxlog2bits=34] [checkcov=1]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int vpf(long long n,long long p){ int s=0; while(n){ n/=p; s+=(int)n; } return s; }

/* bit helpers on a row of length L bits stored in W words (L = p^M) */
static inline int getb(const uint64_t *b, uint64_t i){ return (b[i>>6]>>(i&63))&1; }

/* dst_row |= cyclic_shift(src_row, s) for a row of L bits in W words */
static void cyc_or(uint64_t *dst, const uint64_t *src, uint64_t L, size_t W, uint64_t s){
    /* bits x -> x+s if x+s<L ; x -> x+s-L otherwise */
    if (s==0){ for(size_t i=0;i<W;i++) dst[i]|=src[i]; return; }
    /* part 1: dst[x+s] |= src[x] for x < L-s  (left shift by s, drop bits >= L) */
    size_t ws=s/64; unsigned bs=s%64;
    if (ws < W){
        if(!bs){ for(size_t i=W;i-->ws;) dst[i]|=src[i-ws]; }
        else { for(size_t i=W-1;i>ws;i--) dst[i]|=(src[i-ws]<<bs)|(src[i-ws-1]>>(64-bs)); dst[ws]|=src[0]<<bs; }
    }
    /* mask top */
    uint64_t r=L%64; if(r) dst[W-1]&=((uint64_t)1<<r)-1;
    /* part 2: dst[x+s-L] |= src[x] for x >= L-s : right shift by L-s */
    uint64_t s2=L-s; ws=s2/64; bs=s2%64;
    if (ws < W){
        if(!bs){ for(size_t i=0;i+ws<W;i++) dst[i]|=src[i+ws]; }
        else { for(size_t i=0;i+ws+1<W;i++) dst[i]|=(src[i+ws]>>bs)|(src[i+ws+1]<<(64-bs)); dst[W-1-ws]|=src[W-1]>>bs; }
    }
    if(r) dst[W-1]&=((uint64_t)1<<r)-1;
}

int main(int argc,char**argv){
    if(argc<5){ fprintf(stderr,"usage: %s p t Hmin Hmax [maxlog2] [checkcov]\n",argv[0]); return 1; }
    long long p=atoll(argv[1]); int t=atoi(argv[2]); int Hmin=atoi(argv[3]), Hmax=atoi(argv[4]);
    int maxlog=argc>5?atoi(argv[5]):34; int checkcov=argc>6?atoi(argv[6]):1;
    for(int H=Hmin; H<=Hmax; H++){
        int c=vpf(H-1,p), M=t+c;
        if (t < c){ printf("p=%lld t=%d H=%d c=%d: t<c, X^2 terms may matter; skipped\n",p,t,H,c); continue; }
        uint64_t L=1, R=1; for(int i=0;i<M;i++) L*=p; for(int i=0;i<c;i++) R*=p;
        double lg=0; { long double tot=(long double)L*R; while(tot>1){tot/=2;lg++;} }
        if (lg>maxlog){ printf("p=%lld t=%d H=%d c=%d: 2^%.0f bits too large\n",p,t,H,c,lg); continue; }
        if (H<64 && ((uint64_t)1<<H) < L){ printf("p=%lld t=%d H=%d c=%d M=%d: 2^H < p^M, Cov impossible\n",p,t,H,c,M); continue; }
        size_t W=(L+63)/64;
        uint64_t *Z=calloc((size_t)W*R,8), *T=malloc((size_t)W*R*8);
        if(!Z||!T){ fprintf(stderr,"alloc failed\n"); return 2; }
        /* sigma_i mod L and tau_i mod R via (constant, linear) coefficients of prod (X - (H-s)) mod L */
        /* poly f = a0 + a1 X ; multiply by (X - m): a0' = -m a0 ; a1' = a0 - m a1 */
        uint64_t a0=1%L, a1=0;  /* track a1 mod L too (only need mod R, R | L since c <= t) */
        Z[0]=1; /* (A,B)=(0,0) */
        for(int i=0;i<H;i++){
            if(i>0){ uint64_t m=(uint64_t)(H-i)%L;
                uint64_t n0=(uint64_t)(((unsigned __int128)(L-m)%L*a0)%L);
                uint64_t n1=(uint64_t)((a0 + (unsigned __int128)((L-m)%L)*a1)%L);
                a0=n0; a1=n1; }
            uint64_t sA=a0%L, sB=a1%R;
            memcpy(T,Z,(size_t)W*R*8);
            for(uint64_t b=0;b<R;b++){
                uint64_t nb=(b+sB)%R;
                cyc_or(Z+nb*W, T+b*W, L, W, sA);
            }
        }
        /* E2D: row B=0 full? */
        uint64_t miss0=0; for(uint64_t x=0;x<L;x++) if(!getb(Z,x)) miss0++;
        printf("p=%lld t=%d H=%d c=%d M=%d : E2D row(B=0) missing=%llu of %llu%s",p,t,H,c,M,(unsigned long long)miss0,(unsigned long long)L, miss0==0?"  => E2D HOLDS":"");
        if(checkcov && c>0){
            /* for each unit K' mod R: projection onto A + p^t K' B mod L must be onto */
            uint64_t ptL=1; for(int i=0;i<t;i++) ptL=(uint64_t)(((unsigned __int128)ptL*p)%L);
            uint64_t *P=malloc(W*8); long long nfail=0, ncls=0;
            for(uint64_t K=1;K<R;K++){ if(K%p==0) continue; ncls++;
                memset(P,0,W*8);
                for(uint64_t b=0;b<R;b++){
                    uint64_t sh=(uint64_t)(((unsigned __int128)ptL*((K*b)%R))%L);
                    cyc_or(P, Z+b*W, L, W, sh);
                }
                uint64_t pc=0; for(size_t i=0;i<W;i++) pc+=__builtin_popcountll(P[i]);
                if(pc!=L) nfail++;
            }
            printf(" | Cov: %lld/%lld unit classes fail%s", nfail, ncls, nfail==0?" => Cov HOLDS":"");
            free(P);
        }
        printf("\n"); fflush(stdout);
        free(Z); free(T);
    }
    return 0;
}
