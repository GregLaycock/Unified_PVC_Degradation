# stoichiometric matrix
from datahandling import DataFile, alldatafiles, cuts, trim
from numpy import mean,std
from Adjust_Kinetics import *
import Adjust_Kinetics
from PVC_deg_kinetics import *




# Function accepting parameters to give the modelled curves

def model_curves(p, time):
    from numpy import linspace, array, append, squeeze, zeros
    from scipy.integrate import odeint
    from model_parameters import unpack_parameters

    plot_vals = {}
    C,components = add_component(Adjust_Kinetics.components)
# DELETE IN FINAL BUILD
#    for i in components:
#        plot_vals[i] = []
#
#    plot_vals['T'] = []
#    plot_vals['mu'] = []
#    plot_vals['Tm'] = []
#    plot_vals['Torq'] = []

    #unpack parameter values from parameter structure
    para = unpack_parameters(p)
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, UA, mu_0, E, q, prim_stab_0, LDH_0 = para
    n = 5

    # Reactions( can be edited and rest will take care of itself. just remember to adjust paramters, limits and initials in Adjust_parameters.py!!!)

    kinetic_params = k3,k4,k5,k6,k7,k8,k12,k13,n
    reactions = rxns(kinetic_params)
   
    # temperature curve parameters
    R = 8.314
    	
    # initial concentrations
    HCl_0 = 0.
    poly_act_0 = 5.
    
    # initial temperatures
    T_0 = 125.
    Tm_0 = 200.
    
#    from rxn_rates import r1, r2, r3, r4, r5, r6
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
    plot_vals['mu'] = Physics.mu_plot(mu_0, E, R, plot_vals['T'], k9, k10, k14, k15, C_vals)
    plot_vals['Torq'] = Physics.Torq_plot(plot_vals['mu'],k1)

    return plot_vals

#   DELETE IN FINAL BUILD
#    T = T_0
#    Tm = Tm_0
#    delta_t = time[1]-time[0]
#    for t in time:
#        for i in components:
#            plot_vals[i].append(C[i])
#        mu = mu(mu_0, E, R, T, k9,k10,k14,k15, C)
#        Torq = k1*mu
#
#       plot_vals['mu'].append(mu)
#        plot_vals['T'].append(T)
#        plot_vals['Torq'].append(Torq)
#        plot_vals['Tm'].append(Tm)

#        del_T = dTdt(T, mu_0, E, UA, k9, k10,k14,k15,k11,C)
#        del_Tm = dTmdt(T,Tm,k2)

#        delta = mol_bal(components, reactions, C)

#        for i in components:
#            C[i] += delta[i] * delta_t
#
#        T += del_T*delta_t
#        Tm += del_Tm*delta_t


    
#    soln = plot_vals
#    return soln

# Function only returning torque curve

def torque_curve(p, time):
    curves = model_curves(p, time)
    return curves['Torq']
	
def temp_curve(p, time):
    curves = model_curves(p, time)
    return curves['T']

def fcn2min_torque(p, time, data):
    model = torque_curve(p, time)
    return model - data
	
def fcn2min_temp(p, time, data):
    model = temp_curve(p, time)
    return model - data

def fcn2min(p, time, data):
    model = joined_curves(torque_curve(p, time), temp_curve(p, time))
    return model - data
	
def joined_curves(torque, temp):
    from numpy import append
    t_list = list(torque)
    T_list = list(temp)
      
    # In[2]:
    
    files = alldatafiles()
    
    t_means = []
    T_means = []
    t_stds = []
    T_stds = []
    
    for f in files:
        time_data, temp_data, torque_data = DataFile(f).simple_data()
        
        c = cuts(torque_data)
        time_data = trim(time_data, c)
        temp_data = trim(temp_data, c)
        torque_data = trim(torque_data, c)
        
        t_means.append(mean(torque_data))
        T_means.append(mean(temp_data))
        t_stds.append(std(torque_data))
        T_stds.append(std(temp_data))    
    # In[5]:
    
    meantorgue = mean(t_means)
    meantemp = mean(T_means)
    std_torgue = mean(t_stds)
    std_temp = mean(T_stds)
    
    
    
    
    
    
    
    
	# Manually insert torque and temp mean and std respectively
    t_norm = num_range_equal(t_list, meantorgue, std_torgue)
    T_norm = num_range_equal(T_list, meantemp, std_temp)
    
    return append(t_norm, T_norm)

def num_range_equal(list, m, s):
    nre_list = []
    for i in list:
        nre_val = (i - m)/s
        nre_list.append(nre_val)

    return nre_list		