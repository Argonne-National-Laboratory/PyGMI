# -*- coding: utf-8 -*-
import visa
import time

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::17"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print(self.io.query("*IDN?"))
        sens_list_utf8=['10 mV','100 mV','1 V','10 V','100 V']
        self.sens_list_num=[0.01,0.1,1,10,100]
        self.sensitivity=[]
        for txt in sens_list_utf8:
            self.sensitivity.append(str(txt))

    def initialize(self):
        """commands executed when the instrument is initialized"""
        self.reset_and_query_voltage()
        self.io.write(':SYSTem:LSYNc:STATe ON')
        self.set_integration_rate(3)
        #self.setup_single_shot_Tlink()

    def reset_autozero(self,duration=1):
        self.io.write(':SYSTem:AZERo:STATe ON')
        self.io.write(':syst:faz ON')
        time.sleep(duration)
        self.io.write(':syst:faz off')
        self.io.write(':SYSTem:AZERo:STATe OFF')

    def conf_channel2(self):
        lnanoV=[':SENS:CHAN 2',':CONF:VOLT',':INIT:CONT OFF']
        for txt in lnanoV:
            self.io.write(txt)

    def switch_channel(self,chan=1):
        self.io.write(':SENS:CHAN '+str(chan))

    def setup_single_shot(self,verbose=False):
        print("configuring Keithley2182A for continuously taking low speed single shot readings")
        lnanoV=[':syst:pres', # 2182 - System preset defaults.
                ':CONF:VOLT',
                ':INIT:CONT OFF']
        for txt in lnanoV:
            if verbose:
                print(txt)
            self.io.write(txt)

    def setup_single_shot_Tlink(self,verbose=False):
        print("configuring Keithley2182A for a single shot with trigger link cable")
        lnanoV=[':syst:pres', # 2182 - System preset defaults.
                ':CONF:VOLT',
                ':SENSe:VOLTage:DC:RANGe 0.0001',
                ':SENSe:VOLTage:DC:LPASs OFF',
                ':SENSe:VOLTage:DC:DFILter OFF',
                ':TRIG:DEL:AUTO OFF',
                ':trig:del 0',
                ':SENS:VOLT:NPLC 0.1',
                ':DISPlay:ENABle ON',
                #':sens:volt:delta on',
                ':syst:faz off',
                ':SYSTem:AZERo:STATe OFF',
                ':trig:sour ext',
                #':trac:poin '+buff_pts,
                ':SYSTem:LSYNc:STATe ON',
                #':trac:feed:cont next',
                ':trig:coun inf',
                ':SAMP:COUN 1',
                ':INIT']

        for txt in lnanoV:
            if verbose:
                print(txt)
            self.io.write(txt)
        time.sleep(1) #init needs at least one second to complete

    def setup_sensitivity_combobox(self,comboBox):
        comboBox.clear()
        comboBox.addItems(self.sensitivity)

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def reset_and_query_voltage(self):
        """This query is much slower than a “:READ?” or “:FETCh?” query"""
        return float(self.io.query(":MEAS:VOLT?"))

    def query_voltage(self):
        return float(self.io.query(":READ?"))

    def query_latest_reading(self):
        """This command does not trigger a measurement. The command simply requests the last
available reading."""
        return float(self.io.query(':FETCh?'))

    def query_latest_fresh_reading(self):
        """This query is similar to the “:FETCh?” in that it returns the latest reading from the instrument,
but has the advantage of making sure that it does not return the same reading twice."""
        return float(self.io.query(':sens:data:fresh?'))

    def select_channel(self,chan):
        self.io.write(':SENS:CHAN '+str(chan))

#Select channel to measure; 0, 1 or 2 (0 = internal temperature sensor).

    def output_terminals(self,side):
        if side=='rear':
            self.io.write(':ROUT:TERM REAR')
        elif side=='front':
            self.io.write(':ROUT:TERM FRON')


    def output_ON(self):
        self.io.write(':OUTP 1')

    def output_OFF(self):
        self.io.write(':OUTP 0')

    def current_source_range(self,RANGe):
        self.io.write(':SOUR:CURR:RANG '+str(RANGe))

    def voltage_source_range(self,RANGe):
        self.io.write(':SOUR:CURR:RANG '+str(RANGe))

    def set_integration_rate(self,NPLC):
        self.io.write(':SENS:VOLT:NPLC '+str(NPLC))

    def set_sensitivity(self,RANGE):
        self.io.write(':SENS:VOLT:RANG '+str(RANGE))
