/* winvar.c -- odd-p quenched martingale: exact one-window second moments along trajectories (mode 1)
 *             and atom Monte Carlo of E[M_l], E[M_l^2] (mode 2).   Track T1a, round 3 (2026-10-20).
 *
 * Paths e (e_0=1) are stored as (S_e(x) mod p^P, S_e'(x) mod p^P) with additive updates only.
 * Alive at n  <=>  p^{V_n} | S_e(x).   lambda_e = v_p(S_e'(x)) (capped at L+1).
 * tau_n(e) = -S_e/pi_n;  rho_n(e) = p^lambda a_n^{(lambda)}(tau_n mod p^lambda);  M_n = 2^{-n} p^{V_n} sum rho.
 * Window [n,N): atom x + p^m Z_p (m=V_n), D=V_N-m, w = digits m..m+D-1 relative to x.
 *   X_e(w) = Phi_{lambda,s}((theta_e - beta_e w) mod p^D),  theta_e=(tau-s)/p^lambda,  beta_e = omega^{-1} S_e'/p^lambda,
 *   Phi_{lambda,s}(y) = sum_z c[(s+p^lambda y) mod p^D + p^D z] * p^lambda a_N^{(lambda)}(u^{-1}(floor((s+p^lambda y)/p^D) - z)).
 * Usage: winvar mode seed p L P n0 nwin ratio nsamp [maxpop] [K]
 *   mode 1: nsamp trajectories; exact window statistics at each window (Var exact if p^D*|P| <= 2e9 else K samples of w).
 *   mode 2: one atom (x0 mod p^{m0}); nsamp samples of the higher digits; E[M_l], E[M_l^2], increments.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <complex.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
static u64 rs[2];
static u64 rng(void){u64 s1=rs[0],s0=rs[1];rs[0]=s0;s1^=s1<<23;rs[1]=s1^s0^(s1>>17)^(s0>>26);return rs[1]+s0;}
static u128 pw[130]; static int p,P,L; static u128 MOD;
static u128 mulmod128(u128 a,u128 b){ /* a,b<MOD<2^126; double-and-add */
    u128 r=0; a%=MOD; b%=MOD; while(b){ if(b&1){ r+=a; if(r>=MOD) r-=MOD; } a<<=1; if(a>=MOD) a-=MOD; b>>=1; } return r; }
static u64 mulmod64(u64 a,u64 b,u64 m){ return (u64)(((u128)a*b)%m); }
static u64 powmod64(u64 a,u64 e,u64 m){ u64 r=1%m; a%=m; while(e){ if(e&1) r=mulmod64(r,a,m); a=mulmod64(a,a,m); e>>=1;} return r; }
static u64 inv64(u64 u,u64 m){ u64 phi=m-m/p; return powmod64(u%m,phi-1,m); } /* m = p^k */
static int vp128(u128 a,int cap){ if(a==0) return cap; int k=0; while(a%p==0){ a/=p; k++; if(k>=cap) return cap; } return k; }
typedef struct { u128 S, Sp; } path_t;

/* a_n^{(lam)}(t): distribution of sum_{i<p lam} f_i prod_{k=1}^{i}(x+n+k) mod p^lam ; out[t] */
static void adist(u128 x,int n,int lam,double *out){
    u64 md=(u64)pw[lam]; int K=p*lam; double *c=calloc(md,sizeof(double)),*nw=calloc(md,sizeof(double)); c[0]=1; u64 prod=1;
    for(int i=0;i<K;i++){ u64 term=prod%md; memset(nw,0,md*sizeof(double));
        for(u64 r=0;r<md;r++){ if(c[r]==0) continue; nw[r]+=c[r]; nw[(r+term)%md]+=c[r]; }
        memcpy(c,nw,md*sizeof(double)); prod=mulmod64(prod,(u64)((x+n+i+1)%md),md); }
    double tot=ldexp(1.0,K); for(u64 t=0;t<md;t++) out[t]=c[t]/tot; free(c); free(nw);
}

