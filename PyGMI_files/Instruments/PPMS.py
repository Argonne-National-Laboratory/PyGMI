# -*- coding: utf-8 -*-
"""
Created on Mon May 23 13:25:29 2016

@author: 308791
"""

#!/usr/bin/env python
#The ctypes library includes datatypes for passing data to DLLs
#For instance, c_int to pass integer pointers
import ctypes
import os
import re
import time
import subprocess
print __file__
module_folder = os.path.dirname(__file__)
configmatch = re.compile(r"remote=(?P<rem>True|False);ip=(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3});insttype=(?P<insttype>PPMS|VersaLab|DynaCool|SVSM)")

# Retry decorator with return
def retry_with(tries=2,default_ans=(True,),wait=15):
#    Retries a function until it does not raise an exception or error.
#    It also tries to restart MultiVu if it cannot find it running
#    but it appears the DLL functions already do that by themselves
#    If it runs out of tries, a default answer is returned.
    def deco(f):
        def f_retry(*args, **kwargs):
            mtries = tries # make mutable
            errorstatus = True
            while mtries >0 and errorstatus:
                try:
                    ans = f(*args, **kwargs) # first attempt
                    errorstatus = ans[0]
                except:
                    print 'exception in ',f.func_name
                    errorstatus = True
                if errorstatus:
                    print 'Error detected, checking Multivu...'                    
                    mtries -= 1      # consume an attempt                    
                    listproc = subprocess.check_output("tasklist")
                    if 'PpmsMVu.exe' not in listproc:
                        # not really necessary as it appears the DLL 
                        # will do it by itself
                        print 'Multivu not running, restarting it now'
                        subprocess.Popen(["C:\\QdPpms\\MultiVu\\PpmsMVu.exe","-macro"])                        
                    else:
                        print 'Multivu already running'
                    print 'waiting '+str(wait)+' secs before querying Multivu again'
                    time.sleep(wait)
            if not(errorstatus):
                res = ans
            else:
                print "exception in", f.func_name,"ran out of retries"
                res = default_ans # Ran out of tries :-(
            return res
        return f_retry # true decorator -> decorated function
    return deco
    
    
class Connect_Instrument(object):
    def __init__(self, config_line='remote=False;ip=127.0.0.1;insttype=PPMS'):
        match = configmatch.search(config_line)
        if match is None:
            print 'address line for QD PPMS or similar must follow this format'
            print 'remote=False;ip=127.0.0.1;insttype=PPMS'
            print 'please correct and retry instruments initialization'
        else:
            if match.group('rem')=='True':
                remote = True
            else:
                remote = False
            ip_address=match.group('ip')
            insttype=match.group('insttype')
            
            instdict = {'PPMS':0,
                        'VersaLab':1,
                        'DynaCool':2,
                        'SVSM':3}
            self.t_apprdict = {'FastSettle':0,
                               'NoOvershoot':1}
            self.t_statdict = {0:'TemperatureUnknown',
                               1:'Stable',
                               2:'Tracking',
                               5:'Near',
                               6:'Chasing',
                               7:'Filling',
                               10:'Standby',
                               13:'Disabled',
                               14:'ImpedanceNotFunction',
                               15:'TempFailure'}
            self.h_statdict = {0:'MagnetUnkown',
                               1:'StablePersistent',
                               2:'WarmingSwitch',
                               3:'CoolingSwitch',
                               4:'StableDriven',
                               5:'Iterating',
                               6:'Charging',
                               7:'Discharging',
                               8:'CurrentError',
                               15:'MagnetFailure'}
            self.h_apprdict = {'Linear':0,
                               'NoOvershoot':1,
                               'Oscillate':2}
            self.h_mode = {'Persistent':0,
                           'Driven':1}
            self.a_mode = {'Move to position':0,
                           'Move to limit':1, 
                           'Redefine current position':2,
                           "":3}
            self.ppmsdll = ctypes.cdll.LoadLibrary(module_folder+os.sep+r"MyPPMSDLL/MyPPMSDLL.dll")
            #pass pointers using the byref keyword        
            self.ip = ctypes.byref(ctypes.create_string_buffer(ip_address,len(ip_address)))
            self.rem = ctypes.c_bool(remote)
            self.insttype = ctypes.c_int32(instdict[insttype])
            
    def initialize(self):
        """commands executed when the instrument is initialized"""
        pass
    
    @retry_with(tries=2,default_ans=(True,1e99,'MagnetUnkown'),wait=15)
    def get_field(self):
        #Function Prototype:
