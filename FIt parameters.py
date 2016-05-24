from datahandling import DataFile, alldatafiles, cuts, trim, file_parse
from lmfit import minimize, report_fit
from model_parameters import parameters, parameter_vectors, unpack_parameters, rand_ini_val
from Simulation import torque_curve, fcn2min_torque, fcn2min, model_curves, joined_curves
from time import time as tm
from matplotlib.backends.backend_pdf import PdfPages
from numpy import append,trapz
from Adjust_Kinetics import *

# #### Loading all files

# In[6]:

files = alldatafiles()
no_files = len(files)


# #### Looping over files
# Saving pdf of all torque, temp and species curves

# In[7]:

t = tm()
all_ps = []
all_LDH_type = []
all_errors = []
all_int_errors = []


for i, f in enumerate(files):
    time_data, temp_data, torque_data = DataFile(f).simple_data()

    # Trimming data
    c = cuts(torque_data)
    time_data = trim(time_data, c)
    temp_data = trim(temp_data, c)
    torque_data = trim(torque_data, c)

    #Joining data
    joined_data = joined_curves(torque_data, temp_data,f)

    # Parsing filenames
    LDH_0, LDH_type = 1.3,'mystery' #file_parse(f)

    all_LDH_type = append(all_LDH_type, LDH_type)

    # Multistart
    starts = 2
    smallest_error = 100000.0

    for j in range(starts):

        # Initialising values
        ini_val = rand_ini_val(LDH_0)

        # Initialising and limiting parameters
        p = parameters(ini_val)

        # Fitting data
        result = minimize(fcn2min, p, args=(time_data, joined_data))

        # Calculating average and integral of absolute error
        error_list = fcn2min(p, time_data, joined_data)
        abs_error_list = map(abs, error_list)
        ave_abs_error = sum(abs_error_list)/len(error_list)
        torque_error_list = fcn2min_torque(p, time_data, torque_data)
        abs_torque_error_list = map(abs, torque_error_list)
        int_abs_error = trapz(abs_torque_error_list, dx=0.017)

        # Check error and save parameters
        smallest_error = min([smallest_error, ave_abs_error])
        if smallest_error == ave_abs_error:
            p_best = p
            smallest_int_error = int_abs_error

        print(j + 1)

    #Storing parameter and error values
    all_ps.append(p_best)
    all_errors.append(smallest_error)
    all_int_errors.append(smallest_int_error)

    print('Completed Fit ',(i + 1))
    print('__________________________')

elapsed = tm() - t
print('*******************')
print('elapsed time (min) =', elapsed/60.)