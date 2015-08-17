#this file is launched at start-up when importing PyGMI

print "Launching the User Interface"

#this file is launched at start-up when importing PyGMI
#import the graphical design of the User interface,
#and (re)compile it if necessary
import os
execfile('PyGMI_files'+os.sep+'GUI_Compiler.py')
#import GUI_Compiler


#import the main control of the User interface
import Main 

#make a shortcut name to GUI_instance in order to make the import
#of the package more intuitive, that is:
#       window = PyGMI.start_GUI()
#instead of :
#       window = PyGMI.Main.start_GUI()
start_GUI = Main.start_GUI

