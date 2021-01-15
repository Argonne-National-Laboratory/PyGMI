# -*- coding: utf-8 -*-
import visa
import time
import numpy as np

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::17"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print(self.io.query("*IDN?"))

    def initialize(self):
        """commands executed when the instrument is initialized"""
        self.set_current_source_amplitude(0.0)
        #self.current_source_range_auto()
        #self.set_voltage_compliance(20)
        self.output_ON()

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def reset(self):
        self.io.write('*RST')

    def output_ON(self):
        self.io.write('OUTP ON')

    def output_OFF(self):
        self.io.write('OUTP OFF')

    def query_output_ON(self):
        if self.io.query('OUTP?')=='1':
            return True
        else:
            return False

    def current_source_range(self,RANGe):
        self.io.write('CURR:RANG '+str(RANGe))

    def query_current_source_range(self):
        return float(self.io.query('curr:rang?'))

    def current_source_range_auto(self):
        self.io.write('CURRent:RANGe:AUTO ON')

    def set_current_source_amplitude(self,amp):
        self.io.write('CURR '+str(amp))

    def query_current_source_amplitude(self):
        return float(self.io.query('curr?'))

    def set_voltage_compliance(self,voltage):
        self.io.write('CURRent:COMPliance '+str(voltage))#despite the command name 'CURRent', it really does set the voltage compliance

    def query_voltage_compliance(self):
        return float(self.io.query('curr:comp?'))

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
        return float(self.io.query(':sens:data:fresh?').split(',')[0])

    def query_latest_reading(self):
        return float(self.io.query(':sens:data:lat?').split(',')[0])

    def setup_delta_Tlink_inf(self,verbose=False):
        print("configuring Keithley6221 series for delta mode")
        self.output_OFF()
        #self.current_source_range(0.03)
        #self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*RST'] #Restores 622x defaults.

        for txt in ldcSource:
            if verbose:
                print(txt)
            self.io.write(txt)
        time.sleep(1)


    def setup_delta_Tlink(self,I=1e-6,count=10,I_delay=2e-3,verbose=False):
        print("configuring Keithley6221 series for pulsed mode")
        self.output_OFF()
        #self.current_source_range(0.03)
        #self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*RST', # Restores 622x defaults.
                   'SOUR:DELT:HIGH '+str(I),# Sets high source value to 1mA.
                   'SOUR:DELT:COUN '+str(count), # Sets Delta count to 10
                   'TRAC:POIN '+str(count), # Sets buffer to 10 points
                   'FORM:ELEM READ', # Specify data elements for TRACe:DATA? response. <list> = READing, TSTamp, UNITs, RNUMber, SOURce, COMPliance, AVOLtage. Also accepts DEFault or ALL
                   'SOUR:DELT:DELay '+str(I_delay), # Sets Delta delay to 2ms.
                   'SOUR:DELT:CAB ON', # Enables Compliance Abort.
                   'SOUR:DELT:ARM'] # Arms Delta.

        for txt in ldcSource:
            if verbose:
                print(txt)
            self.io.write(txt)
        time.sleep(1)

    def switch_channel_delta(self,chan=1):
            self.io.write('SYST:COMM:SER:SEND ":SENS:CHAN '+str(chan)+'"')

    def set_integration_rate_delta(self,NPLC):
        self.io.write('SYST:COMM:SER:SEND "VOLT:NPLC '+str(int(NPLC))+'"')

    def start_delta(self):
        self.io.write('INIT:IMM') # Starts Delta measurements.

    def query_delta_readings(self,nb_of_pts=None,waitime=10e-3):
        if nb_of_pts is None:
            return self.io.query_ascii_values('TRAC:DATA?')
        else:
            while int(self.io.query('TRAC:POIN:ACT?'))!=nb_of_pts:
                time.sleep(waitime)
            return self.io.query_ascii_values('TRAC:DATA?')

    def query_delta_readings_as_numpy(self,nb_of_pts=None,waitime=10e-3):
        if nb_of_pts is None:
            return self.io.query_ascii_values('TRAC:DATA?', container=np.array)
        else:
            while int(self.io.query('TRAC:POIN:ACT?'))!=nb_of_pts:
                time.sleep(waitime)
            return self.io.query_ascii_values('TRAC:DATA?', container=np.array)

    def unarm_delta(self):
        self.io.write('SOUR:SWE:ABOR')
