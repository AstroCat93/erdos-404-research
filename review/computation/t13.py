import subprocess
from cov import cover
M=5**8; notfull=[]
for c in range(0,5**6):
    N=25*c if c else 5**8
    xs=[1];pr=1
    for j in range(1,35):
        pr=pr*(N+j)%M; xs.append(pr)
    if cover(M,xs): notfull.append(N)
print("N=0 mod 25 classes mod 5^8 with A_N NOT full mod 5^8:",len(notfull),notfull[:5])
print("5^11 > 2^25:",5**11>2**25)
