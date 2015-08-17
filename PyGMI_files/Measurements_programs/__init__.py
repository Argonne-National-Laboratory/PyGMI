import os
module_folder=__file__[:__file__.rindex(os.sep)]+os.sep
#Make a list of all the measurements programs in the folder
__all__=[]
for my_file in os.listdir(module_folder):
    if '.pyc' not in my_file and '__init__' not in my_file:
        __all__.append(my_file[:-3])

