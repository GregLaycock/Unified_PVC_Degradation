# This set of parameters works the best so far
def parameters(ini_values):
    from lmfit import Parameters
	
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, UA, mu_0, E, q, prim_stab_0, LDH_0 = ini_values
	
    p = Parameters()
    #          (         Name,       Value,  Vary,    Min,     Max)    
    p.add_many((         'k1',          k1,  True,    1.6,     2.1),
               (         'k2',          k2,  True,    8.0,    46.0),
               (         'k3',          k3,  True,    0.0,     6.0),
               (         'k4',          k4,  True,    0.0,     2.1),
               (         'k5',          k5,  True,    0.0,    0.03),
               (         'k6',          k6,  True,    0.0,    39.0),
               (         'k7',          k7,  True,    0.0,     2.7),
               (         'k8',          k8,  True,    0.0,     7.9),
               (         'k9',          k9,  True,    0.0,    13.1),
               (        'k10',         k10,  True,    0.7,    10.9),
               (        'k11',         k11,  True,    2.0,     3.6),
               (         'UA',          UA,  True,  275.0,   402.0),
               (       'mu_0',        mu_0, False,    0.0,     0.1),
               (          'E',           E, False, 5000.0,    None),
               (          'q',           q, False,    0.0,    17.0),
               ('prim_stab_0', prim_stab_0, False,    0.5,     1.3),
               (      'LDH_0',       LDH_0, False,   None,    None))
    return p
	
def unpack_parameters(p):
    #unpack parameter values from parameter structure
    k1 = p['k1'].value
    k2 = p['k2'].value
    k3 = p['k3'].value
    k4 = p['k4'].value
    k5 = p['k5'].value
    k6 = p['k6'].value
    k7 = p['k7'].value
    k8 = p['k8'].value
    k9 = p['k9'].value
    k10 = p['k10'].value
    k11 = p['k11'].value
    UA = p['UA'].value
    mu_0 = p['mu_0'].value
    E = p['E'].value
    q = p['q'].value
    prim_stab_0 = p['prim_stab_0'].value
    LDH_0 = p['LDH_0'].value
    return k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, UA, mu_0, E, q, prim_stab_0, LDH_0

def parameter_vectors(all_ps):
    from numpy import append
    k1_all = []
    k2_all = []
    k3_all = []
    k4_all = []
    k5_all = []
    k6_all = []
    k7_all = []
    k8_all = []
    k9_all = []
    k10_all = []
    k11_all = []
    UA_all = []
    mu_0_all = []
    E_all = []
    q_all = []
    prim_stab_0_all = []
    LDH_0_all = []
    
    for j in range(len(all_ps)):
        para = unpack_parameters(all_ps[j])
        k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, UA, mu_0, E, q, prim_stab_0, LDH_0 = para
    
        k1_all = append(k1_all, k1)
        k2_all = append(k2_all, k2)
        k3_all = append(k3_all, k3)
        k4_all = append(k4_all, k4)
        k5_all = append(k5_all, k5)
        k6_all = append(k6_all, k6)
        k7_all = append(k7_all, k7)
        k8_all = append(k8_all, k8)
        k9_all = append(k9_all, k9)
        k10_all = append(k10_all, k10)
        k11_all = append(k11_all, k11)
        UA_all = append(UA_all, UA)
        mu_0_all = append(mu_0_all, mu_0)
        E_all = append(E_all, E)
        q_all = append(q_all, q)
        prim_stab_0_all = append(prim_stab_0_all, prim_stab_0)
        LDH_0_all = append(LDH_0_all, LDH_0)

    return k1_all, k2_all, k3_all, k4_all, k5_all, k6_all, k7_all, k8_all, k9_all, k10_all, k11_all, UA_all, mu_0_all, E_all, q_all, prim_stab_0_all, LDH_0_all

def ms_var_func(val, factor):
    from random import random
    return val + random()*val*factor - val*factor/2.0

def rand_ini_val(LDH_0):
    from numpy import append
    from random import random
    limits = [[1.6, 2.1],
              [8.0, 46.0],
              [0.0, 6.0],
              [0.0, 2.1],
              [0.0, 0.03],
              [0.0, 39.0], 
              [0.0, 2.7],
              [0.0, 7.9],
              [0.0, 13.1],
              [0.7, 10.9],
              [2.0, 3.6],
              [275.0, 402.0]]
    
    ini_val = []
    for l in range(len(limits)):
        lb = limits[l][0]
        ub = limits[l][1]
        new_val = lb + random()*(ub - lb)
        ini_val.append(new_val)
    
    return append(ini_val, [0.0372, 6208.6, 2.5, 1.3, LDH_0])    