# Import my data

import scipy.io as sio
import numpy as np
import pandas as pd

behavfile = sio.loadmat('./datafiles/Sessions_select_20190415_01_pA_15-20_binsof5.mat')
   
behavdata = behavfile['Sessions_select']

nth_rat = 1
num_sess = 45; setns = 1
# Session_data = np.ndarray([behavdata.size,1]);
# Maybe is better to do a dictionary

# Session_data_np = dict()

# for nth_rat in range(0,behavdata.size):
#     # This is the matrix of behav data for my nth subject:
#     tmpdata = np.array(behavdata[0, nth_rat]['Sess_conc2'])
#     tmpdata = tmpdata[0:num_sess,:]
#     tmpname = np.array(behavdata[0, nth_rat]['Rat']); tmpname = tmpname[0]
#     Session_data_np[tmpname]=tmpdata
#     print('Fetched behav data from', tmpname)

# New version of Session_data, using pandas
Session_data = dict()
for nth_rat in range(0,behavdata.size):     
    # Subject ID:
    tmpname = np.array(behavdata[0, nth_rat]['Rat']); tmpname = tmpname[0]

    # This is the matrix of behav data for my nth subject:
    tmpdata = np.array(behavdata[0, nth_rat]['Sess_conc2'])     # this is a numpy array
    if setns == 1:
        tmpdata = tmpdata[0:num_sess,:] # if I want to standardize num of sessions per subject

    tmpdata = pd.DataFrame(tmpdata, index=['session%s'%x for x in range(1,len(tmpdata)+1)],columns=['var%s'%x for x in range(1,tmpdata.shape[1]+1)])  
    Session_data[tmpname] = tmpdata
    print('Fetched behav data from', tmpname, ',', len(onepd), 'sessions')




