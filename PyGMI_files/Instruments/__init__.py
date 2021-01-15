#for documentation and import purpose set __all__ with a list of the submodules
import os
module_folder=os.path.dirname(__file__)+os.sep
#Make a list of all the Instruments drivers in the folder
__all__=[]

for my_file in os.listdir(module_folder):
    if '.py' in my_file and '.pyc' not in my_file and '__init__' not in my_file:
        __all__.append(my_file[:-3])
        exec('from . import '+__all__[-1])
#print __all__
##example: __all__=["AMI420","CryoCon","ES7215_BNCswitch","Instruments","Keithley2182A","Keithley2420","Keithley6221","Lakeshore340","SR830","Tektronix_TDS2024C","VXMStepmotor"]
