# Viscosity and torque equations

def mu(mu0, E, R, T, k9, deg_poly, k10, x_link, q):
    from math import exp
    return mu0*exp(E/(R*T)) + k9*deg_poly + (k10*x_link)**q

def torque(k1, mu):
    return k1*mu