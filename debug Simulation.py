from Simulation import *
from datahandling import alldatafiles




files = alldatafiles()
no_files = len(files)

#setting up
time_sets = get_timesets(files)

LDH_0 = 3
k1 = 2
k2 = 1.7
k3 = 4
k4 = 1.5
k5 = 0.01
k6 = 20
k7 = 1.5
k8 = 5
k9 = 0
k10 = 0.2
k11 = 2.5
k12 = 0
k13 = 0
k14 = 0
k15 = 0
UA = 300
LDH_0 = 0.3
mu_0 = 0.0372
E = 6208.6
q = 2.5
prim_stab_0 = 1.3
p = k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, UA, mu_0, E, q, prim_stab_0
time = time_sets[0]

res = model_curves(p,time,LDH_0)


print 'res_T',res['T']
print 'mu_0',mu_0
print 'E',E

from numpy import exp
R = 8.314
res_mu = mu_0 *exp(E/(R*res['T']))
res_Torq = k1*res_mu
print res_mu

res['mu'] = res_mu

from matplotlib.pyplot import *
plot(time,res_Torq)
show()