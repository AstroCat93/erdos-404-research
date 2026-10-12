/*
 * miss.c -- list the residues NOT covered by the subset sums of the window
 *     y_i(X) = prod_{s=1}^{i} (X - (H-s)),  0 <= i < H,   X = p^t K   (mod p^M),
 * where M = t + c + k, c = v_p((H-1)!), k >= 0 an extra "surplus" depth.
 * K may be any integer (unit or not).  With k = 0 and K a unit this is the
 * Cov(p,t,H) test of note.md Thm 3.12 at the single class K.
 *
 * usage: miss p t H K [k=0] [maxlist=50]
 * prints: M, number of missing residues, and up to maxlist missing residues r
 *         (as r in [0,p^M) and balanced r - p^M if r > p^M/2).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t Q; static size_t NW; static uint64_t *Bs, *Tmp;
static void mask_top(uint64_t *b){ uint64_t r=Q%64; if(r) b[NW-1]&=((uint64_t)1<<r)-1; }
static void shl_or(uint64_t *d,const uint64_t *s,uint64_t sh){ size_t ws=sh/64; unsigned bs=sh%64; if(ws>=NW) return;
  if(!bs){ for(size_t i=NW;i-->ws;) d[i]|=s[i-ws]; } else { for(size_t i=NW-1;i>ws;i--) d[i]|=(s[i-ws]<<bs)|(s[i-ws-1]>>(64-bs)); d[ws]|=s[0]<<bs; } }
static void shr_or(uint64_t *d,const uint64_t *s,uint64_t sh){ size_t ws=sh/64; unsigned bs=sh%64; if(ws>=NW) return;
  if(!bs){ for(size_t i=0;i+ws<NW;i++) d[i]|=s[i+ws]; } else { for(size_t i=0;i+ws+1<NW;i++) d[i]|=(s[i+ws]>>bs)|(s[i+ws+1]<<(64-bs)); d[NW-1-ws]|=s[NW-1]>>bs; } }
static int vpf(long long n,long long p){ int s=0; while(n){ n/=p; s+=(int)n; } return s; }

int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage: %s p t H K [k] [maxlist]\n",argv[0]); return 1; }
  long long p=atoll(argv[1]); int t=atoi(argv[2]); int H=atoi(argv[3]); long long K=atoll(argv[4]);
  int k=argc>5?atoi(argv[5]):0; int maxlist=argc>6?atoi(argv[6]):50;
  int c=vpf(H-1,p), M=t+c+k; uint64_t q=1;
  for(int i=0;i<M;i++){ if(q>UINT64_MAX/(uint64_t)p){ fprintf(stderr,"modulus too large\n"); return 1;} q*=(uint64_t)p; }
  Q=q; NW=(Q+63)/64; Bs=calloc(NW,8); Tmp=malloc(NW*8);
  if(!Bs||!Tmp){ fprintf(stderr,"alloc\n"); return 2; }
  uint64_t X=1; for(int i=0;i<t;i++) X=(uint64_t)(((unsigned __int128)X*(uint64_t)p)%Q);
  long long Km = K % (long long)Q; if (Km<0) Km += (long long)Q;
  X=(uint64_t)(((unsigned __int128)X*(uint64_t)Km)%Q);
  uint64_t y=1; Bs[0]=1;
  for(int i=0;i<H;i++){
    if(i>0){ uint64_t f=(X+Q-((uint64_t)(H-i)%Q))%Q; y=(uint64_t)(((unsigned __int128)y*f)%Q); }
    if(y==0) continue;
    memcpy(Tmp,Bs,NW*8); shl_or(Bs,Tmp,y); shr_or(Bs,Tmp,Q-y); mask_top(Bs);
  }
  uint64_t pc=0; for(size_t i=0;i<NW;i++) pc+=__builtin_popcountll(Bs[i]);
  printf("p=%lld t=%d H=%d K=%lld c=%d k=%d M=%d missing=%llu of %llu\n",p,t,H,K,c,k,M,(unsigned long long)(Q-pc),(unsigned long long)Q);
  int listed=0;
  for(uint64_t r=0;r<Q && listed<maxlist;r++){
    if(!((Bs[r/64]>>(r%64))&1)){ long long b=(r>Q/2)?(long long)r-(long long)Q:(long long)r;
      printf("  miss %llu  bal %lld\n",(unsigned long long)r,b); listed++; }
  }
  return 0;
}
