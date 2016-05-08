# stoichiometric matrix
from datahandling import DataFile, alldatafiles, cuts, trim
from numpy import mean,std

    
def stoyk():
    from numpy import array
    #reaction kinetics parameters
    n = 10.
    return array([[-n, -1., 0., 0., 0., 0., 0.],
                  [1., 0., -1., 1., 0., 0., 0.],
			   [1., 0., -1., 1., 0., 0., 0.],
		        [0., 0., 0., -1., -1., 0., 0.],
			   [0., 0., 0., -1., 0., 1., 0.],
			   [0., 0., 0., -2., 0., 0., 1.]])

# Function accepting parameters to give the modelled curves

def model_curves(p, time):
    from numpy import linspace, array, append, squeeze, zeros
    from scipy.integrate import odeint
    from model_parameters import unpack_parameters
    
    #unpack parameter values from parameter structure
    para = unpack_parameters(p)
    k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, UA, mu_0, E, q, prim_stab_0, LDH_0 = para
   
    # temperature curve parameters
    R = 8.314
    	
    # initial concentrations
    HCl_0 = 0.
    poly_act_0 = 5.
    
    # initial temperatures
    T_0 = 125.
    Tm_0 = 200.
    
    from rxn_rates import r1, r2, r3, r4, r5, r6
    from visc_torque_eq import mu, torque
    from temp_der import dTdt, dTmdt
    
    # differential equations
    def dXdt(A, time):
        HCl, LDH, poly_act, radical, prim_stab, deg_poly, x_link, T, Tm = A
        
        r = array([r1(k3, HCl, LDH), 
                   r2(k4, HCl, poly_act),
				   r3(k5, poly_act),
				   r4(k6, radical, prim_stab),
				   r5(k7, radical), 
				   r6(k8, radical)])
        return append(squeeze(stoyk().T.dot(r)),
                      [dTdt(T, mu_0, E, UA, k9, deg_poly, k10, x_link, q, k11),
                       dTmdt(T, Tm, k2)]
                      )

    A_0 = array([HCl_0, LDH_0, poly_act_0, 0., prim_stab_0, 0., 0., T_0, Tm_0])
    
    soln = odeint(dXdt, A_0, time)

    HCl = soln[:, 0]
    LDH = soln[:, 1]
    poly_act = soln[:, 2]
    radical = soln[:, 3]
    prim_stab = soln[:, 4]
    deg_poly = soln[:, 5]
    x_link = soln[:, 6]
    T = soln[:, 7]
    Tm = soln[:, 8]

    mu_V = zeros(len(time))
    torque_V = zeros(len(time))

    for i in range(0,len(time)):
        mu_V[i] = mu(mu_0, E, R, T[i], k9, deg_poly[i], k10, x_link[i], q)
        torque_V[i] = torque(k1, mu_V[i])

    return HCl, LDH, poly_act, radical, prim_stab, deg_poly, x_link, T, Tm, mu_V, torque_V

# Function only returning torque curve

def torque_curve(p, time):
    curves = model_curves(p, time)
    return curves[10]
	
def temp_curve(p, time):
    curves = model_curves(p, time)
    return curves[8]

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
    
    meantorgue=mean(t_means)
    meantemp=mean(T_means)
    std_torgue=mean(t_stds)
    std_temp=mean(T_stds)
    
    
    
    
    
    
    
    
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