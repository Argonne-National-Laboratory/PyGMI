import os
module_folder=os.path.dirname(__file__)+os.sep
#Make a list of all the measurements programs in the folder
__all__=[]
for my_file in os.listdir(module_folder):
    if '.py' in my_file and '.pyc' not in my_file and '__init__' not in my_file:
        __all__.append(my_file[:-3])

#if '.pyc' not in my_file and '__init__' not in my_file and '__pycache__' not in my_file:
