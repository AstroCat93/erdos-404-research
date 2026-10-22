import sys, random, collections
sys.path.insert(0, sys.argv[1])
import zcheck
for p in (2,3,5):
    c = collections.Counter(lam for (_,_,lam) in zcheck.find_simple_zeros(p, 120, random.Random(1), tries=2000, m0=8))
    print('slope distribution p=%d'%p, dict(c))
for (p,w,K,nwin,N) in [(2,1,6,3,260),(2,5,6,2,260),(3,1,5,3,200),(3,4,4,2,220),(5,2,4,2,160)]:
    for seed in (5,6):
        print(p,w,K,'seed',seed,zcheck.run(p,w,K,nwin,N,seed,12),flush=True)
