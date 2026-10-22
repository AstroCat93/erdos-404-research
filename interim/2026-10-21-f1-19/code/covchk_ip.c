/*
 * covchk_ip.c -- PROGRAM C' (track T3b, round 3, 2026-10-12).
 * Derived from program C (publish-erdos404/code/round2/review/computation/covchk.c, written by the
 * round-2 computational referee).  Same element computation (z_i = prod (N*-H+s) mod p^M), same
 * two-list split of the low elements, same bucket logic, same final popcount test.
 * CHANGED: the cyclic shift-OR  X <- X | (X + w)  is done IN PLACE with a save buffer of at most
 * p^(M-k)/2 bits (one fibre bitset instead of two).  The in-place kernel (or_off_desc / or_off_alias)
 * is written independently of the kernel in fibcov_ip.c (program A').
 *
 * usage: covchk_ip p t H k MODE ...
 *   MODE pos  K1 K2 ...        actual positions N* = p^t K
 *   MODE cls  LIFT             all unit classes K' mod p^c, each represented by K' + LIFT*p^c
 *   MODE clsrange LIFT i0 i1   unit classes with index in [i0,i1) (in increasing order of K')
 * env STOPFIRST=1: stop at the first non-covering K; STOPFIBRE=1: stop a K at its first bad fibre
 *     (then the reported count is only a lower bound and is marked so).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef uint64_t u64;

static u64 p, Q, PK, F;
static int t, H, c, M, k;
static size_t NW, NSAVE;
static u64 tailmask;

static double wall(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }
static int legendre(u64 n){ int s=0; while(n){ n/=p; s+=(int)n; } return s; }
static u64 pw(u64 b,int e){ u64 r=1; for(int i=0;i<e;i++){ if(r > (((u64)1)<<62) / b){fprintf(stderr,"overflow\n");exit(2);} r*=b;} return r; }
static u64 mm(u64 a,u64 b){ return (u64)(((u128)a*b)%Q); }

/* read 64 bits of X starting at bit position pos (linear; pad words are zero) */
static inline u64 win(const u64 *X, u64 pos){
    u64 w = pos>>6; unsigned o = pos&63;
    if(!o) return X[w];
    return (X[w]>>o) | (X[w+1]<<(64-o));
}
/* dst bits [d0, d0+n) |= src bits [s0, s0+n), ASCENDING.  dst and src MAY alias provided s0 >= d0
   (every source bit is then read before any bit at or above it is written). */
static void or_off_alias(u64 *dst, const u64 *src, u64 d0, u64 s0, u64 n){
    if(n==0) return;
    u64 d = d0, s = s0, end = d0+n;
    while(d<end && (d&63)){
        if((src[s>>6]>>(s&63))&1) dst[d>>6] |= 1ULL<<(d&63);
        d++; s++;
    }
    u64 nwords = (end-d)>>6;
    for(u64 q=0;q<nwords;q++){ u64 v = win(src, s + 64*q); dst[(d>>6)+q] |= v; }
    d += nwords<<6; s += nwords<<6;
    while(d<end){
        if((src[s>>6]>>(s&63))&1) dst[d>>6] |= 1ULL<<(d&63);
        d++; s++;
    }
}
/* dst bits [d0, d0+n) |= src bits [s0, s0+n), DESCENDING.  dst and src MAY alias provided s0 <= d0. */
static void or_off_desc(u64 *dst, const u64 *src, u64 d0, u64 s0, u64 n){
    if(n==0) return;
    u64 d = d0+n, s = s0+n;             /* exclusive ends */
    while(d>d0 && (d&63)){
        d--; s--;
        if((src[s>>6]>>(s&63))&1) dst[d>>6] |= 1ULL<<(d&63);
    }
    u64 nwords = (d-d0)>>6;
    for(u64 q=1;q<=nwords;q++){ u64 v = win(src, s - 64*q); dst[(d>>6)-q] |= v; }
    d -= nwords<<6; s -= nwords<<6;
    while(d>d0){
        d--; s--;
        if((src[s>>6]>>(s&63))&1) dst[d>>6] |= 1ULL<<(d&63);
    }
}
/* SAVE bits [0,n) := X bits [a, a+n) */
static void save_bits(u64 *SAVE, const u64 *X, u64 a, u64 n){
    u64 nw = (n+63)>>6;
    for(u64 q=0;q<nw;q++) SAVE[q] = win(X, a + 64*q);
    if(n&63) SAVE[nw-1] &= (1ULL<<(n&63))-1;
    SAVE[nw] = 0; SAVE[nw+1] = 0;
}
static u64 *SAVE;
/* in place: X[x] |= X[(x-w) mod F] for all x in [0,F); 0 < w < F */
static void cyc_or_inplace(u64 *X, u64 w){
    if(w==0) return;
    if(2*w <= F){
        save_bits(SAVE, X, F-w, w);          /* original bits [F-w,F) */
        or_off_desc(X, X, w, 0, F-w);        /* x in [w,F): source x-w in [0,F-w), descending */
        or_off_alias(X, SAVE, 0, 0, w);      /* x in [0,w): source x-w+F */
    } else {
        u64 u = F-w;                         /* x-w == x+u mod F, u < F/2 */
        save_bits(SAVE, X, 0, u);            /* original bits [0,u) */
        or_off_alias(X, X, 0, u, F-u);       /* x in [0,F-u): source x+u, ascending */
        or_off_alias(X, SAVE, F-u, 0, u);    /* x in [F-u,F): source x+u-F */
    }
    X[NW-1] &= tailmask; X[NW] = 0; X[NW+1] = 0;
}
static u64 popc(const u64 *X){ u64 s=0; for(size_t j=0;j<NW;j++) s+=__builtin_popcountll(X[j]); return s; }