int main(int argc,char**argv){
    if(argc<10){fprintf(stderr,"usage: winvar mode seed p L P n0 nwin ratio nsamp [maxpop] [K]\n");return 1;}
    int mode=atoi(argv[1]); u64 seed=strtoull(argv[2],0,10); p=atoi(argv[3]); L=atoi(argv[4]); P=atoi(argv[5]);
    int n0=atoi(argv[6]), nwin=atoi(argv[7]); double ratio=atof(argv[8]); long nsamp=atol(argv[9]);
    size_t maxpop=argc>10?(size_t)atol(argv[10]):6000000; int Ksamp=argc>11?atoi(argv[11]):256;
    rs[0]=seed*0x9E3779B97F4A7C15ULL+1; rs[1]=seed^0xD1B54A32D192ED03ULL; for(int i=0;i<20;i++) rng();
    pw[0]=1; for(int i=1;i<=P;i++) pw[i]=pw[i-1]*p; MOD=pw[P];
    if(P>125||(long double)MOD>ldexpl(1.0L,126)){fprintf(stderr,"P too large\n");return 1;}
    int wins[128]; wins[0]=n0; for(int l=1;l<=nwin;l++){ int a=(int)floor(ratio*wins[l-1]), b=wins[l-1]+p*(L+1); wins[l]=a>b?a:b; }
    int nmax=wins[nwin];
    printf("# winvar mode=%d p=%d L=%d P=%d n0=%d nwin=%d ratio=%.3f nsamp=%ld maxpop=%zu K=%d seed=%llu\n# windows:",mode,p,L,P,n0,nwin,ratio,nsamp,maxpop,Ksamp,(unsigned long long)seed);
    for(int l=0;l<=nwin;l++) printf(" %d",wins[l]); printf("\n");
    path_t *A=malloc(maxpop*sizeof(path_t)),*B=malloc(maxpop*sizeof(path_t)); if(!A||!B){fprintf(stderr,"alloc\n");return 2;}
    /* mode 2 accumulators */
    double sM[128]={0},sM2[128]={0},sInc2[128]={0},sPop[128]={0}; long zeroM[128]={0},hypfail[128]={0},hypfail2[128]={0},done=0,overflow=0;
    u128 x0=0; int m0=0; u128 xfix=0;
    if(mode==2){ for(;;){ x0=((u128)rng()<<64|rng())%MOD; if(x0%p==(u64)(p-1)) continue; int V=0,Mn=0; for(int i=1;i<=n0;i++){int d=vp128((x0+i)%MOD,P); V+=d; if(d>Mn)Mn=d;} m0=V; if(m0+L+6<P && Mn<m0) break; }
        xfix=x0%pw[m0]; printf("# atom: x0 mod p^%d = %llu (low 64 bits)\n",m0,(unsigned long long)xfix); }
    for(long s=0;s<nsamp;s++){
        u128 x;
        if(mode==2) x=(xfix+(((u128)rng()<<64|rng())%(MOD/pw[m0]))*pw[m0])%MOD;
        else { do { x=((u128)rng()<<64|rng())%MOD; } while(x%p==(u64)(p-1)); }
        if(mode==1){ char buf[64]; int k=63; buf[k]=0; u128 t=x; if(t==0) buf[--k]='0'; while(t){ buf[--k]='0'+(int)(t%10); t/=10; } printf("X sample=%ld x=%s\n",s,buf+k); }
        size_t np=1; A[0].S=0; A[0].Sp=0; /* empty path; step j=0 forces e_0=1 and adds pi_0=1 */
        u128 pi=1,dpi=0; /* pi_j, pi_j' mod p^P (j current) */
        int V=0,Mn=0,wi=0,ok=1; double Mprev=0; int Mwin[128],Vwin[128],LMwin[128];
        for(int j=0;j<=nmax;j++){
            if(j==wins[wi]){
                int n=j,m=V;
                if(P-m<=L+2){ ok=0; break; }
                /* ---- window statistics ---- */
                int N=(wi<nwin)?wins[wi+1]:-1; int H=N-n;
                /* valuations ahead: D, M_N */
                int D=0,MN=Mn; if(N>0){ for(int i=n+1;i<=N;i++){ int d=vp128((x+i)%MOD,P); D+=d; if(d>MN) MN=d; } }
                int lamcap=L; if(N>0 && (D+L>P-m)){ ok=0; break; }
                if((long double)pw[D+L]>ldexpl(1.0L,62)){ fprintf(stderr,"p^(D+L) too large\n"); ok=0; break; }
                u64 mdDL=(u64)pw[D+L];
                int bigwin=(mdDL>40000000ULL);
                u64 omega=(u64)((pi/pw[m])%mdDL); u64 ominv=inv64(omega,mdDL);
                /* a_n^{(lam)} tables */
                double *an[16]; for(int lam=1;lam<=L;lam++){ an[lam]=malloc(sizeof(double)*(u64)pw[lam]); adist(x,n,lam,an[lam]); }
                /* parents: lam, s, theta, beta, rho */
                double sumrho=0; size_t cntL=0;
                int *lamv=malloc(np*sizeof(int)); u64 *thv=malloc(np*sizeof(u64)),*bev=malloc(np*sizeof(u64)),*sv=malloc(np*sizeof(u64)); double *rhov=malloc(np*sizeof(double));
                for(size_t i=0;i<np;i++){
                    int lam=vp128(A[i].Sp,L+1); lamv[i]=lam; if(lam>L){ rhov[i]=0; continue; } cntL++;
                    u64 md=(u64)pw[D+lam]; u64 Sq=(u64)((A[i].S/pw[m])%md); u64 tau=(md-mulmod64(Sq,ominv%md,md))%md;
                    u64 sres=tau%(u64)pw[lam]; sv[i]=sres; thv[i]=((tau-sres)/(u64)pw[lam])%(u64)pw[D];
                    u64 Spq=(u64)((A[i].Sp/pw[lam])%(u64)pw[D]); bev[i]=mulmod64(Spq,ominv%(u64)pw[D],(u64)pw[D]);
                    double rho=(lam==0)?1.0:(double)pw[lam]*an[lam][sres]; rhov[i]=rho; sumrho+=rho;
                }
                int lammax=0; for(size_t i=0;i<np;i++) if(lamv[i]<=L && rhov[i]>0 && lamv[i]>lammax) lammax=lamv[i];
                double norm=exp(-n*log(2.0)+m*log((double)p)); double M=norm*sumrho;
                if(mode==1){ long lh[20]={0}; for(size_t i=0;i<np;i++){ int l2=vp128(A[i].Sp,12); lh[l2]++; } printf("LAMHIST n=%d pop=%zu:",n,np); for(int l2=0;l2<=12;l2++) if(lh[l2]) printf(" %d:%ld",l2,lh[l2]); printf("\n"); }
                if(mode==2){ sM[wi]+=M; sM2[wi]+=M*M; sPop[wi]+=(double)np; if(M==0) zeroM[wi]++; if(wi>0) sInc2[wi]+=(M-Mprev)*(M-Mprev);
                    if(wi>0){ int mm=Vwin[wi-1],DD=V-mm; if(!(DD+L<=mm-Mwin[wi-1] && L<mm-Mn && Mn<mm)) hypfail[wi]++;
                              if(!(DD+LMwin[wi-1]<=mm-Mwin[wi-1] && L<mm-Mn && Mn<mm)) hypfail2[wi]++; } }
                if(mode==1 && N>0 && np>0 && bigwin) printf("W l=%d n=%d N=%d D=%d SKIPPED (p^(D+L) too large)\n",wi,n,N,D);
                if(mode==1 && N>0 && np>0 && !bigwin){
                    int W1=(H>=p*(L+1)), W2=(D+L<=m-Mn), W3=(L<m-MN), ENV=(MN<m), W2b=(D+lammax<=m-Mn);
                    u64 pD=(u64)pw[D];
                    /* window fibre counts mod p^{D+L} */
                    double *c=calloc(mdDL,sizeof(double)),*nw=calloc(mdDL,sizeof(double)); c[0]=1; u128 yprod=1;
                    for(int jj=n;jj<N;jj++){ u64 y=(u64)(yprod%mdDL); memset(nw,0,mdDL*sizeof(double));
                        for(u64 r=0;r<mdDL;r++){ if(c[r]==0) continue; nw[r]+=c[r]; nw[(r+y)%mdDL]+=c[r]; }
                        memcpy(c,nw,mdDL*sizeof(double)); yprod=mulmod128(yprod,(x+jj+1)%MOD); }
                    free(nw);
                    /* unit u = pi_N/(p^D pi_n) mod p^L */
                    u64 uu=1, mdL=(u64)pw[L>0?L:1]; for(int i=n+1;i<=N;i++){ u128 t=(x+i)%MOD; while(t%p==0) t/=p; uu=mulmod64(uu,(u64)(t%mdL),mdL); }
                    double *aN[16]; for(int lam=1;lam<=L;lam++){ aN[lam]=malloc(sizeof(double)*(u64)pw[lam]); adist(x,N,lam,aN[lam]); }
                    /* Psi_lam tables on Z/p^{D+lam}: Phi_{lam,s}(y) = Psi_lam[s + p^lam y] */
                    double *Psi[16]; for(int lam=0;lam<=L;lam++) Psi[lam]=NULL;
                    int lamseen[16]={0}; for(size_t i=0;i<np;i++) if(lamv[i]<=L && rhov[i]>0) lamseen[lamv[i]]=1;
                    long nPhi=0;
                    for(int lam=0;lam<=L;lam++){ if(!lamseen[lam]) continue; nPhi++;
                        u64 pl=(u64)pw[lam], md=(u64)pw[D+lam]; double *cl=calloc(md,sizeof(double));
                        for(u64 r=0;r<mdDL;r++) cl[r%md]+=c[r];
                        double *F=malloc(sizeof(double)*md); u64 uinv=lam?inv64(uu%pl,pl):1;
                        for(u64 t0=0;t0<pD;t0++) for(u64 hi=0;hi<pl;hi++){ double acc=0;
                            for(u64 z=0;z<pl;z++){ double cnt=cl[t0+pD*z]; if(cnt==0) continue; u64 st=lam?mulmod64(uinv,(hi+pl-z)%pl,pl):0; acc+=cnt*(lam?(double)pl*aN[lam][st]:1.0); }
                            F[t0+pD*hi]=acc; }
                        free(cl); Psi[lam]=F; }
#define PHIV(lam,ss,y) Psi[lam][((ss)+(u64)pw[lam]*(y))%(u64)pw[D+(lam)]]
                    double ESig=0, sumVarInd=0;
                    /* per-(lam,s) mean and variance of the profile, computed once */
                    double *pmean=calloc((size_t)(L+1)*(u64)pw[L],sizeof(double)), *pvar=calloc((size_t)(L+1)*(u64)pw[L],sizeof(double)); char *pdone=calloc((size_t)(L+1)*(u64)pw[L],1);
                    for(size_t i=0;i<np;i++){ int lam=lamv[i]; if(lam>L||rhov[i]==0) continue; u64 ss=sv[i]; size_t key=(size_t)lam*(u64)pw[L]+ss;
                        if(!pdone[key]){ double mu=0,m2=0; for(u64 y=0;y<pD;y++){ double v=PHIV(lam,ss,y); mu+=v; m2+=v*v; } pmean[key]=mu/pD; pvar[key]=m2/pD-(mu/pD)*(mu/pD); pdone[key]=1; }
                        ESig+=pmean[key]; sumVarInd+=pvar[key]; }
                    free(pmean); free(pvar); free(pdone);
                    double EpredSig=ldexp(1.0,H)/(double)pD*sumrho;
                    /* Var Sigma: exact if affordable else sampled */
                    int exact=((double)pD*(double)cntL<=2.0e9); double VarSig=0, byorder[64]={0}; long Kused=0;
                    if(exact){ double *Sig=calloc(pD,sizeof(double));
                        for(size_t i=0;i<np;i++){ if(lamv[i]>L||rhov[i]==0) continue; int lam=lamv[i]; u64 ss=sv[i]; u64 th=thv[i],be=bev[i];
                            for(u64 w=0;w<pD;w++){ u64 y=(th+pD-mulmod64(be,w,pD))%pD; Sig[w]+=PHIV(lam,ss,y); } }
                        double mu=0,m2=0; for(u64 w=0;w<pD;w++){ mu+=Sig[w]; m2+=Sig[w]*Sig[w]; } mu/=pD; m2/=pD; VarSig=m2-mu*mu;
                        if(fabs(mu-ESig)>1e-6*fabs(ESig)+1e-9) printf("## WARNING first-moment mismatch %.9g vs %.9g\n",mu,ESig);
                        /* by order: Var(E[Sig|w mod p^d]) differences */
                        double prevv=0; for(int d=1;d<=D;d++){ u64 pd=(u64)pw[d]; double *cm=calloc(pd,sizeof(double)); for(u64 w=0;w<pD;w++) cm[w%pd]+=Sig[w]; double vv=0; for(u64 r=0;r<pd;r++){ double v=cm[r]/(pD/pd); vv+=v*v; } vv=vv/pd-mu*mu; byorder[d]=vv-prevv; prevv=vv; free(cm); }
                        free(Sig); }
                    else { double mu=0,m2=0; for(int k=0;k<Ksamp;k++){ u64 w=rng()%pD; double S=0;
                            for(size_t i=0;i<np;i++){ if(lamv[i]>L||rhov[i]==0) continue; u64 y=(thv[i]+pD-mulmod64(bev[i],w,pD))%pD; S+=PHIV(lamv[i],sv[i],y); }
                            mu+=S; m2+=S*S; } mu/=Ksamp; m2/=Ksamp; VarSig=(m2-mu*mu)*Ksamp/(Ksamp-1.0); Kused=Ksamp; }
                    /* Weyl sums of rho-weighted Newton roots y* = theta/beta at orders d<=3 */
                    double weyl[4]={0,0,0,0}; for(int d=1;d<=D&&d<=3;d++){ u64 pd=(u64)pw[d]; double *hist=calloc(pd,sizeof(double));
                        for(size_t i=0;i<np;i++){ if(lamv[i]>L||rhov[i]==0) continue; u64 bi=inv64(bev[i]%pd,pd); hist[mulmod64(thv[i]%pd,bi,pd)]+=rhov[i]; }
                        double best=0; for(u64 xi=1;xi<pd;xi++){ if(xi%p==0) continue; double re=0,im=0; for(u64 r=0;r<pd;r++){ double ang=2*M_PI*(double)(xi*r%pd)/pd; re+=hist[r]*cos(ang); im+=hist[r]*sin(ang);} double a=hypot(re,im); if(a>best) best=a; }
                        weyl[d]=best/sumrho; free(hist); }
                    double relvar=VarSig/(ESig*ESig);
                    printf("W l=%d n=%d N=%d H=%d m=%d D=%d Mn=%d MN=%d hyp=%d%d%d%d W2b=%d lammax=%d pop=%zu popL=%zu nPhi=%ld M=%.6g EM_N=%.6g ESig=%.6g ESigPred=%.6g VarSig=%.6g VarInd=%.6g corr=%.4g relvar=%.4g exact=%d K=%ld weyl=%.3f/%.3f/%.3f byorder=",
                        wi,n,N,H,m,D,Mn,MN,W1,W2,W3,ENV,W2b,lammax,np,cntL,nPhi,M,norm*ldexp(1.0,-H)*pow((double)p,D)*ESig,ESig,EpredSig,VarSig,sumVarInd,sumVarInd>0?VarSig/sumVarInd:0.0,relvar,exact,Kused,weyl[1],weyl[2],weyl[3]);
                    if(exact) for(int d=1;d<=D;d++) printf("%.4g%s",byorder[d],d<D?",":""); else printf("na");
                    printf(" incr2=%.4g\n",M*M*relvar);
                    for(int lam=0;lam<=L;lam++) if(Psi[lam]) free(Psi[lam]);
                    for(int lam=1;lam<=L;lam++) free(aN[lam]); free(c);
                }
                if(mode==1 && N<0) printf("W l=%d n=%d END m=%d Mn=%d pop=%zu popL=%zu M=%.6g\n",wi,n,m,Mn,np,cntL,M);
                free(lamv);free(thv);free(bev);free(sv);free(rhov); for(int lam=1;lam<=L;lam++) free(an[lam]);
                Mprev=M; Mwin[wi]=Mn; Vwin[wi]=V; LMwin[wi]=lammax; wi++; if(wi>nwin) break;
            }
            /* step j -> j+1: paths e|_{j+1} = (e|_j, e_j); S += e_j pi_j; S' += e_j pi_j'; kill if not alive at j+1 */
            u128 xj=(x+j+1)%MOD; int d=vp128(xj,P); if(d>Mn) Mn=d; int Vnew=V+d; if(Vnew+L+2>=P){ ok=0; break; }
            size_t nb=0; u128 mk=pw[Vnew];
            for(size_t i=0;i<np;i++){
                for(int e=(j==0?1:0);e<=1;e++){
                    u128 S=A[i].S, Sp=A[i].Sp; if(e){ S+=pi; if(S>=MOD) S-=MOD; Sp+=dpi; if(Sp>=MOD) Sp-=MOD; }
                    if(d && (S%mk)!=0) continue;
                    if(nb>=maxpop){ ok=0; break; } B[nb].S=S; B[nb].Sp=Sp; nb++; }
                if(!ok) break; }
            if(!ok){ overflow++; break; }
            dpi=(mulmod128(dpi,xj)+pi)%MOD; pi=mulmod128(pi,xj); path_t*T=A;A=B;B=T; np=nb; V=Vnew;
        }
        if(!ok){ if(mode==1) printf("W ABORT (overflow or precision) sample %ld\n",s); if(++overflow>50+nsamp/10){ fprintf(stderr,"too many aborts\n"); break; } if(mode==2) continue; }
        done++;
    }
    if(mode==2){ printf("# samples=%ld aborts=%ld\n#  l    n   E|P|     E[M]      E[M^2]    Var[M]   E[(M_l-M_{l-1})^2]  P(M=0) hypfail hypfail(lam_max)\n",done,overflow);
        for(int l=0;l<=nwin;l++){ double EM=sM[l]/done,EM2=sM2[l]/done; printf("%3d %4d %9.1f %9.5f %10.5f %9.5f %12.5e %7.4f %7.4f %7.4f\n",l,wins[l],sPop[l]/done,EM,EM2,EM2-EM*EM,sInc2[l]/done,(double)zeroM[l]/done,(double)hypfail[l]/done,(double)hypfail2[l]/done); } }
    free(A);free(B); return 0;
}
