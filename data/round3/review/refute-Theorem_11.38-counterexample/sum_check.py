# Check the elementary counting step of Thm 11.38: S(k)=sum over full blocks below level k of f_p(J_m-1)
# versus theta_p*k (N0=p, so blocks m>=1, levels a_m=v((pm)!)-1).
import sys, math
sys.path.insert(0, sys.argv[1])
from gamma_theta import stats, theta
for p in [2,3,5,7,13]:
    e,G,dist,J0 = stats(p, 8 if p<11 else 7)
    th,_ = theta(p,G,dist,J0,8)
    th=float(th)
    def f(j):
        jj=j+1
        g = (1+G[jj]) if jj in G else 1.5*p**jj/2**p
        return math.log(float(g), p)
    S=0.0; m=1; a=0; worst=-1e9; rows=[]
    K=10**6 if p>2 else 10**6
    while a < K:
        J = 1
        mm=m+1
        while mm%p==0: mm//=p; J+=1
        S += f(J-1); a += J; m += 1
        if a>=2:
            d=(S-th*a)/math.log(a,p)**2
            worst=max(worst,d)
        if a in (10,100,1000,10**4,10**5) or (a>=10**5 and a%250000<J): rows.append((a, round(S-th*a,4)))
    print(p, 'theta',th, 'max (S-theta k)/log_p^2 k =', round(worst,4), rows[:8])
