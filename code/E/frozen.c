// Frozen residues Phi_p via the j-formulation:
//   r = p-1-j is frozen  iff  (-1)^j / j!  notin  S_j  (mod p),
//   S_0 = {0},  S_{j+1} = S_j u (S_j + (-1)^{j+1}/j!).
// Once S_j = Z/p every smaller r is non-frozen.
// usage: frozen pmax  -> lines "p |Phi_p| Jfull list_of_j"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
static u64 pw(u64 b, u64 e, u64 m){u64 r=1;b%=m;while(e){if(e&1)r=(unsigned __int128)r*b%m;b=(unsigned __int128)b*b%m;e>>=1;}return r;}
int main(int argc,char**argv){
  u64 pmax=strtoull(argv[1],0,10);
  char *comp=calloc(pmax+1,1);
  unsigned char *S=malloc(pmax+1), *T=malloc(pmax+1);
  for(u64 p=2;p<=pmax;p++){ if(comp[p]) continue; for(u64 q=p*p;q<=pmax;q+=p) comp[q]=1;
    memset(S,0,p); S[0]=1; u64 cnt=1; u64 fact=1; // fact = j! mod p
    printf("%llu",(unsigned long long)p);
    int nfz=0; char buf[4096]; int bl=0; long Jfull=-1;
    for(u64 j=0;j<p;j++){
      if(j>0) fact=fact*j%p;
      u64 inv=pw(fact,p-2,p);
      u64 x = (j%2==0)? inv : (p-inv)%p;      // (-1)^j/j!
      if(!S[x]){ nfz++; if(bl<4000) bl+=snprintf(buf+bl,4096-bl," %llu",(unsigned long long)j); }
      if(cnt==p){ Jfull=j; break; }
      u64 y = (p - x)%p;                         // (-1)^{j+1}/j!
      memcpy(T,S,p);
      for(u64 s=0;s<p;s++) if(T[s]){ u64 t=s+y; if(t>=p) t-=p; if(!S[t]){S[t]=1;cnt++;} }
    }
    printf(" %d %ld :%s\n",nfz,Jfull,buf);
  }
  return 0;
}
