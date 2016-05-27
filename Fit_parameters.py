import os.path

from datahandling import datadir, DataFile, alldatafiles, cuts, trim, file_parse
from lmfit import minimize, report_fit
from model_parameters import parameters, parameter_vectors, unpack_parameters, rand_ini_val
from time import time as tm
from numpy import append,trapz
from Simulation import *
# #### Loading all files

# In[6]:

files = alldatafiles()
no_files = len(files)

#setting up
time_sets = get_timesets(files)
t = tm()
all_ps = []
all_LDH_type = []
all_errors = []
all_int_errors = []

# getting LDH info - this will be implemented later

#for i, f in enumerate(files):
    # Parsing filenames
#    LDH_0, LDH_type = file_parse(f)
#    all_LDH_type = append(all_LDH_type, LDH_type)

# this is a temporary solution for LDH types and zero values
LDH_inits = []
all_LDH_type = []
for i,lis in enumerate(time_sets):
    LDH_inits.append(0.3)
    all_LDH_type.append('mystery_LDH')

#this should be implemented later once the files have been renamed
#LDH_inits = LDH_zeros()   # this will require that the files be renamed, will test with a list later [1.3,1.3,1.3 .....]
#all_LDH_type = append(all_LDH_type, LDH_type)

# joining data curves( note Joined_data has a capital J and is not a function)
Joined_data = joined_data()

# Multistart


def run_fit(time_sets,LDH_inits,Joined_data,starts):
    smallest_error = 100000.0
    for j in range(starts):

        print 'currently on start', j + 1
        # Initialising values
        ini_val = rand_ini_val()

        # Initialising and limiting parameters
        p = parameters(ini_val)

        # Fitting data
        result = minimize(fcn3min, p, args=(time_sets,LDH_inits,Joined_data))

        # Calculating average and integral of absolute error
        error_list = fcn3min(p, time_sets,LDH_inits, Joined_data)
        abs_error_list = map(abs, error_list)
        ave_abs_error = sum(abs_error_list)/len(error_list)
        int_abs_error = trapz(abs_error_list, dx=0.017)

        # Check error and save parameters
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
    return p_best, smallest_int_error

parfilename = os.path.join(datadir, 'parameters.json')

if __name__ == "__main__":
    fitted_parameters, smallest_int_error = run_fit(time_sets,LDH_inits,Joined_data,50)

    # Write parameters to file:
    with open(parfilename, 'w') as parfile:
        fitted_parameters.dump(parfile)

