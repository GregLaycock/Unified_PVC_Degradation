# Differential equations describing the temperature behaviour
# of the system

def dTdt(T, mu0, E, UA, k9, deg_poly, k10, x_link, q, k11):
    from visc_torque_eq import mu
    R = 8.314
    m = 0.5
    Cp = 900.
    T_inf = 200.
    return (UA/(m*Cp))*(T_inf - T) + k11*mu(mu0, E, R, T, k9, deg_poly, k10, x_link, q)

def dTmdt(T, Tm, k2):
    return k2*(T - Tm)



	

