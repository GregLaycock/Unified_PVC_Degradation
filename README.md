Kinetic analysis of Gear Rheometer results
==========================================

These files can be used to analyse the results of tests on a compounder Gear Rheometer.

Instructions
------------



1. Insert the directory for the data on your machine in the config_sample.json file and change the name of the file to config.json

 

2

. The limits for the parameters can be set using Adjust_parameters.py.  

3.The fitting routine runs with the 'Fit_parameters_to_multi_files.py' . Simply run the code which outputs a json file with all the fitted parameters stored in it. 

4. plotting is done via PDF_plotting.py which simulates curves for all the diferent initial conditions in the experiments and plots them vs the data files. The plots are stored in a PDF file which you can set the name of.

5. note that currently support for datafile name reading is inactive and you will have to specify LDH_inits and PS_inits for the different data files yourself. 

ENJOY its a lot of fun I promise....its really not...like seriously your soul is going to be eaten alive by the 10th run. Good luck