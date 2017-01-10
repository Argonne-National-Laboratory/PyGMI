# -*- coding: utf-8 -*-
import visa
import time
import numpy as np

class Connect_Instrument():
    def __init__(self,VISA_address='USB0::0x0699::0x03A6::c019476::0', factory_settings=True):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        self.my_instr_name='Tektronix_TDS2024C'
        if factory_settings:        
            #start from a known state (there are so many options to check otherwise)
            print "resetting "+self.my_instr_name+" to factory default configuration..."
            self.io.write('FACTORY')
            time.sleep(10) #the reset takes a long time
        #binary encoding would be faster to transmit but require a little more work to decode the data
        self.io.write('data:encdg ascii') 
        try:
            print self.query_unit_Id()
        except:
            print "Instrument "+self.my_instr_name+" at visa address: "+VISA_address+", did not answer to identification request"

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def trigger_coupling(self,t):
        if t in ['AC','DC','HFRej','LFRej','NOISErej']:
            self.io.write('TRIGger:MAIn:EDGE:COUPling '+t)

    def trigger_slope(self,txt):
        if txt in ['FALL','RISe']:
            self.io.write('TRIGger:MAIn:EDGE:SLOpe '+txt)
            
    def trigger_source(self,txt):
        if txt in ['CH1','CH2','CH3','CH4','EXT','EXT5','EXT10','AC','LINE']:
            self.io.write('TRIGger:MAIn:EDGE:SOUrce '+txt)

    def trigger_level(self,volts):
        """Set the main trigger level, in volts"""
        self.io.write('TRIGger:MAIn:LEVel '+str(float(volts)))

    def measuring_channel(self,chan):
        if chan in [1,2,3,4]:
            self.io.write('DATa:SOUrce CH'+str(chan))
        elif chan=='math':
            self.io.write('DATa:SOUrce math')

    def acquire_curve(self,channel=None):
        """return the curve points of the currently selected channel, or of the one specified in argument"""
        if channel!=None:
            self.measuring_channel(channel)
        def my_stripper(cmd):
            txt=self.io.query(cmd)
            return float(txt[txt.index(' ')+1:])
        Xincr=my_stripper('WFMPre:XINcr?')
        
        YMUlt=my_stripper('WFMPre:YMUlt?')
        YOFF_in_dl=my_stripper('WFMPre:YOFf?')
        YZERO_in_YUNits=my_stripper('WFMPre:YZEro?')

        txt=self.io.query('CURVE?')
        #datapoints in digitizer levels
        curve_in_dl=np.array(map(float,txt[txt.index(' ')+1:].split(',')))
        #conversion of the data to something meaningful (in Yunits: Volts or dB)
        value_in_YUNits = ((curve_in_dl - YOFF_in_dl) * YMUlt) + YZERO_in_YUNits

        x=np.arange(0,len(value_in_YUNits)*Xincr,Xincr)
        y=value_in_YUNits
        
        return x,y
    
