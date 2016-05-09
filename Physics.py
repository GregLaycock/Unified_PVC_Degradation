# Viscosity and torque equations

def mu(mu_0, E, R, T, k9,k10,k14,k15, C):
    from math import exp
    return mu_0*exp(-E/(R*T)) +k9*C['dp'] + k10*C['xl']**(q) - k14*C['half'] + k15 * C['double']

def torque(k1, mu):
    return k1*mu

def dTdt(T, mu_0, E, UA, k9, k10,k14,k15,k11,C):
    from visc_torque_eq import mu
    R = 8.314
    m = 0.5
    Cp = 900.
    T_inf = 200.
    return (UA/(m*Cp))*(T_inf - T) + k11*mu(mu_0, E, R, T, k9,k10,k14,k15, C)

def dTmdt(T, Tm, k2):
    return k2*(T - Tm)