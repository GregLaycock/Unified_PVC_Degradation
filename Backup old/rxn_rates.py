# Rates of chemical reactions

def r1(k3, HCl, LDH):
    return k3*HCl*LDH

def r2(k4, HCl, poly_act):
    return k4*HCl*poly_act

def r3(k5, poly_act):
    return k5*poly_act

def r4(k6, radical, prim_stab):
    return k6*radical*prim_stab

def r5(k7, radical):
    return k7*radical

def r6(k8, radical):
    return k8*radical