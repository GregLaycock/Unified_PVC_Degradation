
# coding: utf-8

# ## Looping over data files and fitting parameters to torque and temp curve simultaneously with multistart

# In[5]:

from datahandling import DataFile, alldatafiles, cuts, trim, file_parse
from lmfit import minimize, report_fit
from model_parameters import parameters, parameter_vectors, unpack_parameters, rand_ini_val
from Simulation import torque_curve, fcn2min_torque, fcn2min, model_curves, joined_curves
from time import time as tm
from matplotlib.backends.backend_pdf import PdfPages
from numpy import append
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

with PdfPages('all_curves_14.pdf') as pdf:
    for i, f in enumerate(files):
        time_data, temp_data, torque_data = DataFile(f).simple_data()
        
        # Trimming data
        c = cuts(torque_data)
        time_data = trim(time_data, c)
        temp_data = trim(temp_data, c)
        torque_data = trim(torque_data, c)
        
        #Joining data
        joined_data = joined_curves(torque_data, temp_data)
        
        # Parsing filenames
        LDH_0, LDH_type = file_parse(f)
        all_LDH_type = append(all_LDH_type, LDH_type)
        
        # Multistart
        starts = 10
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
            
            print j + 1
            
        #Storing parameter and error values
        all_ps.append(p_best)
        all_errors.append(smallest_error)
        all_int_errors.append(smallest_int_error)
        
        print 'Completed Fit ',(i + 1)
        print '__________________________'
        
        #Plotting to pdf
        curves = model_curves(p_best, time_data)
   #     HCl, LDH, poly_act, radical, prim_stab, deg_poly, x_link, T, Tm, mu, torque = curves
        
        title = 'Run ' + str(i + 1) + ', LDH type: ' + LDH_type + ', initial LDH: ' + str(LDH_0)
        
        fig_torque = figure()
        fig_torque.suptitle(title)
        plot(time_data, curves['Torq'], label='fitted torque curve')
        plot(time_data, torque_data, label='torque data')
        legend()
        
        fig_temp = figure()
        fig_temp.suptitle(title)
        plot(time_data, curves['Tm'], label='fitted temp curve')
        plot(time_data, temp_data, label='temp data')
        legend()
        xlim([0, time_data[len(time_data) - 1] + 14])
        
        fig_species = figure()
        fig_species.suptitle(title)
        plot(time_data, curves['HCl'], '--', label='HCl')
        #plot(time_data, LDH, label='LDH')
        #plot(time_data, poly_act, '-.', label='poly_act')
        plot(time_data, curves['rad'], ':', label='radical')
        plot(time_data, curves['ps'], '--', label='prim_stab')
        plot(time_data, curves['dp'], label='deg_poly')
        plot(time_data, ['xl'], label='x_link')
        legend()
        xlim([0, time_data[len(time_data) - 1] + 8])
        
        pdf.savefig(fig_torque)
        pdf.savefig(fig_temp)
        pdf.savefig(fig_species)

elapsed = tm() - t
print '*******************'
print 'elapsed time (min) =', elapsed/60.


# #### Generating parameter vectors and plotting

# In[4]:

para_V = parameter_vectors(all_ps)


# In[5]:

figure_headings = figure_heads()

# In[6]:

for h, ps in zip(figure_headings, para_V):
    figure().suptitle(h)
    plot(ps, '.')


# ####Placing parameters into DataFrame

# In[7]:

from pandas import DataFrame


# In[8]:

para_frame = DataFrame.from_records(para_V, index=figure_headings).transpose()


# Mean values of each parameter

# In[9]:

para_frame.mean(axis=0)


# Upper boundary values for each parameter = mean + 2.standard deviation

# In[10]:

upper_bounds = para_frame.mean(axis=0) + 2*para_frame.std(axis=0)
upper_bounds


# In[11]:

lower_bounds = para_frame.mean(axis=0) - 2*para_frame.std(axis=0)
lower_bounds


# Adding columns for LDH type and Average Absolute Error to DataFrame. 
# -Note: the Ave Abs Error is the error on the joined curve with the number ranges equated

# In[12]:

para_frame['LDH type'] = all_LDH_type
para_frame['Average of Absolute Error'] = all_errors
para_frame['Integral of the Absolute Error'] = all_int_errors


# Writing DataFrame to csv

# In[13]:

para_frame.to_csv('all_parameters_14.csv')


# In[ ]:



