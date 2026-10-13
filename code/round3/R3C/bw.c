#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+1e-9*t.tv_nsec;}
int main(int argc,char**argv){
  size_t n = strtoull(argv[1],0,10); /* words */
  uint64_t *a=aligned_alloc(64,n*8+64),*b=aligned_alloc(64,n*8+64);
  for(size_t i=0;i<n;i++){a[i]=i*0x9e3779b97f4a7c15ULL;b[i]=0;}
  for(int rep=0;rep<5;rep++){
    double t0=now();
    size_t off=12345; unsigned o=17;
    for(size_t i=0;i+off+1<n;i++) b[i]=a[i]|(a[i+off]>>o)|(a[i+off+1]<<(64-o));
    double t1=now();
    printf("pass n=%zu words (%.1f MB): %.3f s, %.2f GB/s (3 streams)\n",n,n*8/1e6,t1-t0,3.0*n*8/1e9/(t1-t0));
    uint64_t *t=a;a=b;b=t;
  }
  return 0;
}