static u64 *bufA;

/* returns number of residues mod Q not covered (exact unless stopfibre) */
static u64 check(u64 Kpos, int stopfibre, int *partial){
    *partial = 0;
    u64 Nst = mm(pw(p,t)%Q, Kpos%Q);
    u64 *z = malloc(8*H); int *v = malloc(sizeof(int)*H);
    z[0] = 1%Q;
    for(int i=1;i<H;i++){
        u64 f = (Nst + Q - (u64)H%Q + (u64)i) % Q;   /* N* - H + i  mod Q */
        z[i] = mm(z[i-1], f);
    }
    u64 *lo = malloc(8*H), *hi = malloc(8*H); int nlo=0, nhi=0;
    for(int i=0;i<H;i++){
        u64 a = z[i]; int e=0;
        if(a==0){ fprintf(stderr,"z_%d=0 mod Q\n",i); exit(4);}
        while(a%p==0){ a/=p; e++; }
        int expect = legendre(H-1) - legendre(H-1-i);
        if(e!=expect){ fprintf(stderr,"valuation check failed i=%d %d vs %d\n",i,e,expect); exit(4);}
        v[i]=e;
        if(e<k) lo[nlo++] = z[i]; else hi[nhi++] = (z[i]/PK) % F;
    }
    int n2 = nlo < 22 ? nlo : 22; int n1 = nlo - n2;
    size_t N2 = (size_t)1<<n2, N1 = (size_t)1<<n1;
    u64 *raw = malloc(8*N2);
    for(size_t m=0;m<N2;m++){
        if(m==0){ raw[0]=0; continue; }
        int b = __builtin_ctzll(m);
        u64 s = raw[m & (m-1)] + lo[b]; if(s>=Q) s-=Q; raw[m]=s;
    }
    size_t *start = calloc(PK+1, sizeof(size_t));
    for(size_t m=0;m<N2;m++) start[raw[m]%PK + 1]++;
    for(u64 r=0;r<PK;r++) start[r+1]+=start[r];
    u64 *bk = malloc(8*N2); size_t *pos = malloc(sizeof(size_t)*PK);
    for(u64 r=0;r<PK;r++) pos[r]=start[r];
    for(size_t m=0;m<N2;m++){ u64 r = raw[m]%PK; bk[pos[r]++] = raw[m]; }
    free(raw); free(pos);
    u64 *outer = malloc(8*N1);
    for(size_t m=0;m<N1;m++){
        if(m==0){ outer[0]=0; continue; }
        int b = __builtin_ctzll(m);
        u64 s = outer[m&(m-1)] + lo[n2+b]; if(s>=Q) s-=Q; outer[m]=s;
    }
    u64 miss = 0;
    for(u64 r=0;r<PK;r++){
        u64 *X = bufA;
        memset(X, 0, (NW+2)*8);
        for(size_t q=0;q<N1;q++){
            u64 s1 = outer[q];
            u64 need = (r + PK - s1%PK) % PK;
            for(size_t j=start[need]; j<start[need+1]; j++){
                u64 a = s1 + bk[j]; if(a>=Q) a-=Q;
                u64 d = (a + Q - r) % Q;          /* divisible by PK */
                u64 u = d / PK;
                X[u>>6] |= 1ULL<<(u&63);
            }
        }
        for(int h=0;h<nhi;h++) cyc_or_inplace(X, hi[h]);
        X[NW-1] &= tailmask;
        u64 cnt = popc(X);
        if(cnt != F){ miss += F-cnt; if(stopfibre){ *partial=1; break; } }
    }
    free(z); free(v); free(lo); free(hi); free(start); free(bk); free(outer);
    return miss;
}

