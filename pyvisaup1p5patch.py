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

import os

rep = r'./PyGMI'
for root,dirs,files in os.walk(rep):
    for myfile in files:
        needupdate = False
        if myfile[-3:]=='.py' and 'pyvisaup1p5patch' not in myfile:
            f = open(root+os.sep+myfile,'r')
            txt = f.readlines()
            for i,line in enumerate(txt):
                if "visa.instrument(" in line:
                    line = line.replace("visa.instrument(","visa.ResourceManager().open_resource(")
                    print myfile,"line",i,"visa.instrument("
                    needupdate = True
                if ".ask(" in line:
                    line = line.replace(".ask(",".query(")
                    print myfile,"line",i,".ask("
                    needupdate = True
                if ".term_chars" in line:
                    line = line.replace(".term_chars",".read_termination")
                    print myfile,"line",i,".term_chars"
                    needupdate = True
                if "timeout" in line:
                    print "WARNING: 'timeout' detected in",myfile
                    print "timeout must be in milliseconds for PyVisa > 1.5"
                    print line
                if 'visa.get_instruments_list()' in line:
                    line = line.replace('visa.get_instruments_list()','visa.ResourceManager().list_resources()')
                    print myfile,"line",i,'.get_instruments_list()'
                    needupdate = True
                txt[i] = line
            f.close()
            if needupdate:
                f = open(root+os.sep+myfile,'w')
                f.write("".join(txt))
                f.close()
                print ">>> successfully patched",myfile
                print ""