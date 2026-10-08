/* Referee's independent subset-sum coverage checker.
   stdin: M n x_1 ... x_n   (0 <= x_i < M, M < 2^40)
   Computes the set of subset sums (including empty sum) of x_i mod M as a bitset
   and prints the number of residues NOT reached (0 means full coverage).
   Optional argv[1]="list": also print up to 50 missing residues. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static u64 M, W;
static u64 *B, *T;
static inline int getbit(const u64 *a, u64 i){ return (a[i>>6]>>(i&63))&1; }
/* read 64 bits of T starting at cyclic bit position pos (mod M) */
static inline u64 get64(u64 pos){
  if (pos + 64 <= M) {
    u64 w = pos>>6, o = pos&63;
    if (!o) return T[w];
    u64 lo = T[w]>>o;
    u64 hi = (w+1 < W) ? (T[w+1]<<(64-o)) : 0;
    return lo|hi;
  }
  u64 r=0;
  for (int k=0;k<64;k++){ u64 q=pos+k; if(q>=M) q-=M; r |= (u64)getbit(T,q)<<k; }
  return r;
}
int main(int argc, char**argv){
  u64 n;
  if (scanf("%llu %llu",(unsigned long long*)&M,(unsigned long long*)&n)!=2) return 1;
  W = (M+63)/64;
  B = calloc(W, 8); T = malloc(W*8);
  if(!B||!T){fprintf(stderr,"alloc fail\n");return 2;}
  B[0]=1;
  u64 lastmask = (M%64)? ((1ULL<<(M%64))-1) : ~0ULL;
  for (u64 k=0;k<n;k++){
    unsigned long long x; if(scanf("%llu",&x)!=1) return 1;
    x %= M; if (x==0) continue;
    memcpy(T,B,W*8);
    /* new[i] = B[i] | T[i-x mod M]; for word w, bits 64w..64w+63 come from T at pos 64w - x mod M */
    u64 start = M - x; /* (0 - x) mod M */
    for (u64 w=0; w<W; w++){
      u64 pos = start + 64*w; if (pos>=M) pos-=M;
      B[w] |= get64(pos);
    }
    B[W-1] &= lastmask;
  }
  u64 cnt=0;
  for (u64 w=0;w<W;w++) cnt += __builtin_popcountll(B[w]);
  printf("missing %llu of %llu\n",(unsigned long long)(M-cnt),(unsigned long long)M);
  if (argc>1 && !strcmp(argv[1],"list")){
    int c=0; for(u64 i=0;i<M && c<50;i++) if(!getbit(B,i)){printf("%llu ",(unsigned long long)i);c++;}
    printf("\n");
  }
  return 0;
}
