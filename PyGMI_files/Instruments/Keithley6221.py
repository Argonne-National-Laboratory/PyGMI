# -*- coding: utf-8 -*-
import visa
import time

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::17"):
        self.io = visa.instrument(VISA_address)
        print self.io.ask("*IDN?")
    
    def initialize(self):
        """commands executed when the instrument is initialized"""
        self.set_current_source_amplitude(0.0)
        #self.current_source_range_auto()
        #self.set_voltage_compliance(20)
        self.output_ON()
    
    def query_unit_Id(self):
        return self.io.ask("*IDN?")

    def reset(self):
        self.io.write('*RST')
        
    def output_ON(self):
        self.io.write('OUTP ON')
    
    def output_OFF(self):
        self.io.write('OUTP OFF')

    def query_output_ON(self):
        if self.io.ask('OUTP?')=='1':
            return True
        else:
            return False
        
    def current_source_range(self,RANGe):
        self.io.write('CURR:RANG '+str(RANGe))

    def query_current_source_range(self):
        return float(self.io.ask('curr:rang?'))
        
    def current_source_range_auto(self):
        self.io.write('CURRent:RANGe:AUTO ON')

    def set_current_source_amplitude(self,amp):
        self.io.write('CURR '+str(amp))

    def query_current_source_amplitude(self):
        return float(self.io.ask('curr?'))
        
    def set_voltage_compliance(self,voltage):
        self.io.write('CURRent:COMPliance '+str(voltage))#despite the command name 'CURRent', it really does set the voltage compliance

    def query_voltage_compliance(self):
        return float(self.io.ask('curr:comp?'))

    def set_high_source_delta(self,amp):
        self.io.write('SOUR:DELT:HIGH '+str(amp)) #Sets high source value to X Amp (low source is automatically -high)

    def disarm_delta(self):
        self.io.write('SOURce:SWEep:ABORt')
        
    def arm_delta(self):
        self.io.write('SOUR:DELT:ARM')

    def set_delta_delay(self,secs):
        self.io.write('SOUR:DELT:DELay '+str(secs)) #Sets Delta delay to X secs. 

    def start_delta_cycle(self):
        self.io.write('INIT:IMM') #Starts Delta measurements.

    def query_latest_fresh_reading(self):
        """The SENS:DATA:FRESh? command is the same as the SENS:DATA:LATest?
command except that once a reading is returned, it cannot be returned again. This
read command guarantees that each reading gets returned only once. If a new
(fresh) reading is not available when SENS:DATA:FRESh? is sent, error -230 Data
corrupt or stale will occur."""
        return float(self.io.ask(':sens:data:fresh?').split(',')[0])

    def query_latest_reading(self):
        """The SENS:DATA:FRESh? command is the same as the SENS:DATA:LATest?
command except that once a reading is returned, it cannot be returned again. This
read command guarantees that each reading gets returned only once. If a new
(fresh) reading is not available when SENS:DATA:FRESh? is sent, error -230 Data
corrupt or stale will occur."""
        return float(self.io.ask(':sens:data:lat?').split(',')[0])
        
    def setup_delta_Tlink_inf(self,verbose=False):
        print "configuring Keithley6221 series for delta mode"
        self.output_OFF()
        #self.current_source_range(0.03)
        #self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*RST'] #Restores 622x defaults.
                                   
        for txt in ldcSource:
            if verbose:
                print txt
            self.io.write(txt)
        time.sleep(1)
    
        
    def setup_delta_Tlink(self,verbose=False):
        print "configuring Keithley6221 series for pulsed mode"
        self.output_OFF()
        #self.current_source_range(0.03)
        #self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*RST', #Restores 622x defaults.
                   'SOUR:DELT:COUN 1', #Sets Delta count to 1.
                   'SOUR:DELT:CAB ON'] #Enables Compliance Abort.
 
                   
        for txt in ldcSource:
            if verbose:
                print txt
            self.io.write(txt)
        time.sleep(1)
