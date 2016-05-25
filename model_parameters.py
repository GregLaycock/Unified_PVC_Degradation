# This set of parameters works the best so far
def parameters(ini_values):
    from lmfit import Parameters
    from Adjust_Kinetics import params
    p = Parameters()
    pi = params(ini_values)
    for i,tup in enumerate(pi):
        p.add_many(tup)
    return p
	
def unpack_parameters(p):
    #unpack parameter values from parameter structure
    return p.valuesdict().values()

def parameter_vectors(all_ps):
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

def rand_ini_val():
    from numpy import append
    from random import random
    import Adjust_Kinetics

    lims = Adjust_Kinetics.limits
    
    ini_val = []
    for l in range(len(lims)):
        lb = lims[l][0]
        ub = lims[l][1]
        new_val = lb + random()*(ub - lb)
        ini_val.append(new_val)
    
    return append(ini_val, [0.0372, 6208.6, 2.5, 1.3])