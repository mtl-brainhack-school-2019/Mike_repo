# Manipulate data, organize in X, Y cols for PLS

# From importdata.py, data is saved as
# Behav: Session_data, dict where 'keys' are rat names, 'values' are a pandas dataframe
#           within each pd dataframe, comlums are already named as parameters of interest, 
#           i.e., d-prime, hit-rate, fp-rate, max-lev, max-lev-adj

# (0) import functions/data as needed
import numpy as np
import pandas as pd

from scipy.integrate import simps

from importdata import Session_data, num_sess, Ephys_pd

# (1) fetch  behav data (X)

# (1.1) Prep parameters for behav data and get subject IDs (to access dictionary)
behav_params = ['hit-rate','fp-rate','d-prime','max-lev','max-lev-adj']
num_sess = 45
def getList(dict):          # to get ratnames
    return [*dict]
ratnames = (getList(Session_data))

# (1.2) pre-allocate X as numpy array of size n-subjects x (n_sessions x n_parameters + 1)
X = np.full([len(Session_data), (num_sess+1)*len(behav_params)], np.nan)    # pre-allocate for e-phys data

# (1.3) fetch behav data for nth_rat (as pd dataframe)
for nth_rat in range(0,len(Session_data)):
    nth_name = ratnames[nth_rat]
    nth_Behav = Session_data[nth_name]  
    nth_Behav = nth_Behav[behav_params]     # reduce to keep only params of interest

# (1.4) compute AUC
    AUCs = np.full([1, len(behav_params)], np.nan)
    for i in range(0, len(behav_params)):
        ith_param = behav_params[i]; ith_series = nth_Behav[ith_param].values; 
        AUCs[0,i] = simps(ith_series); #AUCs = pd.Series(AUCs)
    nth_fullBehav = np.concatenate((nth_Behav.values,AUCs))

# (1.5) save to X   Y
    X[nth_rat,:] = nth_fullBehav.flatten('F')


# (2) fetch e-phys data (Y)
ephys_params = ['x-corr', 'x-corr-CNO', 'BW20', 'BW20-CNO']
Y = Ephys_pd.values


# (3) Calculate z-scores
from scipy.stats import zscore

Xz = zscore(X, ddof=1)
Yz = zscore(Y, ddof=1)

# (4) Build cross-correlation matrix
from scipy.linalg import svd

x_corr = (Yz.T @ Xz) / (len(Xz)-1)
U, sval, V = svd(x_corr.T, full_matrices=False)
V = V.T # transpose: feature x component array
print('U shape: {}'.format(U.shape))
print('V shape: {}'.format(V.shape))

# (5) Examine correlations
from scipy.stats import pearsonr

x_scores, y_scores = Xz @ U, Yz @ V

for comp in range(x_scores.shape[-1]):
    corr = pearsonr(x_scores[:,comp], y_scores[:,comp])
    print('Component {:>2}: r = {:.2f}, p = {:.3f}'.format(comp, *corr))


# Look at correlations (1st component)    
import matplotlib.pyplot as plt

y_corr = (Yz.T @ zscore(x_scores, ddof=1)) / (len(x_scores) - 1)
for n, ephys_correlation in enumerate(y_corr[:, 0]):
    print('ephys parameter {:<5} r = {:>5.2f}'.format(ephys_params[n] + ':',ephys_correlation))

fig, ax = plt.subplots(1, 1)
ax.barh(range(len(y_corr))[::-1], width=y_corr[:, 0],)
ax.set(yticks=range(len(y_corr))[::-1], yticklabels=ephys_params)
ax.set(xlabel='Correlation with projected X scores')
fig.tight_layout()    

# Effect size (variance explained)
varexp = sval ** 2 / sum(sval ** 2) 
 
fig, ax = plt.subplots(1, 1) 
ax.plot(varexp * 100, '.-') 
ax.set(xlabel='Component #', ylabel='Variance explained (%)') 

# Get distribution of explained variances
n_perm = 100
rs = np.random.RandomState(1234)  # Set a random seed for reproducibility

sval_perm = np.zeros((len(varexp), n_perm))

for n in range(n_perm):

    # Permute and z-score the Y matrix (leaving the X matrix intact)
    resamp = rs.permutation(len(Y))
    Ypz = zscore(Y[resamp], ddof=1)

    # Regenerate the cross-correlation matrix and compute the decomposition
    cross_corr = (Ypz.T @ Xz) / (len(Xz) - 1)
    U_new, sval_new, V_new = svd(cross_corr.T, full_matrices=False)
    V_new = V_new.T

    # Align the new singular vectors to the original using Procrustes. We can
    # do this with EITHER the left or right singular vectors; we'll use the
    # left vectors since they're much smaller in size so this is more
    # computationally efficient.
    N, _, P = svd(V.T @ V_new, full_matrices=False)
    aligned = V_new @ np.diag(sval_new) @ (P.T @ N.T)

    # Calculate the singular values for the rotated, permuted component space
    sval_perm[:, n] = np.sqrt(np.sum(aligned ** 2, axis=0))

# Calculate the number of permuted singular values larger than the original
# and normalize by the number of permutations. We can treat this value as a
# non-parametric p-value.
sprob = (np.sum(sval_perm > sval[:, None], axis=1) + 1) / (n_perm + 1)
for n, pval in enumerate(sprob):
    print('Component {}: non-parametric p = {:.3f}'.format(n, pval))

# Only the first component is below 0.05 threshold
# Hence, we'll only consider the first component for the 'e-phys score'

figFINAL, ax1 = plt.subplots(1, 1)
ax2 = ax1.twinx()  
ax1.plot(x_scores[:,0], 'g-') 
ax2.plot(y_scores[:,0], 'b-')
ax1.set_xlabel('subject #')                                                                                                                
ax1.set_ylabel('Behav score', color='g')                                                                                                   
ax2.set_ylabel('e-phys score', color='b')     
 