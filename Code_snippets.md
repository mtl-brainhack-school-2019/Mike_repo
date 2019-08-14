Code snipets I'll need

# To import data from matlab
 
    from scipy.io import loadmat
    fl = loadmat('/path/to/matfile.mat')
    # this produces a dictionary of your matfile.
    # To see the structures:
    fl.keys()
    # To access data in the structure
    fl['key']

# Objective
    # Description    
    newObj = some_comand(someObj);