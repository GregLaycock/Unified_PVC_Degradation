import json
import os
import glob
import pandas

# read configuration file and expand ~ to user directory
with open('config.json') as f:
    config = json.load(f)
datadir = os.path.expanduser(config['datadir'])

def alldatafiles():
    return glob.glob(os.path.join(datadir, '**/*.txt'))


class DataFile:
    """ Class for holding data """
    def __init__(self, filename):
        # Split into directory and filename parts
        self.directory, self.filename = os.path.split(filename)
        # Load with pandas
        self.data = pandas.read_table(filename,
                                      skiprows = 4,
                                      sep = ';',
                                      usecols = range(6))

    def simple_data(self):
        time = self.data['t [min]'].values
        temp = self.data[self.data.columns[4]].values
        torque = self.data['M [Nm]'].values

        return time, temp, torque

def cuts(vector):
    l = len(vector)
    vec_1 = vector[:l/2]
    vec_2 = vector[l/2:]
    cut_2 = l
    vector = list(vector)
    cut_1 = vector.index(max(vec_1))
    for j in range(l/2, l):
        if vector[j] > (max(vec_2) - 2) and cut_2 == l:
            cut_2 = j
    return cut_1, cut_2

def half_cuts(vector):
    l = len(vector)
    return 0, l/4
	
def trim(vector, cut):
    return vector[cut[0]:cut[1]]

def file_parse(f):
    from os import path
    
    direct, filename = path.split(f)
    LDH_0, no_use, LDH_type = filename.split('_')
    LDH_type, file_type = LDH_type.split('.')
    
    if LDH_0[0] == '0':
        LDH_0 = float('0.'.join(LDH_0.split('0')))
    else:
        LDH_0 = float(LDH_0)
    
    rem_nos = ['1', '2', '3', '4', '5', '6']
    for rem in rem_nos:
        if LDH_type.find(rem) != -1:
            LDH_type, no_use = LDH_type.split(LDH_type[LDH_type.find(rem)])

    return LDH_0, LDH_type 