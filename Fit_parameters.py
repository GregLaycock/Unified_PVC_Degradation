import os.path

from datahandling import datadir, config
from lmfit import minimize, report_fit
from model_parameters import parameters, parameter_vectors, unpack_parameters, rand_ini_val
from time import time as tm
from numpy import append,trapz
from Simulation import *
# #### Loading all files

# In[6]:
index = 0
files = alldatafiles()
no_files = len(files)

#setting up
time_sets = get_timesets(files)
t = tm()
all_ps = []
all_LDH_type = []
all_errors = []
all_int_errors = []

# getting LDH and prim stab info - this will be implemented later by naming files

#for i, f in enumerate(files):
    # Parsing filenames
#    LDH_0, LDH_type = file_parse(f)
#    all_LDH_type = append(all_LDH_type, LDH_type)

# this is a temporary solution for LDH types and zero values
LDH_inits = [6.918,2.4,4.04,0.72,0.,4.268,2.19,0.989,0.3345,2.64,0.194615,0.53,3.148,0.858,1.274,0.302158,0.,3.599,1.7,1.272697]
PS_inits = [0.421,2.8345,0.218,1.684,0.32,1.385,0.,1.048,4.7239,0.55,0.673,2.076,1.214,6.263,3.256,0.,3.959,3.534,0.655,0.]
all_LDH_type = []

for i,lis in enumerate(time_sets):
 #   LDH_inits.append(0.3)
    all_LDH_type.append('Hydrotalcite')

#this should be implemented later once the files have been renamed
#LDH_inits = LDH_zeros()   # this will require that the files be renamed, will test with a list later [1.3,1.3,1.3 .....]
#all_LDH_type = append(all_LDH_type, LDH_type)

# joining data curves( note Joined_data has a capital J and is not a function)
Joined_data = joined_data()
Single_data = single_data(index)
# Multistart


def run_fit(time_sets,LDH_inits,Joined_data,starts,PS_inits,index):
    smallest_error = 100000.0
    for j in range(starts):

        print 'currently on start', j + 1
        # Initialising values
        ini_val = rand_ini_val()

        # Initialising and limiting parameters
        p = parameters(ini_val)

        # Fitting data
        result = minimize(fcn4min, p, args=(time_sets,LDH_inits,Single_data,PS_inits,index))

        # Calculating average and integral of absolute error
        error_list = fcn4min(p, time_sets,LDH_inits, Single_data,PS_inits,index)
        abs_error_list = map(abs, error_list)
        ave_abs_error = sum(abs_error_list)/len(error_list)
        int_abs_error = trapz(abs_error_list, dx=0.017)

        # Check error and save parametersreturn p_best, smallest_int_error
        smallest_error = min([smallest_error, ave_abs_error])
        if smallest_error == ave_abs_error:
            p_best = p
            smallest_int_error = int_abs_error

        print 'completed start', j + 1

    #Storing parameter and error values
       #all_ps.append(p_best)   obsolete
    #all_errors.append(smallest_error)         obsoleted as these were per fit but we no longer fit data files separately
    #all_int_errors.append(smallest_int_error)

    print 'Completed Fit '
    print('__________________________')


    elapsed = tm() - t
    print('*******************')
    print 'elapsed time (min) =', elapsed/60.
    vals = unpack_parameters(p_best)
    nms = ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7', 'k8', 'k9', 'k10', 'k11', 'k12', 'k13', 'k14', 'k15', 'UA','pas_0', 'mu_0', 'E', 'q']
    for i, name in enumerate(nms):
        print name,vals[i]
    return p_best, smallest_int_error

parfilename = os.path.join(datadir, config['parfilename'])

if __name__ == "__main__":
    fitted_parameters, smallest_int_error = run_fit(time_sets,LDH_inits,Joined_data,500,PS_inits,index)

    # Write parameters to file:
    with open(parfilename, 'w') as parfile:
        fitted_parameters.dump(parfile)

