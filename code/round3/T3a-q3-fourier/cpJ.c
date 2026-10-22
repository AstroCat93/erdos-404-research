/* cpJ.c -- block constants (see cpJ.py docstring): c_p(J), Gam_p(J), A_p.  Usage: cpJ p Jmax */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int argc,char**argv){
  int p=atoi(argv[1]), Jmax=atoi(argv[2]);
  long long e[64]; long long f=1; for(int u=1;u<p;u++) f*=u; /* (p-1)! */
  long long uf=1; for(int u=0;u<p;u++){ if(u) uf*=u; e[u]=(u%2?-1:1)*(f/uf); }
  /* A_p and c_p(1) with pattern r! mod p */
  double A=0,c1=0; for(int xi=1;xi<p;xi++){ double pr=1; long long rf=1; for(int r=0;r<p;r++){ if(r) rf=(rf*r)%p; pr*=fabs(cos(M_PI*xi*(double)rf/p)); } A+=pr; if(pr>c1)c1=pr; }
  printf("p=%d  A_p=%.10f  c_p(1)[r!]=%.10e\n",p,A,c1);
  for(int J=1;J<=Jmax;J++){
    long long m=1; for(int i=0;i<J;i++) m*=p;
    long long em[64]; for(int u=0;u<p;u++){ em[u]=e[u]%m; if(em[u]<0) em[u]+=m; }
    double best=0, gam=0; long long arg=0;
    for(long long xi=1;xi<m;xi++){ double pr=1; for(int u=0;u<p;u++){ pr*=fabs(cos(M_PI*(double)((xi*em[u])%m)/m)); if(pr<1e-300) break; } if(pr>best){best=pr;arg=xi;} gam+=pr*pr; }
    printf("p=%d J=%d  c_p(J)=%.10e  at xi=%lld  Gam_p(J)=%.6e  (p^J-1)c^2=%.6e  rm:p^J(1-1/p)2^-p=%.4e\n",p,J,best,arg,gam,(double)(m-1)*best*best,(double)m*(1-1.0/p)/pow(2,p));
    fflush(stdout);
  }
  return 0;
}
