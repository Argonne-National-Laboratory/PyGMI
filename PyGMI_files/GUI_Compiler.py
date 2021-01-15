"""
This module recompile the GUI if the .ui file
is more recent than the compiled .py file
"""
import os
import PyQt5.uic

if __name__ == '__main__':
    #The program was launched as a script,
    #so there is nothing to do, because the
    #current working directory is already set
    #to the directory of this script
    REP_MODULE = ''
else:
    #The program was launched as a module.
    #Get the module directory name from __file__
    #which contains the absolute path of the file
    #being executed
    REP_MODULE = os.path.dirname(__file__)+os.sep

def compile_if_necessary(input_ui_file, output_py_file):
    """
    recompile the .ui Qt file if this script is launched directly
    or if the compiled .py GUI file does not exist
    or if it is more recent than the compiled .py GUI file
    """
    #prepare the file names
    input_path = REP_MODULE+input_ui_file
    output_path = REP_MODULE+output_py_file
    if not(os.path.isfile(output_path))\
     or os.path.getmtime(input_path) > os.path.getmtime(output_path):
        # need to specify utf8 or it assumes ascii by default and then e.g.
        # it cannot write grrek letter symbols that are in the .ui file
        with open(output_path, encoding='utf-8', mode="w") as outf:
            print("update detected: recompiling "+input_ui_file)
            PyQt5.uic.compileUi(input_path, outf)
            # there seems to be a problem with relative imports and compileUI
            # it used to work but does not anymore as of 8/2/18
            # Graphical_User_Interface_Ui should have a few import statements
            # such as: from .MODULE import CLASSNAME
            # but somehow it does not put the '.' before MODULE now
            # HACK: add the '.' in the name of the headerfile in the .ui
            # from_imports=True,import_from='.'



compile_if_necessary("Graphical_User_Interface.ui",
                     "Graphical_User_Interface_Ui.py")
#Widget for a pyqtgraph PlotWidget with several control buttons
compile_if_necessary("Plot2DDataWidget.ui",
                     "Plot2DDataWidget_Ui.py")
#Widget for a table with three columns and two buttons to add or remove lines
compile_if_necessary("TableWith2Buttons.ui",
                     "TableWith2Buttons_Ui.py")
#Widget for a table with four columns and two buttons to add or remove lines
compile_if_necessary("TableWith2Buttons4Col.ui",
                     "TableWith2Buttons4Col_Ui.py")
#Widget for the main configuration menu of PygMI
compile_if_necessary("Config_menu.ui",
                     "Config_menu_Ui.py")
#Widget to set-up the connection to the instruments
compile_if_necessary("Instruments_connection.ui",
                     "Instruments_connection_Ui.py")
#Widget which handles the macro
compile_if_necessary("Macro_editor.ui",
                     "Macro_editor_Ui.py")
