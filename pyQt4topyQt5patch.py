# -*- coding: utf-8 -*-
##Copyright © 2014 , UChicago Argonne, LLC
##All Rights Reserved
## Python Generic Measurement Interface
##OPEN SOURCE LICENSE
##
##Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
##
##1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.  Software changes, modifications, or derivative works, should be noted with comments and the author and organization’s name.
##
##2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
##
##3. Neither the names of UChicago Argonne, LLC or the Department of Energy nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
##
##4. The software and the end-user documentation included with the redistribution, if any, must include the following acknowledgment:
##
##   "This product includes software produced by UChicago Argonne, LLC under Contract No. DE-AC02-06CH11357 with the Department of Energy.”
##
##******************************************************************************************************
##DISCLAIMER
##
##THE SOFTWARE IS SUPPLIED "AS IS" WITHOUT WARRANTY OF ANY KIND.
##
##NEITHER THE UNITED STATES GOVERNMENT, NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR UCHICAGO ARGONNE, LLC, NOR ANY OF THEIR EMPLOYEES, NOR MAXIME LEROUX, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, DATA, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS.
##
##***************************************************************************************************
##


"""
A tentative patch to make the pyQt4-compatible version of PyGMI compatible
with pyQt5. It will ask for permission before making changes to PyGMI files.
"""

import os
import re

# True will bypass all request
bypass = False

def ischangeOK(oline, nline):
    global bypass
    if bypass: shall = True
    else:
        msg = 'Replace\n> '+oline+'\nby\n> '+nline+'\n?'
        ans = input("%s ([y]es/ [n]o / yes to [a]ll) " % msg).lower()
        bypass = ans == 'a'
        shall = (ans == 'y') or bypass
    return shall

rep = os.getcwd()

replacements = {'PyQt4.uic.compileUi' : 'PyQt5.uic.compileUi',
                'import PyQt4.uic' : 'import PyQt5.uic',
                "(self,fileName=None)" : "(self,checked=False,fileName=None)",
                '.saveInstrconf("' : '.saveInstrconf(fileName="',
                '.loadInstrconf("' : '.loadInstrconf(fileName="',
                '.loadconf("' : '.loadconf(fileName="',
                '.saveconf("' : '.saveconf(fileName="',
                "from PyQt4.QtCore" : "from PyQt5.QtCore",
                ",SIGNAL" : "",
                "fileName = QFileDialog.getOpenFileName" : "fileName, _ = QFileDialog.getOpenFileName",
                "fileName = QFileDialog.getSaveFileName" : "fileName, _ = QFileDialog.getSaveFileName",
                r"INSTRTYPE_COMBOBOXES=re.findall(r'self\.(\w+_instrtype(?:_\d+)?) = QtGui\.QComboBox" : r"INSTRTYPE_COMBOBOXES=re.findall(r'self\.(\w+_instrtype(?:_\d+)?) = QtWidgets\.QComboBox"
                }

# regular expression matching pattern to get PyQt4.QtGui imports
importpattern = re.compile(r'from PyQt4.QtGui import (?P<classes>(?:\w*,?)*)')

# new separation of classes
Qt5QtWidget = ['QWidget','QApplication','QFileDialog',
               'QDialog','QColorDialog','QColorDialog','QTableWidgetItem',
               'QPlainTextEdit','QMainWindow']

Qt5QtGui = ['QColor','QSyntaxHighlighter','QTextCharFormat',
            'QFont','QStandardItemModel','QStandardItem']

for root, dirs, files in os.walk(rep):
    for myfile in files:
        needupdate = False
        if myfile[-3:] == '.py' and 'pyQt4topyQt5patch' not in myfile:
            with open(root+os.sep+myfile,'r',encoding='utf-8') as f:
                txt = f.readlines()
                print(">>> Checking ", myfile)
                for i, line in enumerate(txt):
                    for key in list(replacements.keys()):
                        if key in line:
                            newline = line.replace(key,replacements[key])
                            if ischangeOK(line,newline):
                                print("line",i,"updated")
                                if bypass:print(line, '>', newline)
                                line = newline
                                needupdate = True

                    # logic to separate Qt classes according to their new import
                    match = importpattern.search(line)
                    if match is not None:
                        class_list = match.group('classes').split(',')
                        Qt5QtWidgetclasses = []
                        Qt5QtGuiclasses = []
                        for thisclass in class_list:
                            if thisclass in Qt5QtWidget:
                                Qt5QtWidgetclasses.append(thisclass)
                            elif thisclass in Qt5QtGui:
                                Qt5QtGuiclasses.append(thisclass)
                            else:
                                print("Error: unknown class")
                        newline = ""
                        if len(Qt5QtWidgetclasses)>0:
                            newline+="from PyQt5.QtWidgets import "+",".join(Qt5QtWidgetclasses)+'\n'
                        if len(Qt5QtGuiclasses)>0:
                            newline+="from PyQt5.QtGui import "+",".join(Qt5QtGuiclasses)+'\n'
                        if ischangeOK(line,newline):
                                print("line",i,"updated")
                                if bypass:print(line, '>', newline)
                                line = newline
                                needupdate = True
                    txt[i] = line

            if needupdate:
                with open(root+os.sep+myfile, encoding='utf-8', mode="w") as f:
                    f.write("".join(txt))
                print(">>>>>> successfully patched",myfile)
                print("")
            else:
                print(">>>>>> no changes needed in",myfile)

print("Force recompile all main GUI files")

import PyQt5.uic
def forcecompile(folder,input_ui_file,output_py_file):
    #prepare the file names
    input_path = folder+os.sep+input_ui_file
    output_path = folder+os.sep+output_py_file
    #recompile the .ui Qt file
    with open(output_path, encoding='utf-8', mode="w") as outf:
        print("recompiling ", input_ui_file)
        PyQt5.uic.compileUi(input_path, outf)

mainfilesrep = rep+os.sep+'PyGMI_files'
forcecompile(mainfilesrep,"Graphical_User_Interface.ui",
                          "Graphical_User_Interface_Ui.py")
#Widget for a pyqtgraph PlotWidget with several control buttons
forcecompile(mainfilesrep,"Plot2DDataWidget.ui",
                          "Plot2DDataWidget_Ui.py")
#Widget for a table with three columns and two buttons to add or remove lines
forcecompile(mainfilesrep,"TableWith2Buttons.ui",
                          "TableWith2Buttons_Ui.py")
#Widget for a table with four columns and two buttons to add or remove lines
forcecompile(mainfilesrep,"TableWith2Buttons4Col.ui",
                          "TableWith2Buttons4Col_Ui.py")
#Widget for the main configuration menu of PygMI
forcecompile(mainfilesrep,"Config_menu.ui",
                          "Config_menu_Ui.py")
#Widget to set-up the connection to the instruments
forcecompile(mainfilesrep,"Instruments_connection.ui",
                          "Instruments_connection_Ui.py")
#Widget which handles the macro
forcecompile(mainfilesrep,"Macro_editor.ui",
                          "Macro_editor_Ui.py")

print("Force recompile all instruments panels GUI files")

instrpanelrep = rep+os.sep+'PyGMI_files'+os.sep+'Instruments_panels'
for my_file in os.listdir(instrpanelrep):
    if '.ui' in my_file:
        forcecompile(instrpanelrep,my_file,my_file[:-3]+'_Ui.py')

