from __future__ import division
from PVC_deg_kinetics import add_component,rate,mol_bal
from math import exp
from numpy import array,linspace,zeros
from scipy.integrate import odeint
from matplotlib import pyplot as plot

# initializing some variables


time = linspace(0, 30, 1000)
# consts
To = 125
Tmo = 200
Tinf = 200
mu_0 = 0.03
UA = 0.300
Cp = 0.900
R = 8.314
m = 0.5
E = -6208.6
q = 10
n = 5
T = To
Tm = Tmo

# original model

k1 = 2
k2 = 30
k3 = 5
k4 = 1.5
k5 = 0.02
k6 = 20
k7 = 2.0
k8 = 5.0
k9 = 5
k10 = 5.0
k11 = 2.5

# adding termination reactions

k12 = 100     # half chain
k13 = 10    # double chain
k14 = 10000        # half effect on mu
k15 = 100          # double effect on mu

C,components = add_component({'HCL': 0,
                              'LDH': 1.3,
                              'pas': 5,
                              'rad': 0,
                              'ps': 1.3,
                              'dp': 0,
                              'xl': 0,
                              'double': 0,
                              'half': 0,
                              'none': 1})

# reactions in [({stoic},order,intrinsic_rate_const)]

reactions=[({'HCL': -n, 'LDH': -1}, 1, k3),
           ({'HCL': 1, 'pas': -1, 'rad': 1,'auto': 'HCL'}, 1, k4),
           ({'pas': -1, 'HCL': 1, 'rad': 1}, 1, k5),
           ({'rad': -1, 'ps': -1}, 1, k6),
           ({'rad': -1, 'dp': 1}, 1, k7),
           ({'rad': -1, 'xl': 1}, 1, k8),
           ({'rad': -1, 'half': 2}, 2, k12),          # half
           ({'rad': -2, 'double': 1}, 1, k13)]           # double

plot_vals = {}
for i in components:
    plot_vals[i] = []

plot_vals['T'] = []
plot_vals['mu'] = []
plot_vals['Tm'] = []
plot_vals['Torq'] = []

# 'euler integration'

delta_t=time[1]-time[0]


for t in time:
    for i in components:
        plot_vals[i].append(C[i])
    mu = mu_0*exp(-E/(R*T)) +k9*C['dp'] + k10*C['xl']**(q) - k14*C['half'] + k15 * C['double']
    Torq = k1*mu

    plot_vals['mu'].append(mu)
    plot_vals['T'].append(T)
    plot_vals['Torq'].append(Torq)
    plot_vals['Tm'].append(Tm)

    del_T = (UA/(m*Cp))*(Tinf-T) + k11*mu
    del_Tm = k2*(T-Tm)

    delta = mol_bal(components, reactions, C)

    for i in components:
        C[i] += delta[i] * delta_t

    T += del_T*delta_t
    Tm += del_Tm*delta_t


# plotting

plot.figure(1)
plot.plot(time,plot_vals['Torq'], 'r-', label="Torque in NM")
plot.legend(loc=1)


plot.figure(2)

plot.plot(time,plot_vals['ps'], 'y-', label="[ps]")
plot.plot(time,plot_vals['rad'], 'g-', label="[radical]")
plot.plot(time,plot_vals['half'], 'b-', label="[Half_chains]")
plot.plot(time,plot_vals['double'], 'r-', label="Double_chains")
plot.legend(loc=1)

plot.show()
