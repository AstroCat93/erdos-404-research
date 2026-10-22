# Closed form for theta_3 (Gamma_3(1)=1/32, J0(3)=2 so 1+Gamma_3(j)=3^{j+1}/16 for j>=2):
# theta_3 = (4/9)[log_3(33/32) + 7/4 - 2 log_3 2], evaluated in mpmath interval arithmetic.
from mpmath import iv, mp
iv.dps = 50
t = iv.mpf(4)/9*(iv.log(iv.mpf(33)/32)/iv.log(3) + iv.mpf(7)/4 - 2*iv.log(2)/iv.log(3))
print('theta_3 in', t)
print('theta_3 > 0.2294 ?', t.a > iv.mpf('0.2294'))
