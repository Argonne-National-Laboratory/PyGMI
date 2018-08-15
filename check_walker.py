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
"""
Script that walks through PyGMI folders to find specified strings in code

"""

find = ["encoding","encode"]

rep = os.getcwd()

for root,dirs,files in os.walk(rep):
    for myfile in files:
        if myfile[-3:]=='.py' and 'pyvisaup1p5patch' not in myfile:
            with open(root+os.sep+myfile,'r',encoding='utf-8') as f:
#                print(myfile)
                txt = f.readlines()
                for i,line in enumerate(txt):
                    for word in find:
                        if word in line:
                            print("found",word,"in",root+os.sep+myfile)
                            print("line",i,":",line)

