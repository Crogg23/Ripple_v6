from math import comb, lgamma, exp, log
import numpy as np
def binom_sf(k, n, p):  # P(X>=k)
    return sum(exp(lgamma(n+1)-lgamma(i+1)-lgamma(n-i+1)+i*log(p)+(n-i)*log(1-p)) for i in range(k, n+1))
def fisher(a,b,c,d):  # two-sided
    n=a+b+c+d; r1=a+b; c1=a+c
    def pr(x): return comb(r1,x)*comb(n-r1,c1-x)/comb(n,c1)
    p0=pr(a); lo=max(0,c1-(n-r1)); hi=min(r1,c1)
    return sum(pr(x) for x in range(lo,hi+1) if pr(x)<=p0*(1+1e-9))
def perm_mean_diff(x, y, n=20000, seed=1):
    rng=np.random.default_rng(seed); x=np.asarray(x,float); y=np.asarray(y,float)
    obs=x.mean()-y.mean(); allv=np.concatenate([x,y]); k=len(x); cnt=0
    for _ in range(n):
        rng.shuffle(allv)
        if allv[:k].mean()-allv[k:].mean()>=obs: cnt+=1
    return (cnt+1)/(n+1)
