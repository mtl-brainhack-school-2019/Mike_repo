# Import my data

import scipy.io as sio
import numpy as np
    
behavfile = sio.loadmat('./datafiles/Sessions_select_20190415_01_pA_15-20_binsof5.mat');
   
behavdata = behavfile['Sessions_select']

nth_rat = 1;
num_sess = 45;
# Session_data = np.ndarray([behavdata.size,1]);
# Maybe is better to do a dicexctionary
Session_data = dict()

for nth_rat in range(0,behavdata.size):
    # This is the matrix of behav data for my nth subject:
    tmpdata = np.array(behavdata[0, nth_rat]['Sess_conc2']); 
    tmpdata = tmpdata[0:num_sess,:]
    tmpname = np.array(behavdata[0, nth_rat]['Rat']); tmpname = tmpname[0];
    Session_data[tmpname]=tmpdata;
    print('Fetched behav data from', tmpname)
    
    
    #Session_data[nth_rat,0] = np.array(cc);
    #Session_data[nth_rat,0] = np.array([behavdata[0, nth_rat]['Sess_conc2']);
    #Session_data[nth_rat,0] = behavdata[0, nth_rat]['Sess_conc2']; 




