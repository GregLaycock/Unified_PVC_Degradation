# stoichiometric matrix
from datahandling import DataFile, alldatafiles, cuts, trim
from numpy import mean,std
from Adjust_Kinetics import *
import Adjust_Kinetics
from PVC_deg_kinetics import *




# Function accepting parameters to give the modelled curves

def model_curves(p, time,LDH_0):                                   # remove LDH_0 as a dynamic parameter
    from numpy import linspace, array, append, squeeze, zeros
    from scipy.integrate import odeint
    from model_parameters import unpack_parameters

    plot_vals = {}
    C,components = add_component(Adjust_Kinetics.components)
    C['LDH'] = LDH_0
    components.append('LDH')
    #unpack parameter values from parameter structure
    para = unpack_parameters(p)
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, UA, mu_0, E, q, prim_stab_0 = para

    n = 5

    # Reactions( can be edited and rest will take care of itself. just remember to adjust paramters, limits and initials in Adjust_parameters.py!!!)

    kinetic_params = k3,k4,k5,k6,k7,k8,k12,k13,n
    reactions = rxns(kinetic_params)
   
    # temperature curve parameters
    R = 8.314
    
    # initial temperatures
    T_0 = 125.
    Tm_0 = 200.

    from Physics import mu, torque, dTdt,dTmdt


# define ode function
    import numpy
    names = []
    initials = numpy.zeros(len(C))
    for i,name in enumerate(C):
        names.append(name)
        initials[i] = C[name]
    initials = list(initials)
    initials.append(T_0)
    initials.append(Tm_0)

    def odesys(var,time):
        C = {}
        for i,name in enumerate(names):
            C[name] = var[i]
        Nc = len(names)
        T = var[Nc]
        Tm = var[Nc+1]
        del_T = dTdt(T, mu_0, E, UA, k9, k10, k14, k15, k11, C)
        del_Tm = dTmdt(T,Tm,k2)
        delta = mol_bal(components, reactions, C)
        del_comps = numpy.zeros(len(names))

        for i, name in enumerate(names):
            del_comps[i] = delta[name]

        to_return = list(del_comps)
        to_return.append(del_T)
        to_return.append(del_Tm)
        return to_return
#   integrate differential equations
    solved = odeint(odesys, initials, time)
    sol2 = solved.T
    C_vals = {}
    for i,name in enumerate(names):
        C_vals[name] = sol2[i]
    T_index = len(sol2) - 2
    plot_vals.update(C_vals)
    plot_vals['T'] = sol2[T_index]
    plot_vals['Tm'] = sol2[T_index + 1]
    import Physics
    plot_vals['mu'] = Physics.mu_plot(mu_0, E, R, plot_vals['T'], k9, k10, k14, k15, C_vals,q)
    plot_vals['Torq'] = Physics.Torq_plot(plot_vals['mu'],k1)
    return plot_vals


# defining optimization and plotting functions

def torque_curve(p, time):
    curves = model_curves(p, time)
    return curves['Torq']
	
def temp_curve(p, time):
    curves = model_curves(p, time)
    return curves['T']

#def fcn2min_torque(p, time, data):
#    model = torque_curve(p, time)
#    return model - data
	
#def fcn2min_temp(p, time, data):
#    model = temp_curve(p, time)
#    return model - data

#def fcn2min(p, time, data):             #obsolete
#    curves = model_curves(p, time)
#    torc = curves['Torq']
#    tempc = curves['T']
#    model = joined_curves(torc,tempc)
#    return model - data


def num_range_equal(list, m, s):
    nre_list = []
    for i in list:
        nre_val = (i - m)/s
        nre_list.append(nre_val)

    return nre_list

def norm_and_join(torque, temp):

    from numpy import append
    t_list = list(torque)
    T_list = list(temp)

    meantorgue = mean(t_list)
    meantemp = mean(T_list)
    std_torgue = std(t_list)
    std_temp = std(T_list)

    t_norm = num_range_equal(t_list, meantorgue, std_torgue)
    T_norm = num_range_equal(T_list, meantemp, std_temp)
    
    return append(t_norm, T_norm)

def num_range_equal(list, m, s):
    nre_list = []
    for i in list:
        nre_val = (i - m)/s
        nre_list.append(nre_val)

    return nre_list

def LDH_zeros():
    LDH_inits = []
    from datahandling import file_parse
    files = alldatafiles()
    for i,f in enumerate(files):
        LDH_0, LDH_type = file_parse(f)
        LDH_inits.append(LDH_0)
    return LDH_inits

def joined_sim(p,LDH_inits,time_sets):                          # p = parameters with ldh_0 removed which should still be done.
    from numpy import append
    joined = []
    for i,ldh_0 in enumerate(LDH_inits):        # 1 initial ldh per data file
        time = time_sets[i]
        sim_res = model_curves(p,time,ldh_0)
        torc = sim_res['Torq']
        tempc = sim_res['T']
        joined_i = norm_and_join(torc,tempc)
        return append(joined,joined_i)

def joined_data():
    from numpy import append
    files = alldatafiles()
    joined = []
    for i, f in enumerate(files):
        time_data, temp_data, torque_data = DataFile(f).simple_data()

        # Trimming data
        c = cuts(torque_data)
        temp_data = trim(temp_data, c)
        torque_data = trim(torque_data, c)
        #Joining data
        joined_i = norm_and_join(torque_data, temp_data)
        return append(joined, joined_i)


def fcn3min(p,time_sets,LDH_inits,Joined_data):
    model = joined_sim(p,LDH_inits,time_sets)
    data = Joined_data
    return model - data

def get_timesets(files):
    time_sets = []
    for i, f in enumerate(files):
        time_data, temp_data, torque_data = DataFile(f).simple_data()

        # Trimming data
        c = cuts(torque_data)
        time_data = trim(time_data, c)
        #Joining data
        time_sets.append(time_data)
    return time_sets