"""
for documentation and import purpose set __all__ with a list of the submodules
"""
import os

import PyQt5.uic

if __name__ == '__main__':
    #The program was launched as a script,
    #so there is nothing to do, because the
    #current working directory is already set
    #to the directory of this script
    MODULE_FOLDER = ''
else:
    #The program was launched as a module.
    #Get the module directory name from __file__
    #which contains the absolute path of the file
    #being executed
    MODULE_FOLDER = os.path.dirname(__file__)+os.sep

#Make a list of all the Instrument panels in the folder
__all__ = []

def compile_if_necessary(input_ui_file, output_py_file):
    """
    recompile the .ui Qt file if this script is launched directly
    or if the compiled .py GUI file does not exist
    or if it is more recent than the compiled .py GUI file
    """
    #prepare the file names
    input_path = MODULE_FOLDER+input_ui_file
    output_path = MODULE_FOLDER+output_py_file
    if not(os.path.isfile(output_path)) \
     or os.path.getmtime(input_path) > os.path.getmtime(output_path):
        print("update detected: recompiling "+input_ui_file)
        with open(output_path, encoding='utf-8', mode="w") as outf:
            print(input_path+'\n')
            PyQt5.uic.compileUi(input_path, outf, from_imports=True)

for my_file in os.listdir(MODULE_FOLDER):
    if '.ui' in my_file:
        __all__.append(my_file[:-3])
        compile_if_necessary(my_file, my_file[:-3]+'_Ui.py')
        exec('from . import '+__all__[-1])
