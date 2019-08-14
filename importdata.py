# Import my data

import scipy.io as sio
import numpy as np
    
behavfile = sio.loadmat('./datafiles/Sessions_select_20190415_01_pA_15-20_binsof5.mat');
   
behavdata = behavfile['Sessions_select']

nth_rat = 1;
num_sess = 50;
Session_data = np.ndarray([behavdata.size,1]);

for nth_rat in range(0,behavdata.size):
    Session_data[nth_rat,0] = behavdata[0, nth_rat]['Sess_conc2']; 
    



