#for documentation and import purpose set __all__ with a list of the submodules
import os

if __name__=='__main__':
    #The program was launched as a script,
    #so there is nothing to do, because the
    #current working directory is already set
    #to the directory of this script
    module_folder=''    
else:
    #The program was launched as a module.
    #Get the module directory name from __file__
    #which contains the absolute path of the file
    #being executed
    module_folder=os.path.dirname(__file__)+os.sep        

#Make a list of all the Instrument panels in the folder
__all__=[]

import PyQt4.uic

def compile_if_necessary(input_ui_file,output_py_file):
    #prepare the file names
    input_path = module_folder+input_ui_file
    output_path = module_folder+output_py_file
    #recompile the .ui Qt file if this script is launched directly
    #or if the compiled .py GUI file does not exist
    #or if it is more recent than the compiled .py GUI file,
    #if __name__=='__main__' or not(os.path.isfile(output_path)) or os.path.getmtime(input_path)>os.path.getmtime(output_path):
    if not(os.path.isfile(output_path)) or os.path.getmtime(input_path)>os.path.getmtime(output_path):
        print "update detected: recompiling "+input_ui_file
        f=open(output_path,"w")
        PyQt4.uic.compileUi(input_path,f)
        f.close()    

for my_file in os.listdir(module_folder):
    if '.ui' in my_file:
        __all__.append(my_file[:-3])
        compile_if_necessary(my_file,my_file[:-3]+'_Ui.py')
        exec('import '+__all__[-1])