int main(int argc, char **argv){
    if(argc<6){ fprintf(stderr,"usage\n"); return 1; }
    p = strtoull(argv[1],0,10); t=atoi(argv[2]); H=atoi(argv[3]); k=atoi(argv[4]);
    const char *mode = argv[5];
    c = legendre(H-1); M = t + c;
    if((u64)H > pw(p,t)){ fprintf(stderr,"H>p^t\n"); return 1; }
    Q = pw(p,M); PK = pw(p,k); F = Q/PK;
    NW = (F+63)/64; tailmask = (F%64) ? ((1ULL<<(F%64))-1) : ~0ULL;
    NSAVE = (F/2+63)/64 + 3;
    bufA = calloc(NW+2, 8); SAVE = calloc(NSAVE, 8);
    if(!bufA||!SAVE){ fprintf(stderr,"alloc\n"); return 2; }
    int stopfirst = getenv("STOPFIRST")!=NULL, stopfibre = getenv("STOPFIBRE")!=NULL;
    u64 *Ks=NULL; size_t nK=0;
    Ks = malloc(8*(1<<22));
    if(!strcmp(mode,"pos")){ for(int a=6;a<argc;a++) Ks[nK++]=strtoull(argv[a],0,10); }
    else if(!strcmp(mode,"cls")||!strcmp(mode,"clsrange")){
        u64 lift = strtoull(argv[6],0,10);
        u64 pc = pw(p,c);
        size_t i0=0, i1=(size_t)-1;
        if(!strcmp(mode,"clsrange")){ i0=strtoull(argv[7],0,10); i1=strtoull(argv[8],0,10); }
        size_t idx=0;
        for(u64 K=1; K<=pc; K++){
            if(pc>1 && K==pc) break;
            if(K%p==0) continue;
            if(idx>=i0 && idx<i1) Ks[nK++] = K + lift*pc;
            idx++;
            if(pc==1) break;
        }
    } else { fprintf(stderr,"mode\n"); return 1; }
    printf("# covchk_ip(C') p=%llu t=%d H=%d c=%d M=%d k=%d F=%llu nK=%zu (bitset %zu MB + save %zu MB)\n",(unsigned long long)p,t,H,c,M,k,(unsigned long long)F,nK, (NW*8)>>20, (NSAVE*8)>>20);
    fflush(stdout);
    size_t bad=0; double T0=wall();
    for(size_t q=0;q<nK;q++){
        if(Ks[q]%p==0){ printf("skip K=%llu\n",(unsigned long long)Ks[q]); continue; }
        double t1=wall(); int partial;
        u64 miss = check(Ks[q], stopfibre, &partial);
        printf("C p=%llu t=%d H=%d M=%d K=%llu Kmodpc=%llu miss=%llu%s %s %.2fs\n",(unsigned long long)p,t,H,M,
            (unsigned long long)Ks[q],(unsigned long long)(Ks[q]%pw(p,c)),(unsigned long long)miss, partial?"+(partial)":"",
            miss?"UNCOVERED":"COVERED", wall()-t1);
        fflush(stdout);
        if(miss){ bad++; if(stopfirst) break; }
    }
    printf("END C' p=%llu t=%d H=%d nK=%zu bad=%zu %s %.1fs\n",(unsigned long long)p,t,H,nK,bad,bad?"SOME_UNCOVERED":"ALL_COVERED",wall()-T0);
    return 0;
}
