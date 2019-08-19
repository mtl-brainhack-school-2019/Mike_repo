Code snipets I'll need

# To import data from matlab
 
    from scipy.io import loadmat
    fl = loadmat('/path/to/matfile.mat')
    # this produces a dictionary of your matfile.
    # To see the structures:
    fl.keys()
    # To access data in the structure
    fl['key']

# Import data (importing library)
    # Description    
    import scipy.io as sio
    
    behavfile = loadmat('./datafiles/Sessions_select_20190415_01_pA_15-20_binsof5.mat')
    
    behavdata = behavfile['Sessions_select'];

    nth_rat = 1;


# Adding SSH to your github account
    https://help.github.com/en/articles/adding-a-new-ssh-key-to-your-github-account

# alias commands for git/github
    https://stackoverflow.com/questions/19595067/git-add-commit-and-push-commands-in-one?noredirect=1&lq=1

    to create:
    git config --global alias.add-com-push '!git add . && git commit -a -m "commit" && git push'

    (base) mike@home:~/Brainhack2019/Mike_repo$ git config --get-regexp alias
    alias.addcom !git add -A && git commit -m

    to change:
    git config --global alias.addcom '!git add -u && git commit -a -m "commit"'

    git config --global alias.addcom '!git add -u && git commit -a -m'

    to delete alias:
    (base) mike@home:~/Brainhack2019/Mike_repo$ git config --global --unset alias.st

# Remove a folder from git (stop tracking, and delete from github)

    (base) mike@home:~/Brainhack2019/Mike_repo$ git rm -r --cached datafiles/

# Objective
    # Description    
    newObj = some_comand(someObj);
