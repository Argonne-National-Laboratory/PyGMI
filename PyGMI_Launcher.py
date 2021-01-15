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


import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
import PyGMI_files as PyGMI

# get reference to the running QApplication (if any, otherwise return None)
app = QCoreApplication.instance()

def main():
    newapp = False
    global app
    if app is None:
        # no running QApplication, starts one
        # and pass it the command line arguments
        newapp = True
        app = QApplication(sys.argv)
    app.references = set()
    # create the Graphical User Interface main window
    window = PyGMI.start_GUI()
    app.references.add(window)
    window.show()
    # if a QApplication was just created
    # launch the Qt event manager through "app.exec()" (no more sys.exit)
    if newapp: app.exec()

if __name__ == '__main__':
    main()