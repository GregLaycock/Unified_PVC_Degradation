
# coding: utf-8

# ## Looping over data files and fitting parameters to torque and temp curve simultaneously with multistart

# In[5]:

from datahandling import DataFile, alldatafiles, cuts, trim, file_parse
from model_parameters import parameters, parameter_vectors, unpack_parameters, rand_ini_val
from time import time as tm
from matplotlib.backends.backend_pdf import PdfPages
from numpy import append,trapz
from Adjust_Kinetics import *
from Fit_parameters import parfilename, LDH_inits, all_LDH_type
from Simulation import model_curves
from matplotlib import pyplot as plt

import lmfit

parameters_to_csv = False

# #### Loading all files

# In[6]:

files = alldatafiles()
no_files = len(files)


# #### Looping over files
# Saving pdf of all torque, temp and species curves

# In[7]:

t = tm()

# Read parameters from file
fitted_parameters = lmfit.Parameters()
fitted_parameters.load(open(parfilename))

with PdfPages('all_curves_1.pdf') as pdf:
    for i, f in enumerate(files):
        time_data, temp_data, torque_data = DataFile(f).simple_data()
        
        # Trimming data
        c = cuts(torque_data)
        time_data = trim(time_data, c)
        temp_data = trim(temp_data, c)
        torque_data = trim(torque_data, c)

        #Plotting to pdf

        curves = model_curves(fitted_parameters, time_data, LDH_inits[i])

        
        title = 'Run ' + str(i + 1) + ', LDH type: ' + all_LDH_type[i] + ', initial LDH: ' + str(LDH_inits[i])
        from matplotlib.pyplot import *
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
        plot(time_data, curves['HCL'], '--', label='HCl')
        #plot(time_data, LDH, label='LDH')
        #plot(time_data, poly_act, '-.', label='poly_act')
        plot(time_data, curves['rad'], ':', label='radical')
        plot(time_data, curves['ps'], '--', label='prim_stab')
        plot(time_data, curves['dp'], label='deg_poly')
        plot(time_data, curves['xl'], label='x_link')
        plot(time_data, curves['double'], label='long_chains')
        plot(time_data, curves['half'], label='short_chains')
        legend()
        xlim([0, time_data[len(time_data) - 1] + 8])
        
        pdf.savefig(fig_torque)
        pdf.savefig(fig_temp)
        pdf.savefig(fig_species)

        plt.close(fig_temp)
        plt.close(fig_torque)
        plt.close(fig_species)

elapsed = tm() - t
print('*******************')
print('elapsed time (min) =', elapsed/60.)


# #### Generating parameter vectors and plotting

# In[4]:
if parameters_to_csv:
    # XXX This is currently broken
    para_V = parameter_vectors(fitted_parameters)


    # In[5]:
    import Adjust_Kinetics
    figure_headings = Adjust_Kinetics.figure_heads

    # In[6]:

    #for h, ps in zip(figure_headings, para_V):
     #   figure().suptitle(h)
      #  plot(ps, '.')


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

    para_frame['parameters and errors from fitting for joined curve representing all data'] = 0
    para_frame['Average of Absolute Error'] = Fit_parameters.ave_abs_error
    para_frame['Integral of the Absolute Error'] = Fit_parameters.int_abs_error


    # Writing DataFrame to csv

    # In[13]:

    para_frame.to_csv('all_parameters_1.csv')



