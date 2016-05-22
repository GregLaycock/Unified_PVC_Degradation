# Viscosity and torque equations
q = 1

def mu(mu_0, E, R, T, k9,k10,k14,k15, C):
    from math import exp
    return mu_0*exp(-E/(R*T)) +k9*C['dp'] + k10*C['xl']**(q) - k14*C['half'] + k15 * C['double']

def torque(k1, mu):
    return k1*mu

def dTdt(T, mu_0, E, UA, k9, k10,k14,k15,k11,C):
    R = 8.314
    m = 0.5
    Cp = 900.
    T_inf = 200.
    return (UA/(m*Cp))*(T_inf - T) + k11*mu(mu_0, E, R, T, k9,k10,k14,k15, C)

def dTmdt(T, Tm, k2):
    return k2*(T - Tm)

def mu_plot(mu_0, E, R, T_vals, k9,k10,k14,k15, C_vals):
    from math import exp
    mu_vals = []
    for i,T in enumerate(T_vals):
        mu_val = mu_0*exp(-E/(R*T)) +k9*C_vals['dp'][i] + k10*C_vals['xl'][i]**(q) - k14*C_vals['half'][i] + k15 * C_vals['double'][i]
        mu_vals.append(mu_val)
    return mu_vals

def Torq_plot(mu_vals,k1):
    from numpy import array
    mu_arr = array(mu_vals)
    Torq_vals = k1*mu_arr
    return Torq_vals