#void __cdecl PPMSGetField(char IPAddress[], LVBoolean Remote, 
#	int32_t InstrumentType, double *Field, int32_t *FieldStatus, 
#	LVBoolean *Errorstatus, int32_t *Errorcode);
        FieldStatus = ctypes.c_int32()
        # in Oe
        Field = ctypes.c_double()
        # error management
        Errorstatus = ctypes.c_bool()
        Errorcode = ctypes.c_int32()      
        #Call the Function
        self.ppmsdll.PPMSGetField(self.ip,self.rem,
                                  self.insttype,ctypes.byref(Field),ctypes.byref(FieldStatus),
                                  ctypes.byref(Errorstatus),ctypes.byref(Errorcode))
        return (Errorstatus.value,Field.value,self.h_statdict[FieldStatus.value])
    
    @retry_with(tries=2,default_ans=(True,1e99,'TemperatureUnknown'),wait=15)
    def get_temperature(self):
        #Function Prototype:
#void __cdecl PPMSGetTemp(char IPAddress[], LVBoolean Remote, 
#	int32_t InstrumentType, double *Temperature, int32_t *TemperatureStatus, 
#	LVBoolean *Errorstatus, int32_t *Errorcode);
        TemperatureStatus = ctypes.c_int32()
        # in K
        Temperature = ctypes.c_double()
        # error management
        Errorstatus = ctypes.c_bool()
        Errorcode = ctypes.c_int32() 
        #Call the Function
        self.ppmsdll.PPMSGetTemp(self.ip,self.rem,
                                 self.insttype,ctypes.byref(Temperature),ctypes.byref(TemperatureStatus),
                                  ctypes.byref(Errorstatus),ctypes.byref(Errorcode))
        return (Errorstatus.value,Temperature.value,self.t_statdict[TemperatureStatus.value])

    @retry_with()
    def set_field(self, H, rate, approach='Linear', mode='Persistent'):
        #Function Prototype:
#void __cdecl PPMSSetField(char IPAddress[], LVBoolean Remote, 
#	int32_t InstrumentType, double Field, double Rate, int32_t Approach, 
#	int32_t Mode, LVBoolean *Errorstatus, int32_t *Errorcode);
        Approach = ctypes.c_int32(self.h_apprdict[approach])
        Mode = ctypes.c_int32(self.h_mode[mode])
        # in Oe/s
        Rate = ctypes.c_double(rate)
        # in Oe
        Field = ctypes.c_double(H)
        # error management
        Errorstatus = ctypes.c_bool()
        Errorcode = ctypes.c_int32() 
        #Call the Function
        self.ppmsdll.PPMSSetField(self.ip,self.rem,
                                 self.insttype,Field,Rate,Approach,
                                 Mode,ctypes.byref(Errorstatus),ctypes.byref(Errorcode))
        return (Errorstatus.value,)

    @retry_with()
    def set_temperature(self, T, rate, approach='FastSettle'):
        #Function Prototype:
#void __cdecl PPMSSetTemp(char IPAddress[], LVBoolean Remote, 
#	int32_t InstrumentType, double Temperature, double Rate, int32_t Approach, 
#	LVBoolean *Errorstatus, int32_t *Errorcode);
        a = ctypes.c_int32(self.t_apprdict[approach])
        # in K/min
        r = ctypes.c_double(rate)
        # in K
        t = ctypes.c_double(T)
        # error management
        Errorstatus = ctypes.c_bool()
        Errorcode = ctypes.c_int32() 
        #Call the Function
        self.ppmsdll.PPMSSetTemp(self.ip,self.rem,
                                 self.insttype,t,r,a,
                                 ctypes.byref(Errorstatus),ctypes.byref(Errorcode))
        return (Errorstatus.value,)
    
    @retry_with()
    def wait_for(self,Temperature=False,Field=False,Chamber=False,Position=False):
#void __cdecl PPMSWaitFor(char IPAddress[], LVBoolean Remote, 
#	int32_t InstrumentType, LVBoolean WaitForTemperature, LVBoolean WaitForField, 
#	LVBoolean WaitForChamber, LVBoolean WaitForPosition, LVBoolean *Errorstatus, 
#	int32_t *Errorcode);
        t = ctypes.c_bool(Temperature)
        f = ctypes.c_bool(Field)
        c = ctypes.c_bool(Chamber)
        p = ctypes.c_bool(Position)
        # error management
        Errorstatus = ctypes.c_bool()
        Errorcode = ctypes.c_int32() 
        #Call the Function
        self.ppmsdll.PPMSSetTemp(self.ip,self.rem,
                                 self.insttype,t,f,
                                 c,p,ctypes.byref(Errorstatus),
                                 ctypes.byref(Errorcode))
        return (Errorstatus.value,)