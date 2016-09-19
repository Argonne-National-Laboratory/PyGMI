#This module recompile the GUI if the .ui file
#is more recent than the compiled .py file
import os


if __name__=='__main__':
    #The program was launched as a script,
    #so there is nothing to do, because the
    #current working directory is already set
    #to the directory of this script
    rep_module=''    
else:
    #The program was launched as a module.
    #Get the module directory name from __file__
    #which contains the absolute path of the file
    #being executed
    rep_module=os.path.dirname(__file__)+os.sep        

import PyQt4.uic

def compile_if_necessary(input_ui_file,output_py_file):
    #prepare the file names
    input_path = rep_module+input_ui_file
    output_path = rep_module+output_py_file
    #recompile the .ui Qt file if this script is launched directly
    #or if the compiled .py GUI file does not exist
    #or if it is more recent than the compiled .py GUI file,
    #if __name__=='__main__' or not(os.path.isfile(output_path)) or os.path.getmtime(input_path)>os.path.getmtime(output_path):
    if not(os.path.isfile(output_path)) or os.path.getmtime(input_path)>os.path.getmtime(output_path):
        print "update detected: recompiling "+input_ui_file
        f=open(output_path,"w")
        PyQt4.uic.compileUi(input_path,f)
        f.close()    

compile_if_necessary("Graphical_User_Interface.ui","GUI_compiled.py")
#Widget for a pyqtgraph PlotWidget with several control buttons
compile_if_necessary("Plot2DDataWidget.ui","Plot2DDataWidget_Ui.py")
#Widget for a table with three columns and two buttons to add or remove lines
compile_if_necessary("TableWith2Buttons.ui","TableWith2Buttons_Ui.py")
#Widget for a table with four columns and two buttons to add or remove lines
compile_if_necessary("TableWith2Buttons4Col.ui","TableWith2Buttons4Col_Ui.py")
#Widget for the main configuration menu of PygMI
compile_if_necessary("Config_menu.ui","Config_menu_Ui.py")
#Widget to set-up the connection to the instruments
compile_if_necessary("Instruments_connection.ui","Instruments_connection_Ui.py")
#Widget which handles the macro
compile_if_necessary("Macro_editor.ui","Macro_editor_Ui.py")

