
# coding: utf-8

# In[1]:

from datahandling import DataFile, alldatafiles, cuts, trim
get_ipython().magic(u'pylab inline')


# In[2]:

files = alldatafiles()


# In[3]:

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


# In[4]:

print 'mean torque:', mean(t_means)
print 'mean temperature:', mean(T_means)
print 'standard deviation torque:', mean(t_stds)
print 'standard deviation temperature:', mean(T_stds)


# In[5]:

meantorgue=mean(t_means)
meantemp=mean(T_means)
std_torgue=mean(t_stds)
std_temp=mean(T_stds)


# In[9]:

from numpy import mean


# In[ ]:



