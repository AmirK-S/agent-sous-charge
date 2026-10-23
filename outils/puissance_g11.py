"""G11 : puissance du critère de qualité (section 5 du pré-enregistrement). uv run --with numpy --with scipy python outils/puissance_g11.py"""
import numpy as np
from scipy import optimize, stats
rng=np.random.default_rng(0)
# Hétérogénéité entre tâches : loi Beta calée sur pass^1 et pass^4 publiés (GPT-5.2 high BM25 : 24.48 / 10.31)
def fit(p1,p4):
    def f(lg):
        a,b=np.exp(lg)
        m=a/(a+b); m4=np.prod([(a+k)/(a+b+k) for k in range(4)])
        return [m-p1,m4-p4]
    return np.exp(optimize.fsolve(f,[0,1]))
ab=fit(.2448,.1031); conc=ab.sum()
print('beta fit',ab,'concentration',conc)
T=57
def power(mean,delta,R,nsim=4000,margin=.05,alpha=.025,hetero=True):
    z=stats.norm.ppf(1-alpha); rej=0
    for _ in range(nsim):
        if hetero:
            p=rng.beta(mean*conc,(1-mean)*conc,T)
        else: p=np.full(T,mean)
        # charge : baisse delta absolue, répartie proportionnellement à p (bornée)
        pl=np.clip(p*(1+delta/mean),0,1)
        xr=rng.binomial(R,p); xl=rng.binomial(R,pl)
        d=(xl-xr)/R
        # variance de la moyenne finie : variance intra-tâche estimée
        vr=xr/R*(1-xr/R)/(R-1)*R/R if R>1 else 0
        var_i=( (xr/R)*(1-xr/R) + (xl/R)*(1-xl/R) )/(R-1)
        se=np.sqrt(var_i.sum())/T
        lb=d.mean()-z*se
        rej+= lb>-margin
    return rej/nsim
for mean in [.05,.10,.15,.20,.25]:
    print(f'repos {mean:.0%}: ', ' '.join(f'R={R}: Δ0={power(mean,0,R):.2f} Δ-2={power(mean,-.02,R):.2f}' for R in [3,6,12,24]))
print('homogène 15%, R=3:',power(.15,0,3,hetero=False))
# taille requise (approx normale, homogène vs hétérogène) pour 80% à Δ=0
for mean in [.10,.15,.25]:
    a,b=mean*conc,(1-mean)*conc
    Epq=mean-(a*(a+1))/((a+b)*(a+b+1))  # E[p(1-p)]
    for name,v in [('homogène',mean*(1-mean)),('hétérogène',Epq)]:
        var=2*v
        n=var*((stats.norm.ppf(.975)+stats.norm.ppf(.8))/.05)**2
        print(f'{mean:.0%} {name}: conversations appariées requises ≈ {n:.0f} soit {n/T:.1f} par tâche')
print('--- erreur de 1re espèce (vrai Δ = -5 pts, doit être <= 0.025)')
for mean in [.10,.15,.25]:
    print(mean, {R:power(mean,-.05,R) for R in [3,12]})
print('--- repos 4.5 %, la charge fait tomber à 0 % (Δ = -4.5) :', power(.045,-.045,3))
