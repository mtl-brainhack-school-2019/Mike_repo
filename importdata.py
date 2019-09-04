# Import my data

import scipy.io as sio
import numpy as np
import pandas as pd

behavfile = sio.loadmat('./datafiles/Training_ephys_data.mat')
   
database = behavfile['Training_ephys_data']

num_sess = 45; setns = 1
# Session_data = np.ndarray([database.size,1]);
# Maybe is better to do a dictionary

# Session_data_np = dict()

# for nth_rat in range(0,database.size):
#     # This is the matrix of behav data for my nth subject:
#     tmpBehav = np.array(database[0, nth_rat]['Sess_conc2'])
#     tmpBehav = tmpBehav[0:num_sess,:]
#     tmpname = np.array(database[0, nth_rat]['Rat']); tmpname = tmpname[0]
#     Session_data_np[tmpname]=tmpBehav
#     print('Fetched behav data from', tmpname)

# New version of Session_data, using pandas
Session_data = dict()
# Ephys_data = pd.DataFrame(columns=['x-corr', 'x-corr-CNO', 'BW20', 'BW20-CNO'])
Ephys_data = np.full([database.size, 4], np.nan)    # pre-allocate for e-phys data

for nth_rat in range(0,database.size):     
    # Subject ID:
    tmpname = np.array(database[0, nth_rat]['Rat']); tmpname = tmpname[0]

    # This is the matrix of behav data for my nth subject:
    tmpBehav = np.array(database[0, nth_rat]['Sess_conc2'])     # this is a numpy array
    if setns == 1:
        tmpBehav = tmpBehav[0:num_sess,:] # if I want to standardize num of sessions per subject

    tmpBehav = pd.DataFrame(tmpBehav, index=['session%s'%x for x in range(1,len(tmpBehav)+1)],columns=['var%s'%x for x in range(1,tmpBehav.shape[1]+1)])  
    
    #tag data, use real variable names instead of just 'varx'
    tmpBehav.rename(columns={'var8':'hit-rate',
                             'var9':'fp-rate',
                             'var12':'d-prime',
                             'var10':'max-lev',
                             'var15':'max-lev-adj',},
                             inplace=True)

    Session_data[tmpname] = tmpBehav
    #print('Fetched behav data from', tmpname, ',', len(tmpBehav), 'sessions')

    # This is the matrix of ephys data for my nth subject:
    tmpEphys = np.array(database[0, nth_rat]['ephys'])     # this is a numpy array
    Ephys_data[nth_rat,:] = tmpEphys
    print('Fetched e-phys data from', tmpname)


Ephys_pd = pd.DataFrame(Ephys_data, index=['rat%s'%x for x in range(1,database.size+1)], columns=['x-corr', 'x-corr-CNO', 'BW20', 'BW20-CNO'])
# print('Check var status')


