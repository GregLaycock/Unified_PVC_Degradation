# This set of parameters works the best so far
def parameters(ini_values):
    from lmfit import Parameters
    from Adjust_Kinetics import params
    p = Parameters()
    p.add_many(params(ini_values))
    return p
	
def unpack_parameters(p):
    #unpack parameter values from parameter structure
    lis = []
    for i in p:
        lis.append(p[i].value)
    return lis

def parameter_vectors(all_ps):
    from numpy import append
    all = []
    for i, lis in enumerate(all_ps[0]):
        all.append([])

    
    for j in range(len(all_ps)):
        para = unpack_parameters(all_ps[j])
        for i,val in enumerate(para):
            all[i].append(val)

    return all

def ms_var_func(val, factor):
    from random import random
    return val + random()*val*factor - val*factor/2.0

def rand_ini_val(LDH_0):
    from numpy import append
    from random import random
    from Adjust_Kinetics import limits

    lims = limits()
    
    ini_val = []
    for l in range(len(lims)):
        lb = limits[l][0]
        ub = limits[l][1]
        new_val = lb + random()*(ub - lb)
        ini_val.append(new_val)
    
    return append(ini_val, [0.0372, 6208.6, 2.5, 1.3, LDH_0])    